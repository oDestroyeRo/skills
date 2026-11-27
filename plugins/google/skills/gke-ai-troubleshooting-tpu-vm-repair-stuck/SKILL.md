---
name: gke-ai-troubleshooting-tpu-vm-repair-stuck
description: >-
  Diagnose GKE TPU VM instances stuck in Compute Engine repair (REPAIRING state)
  after host errors, maintenance events, or faulty host reports in single-host,
  multi-host, dynamic slicing, and TPU All Capacity mode node pools. Use when
  TPU instances in a slice node pool remain in REPAIRING, host error events
  appear in audit logs, or TPU slices are unschedulable due to a VM in repair.
  Don't use for nodes reporting Ready: Unknown when no VM is in REPAIRING (use
  gke-ai-troubleshooting-node-unresponsive-timeout), other NotReady nodes when
  no VM is in REPAIRING (use gke-node-notready), Pending Pods when all nodes are
  Ready (use gke-workload-troubleshooting), JobSet preemption events (use
  gke-ai-troubleshooting-jobset-interruption), or Slice custom resource
  lifecycle failures (use gke-ai-troubleshooting-tpu-dynamic-slices-monitoring).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-ai-troubleshooting-tpu-vm-repair-stuck/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-ai-troubleshooting-tpu-vm-repair-stuck/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
