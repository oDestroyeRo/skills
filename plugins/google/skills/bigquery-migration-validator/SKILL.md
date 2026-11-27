---
name: bigquery-migration-validator
description: >-
  Validates that tables migrated to BigQuery match their source (Teradata,
  Snowflake, Oracle, Redshift, Databricks, PostgreSQL, SQL Server, MySQL,
  MariaDB, Hive, Impala, Vertica) with the BigQuery Migration Service (BQMS)
  validation tool: schema and data type comparison, column aggregate
  comparison, and row-level data comparison. Use when generating or editing a
  validation config, running a validation, choosing sampling or partitioning,
  fixing connection or driver errors, or investigating validation results in
  BigQuery and Cloud Storage to decide which mismatches to fix. Don't use for
  SQL translation (use bigquery-migration-sql-translator), extracting source
  database catalog metadata or query logs, generating SQL scripts (such as COPY
  INTO) or exporting or unloading source tables to Parquet on Cloud Storage,
  loading staged files into BigQuery (such as bq load), or general BigQuery
  query failures and tuning (use bigquery-troubleshooting or
  bigquery-optimization).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/bigquery-migration-validator/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/bigquery-migration-validator/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
