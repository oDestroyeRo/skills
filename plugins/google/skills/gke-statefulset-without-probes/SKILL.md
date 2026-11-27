---
name: gke-statefulset-without-probes
description: >-
  Audits, detects, and proposes fixes for GKE StatefulSets that are protected
  by a PodDisruptionBudget (PDB) but lack container readiness probes (GKE
  insight subtype PDB_STATEFULSET_WITHOUT_PROBES), causing replacement Pods to
  be counted as healthy before they are ready during voluntary disruptions. Use
  when asked to check, audit, or propose fixes for the
  PDB_STATEFULSET_WITHOUT_PROBES condition, missing readinessProbe
  configurations on PDB-protected GKE StatefulSets, or premature eviction of
  StatefulSet replicas during node pool upgrades or drains despite having a
  PDB. Don't use for StatefulSets missing a PDB (PDB_UNPROTECTED_STATEFULSET),
  PDBs that allow zero disruptions (PDB_UNPERMISSIVE), general probe and PDB
  setup unrelated to this condition (use gke-reliability), Pods stuck in
  Pending (use gke-workload-troubleshooting), ComputeClass configuration (use
  gke-compute-classes), manifest generation (use gke-manifest-generation), or
  cluster upgrade planning (use gke-upgrades).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-statefulset-without-probes/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-statefulset-without-probes/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
