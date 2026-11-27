---
name: api-gateway-backend-security-and-rate-limiting
description: >-
  Secures and rate limits backend services behind Google Cloud API Gateway
  across OpenAPI 2.0 and OpenAPI 3.x API configurations, including MCP-enabled
  gateways. Use when configuring API key or JWT authentication, locking down
  Cloud Run or Cloud Run functions backends with a gateway service account,
  reading authenticated claims from X-Apigateway-Api-Userinfo, setting
  per-project request quotas, or changing quota metrics without the HTTP 500
  "Failed to call Service Control Quota" error on older gateways. Do not use for
  finding the cause of failing requests from gateway logs, such as an
  unexplained HTTP 429 or 5xx (use api-gateway-troubleshooting), writing or
  migrating a whole spec (use api-gateway-openapi-spec-authoring), MCP tool
  setup (use api-gateway-mcp-server), Apigee, GKE Gateway API, Cloud Load
  Balancing custom domain setup, or LLM model routing.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/api-gateway-backend-security-and-rate-limiting/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/api-gateway-backend-security-and-rate-limiting/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
