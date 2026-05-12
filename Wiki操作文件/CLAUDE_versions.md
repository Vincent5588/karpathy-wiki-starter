---
title: "CLAUDE.md 完整版本歷程"
tags: ["claude-versions", "wiki-meta"]
type: artifact
status: stable
cssclasses: [wide]
---

# CLAUDE.md 完整版本歷程

> **本檔是版本歷程 SSOT**。LLM 不必每次讀完整內容，要查特定版本的變更詳情才來這。
>
> `CLAUDE.md` §0 只保留當前版本號 + 本檔連結。完整歷程在這。

## 維護規則

- 每次 bump version 時，在下表**倒序追加新 row（最新在最下方）**
- CLAUDE.md 標頭版本號同步更新

## 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| **v1.0** | **2026-01-01** | 模板初版建立（基於 karpathy-wiki-pattern v1.4.3，規則 A-M）|
| **v1.1** | **2026-05-11** | **Longform / `atomize: false` 完整支援**：(a) §3.1 Step 3 加分流（atomize:true 建 N 個 / atomize:false 建 1 個 longform）；(b) §3.1.1 完整重寫——三層優先序 + 對照表 + Longform body 兩種模式（X 外部 / Y 個人）；(c) §4 type 詞彙表加 `longform`（9 種）；(d) `Templates/Longform Note.md` entity wrapper 結構；(e) `00-Inbox/longform/` 自動觸發 atomize:false；(f) `Wiki_維護觸發規則.md` §1 加 atomize:false 對照欄；(g) 各 PARA 資料夾 README sync。同步於 Vincent5588 v1.3.28 + IT-WIKI 規則 G。**設計修正**：早期把 atomize:false 設成「跳過 entity」是錯的——應該「建 1 個 entity 不拆」，否則 longform 跟知識網脫節。|
| **v1.2** | **2026-05-11** | **§3.1.1.1 內容性質判定（Step 0.5）新增**：v1.1 atomize 三層判定（frontmatter / 路徑 / 預設）只用 metadata 信號，**沒考慮內容本質**——把旅遊敘事丟 00-Inbox/ 根目錄會無腦走 atomize:true 拆 atomic（破壞敘事）/ 把 8 個獨立技巧的長文丟 longform/ 會無腦建 1 longform（浪費 atomic 抽取機會）。**修正方向**：LLM 必須在 Step 1 前再做一次內容性質判定，用 4 criterion（獨立概念數 / 論證結構 / 引用價值 / 語境完整）客觀分析 → 若內容判定 ≠ 預設旗標就主動 chat 提案切換（規則 E show before write 配套）。同步來源：Vincent5588 v1.3.29。|
| **v1.3** | **2026-05-11** | **規則 N 新增：雲盤 + git 紀律（single-writer policy）**。同步來源：Vincent5588 v1.3.30。|
| **v1.4** | **2026-05-11** | **規則 O 新增：Discovery Before Action（探勘優先）**。同步來源：Vincent5588 v1.3.31。|
| **v1.5** | **2026-05-11** | **規則 O v1.1：§O.4 Reference Discipline 新增**——引用 / 描述既有檔案 / entity / 路徑前必先 ls / grep verify canonical name + 實際狀態，不憑印象。同步來源：Vincent5588 v1.3.32。|
| **v1.6** | **2026-05-11** | **🔄 v1.1 longform-as-type 決策反轉**：把 longform 從「第 9 種 type」廢除，回到 8 種 type 體系。`atomize: false` 是 frontmatter marker 標記呈現方式，不影響 type 維度（永遠從 8 種挑）。同步來源：Vincent5588 v1.3.34。|
| **v1.7** | **2026-05-12** | **Phase 2 拆檔完成：Rules D-L + Heuristics 1-3 全移出 CLAUDE.md 主檔**；規則 D 補「英文技術名詞必加繁中說明 `Term（中文）`」；`Wiki操作文件/` 建立（wiki 維護檔移出根目錄）；`wiki/index.md` 移到根目錄；新建 `CLAUDE_versions.md` 成版本歷程 SSOT。同步來源：Vincent5588 v1.3.35 + v1.3.36。|
