---
name: pstack-blast-radius
description: "Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust."
disable-model-invocation: true
---

Read the complete [upstream skill](source/SKILL.md) before doing the task.

Resolve `source/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](library). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](harness.md) and apply the section for the current harness.
