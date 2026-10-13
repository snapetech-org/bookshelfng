from pathlib import Path
import re
import unittest


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
        runner = next(
            line.strip()
            for line in source.splitlines()
            if line.lstrip().startswith("runs-on:") and "self-hosted" in line
        )
        self.assertNotIn("github.event_name == 'pull_request'", runner)
        self.assertIn(
            "github.event_name == 'push' && github.ref == 'refs/heads/main'",
            runner,
        )
        self.assertIn(
            "(github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main')",
            runner,
        )
        self.assertNotIn("startsWith(github.ref, 'refs/heads/')", runner)
        self.assertIn("fromJSON('[\"self-hosted\",\"Linux\",\"X64\",\"host\"]')", runner)
        self.assertIn("fromJSON('[\"ubuntu-latest\"]')", runner)

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
