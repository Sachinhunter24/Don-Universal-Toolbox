---
name: jarvis-universal-orchestrator
description: Use the Don Universal Toolbox ten-role orchestration code for assigned multi-step tasks, including acquiring a reviewed coding tool when Hermes lacks one.
---

# Hermes ↔ Jarvis Universal Tools

Hermes remains the LLM-driven agent and execution host. This skill connects its workflow to the reusable role implementations in Don-Universal-Toolbox.

## Required behavior

1. Only work on tasks explicitly assigned by Don.
2. Start with the repository/workspace state and available Hermes tools. Do not assume a coding tool, browser, API, or runtime exists until verified.
3. Use the Universal Toolbox intake CLI to persist a task plan:
   `python -m jarvis_universal_tools --goal "USER TASK" --workspace PATH`
4. Treat the returned status `planned` as intake only, not completion. Continue with Hermes reasoning and actual available tools.
5. If a coding capability is missing (example: Don asks for a 3D terminal), inspect registered candidates in `jarvis_universal_tools/tool_registry.json`. Evaluate official source, exact license/build options, dependencies, maintenance, resource requirements, and an immutable commit/release ref.
6. Only after a candidate is approved for that specific task, use `tool_acquisition.acquire_registered_tool` to clone its source into a separate `vendor/` subdirectory. A clone is not an installed or working tool. Review it in isolation, install only in an isolated environment, run its tests, then expose a narrow adapter.
7. Prefer a supported official API when stable and practical; otherwise reuse Hermes/MCP integrations or a documented CLI. Modify third-party source only when necessary and keep changes reversible.
8. Delegate logical roles to available Hermes capabilities; do not pretend ten separate agents are running when they are not. Role 10, Unrestricted.DSH, is reserved/inactive and never bypasses controls.
9. Run tests, inspect the output, save evidence/checkpoints, and report VERIFIED/PARTIAL/BLOCKED/NOT RUN.
10. Never claim a requested 3D terminal or other artifact is finished merely because a plan, source clone, or scaffold exists. Verify the rendered/running artifact against explicit acceptance checks.

## 3D terminal first-task acceptance checks

When Don assigns the 3D terminal task:
- inspect available UI/coding tools and current project state;
- if no suitable coding tool exists, evaluate a registered source tool and acquire it at a pinned commit only after license/resource review;
- build the terminal in a separate project branch/workspace;
- verify that it launches, renders the 3D scene, accepts input, and displays command output;
- test failure handling, resize behavior, and restart/reload;
- report the working URL/path and actual test evidence, or state the exact blocker.
