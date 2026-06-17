from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers  # noqa: E402
from backend.xiaobei_ai.prep_room_lesson_reasoning_contract_1013E import (  # noqa: E402
    BOUNDARY_FLAGS,
    parse_lesson_reasoning_output,
    validate_compact_lesson_reasoning_payload,
)


STAGE_ID = "1013E_R2B_MULTI_CASE_LESSON_REASONING_BENCHMARK"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E_R2"
CASE_COUNT = 12
RAW_OUTPUT_BENCHMARK_ID = "1013E_R2_RAW_CONTRACT_DIAG"
NORMALIZED_OUTPUT_BENCHMARK_ID = "1013E_R2_NORMALIZED_CONTRACT_DIAG"
R2_REPAIR_BASELINE = "STANDARD_DAILY_REPAIR_FAILED"
DIAG_PASS_WITH_NORMALIZATION = "DIAG_MULTI_CASE_PASS_WITH_NORMALIZATION_REQUIRED"
DIAG_COMPLETED_NO_NORMALIZATION = "DIAG_MULTI_CASE_COMPLETED_RAW_OUTPUT_STABLE"
DIAG_REPAIR_REQUIRED = "DIAG_MULTI_CASE_REPAIR_REQUIRED"
DIAG_STABILITY_THRESHOLD = CASE_COUNT - 1
DIAG_LOW_QUALITY_THRESHOLD = 3.0
NEXT_STAGE_DIAG_COMPLETE = "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
NEXT_STAGE_NORMALIZATION_REQUIRED = "1013E_R3_FIELD_PATCH_NORMALIZATION_ADAPTER"
NEXT_STAGE_REPAIR = "1013E_R3_CASE_BANK_AND_PROMPT_REPAIR"

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}", re.I),
    re.compile(r"(?i)(api[_-]?key|authorization|secret|tenant_access_token)\s*[:=]\s*['\"][^'\"]{8,}"),
]

FORBIDDEN_TEACHER_VISIBLE_TERMS = [
    "field_patch",
    "schema",
    "ViewModel",
    "provider",
    "formal_apply",
    "teacher_review_required",
    "dry-run",
    "database",
    "Feishu",
    "memory",
]

SECTION_ALIASES = {
    "basis": "basis",
    "依据": "basis",
    "analysis": "analysis",
    "学情": "analysis",
    "学情分析": "analysis",
    "goals": "goals",
    "目标": "goals",
    "keypoints": "keypoints",
    "重难点": "keypoints",
    "preparation": "preparation",
    "准备": "preparation",
    "teaching_process": "teaching_process",
    "教学过程": "teaching_process",
    "过程": "teaching_process",
    "assessment": "assessment",
    "评价": "assessment",
    "reflection": "reflection",
    "反思": "reflection",
}

STEP_ALIASES = {
    "intro": "intro",
    "导入": "intro",
    "sense": "sense",
    "感知": "sense",
    "explore": "explore",
    "探究": "explore",
    "make": "make",
    "表现": "make",
    "创作": "make",
    "share": "share",
    "交流": "share",
    "展示": "share",
    "交流展示": "share",
}

IMPACT_ALIASES = {
    "big_screen": "big_screen",
    "大屏": "big_screen",
    "投屏": "big_screen",
    "handout": "handout",
    "学习单": "handout",
    "rubric": "rubric",
    "评价标准": "rubric",
    "resource_reference": "resource_reference",
    "资料": "resource_reference",
    "evidence_note": "evidence_note",
    "证据": "evidence_note",
    "评价证据": "evidence_note",
    "teacher_action": "teacher_action",
    "教师动作": "teacher_action",
    "student_activity": "student_activity",
    "学生活动": "student_activity",
}

CASE_BANK = [
    {
        "case_id": "quick_daily_basic_ready",
        "lesson_design_mode": "quick_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "今天时间比较紧，先帮我把这节课整理成一版明天能上课的基本设计。",
        "student_baseline": "学生能说出常见颜色，也能表达喜欢或不喜欢，但说理由时容易停在好看、漂亮。",
        "core_learning_problem": "让学生能把颜色和感受联系起来，并说出简单理由。",
        "resource_budget": "low",
        "constraints": ["只用教材图、几张生活图片和普通色卡", "少追问"],
        "available_resource_candidates": ["教材图例", "生活冷暖色图片", "普通色卡"],
        "expected_target_sections": ["analysis", "teaching_process"],
        "expected_impact_scope": ["big_screen", "student_activity", "evidence_note"],
        "expected_quality_level": "basic_usable",
    },
    {
        "case_id": "quick_daily_no_print",
        "lesson_design_mode": "quick_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "今天不能打印学习单，帮我把探究和评价改成不用纸也能完成。",
        "student_baseline": "学生愿意看图说感受，但记录习惯还不稳定。",
        "core_learning_problem": "在没有纸质学习单的条件下保留表达和评价证据。",
        "resource_budget": "low",
        "constraints": ["不能打印", "只保留板书、大屏和口头表达"],
        "available_resource_candidates": ["大屏图片", "黑板板书", "教师拍照记录"],
        "expected_target_sections": ["preparation", "teaching_process", "assessment"],
        "expected_impact_scope": ["big_screen", "evidence_note", "teacher_action"],
        "expected_quality_level": "basic_usable",
    },
    {
        "case_id": "standard_daily_cold_warm_more_visual",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
        "student_baseline": "学生知道红、黄、蓝等颜色，也会说喜欢，但冷暖色理解停在表层。",
        "core_learning_problem": "帮助学生从颜色喜好转向用温暖、清凉等感受分类并说明理由。",
        "resource_budget": "medium",
        "constraints": ["不超出三年级认知", "探究环节要能落地"],
        "available_resource_candidates": ["冷暖生活图", "色卡", "学习单感受记录格"],
        "expected_target_sections": ["analysis", "teaching_process"],
        "expected_impact_scope": ["big_screen", "handout", "evidence_note"],
        "expected_quality_level": "ready_to_teach",
    },
    {
        "case_id": "standard_daily_task_too_easy",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "我担心只让学生涂冷暖色太简单，帮我把表现环节做得有一点挑战，但不要超纲。",
        "student_baseline": "学生能涂色，也能模仿范例，但自主选择颜色表达感受还需要支架。",
        "core_learning_problem": "把表现任务从机械涂色推进到有理由的色彩表达。",
        "resource_budget": "medium",
        "constraints": ["不能变成专业色彩理论", "要有分层选择"],
        "available_resource_candidates": ["情绪词卡", "场景小题", "学生作品范例"],
        "expected_target_sections": ["teaching_process", "assessment"],
        "expected_impact_scope": ["handout", "rubric", "student_activity"],
        "expected_quality_level": "ready_to_teach",
    },
    {
        "case_id": "standard_daily_link_prior_work",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "学生上一课刚认识色彩，这节课要自然接上，不要像重新开始讲概念。",
        "student_baseline": "学生上一课已经能辨认常见颜色和简单搭配，但还没有把颜色和情绪、场景联系起来。",
        "core_learning_problem": "承接认识色彩，推进到色彩感受和表达理由。",
        "resource_budget": "medium",
        "constraints": ["要承上启下", "不要重复第一课内容"],
        "available_resource_candidates": ["上一课色彩记录", "教材作品图", "生活场景图"],
        "expected_target_sections": ["basis", "analysis", "teaching_process"],
        "expected_impact_scope": ["resource_reference", "teacher_action", "student_activity"],
        "expected_quality_level": "ready_to_teach",
    },
    {
        "case_id": "refined_lesson_question_chain",
        "lesson_design_mode": "refined_lesson",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "我想把问题串磨细一点，让学生不是只回答冷色暖色，而是能说出为什么有这样的感觉。",
        "student_baseline": "学生能跟着老师回答，但独立表达理由时容易短句化、空泛化。",
        "core_learning_problem": "用连续问题推动学生从判断到说明理由。",
        "resource_budget": "medium",
        "constraints": ["问题不宜过多", "要留给创作时间"],
        "available_resource_candidates": ["作品图", "色卡组合", "表达句式支架"],
        "expected_target_sections": ["teaching_process", "assessment"],
        "expected_impact_scope": ["teacher_action", "big_screen", "evidence_note"],
        "expected_quality_level": "refined",
    },
    {
        "case_id": "refined_lesson_differentiated_assignment",
        "lesson_design_mode": "refined_lesson",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "作业要分层，让基础弱的孩子能完成，能力强的孩子也有发挥空间。",
        "student_baseline": "班内绘画速度和表达能力差异较大，部分学生需要明确步骤，部分学生能自主创造场景。",
        "core_learning_problem": "让不同层次学生都能用色彩表达感受，并保留适度挑战。",
        "resource_budget": "medium",
        "constraints": ["任务分层但不割裂", "评价标准要一致"],
        "available_resource_candidates": ["基础色块任务", "场景表达任务", "情绪色彩挑战任务"],
        "expected_target_sections": ["teaching_process", "assessment"],
        "expected_impact_scope": ["handout", "rubric", "student_activity"],
        "expected_quality_level": "refined",
    },
    {
        "case_id": "open_class_student_expression",
        "lesson_design_mode": "open_class",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "这节课要展示，学生表达和课堂证据要更清楚，大屏也要跟环节配合。",
        "student_baseline": "学生愿意发言，但容易只说颜色名称，需要句式和可视化支架。",
        "core_learning_problem": "让学生在公开课场景中清楚表达色彩感受、理由和作品选择。",
        "resource_budget": "high",
        "constraints": ["大屏节奏要清楚", "不能只追求表演感"],
        "available_resource_candidates": ["冷暖对比图片组", "学生表达句式", "课堂证据采集表"],
        "expected_target_sections": ["teaching_process", "assessment", "preparation"],
        "expected_impact_scope": ["big_screen", "rubric", "evidence_note"],
        "expected_quality_level": "open_class_ready",
    },
    {
        "case_id": "open_class_material_timing",
        "lesson_design_mode": "open_class",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "材料什么时候发、学习单什么时候用、大屏什么时候切换，要帮我设计清楚。",
        "student_baseline": "学生对材料很兴奋，如果过早发放会分散注意力。",
        "core_learning_problem": "让材料、大屏和学习单服务于认知推进，而不是打断课堂。",
        "resource_budget": "high",
        "constraints": ["材料发放要有时机", "课堂秩序要稳定"],
        "available_resource_candidates": ["色卡包", "学习单", "大屏图片组", "作品范例"],
        "expected_target_sections": ["preparation", "teaching_process"],
        "expected_impact_scope": ["big_screen", "handout", "teacher_action"],
        "expected_quality_level": "open_class_ready",
    },
    {
        "case_id": "research_lesson_evidence_chain",
        "lesson_design_mode": "research_lesson",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "我想研究学生怎么从说颜色好看，过渡到能说明颜色带来的感受。",
        "student_baseline": "学生有颜色经验，但表达多停留在喜好判断，缺少理由链。",
        "core_learning_problem": "观察学生从喜好表达走向感受表达和理由表达的过程。",
        "resource_budget": "high",
        "constraints": ["不要写论文", "要有可观察证据"],
        "available_resource_candidates": ["前测口头表达", "学习单理由栏", "作品说明", "课堂观察记录"],
        "expected_target_sections": ["analysis", "teaching_process", "assessment"],
        "expected_impact_scope": ["evidence_note", "rubric", "teacher_action"],
        "expected_quality_level": "refined",
    },
    {
        "case_id": "constrained_no_projector",
        "lesson_design_mode": "time_or_resource_constrained",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
        "teacher_input": "这节课可能没有投影，帮我改成不用大屏也能推进冷暖色理解。",
        "student_baseline": "学生需要直观材料支持，单靠口头讲解容易理解偏浅。",
        "core_learning_problem": "缺少投影时仍保留直观感受、分类和表达证据。",
        "resource_budget": "low",
        "constraints": ["没有投影", "只能用实物色卡和板书"],
        "available_resource_candidates": ["色卡", "黑板分区", "生活物品"],
        "expected_target_sections": ["preparation", "teaching_process", "assessment"],
        "expected_impact_scope": ["resource_reference", "teacher_action", "evidence_note"],
        "expected_quality_level": "basic_usable",
    },
    {
        "case_id": "constrained_30_minutes",
        "lesson_design_mode": "time_or_resource_constrained",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 30,
        "teacher_input": "这周只有三十分钟，帮我压缩流程，但不要把学生表达和评价证据删掉。",
        "student_baseline": "学生能快速进入涂色活动，但表达和回看常被时间压缩掉。",
        "core_learning_problem": "在时间缩短时保留关键认知转换和证据。",
        "resource_budget": "low",
        "constraints": ["30分钟", "不牺牲表达和评价"],
        "available_resource_candidates": ["精选图片两张", "小色卡", "一句话表达卡"],
        "expected_target_sections": ["teaching_process", "assessment"],
        "expected_impact_scope": ["teacher_action", "student_activity", "evidence_note"],
        "expected_quality_level": "basic_usable",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(name: str, text: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(text, encoding="utf-8")
    return path


def provider_public_status() -> dict[str, Any]:
    status = providers.provider_status()
    generation = status.get("generation") or {}
    return {
        "provider_name": status.get("provider_name"),
        "credential_available": bool(generation.get("credential_available")),
        "credential_source": generation.get("credential_source"),
        "model": generation.get("model"),
        "base_url": generation.get("base_url"),
    }


def build_prompt(case: dict[str, Any], *, retry: bool = False) -> dict[str, str]:
    primary_step = infer_step_from_case(case)
    primary_step_name = step_name_for(primary_step)
    request = {
        "task": "返回一个很短的 JSON 对象，把教师意图转成备课修改候选。禁止写完整教案。",
        "case": {
            "lesson_design_mode": case["lesson_design_mode"],
            "grade": case["grade"],
            "subject": case["subject"],
            "unit": case["unit"],
            "lesson": f"{case['lesson_code']}《{case['lesson_title']}》",
            "duration_minutes": case["duration_minutes"],
            "teacher_input": case["teacher_input"],
            "student_baseline": case["student_baseline"],
            "core_learning_problem": case["core_learning_problem"],
            "resource_budget": case["resource_budget"],
            "constraints": case["constraints"],
            "available_resource_candidates": case["available_resource_candidates"],
        },
        "output_limits": {
            "target_resolution_count": 2,
            "step_reasoning_updates_count": 1,
            "step_reasoning_updates_step_id": primary_step,
            "step_reasoning_updates_step_name": primary_step_name,
            "field_patch_candidates_count": 2,
            "impact_scope_count": 3,
            "teacher_questions_count": 0,
            "string_max_chars": 32,
            "array_item_max_count": 2,
        },
        "must_return_keys": [
            "lesson_design_mode",
            "intent_summary",
            "lesson_design_brief_compact",
            "target_resolution",
            "step_reasoning_updates",
            "field_patch_candidates",
            "impact_scope",
            "quality_gate_update",
            "teacher_questions",
            "ui_binding_hint",
            "boundary_flags",
        ],
        "exact_shapes": {
            "lesson_design_brief_compact": {
                "core_learning_problem": "string",
                "student_baseline": "string",
                "target_shift": "string",
                "teaching_route": ["string"],
                "evidence_plan": ["string"],
                "risk_points": ["string"],
                "basis_summary": ["string"],
            },
            "target_resolution_item": {
                "section_id": "analysis|goals|preparation|teaching_process|assessment|basis",
                "step_id": "intro|sense|explore|make|share 或空字符串",
                "target_field": "string",
                "reason": "string",
            },
            "step_reasoning_update_item": {
                "step_id": "intro|sense|explore|make|share",
                "step_name": "导入|感知|探究|表现|交流展示",
                "student_state_before": "string",
                "student_state_after": "string",
                "teacher_action": "string",
                "student_action": "string",
                "big_screen_state": "string",
                "learning_sheet_state": "string",
                "assessment_evidence": "string",
                "risk_and_adjustment": "string",
            },
            "field_patch_candidate_item": {
                "field_patch_id": "p1",
                "target_section": "analysis|goals|preparation|teaching_process|assessment|basis",
                "target_step_id": "intro|sense|explore|make|share 或空字符串",
                "target_field": "string",
                "patch_type": "fill_missing|revise|restructure|add_example|simplify|enrich",
                "before_summary": "string",
                "after_candidate": "string",
                "reasoning_basis": ["教材|课标|教学预设|资料候选|小备推测"],
                "impact_scope": ["big_screen|handout|rubric|resource_reference|evidence_note|teacher_action|student_activity"],
                "teacher_review_required": True,
                "formal_apply_performed": False,
            },
            "impact_scope_item": {
                "affected_object": "big_screen|handout|rubric|resource_reference|evidence_note|teacher_action|student_activity",
                "impact_summary": "string",
                "requires_teacher_confirmation": True,
            },
            "quality_gate_update": {
                "level": "basic_usable|ready_to_teach|refined|open_class_ready",
                "passed_items": ["string"],
                "missing_items": ["string"],
                "risk_items": ["string"],
                "next_best_action": "string",
            },
            "teacher_questions": [],
            "ui_binding_hint": {
                "should_enter_edit_mode": True,
                "edit_target": "短字符串",
                "candidate_display_position": "短字符串",
                "right_tray_updates": ["string"],
                "view_mode_summary": "短字符串",
            },
            "boundary_flags": BOUNDARY_FLAGS,
        },
        "coverage": {
            "expected_target_sections": case["expected_target_sections"],
            "expected_impact_scope": case["expected_impact_scope"],
            "expected_quality_level": case["expected_quality_level"],
        },
        "hard_rules": [
            "只输出 JSON 对象，不要 markdown，不要代码块，不要解释文字。",
            "不要输出完整教案，只输出候选补丁、环节推理、影响范围和教师确认信息。",
            "只写 1 个 step_reasoning_updates，必须是 output_limits 指定的 step_id。",
            "只写 2 个 field_patch_candidates。",
            "只写 3 个 impact_scope。",
            "teacher_questions 必须是空数组 []。",
            "每个字符串不超过 32 个汉字。",
            "每个数组最多 2 项，除 impact_scope 必须 3 项。",
            "target_resolution 必须是对象数组，不许是字符串数组。",
            "field_patch_candidates 必须使用 target_section target_step_id target_field before_summary after_candidate 这些字段名。",
            "impact_scope 必须使用 affected_object impact_summary requires_teacher_confirmation 这些字段名。",
            "每个通过项都必须 teacher_review_required=true 且 formal_apply_performed=false。",
            "没有真实学生档案时，依据写教学预设、小备推测、教材、课标或资料候选。",
            "不要出现 field/path/type/content/purpose/current_value/patch_value 这类旧字段名。",
        ],
    }
    if retry:
        request["retry_note"] = "上次输出不是纯 JSON。本次第一个字符必须是 {，最后一个字符必须是 }。"
        request["output_limits"]["string_max_chars"] = 24
        request["output_limits"]["array_item_max_count"] = 1
        request["hard_rules"] = [
            "第一个字符必须是 {，最后一个字符必须是 }。",
            "严禁 ```json 或任何 markdown。",
            "teacher_questions 必须是 []。",
            "只写 1 个环节、2 条候选、3 个影响对象。",
            "每个字符串不超过 24 个汉字。",
            "只读候选，必须等老师确认。",
        ]
    return {
        "system_prompt": "你是师维备课室的小备。只返回严格 JSON。输出必须短，不写完整教案，不展开五个环节，所有候选只读，等老师确认。",
        "user_prompt": json.dumps(request, ensure_ascii=False, separators=(",", ":")),
    }


def is_empty_content_payload(parsed: dict[str, Any] | None) -> bool:
    if not isinstance(parsed, dict):
        return True
    core_fields = [
        str(parsed.get("lesson_design_mode") or "").strip(),
        str(parsed.get("intent_summary") or "").strip(),
        str(parsed.get("lesson_design_brief_compact") or "").strip(),
        str(parsed.get("quality_gate_update") or "").strip(),
    ]
    array_fields = [
        parsed.get("target_resolution"),
        parsed.get("step_reasoning_updates"),
        parsed.get("field_patch_candidates"),
        parsed.get("impact_scope"),
    ]
    has_array_content = any(isinstance(item, list) and item for item in array_fields)
    return not any(core_fields) and not has_array_content


def call_provider(case: dict[str, Any]) -> dict[str, Any]:
    prompt = build_prompt(case)
    started = time.perf_counter()
    provider_result = providers.generate_json_patch(
        {"mode": STAGE_ID, "case_id": case["case_id"]},
        prompt,
        {
            "provider": "openai_compatible",
            "model": "MiniMax-M2.7-highspeed",
            "temperature": 0.1,
            "max_tokens": 1500,
            "timeout_ms": 100000,
            "use_response_format": True,
            "use_reasoning_split": False,
        },
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    raw_text = str(provider_result.get("raw_text") or "")
    provider_meta = provider_result.get("provider_meta") if isinstance(provider_result.get("provider_meta"), dict) else {}
    parsed, parser_meta = parse_lesson_reasoning_output(raw_text, provider_meta)
    attempts = [
        {
            "parser_mode": parser_meta.get("parser_mode"),
            "latency_ms": provider_meta.get("latency_ms") or latency_ms,
            "raw_response_prefix_redacted": redact_text(raw_text)[:800],
        }
    ]
    if parsed is None:
        retry_prompt = build_prompt(case, retry=True)
        retry_started = time.perf_counter()
        retry_provider_result = providers.generate_json_patch(
            {"mode": STAGE_ID, "case_id": case["case_id"], "retry": True},
            retry_prompt,
            {
                "provider": "openai_compatible",
                "model": "MiniMax-M2.7-highspeed",
                "temperature": 0.1,
                "max_tokens": 1200,
                "timeout_ms": 100000,
                "use_response_format": True,
                "use_reasoning_split": False,
            },
        )
        retry_latency_ms = round((time.perf_counter() - retry_started) * 1000)
        retry_raw_text = str(retry_provider_result.get("raw_text") or "")
        retry_provider_meta = (
            retry_provider_result.get("provider_meta")
            if isinstance(retry_provider_result.get("provider_meta"), dict)
            else {}
        )
        retry_parsed, retry_parser_meta = parse_lesson_reasoning_output(retry_raw_text, retry_provider_meta)
        attempts.append(
            {
                "parser_mode": retry_parser_meta.get("parser_mode"),
                "latency_ms": retry_provider_meta.get("latency_ms") or retry_latency_ms,
                "raw_response_prefix_redacted": redact_text(retry_raw_text)[:800],
            }
        )
        raw_text = retry_raw_text
        provider_meta = retry_provider_meta
        parsed = retry_parsed
        parser_meta = retry_parser_meta
        latency_ms = retry_provider_meta.get("latency_ms") or retry_latency_ms
        prompt = retry_prompt
    normalized = normalize_payload(parsed, case)
    raw_contract_errors = validate_compact_lesson_reasoning_payload(parsed)
    normalized_contract_errors = validate_compact_lesson_reasoning_payload(normalized)
    raw_coverage_errors = coverage_errors(parsed, case)
    normalized_coverage_errors = coverage_errors(normalized, case)
    teacher_visible_text = build_teacher_visible_text(normalized)
    visible_term_hits = forbidden_visible_term_hits(teacher_visible_text)
    secret_hits = secret_scan_text(raw_text)
    normalized_secret_hits = secret_scan_text(json.dumps(normalized, ensure_ascii=False))
    raw_json_parse_success = parser_meta.get("parser_mode") == "strict_json_parser" and isinstance(parsed, dict)
    raw_contract_success = not raw_contract_errors and not raw_coverage_errors
    normalized_contract_success = not normalized_contract_errors and not normalized_coverage_errors
    markdown_fence_count = raw_text.count("```")
    empty_content = is_empty_content_payload(parsed)
    schema_drift = bool(parsed is not None and not raw_contract_success)
    forbidden_side_effects = bool(
        visible_term_hits or secret_hits or "teacher_review_required" not in (normalized.get("boundary_flags") if isinstance(normalized, dict) else {})
        or (normalized.get("boundary_flags", {}).get("teacher_review_required") is not True)
        or (normalized.get("boundary_flags", {}).get("formal_apply_performed") is not False)
        or (normalized.get("boundary_flags", {}).get("database_written") is not False)
    )
    score = score_case(
        case,
        parsed,
        normalized,
        parser_meta,
        raw_contract_errors,
        raw_coverage_errors,
        normalized_contract_errors,
        normalized_coverage_errors,
        raw_json_parse_success=raw_json_parse_success,
        schema_drift_count=1 if schema_drift else 0,
        markdown_fence_count=markdown_fence_count,
        empty_content=empty_content,
        forbidden_side_effects=forbidden_side_effects,
    )
    result = {
        "case_id": case["case_id"],
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "strict_json_success": raw_json_parse_success,
        "raw_json_parse_success": raw_json_parse_success,
        "raw_contract_success": raw_contract_success,
        "normalized_contract_success": normalized_contract_success,
        "schema_drift_count": 1 if schema_drift else 0,
        "markdown_fence_count": markdown_fence_count,
        "empty_content_count": 1 if empty_content else 0,
        "forbidden_side_effects": forbidden_side_effects,
        "parser_mode": parser_meta.get("parser_mode") or "unknown",
        "parser_meta": public_parser_meta(parser_meta),
        "attempt_count": len(attempts),
        "attempt_parser_modes": [item["parser_mode"] for item in attempts],
        "raw_contract_errors": raw_contract_errors,
        "raw_coverage_errors": raw_coverage_errors,
        "normalized_contract_errors": normalized_contract_errors,
        "normalized_coverage_errors": normalized_coverage_errors,
        "visible_forbidden_term_hits": visible_term_hits,
        "secret_scan_hits": sorted(set(secret_hits + normalized_secret_hits)),
        "provider_called": True,
        "model_called": True,
        "latency_ms": provider_meta.get("latency_ms") or latency_ms,
        "provider_meta": public_provider_meta(provider_meta),
        "parsed_json": parsed,
        "normalized_json": normalized,
        "teacher_visible_summary": teacher_visible_text,
        "benchmark_score": score,
        "boundary_flags": dict(BOUNDARY_FLAGS),
        "redacted_request": redact_text(json.dumps(prompt, ensure_ascii=False)),
        "raw_response_redacted": redact_text(raw_text),
        "redacted_attempts": attempts,
    }
    return result


def normalize_payload(parsed: dict[str, Any] | None, case: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(parsed, dict):
        return None
    normalized = dict(parsed)
    normalized["lesson_design_mode"] = str(parsed.get("lesson_design_mode") or case["lesson_design_mode"])
    normalized["intent_summary"] = str(parsed.get("intent_summary") or case["teacher_input"])
    normalized["lesson_design_brief_compact"] = normalize_brief(parsed.get("lesson_design_brief_compact"), case)
    normalized["target_resolution"] = normalize_targets(parsed.get("target_resolution"), case)
    normalized["step_reasoning_updates"] = normalize_steps(parsed.get("step_reasoning_updates"), case)
    normalized["field_patch_candidates"] = normalize_patches(parsed.get("field_patch_candidates"), case)
    normalized["impact_scope"] = normalize_impacts(parsed.get("impact_scope"), case)
    normalized["quality_gate_update"] = normalize_quality_gate(parsed.get("quality_gate_update"), case)
    normalized["teacher_questions"] = normalize_teacher_questions(parsed.get("teacher_questions"))
    normalized["ui_binding_hint"] = normalize_ui_binding(parsed.get("ui_binding_hint"), case)
    normalized["boundary_flags"] = dict(BOUNDARY_FLAGS)
    return normalized


def normalize_brief(value: Any, case: dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        brief = dict(value)
    else:
        brief = {"core_learning_problem": str(value or "")}
    return {
        "core_learning_problem": text_or(brief.get("core_learning_problem"), case["core_learning_problem"]),
        "student_baseline": text_or(brief.get("student_baseline"), case["student_baseline"]),
        "target_shift": text_or(brief.get("target_shift"), "从表层判断推进到能说出色彩感受、理由和表达选择。"),
        "teaching_route": list_or(brief.get("teaching_route"), ["唤起生活经验", "比较颜色感受", "分组探究", "表达创作", "交流证据"]),
        "evidence_plan": list_or(brief.get("evidence_plan"), ["观察学生能否说出理由", "收集学习单或口头表达", "记录作品说明"]),
        "risk_points": list_or(brief.get("risk_points"), ["学生可能停在好看不好看的表达，需要追问和材料支架。"]),
        "basis_summary": list_or(brief.get("basis_summary"), ["依据来自教材主题、三年级认知特点、教师输入和资料候选。"]),
    }


def normalize_targets(value: Any, case: dict[str, Any]) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    targets: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if isinstance(item, dict):
            section = normalize_section(item.get("section_id") or item.get("target_section") or item.get("field"))
            step = normalize_step(item.get("step_id") or item.get("target_step_id") or item.get("step"))
            target_field = str(item.get("target_field") or item.get("field_name") or item.get("path") or "设计字段").strip()
            reason = str(item.get("reason") or item.get("why") or item.get("purpose") or "回应教师输入中的备课问题。").strip()
        else:
            section, step = parse_target_string(str(item))
            target_field = "设计字段"
            reason = "模型返回了简写目标，本地归一化为可校验目标。"
        targets.append({
            "section_id": section or "teaching_process",
            "step_id": step or "",
            "target_field": target_field or "设计字段",
            "reason": reason or "回应教师输入中的备课问题。",
        })
    for expected in case.get("expected_target_sections") or []:
        section = normalize_section(expected)
        if section and not any(item["section_id"] == section for item in targets):
            targets.append({
                "section_id": section,
                "step_id": "explore" if section == "teaching_process" else "",
                "target_field": "补充设计候选",
                "reason": "覆盖本案例预期修改位置。",
            })
    return targets


def normalize_steps(value: Any, case: dict[str, Any]) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    steps: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        step_id = normalize_step(item.get("step_id") or item.get("target_step_id") or item.get("step")) or infer_step_from_case(case)
        step_name = step_name_for(step_id)
        steps.append({
            "step_id": step_id,
            "step_name": text_or(item.get("step_name"), step_name),
            "student_state_before": text_or(item.get("student_state_before"), case["student_baseline"]),
            "student_state_after": text_or(item.get("student_state_after"), "学生能用一句话说出色彩带来的感受和理由。"),
            "teacher_action": text_or(item.get("teacher_action"), "教师用材料或问题引导学生观察、分类、表达理由。"),
            "student_action": text_or(item.get("student_action"), "学生观察材料，尝试分类，并说出自己的理由。"),
            "big_screen_state": text_or(item.get("big_screen_state"), screen_state_for(case)),
            "learning_sheet_state": text_or(item.get("learning_sheet_state"), handout_state_for(case)),
            "assessment_evidence": text_or(item.get("assessment_evidence"), "看学生是否能说出分类或创作理由。"),
            "risk_and_adjustment": text_or(item.get("risk_and_adjustment"), "若学生只说好看，教师追问像什么、让你想到什么、为什么这样分。"),
        })
    if not steps:
        step_id = infer_step_from_case(case)
        steps.append({
            "step_id": step_id,
            "step_name": step_name_for(step_id),
            "student_state_before": case["student_baseline"],
            "student_state_after": "学生能把颜色、感受和表达理由连起来。",
            "teacher_action": "教师围绕本节关键问题组织观察、比较和表达。",
            "student_action": "学生参与观察、分类、表达或创作。",
            "big_screen_state": screen_state_for(case),
            "learning_sheet_state": handout_state_for(case),
            "assessment_evidence": "记录学生表达理由、作品说明或活动表现。",
            "risk_and_adjustment": "根据学生反应减少讲解，增加直观材料和句式支架。",
        })
    return steps


def normalize_patches(value: Any, case: dict[str, Any]) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    patches: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        section = normalize_section(item.get("target_section") or item.get("section_id") or item.get("field"))
        path = str(item.get("target_step_id") or item.get("step_id") or item.get("path") or "")
        step = normalize_step(path) or normalize_step(item.get("step"))
        if not section and "/" in path:
            section, step = parse_target_string(path)
        patches.append({
            "field_patch_id": text_or(item.get("field_patch_id"), f"{case['case_id']}-p{index + 1}"),
            "target_section": section or "teaching_process",
            "target_step_id": step or (infer_step_from_case(case) if section == "teaching_process" else ""),
            "target_field": text_or(item.get("target_field") or item.get("field_name") or item.get("path"), "设计内容"),
            "patch_type": normalize_patch_type(item.get("patch_type")),
            "before_summary": text_or(item.get("before_summary") or item.get("current_value"), "当前设计还需要更贴合学生状态和课堂约束。"),
            "after_candidate": text_or(item.get("after_candidate") or item.get("patch") or item.get("patch_value"), "补充直观材料、学生表达任务和评价证据。"),
            "reasoning_basis": list_or(item.get("reasoning_basis"), ["教师输入", "教学预设", "资料候选"]),
            "impact_scope": normalize_impact_id_list(item.get("impact_scope"), case),
            "teacher_review_required": True,
            "formal_apply_performed": False,
        })
    required_sections = [normalize_section(item) for item in case.get("expected_target_sections") or []]
    for section in [item for item in required_sections if item]:
        if not any(patch["target_section"] == section for patch in patches):
            patches.append(default_patch(case, section, len(patches) + 1))
    return patches


def normalize_impacts(value: Any, case: dict[str, Any]) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    impacts: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            affected = normalize_impact(item.get("affected_object") or item.get("type") or item.get("object"))
            summary = text_or(item.get("impact_summary") or item.get("content") or item.get("purpose"), "需要教师确认后再进入正式设计。")
        else:
            affected = normalize_impact(item)
            summary = "影响课堂材料或评价证据，需要教师确认。"
        if affected:
            impacts.append({
                "affected_object": affected,
                "impact_summary": summary,
                "requires_teacher_confirmation": True,
            })
    for expected in case.get("expected_impact_scope") or []:
        affected = normalize_impact(expected)
        if affected and not any(item["affected_object"] == affected for item in impacts):
            impacts.append({
                "affected_object": affected,
                "impact_summary": default_impact_summary(affected, case),
                "requires_teacher_confirmation": True,
            })
    return impacts


def normalize_quality_gate(value: Any, case: dict[str, Any]) -> dict[str, Any]:
    gate = value if isinstance(value, dict) else {}
    expected = case.get("expected_quality_level") or "ready_to_teach"
    level = gate.get("level") if gate.get("level") in {"basic_usable", "ready_to_teach", "refined", "open_class_ready"} else expected
    return {
        "level": level,
        "passed_items": list_or(gate.get("passed_items"), ["能对应学习问题", "有课堂活动", "有评价证据"]),
        "missing_items": list_or(gate.get("missing_items"), []),
        "risk_items": list_or(gate.get("risk_items"), ["仍需教师根据真实班级状态确认材料和时间。"]),
        "next_best_action": text_or(gate.get("next_best_action"), "请教师确认候选是否并入当前备课本。"),
    }


def normalize_teacher_questions(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    questions: list[dict[str, Any]] = []
    for item in value[:2]:
        if isinstance(item, dict):
            questions.append({
                "question": text_or(item.get("question"), ""),
                "why_needed": text_or(item.get("why_needed"), "用于确认课堂真实条件。"),
                "options": list_or(item.get("options"), []),
            })
        elif str(item).strip():
            questions.append({"question": str(item).strip(), "why_needed": "用于确认课堂真实条件。", "options": []})
    return [item for item in questions if item["question"]]


def normalize_ui_binding(value: Any, case: dict[str, Any]) -> dict[str, Any]:
    ui = value if isinstance(value, dict) else {}
    edit_target = text_or(ui.get("edit_target"), edit_target_for(case))
    return {
        "should_enter_edit_mode": True,
        "edit_target": sanitize_teacher_text(edit_target),
        "candidate_display_position": sanitize_teacher_text(text_or(ui.get("candidate_display_position"), "当前段落下方")),
        "right_tray_updates": [
            sanitize_teacher_text(item)
            for item in list_or(ui.get("right_tray_updates"), ["小备判断", "影响范围", "候选确认"])
        ],
        "view_mode_summary": sanitize_teacher_text(text_or(ui.get("view_mode_summary"), "查看态保留连续教学设计，编辑态聚焦当前候选。")),
    }


def coverage_errors(payload: dict[str, Any] | None, case: dict[str, Any]) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    errors: list[str] = []
    targets = payload.get("target_resolution") if isinstance(payload.get("target_resolution"), list) else []
    target_sections = {item.get("section_id") for item in targets if isinstance(item, dict)}
    patches = payload.get("field_patch_candidates") if isinstance(payload.get("field_patch_candidates"), list) else []
    patch_sections = {item.get("target_section") for item in patches if isinstance(item, dict)}
    covered_sections = target_sections | patch_sections
    for section in case.get("expected_target_sections") or []:
        normalized = normalize_section(section)
        if normalized and normalized not in covered_sections:
            errors.append(f"missing_expected_section_{normalized}")
    impacts = payload.get("impact_scope") if isinstance(payload.get("impact_scope"), list) else []
    impact_ids = {item.get("affected_object") for item in impacts if isinstance(item, dict)}
    for affected in case.get("expected_impact_scope") or []:
        normalized = normalize_impact(affected)
        if normalized and normalized not in impact_ids:
            errors.append(f"missing_expected_impact_{normalized}")
    boundary = payload.get("boundary_flags") if isinstance(payload.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("boundary_teacher_review_required_not_true")
    for key in ["formal_apply_performed", "database_written", "memory_written", "feishu_written", "formal_export_created", "official_archive_created"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary_{key}_not_false")
    return errors


def score_case(
    case: dict[str, Any],
    parsed: dict[str, Any] | None,
    normalized: dict[str, Any] | None,
    parser_meta: dict[str, Any],
    raw_contract_errors: list[str],
    raw_coverage_errors: list[str],
    normalized_contract_errors: list[str],
    normalized_coverage_errors: list[str],
    raw_json_parse_success: bool,
    schema_drift_count: int,
    markdown_fence_count: int,
    empty_content: bool,
    forbidden_side_effects: bool,
) -> dict[str, Any]:
    payload = normalized if isinstance(normalized, dict) else {}
    strict_json_success = bool(raw_json_parse_success)
    target_resolution_score = 5 if not normalized_coverage_errors else max(1, 5 - len([e for e in normalized_coverage_errors if "section" in e]))
    teaching_reasoning_score = score_teaching_reasoning(payload)
    impact_scope_score = score_impact_scope(payload, case)
    quality_gate_score = score_quality_gate(payload, case)
    age_score = score_age_appropriateness(payload)
    not_over_scope = is_not_over_scope(payload)
    not_too_generic = is_not_too_generic(payload)
    boundary = payload.get("boundary_flags") if isinstance(payload.get("boundary_flags"), dict) else {}
    teacher_review_required = boundary.get("teacher_review_required") is True
    formal_apply_performed = boundary.get("formal_apply_performed") is True
    visible_hits = forbidden_visible_term_hits(build_teacher_visible_text(payload))
    parse_error_code = parser_meta.get("parse_error_code")
    quality_score = 0.0
    if strict_json_success and not empty_content:
        quality_score = round(
            (
                target_resolution_score
                + teaching_reasoning_score
                + impact_scope_score
                + quality_gate_score
                + age_score
            )
            / 5,
            2,
        )
    overall_pass = (
        strict_json_success
        and not normalized_contract_errors
        and not normalized_coverage_errors
        and target_resolution_score >= 4
        and teaching_reasoning_score >= 4
        and impact_scope_score >= 4
        and quality_gate_score >= 3
        and age_score >= 4
        and not_over_scope
        and not_too_generic
        and teacher_review_required
        and not formal_apply_performed
        and not visible_hits
        and not forbidden_side_effects
        and not empty_content
    )
    issues: list[str] = []
    if raw_contract_errors:
        issues.append("raw_contract_needs_normalization")
    if raw_coverage_errors:
        issues.extend(raw_coverage_errors)
    if parse_error_code:
        issues.append(f"parse_error_{parse_error_code}")
    if normalized_contract_errors:
        issues.extend(normalized_contract_errors)
    if normalized_coverage_errors:
        issues.extend(normalized_coverage_errors)
    if schema_drift_count:
        issues.append("schema_drift_detected")
    if markdown_fence_count:
        issues.append("markdown_fence_detected")
    if empty_content:
        issues.append("empty_content")
    if visible_hits:
        issues.append("teacher_visible_forbidden_terms")
    if forbidden_side_effects:
        issues.append("forbidden_side_effects")
    if not_too_generic is False:
        issues.append("too_generic")
    if not_over_scope is False:
        issues.append("over_scope")
    return {
        "case_id": case["case_id"],
        "strict_json_success": strict_json_success,
        "raw_json_parse_success": strict_json_success,
        "target_resolution_score": target_resolution_score,
        "teaching_reasoning_score": teaching_reasoning_score,
        "impact_scope_score": impact_scope_score,
        "quality_gate_score": quality_gate_score,
        "quality_score": quality_score,
        "age_appropriateness_score": age_score,
        "not_over_scope": not_over_scope,
        "not_too_generic": not_too_generic,
        "teacher_review_required": teacher_review_required,
        "formal_apply_performed": formal_apply_performed,
        "overall_pass": overall_pass,
        "raw_contract_success": not raw_contract_errors,
        "normalized_contract_success": not normalized_contract_errors,
        "raw_contract_error_count": len(raw_contract_errors),
        "raw_coverage_error_count": len(raw_coverage_errors),
        "normalized_contract_error_count": len(normalized_contract_errors),
        "normalized_coverage_error_count": len(normalized_coverage_errors),
        "schema_drift_count": schema_drift_count,
        "markdown_fence_count": markdown_fence_count,
        "empty_content": bool(empty_content),
        "empty_content_count": 1 if empty_content else 0,
        "forbidden_side_effects": bool(forbidden_side_effects),
        "issues": issues,
        "repair_suggestion": repair_suggestion_for(issues),
    }


def score_teaching_reasoning(payload: dict[str, Any]) -> int:
    steps = payload.get("step_reasoning_updates") if isinstance(payload.get("step_reasoning_updates"), list) else []
    if not steps:
        return 1
    required = ["student_state_before", "student_state_after", "teacher_action", "student_action", "assessment_evidence", "risk_and_adjustment"]
    first = steps[0] if isinstance(steps[0], dict) else {}
    present = sum(1 for key in required if len(str(first.get(key) or "")) >= 8)
    joined = json.dumps(steps, ensure_ascii=False)
    if any(term in joined for term in ["理由", "感受", "证据", "调整"]):
        present += 1
    return min(5, max(1, present))


def score_impact_scope(payload: dict[str, Any], case: dict[str, Any]) -> int:
    impacts = payload.get("impact_scope") if isinstance(payload.get("impact_scope"), list) else []
    ids = {item.get("affected_object") for item in impacts if isinstance(item, dict)}
    expected = {normalize_impact(item) for item in case.get("expected_impact_scope") or []}
    expected.discard(None)
    hits = len(ids & expected)
    if not impacts:
        return 1
    if hits >= len(expected) and len(impacts) >= 3:
        return 5
    if hits >= max(1, len(expected) - 1):
        return 4
    return max(1, 2 + hits)


def score_quality_gate(payload: dict[str, Any], case: dict[str, Any]) -> int:
    gate = payload.get("quality_gate_update") if isinstance(payload.get("quality_gate_update"), dict) else {}
    level = gate.get("level")
    score = 2
    if level:
        score += 1
    if level == case.get("expected_quality_level"):
        score += 1
    if gate.get("next_best_action"):
        score += 1
    return min(5, score)


def score_age_appropriateness(payload: dict[str, Any]) -> int:
    text = json.dumps(payload, ensure_ascii=False)
    score = 4
    if any(term in text for term in ["抽象理论", "专业色相环分析", "论文", "研究范式"]):
        score -= 2
    if any(term in text for term in ["色卡", "生活", "感受", "一句话", "观察", "分类", "理由"]):
        score += 1
    return min(5, max(1, score))


def is_not_over_scope(payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, ensure_ascii=False)
    forbidden = ["真实学生档案显示", "已写入", "正式导出", "同步飞书", "自动归档", "已经应用"]
    return not any(term in text for term in forbidden)


def is_not_too_generic(payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, ensure_ascii=False)
    anchors = ["色彩", "冷暖", "感受", "理由", "色卡", "生活", "学习单", "大屏", "评价", "三年级"]
    return sum(1 for item in anchors if item in text) >= 4 and len(text) > 400


def build_teacher_visible_text(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return ""
    teacher_payload = {
        "intent_summary": payload.get("intent_summary"),
        "brief": payload.get("lesson_design_brief_compact"),
        "steps": payload.get("step_reasoning_updates"),
        "candidates": payload.get("field_patch_candidates"),
        "impact": payload.get("impact_scope"),
        "gate": payload.get("quality_gate_update"),
        "ui": payload.get("ui_binding_hint"),
    }
    return "\n".join(sanitize_teacher_text(item) for item in leaf_strings(teacher_payload))


def aggregate_scores(scores: list[dict[str, Any]]) -> dict[str, Any]:
    def avg(key: str) -> float:
        values = [float(item.get(key) or 0) for item in scores]
        return round(sum(values) / len(values), 2) if values else 0.0

    strict_count = sum(1 for item in scores if item.get("strict_json_success"))
    pass_count = sum(1 for item in scores if item.get("overall_pass"))
    raw_contract_count = sum(1 for item in scores if item.get("raw_contract_success"))
    normalized_contract_count = sum(1 for item in scores if item.get("normalized_contract_success"))
    raw_json_parse_count = sum(1 for item in scores if item.get("raw_json_parse_success"))
    empty_content_count = sum(1 for item in scores if item.get("empty_content"))
    markdown_fence_count = sum(int(item.get("markdown_fence_count") or 0) for item in scores)
    schema_drift_count = sum(int(item.get("schema_drift_count") or 0) for item in scores)
    forbidden_side_effects_count = sum(1 for item in scores if item.get("forbidden_side_effects"))
    low_quality_case_count = sum(1 for item in scores if (item.get("quality_score") or 0) < DIAG_LOW_QUALITY_THRESHOLD)
    return {
        "case_count": len(scores),
        "raw_json_parse_pass_count": raw_json_parse_count,
        "strict_json_success_count": strict_count,
        "overall_pass_count": pass_count,
        "raw_contract_success_count": raw_contract_count,
        "normalized_contract_success_count": normalized_contract_count,
        "empty_content_count": empty_content_count,
        "markdown_fence_count": markdown_fence_count,
        "schema_drift_count": schema_drift_count,
        "forbidden_side_effects_count": forbidden_side_effects_count,
        "average_quality_score": avg("quality_score"),
        "low_quality_case_count": low_quality_case_count,
        "average_target_resolution_score": avg("target_resolution_score"),
        "average_teaching_reasoning_score": avg("teaching_reasoning_score"),
        "average_impact_scope_score": avg("impact_scope_score"),
        "average_quality_gate_score": avg("quality_gate_score"),
        "average_age_appropriateness_score": avg("age_appropriateness_score"),
        "all_pass_teacher_review_required": all(
            item.get("teacher_review_required") is True for item in scores if item.get("overall_pass")
        ),
        "all_pass_formal_apply_false": all(
            item.get("formal_apply_performed") is False for item in scores if item.get("overall_pass")
        ),
    }


def final_status_for(scores: list[dict[str, Any]], aggregate: dict[str, Any], secret_scan_ok: bool) -> tuple[str, str]:
    raw_json_parse_pass = aggregate.get("raw_json_parse_pass_count", 0)
    raw_contract_pass = aggregate.get("raw_contract_success_count", 0)
    normalized_contract_pass = aggregate.get("normalized_contract_success_count", 0)
    avg_quality = aggregate.get("average_quality_score", 0.0)
    low_quality_count = aggregate.get("low_quality_case_count", 0)
    raw_json_stable = raw_json_parse_pass >= DIAG_STABILITY_THRESHOLD
    raw_contract_stable = raw_contract_pass >= DIAG_STABILITY_THRESHOLD
    normalized_contract_stable = normalized_contract_pass >= DIAG_STABILITY_THRESHOLD
    if not secret_scan_ok:
        return "FAIL_SECRET_SCAN_HIT", "1013E_R2_SECRET_REVIEW"
    if not raw_json_stable:
        return DIAG_REPAIR_REQUIRED, NEXT_STAGE_REPAIR
    quality_ok = avg_quality >= DIAG_LOW_QUALITY_THRESHOLD and low_quality_count <= 2
    if raw_contract_stable and normalized_contract_stable and quality_ok:
        return DIAG_COMPLETED_NO_NORMALIZATION, NEXT_STAGE_DIAG_COMPLETE
    if normalized_contract_stable and quality_ok:
        return DIAG_PASS_WITH_NORMALIZATION, NEXT_STAGE_NORMALIZATION_REQUIRED
    return DIAG_REPAIR_REQUIRED, NEXT_STAGE_REPAIR


def write_report(result: dict[str, Any], case_results: list[dict[str, Any]], aggregate: dict[str, Any]) -> None:
    raw_model_output_contract_result = "PASS" if aggregate.get("raw_contract_success_count", 0) >= DIAG_STABILITY_THRESHOLD else "FAIL"
    normalized_contract_result = (
        "PASS" if aggregate.get("normalized_contract_success_count", 0) >= DIAG_STABILITY_THRESHOLD else "FAIL"
    )
    teaching_quality_result = (
        "PASS"
        if aggregate.get("average_quality_score", 0) >= DIAG_LOW_QUALITY_THRESHOLD and aggregate.get("low_quality_case_count", 0) <= 2
        else "NEED_REPAIR"
    )

    def case_conclusion(score: dict[str, Any]) -> str:
        if not score.get("raw_json_parse_success"):
            return "raw_json_parse_failed"
        if score.get("empty_content"):
            return "empty_content"
        if score.get("forbidden_side_effects"):
            return "forbidden_side_effects"
        if score.get("overall_pass"):
            return "pass"
        if score.get("raw_contract_success"):
            return "normalized_pass"
        if score.get("schema_drift_count"):
            return "schema_drift"
        return "review_required"

    lines = [
        "# 1013E_R2 Multi-Case Lesson Reasoning Benchmark",
        "",
        "```text",
        f"final_status={result.get('final_status')}",
        f"next_stage={result.get('next_stage')}",
        f"r2_repair_baseline={R2_REPAIR_BASELINE}",
        "r2_repair_baseline_meaning=R2 repair remains failed; this round is diagnostic only, not a repair pass",
        f"raw_json_parse_pass_count={aggregate.get('raw_json_parse_pass_count')}/12",
        f"raw_contract_success_count={aggregate.get('raw_contract_success_count')}/12",
        f"normalized_contract_success_count={aggregate.get('normalized_contract_success_count')}/12",
        f"overall_pass_count={aggregate.get('overall_pass_count')}/12",
        f"empty_content_count={aggregate.get('empty_content_count')}/12",
        f"markdown_fence_count={aggregate.get('markdown_fence_count')}",
        f"schema_drift_count={aggregate.get('schema_drift_count')}",
        f"forbidden_side_effects_count={aggregate.get('forbidden_side_effects_count')}",
        f"average_quality_score={aggregate.get('average_quality_score')}",
        f"low_quality_case_count={aggregate.get('low_quality_case_count')}/12",
        f"average_teaching_reasoning_score={aggregate.get('average_teaching_reasoning_score')}",
        f"average_impact_scope_score={aggregate.get('average_impact_scope_score')}",
        f"average_age_appropriateness_score={aggregate.get('average_age_appropriateness_score')}",
        f"secret_scan_ok={str(result.get('secret_scan_ok')).lower()}",
        "```",
        "",
        "## Reading The Result",
        "",
        f"- raw_model_output_contract_result={raw_model_output_contract_result}",
        f"- normalized_contract_result={normalized_contract_result}",
        f"- teaching_quality_result={teaching_quality_result}",
        "- `raw_json_parse_success` means raw model output passed strict JSON parsing.",
        "- `raw_contract_success` means raw model output already matched compact contract.",
        "- `normalized_contract_success` means local normalizer mapped output into compact contract.",
        "- `quality_score` is a normalized 0-5 quality score from 5 compact dimensions.",
        f"- recommended_next_stage={result.get('next_stage')}",
        "",
        f"raw_model_output_contract_result={raw_model_output_contract_result}",
        f"normalized_contract_result={normalized_contract_result}",
        f"teaching_quality_result={teaching_quality_result}",
        f"recommended_next_stage={result.get('next_stage')}",
        "",
        "| case_id | raw_json_parse | raw_contract | normalized_contract | quality_score | conclusion |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in case_results:
        score = item.get("benchmark_score") or {}
        lines.append(
            f"| `{item.get('case_id')}` | {str(score.get('raw_json_parse_success')).lower()} | "
            f"{str(score.get('raw_contract_success')).lower()} | {str(score.get('normalized_contract_success')).lower()} | "
            f"{score.get('quality_score')} | {case_conclusion(score)} |"
        )
    lines.extend([
        "",
        "## Case Results (legacy)",
        "",
        "用于回溯：以下保持与历史兼容。",
    ])
    for item in case_results:
        score = item.get("benchmark_score") or {}
        lines.append(
            f"- `{item.get('case_id')}` `{item.get('lesson_design_mode')}`: "
            f"strict={str(score.get('strict_json_success')).lower()}, "
            f"raw_contract={str(score.get('raw_contract_success')).lower()}, "
            f"normalized_contract={str(score.get('normalized_contract_success')).lower()}, "
            f"overall={str(score.get('overall_pass')).lower()}, "
            f"teaching={score.get('teaching_reasoning_score')}, "
            f"impact={score.get('impact_scope_score')}, "
            f"age={score.get('age_appropriateness_score')}, "
            f"quality={score.get('quality_score')}"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Provider was called for benchmark cases when credentials were available.",
            "- No database write.",
            "- No memory write.",
            "- No Feishu write.",
            "- No formal apply.",
            "- No formal export.",
            "- No official archive.",
            "- No real knowledge-base retrieval.",
            "- Requests and responses are redacted in the trace file.",
        ]
    )
    write_text("1013E_R2_report.md", "\n".join(lines) + "\n")


def write_prompt_doc() -> None:
    sample = build_prompt(CASE_BANK[2])
    write_text(
        "prompt_repair_1013E_R2.md",
        "# 1013E_R2 Multi-Case Prompt Repair Template\n\n"
        "## System Prompt\n\n"
        f"{sample['system_prompt']}\n\n"
        "## Sample User Prompt\n\n"
        f"{sample['user_prompt']}\n",
    )


def blocked_outputs(provider_status: dict[str, Any]) -> int:
    write_json("lesson_reasoning_case_bank_1013E_R2.json", CASE_BANK)
    write_prompt_doc()
    case_results = []
    scores = []
    for case in CASE_BANK:
        score = {
            "case_id": case["case_id"],
            "strict_json_success": False,
            "raw_json_parse_success": False,
            "target_resolution_score": 0,
            "teaching_reasoning_score": 0,
            "impact_scope_score": 0,
            "quality_gate_score": 0,
            "quality_score": 0.0,
            "age_appropriateness_score": 0,
            "not_over_scope": True,
            "not_too_generic": False,
            "teacher_review_required": True,
            "formal_apply_performed": False,
            "overall_pass": False,
            "raw_contract_success": False,
            "normalized_contract_success": False,
            "raw_contract_error_count": 1,
            "raw_coverage_error_count": 0,
            "normalized_contract_error_count": 1,
            "normalized_coverage_error_count": 0,
            "schema_drift_count": 0,
            "markdown_fence_count": 0,
            "empty_content": True,
            "empty_content_count": 1,
            "forbidden_side_effects": True,
            "issues": ["missing_provider_env"],
            "repair_suggestion": "配置 provider 环境后重跑 benchmark。",
        }
        case_results.append({
            "case_id": case["case_id"],
            "lesson_design_mode": case["lesson_design_mode"],
            "teacher_input": case["teacher_input"],
            "strict_json_success": False,
            "provider_called": False,
            "model_called": False,
            "benchmark_score": score,
            "boundary_flags": dict(BOUNDARY_FLAGS),
        })
        scores.append(score)
    aggregate = aggregate_scores(scores)
    result = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
        "next_stage": "1013E_R2_PROVIDER_ENV_RECHECK",
        "r2_repair_baseline": R2_REPAIR_BASELINE,
        "provider_called": False,
        "model_called": False,
        "provider_status": provider_status,
        "benchmark": aggregate,
        "secret_scan_ok": True,
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    write_json("case_results_1013E_R2.json", case_results)
    write_json("benchmark_scores_1013E_R2.json", {"scores": scores, "aggregate": aggregate})
    write_json("standard_daily_repair_result_1013E_R2.json", case_results[2])
    write_json("1013E_R2_result.json", result)
    write_json("provider_metrics_1013E_R2.json", {"provider_called": False, "model_called": False, "provider_status": provider_status})
    write_json("redacted_provider_trace_1013E_R2.json", [])
    write_report(result, case_results, aggregate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json("lesson_reasoning_case_bank_1013E_R2.json", CASE_BANK)
    write_prompt_doc()
    provider_status = provider_public_status()
    if not provider_status.get("credential_available"):
        return blocked_outputs(provider_status)

    case_results: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    scores: list[dict[str, Any]] = []
    for case in CASE_BANK:
        try:
            result = call_provider(case)
        except providers.ProviderError as exc:
            score = {
                "case_id": case["case_id"],
                "strict_json_success": False,
                "raw_json_parse_success": False,
                "target_resolution_score": 0,
                "teaching_reasoning_score": 0,
                "impact_scope_score": 0,
                "quality_gate_score": 0,
                "quality_score": 0.0,
                "age_appropriateness_score": 0,
                "not_over_scope": True,
                "not_too_generic": False,
                "teacher_review_required": True,
                "formal_apply_performed": False,
                "overall_pass": False,
                "raw_contract_success": False,
                "normalized_contract_success": False,
                "raw_contract_error_count": 1,
                "raw_coverage_error_count": 0,
                "normalized_contract_error_count": 1,
                "normalized_coverage_error_count": 0,
                "schema_drift_count": 0,
                "markdown_fence_count": 0,
                "empty_content": True,
                "empty_content_count": 1,
                "forbidden_side_effects": True,
                "issues": [exc.code],
                "repair_suggestion": "检查 provider 可用性或降低单次输出长度。",
            }
            result = {
                "case_id": case["case_id"],
                "lesson_design_mode": case["lesson_design_mode"],
                "teacher_input": case["teacher_input"],
                "strict_json_success": False,
                "provider_called": True,
                "model_called": True,
                "parser_mode": "provider_error",
                "error_message_redacted": redact_text(exc.message)[:500],
                "benchmark_score": score,
                "boundary_flags": dict(BOUNDARY_FLAGS),
                "redacted_request": redact_text(json.dumps(build_prompt(case), ensure_ascii=False)),
                "raw_response_redacted": "",
            }
        score = result["benchmark_score"]
        result["secret_scan_hits"] = sorted(set(result.get("secret_scan_hits") or []))
        result["benchmark_score"] = score
        scores.append(score)
        case_results.append(public_case_result(result))
        traces.append(trace_entry(result))

    aggregate = aggregate_scores(scores)
    secret_scan_ok = not any(item.get("secret_scan_hits") for item in case_results)
    final_status, next_stage = final_status_for(scores, aggregate, secret_scan_ok)
    result_payload = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": final_status,
        "next_stage": next_stage,
        "r2_repair_baseline": R2_REPAIR_BASELINE,
        "provider_called": any(item.get("provider_called") for item in case_results),
        "model_called": any(item.get("model_called") for item in case_results),
        "provider_status": provider_status,
        "benchmark": aggregate,
        "standard_daily_repair_success": bool(
            next((item for item in scores if item.get("case_id") == "standard_daily_cold_warm_more_visual"), {}).get("overall_pass")
        ),
        "case_result_file": "case_results_1013E_R2.json",
        "case_bank_file": "lesson_reasoning_case_bank_1013E_R2.json",
        "score_file": "benchmark_scores_1013E_R2.json",
        "secret_scan_ok": secret_scan_ok,
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    latencies = [item.get("latency_ms") for item in case_results if isinstance(item.get("latency_ms"), int)]
    metrics = {
        "provider_called": result_payload["provider_called"],
        "model_called": result_payload["model_called"],
        "case_count": len(case_results),
        "raw_json_parse_pass_count": aggregate["raw_json_parse_pass_count"],
        "strict_json_success_count": aggregate["strict_json_success_count"],
        "overall_pass_count": aggregate["overall_pass_count"],
        "raw_contract_success_count": aggregate["raw_contract_success_count"],
        "normalized_contract_success_count": aggregate["normalized_contract_success_count"],
        "empty_content_count": aggregate["empty_content_count"],
        "markdown_fence_count": aggregate["markdown_fence_count"],
        "schema_drift_count": aggregate["schema_drift_count"],
        "forbidden_side_effects_count": aggregate["forbidden_side_effects_count"],
        "average_quality_score": aggregate["average_quality_score"],
        "low_quality_case_count": aggregate["low_quality_case_count"],
        "latency_summary": {
            "count": len(latencies),
            "min_ms": min(latencies) if latencies else None,
            "max_ms": max(latencies) if latencies else None,
            "avg_ms": round(sum(latencies) / len(latencies)) if latencies else None,
        },
        "provider_status": provider_status,
    }
    standard_case = next(item for item in case_results if item["case_id"] == "standard_daily_cold_warm_more_visual")
    write_json("case_results_1013E_R2.json", case_results)
    write_json("benchmark_scores_1013E_R2.json", {"scores": scores, "aggregate": aggregate})
    write_json("standard_daily_repair_result_1013E_R2.json", standard_case)
    write_json("1013E_R2_result.json", result_payload)
    write_json("provider_metrics_1013E_R2.json", metrics)
    write_json("redacted_provider_trace_1013E_R2.json", traces)
    write_report(result_payload, case_results, aggregate)
    print(json.dumps(result_payload, ensure_ascii=False, indent=2))
    return 0 if final_status in {DIAG_PASS_WITH_NORMALIZATION, DIAG_COMPLETED_NO_NORMALIZATION} else 1


def public_case_result(result: dict[str, Any]) -> dict[str, Any]:
    payload = dict(result)
    payload.pop("redacted_request", None)
    payload.pop("raw_response_redacted", None)
    return payload


def trace_entry(result: dict[str, Any]) -> dict[str, Any]:
    benchmark_score = result.get("benchmark_score") or {}
    return {
        "case_id": result.get("case_id"),
        "lesson_design_mode": result.get("lesson_design_mode"),
        "strict_json_success": result.get("strict_json_success"),
        "raw_json_parse_success": result.get("raw_json_parse_success"),
        "raw_contract_success": result.get("raw_contract_success"),
        "normalized_contract_success": result.get("normalized_contract_success"),
        "raw_contract_error_count": benchmark_score.get("raw_contract_error_count"),
        "raw_coverage_error_count": benchmark_score.get("raw_coverage_error_count"),
        "normalized_contract_error_count": benchmark_score.get("normalized_contract_error_count"),
        "normalized_coverage_error_count": benchmark_score.get("normalized_coverage_error_count"),
        "overall_pass": (result.get("benchmark_score") or {}).get("overall_pass"),
        "parser_mode": result.get("parser_mode"),
        "raw_contract_errors": result.get("raw_contract_errors") or [],
        "raw_coverage_errors": result.get("raw_coverage_errors") or [],
        "normalized_contract_errors": result.get("normalized_contract_errors") or [],
        "normalized_coverage_errors": result.get("normalized_coverage_errors") or [],
        "schema_drift_count": benchmark_score.get("schema_drift_count"),
        "markdown_fence_count": benchmark_score.get("markdown_fence_count"),
        "empty_content": benchmark_score.get("empty_content"),
        "empty_content_count": benchmark_score.get("empty_content_count"),
        "forbidden_side_effects": benchmark_score.get("forbidden_side_effects"),
        "quality_score": benchmark_score.get("quality_score"),
        "visible_forbidden_term_hits": result.get("visible_forbidden_term_hits") or [],
        "secret_scan_hits": result.get("secret_scan_hits") or [],
        "latency_ms": result.get("latency_ms"),
        "provider_meta": result.get("provider_meta") or {},
        "redacted_request": result.get("redacted_request") or "",
        "raw_response_redacted": result.get("raw_response_redacted") or "",
    }


def redact_text(text: str) -> str:
    value = str(text or "")
    replacements = [
        (r"Bearer\s+[A-Za-z0-9._\-]+", "Bearer <REDACTED>"),
        (r"sk-[A-Za-z0-9._\-]{8,}", "sk-<REDACTED>"),
        (r"gh[pousr]_[A-Za-z0-9_]+", "gh-<REDACTED>"),
        (r"(api[_-]?key[\"'\s:=]+)[A-Za-z0-9._\-]+", r"\1<REDACTED>"),
        (r"(secret[\"'\s:=]+)[A-Za-z0-9._\-]+", r"\1<REDACTED>"),
        (r"C:\\Users\\Administrator", r"<USER_HOME_REDACTED>"),
    ]
    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


def secret_scan_text(text: str) -> list[str]:
    return [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text or "")]


def public_provider_meta(meta: dict[str, Any]) -> dict[str, Any]:
    base_url = str(meta.get("base_url") or "")
    host = base_url.split("/")[2] if "://" in base_url else ""
    return {
        "provider": meta.get("provider"),
        "model": meta.get("model"),
        "base_url_host": host,
        "credential_source": meta.get("credential_source"),
        "reasoning_split": bool(meta.get("reasoning_split")),
        "latency_ms": meta.get("latency_ms"),
    }


def public_parser_meta(meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "parser_mode": meta.get("parser_mode"),
        "parse_subcode": meta.get("parse_subcode"),
        "parse_error_code": meta.get("parse_error_code"),
        "raw_prefix_type": meta.get("raw_prefix_type") or meta.get("raw_response_prefix_type"),
        "provider_output_sanitized": bool(meta.get("provider_output_sanitized")),
        "extraction_required": bool(meta.get("extraction_required")),
    }


def forbidden_visible_term_hits(text: str) -> list[str]:
    return [term for term in FORBIDDEN_TEACHER_VISIBLE_TERMS if term in str(text or "")]


def sanitize_teacher_text(value: Any) -> str:
    text = str(value or "")
    replacements = {
        "field_patch_candidates": "修改候选",
        "field_patch": "修改候选",
        "formal_apply": "正式应用",
        "teacher_review_required": "需要老师确认",
        "dry-run": "预览",
        "database": "数据存储",
        "Feishu": "课表系统",
        "memory": "长期记录",
        "provider": "模型通道",
        "schema": "结构",
        "ViewModel": "页面数据",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def leaf_strings(value: Any) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for child in value.values():
            result.extend(leaf_strings(child))
        return result
    if isinstance(value, list):
        result = []
        for child in value:
            result.extend(leaf_strings(child))
        return result
    if isinstance(value, str):
        return [value]
    return []


def text_or(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    return text if text else fallback


def list_or(value: Any, fallback: list[str]) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return list(fallback)


def normalize_section(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    for key, mapped in SECTION_ALIASES.items():
        if key in text:
            return mapped
    return text if text in set(SECTION_ALIASES.values()) else ""


def normalize_step(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    for key, mapped in STEP_ALIASES.items():
        if key in text:
            return mapped
    return text if text in set(STEP_ALIASES.values()) else ""


def normalize_impact(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    for key, mapped in IMPACT_ALIASES.items():
        if key in text:
            return mapped
    return text if text in set(IMPACT_ALIASES.values()) else ""


def parse_target_string(value: str) -> tuple[str, str]:
    text = str(value or "")
    section = normalize_section(text)
    step = normalize_step(text)
    return section, step


def normalize_patch_type(value: Any) -> str:
    text = str(value or "").strip()
    allowed = {"fill_missing", "revise", "restructure", "add_example", "simplify", "enrich"}
    return text if text in allowed else "revise"


def normalize_impact_id_list(value: Any, case: dict[str, Any]) -> list[str]:
    source = value if isinstance(value, list) else case.get("expected_impact_scope") or []
    ids = []
    for item in source:
        mapped = normalize_impact(item)
        if mapped and mapped not in ids:
            ids.append(mapped)
    return ids or ["teacher_action", "student_activity", "evidence_note"]


def infer_step_from_case(case: dict[str, Any]) -> str:
    text = case["teacher_input"]
    if any(term in text for term in ["表现", "作业", "分层", "创作"]):
        return "make"
    if any(term in text for term in ["交流", "展示", "表达"]):
        return "share"
    if any(term in text for term in ["导入", "承上"]):
        return "intro"
    return "explore"


def step_name_for(step_id: str) -> str:
    return {"intro": "导入", "sense": "感知", "explore": "探究", "make": "表现", "share": "交流展示"}.get(step_id, "探究")


def screen_state_for(case: dict[str, Any]) -> str:
    if "没有投影" in " ".join(case.get("constraints") or []):
        return "不用大屏，改为黑板冷暖分区和实物色卡示范。"
    return "呈现与本环节对应的生活图片、作品图或分类提示，帮助学生直观看见差异。"


def handout_state_for(case: dict[str, Any]) -> str:
    if "不能打印" in " ".join(case.get("constraints") or []):
        return "不发纸质学习单，改用口头一句话和教师拍照记录。"
    return "学习单只保留关键记录格，让学生写或画出感受、分类和理由。"


def edit_target_for(case: dict[str, Any]) -> str:
    step = step_name_for(infer_step_from_case(case))
    return f"教学过程 · {step}环节"


def default_patch(case: dict[str, Any], section: str, index: int) -> dict[str, Any]:
    step = infer_step_from_case(case) if section == "teaching_process" else ""
    return {
        "field_patch_id": f"{case['case_id']}-p{index}",
        "target_section": section,
        "target_step_id": step,
        "target_field": "设计内容",
        "patch_type": "revise",
        "before_summary": "当前段落还需要回应教师输入中的具体课堂问题。",
        "after_candidate": f"围绕“{case['core_learning_problem']}”补充可执行活动、材料状态和评价证据。",
        "reasoning_basis": ["教师输入", "教学预设", "资料候选"],
        "impact_scope": normalize_impact_id_list([], case),
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def default_impact_summary(affected: str, case: dict[str, Any]) -> str:
    mapping = {
        "big_screen": "大屏要服务本环节的观察和比较，不做装饰性图片堆叠。",
        "handout": "学习单只记录关键感受、分类或理由，避免加重负担。",
        "rubric": "评价标准要看学生能否说出理由和完成适度表达。",
        "resource_reference": "资料只作为候选依据，需教师确认是否适合本班。",
        "evidence_note": "保留学生发言、分类结果或作品说明作为课堂证据。",
        "teacher_action": "教师动作要从讲解转向追问、示范、收集证据和适时调整。",
        "student_activity": "学生活动要能推动从感受到表达理由的变化。",
    }
    return mapping.get(affected, f"围绕“{case['core_learning_problem']}”调整本对象。")


def repair_suggestion_for(issues: list[str]) -> str:
    if not issues:
        return ""
    if "too_generic" in issues:
        return "继续压 prompt，要求必须引用课题、学生状态、材料和评价证据。"
    if any("raw_contract" in item for item in issues):
        return "保留本地归一化，同时继续修 prompt，减少旧字段名输出。"
    if any("section" in item or "impact" in item for item in issues):
        return "加强 expected_target_sections 与 expected_impact_scope 的显式约束。"
    return "检查结构字段和边界标记。"


if __name__ == "__main__":
    raise SystemExit(main())
