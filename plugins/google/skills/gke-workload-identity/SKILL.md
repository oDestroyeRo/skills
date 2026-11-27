---
name: gke-workload-identity
description: >-
  Configures and diagnoses Workload Identity Federation for GKE authentication failures for Pods
  (403 "iam.serviceAccounts.getAccessToken" / permission denied, "could not find
  default credentials", or GKE metadata server unreachable) by verifying
  cluster and node-pool Workload Identity configuration, the Kubernetes
  ServiceAccount (KSA) to IAM binding (direct principal binding and legacy Google
  ServiceAccount impersonation), target-resource IAM roles, and gke-metadata-server
  health. Use when setting up KSA/GSA bindings (`roles/iam.workloadIdentityUser`,
  `iam.gke.io/gcp-service-account`) or when a Pod cannot authenticate to Google Cloud APIs. Don't use for in-cluster
  Kubernetes RBAC errors (API-server authorization), general workload crashes
  (use gke-workload-troubleshooting), or Pod Security Standards and NetworkPolicies
  (use gke-workload-security).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-workload-identity/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-workload-identity/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
