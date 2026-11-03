#!/usr/bin/env python3
"""Sync upstream Agent Skills and link one library into supported harnesses."""

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
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
GLOBAL_DIRS = {
    "codex": [".agents/skills"],
    "claude-code": [".claude/skills"],
    "pi": [".pi/agent/skills"],
    "antigravity": [".gemini/config/skills"],
    "opencode": [".config/opencode/skills"],
    "cursor": [".cursor/skills"],
}
PROJECT_DIRS = {
    "codex": [".agents/skills"],
    "claude-code": [".claude/skills"],
    "pi": [".pi/skills"],
    "antigravity": [".agents/skills"],
    "opencode": [".opencode/skills"],
    "cursor": [".cursor/skills"],
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
        archive = git("archive", "--format=tar", commit, "--", *paths, cwd=checkout)
        extract_snapshot(archive, destination, source["root"])
        for relative in source.get("exclude_paths", []):
            path = destination / relative
            if path.is_symlink() or path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
        return {
            "repository": source["repository"], "ref": source["ref"],
            "root": source["root"], "commit": commit, "sha256": tree_hash(destination),
            "exclude_paths": source.get("exclude_paths", []),
        }


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


def render_skill(name, source_id, fields, source_file="source/SKILL.md", library="library", adapter="harness.md"):
    header = ["name: " + name, fields["description"]]
    for field in ("disable-model-invocation", "user-invocable"):
        if field in fields:
            header.append(fields[field])
    body = (
        "Read the complete [upstream skill](" + source_file + ") before doing the task.\n\n"
        "Resolve `" + source_file + "` to its real path. Resolve the workflow's relative file "
        "references from that upstream file, so its scripts, references, and sibling skills stay together.\n\n"
        "When it names another skill from this collection, use `" + source_id + "-<name>` "
        "or read that skill directly in [the upstream library](" + library + "). Keep this collection's "
        "skills together when names overlap with another collection.\n\n"
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


def make_library(vendor, destination, configured_sources):
    destination.mkdir(parents=True)
    catalog = []
    collections = [(s["id"], vendor / s["id"], skill_roots(s, vendor / s["id"])) for s in configured_sources]
    if (ROOT / "local").is_dir():
        collections.append(("local", ROOT / "local", ["."]))
    for source_id, package, roots in collections:
        skill_files = set()
        for root in roots:
            for directory, children, files in os.walk(package / root):
                children[:] = [child for child in children if not child.startswith(".")]
                if "SKILL.md" in files:
                    skill_files.add(Path(directory) / "SKILL.md")
                    children.clear()
        for file in sorted(skill_files):
            original, fields = metadata(file)
            name = source_id + "-" + original
            if len(name) > 64 or (destination / name).exists():
                raise SkillError("Duplicate or overlong skill name: " + name)
            folder = destination / name
            folder.mkdir()
            source_path = file.parent.relative_to(package)
            real_package = ROOT / ("local" if source_id == "local" else "upstream/" + source_id)
            for link_name, target in {
                "source": real_package / source_path,
                "library": real_package,
                "harness.md": ROOT / "docs/harnesses.md",
            }.items():
                link_base = ROOT / "skills" / name
                (folder / link_name).symlink_to(os.path.relpath(target, link_base))
            if (file.parent / "agents").is_dir():
                copy_agent_metadata(file.parent / "agents", folder / "agents", original, name)
            (folder / "SKILL.md").write_text(render_skill(name, source_id, fields))
            catalog.append({"name": name, "source": source_id, "upstream_name": original,
                            "path": (source_path / "SKILL.md").as_posix()})
    write_json(destination / "catalog.json", catalog)
    return catalog


def protect_generated(lock):
    for directory, expected in [
        *[(ROOT / "upstream" / key, value["sha256"]) for key, value in lock.get("sources", {}).items()],
        (ROOT / "skills", lock.get("skills_sha256")),
    ]:
        actual = tree_hash(directory)
        if actual is not None and actual != expected:
            raise SkillError("Local changes preserved in " + str(directory) + "; move custom skills to local/ before syncing")
    known = set(lock.get("sources", {}))
    upstream = ROOT / "upstream"
    if upstream.is_dir() and any(item.name not in known for item in upstream.iterdir()):
        raise SkillError("Unmanaged files preserved in upstream/")


def replace_directory(staged, destination, backups):
    if destination.exists():
        destination.rename(backups / destination.name)
    try:
        staged.rename(destination)
    except OSError:
        previous = backups / destination.name
        if previous.exists():
            previous.rename(destination)
        raise


def sync(locked=False):
    configured = sources()
    lock = read_json(ROOT / "sources.lock.json", {"sources": {}})
    protect_generated(lock)
    if (ROOT / "distribution.json").is_file():
        from package_skills import preflight_package
        preflight_package(ROOT)
    with tempfile.TemporaryDirectory(prefix=".skills-stage-", dir=ROOT) as temporary:
        stage = Path(temporary)
        vendor = stage / "upstream"
        vendor.mkdir()
        entries = {}
        for source in configured:
            name = source["id"]
            commit = lock["sources"].get(name, {}).get("commit") if locked else None
            if locked and not commit:
                raise SkillError("No locked commit for " + name)
            print("Fetching " + name + (" at " + commit[:12] if commit else " (" + source["ref"] + ")"), flush=True)
            entries[name] = fetch_source(source, vendor / name, commit)
        make_library(vendor, stage / "skills", configured)
        new_lock = {"version": 1, "sources": entries, "skills_sha256": tree_hash(stage / "skills")}
        protect_generated(lock)
        if (ROOT / "distribution.json").is_file():
            preflight_package(ROOT)
        backups = stage / "previous"
        backups.mkdir()
        replace_directory(vendor, ROOT / "upstream", backups)
        replace_directory(stage / "skills", ROOT / "skills", backups)
        write_json(ROOT / "sources.lock.json", new_lock)
    if (ROOT / "distribution.json").is_file():
        from package_skills import build_package
        build_package(ROOT)
    refresh()
    print("Synced upstream sources and shared skills.")


def check(check_distribution=True):
    configured = sources()
    lock = read_json(ROOT / "sources.lock.json")
    if set(lock["sources"]) != {source["id"] for source in configured}:
        raise SkillError("sources.json and sources.lock.json disagree; run sync")
    for source in configured:
        saved = lock["sources"][source["id"]]
        if any(source[key] != saved[key] for key in ("repository", "ref", "root")):
            raise SkillError("Source configuration changed; run sync: " + source["id"])
        if source.get("exclude_paths", []) != saved.get("exclude_paths", []):
            raise SkillError("Source exclusions changed; run sync: " + source["id"])
        if tree_hash(ROOT / "upstream" / source["id"]) != saved["sha256"]:
            raise SkillError("Missing or modified upstream source: " + source["id"])
    with tempfile.TemporaryDirectory(prefix="skills-check-") as temporary:
        generated = Path(temporary) / "skills"
        catalog = make_library(ROOT / "upstream", generated, configured)
        if tree_hash(generated) != tree_hash(ROOT / "skills") or tree_hash(generated) != lock["skills_sha256"]:
            raise SkillError("Generated skills are out of date; run sync")
    for entry in catalog:
        folder = ROOT / "skills" / entry["name"]
        for file in (folder / "source/SKILL.md", folder / "harness.md"):
            if not file.is_file():
                raise SkillError("Broken skill reference: " + str(file))
    print("Verified {} skills and {} upstream snapshots.".format(len(catalog), len(configured)))
    if check_distribution and (ROOT / "distribution.json").is_file():
        from package_skills import check_package
        check_package(ROOT)


def target_directories(agents, home, project):
    expanded = set(agents)
    if "all" in expanded:
        expanded.add("t3")
    if "t3" in expanded:
        expanded.update(GLOBAL_DIRS)
    mapping = GLOBAL_DIRS if project is None else PROJECT_DIRS
    base = home if project is None else project
    directories = {base / relative for agent in expanded if agent in mapping for relative in mapping[agent]}
    if project is None and "t3" in expanded:
        directories.update(home / relative for relative in [".gemini/config/skills", ".gemini/antigravity-cli/skills"])
    return sorted(directories)


def install(directories, remember=True):
    catalog = read_json(ROOT / "skills/catalog.json")
    names = {entry["name"] for entry in catalog}
    changes = []
    for directory in directories:
        directory = directory.expanduser().absolute()
        if directory.resolve() == (ROOT / "skills").resolve():
            raise SkillError("Install into a harness directory, not the shared library itself")
        for name in sorted(names):
            destination = directory / name
            target = ROOT / "skills" / name
            if destination.is_symlink() and destination.resolve() == target.resolve():
                continue
            if destination.exists() or destination.is_symlink():
                raise SkillError("Existing skill preserved: " + str(destination))
            changes.append((destination, target))
        if directory.is_dir():
            for old in directory.iterdir():
                if old.is_symlink() and old.resolve().parent == (ROOT / "skills").resolve() and old.name not in names:
                    changes.append((old, None))
    for destination, target in changes:
        if target is None:
            destination.unlink()
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(target, target_is_directory=True)
    if remember:
        registry = ROOT / ".cache/installations.json"
        previous = read_json(registry, [])
        write_json(registry, sorted(set(previous) | {str(d.expanduser().absolute()) for d in directories}))
    print("Linked {} skills into {} directories.".format(len(names), len(directories)))


def refresh():
    directories = read_json(ROOT / ".cache/installations.json", [])
    if directories:
        install([Path(directory) for directory in directories], remember=False)


def update():
    if git("status", "--porcelain", "--untracked-files=no").strip():
        raise SkillError("Local tracked changes preserved; commit or move them before updating")
    git("pull", "--ff-only")
    check()
    refresh()
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
    sync_parser = commands.add_parser("sync", help="Fetch upstreams, preserve source files, and generate shared entry points")
    sync_parser.add_argument("--locked", action="store_true", help="Fetch the exact commits in sources.lock.json")
    commands.add_parser("check", help="Check source hashes, generated skills, and reference paths")
    commands.add_parser("list", help="List available namespaced skills")
    commands.add_parser("update", help="Fast-forward this checkout and refresh saved installations")
    package_parser = commands.add_parser("package", help="Generate native plugin packages and bump the version when inputs change")
    package_parser.add_argument("--archive", action="store_true", help="Also write standalone ZIP and tar.gz bundles to dist/")
    install_parser = commands.add_parser("install", help="Symlink shared skills into harness discovery directories")
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
        for entry in read_json(ROOT / "skills/catalog.json"):
            print(entry["name"])
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
