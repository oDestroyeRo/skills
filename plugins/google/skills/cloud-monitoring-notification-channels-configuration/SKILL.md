---
name: cloud-monitoring-notification-channels-configuration
description: >-
  Generates Terraform HCL configurations for Cloud Monitoring notification
  channels (`google_monitoring_notification_channel`) and adds notification
  channels to alerting policies (`google_monitoring_alert_policy`) in Google
  Cloud projects. Use when creating or configuring email, SMS, Slack, PagerDuty,
  Pub/Sub, or webhook notification channels, verifying Pub/Sub topic
  compatibility (including cross-project topics, message storage policies, and
  in-transit enforcement) and publishing permissions for the Cloud Monitoring
  Service Agent, or adding notification channels to existing alert policies.
  Don't use for authoring or editing alerting policy conditions, selecting
  metric descriptors, or writing PromQL or Monitoring Filter queries.
---

Resolve this entry point to its real path before following its links.

Read the complete [upstream skill](../../upstream/google/skills/cloud/cloud-monitoring-notification-channels-configuration/SKILL.md) before doing the task.

Resolve `../../upstream/google/skills/cloud/cloud-monitoring-notification-channels-configuration/SKILL.md` to its real path. Resolve the workflow's relative file references from that upstream file, so its scripts, references, and sibling skills stay together.

When it names another skill, select the entry from the same collection or read the matching file in [the upstream library](../../upstream/google).

For harness-specific tools, delegation, models, or settings, read the [harness adapter](../../docs/harnesses.md) and apply the section for the current harness.
