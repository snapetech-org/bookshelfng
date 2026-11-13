import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


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
    def test_release_dispatch_selects_public_hosted_runners(self) -> None:
        source = (WORKFLOWS / "build.yml").read_text(encoding="utf-8")
        self.assertIn("options: [public]", source)
        for name in (
            "test-chocolatey-package-verifier",
            "retry-release-distribution",
            "build",
            "publish-images",
            "container-scan",
            "release",
        ):
            job = job_block(source, name)
            expected = "runs-on: windows-2025" if name == "test-chocolatey-package-verifier" else "runs-on: ubuntu-24.04"
            with self.subTest(job=name):
                self.assertIn(expected, job)

    def test_reusable_release_workflows_use_hosted_runners(self) -> None:
        for filename in (
            "release-build.yml",
            "release-distribution.yml",
            "release-publication.yml",
        ):
            source = (WORKFLOWS / filename).read_text(encoding="utf-8")
            with self.subTest(workflow=filename):
                self.assertIn("# ng-runner-policy: hosted-compatible-v1", source)
                self.assertNotIn('"group":"ng-shared-main-jit"', source)
                self.assertNotIn("private-jit-only", source)

    def test_extra_platform_release_restore_uses_available_runtime_patch(self) -> None:
        source = (WORKFLOWS / "release-build.yml").read_text(encoding="utf-8")
        job = job_block(source, "build-release-assets")
        self.assertIn("--msbuild-arg=-p:TargetLatestRuntimePatch=false", job)
        self.assertIn("--msbuild-arg=-p:RuntimeFrameworkVersion=10.0.15", job)
        props = (ROOT / "src/Targets/PublishAllRids.targets").read_text(encoding="utf-8")
        self.assertEqual(props.count("RuntimeFrameworkVersion=10.0.15</AdditionalProperties>"), 2)
        self.assertNotIn("DOTNETVERSION:", job)

    def test_extra_platform_runtime_packs_use_current_servicing_sources(self) -> None:
        builder = (ROOT / "scripts/build-dotnet10-platform-runtime-packs.sh").read_text(encoding="utf-8")
        self.assertIn('readonly runtime_tag="v10.0.15"', builder)
        self.assertIn('readonly linux_x86_runtime_version="10.0.15"', builder)
        self.assertIn('readonly freebsd_runtime_version="10.0.15"', builder)
        self.assertIn("'$(TargetOS)' != 'freebsd'", builder)
        self.assertIn('<PatchVersion>13</PatchVersion>', builder)
        self.assertIn('<PatchVersion>15</PatchVersion>', builder)
        self.assertIn('<AspNetCorePatchVersion>14</AspNetCorePatchVersion>', builder)
        self.assertIn('<AspNetCorePatchVersion>15</AspNetCorePatchVersion>', builder)
        self.assertIn('<MicrosoftNETCoreAppRefPackageVersion>10.0.14</MicrosoftNETCoreAppRefPackageVersion>', builder)
        self.assertIn('<MicrosoftNETCoreAppRefPackageVersion>10.0.15</MicrosoftNETCoreAppRefPackageVersion>', builder)
        self.assertIn('patch_aspnet_sources linux-x86', builder)
        self.assertIn('patch_aspnet_sources freebsd-x64', builder)
        freebsd_phase = builder.split("# Build FreeBSD from the same Microsoft servicing sources", 1)[1]
        self.assertIn("patch_freebsd_runtime_sources\nbuild_freebsd_runtime", freebsd_phase)
        self.assertIn('docker run --rm --user 0:0', builder)
        self.assertIn('rm -rf /work/runtime /work/aspnetcore', builder)
        self.assertNotIn('rm -rf "$runtime_repo" "$aspnet_repo"', builder)
        self.assertIn("cross-freebsd-14-amd64@sha256:", builder)
        self.assertNotIn("freebsd_archive_url", builder)
        publication = (WORKFLOWS / "release-publication.yml").read_text(encoding="utf-8")
        self.assertEqual(publication.count(".10.0.15.nupkg"), 6)
        self.assertNotIn(".10.0.12.nupkg", publication)

    def test_ordinary_manual_workflows_do_not_require_private_capacity(self) -> None:
        for path in WORKFLOWS.glob("*.yml"):
            if path.name in {"build.yml", "fork-safe-validation.yml"}:
                continue
            source = path.read_text(encoding="utf-8")
            with self.subTest(workflow=path.name):
                self.assertNotIn("private-jit-only", source)
                self.assertNotIn("options: [private]", source)
                self.assertNotIn('"group":"ng-shared-main-jit"', source)

    def test_public_fork_validation_keeps_disposable_isolation(self) -> None:
        source = (WORKFLOWS / "fork-safe-validation.yml").read_text(encoding="utf-8")
        job = job_block(source, "validate")
        self.assertIn("group: public-fork-jit", job)
        self.assertIn("contents: read", job)
        self.assertNotIn("secrets:", job)

    def test_owner_pr_metadata_jobs_keep_exact_private_isolation(self) -> None:
        source = (WORKFLOWS / "build.yml").read_text(encoding="utf-8")
        for name in ("dispatch-owner-pr", "report-owner-pr-check"):
            job = job_block(source, name)
            with self.subTest(job=name):
                self.assertIn('"group":"ng-shared-main-jit"', job)
                self.assertIn('"ng-shared-main-bookshelfng"', job)
                self.assertIn("github.run_id", job)

    def test_codeql_remains_disabled(self) -> None:
        names = {path.name.lower() for path in WORKFLOWS.glob("*.yml")}
        self.assertFalse(any("codeql" in name for name in names))


if __name__ == "__main__":
    unittest.main()
