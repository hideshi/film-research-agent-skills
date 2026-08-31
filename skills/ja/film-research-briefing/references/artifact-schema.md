# 成果物スキーマ

## ディレクトリ

```text
docs/<topic-id>/
|-- design/
|   `-- viewing-lens.md
|-- sources/
|   |-- source-matrix.md
|   `-- notes/
|       `-- <source-id>.md
`-- briefings/
    `-- <work-id>.md
```

`source-matrix.md` は発見索引であり、内容主張の根拠ではない。根拠は `sources/notes/*.md` の grounded ノートである。

## 視聴・理解のレンズ

`design/viewing-lens.md` に主プロファイルを一つ、補助タグを0個以上記録する。主プロファイルはブリーフィングの中心的な問いと構成を決め、補助タグは適用する場面・論点だけを横断的に補う。補助タグを使う場合は、選択理由と適用範囲を記録する。

## 出典ノート

frontmatter の必須項目:

```yaml
source_id: S001
title: 資料名
url: https://example.com/source
source_kind: video-essay
evidence_level: critical-secondary
evidence_domain: critical-discourse
creator: 作成者名
published_at: 2026-01-01
accessed_at: 2026-08-31
grounding_status: grounded
```

`grounding_status`:

- `grounded`: 本文・映像・音声・字幕など内容を確認済み
- `metadata-only`: 書誌・ページ情報しか確認できず、内容主張には使えない
- `manual`: 利用者が提供したメモ・書き抜き。位置情報と入手経路を明記する

`evidence_domain`:

- `screen-work`: 対象となる映画・映像作品本編、公式字幕など、作品が提示する内容と形式についての証拠
- `source-work`: 翻案元の小説、戯曲、漫画、ゲーム、旧作など、比較する原資料についての証拠
- `production-record`: 制作者インタビュー、制作記録など、現実の制作過程についての証拠
- `critical-discourse`: 批評、論文、動画エッセイ、ブログなど、解釈や受容についての証拠
- `real-world`: 現実の技術・歴史・社会についての証拠
- `discovery-only`: 内容未確認で、候補発見にしか使えない資料

`fictional-work` は既存出典ノートとの互換性のため受理するが、新規ノートでは `screen-work` を使う。一つのページが複数ドメインの内容を含む場合は、利用目的ごとに出典ノートを分ける。`screen-work` は「作品が何を提示するか」を支えられるが、ドキュメンタリーを含め、現実世界で実際に起きたことを単独では確認できない。翻案比較には `source-work`、制作条件との比較には `production-record`、現実との比較には `real-world` の資料を別途示す。

本文には `## Evidence anchors` を置き、次の表を使う。

```markdown
| Evidence ID | Location | Observation / short excerpt | Kind | Notes |
|---|---|---|---|---|
| E1 | 12:34 | 忠実な要約または短い引用 | plot | 自動字幕は音声確認済み |
```

## ブリーフィングの Claim ledger

ブリーフィング末尾に次の見出し・列順で置く。検査スクリプトがこの表を読む。

```markdown
## Claim ledger

| Claim ID | Type | Claim | Sources | Status |
|---|---|---|---|---|
| C001 | depiction | 作品が提示する内容 | S001 | confirmed |
| C002 | interpretation | 論者Aは〜と読む | S002 | attributed |
| C003 | contextual-comparison | 作品と現実の比較 | S001, S003 | synthesis |
| C004 | inquiry | 作品から生まれる未決の問い | S001 | synthesis |
```

Type は `depiction`、`plot`、`worldbuilding`、`form`、`production`、`creator-intent`、`reception`、`interpretation`、`representation`、`real-world-fact`、`contextual-comparison`、`inquiry`。既存成果物の `present-day-comparison` と `future-question` も検査スクリプトは受理する。Status は `confirmed`、`provisional`、`attributed`、`synthesis`。

Source ledger には各 ID、資料名、URL、evidence level、grounding status を一覧化する。ローカルノートへのリンクも付ける。
