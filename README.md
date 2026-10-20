# BC STEM Teacher Skill v3.0

Portable AgentSkills-style folder for **BC Grades 10–12**, STEM-first (Mathematics, Science and course-specific ADST/Computer Science). Claude, OpenAI, Grok and OpenClaw can use the *instructions* if their host loads AgentSkills or injects `SKILL.md`; **a model API by itself does not automatically discover skills**. Pure-Python standard-library analysis script creates SVG graphics without model lock-in.

## Installation and verification

Source repository: <https://github.com/ywu82/BC-STEM-Teacher>

Any AgentSkills-compatible host can use the repository's `SKILL.md` and bundled resources. The supplied installer has explicit support for Codex, Claude Code, and OpenClaw. Review `SKILL.md` and the scripts before installation. The installer refuses to overwrite a non-Git destination, a checkout with local changes, or a checkout connected to a different remote.

Python 3 is required only for the optional results-analysis script, not for loading the skill instructions.

### One-prompt installation

Copy the same prompt into Codex, Claude Code, OpenClaw, or another AgentSkills-compatible agent:

```text
Install the `bc-stem-teacher` skill from this public GitHub repository:
https://github.com/ywu82/BC-STEM-Teacher

Complete the installation yourself. Follow these requirements:

1. Detect the current agent host and its official user-level skill directory or native Git skill installer. Use user scope unless I explicitly request project/workspace scope.
2. Inspect the repository's README.md, SKILL.md, and installation scripts before changing anything.
3. For Codex, Claude Code, or OpenClaw, clone the repository into a temporary directory and run:

   bash scripts/install_skill.sh --host <codex|claude-code|openclaw> --scope user

   Run that command from the temporary clone and replace the host placeholder with the detected host. Codex may use its built-in `$skill-installer` for the GitHub repository instead, but it must still run the repository's verification script afterward.
4. For another AgentSkills-compatible host, install the complete repository into that host's documented skill directory under the name `bc-stem-teacher`. Preserve SKILL.md and all bundled directories.
5. Do not overwrite a non-Git installation, local changes, or a checkout connected to a different remote. If one is found, stop and report the exact conflict.
6. Verify the installation at all levels the host supports:
   - structural: SKILL.md, frontmatter, and required resources;
   - inventory/readiness: the host reports the skill as installed and usable, when a non-interactive check exists;
   - runtime discovery: a refreshed session can list or explicitly invoke `bc-stem-teacher`.
7. Do not claim full success from file copying alone. If a new session or restart is required, report structural installation as complete and clearly state the remaining runtime check.
8. Finish by reporting the detected host, installation scope, installed path, Git revision, verification results, and any restart/refresh instruction.
```

The prompt delegates host detection, safe installation, and verification to the agent while keeping the requested outcome identical across hosts. The supplied installer supports `codex`, `claude-code`, and `openclaw`; other compatible hosts use their documented skill location.

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
   - Report the highest, lowest, mean, and median percentage for every assessment using complete responses, alongside missingness and score distributions.
   - Provide evidence-linked teaching recommendations for objective gaps, uneven attainment, differentiation, reteaching, and the next aligned check for learning.
   - On hosts with interactive chat widgets, display a radar chart in the conversation with one axis and visible percentage per objective; hover or keyboard focus reveals the exact evidence and local target.
   - On other hosts, provide the same interactive chart as `objective_radar.html` plus `objective_radar.svg` and an objective table, so the report remains portable.

Official BC curriculum verification is a required check within Steps 1–2, not a separate numbered step. Teacher approval and professional judgment apply throughout the workflow and are not an additional final step. Preserve these canonical labels in plans, manifests, status updates, filenames, and teacher approval gates.

## Start using the skill

After installation, start a new session or refresh the agent's skill list. Select `bc-stem-teacher` with the host's skill picker if one is available, or mention the exact skill name in the prompt.

Universal quick start:

```text
Use the `bc-stem-teacher` skill to start a new BC Grades 10–12 STEM teaching project.
```

Copy this prompt to begin a new teaching project:

```text
Use the `bc-stem-teacher` skill to start a new BC Grades 10–12 STEM teaching project.

Guide me through the canonical workflow one major stage at a time. Preserve the Step 1–8 numbering and the 5A/5B and 6A/6B branch labels. Ask for my approval at each required gate before continuing.

Start at Step 1. Ask me for the subject, grade, and exact BC course if I have not already provided them.
```

If the subject and course are already known, include them in the first message, for example:

```text
Use the `bc-stem-teacher` skill. I teach Grade 12 Foundations of Mathematics in BC. Start at Step 1, retain what I have already supplied, and guide me one approved stage at a time.
```

The skill should respond with the current step, the known course context, and the single next input or approval it needs. Continue in the same conversation so the project manifest and approved decisions remain available.
