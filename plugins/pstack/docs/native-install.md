# Install the native plugins

The `odestroyero-skills` marketplace contains seven independent plugins. Install the collections you want:

```text
plugins/mattpocock/    Matt Pocock's published skills
plugins/pstack/        pstack's published skills
plugins/tstack/        Theo Browne's tstack skills
plugins/cc/     Anthropic's redistributable skills
plugins/mongodb/       MongoDB's query, schema, search, and Atlas skills
plugins/google/        Google's first-party agent skills
plugins/postgres/      Microsoft's PostgreSQL skills
```

Each plugin contains its own workflows, resources, native manifests, and upstream license notices. The repository root is a private development workspace. Codex, Claude Code, and OpenCode v2 use names such as `pstack:how` for native plugins. Folder installations use prefixed names such as `pstack-how`.

If you installed the Anthropic collection under its previous plugin name, reinstall it as `cc` using your harness's instructions below. The plugin identity changed. Skill names and the npm package `@odestroyero/anthropic-skills` stay the same.

The Anthropic plugin includes only skills with approved redistribution terms. Its document skills and unlicensed `doc-coauthoring` skill are excluded. See the [Anthropic runtime notes](harnesses.md#anthropic-workflows).

The MongoDB plugin is a community mirror of the Apache 2.0 skills from `mongodb/agent-skills`. Exported names include `mongodb-mongodb-query-optimizer`. Configure MongoDB MCP tools separately when a skill needs them. See the [MongoDB runtime notes](harnesses.md#mongodb-workflows).

The remote commands below become available after the repository is pushed. Local folder installs work from the generated checkout. Choose one delivery method per harness to avoid duplicate workflows.

## Claude Code

Add the marketplace, then install the collections you want:

```sh
claude plugin marketplace add oDestroyeRo/skills
claude plugin install mattpocock@odestroyero-skills
claude plugin install pstack@odestroyero-skills
claude plugin install tstack@odestroyero-skills
claude plugin install cc@odestroyero-skills
claude plugin install mongodb@odestroyero-skills
claude plugin install google@odestroyero-skills
claude plugin install postgres@odestroyero-skills
```

For local testing, use `claude plugin marketplace add /absolute/path/to/skills` for the first command.

Open `/plugin`, select **Marketplaces**, select `odestroyero-skills`, then select **Enable auto-update**. Third-party marketplaces have automatic updates disabled by default. Updated files load in the next session, or after `/reload-plugins` in a running session.

Invoke a skill as `/mattpocock:code-review`, `/pstack:how`, `/tstack:full-stop`, `/cc:frontend-design`, or `/mongodb:query-optimizer`. For manual updates run:

```sh
claude plugin update mattpocock@odestroyero-skills
claude plugin update pstack@odestroyero-skills
claude plugin update tstack@odestroyero-skills
claude plugin update cc@odestroyero-skills
claude plugin update mongodb@odestroyero-skills
claude plugin update google@odestroyero-skills
claude plugin update postgres@odestroyero-skills
```

See [Claude Code installation and updates](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

## Codex

Add the Git marketplace, then install the plugins you want:

```sh
codex plugin marketplace add oDestroyeRo/skills
codex plugin add mattpocock@odestroyero-skills
codex plugin add pstack@odestroyero-skills
codex plugin add tstack@odestroyero-skills
codex plugin add cc@odestroyero-skills
codex plugin add mongodb@odestroyero-skills
codex plugin add google@odestroyero-skills
codex plugin add postgres@odestroyero-skills
```

Use `codex plugin marketplace add /absolute/path/to/skills` for local testing. The catalog at `.agents/plugins/marketplace.json` points to each generated folder. Each has a portable `plugin.json` and a Codex compatibility manifest.

Run `/plugins` to inspect the installation, then start a new session. Select the skill by its qualified name, such as `pstack:how` or `mattpocock:code-review`. To refresh the Git marketplace, run:

```sh
codex plugin marketplace upgrade odestroyero-skills
```

Automatic refresh of custom marketplaces depends on the Codex host and version. Verify it in your client before removing a scheduled updater. Official OpenAI documentation describes [marketplace commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin-marketplace) and [plugin loading](https://learn.chatgpt.com/docs/plugins#plugin-directory-in-codex-cli).

## Cursor

Download the collection's ZIP from [GitHub Releases](https://github.com/oDestroyeRo/skills/releases), or run `python3 scripts/skills.py package --archive` and use the ZIP from `dist/`. Extract each plugin into its own directory under `~/.cursor/plugins/local/`, such as `~/.cursor/plugins/local/pstack/`. Reload Cursor after extracting a fresh version. For scheduled refresh, use the folder installer with `--agent cursor`. See [Cursor's local plugin guide](https://cursor.com/docs/plugins).

If you previously used this repository as a Cursor Git marketplace, switch to the release bundles or the folder installer.

## Pi

Extract the collection's tar.gz or ZIP from [GitHub Releases](https://github.com/oDestroyeRo/skills/releases) or build it locally with `python3 scripts/skills.py package --archive`. Install the extracted package:

```sh
pi install /absolute/path/to/extracted/pstack
```

Each release package selects its generated prefixed entries via `pi.skills`. To update a local package, extract the newer release at the package path and run `/reload`. To use the scheduled checkout updater, use the folder installer with `--agent pi`.

After publishing the separate npm packages, you can install them from the registry:

```sh
pi install npm:@odestroyero/mattpocock-skills
pi install npm:@odestroyero/pstack-skills
pi install npm:@odestroyero/tstack-skills
pi install npm:@odestroyero/anthropic-skills
pi install npm:@odestroyero/mongodb-skills
pi install npm:@odestroyero/google-skills
pi install npm:@odestroyero/postgres-skills
pi update --extensions
```

For startup and reload refresh without a persistent package declaration, launch with an unpinned npm package, for example `pi -e npm:@odestroyero/mattpocock-skills`. Repeat `-e` for each additional package. Exact npm versions, Git tags, and commit pins keep their selected version. See [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

## OpenCode v2

Install the Git subdirectory packages you want:

```sh
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/mattpocock'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/pstack'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/tstack'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/cc'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/mongodb'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/google'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/postgres'
```

For local testing, select the folders in `opencode.json` or `opencode.jsonc`:

```json
{
  "plugins": [
    "/absolute/path/to/skills/plugins/mattpocock",
    "/absolute/path/to/skills/plugins/pstack",
    "/absolute/path/to/skills/plugins/tstack",
    "/absolute/path/to/skills/plugins/cc",
    "/absolute/path/to/skills/plugins/mongodb",
    "/absolute/path/to/skills/plugins/google",
    "/absolute/path/to/skills/plugins/postgres"
  ]
}
```

Each adapter targets `@opencode/plugin` 2.2.5 and registers its collection through the v2 skill transform API. Skills appear with qualified names such as `mattpocock:tdd` and `pstack:tdd`. Configure upstream agents, hooks, and services separately. For OpenCode v1, use the folder installer.

Check and apply package updates with:

```sh
opencode plugin check
opencode plugin update
```

OpenCode v2 checks unpinned packages at startup but does not apply updates automatically. Schedule its update command for unattended refresh. See [package installation](https://opencode.ai/v2/docs/plugins) and the [v2 skill API](https://opencode.ai/v2/docs/build/plugins/server#skills).

## Antigravity

Download a collection's ZIP from [GitHub Releases](https://github.com/oDestroyeRo/skills/releases) or build it with `python3 scripts/skills.py package --archive`. Extract the plugin folder, then validate and install it:

```sh
agy plugin validate --strict /absolute/path/to/extracted/pstack
agy plugin install /absolute/path/to/extracted/pstack
agy plugin list
```

The release package includes the Antigravity manifest and prefixed skills such as `/pstack-how`. Use the prefixed names when collections share a short name. Install the newer release to update the plugin. For scheduled refresh, use the folder installer with `--agent antigravity`. See [Antigravity's plugin guide](https://antigravity.google/docs/build-plugins).

## DeepSeek Harness

Install the Git subdirectory bundles you want into a DeepSeek Harness profile (such as `web`, `headless`, `sdk`, `acp`, or a custom profile name; requires `pnpm` on `PATH`):

```sh
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/mattpocock'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/pstack'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/tstack'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/cc'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/mongodb'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/google'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/postgres'
```

For local testing from a checkout without installing workspace dependencies, pass `file:` directory specs (or `dist/<name>-<version>.tar.gz` archives); omit `file:` to link directly after running `npm install --ignore-scripts --no-package-lock` in the checkout:

```sh
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/mattpocock
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/pstack
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/tstack
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/cc
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/mongodb
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/google
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/postgres
```

After publishing the separate npm packages, you can also install `@odestroyero/mattpocock-skills`, `@odestroyero/pstack-skills`, `@odestroyero/tstack-skills`, `@odestroyero/anthropic-skills`, `@odestroyero/mongodb-skills`, `@odestroyero/google-skills`, and `@odestroyero/postgres-skills` with `dsh plugin --profile <profile> add` or from the **Plugins** page in Web and Desktop. For the Desktop profile, initialize Desktop once and quit it before running Desktop's bundled `dsh plugin --profile desktop` command, or install through Desktop's **Plugins** UI.

Each bundle's `cordis.patch.yml` mounts `dsh.mjs` (`<package>/dsh`), registering only that collection on `ctx.skills` at bundled rank so `.dsh/skills` and `~/.dsh/skills` overrides still win. Invoke user-invocable skills with `/mattpocock-code-review`, `/pstack-poteto-mode`, `/tstack-full-stop`, `/anthropic-frontend-design`, or `/mongodb-mongodb-query-optimizer`; model-invocable skills also appear in `<available_skills>` when `@deepseek-ai/dsh-tool-skill` is active.

Refresh Git or registry bundles with `dsh plugin --profile <profile> update`, or refresh linked local checkouts with `python3 scripts/skills.py update`. Profiles with `dsh-hmr` enabled (such as `web`) reload live; startup-only profiles apply changes on the next launch. See [`@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh) and the [DeepSeek Harness runtime notes](harnesses.md#deepseek-harness).

## T3 Code

Install the collections through the provider you use in T3. Codex and Claude Code use the marketplace entries; Pi and OpenCode use their per-collection packages. Start a new provider session or refresh its picker after installation.

T3's provider integration determines native plugin discovery. If it does not expose a package, the folder installer can link the separate skills into provider folders:

```sh
python3 scripts/skills.py install --agent t3 --global
```

Keep the [T3 runtime adapter](harnesses.md#t3-code) for delegation and model settings, and read the [tstack runtime requirements](harnesses.md#tstack-workflows) before invoking its PR workflows. The folder installer links into the checkout's generated skill cache. If you linked skills from an older checkout, run `git pull --ff-only` before `python3 scripts/skills.py update` to refresh the saved links using the new installer. Custom collections use their own source and plugin entries.
