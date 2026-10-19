import importlib.util
import json
import subprocess
import tempfile
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


class ReviewedPathDecisionTests(unittest.TestCase):
    source = "a" * 40
    target = "b" * 40
    changed = {"src/Bookshelf/Old.cs", "src/Bookshelf/Removed.cs"}
    source_tree = {
        "src/Bookshelf/Old.cs": {"mode": "100644", "oid": "source-blob"},
        "src/Bookshelf/Removed.cs": {"mode": "100644", "oid": "removed-blob"},
    }
    target_tree = {
        "src/Chaptarr/New.cs": {"mode": "100644", "oid": "target-blob"},
    }

    def load(self, decisions):
        report = {
            "schemaVersion": 1,
            "sourceCommit": self.source,
            "targetCommit": self.target,
            "decisions": decisions,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review-map.json"
            path.write_text(json.dumps(report))
            return AUDIT.load_review_decisions(
                path,
                self.source,
                self.target,
                self.changed,
                self.source_tree,
                self.target_tree,
            )

    def test_accepts_reviewed_rename_with_evidence(self):
        decisions = self.load(
            [
                {
                    "sourcePath": "src/Bookshelf/Old.cs",
                    "decision": "map",
                    "targetPath": "src/Chaptarr/New.cs",
                    "reviewedBy": "maintainer",
                    "rationale": "The target implements the same responsibility.",
                    "evidence": "Reviewed source and target behavior; see PR #123.",
                }
            ]
        )

        self.assertEqual(
            decisions["src/Bookshelf/Old.cs"]["targetPath"], "src/Chaptarr/New.cs"
        )

    def test_rejects_stale_revision_pins(self):
        report = {
            "schemaVersion": 1,
            "sourceCommit": "c" * 40,
            "targetCommit": self.target,
            "decisions": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review-map.json"
            path.write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, "must match the pinned revisions"):
                AUDIT.load_review_decisions(
                    path, self.source, self.target, self.changed,
                    self.source_tree, self.target_tree
                )

    def test_rejects_mapping_to_missing_target(self):
        with self.assertRaisesRegex(ValueError, "missing from the pinned target tree"):
            self.load(
                [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "decision": "map",
                        "targetPath": "src/Chaptarr/DoesNotExist.cs",
                        "reviewedBy": "maintainer",
                        "rationale": "A reviewed mapping.",
                        "evidence": "Reviewed source and target.",
                    }
                ]
            )

    def test_retirement_requires_a_named_approval_reference(self):
        with self.assertRaisesRegex(ValueError, "requires approvalReference"):
            self.load(
                [
                    {
                        "sourcePath": "src/Bookshelf/Removed.cs",
                        "decision": "retire",
                        "approvedBy": "maintainer",
                        "rationale": "No longer supported.",
                        "evidence": "Feature review.",
                    }
                ]
            )

    def test_accepts_retirement_with_maintainer_approval_and_evidence(self):
        decisions = self.load(
            [
                {
                    "sourcePath": "src/Bookshelf/Removed.cs",
                    "decision": "retire",
                    "approvedBy": "maintainer",
                    "approvalReference": "issue #456",
                    "rationale": "The capability is no longer supported.",
                    "evidence": "Maintainer review confirmed no supported use remains.",
                }
            ]
        )

        self.assertEqual(
            decisions["src/Bookshelf/Removed.cs"]["decision"], "retire"
        )

    def test_rejects_duplicate_decisions_for_a_source_path(self):
        mapping = {
            "sourcePath": "src/Bookshelf/Old.cs",
            "decision": "map",
            "targetPath": "src/Chaptarr/New.cs",
            "reviewedBy": "maintainer",
            "rationale": "A reviewed mapping.",
            "evidence": "Reviewed source and target.",
        }
        with self.assertRaisesRegex(ValueError, "multiple decisions"):
            self.load([mapping, mapping])


class FileStateTests(unittest.TestCase):
    def test_reports_reviewed_path_mapping_as_a_comparison_not_equivalence(self):
        state = AUDIT.file_state(
            {"mode": "100644", "oid": "source"},
            {"mode": "100644", "oid": "target"},
            b"source implementation",
            b"target implementation",
        )

        self.assertEqual(state, "different-review-required")

    def test_only_normalizes_brand_and_line_endings(self):
        state = AUDIT.file_state(
            {"mode": "100644", "oid": "source"},
            {"mode": "100644", "oid": "target"},
            b"Readarr\r\n",
            b"Chaptarr\n",
        )

        self.assertEqual(state, "text-equivalent-after-brand-and-newline-normalization")


class AuditCliReviewDecisionTests(unittest.TestCase):
    def git(self, repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), *args]).decode().strip()

    def init_repo(self, path):
        path.mkdir()
        subprocess.run(["git", "init", "-q", str(path)], check=True)
        self.git(path, "config", "user.name", "Audit Test")
        self.git(path, "config", "user.email", "audit-test@example.invalid")

    def commit(self, repo, message):
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", message)
        return self.git(repo, "rev-parse", "HEAD")

    def run_audit(self, source, target, base, source_commit, target_commit, review_map, output):
        subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--bookshelf", str(source),
                "--chaptarr", str(target),
                "--source", source_commit,
                "--target", target_commit,
                "--fork-base", base,
                "--upstream", base,
                "--review-map", str(review_map),
                "--output", str(output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(output.read_text())

    def test_cli_records_reviewed_rename_without_claiming_equivalence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "bookshelf"
            target = root / "chaptarr"
            self.init_repo(source)
            self.init_repo(target)

            (source / "README.md").write_text("base\n")
            base = self.commit(source, "base")
            (source / "src/Bookshelf").mkdir(parents=True)
            (source / "src/Bookshelf/Old.cs").write_text("legacy implementation\n")
            source_commit = self.commit(source, "add legacy path")

            (target / "src/Chaptarr").mkdir(parents=True)
            (target / "src/Chaptarr/New.cs").write_text("replacement implementation\n")
            target_commit = self.commit(target, "add replacement path")

            review_map = root / "review-map.json"
            review_map.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "sourceCommit": source_commit,
                        "targetCommit": target_commit,
                        "decisions": [
                            {
                                "sourcePath": "src/Bookshelf/Old.cs",
                                "decision": "map",
                                "targetPath": "src/Chaptarr/New.cs",
                                "reviewedBy": "maintainer",
                                "rationale": "The target owns the same integration role.",
                                "evidence": "Reviewed implementation and focused tests.",
                            }
                        ],
                    }
                )
            )
            output = root / "inventory.json"
            inventory = self.run_audit(
                source, target, base, source_commit, target_commit, review_map, output
            )

            entry = next(
                row for row in inventory["files"]
                if row["sourcePath"] == "src/Bookshelf/Old.cs"
            )
            self.assertEqual(inventory["schemaVersion"], 3)
            self.assertEqual(inventory["counts"]["reviewedMappings"], 1)
            self.assertEqual(entry["targetPath"], "src/Chaptarr/New.cs")
            self.assertEqual(entry["state"], "different-review-required")
            self.assertEqual(entry["reviewedDecision"]["decision"], "map")

    def test_cli_records_explicit_approved_retirement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "bookshelf"
            target = root / "chaptarr"
            self.init_repo(source)
            self.init_repo(target)

            (source / "README.md").write_text("base\n")
            base = self.commit(source, "base")
            (source / "src/Bookshelf").mkdir(parents=True)
            (source / "src/Bookshelf/Removed.cs").write_text("retired source\n")
            source_commit = self.commit(source, "add legacy path")
            (target / "README.md").write_text("target\n")
            target_commit = self.commit(target, "target")

            review_map = root / "review-map.json"
            review_map.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "sourceCommit": source_commit,
                        "targetCommit": target_commit,
                        "decisions": [
                            {
                                "sourcePath": "src/Bookshelf/Removed.cs",
                                "decision": "retire",
                                "approvedBy": "maintainer",
                                "approvalReference": "issue #456",
                                "rationale": "The integration is no longer supported.",
                                "evidence": "Maintainer reviewed dependent workflows.",
                            }
                        ],
                    }
                )
            )
            output = root / "inventory.json"
            inventory = self.run_audit(
                source, target, base, source_commit, target_commit, review_map, output
            )

            entry = next(
                row for row in inventory["files"]
                if row["sourcePath"] == "src/Bookshelf/Removed.cs"
            )
            self.assertEqual(inventory["counts"]["approvedRetirements"], 1)
            self.assertEqual(entry["state"], "approved-retirement")
            self.assertIsNone(entry["targetPath"])
            self.assertEqual(entry["reviewedDecision"]["approvalReference"], "issue #456")


if __name__ == "__main__":
    unittest.main()
