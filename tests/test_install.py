import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="p3-install-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source with spaces"
        self.source.mkdir()
        shutil.copy2(Path(__file__).resolve().parents[1] / "install.sh", self.source)
        for name in ["p3-help", "p3-mode"]:
            skill = self.source / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
        self.project = self.root / "project with spaces"
        self.home = self.root / "home"
        self.env = dict(os.environ, HOME=str(self.home))
        self.env.pop("CLAUDE_CONFIG_DIR", None)

    def run_install(self, *args):
        return subprocess.run(
            ["bash", str(self.source / "install.sh"), *map(str, args)],
            env=self.env, text=True, capture_output=True, check=True,
        )

    def assert_skill(self, directory, name="p3-help"):
        link = directory / name
        self.assertTrue(link.is_symlink(), str(link))
        self.assertEqual(link.resolve(), self.source / "skills" / name)
        self.assertTrue((link / "SKILL.md").is_file())

    def test_project_installs_for_both_providers(self):
        self.run_install("--project", self.project)
        self.assert_skill(self.project / ".agents/skills")
        self.assert_skill(self.project / ".claude/skills")
        self.assertFalse(self.home.exists())

    def test_global_installs_for_both_providers(self):
        self.run_install()
        self.assert_skill(self.home / ".agents/skills")
        self.assert_skill(self.home / ".claude/skills")

    def test_claude_config_override(self):
        custom = self.root / "custom claude"
        self.env["CLAUDE_CONFIG_DIR"] = str(custom)
        self.run_install("--provider", "claude")
        self.assert_skill(custom / "skills")
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".claude").exists())

    def test_provider_selection_and_argument_order(self):
        self.run_install("--provider", "codex", "--project", self.project)
        self.assert_skill(self.project / ".agents/skills")
        self.assertFalse((self.project / ".claude").exists())
        self.run_install("--project", self.project, "--provider", "claude")
        self.assert_skill(self.project / ".claude/skills")

    def test_reinstall_is_idempotent(self):
        self.run_install("--project", self.project)
        link = self.project / ".agents/skills/p3-help"
        before = link.lstat().st_ino
        result = self.run_install("--project", self.project)
        self.assertEqual(link.lstat().st_ino, before)
        self.assertIn("unchanged 2", result.stdout)
        self.assert_skill(self.project / ".claude/skills")

    def test_preserves_existing_skill_and_foreign_links(self):
        target = self.project / ".claude/skills"
        kept = target / "p3-help"
        kept.mkdir(parents=True)
        (kept / "SKILL.md").write_text("user skill")
        foreign = self.root / "foreign"
        foreign.mkdir()
        (target / "p3-mode").symlink_to(foreign)
        self.run_install("--project", self.project)
        self.assertEqual((kept / "SKILL.md").read_text(), "user skill")
        self.assertEqual((target / "p3-mode").resolve(), foreign)
        self.assert_skill(self.project / ".agents/skills")

    def test_preserves_dangling_foreign_link(self):
        target = self.project / ".agents/skills"
        target.mkdir(parents=True)
        missing = self.root / "missing"
        (target / "p3-help").symlink_to(missing)
        self.run_install("--project", self.project)
        self.assertEqual(os.readlink(target / "p3-help"), str(missing))
        self.assert_skill(self.project / ".claude/skills")

    def test_invalid_arguments_do_not_write(self):
        for args in [("--provider", "wrong"), ("--project",), ("--project", "--provider"), ("--unknown",)]:
            result = subprocess.run(["bash", str(self.source / "install.sh"), *args], env=self.env, capture_output=True)
            self.assertEqual(result.returncode, 2)
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
