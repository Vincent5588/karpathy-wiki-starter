---
title: "規則 Q — PARA Project 維護規範（MOC SSOT + 異動 Cascade）"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-08-13
tags: [rule, para, moc, cascade, project-management]
aliases: [規則 Q, PARA MOC, Project MOC SSOT]
---

# 規則 Q：PARA Project 維護規範（MOC SSOT + 異動 Cascade）

> 每個 `20-Projects/<name>/` 子目錄**必有** `_<name>_MOC.md` 作為該 project 的 SSOT（Single Source of Truth）；任何子目錄內檔案異動（新建 / 修改 / 刪除 / 改名）都要回頭更新 `_MOC`，並同步上游索引（`index.md` 的進行中專案清單）。

---

## 為什麼

PARA project 子目錄常累積 5-30 個檔案（規劃、規格、對外溝通、資料分析、原型、草稿…），沒有 SSOT 入口就會散亂。**`_MOC` 集中索引 + 異動 cascade 確保「打開 `_MOC` = 30 秒掌握 project 全貌」。**

**Root cause**：`_MOC` 維護紀律若只寫在某一個 `_MOC` 檔裡 inline，新建下一個 `_MOC` 時一定漏抄。放進 vault 全域規則，所有未來的 project 都自動受規範。

---

## 觸發條件

凡是動 `20-Projects/<name>/` 子目錄內任何檔案，規則 Q 都生效：

- 新建文件（規格 / 規劃 / 簡報 / 分析…）
- 修改既有文件（內容更新 / bump 版本）
- 刪除 / deprecated 文件
- 改名 / 改 basename / 移動檔
- 新建 project 子目錄（必同時建 `_MOC` + 上游索引加 row）

---

## 如何適用（SOP）

### 1. 動檔前（規則 O 探勘優先）
先讀對應 `_<name>_MOC.md`，確認當前 project 狀態與歷史脈絡。

### 2. 動檔中（規則 E show before write）
新建 / 大改 / 改名 / 刪除前，在 chat 提案 → 等批准 → 才動。

### 3. 動檔後（本規則的 cascade 義務）

| 異動類型 | 必動 `_MOC` 區塊 | 額外 cascade |
|---|---|---|
| **新建文件** | 📚 文件總索引（對應分類加 row）+ frontmatter `updated` | — |
| **修改核心文件**（規格 / 主要規劃）| 🚦 目前進度 + 該文件版本歷程（規則 H）+ frontmatter `updated` | — |
| **刪除 / deprecated** | 📚 文件總索引（改狀態 ⚠️ deprecated 但**保留 row**）+ 說明原因 | 走刪檔處理 SOP 的緩衝期 |
| **改名 / 改 basename** | 📚 文件總索引（更新 wikilink）| grep 全 vault backlink，確認沒漏外部引用 |
| **路線 / Phase 切換** | 🚦 目前進度 + 🔮 未來路線圖 + 📊 專案儀表板 + 📜 路線歷程 | 該文件版本歷程（規則 H）|
| **新建 project 子目錄** | 建 `_<name>_MOC.md` + 上游索引加 row | — |

### 4. 動完後（規則 P cite 義務）
chat 引用「依 `Wiki_維護觸發規則` §8.5 + 規則 Q，本次『<動作>』將 cascade：① … ② …」。

---

## 🔴 登記／鎖定單位＝「專案」，不是「檔」

多個 agent／session 併行時，若你的工作流有「宣告我在改哪個檔」的機制（避免撞版），**登記 `20-Projects/<name>/` 底下任何檔案時，該專案目錄全部 ＋ 它的 `_<name>_MOC.md` 一併算在內**。

**為什麼**：本規則要求「動子目錄任何檔案 → 必須同步更新 `_MOC`」。若只鎖住被改的那一個檔，`_MOC` 就落在**「我一定會寫、但鎖沒涵蓋」的縫**裡——實際踩過的後果是兩個寫者同時改 `_MOC`，檔案版本互相覆蓋、指向它的 wikilink 整批斷鏈。

⭐ **心法**：一把只鎖住「我打算改的檔」、卻不鎖「規則規定我一定要跟著改的檔」的鎖，保護不了任何完整動作——它鎖的是意圖，不是行為的實際落點。**規則之間的接縫，比規則本身更容易漏。**

---

## `_MOC` 標準結構（新 project 建檔模板）

```yaml
---
title: <Name> Map of Content — <project 全名>知識地圖
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [moc, <project-tag>, hub]
cssclasses: [wide]
---
```

必備 sections：

1. **🎯 一行專案定位** — 30 秒掌握這 project 是什麼
2. **📊 專案儀表板** — 狀態 / 截止 / 技術棧 / 資源（table）
3. **🚦 目前進度** — ✅ 已完成 / 🔄 進行中 / ⏳ 即將進入 / 📜 路線歷程
4. **📚 文件總索引** — 按分類列所有 project 內文件 + 對應 `wiki/entities/<domain>/` 索引
5. **🚨 風險清單** — table：風險 / 級別 / 緩解
6. **📞 關鍵聯絡** — table：角色 / 對象 / 用途
7. **🔮 未來路線圖**（選用）
8. **📜 文件維護規範** — 只寫「依 `CLAUDE.md` 規則 Q」一行引用，**不要 inline 重複規則**
9. **🎓 給新成員的快速上手** — 排序好的閱讀清單

**檔名紀律**：`_<分類>_MOC.md`（帶分類名），不要用純 `_MOC.md`——多個同名 basename 會讓 wikilink 歧義、Dataview 清單分不清誰是誰。

---

## 例外

| 情境 | 處理 |
|---|---|
| 純筆誤 / 拼字 / 標點 | 不必動 `_MOC` |
| 對外草稿 / 臨時版 | 只動 `_MOC` 對應索引，不必動其他區塊 |
| Attachments / 圖片更新 | 不必動 `_MOC` |
| 子目錄 README 小調整（不涉及 project 整體狀態）| 不必動 `_MOC` |

---

## 配套規則

| 規則 | 配合方式 |
|---|---|
| 規則 C（PARA 原始檔保留）| Q 不違反 C——`_MOC` 是 LLM 維護的索引層，不動使用者既有檔內容 |
| 規則 E（show before write）| Q 內所有新建 / 大改 / 改名 / 刪除都先 show |
| 規則 H（stable artifact 版本歷程）| 「修改核心文件」要 bump 該文件版本歷程 |
| 規則 L（>30 行拆檔）| 本規則就是用規則 L 拆出來的（主檔只留 1-row 速查）|
| 規則 O（探勘優先）| Q 第 1 步「先讀 `_MOC`」＝規則 O 在 PARA project 的具體化 |
| 規則 P（Cite-or-Die）| 動作完成後必 cite cascade 清單 |
| 規則 R（`_MOC` / README `updated` bump）| R 覆蓋 Q 範圍**以外**的 `_MOC` / 索引型 README，兩者不重複 |

---

## 對 LLM agent 的紀律意義

動 `20-Projects/<name>/` 內任何檔案時：

1. **永遠先 ls + 讀 `_<name>_MOC`**（規則 O）
2. **永遠 show 提案再動手**（規則 E）
3. **動完永遠回頭更新 `_MOC`**（規則 Q）
4. **永遠在 chat cite cascade**（規則 P）

四條 = 在 PARA project 內安全工作的閉環。漏任何一條 = 違規；使用者隨時可喊「規則 Q check」要求你列出「已 cascade vs 應 cascade」的 diff。

---

← 回到 `CLAUDE.md` §10 | `Wiki操作文件/Wiki_維護觸發規則.md` §8.5
