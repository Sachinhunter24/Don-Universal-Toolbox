"""Role 1: turn an explicit user request into a bounded plan."""
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class TaskPlan:
    goal: str
    constraints: list[str]
    steps: list[str]
    acceptance_checks: list[str]
    needs_code_tool: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def plan_task(goal: str, constraints: list[str] | None = None) -> TaskPlan:
    goal = goal.strip()
    if not goal:
        raise ValueError("A user-assigned goal is required.")
    lowered = goal.lower()
    needs_code = any(x in lowered for x in ("build", "create", "implement", "code", "3d terminal", "website", "app", "repository"))
    return TaskPlan(
        goal=goal,
        constraints=list(constraints or []),
        steps=[
            "Inspect the current workspace, available tools, and existing project state.",
            "Choose a compatible execution tool; if a required capability is missing, evaluate a registered source tool.",
            "Execute in a dedicated worktree/branch and preserve existing user data.",
            "Run the narrowest relevant tests and inspect the resulting artifact.",
            "Report evidence, blockers, and the next concrete action."
        ],
        acceptance_checks=[
            "The requested artifact exists at a reported path.",
            "Relevant tests or validation checks pass, or are explicitly marked NOT RUN.",
            "Existing user data and unrelated source files remain unchanged.",
            "The final report distinguishes VERIFIED, PARTIAL, BLOCKED, and NOT RUN."
        ],
        needs_code_tool=needs_code
    )
