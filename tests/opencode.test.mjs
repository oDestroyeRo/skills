import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { test } from "node:test";
import { pathToFileURL } from "node:url";
import { Skill } from "@opencode/plugin";
import { parse } from "yaml";

const distribution = JSON.parse(await readFile(new URL("../distribution.json", import.meta.url), "utf8"));
const collections = distribution.plugins.map(({ name, source }) => ({ name, source }));

for (const { name: collection, source } of collections) {
  test(`${collection} registers only its packaged skills through the OpenCode SDK`, async () => {
    const base = new URL(`../plugins/${collection}/`, import.meta.url);
    const { default: plugin } = await import(new URL("opencode.mjs", base));
    const catalog = JSON.parse(await readFile(new URL("skills/catalog.json", base), "utf8"));
    assert.equal(plugin.id, collection);
    assert.ok(catalog.every((entry) => entry.source === source));
    const definitions = [];
    await plugin.setup({
      skill: { async transform(callback) { callback({ add: (definition) => definitions.push(definition) }); } },
    });
    assert.deepEqual(definitions.map(({ id }) => id).sort(), catalog.map(({ name }) => name).sort());
    for (const definition of definitions) {
      Skill.Info.make(definition);
      const text = await readFile(definition.path, "utf8");
      const header = parse(/^---\n([\s\S]*?)\n---\n/.exec(text)[1]);
      assert.equal(definition.name, header.name);
      assert.equal(definition.autoinvoke, header["disable-model-invocation"] !== true);
      assert.ok(definition.content.length > 0);
      for (const [, link] of definition.content.matchAll(/\]\(([^)]+)\)/g)) {
        await access(new URL(link, pathToFileURL(definition.path)));
      }
    }
  });
}

test("all configured collections coexist without skill-name collisions", async () => {
  const names = new Set();
  for (const { name: collection } of collections) {
    const { default: plugin } = await import(new URL(`../plugins/${collection}/opencode.mjs`, import.meta.url));
    await plugin.setup({
      skill: {
        async transform(callback) {
          callback({
            add({ id }) {
              assert.ok(!names.has(id), `Duplicate skill: ${id}`);
              names.add(id);
            },
          });
        },
      },
    });
  }
  const catalog = JSON.parse(await readFile(new URL("../skills/catalog.json", import.meta.url), "utf8"));
  const sources = new Set(collections.map(({ source }) => source));
  assert.deepEqual([...names].sort(), catalog.filter(({ source }) => sources.has(source)).map(({ name }) => name).sort());
});
