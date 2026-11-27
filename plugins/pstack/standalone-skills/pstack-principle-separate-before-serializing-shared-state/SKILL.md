---
name: pstack-principle-separate-before-serializing-shared-state
description: "Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) before doing the task.

Resolve `../../upstream/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](../../upstream/pstack). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
