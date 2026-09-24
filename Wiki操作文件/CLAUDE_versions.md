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
| **v1.8** | **2026-05-12** | **規則 P 新增：Cite-or-Die Cascade Citation**：codify「任何 vault 寫入動作前 LLM 必須在 chat 引用 [[Wiki_維護觸發規則]] §N 的 cascade 清單；無法引用 = 沒讀 = 必停下來讀」。**Root cause**：CLAUDE.md ⚡「⚠️ 新 session 開始必讀 [[Wiki_維護觸發規則]]」是被動文字，無 enforce 機制，LLM 跳過後使用者也看不出來。**設計理念**：把「我可能跳過」變成 **chat 中明顯 caller-verifiable 的動作**。**規則三角閉環**：規則 E（output 紀律：寫前先 show）+ 規則 O（input 紀律：執行前先探勘）+ **規則 P（process 紀律：cascade plan 寫出來給 caller 看）= 完整 input / output / process 三層 verifiable 紀律**。**改動 4 處**：(a) 新建 `wiki/rules/rule-P-cascade-citation.md`；(b) CLAUDE.md §10 加 1-row 速查；(c) CLAUDE.md ⚡ 新 session 熱身加 🚨 規則 P 提醒；(d) 主檔 §0 版本號 v1.7 → v1.8。**配套**：新建 `wiki/tools/lint.py`（generic 版含 cascade 完整性檢查）+ plugin v1.4.5 wiki-ingest Step 0 Cite-or-Die。同步來源：Vincent5588 v1.3.37。|
| **v1.9** | **2026-08-13** | **一次補齊四條規則 + 五條經驗法則 + 兩組工程紀律**。**新增規則**：**Q**（PARA project `_MOC` = SSOT，子目錄任何檔案異動都要回頭更新 `_MOC` + 上游索引；鎖定 / 登記單位是「**專案**」不是「檔」——只鎖你打算改的檔，`_MOC` 就落在「一定會寫、但鎖沒涵蓋」的縫裡）、**R**（`_MOC` / 含索引 README 的 `updated:` bump，比規則 H 更輕量高頻）、**S**（事實時效三態 timeless / snapshot / pointer——既有品質機制全在**檔案層**，沒有任何機制管**句子層**，`status: stable` 的檔裡可以躺著無日期的過期事實）、**T**（完成宣告必附逐項證據——防的不是「有沒有驗證」，而是「定了判準、宣告符合、但沒逐條對」）。**新增經驗法則**：4（YT 報告 fast-path）、5（promote 待解分兩型 + owner 共審；**age 不等於 trust**）、6（廠商內容 ingest 標立場：骨架 vs 工具置入）、7（AI 轉錄素材必逐項查證——它**讀起來完全不像不確定**，且會憑空生出「決策 / 行動項目」）、8（儀表板五問法：以使用者的問題重排，不是以資料結構呈現）。**主檔改動**：§6 加 Wikilink 語法紀律（含**附件類專條**——PDF / HTML 在 entity 內文一律 inline code，理由是「lint 會誤報 + 真理層分離」，**不是**「不 resolve」，錯的理由會讓規則被繞過）；§13 從單一鐵則擴成四條（新增鐵則 2 腳本路徑引用必 grep、鐵則 3 跨平台編碼 BOM + `encoding="utf-8"`、鐵則 4 整檔重寫先暫存再原子替換——**失敗點與破壞點可以不在同一步**）；§11 Quick Reference 加 6 row。**cascade**：`Wiki_維護觸發規則` 新增 §8.5 / §8.6（v1.1）。同步來源：Vincent5588 v1.3.39-v1.3.78 的通用部分（個人 / 本機 / 專案專屬內容一律排除）。|
| **v1.10** | **2026-09-24** | **新增規則 U（判定用預期必須可達且有鑑別力，Expectation Traceability）**：寫任何 rubric／測試／驗收判準前先追到產生它的路徑並確認可達，觀測到時也要能排除旁路／自證——**走不到＝假紅，分不出＝假綠**；新建 `wiki/rules/rule-U-expectation-traceability.md`。**新增經驗法則 9**（治理工具改動節流 ＋ 以人為尊：治理層一天最多改一次、等真的害到事才改、給人看的頁面只留結論）。**主檔改動**：§4 type 停用清單加入「別為單一內容偷懶開新 type」心法（`type` 詞彙的價值來自封閉，退化成第二個 tag 會讓 Dataview 過濾與 lint 檢查靜默失效）；§13 鐵則 3 補 **3c 行尾紀律**（雲端同步既有檔沿用原行尾、新建檔預設 LF、禁止行尾混用／裸 CR／BOM、寫前正規化優先於寫後偵測）；§11 Quick Reference 加 1 row。**規則檔更新**：`heuristic-4-yt-fastpath.md` 補「平台端易過期參數查表不查記憶」+「驗證探針必須真的執行（規則 U）」+ shell 展開陷阱提醒；`heuristic-5-promote-refinement.md` 補精煉 3（待解看是否為立論承重點）與精煉 4（`inlinks ≥ 1` 不代表值得獨立成頁）。同步來源：Vincent5588 v1.3.79–v1.3.92 的通用部分（個人 / 專案 / 本機專屬內容一律排除，含：規則 F 部署版本鎖、規則 G Quartz 覆蓋繼承、規則 V 專案開工兩閘門——三者經使用者確認後判定不屬本模板範疇，故不搬入）。|
