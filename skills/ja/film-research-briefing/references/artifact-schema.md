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

- `fictional-work`: 作品本編、脚本、公式予告・公式あらすじなど、作品世界についての証拠
- `production-record`: 制作者インタビュー、制作記録など、現実の制作過程についての証拠
- `critical-discourse`: 批評、論文、動画エッセイ、ブログなど、解釈や受容についての証拠
- `real-world`: 現実の技術・歴史・社会についての証拠
- `discovery-only`: 内容未確認で、候補発見にしか使えない資料

一つのページが複数ドメインの内容を含む場合は、利用目的ごとに出典ノートを分ける。`fictional-work` は「作品で何が描かれるか」を支えられるが、現実の技術能力や将来予測を支えられない。これは現実との比較を禁じる規則ではなく、比較を行う場合に現実側の資料を別途示し、論文で映画設定を事実として扱わないための境界である。

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
| C001 | plot | 主張 | S001 | confirmed |
| C002 | interpretation | 論者Aは〜と読む | S002 | attributed |
| C003 | future-question | 作中設定から生まれる未来への問い | S001, S003 | synthesis |
```

Type は `plot`、`worldbuilding`、`production`、`creator-intent`、`reception`、`interpretation`、`real-world-fact`、`present-day-comparison`、`future-question`。Status は `confirmed`、`provisional`、`attributed`、`synthesis`。

Source ledger には各 ID、資料名、URL、evidence level、grounding status を一覧化する。ローカルノートへのリンクも付ける。
