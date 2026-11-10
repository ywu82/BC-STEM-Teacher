# Step 3 — Select the teaching scope

Run this step after course-level objectives are approved and before generating or auditing a teaching plan.

## Scope choices

- `full_course`: plan against the approved course-level objectives.
- `teaching_unit`: record the unit label/topic and parent course objective IDs; break them into measurable unit learning objectives.
- `single_lesson`: record the lesson focus, parent course/unit objective IDs, and available instructional time; define lesson-sized measurable objectives.

## Required state

Persist:

- scope type;
- scope label/topic;
- parent objective IDs;
- time constraint when known;
- scope-level objective IDs and their source relationship;
- teacher approval status.

For unit and lesson scopes, each scope-level objective must include an observable action, conditions or task, proposed success criterion, expected evidence, prerequisites, cognitive demand, accommodations, and mapping to its parent objective and verified curriculum source.

Do not replace or discard approved course objectives when narrowing scope. Do not generate the teaching plan until the teacher has approved the scope-level objectives. If duration is unknown, objectives may be approved first and duration requested at the plan step.

**Completion criterion:** one scope is selected, its state is persisted, and the objectives that will govern planning have teacher approval.

## Procedure

1. Ask the teacher to select exactly one scope: Full Course, Teaching Unit, or Single Lesson.
2. For a unit or lesson, connect the scope to approved parent OIDs and derive scope-sized measurable objectives.
3. Check that the requested content and time constraint are feasible enough to plan.
4. Ask the teacher to approve the scope and derived objectives.

## Persistence

Store the required state above in the project manifest.

## Done

Step 3 is complete when one scope and its measurable objectives are teacher-approved. Advance to **Step 4 — Create or audit the instructional plan**.
