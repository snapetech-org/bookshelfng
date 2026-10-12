# Validation engine

BookshelfNG keeps NUnit and `test.sh` as the native unit-test runner. The
validation engine records the source, discovered C# test files, built test
assemblies, runner identity, and native NUnit result counts used for each run.

## Run locally

Build the test package first. `build.sh` clears `_tests` and `_output`, so use a
disposable worktree when those directories contain artifacts you need to keep.

```sh
./build.sh --backend --frontend
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
pwsh ./_tests/net10.0/linux-x64/playwright.ps1 install chromium
node scripts/validation-engine/engine.mjs --plan
node scripts/validation-engine/engine.mjs --tests-only
```

The engine accepts the repository's two declared Node versions: local Volta
`20.11.1` and CI mise `20.19.4` (CI requires `20.19.4`). It requires .NET SDK
`10.0.401`. The plan checks all ten Linux x64 test assemblies before execution.
Its native test task runs `./test.sh Linux Unit Test` with the same
category filters as CI and requires the test runner's NUnit XML summary. It
reports total, passed, failed, skipped, and inconclusive cases; a missing or
zero-case result cannot pass.

The engine writes task progress to stderr as tasks start and finish, with a
once-per-minute heartbeat during long tasks. Counts describe completed tasks;
the current task and its elapsed time are reported separately. GitHub displays
step summaries after the workflow step finishes, so live updates appear in the
step log.

## Evidence and CI

Every run has a private temporary evidence directory with task logs and a
receipt. The candidate identity binds the Git commit and diff, explicit build
and workflow inputs, source test inventory, and SHA-256 digests of the ten
compiled test assemblies. The engine checks that identity before and after each
task, refuses overlapping runs for the same checkout, and gives runtime probes
and children an explicit environment allowlist and each task's declared settings.
Every task gets run-owned home, temporary, XDG, and .NET CLI directories. NuGet
packages use a private cache shared only within the validation run. Test tasks
use `CI=true` and `NODE_ENV=test` regardless of the invoking shell's values.
Previous results are not reused.

The current CI topology has one Linux x64 unit-test runner. CI retains the
normal NUnit report for pull-request feedback and uploads the machine-readable
validation receipt from that same runner. The build, frontend compilation,
Playwright installation, and artifact packaging remain separate existing CI
steps; the test engine does not claim those steps passed unless their workflow
steps pass.

The unit-test task requires the separately installed Chromium cache. Set PLAYWRIGHT_BROWSERS_PATH for both the install command and engine invocation; the engine passes that path only to this task while keeping its home, temporary, and XDG directories private. The suite uses local fixtures and does not connect to live services or mutate
provider data. Results describe local or GitHub-hosted test execution only; they
do not claim that a live deployment was verified.
