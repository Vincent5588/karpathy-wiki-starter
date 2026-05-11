# 00-Inbox/longform/ — 不想被拆解的長文 raw

> **放這裡的檔，LLM ingest 時預設 `atomize: false`——不拆 atomic，只做 PARA 路由 + 日誌**

## 📌 用途

放**想保留完整、不想被拆解成 atomic entity** 的素材：

- 個人完整心得（一篇完整觀點，不適合拆 atomic）
- 旅遊紀錄 / 敘事體
- 流水帳 / 日記
- 完整書評（你想當「一份作品」保留，不是知識卡片）
- 訪談 / 對話逐字稿（想保留對話脈絡）

## ✅ 何時用

判斷準則一句話：**「我想保留這份的完整性，不要被拆」** → 丟這裡。

如果是「我想抽精華概念出來建知識卡片」→ 放 `00-Inbox/` 根目錄即可（預設 atomize）。

## 🤖 LLM 行為

放這裡的檔，LLM ingest 時依 [[CLAUDE]] §10 規則 K + §3.1：

| 步驟 | 動作 |
|------|------|
| Step 0 預檢 | 偵測路徑含 `longform/` → 設定 `atomize: false` |
| Step 3 抽 atomic entity | ❌ **跳過** |
| Step 6 更新 wiki/index.md | ❌（沒新 entity）|
| Step 7 寫 daily log | ✅ 記錄路由動作 |
| **Step 8 PARA routing** | ✅ **仍要做**——提案搬到 `10-Notes/longform/` 或其他適當位置 |

## 🎯 預設路由目的地

LLM 提案搬到（依內容性質）：

| 內容性質 | 建議目的地 |
|---------|----------|
| 個人完整觀點 / 心得 / 敘事 | `10-Notes/longform/` |
| 書評 / 完整摘要（屬主題集）| `40-Resources/<主題>/` |
| 某 area 的長文（健康 / 工作 / 學習）| `30-Areas/<area>/` |
| 旅遊 / 日記體 | `10-Notes/journal/` 或 `30-Areas/travel/` |

→ 永遠 show before write（規則 E），等使用者批准才搬。

## 💡 三層判斷優先序（atomize 旗標來源）

LLM 判斷 raw 是否 atomize 時依序：

1. **frontmatter `atomize:` 明確指定** → 永遠優先
2. **路徑含 `longform/`** → 預設 `false`
3. **預設** → `true`（拆 atomic）

換言之：你可以在 `00-Inbox/longform/` 內某檔加 `atomize: true` 強制拆（極少數情境）。

## 🆚 跟 `00-Inbox/` 根目錄差異

| 位置 | 預設行為 | 適合 |
|------|---------|------|
| `00-Inbox/` | 拆 atomic | 文章 / 文件 / 想萃取知識的素材 |
| `00-Inbox/longform/` | **不拆**、只路由 | 完整作品、敘事、心得 |
| `00-Inbox/Daily/` | 不 ingest（私人）| 個人 daily note |
