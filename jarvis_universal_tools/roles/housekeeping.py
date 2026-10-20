"""Role 9: clean only explicit temporary paths created by this task."""
from pathlib import Path

def validate_cleanup_targets(workspace: str, targets: list[str]) -> dict:
    root = Path(workspace).resolve()
    approved: list[str] = []
    rejected: list[dict[str, str]] = []
    protected_names = {".git", ".hermes", ".ssh", "state", "memory", "backups"}
    for raw in targets:
        target = (root / raw).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            rejected.append({"path": raw, "reason": "path escapes workspace"})
            continue
        if target == root or any(part in protected_names for part in target.parts):
            rejected.append({"path": raw, "reason": "protected or overly broad path"})
            continue
        approved.append(str(target))
    return {"approved": approved, "rejected": rejected,
            "note": "Validation only; deletion must be a separate explicit, logged operation."}
