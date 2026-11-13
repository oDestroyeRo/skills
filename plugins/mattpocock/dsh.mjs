import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { parse } from "yaml";

const BUNDLED_SKILL_RANK = 600;
const manifest = JSON.parse(await readFile(new URL("./plugin.json", import.meta.url), "utf8"));

function frontmatterBoolean(header, key) {
  if (!Object.hasOwn(header, key)) return undefined;
  const value = header[key];
  if (typeof value === "boolean") return value;
  if (value === 1 || value === "1") return true;
  if (value === 0 || value === "0") return false;
  if (typeof value === "string") {
    switch (value.toLowerCase()) {
      case "true":
      case "yes":
      case "on":
        return true;
      case "false":
      case "no":
      case "off":
        return false;
    }
  }
  throw new TypeError(`Invalid ${key} frontmatter: expected boolean`);
}

function loadSkills() {
  return readFile(new URL("./skills/catalog.json", import.meta.url), "utf8").then(async (rawCatalog) => {
    const catalog = JSON.parse(rawCatalog);
    const entries = await Promise.all(catalog.map(async ({ name }) => {
      const directoryUrl = new URL(`./skills/${name}`, import.meta.url);
      const fileUrl = new URL(`./skills/${name}/SKILL.md`, import.meta.url);
      const text = await readFile(fileUrl, "utf8");
      const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
      if (!match) throw new Error(`Missing skill frontmatter: ${name}`);
      const header = parse(match[1]);
      if (
        typeof header !== "object" || header === null || Array.isArray(header) ||
        header.name !== name || typeof header.description !== "string" || header.description.length === 0
      ) {
        throw new Error(`Invalid skill metadata: ${name}`);
      }
      const disableModelInvocation = frontmatterBoolean(header, "disable-model-invocation");
      const userInvocable = frontmatterBoolean(header, "user-invocable");
      const invocation = {
        modelInvocable: disableModelInvocation !== true,
        userInvocable: userInvocable !== false,
      };
      const resourceBase = { kind: "directory", path: fileURLToPath(directoryUrl) };
      const path = fileURLToPath(fileUrl);
      const optional = {
        ...(typeof header.whenToUse === "string" && header.whenToUse.length > 0 ? { whenToUse: header.whenToUse } : {}),
        ...(typeof header.metadata === "object" && header.metadata !== null && !Array.isArray(header.metadata)
          ? { metadata: header.metadata }
          : {}),
      };
      const definition = {
        name,
        description: header.description,
        ...optional,
        invocation,
        source: "bundled",
        provider: manifest.name,
        resourceBase,
        path,
        content: text.slice(match[0].length).trim(),
      };
      const candidate = {
        name,
        description: header.description,
        ...optional,
        invocation,
        source: "bundled",
        provider: manifest.name,
        resourceBase,
        path,
        rank: BUNDLED_SKILL_RANK,
        locator: name,
      };
      return [name, { candidate, definition }];
    }));
    return new Map(entries);
  });
}

export const name = `skill-${manifest.name}`;
export const inject = ["skills"];

export function apply(ctx) {
  let loaded;
  const skills = () => {
    loaded ??= loadSkills().catch((error) => {
      loaded = undefined;
      throw error;
    });
    return loaded;
  };
  ctx.skills.registerProvider(() => ({
    name: manifest.name,
    async list(options = {}) {
      options.signal?.throwIfAborted();
      const entries = await skills();
      options.signal?.throwIfAborted();
      return [...entries.values()].map(({ candidate }) => candidate);
    },
    async get(candidate, options = {}) {
      options.signal?.throwIfAborted();
      const entries = await skills();
      options.signal?.throwIfAborted();
      const key = typeof candidate.locator === "string" ? candidate.locator : candidate.name;
      return entries.get(key)?.definition;
    },
  }));
}
