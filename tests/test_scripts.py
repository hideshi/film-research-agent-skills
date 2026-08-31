from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills" / "ja" / "film-research-briefing" / "scripts"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class InitTopicTests(unittest.TestCase):
    def test_initializes_expected_structure_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = run_script(
                "init_topic.py",
                "--root",
                str(root),
                "--topic-id",
                "terminator-skynet",
                "--title",
                "ターミネーターとスカイネット",
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            topic = root / "docs" / "terminator-skynet"
            self.assertTrue((topic / "design" / "viewing-lens.md").is_file())
            self.assertTrue((topic / "sources" / "source-matrix.md").is_file())
            self.assertTrue((topic / "sources" / "notes").is_dir())
            self.assertTrue((topic / "briefings").is_dir())

            second = run_script(
                "init_topic.py",
                "--root",
                str(root),
                "--topic-id",
                "terminator-skynet",
                "--title",
                "Do not overwrite",
            )
            self.assertEqual(second.returncode, 1)
            self.assertIn("refusing to overwrite", second.stderr)


class SourceNoteTests(unittest.TestCase):
    def test_creates_note_with_required_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "docs" / "topic"
            topic.mkdir(parents=True)
            result = run_script(
                "create_source_note.py",
                "--topic",
                str(topic),
                "--source-id",
                "S001",
                "--title",
                "Example video essay",
                "--url",
                "https://example.com/video",
                "--source-kind",
                "video-essay",
                "--evidence-level",
                "critical-secondary",
                "--evidence-domain",
                "critical-discourse",
                "--grounding-status",
                "metadata-only",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            note = topic / "sources" / "notes" / "S001.md"
            text = note.read_text(encoding="utf-8")
            self.assertIn('source_id: "S001"', text)
            self.assertIn('evidence_domain: "critical-discourse"', text)
            self.assertIn('grounding_status: "metadata-only"', text)

            duplicate = run_script(
                "create_source_note.py",
                "--topic",
                str(topic),
                "--source-id",
                "S001",
                "--title",
                "Replacement",
                "--url",
                "https://example.com/replacement",
                "--source-kind",
                "blog",
                "--evidence-level",
                "critical-secondary",
                "--evidence-domain",
                "critical-discourse",
                "--grounding-status",
                "metadata-only",
            )
            self.assertEqual(duplicate.returncode, 1)
            self.assertIn("refusing to overwrite", duplicate.stderr)


class GroundingGateTests(unittest.TestCase):
    def make_topic(self, root: Path) -> Path:
        topic = root / "docs" / "topic"
        (topic / "sources" / "notes").mkdir(parents=True)
        (topic / "briefings").mkdir(parents=True)
        return topic

    def write_note(
        self,
        topic: Path,
        source_id: str,
        evidence_level: str,
        grounding_status: str = "grounded",
        evidence_domain: str = "fictional-work",
    ) -> None:
        (topic / "sources" / "notes" / f"{source_id}.md").write_text(
            f"""---
source_id: "{source_id}"
title: "Source {source_id}"
url: "https://example.com/{source_id}"
source_kind: "film"
evidence_level: "{evidence_level}"
evidence_domain: "{evidence_domain}"
creator: "Example"
published_at: "1984-01-01"
accessed_at: "2026-08-31"
grounding_status: "{grounding_status}"
---

# Source

## Evidence anchors

| Evidence ID | Location | Observation / short excerpt | Kind | Notes |
|---|---|---|---|---|
| E1 | 00:10 | Observed event | plot | Test fixture |
""",
            encoding="utf-8",
        )

    def test_passes_traceable_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = self.make_topic(Path(temp))
            self.write_note(topic, "S001", "work-primary")
            self.write_note(topic, "S002", "critical-secondary", evidence_domain="critical-discourse")
            (topic / "briefings" / "film.md").write_text(
                """# Briefing

## Claim ledger

| Claim ID | Type | Claim | Sources | Status |
|---|---|---|---|---|
| C001 | plot | An observed plot event | S001 | confirmed |
| C002 | interpretation | Critic reads the event as a warning | S002 | attributed |
| C003 | future-question | A question invited by the fictional system | S001, S002 | synthesis |
""",
                encoding="utf-8",
            )
            result = run_script("check_grounding.py", str(topic))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("RESULT: PASS", result.stdout)

    def test_rejects_secondary_only_confirmed_plot_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = self.make_topic(Path(temp))
            self.write_note(topic, "S001", "critical-secondary")
            (topic / "briefings" / "film.md").write_text(
                """# Briefing

## Claim ledger

| Claim ID | Type | Claim | Sources | Status |
|---|---|---|---|---|
| C001 | plot | A plot event | S001 | confirmed |
""",
                encoding="utf-8",
            )
            result = run_script("check_grounding.py", str(topic))
            self.assertEqual(result.returncode, 1)
            self.assertIn("confirmed plot claim requires a fictional-work/work-primary Source", result.stdout)

    def test_rejects_metadata_only_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = self.make_topic(Path(temp))
            self.write_note(topic, "S001", "work-primary", "metadata-only")
            (topic / "briefings" / "film.md").write_text(
                """# Briefing

## Claim ledger

| Claim ID | Type | Claim | Sources | Status |
|---|---|---|---|---|
| C001 | plot | A plot event | S001 | confirmed |
""",
                encoding="utf-8",
            )
            result = run_script("check_grounding.py", str(topic))
            self.assertEqual(result.returncode, 1)
            self.assertIn("metadata-only Sources cannot confirm claims", result.stdout)

    def test_rejects_fiction_as_real_world_fact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = self.make_topic(Path(temp))
            self.write_note(topic, "S001", "work-primary", evidence_domain="fictional-work")
            (topic / "briefings" / "film.md").write_text(
                """# Briefing

## Claim ledger

| Claim ID | Type | Claim | Sources | Status |
|---|---|---|---|---|
| C001 | real-world-fact | Autonomous AI starts nuclear wars | S001 | confirmed |
""",
                encoding="utf-8",
            )
            result = run_script("check_grounding.py", str(topic))
            self.assertEqual(result.returncode, 1)
            self.assertIn("real-world-fact requires only real-world Sources", result.stdout)

    def test_present_day_comparison_requires_both_domains(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = self.make_topic(Path(temp))
            self.write_note(topic, "S001", "work-primary", evidence_domain="fictional-work")
            (topic / "briefings" / "film.md").write_text(
                """# Briefing

## Claim ledger

| Claim ID | Type | Claim | Sources | Status |
|---|---|---|---|---|
| C001 | present-day-comparison | The fictional system resembles current technology | S001 | synthesis |
""",
                encoding="utf-8",
            )
            result = run_script("check_grounding.py", str(topic))
            self.assertEqual(result.returncode, 1)
            self.assertIn("requires both fictional-work and real-world Sources", result.stdout)


if __name__ == "__main__":
    unittest.main()
