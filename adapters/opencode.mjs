import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { Plugin, Skill } from "@opencode/plugin";
import { parse } from "yaml";

const manifest = JSON.parse(await readFile(new URL("./plugin.json", import.meta.url), "utf8"));

export default Plugin.define({
  id: manifest.name,
  async setup(ctx) {
    const catalog = JSON.parse(await readFile(new URL("./skills/catalog.json", import.meta.url), "utf8"));
    const definitions = await Promise.all(catalog.map(async ({ name }) => {
      const url = new URL(`./skills/${name}/SKILL.md`, import.meta.url);
      const text = await readFile(url, "utf8");
      const match = /^---\n([\s\S]*?)\n---\n/.exec(text);
      if (!match) throw new Error(`Missing skill frontmatter: ${name}`);
      const header = parse(match[1]);
      if (header.name !== name || typeof header.description !== "string") {
        throw new Error(`Invalid skill metadata: ${name}`);
      }
      return {
        id: Skill.ID.make(name),
        name: Skill.Name.make(name),
        description: header.description,
        path: Skill.Info.fields.path.make(fileURLToPath(url)),
        content: text.slice(match[0].length),
        autoinvoke: header["disable-model-invocation"] !== true,
      };
    }));
    await ctx.skill.transform((editor) => {
      for (const definition of definitions) editor.add(definition);
    });
  },
});
