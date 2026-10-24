# Output Template — `00-Inbox/<影片標題>.md`

> Skill 寫進 `00-Inbox/` 的 markdown 檔長這樣（檔名直接用影片標題，不加日期前綴）。
> 變數用 `{{xxx}}` 標記，實作時替換成實際值。

***

```markdown
***
type: youtube_report
source_type: notebooklm
status: draft
youtube_urls:
{{#each url}}
  - {{url}}
{{/each}}
notebook_id: {{notebook_id}}
notebook_name: {{notebook_name}}
notebook_url: https://notebooklm.google.com/notebook/{{notebook_id}}
artifact_id: {{artifact_id}}
video_titles:
{{#each title}}
  - "{{title}}"
{{/each}}
created: {{YYYY-MM-DD-Taipei}}
updated: {{YYYY-MM-DD-Taipei}}
generated_at: "{{YYYY-MM-DD HH:MM Taipei}}"
humanized_at: "{{YYYY-MM-DD HH:MM Taipei}}"
tags: [youtube, raw, pending-ingest]
skill: youtube-to-notebooklm
skill_version: v1
post_processing: humanizer
***

# {{第一支影片標題（多支則用 notebook 主題標題）}}

> 由 [[youtube-to-notebooklm]] skill 產生於 {{YYYY-MM-DD HH:MM Taipei}}，[[humanizer]] 後處理於 {{YYYY-MM-DD HH:MM Taipei}}。
> 來源頻道：{{channel}} — 時長 {{duration}}
> NotebookLM Notebook：[{{notebook_name}}](https://notebooklm.google.com/notebook/{{notebook_id}})
> 狀態：draft，待 [[wiki-ingest]] 處理

{{#each video}}
![]({{url}})
{{/each}}

***

{{Humanizer 後的 NotebookLM 報告 markdown 內容（8 節結構，照 REPORT_PROMPT.md 走，且 8.1 段 VIDEO_ID placeholder 已替換為實際 URL，AI 痕跡已移除）}}
```

> 版本歷程：
> - **v1**（2026-05-07 初版）：字數 2000-5000，含完整 metadata（處理清單 / NotebookLM 後續 / 測試備註）→ 太冗長
> - **v1.1**（2026-05-07）：字數 800-1500，**完全移除尾段 metadata**（8 段結構結束就結束）→ 使用者反饋偏簡，深度不夠
> - **v1.2**（2026-05-07）：字數 **1200-2500**，重點 **8-16** 條，延伸思考 **3-5** 條，數據 **4-6** 條，引言 **3-4** 條。**維持 v1.1 「無尾段 metadata」決策**
> - **v1.3**（2026-05-07 寫入 REPORT_PROMPT.md / 2026-05-09 metadata 補同步，現行）：字數改 **5-tier 階梯化**（< 10 min 800-1500 / 10-30 min 1500-2500 / 30-60 min 2500-4000 / 60-120 min 4000-6000 / > 120 min 5000-8000），重點 / 延伸 / 數據 / 引言維持 v1.2，長影片靠擴展單條深度而非加條數

## 變數替換對照表

| 變數 | 來源 | 範例 |
|******|******|******|
| `{{YYYY-MM-DD-Taipei}}` | `TZ='Asia/Taipei' date "+%F"` | `2026-05-07` |
| `{{YYYY-MM-DD HH:MM Taipei}}` | `TZ='Asia/Taipei' date "+%F %H:%M"` | `2026-05-07 14:30` |
| `{{notebook_id}}` | step 2 `notebook_create` 回傳 | `8ee96c1a-0ea2-4bef-b68e-af41ead448d9` |
| `{{notebook_name}}` | step 2 取的 / 既有 notebook 標題 | `Claude Code 與 Obsidian 究極研究工作流` |
| `{{artifact_id}}` | studio_create 回傳 | `125fe62f-634d-4105-bcec-e2ec0f8305e9` |
| `{{title}}` | NotebookLM `source_describe` / yt-dlp metadata | `Claude Code + NotebookLM + Obsidian = GOD MODE` |
| `{{channel}}` | 同上 | `Chase AI` |
| `{{duration}}` | 同上 | `00:15:38` |
| `{{publish_date}}` | 同上 | `2024 年（推估）` |
| `{{url}}` | 使用者貼的 | `https://www.youtube.com/watch?v=kU3qYQ7ACMA` |

## 檔名規則（v1 修正：直接用影片標題）

### 單支影片

直接用影片標題當 filename：
- `Claude Code + NotebookLM + Obsidian = GOD MODE.md`
- `如何在 30 分鐘搭出 RAG 系統.md`

### 多支影片

用 notebook 標題（NotebookLM notebook 命名通常是主題級的）：
- `Claude Code 與 Obsidian 究極研究工作流.md`
- `2026 LLM 評測比較.md`

### 字元清理

- **移除**（macOS / 跨平台不允許）：`:`、`/`、`\`、`*`、`?`、`<`、`>`、`|`、`"`
- **保留**：`+`、`=`、`&`、`空格`、`-`、中文標點（譬如 `？`、`！`、`。`）
- **不加**：日期前綴（已在 frontmatter `created`）、`youtube_` 前綴、`_stub` 後綴

### 範例

| 原影片標題 | filename |
|*********--|*********-|
| `Claude Code + NotebookLM + Obsidian = GOD MODE` | `Claude Code + NotebookLM + Obsidian = GOD MODE.md` |
| `🚀 ChatGPT vs Claude：誰更強？(2026 年實測)` | `🚀 ChatGPT vs Claude誰更強？(2026 年實測).md`（去除半形 `:`） |
| `Andrej Karpathy: Software 2.0` | `Andrej Karpathy Software 2.0.md`（去除半形 `:`） |

## 衝突處理

如果 `00-Inbox/{影片標題}.md` 已存在（同支影片重跑）：

- 加 `(2)`、`(3)`... 直到找到不衝突的檔名
- 例：`Claude Code + NotebookLM + Obsidian = GOD MODE (2).md`

不要覆蓋既有檔（可能是使用者手動編輯過了）。
