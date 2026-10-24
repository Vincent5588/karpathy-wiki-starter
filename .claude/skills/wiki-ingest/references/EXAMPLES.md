# wiki-ingest 範例

## 範例 1：Ingest 一篇關於提示工程的文章

**Input**: `raw/articles/prompt-engineering-tips.md`

**Step 1 — Read & summarize**:
> 文章主要講 5 個提示技巧：role prompting、few-shot、CoT、XML tagging、self-check。前 2 個我們 wiki 已經有，後 3 個沒有。
> 
> 主要貢獻：用商業客服例子說明 few-shot 比 zero-shot 好 30%。
> 
> 要建 3 個新 entities？或更新現有 [[Few-shot prompting]] 加更多例子？

**Step 2 — User confirms**:
> 「建 3 個新 entities，並更新 Few-shot 加客服例子。」

**Step 3 — Output**:

新建：
- `wiki/entities/Chain of Thought.md`
- `wiki/entities/XML 標籤提示.md`  
- `wiki/entities/Self-check.md`

更新：
- `wiki/entities/Few-shot prompting.md`（加客服例子）
- `wiki/index.md`（提示工程區加 3 個新 link）
- `wiki/log.md`（追加 ingest 紀錄）

**Step 4 — 報告**:
> ✅ 建了 3 個新概念頁、更新 1 個既有頁
> ⚠️ 發現衝突：文章說「few-shot 提升 30%」但既有 [[Multi-shot prompting]] 引用的研究說「20-50%」——已在兩頁標 ⚠️ 待釐清
> 💡 建議下次 ingest：作者提到的「prompt chaining」概念在 wiki 還沒有

## 範例 2：模糊提示

**User**: 「ingest 那篇文章」

**Skill 應該做**: 用 Glob `raw/articles/*.md` 列出所有文章，問使用者具體哪一篇。

❌ **不該做**: 隨便挑一篇處理。

## 範例 3：明確跳過討論

**User**: 「ingest raw/articles/karpathy-tips.md, 不用問直接做」

**Skill 應該做**: 跳過 step 2 的「summarize 確認」，直接執行步驟 3-7。

## 範例 4：raw/ 中還沒有檔案

**User**: 「ingest 那份新文章」

**Skill 應該做**:
1. 用 Glob 找 raw/，發現空的
2. 回報「raw/articles/ 沒檔案。請先把素材丟到 raw/{papers,articles,transcripts,datasets,books} 對應子目錄」
3. 不執行任何修改

## 衝突偵測案例

如果新 source 說「Anthropic Opus 4.6 是 2026/04 發表」，但既有 entity `Claude 模型家族` 寫「2026/03 發表」，必須：

1. 在新建/更新的頁面加：
   ```
   > ⚠️ 衝突：本來源稱 2026/04 發表；[[Claude 模型家族]] 第 2 段稱 2026/03。需查官方公告確認。
   ```

2. 在既有 [[Claude 模型家族]] 加：
   ```
   > ⚠️ 待釐清：發表日期可能與其他來源（[[新 ingest 頁]]）不一致。
   ```

3. 在報告中明確列出衝突。

**禁止**：直接覆蓋既有頁面的原內容。
