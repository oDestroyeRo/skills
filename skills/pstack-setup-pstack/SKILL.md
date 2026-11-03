---
name: pstack-setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

Read the complete [upstream skill](source/SKILL.md) before doing the task.

Resolve `source/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `pstack-<name>` or read that skill directly in [the upstream library](library). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](harness.md) and apply the section for the current harness.
