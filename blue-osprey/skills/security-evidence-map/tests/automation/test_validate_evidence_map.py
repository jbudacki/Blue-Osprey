#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


TEST_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = TEST_ROOT.parent.parent
SCRIPT = SKILL_ROOT / "scripts" / "validate_evidence_map.py"
SPEC = importlib.util.spec_from_file_location("validate_evidence_map", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class EvidenceMapAutomationTests(unittest.TestCase):
    def fixture(self, name: str) -> str:
        return (TEST_ROOT / "fixtures" / name).read_text(encoding="utf-8")

    def test_valid_map_passes_strict_local_reference_checks(self) -> None:
        issues, row_count = VALIDATOR.validate_markdown(
            self.fixture("valid-map.md"),
            repo_root=TEST_ROOT / "fixtures" / "repo",
            strict_local_references=True,
        )
        self.assertEqual(2, row_count)
        self.assertEqual([], issues)

    def test_invalid_map_reports_contract_errors(self) -> None:
        issues, row_count = VALIDATOR.validate_markdown(self.fixture("invalid-map.md"))
        self.assertEqual(3, row_count)
        codes = {issue.code for issue in issues}
        self.assertIn("duplicate-id", codes)
        self.assertIn("empty-cell", codes)
        self.assertIn("uncontrolled-status", codes)
        self.assertIn("confirmed-without-source", codes)
        self.assertIn("malformed-line-reference", codes)

    def test_out_of_range_local_line_is_an_error_in_strict_mode(self) -> None:
        issues, _ = VALIDATOR.validate_markdown(
            self.fixture("out-of-range-map.md"),
            repo_root=TEST_ROOT / "fixtures" / "repo",
            strict_local_references=True,
        )
        self.assertIn("line-out-of-range", {issue.code for issue in issues})
        self.assertTrue(any(issue.level == "error" for issue in issues))

    def test_missing_column_is_reported(self) -> None:
        markdown = self.fixture("valid-map.md").replace("| SOC evidence to collect ", "")
        issues, _ = VALIDATOR.validate_markdown(markdown)
        self.assertIn("missing-columns", {issue.code for issue in issues})

    def test_soc_corroboration_requires_operational_reference(self) -> None:
        markdown = self.fixture("valid-map.md").replace(
            "Confirmed in source — operationally unverified — open",
            "Confirmed in source — SOC corroborated — open",
            1,
        )
        issues, _ = VALIDATOR.validate_markdown(markdown)
        self.assertIn(
            "corroborated-without-operational-reference",
            {issue.code for issue in issues},
        )

    def test_json_cli_output_is_machine_readable(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(TEST_ROOT / "fixtures" / "valid-map.md"), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(2, payload["rowCount"])


if __name__ == "__main__":
    unittest.main()
