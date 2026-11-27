---
name: gke-capacity-triage
description: >-
  Triage a GKE workload stuck Pending because node provisioning fails with a
  Compute Engine capacity error (ZONE_RESOURCE_POOL_EXHAUSTED, "GCE out of
  resources", scale.up.error.out.of.resources) or a quota error
  (QUOTA_EXCEEDED). Separates resource unavailability from quota limits and
  configuration causes, explains why the ComputeClass fallback didn't help,
  and gives the documented ComputeClass, Pod-level, or cluster-level fix to
  apply. Use when a user pastes a scale-up failure alert or asks why Pods
  are stuck Pending, lack nodes, or hit a stockout. Don't use for
  Standard-cluster TPU slices whose specific reservation lacks consumable
  instances, such as one held by unhealthy node pools with auto-repair
  disabled (gke-ai-troubleshooting-tpu-reservation-stockout), autoscaler
  enablement, profiles, or scale-down (gke-cluster-autoscaler), ComputeClass
  authoring without an incident (gke-compute-classes), Pods already on a
  node (gke-workload-troubleshooting, gke-storage-troubleshooting), or
  non-GKE clusters.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-capacity-triage/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-capacity-triage/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
