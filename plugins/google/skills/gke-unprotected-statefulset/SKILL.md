---
name: gke-unprotected-statefulset
description: >-
  Audits, detects, and proposes fixes for GKE StatefulSets that lack a matching
  PodDisruptionBudget (PDB) to prevent simultaneous Pod evictions during
  voluntary node drains (GKE insight subtype PDB_UNPROTECTED_STATEFULSET). Use
  when investigating the PDB_UNPROTECTED_STATEFULSET insight, checking whether
  GKE StatefulSets have a matching PDB, or proposing fixes for selector
  mismatches where an existing PDB does not match the StatefulSet's
  .spec.selector. Don't use for existing PDBs that allow zero disruptions or
  block node drains (PDB_UNPERMISSIVE), general probe and PDB setup unrelated
  to this insight (use gke-reliability), upgrade planning (use gke-upgrades),
  Pods stuck in Pending (use gke-workload-troubleshooting), node autoscaling or
  capacity stockouts (use gke-cluster-autoscaler), ComputeClass configuration
  (use gke-compute-classes), or general Kubernetes manifest generation (use
  gke-manifest-generation).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-unprotected-statefulset/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-unprotected-statefulset/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
