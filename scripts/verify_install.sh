#!/usr/bin/env bash
set -euo pipefail

skill_name="bc-stem-teacher"
host=""
scope="user"
workspace="${PWD}"
skill_path=""

usage() {
  cat <<'EOF'
Verify a BC STEM Teacher installation.

Usage:
  verify_install.sh --host codex|claude-code --path PATH
  verify_install.sh --host openclaw [--scope user|project] [--workspace PATH]

The check proves file structure and metadata. OpenClaw additionally proves that
the selected Gateway inventories the skill. Codex and Claude Code require a new
or refreshed session for their final runtime-discovery check.
EOF
}

while (($#)); do
  case "$1" in
    --host)
      host="${2:-}"
      shift 2
      ;;
    --path)
      skill_path="${2:-}"
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

if [[ "$host" == "openclaw" ]]; then
  command -v openclaw >/dev/null 2>&1 || {
    echo "OpenClaw CLI is not available on PATH" >&2
    exit 1
  }
  workspace="$(cd "$workspace" && pwd)"
  info_args=(skills info "$skill_name" --json)
  check_args=(skills check --json)
  if [[ "$scope" == "project" ]]; then
    info_json="$(cd "$workspace" && openclaw "${info_args[@]}")"
    (cd "$workspace" && openclaw "${check_args[@]}" >/dev/null)
  else
    info_json="$(openclaw "${info_args[@]}")"
    openclaw "${check_args[@]}" >/dev/null
  fi
  printf '%s' "$info_json" | node -e '
    const fs = require("fs");
    const info = JSON.parse(fs.readFileSync(0, "utf8"));
    const expected = "bc-stem-teacher";
    const missing = Object.values(info.missing || {}).some(
      value => Array.isArray(value) && value.length > 0
    );
    if (
      info.name !== expected ||
      info.disabled !== false ||
      info.eligible !== true ||
      info.modelVisible !== true ||
      info.commandVisible !== true ||
      missing
    ) {
      console.error("OpenClaw found the skill, but it is not fully ready and visible:");
      console.error(JSON.stringify(info, null, 2));
      process.exit(1);
    }
  '
  echo "VERIFIED: OpenClaw inventories '$skill_name'; it is eligible, model-visible, and command-visible."
  echo "Runtime check: start or refresh a session, then ask to use '$skill_name'."
  exit 0
fi

if [[ -z "$skill_path" ]]; then
  echo "--path is required for $host" >&2
  exit 2
fi

skill_path="$(cd "$skill_path" && pwd)"
skill_file="$skill_path/SKILL.md"
[[ -f "$skill_file" ]] || {
  echo "Missing required file: $skill_file" >&2
  exit 1
}

frontmatter="$(awk '
  NR == 1 && $0 == "---" { inside = 1; next }
  inside && $0 == "---" { exit }
  inside { print }
' "$skill_file")"
name_line="$(printf '%s\n' "$frontmatter" | sed -n 's/^name:[[:space:]]*//p' | head -n 1)"
description_line="$(printf '%s\n' "$frontmatter" | sed -n 's/^description:[[:space:]]*//p' | head -n 1)"
[[ "$name_line" == "$skill_name" ]] || {
  echo "Unexpected skill name in $skill_file: $name_line" >&2
  exit 1
}
[[ -n "$description_line" ]] || {
  echo "Missing skill description in $skill_file" >&2
  exit 1
}

for required in workflows references templates scripts/analyze_results.py; do
  [[ -e "$skill_path/$required" ]] || {
    echo "Missing required skill resource: $skill_path/$required" >&2
    exit 1
  }
done

revision="not-a-git-checkout"
if [[ -d "$skill_path/.git" ]]; then
  revision="$(git -C "$skill_path" rev-parse --short HEAD)"
fi

echo "VERIFIED: skill structure and metadata are valid at $skill_path (revision $revision)."
if [[ "$host" == "codex" ]]; then
  echo "Runtime check: start or refresh Codex, run /skills, then invoke \$bc-stem-teacher."
else
  echo "Runtime check: start or refresh Claude Code, then invoke /bc-stem-teacher."
fi
