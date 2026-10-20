"""Guarded source acquisition for a missing tool.

This module does not install or run arbitrary code automatically. It requires a
registered candidate with a reviewed license and pinned ref, clones into a
dedicated vendor directory, and records the exact commit. Runtime use still
requires a separate install/test step by the execution environment.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse

def load_registry(path: str | Path | None = None) -> dict:
    registry_path = Path(path) if path else Path(__file__).with_name("tool_registry.json")
    return json.loads(registry_path.read_text(encoding="utf-8"))

def _run(args: list[str], *, cwd: str | Path | None = None) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True, timeout=900)
    return completed.stdout.strip()

def acquire_registered_tool(name: str, destination: str, *, pinned_ref: str,
                            workspace: str = ".", registry_path: str | None = None) -> dict:
    registry = load_registry(registry_path)
    candidate = next((t for t in registry.get("tools", []) if t.get("name") == name), None)
    if not candidate:
        raise ValueError(f"Tool is not in the reviewed registry: {name}")
    if not pinned_ref or pinned_ref in {"main", "master", "latest", "HEAD"}:
        raise ValueError("Provide an immutable commit SHA or a reviewed release tag; floating refs are not accepted.")
    if not candidate.get("license") or "verify" in candidate["license"].lower():
        raise ValueError("License/build configuration must be reviewed before cloning.")
    parsed = urlparse(candidate.get("repository", ""))
    if parsed.scheme != "https" or parsed.netloc != "github.com" or not parsed.path.endswith(".git"):
        raise ValueError("Only HTTPS GitHub repositories explicitly listed in the registry are allowed.")
    root = Path(workspace).resolve()
    vendor_root = (root / "vendor").resolve()
    target = (root / destination).resolve()
    if target == root or vendor_root not in target.parents:
        raise ValueError("Tool source must be cloned into a dedicated subdirectory under workspace/vendor/.")
    if target.exists():
        raise FileExistsError(f"Destination already exists; refusing to overwrite: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    _run(["git", "clone", "--no-checkout", "--filter=blob:none", candidate["repository"], str(target)])
    try:
        _run(["git", "checkout", "--detach", pinned_ref], cwd=target)
        commit = _run(["git", "rev-parse", "HEAD"], cwd=target)
        if len(commit) != 40:
            raise RuntimeError("Could not verify immutable commit SHA.")
        license_files = [p.name for p in target.iterdir() if p.is_file() and p.name.lower().startswith(("license", "copying"))]
        if not license_files:
            raise RuntimeError("No top-level LICENSE/COPYING file found; manual license review required.")
        return {"status":"cloned_not_installed", "name":name, "repository":candidate["repository"],
                "requested_ref":pinned_ref, "resolved_commit":commit, "license_files":license_files,
                "path":str(target), "next_step":"Review exact license/dependencies, then install and run tests in an isolated environment."}
    except Exception:
        # Preserve the failed checkout for diagnosis; never silently delete source.
        raise
