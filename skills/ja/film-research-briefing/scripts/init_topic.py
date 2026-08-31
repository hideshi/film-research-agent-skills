#!/usr/bin/env python3
"""Create a film-research topic workspace without overwriting existing work."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TOPIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
PROFILES = {
    "general": "プロット、形式、制作、受容、主要解釈",
    "sf-futures": "技術・社会システム・未来像と現実との比較",
    "historical-reality": "作品内の構成と歴史・実話の記録との関係",
    "horror-affect": "恐怖を生む映像・音響・物語・表象",
    "social-political": "制度・権力・社会集団・表象",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Research repository root")
    parser.add_argument("--topic-id", required=True, help="Lowercase kebab-case identifier")
    parser.add_argument("--title", required=True, help="Human-readable research topic")
    parser.add_argument("--profile", choices=PROFILES, default="general", help="Analysis profile")
    return parser.parse_args()


def initialize(root: Path, topic_id: str, title: str, profile: str = "general") -> Path:
    if not TOPIC_ID_RE.fullmatch(topic_id):
        raise ValueError("topic-id must be lowercase kebab-case and at most 63 characters")
    if not title.strip():
        raise ValueError("title must not be empty")
    if profile not in PROFILES:
        raise ValueError(f"unknown profile: {profile}")

    topic_dir = root.resolve() / "docs" / topic_id
    if topic_dir.exists():
        raise FileExistsError(f"refusing to overwrite existing topic: {topic_dir}")

    design_dir = topic_dir / "design"
    notes_dir = topic_dir / "sources" / "notes"
    briefings_dir = topic_dir / "briefings"
    design_dir.mkdir(parents=True)
    notes_dir.mkdir(parents=True)
    briefings_dir.mkdir(parents=True)

    viewing_lens = f"""# 視聴・理解のレンズ — {title.strip()}

## 対象

- 作品・版:
- ネタバレ方針: 全編可
- 読了時間の目安: 5分
- 本編確認状況: 未記録
- 分析プロファイル: {profile}
- プロファイルの観点: {PROFILES[profile]}

## 知りたいこと

- この作品について何を最も理解したいか:
- 作品のどの側面に関心があるか:
- すでに知っていること、誤解かもしれないこと:

## 境界

- 本編による確認が必要な主張:
- 二次解説で把握できる主張:
- 結論を閉じずに残す問い:
- 過去の研究との接続: 明示依頼がない限り行わない
"""
    (design_dir / "viewing-lens.md").write_text(viewing_lens, encoding="utf-8")

    source_matrix = """# 資料マトリクス

> これは候補発見用の索引である。内容主張の根拠は `notes/*.md` に実体化する。

| Source ID | 資料候補 | 種別 | Evidence level | Evidence domain | Grounding status | 関連性 | 出典ノート |
|---|---|---|---|---|---|---|---|
"""
    (topic_dir / "sources" / "source-matrix.md").write_text(source_matrix, encoding="utf-8")

    return topic_dir


def main() -> int:
    args = parse_args()
    try:
        topic_dir = initialize(args.root, args.topic_id, args.title, args.profile)
    except (ValueError, FileExistsError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Created film briefing topic ({args.profile}): {topic_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
