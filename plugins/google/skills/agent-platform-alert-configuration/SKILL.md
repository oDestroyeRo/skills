---
name: agent-platform-alert-configuration
description: >-
  Configures best-practice alerting policies for AI agents using OpenTelemetry
  (OTel) metrics, generating output as Terraform (.tf) configuration files.
  Use when analyzing, writing, or deploying alerting policies
  to monitor agent latency, error rates, token usage, and quality metrics.
  Don't use for standard infrastructure monitoring unrelated to AI agents,
  or when the agent is not instrumented with OpenTelemetry (for Reliability, Cost, Safety, Security alerts).
  NOTE: Reliability, Cost, Safety, and Security alerts use generic OTel metrics
  and work across runtimes (such as Cloud Run, Vertex AI). Quality alerts rely
  on Vertex AI Online Monitors and are strictly bound to Vertex AI deployments.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/agent-platform-alert-configuration/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/agent-platform-alert-configuration/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
