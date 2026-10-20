import tempfile
import unittest
from pathlib import Path

from jarvis_universal_tools.roles.planner import plan_task
from jarvis_universal_tools.roles.architect import choose_integration
from jarvis_universal_tools.roles.recovery import recovery_decision
from jarvis_universal_tools.roles.completion import completion_status
from jarvis_universal_tools.roles.housekeeping import validate_cleanup_targets
from jarvis_universal_tools.roles.unrestricted_dsh import status as dsh_status
from jarvis_universal_tools.orchestrator import run_intake

class RoleTests(unittest.TestCase):
    def test_planner_requires_explicit_goal(self):
        with self.assertRaises(ValueError):
            plan_task("  ")

    def test_planner_flags_coding_goal(self):
        self.assertTrue(plan_task("Build a 3D terminal").needs_code_tool)

    def test_integration_prefers_supported_api(self):
        self.assertEqual(choose_integration(has_supported_api=True, has_hermes_adapter=True, has_stable_cli=True), "api_adapter")

    def test_recovery_is_bounded(self):
        self.assertFalse(recovery_decision(attempts=2, max_attempts=2)["may_retry"])

    def test_completion_requires_evidence(self):
        self.assertEqual(completion_status([]), "blocked")
        self.assertEqual(completion_status([{"status":"passed"}]), "verified")
        self.assertEqual(completion_status([{"status":"not_run"}]), "partial")

    def test_cleanup_rejects_escape(self):
        with tempfile.TemporaryDirectory() as d:
            result = validate_cleanup_targets(d, ["../../important", "temp-output"])
            self.assertEqual(len(result["approved"]), 1)
            self.assertEqual(len(result["rejected"]), 1)

    def test_dsh_is_inactive(self):
        self.assertFalse(dsh_status()["active"])

    def test_intake_persists_plan(self):
        with tempfile.TemporaryDirectory() as d:
            record = run_intake("Build a 3D terminal", workspace=d)
            self.assertEqual(record["status"], "planned")
            self.assertTrue(Path(record["state_file"]).is_file())

if __name__ == "__main__":
    unittest.main()
