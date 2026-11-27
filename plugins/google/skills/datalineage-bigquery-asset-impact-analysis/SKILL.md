---
name: datalineage-bigquery-asset-impact-analysis
description: >-
  Analyzes the downstream impact (blast radius) using data lineage on Google Cloud when a BigQuery table or view is broken, stale, or modified.
  Identifies all downstream tables, dashboards, and processes that will be affected.
  Use when:
  - Performing a blast radius or impact analysis for a BigQuery table or view.
  - Assessing the consequences of modifying, deleting, or pausing updates to a BigQuery asset.
  - Identifying downstream dependencies (tables, dashboards, processes) of a BigQuery asset.
  Don't use for:
  - General BigQuery querying or data analysis (use BigQuery-related tools instead).
  - Non-BigQuery assets (e.g., Cloud Storage files) unless they are part of the BigQuery lineage.
  - Creating or modifying lineage links directly.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/datalineage-bigquery-asset-impact-analysis/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/datalineage-bigquery-asset-impact-analysis/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
