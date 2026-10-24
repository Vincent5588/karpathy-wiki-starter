# Obsidian CLI Helper for wiki-notion-sync v1.3.8

> Read 側 helper：把 frontmatter / outlinks / aliases 從 [[Obsidian CLI]] 一次拿齊，取代 v1.3.7 的「Read 全 vault → 自寫 YAML parser → regex 抓 [[X]]」三步走。

## 為什麼要這份 helper

| | v1.3.7 | v1.3.8 hybrid |
|---|---|---|
| YAML parse | python-frontmatter / 手寫 | `app.metadataCache.getFileCache(f).frontmatter` |
| 抓 outlinks | regex `\[\[([^\]]+)\]\]` | `app.metadataCache.resolvedLinks` |
| Alias 解析 | 漏 | resolvedLinks 已 normalize 到目標 path |
| NFC normalize | 自己呼 `unicodedata.normalize` | Obsidian 自動 |
| 速度 | 1× IPC + 1×N filesystem reads | 1× IPC（單個 eval 一次拿全部）|

→ 實測（一個約 200 頁的 vault）：191 entity / 3245 links / 48 aliased / 144 KB JSON ≈ **< 1 秒**

---

## Pre-flight

執行 hybrid path **之前**必須通過 3 個 check：

```bash
# 1. obsidian-cli 安裝？
which obsidian || { echo "❌ obsidian-cli 未安裝（brew install obsidian-cli）"; exit 1; }

# 2. Obsidian 在前景且回應？
obsidian vault > /dev/null 2>&1 || { echo "❌ Obsidian 沒開或 vault 沒 focus"; exit 1; }

# 3. 對的 vault？
TARGET_VAULT="${VAULT_NAME:?先設定 VAULT_NAME＝你的 vault 名稱}"
ACTUAL_VAULT=$(obsidian vault | grep '^name' | awk '{print $2}')
[ "$ACTUAL_VAULT" = "$TARGET_VAULT" ] || obsidian vault="$TARGET_VAULT" vault > /dev/null
```

任一 check 失敗 → 讀 `CLI_FALLBACK.md` 走 v1.3.7 純 filesystem path。

---

## Snippet 1：全 vault inventory（一次拿齊）

**用途**：取代 SKILL.md step 2「Inventory entities by domain」的 markdown 掃描 + frontmatter parse。

```bash
obsidian eval code='(() => {
  const r = app.metadataCache.resolvedLinks;
  const u = app.metadataCache.unresolvedLinks;
  const wiki = {}, wikiU = {}, frontmatters = {}, aliases = {};
  let entityCount = 0, resolvedLinkCount = 0, unresolvedLinkCount = 0;

  // resolved + unresolved links（only wiki/entities/ + wiki/maps/）
  for (const src in r) {
    if (!src.startsWith("wiki/entities/") && !src.startsWith("wiki/maps/")) continue;
    entityCount++;
    wiki[src] = r[src];
    resolvedLinkCount += Object.values(r[src]).reduce((a,b)=>a+b, 0);
  }
  for (const src in u) {
    if (!src.startsWith("wiki/entities/") && !src.startsWith("wiki/maps/")) continue;
    if (Object.keys(u[src]).length === 0) continue;
    wikiU[src] = u[src];
    unresolvedLinkCount += Object.values(u[src]).reduce((a,b)=>a+b, 0);
  }

  // frontmatters + aliases
  const files = app.vault.getMarkdownFiles().filter(f =>
    f.path.startsWith("wiki/entities/") || f.path.startsWith("wiki/maps/")
  );
  for (const f of files) {
    const cache = app.metadataCache.getFileCache(f);
    if (!cache || !cache.frontmatter) continue;
    const fm = cache.frontmatter;
    frontmatters[f.path] = {
      title: fm.title || f.basename,
      type: fm.type,
      domain: fm.domain,
      status: fm.status || "draft",
      tags: fm.tags || [],
      created: fm.created,
      updated: fm.updated,
    };
    if (fm.aliases) aliases[f.path] = fm.aliases;
  }

  return JSON.stringify({
    summary: {
      entityCount, resolvedLinkCount, unresolvedLinkCount,
      aliasedFiles: Object.keys(aliases).length,
      generatedAt: new Date().toISOString(),
    },
    frontmatters, resolvedLinks: wiki, unresolvedLinks: wikiU, aliases,
  }, null, 2);
})()' | sed 's/^=> //' > /tmp/notion_sync_v138/inventory.json
```

### 輸出 schema

```typescript
{
  summary: {
    entityCount: number,           // 191
    resolvedLinkCount: number,     // 3245
    unresolvedLinkCount: number,   // 32
    aliasedFiles: number,          // 48
    generatedAt: string,           // ISO timestamp
  },
  frontmatters: {
    [path: string]: {              // path = "wiki/entities/<domain>/<type>/X.md"
      title: string,
      type: string,                // concept / system / pattern / ...
      domain: string,              // orders / claude / wiki / ...
      status: "draft" | "stable" | "deprecated",
      tags: string[],
      created?: string,
      updated?: string,
    }
  },
  resolvedLinks: {
    [srcPath: string]: {
      [targetPath: string]: number  // count of links from src to target
    }
  },
  unresolvedLinks: {
    [srcPath: string]: {
      [linkText: string]: number    // broken/external link text
    }
  },
  aliases: {
    [path: string]: string[]        // ["Karpathy", "karpathy"] for Andrej Karpathy.md
  }
}
```

### 驗證輸出對

跑完後對比 [[wiki-lint]]：

```bash
# Obsidian eval 報的 entity 數
jq '.summary.entityCount' /tmp/notion_sync_v138/inventory.json
# 應 == lint 報的 total_pages
python3 wiki/tools/lint.py wiki | jq '.total_pages'
```

不一致 → check filter 條件、check filename 是否含特殊字元（NFD/NFC、emoji）。

---

## Snippet 2：篩 status = stable（hybrid 預設只推 stable）

**用途**：v1.3.7 開始 [[wiki-status-promote]] 把 status 當成 trust marker。Hybrid 模式預設**只推 stable**——避免 draft 內容外流到 Notion 造成誤導。

```bash
# 從 Snippet 1 的 inventory.json 篩
jq '[.frontmatters | to_entries[] | select(.value.status == "stable") | .key]' \
  /tmp/notion_sync_v138/inventory.json \
  > /tmp/notion_sync_v138/sync_targets.json
```

或者直接在 eval 裡篩（避免讀大檔）：

```bash
obsidian eval code='(() => {
  const stable = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith("wiki/entities/"))
    .filter(f => {
      const fm = app.metadataCache.getFileCache(f)?.frontmatter;
      return fm?.status === "stable";
    })
    .map(f => f.path);
  return JSON.stringify(stable);
})()' | sed 's/^=> //'
```

### 例外（使用者要含 draft 時）

明確跟使用者確認後可改 filter：

```javascript
.filter(f => ["stable", "draft"].includes(fm?.status))
```

但 SKILL.md step 1 必明確讓使用者選範圍。

---

## Snippet 3：alias debugging（FYI 用）

**用途**：當 Pass 2 解出來的連結看起來怪、想知道 Obsidian 怎麼解的。

```bash
# 列出所有 alias 跟它指向的 entity
obsidian eval code='(() => {
  const out = {};
  for (const f of app.vault.getMarkdownFiles()) {
    const fm = app.metadataCache.getFileCache(f)?.frontmatter;
    if (fm?.aliases) {
      for (const a of fm.aliases) {
        out[a] = f.path;
      }
    }
  }
  return JSON.stringify(out, null, 2);
})()' | sed 's/^=> //'
```

實測本 vault 部分 alias（用 Snippet 3 拿）：

| 寫 `[[X]]` | Obsidian 解到 |
|------------|---------------|
| `[[BASB]]` | `打造第二大腦.md` |
| `[[Karpathy]]` `[[karpathy]]` | `Andrej Karpathy.md` |
| `[[Bush]]` | `Vannevar Bush.md` |
| `[[/loop]]` `[[/schedule]]` | `loop 與 schedule 自動化.md` |
| `[[@bcherny]]` | `Boris Cherny.md` |

→ regex 自寫 parser **完全不會解** 上面這些。

---

## 失敗模式 + 應對

| 情境 | 症狀 | 應對 |
|------|------|------|
| Obsidian 沒開 | `obsidian vault` 報 `Could not find vault` | abort + 提示開 Obsidian |
| Vault 太大（≥ 1000 entity）| eval timeout / 回 truncated JSON | Snippet 1 改 chunk 模式（看下方）|
| Plugin 升級 break API | `app.metadataCache` undefined | 報 plugin 版本不相容、走 fallback |
| Sync conflict（Obsidian Sync 同步中）| metadataCache 不完整 | 先跑 `obsidian sync:status` 等 idle 再 eval |
| `frontmatter` field 結構古怪（譬如 list）| schema validation fail | inventory.json 內 schema validate，列出問題 entity 給使用者修 |

### Big-vault chunk mode（≥ 1000 entity 用）

```javascript
// 分 domain 跑 eval
const domains = ["orders", "claude", "wiki", "helpdesk", "travel", "productivity"];
const result = {};
for (const d of domains) {
  result[d] = /* 同 Snippet 1，但 filter 加 src.startsWith(`wiki/entities/${d}/`) */;
}
```

實務上 vault 達到 1000+ entity 機率低（karpathy-wiki-pattern 設計 vault 通常 < 500），但留 escape hatch。

---

## 跟其他 reference 的關係

- `LINK_CONVERSION.md` — Pass 2 把 wiki-link → Notion link 的轉換規則（v1.3.3 起）
- `CLI_FALLBACK.md` — 本 helper 失敗時走的 v1.3.7 純 filesystem path
- vault `wiki/reports/notion-sync-staging/cli-dryrun-2026-05-03.json` — Snippet 1 真實樣本（144 KB）

## See also

- vault entity：[[Obsidian CLI]] — CLI 通用文件
- vault entity：[[Notion Sync Hybrid 架構]] — 本 helper 屬於這架構的 read 側
- 上游：<https://help.obsidian.md/cli>
