---
name: agent-platform-access-audit
description: >-
  Audits AI agent data access, blast radius, and blocked policy operations in
  Google Cloud by querying Cloud Audit Logs via BigQuery. Use when
  investigating what resources or services an agent accessed, identifying top
  originating principals the agent is acting as, or triaging PERMISSION_DENIED
  errors to distinguish VPC Service Controls perimeter violations from IAM
  permission denials. Don't use for configuring Cloud Monitoring alert policies,
  modifying IAM policies or VPC Service Controls perimeters, querying non-audit
  application logs, or performing write operations.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/agent-platform-access-audit/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/agent-platform-access-audit/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
