---
name: gke-kueue-troubleshooting
description: Diagnose a GKE batch or AI workload (Job, JobSet, LeaderWorkerSet, RayJob, Kubeflow training jobs, or plain Pods) that is pending, suspended, stuck, evicted or misconfigured when Kueue manages it - from a live GKE cluster, a support bundle or exported controller/audit logs. Load it as soon as the investigation shows a Kueue footprint, even if the user never said "Kueue" - anything under kueue.x-k8s.io (labels, Pod scheduling gates, Workload/LocalQueue/ClusterQueue objects and their conditions), kueue-controller-manager events or logs, or a Job with spec.suspend=true together with a Workload object in its namespace. Scripts compact cluster state and logs into verifiable facts and validate the report, while the agent classifies the cause as Kueue configuration, Kueue defect, or outside Kueue. Don't use for workloads with no Kueue footprint (use gke-node-notready, gke-workload-scaling-troubleshooting, gke-ai-troubleshooting-tpu-reservation-stockout, or gke-ai-troubleshooting-jobset-interruption).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/gke-kueue-troubleshooting/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/gke-kueue-troubleshooting/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
