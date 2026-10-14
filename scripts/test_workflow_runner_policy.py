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

    def test_pull_requests_never_select_the_persistent_runner(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        runner_match = re.search(r"(?m)^    runs-on: (?P<runner>[^\n]+)$", source)
        self.assertIsNotNone(runner_match)
        runner = runner_match.group("runner")
        main_condition = (
            "((github.event_name == 'push' && github.ref == 'refs/heads/main') "
            "|| (github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'))"
        )
        expected = (
            "$" + "{{ (" + main_condition
            + " && vars.TRUSTED_MAIN_RUNNERS_ENABLED == 'true') "
            + "&& 'trusted-main' || 'ubuntu-latest' }}"
        )
        self.assertEqual(runner, expected)
        self.assertNotIn("github.event_name == 'pull_request'", runner)
        self.assertNotIn("startsWith(github.ref, 'refs/heads/')", runner)
        self.assertNotIn("fromJSON", runner)

    def test_playwright_installer_matches_runner_environment(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self_hosted = named_step(source, "Install Chromium on self-hosted Linux")
        hosted = named_step(
            source, "Install Chromium and system dependencies on GitHub-hosted Linux"
        )

        self.assertIn("runner.os == 'Linux'", self_hosted)
        self.assertIn("runner.environment == 'self-hosted'", self_hosted)
        self.assertIn("playwright.ps1 install chromium", self_hosted)
        self.assertNotIn("--with-deps", self_hosted)
        self.assertIn("runner.os == 'Linux'", hosted)
        self.assertIn("runner.environment != 'self-hosted'", hosted)
        self.assertIn("--with-deps chromium", hosted)


if __name__ == "__main__":
    unittest.main()
