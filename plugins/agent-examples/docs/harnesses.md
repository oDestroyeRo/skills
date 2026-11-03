# Using the shared skills

Resolve this adapter file to its real path before following its relative links.

Each entry point lives under `plugins/<collection>/skills/` and opens the original workflow under that plugin's `upstream/` directory. Folder installations link to the same entry points. Resolve the entry point to its real path before following its links. Read the original workflow before acting, and resolve its file references from its real location. For example, `pstack-poteto-mode` opens the plugin's `upstream/pstack/skills/poteto-mode/SKILL.md`; its sibling skills, playbooks, docs, and agent prompts remain in their original layout.

The entry point's collection prefix resolves name collisions. A reference to `tdd` inside a pstack workflow means `pstack-tdd`; inside Matt's workflow it means `mattpocock-tdd`. tstack's references follow the same rule: `full-send` means `tstack-full-send`, for example. Read a related skill's source file directly when a harness has no way to invoke it by name. Paths and metadata are in each plugin's `skills/catalog.json`.

## Shared capabilities

Use the current harness's actual tool schemas and the user's saved settings. Map an action such as searching files, asking a question, or running a command to the available equivalent. A skill cannot register an agent type, install a hook, add MCP tools, or make a provider's model available. If a required capability is missing, report that step and its effect on completion. Preserve the user's scope and authorization for external actions.

When pstack names `poteto-agent` or `comment-sicko`, read the matching prompt under the packaged `upstream/pstack/agents/` directory. Follow the entry point's upstream-library link to find it. Supply those instructions to a supported delegate rather than passing an unregistered agent type. If delegation is unavailable, say so; do not claim an independent review ran. Cursor Automations, Bugbot, and cloud agents still require those services.

## tstack workflows

tstack includes PR preparation, review, monitoring, and merge workflows. `full-send` uses `sol-loop`, `file-pr`, and `babysit-pr`; `full-stop` builds on `full-send`. The complete collection is bundled so these references resolve within `upstream/tstack/skills/`.

Its PR workflows require an authenticated GitHub CLI (`gh`). The bundled `babysit-pr/scripts/pr-wait` helper requires Python 3 and retains its executable permission. `council` and `sol-loop` need subagent and model access; cross-provider review needs the corresponding providers to be available. Use the current harness's tools and the user's configured models. T3-specific tools are optional where the upstream workflow supplies a native fallback. Follow the running T3 session's orchestration rules when using them.

Read a workflow before invoking it. `full-send` includes pushing branches, filing PRs, and merging them. `full-stop` performs the preparation and review, then leaves the PR open for the user to merge. Follow the user's scope and the current session's authorization rules for those actions. See the [tstack README](https://github.com/t3dotgg/tstack#readme) for upstream workflow requirements.

## Anthropic workflows

The `agent-examples` plugin includes skills with approved Apache 2.0 license files. Its source snapshot and bundle omit the restricted document skills and the unlicensed `doc-coauthoring` skill. The bundle's `THIRD_PARTY_NOTICES.md` links to the original skill licenses, dependency notices, and font notices. Preserve those files when redistributing a bundle.

Use the current provider's equivalent tools when an upstream workflow names Claude-specific tools. Some helpers require additional software: Python and Playwright for web testing, Node/npm tooling for web artifacts, Python imaging libraries and FFmpeg for GIF workflows, and the Claude CLI for skill-creator's description optimization. Follow the selected workflow's dependency instructions. The packaged helper archive and font files are resources for those workflows. Adapt example paths such as `/mnt/user-data/outputs/` to the current environment.

The `claude-api` skill documents Anthropic's API and SDKs. It does not add a provider connection or API credentials to the current environment. Native Claude commands use names such as `/agent-examples:anthropic-frontend-design`; folder installs use `/anthropic-frontend-design`. See the [upstream overview](https://github.com/anthropics/skills#readme).

## T3 Code

T3 uses its selected provider's discovery paths. The `t3` install profile installs the same library for Codex, Claude Code, Pi, OpenCode, Cursor, and Antigravity, including Antigravity CLI's additional path. There is no invented `~/.t3/skills` directory.

Use the orchestration instructions supplied by the running T3 session. For a delegate requiring a different provider, explicit model settings, background work, or an isolated checkout, use `delegate_task` when available. Read `orchestrator_capabilities` before the first such delegate and pass saved model and effort choices through `target`. Follow the returned continuation instructions. Same-provider work that meets the session's native-agent conditions can use its native tool. If the chosen provider cannot run a requested role, report the unavailable capability and follow the user's existing fallback preference.

Refresh the skill picker or start a new provider session after first installation. This repo verifies files and paths; it does not claim every T3 provider or upstream workflow has been exercised live. T3's current [Claude discovery source](https://github.com/pingdotgg/t3code/blob/61c3794c32b0eeebfac09add43e403618c65d2d7/apps/server/src/provider/Drivers/ClaudeSkills.ts) and [Antigravity discovery source](https://github.com/pingdotgg/t3code/blob/61c3794c32b0eeebfac09add43e403618c65d2d7/apps/server/src/provider/Drivers/AntigravitySkills.ts) establish the extra profile paths.

## Codex

Use native Codex tools and available delegate roles. Cursor `Task` model identifiers and agent types are not Codex tool parameters. Keep the user's configured models and approval rules. Source-provided `agents/openai.yaml` metadata is exposed when present, with its default prompt updated to the exported skill name. Other metadata, including invocation policy, is preserved. This metadata does not register separate subagent roles. See [official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

When using pstack, read `docs/harness/claude-code.md` inside the upstream library linked by the entry point. The [upstream Claude adapter](https://github.com/cursor/plugins/blob/main/pstack/docs/harness/claude-code.md) maps Cursor tools and model settings. Shared folder installs use `/pstack-poteto-mode`; the native plugin uses `/pstack:pstack-poteto-mode`. Matt's native commands use `/mattpocock:mattpocock-<name>`, and tstack uses `/tstack:tstack-<name>`, such as `/tstack:tstack-full-stop`. Related skills keep the same plugin and collection prefixes. Bundled agent prompts must be supplied to available delegates because these packages register skills only. See [Claude's skill documentation](https://code.claude.com/docs/en/skills).

## Pi

Use Pi's installed tools and extensions. A subagent extension is required for workflows that need delegation; copying an agent prompt does not install one. Run `/reload` after installing or updating if the current session has stale skills. See [Pi's skill documentation](https://pi.dev/docs/latest/skills).

## Antigravity

The global target is the current App/CLI/IDE shared directory, `~/.gemini/config/skills`. The T3 profile also installs into `~/.gemini/antigravity-cli/skills`. Current project discovery uses `.agents/skills`. Older IDE builds may need `--directory ~/.gemini/antigravity/skills` or `--directory /path/to/project/.agent/skills`.

Antigravity documents external skill discovery, but its symlink behavior has not been verified in a running client here. If a version does not discover the installed links, add this repo's `skills/` directory to the documented `~/.gemini/config/skills.json` external-path manifest using that version's schema. Use `/skills reload` in the CLI if necessary. See [skills](https://antigravity.google/docs/skills) and [discovery](https://antigravity.google/docs/customization-discovery).

## OpenCode and Cursor

OpenCode uses its native tools and configured agents; permission rules still apply. Cursor can use pstack's original tool vocabulary, but this repo's packages register skills rather than upstream agents or automations. For upstream's complete native plugin behavior, use its own plugin installation. See [OpenCode skills](https://opencode.ai/docs/skills/) and the [pstack README](https://github.com/cursor/plugins/blob/main/pstack/README.md).
