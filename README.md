# BC STEM Teacher Skill v3.0

Portable AgentSkills-style folder for **BC Grades 10–12**, STEM-first (Mathematics, Science and course-specific ADST/Computer Science). Claude, OpenAI, Grok and OpenClaw can use the *instructions* if their host loads AgentSkills or injects `SKILL.md`; **a model API by itself does not automatically discover skills**. Pure-Python standard-library analysis script creates SVG graphics without model lock-in.

## Install in OpenClaw
Unzip and copy folder as `<workspace>/skills/bc-stem-teacher/SKILL.md` (with subdirectories). Restart/refresh agent skill discovery if needed. Invoke `/bc-stem-teacher` or request a STEM lesson. Reference: https://docs.openclaw.ai/tools/creating-skills . For other agent runtimes, place folder in their documented skills path or provide `SKILL.md` as agent instructions. The terminal must have Python 3 for analysis script, optional otherwise.

## Install from GitHub

Codex, Claude Code, and OpenClaw can install this skill directly from the public repository and verify the result. See [INSTALL.md](INSTALL.md) for:

- a ready-to-paste agent installation prompt;
- the cross-host `scripts/install_skill.sh` installer;
- host-specific paths and native commands;
- structural, inventory/readiness, and runtime-discovery checks.

OpenClaw quick install:

```bash
openclaw skills install git:ywu82/BC-STEM-Teacher@main --as bc-stem-teacher --global
openclaw skills info bc-stem-teacher --json
openclaw skills check --json
```

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
