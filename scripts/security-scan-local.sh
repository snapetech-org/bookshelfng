#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
export EIO_BACKEND="${SEMGREP_EIO_BACKEND:-posix}"
mode="all"
staged=0
ci_mode=0
while (($#)); do
  case "$1" in
    --staged) staged=1 ;;
    --semgrep-only)
      [[ "$mode" == all || "$mode" == semgrep ]] || { echo "Choose only one scanner." >&2; exit 2; }
      mode=semgrep ;;
    --trivy-only)
      [[ "$mode" == all || "$mode" == trivy ]] || { echo "Choose only one scanner." >&2; exit 2; }
      mode=trivy ;;
    --ci) ci_mode=1 ;;
    -h|--help)
      cat <<'HELP'
Usage: scripts/security-scan-local.sh [--staged] [--semgrep-only|--trivy-only] [--ci]

Semgrep uses the local Community Edition engine with p/default and metrics off.
Trivy selects secret, dependency, and IaC scanners from files in this repository.
Findings are report-only by default. Set SEMGREP_FAIL_ON_FINDINGS=1 or
TRIVY_EXIT_CODE=1 to make findings fail the command. TRIVY_SEVERITY defaults to
HIGH,CRITICAL and TRIVY_IGNORE_UNFIXED defaults to true. --ci disables repository
Trivy config and custom secret rules, applies the reviewed exception file,
and fails when no scan targets are detected. --staged scans only staged Semgrep files.
HELP
      exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
if (( staged )) && [[ "$mode" == trivy ]]; then
  echo "Trivy scans the checkout, not the staged index; omit --staged for Trivy." >&2
  exit 2
fi

semgrep_patterns=(-g '*.py' -g '*.js' -g '*.jsx' -g '*.ts' -g '*.tsx' -g '*.mjs' -g '*.cjs' -g '*.go' -g '*.rs' -g '*.java' -g '*.kt' -g '*.kts' -g '*.cs' -g '*.c' -g '*.h' -g '*.cc' -g '*.cpp' -g '*.hpp' -g '*.php' -g '*.rb' -g '*.swift' -g '*.sh' -g '*.bash' -g '*.zsh' -g '*.ps1' -g '*.sql' -g '*.scala' -g '*.ex' -g '*.exs' -g '*.tf' -g 'Dockerfile*' -g 'docker-compose*.yml' -g 'docker-compose*.yaml' -g 'compose*.yml' -g 'compose*.yaml' -g '.github/workflows/*.yml' -g '.github/workflows/*.yaml' -g 'k8s/**/*.yml' -g 'k8s/**/*.yaml' -g 'helm/**/*.yml' -g 'helm/**/*.yaml' -g 'charts/**/*.yml' -g 'charts/**/*.yaml' -g 'deploy/**/*.yml' -g 'deploy/**/*.yaml' -g 'infra/**/*.yml' -g 'infra/**/*.yaml')

has_semgrep_input() {
  rg --files --hidden "${semgrep_patterns[@]}" -g '!**/security-scan-local.sh' -g '!**/update-security-tools.sh' -g '!**/install-security-hooks.sh' -g '!**/.githooks/**' -g '!**/.husky/**' -g '!**/docs/**' >/dev/null 2>&1
}

semgrep_run() {
  local args=(scan --config "${SEMGREP_CONFIG:-p/default}" --metrics=off --jobs "${SEMGREP_JOBS:-2}")
  local targets=()
  if [[ "${SEMGREP_OFFLINE:-0}" == 1 ]]; then
    args+=(--disable-version-check)
  fi
  if [[ "${SEMGREP_FAIL_ON_FINDINGS:-0}" == 1 ]]; then
    args+=(--error)
  fi
  if (( staged )); then
    while IFS= read -r -d '' file; do
      case "$file" in
        *.py|*.js|*.jsx|*.ts|*.tsx|*.mjs|*.cjs|*.go|*.rs|*.java|*.kt|*.kts|*.cs|*.c|*.h|*.cc|*.cpp|*.hpp|*.php|*.rb|*.swift|*.sh|*.bash|*.zsh|*.ps1|*.sql|*.scala|*.ex|*.exs|*.tf|Dockerfile|Dockerfile.*|docker-compose*.yml|docker-compose*.yaml|compose*.yml|compose*.yaml|*.yml|*.yaml)
          targets+=("$file") ;;
      esac
    done < <(git diff --cached --name-only --diff-filter=ACMR -z)
    if ((${#targets[@]} == 0)); then
      echo "Semgrep: no staged source or configuration files; skipped."
      return 0
    fi
  else
    if ! has_semgrep_input; then
      echo "Semgrep: no supported source or configuration files in this repository; skipped."
      return 0
    fi
    targets=(.)
  fi

  echo "Semgrep Community Edition: config=${SEMGREP_CONFIG:-p/default}, targets=${#targets[@]}"
  if [[ -n "${SEMGREP_BIN:-}" ]]; then
    [[ -x "$SEMGREP_BIN" ]] || { echo "SEMGREP_BIN is not executable: $SEMGREP_BIN" >&2; return 127; }
    "$SEMGREP_BIN" "${args[@]}" "${targets[@]}"
  elif command -v uvx >/dev/null 2>&1; then
    local uv_args=()
    [[ "${SEMGREP_OFFLINE:-0}" == 1 ]] && uv_args+=(--offline)
    uvx "${uv_args[@]}" --from semgrep semgrep "${args[@]}" "${targets[@]}"
  elif command -v semgrep >/dev/null 2>&1; then
    semgrep "${args[@]}" "${targets[@]}"
  elif command -v docker >/dev/null 2>&1; then
    local image="semgrep/semgrep:latest"
    if ! docker image inspect "$image" >/dev/null 2>&1; then
      [[ "${SEMGREP_OFFLINE:-0}" == 0 ]] || { echo "Semgrep image is not cached for offline mode." >&2; return 127; }
      docker pull "$image"
    fi
    docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -e "EIO_BACKEND=${SEMGREP_EIO_BACKEND:-posix}" \
      -v "$repo_root:/src:ro" -w /src "$image" semgrep "${args[@]}" "${targets[@]}"
  else
    echo "Semgrep is unavailable. Install uv, pipx, Semgrep, or Docker." >&2
    return 127
  fi
}

has_dependency_files() {
  local file
  while IFS= read -r -d '' file; do
    case "$file" in
      package.json|*/package.json|package-lock.json|*/package-lock.json|pnpm-lock.yaml|*/pnpm-lock.yaml|yarn.lock|*/yarn.lock|bun.lock*|*/bun.lock*|Cargo.toml|*/Cargo.toml|Cargo.lock|*/Cargo.lock|go.mod|*/go.mod|go.sum|*/go.sum|pyproject.toml|*/pyproject.toml|requirements*.txt|*/requirements*.txt|uv.lock|*/uv.lock|poetry.lock|*/poetry.lock|Pipfile*|*/Pipfile*|*.csproj|*.sln|pom.xml|*/pom.xml|build.gradle|*/build.gradle|build.gradle.kts|*/build.gradle.kts|gradle.lockfile|*/gradle.lockfile|Gemfile*|*/Gemfile*|composer.json|*/composer.json|composer.lock|*/composer.lock|mix.lock|*/mix.lock|pubspec.yaml|*/pubspec.yaml)
        return 0 ;;
    esac
  done < <(git ls-files --cached --others --exclude-standard -z)
  return 1
}
has_iac_files() {
  local file
  while IFS= read -r -d '' file; do
    case "$file" in
      Dockerfile|*/Dockerfile|Dockerfile.*|*/Dockerfile.*|docker-compose*.yml|*/docker-compose*.yml|docker-compose*.yaml|*/docker-compose*.yaml|compose*.yml|*/compose*.yml|compose*.yaml|*/compose*.yaml|*.tf|*.tfvars|Chart.yaml|*/Chart.yaml|kustomization.yaml|*/kustomization.yaml|.github/workflows/*.yml|.github/workflows/*.yaml|k8s/*.yml|k8s/*.yaml|k8s/**/*.yml|k8s/**/*.yaml|helm/*.yml|helm/*.yaml|helm/**/*.yml|helm/**/*.yaml|charts/*.yml|charts/*.yaml|charts/**/*.yml|charts/**/*.yaml|deploy/*.yml|deploy/*.yaml|deploy/**/*.yml|deploy/**/*.yaml|infra/*.yml|infra/*.yaml|infra/**/*.yml|infra/**/*.yaml)
        return 0 ;;
    esac
  done < <(git ls-files --cached --others --exclude-standard -z)
  return 1
}
has_code_files() {
  local file
  while IFS= read -r -d '' file; do
    case "$file" in
      *.py|*.js|*.jsx|*.ts|*.tsx|*.mjs|*.cjs|*.go|*.rs|*.java|*.kt|*.kts|*.cs|*.c|*.h|*.cc|*.cpp|*.hpp|*.php|*.rb|*.swift|*.sh|*.bash|*.zsh|*.ps1|*.sql|*.scala|*.ex|*.exs|*.tf|Dockerfile|Dockerfile.*|docker-compose*.yml|docker-compose*.yaml|compose*.yml|compose*.yaml|.github/workflows/*.yml|.github/workflows/*.yaml|k8s/*.yml|k8s/*.yaml|k8s/**/*.yml|k8s/**/*.yaml|helm/*.yml|helm/*.yaml|helm/**/*.yml|helm/**/*.yaml|charts/*.yml|charts/*.yaml|charts/**/*.yml|charts/**/*.yaml|deploy/*.yml|deploy/*.yaml|deploy/**/*.yml|deploy/**/*.yaml|infra/*.yml|infra/*.yaml|infra/**/*.yml|infra/**/*.yaml)
        case "$file" in
          scripts/security-scan-local.sh|scripts/update-security-tools.sh|scripts/install-security-hooks.sh|*/.githooks/*|*/.husky/*|docs/*|*/docs/*) continue ;;
        esac
        return 0 ;;
    esac
  done < <(git ls-files --cached --others --exclude-standard -z)
  return 1
}

trivy_run() {
  local scanners=()
  local args=()
  local config_data=0
  if has_dependency_files; then scanners+=(vuln); fi
  if has_iac_files; then
    scanners+=(misconfig)
    config_data=1
  fi
  if has_code_files || ((${#scanners[@]} > 0)); then scanners+=(secret); fi
  if ((${#scanners[@]} == 0)); then
    if (( ci_mode )); then
      echo "Trivy CI scan found no supported source, dependency, or deployment files; refusing a false-green skip." >&2
      return 1
    fi
    echo "Trivy: no source, dependency, or deployment files; skipped."
    return 0
  fi
  local scanner_list
  printf -v scanner_list '%s,' "${scanners[@]}"
  scanner_list="${scanner_list%,}"
  args+=(fs --scanners "$scanner_list" --timeout "${TRIVY_TIMEOUT:-20m}" --severity "${TRIVY_SEVERITY:-HIGH,CRITICAL}" --exit-code "${TRIVY_EXIT_CODE:-0}")
  if (( config_data )); then
    local config_data_path="$repo_root/security/trivy-misconfig-data.yaml"
    [[ -f "$config_data_path" ]] || {
      echo "Trivy misconfiguration data file is missing: $config_data_path" >&2
      return 1
    }
    args+=(--config-data "$config_data_path")
  fi
  case "${TRIVY_IGNORE_UNFIXED:-true}" in
    1|true|TRUE|yes|YES) args+=(--ignore-unfixed) ;;
    0|false|FALSE|no|NO) ;;
    *) echo "TRIVY_IGNORE_UNFIXED must be true or false." >&2; return 2 ;;
  esac
  for dir in .git node_modules vendor target dist build bin obj coverage .venv _output _artifacts _temp _tests .next .nuxt .turbo .cache '**/bin' '**/obj'; do args+=(--skip-dirs "$dir"); done
  if (( ci_mode )); then
    args+=(--config= --ignorefile=security/trivy-exceptions.yaml --secret-config=)
  fi
  if [[ "${TRIVY_OFFLINE:-0}" == 1 ]]; then args+=(--skip-db-update --skip-java-db-update --skip-check-update); fi

  echo "Trivy filesystem scan: scanners=$scanner_list"
  if command -v trivy >/dev/null 2>&1; then
    trivy "${args[@]}" .
  elif command -v docker >/dev/null 2>&1; then
    local image="aquasec/trivy:latest"
    local cache_dir="${TRIVY_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/trivy}"
    mkdir -p "$cache_dir"
    if ! docker image inspect "$image" >/dev/null 2>&1; then
      [[ "${TRIVY_OFFLINE:-0}" == 0 ]] || { echo "Trivy image is not cached for offline mode." >&2; return 127; }
      docker pull "$image"
    fi
    docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -e TRIVY_CACHE_DIR=/cache \
      -v "$repo_root:/src:ro" -v "$cache_dir:/cache" -w /src "$image" "${args[@]}" .
  else
    echo "Trivy is unavailable; install Trivy or Docker to run this project scan." >&2
    [[ "${REQUIRE_TRIVY:-0}" == 1 ]] && return 127
  fi
}

if [[ "$mode" == all ]] && (( ! staged )) && [[ -x scripts/run-security-scans.sh ]]; then
  # Preserve this repository's established Semgrep + Trivy policy and exclusions.
  SLSKR_SECURITY_SCANS_REQUIRED="${SLSKR_SECURITY_SCANS_REQUIRED:-0}" bash scripts/run-security-scans.sh
  exit $?
fi
if [[ "$mode" != trivy ]]; then
  if (( staged )); then
    semgrep_run
  elif [[ -x scripts/semgrep-local.sh && -z "${SEMGREP_BIN:-}" && "${SEMGREP_USE_GENERIC:-0}" != 1 ]]; then
    bash scripts/semgrep-local.sh
  elif [[ -x scripts/security-scan.sh && -z "${SEMGREP_BIN:-}" && "${SEMGREP_USE_GENERIC:-0}" != 1 ]]; then
    bash scripts/security-scan.sh
  else
    semgrep_run
  fi
fi
if [[ "$mode" != semgrep ]] && (( ! staged )); then trivy_run; fi
