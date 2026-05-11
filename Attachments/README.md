# Attachments — 圖片 / PDF / 二進位附件

> **vault 內所有非 markdown 檔的統一存放區**

## 📌 用途（給人）

放**圖片、PDF、影片、二進位附件**。Markdown 檔內用相對路徑引用，譬如：

```markdown
![截圖說明](Attachments/some-source/01-架構圖.png)
```

## 🗂 子資料夾規範（依 [[CLAUDE]] 規則 I）

每個來源（raw / entity）對應一個子資料夾：

```
Attachments/
├── <source-basename>/          ← 對應某個 raw / entity
│   ├── 01-架構圖.png
│   ├── 02-流程說明.png
│   └── 03-結果截圖.jpg
├── youtube-某影片標題/
│   ├── 01-thumbnail.jpg
│   └── 02-關鍵畫面.png
└── article-某文章/
    └── 01-原圖.png
```

**子資料夾命名**：raw / entity 的 basename（kebab-case 縮短版）

**檔案命名**：`<NN>-<short-desc>.<ext>`
- `NN`：兩位數序號（01, 02, ...）
- `short-desc`：圖片用途的中文短描述
- 範例：`01-cmux 介面截圖.png`

## 🤖 LLM 行為規範

- ✅ ingest 含外部圖的 raw 時，**必須下載到本地**（依規則 I）：
  ```
  raw 內 ![alt](https://外部 URL) 
       ↓
  下載到 Attachments/<source>/<NN>-<desc>.<ext>
       ↓
  entity 引用改為 ![alt](Attachments/<source>/<NN>-<file>.ext)
  ```
- ✅ web-restricted 環境（Cowork / Claude.ai 無法直接下載）→ 產 `outputs/download_*.sh` 腳本給使用者執行
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

## 💡 子資料夾不需 README

Attachments 子資料夾是**機器產生**的，不需要 README。要描述用途 → 在引用該圖的 entity 內寫。
