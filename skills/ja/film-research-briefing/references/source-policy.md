# 映画資料の史料批判ポリシー

## 1. 資料の階層

階層は資料全体の優劣ではなく、どの種類の主張を支えられるかを表す。

| Evidence level | 例 | 主に支えられる主張 | 主な限界 |
|---|---|---|---|
| `work-primary` | 作品本編、正規の脚本、公式字幕 | プロット、台詞、画面・音響の観察 | 版違い、字幕差、解釈は別問題 |
| `production-primary` | 制作者・出演者の直接インタビュー、音声解説、制作記録 | 制作経緯、本人が表明した意図 | 記憶違い、事後的説明、複数制作者間の差異 |
| `scholarly-secondary` | 査読論文、学術書、映画アーカイブの解説 | 概念化、歴史的位置づけ、受容 | 個別場面は原作品との照合が必要 |
| `critical-secondary` | 署名付き批評、動画エッセイ、専門誌、詳細ブログ | 解釈、論点の発見、プロットの補助確認 | 解釈を作品事実や制作者意図にしない |
| `informal-discovery` | 匿名まとめ、掲示板、短い反応、出典不明の百科記述 | 検索語、資料候補、論争点の発見 | 原則として確定主張を支えない |

YouTube やブログは媒体名だけで階層を決めない。作成者、根拠の提示、対象場面へのアンカー、訂正可能性、利益相反を見て `critical-secondary` または `informal-discovery` に分類する。大学講義や制作者本人の公式動画は、内容に応じて別の階層になりうる。

## 2. 主張と必要証拠

| Claim type | `confirmed` の最小条件 |
|---|---|
| `plot` | `work-primary` 1件。入手不能なら、独立した grounded 二次資料2件で `provisional` に留める |
| `worldbuilding` | `work-primary` 1件。脚本と完成作品が異なる場合は、どの版の設定かを明記する |
| `production` | `production-primary` または `scholarly-secondary` 1件。伝聞なら `provisional` |
| `creator-intent` | 発言者を特定できる `production-primary` 1件。批評家による意図推定は `interpretation` |
| `reception` | 対象と範囲に合う `scholarly-secondary`、同時代資料、または複数の署名付き批評 |
| `interpretation` | 根拠資料を示し、論者へ帰属して `attributed`。調査者自身なら `synthesis` |
| `real-world-fact` | `real-world` ドメインの資料。`fictional-work` は使用不可 |
| `present-day-comparison` | 作品側資料と現在についての信頼できる資料を分けて `synthesis`。比較時点を明記する |
| `future-question` | 原則 `synthesis`。問いの起点となる作中設定を示し、予測や作品の主張へ変換しない |

## 3. 独立性

複数資料が同じ第三資料を写している場合は一件と数える。動画が Wikipedia を読み上げ、ブログがその動画を要約しているような依存関係を記録する。独立性を確認できない場合は `provisional` とする。

## 4. 技術概念との比較と未来への想像

作品内の架空技術を現代の技術概念と比較するときは、次を分ける。

1. 作品内で明示される能力・制約
2. 解説者が読み込んだ能力・意図
3. 比較に使う現代の概念の意味
4. 両者が対応する特徴
5. 対応しない特徴、描写不足、時代差

`X is AGI` のような同一視より、`現在 AGI と呼ばれるものの特徴 a/b には対応するが c は描写されない` のように違いが見える書き方をする。ここから生まれる未来への問いは自由に広げてよいが、作品が明示した命題や現実の予測として帰属させない。

## 5. 証拠ドメイン境界

- `fictional-work` は `plot` と `worldbuilding` を支える。現実世界の事実、制作史、制作者意図を支えない。
- `production-record` は `production` と `creator-intent` を支える。作品内で実際に描かれた内容の代用にはしない。
- `critical-discourse` は帰属付き `interpretation` と受容を支える。解釈を作品内事実へ昇格させない。
- `real-world` は現実の技術・歴史・社会に関する主張を支える。作品との類似は別途 `synthesis` とする。
- `present-day-comparison` には、少なくとも `fictional-work` と `real-world` の双方を付ける。
- ページが複数の役割を持つ場合、同じ URL でも用途別に出典ノートを分ける。

## 6. 不一致の処理

- 版違い、字幕差、時系列差を最初に疑う。
- 一致しない資料を都合よく統合しない。
- 少数説でも作品理解に重要なら、提唱者と根拠を付けて残す。
- 解消できなければ Claim ledger を `provisional` にし、何を確認すれば確定できるかを書く。
