---
name: gke-platform-security
description: >-
  Plans, configures, and hardens platform-level Google Kubernetes Engine (GKE)
  cluster security. Covers cluster add-ons (Secret Manager enablement), RBAC
  hardening (disabling insecure bindings, audit tools), Binary Authorization,
  Secrets Encryption (--database-encryption-key), Security Posture (--security-posture),
  enabling Shielded Nodes, GKE Sandbox cluster enablement, GKE IAM roles, and
  cross-service authentication IAM patterns. Use when securing cluster control
  planes, hardening GKE RBAC, enabling Shielded Nodes, enabling GKE Sandbox runtime,
  enabling cluster-wide security add-ons, or managing GKE IAM roles. Don't use
  for Workload Identity (use gke-workload-identity) or workload-level security
  (SecretProviderClass, PSS, NetPol, gVisor pod runtimeClassName; use gke-workload-security).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-platform-security/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-platform-security/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
