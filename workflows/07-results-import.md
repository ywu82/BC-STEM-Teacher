# Step 7 — Import anonymized student results

## Trigger

Run when the teacher supplies pseudonymous student-by-item results for a registered diagnostic, quiz, test, or other approved evidence source.

## Required input

- anonymized results CSV or pasted table;
- item blueprint with assessment type, OID, and maximum points;
- objective configuration and teacher-selected local targets.

## Procedure

1. Reject direct identifiers, duplicate student/assessment/item rows, unknown items or OIDs, invalid assessment types, missing required fields, negative scores, over-maximum scores, and zero denominators.
2. Preserve partial and missing responses as explicit states; never silently convert them to zero.
3. Confirm the mapping between each score, assessment, item, OID, and maximum point value.
4. Report import counts, validation failures, exclusions, and limitations without interpreting attainment yet.
5. Obtain teacher confirmation before using the validated dataset in Step 8.

## Persistence

Store only the approved pseudonymous dataset location, checksum or stable identifier, schema status, assessment IDs, row counts, missingness counts, warnings, and teacher approval status in the project manifest. Do not place identifiable student data in reports or the manifest.

## Done

Step 7 is complete when a validated, teacher-approved anonymized dataset and its item/objective mapping are registered. Advance to **Step 8 — Analyze results and generate reports, charts, and objective-attainment evidence**.
