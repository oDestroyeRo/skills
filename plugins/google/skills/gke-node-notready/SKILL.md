---
name: gke-node-notready
description: >-
  Diagnoses GKE nodes reporting NotReady or Unknown status by inspecting node conditions, events, kubelet/containerd logs, and node metrics, then proposing safe remediations. Use when nodes show NotReady, when the kubelet stops posting node status, or when workloads are evicted or stuck Pending due to node health. Don't use for pod-level application failures (use gke-workload-troubleshooting), autoscaler scale-up/scale-down decisions (use gke-cluster-autoscaler), or non-GKE compute.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-node-notready/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-node-notready/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
