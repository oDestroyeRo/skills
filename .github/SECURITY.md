# Security policy

Security fixes target the current `main` branch and the latest generated plugin bundles. Update your checkout or native plugin before checking whether a reported issue still applies.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/oDestroyeRo/skills/security/advisories/new) for vulnerabilities in the installer, sync process, packaging, dependencies, or mirrored skills.

Include the affected commit or plugin version, the source collection and skill path, reproduction steps, and the possible impact. Use a minimal example with synthetic credentials and data. Keep security reports private while maintainers investigate.

For a mirrored skill, include the upstream revision from `sources.lock.json`. A fix may need to land in its upstream project before this repository can sync it.

## Dependency fixes

Dependabot alerts track vulnerable dependencies. GitHub Actions updates arrive as pull requests. OpenCode dependencies are pinned in `DEPENDENCIES` in `scripts/package_skills.py`. Update that mapping and regenerate the bundles so the workspace and all plugin manifests agree.

The license filter controls redistribution eligibility. It does not establish that a skill or its supporting scripts are safe to run.
