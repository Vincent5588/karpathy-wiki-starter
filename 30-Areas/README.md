# 30-Areas — 長期關注的領域

> **PARA 第 3 層：你會「一輩子持續關注」、沒有終點的主題**

## 📌 用途（給人）

放**長期維護、沒有截止日**的主題資料夾。Areas 是你選擇要持續投入的人生面向，跟 Projects 不同的是——**它永遠不會「完成」**。

**典型內容**：
- 健康（運動 / 飲食 / 睡眠紀錄）
- 工作角色（你目前職位的長期知識）
- 理財（投資組合追蹤 / 預算）
- 學習領域（你的長期興趣，譬如「AI/LLM」「攝影」）
- 家庭 / 關係維護

## ✅ 何時放東西進來

每個 area 開一個子資料夾：

```
30-Areas/
├── health/
│   ├── 運動紀錄.md
│   └── 體檢報告/
├── work-role-PM/
├── investing/
└── learning-LLM/
```

跟 20-Projects 不同：area 子資料夾**不需要日期 / 完成條件**，命名就是主題名。

## 🤖 LLM 行為規範

- ✅ LLM 可從 `00-Inbox/` 把 area 相關 raw 路由到對應 `30-Areas/<area>/<子分類>/`
- ✅ ingest 時可從這裡的檔抽 entity 到 `wiki/entities/`
- ✅ 使用者說「這個 area 我不再關注了」→ 提案搬 `50-Archive/`
- ❌ **不刪除、不修改既有檔案內容**（規則 C）
- ❌ 不自動把「久未更新的 area」搬去 archive——area 本來就可能靜默
- ❌ 不重命名 area 子資料夾

## 🆚 跟其他層比較

| 層 | 跟 30-Areas 差異 |
|---|------------------|
| 20-Projects | 有截止日 vs **30 沒終點** |
| 40-Resources | 別人寫的參考 vs **30 是你的持續投入** |
| 50-Archive | 不再活躍 vs **30 仍在投入** |

**判斷準則**：問自己「我會在 5 年後還在做這件事嗎？」→ 是 → 30-Areas；否 → 20-Projects。

## 💡 何時把 Area 轉成 Archive

- 換工作 → 舊的 `work-role-X/` 搬 50-Archive
- 不再關注某主題 → 直接 archive，未來想回頭仍找得到
- 該領域成為「歷史記錄」而非「持續維護」

## 💡 跟 wiki/entities/ 的關係

30-Areas 裡的檔可作為 LLM ingest 的 source。譬如：
- `30-Areas/learning-LLM/某篇心得.md` → LLM 抽出 `wiki/entities/learning/concept/某觀念.md`
- area 內檔保留為深入閱讀資料，wiki entity 是精煉版
