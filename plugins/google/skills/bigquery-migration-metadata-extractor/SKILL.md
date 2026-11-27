---
name: bigquery-migration-metadata-extractor
description: >-
  Extracts database catalog metadata and query logs from data warehouses by
  running the DWH migration extractor locally or on a temporary Google Cloud VM
  through the BigQuery Migration Cloud Extractor (credentials held in Secret
  Manager), and inspects extracted `.zip` archives to report object and volume
  statistics. Use when extracting database metadata or query logs from
  Snowflake, Redshift, Teradata, Oracle, PostgreSQL, SQL Server, Hive, etc.,
  deciding between local and cloud (Cloud Extractor) extraction, or inspecting
  extracted dwh-migration-*.zip archives to print post-extraction statistics.
  Don't use for SQL dialect translation (use bigquery-migration-sql-translator),
  exporting table data to Parquet or CSV files (such as Snowflake `COPY INTO`
  unloads) or loading it into BigQuery (use the BigQuery Data Transfer Service
  or bigquery-basics), or validating migrated data.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/bigquery-migration-metadata-extractor/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/bigquery-migration-metadata-extractor/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
