---
name: gke-workload-security
description: >-
  Audits, configures, and hardens workload-level security controls for Google
  Kubernetes Engine (GKE) applications and namespaces. Covers running security
  audits (`audit_cluster.sh`), enforcing Network Policies (default-deny and Dataplane
  V2 logging), isolating high-risk pods inside GKE Sandbox (`gVisor`), enforcing Pod
  Security Standards (`restricted` labeling) and pod securityContext, and mounting Secret Manager secrets via
  CSI (`SecretProviderClass`). Use when auditing workload security posture, isolating
  namespaces, applying pod security standards, or
  configuring network policies and secret volume mounts. Don't use for Workload Identity (use gke-workload-identity), cluster-wide
  control plane security, RBAC hardening, Binary Authorization, Shielded Nodes,
  or enabling platform-level GKE add-ons (use gke-platform-security instead).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-workload-security/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-workload-security/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
