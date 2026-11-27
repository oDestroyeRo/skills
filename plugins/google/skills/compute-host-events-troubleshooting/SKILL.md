---
name: compute-host-events-troubleshooting
description: >-
  Investigates, diagnoses, and mitigates Google Compute Engine virtual
  machine (VM) host events, including planned infrastructure maintenance
  (migrateOnHostMaintenance, terminateOnHostMaintenance), physical host hardware
  errors (hostError), guest OS terminations (guestTerminate), and Spot or
  Preemptible VM preemptions (compute.instances.preempted) using shutdown-script
  metadata. Use ONLY when an existing Compute Engine VM unexpectedly reboots,
  stops, crashes, is preempted, or becomes unresponsive due to physical host
  maintenance, hardware errors, or Local SSD recovery. DO NOT read or use for
  creating new standalone VMs, Managed Instance Group (MIG) autoscaler scale-out
  or scale-in failures, Google Kubernetes Engine (GKE) clusters, application OOM
  debugging, or VPC firewall issues.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/compute-host-events-troubleshooting/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/compute-host-events-troubleshooting/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
