# Security scanning

Run `./scripts/security-scan-local.sh` to scan this checkout locally. Semgrep Community Edition uses the free `p/default` community rules with metrics disabled; the source stays on the machine. The rule pack is fetched from the public Semgrep Registry when it is missing or refreshed, so the first scan needs network access. For a disconnected run, set `SEMGREP_CONFIG` to a local rules directory and `SEMGREP_OFFLINE=1` after caching the Semgrep package.

Semgrep runs on supported source and security configuration. It defaults to two worker jobs for memory-limited environments; set `SEMGREP_JOBS` to change that. Trivy selects `secret` for source/config, `vuln` when dependency manifests or lockfiles are present, and `misconfig` for container, workflow, Kubernetes, Helm, or Terraform files.

The installed pre-commit hook runs Semgrep on staged source/config files; Trivy runs during full local scans and any configured CI workflow.

Local scans use Semgrep Community Edition and do not require a Semgrep SaaS account.

Public Semgrep and Trivy workflows scan on pushes, pull requests, and weekly schedules. They use current scanner releases; any existing CodeQL workflow remains enabled.

Local scans report findings without failing by default. Set `SEMGREP_FAIL_ON_FINDINGS=1` or `TRIVY_EXIT_CODE=1` to make a local scan fail on findings. The required Trivy workflow sets `TRIVY_EXIT_CODE=1`, requires Trivy to be installed, and fails closed if no supported files are detected. It excludes generated `bin`, `obj`, `_output`, `_artifacts`, and `_temp` directories. Its `security/trivy-exceptions.yaml` allowlist is limited to the legacy LinuxServer startup paths, has an expiration date, and records the reason. Trivy downloads its vulnerability and check databases automatically; use `TRIVY_OFFLINE=1` only after those databases are cached. The default timeout is 20 minutes for slow first downloads; set `TRIVY_TIMEOUT` to change it.

The routine Trivy gate reports fixable `HIGH` and `CRITICAL` results. To audit every severity and include CVEs without an available fix, manually dispatch **Trivy filesystem scan** on `main` with `full_vulnerability_audit` enabled. The workflow uses the same isolated private runner and reviewed exception list, and it fails on any reported finding. Use **Full-severity published image audit** with the release tag and immutable GHCR digests to scan the published Softcover and Hardcover images at every severity, including unfixed CVEs.

Kubernetes image trust is explicit: the Helm chart defaults to the organization-owned `ghcr.io/snapetech-org/bookshelfng` image, and `security/trivy-misconfig-data/ksv0125.yaml` trusts only `ghcr.io` for Trivy's KSV-0125 registry check.

Run `./scripts/update-security-tools.sh` to refresh the local Semgrep package cache, pull the current Semgrep fallback image, and refresh Trivy's database.

Semgrep uses the POSIX I/O backend by default for compatibility with restricted Linux runners. Set `SEMGREP_EIO_BACKEND` only if your runner needs a different backend.
