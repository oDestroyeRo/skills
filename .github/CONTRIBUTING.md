# Contribute to shared agent skills

Create a branch named `<type>/<short-kebab-description>` and keep each pull request focused on one change. Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages and pull request titles.

## Edit the owning source

| Change | Owning files | Regenerate with |
| --- | --- | --- |
| Upstream collections, discovery, or license filters | `sources.json` | `python3 scripts/skills.py sync` |
| Plugin identity or marketplace metadata | `distribution.json` | `python3 scripts/skills.py package` |
| OpenCode dependencies | `DEPENDENCIES` in `scripts/package_skills.py` | `python3 scripts/skills.py package` |
| Installer, sync, or bundle behavior | `scripts/`, `adapters/` | `python3 scripts/skills.py package` |
| Bundled documentation or assets | `README.md`, `docs/`, `assets/` | `python3 scripts/skills.py package` |
| GitHub automation or community files | `.github/` | No plugin rebuild |

`plugins/`, the marketplace catalogs, root `package.json`, and the lock files are generated. Submit skill-content fixes to the relevant upstream project, then sync the accepted revision here. Preserve upstream license notices. Review changed license terms before adding a hash to an allowlist.

To reproduce the recorded source revisions, run `python3 scripts/skills.py sync --locked`.

## Check your change

Run the checks affected by your change. The full verification workflow runs:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/skills.py check
npm install --ignore-scripts --no-package-lock --no-audit --no-fund
node --test tests/opencode.test.mjs
python3 scripts/skills.py package --archive
```

Use Python 3.9 or newer, Git, and Node.js 22 or newer. Integration tests use temporary repositories and installation directories.

Explain the resulting behavior and validation in the pull request. Include any client verification gaps. The [repository settings guide](REPOSITORY_SETTINGS.md) explains how GitHub protections preserve the daily updater.

Report vulnerabilities through the [security policy](SECURITY.md).
