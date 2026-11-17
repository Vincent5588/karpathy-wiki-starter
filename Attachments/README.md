---
title: "Attachments — 圖片 / PDF / 二進位附件"
type: artifact
status: active
tags: [attachments, readme]
created: 2026-05-11  # 依 git 第一次加入的日期
updated: 2026-11-17
---

# Attachments — 圖片 / PDF / 二進位附件

> **vault 內所有非 markdown 檔的統一存放區**

## 📌 用途（給人）

放**圖片、PDF、影片、二進位附件**。Obsidian 已預設：貼上或拖進來的新附件會放到這裡（設定 → 檔案與連結 → 附件資料夾路徑）。

## 🗂 結構：`<分類>/<來源>/` 兩層（依 [[CLAUDE]] 規則 I）

```
Attachments/
├── README.md                     ← 根層只放這份 README 與分類夾
├── learning/                     ← 分類：跟 40-Resources/ 的分類同一套
│   ├── <source-basename>/        ← 對應某個 raw / entity
│   │   ├── 01-架構圖.png
│   │   └── 02-流程說明.png
│   └── youtube-某影片標題/
│       └── 01-關鍵畫面.png
└── work/
    └── article-某文章/
        └── 01-原圖.png
```

- **分類**：主題或專案，名稱跟 `40-Resources/` 的分類同一套；用過的就沿用，不開同義詞
- **來源夾命名**：raw / entity 的 basename（縮短版）
- **檔案命名**：`<NN>-<short-desc>.<ext>`——`NN` 兩位數序號、`short-desc` 中文短描述，例如 `01-cmux 介面截圖.png`
- 🔴 **根層不放零散檔案**：直接貼在根層的圖＝待分類，整理時請 AI 歸到分類夾

## 🤖 LLM 行為規範

- ✅ ingest 含外部圖的 raw 時，**必須下載到本地**（規則 I）：
  ```
  raw 內 ![alt](https://外部 URL)
       ↓
  下載到 Attachments/<分類>/<source>/<NN>-<desc>.<ext>
       ↓
  entity 引用改為 ![alt](Attachments/<分類>/<source>/<NN>-<file>.ext)
  ```
- ✅ 路徑含空白或全形括號時，引用改用 `![[檔名]]`
- ✅ 搬附件一律在 Obsidian 裡搬（檔案列表拖曳或右鍵移動），連結才會自動改
- ✅ 不能連外下載的環境（Cowork、對話分頁、Claude.ai）→ 產 `outputs/download_*.sh` 腳本給使用者執行
- ❌ **不直接引用外部 CDN URL**——原作者刪文 / 換 domain 後圖會壞
- ❌ 不刪 attachments（即使對應 entity 已刪）——可能有別處引用

## 💡 為什麼必須本地化

| 風險 | 後果 |
|------|------|
| 外部 CDN 連結會壞 | 原作者刪文 → 圖永遠失效 |
| 部署成靜態網站 | 不依賴外部站 = 部署可靠、離線可看 |
| vault 不自包含 | 備份 / 搬家時得另外處理外部資源 |

## 💡 例外條款

- **純裝飾圖**（網站 banner / footer logo）可省略
- **太大 / 版權敏感的圖** 只放原檔連結 + 註明「原檔有圖」
- **網路圖示截圖**（譬如別家 app 的官方 logo）→ 看版權
- **既有附件不另開搬遷工程**：新下載的照新結構放；舊的改到時再順手搬

## 💡 子資料夾不需 README

Attachments 子資料夾是**機器產生**的，不需要 README。要描述用途 → 在引用該圖的 entity 內寫。
