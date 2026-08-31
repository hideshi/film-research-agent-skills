# 映画資料の史料批判ポリシー

## 1. 資料の階層

階層は資料全体の優劣ではなく、どの種類の主張を支えられるかを表す。

| Evidence level | 例 | 主に支えられる主張 | 主な限界 |
|---|---|---|---|
| `work-primary` | 対象映像作品、正規の脚本・字幕、翻案元の原資料 | 作品内容、台詞、画面・音響、原資料の内容 | 版違い、字幕・翻訳差、解釈は別問題 |
| `production-primary` | 制作者・出演者の直接インタビュー、音声解説、制作記録 | 制作経緯、本人が表明した意図 | 記憶違い、事後的説明、複数制作者間の差異 |
| `scholarly-secondary` | 査読論文、学術書、映画アーカイブの解説 | 概念化、歴史的位置づけ、受容 | 個別場面は原作品との照合が必要 |
| `critical-secondary` | 署名付き批評、動画エッセイ、専門誌、詳細ブログ | 解釈、論点の発見、プロットの補助確認 | 解釈を作品事実や制作者意図にしない |
| `informal-discovery` | 匿名まとめ、掲示板、短い反応、出典不明の百科記述 | 検索語、資料候補、論争点の発見 | 原則として確定主張を支えない |

YouTube やブログは媒体名だけで階層を決めない。作成者、根拠の提示、対象場面へのアンカー、訂正可能性、利益相反を見て `critical-secondary` または `informal-discovery` に分類する。大学講義や制作者本人の公式動画は、内容に応じて別の階層になりうる。

## 2. 主張と必要証拠

| Claim type | `confirmed` の最小条件 |
|---|---|
| `plot` | `work-primary` 1件。入手不能なら、独立した grounded 二次資料2件で `provisional` に留める |
| `depiction` | 対象映像作品の `screen-work` / `work-primary` 1件。作品が提示する内容を現実の事実へ昇格させない |
| `worldbuilding` | `work-primary` 1件。脚本と完成作品が異なる場合は、どの版の設定かを明記する |
| `form` | 作品本編で観察できる映像・編集・音響・演技。効果や意味の推定は `interpretation` に分ける |
| `production` | `production-primary` または `scholarly-secondary` 1件。伝聞なら `provisional` |
| `creator-intent` | 発言者を特定できる `production-primary` 1件。批評家による意図推定は `interpretation` |
| `reception` | 対象と範囲に合う `scholarly-secondary`、同時代資料、または複数の署名付き批評 |
| `interpretation` | 根拠資料を示し、論者へ帰属して `attributed`。調査者自身なら `synthesis` |
| `representation` | 対象場面または批評へ追跡し、論者へ帰属した `attributed` または調査者の `synthesis` |
| `real-world-fact` | `real-world` ドメインの資料。`screen-work` と `source-work` は使用不可 |
| `contextual-comparison` | `screen-work` と、比較対象に応じた `source-work`、`production-record`、`real-world` のいずれかを分けた `synthesis` |
| `inquiry` | 原則 `synthesis`。問いの起点となる作品上の根拠を示し、作品や論者の主張へ変換しない |

`present-day-comparison` と `future-question` は既存成果物との互換性のため受理する。新規成果物では、それぞれ `contextual-comparison` と `inquiry` を使う。

## 3. 独立性

複数資料が同じ第三資料を写している場合は一件と数える。動画が Wikipedia を読み上げ、ブログがその動画を要約しているような依存関係を記録する。独立性を確認できない場合は `provisional` とする。

## 4. 作品と外部資料の比較

作品を原資料または現実の技術、歴史、制度、社会状況と比較するときは、次を分ける。

1. 作品内で確認できる描写
2. 解説者が読み込んだ意味や意図
3. 比較する原資料または現実側の対象、概念、版、時点
4. 両者が対応する特徴
5. 対応しない特徴、描写不足、記録上の不確実性

比較は同一視や単純な正誤判定ではなく、類似と非類似が見えるように書く。具体的な観点と追加資料は、選択した主プロファイルと補助タグに従う。

## 5. 証拠ドメイン境界

- `screen-work` は `depiction`、`plot`、`worldbuilding`、直接観察できる `form` を支える。フィクションかノンフィクションかを問わず、現実世界の事実、制作史、制作者意図を単独では支えない。
- `source-work` は翻案元など原資料の内容を支える。対象映画の内容や現実世界の事実を支えない。
- `production-record` は `production` と `creator-intent` を支える。作品内で実際に描かれた内容の代用にはしない。
- `critical-discourse` は帰属付き `interpretation`、`representation`、受容を支える。解釈を作品内事実へ昇格させない。
- `real-world` は現実の技術・歴史・社会に関する主張を支える。作品との類似は別途 `synthesis` とする。
- `contextual-comparison` には、少なくとも `screen-work` と、比較対象に応じた `source-work`、`production-record`、`real-world` のいずれかを付ける。
- `fictional-work` は既存出典ノートとの互換性のため `screen-work` と同等に受理するが、新規ノートでは使わない。
- ページが複数の役割を持つ場合、同じ URL でも用途別に出典ノートを分ける。

## 6. 不一致の処理

- 版違い、字幕差、時系列差を最初に疑う。
- 一致しない資料を都合よく統合しない。
- 少数説でも作品理解に重要なら、提唱者と根拠を付けて残す。
- 解消できなければ Claim ledger を `provisional` にし、何を確認すれば確定できるかを書く。
