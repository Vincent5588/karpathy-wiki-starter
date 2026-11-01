---
title: "規則 W：Mermaid 視覺規範（Obsidian Dark — Grouped Workflow）"
description: "vault 內新寫或被改到的 Mermaid 圖一律套同一套深色配色：共用開頭（所有圖種）＋九類語意色與圓角（流程圖）＋深藍／深紫分區面板；Obsidian 筆記與 HTML 報告同一套。匯出與展示的成品優先用 Pele 畫成 SVG／PNG。"
type: rule
domain: wiki
status: stable
tags: [rule, mermaid, 視覺規範, obsidian, pele]
created: 2026-11-01
updated: 2026-11-01
aliases: [規則 W, Mermaid 視覺規範, Obsidian Dark — Grouped Workflow]
---

# 規則 W：Mermaid 視覺規範（Obsidian Dark — Grouped Workflow）

> vault 內**新寫或被改到**的 Mermaid 圖，一律套同一套深色配色；**匯出與展示的成品優先用 Pele 畫**（§W.8）。
> 可複製的程式碼在 [[Mermaid 圖範本]]；本檔講範圍、怎麼用、為什麼。語法地雷（特殊字元加引號等）仍看 `CLAUDE.md` §15。
> 這套配色是預設值，想換可以換——但**整個 vault 只用一套**。改色要改兩處：[[Mermaid 圖範本]]（Obsidian 裡的圖）和 `wiki/tools/pele/rule-w-pele.css`（Pele 匯出的圖）。

## 0. 版本歷程

| 版 | 日期 | 內容 |
|---|---|---|
| v1.0 | 2026-11-01 | 模板初版（`CLAUDE.md` v1.12）。移植自維護者 vault 規則 W v1.7 的通用部分：共用開頭、九類語意色、分區留白、直角折線、HTML 報告寫法、已知限制、用 Pele 匯出（§W.8）。維護者 vault 自用的箭頭計算腳本、寫入當下的檢查 hook、備援 CSS 片段不隨模板附，改成手動作法（§W.2 第 3 步） |

## W.1 範圍

| 項目 | 規定 |
|---|---|
| 哪裡的圖 | Obsidian 筆記＋HTML 報告用同一套 |
| 哪些圖種 | **配色全套**：所有圖種第一行都貼共用開頭。**排版只管流程圖**：分區、語意色、圓角 |
| 既有的圖 | **順手改**：之後哪份檔被改到，就把裡面的 Mermaid 一起換成本規範；不另開遷移工程 |
| 語意色 | 九類（§W.3） |
| 用哪個畫 | **匯出與展示的成品**（HTML 報告、SVG、PNG、給 vault 以外的人看的圖）**優先用 Pele**（§W.8）；Pele 畫不出來或版面不清楚才改用原生 Mermaid。**Obsidian 筆記裡的 Mermaid 區塊照舊由 Obsidian 畫**——Pele 改不了它。不管用哪個，Mermaid 原文都留在 vault 筆記裡，是唯一的維護來源 |

## W.2 怎麼用

1. 每張圖第一行貼 [[Mermaid 圖範本]] ① 共用開頭（xychart 改貼 ④）；**流程圖有分區（`subgraph`）時，開頭最後一行 `flowchart` 改用 ①-2 的寫法**（直向、橫向各一種）
2. 流程圖：最後貼 ② 九類 `classDef`，**每個節點都掛 class**（`A["…"]:::step`）。沒掛 class 的節點是直角細字，整張圖就不一致
3. 流程圖：預覽時看接在方塊**左右兩側**的線——箭頭若貼著方塊的邊、沒有指進去，在圖的最後加一行 `linkStyle <編號> interpolate stepBefore`。編號是那條連線在原文裡出現的順序，從 0 數，多條用逗號隔開（`linkStyle 3,5 interpolate stepBefore`）。之後改了連線的先後，編號要重算
4. 寫完在 Obsidian 預覽看一次（`CLAUDE.md` §15 原本就要求）——要看**深色模式下實際畫到螢幕上的樣子**（截圖）。讀節點的顏色值、或直接呼叫 `mermaid.render` 試畫，都看不出 Obsidian 的內建反相（W.6 第一列），也看不出箭頭方向

## W.3 九類語意色

| class | 框色 | 用在 |
|---|---|---|
| `input` | 灰 `#64748B` | 起點、輸入、外部來源 |
| `step` | 靛 `#818CF8` | 一般處理步驟 |
| `agent` | 紫 `#C084FC` | AI／agent 產出物 |
| `handoff` | 藍 `#60A5FA` | 交接給下一個人或 agent |
| `decide` | 琥珀 `#F59E0B`（虛線框） | 要判斷的地方，配菱形 `{}` |
| `check` | 青 `#2DD4BF` | 檢查、稽核、對帳 |
| `ok` | 綠 `#34D399` | 成功、落地、核准 |
| `fail` | 紅 `#F87171` | 失敗、重試、被擋下 |
| `archive` | 石板 `#94A3B8` | 封存、結束 |

每類的底色是深色帶一點該色的色調（例：`fail` 底 `#241A19`），文字一律白色粗體，節點圓角 10px。完整色碼只放在範本，本檔不重抄。

## W.4 流程圖寫法

- **方向**：預設 `flowchart TD`。LR 只用在 5 格以內的單線流程——Obsidian 筆記欄寬有限，橫向長圖會被縮到看不清楚
- **分區**：多階段流程用 `subgraph` 分區，標題可帶 emoji（☀️／🌙／📚）。一般區塊不設色（共用開頭已給深藍 `#111827`、框 `#334155`）；要跟其他區分開的（如夜間）加 `style <ID> fill:#1C1725,stroke:#4C1D95,color:#E8E8E8`
- **分區的留白**：有分區就用範本 ①-2 的 `flowchart` 行——標題離方框上緣 14、區塊之間約 70～76。直向圖拉 `rankSpacing`、橫向圖拉 `nodeSpacing`（橫向圖的上下區塊是靠 `nodeSpacing` 隔開，改 `rankSpacing` 只會變寬）。連線若仍穿過某塊的標題，調整那一排方塊的宣告順序，讓連線走左右兩側，標題留在中間
- **線條**：主流程實線 `-->`；失敗、旁支、通知用虛線 `-.->`。不用 `linkStyle` 幫單一條線換色——顏色只用來表達節點語意
- **直角折線**：共用開頭一律 `"curve": "stepAfter"`，直向橫向都一樣，不要改成 `step`。**接在方塊左右兩側的那幾條線**，在圖的最後加 `linkStyle <編號> interpolate stepBefore`（W.2 第 3 步）——這是指定折線方向，不是換色，跟上一條不衝突
- **複雜圖拆小**：連線會繞回頭的大圖，少數箭頭會從方塊側邊擦過（W.6）；要清楚就拆成幾張小圖
- **斷行**：每行自己用 `<br/>` 斷，一行約 14 個中文字以內。共用開頭已把自動斷行寬度設成 320px；預設的 200px 遇到粗體字會把短句切成兩行
- **引號**：節點、分區標題、連線標籤遇到中文標點、emoji、括號、冒號、箭頭，一律用 `["…"]` 包住（沿用 `CLAUDE.md` §15）

## W.5 HTML 報告

- **優先嵌 Pele 畫好的 SVG**（§W.8）：SVG 已自帶本規範的配色，HTML 不必載入 Mermaid 函式庫；Mermaid 原文照樣留在對應的 vault 筆記
- Pele 畫不出來時才用原生 `<div class="mermaid">`（以下兩條是原生的寫法）
- 每張圖照樣自己帶共用開頭，跟 Obsidian 用同一份碼，不另寫 `mermaid.initialize` 主題
- `<div class="mermaid">` 外面包一層深色外框，例如 `<div style="background:#181818;border-radius:12px;padding:16px">`。HTML 能真正塗出 `#181818` 畫布；頁面是亮色主題時，深色圖也是整塊放在外框裡，不會變成白底上零散的深色方塊

## W.6 已知限制

> 於 Obsidian 1.14.4 與 Pele 1.13.0 實測（2026-10～11）。

| 現象 | 原因 | 處理 |
|---|---|---|
| **深色模式下整張圖變淺色**：淺底黑字、連線標籤白底，只有框線還看得出九類顏色 | Obsidian 內建 `app.css`：`.theme-dark .mermaid > svg { filter: invert(100%) hue-rotate(180deg) saturate(1.25); }`——它假設圖是亮色主題畫的，深色模式就整張反相；本規範的圖本來是深色，反相後變淺。濾鏡不改元素的計算顏色，**讀 DOM 的 `fill` 值看到的仍是深色**，直接呼叫 `mermaid.render` 試畫也繞過它 | 共用開頭的 `"themeCSS": "filter: none !important;"`——Mermaid 把它編成 `#<圖的 id>{filter:none !important}`，蓋過 `app.css`，每張圖自己取消反相；流程、時序、狀態、ER、timeline、xychart 都實測有效，不用每台裝置設定。**這行不要刪** |
| Obsidian 裡的畫布是佈景主題的底色（例：Things 深色 `#1c2127`），不是 `#181818` | Mermaid 的 SVG 背景透明；`background` 變數只拿來推算其他顏色，不會塗底 | 不處理，以深色模式為準。切到亮色模式時會是白底上的深色區塊 |
| 共用開頭少了 `edgeLabelBackground`，連線標籤變成淺粉底配淺色字，讀不到 | base 主題自動推算出來的標籤底色是淺色 | 共用開頭已設 `#131313`，不要刪 |
| **分區標題貼著方框上緣、下一塊緊貼上來**，連線穿過標題 | Mermaid 預設 `subGraphTitleMargin` 為 0，區塊間距只有 `rankSpacing`（直向）或 `nodeSpacing`（橫向）減去框內留白 | 範本 ①-2。⚠️ 只加 `subGraphTitleMargin`、不加間距時，直向圖的區塊會更擠（標題留白吃掉的是區塊之間的空間），所以兩者要一起改 |
| 時序圖備註亮黃；ER 圖屬性列淺灰底配白字 | base 主題預設值 | 共用開頭已設 `note*` 三項；ER 列底色新版 Mermaid 用 `rowOdd`／`rowEven`、舊版用 `attributeBackgroundColor*`，兩組都留 |
| xychart 只寫 `plotColorPalette`，整張變白底黑字 | 寫了 `xyChart` 這段，其餘顏色就不再自動推算 | 用範本 ④，整段一起貼 |
| **箭頭沒有指進方塊**：直向圖箭頭朝右；橫向圖箭頭貼著方塊頂邊 | ① `curve: step` 在線條終點留下一段長度 0 的線，箭頭（`marker orient=auto`）取最後一段方向，長度 0 時畫成朝右 ② 版面引擎（dagre）讓部分連線從方塊上方、部分從側邊接入，直角折線整張圖只能選一種轉彎順序，總有一部分最後一段貼著邊走 | 共用開頭 `stepAfter`，接在左右兩側的線逐條改 `stepBefore`（W.2 第 3 步）。Obsidian 內建 Mermaid 沒有能畫正交連線的 ELK 引擎（設 `layout: elk` 會靜默退回原本的引擎）。⚠️ 檢查時要看「箭頭是否指進它碰到的那一邊」，只看線段長度會漏掉第 ② 種。線條穿過分區標題、多條線擠在同一側，屬版面排列，折線解決不了；要清楚就拆小 |
| timeline 超過 6 段，第 7 段起變回淺色 | 只設 `cScale0`～`cScale5` 時，後面的色階會自動推算成淺色 | 共用開頭已補到 `cScale11`（沿用前 6 色循環） |
| 圓角寫成 `rx:10`（沒帶單位）：Obsidian 桌面版與 Chrome 有圓角，**Safari、iPhone／iPad 上的 Obsidian 是直角** | Mermaid 把值原樣寫進 CSS；沒單位的長度，Chromium 寬鬆接受、WebKit 當成無效值忽略 | 一律寫 `rx:10px,ry:10px`（範本已是）。⚠️ 讀到的樣式值是 `10px`，不代表畫面有圓角——要用截圖確認，而且兩種引擎都要看 |
| **Pele：分區內的連線變白色** | 分區有深色填色時，Pele 依對比自動把區內連線換成 `--pele-fg-on-dark`（白） | `wiki/tools/pele/rule-w-pele.css` 已把所有連線統一成 `--pele-line` 灰色 |

## W.7 色碼從哪來

- **色碼是量出來的，不是目測**：從一張參考圖逐點取樣像素（參考圖不隨模板附）。憑眼睛寫的初版色碼有一半對不上（例：判斷框寫 `#E7C878`，實際是 `#F59E0B`；紫色寫 `#A78BFA`，實際是 `#C084FC`；節點底色寫成統一一色，實際每類各帶色調）
- **參考圖的原始碼放進 Obsidian，長得跟參考圖不一樣**：底色較亮、節點直角、連線是彎的，連線標籤讀不到。參考圖是另一個渲染器畫的，它自己加了圓角，也把底色壓暗了。所以本規範以**參考圖的實際長相**為準，不以那份原始碼為準
- ⭐ **要複製的是畫面，就量畫面**——畫面跟產生它的程式碼，可以不是同一回事

## W.8 用 Pele 畫匯出與展示的成品

**Pele 是什麼**：Obsidian 官方 GitHub 組織 `obsidianmd` 發布的開源函式庫（npm 套件 `pele`，MIT 授權），把 Mermaid 原文畫成 SVG，配色用 CSS 變數控制。網站 <https://pele.run/>、原始碼 <https://github.com/obsidianmd/pele>。跟原生 Mermaid 的差別（官方相容性頁）：用自己的排版引擎，節點位置與連線路徑會不一樣；Mermaid 的主題設定不生效，顏色改由 CSS 變數決定；標籤只支援換行、粗體、斜體。

1. **原文照常寫**：同一份 Mermaid 原文（含共用開頭、九類 classDef），先寫進 vault 筆記。Pele 不吃開頭的配色變數，但會照 `flowchart` 那行的 `curve`、間距設定排版（用範本 ③ 實測：直角折線、分區間距都生效）
2. **畫成檔案**：`node wiki/tools/pele/render.mjs <筆記.md 或 .mmd> <輸出.svg> [--png 輸出.png] [--html 輸出.html] [--index N]`——`.md` 取第 N 個 mermaid 區塊（從 1 數）。配色只來自 `wiki/tools/pele/rule-w-pele.css`（唯一一份），原樣嵌進 SVG，單獨打開也是深色。出 PNG 要本機有 Chrome 或 Edge
3. **放對地方**：PNG、SVG 照規則 I（`wiki/rules/rule-I-image-localization.md`）放 `Attachments/<來源>/`；HTML 放你存報告的地方
4. **打開成品看一次**：內容沒漏、語意色對、文字不截斷不重疊、箭頭指到目標；給手機看的在手機上開過。只看程式沒報錯不算
5. **回退**：Pele 報錯（`render.mjs` exit 4）或版面不清楚 → 改用原生 Mermaid（§W.5 原生寫法），在交付說明裡寫一句原因。§W.2 第 3 步的 `linkStyle` 是照 Obsidian 原生畫面調的，**拿來修 Pele 的圖不一定有效**

**每台電腦要先裝一次**（需要 Node.js；版本鎖在 `wiki/tools/pele/package-lock.json`，裝在本機、不放進 vault）：macOS／Linux `sh wiki/tools/pele/install.sh`（裝到 `~/.local/share/pele-render`），Windows `powershell -ExecutionPolicy Bypass -File wiki\tools\pele\install.ps1`（裝到 `%LOCALAPPDATA%\pele-render`）。沒裝或版本不對，`render.mjs` 會停下並印安裝指令（exit 2／3）。升 Pele 版本＝改 `package.json`＋重產 lock，先用範本 ③ 重畫驗證。

| `render.mjs` 結束碼 | 意思 |
|---|---|
| 0 | 完成 |
| 1 | 參數寫錯，或 `.md` 裡沒有第 N 個 mermaid 區塊 |
| 2 | 這台還沒裝 Pele |
| 3 | 裝的版本跟 `package.json` 鎖的不一樣 |
| 4 | Pele 畫不出這張圖 → 改用原生 Mermaid |
| 5 | 找不到 Chrome／Edge，PNG 沒產出（SVG 已完成） |

## 相關

- `CLAUDE.md` §15（Mermaid 語法地雷）｜[[Mermaid 圖範本]]｜規則 I（`wiki/rules/rule-I-image-localization.md`，匯出的圖放哪）

---

← 回到 `CLAUDE.md` §10
