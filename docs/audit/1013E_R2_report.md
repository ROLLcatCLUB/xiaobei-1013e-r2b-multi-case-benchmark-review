# 1013E_R2 Multi-Case Lesson Reasoning Benchmark

```text
final_status=DIAG_MULTI_CASE_REPAIR_REQUIRED
next_stage=1013E_R3_CASE_BANK_AND_PROMPT_REPAIR
r2_repair_baseline=STANDARD_DAILY_REPAIR_FAILED
r2_repair_baseline_meaning=R2 repair remains failed; this round is diagnostic only, not a repair pass
raw_json_parse_pass_count=6/12
raw_contract_success_count=5/12
normalized_contract_success_count=6/12
overall_pass_count=5/12
empty_content_count=6/12
markdown_fence_count=0
schema_drift_count=6
forbidden_side_effects_count=6
average_quality_score=2.48
low_quality_case_count=6/12
average_teaching_reasoning_score=2.83
average_impact_scope_score=2.92
average_age_appropriateness_score=4.17
secret_scan_ok=true
```

## Reading The Result

- raw_model_output_contract_result=FAIL
- normalized_contract_result=FAIL
- teaching_quality_result=NEED_REPAIR
- `raw_json_parse_success` means raw model output passed strict JSON parsing.
- `raw_contract_success` means raw model output already matched compact contract.
- `normalized_contract_success` means local normalizer mapped output into compact contract.
- `quality_score` is a normalized 0-5 quality score from 5 compact dimensions.
- recommended_next_stage=1013E_R3_CASE_BANK_AND_PROMPT_REPAIR

raw_model_output_contract_result=FAIL
normalized_contract_result=FAIL
teaching_quality_result=NEED_REPAIR
recommended_next_stage=1013E_R3_CASE_BANK_AND_PROMPT_REPAIR

| case_id | raw_json_parse | raw_contract | normalized_contract | quality_score | conclusion |
| --- | --- | --- | --- | --- | --- |
| `quick_daily_basic_ready` | true | true | true | 4.8 | pass |
| `quick_daily_no_print` | true | true | true | 5.0 | pass |
| `standard_daily_cold_warm_more_visual` | false | false | false | 0.0 | raw_json_parse_failed |
| `standard_daily_task_too_easy` | false | false | false | 0.0 | raw_json_parse_failed |
| `standard_daily_link_prior_work` | true | true | true | 5.0 | pass |
| `refined_lesson_question_chain` | false | false | false | 0.0 | raw_json_parse_failed |
| `refined_lesson_differentiated_assignment` | false | false | false | 0.0 | raw_json_parse_failed |
| `open_class_student_expression` | true | true | true | 5.0 | pass |
| `open_class_material_timing` | false | false | false | 0.0 | raw_json_parse_failed |
| `research_lesson_evidence_chain` | false | false | false | 0.0 | raw_json_parse_failed |
| `constrained_no_projector` | true | false | true | 5.0 | pass |
| `constrained_30_minutes` | true | true | true | 5.0 | normalized_pass |

## Case Results (legacy)

用于回溯：以下保持与历史兼容。
- `quick_daily_basic_ready` `quick_daily`: strict=true, raw_contract=true, normalized_contract=true, overall=true, teaching=4, impact=5, age=5, quality=4.8
- `quick_daily_no_print` `quick_daily`: strict=true, raw_contract=true, normalized_contract=true, overall=true, teaching=5, impact=5, age=5, quality=5.0
- `standard_daily_cold_warm_more_visual` `standard_daily`: strict=false, raw_contract=false, normalized_contract=false, overall=false, teaching=1, impact=1, age=4, quality=0.0
- `standard_daily_task_too_easy` `standard_daily`: strict=false, raw_contract=false, normalized_contract=false, overall=false, teaching=1, impact=1, age=4, quality=0.0
- `standard_daily_link_prior_work` `standard_daily`: strict=true, raw_contract=true, normalized_contract=true, overall=true, teaching=5, impact=5, age=5, quality=5.0
- `refined_lesson_question_chain` `refined_lesson`: strict=false, raw_contract=false, normalized_contract=false, overall=false, teaching=1, impact=1, age=4, quality=0.0
- `refined_lesson_differentiated_assignment` `refined_lesson`: strict=false, raw_contract=false, normalized_contract=false, overall=false, teaching=0, impact=0, age=0, quality=0.0
- `open_class_student_expression` `open_class`: strict=true, raw_contract=true, normalized_contract=true, overall=true, teaching=5, impact=5, age=5, quality=5.0
- `open_class_material_timing` `open_class`: strict=false, raw_contract=false, normalized_contract=false, overall=false, teaching=1, impact=1, age=4, quality=0.0
- `research_lesson_evidence_chain` `research_lesson`: strict=false, raw_contract=false, normalized_contract=false, overall=false, teaching=1, impact=1, age=4, quality=0.0
- `constrained_no_projector` `time_or_resource_constrained`: strict=true, raw_contract=false, normalized_contract=true, overall=true, teaching=5, impact=5, age=5, quality=5.0
- `constrained_30_minutes` `time_or_resource_constrained`: strict=true, raw_contract=true, normalized_contract=true, overall=false, teaching=5, impact=5, age=5, quality=5.0

## Boundary

- Provider was called for benchmark cases when credentials were available.
- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No formal export.
- No official archive.
- No real knowledge-base retrieval.
- Requests and responses are redacted in the trace file.
