---
name: pstack-principle-fix-root-causes
description: "Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate."
disable-model-invocation: true
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/pstack/skills/principle-fix-root-causes/SKILL.md) before doing the task.

Resolve `../../upstream/pstack/skills/principle-fix-root-causes/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](../../upstream/pstack). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
