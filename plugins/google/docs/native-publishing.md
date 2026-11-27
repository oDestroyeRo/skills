# Build and distribute native plugins

Generate one marketplace with `mattpocock`, `pstack`, `tstack`, `cc`, `mongodb`, `google`, and `postgres` plugins. Each has its own folder, package identity, resources, and release archives. They share the repository's release version. Changes to any collection produce a new release, while consumers choose which plugins to install.

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
.agents/plugins/marketplace.json       Seven Codex entries
.claude-plugin/marketplace.json        Seven Claude Code entries
package.json                           Private development workspace
plugins/
  mattpocock/                          Matt's native plugin and npm package
  pstack/                             pstack's native plugin and npm package
  tstack/                             tstack's native plugin and npm package
  cc/                       Anthropic's community plugin and npm package
  mongodb/                            MongoDB's community plugin and npm package
  google/                             Google's community plugin and npm package
  postgres/                           Microsoft's PostgreSQL community plugin and npm package
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
  google-<version>.zip
  google-<version>.tar.gz
  postgres-<version>.zip
  postgres-<version>.tar.gz
```

Each plugin folder contains a skill catalog, native manifests, adapters, `skills/`, and its own upstream resources and license notices. The ZIP and tar.gz bundles also contain the Cursor and Antigravity manifests and `prefixed-skills/` for Pi, Cursor, and Antigravity. The root workspace is private. The builder discovers skills from each configured upstream and writes entry points only into that source's plugin folder. Custom collections use their own source and plugin entries.

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
claude plugin validate --strict --profile directory plugins/google
claude plugin validate --strict --profile directory plugins/postgres
claude plugin validate --strict .claude-plugin/marketplace.json
```

For OpenCode and DeepSeek Harness adapter checks and separate npm archives, use Node.js 22 or newer:

```sh
npm install --ignore-scripts --no-package-lock
node --test tests/opencode.test.mjs tests/dsh.test.mjs
```

The npm packages are `@odestroyero/mattpocock-skills`, `@odestroyero/pstack-skills`, `@odestroyero/tstack-skills`, `@odestroyero/anthropic-skills`, `@odestroyero/mongodb-skills`, `@odestroyero/google-skills`, and `@odestroyero/postgres-skills`. Registry publication requires ownership of that scope. The repo's packaging code uses MIT. Upstream terms remain in each bundle's `upstream/` folder and are linked from its notice index. Anthropic's npm license field points to that index because its skills and assets have separate terms. MongoDB's npm license field also points to its notice index, which links its Apache 2.0 source license.

If Antigravity is installed, validate each extracted plugin folder with `agy plugin validate --strict`. Check skill names and versions in each target client. Schema and SDK checks do not prove live discovery or workflow execution across every client.

## Update the Git marketplaces

The daily workflow runs `sync`, which reads each upstream's configured manifest or skill roots, rebuilds each plugin, and updates the release version when inputs change. It checks the result and runs tests before committing generated updates. Additions and removals update the appropriate plugin without a second skill list. tstack and MongoDB use their `skills/` directories directly, so newly added or removed skills are picked up automatically. Anthropic also uses that directory, with a license-file hash filter applied before archiving. New skills with approved terms are included; missing or changed terms are omitted and recorded in `sources.lock.json`. Review license changes before extending the hash list.

The daily workflow publishes the ZIP and tar.gz bundles to [GitHub Releases](https://github.com/oDestroyeRo/skills/releases) after validation and push. It uses the package version as the tag and resumes incomplete draft uploads on the next run.

For a manual change, review and commit source inputs, the regenerated `plugins/`, the marketplace catalogs, `distribution.lock.json`, and the root `package.json`. Keep `dist/`, `node_modules/`, and `.cache/` out of commits.

Installed clients receive updates through their configured updater. For the scheduled folder updater, `skills.py update` pulls the checkout and regenerates entries. For installed copies of release archives, download and install the new version. See the [installation guide](native-install.md).

## Publish separate npm releases

After your npm account has access to the configured scope, build the archives and publish the desired versioned tar.gz:

```sh
python3 scripts/skills.py package --archive
version=$(python3 -c 'import json; print(json.load(open("distribution.lock.json"))["package_version"])')
npm publish "./dist/pstack-$version.tar.gz" --access public --ignore-scripts
```

Publish each collection you want to distribute through npm. The daily workflow publishes to GitHub Releases. Publishing to the npm registry uses separate credentials.

## Submit public marketplace plugins

Submit each selected release ZIP or extracted plugin folder as a separate plugin. Review publisher metadata, original notices, and workflow requirements before submission. Cursor, Antigravity, and OpenAI have intake and review processes separate from a repo marketplace. Generating these catalogs does not list the plugins in a public directory.

Formats follow the [Agent Plugins schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [OpenAI packaging guide](https://developers.openai.com/plugins/build/plugins), [Claude manifest reference](https://code.claude.com/docs/en/plugins-reference), [Cursor plugin guide](https://cursor.com/docs/plugins), and [Antigravity authoring guide](https://antigravity.google/docs/build-plugins).
