---
name: agent-platform-deploy
description: >-
  Deploy open models or custom weights from Model Garden to Agent Platform
  endpoints, check the status of an in-progress deployment operation, or clean
  up resources by undeploying models and deleting endpoints. Use when asked to
  actively deploy a model, list the Model Garden CATALOG of available models,
  check if a specific model is deployable
  (`gcloud ai model-garden models list-deployment-config`), query deployment
  cost, troubleshoot deployment errors (like quota limits), or undeploy/clean
  up endpoints. Also use when copying and deploying a 1P Tuned Model. Don't
  use for pure listing/discovery questions of the form "is X deployed?",
  "list my endpoints", or "which regions have models running?" — for those
  use `agent-platform-endpoint-management`. Don't use for running model evaluations
  (use `agent-platform-eval-flywheel` skill).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/agent-platform-deploy/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/agent-platform-deploy/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
