import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/skills.py"


class SharedSkillsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="shared-skills-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "library"
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.repo / "scripts/skills.py")
        (self.repo / "docs").mkdir()
        (self.repo / "docs/harnesses.md").write_text("Use the tools of the current harness.\n")
        (self.repo / ".gitignore").write_text(".cache/\n.skills-stage-*/\n")
        self.upstreams = {}
        for name, root in [("mattpocock", "."), ("pstack", "pstack")]:
            checkout = self.base / name
            checkout.mkdir()
            self.git("init", "--quiet", "--initial-branch=main", cwd=checkout)
            package = checkout if root == "." else checkout / root
            skill = package / "skills/tdd"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: tdd\ndescription: Test a public behavior.\n---\n\nRead [examples](examples.md).\n"
            )
            (skill / "examples.md").write_text("Original example for " + name + "\n")
            (package / "LICENSE").write_text("MIT fixture license\n")
            self.commit(checkout, "initial source")
            self.upstreams[name] = checkout
        self.config = {"version": 1, "sources": [
            {"id": name, "repository": checkout.as_uri(), "ref": "main",
             "root": "." if name == "mattpocock" else "pstack", "skill_roots": ["skills"]}
            for name, checkout in self.upstreams.items()
        ]}
        self.write_config()

    def git(self, *args, cwd=None):
        result = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
             "-c", "user.name=Skill Test", "-c", "user.email=skill-test@example.invalid", *args],
            cwd=cwd or self.repo, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.strip()

    def commit(self, checkout, message):
        self.git("add", ".", cwd=checkout)
        self.git("commit", "--quiet", "-m", message, cwd=checkout)

    def write_config(self):
        (self.repo / "sources.json").write_text(json.dumps(self.config))

    def command(self, *args, success=True, repo=None):
        repo = repo or self.repo
        result = subprocess.run([sys.executable, str(repo / "scripts/skills.py"), *args],
                                cwd=repo, capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def add_skill(self, name="new-skill"):
        checkout = self.upstreams["pstack"]
        folder = checkout / "pstack/skills" / name
        folder.mkdir()
        (folder / "SKILL.md").write_text("---\nname: " + name + "\ndescription: A newly published skill.\n---\n\nNew workflow.\n")
        self.commit(checkout, "add skill")

    def test_one_library_installs_for_all_harnesses_and_t3(self):
        self.command("sync")
        self.command("check")
        home = self.base / "home"
        self.command("install", "--agent", "t3", "--global", "--home", str(home))
        expected = [".agents/skills", ".claude/skills", ".pi/agent/skills",
                    ".gemini/config/skills", ".gemini/antigravity-cli/skills",
                    ".config/opencode/skills", ".cursor/skills"]
        for relative in expected:
            for name in ["mattpocock-tdd", "pstack-tdd"]:
                folder = home / relative / name
                self.assertTrue(folder.is_symlink())
                self.assertEqual(folder.resolve(), (self.repo / "skills" / name).resolve())
                self.assertIn("name: " + name, (folder / "SKILL.md").read_text())
                self.assertTrue((folder / "harness.md").is_file())
                self.assertIn("Original example", (folder / "source/examples.md").read_text())
        self.command("install", "--agent", "t3", "--global", "--home", str(home))
        project = self.base / "consumer project"
        self.command("install", "--agent", "all", "--project", str(project))
        for relative in [".agents/skills", ".claude/skills", ".pi/skills", ".opencode/skills", ".cursor/skills"]:
            self.assertTrue((project / relative / "pstack-tdd/SKILL.md").is_file())

    def test_sync_adds_updates_and_removes_only_managed_installed_skills(self):
        self.command("sync")
        target = self.base / "custom target"
        self.command("install", "--directory", str(target))
        unrelated = target / "my-own-skill"
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("My existing skill\n")
        matt = self.upstreams["mattpocock"]
        (matt / "skills/tdd/examples.md").write_text("Updated upstream example\n")
        self.commit(matt, "update existing skill resource")
        checkout = self.upstreams["pstack"]
        shutil.rmtree(checkout / "pstack/skills/tdd")
        self.add_skill()
        self.command("sync")
        self.assertFalse((target / "pstack-tdd").is_symlink())
        self.assertTrue((target / "pstack-new-skill/source/SKILL.md").is_file())
        self.assertEqual((target / "mattpocock-tdd/source/examples.md").read_text(), "Updated upstream example\n")
        self.assertEqual((unrelated / "SKILL.md").read_text(), "My existing skill\n")
        self.command("check")
        lock = (self.repo / "sources.lock.json").read_bytes()
        self.command("sync")
        self.assertEqual(lock, (self.repo / "sources.lock.json").read_bytes())

    def test_install_conflict_preserves_existing_work_before_creating_links(self):
        self.command("sync")
        home = self.base / "home"
        conflict = home / ".claude/skills/pstack-tdd"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("Keep this content\n")
        self.command("install", "--agent", "t3", "--global", "--home", str(home), success=False)
        self.assertEqual((conflict / "SKILL.md").read_text(), "Keep this content\n")
        self.assertFalse((home / ".agents/skills/mattpocock-tdd").exists())
        self.assertFalse((self.repo / ".cache/installations.json").exists())

    def test_local_edits_in_sources_and_exports_are_preserved(self):
        self.command("sync")
        lock = (self.repo / "sources.lock.json").read_bytes()
        for relative in ["upstream/pstack/skills/tdd/SKILL.md", "skills/pstack-tdd/SKILL.md"]:
            file = self.repo / relative
            original = file.read_text()
            file.write_text(original + "\nUser's local edit\n")
            self.command("sync", success=False)
            self.assertIn("User's local edit", file.read_text())
            self.assertEqual(lock, (self.repo / "sources.lock.json").read_bytes())
            file.write_text(original)

    def test_failed_second_source_does_not_publish_first_source_changes(self):
        self.command("sync")
        lock = (self.repo / "sources.lock.json").read_bytes()
        checkout = self.upstreams["mattpocock"]
        (checkout / "skills/tdd/examples.md").write_text("Changed upstream example\n")
        self.commit(checkout, "change source")
        self.config["sources"][1]["repository"] = (self.base / "missing-repo").as_uri()
        self.write_config()
        self.command("sync", success=False)
        self.assertEqual(lock, (self.repo / "sources.lock.json").read_bytes())
        self.assertNotIn("Changed", (self.repo / "upstream/mattpocock/skills/tdd/examples.md").read_text())

    def test_locked_sync_uses_exact_revision_after_upstream_advances(self):
        self.command("sync")
        lock = (self.repo / "sources.lock.json").read_bytes()
        self.add_skill()
        self.command("sync", "--locked")
        self.assertEqual(lock, (self.repo / "sources.lock.json").read_bytes())
        self.assertFalse((self.repo / "skills/pstack-new-skill").exists())
        self.command("sync")
        self.assertTrue((self.repo / "skills/pstack-new-skill/SKILL.md").is_file())

    def test_upstream_manifest_can_publish_a_new_category_and_retire_an_existing_skill(self):
        checkout = self.upstreams["mattpocock"]
        manifest = checkout / "plugin.json"
        manifest.write_text(json.dumps({"skills": ["./skills/tdd"]}))
        self.commit(checkout, "publish initial skill selection")
        self.config["sources"][0].pop("skill_roots")
        self.config["sources"][0]["skills_manifest"] = "plugin.json"
        self.write_config()
        self.command("sync")
        target = self.base / "installed"
        self.command("install", "--directory", str(target))
        folder = checkout / "new-category/new-workflow"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("---\nname: new-workflow\ndescription: A newly published category.\n---\n\nWorkflow.\n")
        manifest.write_text(json.dumps({"skills": ["./new-category/new-workflow"]}))
        self.commit(checkout, "publish new category and retire old skill")
        self.command("sync")
        self.command("check")
        self.assertTrue((target / "mattpocock-new-workflow/source/SKILL.md").is_file())
        self.assertFalse((target / "mattpocock-tdd").is_symlink())
        self.assertTrue((self.repo / "upstream/mattpocock/skills/tdd/SKILL.md").is_file())
        manifest.write_text(json.dumps({"skills": []}))
        self.commit(checkout, "unpublish all skills")
        self.command("sync")
        self.assertFalse((target / "mattpocock-new-workflow").is_symlink())
        self.assertTrue((target / "pstack-tdd/SKILL.md").is_file())

    def test_removing_the_last_skill_then_adding_one_again_refreshes_saved_installations(self):
        self.command("sync")
        target = self.base / "installed"
        self.command("install", "--directory", str(target))
        checkout = self.upstreams["pstack"]
        shutil.rmtree(checkout / "pstack/skills")
        self.commit(checkout, "remove the last skill")
        self.command("sync")
        self.command("check")
        self.assertFalse((target / "pstack-tdd").is_symlink())
        self.assertTrue((target / "mattpocock-tdd/source/SKILL.md").is_file())
        (checkout / "pstack/skills").mkdir()
        self.add_skill()
        self.command("sync")
        self.assertTrue((target / "pstack-new-skill/source/SKILL.md").is_file())

    def test_skill_move_preserves_its_name_and_skill_rename_replaces_its_link(self):
        self.command("sync")
        target = self.base / "installed"
        self.command("install", "--directory", str(target))
        checkout = self.upstreams["pstack"]
        moved = checkout / "pstack/skills/moved-folder"
        (checkout / "pstack/skills/tdd").rename(moved)
        self.commit(checkout, "move skill folder")
        self.command("sync")
        self.assertTrue((target / "pstack-tdd/source/examples.md").is_file())
        self.assertEqual((target / "pstack-tdd/source").resolve().name, "moved-folder")
        file = moved / "SKILL.md"
        file.write_text(file.read_text().replace("name: tdd\n", "name: renamed\n"))
        self.commit(checkout, "rename skill")
        self.command("sync")
        self.command("check")
        self.assertFalse((target / "pstack-tdd").is_symlink())
        self.assertTrue((target / "pstack-renamed/source/examples.md").is_file())

    def test_invalid_manifest_does_not_replace_previous_library(self):
        checkout = self.upstreams["mattpocock"]
        manifest = checkout / "plugin.json"
        manifest.write_text(json.dumps({"skills": "./skills"}))
        self.commit(checkout, "publish manifest")
        self.config["sources"][0].pop("skill_roots")
        self.config["sources"][0]["skills_manifest"] = "plugin.json"
        self.write_config()
        self.command("sync")
        lock = (self.repo / "sources.lock.json").read_bytes()
        manifest.write_text(json.dumps({"skills": ["../../outside"]}))
        self.commit(checkout, "invalid published path")
        self.command("sync", success=False)
        self.assertEqual(lock, (self.repo / "sources.lock.json").read_bytes())
        self.assertTrue((self.repo / "skills/mattpocock-tdd/source/SKILL.md").is_file())

    def test_custom_skill_is_exported_without_editing_upstream(self):
        folder = self.repo / "local/example"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("---\nname: example\ndescription: >-\n  A local workflow\n  with a folded description.\n---\n\nLocal instructions.\n")
        self.command("sync")
        self.command("check")
        self.assertTrue((self.repo / "skills/local-example/source/SKILL.md").is_file())
        self.assertEqual((folder / "SKILL.md").read_bytes(), (self.repo / "skills/local-example/source/SKILL.md").read_bytes())

    def test_embedded_skill_template_is_a_resource_not_a_second_export(self):
        checkout = self.upstreams["pstack"]
        template = checkout / "pstack/skills/tdd/templates/example"
        template.mkdir(parents=True)
        (template / "SKILL.md").write_text("A template with unfinished metadata, not an installed skill.\n")
        self.commit(checkout, "add embedded template")
        self.command("sync")
        self.command("check")
        catalog = json.loads((self.repo / "skills/catalog.json").read_text())
        self.assertEqual({entry["name"] for entry in catalog}, {"mattpocock-tdd", "pstack-tdd"})
        self.assertTrue((self.repo / "skills/pstack-tdd/source/templates/example/SKILL.md").is_file())

    def test_archive_cannot_write_through_escaping_symlink(self):
        self.command("sync")
        lock = (self.repo / "sources.lock.json").read_bytes()
        checkout = self.upstreams["pstack"]
        outside = self.base / "outside"
        (checkout / "pstack/escape").symlink_to(outside)
        self.commit(checkout, "unsafe source link")
        self.command("sync", success=False)
        self.assertFalse(outside.exists())
        self.assertEqual(lock, (self.repo / "sources.lock.json").read_bytes())

    def test_repository_update_refreshes_installations_and_refuses_dirty_work(self):
        self.command("sync")
        self.git("init", "--quiet", "--initial-branch=main")
        self.commit(self.repo, "initial library")
        remote = self.base / "remote.git"
        self.git("clone", "--quiet", "--bare", str(self.repo), str(remote))
        self.git("remote", "add", "origin", str(remote))
        self.git("fetch", "--quiet", "origin")
        self.git("branch", "--set-upstream-to=origin/main")
        target = self.base / "installed"
        self.command("install", "--directory", str(target))
        publisher = self.base / "publisher"
        self.git("clone", "--quiet", str(remote), str(publisher))
        self.add_skill()
        self.command("sync", repo=publisher)
        self.commit(publisher, "sync upstream")
        self.git("push", "--quiet", cwd=publisher)
        self.command("update")
        self.assertTrue((target / "pstack-new-skill/source/SKILL.md").is_file())
        self.assertEqual(self.git("rev-parse", "HEAD"), self.git("rev-parse", "HEAD", cwd=publisher))
        source = self.repo / "sources.json"
        source.write_text(source.read_text() + "\n")
        self.command("update", success=False)
        self.assertTrue(source.read_text().endswith("\n"))


if __name__ == "__main__":
    unittest.main()
