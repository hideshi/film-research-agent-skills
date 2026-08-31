# SF Film Agent Skills

SF映画を全部見る時間が取れないときに、YouTube 解説、ブログ、批評などから作品単体の理解を深め、そこに描かれた未来への想像を広げるための AI エージェント用スキル集です。

最初のスキル `film-research-briefing` は、単なる「あらすじ要約」ではなく、次を分離して記録します。

- 作品内で確認できる事実
- 制作者が実際に述べたこと
- 解説者・批評家による解釈
- 現在との比較と、作品から生まれた未来への問い
- 作品世界の証拠と現実世界の証拠を分ける `evidence_domain`

利用者が明示しない限り、過去の論文や既存の研究テーマには接続しません。

この構造は scholarly-agent-skills の Discovery / Grounding、文献マトリクス、リポジトリ内実体化、Claim–Evidence 対応を映画資料向けに翻案したものです。

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
  --title "ターミネーターとスカイネット"
```

エージェントへの依頼例:

```text
$film-research-briefing を使い、『ターミネーター』（1984年）を
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

MVP は日本語スキル、調査ディレクトリ生成、出典ノート生成、Claim–Evidence 検査を提供します。YouTube やブログの取得・閲覧はエージェントのブラウザー機能を使い、自動字幕の一括ダウンロードやアクセス制限の回避は行いません。

## 開発

```bash
python3 -m unittest discover -s tests -v
python3 /home/ogoshi/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/ja/film-research-briefing
```

## 免責

本リポジトリは無保証の調査支援ツールです。要約、出典判定、作品解釈、現在との比較には誤りが残り得ます。重要な主張は作品本編と一次資料で利用者自身が確認してください。著作権、研究倫理、個人情報、サイト・API 規約の遵守は利用者の責任です。法律・医療・投資その他の専門助言を提供しません。詳細は [DISCLAIMER.md](DISCLAIMER.md) を参照してください。
