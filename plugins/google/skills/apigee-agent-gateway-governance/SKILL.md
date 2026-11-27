---
name: apigee-agent-gateway-governance
description: >-
  Stands up an Apigee API proxy that a Google Cloud Agent Gateway calls as an
  ext-proc (Service Extension) callout on an agent's LLM traffic, to meter
  token usage per model, extract caller identity, and apply Model Armor prompt
  screening or a semantic cache. Use when wiring Apigee in as an AI gateway
  behind an Agent Gateway, when an agent's model egress needs governing, or
  when a callout proxy returns no verdict and you need to find out why. The
  distinguishing question is whether Apigee forwards the traffic or only
  inspects it: this skill is inspect-only, and builds the proxy itself. Don't
  use it when Apigee is meant to receive a request and route it onward to a
  backend — including hosting an MCP server behind Apigee — which needs a proxy
  with a target instead. Don't use for governing the agent's calls to tools or
  MCP servers. Don't use for choosing or switching which model a request goes
  to. Don't use for creating the Agent Gateway itself, nor for Apigee hybrid.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/apigee-agent-gateway-governance/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/apigee-agent-gateway-governance/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
