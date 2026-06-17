from __future__ import annotations

from typing import Any

from .output_parser import OutputParserError, parse_patch_output


STAGE_ID = "1013E_MODEL_PROMPT_TO_REASONING_FIELD_PATCH_POC"
R1_STAGE_ID = "1013E_R1_PROMPT_REPAIR_AND_READONLY_REASONING_PIPELINE"

LESSON_CONTEXT = {
    "semester": "2026春学期",
    "subject": "美术",
    "grade": "三年级",
    "unit": "色彩单元",
    "lesson_code": "1-2",
    "lesson_title": "色彩的感觉",
    "duration_minutes": 40,
    "initial_teaching_judgment": [
        "学生知道很多颜色，也会说喜欢或不喜欢。",
        "但他们未必能把颜色、情绪、生活场景和作品表达联系起来。",
        "本课目标不是只认识冷暖色，而是让学生能说出颜色带来的感受，并尝试用色彩表达心情或场景。",
    ],
    "available_resource_candidates": [
        "色彩单元课标摘要",
        "教材图例",
        "冷暖色图片素材",
        "优秀课例《色彩的感觉》",
        "美术评价量规维度：色彩、创意、过程性评价",
    ],
}

BOUNDARY_FLAGS = {
    "teacher_review_required": True,
    "formal_apply_performed": False,
    "database_written": False,
    "memory_written": False,
    "feishu_written": False,
    "formal_export_created": False,
    "official_archive_created": False,
}

ALLOWED_IDS = {
    "section_id": [
        "basis",
        "analysis",
        "goals",
        "keypoints",
        "preparation",
        "teaching_process",
        "assessment",
        "reflection",
    ],
    "step_id": ["intro", "sense", "explore", "make", "share"],
    "affected_object": [
        "big_screen",
        "handout",
        "rubric",
        "resource_reference",
        "evidence_note",
        "teacher_action",
        "student_activity",
    ],
    "quality_gate_level": ["basic_usable", "ready_to_teach", "refined", "open_class_ready"],
}

REQUIRED_OUTPUT_SHAPE = {
    "lesson_design_mode": "",
    "intent_summary": "",
    "intent_classification": {
        "intent_type": "",
        "confidence": "high | medium | low",
        "reason": "",
    },
    "lesson_design_brief": {
        "core_learning_problem": "",
        "student_baseline": "",
        "target_shift": "",
        "unit_position": "",
        "curriculum_basis": [],
        "textbook_basis": [],
        "prior_learning_basis": [],
        "teacher_intent": "",
        "classroom_constraints": [],
        "resource_budget": "low | medium | high",
        "teaching_route": [],
        "evidence_plan": [],
        "risk_points": [],
        "next_best_questions": [],
    },
    "patch_target_resolution": [
        {
            "section_id": "",
            "step_id": "",
            "target_field": "",
            "reason": "",
        }
    ],
    "teaching_step_reasoning_updates": [
        {
            "step_id": "",
            "step_name": "",
            "duration": "",
            "step_role": "",
            "design_intent": "",
            "student_state_before": "",
            "student_state_after": "",
            "teacher_action": "",
            "student_action": "",
            "big_screen_state": "",
            "textbook_or_material_state": "",
            "learning_sheet_state": "",
            "assessment_evidence": "",
            "transition_from_previous": "",
            "transition_to_next": "",
            "risk_and_adjustment": "",
        }
    ],
    "field_patch_candidates": [
        {
            "field_patch_id": "",
            "target_section": "",
            "target_step_id": "",
            "target_field": "",
            "patch_type": "fill_missing | revise | restructure | add_example | simplify | enrich",
            "before_summary": "",
            "after_candidate": "",
            "reasoning_basis": [],
            "impact_scope": [],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        }
    ],
    "impact_scope": [
        {
            "affected_object": "big_screen | handout | rubric | resource_reference | evidence_note | teacher_action | student_activity",
            "impact_summary": "",
            "requires_teacher_confirmation": True,
        }
    ],
    "quality_gate_update": {
        "level": "basic_usable | ready_to_teach | refined | open_class_ready",
        "passed_items": [],
        "missing_items": [],
        "risk_items": [],
        "next_best_action": "",
    },
    "teacher_questions": [
        {
            "question": "",
            "why_needed": "",
            "options": [],
        }
    ],
    "ui_binding_hint": {
        "should_enter_edit_mode": True,
        "edit_target": "",
        "candidate_display_position": "",
        "right_tray_updates": [],
        "view_mode_summary": "",
    },
    "boundary_flags": dict(BOUNDARY_FLAGS),
}

HARD_RULES = [
    "只输出 JSON，不要 markdown，不要解释，不要代码块。",
    "不要生成整篇教案；只输出设计判断、字段补丁、影响范围、质量门和页面绑定提示。",
    "field_patch_candidates 必须映射到具体 section_id 或 step_id。",
    "teacher_review_required 必须为 true。",
    "formal_apply_performed、database_written、memory_written、feishu_written、formal_export_created、official_archive_created 必须为 false。",
    "教师可见内容要说人话，不要出现 schema、provider、database、memory、Feishu、formal_apply 等界面词。",
    "不要伪造真实学生档案；没有真实记录时标明为教学预设或小备推测。",
]

R1_COMPACT_OUTPUT_SHAPE = {
    "lesson_design_mode": "",
    "intent_summary": "",
    "lesson_design_brief_compact": {
        "core_learning_problem": "",
        "student_baseline": "",
        "target_shift": "",
        "teaching_route": [],
        "evidence_plan": [],
        "risk_points": [],
        "basis_summary": [],
    },
    "target_resolution": [
        {
            "section_id": "",
            "step_id": "",
            "target_field": "",
            "reason": "",
        }
    ],
    "step_reasoning_updates": [
        {
            "step_id": "",
            "step_name": "",
            "student_state_before": "",
            "student_state_after": "",
            "teacher_action": "",
            "student_action": "",
            "big_screen_state": "",
            "learning_sheet_state": "",
            "assessment_evidence": "",
            "risk_and_adjustment": "",
        }
    ],
    "field_patch_candidates": [
        {
            "field_patch_id": "",
            "target_section": "",
            "target_step_id": "",
            "target_field": "",
            "patch_type": "fill_missing | revise | restructure | add_example | simplify | enrich",
            "before_summary": "",
            "after_candidate": "",
            "reasoning_basis": [],
            "impact_scope": [],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        }
    ],
    "impact_scope": [
        {
            "affected_object": "big_screen | handout | rubric | resource_reference | evidence_note | teacher_action | student_activity",
            "impact_summary": "",
            "requires_teacher_confirmation": True,
        }
    ],
    "quality_gate_update": {
        "level": "basic_usable | ready_to_teach | refined | open_class_ready",
        "passed_items": [],
        "missing_items": [],
        "risk_items": [],
        "next_best_action": "",
    },
    "teacher_questions": [
        {
            "question": "",
            "why_needed": "",
            "options": [],
        }
    ],
    "ui_binding_hint": {
        "should_enter_edit_mode": True,
        "edit_target": "",
        "candidate_display_position": "",
        "right_tray_updates": [],
        "view_mode_summary": "",
    },
    "boundary_flags": dict(BOUNDARY_FLAGS),
}

R1_HARD_RULES = [
    "只输出一个 JSON 对象，不要 markdown，不要解释，不要代码块。",
    "输出 compact 结构，不要重写整篇教案。",
    "每个 field_patch_candidates 必须有 target_section 或 target_step_id，并且 teacher_review_required=true。",
    "即使是快速日常课，也必须至少输出 1 个 field_patch_candidates 和 1 个 impact_scope。",
    "lesson_design_brief_compact 必须包含 core_learning_problem、student_baseline、target_shift、teaching_route、evidence_plan。",
    "所有 boundary_flags 中的写入、应用、导出、归档必须为 false。",
    "所有字符串内部不要使用英文双引号，必须改用中文引号或省略引号，避免 JSON 断裂。",
    "没有真实学生档案时，依据写成教学预设、小备推测、教材、课标或资料候选，不要伪造长期记录。",
    "教师可见文字要自然简短，不要出现 schema、provider、database、memory、Feishu、formal_apply、field_patch。",
]


def parse_lesson_reasoning_output(
    raw_text: str,
    provider_meta: dict[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        payload, parser_meta = parse_patch_output(raw_text, provider_meta)
    except OutputParserError as exc:
        return None, {
            "parser_mode": "json_parse_error",
            "parse_subcode": exc.parse_subcode,
            "parse_error_code": exc.code,
            "parse_error_message": exc.message,
            "diagnostics": exc.diagnostics,
            "extraction_required": False,
        }
    if not isinstance(payload, dict):
        return None, {
            "parser_mode": "strict_json_parser",
            "parse_subcode": "non_object_json",
            "parse_error_code": "json_contract_error",
            "parse_error_message": "Provider output JSON must be an object.",
            "diagnostics": {},
            "extraction_required": False,
        }
    meta = dict(parser_meta or {})
    meta["extraction_required"] = bool(meta.get("provider_output_sanitized"))
    return payload, meta


def validate_lesson_reasoning_payload(parsed: dict[str, Any] | None) -> list[str]:
    if not isinstance(parsed, dict):
        return ["parsed_result_not_object"]
    errors: list[str] = []
    required_keys = [
        "lesson_design_mode",
        "intent_summary",
        "intent_classification",
        "lesson_design_brief",
        "patch_target_resolution",
        "teaching_step_reasoning_updates",
        "field_patch_candidates",
        "impact_scope",
        "quality_gate_update",
        "teacher_questions",
        "ui_binding_hint",
        "boundary_flags",
    ]
    for key in required_keys:
        if key not in parsed:
            errors.append(f"missing_{key}")

    brief = parsed.get("lesson_design_brief")
    if not isinstance(brief, dict):
        errors.append("lesson_design_brief_not_object")
    else:
        for key in ["core_learning_problem", "student_baseline", "target_shift", "teaching_route", "evidence_plan"]:
            if not brief.get(key):
                errors.append(f"lesson_design_brief_missing_{key}")

    patches = parsed.get("field_patch_candidates")
    if not _is_non_empty_list(patches):
        errors.append("missing_field_patch_candidates")
    else:
        for index, patch in enumerate(patches):
            if not isinstance(patch, dict):
                errors.append(f"patch_{index}_not_object")
                continue
            if not patch.get("target_section") and not patch.get("target_step_id"):
                errors.append(f"patch_{index}_missing_target")
            if not patch.get("target_field"):
                errors.append(f"patch_{index}_missing_target_field")
            if patch.get("teacher_review_required") is not True:
                errors.append(f"patch_{index}_teacher_review_required_not_true")
            if patch.get("formal_apply_performed") is not False:
                errors.append(f"patch_{index}_formal_apply_not_false")

    step_updates = parsed.get("teaching_step_reasoning_updates")
    if not isinstance(step_updates, list):
        errors.append("teaching_step_reasoning_updates_not_list")
    elif step_updates:
        needed = [
            "student_state_before",
            "student_state_after",
            "teacher_action",
            "student_action",
            "big_screen_state",
            "learning_sheet_state",
            "assessment_evidence",
        ]
        for key in needed:
            if not any(isinstance(item, dict) and item.get(key) for item in step_updates):
                errors.append(f"step_updates_missing_{key}")

    impact = parsed.get("impact_scope")
    if not _is_non_empty_list(impact):
        errors.append("missing_impact_scope")

    gate = parsed.get("quality_gate_update")
    if not isinstance(gate, dict):
        errors.append("quality_gate_update_not_object")
    elif gate.get("level") not in {"basic_usable", "ready_to_teach", "refined", "open_class_ready"}:
        errors.append("quality_gate_level_invalid")

    boundary = parsed.get("boundary_flags") if isinstance(parsed.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("boundary_teacher_review_required_not_true")
    for key in [
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_export_created",
        "official_archive_created",
    ]:
        if boundary.get(key) is not False:
            errors.append(f"boundary_{key}_not_false")
    return errors


def validate_compact_lesson_reasoning_payload(parsed: dict[str, Any] | None) -> list[str]:
    if not isinstance(parsed, dict):
        return ["parsed_result_not_object"]
    errors: list[str] = []
    required_keys = [
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
    ]
    for key in required_keys:
        if key not in parsed:
            errors.append(f"missing_{key}")

    brief = parsed.get("lesson_design_brief_compact")
    if not isinstance(brief, dict):
        errors.append("lesson_design_brief_compact_not_object")
    else:
        for key in ["core_learning_problem", "student_baseline", "target_shift", "teaching_route", "evidence_plan"]:
            if not brief.get(key):
                errors.append(f"lesson_design_brief_compact_missing_{key}")

    targets = parsed.get("target_resolution")
    if not _is_non_empty_list(targets):
        errors.append("missing_target_resolution")
    else:
        for index, target in enumerate(targets):
            if not isinstance(target, dict):
                errors.append(f"target_{index}_not_object")
                continue
            if not target.get("section_id") and not target.get("step_id"):
                errors.append(f"target_{index}_missing_section_or_step")
            if not target.get("target_field"):
                errors.append(f"target_{index}_missing_target_field")

    _validate_patch_candidates(parsed.get("field_patch_candidates"), errors)
    _validate_step_updates(parsed.get("step_reasoning_updates"), errors, compact=True)
    _validate_impact_scope(parsed.get("impact_scope"), errors)
    _validate_quality_gate(parsed.get("quality_gate_update"), errors)
    _validate_boundary_flags(parsed.get("boundary_flags"), errors)
    return errors


def build_lesson_reasoning_request(case: dict[str, Any], source_context: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "task": "把教师自然语言意图转成课时设计推理字段补丁，验证模型是否稳定输出结构化 JSON。",
        "fixed_lesson_context": LESSON_CONTEXT,
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "case_expectation": case["expectation"],
        "source_context": source_context,
        "required_output_shape": REQUIRED_OUTPUT_SHAPE,
        "allowed_ids": ALLOWED_IDS,
        "hard_rules": HARD_RULES,
    }


def build_compact_lesson_reasoning_request(case: dict[str, Any], source_context: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": R1_STAGE_ID,
        "task": "把教师自然语言意图转成只读课时设计推理候选，验证模型能否稳定输出 compact JSON。",
        "fixed_lesson_context": LESSON_CONTEXT,
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "case_expectation": case.get("expectation") or [],
        "compact_source_context": source_context,
        "required_output_shape": R1_COMPACT_OUTPUT_SHAPE,
        "allowed_ids": ALLOWED_IDS,
        "hard_rules": R1_HARD_RULES,
    }


def normalize_compact_lesson_reasoning_payload(parsed: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(parsed, dict):
        return None
    brief = parsed.get("lesson_design_brief_compact") if isinstance(parsed.get("lesson_design_brief_compact"), dict) else {}
    normalized = dict(parsed)
    normalized["lesson_design_brief"] = {
        "core_learning_problem": brief.get("core_learning_problem") or "",
        "student_baseline": brief.get("student_baseline") or "",
        "target_shift": brief.get("target_shift") or "",
        "unit_position": brief.get("unit_position") or "三年级美术色彩单元 1-2《色彩的感觉》。",
        "curriculum_basis": brief.get("curriculum_basis") if isinstance(brief.get("curriculum_basis"), list) else [],
        "textbook_basis": brief.get("textbook_basis") if isinstance(brief.get("textbook_basis"), list) else [],
        "prior_learning_basis": brief.get("prior_learning_basis") if isinstance(brief.get("prior_learning_basis"), list) else [],
        "teacher_intent": parsed.get("intent_summary") or "",
        "classroom_constraints": brief.get("classroom_constraints") if isinstance(brief.get("classroom_constraints"), list) else ["40分钟一课时。"],
        "resource_budget": brief.get("resource_budget") or "medium",
        "teaching_route": brief.get("teaching_route") if isinstance(brief.get("teaching_route"), list) else [],
        "evidence_plan": brief.get("evidence_plan") if isinstance(brief.get("evidence_plan"), list) else [],
        "risk_points": brief.get("risk_points") if isinstance(brief.get("risk_points"), list) else [],
        "next_best_questions": brief.get("next_best_questions") if isinstance(brief.get("next_best_questions"), list) else [],
    }
    normalized["patch_target_resolution"] = parsed.get("target_resolution") if isinstance(parsed.get("target_resolution"), list) else []
    normalized["teaching_step_reasoning_updates"] = parsed.get("step_reasoning_updates") if isinstance(parsed.get("step_reasoning_updates"), list) else []
    return normalized


def _validate_patch_candidates(value: Any, errors: list[str]) -> None:
    if not _is_non_empty_list(value):
        errors.append("missing_field_patch_candidates")
        return
    for index, patch in enumerate(value):
        if not isinstance(patch, dict):
            errors.append(f"patch_{index}_not_object")
            continue
        if not patch.get("target_section") and not patch.get("target_step_id"):
            errors.append(f"patch_{index}_missing_target")
        if not patch.get("target_field"):
            errors.append(f"patch_{index}_missing_target_field")
        if patch.get("teacher_review_required") is not True:
            errors.append(f"patch_{index}_teacher_review_required_not_true")
        if patch.get("formal_apply_performed") is not False:
            errors.append(f"patch_{index}_formal_apply_not_false")


def _validate_step_updates(value: Any, errors: list[str], *, compact: bool = False) -> None:
    field_name = "step_reasoning_updates" if compact else "teaching_step_reasoning_updates"
    if not isinstance(value, list):
        errors.append(f"{field_name}_not_list")
        return
    if not value:
        return
    needed = [
        "student_state_before",
        "student_state_after",
        "teacher_action",
        "student_action",
        "big_screen_state",
        "learning_sheet_state",
        "assessment_evidence",
    ]
    for key in needed:
        if not any(isinstance(item, dict) and item.get(key) for item in value):
            errors.append(f"{field_name}_missing_{key}")


def _validate_impact_scope(value: Any, errors: list[str]) -> None:
    if not _is_non_empty_list(value):
        errors.append("missing_impact_scope")
        return
    allowed = set(ALLOWED_IDS["affected_object"])
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"impact_{index}_not_object")
            continue
        if item.get("affected_object") not in allowed:
            errors.append(f"impact_{index}_affected_object_invalid")
        if not item.get("impact_summary"):
            errors.append(f"impact_{index}_missing_summary")
        if item.get("requires_teacher_confirmation") is not True:
            errors.append(f"impact_{index}_confirmation_not_true")


def _validate_quality_gate(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("quality_gate_update_not_object")
    elif value.get("level") not in {"basic_usable", "ready_to_teach", "refined", "open_class_ready"}:
        errors.append("quality_gate_level_invalid")


def _validate_boundary_flags(value: Any, errors: list[str]) -> None:
    boundary = value if isinstance(value, dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("boundary_teacher_review_required_not_true")
    for key, expected in BOUNDARY_FLAGS.items():
        if key == "teacher_review_required":
            continue
        if boundary.get(key) is not expected:
            errors.append(f"boundary_{key}_not_false")


def _is_non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


UNFOLDING_EVENT_TYPES = {
    "experience_evoke",
    "analysis",
    "comparison",
    "demo",
    "practice",
    "discussion",
    "creation",
    "sharing",
    "assessment",
    "transition",
}

UNFOLDING_RESPONSE_TYPES = {"expected", "partial", "misconception", "off_focus", "silent"}
LESSON_POSITION_VALUES = {"unit_start", "unit_middle", "unit_end"}


def normalize_lesson_reasoning_wide_payload(raw_payload: dict[str, Any] | None) -> dict[str, Any] | None:
    """Normalize wide lesson-reasoning output into the R3 unfolding graph contract.

    This is a tolerance layer, not a pass gate. Callers must still validate the
    normalized result and keep raw parse failures out of usable candidates.
    """
    if not isinstance(raw_payload, dict):
        return None
    graph_input = raw_payload.get("lesson_unfolding_graph")
    graph = dict(graph_input) if isinstance(graph_input, dict) else {}
    compact_brief = raw_payload.get("lesson_design_brief_compact") if isinstance(raw_payload.get("lesson_design_brief_compact"), dict) else {}
    full_brief = raw_payload.get("lesson_design_brief") if isinstance(raw_payload.get("lesson_design_brief"), dict) else {}
    grounding_input = graph.get("cognitive_grounding") if isinstance(graph.get("cognitive_grounding"), dict) else {}
    constraints_input = graph.get("constraints") if isinstance(graph.get("constraints"), dict) else {}
    events = _normalize_classroom_events(raw_payload, graph)
    total_minutes = _coerce_number(
        constraints_input.get("total_duration_minutes")
        or raw_payload.get("duration_minutes")
        or LESSON_CONTEXT.get("duration_minutes")
        or 40,
        40.0,
    )
    time_balance = evaluate_time_balance(events, total_minutes)
    normalized_graph = {
        "lesson_design_mode": _text(
            graph.get("lesson_design_mode")
            or raw_payload.get("lesson_design_mode")
            or "standard_daily"
        ),
        "design_context": _object_or(
            graph.get("design_context"),
            {
                "grade": LESSON_CONTEXT.get("grade"),
                "subject": LESSON_CONTEXT.get("subject"),
                "unit": LESSON_CONTEXT.get("unit"),
                "lesson_code": LESSON_CONTEXT.get("lesson_code"),
                "lesson_title": LESSON_CONTEXT.get("lesson_title"),
            },
        ),
        "cognitive_grounding": {
            "core_learning_problem": _text(
                grounding_input.get("core_learning_problem")
                or compact_brief.get("core_learning_problem")
                or full_brief.get("core_learning_problem")
                or raw_payload.get("core_learning_problem")
            ),
            "student_baseline": _text(
                grounding_input.get("student_baseline")
                or compact_brief.get("student_baseline")
                or full_brief.get("student_baseline")
            ),
            "real_stuck_point": _text(
                grounding_input.get("real_stuck_point")
                or grounding_input.get("key_difficulty")
                or compact_brief.get("risk_points")
                or full_brief.get("risk_points")
            ),
            "target_shift": _text(
                grounding_input.get("target_shift")
                or compact_brief.get("target_shift")
                or full_brief.get("target_shift")
            ),
            "key_focus": _text(grounding_input.get("key_focus") or compact_brief.get("key_focus") or full_brief.get("key_focus")),
            "key_difficulty": _text(
                grounding_input.get("key_difficulty")
                or full_brief.get("keypoints")
                or "把直观感受转成可表达、可观察的学习证据。"
            ),
        },
        "constraints": {
            "total_duration_minutes": total_minutes,
            "resource_budget": _choice(
                constraints_input.get("resource_budget") or full_brief.get("resource_budget") or "medium",
                {"low", "medium", "high"},
                "medium",
            ),
            "class_condition": _text(constraints_input.get("class_condition") or "普通课堂"),
            "lesson_position": _choice(constraints_input.get("lesson_position") or "unit_middle", LESSON_POSITION_VALUES, "unit_middle"),
            "material_conditions": _list_of_text(constraints_input.get("material_conditions") or full_brief.get("classroom_constraints")),
        },
        "main_event_sequence": _main_event_sequence(events, graph),
        "classroom_events": events,
        "structure_rebalance_candidates": _list_of_objects(graph.get("structure_rebalance_candidates")) + time_balance.get("rebalance_candidates", []),
        "evidence_plan": _list_of_text(graph.get("evidence_plan") or compact_brief.get("evidence_plan") or full_brief.get("evidence_plan")),
        "lesson_position_connection": _object_or(
            graph.get("lesson_position_connection"),
            {
                "unit_start_entry": "",
                "unit_middle_next_lesson_connection": _text(graph.get("next_lesson_connection")),
                "unit_end_closure": _text(graph.get("closure_plan")),
            },
        ),
        "closure_plan": _text(graph.get("closure_plan") or raw_payload.get("closure_plan")),
        "next_lesson_connection": _text(graph.get("next_lesson_connection") or raw_payload.get("next_lesson_connection")),
        "quality_gate": _object_or(graph.get("quality_gate") or raw_payload.get("quality_gate_update"), {}),
        "time_balance": time_balance,
    }
    normalized = dict(raw_payload)
    normalized["lesson_unfolding_graph"] = normalized_graph
    normalized["classroom_events"] = events
    normalized["field_patch_candidates"] = _normalize_wide_patch_candidates(raw_payload)
    normalized["impact_scope"] = _normalize_wide_impact_scope(raw_payload)
    normalized["quality_gate_update"] = _object_or(raw_payload.get("quality_gate_update"), normalized_graph["quality_gate"])
    normalized["boundary_flags"] = dict(BOUNDARY_FLAGS)
    return normalized


def validate_lesson_unfolding_graph_payload(payload: dict[str, Any] | None) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    graph = payload.get("lesson_unfolding_graph")
    if not isinstance(graph, dict):
        return ["missing_lesson_unfolding_graph"]
    errors: list[str] = []
    grounding = graph.get("cognitive_grounding") if isinstance(graph.get("cognitive_grounding"), dict) else {}
    for key in ["core_learning_problem", "target_shift"]:
        if not _text(grounding.get(key)):
            errors.append(f"cognitive_grounding_missing_{key}")
    if not isinstance(graph.get("main_event_sequence"), list) or not graph.get("main_event_sequence"):
        errors.append("missing_main_event_sequence")
    events = graph.get("classroom_events")
    if not _is_non_empty_list(events):
        errors.append("missing_classroom_events")
    else:
        for index, event in enumerate(events):
            if not isinstance(event, dict):
                errors.append(f"event_{index}_not_object")
                continue
            for key in ["event_id", "event_name"]:
                if not _text(event.get(key)):
                    errors.append(f"event_{index}_missing_{key}")
            duration = event.get("duration") if isinstance(event.get("duration"), dict) else {}
            if _coerce_number(duration.get("recommended_minutes"), 0) <= 0:
                errors.append(f"event_{index}_missing_duration")
            execution = event.get("execution_view") if isinstance(event.get("execution_view"), dict) else {}
            if not _text(execution.get("core_question")) and not _text(execution.get("student_task")):
                errors.append(f"event_{index}_execution_view_too_empty")
            design = event.get("design_view") if isinstance(event.get("design_view"), dict) else {}
            for key in ["student_state_before", "student_state_after", "assessment_evidence"]:
                if not _text(design.get(key)):
                    errors.append(f"event_{index}_design_view_missing_{key}")
            if event.get("teacher_review_required") is not True:
                errors.append(f"event_{index}_teacher_review_required_not_true")
            if event.get("formal_apply_performed") is not False:
                errors.append(f"event_{index}_formal_apply_not_false")
    _validate_boundary_flags(payload.get("boundary_flags"), errors)
    return errors


def evaluate_time_balance(events_or_graph: Any, total_duration_minutes: float | int = 40) -> dict[str, Any]:
    events = _events_from_any(events_or_graph)
    target = _coerce_number(total_duration_minutes, 40.0)
    total = 0.0
    for event in events:
        duration = event.get("duration") if isinstance(event.get("duration"), dict) else {}
        total += _coerce_number(duration.get("recommended_minutes") or event.get("duration_minutes"), 0.0)
    over = max(0.0, total - target)
    under = max(0.0, target - total)
    tolerance = max(2.0, target * 0.05)
    passed = over <= tolerance and under <= tolerance
    candidates = []
    if over > tolerance and events:
        sorted_events = sorted(
            events,
            key=lambda item: _coerce_number((item.get("duration") or {}).get("recommended_minutes"), 0.0)
            if isinstance(item.get("duration"), dict)
            else _coerce_number(item.get("duration_minutes"), 0.0),
            reverse=True,
        )
        for event in sorted_events[:2]:
            candidates.append(
                {
                    "action": "compress",
                    "target_event_id": event.get("event_id") or "",
                    "reason": f"当前总时长超出约 {round(over, 1)} 分钟，优先压缩非核心展开或展示数量。",
                    "impact_chain": ["压缩后需要同步减少学生分享数量或学习单记录量。"],
                }
            )
    elif under > tolerance and events:
        candidates.append(
            {
                "action": "expand",
                "target_event_id": events[-1].get("event_id") or "",
                "reason": f"当前总时长少约 {round(under, 1)} 分钟，可增加表达、展示或反馈证据。",
                "impact_chain": ["扩展时优先补学生表达和评价证据，不增加无目的活动。"],
            }
        )
    return {
        "total_event_minutes": round(total, 2),
        "target_minutes": target,
        "over_time_minutes": round(over, 2),
        "under_time_minutes": round(under, 2),
        "time_balance_pass": passed,
        "rebalance_candidates": candidates,
    }


def evaluate_classroom_unfolding_effectiveness(payload: dict[str, Any] | None) -> dict[str, Any]:
    graph = payload.get("lesson_unfolding_graph") if isinstance(payload, dict) else None
    if not isinstance(graph, dict):
        return _effectiveness_result(False, ["missing_lesson_unfolding_graph"])
    events = graph.get("classroom_events") if isinstance(graph.get("classroom_events"), list) else []
    blockers = []
    if not events:
        blockers.append("missing_classroom_events")
    grounding = graph.get("cognitive_grounding") if isinstance(graph.get("cognitive_grounding"), dict) else {}
    if not _text(grounding.get("core_learning_problem")) or not _text(grounding.get("target_shift")):
        blockers.append("missing_core_learning_problem_or_target_shift")
    time_balance = graph.get("time_balance") if isinstance(graph.get("time_balance"), dict) else evaluate_time_balance(events, (graph.get("constraints") or {}).get("total_duration_minutes", 40))
    scores = {
        "resource_purpose_score": _score_resource_purpose(events),
        "attention_focus_score": _score_attention_focus(events),
        "teacher_guidance_score": _score_teacher_guidance(events),
        "student_response_prediction_score": _score_student_response_prediction(events),
        "scaffold_quality_score": _score_scaffold_quality(events),
        "collection_method_reasoning_score": _score_collection_method(events),
        "media_material_timing_score": _score_media_material_timing(events),
        "assessment_evidence_score": _score_assessment_evidence(events),
        "transition_script_score": _score_transition(events),
        "time_feasibility_score": 5 if time_balance.get("time_balance_pass") else 2,
        "age_appropriateness_score": _score_age_appropriateness(graph),
    }
    overall = round(sum(scores.values()) / len(scores), 2)
    issues = []
    for key, value in scores.items():
        if value < 3.8:
            issues.append(f"{key}_low")
    passed = (
        not blockers
        and overall >= 4.0
        and scores["resource_purpose_score"] >= 4.0
        and scores["teacher_guidance_score"] >= 4.0
        and scores["student_response_prediction_score"] >= 3.8
        and scores["assessment_evidence_score"] >= 3.8
        and scores["age_appropriateness_score"] >= 4.0
    )
    return {
        **scores,
        "overall_effectiveness_score": overall,
        "pass": passed,
        "blockers": blockers,
        "issues": issues,
        "time_balance": time_balance,
    }


def _effectiveness_result(passed: bool, blockers: list[str]) -> dict[str, Any]:
    return {
        "resource_purpose_score": 0,
        "attention_focus_score": 0,
        "teacher_guidance_score": 0,
        "student_response_prediction_score": 0,
        "scaffold_quality_score": 0,
        "collection_method_reasoning_score": 0,
        "media_material_timing_score": 0,
        "assessment_evidence_score": 0,
        "transition_script_score": 0,
        "time_feasibility_score": 0,
        "age_appropriateness_score": 0,
        "overall_effectiveness_score": 0,
        "pass": passed,
        "blockers": blockers,
        "issues": blockers,
    }


def _normalize_classroom_events(raw_payload: dict[str, Any], graph: dict[str, Any]) -> list[dict[str, Any]]:
    source = graph.get("classroom_events")
    if not isinstance(source, list):
        source = raw_payload.get("classroom_events")
    if not isinstance(source, list):
        source = raw_payload.get("teaching_step_reasoning") or raw_payload.get("step_reasoning_updates") or raw_payload.get("teaching_step_reasoning_updates")
    if not isinstance(source, list):
        route = graph.get("main_event_sequence") or raw_payload.get("teaching_route")
        source = route if isinstance(route, list) else []
    events: list[dict[str, Any]] = []
    for index, item in enumerate(source[:8]):
        event = item if isinstance(item, dict) else {"event_name": str(item)}
        events.append(_normalize_single_event(event, index))
    return events


def _normalize_single_event(event: dict[str, Any], index: int) -> dict[str, Any]:
    event_id = _text(event.get("event_id") or event.get("step_id") or f"E{index + 1}")
    event_name = _text(event.get("event_name") or event.get("step_name") or event.get("name") or f"课堂事件{index + 1}")
    duration_input = event.get("duration") if isinstance(event.get("duration"), dict) else {}
    recommended = _coerce_number(duration_input.get("recommended_minutes") or event.get("duration_minutes") or event.get("minutes"), 5.0)
    execution = event.get("execution_view") if isinstance(event.get("execution_view"), dict) else {}
    design = event.get("design_view") if isinstance(event.get("design_view"), dict) else {}
    resource = event.get("resource_use") if isinstance(event.get("resource_use"), dict) else event.get("resource_used") if isinstance(event.get("resource_used"), dict) else {}
    return {
        "event_id": event_id,
        "event_name": event_name,
        "duration": {
            "recommended_minutes": recommended,
            "min_minutes": _coerce_number(duration_input.get("min_minutes"), max(1.0, recommended - 2)),
            "max_minutes": _coerce_number(duration_input.get("max_minutes"), recommended + 2),
            "time_risk": _text(duration_input.get("time_risk") or event.get("time_risk")),
        },
        "execution_view": {
            "teacher_focus_cue": _text(execution.get("teacher_focus_cue") or event.get("teacher_focus_cue") or event.get("teacher_opening_prompt")),
            "core_question": _text(execution.get("core_question") or event.get("core_question")),
            "student_task": _text(execution.get("student_task") or event.get("student_observation_task") or event.get("student_action")),
            "teacher_summary_sentence": _text(execution.get("teacher_summary_sentence") or event.get("transition_script") or event.get("teacher_summary_sentence")),
        },
        "design_view": {
            "learning_purpose": _text(design.get("learning_purpose") or event.get("learning_purpose") or event.get("step_role")),
            "design_intent": _text(design.get("design_intent") or event.get("design_intent")),
            "student_state_before": _text(design.get("student_state_before") or event.get("student_state_before")),
            "student_state_after": _text(design.get("student_state_after") or event.get("student_state_after")),
            "teacher_action": _text(design.get("teacher_action") or event.get("teacher_action")),
            "student_action": _text(design.get("student_action") or event.get("student_action")),
            "big_screen_state": _text(design.get("big_screen_state") or event.get("big_screen_state")),
            "textbook_or_material_state": _text(design.get("textbook_or_material_state") or event.get("textbook_or_material_state")),
            "learning_sheet_state": _text(design.get("learning_sheet_state") or event.get("learning_sheet_state")),
            "assessment_evidence": _text(design.get("assessment_evidence") or event.get("assessment_evidence")),
            "transition_from_previous": _text(design.get("transition_from_previous") or event.get("transition_from_previous")),
            "transition_to_next": _text(design.get("transition_to_next") or event.get("transition_to_next") or event.get("transition_script")),
            "risk_and_adjustment": _text(design.get("risk_and_adjustment") or event.get("risk_and_adjustment")),
        },
        "student_response_model": _normalize_student_response_model(event.get("student_response_model") or event.get("student_possible_responses") or event.get("possible_reactions")),
        "resource_use": {
            "resource_type": _text(resource.get("resource_type") or resource.get("type") or event.get("resource_type")),
            "why_needed": _text(resource.get("why_needed") or resource.get("reason") or event.get("resource_reason")),
            "attention_focus": _text(resource.get("attention_focus") or event.get("attention_focus")),
            "fallback_if_unavailable": _text(resource.get("fallback_if_unavailable") or event.get("fallback_if_unavailable")),
        },
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def _normalize_student_response_model(value: Any) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    normalized = []
    for index, item in enumerate(items[:5]):
        if isinstance(item, dict):
            response_type = _choice(item.get("type") or item.get("response_type"), UNFOLDING_RESPONSE_TYPES, "partial")
            normalized.append(
                {
                    "type": response_type,
                    "student_response": _text(item.get("student_response") or item.get("response")),
                    "teacher_next_move": _text(item.get("teacher_next_move") or item.get("next_move")),
                    "scaffold": _text(item.get("scaffold")),
                }
            )
        elif _text(item):
            normalized.append(
                {
                    "type": "partial" if index else "expected",
                    "student_response": _text(item),
                    "teacher_next_move": "",
                    "scaffold": "",
                }
            )
    return normalized


def _normalize_wide_patch_candidates(raw_payload: dict[str, Any]) -> list[dict[str, Any]]:
    patches = raw_payload.get("field_patch_candidates") if isinstance(raw_payload.get("field_patch_candidates"), list) else []
    normalized = []
    for index, patch in enumerate(patches):
        if not isinstance(patch, dict):
            continue
        normalized.append(
            {
                "field_patch_id": _text(patch.get("field_patch_id") or f"r3-p{index + 1}"),
                "target_section": _text(patch.get("target_section") or patch.get("section_id") or patch.get("field") or "teaching_process"),
                "target_step_id": _text(patch.get("target_step_id") or patch.get("step_id") or patch.get("path")),
                "target_field": _text(patch.get("target_field") or patch.get("field_name") or "classroom_event"),
                "patch_type": _text(patch.get("patch_type") or "revise"),
                "before_summary": _text(patch.get("before_summary") or patch.get("current_value")),
                "after_candidate": _text(patch.get("after_candidate") or patch.get("patch") or patch.get("patch_value")),
                "reasoning_basis": _list_of_text(patch.get("reasoning_basis") or ["教师输入", "教学预设"]),
                "impact_scope": _list_of_text(patch.get("impact_scope")),
                "teacher_review_required": True,
                "formal_apply_performed": False,
            }
        )
    return normalized


def _normalize_wide_impact_scope(raw_payload: dict[str, Any]) -> list[dict[str, Any]]:
    impacts = raw_payload.get("impact_scope") if isinstance(raw_payload.get("impact_scope"), list) else []
    normalized = []
    for item in impacts:
        if isinstance(item, dict):
            normalized.append(
                {
                    "affected_object": _text(item.get("affected_object") or item.get("type") or "teacher_action"),
                    "impact_summary": _text(item.get("impact_summary") or item.get("content") or item.get("purpose")),
                    "requires_teacher_confirmation": True,
                }
            )
    return normalized


def _main_event_sequence(events: list[dict[str, Any]], graph: dict[str, Any]) -> list[str]:
    existing = graph.get("main_event_sequence")
    if isinstance(existing, list) and existing:
        return [_text(item.get("event_id") if isinstance(item, dict) else item) for item in existing if _text(item.get("event_id") if isinstance(item, dict) else item)]
    return [event.get("event_id") for event in events if event.get("event_id")]


def _events_from_any(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        graph = value.get("lesson_unfolding_graph") if isinstance(value.get("lesson_unfolding_graph"), dict) else value
        events = graph.get("classroom_events")
        return events if isinstance(events, list) else []
    return value if isinstance(value, list) else []


def _score_resource_purpose(events: list[dict[str, Any]]) -> int:
    if not events:
        return 0
    hits = 0
    for event in events:
        resource = event.get("resource_use") if isinstance(event.get("resource_use"), dict) else {}
        design = event.get("design_view") if isinstance(event.get("design_view"), dict) else {}
        if _text(resource.get("why_needed")) or _text(design.get("learning_purpose")):
            hits += 1
    return _score_ratio(hits, len(events))


def _score_attention_focus(events: list[dict[str, Any]]) -> int:
    return _score_event_fields(events, [("execution_view", "teacher_focus_cue"), ("resource_use", "attention_focus"), ("execution_view", "core_question")])


def _score_teacher_guidance(events: list[dict[str, Any]]) -> int:
    return _score_event_fields(events, [("execution_view", "teacher_focus_cue"), ("execution_view", "core_question"), ("design_view", "teacher_action")])


def _score_student_response_prediction(events: list[dict[str, Any]]) -> int:
    if not events:
        return 0
    hits = 0
    type_hits = set()
    for event in events:
        responses = event.get("student_response_model") if isinstance(event.get("student_response_model"), list) else []
        if responses:
            hits += 1
        for response in responses:
            if isinstance(response, dict):
                type_hits.add(response.get("type"))
    score = _score_ratio(hits, len(events))
    if {"off_focus", "silent", "misconception"} & type_hits:
        score = min(5, score + 1)
    return score


def _score_scaffold_quality(events: list[dict[str, Any]]) -> int:
    if not events:
        return 0
    hits = 0
    for event in events:
        responses = event.get("student_response_model") if isinstance(event.get("student_response_model"), list) else []
        design = event.get("design_view") if isinstance(event.get("design_view"), dict) else {}
        if any(isinstance(item, dict) and (_text(item.get("scaffold")) or _text(item.get("teacher_next_move"))) for item in responses) or _text(design.get("risk_and_adjustment")):
            hits += 1
    return _score_ratio(hits, len(events))


def _score_collection_method(events: list[dict[str, Any]]) -> int:
    if not events:
        return 0
    hits = 0
    for event in events:
        execution = event.get("execution_view") if isinstance(event.get("execution_view"), dict) else {}
        design = event.get("design_view") if isinstance(event.get("design_view"), dict) else {}
        if _text(execution.get("student_task")) and _text(design.get("assessment_evidence")):
            hits += 1
    return _score_ratio(hits, len(events))


def _score_media_material_timing(events: list[dict[str, Any]]) -> int:
    return _score_event_fields(events, [("design_view", "big_screen_state"), ("design_view", "textbook_or_material_state"), ("design_view", "learning_sheet_state")])


def _score_assessment_evidence(events: list[dict[str, Any]]) -> int:
    return _score_event_fields(events, [("design_view", "assessment_evidence")])


def _score_transition(events: list[dict[str, Any]]) -> int:
    return _score_event_fields(events, [("design_view", "transition_to_next"), ("execution_view", "teacher_summary_sentence")])


def _score_age_appropriateness(graph: dict[str, Any]) -> int:
    text = str(graph)
    score = 4
    if any(term in text for term in ["论文", "色彩心理学", "专业理论", "复杂模型", "大学"]):
        score -= 2
    if any(term in text for term in ["观察", "说一说", "画", "颜色", "感受", "同桌", "词卡", "三年级"]):
        score += 1
    return max(0, min(5, score))


def _score_event_fields(events: list[dict[str, Any]], fields: list[tuple[str, str]]) -> int:
    if not events:
        return 0
    hits = 0
    for event in events:
        if any(isinstance(event.get(group), dict) and _text(event[group].get(key)) for group, key in fields):
            hits += 1
    return _score_ratio(hits, len(events))


def _score_ratio(hits: int, total: int) -> int:
    if total <= 0:
        return 0
    ratio = hits / total
    if ratio >= 0.9:
        return 5
    if ratio >= 0.7:
        return 4
    if ratio >= 0.5:
        return 3
    if ratio > 0:
        return 2
    return 0


def _text(value: Any) -> str:
    if isinstance(value, list):
        return "；".join(_text(item) for item in value if _text(item))
    if isinstance(value, dict):
        return "；".join(f"{key}:{_text(item)}" for key, item in value.items() if _text(item))
    return str(value or "").strip()


def _list_of_text(value: Any) -> list[str]:
    if isinstance(value, list):
        return [_text(item) for item in value if _text(item)]
    if _text(value):
        return [_text(value)]
    return []


def _list_of_objects(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _object_or(value: Any, fallback: dict[str, Any]) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else dict(fallback)


def _choice(value: Any, allowed: set[str], fallback: str) -> str:
    text = _text(value)
    return text if text in allowed else fallback


def _coerce_number(value: Any, fallback: float) -> float:
    try:
        if value in {None, ""}:
            return fallback
        return float(value)
    except (TypeError, ValueError):
        return fallback
