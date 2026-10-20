"""CLI: python -m jarvis_universal_tools --goal 'Build a 3D terminal'."""
import argparse
import json
from .orchestrator import run_intake

def main() -> int:
    parser = argparse.ArgumentParser(description="Create a persistent Jarvis task plan for Hermes to execute.")
    parser.add_argument("--goal", required=True, help="Explicit user-assigned task")
    parser.add_argument("--workspace", default=".", help="Existing project workspace")
    parser.add_argument("--constraint", action="append", default=[], help="Repeat for each constraint")
    args = parser.parse_args()
    try:
        record = run_intake(args.goal, workspace=args.workspace, constraints=args.constraint)
    except Exception as exc:
        print(json.dumps({"status":"blocked", "error_type":type(exc).__name__, "error":str(exc)}, indent=2))
        return 2
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
