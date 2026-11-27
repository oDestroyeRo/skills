---
name: bigquery-migration-data-loader
description: >-
  Provisions BigQuery datasets, ingests staged Parquet files directly into
  native BigQuery tables by using bq load, and deploys already-translated views
  from local or Cloud Storage BigQuery Migration Service (BQMS) translation
  outputs. Use when provisioning target BigQuery datasets for warehouse
  migrations, batch loading staged Parquet files into native BigQuery tables by
  using bq load, auditing loaded table row counts, or deploying
  already-translated BigQuery views into a target dataset. Don't use for
  extracting source database catalog metadata, translating SQL queries, views,
  stored procedures, or DDL schemas to GoogleSQL (use
  bigquery-migration-sql-translator), exporting or unloading source database
  tables (such as Snowflake, Databricks, Teradata, or Oracle) to Parquet on
  Cloud Storage, or running post-migration cross-database data validation.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/bigquery-migration-data-loader/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/bigquery-migration-data-loader/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
