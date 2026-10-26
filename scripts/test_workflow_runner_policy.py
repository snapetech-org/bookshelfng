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
SETUP_GITHUB_CLI = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "actions"
    / "setup-github-cli"
    / "action.yml"
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
    def test_public_fork_static_validation_uses_the_secretless_jit_group(self) -> None:
        source = (WORKFLOW.parent / "fork-safe-validation.yml").read_text(encoding="utf-8")
        job = job_block(source, "validate")

        self.assertIn("group: public-fork-jit", job)
        self.assertIn("disposable VM", job)
        self.assertIn("public-pr-bookshelfng", job)
        self.assertIn("github.event.pull_request.head.repo.fork == true", job)
        self.assertIn("permissions:", job)
        self.assertIn("contents: read", job)
        self.assertNotIn("ubuntu-latest", job)
        self.assertNotIn("secrets:", job)

    def test_github_cli_setup_uses_a_pinned_github_release_asset(self) -> None:
        action = SETUP_GITHUB_CLI.read_text(encoding="utf-8")
        self.assertIn("version=2.103.2", action)
        self.assertIn(
            "https://github.com/cli/cli/releases/download/v${version}/${archive_name}",
            action,
        )
        self.assertIn(
            "62ccf747115ddc61237efffdde66a3c8f70ba249433dc64f70801089b59c59c8",
            action,
        )
        self.assertIn("sha256sum --check --status", action)
        self.assertIn("tar --extract --gzip", action)
        self.assertIn('>> "$GITHUB_PATH"', action)
        self.assertIn("gh --version", action)
        self.assertNotIn("cli.github.com", action)
        self.assertNotIn("apt-get", action)

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
        self.assertNotIn("retry-release-distribution-hosted", source)
        self.assertNotIn("NG_HOSTED_FIRST", source)
        self.assertNotIn("NG_FORCE_JIT", source)

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

    def test_chocolatey_verifier_uses_the_private_windows_jit_group(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        job = job_block(source, "test-chocolatey-package-verifier")
        self.assertIn("group: packer-windows", job)
        self.assertIn("- on-demand", job)
        self.assertIn("- bookshelfng", job)
        self.assertNotIn("windows-latest", job)
        self.assertIn("inputs.release_tag == ''", job)

    def test_new_release_build_and_publish_path_stays_on_private_jit(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        dispatch = event_block(source, "workflow_dispatch")
        self.assertIn("      release_build_tag:", dispatch)

        for job_name in ("build", "publish-images", "container-scan", "release"):
            job = job_block(source, job_name)
            with self.subTest(job=job_name):
                self.assertIn("inputs.release_build_tag", job)
                self.assertIn('"group":"ng-shared-main-jit"', job)
                self.assertIn('"ng-main-run-{0}"', job)

        publisher = job_block(source, "publish-private-release")
        self.assertIn("github.ref == 'refs/heads/main'", publisher)
        self.assertIn("vars.BOOKSHELFNG_RELEASE_READY == 'true'", publisher)
        self.assertIn("uses: ./.github/workflows/release-publication.yml", publisher)
        self.assertIn("softcover_digest: ${{ needs.publish-images.outputs.softcover_digest }}", publisher)
        self.assertIn("hardcover_digest: ${{ needs.publish-images.outputs.hardcover_digest }}", publisher)

        release_build = (WORKFLOW.parent / "release-build.yml").read_text(encoding="utf-8")
        for job_name, role in (
            ("validate", "release-build-validate"),
            ("build-platform-runtime-packs", "release-build-runtime-packs"),
            ("build-release-assets", "release-build-assets"),
            ("build-linux-packages", "release-build-linux-packages"),
        ):
            job = job_block(release_build, job_name)
            with self.subTest(release_job=job_name):
                self.assertIn("inputs.tag != ''", job)
                self.assertIn(f'"gha-{{0}}-{role}"', job)
                self.assertNotIn(f"runs-on: ubuntu-22.04\n", job)

        publication = (WORKFLOW.parent / "release-publication.yml").read_text(encoding="utf-8")
        self.assertIn("  workflow_call:", publication)
        self.assertIn("inputs.tag != ''", job_block(publication, "prepare"))
        self.assertIn('"gha-{0}-release-prepare"', job_block(publication, "prepare"))
        self.assertIn('"gha-{0}-publish-release-assets"', job_block(publication, "publish-assets"))

        distribution = (WORKFLOW.parent / "release-distribution.yml").read_text(encoding="utf-8")
        for job_name, role in (("publish-ppa", "publish-ppa"), ("publish-chocolatey", "publish-chocolatey")):
            job = job_block(distribution, job_name)
            with self.subTest(publisher=job_name):
                self.assertIn(f'"gha-{{0}}-{role}"', job)
                self.assertNotIn("runs-on: windows-latest", job)
        chocolatey = job_block(distribution, "publish-chocolatey")
        self.assertIn("dotnet pack", chocolatey)
        self.assertIn("dotnet nuget push", chocolatey)

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

    def test_build_uses_private_jit_and_excludes_public_fork_code(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        build = source.split("  build:\n", 1)[1].split("\n  publish-images:", 1)[0]
        self.assertIn('"group":"ng-shared-main-jit"', build)
        self.assertIn('"ng-shared-main-bookshelfng"', build)
        self.assertIn('"ng-main-run-{0}"', build)
        self.assertIn("github.run_id", build)
        self.assertIn("github.event.pull_request.head.repo.full_name == github.repository", build)
        self.assertNotIn("NG_HOSTED_FIRST", source)
        self.assertNotIn("NG_FORCE_JIT", source)
        self.assertNotIn("ubuntu-latest", source)
        self.assertIn("  pull_request:", source)
        self.assertNotIn("TRUSTED_MAIN_RUNNERS_ENABLED", source)

    def test_release_jobs_route_to_private_jit_without_hosted_fallback(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        for job_name in ("publish-images", "container-scan", "release"):
            with self.subTest(job=job_name):
                job = job_block(source, job_name)
                runner = re.search(r"(?m)^    runs-on: (?P<runner>[^\n]+)$", job)
                self.assertIsNotNone(runner)
                self.assertIn('"group":"ng-shared-main-jit"', runner.group("runner"))
                self.assertIn('"ng-shared-main-bookshelfng"', runner.group("runner"))
                self.assertIn('"ng-main-run-{0}"', runner.group("runner"))
                self.assertNotIn("ubuntu-latest", runner.group("runner"))

    def test_playwright_installer_uses_linux_dependencies(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Install Chromium and system dependencies on Linux", source)
        self.assertIn("install --with-deps chromium", source)
        self.assertNotIn("runner.environment", source)

    def test_security_scans_use_private_jit_and_skip_public_fork_code(self) -> None:
        workflow_dir = WORKFLOW.parent
        for workflow_name, job_name in (
            ("codeql.yml", "analyze"),
            ("semgrep-community.yml", "semgrep"),
            ("trivy-filesystem.yml", "trivy"),
        ):
            source = (workflow_dir / workflow_name).read_text(encoding="utf-8")
            job = source.split(f"  {job_name}:\n", 1)[1]
            runner = re.search(r"(?m)^    runs-on: (?P<runner>[^\n]+)$", job)
            self.assertIsNotNone(runner, workflow_name)
            self.assertIn('"group":"ng-shared-main-jit"', runner.group("runner"))
            self.assertIn('"ng-shared-main-bookshelfng"', runner.group("runner"))
            self.assertIn('"ng-main-run-{0}"', runner.group("runner"))
            self.assertIn("github.event.pull_request.head.repo.full_name == github.repository", job)
            self.assertNotIn("ubuntu-latest", runner.group("runner"))
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
        self.assertIn('"group":"ng-shared-main-jit"', filesystem)
        self.assertIn("github.event.pull_request.head.repo.full_name == github.repository", filesystem)
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
