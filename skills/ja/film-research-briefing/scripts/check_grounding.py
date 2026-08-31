#!/usr/bin/env python3
"""Validate source notes and Claim ledgers for a film-research topic."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_FIELDS = {
    "source_id",
    "title",
    "url",
    "source_kind",
    "evidence_level",
    "evidence_domain",
    "creator",
    "published_at",
    "accessed_at",
    "grounding_status",
}
EVIDENCE_LEVELS = {
    "work-primary",
    "production-primary",
    "scholarly-secondary",
    "critical-secondary",
    "informal-discovery",
}
EVIDENCE_DOMAINS = {
    "fictional-work",
    "production-record",
    "critical-discourse",
    "real-world",
    "discovery-only",
}
GROUNDING_STATUSES = {"grounded", "metadata-only", "manual"}
CLAIM_TYPES = {
    "plot",
    "worldbuilding",
    "production",
    "creator-intent",
    "reception",
    "interpretation",
    "real-world-fact",
    "present-day-comparison",
    "future-question",
}
CLAIM_STATUSES = {"confirmed", "provisional", "attributed", "synthesis"}
SOURCE_ID_RE = re.compile(r"\bS[0-9]{3,}\b")


@dataclass(frozen=True)
class Source:
    source_id: str
    url: str
    evidence_level: str
    evidence_domain: str
    grounding_status: str
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", type=Path, help="docs/<topic-id> directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args()


def scalar(value: str) -> str:
    value = value.strip()
    if value.startswith(('"', "'")):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, str):
                return parsed
        except json.JSONDecodeError:
            return value.strip("'\"")
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = scalar(value)
    return {}


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def has_evidence_row(text: str) -> bool:
    in_section = False
    for line in text.splitlines():
        if line.strip() == "## Evidence anchors":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            return False
        if in_section and re.match(r"^\|\s*E[0-9]+\s*\|", line):
            return True
    return False


def load_sources(topic: Path, errors: list[str], warnings: list[str]) -> dict[str, Source]:
    notes_dir = topic / "sources" / "notes"
    sources: dict[str, Source] = {}
    if not notes_dir.is_dir():
        errors.append(f"missing source-notes directory: {notes_dir}")
        return sources

    for path in sorted(notes_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        missing = sorted(field for field in REQUIRED_FIELDS if not meta.get(field))
        if missing:
            errors.append(f"{path}: missing frontmatter fields: {', '.join(missing)}")
            continue

        source_id = meta["source_id"]
        if source_id in sources:
            errors.append(f"{path}: duplicate source_id {source_id}")
            continue
        if not SOURCE_ID_RE.fullmatch(source_id):
            errors.append(f"{path}: invalid source_id {source_id}")
        if path.stem != source_id:
            errors.append(f"{path}: filename must match source_id {source_id}.md")
        if not is_http_url(meta["url"]):
            errors.append(f"{path}: url must be an absolute http(s) URL")
        if meta["evidence_level"] not in EVIDENCE_LEVELS:
            errors.append(f"{path}: unknown evidence_level {meta['evidence_level']}")
        if meta["evidence_domain"] not in EVIDENCE_DOMAINS:
            errors.append(f"{path}: unknown evidence_domain {meta['evidence_domain']}")
        if meta["grounding_status"] not in GROUNDING_STATUSES:
            errors.append(f"{path}: unknown grounding_status {meta['grounding_status']}")
        if meta["grounding_status"] in {"grounded", "manual"} and not has_evidence_row(text):
            errors.append(f"{path}: {meta['grounding_status']} note has no Evidence anchor row")
        if meta["evidence_level"] == "informal-discovery" and meta["grounding_status"] != "metadata-only":
            warnings.append(f"{path}: informal-discovery should not support confirmed claims")

        sources[source_id] = Source(
            source_id=source_id,
            url=meta["url"],
            evidence_level=meta["evidence_level"],
            evidence_domain=meta["evidence_domain"],
            grounding_status=meta["grounding_status"],
            path=path,
        )
    return sources


def table_rows_after_heading(text: str, heading: str) -> list[list[str]]:
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        return []

    rows: list[list[str]] = []
    seen_table = False
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if not stripped and not seen_table:
            continue
        if not stripped.startswith("|"):
            if seen_table:
                break
            continue
        seen_table = True
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0] == "Claim ID" or all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def validate_claims(
    briefing: Path,
    sources: dict[str, Source],
    errors: list[str],
    warnings: list[str],
) -> None:
    text = briefing.read_text(encoding="utf-8")
    rows = table_rows_after_heading(text, "## Claim ledger")
    if not rows:
        errors.append(f"{briefing}: missing or empty Claim ledger")
        return

    seen_claims: set[str] = set()
    for index, row in enumerate(rows, start=1):
        label = f"{briefing}: Claim ledger row {index}"
        if len(row) != 5:
            errors.append(f"{label}: expected 5 columns, found {len(row)}")
            continue
        claim_id, claim_type, claim, source_cell, status = row
        if not re.fullmatch(r"C[0-9]{3,}", claim_id):
            errors.append(f"{label}: invalid Claim ID {claim_id}")
        if claim_id in seen_claims:
            errors.append(f"{label}: duplicate Claim ID {claim_id}")
        seen_claims.add(claim_id)
        if not claim:
            errors.append(f"{label}: empty claim")
        if claim_type not in CLAIM_TYPES:
            errors.append(f"{label}: unknown Type {claim_type}")
        if status not in CLAIM_STATUSES:
            errors.append(f"{label}: unknown Status {status}")

        referenced_ids = SOURCE_ID_RE.findall(source_cell)
        unknown = [source_id for source_id in referenced_ids if source_id not in sources]
        if unknown:
            errors.append(f"{label}: unknown Sources {', '.join(unknown)}")
        referenced = [sources[source_id] for source_id in referenced_ids if source_id in sources]

        if status in {"confirmed", "attributed"} and not referenced:
            errors.append(f"{label}: {status} claim requires at least one source")
        if status == "confirmed":
            unusable = [s.source_id for s in referenced if s.grounding_status == "metadata-only"]
            if unusable:
                errors.append(f"{label}: metadata-only Sources cannot confirm claims: {', '.join(unusable)}")
            informal = [s.source_id for s in referenced if s.evidence_level == "informal-discovery"]
            if informal:
                errors.append(f"{label}: informal-discovery Sources cannot confirm claims: {', '.join(informal)}")
            discovery = [s.source_id for s in referenced if s.evidence_domain == "discovery-only"]
            if discovery:
                errors.append(f"{label}: discovery-only Sources cannot confirm claims: {', '.join(discovery)}")

        if claim_type in {"plot", "worldbuilding"} and status == "confirmed":
            if not any(
                s.evidence_level == "work-primary" and s.evidence_domain == "fictional-work"
                for s in referenced
            ):
                errors.append(
                    f"{label}: confirmed {claim_type} claim requires a fictional-work/work-primary Source"
                )
        if claim_type == "production" and status == "confirmed":
            if not any(s.evidence_domain == "production-record" for s in referenced):
                errors.append(f"{label}: confirmed production claim requires a production-record Source")
        if claim_type == "creator-intent" and status == "confirmed":
            if not any(
                s.evidence_level == "production-primary" and s.evidence_domain == "production-record"
                for s in referenced
            ):
                errors.append(
                    f"{label}: confirmed creator-intent requires a production-record/production-primary Source"
                )
        if claim_type == "real-world-fact" and status == "confirmed":
            if not referenced or any(s.evidence_domain != "real-world" for s in referenced):
                errors.append(f"{label}: confirmed real-world-fact requires only real-world Sources")
        if claim_type == "interpretation" and status not in {"attributed", "synthesis"}:
            errors.append(f"{label}: interpretation must be attributed or synthesis")
        if claim_type in {"present-day-comparison", "future-question"} and status not in {
            "attributed",
            "synthesis",
        }:
            errors.append(f"{label}: {claim_type} must be attributed or synthesis")
        if claim_type == "present-day-comparison" and status == "synthesis":
            domains = {source.evidence_domain for source in referenced}
            if not {"fictional-work", "real-world"}.issubset(domains):
                errors.append(
                    f"{label}: present-day-comparison synthesis requires both fictional-work and real-world Sources"
                )
        if status == "provisional" and not referenced:
            warnings.append(f"{label}: source-free provisional claim should explain how it can be checked")


def validate(topic: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    topic = topic.resolve()
    if not topic.is_dir():
        return [f"topic directory does not exist: {topic}"], warnings

    sources = load_sources(topic, errors, warnings)
    briefings_dir = topic / "briefings"
    briefings = sorted(briefings_dir.glob("*.md")) if briefings_dir.is_dir() else []
    if not briefings:
        warnings.append(f"no briefing files found in {briefings_dir}")
    for briefing in briefings:
        validate_claims(briefing, sources, errors, warnings)
    return errors, warnings


def main() -> int:
    args = parse_args()
    errors, warnings = validate(args.topic)
    for message in warnings:
        print(f"WARN: {message}")
    for message in errors:
        print(f"FAIL: {message}")
    if errors or (args.strict and warnings):
        print(f"RESULT: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    print(f"RESULT: PASS ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
