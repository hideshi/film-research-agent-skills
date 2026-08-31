# Film Research Agent Skills

映画を全部見る時間が取れないときや、特定の観点から再理解したいときに、作品本編、YouTube 解説、ブログ、批評、一次資料などから作品単体の理解を深める AI エージェント用スキル集です。

最初のスキル `film-research-briefing` は、単なる「あらすじ要約」ではなく、次を分離して記録します。

- 作品内で確認できる事実
- 制作者が実際に述べたこと
- 解説者・批評家による解釈
- 映像・音響などの形式と、作品から生まれる解釈
- 選択した主プロファイルと補助タグに応じた比較や問い
- 作品世界の証拠と現実世界の証拠を分ける `evidence_domain`

利用者が明示しない限り、過去の論文や既存の研究テーマには接続しません。

この構造は scholarly-agent-skills の Discovery / Grounding、文献マトリクス、リポジトリ内実体化、Claim–Evidence 対応を映画資料向けに翻案したものです。

## 主プロファイルと補助タグ

共通スキルはジャンル非依存です。利用者の問いに応じて主プロファイルを一つ選び、横断的な観点は必要最小限の補助タグとして加えます。ジャンル名だけでは自動決定しません。

| Primary profile | 主な用途 |
|---|---|
| `general` | プロット、形式、制作、受容、主要解釈を偏りなく整理 |
| `sf-futures` | 技術、社会システム、未来像、現在との比較 |
| `historical-reality` | 歴史・伝記・実話と作品上の省略、圧縮、改変 |
| `horror-affect` | 恐怖を生む映像、音響、物語、身体、怪物、観客経験 |
| `social-political` | 制度、権力、階級、ジェンダー、人種・民族、表象 |
| `adaptation-intermedia` | 原作・舞台・漫画・ゲーム・旧作からの翻案と媒体差 |
| `documentary-evidence` | ドキュメンタリーの証拠、編集、語り、外部事実との照合 |
| `form-style` | 撮影、画面構成、編集、色彩、音響、演技 |
| `industry-production` | 資金、労働、技術、検閲、配給などの制作・産業条件 |

| Auxiliary tag | 横断観点 |
|---|---|
| `ecology-environment` | 環境、生態系、気候、資源、非人間的主体 |
| `philosophy-ethics` | 人格、自由、責任、正義、知識、倫理的ジレンマ |
| `religion-myth` | 信仰、儀礼、聖典、宗教表象、神話的モチーフ |
| `queer-feminist` | ジェンダー、セクシュアリティ、身体、労働、視線 |
| `postcolonial` | 帝国、植民地主義、土地、移動、言語、資源支配 |
| `disability-representation` | 障害、病気、ケア、依存、アクセスの表象 |

複数ジャンルにまたがる作品でも、主目的が一般的なら `general` を使います。補助タグは通常0〜2個とし、独立した章を増やすのではなく、関連する分析節へ統合します。

## クイックスタート

Codex へスキルを認識させる例:

```bash
ln -s /home/ogoshi/repo/film-research-agent-skills/skills/ja/film-research-briefing \
  "${CODEX_HOME:-$HOME/.codex}/skills/film-research-briefing"
```

調査対象のリポジトリで、トピック用ディレクトリを作る例:

```bash
python3 skills/ja/film-research-briefing/scripts/init_topic.py \
  --root /path/to/research-repo \
  --topic-id terminator-skynet \
  --title "ターミネーターとスカイネット" \
  --profile sf-futures \
  --tag philosophy-ethics
```

エージェントへの依頼例:

```text
$film-research-briefing を使い、『ターミネーター』（1984年）を
sf-futures を主プロファイル、philosophy-ethics を補助タグとして、
5分で理解できる資料にしてください。全編ネタバレ可です。
スカイネットの設定と、作品から想像できる未来への問いを知りたいです。
作品事実と解説者の解釈は分けてください。
```

作成後の検査:

```bash
python3 skills/ja/film-research-briefing/scripts/check_grounding.py \
  /path/to/research-repo/docs/terminator-skynet
```

## 対応エージェント

共通ルールは `AGENTS.md` に集約しています。Cursor、Claude Code、Gemini
ベースのエージェント（Antigravity を含む想定）には、それぞれの入口ファイル
（`.cursorrules`、`CLAUDE.md`、`GEMINI.md`）を用意しています。入口ファイルは
正本を複製せず、`AGENTS.md` と `SKILL.md` を参照します。

Codex では `agents/openai.yaml` と `SKILL.md` を利用できます。エージェントが
入口ファイルを自動認識しない場合は、`AGENTS.md` と
`skills/ja/film-research-briefing/SKILL.md` を明示的に読み込ませてください。

## 現在の範囲

MVP は日本語の共通映画調査スキル、8つの専門主プロファイル、6つの補助タグ、調査ディレクトリ生成、出典ノート生成、Claim–Evidence 検査を提供します。YouTube やブログの取得・閲覧はエージェントのブラウザー機能を使い、自動字幕の一括ダウンロードやアクセス制限の回避は行いません。

## 開発

```bash
python3 -m unittest discover -s tests -v
python3 /home/ogoshi/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/ja/film-research-briefing
```

## 免責

本リポジトリは無保証の調査支援ツールです。要約、出典判定、作品解釈、現在との比較には誤りが残り得ます。重要な主張は作品本編と一次資料で利用者自身が確認してください。著作権、研究倫理、個人情報、サイト・API 規約の遵守は利用者の責任です。法律・医療・投資その他の専門助言を提供しません。詳細は [DISCLAIMER.md](DISCLAIMER.md) を参照してください。
