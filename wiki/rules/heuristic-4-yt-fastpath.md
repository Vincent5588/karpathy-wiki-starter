---
title: "經驗法則 4 — YT 報告 fast-path（yt-dlp + 本地 Whisper）"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-09-24
tags: [rule, heuristic, youtube, whisper, yt-dlp, workflow]
aliases: [heuristic-4, YT fast-path, 易過期參數查表]
---

# 經驗法則 4：YT 報告 fast-path

> **單支影片要中文報告 → 優先用 yt-dlp 抓內容 + LLM 直接產報告，跳過雲端服務的輪詢。**

## Why

雲端流程（建 notebook → 加 source → 等字幕 → 生成 → 輪詢 → 下載 → 潤稿）單支要 **5-15 分鐘**，慢在雲端來回。對**單支影片**，本地抓字幕／音檔再直接產報告只要 **2-4 分鐘**，而且純本地、中文直出（免「中文影片吐英文再翻回來」）。

## How（決策樹）

```
單支影片？
├─ 有字幕 → yt-dlp 抓字幕（zh-Hant / zh / en）→ 直接產報告        ← 最快 ~2-4 分
├─ 無字幕 → yt-dlp 抓音檔 + 本地 Whisper 轉錄 → 產報告            ← ~3-5 分
└─ 多支要跨來源綜合 / 想留 notebook 續聊 → 走雲端服務原路徑
```

**工具鏈**（需自行安裝）：

- `yt-dlp` — 抓字幕／音檔
- 本地 Whisper（Apple Silicon 可用 `mlx-whisper`，接近實時；其他平台用 `faster-whisper` 等）
- `ffmpeg` — 音檔轉檔

**關鍵指令**：

```bash
# 有字幕
yt-dlp --skip-download --write-auto-sub --sub-lang "zh-Hant,zh,en" <url>

# 無字幕：抓音檔（某些情況需指定 client 才拿得到串流）
yt-dlp -f bestaudio --extractor-args "youtube:player_client=android" \
  -x --audio-format mp3 -o "/tmp/aud.%(ext)s" <url>

# 本地轉錄（中文用 zh、英文用 en）
mlx_whisper /tmp/aud.mp3 --model mlx-community/whisper-large-v3-turbo \
  --language zh --output-format txt
```

### 🔴 平台端參數是會過期的值，不是定值

`player_client` 這類「繞過抓取限制」用的參數，服務端會不定期調整——今天能用的值明天可能失敗，也可能反過來。**不要把它寫死在指令範例裡當成永久答案**。

**做法**：另外維護一份「日期 + 實測結果」的小表，撞牆時**先查表**、從最近一次成功的值開始試，不要照抄範例裡的舊值，也不要背一個固定的嘗試順序——**順序本身也是會過期的值**。

⭐ **心法：把一個會變的值寫進規範本體，等於規範每隔一段時間就自動變成錯的。** 快速變動的事實要用「帶日期的觀測記錄」呈現，不要用單一的現在式陳述（同規則 S，`wiki/rules/rule-S-fact-freshness.md`）。

### 🔴 驗證「能不能抓」的探針必須真的執行（規則 U）

快篩多個候選參數時，容易踩兩種相反方向的錯：

| 探針寫法 | 錯法 | 為什麼 |
|---|---|---|
| 只印出格式清單、不下載 | **假綠** | 只證明「解析得到」，不代表真的抓得到——某些設定能列出格式，實際下載卻被擋 |
| 只切一小段測試 | **假紅** | 失敗可能卡在「切片」那一步，跟參數能不能下載無關，會誤判一個其實可行的參數 |

⭐ **測「能不能抓」就要真的抓一次完整檔案**（或至少確認落地檔案存在且大小合理），不能只看「有沒有報錯」（詳見規則 U，`wiki/rules/rule-U-expectation-traceability.md`）。

⚠️ **shell 陷阱提醒**：用變數組合命令列參數時，不同 shell 對「未加引號的變數展開」處理不同（有的會自動拆字，有的不會）——命令送出前，先確認參數真的照你以為的樣子被拆開，再去懷疑工具本身。

**必守**：

- 報告仍照 `youtube-to-notebooklm` skill 的字數階梯 + 段落結構 + 規則 D／J（英文 quote 加中譯、專有名詞中英對照）。
- 寫進 `00-Inbox/<標題>.md`，frontmatter 標明 `source_type`（例如 `yt-dlp+whisper`）與 skill 版本變體。
- 本地轉錄**沒有人工校對**，專有名詞極易出錯 → 報告尾部加辨識誤差警告，**ingest 前必照經驗法則 7 逐項查證**。

## 何時**不**用 fast-path

- 多支影片要跨來源綜合對比 → 雲端服務的強項。
- 想保留一個可以續聊的 notebook。
- 影片無字幕且本機轉錄太慢（非 Apple Silicon）→ 評估雲端自帶 ASR。

## 相關

- `youtube-to-notebooklm` skill — 本 fast-path 是其變體，雲端為原路徑
- 規則 K（`wiki/rules/rule-K-raw-precheck.md`）— raw 預檢分流，YT URL 先判性質
- 經驗法則 7（`wiki/rules/heuristic-7-transcript-verification.md`）— **本法則大量產出的正是它要查證的素材**

---

← 回到 `CLAUDE.md` §10
