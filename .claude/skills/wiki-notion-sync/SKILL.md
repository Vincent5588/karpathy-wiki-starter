---
name: wiki-notion-sync
description: |
  Sync wiki/entities/ + wiki/maps/ to a Notion workspace, creating a parent
  page with all entities as child pages. v1.3.8: hybrid mode — Read 側交給
  Obsidian CLI 的 resolver / metadataCache（自動處理 alias / NFC / 邊角），
  Write 側仍走 Notion MCP。失敗自動降級回 v1.3.7 純 filesystem path。
  v1.3.3 supports per-domain notebook structure (each domain = one Notion
  parent page). Includes Obsidian wiki-link → Notion internal link
  conversion. Use when user says:
  「同步到 Notion」「push 到 Notion」「Notion sync」「把 wiki 推 Notion」
  「sync wiki to notion」「在 Notion 建知識庫」「依 domain 分筆記本」
  「hybrid sync」「v1.3.8 sync」.

  Requires Notion MCP server connected. v1.3.8 additionally benefits from
  obsidian-cli + Obsidian running (graceful fallback if not). Two-pass
  execution: pass 1 creates pages with bold placeholders for cross-refs,
  pass 2 (optional) converts bolds to real Notion links once all page IDs
  are known.
allowed-tools: [Read, Glob, Bash]
---

# wiki-notion-sync

Push `wiki/entities/<domain>/<type>/` + `wiki/maps/` to Notion. v1.3.3 預設
**per-domain notebook structure** — 每個 domain 在 Notion 工作區建立一個獨立
的「筆記本」（parent page），entity 依 type 分組為子頁。

## When this skill triggers

User says: 「同步到 Notion」「push 到 Notion」「Notion sync」「把 wiki 推 Notion」「sync wiki to notion」「在 Notion 建知識庫」「依 domain 分筆記本」「each domain own parent」.

## Prerequisite

A Notion MCP server must be connected to the Cowork session. Check via tools available — if `notion-create-pages` is unavailable, ask user to install/authorize the Notion connector first.

## v1.3.3 結構模式

### Mode A — Flat（v1.3.2 行為，仍可選）

```
{Topic} Wiki
├── Entity1
├── Entity2
└── ...
```

### Mode B — Per-domain（v1.3.3 預設）

```
My_Wiki  ← workspace 根
├── 📋 訂單系統 (34 entities)
│   ├── 📖 入口頁（Top hub + ToC）
│   ├── 📂 process/  → N 個 entity
│   ├── 📂 system/   → N 個 entity
│   └── ...
├── 🤖 Claude / AI 工具 (53)
├── 🧳 旅遊規劃 (14)
├── 🧠 生產力 / PKM (29)
├── 🎧 客服工單 (6)
└── 🔧 Wiki Plugin 工具 (8)
```

### Mode C — Per-domain × per-type（最深）

每個 type 也是獨立 child page，再 collapse entities 到該 type 下。對 entity 數很多的 domain（如 Claude 53）有用，但層級深、Notion 端點擊體驗較重。預設不開，要時手動指定。

## Steps（v1.3.3 預設 Mode B）

### 0. Pre-check（v1.3.8 — Hybrid 模式判定）

執行任何步驟前先 detect 環境，決定走 **hybrid path**（推薦）還是 **v1.3.7 fallback**。

#### 4-state 偵測順序

按以下順序 check（任一條件不符就降級）：

```bash
# State 3 check — CLI 沒裝 → 純 filesystem
which obsidian > /dev/null 2>&1 || GOTO state3_fallback

# State 2 check — Obsidian 沒回應
obsidian vault > /dev/null 2>&1 || GOTO state2_ask

# State 4 check — 對的 vault？（VAULT_NAME＝你的 vault 名稱，Obsidian 視窗左下角那個，用前先設定）
ACTUAL=$(obsidian vault | awk '/^name/{print $2}')
[ "$ACTUAL" = "$VAULT_NAME" ] || obsidian vault="$VAULT_NAME" vault > /dev/null

# Edge — Obsidian < 1.9 沒 metadataCache.resolvedLinks
obsidian eval code='app.metadataCache.resolvedLinks ? "ok" : "missing"' \
  | grep -q ok || GOTO state3_fallback

# Edge — Sync 同步中（如有用 Obsidian Sync）
obsidian sync:status 2>&1 | grep -q "syncing" && WAIT_OR_ABORT

# 全部通過 → State 1 hybrid path
echo "✅ Hybrid mode active"
```

#### 4 種 state 應對

| State | 偵測 | 動作 |
|-------|------|------|
| **1. Hybrid OK** | 全部 check pass | 跑 hybrid path（step 2 用 `OBSIDIAN_CLI_HELPER.md` Snippet 1+2）|
| **2. Obsidian 沒回應** | CLI 裝了但 `obsidian vault` fail | **ASK 使用者**：retry / 降級 / 取消（不靜默降級）|
| **3. CLI 沒裝 / API 太舊** | `which obsidian` fail OR `metadataCache.resolvedLinks` undefined | 純 filesystem fallback + 明確告知失去 alias resolution（本 vault 93 個 alias 會漏）|
| **4. Wrong vault** | vault name ≠ 預期 | 自動 `obsidian vault=X vault` 切回，重 check |

詳細決策樹 + edge case → [`references/CLI_FALLBACK.md`](references/CLI_FALLBACK.md)

#### Hybrid 模式特色

走 hybrid 時，後續 step 行為改變：

| Step | v1.3.7 | v1.3.8 hybrid |
|------|--------|---------------|
| Step 2 Inventory | Read + 自寫 YAML parse | `obsidian eval` 一次拿 frontmatter + resolvedLinks |
| Step 5 Bulk push | regex 抓 `[[X]]` | 從 step 2 cache 拿 outlinks |
| Step 7 Pass 2 | 重 parse markdown | 直接套 step 5 staging plan，**不再 parse** |

→ 失去什麼能力（fallback 時）：alias 解（93 條）、NFC normalize、stale push 檢查

跟使用者報告當前模式：

```
🔍 wiki-notion-sync v1.3.8
模式：Hybrid（Obsidian CLI active）
偵測：✅ obsidian-cli ✅ Obsidian 前景 ✅ 目標 vault ✅ resolvedLinks API
```

或：

```
🔍 wiki-notion-sync v1.3.8
模式：v1.3.7 fallback（純 filesystem）
原因：obsidian-cli 未安裝
失去能力：alias 解 / NFC normalize / stale check
繼續？[Y/n]
```

### 1. Identify scope

Ask the user:
- **Mode**：A flat / B per-domain（預設）/ C per-domain × per-type
- **範圍**：整 vault / 單一 domain（如「只 sync productivity」）/ 多 domain（如「orders + claude」）
- **Notion 位置**：
  - 既有 workspace 父頁（給 Notion URL/ID）
  - 或在 workspace 根建新父頁（如「My_Wiki」）

If unclear, list available Notion pages via `notion-search` and let user pick.

### 2. Inventory entities by domain

依 step 0 偵測結果，走 hybrid 或 v1.3.7 fallback。**結果結構相同**（只是 source 不同）：

```python
buckets = {
  "orders":            {"process": [...], "system": [...]},
  "claude":         {"system":  [...], "concept": [...]},
  "travel": {"concept": [...], "process": [...]},
  "productivity":   {"concept": [...], "person":  [...]},
  "helpdesk":         {...},
  "wiki":           {"system":  [...]},
}
```

#### 🟢 Hybrid path（v1.3.8 — state 1，推薦）

跑**單個** `obsidian eval` 一次拿 `(path, frontmatter, outlinks, aliases)` 完整 map。完整 snippet 在 [`references/OBSIDIAN_CLI_HELPER.md`](references/OBSIDIAN_CLI_HELPER.md) §Snippet 1：

```bash
mkdir -p /tmp/notion_sync_v138
obsidian eval code='(...見 OBSIDIAN_CLI_HELPER.md Snippet 1...)' \
  | sed 's/^=> //' > /tmp/notion_sync_v138/inventory.json
```

→ 輸出含 4 大 field：

| Field | 用途 |
|-------|------|
| `summary` | entityCount / resolvedLinkCount / unresolvedLinkCount / aliasedFiles |
| `frontmatters` | `{path: {title, type, domain, status, tags, created, updated}}` |
| `resolvedLinks` | `{srcPath: {targetPath: count}}` — **alias 已自動解** |
| `aliases` | `{path: [alias1, alias2, ...]}` — debug 用 |
| `unresolvedLinks` | `{srcPath: {linkText: count}}` — broken / cross-folder ref |

**hybrid 模式直接拿到** v1.3.7 要自寫程式碼才有的東西：
- ✅ frontmatter（含 status / domain / type）→ 不需自己 parse YAML
- ✅ outlinks（path → path）→ 不需 regex 抓 `[[X]]`
- ✅ alias 解析 → vault 93 個 alias 全自動解（包括 `[[BASB]]` `[[Karpathy]]` `[[/loop]]` 等）
- ✅ NFC normalize → 含變音符 filename 不會踩

#### 🟡 v1.3.7 fallback path（state 2 confirmed / state 3）

走純 filesystem path（v1.3.7 行為，已驗證）：

```python
import frontmatter, glob, re

inventory = []
for path in glob.glob("wiki/entities/**/*.md", recursive=True):
    with open(path) as f:
        post = frontmatter.load(f)
    inventory.append({
        "path": path,
        "frontmatter": post.metadata,
        "content": post.content,
        "outlinks": re.findall(r'\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]', post.content),
    })
```

**已知限制**（state 0 已通知使用者）：
- ❌ alias 漏：`[[BASB]]` 等 93 條都被當 missing
- ❌ NFC/NFD：含變音符 filename 比對可能失敗
- ⚠️ Cross-folder ref（`[[40-Resources/X]]`）會出現在 outlinks 裡，需要二次篩

#### Filter status（兩個路徑都做）

預設只 sync `status: stable`（v1.3.7 起 [[wiki-status-promote]] 把 status 當 trust marker）。

```python
buckets_filtered = {
    domain: {
        type: [e for e in entities if e["frontmatter"].get("status") == "stable"]
        for type, entities in types.items()
    }
    for domain, types in buckets.items()
}
```

**例外**：使用者明確要含 draft 才放寬，且必須再 confirm 一次（draft 推到 Notion = 外人可能看到未驗證內容）。

#### Bucket assembly

把 inventory 整理成 buckets dict（前面範例的格式），寫入 `/tmp/notion_sync_v138/manifest.json` — 每個 entity 含：

- `title`（去 emoji 前綴；emoji 進 `icon` field）
- `domain` / `type`（從 frontmatter）
- `path`（vault 相對路徑）
- `outlinks`（hybrid: targetPath list / fallback: basename list）
- `content`（預處理過的 markdown — 拿掉 frontmatter / H1 / `← 回到 ...` footer，wiki-link 換成 placeholder bold）

預處理規則 → [`references/LINK_CONVERSION.md`](references/LINK_CONVERSION.md)。

#### 驗證 inventory 對

跑完比對：

```bash
# entity 數
jq '.summary.entityCount' /tmp/notion_sync_v138/inventory.json
# 應 ≈ lint 報的（filter stable 後會少一些）
python3 wiki/tools/lint.py wiki | jq '.total_pages'

# alias 抽檢（hybrid only）
jq '.aliases | to_entries[] | select(.value[] | contains("BASB"))' \
  /tmp/notion_sync_v138/inventory.json
# 應指到 打造第二大腦.md
```

### 3. Create workspace root（可選）

如果使用者想全部裝在一個 Notion workspace 根頁：

Call `notion-create-pages` with parent = user-provided root → 建一頁：
- Title: `My_Wiki`（或使用者指定名稱）
- Body: workspace 概覽 + 6 domain 一句話介紹

或直接用使用者既有的 Notion 父頁。

### 4. Per-domain：建 domain parent + ToC

對每個要 sync 的 domain：

```python
for domain in domains_to_sync:
    parent_payload = {
        "properties": {"title": DOMAIN_LABELS[domain]},
        "icon": DOMAIN_EMOJI[domain],
        "content": build_domain_overview(domain, buckets[domain]),
    }
    parent_id = notion-create-pages(parent=workspace_root_id, pages=[parent_payload])
    domain_parent_ids[domain] = parent_id
```

`DOMAIN_LABELS`（建議；可被使用者覆寫）：

| domain | Notion 父頁標題 | emoji |
|--------|---------------|-------|
| `orders` | 訂單系統 | 📋 |
| `claude` | Claude / AI 工具 | 🤖 |
| `travel` | 旅遊規劃 | 🧳 |
| `productivity` | 生產力 / PKM | 🧠 |
| `helpdesk` | 客服工單 | 🎧 |
| `wiki` | Wiki Plugin 工具 | 🔧 |

`build_domain_overview` 產的 body：
1. 一段話介紹這 domain 是什麼
2. Top hub 入口頁列表（取該 domain 內 inlinks ≥ 5 的 entity，最多 3 個）
3. 依 type 分組的 ToC：
   ```
   ### 📂 concept (N)
   - **EntityA**
   - **EntityB**

   ### 📂 process (N)
   - **EntityC**
   ```
   ToC 列項先用 bold 占位，Pass 2 換成真連結。

### 5. Bulk push entities under each domain parent（batches of ~10）

```python
for domain, types in buckets.items():
    parent_id = domain_parent_ids[domain]
    all_entities = [e for type_list in types.values() for e in type_list]
    for batch in chunk(all_entities, 10):
        pages_payload = [
            {
                "properties": {"title": f"{e.emoji} {e.title}"},
                "icon": e.emoji,
                "content": e.preprocessed_markdown,
            }
            for e in batch
        ]
        ids = notion-create-pages(parent=parent_id, pages=pages_payload)
        for e, pid in zip(batch, ids):
            id_map[e.title] = pid  # 全 vault ID map（跨 domain 用）
```

Notion 限 create-pages ≤ 100 per call。Batch 10-12 為安全值。

### 6. Build cross-domain ID mapping + Update Plan staging

#### 6a. ID map（兩條路徑都做）

跑完所有 domain 後，`id_map` 是 `{entity_title → notion_page_id}` 全 vault 對照。

這是 Pass 2 用來解 cross-domain 連結的關鍵 — 例如 productivity 的「打造第二大腦」連到 wiki 的「wiki-ingest」，pass 1 因為當時 wiki domain 還沒建完，一律當 bold；現在全部 ID 在手，可以一次解齊。

#### 6b. Update Plan staging（v1.3.8 hybrid 加）

🟢 **Hybrid path only**（state 1）—— v1.3.7 fallback 跳這段。

用 step 2 的 `resolvedLinks` 配 6a 的 `id_map`，**預算出**每個 page 要替換的連結清單，存到 staging。step 7 只要讀 staging 套用，不再 parse markdown。

```python
import json

with open("/tmp/notion_sync_v138/inventory.json") as f:
    inv = json.load(f)

update_plan = []
for src_path, fm in inv["frontmatters"].items():
    page_id = id_map.get(fm["title"])
    if not page_id:
        continue  # 該 entity 沒推（可能是 draft 被 filter 掉）

    # step 2 已 resolved 的 outlinks
    resolved_outlinks = inv["resolvedLinks"].get(src_path, {})
    link_replacements = []
    for target_path, count in resolved_outlinks.items():
        target_title = inv["frontmatters"].get(target_path, {}).get("title")
        target_pid = id_map.get(target_title) if target_title else None
        if target_pid:
            link_replacements.append({
                "bold_placeholder": target_title,
                "target_path": target_path,
                "target_page_id": target_pid,
                "occurrences": count,
            })

    # 留 bold 的（cross-folder ref 到 40-Resources/ 等）
    unresolved_bolds = list(inv["unresolvedLinks"].get(src_path, {}).keys())

    update_plan.append({
        "page_id": page_id,
        "title": fm["title"],
        "path": src_path,
        "domain": fm["domain"],
        "type": fm["type"],
        "link_replacements": link_replacements,
        "unresolved_bolds": unresolved_bolds,
    })

with open("/tmp/notion_sync_v138/update_plan.json", "w") as f:
    json.dump(update_plan, f, indent=2, ensure_ascii=False)
```

#### Update Plan schema

```typescript
[
  {
    page_id: string,           // Notion page ID
    title: string,             // entity title (純文字，無 emoji)
    path: string,              // vault 相對路徑
    domain: string,
    type: string,
    link_replacements: [
      {
        bold_placeholder: string,  // 即 target entity title，Pass 1 已 bold
        target_path: string,
        target_page_id: string,    // 從 id_map
        occurrences: number,
      }
    ],
    unresolved_bolds: string[],   // 不轉 link，留 bold（cross-folder ref）
  }
]
```

#### 數量預期

對 191 entity 全 vault 跑：

```
update_plan.length         ≈ 191（含 deprecated / draft 被篩掉的會少）
sum(link_replacements)     ≈ 3245（≈ inventory.summary.resolvedLinkCount）
sum(unresolved_bolds)      ≈ 32（≈ inventory.summary.unresolvedLinkCount）
```

跑完比對：

```bash
jq 'length' /tmp/notion_sync_v138/update_plan.json
# 應 ≈ id_map size

jq '[.[] | .link_replacements | length] | add' /tmp/notion_sync_v138/update_plan.json
# 應 ≈ inventory.json 的 resolvedLinkCount
```

數字對不上 → step 6b 邏輯有 bug（譬如 title vs path 對應錯）。

#### v1.3.7 fallback 跳過 6b

state 3 走純 filesystem 時，沒有 inventory.json 可用。step 7 會自己 re-parse markdown（v1.3.7 行為）。

跟 hybrid 比慢、且 alias 漏 — 但是 known-good baseline。

### 7.（Optional）Pass 2：Convert bold → real Notion links

依 step 0 偵測，走 hybrid（套 staging plan）或 v1.3.7 fallback（重 parse markdown）。

#### 🟢 Hybrid path（v1.3.8 — state 1）

直接讀 step 6b 產的 `/tmp/notion_sync_v138/update_plan.json`，**不再 parse markdown**：

```python
import json

with open("/tmp/notion_sync_v138/update_plan.json") as f:
    plan = json.load(f)

# Ask user before running heavyweight update
print(f"Pass 2 will run {len(plan)} notion-update-page calls. Continue? [Y/n]")

# Batch 3 / call（v1.3.4 經驗值不變）
for batch in chunk(plan, 3):
    for entry in batch:
        # Build new content：把每個 link_replacement 的 bold placeholder 換成 real link
        new_content = build_notion_content(entry)
        notion-update-page(
            page_id=entry["page_id"],
            command="replace_content",
            content=new_content,
        )
```

`build_notion_content(entry)`：

```python
def build_notion_content(entry):
    """從 vault path 讀原始 markdown，套 entry.link_replacements。"""
    raw = read_vault_file(entry["path"])  # 純 file read，不 parse YAML
    content = preprocess(raw)             # 拿掉 frontmatter / H1 / footer

    # 用 step 6b 已 resolved 的 mapping 做替換
    for r in entry["link_replacements"]:
        # 把粗體 placeholder「**Title**」換成 [Title](https://www.notion.so/{page-id})
        old = f"**{r['bold_placeholder']}**"
        new = f"[{r['bold_placeholder']}](https://www.notion.so/{r['target_page_id'].replace('-', '')})"
        content = content.replace(old, new, r["occurrences"])

    # entry.unresolved_bolds 留 bold（不轉 link）
    return content
```

#### 跟 v1.3.7 比

| | v1.3.7 fallback | v1.3.8 hybrid |
|---|---|---|
| 抓連結位置 | regex 抓 markdown | step 6b 已預算（occurrences 也對齊）|
| Alias 解析 | ❌ `[[BASB]]` 找不到 → 留 bold | ✅ 已從 `打造第二大腦.md` resolve（93 條 alias 全收）|
| NFC 處理 | ❌ macOS NFD filename 漏 | ✅ Obsidian metadataCache 已 normalize |
| Cross-folder ref | regex 篩 | 在 `unresolved_bolds` 已分離 |
| Performance | 每頁 re-read + re-parse | 純 lookup 套用 |

#### 🟡 v1.3.7 fallback path（state 3）

走純 filesystem，每頁 re-read + regex 找 `[[X]]` + 配 id_map 換 link：

```python
for page_id, src_path in id_map.items():
    raw = read_vault_file(src_path)
    content = preprocess(raw)
    # regex 找 [[X]] → 配 id_map 換 link
    content = re.sub(
        r'\*\*([^*]+)\*\*',
        lambda m: build_link_or_keep_bold(m.group(1), id_map),
        content,
    )
    notion-update-page(page_id=page_id, command="replace_content", content=content)
```

**已知 fail mode**：alias 邊角（93 條）會被當「找不到 → 留 bold」。

#### Heavyweight 警告（兩條路徑都有）

對 191 entity 全 vault 跑 = ~191 次 `notion-update-page`。Notion API rate limit + Cowork tool args 都要考慮：

- **Batch 3 / call** 上限（v1.3.4 經驗值）
- **每 batch 之間 sleep 1-2 秒**避撞 rate limit
- 預估時間：191 / 3 ≈ 64 batches × 2 sec = 2-3 分鐘最低
- **Ask user before running**

#### 驗證

```bash
# Pass 2 跑完，去 Notion 端點 5 個樣本 page，看 cross-domain link 是否點得開
# 例：productivity 的 [[Andrej Karpathy]] 應指到 wiki domain 的 page
```

如果 hybrid path 跑出來 link 數 << update_plan 預期 → step 6b 邏輯有 bug。

### 8.（Optional）Per-domain Database index

問使用者是否要 queryable database。如果要，**為每個 domain** 建一個 database（不要全 vault 共用一個 — 太大）：

```python
for domain in domains_to_sync:
    notion-create-database(
        parent=domain_parent_ids[domain],
        schema={
            "Name": "TITLE",
            "Type": "SELECT(concept, process, system, pattern, role, artifact, person, rule)",
            "Status": "SELECT(stable, draft, deprecated)",
            "Tags": "MULTI_SELECT",
            "Page Link": "URL",
        }
    )
```

然後 bulk-insert 該 domain 的 entity 為 row。

### 9. Report

Summarize per-domain：
- 該 domain 父頁 URL
- entity 數 / type 分布
- 是否建了 database
- pass 2 是否跑了

Plus 全局：
- 總 pages created（root + N domain parent + M entity）
- 總 cross-domain links 解析數（pass 2 跑時）

### 10. Append to wiki/log.md

```
| 2026-05-XX | NotionSync v1.3.8 | per-domain (hybrid) | 6 parents + N entities + 6 DB | Workspace: {url}, staging: /tmp/notion_sync_v138/ |
```

備註欄記下：mode（hybrid / fallback）、Pass 2 是否跑、staging 保留路徑。

### 11. Cleanup（v1.3.8 新增）

#### 立刻清

跑成功確認無誤後，**保留** staging 7 天供 audit / debug：

```bash
# 立刻清的東西（沒留下價值）
# 無 — staging 都先留 7 天

# 預定清理（cron 或下次 sync 開頭）
find /tmp/notion_sync_v138/ -mtime +7 -type f -delete
find /tmp/notion_sync_v138/ -type d -empty -delete
```

#### 保留的 staging 檔

| 檔 | 保留理由 |
|---|------|
| `inventory.json` | 上次 sync 的 vault snapshot — debug 連結走鐘問題用 |
| `update_plan.json` | Pass 2 重跑 / 補連結用（如 v1.3.3 那 112 個 entity 案例就是靠這份解的）|
| `manifest.json` | Pass 1 push 進去什麼內容，對比現況找 drift |

#### 失敗中斷時（不清）

如果 Pass 2 跑到一半 rate limit / Notion 503 中斷：

- **不要清 staging**
- 可以單獨 retry 沒跑的 entries（從 update_plan 找哪些沒在 6b 標 done）
- 手動補完之後才走 cleanup

#### 跟既有 staging 的關係

vault 已有 `wiki/reports/notion-sync-staging/` 是 v1.3.3-1.3.4 留下來的（id_map.json + entities_full_content.json）+ v1.3.8 dry-run（cli-dryrun-2026-05-03.json）。**那個 staging 別動**——是 vault 內持久參考資料。`/tmp/notion_sync_v138/` 是每次 sync 的 ephemeral 工作空間。

兩者不混。

## Rules

### 🚨 Title 不含 emoji 前綴（v1.3.4 強制）

**Notion 同時用 `icon` 屬性跟 title 渲染。如果 title 寫成「📦 Heptabase」+ icon「📦」，Notion sidebar 顯示「📦 📦 Heptabase」雙 emoji。**

**正確做法：**
```python
{
    "properties": {"title": "Heptabase"},   # 純文字，不含 emoji
    "icon": "📦",                            # emoji 放這
    "content": ...
}
```

**錯誤做法：**
```python
{
    "properties": {"title": "📦 Heptabase"}, # ❌ title 含 emoji
    "icon": "📦",                            # 結果：Notion 顯示「📦 📦 Heptabase」
    ...
}
```

**這條規則對 entity 子頁、domain parent、workspace root 全部適用。**

如果歷史 sync 已經有 emoji-prefix 的 title，用 `notion-update-page` 命令 + `command: update_properties` + `properties.title: "純文字"` 修正。

### 其他規則

- **Always check Notion MCP availability first.** Don't fail mid-sync.
- **Confirm scope before pushing.** 整 vault sync 144 entities ≈ 6 root call + 14 batch call + (optional 144) update call。
- **Batch 大小實務上限是 3 entity / call**（v1.3.4 修正）— SKILL 之前寫 batch 10-12，但 MCP tool args 通常容不下 10 個 entity 完整內容（總 args 約 50KB+，超過很多 LLM 輸出 token 上限）。實務 3 entity / batch 比較安穩，每個 batch ~10KB tool args。
- **中文字 escape 編碼自查**（v1.3.4 加）— 構造 JSON 時 `\u651d` 是「攝」、`\u6458` 才是「摘」；`\u840a` 是「萊」、`\u8403` 才是「萃」。長中文字串先用 `python3 -c "print(repr(x))"` 驗證 codepoint。
- **Pass 2 全 vault ID map**（v1.3.3 改動重點）— 之前 v1.3.2 的 mapping 只在單一 batch 內，cross-domain ref 永遠是 bold。v1.3.3 因為先建完所有 domain 才跑 pass 2，map 是完整的。
- **Per-domain database 不要合併。** Notion database row 上限變動但實務上 per-domain（最多 53 row）查詢體感更好。
- **Cross-folder refs 仍保 bold。** 不要為 `[[40-Resources/X]]` 偽造 Notion link。
- **Mode A 仍可用** — 如果使用者只想 sync 單一 cluster（如「只推 orders」），flat 比較單純。
- **Domain 名稱可被使用者覆寫**：「我希望 productivity 在 Notion 顯示為『知識管理』」應接受。

## 跟 v1.3.2 的差別

| | v1.3.2 (flat) | v1.3.3 (per-domain) |
|---|---|---|
| 預設結構 | 1 parent → all entities flat | 1 root → N domain parents → entities |
| ToC | 單一巨型 ToC | 每 domain 一個 ToC，依 type 分組 |
| Pass 2 mapping | per-batch | 全 vault（解 cross-domain） |
| Database | 1 個（全 vault） | N 個（per-domain） |
| 適合場景 | 單 cluster sync (≤30 entity) | 整 vault sync (>50 entity) |
| Notion 端體感 | 大平面難找 | 像 6 個獨立筆記本 |

## See also

- `references/LINK_CONVERSION.md` — wiki-link to Notion link transformation rules（v1.3.3 加 cross-domain 處理）
