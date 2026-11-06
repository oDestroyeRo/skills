# Build and distribute native plugins

Generate one marketplace with `mattpocock`, `pstack`, `tstack`, `cc`, and `mongodb` plugins. Each has its own folder, package identity, resources, and release archives. They share the repository's release version. Changes to any collection produce a new release, while consumers choose which plugins to install.

Run these commands from the source checkout, which contains `scripts/`. Installed and extracted plugins contain runtime resources rather than the source build tools. Generation writes local artifacts; publishing and installations are separate actions.

## Build the packages

```sh
python3 scripts/skills.py package --archive
python3 scripts/skills.py check
```

`distribution.json` owns marketplace metadata and the `plugins` list. Each entry names its source, plugin identity, npm package, display text, and suggested prompts. `distribution.lock.json` records the release version, input hash, bundle hashes, and generated catalog hashes.

The first build uses `initial_version`, currently `1.0.0`. Later builds increment the patch version once when inputs change. Repeating an unchanged build keeps its version. Skill additions, removals, resource edits, and adapter changes all trigger a release. Native manifests receive the same release version; catalogs point at their respective bundles.

The generated layout is:

```text
.agents/plugins/marketplace.json       Five Codex entries
.claude-plugin/marketplace.json        Five Claude Code entries
.cursor-plugin/marketplace.json        Five Cursor entries
package.json                           Private development workspace
plugins/
  mattpocock/                          Matt's native plugin and npm package
  pstack/                             pstack's native plugin and npm package
  tstack/                             tstack's native plugin and npm package
  cc/                       Anthropic's community plugin and npm package
  mongodb/                       MongoDB's community plugin and npm package
dist/
  mattpocock-<version>.zip
  mattpocock-<version>.tar.gz
  pstack-<version>.zip
  pstack-<version>.tar.gz
  tstack-<version>.zip
  tstack-<version>.tar.gz
  cc-<version>.zip
  cc-<version>.tar.gz
  mongodb-<version>.zip
  mongodb-<version>.tar.gz
```

Each plugin folder contains `plugin.json`, `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.antigravity-plugin/`, `package.json`, `opencode.mjs`, `skills/`, its own `upstream/` source, guides, a logo, and a `THIRD_PARTY_NOTICES.md` license index. The root workspace is private. The builder discovers skills from each configured upstream and writes entry points only into that source's plugin folder. Custom collections use their own source and plugin entries.

Bundles use regular files with materialized copies of source symlinks. Skill links resolve within their own bundle. ZIP contents start at the plugin root; tarballs contain a directory named for the plugin. Workstation installation records, Git credentials, dependency installations, and build caches are excluded.

Generated-output edits stop a rebuild so custom work is preserved. Change source inputs, then regenerate. Repeated archive builds preserve identical artifacts. Output symlinks and files with different contents stop the archive build without overwriting them.

## Validate before distribution

Run the integration tests and validate all native plugins and the marketplace:

```sh
python3 -m unittest discover -s tests -v
claude plugin validate --strict --profile directory plugins/mattpocock
claude plugin validate --strict --profile directory plugins/pstack
claude plugin validate --strict --profile directory plugins/tstack
claude plugin validate --strict --profile directory plugins/cc
claude plugin validate --strict --profile directory plugins/mongodb
claude plugin validate --strict .claude-plugin/marketplace.json
```

For OpenCode SDK checks and separate npm archives, use Node.js 22 or newer:

```sh
npm install --ignore-scripts --no-package-lock
node --test tests/opencode.test.mjs
npm pack --ignore-scripts --workspaces --pack-destination dist
```

The npm packages are `@odestroyero/mattpocock-skills`, `@odestroyero/pstack-skills`, `@odestroyero/tstack-skills`, `@odestroyero/anthropic-skills`, and `@odestroyero/mongodb-skills`. Registry publication requires ownership of that scope. The repo's packaging code uses MIT. Upstream terms remain in each bundle's `upstream/` folder and are linked from its notice index. Anthropic's npm license field points to that index because its skills and assets have separate terms. MongoDB's npm license field also points to its notice index, which links its Apache 2.0 source license.

If Antigravity is installed, validate each folder with `agy plugin validate --strict`. Check skill names and versions in each target client. Schema and SDK checks do not prove live discovery or workflow execution across every client.

## Update the Git marketplaces

The daily workflow runs `sync`, which reads each upstream's configured manifest or skill roots, rebuilds each plugin, and updates the release version when inputs change. It checks the result and runs tests before committing generated updates. Additions and removals update the appropriate plugin without a second skill list. tstack and MongoDB use their `skills/` directories directly, so newly added or removed skills are picked up automatically. Anthropic also uses that directory, with a license-file hash filter applied before archiving. New skills with approved terms are included; missing or changed terms are omitted and recorded in `sources.lock.json`. Review license changes before extending the hash list.

For a manual release, review and commit source and generated changes through your normal process. Include `distribution.lock.json`, `plugins/`, the three catalogs, and root `package.json`. Push to the branch tracked by your marketplaces. Keep `dist/`, `node_modules/`, and `.cache/` out of commits.

Consumers need their host's updater enabled. Claude Code has a marketplace switch, Cursor team marketplaces have Auto Refresh, Pi supports package updates and unpinned startup packages, and OpenCode v2 has an update command. Codex custom-marketplace refresh and Antigravity Git/local refresh need verification in the deployed host. See the [installation guide](native-install.md).

## Publish separate npm releases

After your npm account has access to the configured scope, inspect and publish the workspace packages:

```sh
npm pack --ignore-scripts --workspaces --pack-destination dist
npm publish --workspaces --access public --ignore-scripts
```

The private root workspace is excluded. You can publish a single collection with `--workspace plugins/mattpocock`, `--workspace plugins/pstack`, `--workspace plugins/tstack`, `--workspace plugins/cc`, or `--workspace plugins/mongodb` instead of `--workspaces`.

The daily workflow updates Git consumers and marketplaces; it does not publish npm releases. Publish each release separately if consumers track npm packages.

## Submit public marketplace plugins

Submit each selected `plugins/<name>/` folder, or its ZIP, as a separate plugin. Review publisher metadata, original notices, and workflow requirements before submission. Cursor, Antigravity, and OpenAI have intake and review processes separate from a repo marketplace. Generating these catalogs does not list the plugins in a public directory.

Formats follow the [Agent Plugins schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [OpenAI packaging guide](https://developers.openai.com/plugins/build/plugins), [Claude manifest reference](https://code.claude.com/docs/en/plugins-reference), [Cursor plugin guide](https://cursor.com/docs/plugins), and [Antigravity authoring guide](https://antigravity.google/docs/build-plugins).
