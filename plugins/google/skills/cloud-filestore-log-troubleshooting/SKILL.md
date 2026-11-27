---
name: cloud-filestore-log-troubleshooting
description: >-
  Diagnoses and resolves Filestore client mount failures on Google Cloud,
  permission errors (EACCES), and network timeouts (ETIMEDOUT). Use when an NFS
  mount hangs or fails from a Compute Engine VM, GKE pod, Cloud Run service, or
  Vertex AI workload, when `mount.nfs` reports "Connection timed out" or "access
  denied by server", when checking whether VPC ingress firewall rules or
  `nfsExportOptions` allow a client IP, or when a previously working Filestore
  share suddenly stops mounting after an administrative change. Don't use for
  Cloud Storage (GCS) buckets, Persistent Disk, or Cloud NetApp Volumes, and
  don't use for Filestore capacity scaling or backup and export-policy auditing.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/google-cloud-filestore-log-troubleshooting/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/google-cloud-filestore-log-troubleshooting/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
