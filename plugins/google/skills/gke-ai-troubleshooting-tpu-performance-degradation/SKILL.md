---
name: gke-ai-troubleshooting-tpu-performance-degradation
description: >-
  Diagnose GKE Cloud TPU training throughput drops and step-time regressions
  (15%+ TPU duty-cycle drop) using ML Diagnostics Workload Monitoring (`gcloud
  alpha mldiagnostics monitored-events` /
  `hypercomputecluster.googleapis.com/v1alpha`) and 1-minute Cloud Monitoring
  system metrics (`kubernetes.io/node/accelerator/*`). Distinguishes hardware
  and network fabric throttling from workload resource bottlenecks (HBM
  capacity, host memory, or host CPU saturation). Use when TPU training
  throughput or duty cycle drops without crashing pods, when
  `PERFORMANCE_DEGRADATION` monitored events fire, or when triaging slow
  multi-slice training steps. Don't use for complete multi-slice XLA execution
  stalls with `HANG_DETECTED` logs (use gke-ai-troubleshooting-tpu-mxla-hang) or
  pod eviction/interruption restarts (use
  gke-ai-troubleshooting-jobset-interruption).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-ai-troubleshooting-tpu-performance-degradation/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-ai-troubleshooting-tpu-performance-degradation/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
