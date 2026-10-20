# Don Universal Toolbox — Jarvis orchestration

This repository holds the reusable source implementation of Jarvis's ten logical roles and the bridge instructions Hermes uses to orchestrate them.

## What is included

- `jarvis_universal_tools/roles/`: source for Planner, Researcher, Architect, Executor, Verifier, Recovery, Completion, Reporter, Housekeeping, and the reserved/inactive Unrestricted.DSH slot.
- `jarvis_universal_tools/orchestrator.py`: creates a durable task-intake record and records workspace inspection. This is the start of a workflow, not a full autonomous task executor.
- `jarvis_universal_tools/tool_registry.json`: candidate source tools and the policy for evaluating them.
- `jarvis_universal_tools/tool_acquisition.py`: guarded source clone into a separate `vendor/` directory, requiring a registered candidate, reviewed license metadata, and a pinned ref. A clone is not installed or verified.
- `hermes-integration/SKILL.md`: operating contract for Hermes to use these role implementations and acquire a coding tool when needed.
- `tests/test_jarvis_roles.py`: standard-library tests.

## Flow

Don's explicit task → Planner/task record → Researcher/tool inventory → Architect chooses API, existing Hermes/MCP adapter, CLI, or justified source integration → Executor → independent verification → bounded recovery if needed → completion status and report → safe housekeeping.

The roles are responsibilities, not ten separate models. Hermes remains the main agent and invokes tools. Prefer a stable supported API where appropriate; use an existing Hermes/MCP interface or CLI when that is simpler and more reliable. Never force every tool through a custom API server.

## Missing coding tool behavior

For a task such as a 3D terminal, Hermes must first inspect available coding capabilities. If none is suitable, it must evaluate a registered source candidate (for example OpenHands) for license, exact release/commit, dependencies, compatibility, storage, RAM/CPU, and install/test strategy. It may then clone to an isolated `vendor/` path. It must not silently install arbitrary code or claim success before tests.

## Run the intake CLI

```bash
python -m jarvis_universal_tools --goal "Build a 3D terminal" --workspace .
python -m unittest discover -s tests -v
```

Use Python 3.11+ (the code uses standard-library features). The repository integration must be wired into Hermes's actual installed skill/tool paths and tested in the target runtime before it can be called production-ready.

## Status honesty

- **VERIFIED**: acceptance checks passed with evidence.
- **PARTIAL**: some work exists, but required checks are missing.
- **BLOCKED**: a required capability or permission is unavailable.
- **NOT RUN**: no test result exists.

**NO EVIDENCE = NOT DONE.** This source branch is an implementation candidate; creating files in GitHub does not activate them in a running Hermes gateway.
