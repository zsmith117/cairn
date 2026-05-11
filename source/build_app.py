#!/usr/bin/env python3
"""Build a self-contained HTML web app from the UXR SOP markdown library."""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
SOP_DIR = ROOT / "markdown"
CHECKLIST_DIR = ROOT / "Checklists"
TEMPLATE_DIR = ROOT / "Templates"
PHASE_DIR = ROOT / "phases"
OUT = ROOT / "index.html"

# Project-guide phases (5-phase research workflow, source: Notion Research Project Guide).
GUIDE_PHASES = [
    {
        "id": "phase-1",
        "number": 1,
        "title": "Project Initiation",
        "blurb": "Stakeholder alignment, ethics approval, and project setup.",
        "duration": "1–2 weeks",
        "sops": ["UXR-001", "UXR-004"],
        "file": "phase-1-project-initiation.md",
    },
    {
        "id": "phase-2",
        "number": 2,
        "title": "Research Design",
        "blurb": "Methodology, recruitment criteria, and materials development.",
        "duration": "1–3 weeks",
        "sops": ["UXR-003", "UXR-004", "UXR-005"],
        "file": "phase-2-research-design.md",
    },
    {
        "id": "phase-3",
        "number": 3,
        "title": "Field Work",
        "blurb": "Recruitment execution, sessions, and live documentation.",
        "duration": "2–4 weeks",
        "sops": ["UXR-001", "UXR-002", "UXR-003", "UXR-006"],
        "file": "phase-3-field-work.md",
    },
    {
        "id": "phase-4",
        "number": 4,
        "title": "Analysis",
        "blurb": "Coding, pattern identification, and insight development.",
        "duration": "1–3 weeks",
        "sops": ["UXR-007"],
        "file": "phase-4-analysis.md",
    },
    {
        "id": "phase-5",
        "number": 5,
        "title": "Delivery & Close",
        "blurb": "Reporting, presentation, and repository archiving.",
        "duration": "1–2 weeks",
        "sops": ["UXR-008", "UXR-009"],
        "file": "phase-5-delivery-close.md",
    },
]

# Lifecycle phase grouping
PHASES = [
    {
        "id": "govern",
        "name": "Govern",
        "blurb": "Ethics, consent, and data protection that earn participant trust.",
        "sops": ["UXR-001", "UXR-002"],
    },
    {
        "id": "plan",
        "name": "Plan",
        "blurb": "Scope studies that answer the right question on the right timeline.",
        "sops": ["UXR-004"],
    },
    {
        "id": "recruit",
        "name": "Recruit",
        "blurb": "Find the right participants and keep the funnel honest.",
        "sops": ["UXR-003"],
    },
    {
        "id": "conduct",
        "name": "Conduct",
        "blurb": "Run sessions that produce data worth analyzing.",
        "sops": ["UXR-005", "UXR-006"],
    },
    {
        "id": "analyze",
        "name": "Analyze",
        "blurb": "Turn raw observation into validated, defensible findings.",
        "sops": ["UXR-007"],
    },
    {
        "id": "communicate",
        "name": "Communicate",
        "blurb": "Move stakeholders from interest to decision.",
        "sops": ["UXR-008"],
    },
    {
        "id": "curate",
        "name": "Curate",
        "blurb": "Compound past research into an asset the team can reuse.",
        "sops": ["UXR-009"],
    },
]

# Shorter display titles for cards/navigation
SOP_DISPLAY = {
    "UXR-001": "Informed Consent & Ethics",
    "UXR-002": "Data Handling & Privacy",
    "UXR-003": "Participant Recruitment & Screening",
    "UXR-004": "Research Planning & Scoping",
    "UXR-005": "Interview Moderation & Guide Development",
    "UXR-006": "Note-Taking & Documentation",
    "UXR-007": "Analysis & Synthesis",
    "UXR-008": "Stakeholder Communication",
    "UXR-009": "Research Repository",
}


def normalize_codeblocks(md: str) -> str:
    """Unwrap fenced blocks that wrap markdown tables.

    Many SOP templates wrap tables inside unlabeled ``` fences for a form-like
    visual, which forces marked to render the table as preformatted text.
    Detect those blocks and convert them to real markdown so tables render
    properly; bold the ALL-CAPS section headers inside them for hierarchy.
    """
    lines = md.split("\n")
    out = []
    i = 0
    # ALL-CAPS form-section headers, e.g. "DATA COLLECTED:" or "THIRD-PARTY PROCESSORS"
    # ALL-CAPS labels like "DATA COLLECTED:" or "2 WEEKS BEFORE:"
    section_label = re.compile(r"^[A-Z0-9][A-Z0-9 _\-/&:]{2,}$")
    # Step-style labels with descriptive text after, like "STEP 1: Required Tags"
    stepped_label = re.compile(r"^[A-Z][A-Z]+\s+\d+:\s+\S")
    fence_open = re.compile(r"^```\s*$")  # only unlabeled fences
    while i < len(lines):
        if fence_open.match(lines[i].strip()):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            block = lines[i + 1 : j]
            has_table = any(
                "|" in line and line.count("|") >= 2 for line in block
            )
            numbered_count = sum(
                1 for line in block if re.match(r"^\s*\d+\.\s+\S", line)
            )
            bulleted_count = sum(
                1 for line in block if re.match(r"^\s*[-*]\s+\S", line)
            )
            form_field_count = sum(1 for line in block if "___" in line)
            checkbox_count = sum(
                1 for line in block
                if re.match(r"^\s*\[[xX ]?\]\s+\S", line)
            )
            label_count = sum(
                1 for line in block
                if section_label.match(line.strip())
                or stepped_label.match(line.strip())
            )
            # Unwrap if the block has any strong markdown signal.
            # Code-like content (ASCII trees, file paths, arrow flows) has none
            # of these, so it stays as a <pre> block.
            should_unwrap = (
                has_table
                or numbered_count >= 2
                or bulleted_count >= 2
                or form_field_count >= 3
                or label_count >= 2
                or checkbox_count >= 2
            )
            if should_unwrap:
                out.append("")
                in_table = False
                for raw in block:
                    s = raw.rstrip()
                    is_table_line = s.lstrip().startswith("|")
                    if is_table_line and not in_table:
                        out.append("")  # blank line before table
                        in_table = True
                    if not is_table_line and in_table:
                        out.append("")  # blank line after table
                        in_table = False
                    stripped = s.strip()
                    if section_label.match(stripped):
                        out.append("**" + stripped + "**")
                    elif stepped_label.match(stripped):
                        out.append("**" + stripped + "**")
                    elif re.match(r"^\s*\[[xX ]?\]\s+\S", s):
                        # Convert bare "[ ] item" to markdown task list "- [ ] item"
                        out.append(re.sub(r"^(\s*)\[", r"\1- [", s))
                    else:
                        out.append(s)
                out.append("")
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def read(path: Path) -> str:
    return normalize_codeblocks(path.read_text(encoding="utf-8"))


def extract_first_h1(md: str) -> str:
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def parse_sop_filename(name: str):
    # e.g. "UXR-001_Informed_Consent_Ethics.md"
    m = re.match(r"(UXR-\d{3})_(.+)\.md$", name)
    if not m:
        return None
    return m.group(1), m.group(2).replace("_", " ")


def parse_attachment_filename(name: str):
    # e.g. "UXR-001_Checklist_7.1_Pre-Study.md"
    # or  "UXR-001_Template_5.1_Standard_Consent_Form.md"
    m = re.match(r"(UXR-\d{3})_(Checklist|Template)_(\d+\.\d+)_(.+)\.md$", name)
    if not m:
        return None
    sop_id, kind, section, rest = m.groups()
    label = rest.replace("_", " ")
    # Trim trailing " Checklist" / " Template" duplication
    for suffix in (" Checklist", " Template"):
        if label.endswith(suffix):
            label = label[: -len(suffix)]
    return {
        "sop_id": sop_id,
        "kind": kind.lower(),
        "section": section,
        "label": label.strip(),
    }


def dedupe(files):
    """For each (sop_id, kind, section) key, keep the file with the longer body."""
    by_key = {}
    for f in files:
        key = (f["sop_id"], f["kind"], f["section"])
        prev = by_key.get(key)
        if prev is None or len(f["content"]) > len(prev["content"]):
            by_key[key] = f
    return sorted(by_key.values(), key=lambda x: (x["sop_id"], x["section"]))


def collect_attachments(dir_path: Path):
    out = []
    for path in sorted(dir_path.glob("*.md")):
        meta = parse_attachment_filename(path.name)
        if not meta:
            continue
        meta["content"] = read(path)
        meta["filename"] = path.name
        out.append(meta)
    return dedupe(out)


def collect_sops():
    sops = {}
    for path in sorted(SOP_DIR.glob("*.md")):
        parsed = parse_sop_filename(path.name)
        if not parsed:
            continue
        sop_id, _ = parsed
        content = read(path)
        sops[sop_id] = {
            "id": sop_id,
            "title": extract_first_h1(content) or SOP_DISPLAY.get(sop_id, sop_id),
            "display": SOP_DISPLAY.get(sop_id, sop_id),
            "content": content,
            "checklists": [],
            "templates": [],
        }
    return sops


def estimate_read_minutes(md: str) -> int:
    words = len(re.findall(r"\w+", md))
    return max(1, round(words / 220))


def collect_guide_phases():
    phases = []
    for ph in GUIDE_PHASES:
        path = PHASE_DIR / ph["file"]
        content = read(path) if path.exists() else f"# {ph['title']}\n\n_Phase content not yet loaded._"
        phases.append(
            {
                "id": ph["id"],
                "number": ph["number"],
                "title": ph["title"],
                "blurb": ph["blurb"],
                "duration": ph["duration"],
                "sops": ph["sops"],
                "content": content,
                "read_minutes": estimate_read_minutes(content),
            }
        )
    return phases


def compute_sop_to_phases(guide_phases):
    """Reverse map: { 'UXR-001': ['phase-1', 'phase-3'], ... }"""
    out = {}
    for ph in guide_phases:
        for sop_id in ph["sops"]:
            out.setdefault(sop_id, []).append(
                {"id": ph["id"], "number": ph["number"], "title": ph["title"]}
            )
    return out


def main():
    sops = collect_sops()
    checklists = collect_attachments(CHECKLIST_DIR)
    templates = collect_attachments(TEMPLATE_DIR)

    for c in checklists:
        if c["sop_id"] in sops:
            sops[c["sop_id"]]["checklists"].append(
                {
                    "section": c["section"],
                    "label": c["label"],
                    "content": c["content"],
                }
            )
    for t in templates:
        if t["sop_id"] in sops:
            sops[t["sop_id"]]["templates"].append(
                {
                    "section": t["section"],
                    "label": t["label"],
                    "content": t["content"],
                }
            )

    for sop in sops.values():
        sop["read_minutes"] = estimate_read_minutes(sop["content"])
        sop["checklist_count"] = len(sop["checklists"])
        sop["template_count"] = len(sop["templates"])

    # Assemble ordered SOP list grouped by phase
    phase_blocks = []
    for ph in PHASES:
        phase_blocks.append(
            {
                "id": ph["id"],
                "name": ph["name"],
                "blurb": ph["blurb"],
                "sops": [sops[s] for s in ph["sops"] if s in sops],
            }
        )

    guide_phases = collect_guide_phases()
    sop_to_phases = compute_sop_to_phases(guide_phases)

    # Attach phase cross-refs to each SOP
    for sop_id, sop in sops.items():
        sop["phase_refs"] = sop_to_phases.get(sop_id, [])

    totals = {
        "sops": len(sops),
        "checklists": sum(len(s["checklists"]) for s in sops.values()),
        "templates": sum(len(s["templates"]) for s in sops.values()),
        "guide_phases": len(guide_phases),
    }

    data = {
        "phases": phase_blocks,
        "guide_phases": guide_phases,
        "totals": totals,
    }
    data_json = json.dumps(data, ensure_ascii=False)

    # Pull marked.min.js so the app is offline-portable
    marked_path = ROOT / ".marked.min.js"
    if not marked_path.exists():
        print("Downloading marked.min.js…")
        url = "https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"
        urllib.request.urlretrieve(url, marked_path)
    marked_js = marked_path.read_text(encoding="utf-8")

    html = TEMPLATE.replace("__DATA__", data_json).replace("__MARKED__", marked_js)
    OUT.write_text(html, encoding="utf-8")
    print(
        f"Wrote {OUT} — {totals['sops']} SOPs, "
        f"{totals['checklists']} checklists, {totals['templates']} templates, "
        f"{OUT.stat().st_size/1024:.0f} KB"
    )


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UX Research SOP Library</title>
<style>
  :root {
    --bg: #fbfaf7;
    --surface: #ffffff;
    --surface-2: #f4f2ec;
    --border: #e7e3da;
    --border-strong: #d4cfc2;
    --text: #1c1b18;
    --text-muted: #6b6960;
    --text-faint: #94918a;
    --accent: #2b4a3e;
    --accent-soft: #e8efe9;
    --accent-ink: #1d342c;
    --tag: #efece4;
    --shadow: 0 1px 2px rgba(20,20,20,.03), 0 8px 24px rgba(20,20,20,.04);
    --radius: 10px;
    --serif: "Iowan Old Style", "Apple Garamond", "Charter", Georgia, "Source Serif Pro", serif;
    --sans: -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", Arial, sans-serif;
    --mono: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
  }
  html[data-theme="dark"] {
    --bg: #15171a;
    --surface: #1c1f23;
    --surface-2: #23272c;
    --border: #2c3036;
    --border-strong: #3b4047;
    --text: #ebe9e3;
    --text-muted: #a4a39c;
    --text-faint: #75736c;
    --accent: #8fc4af;
    --accent-soft: #1f2c27;
    --accent-ink: #c8e4d7;
    --tag: #262a2f;
    --shadow: 0 1px 2px rgba(0,0,0,.3), 0 12px 32px rgba(0,0,0,.35);
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text); }
  body {
    font-family: var(--sans);
    font-size: 15px;
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
  }
  a { color: inherit; text-decoration: none; }
  button { font-family: inherit; cursor: pointer; }

  /* Layout */
  .app {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 100vh;
  }
  @media (max-width: 880px) {
    .app { grid-template-columns: 1fr; }
    .sidebar { position: static !important; height: auto !important; border-right: none !important; border-bottom: 1px solid var(--border); }
  }

  /* Sidebar */
  .sidebar {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 24px 20px;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
    cursor: pointer;
  }
  .brand-mark {
    width: 28px; height: 28px;
    border-radius: 7px;
    background: var(--accent);
    color: var(--surface);
    display: grid; place-items: center;
    font-family: var(--serif);
    font-weight: 600;
    font-size: 14px;
    letter-spacing: .02em;
  }
  html[data-theme="dark"] .brand-mark { color: var(--bg); }
  .brand-name {
    font-family: var(--serif);
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -.01em;
  }
  .brand-sub {
    margin: 4px 0 22px 38px;
    font-size: 12px;
    color: var(--text-faint);
    letter-spacing: .04em;
    text-transform: uppercase;
  }

  .mode-toggle {
    display: flex;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 2px;
    margin-bottom: 14px;
  }
  .mode-toggle button {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 6px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: .01em;
    cursor: pointer;
    transition: background .15s, color .15s;
  }
  .mode-toggle button.active {
    background: var(--surface);
    color: var(--text);
    box-shadow: 0 1px 2px rgba(0,0,0,.05);
  }
  html[data-theme="dark"] .mode-toggle button.active { box-shadow: 0 1px 2px rgba(0,0,0,.3); }

  .search-btn {
    width: 100%;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 8px 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    margin-bottom: 20px;
    transition: border-color .15s;
  }
  .search-btn:hover { border-color: var(--border-strong); }
  .search-btn .kbd {
    margin-left: auto;
    font-family: var(--mono);
    font-size: 11px;
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 1px 5px;
    border-radius: 4px;
    color: var(--text-faint);
  }

  .nav-phase {
    margin-bottom: 18px;
  }
  .nav-phase-header {
    display: flex;
    align-items: baseline;
    gap: 8px;
    font-size: 11px;
    color: var(--text-faint);
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 6px;
    font-weight: 600;
  }
  .nav-phase-num {
    font-family: var(--mono);
    color: var(--text-faint);
  }
  .nav-link {
    display: block;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 13.5px;
    color: var(--text-muted);
    line-height: 1.35;
    margin-bottom: 1px;
    cursor: pointer;
    border-left: 2px solid transparent;
  }
  .nav-link:hover { background: var(--surface-2); color: var(--text); }
  .nav-link.active {
    background: var(--accent-soft);
    color: var(--accent-ink);
    border-left-color: var(--accent);
    font-weight: 500;
  }
  .nav-link .nav-id {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    margin-right: 6px;
  }
  .nav-link.active .nav-id { color: var(--accent); }

  .sidebar-footer {
    margin-top: 28px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .theme-toggle {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    width: 32px; height: 32px;
    border-radius: 8px;
    display: grid; place-items: center;
    transition: border-color .15s, color .15s;
  }
  .theme-toggle:hover { color: var(--text); border-color: var(--border-strong); }
  .footer-meta {
    font-size: 11px;
    color: var(--text-faint);
    margin-left: auto;
  }

  /* Main */
  .main { padding: 56px 64px 96px; max-width: 1100px; }
  @media (max-width: 1100px) { .main { padding: 40px 32px 64px; } }
  @media (max-width: 600px) { .main { padding: 24px 18px 64px; } }

  .home-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  .home-title {
    font-family: var(--serif);
    font-size: 44px;
    line-height: 1.08;
    letter-spacing: -.02em;
    margin: 0 0 16px;
    font-weight: 500;
  }
  .home-lede {
    font-family: var(--serif);
    font-size: 19px;
    line-height: 1.55;
    color: var(--text-muted);
    max-width: 640px;
    margin: 0 0 36px;
  }

  .stat-row {
    display: flex;
    gap: 28px;
    padding: 18px 0 28px;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin-bottom: 44px;
  }
  .stat .n {
    font-family: var(--serif);
    font-size: 28px;
    font-weight: 500;
    letter-spacing: -.01em;
  }
  .stat .l {
    font-size: 11px;
    color: var(--text-faint);
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-top: 2px;
  }

  .phase-section { margin-bottom: 44px; }
  .phase-head {
    display: flex;
    align-items: baseline;
    gap: 14px;
    margin-bottom: 14px;
  }
  .phase-num {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-faint);
    letter-spacing: .08em;
  }
  .phase-name {
    font-family: var(--serif);
    font-size: 22px;
    font-weight: 500;
    letter-spacing: -.01em;
    margin: 0;
  }
  .phase-blurb {
    color: var(--text-muted);
    font-size: 14px;
    margin: 2px 0 14px;
    max-width: 640px;
  }
  .phase-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
  }
  .sop-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 18px 16px;
    cursor: pointer;
    transition: border-color .15s, transform .15s, box-shadow .15s;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .sop-card:hover {
    border-color: var(--border-strong);
    transform: translateY(-1px);
    box-shadow: var(--shadow);
  }
  .sop-card-id {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    letter-spacing: .04em;
  }
  .sop-card-title {
    font-family: var(--serif);
    font-size: 18px;
    font-weight: 500;
    line-height: 1.25;
    letter-spacing: -.01em;
    color: var(--text);
  }
  .sop-card-meta {
    display: flex;
    gap: 10px;
    margin-top: auto;
    padding-top: 12px;
    font-size: 12px;
    color: var(--text-faint);
  }
  .sop-card-meta span { display: inline-flex; align-items: center; gap: 4px; }

  /* SOP detail page */
  .sop-detail-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 220px;
    gap: 48px;
    align-items: start;
  }
  @media (max-width: 1000px) {
    .sop-detail-grid { grid-template-columns: 1fr; }
    .toc { display: none; }
  }
  .breadcrumb {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    letter-spacing: .08em;
    margin-bottom: 14px;
    text-transform: uppercase;
  }
  .breadcrumb a { color: var(--text-muted); }
  .breadcrumb a:hover { color: var(--text); }
  .breadcrumb .sep { margin: 0 8px; opacity: .5; }

  .sop-title-row { display: flex; align-items: flex-start; gap: 12px; }
  .sop-title {
    font-family: var(--serif);
    font-size: 36px;
    font-weight: 500;
    line-height: 1.12;
    letter-spacing: -.02em;
    margin: 0 0 12px;
  }
  .sop-id-pill {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--accent-ink);
    background: var(--accent-soft);
    padding: 3px 8px;
    border-radius: 999px;
    margin-top: 12px;
    white-space: nowrap;
  }
  .sop-meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 12.5px;
    color: var(--text-faint);
    margin-bottom: 28px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--border);
  }

  .tabs {
    display: flex;
    gap: 4px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
    position: sticky;
    top: 0;
    background: var(--bg);
    z-index: 5;
    padding-top: 4px;
  }
  .tab {
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 10px 4px;
    margin-right: 22px;
    font-size: 13px;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    position: relative;
    top: 1px;
    letter-spacing: .01em;
  }
  .tab .count {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    margin-left: 4px;
  }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--text); border-bottom-color: var(--accent); }
  .tab.active .count { color: var(--text-muted); }

  /* Prose */
  .prose { font-size: 15px; line-height: 1.65; color: var(--text); }
  .prose h1 { display: none; }
  .prose h2 {
    font-family: var(--serif);
    font-weight: 500;
    font-size: 24px;
    letter-spacing: -.01em;
    margin: 44px 0 12px;
    padding-top: 8px;
    line-height: 1.2;
    scroll-margin-top: 64px;
  }
  .prose h3 {
    font-family: var(--serif);
    font-weight: 500;
    font-size: 19px;
    letter-spacing: -.005em;
    margin: 28px 0 10px;
    line-height: 1.25;
    scroll-margin-top: 64px;
  }
  .prose h4 {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: var(--text-muted);
    margin: 22px 0 8px;
    font-weight: 600;
  }
  .prose p { margin: 0 0 14px; }
  .prose strong { color: var(--text); font-weight: 600; }
  .prose ul, .prose ol { margin: 0 0 16px; padding-left: 22px; }
  .prose li { margin: 4px 0; }
  .prose li > p { margin: 0; }
  .prose hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }
  .prose code {
    font-family: var(--mono);
    font-size: 13px;
    background: var(--surface-2);
    padding: 1px 5px;
    border-radius: 4px;
  }
  .prose pre {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    overflow-x: auto;
    font-size: 13px;
  }
  .prose pre code { background: transparent; padding: 0; }
  .prose blockquote {
    border-left: 3px solid var(--border-strong);
    padding: 2px 0 2px 16px;
    color: var(--text-muted);
    margin: 16px 0;
    font-style: italic;
  }
  .prose .table-scroll {
    overflow-x: auto;
    margin: 16px 0;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--surface);
  }
  .prose .table-scroll table {
    width: 100%;
    border-collapse: collapse;
    margin: 0;
    font-size: 13.5px;
    min-width: max-content;
  }
  .prose th, .prose td {
    border-bottom: 1px solid var(--border);
    border-right: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
    vertical-align: top;
  }
  .prose th:last-child, .prose td:last-child { border-right: none; }
  .prose tr:last-child td { border-bottom: none; }
  .prose th {
    background: var(--surface-2);
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: var(--text-muted);
    white-space: nowrap;
  }
  .prose a {
    color: var(--accent);
    border-bottom: 1px solid color-mix(in srgb, var(--accent) 35%, transparent);
  }
  .prose a:hover { border-bottom-color: var(--accent); }

  /* Collapsible attachment list */
  .attach-list { display: flex; flex-direction: column; gap: 8px; }
  .attach {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    scroll-margin-top: 64px;
  }
  .attach-head {
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    color: var(--text);
  }
  .attach-head:hover { background: var(--surface-2); }
  .attach-section {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    background: var(--surface-2);
    padding: 2px 7px;
    border-radius: 4px;
    flex-shrink: 0;
  }
  .attach-title {
    font-family: var(--serif);
    font-size: 16px;
    font-weight: 500;
    letter-spacing: -.005em;
    flex: 1;
  }
  .attach-chev {
    color: var(--text-faint);
    transition: transform .2s;
  }
  .attach.open .attach-chev { transform: rotate(90deg); }
  .attach-body {
    display: none;
    padding: 4px 28px 20px 28px;
    border-top: 1px solid var(--border);
  }
  .attach.open .attach-body { display: block; }

  /* Word download button */
  .word-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 7px 12px;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 500;
    transition: background .15s, border-color .15s, color .15s;
  }
  .word-btn:hover {
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent-ink);
  }
  html[data-theme="dark"] .word-btn:hover { color: var(--accent); }
  .attach-actions {
    margin-top: 18px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
  }
  .attach-hint {
    font-size: 11.5px;
    color: var(--text-faint);
  }
  .proc-actions {
    margin-bottom: 20px;
    display: flex;
    justify-content: flex-end;
  }

  /* Guide phase cards on the home page */
  .guide-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 26px;
    cursor: pointer;
    display: grid;
    grid-template-columns: 56px 1fr auto;
    gap: 24px;
    align-items: center;
    margin-bottom: 12px;
    transition: border-color .15s, transform .15s, box-shadow .15s;
  }
  .guide-card:hover {
    border-color: var(--border-strong);
    transform: translateY(-1px);
    box-shadow: var(--shadow);
  }
  .guide-card-num {
    font-family: var(--serif);
    font-size: 36px;
    font-weight: 500;
    color: var(--accent);
    line-height: 1;
    letter-spacing: -.02em;
  }
  .guide-card-body { min-width: 0; }
  .guide-card-title {
    font-family: var(--serif);
    font-size: 20px;
    font-weight: 500;
    letter-spacing: -.01em;
    margin: 0 0 4px;
  }
  .guide-card-blurb {
    color: var(--text-muted);
    font-size: 13.5px;
    margin: 0 0 10px;
  }
  .guide-card-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 12px;
    color: var(--text-faint);
  }
  .guide-card-arrow {
    color: var(--text-faint);
    font-size: 22px;
    transition: color .15s, transform .15s;
  }
  .guide-card:hover .guide-card-arrow { color: var(--accent); transform: translateX(2px); }
  .guide-card-progress {
    height: 3px;
    background: var(--surface-2);
    border-radius: 2px;
    margin-top: 10px;
    overflow: hidden;
  }
  .guide-card-progress-bar {
    height: 100%;
    background: var(--accent);
    transition: width .25s;
  }

  /* Phase pill on SOP detail (cross-reference back to guide) */
  .phase-pills {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
  }
  .phase-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--accent-ink);
    background: var(--accent-soft);
    border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
    padding: 3px 9px;
    border-radius: 999px;
    cursor: pointer;
    text-decoration: none;
    transition: background .15s;
  }
  html[data-theme="dark"] .phase-pill { color: var(--accent); }
  .phase-pill:hover { background: color-mix(in srgb, var(--accent) 15%, var(--surface)); }

  /* Phase detail view */
  .phase-hero {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
  }
  .phase-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--accent);
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-weight: 600;
  }
  .phase-title-detail {
    font-family: var(--serif);
    font-size: 38px;
    font-weight: 500;
    line-height: 1.1;
    letter-spacing: -.02em;
    margin: 0 0 10px;
  }
  .phase-meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    font-size: 12.5px;
    color: var(--text-faint);
    margin-top: 12px;
  }
  .phase-meta-row strong { color: var(--text-muted); font-weight: 600; }

  /* Sidebar nav variants */
  .nav-phase-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 6px;
    font-size: 13.5px;
    color: var(--text-muted);
    cursor: pointer;
    margin-bottom: 2px;
    border-left: 2px solid transparent;
  }
  .nav-phase-link:hover { background: var(--surface-2); color: var(--text); }
  .nav-phase-link.active {
    background: var(--accent-soft);
    color: var(--accent-ink);
    border-left-color: var(--accent);
    font-weight: 500;
  }
  html[data-theme="dark"] .nav-phase-link.active { color: var(--accent); }
  .nav-phase-num-circle {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: var(--surface-2);
    color: var(--text-muted);
    display: grid;
    place-items: center;
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 600;
    flex-shrink: 0;
  }
  .nav-phase-link.active .nav-phase-num-circle {
    background: var(--accent);
    color: var(--surface);
  }
  html[data-theme="dark"] .nav-phase-link.active .nav-phase-num-circle { color: var(--bg); }
  .nav-section-label {
    font-size: 10px;
    color: var(--text-faint);
    text-transform: uppercase;
    letter-spacing: .14em;
    margin: 4px 0 10px 2px;
    font-weight: 600;
  }

  /* TOC */
  .toc {
    position: sticky;
    top: 80px;
    align-self: start;
    border-left: 1px solid var(--border);
    padding-left: 18px;
    max-height: calc(100vh - 120px);
    overflow-y: auto;
  }
  .toc-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: var(--text-faint);
    margin-bottom: 12px;
    font-weight: 600;
  }
  .toc a {
    display: block;
    padding: 4px 0;
    font-size: 12.5px;
    color: var(--text-muted);
    line-height: 1.4;
    border-left: 2px solid transparent;
    padding-left: 10px;
    margin-left: -10px;
  }
  .toc a.h3 { padding-left: 22px; font-size: 12px; }
  .toc a:hover { color: var(--text); }
  .toc a.active {
    color: var(--accent-ink);
    border-left-color: var(--accent);
    font-weight: 500;
  }
  html[data-theme="dark"] .toc a.active { color: var(--accent); }

  /* Search modal */
  .modal-bg {
    position: fixed; inset: 0;
    background: rgba(20,20,20,.35);
    display: none;
    z-index: 50;
    padding-top: 12vh;
  }
  html[data-theme="dark"] .modal-bg { background: rgba(0,0,0,.55); }
  .modal-bg.open { display: block; }
  .modal {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    max-width: 640px;
    margin: 0 auto;
    box-shadow: var(--shadow);
    overflow: hidden;
  }
  .search-input {
    width: 100%;
    border: none;
    border-bottom: 1px solid var(--border);
    background: transparent;
    padding: 18px 22px;
    font-size: 16px;
    color: var(--text);
    outline: none;
    font-family: var(--sans);
  }
  .search-results {
    max-height: 60vh;
    overflow-y: auto;
    padding: 6px 0;
  }
  .search-result {
    padding: 10px 22px;
    cursor: pointer;
    border-left: 2px solid transparent;
  }
  .search-result:hover, .search-result.sel {
    background: var(--surface-2);
    border-left-color: var(--accent);
  }
  .search-result-title {
    font-family: var(--serif);
    font-size: 15px;
    font-weight: 500;
  }
  .search-result-meta {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    margin-top: 2px;
  }
  .search-result-snippet {
    color: var(--text-muted);
    font-size: 12.5px;
    margin-top: 4px;
    line-height: 1.4;
  }
  .search-result-snippet mark {
    background: var(--accent-soft);
    color: var(--accent-ink);
    padding: 0 2px;
    border-radius: 3px;
  }
  .search-empty {
    padding: 32px 22px;
    text-align: center;
    color: var(--text-faint);
    font-size: 13px;
  }
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="brand" onclick="goHome()">
      <div class="brand-mark">UX</div>
      <div class="brand-name">SOP Library</div>
    </div>
    <div class="brand-sub">UX Research Operations</div>

    <div class="mode-toggle" id="mode-toggle">
      <button id="mode-guide" onclick="route('guide')">Project Guide</button>
      <button id="mode-library" onclick="route('library')">SOP Library</button>
    </div>

    <button class="search-btn" onclick="openSearch()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      Search SOPs, checklists, templates
      <span class="kbd">⌘K</span>
    </button>

    <nav id="nav"></nav>

    <div class="sidebar-footer">
      <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
        <svg id="theme-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"></svg>
      </button>
      <div class="footer-meta">v1.0 · 2026</div>
    </div>
  </aside>

  <main class="main" id="main"></main>
</div>

<div class="modal-bg" id="modal-bg" onclick="if(event.target===this)closeSearch()">
  <div class="modal">
    <input id="search-input" class="search-input" type="text" placeholder="Search across all documents…" autocomplete="off">
    <div id="search-results" class="search-results"></div>
  </div>
</div>

<script>__MARKED__</script>
<script>
const DATA = __DATA__;

// Flatten for lookups
const SOPS = {};
DATA.phases.forEach(p => p.sops.forEach(s => SOPS[s.id] = s));

// Build search index
const SEARCH_DOCS = [];
DATA.phases.forEach(phase => {
  phase.sops.forEach(sop => {
    SEARCH_DOCS.push({
      route: `sop/${sop.id}/procedure`,
      title: sop.display,
      kind: 'SOP',
      sopId: sop.id,
      phase: phase.name,
      body: sop.content.toLowerCase(),
      raw: sop.content,
    });
    sop.checklists.forEach(c => SEARCH_DOCS.push({
      route: `sop/${sop.id}/checklists#sec-${c.section.replace('.','-')}`,
      title: c.label,
      kind: 'Checklist',
      sopId: sop.id,
      section: c.section,
      phase: phase.name,
      body: c.content.toLowerCase(),
      raw: c.content,
    }));
    sop.templates.forEach(t => SEARCH_DOCS.push({
      route: `sop/${sop.id}/templates#sec-${t.section.replace('.','-')}`,
      title: t.label,
      kind: 'Template',
      sopId: sop.id,
      section: t.section,
      phase: phase.name,
      body: t.content.toLowerCase(),
      raw: t.content,
    }));
  });
});
// Index guide phases too
DATA.guide_phases.forEach(ph => {
  SEARCH_DOCS.push({
    route: `guide/${ph.id}`,
    title: `Phase ${ph.number}: ${ph.title}`,
    kind: 'Guide Phase',
    sopId: '',
    phase: 'Project Guide',
    body: ph.content.toLowerCase(),
    raw: ph.content,
  });
});

marked.setOptions({ gfm: true, breaks: false });

function renderMd(md) {
  const html = marked.parse(md);
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  tmp.querySelectorAll('table').forEach(t => {
    if (t.parentElement.classList.contains('table-scroll')) return;
    const wrap = document.createElement('div');
    wrap.className = 'table-scroll';
    t.parentNode.insertBefore(wrap, t);
    wrap.appendChild(t);
  });
  return tmp.innerHTML;
}

// ---- Word download ----
const WORD_CSS = `
  body { font-family: Calibri, "Segoe UI", sans-serif; font-size: 11pt; color: #1a1a1a; max-width: 6.5in; margin: 0.5in auto; line-height: 1.4; }
  h1 { font-family: "Cambria", Georgia, serif; font-size: 22pt; font-weight: 500; margin: 0 0 12pt; }
  h2 { font-family: "Cambria", Georgia, serif; font-size: 15pt; font-weight: 500; margin: 24pt 0 8pt; }
  h3 { font-family: "Cambria", Georgia, serif; font-size: 13pt; font-weight: 500; margin: 18pt 0 6pt; }
  h4 { font-size: 11pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5pt; margin: 14pt 0 4pt; }
  p { margin: 0 0 8pt; }
  ul, ol { margin: 0 0 10pt; padding-left: 24pt; }
  li { margin: 2pt 0; }
  hr { border: none; border-top: 1pt solid #ccc; margin: 18pt 0; }
  table { border-collapse: collapse; width: 100%; margin: 10pt 0; }
  th, td { border: 1pt solid #888; padding: 6pt 8pt; text-align: left; vertical-align: top; font-size: 10pt; }
  th { background: #eee; font-weight: 700; }
  blockquote { border-left: 2pt solid #888; padding-left: 12pt; color: #555; margin: 10pt 0; }
  code { font-family: "Consolas", monospace; background: #f4f4f4; padding: 1pt 3pt; }
  pre { font-family: "Consolas", monospace; background: #f4f4f4; padding: 8pt; white-space: pre-wrap; }
  .meta { color: #666; font-size: 9.5pt; margin-bottom: 18pt; padding-bottom: 10pt; border-bottom: 1pt solid #ddd; }
`;

function downloadAsWord(title, sopId, markdown) {
  let html = marked.parse(markdown);
  // Word-friendly checkboxes: replace marked's <input> with Unicode glyphs
  html = html.replace(/<input[^>]*type="checkbox"[^>]*checked[^>]*>\s*/gi, '☑ ');
  html = html.replace(/<input[^>]*type="checkbox"[^>]*>\s*/gi, '☐ ');
  // Remove the bullet on task-list items so the box stands alone
  html = html.replace(/<li>(\s*☐|\s*☑)/g, '<li style="list-style:none; margin-left:-18pt;">$1');

  const today = new Date().toISOString().slice(0, 10);
  const doc = `<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8"><title>${escapeHtml(title)}</title>
<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->
<style>${WORD_CSS}</style></head>
<body>
<h1>${escapeHtml(title)}</h1>
<div class="meta">Source: ${escapeHtml(sopId)} · Exported ${today}</div>
${html}
</body></html>`;

  const filename = (title.replace(/[\\/:*?"<>|]+/g, '').replace(/\s+/g, ' ').trim()) + '.doc';
  const blob = new Blob(['﻿', doc], { type: 'application/msword' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 100);
}

// Use a data-store so the markdown content doesn't have to be re-embedded in onclick handlers
const DOWNLOAD_REGISTRY = new Map();
function registerDownload(key, title, sopId, markdown) {
  DOWNLOAD_REGISTRY.set(key, { title, sopId, markdown });
}
function triggerDownload(key) {
  const d = DOWNLOAD_REGISTRY.get(key);
  if (d) downloadAsWord(d.title, d.sopId, d.markdown);
}

const DOWNLOAD_ICON = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>';

// ---- Theme ----
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('sop-theme', t);
  const icon = document.getElementById('theme-icon');
  if (t === 'dark') {
    icon.innerHTML = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>';
  } else {
    icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
  }
}
function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme') || 'light';
  applyTheme(cur === 'dark' ? 'light' : 'dark');
}
applyTheme(localStorage.getItem('sop-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));

// ---- Sidebar ----
function renderGuideNav(activePhaseId) {
  const nav = document.getElementById('nav');
  nav.innerHTML = `<div class="nav-section-label">Research Phases</div>` +
    DATA.guide_phases.map(ph => {
      const pct = phaseCompletionPercent(ph.id);
      return `
        <a class="nav-phase-link ${ph.id===activePhaseId?'active':''}" onclick="route('guide/${ph.id}')">
          <span class="nav-phase-num-circle">${ph.number}</span>
          <span style="flex:1;min-width:0;">
            ${ph.title}
            ${pct > 0 ? `<div style="font-size:10px;color:var(--text-faint);margin-top:2px;">${pct}% complete</div>` : ''}
          </span>
        </a>
      `;
    }).join('');
}

function renderLibraryNav(activeSopId) {
  const nav = document.getElementById('nav');
  nav.innerHTML = DATA.phases.map((phase, i) => `
    <div class="nav-phase">
      <div class="nav-phase-header">
        <span class="nav-phase-num">${String(i+1).padStart(2,'0')}</span>
        <span>${phase.name}</span>
      </div>
      ${phase.sops.map(s => `
        <a class="nav-link ${s.id===activeSopId?'active':''}" onclick="route('sop/${s.id}/procedure')">
          <span class="nav-id">${s.id.replace('UXR-','')}</span>${s.display}
        </a>
      `).join('')}
    </div>
  `).join('');
}

function updateModeToggle(mode) {
  document.getElementById('mode-guide').classList.toggle('active', mode === 'guide');
  document.getElementById('mode-library').classList.toggle('active', mode === 'library');
}

// ---- Routing ----
function route(hash) {
  location.hash = hash;
}
function goHome() {
  location.hash = 'guide';
}

function parseHash() {
  const h = location.hash.replace(/^#/, '');
  if (!h || h === 'guide') return { view: 'guide-home' };
  const [path, anchor] = h.split('#');
  const parts = path.split('/');
  if (parts[0] === 'guide' && parts[1]) {
    return { view: 'phase', phaseId: parts[1], anchor };
  }
  if (parts[0] === 'library') return { view: 'library-home' };
  if (parts[0] === 'sop' && parts[1]) {
    return { view: 'sop', sopId: parts[1], tab: parts[2] || 'procedure', anchor };
  }
  return { view: 'guide-home' };
}

function currentMode(r) {
  if (r.view === 'guide-home' || r.view === 'phase') return 'guide';
  return 'library';
}

function render() {
  const r = parseHash();
  const mode = currentMode(r);
  updateModeToggle(mode);

  if (r.view === 'guide-home') {
    renderGuideNav(null);
    renderGuideHome();
  } else if (r.view === 'phase') {
    renderGuideNav(r.phaseId);
    renderPhase(r.phaseId, r.anchor);
  } else if (r.view === 'library-home') {
    renderLibraryNav(null);
    renderLibraryHome();
  } else if (r.view === 'sop') {
    renderLibraryNav(r.sopId);
    renderSop(r.sopId, r.tab, r.anchor);
  }
  if (!r.anchor) window.scrollTo({top: 0, behavior: 'instant'});
}
window.addEventListener('hashchange', render);

// ---- Checklist persistence (Project Guide phases) ----
const CHECKLIST_STATE_KEY = 'sop-guide-checklist-state';
function loadChecklistState() {
  try { return JSON.parse(localStorage.getItem(CHECKLIST_STATE_KEY) || '{}'); }
  catch { return {}; }
}
function saveChecklistState(state) {
  localStorage.setItem(CHECKLIST_STATE_KEY, JSON.stringify(state));
}
function phaseCompletionPercent(phaseId) {
  const state = loadChecklistState();
  const phase = DATA.guide_phases.find(p => p.id === phaseId);
  if (!phase) return 0;
  const matches = phase.content.match(/^- \[[ x]\]/gm) || [];
  if (!matches.length) return 0;
  const phaseState = state[phaseId] || {};
  const checked = Object.values(phaseState).filter(v => v === true).length;
  return Math.round((checked / matches.length) * 100);
}
function bindPhaseCheckboxes(container, phaseId) {
  const state = loadChecklistState();
  const phaseState = state[phaseId] = state[phaseId] || {};
  container.querySelectorAll('input[type="checkbox"]').forEach((cb, idx) => {
    cb.disabled = false;
    cb.checked = phaseState[idx] === true;
    cb.addEventListener('change', () => {
      phaseState[idx] = cb.checked;
      saveChecklistState(state);
      renderGuideNav(phaseId); // refresh progress in sidebar
    });
  });
}

// ---- Guide home view ----
function renderGuideHome() {
  const t = DATA.totals;
  document.getElementById('main').innerHTML = `
    <div class="home-eyebrow">UX Research Operations · Project Guide</div>
    <h1 class="home-title">Run a research project end to end.</h1>
    <p class="home-lede">
      Five phases from kickoff to close. Each phase shows the work, references the SOPs you'll need,
      and tracks your completion locally — so you can step away and pick up exactly where you left off.
    </p>
    <div class="stat-row">
      <div class="stat"><div class="n">${t.guide_phases}</div><div class="l">Phases</div></div>
      <div class="stat"><div class="n">${t.sops}</div><div class="l">SOPs referenced</div></div>
      <div class="stat"><div class="n">${t.checklists}</div><div class="l">Checklists</div></div>
      <div class="stat"><div class="n">${t.templates}</div><div class="l">Templates</div></div>
    </div>

    ${DATA.guide_phases.map(ph => {
      const pct = phaseCompletionPercent(ph.id);
      return `
        <div class="guide-card" onclick="route('guide/${ph.id}')">
          <div class="guide-card-num">${String(ph.number).padStart(2,'0')}</div>
          <div class="guide-card-body">
            <h2 class="guide-card-title">${ph.title}</h2>
            <p class="guide-card-blurb">${ph.blurb}</p>
            <div class="guide-card-meta">
              <span>${ph.duration}</span>
              <span>·</span>
              <span>${ph.sops.length} SOP${ph.sops.length===1?'':'s'}: ${ph.sops.join(', ')}</span>
              ${pct > 0 ? `<span>·</span><span><strong style="color:var(--accent)">${pct}% complete</strong></span>` : ''}
            </div>
            ${pct > 0 ? `<div class="guide-card-progress"><div class="guide-card-progress-bar" style="width:${pct}%"></div></div>` : ''}
          </div>
          <div class="guide-card-arrow">→</div>
        </div>
      `;
    }).join('')}

    <div style="margin-top:48px; padding-top:24px; border-top:1px solid var(--border); color:var(--text-muted); font-size:13.5px;">
      Looking for the underlying SOPs, checklists, and templates organized by topic?
      <a onclick="route('library')" style="color:var(--accent); cursor:pointer; border-bottom: 1px solid color-mix(in srgb, var(--accent) 35%, transparent);">Switch to the SOP Library →</a>
    </div>
  `;
}

// ---- Phase detail view ----
function renderPhase(phaseId, anchor) {
  const phase = DATA.guide_phases.find(p => p.id === phaseId);
  if (!phase) { goHome(); return; }

  const main = document.getElementById('main');
  main.innerHTML = `
    <div class="breadcrumb">
      <a onclick="route('guide')">Project Guide</a>
      <span class="sep">/</span>
      <span>Phase ${phase.number}</span>
    </div>
    <div class="phase-hero">
      <div class="phase-eyebrow">Phase ${phase.number} of ${DATA.guide_phases.length}</div>
      <h1 class="phase-title-detail">${phase.title}</h1>
      <p style="color:var(--text-muted); font-size:16px; margin: 0;">${phase.blurb}</p>
      <div class="phase-meta-row">
        <span><strong>Duration:</strong> ${phase.duration}</span>
        <span>·</span>
        <span><strong>SOPs:</strong> ${phase.sops.map(s => `<a class="phase-pill" onclick="route('sop/${s}/procedure')" style="margin-left:4px;">${s}</a>`).join('')}</span>
      </div>
    </div>
    <div id="phase-body"><div class="prose">${renderMd(phase.content)}</div></div>
  `;

  const body = document.getElementById('phase-body');
  bindPhaseCheckboxes(body, phaseId);

  if (anchor) {
    const el = document.getElementById(anchor);
    if (el) scrollToElement(el, false);
  }
}

// ---- Library home view ----
function renderLibraryHome() {
  const t = DATA.totals;
  document.getElementById('main').innerHTML = `
    <div class="home-eyebrow">UX Research Operations · SOP Library</div>
    <h1 class="home-title">A working library for industrial UX research.</h1>
    <p class="home-lede">
      Nine SOPs, ${t.checklists} checklists, and ${t.templates} templates covering the full research lifecycle —
      from informed consent through repository curation. Built for B2B teams where research evidence has to survive
      procurement, engineering, and the C-suite.
    </p>
    <div class="stat-row">
      <div class="stat"><div class="n">${t.sops}</div><div class="l">SOPs</div></div>
      <div class="stat"><div class="n">${t.checklists}</div><div class="l">Checklists</div></div>
      <div class="stat"><div class="n">${t.templates}</div><div class="l">Templates</div></div>
      <div class="stat"><div class="n">7</div><div class="l">Lifecycle phases</div></div>
    </div>

    ${DATA.phases.map((phase, i) => `
      <section class="phase-section">
        <div class="phase-head">
          <span class="phase-num">${String(i+1).padStart(2,'0')} / ${String(DATA.phases.length).padStart(2,'0')}</span>
          <h2 class="phase-name">${phase.name}</h2>
        </div>
        <p class="phase-blurb">${phase.blurb}</p>
        <div class="phase-cards">
          ${phase.sops.map(s => `
            <div class="sop-card" onclick="route('sop/${s.id}/procedure')">
              <div class="sop-card-id">${s.id}</div>
              <div class="sop-card-title">${s.display}</div>
              <div class="sop-card-meta">
                <span>${s.read_minutes} min read</span>
                <span>·</span>
                <span>${s.checklist_count} checklists</span>
                <span>·</span>
                <span>${s.template_count} templates</span>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `).join('')}
  `;
}

// ---- SOP detail view ----
function renderSop(sopId, tab, anchor) {
  const sop = SOPS[sopId];
  if (!sop) { goHome(); return; }
  const phase = DATA.phases.find(p => p.sops.some(s => s.id === sopId));
  const phaseRefs = sop.phase_refs || [];

  document.getElementById('main').innerHTML = `
    <div class="breadcrumb">
      <a onclick="route('library')">Library</a>
      <span class="sep">/</span>
      <span>${phase.name}</span>
    </div>
    <div class="sop-title-row">
      <h1 class="sop-title">${sop.display}</h1>
      <span class="sop-id-pill">${sop.id}</span>
    </div>
    <div class="sop-meta-row">
      <span>Owner: UX Research Lead</span>
      <span>·</span>
      <span>${sop.read_minutes} min read</span>
      <span>·</span>
      <span>${sop.checklist_count} checklists</span>
      <span>·</span>
      <span>${sop.template_count} templates</span>
    </div>
    ${phaseRefs.length ? `
      <div class="phase-pills" style="margin-bottom:24px;">
        <span style="font-size:11.5px; color:var(--text-faint); margin-right:4px; align-self:center;">Used in:</span>
        ${phaseRefs.map(p => `<a class="phase-pill" onclick="route('guide/${p.id}')">Phase ${p.number} · ${p.title}</a>`).join('')}
      </div>
    ` : ''}

    <div class="tabs">
      <button class="tab ${tab==='procedure'?'active':''}" onclick="route('sop/${sopId}/procedure')">Procedure</button>
      <button class="tab ${tab==='checklists'?'active':''}" onclick="route('sop/${sopId}/checklists')">Checklists<span class="count">${sop.checklist_count}</span></button>
      <button class="tab ${tab==='templates'?'active':''}" onclick="route('sop/${sopId}/templates')">Templates<span class="count">${sop.template_count}</span></button>
    </div>

    <div class="sop-detail-grid">
      <div id="sop-body"></div>
      <aside class="toc" id="toc"></aside>
    </div>
  `;

  const body = document.getElementById('sop-body');
  const toc = document.getElementById('toc');

  if (tab === 'procedure') {
    const procKey = `${sopId}-procedure`;
    registerDownload(procKey, `${sopId} — ${sop.display}`, sopId, sop.content);
    body.innerHTML = `
      <div class="proc-actions">
        <button class="word-btn" onclick="triggerDownload('${procKey}')">${DOWNLOAD_ICON} Open in Word</button>
      </div>
      <div class="prose">${renderMd(sop.content)}</div>
    `;
    buildToc(body, toc);
  } else if (tab === 'checklists') {
    body.innerHTML = renderAttachments(sop.checklists, 'checklist', sopId);
    toc.innerHTML = renderAttachmentToc(sop.checklists);
    wireAttachments(anchor);
  } else if (tab === 'templates') {
    body.innerHTML = renderAttachments(sop.templates, 'template', sopId);
    toc.innerHTML = renderAttachmentToc(sop.templates);
    wireAttachments(anchor);
  }

  if (anchor && tab === 'procedure') {
    scrollToElement(document.getElementById(anchor), false);
  }
}

function renderAttachments(items, kind, sopId) {
  if (!items.length) return `<p style="color:var(--text-muted)">No ${kind}s available.</p>`;
  const kindLabel = kind.charAt(0).toUpperCase() + kind.slice(1);
  return `<div class="attach-list">${items.map(item => {
    const filename = `${sopId} — ${item.section} ${item.label} ${kindLabel}`;
    const key = `${sopId}-${kind}-${item.section}`;
    registerDownload(key, filename, sopId, item.content);
    return `
    <div class="attach" id="sec-${item.section.replace('.','-')}">
      <button class="attach-head" onclick="this.parentElement.classList.toggle('open')">
        <span class="attach-section">${item.section}</span>
        <span class="attach-title">${item.label}</span>
        <span class="attach-chev">›</span>
      </button>
      <div class="attach-body">
        <div class="prose">${renderMd(item.content)}</div>
        <div class="attach-actions">
          <button class="word-btn" onclick="triggerDownload('${key}')">${DOWNLOAD_ICON} Open in Word</button>
          <span class="attach-hint">Downloads as .doc — save locally and edit in Word.</span>
        </div>
      </div>
    </div>
    `;
  }).join('')}</div>`;
}

function renderAttachmentToc(items) {
  if (!items.length) return '';
  return `<div class="toc-label">In this set</div>` + items.map(i =>
    `<a onclick="scrollToAttach('sec-${i.section.replace('.','-')}')"><span style="font-family:var(--mono);color:var(--text-faint);margin-right:6px">${i.section}</span>${i.label}</a>`
  ).join('');
}

function wireAttachments(anchor) {
  if (anchor) {
    const el = document.getElementById(anchor);
    if (el) { el.classList.add('open'); setTimeout(() => scrollToElement(el, false), 40); }
  }
}

function scrollToAttach(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add('open');
  scrollToElement(el);
}

function scrollToElement(el, smooth = true) {
  if (!el) return;
  const tabs = document.querySelector('.tabs');
  const offset = (tabs ? tabs.getBoundingClientRect().height : 0) + 16;
  const top = el.getBoundingClientRect().top + window.scrollY - offset;
  window.scrollTo({ top, behavior: smooth ? 'smooth' : 'auto' });
}

function jumpToHeading(id) {
  const el = document.getElementById(id);
  if (!el) return;
  scrollToElement(el);
  const path = location.hash.replace(/^#/, '').split('#')[0];
  history.replaceState(null, '', '#' + path + '#' + id);
}

// ---- TOC for procedure ----
function buildToc(body, toc) {
  const headings = body.querySelectorAll('h2, h3');
  if (!headings.length) { toc.innerHTML = ''; return; }
  const items = [];
  headings.forEach((h, idx) => {
    const id = 'h-' + idx + '-' + h.textContent.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0, 40);
    h.id = id;
    items.push({ id, text: h.textContent, level: h.tagName.toLowerCase() });
  });
  toc.innerHTML = `<div class="toc-label">On this page</div>` + items.map(i =>
    `<a onclick="jumpToHeading('${i.id}')" class="${i.level === 'h3' ? 'h3' : ''}" data-target="${i.id}">${i.text}</a>`
  ).join('');

  // Scroll spy
  const links = Array.from(toc.querySelectorAll('a'));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const id = e.target.id;
        links.forEach(l => l.classList.toggle('active', l.dataset.target === id));
      }
    });
  }, { rootMargin: '-15% 0px -70% 0px' });
  headings.forEach(h => observer.observe(h));
}

// ---- Search ----
let searchSelIdx = 0;
let searchResults = [];

function openSearch() {
  document.getElementById('modal-bg').classList.add('open');
  const input = document.getElementById('search-input');
  input.value = '';
  input.focus();
  renderSearchResults('');
}
function closeSearch() {
  document.getElementById('modal-bg').classList.remove('open');
}

function snippet(raw, q) {
  if (!q) return '';
  const lc = raw.toLowerCase();
  const idx = lc.indexOf(q);
  if (idx === -1) return '';
  const start = Math.max(0, idx - 50);
  const end = Math.min(raw.length, idx + q.length + 90);
  const before = raw.slice(start, idx);
  const match = raw.slice(idx, idx + q.length);
  const after = raw.slice(idx + q.length, end);
  return (start > 0 ? '… ' : '') + escapeHtml(before) + '<mark>' + escapeHtml(match) + '</mark>' + escapeHtml(after) + (end < raw.length ? ' …' : '');
}

function escapeHtml(s) {
  return s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

function renderSearchResults(q) {
  q = q.trim().toLowerCase();
  const results = document.getElementById('search-results');
  if (!q) {
    results.innerHTML = `<div class="search-empty">Type to search across SOPs, checklists, and templates.</div>`;
    searchResults = [];
    return;
  }
  const hits = [];
  for (const d of SEARCH_DOCS) {
    let score = 0;
    if (d.title.toLowerCase().includes(q)) score += 10;
    if (d.body.includes(q)) score += 1;
    if (score > 0) hits.push({ doc: d, score });
  }
  hits.sort((a, b) => b.score - a.score);
  searchResults = hits.slice(0, 30);
  if (!searchResults.length) {
    results.innerHTML = `<div class="search-empty">No matches for "${escapeHtml(q)}".</div>`;
    return;
  }
  results.innerHTML = searchResults.map((h, i) => `
    <div class="search-result ${i===searchSelIdx?'sel':''}" data-i="${i}" onclick="goSearch(${i})">
      <div class="search-result-title">${escapeHtml(h.doc.title)}</div>
      <div class="search-result-meta">${h.doc.kind} · ${h.doc.sopId}${h.doc.section ? ' · ' + h.doc.section : ''} · ${h.doc.phase}</div>
      ${snippet(h.doc.raw, q) ? `<div class="search-result-snippet">${snippet(h.doc.raw, q)}</div>` : ''}
    </div>
  `).join('');
}

function goSearch(i) {
  const r = searchResults[i];
  if (!r) return;
  closeSearch();
  location.hash = r.doc.route;
}

document.getElementById('search-input').addEventListener('input', e => {
  searchSelIdx = 0;
  renderSearchResults(e.target.value);
});
document.getElementById('search-input').addEventListener('keydown', e => {
  if (e.key === 'Escape') closeSearch();
  else if (e.key === 'ArrowDown') {
    e.preventDefault();
    searchSelIdx = Math.min(searchResults.length - 1, searchSelIdx + 1);
    renderSearchResults(e.target.value);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    searchSelIdx = Math.max(0, searchSelIdx - 1);
    renderSearchResults(e.target.value);
  } else if (e.key === 'Enter') {
    e.preventDefault();
    goSearch(searchSelIdx);
  }
});

document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openSearch();
  } else if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    openSearch();
  }
});

render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
