---
name: pstack-principle-migrate-callers-then-delete-legacy-apis
description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
disable-model-invocation: true
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) before doing the task.

Resolve `../../upstream/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](../../upstream/pstack). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
