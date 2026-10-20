# BC STEM Teacher Skill v3.0

Portable AgentSkills-style folder for **BC Grades 10–12**, STEM-first (Mathematics, Science and course-specific ADST/Computer Science). Claude, OpenAI, Grok and OpenClaw can use the *instructions* if their host loads AgentSkills or injects `SKILL.md`; **a model API by itself does not automatically discover skills**. Pure-Python standard-library analysis script creates SVG graphics without model lock-in.

## Installation and verification

Source repository: <https://github.com/ywu82/BC-STEM-Teacher>

Any AgentSkills-compatible host can use the repository's `SKILL.md` and bundled resources. The supplied installer has explicit support for Codex, Claude Code, and OpenClaw. Review `SKILL.md` and the scripts before installation. The installer refuses to overwrite a non-Git destination, a checkout with local changes, or a checkout connected to a different remote.

Python 3 is required only for the optional results-analysis script, not for loading the skill instructions.

### Ask an agent to install it

Give a supported agent this prompt:

> Install the `bc-stem-teacher` skill from `https://github.com/ywu82/BC-STEM-Teacher`. Detect which AgentSkills-compatible host you are running in, read the repository README's **Installation and verification** section, use that host's official skill location or native installer, and do not overwrite local changes. Run the repository's verification script after installation. Report the installed path, Git revision, structural verification result, and runtime-discovery result. If runtime discovery requires a refreshed session, say so instead of claiming it succeeded.

### Unified installer

Clone a temporary copy, then run the installer for the current host:

```bash
install_tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/ywu82/BC-STEM-Teacher.git "$install_tmp/BC-STEM-Teacher"
bash "$install_tmp/BC-STEM-Teacher/scripts/install_skill.sh" --host codex --scope user
```

Replace `codex` with `claude-code` or `openclaw`. Use `--scope project --workspace /absolute/project/path` for a project/workspace-only installation. For Codex and Claude Code, re-running the command updates a clean Git checkout by fast-forward and stops if the checkout has local changes. OpenClaw uses its native Git installer and refuses an existing destination unless the operator intentionally reviews and replaces it.

### Host-specific installation

#### Codex

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

#### Claude Code

The installer places a personal skill at `~/.claude/skills/bc-stem-teacher`, or a project skill at `<project>/.claude/skills/bc-stem-teacher`.

Verify the files:

```bash
bash scripts/verify_install.sh --host claude-code --path ~/.claude/skills/bc-stem-teacher
```

Then start or refresh Claude Code and invoke `/bc-stem-teacher`. File verification alone does not prove runtime discovery.

#### OpenClaw

OpenClaw has a native Git installer:

```bash
openclaw skills install git:ywu82/BC-STEM-Teacher@main --as bc-stem-teacher --global
openclaw skills info bc-stem-teacher --json
openclaw skills check --json
```

Omit `--global` to install into the active workspace. The unified installer runs the same native workflow and verifies that the selected Gateway inventories the skill and completes its readiness check. Start or refresh an agent session before the final invocation test.

Other AgentSkills-compatible hosts can clone the repository into their documented skills directory and use `scripts/verify_install.sh` as a structural reference, adapting the final runtime-discovery check to the host.

### Verification levels

1. **Structural:** `SKILL.md`, frontmatter, and required resources exist.
2. **Inventory/readiness:** the host reports the skill when it exposes a non-interactive check.
3. **Runtime discovery:** a refreshed agent session lists or explicitly invokes the skill.

Do not report full installation success until the checks available for that host have passed. When a host cannot prove runtime discovery non-interactively, report structural success and the remaining manual invocation check separately.

### Official references

- [Agent Skills open standard](https://agentskills.io/)
- [OpenAI: Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills)
- [Anthropic: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [OpenClaw: Skills](https://docs.openclaw.ai/tools/skills)
- [OpenClaw: Skills CLI](https://docs.openclaw.ai/cli/skills)

## Typical workflow
`subject → objectives (typed or document) → plan (create or audit) → (materials / diagnostic) → (instructional quiz / test) → results → visual evidence & objective attainment`.

**Diagnostic and post-instruction assessments are distinct**, with different target constructs, timing and interpretation. See `references/assessment-design.md`.

## Canonical eight-step workflow

Use the following step and branch labels consistently:

1. **Step 1 — Select and confirm the exact course**
2. **Step 2 — Develop course-level learning objectives**
3. **Step 3 — Select the teaching scope**
   - Full Course
   - Teaching Unit
   - Single Lesson
4. **Step 4 — Create or audit the instructional plan**
5. **Step 5 — Pre-instruction preparation**
   - **Step 5A — Prerequisite diagnostic**
   - **Step 5B — Teaching materials**
   - Steps 5A and 5B are independent branches and may be completed in either order.
6. **Step 6 — Post-instruction assessment**
   - **Step 6A — Post-instruction quiz**
   - **Step 6B — Final unit test**
7. **Step 7 — Import anonymized student results**
8. **Step 8 — Analyze results and generate reports, charts, and objective-attainment evidence**

Official BC curriculum verification is a required check within Steps 1–2, not a separate numbered step. Teacher approval and professional judgment apply throughout the workflow and are not an additional final step. Preserve these canonical labels in plans, manifests, status updates, filenames, and teacher approval gates.

## Demo
`python3 scripts/analyze_results.py --input examples/sample-results.csv --items examples/sample-items.csv --objectives examples/sample-objectives.json --out demo-report`
Inspect `demo-report/summary.md`, `report.json`, and `*.svg`. All example scores are synthetic. Tests: `python3 -m unittest discover -s tests -v`.

## Scope / provenance
`references/official-links.md` has authoritative entrypoints, not a locally scraped exhaustive curriculum database. Do not claim full provincial standards are bundled. V2 preserved in `legacy-v2` for continuity. The demonstration is NOT a validated psychometric instrument, and the skill is NOT a gradebook or connected SIS.
