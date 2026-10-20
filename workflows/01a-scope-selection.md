# 01a Teaching Scope Selection

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
