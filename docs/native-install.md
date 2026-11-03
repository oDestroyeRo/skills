# Install the native plugins

The `odestroyero-skills` marketplace contains three independent plugins. Install the collections you want:

```text
plugins/mattpocock/    Matt Pocock's published skills
plugins/pstack/        pstack's published skills
plugins/tstack/        Theo Browne's tstack skills
```

Each plugin contains its own workflows, resources, native manifests, and upstream license notices. The repository root is a private development workspace. Skill names retain their collection prefixes across harnesses, such as `mattpocock-tdd` and `pstack-tdd`.

The remote commands below become available after the repository is pushed. Local folder installs work from the generated checkout. Choose one delivery method per harness to avoid duplicate workflows.

## Claude Code

Add the marketplace, then install the collections you want:

```sh
claude plugin marketplace add oDestroyeRo/skills
claude plugin install mattpocock@odestroyero-skills
claude plugin install pstack@odestroyero-skills
claude plugin install tstack@odestroyero-skills
```

For local testing, use `claude plugin marketplace add /absolute/path/to/skills` for the first command.

Open `/plugin`, select **Marketplaces**, select `odestroyero-skills`, then select **Enable auto-update**. Third-party marketplaces have automatic updates disabled by default. Updated files load in the next session, or after `/reload-plugins` in a running session.

Invoke a skill as `/mattpocock:mattpocock-code-review`, `/pstack:pstack-poteto-mode`, or `/tstack:tstack-full-stop`. For manual updates:

```sh
claude plugin update mattpocock@odestroyero-skills
claude plugin update pstack@odestroyero-skills
claude plugin update tstack@odestroyero-skills
```

See [Claude Code installation and updates](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

## Codex

Add the Git marketplace, then install the plugins you want:

```sh
codex plugin marketplace add oDestroyeRo/skills
codex plugin add mattpocock@odestroyero-skills
codex plugin add pstack@odestroyero-skills
codex plugin add tstack@odestroyero-skills
```

Use `codex plugin marketplace add /absolute/path/to/skills` for local testing. The catalog at `.agents/plugins/marketplace.json` points to each generated folder. Each has a portable `plugin.json` and a Codex compatibility manifest.

Run `/plugins` to inspect the installation, then start a new session. Select the skill shown by its plugin or skill picker. Refresh the Git marketplace explicitly with:

```sh
codex plugin marketplace upgrade odestroyero-skills
```

Automatic refresh of custom marketplaces depends on the Codex host and version. Verify it in your client before removing a scheduled updater. Official OpenAI documentation describes [marketplace commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin-marketplace) and [plugin loading](https://learn.chatgpt.com/docs/plugins#plugin-directory-in-codex-cli).

## Cursor

On Teams or Enterprise, open **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace**. Choose **Import from Repo** and enter `https://github.com/oDestroyeRo/skills`. Select `mattpocock`, `pstack`, and/or `tstack` in **Customize**.

Enable **Auto Refresh** in the marketplace settings and grant the Cursor GitHub App access to this repository. Import the whole repository so refresh also reads catalog changes. Existing Cloud Agents keep their starting versions; start a new agent after an update.

For local testing, copy each complete folder into Cursor's local-plugin directory:

```text
plugins/mattpocock/ → ~/.cursor/plugins/local/mattpocock/
plugins/pstack/     → ~/.cursor/plugins/local/pstack/
plugins/tstack/     → ~/.cursor/plugins/local/tstack/
```

Reload Cursor after copying. A symlink to a checkout outside that local-plugin directory is not a supported substitute. Public Marketplace listing requires submission and review. See [Cursor installation and refresh](https://cursor.com/docs/plugins#keep-plugins-up-to-date).

## Pi

Install the per-collection local packages from a checkout:

```sh
pi install /absolute/path/to/skills/plugins/mattpocock
pi install /absolute/path/to/skills/plugins/pstack
pi install /absolute/path/to/skills/plugins/tstack
```

Each package's `pi.skills` entry selects only that collection. Local packages load from their folder. A scheduled `python3 scripts/skills.py update` keeps the checkout current; run `/reload` in Pi if the session has stale skills.

After publishing the separate npm packages, you can install them from the registry:

```sh
pi install npm:@odestroyero/mattpocock-skills
pi install npm:@odestroyero/pstack-skills
pi install npm:@odestroyero/tstack-skills
pi update --extensions
```

For startup and reload refresh without a persistent package declaration, launch with an unpinned npm package, for example `pi -e npm:@odestroyero/mattpocock-skills`. Repeat `-e` for each additional package. Exact npm versions, Git tags, and commit pins keep their selected version. See [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

## OpenCode v2

Install the Git subdirectory packages you want:

```sh
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/mattpocock'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/pstack'
opencode plugin add 'github:oDestroyeRo/skills#main::path:plugins/tstack'
```

For local testing, select the folders in `opencode.json` or `opencode.jsonc`:

```json
{
  "plugins": [
    "/absolute/path/to/skills/plugins/mattpocock",
    "/absolute/path/to/skills/plugins/pstack",
    "/absolute/path/to/skills/plugins/tstack"
  ]
}
```

Each adapter targets `@opencode/plugin` 2.2.5 and registers only its collection through the v2 skill transform API. Upstream agents, hooks, and services still require their own configuration. OpenCode v1 has a different plugin API; use the shared installer there.

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
agy plugin list
```

Each folder has the Antigravity manifest, logo, suggested prompt, skills, and resources for that collection. Its standalone ZIP or tar.gz can also be extracted and installed as a local plugin.

After refreshing the checkout, re-run the local install and check the version with `agy plugin list`. Automatic updates for arbitrary Git or local installs have not been verified. Use shared folder installs with a scheduled repository updater when you need the existing automatic-refresh path.

For marketplace delivery, submit each standalone plugin through Antigravity's official intake after validation. See [plugin authoring](https://antigravity.google/docs/build-plugins) and [marketplace installation](https://antigravity.google/docs/marketplace).

## T3 Code

Install the collections through the provider you use in T3. Codex and Claude Code use the marketplace entries; Pi and OpenCode use their per-collection packages. Start a new provider session or refresh its picker after installation.

T3's provider integration determines native plugin discovery. If it does not expose a package, the shared installer can link the separate skills into provider folders:

```sh
python3 scripts/skills.py install --agent t3 --global
```

Keep the [T3 runtime adapter](harnesses.md#t3-code) for delegation and model settings, and read the [tstack runtime requirements](harnesses.md#tstack-workflows) before invoking its PR workflows. Personal `local/` skills use the shared installer; each native plugin mirrors its named upstream collection.
