# BC High School Teacher Skill V2
Teacher copilot for BC Grades 10–12: Mathematics, Science and ELA.

## Install
Copy the `bc-high-school-teacher-v2` folder into your agent's skills directory. The loader should expose `SKILL.md` as the skill entry point and allow on-demand reading of sibling files. Environment/agent-specific install paths vary.

## V2 additions
Dedicated subject engines, workflow router, curriculum validation protocol, course navigation index, unit and assessment templates, QA checklist and test prompts.

## Critical constraints
This package is a **procedural skill**, not an offline licensed repository of all BC learning standards. Exact provincial course alignment needs access to current official curriculum sources. Rubrics and lesson designs are generated drafts, not Ministry-issued documents.

## Validation
Test each prompt in `examples/three-subject-requests.md`; confirm source links, alignment status, answer-key correctness, safety and privacy before classroom deployment.
