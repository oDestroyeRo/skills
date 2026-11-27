---
name: pathways-workload
description: >-
  Debugs failed, crashing or hung Pathways on Cloud workloads (JAX training or
  inference on Cloud TPU in GKE, run as a JobSet, PathwaysJob or
  LeaderWorkerSet). Reads Cloud Logging for every Pathways container (user
  workload, IFRT proxy, pathways-rm, pathways-worker, colocated Python
  sidecar), node kernel logs and GKE events, then reports the earliest real
  error, the root cause and a fix. Use when a Pathways workload fails to start,
  crashes, restarts or stops making progress, or shows errors such as IFRT
  proxy connection failures, DEADLINE_EXCEEDED lost connection to peer, host
  OOM kills, ImagePullBackOff, or JAX and Pathways version mismatches. Don't
  use for GKE workloads that don't use Pathways, or for creating clusters or
  deploying new Pathways workloads.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/pathways-workload/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/pathways-workload/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
