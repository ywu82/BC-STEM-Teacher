# Install and verify BC STEM Teacher

Source repository: <https://github.com/ywu82/BC-STEM-Teacher>

Review `SKILL.md` and the scripts before installation. The installer refuses to overwrite a non-Git destination, a checkout with local changes, or a checkout connected to a different remote.

## Ask an agent to install it

Give Codex, Claude Code, or OpenClaw this prompt:

> Install the `bc-stem-teacher` skill from `https://github.com/ywu82/BC-STEM-Teacher`. Detect which supported host you are running in, read the repository's `INSTALL.md`, use that host's official skill location or native installer, and do not overwrite local changes. Run the repository's verification script after installation. Report the installed path, Git revision, structural verification result, and runtime-discovery result. If runtime discovery requires a refreshed session, say so instead of claiming it succeeded.

## Unified installer

Clone a temporary copy, then run the installer for the current host:

```bash
install_tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/ywu82/BC-STEM-Teacher.git "$install_tmp/BC-STEM-Teacher"
bash "$install_tmp/BC-STEM-Teacher/scripts/install_skill.sh" --host codex --scope user
```

Replace `codex` with `claude-code` or `openclaw`. Use `--scope project --workspace /absolute/project/path` for a project/workspace-only installation. For Codex and Claude Code, re-running the command updates a clean Git checkout by fast-forward and stops if the checkout has local changes. OpenClaw uses its native Git installer and refuses an existing destination unless the operator intentionally reviews and replaces it.

## Host-specific installation

### Codex

The installer places a user skill at `$CODEX_HOME/skills/bc-stem-teacher` when `CODEX_HOME` is configured; otherwise it uses the current official user location `~/.agents/skills/bc-stem-teacher`. A project skill is installed at `<project>/.agents/skills/bc-stem-teacher`.

Codex can also use its built-in installer:

```text
$skill-installer install the skill from https://github.com/ywu82/BC-STEM-Teacher
```

Verify the files:

```bash
bash scripts/verify_install.sh --host codex --path ~/.agents/skills/bc-stem-teacher
```

Then start or refresh Codex, run `/skills`, and invoke `$bc-stem-teacher`. File verification alone does not prove runtime discovery.

### Claude Code

The installer places a personal skill at `~/.claude/skills/bc-stem-teacher`, or a project skill at `<project>/.claude/skills/bc-stem-teacher`.

Verify the files:

```bash
bash scripts/verify_install.sh --host claude-code --path ~/.claude/skills/bc-stem-teacher
```

Then start or refresh Claude Code and invoke `/bc-stem-teacher`. File verification alone does not prove runtime discovery.

### OpenClaw

OpenClaw has a native Git installer:

```bash
openclaw skills install git:ywu82/BC-STEM-Teacher@main --as bc-stem-teacher --global
openclaw skills info bc-stem-teacher --json
openclaw skills check --json
```

Omit `--global` to install into the active workspace. The unified installer runs the same native workflow and verifies that the selected Gateway inventories the skill and completes its readiness check. Start or refresh an agent session before the final invocation test.

## Verification levels

1. **Structural:** `SKILL.md`, frontmatter, and required resources exist.
2. **Inventory/readiness:** the host reports the skill when it exposes a non-interactive check (currently OpenClaw).
3. **Runtime discovery:** a refreshed agent session lists or explicitly invokes the skill.

Do not report full installation success until the checks available for that host have passed. When a host cannot prove runtime discovery non-interactively, report structural success and the remaining manual invocation check separately.

## Official references

- [OpenAI: Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills)
- [Anthropic: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [OpenClaw: Skills](https://docs.openclaw.ai/tools/skills)
- [OpenClaw: Skills CLI](https://docs.openclaw.ai/cli/skills)
