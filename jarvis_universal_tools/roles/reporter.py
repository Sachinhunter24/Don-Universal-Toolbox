"""Role 8: concise, evidence-based completion report."""
def build_report(*, goal: str, status: str, changed_files: list[str] | None = None,
                 tests: list[dict] | None = None, artifacts: list[str] | None = None,
                 blockers: list[str] | None = None, next_action: str = "") -> dict:
    return {
        "goal": goal,
        "status": status.upper(),
        "changed_files": list(changed_files or []),
        "tests": list(tests or []),
        "artifacts": list(artifacts or []),
        "blockers": list(blockers or []),
        "next_action": next_action,
        "rule": "NO EVIDENCE = NOT DONE"
    }
