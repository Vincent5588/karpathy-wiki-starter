---
name: youtube-to-notebooklm
description: |
  將 YouTube 影片產成繁體中文分析報告，過 humanizer 潤飾後寫進 vault 的
  00-Inbox 等待 wiki-ingest 處理。單支影片優先走 yt-dlp fast-path（經驗法則 4），
  多支跨來源綜合才送進 NotebookLM。
  當使用者貼出 YouTube URL 並說「YT 分析」「YouTube 報告」
  「這個 YT 給 NotebookLM」「ingest 這個影片」「YT analyze」時，
  立即啟動此 Skill。報告字數依影片長度 5-tier 階梯化（800 字至 8000 字），重點 8-16 條，延伸思考 3-5 條，
  10 節（v1.4 起含全片逐段摘要與查證表）。
  強制繁中 + 英文專有名詞中英對照（vault 規則 J）
  + 英文 quote 加繁中翻譯（vault 規則 D）。
---

# youtube-to-notebooklm v1.4.0 — 階梯化 + CLI 優先 + 單支 fast-path + 全片逐段摘要與查證表

> **v1.4.0 於 2026-10-18**（vault 規則 K v2）：報告改照 REPORT_PROMPT **v1.4**——8 節 → **10 節**（第 9 節全片逐段摘要、第 10 節查證表）。NotebookLM 路徑的查證表先列「待查證」，Step 5.5 後由 Claude 逐項查完；Web Clipper 空殼來的報告另存 `<空殼檔名>_報告.md`＋`supersedes:`（規則 K v2 §K.2，原剪報不動）。

> **v1.3.2 patch 於 2026-10-09**：新增「路徑選擇」——單支影片預設走 yt-dlp fast-path（經驗法則 4），NotebookLM 路徑保留給多支跨來源綜合；Step 1 的 yt-dlp 由「可選」改為預設。

> **v1.3.1 patch 於 2026-05-11**：Step 3 改用 CLI `nlm source add --youtube` 取代 MCP `source_add(source_type: url)`——MCP 對 YouTube URL 必失敗（ingest [[Live Artifacts (Cowork)]] 影片 `1nfDHwBHn88` 時兩次 MCP call 都 error: "Could not add url source"，URL public 確認可訪問，改用 CLI `--youtube` flag 立刻成功）。MCP 的 `source_type: url` 設計上不區分一般網頁 vs YouTube，CLI 的 `--youtube` flag 走專門路徑。
>
> **v1.3 拍板於 2026-05-07（REPORT_PROMPT.md），2026-05-09 metadata 補同步**。經 11 次測試 v1.2 定案 1200-2500，但對 3 小時 Naval 訪談類長片 over-compressed，改為**字數依影片長度 5-tier 階梯化**（< 10 min 800-1500 / 10-30 min 1500-2500 / 30-60 min 2500-4000 / 60-120 min 4000-6000 / > 120 min 5000-8000）。重點 8-16 / 延伸 3-5 維持固定，長影片靠擴展單條深度而非加條數。Source of truth：`references/REPORT_PROMPT.md`。
>
> 11 次測試共識：
> - NotebookLM 8.1 URL 100% 不可信，humanizer 階段強制覆蓋（11 次都中）
> - NotebookLM puffy 標題（「【深度分析報告】...新紀元」），humanizer 階段強制覆蓋成影片原標題
> - 報告結構結束就結束（v1.4 起 10 節），**不放尾段 metadata**（處理清單 / NotebookLM 後續 / 測試備註）—— 使用者要 ingest 處理清單時手動加
> - **MCP source_add 對 YouTube URL 必失敗**（v1.3.1 確認）—— 預設走 CLI 路徑

## 路徑選擇（v1.3.2 新增）

| 情境 | 路徑 | 耗時 |
|---|---|---|
| **單支**，有字幕 | yt-dlp 抓字幕 → 直接產報告 | 約 2–4 分 |
| **單支**，無字幕 | yt-dlp 抓音檔 + 本機 Whisper 轉錄（Apple Silicon 用 mlx-whisper，其他電腦用 faster-whisper 等）→ 產報告 | 約 3–5 分 |
| **多支**跨來源綜合，或想留 notebook 續聊 | 下方 6 步驟（NotebookLM） | 5–15 分 |

fast-path 的指令、`player_client` 試序與 dated 實測表，**一律查 [[heuristic-4-yt-fastpath]]**（client 會過期，本檔不存副本）。
報告格式兩條路徑相同：REPORT_PROMPT v1.4（5-tier 字數、10 節含全片逐段摘要與查證表、規則 D／J）。本地轉錄沒有 ASR 校對，第 10 節查證表要把專有名詞逐項查完（[[heuristic-7-transcript-verification]]）。fast-path 的 frontmatter 與檔名照 `references/OUTPUT_TEMPLATE.md`，只有 `source_type` 照實改寫成 `yt-dlp-subtitle`（抓字幕）或 `yt-dlp+whisper`（本機轉錄）。
以下 6 步驟是 **NotebookLM 路徑**。

## 為什麼存在

YouTube 上有大量技術 / 商業 / 教學內容值得放進 vault 知識庫，但**手動看完一支 30 分鐘影片 + 寫摘要 + 整理重點 = 1-2 小時**。單支影片走 yt-dlp fast-path（2–4 分鐘）；多支跨來源綜合改用 NotebookLM（Google 旗下的 AI 研究工具）抓字幕 + 綜合分析 → 5-15 分鐘產出結構化繁中報告。

這個 skill 把流程封裝起來：你貼 URL → 我跑 6 步驟 → vault 的 `raw/` 多一個待 ingest 的 markdown。之後跑 wiki-ingest 拆成 entity，知識庫就長大一點。

## 觸發詞

任何包含 YouTube URL 的訊息搭配下列任一片語：

| 使用者說 | 啟動 |
|---------|------|
| 「YT 分析」/ 「YouTube 分析」 | ✅ |
| 「YT 報告」/ 「YouTube 報告」 | ✅ |
| 「這個 YT 給 NotebookLM」 | ✅ |
| 「ingest 這個影片」 | ✅ |
| 「YT analyze」/ 「YT 給我做報告」 | ✅ |
| 純貼 URL 不講話 | ❌ 主動問「要做 YT 報告嗎」 |

支援多支 URL 一次貼進來，全部丟到**同一個 NotebookLM notebook**做跨來源綜合報告（決策 v1：A）。

## 標準工作流（6 步驟）

依 vault CLAUDE.md 規則 E（show before write）執行。NotebookLM 路徑估計 5-15 分鐘，期間我會用 sleep poll 等 NotebookLM。

### Step 1｜URL 驗證 + 取 stub

對每個 URL：

- 確認是 `youtube.com/watch?v=...` 或 `youtu.be/...` 格式
- 取 video ID（11 字元）

**yt-dlp 預檢（預設，本機已裝）**：
- 跑 `yt-dlp --skip-download --print "%(title)s|%(channel)s|%(duration_string)s|%(upload_date)s" <url>` 抓 metadata
- 跑 `yt-dlp --skip-download --list-subs <url>` 確認有字幕
- 用第一支影片標題前 30 字元做 stub

**如果 yt-dlp 不可用（退路）**：
- 直接用 video ID 當 stub
- 影片標題、頻道、時長等 metadata 改在 step 3 之後從 `source_describe` 拿
- 不必預檢字幕：source_add 完後 NotebookLM 若抓不到字幕，source_describe 會看出來（summary 會空 / 短）

### Step 2｜建 NotebookLM notebook

```
mcp__notebooklm-mcp__notebook_create
  name: "YT-{YYYYMMDD-HHMM}-{stub}"
```

例：`YT-20260507-1430-Anthropic_Skill教學`

記下 `notebook_id`，後續所有操作都靠它。

**Auth 失敗時**：訊息會出現「authentication」字樣 → 告訴使用者「跑 `nlm login`」並停下，**不要自己嘗試重連**（避免無限 retry）。

### Step 3｜加 source（v1.3.1：CLI 優先，2026-05-11 修正）

**對每個 YouTube URL，優先用 CLI**（透過 Bash tool）：

```bash
nlm source add <notebook_id> --youtube "<youtube URL>" --wait
```

範例：

```bash
nlm source add 29cf6898-8129-4c20-bd07-07d9abc2e37b \
  --youtube "https://www.youtube.com/watch?v=1nfDHwBHn88" --wait
```

回應會給 `Source ID: <uuid>`，記下備用（後續 source_describe 等可用）。

**為什麼 CLI 不是 MCP**：

`mcp__notebooklm-mcp__source_add` 的 `source_type: "url"` 對 YouTube URL **必失敗**（2026-05-11 觀察兩次 call 都 error: "Could not add url source"，URL public 確認可訪問）。CLI 的 `--youtube` flag 走專門路徑能正常處理。MCP `source_type` 沒有 `youtube` 選項——這是 MCP 設計缺口，不是 auth 或 rate limit 問題。

**Fallback**（罕見場景）：

如果環境沒裝 nlm CLI（譬如 Cowork / Claude.ai web 環境）：

1. 先試 MCP `source_add(source_type: "url")`——對非 YouTube URL（普通網頁 / Google Drive）有效
2. 對 YouTube URL，**不要重試 MCP**，告訴使用者「環境沒裝 nlm CLI，需手動到 NotebookLM web UI 加 source」並停下

**Auth 失敗時**（CLI 跟 MCP 都會發生）：

跑 `nlm login --check` 驗證。如果失敗，告訴使用者「跑 `nlm login`」並停下，**不要自己嘗試重連**（避免無限 retry）。

NotebookLM 會在背景抓字幕（auto-generated 或人工字幕都吃）。**字幕缺失就抓不到內容** → 報告會空。`--wait` flag 會等到字幕處理完成才回（典型 < 30 秒，4 小時影片約 30 秒，韓文等需翻譯字幕 < 1 分鐘）。

### Step 4｜啟動 report 生成

```
mcp__notebooklm-mcp__studio_create
  notebook_id: <ID>
  artifact_type: "report"
  custom_prompt: <讀 references/REPORT_PROMPT.md 全文>
```

把 [`REPORT_PROMPT.md`](references/REPORT_PROMPT.md) 的全部內容當 `custom_prompt` 傳入。**不要簡化或改寫 prompt**，那是這個 skill 的核心 — 確保報告品質一致。

### Step 5｜輪詢 + 下載

```python
# 每 30 秒 poll 一次，最多等 20 分鐘
for _ in range(40):
    status = mcp__notebooklm-mcp__studio_status(notebook_id=...)
    if status == "done": break
    sleep(30)
```

完成後：

```
mcp__notebooklm-mcp__download_artifact
  notebook_id: <ID>
  artifact_type: "report"
  output_path: "/tmp/yt_report_{video_id}.md"
```

拿到 markdown 內容（字串），先存 `/tmp/`，下一步處理完才寫進 vault。

### Step 5.5｜Humanizer 後處理（**強制**）

NotebookLM 產出的報告有典型 AI 寫作痕跡（significance inflation / promotional 形容詞 / `-ing` 肥句 / negative parallelism / rule of three / `**bold:**` 列點開頭）。報告寫進 vault 前**必須**先過 [[humanizer]] skill 潤飾。

執行：

```
Skill tool: humanizer
```

skill 載入後依其指引：
1. 讀 step 5 下載的報告內容
2. 套 29 個 AI pattern 全掃過一輪
3. 維持 vault 規則 D（英文 quote 加繁中翻譯）跟 規則 J（英文專有名詞中英對照）
4. 維持 10 節結構（REPORT_PROMPT v1.4 規定），標題逐字 `## 1. 影片基本資訊` 到 `## 10. 查證表`
5. 不要在 humanize 過程移除：時間戳、URL、frontmatter 欄位

draft → audit → final 三輪走完，把 final 版用在 step 6。

**查證（v1.4 新增，強制）**：NotebookLM 交出的第 10 節查證表「查證結果」都是 `待查證`。寫進 vault 前逐項查完（WebSearch、官方網站、yt-dlp metadata），改成 `正確`／`更正為「…」`／`查無` 並補出處；正文同步改成更正後寫法、查無的第一次出現加「（查無）」。格式照 vault 規則 K §K.3（`wiki/rules/rule-K-raw-precheck.md`）。**留下任何一格 `待查證` 就不准寫進 vault。**

### Step 6｜寫進 vault

依 [`references/OUTPUT_TEMPLATE.md`](references/OUTPUT_TEMPLATE.md) 格式，寫到：

```
00-Inbox/{video_title}.md
```

檔名規則（**v1 修正**）：
- **單支影片**：用影片標題當 filename（譬如 `Claude Code + NotebookLM + Obsidian = GOD MODE.md`）
- **多支影片**：用 notebook 標題當 filename（譬如 `Claude Code 與 Obsidian 究極研究工作流.md`）
- 移除 `:`、`/`、`\`、`*`、`?`、`<`、`>`、`|`、`"` 等 macOS / 跨平台不允許字元
- `+`、`=`、`&`、`空格` 都允許保留
- 不加日期前綴（日期已在 frontmatter `created`/`updated`）
- 不加 `youtube_` 前綴或 `_stub` 後綴（影片標題本身有辨識度）
- **Web Clipper 空殼來的**：檔名 `<空殼檔名>_報告.md`，frontmatter 加 `supersedes: "[[<空殼檔名>]]"`（規則 K v2 §K.2；空殼本身不動）
- **同名已存在就停**，回報「已有：<檔名>」——不加 `(2)`（v1.4 起；同一支影片兩份報告會被去重檢查報重複）
- 寫進 vault 前自己對一次格式：10 節標題逐字、第 10 節查證表的表頭與結果寫法（規則 K §K.3）、沒有任何 `待查證`；對不上就改完再寫

**Auto Embed plugin 整合**（target vault 已裝）：報告 header 後**必須**加一行 image syntax 觸發內嵌播放器：

```markdown
![](https://www.youtube.com/watch?v={video_id})
```

注意：必須是 `![]()` 不是 `[]()` — Auto Embed plugin 偵測 image syntax 才會渲染 iframe。多支影片就多行。

**修正 NotebookLM 的 placeholder**：報告產出時 `8.1 影片連結` 段落會出現 `https://www.youtube.com/watch?v=VIDEO_ID` 這種 placeholder（NotebookLM 不知道實際 URL）。下載後在 step 6 用 sed 替換成實際 URL：

```bash
sed -i '' "s|watch?v=VIDEO_ID|watch?v={actual_video_id}|g" /tmp/yt_report_*.md
```

多支影片時這招會出問題（無法區分哪個 placeholder 對應哪個 URL）→ 這時改用 prompt 內明確列出 URL 給 NotebookLM。

> 路徑用 vault-relative `00-Inbox/`，**不分子目錄**（v1.3.14 已廢 `raw/`，使用者偏好平鋪）
>
> - 規則 A：00-Inbox/ 內容**唯讀**，但 LLM 新寫入後使用者批准就會被 ingest 路由
> - vault v1.3.12 起已停寫 `wiki/log.md`，改用 `wiki/daily/YYYY/MM/YYYY-MM-DD.md`

frontmatter 必須包含（v1.4 起與 fast-path、外部對帳同一種格式；欄位全文見 OUTPUT_TEMPLATE）：
- `type: youtube-report`（v1.4 前是 `youtube_report`，既有舊檔不改）
- `title`／`source`／`youtube_url`／`channel`／`duration`／`published`／`generated_at`
- `source_type: notebooklm`
- `skill_version: youtube-to-notebooklm-1.4.0`
- `status: draft`
- `youtube_urls: [...]`
- `notebook_id: <NotebookLM ID>`
- `notebook_name: <name>`
- `created` / `updated`: 今天台北日期（用 `TZ='Asia/Taipei' date "+%F"`）
- `tags: [youtube, raw, pending-ingest]`

然後 append 一筆到 `wiki/daily/YYYY/MM/YYYY-MM-DD.md`（當日 daily）的「## 📥 00-Inbox 新增」段（沒這段就建）：

```markdown
- [[{filename}|{影片標題}]] — 由 [[youtube-to-notebooklm]] skill 從 YT 影片 {YT_URL} 產生 NotebookLM 報告。Notebook: `{notebook_name}`
```

時間用台北時區（vault CLAUDE.md 時區規範）。

## 完成後告訴使用者

```
✅ YT 報告完成
- 檔案：[[raw/{YYYY-MM-DD}_youtube_{stub}]]
- NotebookLM notebook：{name}（保留，可直接到 web UI 互動聊）
- 影片：{title}（{duration}）

下一步：
1. 開檔看一輪、改正錯誤
2. 想 ingest 時說「ingest raw/{filename}.md」我就跑 wiki-ingest
```

## 重要約束

### 報告語言與格式

- **全文繁體中文**（vault 是繁中環境）
- **英文專有名詞中英對照**：第一次出現英文用語時加 `English（中文說明）` 或 `中文（English）`（vault 規則 J）
- **英文 quote 必加繁中翻譯**：原文 quote 下方緊接著繁中 quote（vault 規則 D）
- 純技術名詞（命令、設備型號、廠商名）不必中譯

### 不要做的事

- ❌ 不要簡化 REPORT_PROMPT.md 內容傳給 NotebookLM（會降低報告品質）
- ❌ 不要報告完成後自動觸發 wiki-ingest（決策 v1：A — 留給使用者看過 raw 再決定 ingest 方向）
- ❌ 不要刪掉 NotebookLM notebook（決策 v1：A — 保留供使用者後續互動）
- ❌ 不要要求使用者打 cmd（能在 chat 內完成的就在 chat 內）

### 多支 URL 處理

全部進**同一個** notebook，產**一份**綜合報告（決策 v1：A）。NotebookLM 強項在跨來源綜合 — 把同主題的 5 支影片丟進去，能做到單支影片做不到的對比 / 印證 / 補充。

如果使用者明確要求「分開」每支一份報告 → 為每支建獨立 notebook、跑獨立 report、寫獨立 raw 檔。

## NotebookLM 限制與踩雷

| 問題 | 處置 |
|------|------|
| **MCP `source_add(source_type: "url")` 對 YouTube URL 失敗**（v1.3.1 確認）| **預設走 CLI `nlm source add --youtube`**——MCP 路徑對 YouTube URL 必 error: "Could not add url source"，不是 auth 問題。Step 3 v1.3.1 已改用 CLI 優先 |
| 影片無字幕 | NotebookLM 報告會空。Step 1 用 yt-dlp 檢查 `--list-subs`；無字幕時改走 fast-path 的本機 Whisper 轉錄，不要硬丟 NotebookLM |
| 影片設成 private / 已下架 | source_add 會 fail。把 fail 的 URL 跳過、其他繼續 |
| Auth 過期 | `nlm login`，不要自動重連。先用 `nlm login --check` 驗證 |
| 報告超過 20 分鐘還沒好 | 跳出 poll loop、告訴使用者 notebook ID，請他到 web UI 看狀態 |
| 多支影片合計超過 NotebookLM source 上限 | 切批處理（每 batch ≤ N 支，N 看當下版本上限） |
| 非英文 source（韓文 / 日文 / 簡中）NotebookLM 100% 給英文報告 | 觀察自 [[一天內開發業務自動化程式 Claude Code AI 編碼三大秘訣]] ingest（韓文影片）。humanizer 階段必須兜底翻譯成繁中。英文 / 繁中 source 通常正常給繁中 |

## 事後檢查（self-check）

寫完報告後跑：

```bash
# 確認檔案有寫進去（檔名就是影片標題）
ls -la "00-Inbox/<影片標題>.md"

# 確認今天的 daily 有記錄
tail -5 "wiki/daily/$(date +%Y/%m/%F).md"
```

如果報告內容明顯品質有問題（< 1000 字 / 結構不完整 / 沒按 prompt 走）→ 標記 frontmatter 加 `quality: poor`，daily log 記一筆「此次 NotebookLM 輸出品質不佳，原因 XX」。累積觀察會餵回去調 REPORT_PROMPT.md。

## Compounding 飛輪

每跑完一次 skill，自我反思：

- 這次 prompt 哪段被 NotebookLM 忽略 / 解釋錯？→ 改 REPORT_PROMPT.md
- 這次 stub 命名被截斷 / 衝突？→ 改 stub 規則
- 這次有什麼新雷？→ 寫進本檔「踩雷」段

每月或每跑 5 次後 review 一次本檔，把規律往 vault CLAUDE.md 提升。
