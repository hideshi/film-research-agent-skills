#!/usr/bin/env python3
"""Create a structured source note for a film-research topic."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


SOURCE_ID_RE = re.compile(r"^S[0-9]{3,}$")
SOURCE_KINDS = (
    "film",
    "source-work",
    "screenplay",
    "official-material",
    "creator-interview",
    "academic",
    "journalism",
    "review",
    "video-essay",
    "blog",
    "encyclopedia",
    "forum",
    "archive",
    "dataset",
)
EVIDENCE_LEVELS = (
    "work-primary",
    "production-primary",
    "scholarly-secondary",
    "critical-secondary",
    "informal-discovery",
)
EVIDENCE_DOMAINS = (
    "screen-work",
    "source-work",
    # Legacy domain retained for existing source notes.
    "fictional-work",
    "production-record",
    "critical-discourse",
    "real-world",
    "discovery-only",
)
GROUNDING_STATUSES = ("grounded", "metadata-only", "manual")


def yaml_string(value: str) -> str:
    """JSON strings are valid YAML scalars and avoid ambiguous punctuation."""
    return json.dumps(value, ensure_ascii=False)


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", type=Path, required=True, help="docs/<topic-id> directory")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-kind", choices=SOURCE_KINDS, required=True)
    parser.add_argument("--evidence-level", choices=EVIDENCE_LEVELS, required=True)
    parser.add_argument("--evidence-domain", choices=EVIDENCE_DOMAINS, required=True)
    parser.add_argument("--creator", default="unknown")
    parser.add_argument("--published-at", default="unknown")
    parser.add_argument("--accessed-at", default=dt.date.today().isoformat())
    parser.add_argument("--grounding-status", choices=GROUNDING_STATUSES, required=True)
    return parser.parse_args()


def create_note(args: argparse.Namespace) -> Path:
    if not SOURCE_ID_RE.fullmatch(args.source_id):
        raise ValueError("source-id must match S followed by at least three digits, e.g. S001")
    if not args.title.strip():
        raise ValueError("title must not be empty")
    if not valid_url(args.url):
        raise ValueError("url must be an absolute http(s) URL")

    topic = args.topic.resolve()
    if not topic.is_dir():
        raise FileNotFoundError(f"topic directory does not exist: {topic}")
    notes_dir = topic / "sources" / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    note_path = notes_dir / f"{args.source_id}.md"
    if note_path.exists():
        raise FileExistsError(f"refusing to overwrite existing note: {note_path}")

    content = f"""---
source_id: {yaml_string(args.source_id)}
title: {yaml_string(args.title.strip())}
url: {yaml_string(args.url)}
source_kind: {yaml_string(args.source_kind)}
evidence_level: {yaml_string(args.evidence_level)}
evidence_domain: {yaml_string(args.evidence_domain)}
creator: {yaml_string(args.creator.strip() or 'unknown')}
published_at: {yaml_string(args.published_at.strip() or 'unknown')}
accessed_at: {yaml_string(args.accessed_at)}
grounding_status: {yaml_string(args.grounding_status)}
---

# {args.source_id} — {args.title.strip()}

## 範囲と来歴

- 実際に確認した内容:
- トランスクリプト・字幕の状態:
- 対象作品・版:
- 他資料への依存:

## Evidence anchors

| Evidence ID | Location | Observation / short excerpt | Kind | Notes |
|---|---|---|---|---|

## 信頼性と限界

- 著者・話者の専門性:
- 資料内で提示された根拠:
- 利益相反・不確実性:
- 追加確認:
"""
    note_path.write_text(content, encoding="utf-8")
    return note_path


def main() -> int:
    args = parse_args()
    try:
        note_path = create_note(args)
    except (ValueError, FileNotFoundError, FileExistsError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Created source note: {note_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
