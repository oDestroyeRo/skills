---
name: mongodb-mongodb-natural-language-querying
description: Generate read-only MongoDB queries (find) or aggregation pipelines using natural language, with collection schema context and sample documents. Use this skill whenever the user asks to write, create, or generate MongoDB queries, wants to filter/query/aggregate data in MongoDB, asks "how do I query...", needs help with query syntax, or discusses finding/filtering/grouping MongoDB documents. Also use for translating SQL-like requests to MongoDB syntax. Does NOT handle Atlas Search ($search operator), vector/semantic search ($vectorSearch operator), fuzzy matching, autocomplete indexes, or relevance scoring - use search-and-ai for those. Does NOT analyze or optimize existing queries - use mongodb-query-optimizer for that. Does NOT handle aggregation pipelines that involve write operations. Requires MongoDB MCP server.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/mongodb/skills/mongodb-natural-language-querying/SKILL.md) before doing the task.

Resolve `../../upstream/mongodb/skills/mongodb-natural-language-querying/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill from this collection, use `mongodb-<name>` or read that skill directly in [the upstream library](../../upstream/mongodb). Keep this collection's skills together when names overlap with another collection.

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
