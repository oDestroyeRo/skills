---
name: gke-ai-troubleshooting-tpu-mxla-hang
description: >-
  Diagnose GKE Cloud TPU multi-slice training hangs (Megascale `HANG_DETECTED`
  logs and hang monitored events) using the ML Diagnostics `Megascale XLA (MXLA)
  Hang Analyzer` (`gcloud alpha mldiagnostics monitored-events`) and 1-minute
  Cloud Monitoring multi-slice latency metrics
  (`kubernetes.io/container/multislice/*`). Distinguishes XLA compiler/HLO
  launch divergence and host data-input stalls from TPU chip, SparseCore, ICI,
  or network fabric faults. Use when multi-slice TPU training jobs freeze
  without progressing steps, emit `HANG_DETECTED`, or stall in collective
  operations. Don't use for gradual step-time throughput drops without hangs
  (use gke-ai-troubleshooting-tpu-performance-degradation) or pod
  preemption/eviction restarts (use gke-ai-troubleshooting-jobset-interruption).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-ai-troubleshooting-tpu-mxla-hang/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-ai-troubleshooting-tpu-mxla-hang/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
