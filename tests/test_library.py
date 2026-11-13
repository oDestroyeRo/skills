import json
from pathlib import Path
import re
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
            self.assertFalse((checkout / "skills").exists())
            folders = {}
            for file in (checkout / "plugins").glob("*/skills/catalog.json"):
                for entry in json.loads(file.read_text()):
                    folders[entry["name"]] = file.parent / entry["name"]
            targets = [".agents/skills", ".claude/skills", ".pi/agent/skills", ".gemini/config/skills",
                       ".gemini/antigravity-cli/skills", ".config/opencode/skills", ".cursor/skills",
                       ".dsh/skills"]
            for relative in targets:
                directory = home / relative
                self.assertEqual({path.name for path in directory.iterdir()}, set(folders))
                for name, folder in folders.items():
                    installed = directory / name
                    self.assertEqual(installed.resolve(), folder.resolve())
                    text = (installed / "SKILL.md").read_text()
                    for link in re.findall(r'\]\(([^)]+)\)', text):
                        self.assertTrue((installed.resolve() / link).exists(), (name, link))
            self.assertEqual(registry.read_bytes() if registry.exists() else None, previous_registry)


if __name__ == "__main__":
    unittest.main()
