import assert from "node:assert/strict";
import { access, readFile, stat } from "node:fs/promises";
import { join } from "node:path";
import { test } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parse } from "yaml";

const SKILL_NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const MAX_ICON_BYTES = 256 * 1024;
const distribution = JSON.parse(await readFile(new URL("../distribution.json", import.meta.url), "utf8"));
const collections = distribution.plugins;

for (const { name: collection, source, npm_name: npmName, display_name: displayName, description } of collections) {
  test(`${collection} ships valid DeepSeek Harness bundle metadata and skill provider`, async () => {
    const base = new URL(`../plugins/${collection}/`, import.meta.url);
    const pkg = JSON.parse(await readFile(new URL("package.json", base), "utf8"));
    assert.equal(pkg.name, npmName);
    assert.deepEqual(pkg.dsh, { bundle: { patch: "./cordis.patch.yml" } });
    assert.equal(pkg.engines?.dsh, undefined);
    assert.equal(pkg.peerDependencies, undefined);
    assert.equal(pkg.icon, "./assets/logo.svg");
    const iconStat = await stat(new URL(pkg.icon, base));
    assert.ok(iconStat.isFile() && iconStat.size > 0 && iconStat.size <= MAX_ICON_BYTES);

    const locale = JSON.parse(await readFile(new URL("locale/en.json", base), "utf8"));
    assert.deepEqual(locale, { meta: { title: displayName, description } });

    const patch = parse(await readFile(new URL("cordis.patch.yml", base), "utf8"));
    assert.deepEqual(patch, [
      {
        insert: [
          {
            id: `skill-${collection}`,
            name: `${npmName}/dsh`,
          },
        ],
      },
    ]);

    assert.equal(import.meta.resolve(`${npmName}/dsh`), new URL("dsh.mjs", base).href);
    assert.equal(import.meta.resolve(`${npmName}/dsh/icon`), new URL("assets/logo.svg", base).href);
    assert.equal(import.meta.resolve(`${npmName}/dsh/locale/en.json`), new URL("locale/en.json", base).href);
    assert.equal(import.meta.resolve(`${npmName}/cordis.patch.yml`), new URL("cordis.patch.yml", base).href);
    assert.equal(import.meta.resolve(`${npmName}/locale/en.json`), new URL("locale/en.json", base).href);
    assert.equal(import.meta.resolve(`${npmName}/package.json`), new URL("package.json", base).href);

    const adapter = await import(`${npmName}/dsh`);
    assert.equal(adapter.name, `skill-${collection}`);
    assert.deepEqual(adapter.inject, ["skills"]);

    let provider;
    adapter.apply({
      skills: {
        registerProvider(factory) {
          provider = factory({ signal: new AbortController().signal, invalidate() {} });
          return () => {};
        },
      },
    });
    assert.ok(provider);
    assert.equal(provider.name, collection);

    const catalog = JSON.parse(await readFile(new URL("skills/catalog.json", base), "utf8"));
    assert.ok(catalog.every((entry) => entry.source === source));
    const candidates = await provider.list({});
    assert.deepEqual(
      candidates.map((candidate) => candidate.name).sort(),
      catalog.map((entry) => entry.name).sort(),
    );

    for (const candidate of candidates) {
      assert.match(candidate.name, SKILL_NAME);
      assert.equal(typeof candidate.description, "string");
      assert.ok(candidate.description.length > 0);
      assert.equal(candidate.provider, collection);
      assert.equal(candidate.source, "bundled");
      assert.equal(candidate.rank, 600);
      assert.equal(candidate.resourceBase?.kind, "directory");
      assert.equal(candidate.resourceBase.path, fileURLToPath(new URL(`skills/${candidate.name}`, base)));
      assert.equal(candidate.path, join(candidate.resourceBase.path, "SKILL.md"));

      const raw = await readFile(candidate.path, "utf8");
      const header = parse(/^---\n([\s\S]*?)\n---\n/.exec(raw)[1]);
      assert.deepEqual(candidate.invocation, {
        modelInvocable: header["disable-model-invocation"] !== true,
        userInvocable: header["user-invocable"] !== false,
      });

      const definition = await provider.get(candidate, {});
      assert.ok(definition);
      assert.equal(definition.name, candidate.name);
      assert.equal(definition.description, candidate.description);
      assert.deepEqual(definition.invocation, candidate.invocation);
      assert.equal(definition.provider, collection);
      assert.equal(definition.source, "bundled");
      assert.deepEqual(definition.resourceBase, candidate.resourceBase);
      assert.equal(definition.path, candidate.path);
      assert.ok(definition.content.length > 0);
      for (const [, link] of definition.content.matchAll(/\]\(([^)]+)\)/g)) {
        await access(new URL(link, pathToFileURL(definition.path)));
        await access(join(definition.resourceBase.path, link));
      }
    }

    const aborted = AbortSignal.abort(new Error("cancelled"));
    await assert.rejects(() => provider.list({ signal: aborted }), /cancelled/);
    if (candidates.length > 0) {
      await assert.rejects(() => provider.get(candidates[0], { signal: aborted }), /cancelled/);
    }
  });
}

test("all DeepSeek Harness bundles coexist with distinct row ids, providers, and skill names", async () => {
  const rowIds = new Set();
  const providers = new Set();
  const skills = new Set();
  const expected = [];

  for (const { name: collection, npm_name: npmName } of collections) {
    const catalog = JSON.parse(
      await readFile(new URL(`../plugins/${collection}/skills/catalog.json`, import.meta.url), "utf8"),
    );
    expected.push(...catalog.map((entry) => entry.name));

    const patch = parse(
      await readFile(new URL(`../plugins/${collection}/cordis.patch.yml`, import.meta.url), "utf8"),
    );
    for (const item of patch) {
      for (const row of item.insert ?? []) {
        assert.ok(!rowIds.has(row.id), `Duplicate row id: ${row.id}`);
        rowIds.add(row.id);
      }
    }

    const adapter = await import(`${npmName}/dsh`);
    let provider;
    adapter.apply({
      skills: {
        registerProvider(factory) {
          provider = factory({ signal: new AbortController().signal, invalidate() {} });
          return () => {};
        },
      },
    });
    assert.ok(!providers.has(provider.name), `Duplicate provider: ${provider.name}`);
    providers.add(provider.name);
    for (const candidate of await provider.list({})) {
      assert.ok(!skills.has(candidate.name), `Duplicate skill: ${candidate.name}`);
      skills.add(candidate.name);
    }
  }

  assert.deepEqual([...skills].sort(), expected.sort());
});
