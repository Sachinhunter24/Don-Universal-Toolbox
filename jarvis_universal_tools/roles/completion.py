"""Role 7: decide status from evidence, never from intention."""
VALID = {"passed", "failed", "not_run"}
def completion_status(checks: list[dict]) -> str:
    if not checks:
        return "blocked"
    statuses = [c.get("status") for c in checks]
    if any(s not in VALID for s in statuses):
        return "partial"
    if "failed" in statuses:
        return "blocked"
    if "not_run" in statuses:
        return "partial"
    return "verified"
