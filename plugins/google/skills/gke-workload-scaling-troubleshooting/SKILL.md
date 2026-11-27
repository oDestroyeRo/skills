---
name: gke-workload-scaling-troubleshooting
description: >-
  Diagnoses GKE HorizontalPodAutoscaler (HPA) failures — metrics showing as
  <unknown>, FailedGetResourceMetric / FailedGetScale / FailedComputeMetricsReplicas
  events, missing Pod resource requests, custom/external metrics-pipeline breakage
  (FailedGetExternalMetric / FailedGetCustomMetric, unavailable metrics adapter,
  control-plane firewall blocking the adapter), HPA that won't scale up or down
  (tolerance / stabilization window / unavailable rate metrics), scale-to/from-zero
  problems, and slow HPA reaction on large clusters. Use when an HPA isn't scaling a
  workload as expected or reports metric errors. Don't use for configuring or
  authoring new HPA/VPA objects or scaling best practices (see the
  gke-workload-scaling skill), or for Cluster Autoscaler / node-pool sizing.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-workload-scaling-troubleshooting/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-workload-scaling-troubleshooting/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
