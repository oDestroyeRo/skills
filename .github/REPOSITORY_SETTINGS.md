# GitHub repository settings

This repository uses GitHub settings and files in `.github/` to protect its history, check code, and keep upstream syncing active.

## History and merges

The `Protect main history` ruleset blocks deletion and force pushes to `main` and requires linear history. Pull requests use squash merges, and GitHub deletes merged branches automatically.

The daily updater validates changed snapshots before pushing directly to `main`. Required pull requests, required status checks before a push, and required signed commits would need a different updater delivery flow. Review that workflow before adding these gates.

`CODEOWNERS` requests review from `@oDestroyeRo` when another contributor opens a pull request. It does not prevent the updater from pushing verified snapshots.

## Actions

GitHub-owned actions are allowed. Repository workflow files pin actions to full commit hashes. The default `GITHUB_TOKEN` permissions are read-only, and workflows cannot create or approve pull requests through the repository default. The upstream workflow explicitly requests `contents: write` for its final push.

External contributors need approval before their fork workflows run. Logs and artifacts expire after 14 days.

The repository-wide SHA-only policy remains off because GitHub's managed CodeQL workflow uses action tags. Repository-owned workflows pin their actions, and Dependabot maintains those pins.

`dependabot.yml` requests weekly GitHub Actions updates on Monday at 09:30 in Bangkok. Those updates arrive as pull requests for review. The separate upstream sync runs daily at 09:17 in Bangkok.

## Security

Dependency alerts, secret scanning, push protection, and private vulnerability reporting are enabled. CodeQL default setup scans GitHub Actions, JavaScript and TypeScript, and Python with the standard security query suite.

GitHub restricts [generic-pattern scanning](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enabling-secret-scanning-for-generic-patterns) and [credential-validity checks](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/customize-leak-detection/enable-validity-checks) to organization repositories with GitHub Secret Protection. Those options are unavailable for this personal repository.

Automatic Dependabot edits to npm manifests are disabled because those files are generated. Change `DEPENDENCIES` in `scripts/package_skills.py`, then run `python3 scripts/skills.py package` and the affected checks.

The [security policy](SECURITY.md) provides the private reporting route. Issue forms also link to it.

## References

- [Repository ruleset](https://github.com/oDestroyeRo/skills/rules/26443325)
- [GitHub Actions settings](https://github.com/oDestroyeRo/skills/settings/actions)
- [GitHub security settings](https://github.com/oDestroyeRo/skills/settings/security_analysis)
- [CodeQL default setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)
- [Dependabot for GitHub Actions](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions)
