# 1013E R2 Multi-Case Benchmark Review Area

This is a dedicated GitHub review area for **1013E_R2B_MULTI_CASE_LESSON_REASONING_BENCHMARK**.

## Stage Snapshot

- stage_id: `1013E_R2B_MULTI_CASE_LESSON_REASONING_BENCHMARK`
- final_status: `DIAG_MULTI_CASE_REPAIR_REQUIRED`
- next_stage: `1013E_R3_CASE_BANK_AND_PROMPT_REPAIR`
- scope: multi-case benchmark (12 cases) + raw/normalized/quality traces
- boundary: no database write, no memory write, no formal apply, no Feishu write

## Review Files

- `docs/audit/1013E_R2_result.json`
- `docs/audit/1013E_R2_report.md`
- `docs/audit/case_results_1013E_R2.json`
- `docs/audit/benchmark_scores_1013E_R2.json`
- `docs/audit/lesson_reasoning_case_bank_1013E_R2.json`
- `docs/audit/prompt_repair_1013E_R2.md`
- `docs/audit/prompt_repair_standard_daily_1013E_R2.md`
- `docs/audit/provider_metrics_1013E_R2.json`
- `docs/audit/redacted_provider_trace_1013E_R2.json`
- `docs/audit/standard_daily_repair_result_1013E_R2.json`
- `docs/audit/test_standard_daily_repair_result.json`
- `docs/review/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1_README.md`
- `scripts/run_prep_room_1013e_r2_multi_case_benchmark.py`
- `backend/xiaobei_ai/prep_room_lesson_reasoning_contract_1013E.py`

## Validation Notes

Recommended local check:

```powershell
python scripts/run_prep_room_1013e_r2_multi_case_benchmark.py
```

Notes:

- This stage is diagnostic. `final_status` is intentionally not a pass.
- `DIAG_MULTI_CASE_REPAIR_REQUIRED` means raw/normalized structural stability is still insufficient.

## Raw links for GPT

Repository:

https://github.com/ROLLcatCLUB/xiaobei-1013e-r2b-multi-case-benchmark-review

Result:

https://raw.githubusercontent.com/ROLLcatCLUB/xiaobei-1013e-r2b-multi-case-benchmark-review/main/docs/audit/1013E_R2_result.json

Report:

https://raw.githubusercontent.com/ROLLcatCLUB/xiaobei-1013e-r2b-multi-case-benchmark-review/main/docs/audit/1013E_R2_report.md

Case matrix:

https://raw.githubusercontent.com/ROLLcatCLUB/xiaobei-1013e-r2b-multi-case-benchmark-review/main/docs/audit/case_results_1013E_R2.json

Prompt template:

https://raw.githubusercontent.com/ROLLcatCLUB/xiaobei-1013e-r2b-multi-case-benchmark-review/main/docs/audit/prompt_repair_1013E_R2.md

Contract runner:

https://raw.githubusercontent.com/ROLLcatCLUB/xiaobei-1013e-r2b-multi-case-benchmark-review/main/scripts/run_prep_room_1013e_r2_multi_case_benchmark.py

## GPT Review Focus

请重点核验：

1. raw_json_parse / raw_contract / normalized_contract 通过率是否与报告一致；
2. 空内容、低质量、schema drift 与 forbidden_side_effects 的统计是否一致；
3. 报告中的边界字段是否与输出中的 boundary_flags 一致；
4. 是否有违反 `DIAG_MULTI_CASE_REPAIR_REQUIRED` 的解读偏差；
5. 文件是否齐全且不含敏感凭据。

## Important

This repo is a review area only. It is **not** a full deployment or mainline code source.


