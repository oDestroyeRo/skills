import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import unittest
import zipfile

import test_skills


ROOT = Path(__file__).resolve().parents[1]


class NativePackagingTest(unittest.TestCase):
    def setUp(self):
        self.fixture = test_skills.SharedSkillsTest("test_one_library_installs_for_all_harnesses_and_t3")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.repo = self.fixture.repo
        script = self.fixture.upstreams["pstack"] / "pstack/skills/tdd/tool.sh"
        script.write_text("#!/bin/sh\nexit 0\n")
        script.chmod(0o755)
        self.fixture.commit(self.fixture.upstreams["pstack"], "add executable resource")
        self.fixture.command("sync")
        self.bundle = self.repo / "plugins/pstack"

    def lock(self):
        return json.loads((self.repo / "distribution.lock.json").read_text())

    def test_native_bundle_has_complete_regular_resources_and_consistent_versions(self):
        self.fixture.command("check")
        version = self.lock()["package_version"]
        for relative in ["plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
                         ".cursor-plugin/plugin.json", ".antigravity-plugin/plugin.json", "package.json"]:
            manifest = json.loads((self.bundle / relative).read_text())
            self.assertEqual(manifest["version"], version)
            self.assertEqual(manifest["license"], "MIT")
        self.assertFalse(any(path.is_symlink() for path in self.bundle.rglob("*")))
        self.assertEqual((self.bundle / "upstream/pstack/skills/tdd/examples.md").read_text(), "Original example for pstack\n")
        text = (self.bundle / "skills/pstack-tdd/SKILL.md").read_text()
        self.assertIn("../../upstream/pstack/skills/tdd/SKILL.md", text)
        self.assertTrue((self.bundle / "LICENSE").is_file())
        self.assertFalse((self.bundle / ".cache").exists())
        root_package = json.loads((self.repo / "package.json").read_text())
        self.assertTrue(root_package["private"])
        self.assertEqual(root_package["pi"]["skills"], [])
        self.assertEqual(root_package["files"], [])
        self.assertNotIn("exports", root_package)
        for name in ["mattpocock", "pstack"]:
            package = self.repo / "plugins" / name
            manifest = json.loads((package / "package.json").read_text())
            self.assertTrue((package / manifest["pi"]["skills"][0]).is_dir())
            self.assertTrue((package / manifest["exports"]["."]).is_file())
            catalog = json.loads((package / "skills/catalog.json").read_text())
            self.assertEqual({entry["source"] for entry in catalog}, {name})
            self.assertEqual({path.name for path in (package / "upstream").iterdir()}, {name})
        for path in [".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json"]:
            entries = json.loads((self.repo / path).read_text())["plugins"]
            self.assertEqual({entry["name"] for entry in entries}, {"mattpocock", "pstack"})
            self.assertEqual(len(entries), 2)
        self.assertFalse((self.repo / "plugins/shared-skills").exists())

    def test_unchanged_build_keeps_its_version_and_archives_are_reproducible(self):
        self.fixture.command("package", "--archive")
        original = self.lock()
        before = {file.name: hashlib.sha256(file.read_bytes()).hexdigest() for file in (self.repo / "dist").iterdir()}
        self.fixture.command("package", "--archive")
        after = {file.name: hashlib.sha256(file.read_bytes()).hexdigest() for file in (self.repo / "dist").iterdir()}
        self.assertEqual(self.lock(), original)
        self.assertEqual(before, after)

    def test_source_exclusions_remove_only_configured_maintenance_files(self):
        checkout = self.fixture.upstreams["pstack"]
        package = checkout / "pstack"
        (package / ".github/workflows").mkdir(parents=True)
        (package / ".github/workflows/release.yml").write_text("Upstream release tooling.\n")
        (package / "package.json").write_text('{"private":true}\n')
        source = next(source for source in self.fixture.config["sources"] if source["id"] == "pstack")
        source["exclude_paths"] = [".github", "package.json"]
        self.fixture.write_config()
        self.fixture.commit(checkout, "add upstream maintenance files")
        self.fixture.command("sync")
        self.fixture.command("check")
        for snapshot in (self.repo / "upstream/pstack", self.bundle / "upstream/pstack"):
            self.assertFalse((snapshot / ".github").exists())
            self.assertFalse((snapshot / "package.json").exists())
            self.assertEqual((snapshot / "LICENSE").read_bytes(), (package / "LICENSE").read_bytes())
            self.assertEqual((snapshot / "skills/tdd/examples.md").read_bytes(),
                             (package / "skills/tdd/examples.md").read_bytes())
            self.assertTrue((snapshot / "skills/tdd/tool.sh").stat().st_mode & 0o111)
        source["exclude_paths"] = [".github"]
        self.fixture.write_config()
        self.assertIn("exclusions changed", self.fixture.command("check", success=False).stderr)
        self.fixture.command("sync", "--locked")
        self.fixture.command("check")
        self.assertEqual((self.bundle / "upstream/pstack/package.json").read_bytes(),
                         (package / "package.json").read_bytes())
        before = (self.repo / "sources.lock.json").read_bytes()
        for invalid in (".", "../outside"):
            source["exclude_paths"] = [invalid]
            self.fixture.write_config()
            self.fixture.command("sync", success=False)
            self.assertEqual((self.repo / "sources.lock.json").read_bytes(), before)

    def test_additions_and_removals_bump_versions_and_remove_retired_bundle_files(self):
        original = self.lock()["package_version"]
        self.fixture.add_skill()
        self.fixture.command("sync")
        added = self.lock()["package_version"]
        self.assertNotEqual(added, original)
        self.assertTrue((self.bundle / "skills/pstack-new-skill/SKILL.md").is_file())
        shutil.rmtree(self.fixture.upstreams["pstack"] / "pstack/skills/tdd")
        self.fixture.commit(self.fixture.upstreams["pstack"], "retire existing skill")
        self.fixture.command("sync")
        removed = self.lock()["package_version"]
        self.assertNotEqual(removed, added)
        self.assertFalse((self.bundle / "skills/pstack-tdd").exists())
        self.assertFalse((self.bundle / "upstream/pstack/skills/tdd").exists())
        for relative in ["package.json", ".claude-plugin/plugin.json", ".antigravity-plugin/plugin.json"]:
            self.assertEqual(json.loads((self.bundle / relative).read_text())["version"], removed)
        self.fixture.command("check")

    def test_local_edits_to_generated_native_outputs_are_preserved(self):
        original = self.lock()
        file = self.bundle / "skills/pstack-tdd/SKILL.md"
        file.write_text(file.read_text() + "\nLocal edit\n")
        result = self.fixture.command("package", success=False)
        self.assertIn("Local edit", file.read_text())
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.lock(), original)

    def test_native_conflict_stops_sync_before_shared_state_or_installed_links_change(self):
        before_lock = (self.repo / "sources.lock.json").read_bytes()
        before_catalog = (self.bundle / "skills/catalog.json").read_bytes()
        before_version = self.lock()
        target = self.fixture.base / "installed"
        self.fixture.command("install", "--directory", str(target))
        file = self.bundle / "skills/pstack-tdd/SKILL.md"
        file.write_text(file.read_text() + "\nLocal native edit\n")
        self.fixture.add_skill()
        self.fixture.command("sync", success=False)
        self.assertEqual((self.repo / "sources.lock.json").read_bytes(), before_lock)
        self.assertEqual((self.bundle / "skills/catalog.json").read_bytes(), before_catalog)
        self.assertEqual(self.lock(), before_version)
        self.assertFalse((target / "pstack-new-skill").exists())
        self.assertTrue((target / "pstack-tdd/SKILL.md").is_file())

    def test_archives_preserve_existing_symlinks_files_and_symlinked_directories(self):
        self.fixture.command("package", "--archive")
        version = self.lock()["package_version"]
        archive = self.repo / "dist" / ("pstack-" + version + ".zip")
        archive.unlink()
        outside = self.fixture.base / "unrelated.txt"
        outside.write_text("Keep this file\n")
        archive.symlink_to(outside)
        self.fixture.command("package", "--archive", success=False)
        self.assertEqual(outside.read_text(), "Keep this file\n")
        self.assertTrue(archive.is_symlink())
        archive.unlink()
        archive.write_text("Unknown existing artifact\n")
        self.fixture.command("package", "--archive", success=False)
        self.assertEqual(archive.read_text(), "Unknown existing artifact\n")
        (self.repo / "dist").rename(self.repo / "previous-dist")
        external = self.fixture.base / "unrelated-directory"
        external.mkdir()
        (self.repo / "dist").symlink_to(external, target_is_directory=True)
        self.fixture.command("package", "--archive", success=False)
        self.assertFalse(list(external.iterdir()))

    def test_regular_archives_keep_skill_resources_licenses_and_executable_modes(self):
        self.fixture.command("package", "--archive")
        version = self.lock()["package_version"]
        with zipfile.ZipFile(self.repo / "dist" / ("pstack-" + version + ".zip")) as archive:
            self.assertIn("plugin.json", archive.namelist())
            self.assertIn("LICENSE", archive.namelist())
            self.assertIn("upstream/pstack/LICENSE", archive.namelist())
            item = archive.getinfo("upstream/pstack/skills/tdd/tool.sh")
            self.assertTrue(item.external_attr >> 16 & 0o111)
        with tarfile.open(self.repo / "dist" / ("pstack-" + version + ".tar.gz")) as archive:
            self.assertTrue(all(member.isfile() for member in archive.getmembers()))
            item = archive.getmember("pstack/upstream/pstack/skills/tdd/tool.sh")
            self.assertTrue(item.mode & 0o111)

    def test_adapter_or_guide_changes_produce_a_new_version(self):
        before = self.lock()["package_version"]
        guide = self.repo / "docs/native-install.md"
        guide.write_text(guide.read_text() + "\nUpdated install instructions.\n")
        self.fixture.command("package")
        self.assertNotEqual(self.lock()["package_version"], before)
        self.assertIn("Updated install instructions", (self.bundle / "docs/native-install.md").read_text())

    def test_retired_combined_bundle_is_removed_only_when_its_owned_contents_match(self):
        retired = self.repo / "plugins/shared-skills"
        shutil.copytree(self.bundle, retired)
        state = self.lock()
        state["bundle_hashes"]["shared-skills"] = state["bundle_hashes"]["pstack"]
        (self.repo / "distribution.lock.json").write_text(json.dumps(state))
        file = retired / "skills/pstack-tdd/SKILL.md"
        original = file.read_text()
        file.write_text(original + "\nKeep this edit\n")
        self.fixture.command("package", success=False)
        self.assertIn("Keep this edit", file.read_text())
        file.write_text(original)
        self.fixture.command("package")
        self.assertFalse(retired.exists())
        self.assertEqual(set(self.lock()["bundle_hashes"]), {"mattpocock", "pstack"})

    def test_third_collection_preserves_resources_and_tracks_added_and_removed_skills(self):
        checkout = self.fixture.base / "tstack"
        checkout.mkdir()
        self.fixture.git("init", "--quiet", "--initial-branch=main", cwd=checkout)
        skill = checkout / "skills/full-stop"
        (skill / "agents").mkdir(parents=True)
        (skill / "scripts").mkdir()
        (skill / "SKILL.md").write_text("---\nname: full-stop\ndescription: Prepare a PR for review.\n---\n\nRead scripts/pr-wait.\n")
        original_ui = 'interface:\n  display_name: "Full Stop"\n  default_prompt: "Use $full-stop to prepare a PR."\npolicy:\n  allow_implicit_invocation: false\n'
        (skill / "agents/openai.yaml").write_text(original_ui)
        helper = skill / "scripts/pr-wait"
        helper.write_text("#!/bin/sh\nexit 0\n")
        helper.chmod(0o755)
        (checkout / "LICENSE").write_text("MIT tstack fixture notice\n")
        self.fixture.commit(checkout, "publish tstack fixture")
        target = self.fixture.base / "installed"
        self.fixture.command("install", "--directory", str(target))
        self.fixture.config["sources"].append({"id": "tstack", "repository": checkout.as_uri(),
                                               "ref": "main", "root": ".", "skill_roots": ["skills"]})
        self.fixture.write_config()
        config = json.loads((self.repo / "distribution.json").read_text())
        tstack = next(plugin for plugin in json.loads((ROOT / "distribution.json").read_text())["plugins"]
                      if plugin["source"] == "tstack")
        config["plugins"].append(tstack)
        (self.repo / "distribution.json").write_text(json.dumps(config))
        self.fixture.command("sync")
        self.fixture.command("check")
        bundle = self.repo / "plugins/tstack"
        catalog = json.loads((bundle / "skills/catalog.json").read_text())
        self.assertEqual([entry["name"] for entry in catalog], ["tstack-full-stop"])
        self.assertEqual({item.name for item in (bundle / "upstream").iterdir()}, {"tstack"})
        self.assertEqual((bundle / "upstream/tstack/LICENSE").read_text(), "MIT tstack fixture notice\n")
        self.assertTrue((bundle / "upstream/tstack/skills/full-stop/scripts/pr-wait").stat().st_mode & 0o111)
        self.assertTrue((target / "tstack-full-stop/SKILL.md").is_file())
        self.assertIn("$tstack-full-stop", (target / "tstack-full-stop/agents/openai.yaml").read_text())
        native_ui = (bundle / "skills/tstack-full-stop/agents/openai.yaml").read_text()
        self.assertIn("$tstack-full-stop", native_ui)
        self.assertIn("allow_implicit_invocation: false", native_ui)
        self.assertEqual((self.repo / "upstream/tstack/skills/full-stop/agents/openai.yaml").read_text(), original_ui)
        for path in [".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json"]:
            entries = json.loads((self.repo / path).read_text())["plugins"]
            self.assertEqual({entry["name"] for entry in entries}, {"mattpocock", "pstack", "tstack"})
        shutil.rmtree(skill)
        replacement = checkout / "skills/review"
        replacement.mkdir()
        (replacement / "SKILL.md").write_text("---\nname: review\ndescription: Review a change.\n---\n\nReview workflow.\n")
        self.fixture.commit(checkout, "replace a published tstack skill")
        self.fixture.command("sync")
        self.fixture.command("check")
        self.assertFalse((target / "tstack-full-stop").is_symlink())
        self.assertTrue((target / "tstack-review/SKILL.md").is_file())
        self.assertFalse((bundle / "skills/tstack-full-stop").exists())
        self.assertFalse((bundle / "upstream/tstack/skills/full-stop").exists())
        self.assertEqual([entry["name"] for entry in json.loads((bundle / "skills/catalog.json").read_text())],
                         ["tstack-review"])
        for other in ("mattpocock", "pstack"):
            self.assertTrue((self.repo / "plugins" / other / "skills" / (other + "-tdd/SKILL.md")).is_file())


if __name__ == "__main__":
    unittest.main()
