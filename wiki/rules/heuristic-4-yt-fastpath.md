---
title: "經驗法則 4 — YT 報告 fast-path（yt-dlp + 本地 Whisper）"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-08-13
tags: [rule, heuristic, youtube, whisper, yt-dlp, workflow]
aliases: [heuristic-4, YT fast-path]
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
