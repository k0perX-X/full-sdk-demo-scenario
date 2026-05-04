from __future__ import annotations

from typing import Any


def run(sdk, context: dict[str, Any]) -> dict[str, Any]:
    sdk.log("INFO", "Full SDK demo scenario started")

    task_description = str(context.get("task_description") or "hello world")
    child_prompt = str(context.get("child_prompt") or "hello child request")
    cancel_prompt = str(context.get("cancel_prompt") or "hello cancelled request")

    primary_result = sdk.generate(
        f"Return a short hello world response for this text: {task_description}"
    )

    child_request_id = sdk.create_request(
        prompt=child_prompt,
        priority=5,
        parameters={"temperature": 0},
    )
    child_initial_status = sdk.get_request_status(child_request_id)
    child_final_status = sdk.wait_for_completion(child_request_id, timeout=30)

    cancelled_request_id = sdk.create_request(
        prompt=cancel_prompt,
        priority=1,
        parameters={"temperature": 0},
    )
    cancelled = sdk.cancel_request(cancelled_request_id)
    cancelled_status = sdk.get_request_status(cancelled_request_id)

    sdk.emit_metric(
        "demo_scenario_runs_total",
        1.0,
        tags={"scenario": "full-sdk-demo-scenario"},
    )
    sdk.log("INFO", "Full SDK demo scenario finished")

    return {
        "summary": "full sdk demo completed",
        "primary_result": primary_result,
        "child_request": {
            "request_id": child_request_id,
            "initial_status": child_initial_status,
            "final_status": child_final_status,
        },
        "cancelled_request": {
            "request_id": cancelled_request_id,
            "cancelled": cancelled,
            "status": cancelled_status,
        },
    }
