---
name: pstack-maintain-formal-verification-skill
description: "Bring a project's formal verification back in line with the code after the code changes: find the commits that touched verified code, update the model, harness, or properties to describe the code as it is now, rerun, and say whether each failure is drift in the verification or a bug in the code. Use for /maintain-formal-verification-skill, \"is the model still true to the code\", or after merges and refactors that touched verified code without rechecking it."
disable-model-invocation: true
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/pstack/skills/maintain-formal-verification-skill/SKILL.md) before doing the task.

Resolve `../../upstream/pstack/skills/maintain-formal-verification-skill/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](../../upstream/pstack). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
