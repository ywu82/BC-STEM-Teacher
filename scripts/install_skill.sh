#!/usr/bin/env bash
set -euo pipefail

repo_url="https://github.com/ywu82/BC-STEM-Teacher.git"
repo_ref="main"
skill_name="bc-stem-teacher"
host=""
scope="user"
workspace="${PWD}"
verify_only=false

usage() {
  cat <<'EOF'
Install BC STEM Teacher from GitHub.

Usage:
  install_skill.sh --host codex|claude-code|openclaw [options]

Options:
  --scope user|project   Install for the current user or one workspace (default: user)
  --workspace PATH      Project/workspace root for project scope (default: current directory)
  --ref REF             Git branch, tag, or commit (default: main)
  --verify-only         Verify an existing installation without changing it
  -h, --help            Show this help

The installer never overwrites a non-Git installation or a Git checkout with
local changes. Existing clean checkouts update only by fast-forward.
EOF
}

while (($#)); do
  case "$1" in
    --host)
      host="${2:-}"
      shift 2
      ;;
    --scope)
      scope="${2:-}"
      shift 2
      ;;
    --workspace)
      workspace="${2:-}"
      shift 2
      ;;
    --ref)
      repo_ref="${2:-}"
      shift 2
      ;;
    --verify-only)
      verify_only=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$host" in
  codex|claude-code|openclaw) ;;
  *)
    echo "--host must be codex, claude-code, or openclaw" >&2
    exit 2
    ;;
esac

case "$scope" in
  user|project) ;;
  *)
    echo "--scope must be user or project" >&2
    exit 2
    ;;
esac

workspace="$(cd "$workspace" && pwd)"

destination_for_host() {
  case "$host:$scope" in
    codex:user)
      if [[ -n "${CODEX_HOME:-}" ]]; then
        printf '%s\n' "${CODEX_HOME}/skills/${skill_name}"
      else
        printf '%s\n' "${HOME}/.agents/skills/${skill_name}"
      fi
      ;;
    codex:project)
      printf '%s\n' "${workspace}/.agents/skills/${skill_name}"
      ;;
    claude-code:user)
      printf '%s\n' "${CLAUDE_CONFIG_DIR:-${HOME}/.claude}/skills/${skill_name}"
      ;;
    claude-code:project)
      printf '%s\n' "${workspace}/.claude/skills/${skill_name}"
      ;;
  esac
}

install_git_checkout() {
  local destination="$1"
  local parent
  parent="$(dirname "$destination")"
  mkdir -p "$parent"

  if [[ ! -e "$destination" ]]; then
    git clone --depth 1 --branch "$repo_ref" "$repo_url" "$destination"
    return
  fi

  if [[ ! -d "$destination/.git" ]]; then
    echo "Refusing to overwrite non-Git installation: $destination" >&2
    exit 1
  fi

  if [[ -n "$(git -C "$destination" status --porcelain)" ]]; then
    echo "Refusing to update installation with local changes: $destination" >&2
    exit 1
  fi

  local origin
  origin="$(git -C "$destination" remote get-url origin)"
  if [[ "$origin" != "$repo_url" && "$origin" != "${repo_url%.git}" ]]; then
    echo "Refusing to update checkout from a different origin: $origin" >&2
    exit 1
  fi

  git -C "$destination" fetch --depth 1 origin "$repo_ref"
  git -C "$destination" merge --ff-only FETCH_HEAD
}

if [[ "$host" == "openclaw" ]]; then
  if ! command -v openclaw >/dev/null 2>&1; then
    echo "OpenClaw CLI is not available on PATH" >&2
    exit 1
  fi

  if [[ "$verify_only" == false ]]; then
    install_args=(skills install "git:ywu82/BC-STEM-Teacher@${repo_ref}" --as "$skill_name")
    if [[ "$scope" == "user" ]]; then
      install_args+=(--global)
    fi
    (cd "$workspace" && openclaw "${install_args[@]}")
  fi

  exec "$(dirname "$0")/verify_install.sh" --host openclaw --scope "$scope" --workspace "$workspace"
fi

destination="$(destination_for_host)"
if [[ "$verify_only" == false ]]; then
  install_git_checkout "$destination"
fi

exec "$(dirname "$0")/verify_install.sh" --host "$host" --path "$destination"
