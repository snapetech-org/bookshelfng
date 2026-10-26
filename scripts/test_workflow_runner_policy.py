import re
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "build.yml"
RELEASE_DISTRIBUTION = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "release-distribution.yml"
)
RETRY_RELEASE_DISTRIBUTION = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "retry-release-distribution.yml"
)


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


def job_block(source: str, name: str) -> str:
    lines = source.splitlines()
    start = lines.index(f"  {name}:")
    body = []
    for line in lines[start + 1 :]:
        if line.strip() and len(line) - len(line.lstrip()) <= 2:
            break
        body.append(line)
    return "\n".join(body)


class WorkflowRunnerPolicyTests(unittest.TestCase):
    def test_manual_distribution_reuses_published_outputs_and_allows_explicit_announcement(
        self,
    ) -> None:
        distribution = RELEASE_DISTRIBUTION.read_text(encoding="utf-8")
        retry = RETRY_RELEASE_DISTRIBUTION.read_text(encoding="utf-8")
        self.assertRegex(distribution, r"(?m)^  workflow_call:$")
        self.assertNotRegex(distribution, r"(?m)^  workflow_dispatch:")
        self.assertRegex(retry, r"(?m)^  workflow_call:$")
        self.assertIn("inputs.skip_announcement != true", distribution)
        self.assertNotIn("inputs.recovery_only != true", distribution)
        self.assertIn("Require an already-published release for publisher recovery", distribution)
        self.assertIn("gh release download \"$TAG\"", distribution)
        self.assertIn("recovery_only: true", retry)
        self.assertIn("skip_announcement: ${{ inputs.skip_announcement }}", retry)
        self.assertIn("true by default for retries", retry)
        self.assertIn("softcover_digest: ${{ inputs.softcover_digest }}", retry)
        self.assertIn("hardcover_digest: ${{ inputs.hardcover_digest }}", retry)
        self.assertIn("Previously published BookshelfNG release tag to retry", retry)

    def test_release_retry_has_an_owner_only_trusted_main_jit_entrypoint(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        dispatch = event_block(source, "workflow_dispatch")
        for name in (
            "release_tag",
            "release_softcover_digest",
            "release_hardcover_digest",
            "release_channels",
            "release_chocolatey_use_main_packaging",
            "release_skip_announcement",
        ):
            with self.subTest(input=name):
                self.assertIn(f"      {name}:", dispatch)

        retry_job = job_block(source, "retry-release-distribution")
        for required in (
            "github.actor == 'snapetech'",
            "github.ref == 'refs/heads/main'",
            "inputs.release_tag != ''",
            "inputs.pr_number == ''",
            "runs-on: ${{ fromJSON(format('",
            '"gha-{0}-retry-release-distribution"',
            "permissions:",
            "contents: read",
            "packages: write",
            "id-token: write",
            "Validate published release and requested JIT channels",
            "Validate Discord destination",
            "Publish AUR package",
            "Trigger COPR build",
            "Publish signed Helm OCI chart",
            "Send complete release announcement",
            "DISCORD_WEBHOOK: ${{ secrets.DISCORD_RELEASE_WEBHOOK }}",
            "inputs.release_skip_announcement != true",
        ):
            with self.subTest(required=required):
                self.assertIn(required, retry_job)
        self.assertNotIn("uses: ./.github/workflows/retry-release-distribution.yml", retry_job)
        self.assertNotIn("|| 'ubuntu-latest'", retry_job)

        hosted_retry = job_block(source, "retry-release-distribution-hosted")
        self.assertIn("vars.NG_HOSTED_FIRST == 'true'", hosted_retry)
        self.assertIn("vars.NG_FORCE_JIT != 'true'", hosted_retry)
        self.assertIn("github.run_attempt == 1", hosted_retry)
        self.assertIn(
            "uses: ./.github/workflows/retry-release-distribution.yml", hosted_retry
        )
        self.assertIn(
            "skip_announcement: ${{ inputs.release_skip_announcement }}", hosted_retry
        )
        self.assertNotIn("secrets: inherit", hosted_retry)

        release_retry = RETRY_RELEASE_DISTRIBUTION.read_text(encoding="utf-8")
        call = event_block(release_retry, "workflow_call")
        for name in (
            "tag",
            "softcover_digest",
            "hardcover_digest",
            "channels",
            "chocolatey_use_main_packaging",
            "skip_announcement",
            "AUR_SSH_KEY",
            "COPR_WEBHOOK_URL",
            "GPG_PRIVATE_KEY",
            "LAUNCHPAD_PPA",
            "CHOCOLATEY_API_KEY",
            "DISCORD_RELEASE_WEBHOOK",
        ):
            with self.subTest(reusable_workflow_input=name):
                self.assertIn(f"      {name}:", call)

    def test_chocolatey_verifier_needs_hosted_runner_mode(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        job = job_block(source, "test-chocolatey-package-verifier")
        self.assertIn("vars.NG_HOSTED_FIRST == 'true'", job)
        self.assertIn("runs-on: windows-latest", job)
        self.assertIn("inputs.release_tag == ''", job)

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

    def test_build_uses_the_shared_pool_only_for_trusted_main(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        build = source.split("  build:\n", 1)[1].split("\n  publish-images:", 1)[0]
        self.assertIn('"group":"ng-shared-main-jit"', build)
        self.assertIn('"ng-shared-main-bookshelfng"', build)
        self.assertIn('"ng-main-run-{0}"', build)
        self.assertIn("github.run_id", build)
        self.assertIn(
            "contains(fromJSON('[\"push\",\"workflow_dispatch\",\"schedule\",\"release\",\"repository_dispatch\"]'), github.event_name)",
            build,
        )
        self.assertIn(
            "github.ref == 'refs/heads/main' || (github.ref_type == 'tag' && startsWith(github.ref_name, 'v'))",
            build,
        )
        self.assertIn("vars.NG_HOSTED_FIRST", build)
        self.assertIn("vars.NG_FORCE_JIT", build)
        self.assertIn("github.run_attempt > 1", build)
        self.assertIn("|| 'ubuntu-latest'", build)
        self.assertIn("  pull_request:", source)
        self.assertNotIn("TRUSTED_MAIN_RUNNERS_ENABLED", source)

    def test_release_jobs_route_trusted_tags_with_hosted_fallback(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        for job_name in ("publish-images", "container-scan", "release"):
            with self.subTest(job=job_name):
                job = job_block(source, job_name)
                runner = re.search(r"(?m)^    runs-on: (?P<runner>[^\n]+)$", job)
                self.assertIsNotNone(runner)
                self.assertIn('"group":"ng-shared-main-jit"', runner.group("runner"))
                self.assertIn('"ng-shared-main-bookshelfng"', runner.group("runner"))
                self.assertIn('"ng-main-run-{0}"', runner.group("runner"))
                self.assertIn(
                    "github.ref_type == 'tag' && startsWith(github.ref_name, 'v')",
                    runner.group("runner"),
                )
                self.assertIn("|| 'ubuntu-latest'", runner.group("runner"))

    def test_playwright_installer_uses_hosted_linux_dependencies(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Install Chromium and system dependencies on Linux", source)
        self.assertIn("install --with-deps chromium", source)
        self.assertNotIn("runner.environment", source)

    def test_security_scans_use_the_shared_pool_only_on_trusted_main_runs(self) -> None:
        workflow_dir = WORKFLOW.parent
        for workflow_name, job_name in (
            ("codeql.yml", "analyze"),
            ("semgrep-community.yml", "semgrep"),
        ):
            source = (workflow_dir / workflow_name).read_text(encoding="utf-8")
            job = source.split(f"  {job_name}:\n", 1)[1]
            runner = re.search(r"(?m)^    runs-on: (?P<runner>[^\n]+)$", job)
            self.assertIsNotNone(runner, workflow_name)
            self.assertIn('"group":"ng-shared-main-jit"', runner.group("runner"))
            self.assertIn('"ng-shared-main-bookshelfng"', runner.group("runner"))
            self.assertIn('"ng-main-run-{0}"', runner.group("runner"))
            self.assertIn("github.event_name == 'push'", runner.group("runner"))
            self.assertIn("github.event_name == 'workflow_dispatch'", runner.group("runner"))
            self.assertIn("github.event_name == 'schedule'", runner.group("runner"))
            self.assertIn("github.ref == 'refs/heads/main'", runner.group("runner"))
            self.assertIn("|| 'ubuntu-latest'", runner.group("runner"))
        semgrep = (workflow_dir / "semgrep-community.yml").read_text(encoding="utf-8")
        self.assertIn("docker info", semgrep)
        self.assertIn("docker run", semgrep)

    def test_full_severity_trivy_audits_use_private_runners_and_include_unfixed_cves(self) -> None:
        workflow_dir = WORKFLOW.parent
        filesystem = (workflow_dir / "trivy-filesystem.yml").read_text(encoding="utf-8")
        published_images = (
            workflow_dir / "trivy-published-image-audit.yml"
        ).read_text(encoding="utf-8")
        scanner = (WORKFLOW.parents[2] / "scripts" / "security-scan-local.sh").read_text(
            encoding="utf-8"
        )

        self.assertIn("full_vulnerability_audit:", filesystem)
        self.assertIn(
            "inputs.full_vulnerability_audit == true && fromJSON(format(", filesystem
        )
        self.assertIn('TRIVY_IGNORE_UNFIXED: ${{', filesystem)
        self.assertIn("TRIVY_SEVERITY:-HIGH,CRITICAL", scanner)
        self.assertIn("TRIVY_IGNORE_UNFIXED:-true", scanner)
        self.assertIn("Full-severity published image audit", published_images)
        self.assertIn('gha-{0}-trivy-image-audit', published_images)
        self.assertNotIn("ubuntu-latest", published_images)
        self.assertIn("UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL", published_images)
        self.assertIn("ignore-unfixed: false", published_images)


if __name__ == "__main__":
    unittest.main()
