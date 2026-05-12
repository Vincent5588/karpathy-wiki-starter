---
title: "規則 N：雲盤 + git 紀律（single-writer policy）"
tags: ["claude-md-rule", "rule-N", "git", "cloud-sync", "single-writer", "icloud", "dropbox", "onedrive"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-11
updated: 2026-05-11
---

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-11 | 初版——從「雲盤 + git 多寫者必爆」的經驗實證 codify。同步來源：Vincent5588 vault v1.3.30 + 同期 Windows 端踩雷實證（iCloud 對 `.git/index` / `refs/heads/main` 製造多版本衝突累積 70+ 案例）|

# 規則 N：雲盤 + git 紀律（single-writer policy）

> **核心鐵則**：vault 用雲盤跨機同步編輯 OK，但 **git operations 只在一台機器** 的「**雲盤外**」位置進行。多寫者必爆雲盤 conflict，必須避免。

## Why

雲盤同步機制（iCloud / Dropbox / OneDrive 等）跟 git low-level binary 檔本質不相容：

| 雲盤對 git 內檔的破壞 | 結果 |
|----------------------|------|
| `.git/index` 兩機同時寫 | 雲盤產 `index 2` / `index 3` / ... 衝突副本 |
| `.git/refs/heads/main` 兩機同時 push | 雲盤改名 `main 2`，git 找不到 HEAD |
| `.git/objects/` 暫存物件 | 雲盤未完整 sync 就被 git 讀，corrupt object 錯誤 |
| `.git/HEAD` 衝突 | git status 失靈、commit 報「fatal: bad object HEAD」|

→ 即使「只在 Mac 上發生風險較低」，仍然是定時炸彈。**單寫者紀律**是唯一可靠解。

## 三層架構（推薦實作）

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1：雲盤 vault（純檔案，跨機 sync）                  │
│  ~/Library/Mobile Documents/.../my-wiki/（macOS iCloud 範例）│
│  ├── *.md, .obsidian/, 00-50/, wiki/, Templates/           │
│  └── ❌ 不放 .git（解耦於 git）                              │
│                                                              │
│  ↕️ 雲盤自動 sync 跨多機（Mac / iPad / iPhone / PC）         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                       ↓ 手動 sync script
┌─────────────────────────────────────────────────────────────┐
│  Layer 2：雲盤外 git working tree（單寫者）                 │
│  ~/git-mirrors/my-wiki/ （macOS）                            │
│  or D:\vault-git\my-wiki\ （Windows）                       │
│  ├── .git/                ← 正常 git 目錄（無雲盤干擾）      │
│  ├── *.md, .obsidian/, ... ← 同步來的 vault 內容            │
│  └── sync.sh / sync.ps1   ← rsync / robocopy 腳本           │
└─────────────────────────────────────────────────────────────┘
                       ↓ git push / pull
┌─────────────────────────────────────────────────────────────┐
│  Layer 3：GitHub                                            │
│  github.com/<you>/<your-vault>                              │
└─────────────────────────────────────────────────────────────┘
```

**雲盤仍是跨機 sync 真理**——iPad / iPhone / Mac / PC 都直接吃雲盤；只是「主寫者機」多一道 git working tree 中介，雙擊 sync 腳本同步 → git push。

## How to apply

### 一般紀律

1. **編輯 vault**：任何機器 OK（雲盤自動 sync）
2. **想 push 到 GitHub**：到主寫者機，跑 sync 腳本（譬如 `sync.sh` / `sync.ps1`）→ 自動 commit + push
3. **想看 git history / diff**：到主寫者機跑 `git log` / `git diff`
4. **緊急 push（主寫者不在）**：等回去或臨時 setup（見「例外觸發」）

### 加新機器時

- 預設**不建** 雲盤外 `.git/`——機器純當 vault 編輯點
- 例外：該機需要獨立 push 能力（譬如旅行筆電長期不在主寫者機附近）→ 走「例外觸發條件」

### 廢棄不再用的 git folder

當切換主寫者機，舊機器的 `.git/` working tree 廢棄處理流程：

1. 確認所有 commit 都 push 到 origin（`git log origin/main..HEAD` 無 output）
2. 確認 working tree 無未 commit 重要 changes（grep 排除 `.DS_Store` 等 system noise）
3. 確認 GitHub 有完整 history（`git log -3` vs `git log origin/main -3` 比對 commit hash）
4. 刪除整個 folder（`rm -rf <path>`）

## 例外觸發條件（什麼時候要走多寫者）

### 觸發條件

- 第二人加入協作（不是個人 vault）
- 主寫者機**長期**不在身邊（≥ 1 週）且其他機需要 commit
- 主寫者機 hardware failure

### 多寫者必備紀律

若必須走多寫者：

1. **每台**都建雲盤外 `.git/`（譬如 Mac 走 `~/git-mirrors/<vault>/`、Windows 走 `D:\vault-git\<vault>\`）
2. **嚴格 pull-before-edit**：每次回到 git folder 先 `git pull` 再動
3. **嚴格 push-after-edit**：每次編完馬上 commit + push
4. **不要兩機同時開 git folder 跑 commit**
5. **衝突發生時走 conflict-resolution discipline**：`git stash` → `git pull --rebase` → resolve → `git push`

### 多寫者風險

即使遵守紀律，仍有：

- conflict resolution 出錯導致 commit 丟失
- 兩機 push window 重疊導致 GitHub 拒絕後者 push
- LLM agent 跨機 session 互不知道對方狀態

→ 強烈建議**寧可繞路單寫者**，不要為「方便」開多寫者。

## 雲盤 conflict 累積清理（per-machine config 衝突）

即使 git 已雲盤外，vault 內 **per-machine config** 仍會被雲盤累積衝突：

- `.obsidian/workspace.json`（layout，每機不同）
- `.obsidian/plugins/*/data.json`（plugin 設定，每機可能不同）
- `.claude/settings.local.json` 或類似 per-machine LLM 工具設定

兩台機都寫 → 雲盤撞 → 累積成 `* 2.json` / `* 3.json` / ... 衝突檔。

**清理腳本範本**（macOS bash）：

```bash
#!/usr/bin/env bash
# clean-cloud-conflicts.sh
# 清理 vault 內雲盤 sync 衝突檔（per-machine config 撞造成的 N.json 累積）
#
# 用法：
#   bash clean-cloud-conflicts.sh          # dry-run
#   bash clean-cloud-conflicts.sh delete   # 真刪

set -euo pipefail

VAULT="<your-vault-path>"   # 改成你的 vault 路徑
MODE="${1:-dry-run}"

cd "$VAULT" || exit 1

TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

# 找所有 conflict pattern: "* N.json" 含數字 suffix
{
    find . -type f \
        \( -name "* 2.json" -o -name "* 3.json" -o -name "* [4-9].json" \
           -o -name "* 1[0-9].json" -o -name "* [2-9][0-9].json" \
           -o -name "workspace [0-9]*.json" \) \
        2>/dev/null | grep -v "/\.git/" > "$TMPFILE"
} || true

TOTAL=$(wc -l < "$TMPFILE" | tr -d ' ')
echo "found: $TOTAL conflict file(s)"

if [[ $TOTAL -eq 0 ]]; then
    echo "✅ vault clean"
    exit 0
fi

if [[ "$MODE" == "delete" ]]; then
    while IFS= read -r f; do rm -f "$f"; done < "$TMPFILE"
    echo "deleted $TOTAL file(s)"
else
    head -10 "$TMPFILE"
    echo "(dry-run, run with 'delete' to actually remove)"
fi
```

**特別處理 `.claude/settings.local.json` 等含資訊的衝突檔**：直接刪會丟資訊（每台機 permissions 不同），建議**手動 merge** unique entries 進主版後再刪。

## 跟其他規則的關係

- **規則 F（deploy pipeline 必鎖版本）**：規則 N 是「source code 端紀律」，規則 F 是「build pipeline 端紀律」，兩者搭配確保「從 source 到 deploy 全鏈路無漂移」
- **規則 H（stable artifact 版本歷程）**：本規則 N 自身 §0 版本歷程實踐規則 H
- **規則 L（未來新規則拆檔）**：本規則符合 L 拆檔模式（CLAUDE.md 主檔留 1-row 速查，詳細在本檔）

## 反模式警覺

- ❌ **想方便 / 想跨機 push** → 開多寫者：必爆雲盤衝突。即使現在沒爆，累積到某天會爆
- ❌ **把 `.git/` 放回雲盤路徑**：跟「雲盤外」原則衝突，衝突一定回來
- ❌ **多機都用 cron / hook 自動 push**：自動化 + 多寫者 = 衝突指數成長
- ❌ **不寫紀錄就刪 git folder**：未來想還原找不到刪除原因

## 例外條款

- 純臨時測試（譬如 throwaway branch）→ 可破例
- 真的有第二位 collaborator → 必須走多寫者紀律
- 主寫者機壞掉緊急情況 → 臨時 setup 一台當主寫者，事後拆掉
