#!/usr/bin/env python3
"""Sync source plugins and link their skills into supported harnesses."""

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CACHED_SKILLS = ".cache/skill-files"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
T3_AGENTS = ("codex", "claude-code", "pi", "antigravity", "opencode", "cursor")
GLOBAL_DIRS = {
    "codex": [".agents/skills"],
    "claude-code": [".claude/skills"],
    "pi": [".pi/agent/skills"],
    "antigravity": [".gemini/config/skills"],
    "opencode": [".config/opencode/skills"],
    "cursor": [".cursor/skills"],
    "deepseek-harness": [".dsh/skills"],
}
PROJECT_DIRS = {
    "codex": [".agents/skills"],
    "claude-code": [".claude/skills"],
    "pi": [".pi/skills"],
    "antigravity": [".agents/skills"],
    "opencode": [".opencode/skills"],
    "cursor": [".cursor/skills"],
    "deepseek-harness": [".dsh/skills"],
}
AGENTS = list(GLOBAL_DIRS) + ["t3", "all"]


class SkillError(Exception):
    pass


def git(*args, cwd=ROOT):
    result = subprocess.run(
        ["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode:
        raise SkillError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def read_json(file, default=None):
    if not file.exists() and default is not None:
        return default
    return json.loads(file.read_text())


def write_json(file, value):
    file.parent.mkdir(parents=True, exist_ok=True)
    temporary = file.with_suffix(file.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(file)


def relative_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not value:
        raise SkillError("Expected a relative path inside a source: " + value)
    return path


def sources():
    config = read_json(ROOT / "sources.json")
    if config.get("version") != 1:
        raise SkillError("Unsupported sources.json version")
    seen = set()
    for source in config["sources"]:
        name = source["id"]
        if not SLUG.fullmatch(name) or name in seen or name == "local":
            raise SkillError("Invalid or duplicate source id: " + name)
        seen.add(name)
        relative_path(source["root"])
        if "skills_manifest" in source:
            relative_path(source["skills_manifest"])
        else:
            for skill_root in source["skill_roots"]:
                relative_path(skill_root)
        excluded = source.get("exclude_paths", [])
        if not isinstance(excluded, list) or not all(isinstance(path, str) for path in excluded):
            raise SkillError("Expected a list of excluded source paths: " + name)
        for path in excluded:
            if relative_path(path) == PurePosixPath("."):
                raise SkillError("Cannot exclude an entire source: " + name)
        overrides = source.get("description_overrides", {})
        if not isinstance(overrides, dict) or not all(
            SLUG.fullmatch(key) and isinstance(value, str) and 0 < len(value) <= 1024
            for key, value in overrides.items()
        ):
            raise SkillError("Expected skill description overrides of at most 1024 characters: " + name)
        policy = source.get("license_filter")
        if "license_filter" in source:
            if "skill_roots" not in source or "skills_manifest" in source or not isinstance(policy, dict):
                raise SkillError("License filtering requires explicit skill_roots: " + name)
            if not isinstance(policy["file"], str) or len(relative_path(policy["file"]).parts) != 1:
                raise SkillError("Expected a skill-level license filename: " + name)
            hashes = policy["allowed_sha256"]
            if not isinstance(hashes, list) or not hashes or not all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) for value in hashes):
                raise SkillError("Expected approved license SHA256 hashes: " + name)
            support_paths = policy["support_paths"]
            if not isinstance(support_paths, list) or not all(isinstance(path, str) for path in support_paths):
                raise SkillError("Expected a list of license support paths: " + name)
            for path in support_paths:
                support = relative_path(path)
                for root in source["skill_roots"]:
                    root = relative_path(root)
                    if support.is_relative_to(root) or root.is_relative_to(support):
                        raise SkillError("License support paths must stay outside skill roots: " + name)
        if not source["repository"] or source["repository"].startswith("-"):
            raise SkillError("Invalid source repository: " + name)
        if not source["ref"] or source["ref"].startswith("-"):
            raise SkillError("Invalid source ref: " + name)
    return config["sources"]


def tree_hash(directory):
    digest = hashlib.sha256()
    if not directory.is_dir():
        return None
    for file in sorted(directory.rglob("*")):
        if file.is_symlink():
            data = b"link\0" + os.readlink(file).encode()
        elif file.is_file():
            data = b"file\0" + str(file.stat().st_mode & 0o111).encode() + b"\0" + file.read_bytes()
        else:
            continue
        digest.update(file.relative_to(directory).as_posix().encode() + b"\0" + data + b"\0")
    return digest.hexdigest()


def extract_snapshot(archive, destination, root):
    prefix = relative_path(root)
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            name = relative_path(member.name)
            if root != ".":
                name = name.relative_to(prefix)
            if str(name) == ".":
                continue
            target = destination.joinpath(*name.parts)
            if not target.resolve().is_relative_to(destination.resolve()):
                raise SkillError("Archive path escapes its source: " + member.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            if member.isdir():
                target.mkdir(exist_ok=True)
            elif member.isfile():
                with bundle.extractfile(member) as content:
                    target.write_bytes(content.read())
                target.chmod(0o755 if member.mode & 0o111 else 0o644)
            elif member.issym():
                link = Path(member.linkname)
                if link.is_absolute() or not (target.parent / link).resolve().is_relative_to(destination.resolve()):
                    raise SkillError("Archive symlink escapes its source: " + member.name)
                target.symlink_to(member.linkname)
            else:
                raise SkillError("Unsupported archive entry: " + member.name)


def copy_materialized(source, target):
    boundary = source.resolve()
    for path in source.rglob("*"):
        if path.is_symlink() and not path.resolve().is_relative_to(boundary):
            raise SkillError("Package resource points outside its source: " + str(path))
    shutil.copytree(source, target, symlinks=False)


def licensed_archive_paths(source, checkout, commit):
    policy = source["license_filter"]
    prefix = relative_path(source["root"])
    scope = [] if source["root"] == "." else [source["root"]]
    paths = git("--literal-pathspecs", "ls-tree", "-r", "-z", "--name-only", commit, "--", *scope, cwd=checkout)
    files = {relative_path(path.decode()).relative_to(prefix) for path in paths.split(b"\0") if path}
    roots = [relative_path(root) for root in source["skill_roots"]]
    license_names = {policy["file"].lower(), "license", "license.txt", "license.md", "copying", "copying.txt"}
    license_hashes = {}

    def approved_license(path):
        if path not in license_hashes:
            content = git("show", commit + ":" + str(prefix / path), cwd=checkout)
            license_hashes[path] = hashlib.sha256(content).hexdigest()
        return license_hashes[path] in policy["allowed_sha256"]

    candidates = sorted((path.parent for path in files if path.name == "SKILL.md" and
                         any(path.is_relative_to(root) for root in roots)), key=lambda path: (len(path.parts), str(path)))
    visited, approved, omitted = [], [], []
    for folder in candidates:
        if any(folder.is_relative_to(parent) for parent in visited):
            continue
        visited.append(folder)
        license_file = folder / policy["file"]
        if license_file not in files:
            omitted.append({"path": str(folder), "reason": "missing license file"})
            continue
        if not approved_license(license_file):
            omitted.append({"path": str(folder), "reason": "unapproved license"})
            continue
        nested = sorted(path for path in files if path != license_file and path.is_relative_to(folder) and
                        path.name.lower() in license_names)
        blocked = next((path for path in nested if not approved_license(path)), None)
        if blocked is not None:
            omitted.append({"path": str(folder), "reason": "unapproved nested license", "license": str(blocked)})
            continue
        approved.append(folder)
    support = [relative_path(path) for path in policy["support_paths"] if relative_path(path) in files]
    return [str(prefix / path) for path in [*support, *approved]], omitted


def fetch_source(source, destination, locked_commit=None):
    with tempfile.TemporaryDirectory(prefix="skills-fetch-") as temporary:
        checkout = Path(temporary) / "repo"
        git("clone", "--quiet", "--depth=1", "--filter=blob:none", "--no-checkout",
            "--branch", source["ref"], "--", source["repository"], str(checkout))
        revision = "HEAD"
        if locked_commit:
            if not re.fullmatch(r"[0-9a-f]{40,64}", locked_commit):
                raise SkillError("Invalid locked commit for " + source["id"])
            git("fetch", "--quiet", "--depth=1", "origin", locked_commit, cwd=checkout)
            revision = "FETCH_HEAD"
        commit = git("rev-parse", revision, cwd=checkout).decode().strip()
        paths = [] if source["root"] == "." else [source["root"]]
        omitted = []
        if "license_filter" in source:
            paths, omitted = licensed_archive_paths(source, checkout, commit)
        if paths or "license_filter" not in source:
            archive = git("--literal-pathspecs", "archive", "--format=tar", commit, "--", *paths, cwd=checkout)
            extract_snapshot(archive, destination, source["root"])
        else:
            destination.mkdir(parents=True)
        for relative in source.get("exclude_paths", []):
            path = destination / relative
            if path.is_symlink() or path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
        # Bundles store regular files, so the locked hash must describe the materialized tree.
        materialized = destination.with_name(destination.name + ".files")
        copy_materialized(destination, materialized)
        shutil.rmtree(destination)
        materialized.rename(destination)
        saved = {
            "repository": source["repository"], "ref": source["ref"],
            "root": source["root"], "commit": commit, "sha256": tree_hash(destination),
            "exclude_paths": source.get("exclude_paths", []),
        }
        if "license_filter" in source:
            saved.update({"license_filter": source["license_filter"], "omitted_skills": omitted})
            print("License filter for {} omitted {} skills without approved terms.".format(source["id"], len(omitted)), flush=True)
        return saved


def metadata(file):
    text = file.read_text()
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        raise SkillError("Missing YAML frontmatter: " + str(file))
    header = match.group(1)
    keys = list(re.finditer(r"(?m)^([a-z][a-z0-9-]*):", header))
    fields = {
        key.group(1): header[key.start(): keys[i + 1].start() if i + 1 < len(keys) else len(header)].rstrip()
        for i, key in enumerate(keys)
    }
    name = fields.get("name", "").partition(":")[2].strip().strip("\"'")
    if not SLUG.fullmatch(name) or "description" not in fields:
        raise SkillError("Invalid skill name or missing description: " + str(file))
    return name, fields


def skill_roots(source, package):
    if "skills_manifest" not in source:
        return source["skill_roots"]
    manifest = read_json(package / source["skills_manifest"])
    declared = manifest.get("skills", ["skills"])
    roots = [declared] if isinstance(declared, str) else declared
    if not isinstance(roots, list) or not all(isinstance(root, str) for root in roots):
        raise SkillError("Expected skill paths in upstream manifest: " + source["id"])
    for root in roots:
        relative_path(root)
    return roots


def render_skill(name, fields, source_file, library, adapter):
    description = "\n".join(line.rstrip() for line in fields["description"].splitlines())
    header = ["name: " + name, description]
    for field in ("disable-model-invocation", "user-invocable"):
        if field in fields:
            header.append(fields[field])
    body = (
        "Resolve this entry point to its real path before following its links.\n\n"
        "Read the complete [upstream skill](" + source_file + ") before doing the task.\n\n"
        "Resolve `" + source_file + "` to its real path. Resolve the workflow's relative file "
        "references from that upstream file, so its scripts, references, and sibling skills stay together.\n\n"
        "When it names another skill, select the entry from the same collection or read "
        "the matching file in [the upstream library](" + library + ").\n\n"
        "For harness-specific tools, delegation, models, or settings, read the "
        "[harness adapter](" + adapter + ") and apply the section for the current harness.\n"
    )
    return "---\n" + "\n".join(header) + "\n---\n\n" + body


def copy_agent_metadata(source, destination, original_name, invocation_name):
    shutil.copytree(source, destination)
    config = destination / "openai.yaml"
    if config.is_file():
        text = config.read_text()
        token = re.compile(r"\$" + re.escape(original_name) + r"(?![a-zA-Z0-9_:-])")
        prompt = r"(?m)^  default_prompt:[^\n]*(?:\n    [^\n]*)*"
        text = re.sub(prompt, lambda match: token.sub(lambda _: "$" + invocation_name, match.group()), text)
        config.write_text(text)


def write_skill_entry(folder, bundle, entry, fields, invocation, *, link_from=None):
    library = bundle / "upstream" / entry["source"]
    original = library / entry["path"]
    link_from = folder if link_from is None else link_from
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(render_skill(
        folder.name, fields, os.path.relpath(original, link_from),
        os.path.relpath(library, link_from), os.path.relpath(bundle / "docs/harnesses.md", link_from),
    ))
    agents = original.parent / "agents"
    if agents.is_dir():
        copy_agent_metadata(agents, folder / "agents", entry["upstream_name"], invocation)


def write_prefixed_skill(folder, bundle, entry, *, link_from=None):
    _, fields = metadata(bundle / "skills" / entry["native_name"] / "SKILL.md")
    write_skill_entry(folder, bundle, entry, fields, entry["name"], link_from=link_from)


def discover_skills(snapshots, configured_sources):
    catalog = []
    names = set()
    collections = [(s["id"], snapshots[s["id"]], skill_roots(s, snapshots[s["id"]])) for s in configured_sources]
    for source_id, package, roots in collections:
        skill_files = set()
        for root in roots:
            for directory, children, files in os.walk(package / root):
                children[:] = [child for child in children if not child.startswith(".")]
                if "SKILL.md" in files:
                    skill_files.add(Path(directory) / "SKILL.md")
                    children.clear()
        for file in sorted(skill_files):
            original, _ = metadata(file)
            name = source_id + "-" + original
            if len(name) > 64 or name in names:
                raise SkillError("Duplicate or overlong skill name: " + name)
            names.add(name)
            source_path = file.parent.relative_to(package)
            catalog.append({"name": name, "source": source_id, "upstream_name": original,
                            "path": (source_path / "SKILL.md").as_posix()})
    return catalog


def plugin_skills():
    from package_skills import configuration
    entries = {}
    for plugin in configuration(ROOT)["plugins"]:
        bundle = ROOT / "plugins" / plugin["name"]
        for entry in read_json(bundle / "catalog.json"):
            name = entry["name"]
            if not SLUG.fullmatch(name) or name in entries:
                raise SkillError("Invalid or duplicate packaged skill: " + name)
            entries[name] = (bundle, entry)
    return entries


def protect_generated(lock):
    legacy = ROOT / "skills"
    if legacy.is_symlink() or (legacy.exists() and not legacy.is_dir()):
        raise SkillError("Unmanaged root skills path preserved; move it before syncing")
    actual = tree_hash(legacy)
    if actual is not None and actual != lock.get("skills_sha256"):
        raise SkillError("Local changes preserved in " + str(legacy) + "; restore generated files before syncing")


def sync(locked=False):
    from package_skills import build_package, preflight_package
    configured = sources()
    lock = read_json(ROOT / "sources.lock.json", {"sources": {}})
    protect_generated(lock)
    preflight_package(ROOT)
    previous_plugins = managed_plugin_names()
    with tempfile.TemporaryDirectory(prefix=".skills-stage-", dir=ROOT) as temporary:
        stage = Path(temporary)
        snapshots = {source["id"]: stage / "upstream" / source["id"] for source in configured}
        entries = {}
        for source in configured:
            name = source["id"]
            commit = lock["sources"].get(name, {}).get("commit") if locked else None
            if locked and not commit:
                raise SkillError("No locked commit for " + name)
            print("Fetching " + name + (" at " + commit[:12] if commit else " (" + source["ref"] + ")"), flush=True)
            entry = fetch_source(source, snapshots[name], commit)
            previous = lock["sources"].get(name)
            # Unrelated upstream commits must not publish a new package version.
            unchanged = previous and {**previous, "commit": None} == {**entry, "commit": None}
            entries[name] = previous if unchanged else entry
        catalog = discover_skills(snapshots, configured)
        new_lock = {"version": 1, "sources": entries}
        protect_generated(lock)
        distribution = preflight_package(ROOT)
        plugins = {plugin["source"]: plugin["name"] for plugin in distribution["plugins"]}
        prospective = {entry["name"]: ROOT / CACHED_SKILLS / plugins[entry["source"]] / entry["name"]
                       for entry in catalog}
        remembered = [Path(path) for path in read_json(ROOT / ".cache/installations.json", [])]
        installation_changes(remembered, prospective, previous_plugins)
        backups = stage / "previous"
        backups.mkdir()
        lock_file = ROOT / "sources.lock.json"
        previous_lock = lock_file.read_bytes() if lock_file.exists() else None
        try:
            legacy = ROOT / "skills"
            if legacy.exists():
                legacy.rename(backups / "skills")
            write_json(lock_file, new_lock)
            build_package(ROOT, snapshots)
        except Exception:
            if (backups / "skills").exists():
                (backups / "skills").rename(ROOT / "skills")
            if previous_lock is None:
                lock_file.unlink(missing_ok=True)
            else:
                lock_file.write_bytes(previous_lock)
            raise
    refresh(previous_plugins)
    print("Synced upstream sources and per-collection plugins.")


def check(check_distribution=True):
    from package_skills import bundle_snapshots, check_package
    configured = sources()
    lock = read_json(ROOT / "sources.lock.json")
    if set(lock["sources"]) != {source["id"] for source in configured}:
        raise SkillError("sources.json and sources.lock.json disagree; run sync")
    snapshots = bundle_snapshots(ROOT)
    for source in configured:
        saved = lock["sources"][source["id"]]
        if any(source[key] != saved[key] for key in ("repository", "ref", "root")):
            raise SkillError("Source configuration changed; run sync: " + source["id"])
        if source.get("exclude_paths", []) != saved.get("exclude_paths", []):
            raise SkillError("Source exclusions changed; run sync: " + source["id"])
        if source.get("license_filter") != saved.get("license_filter"):
            raise SkillError("Source license filter changed; run sync: " + source["id"])
        if tree_hash(snapshots[source["id"]]) != saved["sha256"]:
            raise SkillError("Missing or modified upstream source: " + source["id"] + "; restore it or run sync --locked")
    if (ROOT / "skills").exists() or (ROOT / "skills").is_symlink():
        raise SkillError("Legacy root skills/ directory found; run sync to migrate to plugin folders")
    catalog = discover_skills(snapshots, configured)
    print("Verified {} skills and {} upstream snapshots.".format(len(catalog), len(configured)))
    if check_distribution:
        check_package(ROOT)


def target_directories(agents, home, project):
    expanded = set(agents)
    if "all" in expanded:
        expanded.update(GLOBAL_DIRS)
        expanded.add("t3")
    if "t3" in expanded:
        expanded.update(T3_AGENTS)
    mapping = GLOBAL_DIRS if project is None else PROJECT_DIRS
    base = home if project is None else project
    directories = {base / relative for agent in expanded if agent in mapping for relative in mapping[agent]}
    if project is None and "t3" in expanded:
        directories.update(home / relative for relative in [".gemini/config/skills", ".gemini/antigravity-cli/skills"])
    return sorted(directories)


def managed_plugin_names():
    config = read_json(ROOT / "distribution.json")
    lock = read_json(ROOT / "distribution.lock.json", {})
    return {plugin["name"] for plugin in config["plugins"]} | set(lock.get("bundle_hashes", {}))


def owned_skill_link(file, plugins):
    if not file.is_symlink():
        return False
    target = file.resolve()
    if target == ROOT / "skills" / file.name:
        return True
    if target.is_relative_to(ROOT / CACHED_SKILLS):
        parts = target.relative_to(ROOT / CACHED_SKILLS).parts
        return len(parts) == 2 and parts[1] == file.name
    try:
        parts = target.relative_to(ROOT / "plugins").parts
    except ValueError:
        return False
    if len(parts) != 3 or parts[0] not in plugins or parts[2] != file.name:
        return False
    if parts[1] == "standalone-skills":
        return True
    return parts[1] == "skills" and not target.exists()


def installation_changes(directories, entries, plugins):
    names = set(entries)
    changes = []
    for directory in directories:
        directory = directory.expanduser().absolute()
        resolved = directory.resolve()
        if (resolved.is_relative_to(ROOT / "plugins") or resolved == ROOT / "skills" or
            resolved.is_relative_to(ROOT / CACHED_SKILLS)):
            raise SkillError("Install into a harness directory, not a generated plugin directory")
        for name in sorted(names):
            destination = directory / name
            target = entries[name]
            if destination.is_symlink() and destination.resolve() == target.resolve():
                continue
            legacy_bundle_entry = target.parent.name in plugins and destination.is_symlink() and (
                destination.resolve() == ROOT / "plugins" / target.parent.name / "skills" / name
            )
            if ((destination.exists() or destination.is_symlink()) and
                not (legacy_bundle_entry or owned_skill_link(destination, plugins))):
                raise SkillError("Existing skill preserved: " + str(destination))
            changes.append((destination, target))
        if directory.is_dir():
            for old in directory.iterdir():
                if owned_skill_link(old, plugins) and old.name not in names:
                    changes.append((old, None))
    return changes


def generate_cached_skills(entries, targets):
    cache = ROOT / CACHED_SKILLS
    if cache.is_symlink() or (cache.exists() and not (cache / ".generated").is_file()):
        raise SkillError("Unmanaged skill cache preserved: " + str(cache))
    with tempfile.TemporaryDirectory(prefix="skill-entries-", dir=cache.parent) as temporary:
        stage = Path(temporary) / "next"
        stage.mkdir()
        (stage / ".generated").touch()
        for name, (bundle, entry) in entries.items():
            write_prefixed_skill(stage / bundle.name / name, bundle, entry, link_from=targets[name])
        if tree_hash(cache) == tree_hash(stage):
            return
        previous = Path(temporary) / "previous"
        if cache.exists():
            cache.rename(previous)
        try:
            stage.rename(cache)
        except OSError:
            if previous.exists():
                previous.rename(cache)
            raise


def install(directories, remember=True, previous_plugins=()):
    entries = plugin_skills()
    targets = {name: ROOT / CACHED_SKILLS / bundle.name / name for name, (bundle, _) in entries.items()}
    changes = installation_changes(directories, targets, managed_plugin_names() | set(previous_plugins))
    generate_cached_skills(entries, targets)
    for destination, target in changes:
        if destination.is_symlink():
            destination.unlink()
        if target is None:
            continue
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(target, target_is_directory=True)
    if remember:
        registry = ROOT / ".cache/installations.json"
        previous = read_json(registry, [])
        write_json(registry, sorted(set(previous) | {str(d.expanduser().absolute()) for d in directories}))
    print("Linked {} skills into {} directories.".format(len(entries), len(directories)))


def refresh(previous_plugins=()):
    directories = read_json(ROOT / ".cache/installations.json", [])
    if directories:
        install([Path(directory) for directory in directories], remember=False, previous_plugins=previous_plugins)


def update():
    if git("status", "--porcelain", "--untracked-files=no").strip():
        raise SkillError("Local tracked changes preserved; commit or move them before updating")
    previous_plugins = managed_plugin_names()
    git("pull", "--ff-only")
    check()
    refresh(previous_plugins)
    print("Updated from the repository's tracking branch and refreshed installations.")


@contextmanager
def mutation_lock():
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    with (cache / "skills.lock").open("w") as file:
        try:
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SkillError("Another skills command is writing this checkout; retry after it finishes")
        yield


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    sync_parser = commands.add_parser("sync", help="Fetch upstreams, preserve source files, and generate per-collection plugins")
    sync_parser.add_argument("--locked", action="store_true", help="Fetch the exact commits in sources.lock.json")
    commands.add_parser("check", help="Check source hashes, generated skills, and reference paths")
    commands.add_parser("list", help="List available namespaced skills")
    commands.add_parser("update", help="Fast-forward this checkout and refresh saved installations")
    package_parser = commands.add_parser("package", help="Generate native plugin packages and bump the version when inputs change")
    package_parser.add_argument("--archive", action="store_true", help="Also write standalone ZIP and tar.gz bundles to dist/")
    install_parser = commands.add_parser("install", help="Link plugin skills into harness discovery directories")
    install_parser.add_argument("--agent", action="append", choices=AGENTS, default=[])
    scope = install_parser.add_mutually_exclusive_group()
    scope.add_argument("--global", dest="global_scope", action="store_true")
    scope.add_argument("--project", type=Path)
    scope.add_argument("--directory", type=Path, help="Custom skill directory (for non-default harness config)")
    install_parser.add_argument("--home", type=Path, default=Path.home(), help="Home directory for global targets")
    args = parser.parse_args()
    if args.command == "install" and not args.directory and (not args.agent or not (args.global_scope or args.project)):
        parser.error("install requires --agent plus --global or --project, or --directory")
    if args.command == "check":
        check()
    elif args.command == "list":
        for name in sorted(plugin_skills()):
            print(name)
    else:
        with mutation_lock():
            if args.command == "sync":
                sync(args.locked)
            elif args.command == "update":
                update()
            elif args.command == "package":
                from package_skills import archive_package, build_package
                check(check_distribution=False)
                build_package(ROOT)
                if args.archive:
                    archive_package(ROOT)
            elif args.command == "install":
                check()
                directories = [args.directory] if args.directory else target_directories(args.agent, args.home, args.project)
                install(directories)


if __name__ == "__main__":
    sys.modules.setdefault("skills", sys.modules[__name__])
    try:
        main()
    except (SkillError, OSError, ValueError, KeyError) as error:
        print("skills: " + str(error), file=sys.stderr)
        sys.exit(1)
