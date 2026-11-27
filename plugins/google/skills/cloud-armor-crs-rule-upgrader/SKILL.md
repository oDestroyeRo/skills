---
name: cloud-armor-crs-rule-upgrader
description: >-
  Upgrades Google Cloud Armor security policies from OWASP CRS 3.0 and 3.3 to OWASP CRS 4.22. Preserves signature opt-in and opt-out lists, translates evaluatePreconfiguredExpr to native evaluatePreconfiguredWaf dictionary parameters, remaps signature IDs to v042200, drops retired signature IDs, and updates structured preconfiguredWafConfig fine-tuning exclusions. Evaluates operational risk (High Breaking Change, Medium Attention Required, Low Clean Upgrade) including Method Enforcement breaking changes (PUT/PATCH/DELETE blocking) and sensitivity coverage expansions. Supports both in-place rule upgrades and smooth preview mode deployments with priority spacing and a 200-rule quota guardrail. Use when a user or agent needs to audit, upgrade, or transition Cloud Armor WAF rules to CRS 4.22. Don't use for non-WAF Cloud Armor rules (IP rate-limiting, geo-blocking, reCAPTCHA) or AWS/Azure WAF migrations.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/cloud-armor-crs-rule-upgrader/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/cloud-armor-crs-rule-upgrader/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
