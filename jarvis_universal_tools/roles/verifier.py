"""Role 5: validate artifacts and test evidence independently."""
from pathlib import Path
from typing import Any

def verify_artifact(path: str, checks: list[str] | None = None) -> dict[str, Any]:
    artifact = Path(path)
    exists = artifact.exists()
    return {
        "status": "partial" if exists else "blocked",
        "artifact": str(artifact),
        "exists": exists,
        "is_file": artifact.is_file() if exists else False,
        "is_directory": artifact.is_dir() if exists else False,
        "checks_requested": list(checks or []),
        "warning": "Artifact existence alone does not prove quality or correctness."
    }

def summarize_test_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(r.get("status") == "passed" for r in results)
    failed = sum(r.get("status") == "failed" for r in results)
    not_run = sum(r.get("status") == "not_run" for r in results)
    return {"passed": passed, "failed": failed, "not_run": not_run,
            "status": "verified" if results and failed == 0 and not_run == 0 else "partial"}
