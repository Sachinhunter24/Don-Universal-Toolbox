"""Small, testable orchestration entry point for Hermes.

The host agent supplies actual model reasoning and registered execution adapters.
This module persists a task plan/report and detects when a coding tool is needed.
"""
from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .roles.planner import plan_task
from .roles.researcher import inspect_workspace
from .roles.unrestricted_dsh import status as dsh_status

def run_intake(goal: str, *, workspace: str = ".", constraints: list[str] | None = None,
               state_dir: str = ".jarvis/tasks") -> dict[str, Any]:
    root = Path(workspace).resolve()
    state = (root / state_dir).resolve()
    try:
        state.relative_to(root)
    except ValueError as exc:
        raise ValueError("Task state directory must stay inside the workspace.") from exc
    plan = plan_task(goal, constraints)
    inspection = inspect_workspace(str(root))
    task_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    record = {
        "task_id": task_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "planned",
        "goal": plan.goal,
        "constraints": plan.constraints,
        "plan": plan.to_dict(),
        "workspace_inspection": inspection,
        "roles": {"unrestricted_dsh": dsh_status()},
        "execution": {"status":"not_started", "reason":"Hermes must choose and invoke an available adapter."},
        "evidence": [],
        "warning": "Planning/intake is not task completion."
    }
    state.mkdir(parents=True, exist_ok=True)
    destination = state / f"{task_id}.json"
    destination.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    record["state_file"] = str(destination)
    return record
