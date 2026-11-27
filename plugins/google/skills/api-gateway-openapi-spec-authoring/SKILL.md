---
name: api-gateway-openapi-spec-authoring
description: >-
  Writes, migrates, and fixes OpenAPI specs for Google Cloud API Gateway. Use
  when converting an OpenAPI 2.0 (Swagger) spec to OpenAPI 3.x, writing a new
  OpenAPI 3.x spec, or fixing a failed "gcloud api-gateway api-configs create",
  such as "extension is only supported in OpenAPI 2.x". Also use when quotas
  set with x-google-quota are never enforced, or when a backend receives path
  parameters as query parameters. Don't use for adding or debugging MCP tools
  (use api-gateway-mcp-server), adding or changing API key, JWT, or quota
  settings in a working spec, or backend lockdown (use
  api-gateway-backend-security-and-rate-limiting), failing requests or service
  account and concurrency errors (use api-gateway-troubleshooting), Cloud
  Endpoints, Apigee, or GKE Gateway API.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/api-gateway-openapi-spec-authoring/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/api-gateway-openapi-spec-authoring/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
