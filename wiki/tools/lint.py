#!/usr/bin/env python3
"""
wiki-lint script for the karpathy-wiki-pattern (generic starter version).

v1.3.9 (2026-05-12):
- Cascade completeness check（配合規則 P / CLAUDE.md v1.8）：掃過去 14 天 daily log，
  若該日含 ingest 標記但 Wiki_儀表板 / Wiki_健康度監控 frontmatter `updated:` < daily date
  + 月份檔缺該日 section → 標 incomplete_cascade（warning，不扣分，獨立 output field）。
- frontmatter `updated` 用「>= daily date」判定（不是 ==），消除「ingest 完當天 bump 後
  舊 daily 看起來都不同日」假陽性。
- 不檢查 Wiki_主目錄 提及（主目錄「最近 ingest」是 rolling window 3 批，舊 daily trim
  是預期行為，月份檔才是 SSOT）。

v1.3.7:
- vault root 「四大監控報表」掃描：vault_root/Wiki_*.md 與 WIKI_*.md
  也納入 lint 範圍（依使用者的 vault 結構決定，generic 版若 root 沒這些檔則無影響）。

v1.3.6:
- 防禦：跳過所有 `.fuse_hidden*` 與其他點號開頭的檔（macOS / FUSE / iCloud 暫存）。
- 內容區段塊更精準：改用逐行 fence 偵測。

v1.3.5:
- NFC Unicode normalization fix：macOS APFS 把含變音符的 filename 存成 NFD
  （e.g. ö → o + combining diaeresis），但 wiki 連結內文用 NFC。

v1.3.2:
- glob → rglob for entities/ and maps/ (v1.3 hierarchical 支援)
- cross-domain basename collision 偵測

v1.2:
- god-node 偵測（高 inlink 但內文薄弱）+ 推斷連結密度。

Usage:
    python3 wiki/tools/lint.py /path/to/vault/wiki

Outputs JSON to stdout.
"""
import sys
import re
import json
import unicodedata
import datetime as _dt
from pathlib import Path
from collections import defaultdict


LEGITIMATE_PREFIXES = (
    "40-Resources", "raw/", "wiki/", "Welcome", "Templates", "CLAUDE",
    "image", "20-Projects", "30-Areas", "10-Notes", "00-Inbox", "50-Archive",
)
LEGITIMATE_NAMES = {"index", "README"}
GOD_NODE_INLINK_MIN = 8
GOD_NODE_WORDS_THIN = 200
GOD_NODE_RATIO_THIN = 25

INGEST_MARKERS = re.compile(r"ingest|新建 entity|補既有|🆕|🔧 補強|🔧 規則|擴充 \[\[")


def nfc(s: str) -> str:
    """Normalize to NFC — fixes macOS NFD filesystem vs NFC file-content mismatch."""
    return unicodedata.normalize("NFC", s)


def parse_md(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        if end > 0:
            raw = raw[end + 5:]
    cjk = len(re.findall(r'[一-鿿]', raw))
    ascii_words = len(re.findall(r'\b[A-Za-z][A-Za-z0-9_-]*\b', raw))
    return raw, cjk + ascii_words


def extract_links(text: str):
    strong = set()
    inferred = set()
    full = []
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`\n]+`', '', text)
    for m in re.finditer(r'\[\[([^|\]\\]+)\\?(?:\|[^\]]+)?\]\](\s*\?\?)?', text):
        raw_target = m.group(1).strip()
        is_inferred = bool(m.group(2))
        full_target = raw_target.split("#")[0]
        full.append((full_target, is_inferred))
        stripped = full_target
        if "/" in stripped:
            stripped = stripped.split("/")[-1]
        stripped = nfc(stripped)
        (inferred if is_inferred else strong).add(stripped)
    return strong, inferred, full


def check_cascade_completeness(vault_root: Path, max_age_days: int = 14) -> list:
    """v1.3.8/9: 偵測 daily 提到 ingest 但 cascade 沒做齊 → 規則 P 配套。"""
    incomplete = []
    daily_dir = vault_root / "wiki" / "daily"
    if not daily_dir.exists():
        return incomplete

    today = _dt.date.today()
    cutoff = today - _dt.timedelta(days=max_age_days)

    file_cache = {}

    def read_file(rel: str) -> str:
        if rel not in file_cache:
            p = vault_root / rel
            try:
                file_cache[rel] = p.read_text(encoding="utf-8") if p.exists() else ""
            except Exception:
                file_cache[rel] = ""
        return file_cache[rel]

    def extract_updated(content: str):
        m = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2})', content, re.M)
        return m.group(1) if m else None

    for daily_path in daily_dir.rglob("*.md"):
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})\.md", daily_path.name)
        if not m:
            continue
        y, mo, d = map(int, m.groups())
        try:
            date = _dt.date(y, mo, d)
        except ValueError:
            continue
        if date < cutoff or date > today:
            continue

        try:
            content = daily_path.read_text(encoding="utf-8")
        except Exception:
            continue
        if not INGEST_MARKERS.search(content):
            continue

        date_str = date.isoformat()
        issues = []

        # v1.3.9: monitoring frontmatter 用 >= 判定（ingest 完當天或之後 bump 即算完整）
        dash = read_file("Wiki操作文件/Wiki_儀表板.md")
        if dash:
            up = extract_updated(dash)
            if up is None or up < date_str:
                issues.append(f"Wiki_儀表板 frontmatter `updated:`（{up or '無'}） < {date_str}")

        health = read_file("Wiki操作文件/Wiki_健康度監控.md")
        if health:
            up = extract_updated(health)
            if up is None or up < date_str:
                issues.append(f"Wiki_健康度監控 frontmatter `updated:`（{up or '無'}） < {date_str}")

        # 月份檔 SSOT 檢查（hub 系統未啟用時可忽略）
        month_archive_rel = f"wiki/最新資料歷史/{y}/{y}-{mo:02d}.md"
        archive = read_file(month_archive_rel)
        if archive and f"### {date_str}" not in archive:
            issues.append(f"{month_archive_rel} 缺 ### {date_str} section")

        # v1.3.9: 取消 Wiki_主目錄 提及檢查——主目錄「最近 ingest」是 rolling
        # window（只保留最新 3 批），舊 daily 不在主目錄是預期行為。

        if issues:
            incomplete.append({
                "date": date_str,
                "daily_log": str(daily_path.relative_to(vault_root)),
                "issues": issues,
                "rule": "P (Cite-or-Die Cascade Citation)",
            })

    incomplete.sort(key=lambda x: x["date"], reverse=True)
    return incomplete


def lint(wiki_path: Path) -> dict:
    entities_dir = wiki_path / "entities"
    maps_dir = wiki_path / "maps"

    if not entities_dir.exists():
        return {"error": f"wiki/entities/ not found at {entities_dir}"}

    pages = {}
    paths_by_basename = defaultdict(list)
    files = list(entities_dir.rglob("*.md"))
    if maps_dir.exists():
        files += list(maps_dir.rglob("*.md"))

    # v1.3.7: vault root 的 Wiki_*.md 與 WIKI_*.md 也納入掃描
    vault_root = wiki_path.parent
    if vault_root.exists():
        for p in vault_root.glob("Wiki_*.md"):
            files.append(p)
        for p in vault_root.glob("WIKI_*.md"):
            files.append(p)

    # v1.3.6: 跳過 .fuse_hidden* 與其他點號開頭的暫存檔
    files = [p for p in files if not p.name.startswith(".")]

    for p in files:
        name = nfc(p.stem)
        try:
            rel = str(p.relative_to(wiki_path))
        except ValueError:
            rel = str(p)
        paths_by_basename[name].append(rel)

        content, words = parse_md(p)
        strong, inferred, full = extract_links(content)
        if name in pages:
            continue
        pages[name] = {
            "outlinks_strong": strong,
            "outlinks_inferred": inferred,
            "outlinks_all": strong | inferred,
            "outlinks_full": full,
            "inlinks": set(),
            "inlinks_strong": set(),
            "inlinks_inferred": set(),
            "words": words,
        }

    for name, page in pages.items():
        for target in page["outlinks_strong"]:
            if target in pages and target != name:
                pages[target]["inlinks"].add(name)
                pages[target]["inlinks_strong"].add(name)
        for target in page["outlinks_inferred"]:
            if target in pages and target != name:
                pages[target]["inlinks"].add(name)
                pages[target]["inlinks_inferred"].add(name)

    missing = defaultdict(list)
    for name, page in pages.items():
        for full_target, _is_inferred in page["outlinks_full"]:
            if any(full_target.startswith(p) for p in LEGITIMATE_PREFIXES):
                continue
            stripped = full_target.split("/")[-1] if "/" in full_target else full_target
            if not stripped:
                missing["(empty)"].append(name)
                continue
            stripped = nfc(stripped)
            if stripped in pages or stripped in LEGITIMATE_NAMES:
                continue
            if re.match(r'^\d+-', stripped):
                continue
            missing[stripped].append(name)

    orphans = [n for n, p in pages.items() if len(p["inlinks"]) == 0]

    low_inlink = sorted(
        [(n, len(p["inlinks"])) for n, p in pages.items()
         if 0 < len(p["inlinks"]) < 2],
        key=lambda x: x[1]
    )

    hubs = sorted(
        [(n, len(p["inlinks"])) for n, p in pages.items()],
        key=lambda x: -x[1]
    )[:10]

    god_nodes = []
    for name, p in pages.items():
        inlink_count = len(p["inlinks"])
        if inlink_count < GOD_NODE_INLINK_MIN:
            continue
        words = p["words"]
        ratio = words / max(inlink_count, 1)
        if words < GOD_NODE_WORDS_THIN or ratio < GOD_NODE_RATIO_THIN:
            severity = "critical" if (words < GOD_NODE_WORDS_THIN and ratio < GOD_NODE_RATIO_THIN) else "warn"
            god_nodes.append({
                "name": name,
                "inlinks": inlink_count,
                "words": words,
                "ratio": round(ratio, 1),
                "severity": severity,
            })
    god_nodes.sort(key=lambda g: (-g["inlinks"], g["ratio"]))

    inferred_pages = []
    for name, p in pages.items():
        s = len(p["outlinks_strong"])
        i = len(p["outlinks_inferred"])
        total = s + i
        if total < 3:
            continue
        ratio = i / total
        if ratio >= 0.5:
            inferred_pages.append([name, i, total, round(ratio * 100, 1)])
    inferred_pages.sort(key=lambda x: -x[3])

    collisions = []
    for basename, paths in paths_by_basename.items():
        if len(paths) > 1:
            collisions.append({
                "basename": basename,
                "paths": sorted(paths),
                "count": len(paths),
            })
    collisions.sort(key=lambda c: (-c["count"], c["basename"]))

    orphan_score = max(0, 16 - len(orphans) * 4)
    missing_score = max(0, 16 - len(missing) * 2)
    density_score = max(0, 16 - len(low_inlink) * 2)
    hub_score = 16 if hubs and hubs[0][1] >= 10 else 10
    crit = sum(1 for g in god_nodes if g["severity"] == "critical")
    warn = sum(1 for g in god_nodes if g["severity"] == "warn")
    godnodes_score = max(0, 16 - crit * 4 - warn * 2)
    collision_score = max(0, 20 - len(collisions) * 5)

    total_score = orphan_score + missing_score + density_score + hub_score + godnodes_score + collision_score

    # v1.3.8/9: cascade completeness check（規則 P 配套，獨立 output 不影響 score）
    incomplete_cascade = check_cascade_completeness(wiki_path.parent, max_age_days=14)

    return {
        "total_pages": len(pages),
        "orphans": orphans,
        "missing_links": dict(missing),
        "low_inlink_pages": low_inlink,
        "hubs": hubs,
        "god_nodes": god_nodes,
        "inferred_link_pages": inferred_pages,
        "collisions": collisions,
        "incomplete_cascade": incomplete_cascade,
        "score": total_score,
        "score_breakdown": {
            "orphans": orphan_score,
            "missing": missing_score,
            "density": density_score,
            "hubs": hub_score,
            "godnodes": godnodes_score,
            "collisions": collision_score,
        },
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: lint.py <wiki_path>"}))
        sys.exit(1)
    wiki_path = Path(sys.argv[1])
    result = lint(wiki_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
