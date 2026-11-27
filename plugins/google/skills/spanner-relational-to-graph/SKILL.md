---
name: spanner-relational-to-graph
description: >-
  Analyzes existing Spanner relational schemas on Google Cloud (DDL, foreign
  keys, interleaved tables, and junction tables) and generates
  `CREATE PROPERTY GRAPH` DDL statements (`NODE TABLES`, `EDGE TABLES`) without
  modifying underlying relational tables. Use when mapping existing Spanner
  tables to a Spanner Graph, identifying node and edge candidates from
  relational tables, creating SQL bridge views for implicit `ARRAY`/`JSON` or
  type-mismatched relationships, mapping polymorphic or self-referential tables,
  or troubleshooting `CREATE PROPERTY GRAPH` DDL compiler errors. Don't use for
  greenfield physical table design (use spanner-graph-schema-best-practices) or
  tuning slow ISO GQL queries (use spanner-graph-query-tuning).
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/spanner-relational-to-graph/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/spanner-relational-to-graph/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
