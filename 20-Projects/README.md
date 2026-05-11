# 20-Projects — 進行中的專案

> **PARA 第 2 層：有截止日、做完就結束的具體工作**

## 📌 用途（給人）

放**有明確目標 + 有結束時間**的工作資料。專案結束後（成功或放棄）就搬去 `50-Archive/`，不留在這裡占空間。

**典型內容**：
- 準備某場演講 / 簡報
- 完成某門課（有結業日期）
- 寫一篇論文 / 部落格文
- 規劃一次旅行
- 蓋一個側專案到 v1.0

## ✅ 何時放東西進來

每個專案開一個子資料夾：

```
20-Projects/
├── 2026-Q1-簡報-某主題/
│   ├── README.md            ← 專案目標 + 截止日
│   ├── outline.md
│   └── 參考資料/
├── 學完-AWS-認證-2026-06/
└── 部落格-LLM 系列-完成-3-篇/
```

子資料夾**命名建議**：含「日期 / 目標 / 完成條件」。看一眼就知道狀態。

## 🤖 LLM 行為規範

- ✅ LLM 可從 `00-Inbox/` 把專案相關 raw 路由到對應 `20-Projects/<X>/` 子分類
- ✅ ingest 時可從這裡的檔抽 entity 到 `wiki/entities/`（依使用者明確指定）
- ✅ 專案完成後使用者明確說「歸檔 X」→ LLM 可移到 `50-Archive/`
- ❌ **不刪除、不修改既有檔案內容**（規則 C）
- ❌ 不自動判定「這專案結束了」搬去 archive——使用者決定
- ❌ 不重命名子資料夾（影響既有 wiki-link）
- ❌ **不主動掃描** 20-Projects/ 找東西 ingest（規則 C；使用者明確指定才掃）

## 📥 Longform 路由（atomize: false）

從 `00-Inbox/longform/` 路由過來的 raw（譬如「Q1 簡報事後回顧長文」「某專案 lessons learned 完整版」）可以放：

```
20-Projects/<專案名>/
├── retrospective.md     ← longform 心得
├── lessons-learned.md   ← longform 教訓總結
└── ...
```

→ LLM 看 `atomize: false` 時不抽 atomic entity，只搬檔到此 + 寫 daily log。詳見 [[CLAUDE]] §3.1.1。

## 🆚 跟其他層比較

| 層 | 跟 20-Projects 差異 |
|---|---------------------|
| 30-Areas | 長期沒終點 vs **20 有截止日** |
| 50-Archive | 已完成 / 放棄 vs **20 進行中** |

**判斷準則**：如果你能說「做完 X 就算結束」→ 20-Projects；如果是「我永遠都會做這個」→ 30-Areas。

## 💡 子資料夾結構建議

每個專案下：

```
<專案名>/
├── README.md       ← 目標、截止日、完成條件
├── outline.md      ← 大綱
├── notes/          ← 你的工作筆記
├── sources/        ← 收集的參考資料（或讓 LLM 路由到 40-Resources）
└── outputs/        ← 最終產出
```
