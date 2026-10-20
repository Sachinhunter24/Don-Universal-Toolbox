"""Role 2: inspect evidence before selecting tools or dependencies."""
from pathlib import Path
from typing import Any

def inspect_workspace(root: str = ".") -> dict[str, Any]:
    base = Path(root).resolve()
    if not base.exists() or not base.is_dir():
        return {"status": "blocked", "reason": "workspace does not exist", "root": str(base)}
    names = sorted(p.name for p in base.iterdir() if p.name not in {".git", "__pycache__"})
    return {"status": "inspected", "root": str(base), "top_level_entries": names}

def evaluate_tool_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    required = ("name", "repository", "license", "integration")
    missing = [k for k in required if not candidate.get(k)]
    return {
        "name": candidate.get("name", "unknown"),
        "eligible_for_review": not missing,
        "missing_metadata": missing,
        "note": "Metadata completeness is not proof of compatibility; test the actual tool before adoption."
    }
