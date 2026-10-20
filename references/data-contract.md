# Artifact & data contract (model-independent)
Use stable IDs: project P1, O1..On objective, S1..Sn slide, D1..Dn diagnostic item, Q1..Qn instructional quiz item, T1..Tn test item.

`objective`: `{id,statement,source_type,source_url,source_checked_date,success_criterion,prerequisites,cognitive_level}`.
`material`: `{id,type,objective_ids,content,source_material_ids}`; each slide includes title, speaker notes, student activity, worked example where applicable.
`item`: `{item_id,assessment_type,objective_id,max_points,cognitive_level,material_ids,prerequisite_ids,answer_key,rubric}`. For machine analysis `sample-items.csv` contains `item_id,assessment_type,objective_id,max_points,cognitive_level,material_ids,comparable_group` (answer keys in private teacher file, never in student distribution).
`result row`: `{student_id,assessment_type,item_id,points}`; optional `assessment_instance` planned for future; do not mix multiple attempts under same student/type/item. `points` numeric 0..max_points; blank is invalid/missing and must be repaired not silently zero-filled.
`objectives.json`: `{course, threshold, objectives:[{id,label,target,comparable}...]}`; objective-specific `target` in 0..1 overrides default report threshold. Thresholds only for **local evidence flags**, not BC letter-grade cutoffs.
`report.json.assessments.<type>`: `{n_complete,n_partial,n_missing,possible_points_per_complete_student,highest_percent,lowest_percent,mean_percent,median_percent,distribution}`. Highest, lowest, mean, median and distribution use complete responses only; partial and missing counts remain separate.
`report.json.teaching_recommendations`: `{assessment_type,items:[...]}`. Each recommendation must cite measured evidence and remain advisory: objective ID/label, observed percentage, local target, target-attainment count or score spread, followed by a concrete next instructional action and evidence check.

Use only anonymized student pseudonyms (e.g. P01) and no identifying metadata. `assessment_type` values: `diagnostic`, `quiz`, `test`. Item IDs should not be shared across different types. Data analysis warns about missing students, objectives and mismatched item mappings.
