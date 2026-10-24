#!/usr/bin/env python3
"""
wiki-status-promote 候選清單產生器
跑：python3 promote.py /path/to/your-vault/wiki [--mode quick|triage|full]
輸出：候選清單 JSON（給 LLM 讀，做分類提案）
"""

import sys
import os
import re
import json
import unicodedata
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict


def parse_frontmatter(text):
    """解析 YAML frontmatter，回傳 dict + body"""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 3:].strip()
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def count_words(text):
    """中英文字數合計（中文按 char，英文按 word）"""
    chinese_chars = len(re.findall(r"[一-鿿]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    return chinese_chars + english_words


def has_warning_block(body):
    """偵測 ## 待解 / ## 矛盾 / ## TODO 等警示區塊"""
    warning_patterns = [
        r"^##\s+.*待解",
        r"^##\s+.*矛盾",
        r"^##\s+.*TODO",
        r"^##\s+.*⚠️",
        r"^##\s+.*Deprecated",
    ]
    for line in body.split("\n"):
        for pat in warning_patterns:
            if re.search(pat, line):
                return True
    return False


def count_outlinks(body):
    """數內文 [[wiki-link]] 條數（粗略 inlinks 算法的對偶——但這只算 outlinks）"""
    return len(re.findall(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", body))


def count_inlinks(target_basename, all_entities):
    """數有多少 entity 的內文連到這個 basename"""
    target = unicodedata.normalize("NFC", target_basename)
    count = 0
    for path, (fm, body) in all_entities.items():
        if path.stem == target:
            continue  # 不算自己
        for m in re.finditer(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", body):
            link = unicodedata.normalize("NFC", m.group(1))
            if link == target:
                count += 1
                break  # 同一頁多次引用算一次
    return count


def first_para(body):
    """抓第一個 blockquote 或第一段非空文字當摘要"""
    for line in body.split("\n"):
        if line.startswith(">"):
            return line[1:].strip()[:120]
    for line in body.split("\n"):
        if line.strip() and not line.startswith("#"):
            return line.strip()[:120]
    return ""


def days_since(date_str):
    """日期字串 → 距今天數"""
    if not date_str:
        return None
    try:
        d = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        return (date.today() - d).days
    except (ValueError, AttributeError):
        return None


def score_entity(fm, body, inlinks, min_age=1):
    """打分（依 PROMOTE_RULES.md）"""
    score = 0
    reasons = []

    # 加分
    if inlinks >= 3:
        score += 3
        reasons.append(f"inlinks={inlinks} (+3)")
    elif inlinks >= 1:
        score += 2
        reasons.append(f"inlinks={inlinks} (+2)")

    age = days_since(fm.get("created", ""))
    if age is not None:
        if age >= 90:
            score += 2
            reasons.append(f"age {age}d (+2)")
        elif age >= 30:
            score += 1
            reasons.append(f"age {age}d (+1)")

    if fm.get("updated") and fm.get("created") and fm["updated"] != fm["created"]:
        score += 1
        reasons.append("iterated (+1)")

    word_count = count_words(body)
    if word_count >= 500:
        score += 2
        reasons.append(f"len {word_count} (+2)")
    elif word_count >= 200:
        score += 1
        reasons.append(f"len {word_count} (+1)")

    if "## 相關概念" in body and count_outlinks(body) >= 3:
        score += 1
        reasons.append("connected (+1)")

    required_fm = ["domain", "type", "source", "created", "updated"]
    if all(k in fm for k in required_fm):
        score += 1
        reasons.append("frontmatter complete (+1)")

    # 扣分
    if has_warning_block(body):
        score -= 5
        reasons.append("⚠️ warning block (-5)")

    if inlinks == 0:
        score -= 2
        reasons.append("no inlinks (-2)")

    if word_count < 200:
        score -= 3
        reasons.append(f"len {word_count} too short (-3)")

    # too-new 不打分而是回傳 sentinel，由 classify 函式特別處理
    if age is not None and age < min_age:
        return None, [f"too new (skip until ≥{min_age} day(s))"]

    # 強制例外
    type_ = fm.get("type", "")
    if type_ == "rule" and word_count >= 200 and age and age >= 30:
        score = max(score, 5)
        reasons.append("rule override → ≥5")

    if type_ == "person" and word_count >= 300:
        score = max(score, 5)
        reasons.append("person override → ≥5")

    if inlinks >= 5:
        score = max(score, 7)
        reasons.append("hub override → ≥7")

    return score, reasons


def classify(score, mode="triage"):
    """分數 → 分類。score=None 代表 too new，跳過評分。"""
    if score is None:
        return "🔵 too new (skip)"
    threshold_stable = {"quick": 6, "triage": 5, "full": 999}.get(mode, 5)
    if score >= threshold_stable:
        return "🟢 stable"
    elif score >= 0:
        return "🟡 keep draft"
    else:
        return "🔴 deprecate"


def render_review_queue(data, vault_name="vault"):
    """把候選資料渲染成 markdown review queue（Obsidian task syntax）"""
    today = date.today().isoformat()
    summary = data["summary"]

    lines = [
        "---",
        f'title: "Wiki Review Queue — {today}"',
        'tags: ["review-queue", "wiki-status-promote"]',
        f"date: {today}",
        f"total_drafts: {data['total_drafts']}",
        f"mode: {data['mode']}",
        "---",
        "",
        f"# 📋 Wiki Review Queue — {today}",
        "",
        f"> 跑 wiki-status-promote 後產生的審查清單。**任何同事可認領**。",
        "> 認領 SOP：[[wiki/_review-queue/README|README]]",
        "",
        "## 統計",
        "",
        f"- Total drafts: {data['total_drafts']}",
        f"- 🟢 升 stable: {summary['stable_recommended']}",
        f"- 🟡 留 draft: {summary['keep_draft_recommended']}",
        f"- 🔴 改 deprecated: {summary['deprecate_recommended']}",
        f"- 🔵 太新跳過: {summary['too_new_skipped']}",
        "",
    ]

    # 按建議分類排序：🟢 stable / 🟡 keep / 🔴 deprecate（🔵 不入 queue）
    for category, emoji, title, hint in [
        ("🟢 stable", "🟢", "建議升 stable", "確認內容無誤後直接升"),
        ("🟡 keep draft", "🟡", "留 draft（待補強或待裁決）", "通常需補內容、加 backlink、或待業務裁決"),
        ("🔴 deprecate", "🔴", "改 deprecated（疑似過期）", "判斷：完全下線 → archive / 還在用但 SOP 過時 → 留 draft 補新版"),
    ]:
        # 算總數
        items = []
        for domain, by_cat in data["by_domain"].items():
            items.extend([(domain, c) for c in by_cat.get(category, [])])
        if not items:
            continue

        lines.append(f"## {emoji} {title}（{len(items)}）")
        lines.append("")
        lines.append(f"> {hint}")
        lines.append("")

        # 按 domain 分組
        by_domain = {}
        for domain, c in items:
            by_domain.setdefault(domain, []).append(c)

        for domain in sorted(by_domain.keys()):
            domain_items = by_domain[domain]
            lines.append(f"### domain: {domain} ({len(domain_items)})")
            lines.append("")
            for c in domain_items:
                first = c["first_para"][:60].replace("\n", " ").replace("|", "\\|")
                lines.append(
                    f"- [ ] [[{c['basename']}]] 👤 _待認領_  "
                    f"📊 inlinks={c['inlinks']} 字數 {c['word_count']} ┊ score {c['score']}"
                )
                lines.append(f"      📝 {first}")
                lines.append("")
            lines.append("")

    # SOP
    lines.extend([
        "---",
        "",
        "## 🛠 認領與處理 SOP（簡版）",
        "",
        "### 步驟 1：認領",
        "把 `_待認領_` 改成 `@<你的名字>（領了 YYYY-MM-DD）`，task `[ ]` → `[/]`",
        "",
        "範例：",
        "",
        "```markdown",
        "- [/] [[印表機設定]] 👤 @you（領了 2026-05-02）",
        "```",
        "",
        "### 步驟 2：去看該 entity 內容並判斷",
        "",
        "- **升 stable**：改 entity frontmatter `status: stable` + `updated: today`",
        "- **留 draft**：補內容 / 加 backlink / 加 `review_by: YYYY-MM-DD`",
        "- **改 deprecated**：改 frontmatter + 加 `## ⚠️ Deprecated` 區塊（含原因 + 替代 entity）",
        "- **進一步 archive**：見 vault CLAUDE.md「已下線系統的進一步處置」",
        "",
        "### 步驟 3：回 queue 標 done",
        "task 改 `[x]`，加結論：",
        "",
        "範例：",
        "",
        "```markdown",
        "- [x] [[印表機設定]] 👤 @you ✅ 升 stable（2026-05-02 設備在線確認）",
        "- [x] [[舊 SOP]] 👤 @engineerA 🔴 改 deprecated（設備 2025-12 退役）",
        "```",
        "",
        "---",
        "",
        "## ⏰ 截止與升級規則",
        "",
        "- 此 queue 預設 **2 週內處理**",
        "- 逾期未認領的：vault owner 月底再過一輪",
        "- 仍無人認領的老舊架構圖類 → 考慮自動 archive 到 `wiki/_archive/`",
        "",
        "---",
        "",
        "← 回到 [[wiki/index|wiki/]] | [[wiki/_review-queue/README|review-queue]]",
    ])

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: promote.py <wiki/ path> [options]")
        print("Options:")
        print("  --mode quick|triage|full     promote mode (default: triage)")
        print("  --min-age N                  skip entities created within N days (default: 1)")
        print("  --output-format json|review-queue   output format (default: json)")
        print("  --output-file PATH           output file path (required for review-queue)")
        sys.exit(1)

    wiki_root = Path(sys.argv[1])
    mode = "triage"
    min_age = 1
    output_format = "json"
    output_file = None

    if "--mode" in sys.argv:
        mode = sys.argv[sys.argv.index("--mode") + 1]
    if "--min-age" in sys.argv:
        min_age = int(sys.argv[sys.argv.index("--min-age") + 1])
    if "--output-format" in sys.argv:
        output_format = sys.argv[sys.argv.index("--output-format") + 1]
    if "--output-file" in sys.argv:
        output_file = sys.argv[sys.argv.index("--output-file") + 1]

    entities_dir = wiki_root / "entities"
    if not entities_dir.exists():
        print(f"❌ {entities_dir} 不存在")
        sys.exit(1)

    # 載入全部 entity（用於算 inlinks）
    all_entities = {}
    for path in entities_dir.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            all_entities[path] = (fm, body)
        except Exception as e:
            print(f"⚠️ Skip {path}: {e}", file=sys.stderr)

    # 篩 draft
    candidates = []
    for path, (fm, body) in all_entities.items():
        if fm.get("status") != "draft":
            continue
        inlinks = count_inlinks(path.stem, all_entities)
        score, reasons = score_entity(fm, body, inlinks, min_age=min_age)
        category = classify(score, mode)
        candidates.append({
            "path": str(path.relative_to(wiki_root.parent)),
            "basename": path.stem,
            "domain": fm.get("domain", "?"),
            "type": fm.get("type", "?"),
            "created": fm.get("created", ""),
            "updated": fm.get("updated", ""),
            "inlinks": inlinks,
            "word_count": count_words(body),
            "first_para": first_para(body),
            "score": score,
            "reasons": reasons,
            "category": category,
        })

    # 按 domain 分組 + 分類排序
    by_domain = defaultdict(lambda: {"🟢 stable": [], "🟡 keep draft": [], "🔴 deprecate": [], "🔵 too new (skip)": []})
    for c in candidates:
        by_domain[c["domain"]][c["category"]].append(c)

    # 輸出
    output = {
        "mode": mode,
        "total_drafts": len(candidates),
        "by_domain": dict(by_domain),
        "summary": {
            "stable_recommended": sum(1 for c in candidates if c["category"] == "🟢 stable"),
            "keep_draft_recommended": sum(1 for c in candidates if c["category"] == "🟡 keep draft"),
            "deprecate_recommended": sum(1 for c in candidates if c["category"] == "🔴 deprecate"),
            "too_new_skipped": sum(1 for c in candidates if c["category"] == "🔵 too new (skip)"),
        },
    }

    if output_format == "review-queue":
        markdown = render_review_queue(output, vault_name=str(wiki_root.parent.name))
        if output_file:
            Path(output_file).write_text(markdown, encoding="utf-8")
            print(f"✅ Review queue written to: {output_file}")
            print(f"   Total candidates: {len(candidates)} (🟢 {output['summary']['stable_recommended']} / 🟡 {output['summary']['keep_draft_recommended']} / 🔴 {output['summary']['deprecate_recommended']} / 🔵 {output['summary']['too_new_skipped']})")
        else:
            print(markdown)
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
