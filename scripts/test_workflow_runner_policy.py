import re
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "build.yml"


def event_block(source: str, event: str) -> str:
    lines = source.splitlines()
    start = lines.index(f"  {event}:")
    body = []
    for line in lines[start + 1 :]:
        if line.strip() and len(line) - len(line.lstrip()) <= 2:
            break
        body.append(line)
    return "\n".join(body)


def named_step(source: str, name: str) -> str:
    lines = source.splitlines()
    start = next(
        index for index, line in enumerate(lines) if line.strip() == f"- name: {name}"
    )
    body = []
    for line in lines[start + 1 :]:
        if line.startswith("      - name: "):
            break
        body.append(line)
    return "\n".join(body)


class WorkflowRunnerPolicyTests(unittest.TestCase):
    def test_push_trigger_is_main_only(self) -> None:
        push = event_block(WORKFLOW.read_text(encoding="utf-8"), "push")
        match = re.search(
            r"(?m)^    branches:\n(?P<entries>(?:^      - [^\n]*\n)+)", push
        )
        self.assertIsNotNone(match)
        branches = [
            line.strip().removeprefix("- ")
            for line in match.group("entries").splitlines()
        ]
        self.assertEqual(branches, ["main"])

    def test_build_uses_a_github_hosted_runner(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(source, r"(?m)^    runs-on: ubuntu-latest$")
        self.assertNotIn("self-hosted", source)
        self.assertNotIn("TRUSTED_MAIN_RUNNERS_ENABLED", source)

    def test_playwright_installer_uses_hosted_linux_dependencies(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Install Chromium and system dependencies on GitHub-hosted Linux", source)
        self.assertIn("install --with-deps chromium", source)
        self.assertNotIn("runner.environment", source)


if __name__ == "__main__":
    unittest.main()
