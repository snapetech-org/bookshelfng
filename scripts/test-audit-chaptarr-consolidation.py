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
                    "evidence": f"Reviewed source and target behavior at {self.target}; target blob target-blob; see PR #123.",
                }
            ]
        )

        self.assertEqual(
            decisions["src/Bookshelf/Old.cs"]["targetPath"], "src/Chaptarr/New.cs"
        )

    def test_rejects_mapping_evidence_without_current_target_blob(self):
        with self.assertRaisesRegex(ValueError, "pinned target blob"):
            self.load(
                [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "decision": "map",
                        "targetPath": "src/Chaptarr/New.cs",
                        "reviewedBy": "maintainer",
                        "rationale": "A reviewed mapping.",
                        "evidence": f"Reviewed at {self.target}; stale-blob.",
                    }
                ]
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
                    "evidence": f"Maintainer review at {self.target} confirmed no supported use remains.",
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
            "evidence": f"Reviewed source and target at {self.target}; target blob target-blob.",
        }
        with self.assertRaisesRegex(ValueError, "multiple decisions"):
            self.load([mapping, mapping])


class ReviewedFeatureDispositionTests(unittest.TestCase):
    source = "a" * 40
    target = "b" * 40
    changed = {"src/Bookshelf/Old.cs", "src/Bookshelf/Removed.cs"}
    target_tree = {
        "src/Chaptarr/New.cs": {"mode": "100644", "oid": "target-blob"},
    }

    def load(self, dispositions):
        report = {
            "schemaVersion": 1,
            "sourceCommit": self.source,
            "targetCommit": self.target,
            "dispositions": dispositions,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "disposition-map.json"
            path.write_text(json.dumps(report))
            return AUDIT.load_disposition_decisions(
                path, self.source, self.target, self.changed, self.target_tree
            )

    def test_accepts_reviewed_port_with_target_and_evidence(self):
        decisions = self.load(
            [
                {
                    "sourcePath": "src/Bookshelf/Old.cs",
                    "disposition": "ported",
                    "feature": "Bookshelf import workflow",
                    "targetPaths": ["src/Chaptarr/New.cs"],
                    "reviewedBy": "maintainer",
                    "rationale": "The behavior was ported into the target service.",
                    "evidence": f"Compared source and target at {self.target}; target blob target-blob. Focused regression tests cover the contract.",
                }
            ]
        )

        self.assertEqual(
            decisions["src/Bookshelf/Old.cs"]["disposition"], "ported"
        )

    def test_rejects_disposition_evidence_without_current_target_blob(self):
        with self.assertRaisesRegex(ValueError, "pinned target blob"):
            self.load(
                [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "disposition": "equivalent",
                        "feature": "Bookshelf import workflow",
                        "targetPaths": ["src/Chaptarr/New.cs"],
                        "reviewedBy": "maintainer",
                        "rationale": "The target is equivalent.",
                        "evidence": f"Reviewed at {self.target}; stale-blob.",
                    }
                ]
            )

    def test_rejects_disposition_target_missing_from_pinned_tree(self):
        with self.assertRaisesRegex(ValueError, "missing from the pinned target tree"):
            self.load(
                [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "disposition": "equivalent",
                        "feature": "Bookshelf import workflow",
                        "targetPaths": ["src/Chaptarr/Missing.cs"],
                        "reviewedBy": "maintainer",
                        "rationale": "The target is equivalent.",
                        "evidence": "Reviewed behavior and regression coverage.",
                    }
                ]
            )

    def test_rejects_stale_disposition_revision_pins(self):
        report = {
            "schemaVersion": 1,
            "sourceCommit": "c" * 40,
            "targetCommit": self.target,
            "dispositions": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "disposition-map.json"
            path.write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, "must match the pinned revisions"):
                AUDIT.load_disposition_decisions(
                    path, self.source, self.target, self.changed, self.target_tree
                )

    def test_retirement_requires_maintainer_approval_reference(self):
        with self.assertRaisesRegex(ValueError, "requires approvalReference"):
            self.load(
                [
                    {
                        "sourcePath": "src/Bookshelf/Removed.cs",
                        "disposition": "retired",
                        "feature": "Obsolete integration",
                        "approvedBy": "maintainer",
                        "rationale": "No supported use remains.",
                        "evidence": "Reviewed provider usage and migration behavior.",
                    }
                ]
            )

    def test_accepts_approved_retirement_with_evidence(self):
        decisions = self.load(
            [
                {
                    "sourcePath": "src/Bookshelf/Removed.cs",
                    "disposition": "retired",
                    "feature": "Obsolete integration",
                    "approvedBy": "maintainer",
                    "approvalReference": "issue #456",
                    "rationale": "No supported use remains.",
                    "evidence": f"Reviewed provider usage at {self.target} and migration behavior.",
                }
            ]
        )

        self.assertEqual(
            decisions["src/Bookshelf/Removed.cs"]["approvalReference"], "issue #456"
        )

    def test_rejects_duplicate_dispositions_for_a_source_path(self):
        disposition = {
            "sourcePath": "src/Bookshelf/Old.cs",
            "disposition": "ported",
            "feature": "Bookshelf import workflow",
            "targetPaths": ["src/Chaptarr/New.cs"],
            "reviewedBy": "maintainer",
            "rationale": "The behavior was ported into the target service.",
            "evidence": f"Compared source and target at {self.target}; target blob target-blob.",
        }

        with self.assertRaisesRegex(ValueError, "multiple decisions"):
            self.load([disposition, disposition])


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

    def test_ignores_csharp_comments_and_whitespace_but_keeps_literal_text(self):
        source = b'class A { string Name = "the same text"; /* source note */ int Count = 1; }'
        target = b'class A{string Name="the same text";// target note\nint Count=1;}'

        self.assertEqual(
            AUDIT.csharp_token_stream(source),
            AUDIT.csharp_token_stream(target),
        )
        self.assertNotEqual(
            AUDIT.csharp_token_stream(source, include_comments=True),
            AUDIT.csharp_token_stream(target, include_comments=True),
        )

    def test_csharp_token_stream_preserves_string_and_character_literals(self):
        self.assertNotEqual(
            AUDIT.csharp_token_stream(b'string value = "two words";'),
            AUDIT.csharp_token_stream(b'string value = "twowords";'),
        )
        self.assertNotEqual(
            AUDIT.csharp_token_stream(b"char value = 'a';"),
            AUDIT.csharp_token_stream(b"char value = 'b';"),
        )

    def test_csharp_token_stream_preserves_operator_boundaries(self):
        self.assertNotEqual(
            AUDIT.csharp_token_stream(b'int value = left + +right;'),
            AUDIT.csharp_token_stream(b'int value = left++right;'),
        )

    def test_csharp_token_stream_leaves_interpolated_and_raw_strings_unclassified(self):
        self.assertIsNone(AUDIT.csharp_token_stream(b'$"value {item}"'))
        self.assertIsNone(AUDIT.csharp_token_stream(b'"""raw value"""'))

    def test_reports_csharp_token_equivalence_as_a_file_state(self):
        state = AUDIT.file_state(
            {"mode": "100644", "oid": "source"},
            {"mode": "100644", "oid": "target"},
            b"class A { /* same note */ int Count = 1; }",
            b"class A{/* same\n note */int Count=1;}",
            "src/TagLibSharp/Audio.cs",
        )

        self.assertEqual(state, "code-equivalent-after-csharp-trivia-normalization")

    def test_different_csharp_comment_content_stays_for_review(self):
        state = AUDIT.file_state(
            {"mode": "100644", "oid": "source"},
            {"mode": "100644", "oid": "target"},
            b"class A { /* source note */ int Count = 1; }",
            b"class A { /* target note */ int Count = 1; }",
            "src/TagLibSharp/Audio.cs",
        )

        self.assertEqual(state, "different-review-required")


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

    def run_audit(
        self, source, target, base, source_commit, target_commit, review_map,
        output, disposition_map=None, require_complete_dispositions=False,
    ):
        command = [
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
        ]
        if disposition_map is not None:
            command.extend(["--disposition-map", str(disposition_map)])
        if require_complete_dispositions:
            command.append("--require-complete-dispositions")
        subprocess.run(
            command,
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
                                "evidence": f"Reviewed at {target_commit}; target blob {AUDIT.tree(target, target_commit)['src/Chaptarr/New.cs']['oid']}. Focused tests cover the contract.",
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
            self.assertEqual(inventory["schemaVersion"], 4)
            self.assertEqual(inventory["counts"]["reviewedMappings"], 1)
            self.assertEqual(inventory["counts"]["reviewedDispositions"], 0)
            self.assertEqual(inventory["counts"]["undispositionedPaths"], 1)
            self.assertEqual(
                inventory["counts"]["undispositionedFileStates"],
                {"different-review-required": 1},
            )
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
                                "evidence": f"Maintainer reviewed dependent workflows at target {target_commit}.",
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

    def test_cli_requires_a_complete_path_disposition_map_when_requested(self):
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
            review_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "decisions": [],
            }))
            disposition_map = root / "disposition-map.json"
            disposition_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "dispositions": [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "disposition": "ported",
                        "feature": "Bookshelf import workflow",
                        "targetPaths": ["src/Chaptarr/New.cs"],
                        "reviewedBy": "maintainer",
                        "rationale": "The behavior was ported into the target service.",
                        "evidence": f"Compared source and target at {target_commit}; target blob {AUDIT.tree(target, target_commit)['src/Chaptarr/New.cs']['oid']}. Focused regression tests cover the contract.",
                    }
                ],
            }))
            output = root / "inventory.json"
            inventory = self.run_audit(
                source, target, base, source_commit, target_commit,
                review_map, output, disposition_map,
                require_complete_dispositions=True,
            )

            entry = next(
                row for row in inventory["files"]
                if row["sourcePath"] == "src/Bookshelf/Old.cs"
            )
            self.assertEqual(inventory["counts"]["reviewedDispositions"], 1)
            self.assertEqual(inventory["counts"]["undispositionedPaths"], 0)
            self.assertEqual(
                entry["reviewedDisposition"]["disposition"], "ported"
            )

    def test_cli_rejects_incomplete_disposition_map_when_requested(self):
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
            (target / "README.md").write_text("target\n")
            target_commit = self.commit(target, "target")

            review_map = root / "review-map.json"
            review_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "decisions": [],
            }))
            disposition_map = root / "disposition-map.json"
            disposition_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "dispositions": [],
            }))
            output = root / "inventory.json"

            with self.assertRaises(subprocess.CalledProcessError) as error:
                self.run_audit(
                    source, target, base, source_commit, target_commit,
                    review_map, output, disposition_map,
                    require_complete_dispositions=True,
                )

            self.assertIn("1 changed paths have no disposition", error.exception.stderr)

    def test_cli_records_retired_disposition_as_approved_retirement(self):
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
            review_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "decisions": [],
            }))
            disposition_map = root / "disposition-map.json"
            disposition_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "dispositions": [
                    {
                        "sourcePath": "src/Bookshelf/Removed.cs",
                        "disposition": "retired",
                        "feature": "Obsolete integration",
                        "approvedBy": "maintainer",
                        "approvalReference": "issue #456",
                        "rationale": "No supported use remains.",
                        "evidence": f"Reviewed provider usage at target {target_commit} and migration behavior.",
                    }
                ],
            }))
            output = root / "inventory.json"
            inventory = self.run_audit(
                source, target, base, source_commit, target_commit,
                review_map, output, disposition_map,
            )

            entry = next(
                row for row in inventory["files"]
                if row["sourcePath"] == "src/Bookshelf/Removed.cs"
            )
            self.assertEqual(inventory["counts"]["approvedRetirements"], 1)
            self.assertEqual(entry["state"], "approved-retirement")
            self.assertIsNone(entry["targetPath"])
            self.assertEqual(
                entry["reviewedDisposition"]["approvalReference"], "issue #456"
            )

    def test_cli_rejects_conflicting_retirement_decisions(self):
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
            review_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "decisions": [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "decision": "map",
                        "targetPath": "src/Chaptarr/New.cs",
                        "reviewedBy": "maintainer",
                        "rationale": "The target path is mapped for comparison.",
                        "evidence": f"Reviewed the path relationship at {target_commit}; target blob {AUDIT.tree(target, target_commit)['src/Chaptarr/New.cs']['oid']}.",
                    }
                ],
            }))
            disposition_map = root / "disposition-map.json"
            disposition_map.write_text(json.dumps({
                "schemaVersion": 1,
                "sourceCommit": source_commit,
                "targetCommit": target_commit,
                "dispositions": [
                    {
                        "sourcePath": "src/Bookshelf/Old.cs",
                        "disposition": "retired",
                        "feature": "Obsolete integration",
                        "approvedBy": "maintainer",
                        "approvalReference": "issue #456",
                        "rationale": "No supported use remains.",
                        "evidence": f"Reviewed provider usage at target {target_commit} and migration behavior.",
                    }
                ],
            }))
            output = root / "inventory.json"

            with self.assertRaises(subprocess.CalledProcessError) as error:
                self.run_audit(
                    source, target, base, source_commit, target_commit,
                    review_map, output, disposition_map,
                )

            self.assertIn("disagree about retirement", error.exception.stderr)


if __name__ == "__main__":
    unittest.main()
