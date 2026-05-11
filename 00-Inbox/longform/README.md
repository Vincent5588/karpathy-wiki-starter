# 00-Inbox/longform/ — 不想被拆解的長文 raw

> **放這裡的檔，LLM ingest 時觸發 `atomize: false`——建 1 個 longform entity（不拆成多個 atomic），仍走完整 cascade（index / 路由 / daily log）**

## 📌 用途

放**想保留完整、不想被拆解成 N 個 atomic entity** 的素材：

- 個人完整心得（一篇完整觀點，不適合拆 atomic）
- 旅遊紀錄 / 敘事體
- 流水帳 / 日記
- 完整書評（你想當「一份作品」保留）
- 訪談 / 對話逐字稿（想保留對話脈絡）
- 完整外部文章

## ✅ 何時用

判斷準則一句話：**「我想保留這份的完整性，不要被拆」** → 丟這裡。

如果是「我想抽精華概念出來建多個知識卡片」→ 放 `00-Inbox/` 根目錄即可（預設 atomize:true）。

## 🤖 LLM 行為

放這裡的檔，LLM ingest 時依 [[CLAUDE]] §3.1.1：

| 步驟 | 動作 |
|------|------|
| Step 0 預檢 | 偵測路徑含 `longform/` → 設定 `atomize: false` |
| Step 3 建 entity | ✅ **建 1 個** `wiki/entities/<domain>/longform/<basename>.md`（type=longform）|
| Step 3 entity body | ✅ LLM 加 wrapper：摘要 + 核心要點 5-7 條 + 強連結/推斷連結/深入閱讀 + 原文（個人時內含 / 外部時連回 PARA）+ 待解 |
| Step 4 加 backlink | ✅ 仍做 |
| Step 6 更新 wiki/index.md | ✅ 仍做（longform entity 也算新 entity）|
| Step 7 寫 daily log | ✅ 仍做 |
| Step 8 PARA routing raw | ✅ 仍做（外部文章 raw 搬到 40-Resources；個人 longform 不必另搬）|

→ **重點**：不是「跳過 entity」是「**建 1 個 entity 不拆**」。所有 cascade 跟標準 ingest 一樣做。

## 🎯 預設路由目的地

| 內容性質 | raw 路由到 | entity 在 |
|---------|----------|----------|
| 別人寫的完整文章 | `40-Resources/<domain>/<sub>/` | `wiki/entities/<domain>/longform/<X>.md` |
| 個人完整觀點 / 心得 | 不必另外搬（entity 本身即內容）| `wiki/entities/<domain>/longform/<X>.md` |
| 旅遊 / 日記敘事 | `10-Notes/journal/` 或 `30-Areas/<area>/` | 同上 |

→ 永遠 show before write（規則 E），等使用者批准才搬。

## 💡 三層判斷優先序（atomize 旗標來源）

1. **frontmatter `atomize:` 明確指定** → 永遠優先
2. **路徑含 `longform/`** → 預設 `false`
3. **預設** → `true`（拆 atomic）

詳見 [[CLAUDE]] §3.1.1。
