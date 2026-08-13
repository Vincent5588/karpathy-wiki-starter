---
title: "規則 R — _MOC / README updated bump 紀律"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-08-13
tags: [rule, moc, readme, frontmatter, cascade, vault-discipline]
aliases: [規則 R, MOC updated bump, README updated bump]
---

# 規則 R：_MOC / README updated bump 紀律

> 內含同層索引的 `_MOC.md` / `README.md`，該層任何 `.md` 檔異動（新建 / 修改 / 刪除 / 改名）後**必須** bump frontmatter `updated:` 為當日日期。

---

## 為什麼

`_MOC` / `README` 是該層的 SSOT，frontmatter `updated:` 反映「這層最後一次異動是什麼時候」。沒有它，打開 `_MOC` 的人（含未來的你、含下一個 LLM session）無法判斷：

- 索引內容是否新鮮（列出的檔清單是不是該層真實現況）
- 上次整理是什麼時候
- 這層該不該再 review

**Root cause**：沒有規則強制 bump，就只能靠使用者自己發現後手動補——同類事件會反覆發生，這正是該規則化的信號。

---

## 觸發條件（範圍精準化）

### ✅ 適用

| 檔類 | 說明 |
|------|---|
| `_MOC.md` | 任何主題 hub |
| `README.md` **含同層索引**（手寫表 / Dataview / 章節列表）| 該 README 實際扮演索引角色 |

### ❌ 不適用

| 檔類 | 理由 |
|------|------|
| `20-Projects/<name>/_<name>_MOC.md` | 已被**規則 Q** 覆蓋，不重複 |
| 純導覽 stub 型 `README.md`（只有「← 回到 index」之類）| 沒有索引語義 |

### 例外（不算「異動」，不必 bump）

- 純筆誤 / 拼字 / 標點修正
- Attachments / 圖片更新
- Dataview 後台資料變化（資料層異動，不是索引 schema 改動）
- 規則 R 自身的規範修訂（self-referential 排除，避免無窮觸發）

---

## 如何適用（SOP）

1. **動完該層任何 `.md` 檔**後，立刻自問：這層有 `_MOC.md` 或含索引的 `README.md` 嗎？
   - 有 → 進 step 2；沒有 → 跳過。
2. **打開該檔的 frontmatter。**
3. **Edit `updated:`**
   - 已有欄位 → 改成當日（`YYYY-MM-DD`）
   - 沒有欄位 → 新增（放在 `created:` 之後）
4. **chat cite cascade**（規則 P）：引用規則 R + `Wiki_維護觸發規則` §8.6，列出已 bump 的檔。

---

## 跟其他規則的關係

| 規則 | 配合 |
|---|---|
| 規則 H（stable artifact 版本歷程）| H 對「stable + 重大改動」要求版本表；R 對「索引層 + 同層任何異動」要求 `updated`。**R 更輕量、頻次更高。** |
| 規則 Q（PARA project `_MOC`）| Q 已強制 project `_MOC` bump，R 只覆蓋 Q 範圍外的 `_MOC` / README |
| 規則 E（show before write）| 動該層檔本身仍走 show；R 觸發在動完之後 |
| 規則 O（探勘優先）| 動檔前先讀該層 `_MOC` / README 看現況，不能憑印象 |
| 規則 P（cite cascade）| 觸發時要 cite「依規則 R 將 bump `_MOC` frontmatter」|

---

## 範例

**新增一個 entity 到某資源庫**

```
動作：在 40-Resources/<主題>/ 新建 某工具評估.md
規則 R 觸發：
  ① ls 同層 → 看到 _<主題>_MOC.md（含 Dataview 索引）
  ② Edit _MOC frontmatter：updated: 2026-05-09 → 當日
  ③ 同層 README.md 若也含索引 → 一併 bump
  ④ chat cite：依規則 R 已 bump _MOC.md updated
```

**純筆誤修正（例外）**

```
動作：修 40-Resources/<主題>/03-某章節.md 的錯字
規則 R 不觸發（純筆誤排除）→ 不必動同層 README
```

---

## 可選配套

- 全 vault 現有 `_MOC` / 索引型 README 一次性補齊 `updated` 欄位
- `wiki/tools/lint.py` 可加檢查項：「`_MOC` / README 含索引但無 `updated`」→ 標 🟡

---

← 回到 `CLAUDE.md` §10 | `Wiki操作文件/Wiki_維護觸發規則.md` §8.6
