# 50-Archive — 已封存

> **PARA 第 5 層：不再活躍但不捨得刪的歷史資料**

## 📌 用途（給人）

放**不活躍但保留歷史**的檔。Archive 不是垃圾桶——它是**未來可能想回頭參考的東西**。真要刪請走 [[Wiki_刪檔處理SOP]] 三層緩衝期。

**典型內容**：
- 已完成的 20-Projects（搬過來）
- 不再關注的 30-Areas（搬過來）
- 過時但仍有參考價值的 40-Resources
- 廢棄的點子 / 草稿（10-Notes 搬來）
- 規範改版前的歷史版本

## ✅ 何時放東西進來

- **專案完成**：`20-Projects/<X>/` → `50-Archive/projects/<X>/`
- **領域退場**：`30-Areas/<X>/` → `50-Archive/areas/<X>/`
- **參考過時**：`40-Resources/<X>/` → `50-Archive/resources/<X>/`
- **想刪但不確定**：先丟這裡觀察 30 天（依刪檔 SOP）

## 🗂 子資料夾建議

依來源層分類：

```
50-Archive/
├── projects/       ← 已完成 / 放棄的專案
├── areas/          ← 不再關注的領域
├── resources/      ← 過時的參考
├── notes/          ← 廢棄的個人筆記
└── vault-versions/ ← vault 結構改版前的快照
```

## 🤖 LLM 行為規範

- ✅ LLM 可從 20/30/40 搬檔過來（使用者批准後）
- ✅ ingest 時**仍可**從這裡的檔當 source（archive ≠ 看不到，但需使用者明確指定）
- ✅ 使用者明確說「真的刪 X」→ 走 [[Wiki_刪檔處理SOP]] 真刪
- ❌ **不主動刪 archive 內檔**——archive 是緩衝區，30 天觀察期由使用者決定
- ❌ 不批次清理 archive（規則 C：永不刪除）
- ❌ 不重命名 archive 子資料夾
- ❌ **永不主動掃描** 50-Archive 找東西 ingest（即使有更新也不主動提示——archive 不該動）

## 📥 Longform 不直接路由到 archive

`00-Inbox/longform/` 內檔**不該**直接路由到 50-Archive——archive 是「曾經活躍、現在不活躍」的資料層。

正確流程：
1. longform raw 先路由到 `10-Notes/longform/` 或 `30-Areas/<area>/` 等活躍層
2. 之後該檔不再活躍 → 才搬到 `50-Archive/`

詳見 [[CLAUDE]] §3.1.1（longform 預設路由表沒列 50-Archive）。

## 🆚 跟「真正刪除」的差異

| 動作 | 後果 |
|------|------|
| **Archive** | 檔還在、git history 還在、能 grep 到 |
| **Git rm** | 檔消失、但 git history 仍可回溯 |
| **rm（直接刪）** | ❌ **絕對不准**——破壞 git 同步、可能誤刪 |

## 💡 三層緩衝期（依 [[Wiki_刪檔處理SOP]]）

```
Active（10/20/30/40）
    ↓ Step 1：搬到 50-Archive（保留 + 留 redirect stub）
50-Archive
    ↓ Step 2：30 天觀察期
    ↓ Step 3：人類批准才 git rm（極少數）
真正刪除
```

→ 80% 的「想刪」其實該停在 Step 1 就好。完整 SOP + 追蹤表見 [[Wiki_刪檔處理SOP]]。

## 💡 archive 還能查到嗎？

可以：
- Obsidian 全域搜尋 / Dataview 都看得到 archive 內容
- LLM ingest 仍可把 archive 內檔當 source
- wiki-link `[[X]]` 仍能解析到 archive 內檔（basename 穩定）

**但 archive 不該出現在 [[wiki/index]] 的主目錄**——只在使用者特別查詢時露面。
