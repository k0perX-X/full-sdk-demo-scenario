from __future__ import annotations

from typing import Any


def run(sdk, context: dict[str, Any]) -> dict[str, Any]:
    sdk.log("INFO", "Full SDK demo scenario started")

    task_description = str(context.get("task_description") or "hello world")
    planner_prompt = str(
        context.get("planner_prompt")
        or f"Return a short hello world response for this text: {task_description}"
    )
    critic_prompt = str(
        context.get("critic_prompt")
        or "Check that the answer is concise and safe. Return a short verdict."
    )
    cancel_prompt = str(
        context.get("cancel_prompt")
        or "Return a very short draft that could be cancelled before execution."
    )

    primary_result = sdk.generate(
        planner_prompt,
        model_type="planner",
        parameters={"temperature": 0},
    )

    critic_operation_id = sdk.start_generation(
        critic_prompt,
        model_type="critic",
        parameters={"temperature": 0},
    )
    critic_initial_status = sdk.get_operation_status(critic_operation_id)
    critic_final_status = sdk.wait_for_operation(critic_operation_id, timeout=30)

    cancelled_operation_id = sdk.start_generation(
        cancel_prompt,
        model_type="planner",
        parameters={"temperature": 0},
    )
    cancelled = sdk.cancel_operation(cancelled_operation_id)
    cancelled_status = sdk.get_operation_status(cancelled_operation_id)

    sdk.emit_metric(
        "demo_scenario_runs_total",
        1.0,
        tags={"scenario": "full-sdk-demo-scenario"},
    )
    sdk.log("INFO", "Full SDK demo scenario finished")

    return {
        "summary": "full sdk demo completed",
        "primary_result": primary_result,
        "critic_operation": {
            "operation_id": critic_operation_id,
            "initial_status": critic_initial_status,
            "final_status": critic_final_status,
        },
        "cancelled_operation": {
            "operation_id": cancelled_operation_id,
            "cancelled": cancelled,
            "status": cancelled_status,
        },
    }
