# Plan audit

This Markdown file is an internal specification. The teacher-facing deliverable is a separate, rendered `plan_audit.html` created from `templates/plan-audit.html`; never deliver this Markdown source as the report.

Write the audit in English by default. Use another language only when the user explicitly names that language.

1. Show one English verdict at the top:
   - `Revision Recommended` in orange/yellow only when a blocking gap would prevent coherent use in Step 5: material objective coverage, feasible pacing, essential learning evidence, required safety/access provisions, or a prerequisite dependency that cannot safely wait.
   - `Ready to Use` in green when the plan is sufficiently complete for Step 5, even if it has concise non-blocking implementation notes.
2. State explicitly whether the plan can proceed to the next step.
3. Include a compact objective-alignment table using the required 0/1/2 coverage judgment; group objectives when that improves readability.
4. When the verdict is `Revision Recommended`, highlight only the required changes and give a clear `Why` for each change.
5. When the verdict is `Ready to Use`, omit the `Required changes` section entirely. Put optional enrichment, wording polish, extra examples, and details that can safely be completed during material authoring under `Non-blocking notes`; these do not change the verdict.
6. Omit nonessential narrative. Retain only the verdict, concise alignment evidence, blocking changes with reasons, optional notes when useful, the decision rule, and provenance/limits.
7. Always preserve the imported plan and propose diffs; do not replace it or advance the project stage without teacher approval.
8. The HTML must be self-contained, responsive, accessible, printable, and include a visible `Print / Save as PDF` button calling `window.print()`.
