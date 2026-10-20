"""Role 4: execute only through explicitly registered tool adapters."""
from typing import Any, Callable

def execute_with_adapter(adapter: Callable[..., Any], *, goal: str, workspace: str,
                         config: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        result = adapter(goal=goal, workspace=workspace, config=config or {})
        return {"status": "executed", "result": result}
    except Exception as exc:
        return {"status": "failed", "error_type": type(exc).__name__, "error": str(exc)}
