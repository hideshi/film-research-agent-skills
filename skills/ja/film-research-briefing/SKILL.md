---
name: film-research-briefing
description: 映画・映像作品を短時間で深く理解するため、作品情報、解説、批評、一次資料を探索・実体化し、作品事実と解釈を分けた出典付きブリーフィングを作成する。問いに応じて主プロファイルと補助タグを選ぶ。
---

# 映画理解ブリーフィング

映画を未見または再視聴できない状況でも、作品内容、表現、制作情報、受容、解釈を混同せずに把握できる成果物を作る。既定目的は作品単体の理解であり、利用者が明示しない限り、過去の論文や研究プロジェクトへ接続しない。

## 基本原則

- 検索結果、タイトル、サムネイル、LLM の記憶は候補発見にのみ使う。内容上の主張は、開いた原資料を読んで出典ノートへ実体化してから書く。
- 作品内で確認できること、制作者の発言、批評者の解釈、調査者による統合を分離する。
- YouTube やブログは有用な二次資料になりうるが、その解釈を作品事実や制作者の意図へ昇格させない。
- 映画を見ていない場合は明記する。映像、編集、音響、演技、曖昧な場面を、あらすじ資料だけから確定しない。
- 保護を回避せず、URL、メタデータ、位置情報、必要最小限の短い証拠箇所、忠実な要約を保存する。取得できない資料は `metadata-only` とする。
- 成果物は無保証の調査支援である。重要な主張は利用者が作品本編と一次資料で確認する。

## 1. 調査条件、主プロファイル、補助タグを決める

作品名、公開年または版、ネタバレ許容度、利用可能時間、知りたいことを確認する。同名作品やリメイクがあれば対象を識別する。情報がなければ、全編ネタバレ可・5分で読める作品理解を既定値とし、その仮定を冒頭に示す。

利用者の問いに合う主プロファイルを一つ選ぶ。ジャンル名だけで自動決定せず、問いが一般的なら `general` とする。複数の主プロファイルを併用せず、横断的な観点は補助タグで加える。

- `general`: プロット、形式、制作、受容、主要解釈を偏りなく整理する。追加資料は不要。
- `sf-futures`: 技術、社会システム、未来像を扱う場合は [sf-futures.md](references/profiles/sf-futures.md) を読む。
- `historical-reality`: 歴史、伝記、実話との関係を扱う場合は [historical-reality.md](references/profiles/historical-reality.md) を読む。
- `horror-affect`: 恐怖の形式、身体、怪物、観客経験を扱う場合は [horror-affect.md](references/profiles/horror-affect.md) を読む。
- `social-political`: 制度、権力、社会集団、表象を扱う場合は [social-political.md](references/profiles/social-political.md) を読む。
- `adaptation-intermedia`: 原資料からの翻案と媒体差を扱う場合は [adaptation-intermedia.md](references/profiles/adaptation-intermedia.md) を読む。
- `documentary-evidence`: ドキュメンタリーの証拠、構成、現実との照合を扱う場合は [documentary-evidence.md](references/profiles/documentary-evidence.md) を読む。
- `form-style`: 映像、編集、音響、演技を詳しく扱う場合は [form-style.md](references/profiles/form-style.md) を読む。
- `industry-production`: 資金、労働、技術、検閲、配給などの制作条件を扱う場合は [industry-production.md](references/profiles/industry-production.md) を読む。

補助タグは必要な場合だけ選び、通常は0〜2個に留める。`ecology-environment`、`philosophy-ethics`、`religion-myth`、`queer-feminist`、`postcolonial`、`disability-representation` の意味と適用規則は、タグを一つでも使う場合にだけ [auxiliary-tags.md](references/auxiliary-tags.md) を読む。タグは主プロファイルの章立てを置き換えず、関連する節へ横断観点を加える。

必要なら調査ディレクトリを作る。

```bash
python3 <skill-dir>/scripts/init_topic.py \
  --root . --topic-id work-id --title "作品名" --profile general \
  --tag philosophy-ethics
```

## 2. 資料候補を探す

最低限、次の異なる経路を検討する。

1. 作品そのものに近い資料: 正規配信・上映、脚本、公式字幕、公式あらすじ
2. 制作の一次資料: 監督、脚本家、出演者のインタビュー、音声解説、制作資料
3. 研究・批評資料: 査読論文、書籍、映画機関、署名付き批評
4. 説明資料: 動画エッセイ、ブログ、百科事典
5. 選択した主プロファイルと補助タグが要求する原資料・現実世界側の資料

検索スニペットは根拠にしない。主張別の証拠要件は [source-policy.md](references/source-policy.md) を読む。

## 3. 原資料を出典ノートへ実体化する

採用する各資料の本文、字幕、トランスクリプト、映像または音声を実際に確認する。取得日、著者、公開日、URL、資料種別、グラウンディング状態、ページ・節・タイムコードを記録する。

```bash
python3 <skill-dir>/scripts/create_source_note.py \
  --topic docs/work-id --source-id S001 --title "資料タイトル" \
  --url "https://example.com/source" --source-kind review \
  --evidence-level critical-secondary --evidence-domain critical-discourse \
  --creator "作成者名" --grounding-status grounded
```

YouTube、ブログ、字幕を扱う場合は [web-source-acquisition.md](references/web-source-acquisition.md) を読む。全文転載はしない。

## 4. 主張を型付けして照合する

主張を `depiction`、`plot`、`worldbuilding`、`form`、`production`、`creator-intent`、`reception`、`interpretation`、`representation`、`real-world-fact`、`contextual-comparison`、`inquiry` のいずれかに分ける。`depiction` はフィクションかノンフィクションかを問わず、作品が画面・音声・字幕で提示する内容に使う。既存成果物との互換性のため `present-day-comparison` と `future-question` も受理するが、新規成果物では汎用型を使う。

- `confirmed`: 要件を満たす資料で確認できた
- `provisional`: 二次資料のみ、または資料間に未解決の差異がある
- `attributed`: 特定の論者による解釈として帰属を明記した
- `synthesis`: 複数資料から本調査で導いた整理、比較、問い。作品や論者の主張として書かない

出典の不一致は平均化せず、両論と未確定点を残す。各出典ノートに `evidence_domain` を付け、映像作品が提示する内容を現実の事実として扱わない。原資料との比較では `source-work`、制作条件との比較では `production-record`、現実との比較では `real-world` を映像作品側の `screen-work` と分ける。構造は [artifact-schema.md](references/artifact-schema.md) に従う。

## 5. 時間制約付きブリーフィングを書く

既定の成果物は `docs/<topic-id>/briefings/<work-id>.md` とし、次を含める。

1. 主プロファイル、補助タグと適用箇所、読了時間、ネタバレ範囲、本編確認状況
2. 30秒要約
3. 物語の因果鎖と結末
4. 登場人物・勢力・世界設定
5. 注目すべき映像、編集、音響、演技。ただし本編未確認なら省略または未確認とする
6. 中核テーマと代表的な解釈
7. 主プロファイル固有の分析と、関連節へ統合した補助タグの観点
8. 資料間の一致・不一致と未確認点
9. 本編を見るなら優先したい場面または論点
10. Claim ledger と Source ledger

主プロファイル固有の節は作品と問いに合わせ、該当しない項目を機械的に埋めない。補助タグごとの独立章を機械的に追加せず、選択理由と適用箇所を冒頭で示す。台帳は本文末尾に `Claim ledger`、`Source ledger` の順で置き、Source ledger の最後の行をファイル末尾とする。

## 6. 品質ゲートを通す

```bash
python3 <skill-dir>/scripts/check_grounding.py docs/<topic-id>
```

FAIL は出典ノートの追加、主張ステータスの弱化、帰属の明示で解消する。WARN は残せるが、ブリーフィングの限界・未確認点に転記する。

## 完了条件

- 各内容主張が Claim ledger から grounded な出典ノートへ追跡できる
- 作品事実、制作者の発言、他者の解釈、調査者の統合が明示的に分離されている
- 主プロファイル、補助タグ、各観点を適用した範囲が分かる
- 未見、未取得、自動字幕、版違いなどの限界が読者に見える
- 短時間で作品単体の要点を把握でき、必要なら本編や原資料へ戻れる
- 検査スクリプトが PASS（WARN がある場合は説明済み）
