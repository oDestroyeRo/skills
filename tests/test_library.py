import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CheckedInLibraryTest(unittest.TestCase):
    def test_real_library_can_move_and_install_in_every_provider_directory(self):
        registry = ROOT / ".cache/installations.json"
        previous_registry = registry.read_bytes() if registry.exists() else None
        with tempfile.TemporaryDirectory(prefix="skills-library-test-") as temporary:
            base = Path(temporary)
            checkout = base / "relocated checkout"

            def ignore(directory, names):
                return {".git", ".cache", "__pycache__", "node_modules", "dist"} & set(names) if Path(directory) == ROOT else set()

            shutil.copytree(ROOT, checkout, symlinks=True, ignore=ignore)
            home = base / "user home"
            for args in [("check",), ("install", "--agent", "all", "--global", "--home", str(home))]:
                result = subprocess.run([sys.executable, str(checkout / "scripts/skills.py"), *args],
                                        cwd=checkout, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            catalog = json.loads((checkout / "skills/catalog.json").read_text())
            targets = [".agents/skills", ".claude/skills", ".pi/agent/skills", ".gemini/config/skills",
                       ".gemini/antigravity-cli/skills", ".config/opencode/skills", ".cursor/skills"]
            for relative in targets:
                directory = home / relative
                self.assertEqual({path.name for path in directory.iterdir()}, {entry["name"] for entry in catalog})
                for entry in catalog:
                    installed = directory / entry["name"]
                    package = checkout / ("local" if entry["source"] == "local" else "upstream/" + entry["source"])
                    self.assertEqual(installed.resolve(), (checkout / "skills" / entry["name"]).resolve())
                    self.assertEqual((installed / "source/SKILL.md").resolve(), (package / entry["path"]).resolve())
                    self.assertEqual((installed / "library").resolve(), package.resolve())
                    self.assertTrue((installed / "harness.md").is_file())
            self.assertEqual(registry.read_bytes() if registry.exists() else None, previous_registry)


if __name__ == "__main__":
    unittest.main()
