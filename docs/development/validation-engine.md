# Validation engine

BookshelfNG keeps NUnit and `test.sh` as the native unit-test runner. The
validation engine records the source, discovered C# test files, built test
assemblies, runner identity, and native NUnit result counts used for each run.

## Run locally

Build the test package first. `build.sh` clears `_tests` and `_output`, so use a
disposable worktree when those directories contain artifacts you need to keep.

```sh
./build.sh --backend --frontend
node scripts/validation-engine/engine.mjs --plan
node scripts/validation-engine/engine.mjs --tests-only
```

The engine accepts the repository's two declared Node versions: local Volta
`20.11.1` and CI mise `20.19.4` (CI requires `20.19.4`). It requires .NET SDK
`10.0.401`. The plan checks all ten Linux x64 test assemblies before execution.
Its native test task runs `./test.sh Linux Unit Test` with the same
category filters as CI and requires the test runner's NUnit XML summary. It
reports total, passed, failed, skipped, and inconclusive cases; a missing or
zero-case result cannot pass. Failed NUnit receipts also include up to 100 case
names so CI failures can be identified from the machine-readable evidence.

The engine writes task progress to stderr as tasks start and finish, with a
once-per-minute heartbeat during long tasks. It runs up to two independent
tasks at a time within a stage, respecting task dependencies and shared-output
groups. The engine contract suite can now run alongside the native NUnit test
process. NUnit still owns all ten test assemblies in one invocation so its
filters and native result accounting stay intact. Progress lists each active
task and its elapsed time. GitHub displays step summaries after the workflow
step finishes, so live updates appear in the step log.

## Evidence and CI

Every run has a private temporary evidence directory with task logs and a
receipt. The candidate identity binds the Git commit and diff, explicit build
and workflow inputs, source test inventory, and SHA-256 digests of the ten
compiled test assemblies. The engine checks that identity before and after each
task batch and rejects successful results if source or compiled artifacts
change while concurrent tasks are running. Each task owns separate logs and
NUnit result paths. It refuses overlapping runs for the same checkout and gives
runtime probes and children an explicit environment allowlist and each task's
declared settings.
Every task gets run-owned home, temporary, XDG, and .NET CLI directories. NuGet
packages use a private cache shared only within the validation run. Test tasks
use `CI=true` and `NODE_ENV=test` regardless of the invoking shell's values.
Previous results are not reused.

The current CI topology uses GitHub-hosted runners for Linux x64 unit tests and
all pull-request validation. CI uploads the machine-readable validation receipt
from the job that performed the tests.

The build,
frontend compilation, Playwright installation, and artifact packaging remain
separate existing CI steps; the test engine does not claim those steps passed
unless their workflow steps pass.

The Linux CI job installs Chromium into a run-specific Playwright cache and
passes only that cache path to the NUnit task. GitHub-hosted Linux installs its system dependencies with Playwright. Local Linux
runs that need direct-download browser tests should set `PLAYWRIGHT_BROWSERS_PATH`
to a task-owned cache directory and install Chromium with
`pwsh ./_tests/net10.0/linux-x64/playwright.ps1 install chromium`. The suite
uses local fixtures and does not connect to live services or mutate provider
data. Results describe local or GitHub-hosted test execution only; they do not
claim that a live deployment was verified.
