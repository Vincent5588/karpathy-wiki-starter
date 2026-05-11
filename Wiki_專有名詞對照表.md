---
title: "Wiki 專有名詞對照表（中英對照）"
tags: ["glossary", "translation", "vault-meta", "中英對照"]
domain: wiki
type: glossary
status: draft
maintained_by: LLM
parent: "[[CLAUDE]] §10 規則 J.2（中英對照規範）"
created: 2026-01-01
updated: 2026-01-01
cssclasses: [wide]
---

# 📖 Wiki 專有名詞對照表（中英對照）

> Vault 內常出現的英文專有名詞與其中文對照表。**精選版 ~100 詞**，覆蓋 8 大領域。給人讀為主，LLM 寫 entity 時遇到首次英文出現可查這裡確認譯名（依 [[CLAUDE]] §10 規則 J.2）。
>
> ⚠️ **模板初版**：本表預設涵蓋 AI/LLM / Claude / PKM / 生產力 / 開發 / 軟體工具 / 部署 / 人物共 8 節。使用者可依 vault 主題擴充（如加入半導體 / 醫療 / 法律等 domain 特定詞彙）。

## 維護規則

**何時更新**（依 [[CLAUDE]] §10 規則 L 框架）：

- ingest 新 entity 含未收錄的英文專有名詞 → 加新 row
- vault grep 看到頻繁出現的英文術語還沒進表 → 加進來
- 既有譯名修正 → 改 row + 同步影響的 entity aliases
- 跨 domain 同英文不同中文 → 兩 row 並列 + 註明差異

**LLM 維護紀律**：每次 wiki-ingest 完成自我檢查——新 entity 是否有英文專有名詞還沒進本表？有則 cascade 加進來。

## 分類目錄

1. [AI / LLM 核心](#1-ai--llm-核心)（Token / Context / RAG / Hallucination 等）
2. [Claude 生態](#2-claude-生態)（Claude Code / MCP / Skill / Sub-agent 等）
3. [PKM / 知識管理](#3-pkm--知識管理)（PKM / Zettelkasten / BASB / PARA 等）
4. [生產力 / 思維](#4-生產力--思維)（Compounding / Vibe Coding / Plan Mode 等）
5. [開發 / 工程](#5-開發--工程)（CLI / API / OAuth / OCR 等）
6. [軟體系統 / 工具](#6-軟體系統--工具)（Notion / Obsidian / NotebookLM 等）
7. [部署 / DevOps](#7-部署--devops)（GitHub Actions / Quartz / rsync 等）
8. [人物 People](#8-人物-people)（Andrej Karpathy / Tiago Forte / Naval Ravikant 等）

---

## 1. AI / LLM 核心

| 英文 | 中文 | 說明 |
|------|------|------|
| LLM (Large Language Model) | 大型語言模型 | 用神經網路訓練、能生成自然語言的模型；GPT / Claude / Gemini 都是 |
| Token | 詞元（一般保留 token 不譯） | LLM 處理文字的最小單位（常 ~1 字 = 1-3 token）。計費 / 額度 / context 都按 token 算 |
| Context Window | 上下文視窗 | LLM 一次能讀進來的最大 token 數（Claude Sonnet 4.6 = 200K tokens）|
| Context Engineering | 上下文工程 | 設計 / 安排放進 LLM context 的內容的學科 |
| RAG (Retrieval-Augmented Generation) | 檢索增強生成 | LLM 回答前先檢索外部知識庫，把結果送進 prompt 一起生成 |
| Hallucination | 幻覺 | LLM 編造看似合理但錯誤的內容 |
| Prompt Engineering | 提示工程 | 設計 prompt 讓 LLM 產出想要的結果 |
| System Prompt | 系統提示 | LLM 對話最頂層的指令，定義角色 / 規則 / 輸出格式 |
| Few-shot prompting | 少樣本提示 | 在 prompt 裡放幾個範例讓 LLM 學會輸出模式 |
| Chain of Thought (CoT) | 思維鏈 | 讓 LLM 寫出推理步驟而不是直接給答案，提高複雜任務正確率 |
| Inference | 推論 | LLM 接收 prompt 後生成回應的計算過程（vs 訓練）|
| Embedding | 嵌入向量 | 把文字轉成多維數字向量，用來做相似度比對 / 語義搜尋 |
| Vector Database | 向量資料庫 | 儲存 + 索引 embedding，常見於 RAG 後端 |
| Temperature | 溫度（保留原文） | 採樣參數，越高越隨機（0 = 確定，1 = 多樣）|
| Auto-compaction | 自動壓縮 | Claude Code 在 context 即將爆時自動摘要早期訊息 |
| Jagged Intelligence | 鋸齒狀智能 | Karpathy 概念：AI 能力在不同任務上分佈不均勻 |
| Agentic Engineering | 代理工程 | 嚴謹的 AI agent 工程學科（Karpathy 創詞，取代 prompt engineering）|

---

## 2. Claude 生態

| 英文 | 中文 | 說明 |
|------|------|------|
| Anthropic | Anthropic（生產 Claude 的 AI 公司）| 不譯。San Francisco AI 安全公司，2021 創立 |
| Claude Code | Claude 程式碼助理 | Claude 的 CLI 工具，在 terminal 跑，能讀寫本機檔 |
| Claude Desktop | Claude 桌面版 | Anthropic 出的 Mac/Windows 桌面 app |
| Sonnet / Opus / Haiku | Claude 模型家族（不譯）| Claude 三個 tier：Opus = 最強、Sonnet = 平衡、Haiku = 最快 |
| MCP (Model Context Protocol) | 模型上下文協定 | Anthropic 設計的 LLM ↔ 外部工具溝通協定 |
| Skill | 技能（一般保留 Skill 不譯）| Claude Code 裡可重用的工作流封裝 |
| Sub-agent | 子代理 | Claude Code 內 `.claude/agents/` 的個別 agent 定義 |
| Hook | 鉤子（一般保留 hook 不譯）| Claude Code 在特定事件觸發的 shell 命令 |
| Plan Mode | 計畫模式 | Shift+Tab 啟動，先給計畫等批准再執行（Claude Code 安全機制）|
| Vibe Coding | 氛圍編程（一般保留 Vibe Coding 不譯）| Karpathy 創詞：信任 AI 寫大塊程式碼、不讀每一行 |
| Orchestrator | 編排者 | 多代理人系統中負責分派任務的角色 |
| Specialist Agent | 專才代理 | 多代理人系統中執行特定領域任務的角色 |
| CLAUDE.md | CLAUDE.md（不譯檔名）| 資料夾級的 LLM 記憶層，每 session 自動讀 |
| Compounding Engineering | 複利工程 | 持續累積規則 / 偏好 / 修正到 CLAUDE.md 形成飛輪 |
| Headless Mode | 無頭模式 | Claude Code 跑在伺服器、無人介入，常用於 CI/CD |
| Context Rot | 上下文腐化 | LLM context 越長 → 早期內容遞迴影響後期判斷的問題 |
| Externalized Memory | 外部化記憶 | 把 LLM context 該記住的東西寫到外部檔案（CLAUDE.md / artifacts）|
| Slash Command | 斜線指令 | Claude Code 的 `/voice` `/remote` `/plan` 等內建指令 |

---

## 3. PKM / 知識管理

| 英文 | 中文 | 說明 |
|------|------|------|
| PKM (Personal Knowledge Management) | 個人知識管理 | 個人整理 / 連結 / 提取知識的方法論集合 |
| PKA (Personal Knowledge Assistance) | 個人知識助理 | PKM 後繼範式：本機資料夾 + AI 代理 |
| Zettelkasten | 卡片盒筆記法（不譯亦可）| Niklas Luhmann 發明的原子筆記 + 鏈結方法論 |
| BASB (Building a Second Brain) | 打造第二大腦 | Tiago Forte 創辦的 PKM 方法論，主張 CODE 框架 |
| PARA | PARA 整理法（不譯）| Tiago Forte 設計的四層資料夾分類：Projects / Areas / Resources / Archive |
| MOC (Map of Content) | 內容地圖（一般保留 MOC 不譯）| 用一份筆記列出某主題的所有相關筆記連結 |
| Atomic Note | 原子筆記 | 一份筆記只講一個概念（Zettelkasten 核心原則）|
| Backlink | 反向連結 | 從目標頁反查所有指向它的頁的連結 |
| Wikilink | 維基連結（不譯）| `[[Name]]` 格式，Obsidian / Roam 標準雙向連結語法 |
| Vault | 知識庫（不譯）| Obsidian 的整個 markdown 資料夾根目錄 |
| Frontmatter | 前置元資料（不譯）| Markdown 檔頂部的 `---` YAML 區塊 |
| Source of Truth | 真理來源 | 系統中某資料的權威版本（其他副本以此為準）|
| Visual PKM | 視覺化個人知識管理 | 用畫布 / 圖形（Excalidraw）做 PKM |
| Infinite Canvas | 無限畫布 | Excalidraw / Heptabase 等工具的無邊界 2D 工作區 |
| Local-first | 本機優先 | 設計原則：資料本機儲存、雲是備份而非主體 |
| Personal Sovereignty | 個人主權 | 對自己資料 / 工具 / 注意力的完全控制權 |
| Tool Agnostic | 工具無關論 | 設計流程不依賴特定工具，方便換工具不丟資產 |

---

## 4. 生產力 / 思維

| 英文 | 中文 | 說明 |
|------|------|------|
| Compounding | 複利效應 | 小規律 / 小改進反覆累積產生指數成長 |
| GTD (Getting Things Done) | 把事做完（David Allen 法）| David Allen 的個人工作管理法 |
| Show Before Write | 寫前先提案 | 規則 E：對檔案系統寫入前先在對話中描述 |
| Design-first | 設計優先 | 先做設計再寫程式碼（vs 先 coding 再回頭設計）|
| Bookkeeping by LLM | LLM 記帳哲學 | 讓 LLM 維護結構化記錄、人類做信任分級 |
| Self-check | 自我檢查 | LLM 寫完後自己驗證輸出（用 checklist / re-read）|
| Externalized Artifacts | 外部化製品 | 把工作成果寫到外部檔（vs 留在 LLM context 裡）|
| Leaf Node vs Core Code | 葉節點 vs 核心程式碼 | Vibe Coding 適用判準：leaf 可放手、core 必審 |
| Karpathy Notes Principle | Karpathy 筆記原則 | 寫給未來自己看（不為他人用詞，自然語言為主）|
| Seven Powers | 七種護城河 | Hamilton Helmer 框架，把商業壁壘拆 7 種 |
| Switching Costs | 轉換成本 | 客戶從 A 工具搬到 B 工具的痛點 |
| Network Effects | 網路效應 | 用戶越多每用戶價值越高 |
| Scale Economies | 規模經濟 | 規模越大單位成本越低 |
| Counter-Positioning | 反向定位 | 新進者用新模式讓既有玩家無法跟進 |
| Training Distribution | 訓練分布（密度）| AI 模型在某 codebase 的「熟悉度」由訓練資料覆蓋密度決定 |

---

## 5. 開發 / 工程

| 英文 | 中文 | 說明 |
|------|------|------|
| CLI (Command Line Interface) | 命令列介面 | 終端機文字介面（vs GUI 圖形介面）|
| API (Application Programming Interface) | 應用程式介面 | 系統間資料交換的標準接口 |
| OAuth (Open Authorization) | 開放授權 | 第三方登入授權標準（Google / GitHub 登入用）|
| OCR (Optical Character Recognition) | 光學字元辨識 | 把圖片中的文字提取成可編輯文字 |
| HTML | 超文本標記語言（不譯）| 網頁基本標記語言 |
| CSS | 串聯樣式表（不譯）| 網頁排版樣式語言 |
| SQL | 結構化查詢語言（不譯）| 關聯資料庫操作語言 |
| JSON (JavaScript Object Notation) | JS 物件表示法（不譯）| 結構化資料交換格式 |
| YAML | YAML（不譯）| 人類可讀的資料序列化格式（用於 frontmatter）|
| TDD (Test-Driven Development) | 測試驅動開發 | 先寫測試、再寫實作的流程 |
| e2e Test (End-to-End) | 端到端測試 | 從 UI 到 backend 完整跑一遍的測試 |
| Git Worktree | Git 工作樹 | Git 多分支同時 checkout 的機制 |
| Code Review | 程式碼審查 | 同事 / AI 看你的 diff 找問題 |
| NFC / NFD (Unicode Normalization) | NFC / NFD（不譯）| Unicode 正規化形式：NFC 組合形 / NFD 分解形（macOS APFS 用 NFD）|
| Hot Reload | 熱重載（不譯）| 程式改動後不重啟、即時生效 |
| Failover | 容錯切換 | 主系統失效時自動切到備援 |

---

## 6. 軟體系統 / 工具

| 英文 | 中文 | 說明 |
|------|------|------|
| Notion | Notion（不譯）| 整合式筆記 / 資料庫 / 協作工具 |
| Obsidian | Obsidian（不譯）| 本機優先 markdown PKM 工具 |
| Heptabase | Heptabase（不譯）| Card-based 視覺化 PKM 工具，支援深度思考 |
| Roam Research | Roam Research（不譯）| 雙向連結 PKM 始祖 |
| Logseq | Logseq（不譯）| open source outliner，類似 Roam 的本機版 |
| NotebookLM | NotebookLM（不譯）| Google 出的 AI 研究 / 摘要工具 |
| SQLite | SQLite（不譯）| 嵌入式關聯資料庫，單檔即可運作 |
| Excalidraw | Excalidraw（不譯）| 手繪風格 SVG 白板工具 |
| Dataview | Dataview（不譯）| Obsidian 外掛，用類 SQL 動態查詢 vault |
| Cursor | Cursor（不譯）| AI-native IDE（VSCode fork + Claude / GPT 整合）|
| Perplexity | Perplexity（不譯）| AI 搜尋引擎，常用於查詢輔助 |
| iCloud / Dropbox / Google Drive | 雲端同步服務（不譯）| 跨裝置檔案同步 |

---

## 7. 部署 / DevOps

| 英文 | 中文 | 說明 |
|------|------|------|
| GitHub Actions | GitHub Actions（不譯）| GitHub 的 CI/CD 自動化平台 |
| Cloudflare Pages | Cloudflare Pages（不譯）| 靜態網站託管平台 |
| Quartz | Quartz（不譯）| 把 Obsidian vault 編譯成靜態網站的工具 |
| rsync | rsync（不譯）| Unix 遠端 / 本機檔案同步工具 |
| Cron | cron（不譯）| Unix 排程任務系統 |
| npm / Node.js | npm / Node.js（不譯）| JavaScript 套件管理器 / 執行環境 |
| Plugin | 外掛 / 套件（一般保留 plugin 不譯）| 擴充軟體功能的模組 |
| CI/CD (Continuous Integration / Deployment) | 持續整合 / 持續部署 | 自動化建置 / 測試 / 部署流水線 |
| Lockfile | 鎖定檔 | 鎖定依賴版本確保可重現 build（package-lock.json 等）|
| Tag / SHA | 標籤 / SHA（不譯）| Git commit 識別子；deploy pipeline 必鎖 tag/sha 不抓 HEAD |
| SCSS | SCSS（不譯）| CSS 預處理器（Quartz 使用）|
| Cache | 快取 / cache（一般保留不譯）| 暫存提速機制 |

---

## 8. 人物 People

| 英文 | 中文 | 說明 |
|------|------|------|
| Andrej Karpathy | 安德烈 · 卡帕西 | 前 Tesla AI 主管 / OpenAI 共同創辦人 / Eureka Labs 創辦人；Software 2.0 / Vibe Coding / Agentic Engineering 創詞者 |
| Vannevar Bush | 范尼瓦爾 · 布許 | MIT 工程師 / 1945《As We May Think》提出 Memex 概念 |
| Niklas Luhmann | 尼克拉斯 · 盧曼 | 德國社會學家，Zettelkasten 卡片盒筆記法發明者 |
| Sönke Ahrens | 桑克 · 阿倫斯 | 《How to Take Smart Notes》作者，把 Zettelkasten 介紹給英文世界 |
| Tiago Forte | 蒂亞戈 · 福爾特 | BASB 打造第二大腦創辦人，PARA 整理法提出者 |
| Naval Ravikant | 納瓦爾 · 拉維坎特 | AngelList 創辦人，《納瓦爾寶典》作者 |
| David Allen | 大衛 · 艾倫 | GTD（Getting Things Done）方法論提出者 |
| Hamilton Helmer | 漢密爾頓 · 賀爾默 | 戰略投資人，《Seven Powers》作者 |

---

## Vault 用詞慣例

| 情況 | 處置 |
|------|------|
| 純英文縮寫（MCP / RAG / LLM / API / OCR） | 直用英文，不翻 |
| 有共識中文譯名（提示工程 / 上下文 / 容器化）| 優先中文 + 首次出現加英文括號 |
| Karpathy 創詞（Vibe Coding / Jagged Intelligence） | 中英並列，視頻率決定主從 |
| 新創術語（PKA / Agentic Engineering） | 中英並列：英文（中文說明） |
| 軟體 / 工具 / 廠商名（Notion / Obsidian / Anthropic / GitHub）| 直用英文 |
| 人物中文譯名 | 採台灣慣用音譯 |

詳細規範見：[[CLAUDE]] §10 規則 J（entity 必繁中）+ J.2（中英對照）

---

## 自動補充：Dataview 動態列表

### 全部 person 類 entity（自動）

```dataview
TABLE WITHOUT ID file.link AS "頁面", aliases AS "別名", domain
FROM "wiki/entities"
WHERE type = "person"
SORT file.name ASC
```

### 含 alias 的 entity（含英文別名）

```dataview
TABLE WITHOUT ID file.link AS "Entity", aliases AS "別名 / Aliases", domain
FROM "wiki/entities"
WHERE aliases AND length(aliases) > 0
SORT file.name ASC
LIMIT 50
```

---

## 相關

- [[CLAUDE]] §10 規則 J — entity 必繁中 + 中英對照規範
- [[CLAUDE]] §10 規則 D — 英文 quote 加繁中翻譯
- [[wiki/index]] — vault 主目錄
- [[WIKI_TODO]] — 待辦清單

← 回到 [[wiki/index]]
