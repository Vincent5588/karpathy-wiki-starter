# Wiki Health Rules

## Definitions

### Orphan page
An entity or map that has **0 inlinks** from other entities/maps in `wiki/`. Note: `wiki/index.md` doesn't count toward inlink count (or every page would be linked).

### Missing concept
A `[[X]]` reference where `wiki/entities/X.md` doesn't exist, AND X isn't:
- A cross-folder path (`40-Resources/...`, `raw/...`)
- A chapter-style reference (`01-Topic`, `12-Subject`)
- Standard files (`README`, `index`, `Welcome`, `CLAUDE`, `Templates`)

### Hub
An entity with `≥8 inlinks`. Top hubs (`≥10`) indicate the knowledge base has clear central concepts.

### Low-inlink page
An entity with `inlinks == 1`. Often indicates:
- New page that hasn't accumulated cross-references yet (OK)
- Or a concept that should be merged or extended (problem)

### God node（v1.2 新增）
高度被連結但**內文薄弱**的頁面：

| 條件 | 門檻 |
|------|------|
| inlinks | ≥ 8 |
| words（CJK + ASCII 詞） | < 200 |
| ratio = words / inlinks | < 25 |

**Severity**：
- `critical`：words < 200 **且** ratio < 25（兩者都中）
- `warn`：words < 200 **或** ratio < 25（只中一個）

**為什麼這條規則重要**：
- inlinks 多 = 概念被廣泛引用 = 重要
- 但內文薄 = 沒寫透徹 = 知識網的中心是個空殼
- 應該優先擴充內容，把它做成真正的「樞紐文章」

不一定是錯——索引頁、術語頁本來就短，但很被引用。判斷時看內容性質。

### 推斷連結比例（v1.2 新增）
頁面的 `[[X]] ??` 軟連結占全部 outlinks 的比例。

| 比例 | 評價 |
|------|------|
| < 25% | 健康（連結多源自原文） |
| 25-50% | 可接受 |
| ≥ 50% | 偏高，建議審查並升級為強連結或刪除 |

只計算 outlinks ≥ 3 條的頁面（少於 3 條樣本太小）。

### Cross-domain basename collision（v1.3.2 新增）
兩個或以上的 entity file 在 `wiki/entities/` 樹的不同子路徑下擁有**同 basename**。例：

```
wiki/entities/orders/concept/X.md
wiki/entities/claude/concept/X.md
```

**為什麼是錯的**：Obsidian wiki-link `[[X]]` 是 basename-based。兩個都叫 X，`[[X]]` 解析變歧義，Obsidian 隨便挑一個（通常字母序在前的），inlink 統計也會誤算。

**Severity**：**🔴 High**——直接影響知識庫可用性。

**處理**：重命名其中一個 entity 加 disambiguation 後綴（例：`X (訂單).md`），更新所有引用點，再交給 lint 重跑確認。

## Filter rules (false positives)

The lint script does NOT report these as missing:

1. **Markdown table pipe escapes**: `[[X\|Y]]` is valid Obsidian wiki-link in tables. Strip trailing `\` before checking.

2. **Cross-folder references**: `[[40-Resources/訂單系統/03-功能模組/通知系統]]` — these point to non-wiki/ files, not entities.

3. **Chapter references**: `[[09-Claude Code 建置與使用]]` — these are referenced from entities pointing to source learning material.

4. **Standard files**: `[[index]]`, `[[README]]`, `[[CLAUDE]]`, `[[Welcome]]`, `[[Templates/...]]`.

## Score components (out of 100, v1.2 重新分配)

| Component | Max | Calculation |
|-----------|-----|-------------|
| Orphans | 16 | 16 - (orphan_count × 4), floor 0 |
| Missing | 16 | 16 - (missing_count × 2), floor 0 |
| Density | 16 | 16 - (low_inlink_count × 2), floor 0 |
| Hub health | 16 | 16 if top_hub ≥ 10 inlinks else 10 |
| God nodes | 16 | 16 - (critical × 4) - (warn × 2), floor 0 |
| **Collisions** | **20** | **20 - (collision_count × 5), floor 0**（v1.3.2 新） |

> v1.1 是 4 個 component × 25 分；v1.2 改成 5 個 component × 20 分（加 god-node）；v1.3.2 改 6 個 component（5×16 + 1×20）把 collision 納入，且**權重最重**——歧義對知識庫殺傷力最大。

## Health interpretations

| Score | Status |
|-------|--------|
| 90-100 | Excellent |
| 75-89 | Healthy |
| 60-74 | Needs maintenance |
| 40-59 | Major gaps |
| < 40 | Restart consideration |

## Common issue → fix mapping

| Issue | Fix |
|-------|-----|
| Missing concept ≥2 refs | Create the entity page |
| Missing concept 1 ref | Either create OR change `[[X]]` to plain text |
| Orphan map | Add link in 1-2 thematically related entities' "相關概念" |
| Low-inlink (1) page | Add cross-references in semantically related entities |
| God node (warn) | 擴充頁面內容，目標 words/inlinks ratio ≥ 30 |
| God node (critical) | 優先處理：擴充至少 ≥ 800 字，或拆成多個原子頁 |
| 推斷連結 ≥ 50% | Read 該頁，判斷每條 `??` 該升級為強連結（移 `??`）或刪 |
| `[[script.py]]` | Replace with inline code: `` `script.py` `` |
| `[[X#anchor]]` opportunity | Convert flat `[[X]]` to anchored `[[X#section]]` |

## Lint frequency

Recommended: **weekly** (Sunday 30 min review).

After every major ingest/compile session, also run lint to catch new dangling refs immediately.

## v1.2 升級路徑

舊 wiki（v1.0/v1.1 寫的）的連結都是平的，沒有 `??` 標記。
跑 v1.2 lint 時 `inferred_link_pages` 永遠空——這是預期。

升級步驟：
1. 跑 lint 看 god nodes（不受影響，全自動偵測）
2. 處理 god nodes 時順便照新 ENTITY_TEMPLATE 把連結分強/推/外部三組
3. 之後 ingest 自動會用新格式
