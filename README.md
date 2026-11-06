# Shared agent skills

One library for **T3 Code, Codex, Claude Code, Pi, Antigravity, OpenCode, and Cursor**, with updates from [Matt Pocock's skills](https://github.com/mattpocock/skills), [pstack](https://github.com/cursor/plugins/tree/main/pstack), [tstack](https://github.com/t3dotgg/tstack), [Anthropic's redistributable skills](https://github.com/anthropics/skills), and [MongoDB's skills](https://github.com/mongodb/agent-skills).

Upstream files stay together with their references, scripts, agent prompts, and licenses. Namespaced entry points let the collections coexist: `mattpocock-tdd` and `pstack-tdd` are separate skills, while tstack uses names such as `tstack-full-stop`. Each collection's entry points live in `plugins/<name>/skills/`. Folder installs link directly to those entries; native packages contain self-contained copies. The installer and bundle generator use Python **3.9+** and Git on macOS or Linux without third-party Python packages. OpenCode's package and SDK checks use Node.js **22+**.

## Install

The native marketplace contains five independent plugins: **mattpocock**, **pstack**, **tstack**, **cc**, and **mongodb**, in their respective `plugins/<name>/` folders. Install the collections you want using the [native installation guide](docs/native-install.md). It covers Claude Code, Codex, Cursor, Pi, OpenCode v2, Antigravity, and T3 Code. The [publishing guide](docs/native-publishing.md) covers versions, validation, and separate release artifacts.

Use the folder installer below to link plugin skills from one checkout across harnesses:

Clone this repository, then run:

```sh
python3 scripts/skills.py check
python3 scripts/skills.py install --agent t3 --global
```

The T3 profile covers its Codex, Claude Code, Pi, Antigravity, OpenCode, and Cursor provider directories. To choose native harnesses individually:

```sh
python3 scripts/skills.py install --agent codex --agent claude-code --global
python3 scripts/skills.py install --agent all --project /path/to/your/project
```

Refresh the harness's skill picker or start a new session. Choose an exported name such as `pstack-poteto-mode` or `mattpocock-code-review`. Invocation syntax varies by harness; T3 exposes skills through its picker. Run `python3 scripts/skills.py list` for the full list.

Existing skills are preserved. A conflicting name stops installation before links are created. If your harness uses a custom config directory, install directly into its skill directory:

```sh
python3 scripts/skills.py install --directory /custom/config/skills
```

The installer remembers target directories in ignored `.cache/installations.json`. Updates add new links and remove obsolete links owned by this checkout. Keep the checkout in place; moving or deleting it breaks its installed links. To uninstall, remove only the links pointing to this checkout and remove that destination from `.cache/installations.json` so a later update does not restore them.

For an existing clone of the first release, pull this repository before running its updated installer:

```sh
git pull --ff-only
python3 scripts/skills.py update
```

The updated installer retargets remembered links to the plugin folders. A manual `sync` also removes an unchanged legacy root folder and migrates remembered links. Local edits stop that migration for review.

## Automatic updates

There are two update steps:

1. **Upstream → this repository.** The [daily workflow](.github/workflows/sync-upstream.yml) fetches all configured upstream branches, validates them, runs tests, and commits changed snapshots and entry points. It also supports **Run workflow**. It becomes active after these files are pushed to the repository's default branch with Actions enabled. The bot needs permission to push; protected branches may require adapting this to your contribution policy.
2. **This repository → each machine.** Run the command below from a scheduler on each machine. It fast-forwards the checkout's tracking branch, validates the library, and refreshes all remembered installations. Existing skill links then see the updated source.

```sh
python3 scripts/skills.py update
```

For example, add a daily job with `crontab -e`, replacing both absolute paths with your checkout and Python executable (`command -v python3`). Quote paths containing spaces:

```cron
35 9 * * * /absolute/path/to/python3 /absolute/path/to/skills/scripts/skills.py update >> /absolute/path/to/skills/.cache/update.log 2>&1
```

Use a clone of the repository's default branch for this job. The updater preserves tracked local changes and refuses a merge or rebase. Schedulers and global harness installations are opt-in; creating this repository does not enable them on your computer. Current sessions may need a reload; see the [harness notes](docs/harnesses.md).

## Maintain the library

```sh
# Fetch current upstream revisions directly into this checkout.
python3 scripts/skills.py sync

# Re-fetch exactly the revisions recorded in the lock file.
python3 scripts/skills.py sync --locked

# Verify snapshots, generated entry points, and reference paths.
python3 scripts/skills.py check

# Build versioned native packages and standalone ZIP/tar.gz artifacts.
python3 scripts/skills.py package --archive

# Run isolated integration tests without touching your installed skills.
python3 -m unittest discover -s tests -v
```

`sources.json` owns upstream URLs, branches, package roots, and skill manifests. Each sync reads the current upstream plugin manifest to discover its published skills. New skills and newly published categories are included automatically; removed or unpublished skills lose their exports and managed installation links. A rename is handled as a removal and an addition. An empty collection is allowed, and unrelated installed skills stay in place. Sources without a plugin manifest can use explicit `skill_roots` instead.

Matt's manifest currently publishes the stable engineering and productivity collections. tstack has no plugin manifest, so its `skills/` directory is discovered directly on every sync. `sources.lock.json` records exact commits, excluded paths, and content hashes. An upstream commit that leaves a snapshot unchanged keeps the recorded commit and the package version.

Each plugin keeps its source skill tree, supporting resources, guides, manifests, and licenses in `plugins/<name>/upstream/<source>/`. `exclude_paths` in `sources.json` omits upstream release tooling and contributor files on every sync. Each excluded path is relative to that source's `root`. Retained files keep their original contents and layout. Generated entry points and catalogs live only in `plugins/<name>/skills/`.

Anthropic's source uses a `license_filter` with approved license-file SHA256 hashes. Sync archives only approved skill folders and the configured attribution notices. New skills with approved terms are included automatically; missing or changed licenses are omitted and recorded in `sources.lock.json`. At the current revision, 14 Apache 2.0 skills are included. `docx`, `pdf`, `pptx`, and `xlsx` prohibit redistribution, and `doc-coauthoring` has no license file, so those five are excluded. Review new terms before adding a license hash. See the [upstream document license](https://github.com/anthropics/skills/blob/main/skills/docx/LICENSE.txt).

`description_overrides` can shorten an exported description without changing the original skill. Anthropic's `claude-api` entry uses this to stay within the 1024-character skill description limit.

MongoDB's source discovers `skills/` directly and preserves its Apache 2.0 license, references, and scripts. The `mongodb` plugin is a community mirror of those skills. The collection prefix applies to upstream names that already start with `mongodb-`, so exported names include `mongodb-mongodb-query-optimizer` and `mongodb-mongodb-schema-design`. These packages install skills only. Configure the MongoDB MCP server separately when a workflow needs it. See the [MongoDB runtime notes](docs/harnesses.md#mongodb-workflows).

Local edits to snapshots or generated skills stop a sync so custom work is preserved. All sources are downloaded and their exports validated before a new library is published. Failed downloads or invalid manifests leave the previous snapshots and exports in place.

To add a custom collection, put its skills in a Git repository, add that source to `sources.json`, and add its plugin entry to `distribution.json`. A local Git repository can use a `file:///absolute/path/to/repo` source URL. Each source has one plugin. To adopt library changes into the hosted repository, review the result and use your normal commit/push process; `sync` itself never commits or pushes. Use the scheduled `update` command for an installed machine rather than `sync`, which intentionally creates local snapshot changes.

Every sync also rebuilds each native plugin folder and its marketplace entries. A changed skill set or package input increments the release version; an unchanged build keeps it. Additions and removals update their own collection's bundle. All bundles contain regular files and preserve the source layout. The root npm file is a private development workspace with no combined skill package.

## Compatibility and verification

The folder installer and native packages use the same per-plugin skill files. Both methods use the available tools of the current harness. Some pstack and tstack workflows need subagents, selected models, services, or other plugins. tstack's PR workflows also need an authenticated GitHub CLI, and its PR wait helper needs Python 3. The [harness adapter](docs/harnesses.md) describes those boundaries and how T3 delegation fits. Existing plugin installations may also expose duplicate workflows under their original names.

The tests exercise real local Git repositories, source advances, locked revisions, update failures, protected local edits, file references, name collisions, and isolated installs for every profile. `check` verifies the actual library. These checks establish filesystem and updater behavior; live discovery and every upstream workflow across all installed harness versions still need client-level verification. In particular, Antigravity's documented discovery paths are used, but its symlink discovery has not been exercised in a running client.

The [harness notes](docs/harnesses.md) and [installation guide](docs/native-install.md) link to official documentation. Upstream license notices remain in [Matt's snapshot](plugins/mattpocock/upstream/mattpocock/LICENSE), [pstack's snapshot](plugins/pstack/upstream/pstack/LICENSE), [tstack's snapshot](plugins/tstack/upstream/tstack/LICENSE), [Anthropic's bundle notice index](plugins/cc/THIRD_PARTY_NOTICES.md), and [MongoDB's snapshot](plugins/mongodb/upstream/mongodb/LICENSE). Those terms govern their respective content and assets.

This repo's code and packaging use the [MIT license](LICENSE).
