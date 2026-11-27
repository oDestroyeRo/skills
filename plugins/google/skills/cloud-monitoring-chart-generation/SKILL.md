---
name: cloud-monitoring-chart-generation
description: >-
  Generates Cloud Monitoring Server-Driven UI (SDUI) Widget and XyChart Protocol
  Buffer textprotos on Google Cloud from resolved PromQL or ListTimeSeries
  queries.
  Use when:
    - Generating valid google.monitoring.dashboard.v1.Widget textprotos,
      containing PrometheusQuery or TimeSeriesFilter datasets, for use with the Cloud Monitoring
      Dashboards API, gcloud CLI, or declarative dashboard definitions.
    - Synthesizing Server-Driven UI (SDUI) widget titles, axis labels, and
      plot types for Prometheus or ListTimeSeries queries.
  Don't use for:
    - Metric discovery or PromQL query generation. For those tasks, use the
      cloud-monitoring-metric-selection or cloud-monitoring-promql-query skills.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/cloud-monitoring-chart-generation/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/cloud-monitoring-chart-generation/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
