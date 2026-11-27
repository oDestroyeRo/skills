---
name: api-gateway-mcp-server
description: >-
  Configures Google Cloud API Gateway to act as a remote Model Context Protocol
  (MCP) server (Public Preview) that exposes REST APIs as agent tools over HTTP
  (POST /mcp). Use when exposing an API Gateway API as MCP tools, migrating
  OpenAPI 2.0 specs to OpenAPI 3.x for MCP, annotating specs with
  x-google-api-management.mcp and x-google-mcp-tool, securing tools/list with
  JWTs or API keys, connecting Google ADK (McpToolset) or Apigee API hub and
  Agent Registry, or troubleshooting MCP JSON-RPC errors (-32601, -32602,
  -32000), /mcp HTTP 404 or 405 errors, and MCP errors from api-configs create.
  Do not use for a migration without MCP or another OpenAPI error from
  api-configs create (use api-gateway-openapi-spec-authoring), API key, JWT, or
  quota setup for REST only (use
  api-gateway-backend-security-and-rate-limiting), failing non-MCP requests (use
  api-gateway-troubleshooting), Apigee X proxy bundles, outbound LLM model
  routing, or GKE Gateway API.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/api-gateway-mcp-server/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/api-gateway-mcp-server/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
