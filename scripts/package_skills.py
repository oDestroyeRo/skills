"""Generate a native bundle for each configured collection and marketplace catalogs."""

import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tarfile
import tempfile
import zipfile

from skills import SkillError, SLUG, copy_agent_metadata, copy_materialized, discover_skills, metadata, read_json, render_skill, tree_hash, write_json


PORTABLE_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
DEPENDENCIES = {"@opencode/plugin": "2.2.5", "yaml": "2.8.1"}


def configuration(root):
    config = read_json(root / "distribution.json")
    if config.get("version") != 1:
        raise SkillError("Unsupported distribution.json version")
    for key in ("marketplace",):
        if not SLUG.fullmatch(config[key]):
            raise SkillError("Invalid distribution " + key)
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", config["initial_version"]):
        raise SkillError("initial_version must be a three-part release version")
    names = set()
    published_sources = set()
    source_ids = {source["id"] for source in read_json(root / "sources.json")["sources"]}
    if not config.get("plugins"):
        raise SkillError("distribution.json must declare its native plugins")
    for plugin in config["plugins"]:
        if not SLUG.fullmatch(plugin["name"]) or plugin["name"] in names:
            raise SkillError("Invalid or duplicate native plugin name")
        if plugin["source"] not in source_ids:
            raise SkillError("Native plugin references an unknown source: " + plugin["source"])
        if plugin["source"] in published_sources:
            raise SkillError("Each source must have exactly one plugin: " + plugin["source"])
        if not re.fullmatch(r"(?:@[a-z0-9-]+/)?[a-z0-9-]+", plugin["npm_name"]):
            raise SkillError("Invalid npm package name: " + plugin["name"])
        names.add(plugin["name"])
        published_sources.add(plugin["source"])
    if published_sources != source_ids:
        raise SkillError("Every source in sources.json must have a plugin in distribution.json")
    return config


def bundle_snapshots(root):
    return {plugin["source"]: root / "plugins" / plugin["name"] / "upstream" / plugin["source"]
            for plugin in configuration(root)["plugins"]}


def input_hash(root):
    digest = hashlib.sha256()
    for relative in (
        "distribution.json", "sources.json", "sources.lock.json", "README.md", "LICENSE",
        "docs", "assets", "adapters",
        "scripts/skills.py", "scripts/package_skills.py",
    ):
        path = root / relative
        if path.is_dir():
            value = tree_hash(path)
        elif path.is_file():
            value = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            raise SkillError("Missing package input: " + relative)
        digest.update((relative + "\0" + value + "\n").encode())
    return digest.hexdigest()


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def npm_manifest(config, version):
    manifest = {
        "name": config["npm_name"], "version": version,
        "description": config["description"], "type": "module",
        "license": config["license"],
        "author": config["author"],
        "repository": {"type": "git", "url": config["repository"] + ".git"},
        "homepage": config["repository"],
        "engines": {"node": ">=22"},
        "dependencies": DEPENDENCIES,
    }
    manifest.update({
        "icon": "./assets/logo.svg",
        "exports": {
            ".": "./opencode.mjs",
            "./dsh": "./dsh.mjs",
            "./dsh/icon": "./assets/logo.svg",
            "./dsh/locale/*.json": "./locale/*.json",
            "./cordis.patch.yml": "./cordis.patch.yml",
            "./locale/*.json": "./locale/*.json",
            "./package.json": "./package.json",
        },
        "pi": {"skills": ["./skills"]},
        "dsh": {"bundle": {"patch": "./cordis.patch.yml"}},
        "files": [
            "plugin.json", ".claude-plugin", ".codex-plugin", ".cursor-plugin",
            ".antigravity-plugin", "skills", "upstream", "docs",
            "assets", "locale", "opencode.mjs", "dsh.mjs", "cordis.patch.yml",
            "sources.lock.json", "LICENSE", "THIRD_PARTY_NOTICES.md",
        ],
    })
    return manifest


def workspace_manifest(config, version):
    return {
        "name": config["marketplace"] + "-workspace", "version": version,
        "private": True, "license": config["license"],
        "pi": {"skills": []}, "files": [],
        "workspaces": ["plugins/" + plugin["name"] for plugin in config["plugins"]],
        "devDependencies": DEPENDENCIES,
    }


def plugin_manifests(config, version):
    identity = {
        "name": config["name"], "version": version, "description": config["description"],
        "author": config["author"], "homepage": config["repository"],
        "repository": config["repository"],
        "license": config["license"],
    }
    return {
        "plugin.json": {"$schema": PORTABLE_SCHEMA, **identity},
        ".claude-plugin/plugin.json": identity,
        ".codex-plugin/plugin.json": {**identity, "skills": "./skills/"},
        ".cursor-plugin/plugin.json": {
            **identity, "displayName": config["display_name"], "skills": "./skills/",
            "logo": "assets/logo.svg", "keywords": ["skills", "engineering"],
        },
        ".antigravity-plugin/plugin.json": {
            "$schema": "https://antigravity.google/schemas/v1/plugin.json", **identity,
            "displayName": config["display_name"], "skills": "./skills/",
            "logo": "assets/logo.svg",
            "suggestedPrompts": config["suggested_prompts"],
            "keywords": ["skills", "engineering"],
        },
        "package.json": npm_manifest(config, version),
    }


def marketplace_files(config, version):
    common = {
        "name": config["marketplace"], "owner": {"name": config["author"]["name"]},
        "metadata": {"description": config["description"]},
        "plugins": [{"name": plugin["name"], "source": "./plugins/" + plugin["name"],
                     "description": plugin["description"], "version": version}
                    for plugin in config["plugins"]],
    }
    return {
        ".claude-plugin/marketplace.json": common,
        ".cursor-plugin/marketplace.json": common,
        ".agents/plugins/marketplace.json": {
            "name": config["marketplace"], "interface": {"displayName": config["display_name"]},
            "plugins": [{"name": plugin["name"], "source": {
                             "source": "local", "path": "./plugins/" + plugin["name"]},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": "Productivity"} for plugin in config["plugins"]],
        },
        "package.json": workspace_manifest(config, version),
    }


def populate_bundle(root, bundle, config, version, snapshot):
    bundle.mkdir(parents=True)
    for relative in ("docs", "assets"):
        copy_materialized(root / relative, bundle / relative)
    source_id = config["source"]
    copy_materialized(snapshot, bundle / "upstream" / source_id)
    source = next(source for source in read_json(root / "sources.json")["sources"] if source["id"] == source_id)
    catalog = discover_skills({source_id: snapshot}, [source])
    for entry in catalog:
        library = "upstream/" + entry["source"]
        original = snapshot / entry["path"]
        _, fields = metadata(original)
        description = source.get("description_overrides", {}).get(entry["upstream_name"])
        if description is not None:
            fields["description"] = "description: " + json.dumps(description, ensure_ascii=False)
        folder = bundle / "skills" / entry["name"]
        folder.mkdir(parents=True)
        text = render_skill(entry["name"], entry["source"], fields,
                            "../../" + library + "/" + entry["path"],
                            "../../" + library, "../../docs/harnesses.md")
        marker = text.index("\n---\n") + len("\n---\n")
        text = text[:marker] + "\nResolve this entry point to its real path before following its links.\n" + text[marker:]
        (folder / "SKILL.md").write_text(text)
        if (original.parent / "agents").is_dir():
            copy_agent_metadata(original.parent / "agents", folder / "agents", entry["upstream_name"],
                                entry["name"])
    write_json(bundle / "skills/catalog.json", catalog)
    shutil.copy2(root / "adapters/opencode.mjs", bundle / "opencode.mjs")
    shutil.copy2(root / "adapters/dsh.mjs", bundle / "dsh.mjs")
    (bundle / "cordis.patch.yml").write_text(
        "- insert:\n"
        "    - id: skill-" + config["name"] + "\n"
        "      name: '" + config["npm_name"] + "/dsh'\n"
    )
    write_json(bundle / "locale/en.json", {
        "meta": {
            "title": config["display_name"],
            "description": config["description"],
        },
    })
    source_lock = read_json(root / "sources.lock.json")
    write_json(bundle / "sources.lock.json", {"version": 1, "sources": {
        source_id: source_lock["sources"][source_id]
    }})
    shutil.copy2(root / "LICENSE", bundle / "LICENSE")
    notices = [path for path in sorted((bundle / "upstream").rglob("*")) if path.is_file() and
               ("license" in path.name.lower() or "notice" in path.name.lower() or path.name.endswith("-OFL.txt"))]
    (bundle / "THIRD_PARTY_NOTICES.md").write_text(
        "# Licenses and upstream notices\n\n"
        "This bundle's packaging code and adapters use the [MIT license](LICENSE).\n\n"
        "Upstream skills, assets, and dependencies retain their own terms. "
        "Their original notices are preserved in the files below.\n\n" +
        "".join("- [" + path.relative_to(bundle).as_posix() + "](" + path.relative_to(bundle).as_posix() + ")\n"
                for path in notices)
    )
    for relative, value in plugin_manifests(config, version).items():
        write_json(bundle / relative, value)
    (bundle / "README.md").write_text(
        "# " + config["display_name"] + "\n\n" + config["description"] + "\n\n"
        "Version " + version + ". This bundle contains " + str(len(catalog)) + " namespaced skills.\n\n"
        "Install in Claude Code with `claude plugin install " + config["name"] +
        " --marketplace " + config["repository"].removeprefix("https://github.com/") + "`.\n\n"
        "Follow the [installation guide](docs/native-install.md) and "
        "[publishing guide](docs/native-publishing.md). See the "
        "[harness adapter](docs/harnesses.md) for runtime capabilities.\n\n"
        "See [licenses and upstream notices](THIRD_PARTY_NOTICES.md). "
        "Upstream copyright and license notices remain under `upstream/`. "
        "`sources.lock.json` records the original Git revisions. Source symlinks "
        "are materialized as regular files for archive installation.\n"
    )
    if any(path.is_symlink() for path in bundle.rglob("*")):
        raise SkillError("Native bundle still contains symlinks")


def managed_bundles(config, lock):
    hashes = dict(lock.get("bundle_hashes", {}))
    if "bundle_sha256" in lock:
        hashes["shared-skills"] = lock["bundle_sha256"]
    return hashes


def protect_outputs(root, config, lock, files):
    hashes = managed_bundles(config, lock)
    names = set(hashes) | {plugin["name"] for plugin in config["plugins"]}
    for name in names:
        bundle = root / "plugins" / name
        if (bundle.exists() or bundle.is_symlink()) and (
            bundle.is_symlink() or name not in hashes or tree_hash(bundle) != hashes[name]
        ):
            raise SkillError("Local edits preserved in native bundle " + name + "; change its source inputs before rebuilding")
    for relative in files:
        file = root / relative
        expected = lock.get("generated_files", {}).get(relative)
        if file.exists() and hashlib.sha256(file.read_bytes()).hexdigest() != expected:
            raise SkillError("Local edits preserved in " + relative + "; edit distribution.json instead")


def preflight_package(root):
    config = configuration(root)
    lock = read_json(root / "distribution.lock.json", {})
    version = lock.get("package_version", config["initial_version"])
    protect_outputs(root, config, lock, marketplace_files(config, version))
    return config


def build_package(root, snapshots=None):
    config = configuration(root)
    if snapshots is None:
        snapshots = bundle_snapshots(root)
    lock = read_json(root / "distribution.lock.json", {})
    digest = input_hash(root)
    version = lock.get("package_version", config["initial_version"])
    if lock and digest != lock["input_sha256"]:
        major, minor, patch = map(int, version.split("."))
        version = "{}.{}.{}".format(major, minor, patch + 1)
    files = marketplace_files(config, version)
    protect_outputs(root, config, lock, files)
    with tempfile.TemporaryDirectory(prefix=".native-stage-", dir=root) as temporary:
        stage = Path(temporary)
        staged = stage / "bundles"
        for plugin in config["plugins"]:
            populate_bundle(root, staged / plugin["name"], {**config, **plugin}, version,
                            snapshots[plugin["source"]])
        if input_hash(root) != digest:
            raise SkillError("Package inputs changed while building; retry after edits finish")
        protect_outputs(root, config, lock, files)
        state = {
            "version": 2, "package_version": version, "input_sha256": digest,
            "bundle_hashes": {plugin["name"]: tree_hash(staged / plugin["name"])
                              for plugin in config["plugins"]},
            "generated_files": {name: hashlib.sha256(json_text(value).encode()).hexdigest()
                                for name, value in files.items()},
        }
        destination = root / "plugins"
        destination.mkdir(exist_ok=True)
        previous = stage / "previous"
        previous.mkdir()
        old_files = {relative: (root / relative).read_bytes() if (root / relative).exists() else None
                     for relative in [*files, "distribution.lock.json"]}
        published = []
        try:
            for name in managed_bundles(config, lock):
                target = destination / name
                if target.exists():
                    target.rename(previous / name)
            for plugin in config["plugins"]:
                name = plugin["name"]
                (staged / name).rename(destination / name)
                published.append(name)
            for relative, value in files.items():
                write_json(root / relative, value)
            write_json(root / "distribution.lock.json", state)
        except OSError:
            for name in reversed(published):
                (destination / name).rename(staged / name)
            for backup in previous.iterdir():
                backup.rename(destination / backup.name)
            for relative, content in old_files.items():
                file = root / relative
                if content is None:
                    file.unlink(missing_ok=True)
                else:
                    file.write_bytes(content)
            raise
    print("Built {} native plugins at version {}.".format(len(config["plugins"]), version))


def check_package(root):
    config = configuration(root)
    lock = read_json(root / "distribution.lock.json")
    if lock["input_sha256"] != input_hash(root):
        raise SkillError("Native package inputs changed; run python3 scripts/skills.py package")
    files = marketplace_files(config, lock["package_version"])
    protect_outputs(root, config, lock, files)
    for relative, value in files.items():
        if not (root / relative).is_file() or (root / relative).read_text() != json_text(value):
            raise SkillError("Missing or outdated native manifest: " + relative)
    snapshots = bundle_snapshots(root)
    with tempfile.TemporaryDirectory(prefix="native-check-") as temporary:
        for plugin in config["plugins"]:
            expected = Path(temporary) / plugin["name"]
            populate_bundle(root, expected, {**config, **plugin}, lock["package_version"],
                            snapshots[plugin["source"]])
            bundle = root / "plugins" / plugin["name"]
            if tree_hash(expected) != tree_hash(bundle):
                raise SkillError("Native bundle " + plugin["name"] + " is missing or outdated; run package")
    print("Verified {} native plugins at version {}.".format(len(config["plugins"]), lock["package_version"]))


def archive_package(root):
    check_package(root)
    config = configuration(root)
    version = read_json(root / "distribution.lock.json")["package_version"]
    output = root / "dist"
    if output.is_symlink():
        raise SkillError("Archive directory is a symlink; existing destination preserved")
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".archive-stage-", dir=output) as temporary:
        staged = Path(temporary)
        for plugin in config["plugins"]:
            name = plugin["name"]
            bundle = root / "plugins" / name
            stem = name + "-" + version
            files = [file for file in sorted(bundle.rglob("*")) if file.is_file()]
            with zipfile.ZipFile(staged / (stem + ".zip"), "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for file in files:
                    item = zipfile.ZipInfo(file.relative_to(bundle).as_posix())
                    item.create_system = 3
                    item.external_attr = (0o100000 | file.stat().st_mode & 0o777) << 16
                    item.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(item, file.read_bytes())
            with (staged / (stem + ".tar.gz")).open("wb") as stream:
                with gzip.GzipFile(fileobj=stream, mode="wb", filename="", mtime=0) as compressed:
                    with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                        for file in files:
                            info = archive.gettarinfo(str(file), arcname=name + "/" + file.relative_to(bundle).as_posix())
                            info.uid = info.gid = info.mtime = 0
                            info.uname = info.gname = ""
                            with file.open("rb") as content:
                                archive.addfile(info, content)
        for file in staged.iterdir():
            destination = output / file.name
            if destination.is_symlink() or (destination.exists() and (
                not destination.is_file() or destination.read_bytes() != file.read_bytes()
            )):
                raise SkillError("Existing archive preserved: " + str(destination))
        for file in staged.iterdir():
            destination = output / file.name
            if not destination.exists():
                os.link(file, destination)
    print("Wrote native archives to " + str(output) + ".")
