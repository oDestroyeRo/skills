---
name: pstack-principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
disable-model-invocation: true
---

Read the complete [upstream skill](source/SKILL.md) before doing the task.

Resolve `source/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](library). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](harness.md) and apply the section for the current harness.
