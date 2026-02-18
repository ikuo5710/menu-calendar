# プロジェクトメモリ

## 重要なルール

### 実装前の確認

新しい実装を始める前に、必ず以下を確認:

1. CLAUDE.mdを読む
2. SPEC.md
3. BeadsでEpicの進捗状況を確認し取り組むべきタスクを特定する。
3. Grepで既存の類似実装を検索
4. 既存パターンを理解してから実装開始

### タスクの管理

作業管理は beads（bd）で行う。GitHub Issue と beads を連携させて運用する。

- GitHub Issue 1件 → beads Epic 1件（親）
- Issue内のチェックリスト項目 → beads 子タスク（`--parent` で紐付け）
- beads Epic の description に GitHub Issue URL を記載して相互参照
- コミットメッセージに `#N`（GitHub Issue番号）を含める
- PRの description に `Closes #N` を含め、マージ時にIssue自動クローズ

#### GitHub Issue の起票ルール

新しい作業単位は GitHub Issue を起点とする。

1. GitHub Issue を作成（設計・要件・チェックリスト `- [ ]` を記載）
2. beads に Epic を作成し、description に Issue URL を記載:
   `bd create --title="GH#N: タイトル" --type=epic --description="https://github.com/<OWNER>/<REPO>/issues/N"`
3. Issue 内のチェックリスト項目ごとに beads 子タスクを作成:
   `bd create --title="タスク名" --type=task --parent=<EPIC_ID>`
4. 必要に応じてタスク間の依存を設定:
   `bd dep add <後続タスク> <先行タスク>`

#### beads 運用ルール

**セッション開始時（必須）:**
1. `git status` で作業ツリーを確認（汚れていたら commit / stash が必要と伝えて止まる）
2. `bd sync` で beads を同期

**作業中:**
- 着手: `bd update <ID> --status=in_progress`
- 意思決定やブロッカーはコメントで記録:
  - `bd comments add <ID> "DECISION: …"`
  - `bd comments add <ID> "ROOT CAUSE: …"`
  - `bd comments add <ID> "BLOCKER: …"`
  - `bd comments add <ID> "LEARNED: …"`
  - `bd comments add <ID> "NEXT: …"`
- 完了: `bd close <ID> --reason "…"` し、対応する GitHub Issue のチェックリスト項目を `- [x]` に更新する（`gh issue edit` で body を更新）

**コミット・PR:**
- コミットメッセージに `#N`（GitHub Issue番号）を含める
- PR description に `Closes #N` を含める

**セッション終了時（必須）:**
1. `git status` を確認（汚れていたら確認して止まる）
2. `bd sync` で beads を同期
3. 可能なら `bd doctor` で健康チェック

**ブランチ運用:**
- main/feature ブランチに `.beads/*.jsonl` を混ぜない
- 混入したら即除外: `git restore --staged .beads`
- `.beads/config.yaml` は main に含めてよい

**ガードレール（止まって確認する条件）:**
- `bd sync` 中に rebase/merge/conflict が出た
- `git status` が汚れているのに `bd sync` が必要になった
- `.beads/*.jsonl` が main/feature に混入した
- `bd doctor` が Sync Divergence を繰り返し検出する