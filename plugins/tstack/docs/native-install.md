# Install the native plugins

The `odestroyero-skills` marketplace contains five independent plugins. Install the collections you want:

```text
plugins/mattpocock/    Matt Pocock's published skills
plugins/pstack/        pstack's published skills
plugins/tstack/        Theo Browne's tstack skills
plugins/cc/     Anthropic's redistributable skills
plugins/mongodb/           MongoDB's query, schema, search, and Atlas skills
```

Each plugin contains its own workflows, resources, native manifests, and upstream license notices. The repository root is a private development workspace. Skill names retain their collection prefixes across harnesses, such as `mattpocock-tdd` and `pstack-tdd`.

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
```

For local testing, use `claude plugin marketplace add /absolute/path/to/skills` for the first command.

Open `/plugin`, select **Marketplaces**, select `odestroyero-skills`, then select **Enable auto-update**. Third-party marketplaces have automatic updates disabled by default. Updated files load in the next session, or after `/reload-plugins` in a running session.

Invoke a skill as `/mattpocock:mattpocock-code-review`, `/pstack:pstack-poteto-mode`, `/tstack:tstack-full-stop`, `/cc:anthropic-frontend-design`, or `/mongodb:mongodb-mongodb-query-optimizer`. For manual updates:

```sh
claude plugin update mattpocock@odestroyero-skills
claude plugin update pstack@odestroyero-skills
claude plugin update tstack@odestroyero-skills
claude plugin update cc@odestroyero-skills
claude plugin update mongodb@odestroyero-skills
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
```

Use `codex plugin marketplace add /absolute/path/to/skills` for local testing. The catalog at `.agents/plugins/marketplace.json` points to each generated folder. Each has a portable `plugin.json` and a Codex compatibility manifest.

Run `/plugins` to inspect the installation, then start a new session. Select the skill shown by its plugin or skill picker. Refresh the Git marketplace explicitly with:

```sh
codex plugin marketplace upgrade odestroyero-skills
```

Automatic refresh of custom marketplaces depends on the Codex host and version. Verify it in your client before removing a scheduled updater. Official OpenAI documentation describes [marketplace commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin-marketplace) and [plugin loading](https://learn.chatgpt.com/docs/plugins#plugin-directory-in-codex-cli).

## Cursor

On Teams or Enterprise, open **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace**. Choose **Import from Repo** and enter `https://github.com/oDestroyeRo/skills`. Select the collections you want in **Customize**: `mattpocock`, `pstack`, `tstack`, `cc`, or `mongodb`.

Enable **Auto Refresh** in the marketplace settings and grant the Cursor GitHub App access to this repository. Import the whole repository so refresh also reads catalog changes. Existing Cloud Agents keep their starting versions; start a new agent after an update.

For local testing, copy each complete folder into Cursor's local-plugin directory:

```text
plugins/mattpocock/ → ~/.cursor/plugins/local/mattpocock/
plugins/pstack/     → ~/.cursor/plugins/local/pstack/
plugins/tstack/     → ~/.cursor/plugins/local/tstack/
plugins/cc/ → ~/.cursor/plugins/local/cc/
plugins/mongodb/ → ~/.cursor/plugins/local/mongodb/
```

Reload Cursor after copying. A symlink to a checkout outside that local-plugin directory is not a supported substitute. Public Marketplace listing requires submission and review. See [Cursor installation and refresh](https://cursor.com/docs/plugins#keep-plugins-up-to-date).

## Pi

Install the per-collection local packages from a checkout:

```sh
pi install /absolute/path/to/skills/plugins/mattpocock
pi install /absolute/path/to/skills/plugins/pstack
pi install /absolute/path/to/skills/plugins/tstack
pi install /absolute/path/to/skills/plugins/cc
pi install /absolute/path/to/skills/plugins/mongodb
```

Each package's `pi.skills` entry selects only that collection. Local packages load from their folder. A scheduled `python3 scripts/skills.py update` keeps the checkout current; run `/reload` in Pi if the session has stale skills.

After publishing the separate npm packages, you can install them from the registry:

```sh
pi install npm:@odestroyero/mattpocock-skills
pi install npm:@odestroyero/pstack-skills
pi install npm:@odestroyero/tstack-skills
pi install npm:@odestroyero/anthropic-skills
pi install npm:@odestroyero/mongodb-skills
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
```

For local testing, select the folders in `opencode.json` or `opencode.jsonc`:

```json
{
  "plugins": [
    "/absolute/path/to/skills/plugins/mattpocock",
    "/absolute/path/to/skills/plugins/pstack",
    "/absolute/path/to/skills/plugins/tstack",
    "/absolute/path/to/skills/plugins/cc",
    "/absolute/path/to/skills/plugins/mongodb"
  ]
}
```

Each adapter targets `@opencode/plugin` 2.2.5 and registers only its collection through the v2 skill transform API. Upstream agents, hooks, and services still require their own configuration. OpenCode v1 has a different plugin API; use the folder installer there.

Check and apply package updates with:

```sh
opencode plugin check
opencode plugin update
```

OpenCode v2 checks unpinned packages at startup but does not apply updates automatically. Schedule its update command for unattended refresh. See [package installation](https://opencode.ai/v2/docs/plugins) and the [v2 skill API](https://opencode.ai/v2/docs/build/plugins/server#skills).

## Antigravity

Validate and install each selected native folder:

```sh
agy plugin validate --strict /absolute/path/to/skills/plugins/mattpocock
agy plugin install /absolute/path/to/skills/plugins/mattpocock
agy plugin validate --strict /absolute/path/to/skills/plugins/pstack
agy plugin install /absolute/path/to/skills/plugins/pstack
agy plugin validate --strict /absolute/path/to/skills/plugins/tstack
agy plugin install /absolute/path/to/skills/plugins/tstack
agy plugin validate --strict /absolute/path/to/skills/plugins/cc
agy plugin install /absolute/path/to/skills/plugins/cc
agy plugin validate --strict /absolute/path/to/skills/plugins/mongodb
agy plugin install /absolute/path/to/skills/plugins/mongodb
agy plugin list
```

Each folder has the Antigravity manifest, logo, suggested prompt, skills, and resources for that collection. Its standalone ZIP or tar.gz can also be extracted and installed as a local plugin.

After refreshing the checkout, re-run the local install and check the version with `agy plugin list`. Automatic updates for arbitrary Git or local installs have not been verified. Use folder installs with a scheduled repository updater when you need the existing automatic-refresh path.

For marketplace delivery, submit each standalone plugin through Antigravity's official intake after validation. See [plugin authoring](https://antigravity.google/docs/build-plugins) and [marketplace installation](https://antigravity.google/docs/marketplace).

## DeepSeek Harness

Install the Git subdirectory bundles you want into a DeepSeek Harness profile (such as `web`, `headless`, `sdk`, `acp`, or a custom profile name; requires `pnpm` on `PATH`):

```sh
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/mattpocock'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/pstack'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/tstack'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/cc'
dsh plugin --profile web add 'github:oDestroyeRo/skills#main&path:plugins/mongodb'
```

For local testing from a checkout without installing workspace dependencies, pass `file:` directory specs (or `dist/<name>-<version>.tar.gz` archives); omit `file:` to link directly after running `npm install --ignore-scripts --no-package-lock` in the checkout:

```sh
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/mattpocock
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/pstack
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/tstack
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/cc
dsh plugin --profile web add file:/absolute/path/to/skills/plugins/mongodb
```

After publishing the separate npm packages, you can also install `@odestroyero/mattpocock-skills`, `@odestroyero/pstack-skills`, `@odestroyero/tstack-skills`, `@odestroyero/anthropic-skills`, and `@odestroyero/mongodb-skills` with `dsh plugin --profile <profile> add` or from the **Plugins** page in Web and Desktop. For the Desktop profile, initialize Desktop once and quit it before running Desktop's bundled `dsh plugin --profile desktop` command, or install through Desktop's **Plugins** UI.

Each bundle's `cordis.patch.yml` mounts `dsh.mjs` (`<package>/dsh`), registering only that collection on `ctx.skills` at bundled rank so `.dsh/skills` and `~/.dsh/skills` overrides still win. Invoke user-invocable skills with `/mattpocock-code-review`, `/pstack-poteto-mode`, `/tstack-full-stop`, `/anthropic-frontend-design`, or `/mongodb-mongodb-query-optimizer`; model-invocable skills also appear in `<available_skills>` when `@deepseek-ai/dsh-tool-skill` is active.

Refresh Git or registry bundles with `dsh plugin --profile <profile> update`, or refresh linked local checkouts with `python3 scripts/skills.py update`. Profiles with `dsh-hmr` enabled (such as `web`) reload live; startup-only profiles apply changes on the next launch. See [`@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh) and the [DeepSeek Harness runtime notes](harnesses.md#deepseek-harness).

## T3 Code

Install the collections through the provider you use in T3. Codex and Claude Code use the marketplace entries; Pi and OpenCode use their per-collection packages. Start a new provider session or refresh its picker after installation.

T3's provider integration determines native plugin discovery. If it does not expose a package, the folder installer can link the separate skills into provider folders:

```sh
python3 scripts/skills.py install --agent t3 --global
```

Keep the [T3 runtime adapter](harnesses.md#t3-code) for delegation and model settings, and read the [tstack runtime requirements](harnesses.md#tstack-workflows) before invoking its PR workflows. The folder installer links directly to each plugin's `skills/` directory. Custom collections use their own source and plugin entries.
