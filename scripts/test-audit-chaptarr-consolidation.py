import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("audit-chaptarr-consolidation.py")
SPEC = importlib.util.spec_from_file_location("audit_chaptarr_consolidation", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class UniqueBasenameCandidateTests(unittest.TestCase):
    def test_returns_the_only_target_with_the_same_basename(self) -> None:
        candidates = {"DiagnosticsReporter.cs": ["src/Chaptarr.Diagnostics/DiagnosticsReporter.cs"]}

        self.assertEqual(
            AUDIT.unique_basename_candidate(
                "src/Bookshelf.Diagnostics/DiagnosticsReporter.cs", candidates
            ),
            "src/Chaptarr.Diagnostics/DiagnosticsReporter.cs",
        )

    def test_returns_no_candidate_when_basename_is_absent(self) -> None:
        self.assertIsNone(AUDIT.unique_basename_candidate("src/Old/OnlyHere.cs", {}))

    def test_returns_no_candidate_when_basename_is_ambiguous(self) -> None:
        candidates = {
            "Fixture.cs": [
                "src/Chaptarr.Core.Test/Books/Fixture.cs",
                "src/Chaptarr.Core.Test/Import/Fixture.cs",
            ]
        }

        self.assertIsNone(
            AUDIT.unique_basename_candidate("src/Bookshelf.Core.Test/Fixture.cs", candidates)
        )


if __name__ == "__main__":
    unittest.main()
