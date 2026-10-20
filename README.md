# BC STEM Teacher Skill v3.0

Portable AgentSkills-style folder for **BC Grades 10–12**, STEM-first (Mathematics, Science and course-specific ADST/Computer Science). Claude, OpenAI, Grok and OpenClaw can use the *instructions* if their host loads AgentSkills or injects `SKILL.md`; **a model API by itself does not automatically discover skills**. Pure-Python standard-library analysis script creates SVG graphics without model lock-in.

## Install in OpenClaw
Unzip and copy folder as `<workspace>/skills/bc-stem-teacher/SKILL.md` (with subdirectories). Restart/refresh agent skill discovery if needed. Invoke `/bc-stem-teacher` or request a STEM lesson. Reference: https://docs.openclaw.ai/tools/creating-skills . For other agent runtimes, place folder in their documented skills path or provide `SKILL.md` as agent instructions. The terminal must have Python 3 for analysis script, optional otherwise.

## Typical workflow
`subject → objectives (typed or document) → plan (create or audit) → (materials / diagnostic) → (instructional quiz / test) → results → visual evidence & objective attainment`.

**Diagnostic and post-instruction assessments are distinct**, with different target constructs, timing and interpretation. See `references/assessment-design.md`.

## Demo
`python3 scripts/analyze_results.py --input examples/sample-results.csv --items examples/sample-items.csv --objectives examples/sample-objectives.json --out demo-report`
Inspect `demo-report/summary.md`, `report.json`, and `*.svg`. All example scores are synthetic. Tests: `python3 -m unittest discover -s tests -v`.

## Scope / provenance
`references/official-links.md` has authoritative entrypoints, not a locally scraped exhaustive curriculum database. Do not claim full provincial standards are bundled. V2 preserved in `legacy-v2` for continuity. The demonstration is NOT a validated psychometric instrument, and the skill is NOT a gradebook or connected SIS.
