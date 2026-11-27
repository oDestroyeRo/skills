---
name: bigquery-migration-data-exporter
description: >-
  Generates type-safe, schema-aligned database data export SQL files (.sql) for
  Snowflake, Databricks, Teradata, Oracle, and PostgreSQL directly from
  BigQuery Migration Service (BQMS) translation_output/metadata
  configs, exporting into target file formats (such as Parquet). Use when
  generating source database export SQL scripts for BigQuery ingestion without
  connecting to the source database. Don't use for executing SQL against source
  databases or streaming/staging exported files, extracting source database
  catalog metadata, translating SQL queries or DDL schemas (use
  bigquery-migration-sql-translator), loading staged Parquet files into
  BigQuery, or running post-migration data validation.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/bigquery-migration-data-exporter/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/bigquery-migration-data-exporter/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
