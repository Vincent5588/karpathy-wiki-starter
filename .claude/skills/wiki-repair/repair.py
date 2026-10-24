#!/usr/bin/env python3
"""
wiki-repair detection script for the karpathy-wiki-pattern plugin (v1.3.1).

Categorizes issues from a wiki-lint output into:
  - auto_fixable: structural fixes the LLM can apply atomically
  - needs_review: judgment-call fixes the LLM should plan but not auto-apply

Usage:
    python3 repair.py --vault /path/to/vault [--lint /path/to/lint.json] [--plan-only]

If --lint omitted, runs wiki-lint internally (assumes lint.py is sibling skill).

Outputs JSON to stdout.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from collections import defaultdict


REQUIRED_FRONTMATTER_FIELDS = ["title", "domain", "type", "status", "created", "updated"]
DEFAULT_FRONTMATTER_VALUES = {
    "status": "draft",
    "aliases": "[]",
}

# v1.3 standard type vocabulary
V13_TYPE_VOCABULARY = {"process", "concept", "role", "artifact", "pattern", "system", "rule"}


def parse_frontmatter(text):
    """Return dict of frontmatter fields, or None if no frontmatter block."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fm_text = text[4:end]
    fm = {}
    current_key = None
    for line in fm_text.split("\n"):
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$', line)
        if m:
            current_key = m.group(1)
            value = m.group(2).strip()
            if value:
                fm[current_key] = value
            else:
                fm[current_key] = []
        elif line.startswith("  - ") and current_key in fm and isinstance(fm[current_key], list):
            fm[current_key].append(line[4:].strip())
    return fm


def extract_basename_from_wikilink(target):
    target = target.split("#")[0]
    if "/" in target:
        target = target.split("/")[-1]
    return target.strip()


def extract_source_paths(fm):
    src = fm.get("source") or fm.get("sources")
    if not src:
        return []
    if isinstance(src, str):
        src = src.strip().strip('"').strip("'")
        src = re.sub(r'^\[\[(.+)\]\]$', r'\1', src)
        return [src]
    paths = []
    for s in src:
        s = s.strip().strip('"').strip("'")
        s = re.sub(r'^\[\[(.+)\]\]$', r'\1', s)
        if s:
            paths.append(s)
    return paths


def find_basename_in_vault(vault, basename):
    return list(vault.rglob(f"{basename}.md"))


def detect_broken_sources(vault, entities_dir):
    issues = []
    for md_file in entities_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8-sig")
        fm = parse_frontmatter(text)
        if not fm:
            continue
        for src_path in extract_source_paths(fm):
            if src_path.startswith(("http://", "https://")):
                continue
            full = vault / src_path
            if not full.exists() and not src_path.endswith(".md"):
                full = vault / (src_path + ".md")
            if full.exists():
                continue
            basename = extract_basename_from_wikilink(src_path)
            if basename.endswith(".md"):
                basename = basename[:-3]
            matches = find_basename_in_vault(vault, basename)
            matches = [m for m in matches if m.resolve() != md_file.resolve()]
            if len(matches) == 1:
                relative = matches[0].relative_to(vault).as_posix()
                wikilink_form = relative
                if wikilink_form.endswith(".md"):
                    wikilink_form = wikilink_form[:-3]
                issues.append({
                    "entity": md_file.relative_to(vault).as_posix(),
                    "frontmatter_field": "source",
                    "broken_path": src_path,
                    "suggested_path": wikilink_form,
                    "match_basis": "single basename match",
                    "auto_fixable": True,
                })
            elif len(matches) > 1:
                issues.append({
                    "entity": md_file.relative_to(vault).as_posix(),
                    "frontmatter_field": "source",
                    "broken_path": src_path,
                    "candidates": [m.relative_to(vault).as_posix() for m in matches],
                    "match_basis": f"{len(matches)} basename matches",
                    "auto_fixable": False,
                })
            else:
                issues.append({
                    "entity": md_file.relative_to(vault).as_posix(),
                    "frontmatter_field": "source",
                    "broken_path": src_path,
                    "candidates": [],
                    "match_basis": "no basename match found",
                    "auto_fixable": False,
                })
    return issues


def detect_missing_frontmatter(vault, entities_dir):
    issues = []
    for md_file in entities_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8-sig")
        fm = parse_frontmatter(text)
        rel = md_file.relative_to(vault).as_posix()
        if not fm:
            issues.append({
                "entity": rel,
                "missing_fields": REQUIRED_FRONTMATTER_FIELDS,
                "suggested_values": {"status": "draft"},
                "auto_fixable": False,
                "note": "Entire frontmatter missing — needs human attention",
            })
            continue
        missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if f not in fm]
        if not missing:
            continue
        suggested = {}
        for field in missing:
            if field == "status":
                suggested[field] = "draft"
            elif field in ("domain", "type"):
                parts = md_file.parts
                try:
                    eidx = parts.index("entities")
                    if field == "domain" and len(parts) > eidx + 1:
                        suggested[field] = parts[eidx + 1]
                    elif field == "type" and len(parts) > eidx + 2:
                        suggested[field] = parts[eidx + 2]
                except ValueError:
                    pass
        auto = bool(missing) and all(f in suggested for f in missing)
        issues.append({
            "entity": rel,
            "missing_fields": missing,
            "suggested_values": suggested,
            "auto_fixable": auto,
        })
    return issues


def detect_orphan_backlink_candidates(vault, entities_dir, lint_data):
    issues = []
    orphans = lint_data.get("orphans", [])
    if not orphans:
        return []
    for orphan_name in orphans:
        candidates = []
        for f in entities_dir.rglob("*.md"):
            if f.stem == orphan_name:
                continue
            content = f.read_text(encoding="utf-8-sig")
            if content.startswith("---\n"):
                end = content.find("\n---\n", 4)
                if end > 0:
                    content = content[end + 5:]
            # Strip fenced code blocks
            content_clean = re.sub(r'```[\s\S]*?```', '', content)
            mentions = []
            for m in re.finditer(re.escape(orphan_name), content_clean):
                pos = m.start()
                preceding = content_clean[max(0, pos - 2):pos]
                if preceding == "[[":
                    continue
                # Skip if it's part of a path-style wiki-link like [[X/orphan_name]]
                line_start = content_clean.rfind("\n", 0, pos) + 1
                seg = content_clean[line_start:pos + len(orphan_name) + 2]
                if "[[" in seg:
                    bracket_open = seg.rfind("[[")
                    bracket_close = seg.find("]]", bracket_open)
                    if bracket_open >= 0 and (bracket_close < 0 or bracket_close > pos - line_start):
                        # Possibly wrapped — be conservative, skip
                        if seg[bracket_open:].find(orphan_name) >= 0:
                            continue
                mentions.append(pos)
            if mentions:
                candidates.append({
                    "candidate_entity": f.relative_to(vault).as_posix(),
                    "mention_count": len(mentions),
                })
        if candidates:
            candidates.sort(key=lambda c: -c["mention_count"])
            auto = len(candidates) <= 2
            issues.append({
                "orphan": orphan_name,
                "candidates": candidates[:3],
                "auto_fixable": auto,
                "note": "Top candidate gets the backlink" if auto else "Multiple candidates — user picks",
            })
    return issues


def detect_god_nodes_review(lint_data):
    return [{
        "page": gn["name"],
        "inlinks": gn["inlinks"],
        "words": gn["words"],
        "ratio": gn["ratio"],
        "severity": gn["severity"],
        "split_suggestion": "Consider splitting into atomic sub-pages" if gn["inlinks"] >= 15 else "Expand body content to >=800 words",
    } for gn in lint_data.get("god_nodes", [])]


def detect_dead_links_resolvable(vault, entities_dir, lint_data):
    issues = []
    missing = lint_data.get("missing_links", {})
    file_index = {}
    for f in entities_dir.rglob("*.md"):
        file_index.setdefault(f.stem, []).append(f)
    maps_dir = vault / "wiki" / "maps"
    if maps_dir.exists():
        for f in maps_dir.rglob("*.md"):
            file_index.setdefault(f.stem, []).append(f)
    for missing_name, referrers in missing.items():
        if missing_name in file_index:
            issues.append({
                "missing_link": missing_name,
                "referrers": referrers,
                "found_at": [f.relative_to(vault).as_posix() for f in file_index[missing_name]],
                "note": "Obsidian resolves by basename — link works, no edit needed",
            })
    return issues


def main():
    parser = argparse.ArgumentParser(description="wiki-repair detection script")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--lint", help="Path to lint.json (if omitted, runs lint internally)")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    entities_dir = vault / "wiki" / "entities"
    if not entities_dir.exists():
        print(json.dumps({"error": f"wiki/entities/ not found at {entities_dir}"}))
        sys.exit(1)

    lint_data = {}
    if args.lint:
        p = Path(args.lint)
        if not p.exists():
            print(json.dumps({"error": f"lint.json not found: {p}"}))
            sys.exit(1)
        # utf-8-sig handles both with-BOM (PowerShell Out-File default) and without-BOM
        lint_data = json.loads(p.read_text(encoding="utf-8-sig"))
    else:
        lint_script = Path(__file__).parent.parent / "wiki-lint" / "lint.py"
        if lint_script.exists():
            try:
                proc = subprocess.run(
                    ["python3", str(lint_script), str(vault / "wiki")],
                    capture_output=True, text=True, check=True,
                )
                lint_data = json.loads(proc.stdout)
            except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
                print(json.dumps({"error": f"Could not run lint: {e}"}))
                sys.exit(1)

    broken_sources = detect_broken_sources(vault, entities_dir)
    missing_fm = detect_missing_frontmatter(vault, entities_dir)
    orphan_backlinks = detect_orphan_backlink_candidates(vault, entities_dir, lint_data)
    god_nodes = detect_god_nodes_review(lint_data)
    dead_links_resolvable = detect_dead_links_resolvable(vault, entities_dir, lint_data)

    auto_fixable = {
        "broken_sources": [i for i in broken_sources if i.get("auto_fixable")],
        "missing_frontmatter": [i for i in missing_fm if i.get("auto_fixable")],
        "orphan_backlinks": [i for i in orphan_backlinks if i.get("auto_fixable")],
        "dead_links_resolvable": dead_links_resolvable,
    }
    needs_review = {
        "broken_sources_ambiguous": [i for i in broken_sources if not i.get("auto_fixable")],
        "missing_frontmatter_unsuggestable": [i for i in missing_fm if not i.get("auto_fixable")],
        "orphan_backlinks_multi_candidate": [i for i in orphan_backlinks if not i.get("auto_fixable")],
        "god_nodes": god_nodes,
        "contradictions": [],
        "near_duplicates": [],
    }

    auto_count = sum(len(v) for k, v in auto_fixable.items() if k != "dead_links_resolvable")
    review_count = sum(len(v) for v in needs_review.values())

    output = {
        "auto_fixable": auto_fixable,
        "needs_review": needs_review,
        "stats": {
            "auto_count": auto_count,
            "review_count": review_count,
            "informational_count": len(dead_links_resolvable),
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
