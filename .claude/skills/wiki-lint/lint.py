#!/usr/bin/env python3
"""
wiki-lint script for the karpathy-wiki-pattern plugin.

v1.3.5 (vault patched copy):
- NFC Unicode normalization fix：macOS APFS 把含變音符的 filename 存成 NFD
  （e.g. ö → o + combining diaeresis），但 wiki 連結內文用 NFC。
  加入 unicodedata.normalize('NFC', ...) 讓兩邊比對前都正規化，
  消除 Sönke Ahrens 之類的假 orphan / 假 missing。

v1.3.2 patches (from plugin):
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
    for m in re.finditer(r'\[\[([^|\]\\]+)\\?(?:\|[^\]]+)?\]\](\s*\?\?)?', text):
        raw_target = m.group(1).strip()
        is_inferred = bool(m.group(2))
        full_target = raw_target.split("#")[0]
        full.append((full_target, is_inferred))
        stripped = full_target
        if "/" in stripped:
            stripped = stripped.split("/")[-1]
        # NFC normalize link targets before storing
        stripped = nfc(stripped)
        (inferred if is_inferred else strong).add(stripped)
    return strong, inferred, full


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

    for p in files:
        # NFC normalize the filename stem — macOS APFS stores NFD, links use NFC
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

    return {
        "total_pages": len(pages),
        "orphans": orphans,
        "missing_links": dict(missing),
        "low_inlink_pages": low_inlink,
        "hubs": hubs,
        "god_nodes": god_nodes,
        "inferred_link_pages": inferred_pages,
        "collisions": collisions,
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
