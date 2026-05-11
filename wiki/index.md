---
title: "Wiki 主目錄"
tags: ["index", "wiki"]
updated: YYYY-MM-DD
cssclasses: [wide]
---

# 📚 Wiki 主目錄

> 所有知識卡片（entity）的入口。
> 條目格式：`- [[basename]] — 一行摘要（< 30 字）`
> ⚠️ 每次 ingest 後 Claude 必須更新此檔。

**Entity 總數**：0｜**最後更新**：YYYY-MM-DD

---

## 依 Domain 瀏覽

> 建立第一批 entity 後，依你的 domain 在此分類整理。

### 範例 Domain：learning（學習）
<!-- Claude 會在 ingest 後自動在此補充條目 -->
<!-- 格式：- [[entity-basename]] — 一行摘要 -->

### 範例 Domain：work（工作）

### 範例 Domain：personal（個人）

---

## 依 Type 瀏覽

| Type | 說明 | 數量 |
|------|------|------|
| `concept` | 抽象概念 / 原理 | 0 |
| `process` | 流程 / SOP | 0 |
| `system` | 系統 / 工具 | 0 |
| `pattern` | 可重複使用的技巧 | 0 |
| `rule` | 規則 / 政策 | 0 |
| `artifact` | 具體文件 / 報表 | 0 |
| `role` | 角色 / 職責 | 0 |
| `person` | 真實人物 | 0 |

---

## Dataview 查詢（需啟用 Dataview 外掛）

### 最近更新 10 個

```dataview
TABLE WITHOUT ID file.link AS "頁面", domain AS "Domain", type AS "Type", updated AS "最後更新"
FROM "wiki/entities"
SORT updated DESC
LIMIT 10
```

### 待審 Draft

```dataview
LIST
FROM "wiki/entities"
WHERE status = "draft"
```

### 孤兒頁（無 backlink）

```dataview
LIST
FROM "wiki/entities"
WHERE length(file.inlinks) = 0
```
