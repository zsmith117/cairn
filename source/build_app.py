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
        "recommended_artifact": "UXR-004-template-5.1",  # Research Brief
        "recommended_label": "Draft your Research Brief",
    },
    {
        "id": "phase-2",
        "number": 2,
        "title": "Research Design",
        "blurb": "Methodology, recruitment criteria, and materials development.",
        "duration": "1–3 weeks",
        "sops": ["UXR-003", "UXR-004", "UXR-005"],
        "file": "phase-2-research-design.md",
        "recommended_artifact": "UXR-004-template-5.2",  # Research Plan
        "recommended_label": "Build the Research Plan",
    },
    {
        "id": "phase-3",
        "number": 3,
        "title": "Field Work",
        "blurb": "Recruitment execution, sessions, and live documentation.",
        "duration": "2–4 weeks",
        "sops": ["UXR-001", "UXR-002", "UXR-003", "UXR-006"],
        "file": "phase-3-field-work.md",
        "recommended_artifact": "UXR-003-template-5.4",  # Recruitment Email
        "recommended_label": "Send the Recruitment Outreach",
    },
    {
        "id": "phase-4",
        "number": 4,
        "title": "Analysis",
        "blurb": "Coding, pattern identification, and insight development.",
        "duration": "1–3 weeks",
        "sops": ["UXR-007"],
        "file": "phase-4-analysis.md",
        "recommended_artifact": "UXR-007-template-5.1",  # Analysis Plan
        "recommended_label": "Set up your Analysis Plan",
    },
    {
        "id": "phase-5",
        "number": 5,
        "title": "Delivery & Close",
        "blurb": "Reporting, presentation, and repository archiving.",
        "duration": "1–2 weeks",
        "sops": ["UXR-008", "UXR-009"],
        "file": "phase-5-delivery-close.md",
        "recommended_artifact": "UXR-008-template-5.2",  # Executive Summary
        "recommended_label": "Draft the Executive Summary",
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
                "recommended_artifact": ph.get("recommended_artifact"),
                "recommended_label": ph.get("recommended_label"),
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


# Fillable template forms. Each entry replaces the markdown view of a template
# with an interactive form when the user is inside a project.
TEMPLATE_FORMS = {
    "UXR-004-template-5.1": {
        "title": "Research Brief",
        "intro": "Align the team on what we're learning, why, and how the findings will be used. Created at project kickoff.",
        "sections": [
            {
                "id": "header",
                "title": "Project",
                "fields": [
                    {"name": "project", "label": "Project name", "type": "text", "autofill": "project.name"},
                    {"name": "date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "requester", "label": "Requester", "type": "text", "placeholder": "Who is asking for this research?"},
                    {"name": "researcher", "label": "Researcher", "type": "text", "autofill": "project.owner"},
                ],
            },
            {
                "id": "background",
                "title": "Background",
                "blurb": "What's happening that prompts this research request?",
                "fields": [{"name": "background", "type": "textarea", "rows": 4}],
            },
            {
                "id": "decision",
                "title": "Business decision",
                "blurb": "This research will inform the decision to…",
                "fields": [{"name": "decision", "type": "textarea", "rows": 3}],
            },
            {
                "id": "questions",
                "title": "Key questions",
                "blurb": "Up to three things we need to learn.",
                "fields": [
                    {"name": "question_1", "label": "Question 1", "type": "textarea", "rows": 2},
                    {"name": "question_2", "label": "Question 2", "type": "textarea", "rows": 2},
                    {"name": "question_3", "label": "Question 3", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "assumptions",
                "title": "What we think we know",
                "blurb": "Current assumptions or hypotheses going in.",
                "fields": [
                    {"name": "assumption_1", "label": "Assumption 1", "type": "text"},
                    {"name": "assumption_2", "label": "Assumption 2", "type": "text"},
                    {"name": "assumption_3", "label": "Assumption 3", "type": "text"},
                ],
            },
            {
                "id": "timeline",
                "title": "Timeline",
                "fields": [
                    {"name": "decision_deadline", "label": "Decision needed by", "type": "date"},
                    {"name": "research_completion", "label": "Research completion target", "type": "date"},
                ],
            },
            {
                "id": "constraints",
                "title": "Constraints",
                "fields": [
                    {"name": "budget", "label": "Budget", "type": "text"},
                    {"name": "participant_access", "label": "Participant access", "type": "text"},
                    {"name": "other_constraints", "label": "Other", "type": "text"},
                ],
            },
            {
                "id": "existing_research",
                "title": "Existing research",
                "fields": [
                    {"name": "checked_repo", "label": "Checked repository", "type": "checkbox"},
                    {"name": "relevant_studies", "label": "Relevant studies found", "type": "text"},
                    {"name": "no_prior", "label": "No prior research found", "type": "checkbox"},
                ],
            },
            {
                "id": "assessment",
                "title": "Preliminary assessment",
                "fields": [
                    {"name": "approach", "label": "Recommended approach", "type": "textarea", "rows": 3},
                    {
                        "name": "effort",
                        "label": "Estimated effort",
                        "type": "radio",
                        "options": [
                            {"value": "small", "label": "Small (1–2 weeks)"},
                            {"value": "medium", "label": "Medium (3–5 weeks)"},
                            {"value": "large", "label": "Large (6+ weeks)"},
                        ],
                    },
                ],
            },
            {
                "id": "next_steps",
                "title": "Next steps",
                "fields": [
                    {
                        "name": "next_step",
                        "type": "radio",
                        "options": [
                            {"value": "proceed", "label": "Proceed to full research plan"},
                            {"value": "more_info", "label": "Need more information"},
                            {"value": "defer", "label": "Defer"},
                            {"value": "decline", "label": "Decline"},
                        ],
                    },
                    {"name": "next_step_note", "label": "Notes / reason", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "approval",
                "title": "Approval",
                "fields": [
                    {"name": "approved_by", "label": "Approved by", "type": "text"},
                    {"name": "approval_date", "label": "Approval date", "type": "date"},
                ],
            },
        ],
    },
    "UXR-004-template-5.2": {
        "title": "Research Plan",
        "intro": "Detailed planning artifact — goes deeper than the Research Brief. Covers methodology, timeline, budget, and approvals. Built section by section; export to Word when you're ready to circulate.",
        "sections": [
            {
                "id": "header",
                "title": "Study details",
                "fields": [
                    {"name": "study_name", "label": "Study name", "type": "text", "autofill": "project.name"},
                    {"name": "study_code", "label": "Study code", "type": "text", "placeholder": "e.g. PRJ2026-014"},
                    {"name": "version", "label": "Version", "type": "text", "placeholder": "1.0"},
                    {"name": "date", "label": "Date", "type": "date", "autofill": "today"},
                ],
            },
            {
                "id": "team",
                "title": "Study team",
                "fields": [
                    {"name": "lead_researcher", "label": "Lead researcher", "type": "text", "autofill": "project.owner"},
                    {"name": "supporting_researchers", "label": "Supporting researchers", "type": "text"},
                    {"name": "sponsor", "label": "Research sponsor", "type": "text", "autofill": "project.stakeholder"},
                    {"name": "key_stakeholders", "label": "Key stakeholders", "type": "text"},
                ],
            },
            {
                "id": "background",
                "title": "1. Background and context",
                "blurb": "Why is this research being conducted? What business context drives it?",
                "fields": [
                    {"name": "background", "type": "textarea", "rows": 4},
                    {"name": "prior_research", "label": "Prior research (one study per line)", "type": "textarea", "rows": 3, "placeholder": "Q1 onboarding study, March 2026 — found users abandon at step 3"},
                ],
            },
            {
                "id": "objectives",
                "title": "2. Research objectives",
                "blurb": "This research aims to…",
                "fields": [
                    {"name": "objective_1", "label": "Objective 1", "type": "textarea", "rows": 2},
                    {"name": "objective_2", "label": "Objective 2", "type": "textarea", "rows": 2},
                    {"name": "decision_informed", "label": "…in order to inform the decision to…", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "questions",
                "title": "3. Research questions",
                "fields": [
                    {"name": "rq_primary_1", "label": "Primary question 1 (must answer)", "type": "textarea", "rows": 2},
                    {"name": "rq_primary_2", "label": "Primary question 2", "type": "textarea", "rows": 2},
                    {"name": "rq_primary_3", "label": "Primary question 3", "type": "textarea", "rows": 2},
                    {"name": "rq_secondary_1", "label": "Secondary question 1 (important)", "type": "textarea", "rows": 2},
                    {"name": "rq_secondary_2", "label": "Secondary question 2", "type": "textarea", "rows": 2},
                    {"name": "rq_exploratory", "label": "Exploratory question (if time permits)", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "hypotheses",
                "title": "4. Hypotheses (if applicable)",
                "fields": [
                    {"name": "h1", "label": "H1", "type": "textarea", "rows": 2},
                    {"name": "h2", "label": "H2", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "method",
                "title": "5. Methodology",
                "fields": [
                    {"name": "method", "label": "Method", "type": "text", "placeholder": "e.g. semi-structured interviews"},
                    {"name": "method_rationale", "label": "Rationale", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "participants",
                "title": "Participant requirements",
                "fields": [
                    {"name": "target_population", "label": "Target population", "type": "textarea", "rows": 2},
                    {"name": "criteria_must_have", "label": "Must have", "type": "textarea", "rows": 2},
                    {"name": "criteria_nice_to_have", "label": "Nice to have", "type": "textarea", "rows": 2},
                    {"name": "criteria_quotas", "label": "Quotas", "type": "textarea", "rows": 2},
                    {"name": "criteria_exclusions", "label": "Exclusions", "type": "textarea", "rows": 2},
                    {"name": "sample_size", "label": "Sample size", "type": "text", "placeholder": "e.g. 8–10"},
                    {"name": "sample_rationale", "label": "Sample size rationale", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "sessions",
                "title": "Session details",
                "fields": [
                    {
                        "name": "session_format",
                        "label": "Format",
                        "type": "radio",
                        "options": [
                            {"value": "remote", "label": "Remote"},
                            {"value": "in_person", "label": "In-person"},
                            {"value": "field", "label": "Field visit"},
                        ],
                    },
                    {"name": "session_duration", "label": "Duration (minutes)", "type": "text", "placeholder": "60"},
                    {"name": "rec_audio", "label": "Recording: Audio", "type": "checkbox"},
                    {"name": "rec_video", "label": "Recording: Video", "type": "checkbox"},
                    {"name": "rec_screen", "label": "Recording: Screen", "type": "checkbox"},
                    {"name": "tools", "label": "Tools (Zoom, Otter, Figma, etc.)", "type": "text"},
                ],
            },
            {
                "id": "timeline",
                "title": "6. Timeline",
                "blurb": "Target dates for each milestone.",
                "fields": [
                    {"name": "tl_plan_approved", "label": "Plan approved", "type": "date"},
                    {"name": "tl_recruit_begin", "label": "Recruitment begins", "type": "date"},
                    {"name": "tl_recruit_done", "label": "Recruitment complete", "type": "date"},
                    {"name": "tl_sessions_begin", "label": "Sessions begin", "type": "date"},
                    {"name": "tl_sessions_done", "label": "Sessions complete", "type": "date"},
                    {"name": "tl_analysis_done", "label": "Analysis complete", "type": "date"},
                    {"name": "tl_findings_delivered", "label": "Findings delivered", "type": "date"},
                ],
            },
            {
                "id": "deliverables",
                "title": "7. Deliverables",
                "blurb": "One deliverable per line: format · audience · date.",
                "fields": [
                    {"name": "deliverables", "type": "textarea", "rows": 4, "placeholder": "Top-line readout · slide deck · exec team · 2026-06-15\nFull report · doc · all-hands · 2026-06-22"},
                ],
            },
            {
                "id": "budget",
                "title": "8. Resources and budget",
                "fields": [
                    {"name": "budget_incentives", "label": "Incentives", "type": "text"},
                    {"name": "budget_recruitment", "label": "Recruitment", "type": "text"},
                    {"name": "budget_tools", "label": "Tools", "type": "text"},
                    {"name": "budget_travel", "label": "Travel", "type": "text"},
                    {"name": "budget_total", "label": "Total", "type": "text"},
                ],
            },
            {
                "id": "risks",
                "title": "9. Risks and mitigations",
                "blurb": "One risk per line: risk · probability · impact · mitigation.",
                "fields": [
                    {"name": "risks", "type": "textarea", "rows": 4, "placeholder": "Low recruitment yield · medium · high · prepay vendor and over-screen by 30%"},
                ],
            },
            {
                "id": "comms",
                "title": "10. Communication plan",
                "fields": [
                    {"name": "status_updates", "label": "Status updates", "type": "text", "placeholder": "Weekly Slack on Mondays"},
                    {"name": "check_ins", "label": "Stakeholder check-ins", "type": "text"},
                    {"name": "escalation", "label": "Issue escalation", "type": "text"},
                ],
            },
            {
                "id": "ethics",
                "title": "11. Ethical considerations",
                "fields": [
                    {"name": "consent_approach", "label": "Consent approach", "type": "textarea", "rows": 2},
                    {"name": "data_handling", "label": "Data handling", "type": "textarea", "rows": 2},
                    {"name": "participant_considerations", "label": "Participant considerations", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "approvals",
                "title": "Approvals",
                "fields": [
                    {"name": "approval_lead_name", "label": "Research lead — name", "type": "text"},
                    {"name": "approval_lead_date", "label": "Date", "type": "date"},
                    {"name": "approval_sponsor_name", "label": "Research sponsor — name", "type": "text"},
                    {"name": "approval_sponsor_date", "label": "Date", "type": "date"},
                    {"name": "approval_other_name", "label": "Other (if required) — name", "type": "text"},
                    {"name": "approval_other_date", "label": "Date", "type": "date"},
                ],
            },
        ],
    },
    "UXR-006-template-5.1": {
        "title": "Interview Session Notes",
        "multi_instance": True,
        "instance_singular": "session",
        "instance_plural": "sessions",
        "intro": "One entry per interview. Add a session, fill in notes, then add another when the next interview is done. Each session exports to its own Word doc.",
        "sections": [
            {
                "id": "header",
                "title": "Session header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "session_number", "label": "Session #", "type": "text", "placeholder": "S03"},
                    {"name": "participant_id", "label": "Participant ID (code, not real name)", "type": "text", "placeholder": "P03"},
                    {"name": "session_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "start_time", "label": "Start time", "type": "text", "placeholder": "10:00"},
                    {"name": "end_time", "label": "End time", "type": "text", "placeholder": "10:55"},
                    {"name": "duration", "label": "Actual duration", "type": "text", "placeholder": "55 min"},
                    {"name": "location", "label": "Location", "type": "text", "placeholder": "Remote via Zoom"},
                    {"name": "moderator", "label": "Moderator", "type": "text", "autofill": "project.owner"},
                    {"name": "notetaker", "label": "Notetaker", "type": "text"},
                    {"name": "observers", "label": "Other observers", "type": "text"},
                ],
            },
            {
                "id": "context",
                "title": "Participant context",
                "blurb": "Relevant background from the screener that shapes how you interpret what they say.",
                "fields": [
                    {"name": "p_role", "label": "Role", "type": "text"},
                    {"name": "p_experience", "label": "Experience level", "type": "text"},
                    {"name": "p_characteristics", "label": "Key characteristics relevant to this study", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "research_questions",
                "title": "Research questions this session should help answer",
                "fields": [
                    {"name": "rq_1", "label": "Question 1", "type": "textarea", "rows": 2},
                    {"name": "rq_2", "label": "Question 2", "type": "textarea", "rows": 2},
                    {"name": "rq_3", "label": "Question 3", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "warmup_notes",
                "title": "Warm-up notes",
                "fields": [
                    {"name": "warmup_notes", "type": "textarea", "rows": 3, "placeholder": "Quick context-setting; rapport notes."},
                ],
            },
            {
                "id": "topic1_notes",
                "title": "Topic area 1",
                "fields": [
                    {"name": "t1_name", "label": "Topic name", "type": "text"},
                    {"name": "t1_notes", "label": "Notes (questions, responses, observations)", "type": "textarea", "rows": 8},
                    {"name": "t1_key_moment", "label": "Key moment (with timestamp if recording)", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "topic2_notes",
                "title": "Topic area 2",
                "fields": [
                    {"name": "t2_name", "label": "Topic name", "type": "text"},
                    {"name": "t2_notes", "label": "Notes", "type": "textarea", "rows": 8},
                    {"name": "t2_key_moment", "label": "Key moment", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "closing_notes",
                "title": "Closing notes",
                "fields": [
                    {"name": "closing_notes", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "quotes",
                "title": "Key quotes",
                "blurb": "Verbatim quotes worth surfacing later in analysis or the readout.",
                "fields": [
                    {"name": "quote_1", "label": "Quote 1", "type": "textarea", "rows": 2},
                    {"name": "quote_1_context", "label": "Context", "type": "text"},
                    {"name": "quote_2", "label": "Quote 2", "type": "textarea", "rows": 2},
                    {"name": "quote_2_context", "label": "Context", "type": "text"},
                    {"name": "quote_3", "label": "Quote 3", "type": "textarea", "rows": 2},
                    {"name": "quote_3_context", "label": "Context", "type": "text"},
                ],
            },
            {
                "id": "reflections",
                "title": "Observer notes & reflections",
                "fields": [
                    {"name": "patterns", "label": "Patterns observed (how this connects to other sessions)", "type": "textarea", "rows": 3},
                    {"name": "surprises", "label": "Surprises (unexpected findings)", "type": "textarea", "rows": 3},
                    {"name": "questions_raised", "label": "Questions raised for future sessions", "type": "textarea", "rows": 3},
                    {"name": "method_notes", "label": "Methodological notes (guide issues, timing, technical)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "post_session",
                "title": "Post-session tasks",
                "fields": [
                    {"name": "ps_recording", "label": "Recording saved and backed up", "type": "checkbox"},
                    {"name": "ps_summary", "label": "Session summary completed", "type": "checkbox"},
                    {"name": "ps_notes_clean", "label": "Notes cleaned up and readable", "type": "checkbox"},
                    {"name": "ps_shared", "label": "Key insights shared with team", "type": "checkbox"},
                    {"name": "ps_followups", "label": "Follow-up questions documented", "type": "checkbox"},
                    {"name": "ps_filed", "label": "Files properly named and stored", "type": "checkbox"},
                ],
            },
        ],
    },
    "UXR-006-template-5.2": {
        "title": "Usability Test Observation Notes",
        "multi_instance": True,
        "instance_singular": "session",
        "instance_plural": "sessions",
        "intro": "One entry per usability session. Up to three tasks per session — combine into the issues log at the bottom and export to Word.",
        "sections": [
            {
                "id": "header",
                "title": "Session header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "session_number", "label": "Session #", "type": "text", "placeholder": "S03"},
                    {"name": "participant_id", "label": "Participant ID", "type": "text", "placeholder": "P03"},
                    {"name": "session_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "product", "label": "Product / prototype", "type": "text"},
                    {
                        "name": "device",
                        "label": "Device",
                        "type": "radio",
                        "options": [
                            {"value": "desktop", "label": "Desktop"},
                            {"value": "mobile", "label": "Mobile"},
                            {"value": "tablet", "label": "Tablet"},
                        ],
                    },
                    {"name": "moderator", "label": "Moderator", "type": "text", "autofill": "project.owner"},
                    {"name": "observer", "label": "Observer", "type": "text"},
                ],
            },
            {
                "id": "context",
                "title": "Participant context",
                "fields": [
                    {"name": "p_experience", "label": "Experience level with this product type", "type": "text"},
                    {"name": "p_tools", "label": "Current tools used", "type": "text"},
                    {"name": "p_background", "label": "Relevant background", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "pre_task",
                "title": "Pre-task questions",
                "fields": [
                    {"name": "pre_task_notes", "label": "Context-setting Q&A", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "task1",
                "title": "Task 1",
                "fields": [
                    {"name": "t1_name", "label": "Task name", "type": "text"},
                    {"name": "t1_duration", "label": "Duration", "type": "text", "placeholder": "4:30"},
                    {"name": "t1_scenario", "label": "Scenario (read to participant)", "type": "textarea", "rows": 2},
                    {"name": "t1_success_criteria", "label": "Success criteria (one per line)", "type": "textarea", "rows": 3},
                    {"name": "t1_path", "label": "Path taken (steps + result)", "type": "textarea", "rows": 4},
                    {"name": "t1_behaviors", "label": "Behaviors & verbalizations (timestamps welcome)", "type": "textarea", "rows": 4},
                    {"name": "t1_errors", "label": "Errors / usability issues", "type": "textarea", "rows": 3},
                    {
                        "name": "t1_outcome",
                        "label": "Outcome",
                        "type": "radio",
                        "options": [
                            {"value": "success", "label": "Success — without assistance"},
                            {"value": "success_difficulty", "label": "Success with difficulty"},
                            {"value": "partial", "label": "Partial success"},
                            {"value": "failure", "label": "Failure"},
                        ],
                    },
                    {
                        "name": "t1_ease",
                        "label": "Ease rating (1 = very easy, 5 = very difficult)",
                        "type": "radio",
                        "options": [
                            {"value": "1", "label": "1"},
                            {"value": "2", "label": "2"},
                            {"value": "3", "label": "3"},
                            {"value": "4", "label": "4"},
                            {"value": "5", "label": "5"},
                        ],
                    },
                    {"name": "t1_post", "label": "Post-task notes (what made it easy / hard, observed behavior)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "task2",
                "title": "Task 2",
                "fields": [
                    {"name": "t2_name", "label": "Task name", "type": "text"},
                    {"name": "t2_duration", "label": "Duration", "type": "text"},
                    {"name": "t2_scenario", "label": "Scenario", "type": "textarea", "rows": 2},
                    {"name": "t2_success_criteria", "label": "Success criteria", "type": "textarea", "rows": 3},
                    {"name": "t2_path", "label": "Path taken", "type": "textarea", "rows": 4},
                    {"name": "t2_behaviors", "label": "Behaviors & verbalizations", "type": "textarea", "rows": 4},
                    {"name": "t2_errors", "label": "Errors / issues", "type": "textarea", "rows": 3},
                    {
                        "name": "t2_outcome",
                        "label": "Outcome",
                        "type": "radio",
                        "options": [
                            {"value": "success", "label": "Success"},
                            {"value": "success_difficulty", "label": "Success with difficulty"},
                            {"value": "partial", "label": "Partial"},
                            {"value": "failure", "label": "Failure"},
                        ],
                    },
                    {
                        "name": "t2_ease",
                        "label": "Ease rating (1–5)",
                        "type": "radio",
                        "options": [
                            {"value": "1", "label": "1"},
                            {"value": "2", "label": "2"},
                            {"value": "3", "label": "3"},
                            {"value": "4", "label": "4"},
                            {"value": "5", "label": "5"},
                        ],
                    },
                    {"name": "t2_post", "label": "Post-task notes", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "task3",
                "title": "Task 3",
                "fields": [
                    {"name": "t3_name", "label": "Task name", "type": "text"},
                    {"name": "t3_duration", "label": "Duration", "type": "text"},
                    {"name": "t3_scenario", "label": "Scenario", "type": "textarea", "rows": 2},
                    {"name": "t3_success_criteria", "label": "Success criteria", "type": "textarea", "rows": 3},
                    {"name": "t3_path", "label": "Path taken", "type": "textarea", "rows": 4},
                    {"name": "t3_behaviors", "label": "Behaviors & verbalizations", "type": "textarea", "rows": 4},
                    {"name": "t3_errors", "label": "Errors / issues", "type": "textarea", "rows": 3},
                    {
                        "name": "t3_outcome",
                        "label": "Outcome",
                        "type": "radio",
                        "options": [
                            {"value": "success", "label": "Success"},
                            {"value": "success_difficulty", "label": "Success with difficulty"},
                            {"value": "partial", "label": "Partial"},
                            {"value": "failure", "label": "Failure"},
                        ],
                    },
                    {
                        "name": "t3_ease",
                        "label": "Ease rating (1–5)",
                        "type": "radio",
                        "options": [
                            {"value": "1", "label": "1"},
                            {"value": "2", "label": "2"},
                            {"value": "3", "label": "3"},
                            {"value": "4", "label": "4"},
                            {"value": "5", "label": "5"},
                        ],
                    },
                    {"name": "t3_post", "label": "Post-task notes", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "more_tasks",
                "title": "Additional tasks (if any)",
                "blurb": "Use this for any tasks 4+. Mirror the structure above.",
                "fields": [
                    {"name": "extra_tasks", "type": "textarea", "rows": 6},
                ],
            },
            {
                "id": "debrief",
                "title": "Debrief",
                "fields": [
                    {"name": "d_overall", "label": "Overall impression", "type": "textarea", "rows": 3},
                    {"name": "d_worked_well", "label": "What worked well", "type": "textarea", "rows": 3},
                    {"name": "d_frustrating", "label": "What was frustrating", "type": "textarea", "rows": 3},
                    {"name": "d_comparison", "label": "How does this compare to [current tool]?", "type": "textarea", "rows": 3},
                    {
                        "name": "d_would_use",
                        "label": "Would you use this?",
                        "type": "radio",
                        "options": [
                            {"value": "definitely", "label": "Definitely"},
                            {"value": "probably", "label": "Probably"},
                            {"value": "maybe", "label": "Maybe"},
                            {"value": "probably_not", "label": "Probably not"},
                            {"value": "definitely_not", "label": "Definitely not"},
                        ],
                    },
                    {"name": "d_why", "label": "Why", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "issues_log",
                "title": "Usability issues log",
                "blurb": "One issue per line: # · task · severity (Critical/Serious/Minor) · description · screen · timestamp",
                "fields": [
                    {"name": "issues", "type": "textarea", "rows": 6, "placeholder": "1 · Task 1 · Critical · Couldn't find primary CTA after step 3 · Configurator results · 04:12"},
                ],
            },
            {
                "id": "insights",
                "title": "Observer insights",
                "fields": [
                    {"name": "patterns", "label": "Patterns (how this session compares to others)", "type": "textarea", "rows": 3},
                    {"name": "key_findings", "label": "Key findings (one per line)", "type": "textarea", "rows": 4},
                    {"name": "recommendations", "label": "Recommendations (one per line)", "type": "textarea", "rows": 4},
                ],
            },
        ],
    },
    "UXR-009-template-5.1": {
        "title": "Study Summary",
        "intro": "One per study. The canonical short-form record of what the research was, what it found, and what came of it. Lives in the repository as the entry's overview.",
        "sections": [
            {
                "id": "header",
                "title": "Study identification",
                "fields": [
                    {"name": "study_id", "label": "Study ID", "type": "text", "placeholder": "UXR-2026-Q2-014"},
                    {"name": "study_title", "label": "Study title", "type": "text", "autofill": "project.name"},
                    {"name": "short_title", "label": "Short title (for lists)", "type": "text"},
                    {"name": "study_date", "label": "Date / range", "type": "text", "placeholder": "April–May 2026"},
                    {
                        "name": "status",
                        "label": "Status",
                        "type": "radio",
                        "options": [
                            {"value": "completed", "label": "Completed"},
                            {"value": "published", "label": "Published"},
                            {"value": "archived", "label": "Archived"},
                        ],
                    },
                ],
            },
            {
                "id": "team",
                "title": "Study team",
                "fields": [
                    {"name": "research_lead", "label": "Research lead", "type": "text", "autofill": "project.owner"},
                    {"name": "team_members", "label": "Team members", "type": "text"},
                    {"name": "stakeholders", "label": "Key stakeholders", "type": "text", "autofill": "project.stakeholder"},
                ],
            },
            {
                "id": "overview",
                "title": "Research overview",
                "fields": [
                    {"name": "purpose", "label": "Purpose (2–3 sentences)", "type": "textarea", "rows": 3},
                    {"name": "rq_primary", "label": "Primary research question", "type": "textarea", "rows": 2},
                    {"name": "rq_secondary", "label": "Secondary question", "type": "textarea", "rows": 2},
                    {"name": "rq_additional", "label": "Additional questions", "type": "textarea", "rows": 2},
                    {"name": "method", "label": "Method", "type": "text"},
                    {"name": "participants", "label": "Participants (count + description)", "type": "text"},
                    {"name": "duration", "label": "Duration", "type": "text", "placeholder": "12 sessions over 4 weeks"},
                ],
            },
            {
                "id": "findings",
                "title": "Key findings",
                "blurb": "Per finding: one-sentence headline + 1–2 sentences of supporting evidence.",
                "fields": [
                    {"name": "finding_1", "label": "Finding 1", "type": "textarea", "rows": 3},
                    {"name": "finding_2", "label": "Finding 2", "type": "textarea", "rows": 3},
                    {"name": "finding_3", "label": "Finding 3", "type": "textarea", "rows": 3},
                    {"name": "finding_4", "label": "Finding 4 (optional)", "type": "textarea", "rows": 3},
                    {"name": "finding_5", "label": "Finding 5 (optional)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "recommendations",
                "title": "Top recommendations",
                "fields": [
                    {"name": "rec_1", "label": "Recommendation 1 + priority + rationale", "type": "textarea", "rows": 3},
                    {"name": "rec_2", "label": "Recommendation 2", "type": "textarea", "rows": 3},
                    {"name": "rec_3", "label": "Recommendation 3", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "impact",
                "title": "Impact",
                "fields": [
                    {"name": "decisions", "label": "Decisions influenced (one per line)", "type": "textarea", "rows": 4},
                    {"name": "outcomes", "label": "Measurable outcomes (if available)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "artifacts",
                "title": "Artifacts & materials",
                "fields": [
                    {"name": "report_link", "label": "Research report", "type": "text"},
                    {"name": "deck_link", "label": "Presentation", "type": "text"},
                    {"name": "highlight_link", "label": "Highlight one-pager", "type": "text"},
                    {"name": "journey_link", "label": "Journey map (if applicable)", "type": "text"},
                    {"name": "other_artifacts", "label": "Other artifacts", "type": "textarea", "rows": 2},
                    {"name": "notes_location", "label": "Session notes (restricted)", "type": "text"},
                    {"name": "transcripts_location", "label": "Transcripts (restricted)", "type": "text"},
                    {"name": "recordings_location", "label": "Recordings (restricted)", "type": "text"},
                ],
            },
            {
                "id": "metadata",
                "title": "Metadata",
                "fields": [
                    {"name": "product_area", "label": "Product area", "type": "text"},
                    {"name": "feature", "label": "Specific feature", "type": "text"},
                    {"name": "user_segment", "label": "User segment", "type": "text"},
                    {"name": "topics", "label": "Topics / themes (one per line)", "type": "textarea", "rows": 3},
                    {
                        "name": "research_type",
                        "label": "Research type",
                        "type": "radio",
                        "options": [
                            {"value": "generative", "label": "Generative"},
                            {"value": "evaluative", "label": "Evaluative"},
                            {"value": "formative", "label": "Formative"},
                            {"value": "summative", "label": "Summative"},
                        ],
                    },
                    {"name": "related_studies", "label": "Related studies (prior research + follow-ups)", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
    "UXR-009-template-5.2": {
        "title": "Repository Entry Metadata",
        "intro": "Long-form metadata record for the repository. More detailed than the Study Summary — includes tagging, relationships to other studies, and access controls.",
        "sections": [
            {
                "id": "identification",
                "title": "Study identification",
                "fields": [
                    {"name": "study_id", "label": "Study ID", "type": "text", "placeholder": "UXR-2026-Q2-014"},
                    {"name": "study_name", "label": "Study name", "type": "text", "autofill": "project.name"},
                    {"name": "short_name", "label": "Short name (max 50 chars)", "type": "text"},
                    {"name": "alternate_names", "label": "Alternate names / nicknames", "type": "text"},
                ],
            },
            {
                "id": "dates",
                "title": "Dates",
                "fields": [
                    {"name": "start_date", "label": "Start date", "type": "date"},
                    {"name": "end_date", "label": "End date", "type": "date"},
                    {"name": "quarter", "label": "Quarter", "type": "text", "placeholder": "Q2 2026"},
                    {"name": "year", "label": "Year", "type": "text"},
                    {"name": "duration", "label": "Duration", "type": "text", "placeholder": "4 weeks"},
                ],
            },
            {
                "id": "people",
                "title": "People",
                "fields": [
                    {"name": "research_lead", "label": "Research lead", "type": "text", "autofill": "project.owner"},
                    {"name": "research_lead_email", "label": "Lead email", "type": "text"},
                    {"name": "supporting", "label": "Supporting researchers", "type": "text"},
                    {"name": "primary_stakeholder", "label": "Primary stakeholder", "type": "text", "autofill": "project.stakeholder"},
                    {"name": "primary_stakeholder_title", "label": "Stakeholder title", "type": "text"},
                    {"name": "other_stakeholders", "label": "Other stakeholders", "type": "text"},
                ],
            },
            {
                "id": "classification",
                "title": "Classification",
                "fields": [
                    {
                        "name": "method",
                        "label": "Method",
                        "type": "radio",
                        "options": [
                            {"value": "interview", "label": "Interview"},
                            {"value": "usability", "label": "Usability testing"},
                            {"value": "field", "label": "Field research"},
                            {"value": "focus_group", "label": "Focus group"},
                            {"value": "survey", "label": "Survey"},
                            {"value": "diary", "label": "Diary study"},
                            {"value": "card_sort", "label": "Card sorting"},
                            {"value": "tree_test", "label": "Tree testing"},
                            {"value": "concept_test", "label": "Concept testing"},
                            {"value": "other", "label": "Other"},
                        ],
                    },
                    {
                        "name": "research_type",
                        "label": "Research type",
                        "type": "radio",
                        "options": [
                            {"value": "generative", "label": "Generative"},
                            {"value": "evaluative", "label": "Evaluative"},
                            {"value": "formative", "label": "Formative"},
                            {"value": "summative", "label": "Summative"},
                        ],
                    },
                    {"name": "product_area", "label": "Product area", "type": "text"},
                    {"name": "feature", "label": "Feature (specific)", "type": "text"},
                    {"name": "user_segment", "label": "User segment", "type": "text"},
                ],
            },
            {
                "id": "overview",
                "title": "Research overview",
                "fields": [
                    {"name": "purpose", "label": "Purpose (2–3 sentences)", "type": "textarea", "rows": 3},
                    {"name": "rq_primary", "label": "Primary research question", "type": "textarea", "rows": 2},
                    {"name": "rq_secondary", "label": "Secondary question", "type": "textarea", "rows": 2},
                    {"name": "rq_additional", "label": "Additional question", "type": "textarea", "rows": 2},
                    {"name": "sample_size", "label": "Sample size", "type": "text"},
                    {"name": "participant_types", "label": "Participant types", "type": "text"},
                    {"name": "recruitment", "label": "Recruitment method", "type": "text"},
                    {"name": "segments_breakdown", "label": "Segments breakdown", "type": "text"},
                ],
            },
            {
                "id": "findings_summary",
                "title": "Key findings (one-line each)",
                "fields": [
                    {"name": "finding_1", "label": "Finding 1", "type": "text"},
                    {"name": "finding_2", "label": "Finding 2", "type": "text"},
                    {"name": "finding_3", "label": "Finding 3", "type": "text"},
                    {"name": "finding_4", "label": "Finding 4 (optional)", "type": "text"},
                    {"name": "finding_5", "label": "Finding 5 (optional)", "type": "text"},
                ],
            },
            {
                "id": "rec_summary",
                "title": "Top recommendations (one-line each)",
                "fields": [
                    {"name": "rec_1", "label": "Rec 1 (with priority)", "type": "text"},
                    {"name": "rec_2", "label": "Rec 2", "type": "text"},
                    {"name": "rec_3", "label": "Rec 3", "type": "text"},
                ],
            },
            {
                "id": "tags_topics",
                "title": "Topics / themes",
                "blurb": "Multi-select all that apply.",
                "fields": [
                    {"name": "topic_onboarding", "label": "Onboarding", "type": "checkbox"},
                    {"name": "topic_navigation", "label": "Navigation", "type": "checkbox"},
                    {"name": "topic_search", "label": "Search", "type": "checkbox"},
                    {"name": "topic_reporting", "label": "Reporting", "type": "checkbox"},
                    {"name": "topic_collaboration", "label": "Collaboration", "type": "checkbox"},
                    {"name": "topic_integration", "label": "Integration", "type": "checkbox"},
                    {"name": "topic_mobile", "label": "Mobile experience", "type": "checkbox"},
                    {"name": "topic_accessibility", "label": "Accessibility", "type": "checkbox"},
                    {"name": "topic_performance", "label": "Performance", "type": "checkbox"},
                    {"name": "topic_other", "label": "Other (specify below)", "type": "checkbox"},
                    {"name": "topic_other_text", "label": "Other topics", "type": "text"},
                ],
            },
            {
                "id": "tags_needs",
                "title": "User needs identified",
                "fields": [
                    {"name": "need_efficiency", "label": "Efficiency", "type": "checkbox"},
                    {"name": "need_control", "label": "Control", "type": "checkbox"},
                    {"name": "need_flexibility", "label": "Flexibility", "type": "checkbox"},
                    {"name": "need_visibility", "label": "Visibility", "type": "checkbox"},
                    {"name": "need_confidence", "label": "Confidence", "type": "checkbox"},
                    {"name": "need_support", "label": "Support", "type": "checkbox"},
                    {"name": "need_automation", "label": "Automation", "type": "checkbox"},
                    {"name": "need_customization", "label": "Customization", "type": "checkbox"},
                    {"name": "need_simplicity", "label": "Simplicity", "type": "checkbox"},
                    {"name": "need_other", "label": "Other (specify below)", "type": "checkbox"},
                    {"name": "need_other_text", "label": "Other needs", "type": "text"},
                ],
            },
            {
                "id": "artifacts_files",
                "title": "Artifacts & files",
                "fields": [
                    {"name": "summary_link", "label": "Study summary", "type": "text"},
                    {"name": "report_link", "label": "Research report", "type": "text"},
                    {"name": "deck_link", "label": "Presentation", "type": "text"},
                    {"name": "highlight_link", "label": "Highlight one-pager", "type": "text"},
                    {"name": "journey_link", "label": "Journey map", "type": "text"},
                    {"name": "personas_link", "label": "Personas", "type": "text"},
                    {"name": "framework_link", "label": "Framework / model", "type": "text"},
                    {"name": "other_artifacts", "label": "Other artifacts (links)", "type": "textarea", "rows": 2},
                    {"name": "notes_folder", "label": "Session notes folder (restricted)", "type": "text"},
                    {"name": "transcripts_folder", "label": "Transcripts folder (restricted)", "type": "text"},
                    {"name": "recordings_folder", "label": "Recordings folder (restricted)", "type": "text"},
                    {"name": "plan_link", "label": "Research plan", "type": "text"},
                ],
            },
            {
                "id": "impact",
                "title": "Impact",
                "fields": [
                    {"name": "decisions_influenced", "label": "Decisions influenced", "type": "textarea", "rows": 4},
                    {"name": "actions_taken", "label": "Actions taken (with status)", "type": "textarea", "rows": 4},
                    {"name": "metrics_changed", "label": "Metrics changed (before → after)", "type": "textarea", "rows": 3},
                    {"name": "impact_assessment_link", "label": "Impact assessment link", "type": "text"},
                ],
            },
            {
                "id": "relationships",
                "title": "Relationships",
                "fields": [
                    {"name": "prior_research", "label": "Prior research (built on)", "type": "textarea", "rows": 2},
                    {"name": "followup_research", "label": "Follow-up research (this led to)", "type": "textarea", "rows": 2},
                    {"name": "related_studies", "label": "Related studies (connected)", "type": "textarea", "rows": 2},
                    {"name": "initiative", "label": "Part of initiative", "type": "text"},
                    {"name": "synthesis_link", "label": "Included in synthesis (link)", "type": "text"},
                ],
            },
            {
                "id": "access",
                "title": "Status & access",
                "fields": [
                    {
                        "name": "entry_status",
                        "label": "Entry status",
                        "type": "radio",
                        "options": [
                            {"value": "draft", "label": "Draft"},
                            {"value": "in_review", "label": "In review"},
                            {"value": "published", "label": "Published"},
                            {"value": "archived", "label": "Archived"},
                        ],
                    },
                    {"name": "publication_date", "label": "Publication date", "type": "date"},
                    {"name": "last_updated", "label": "Last updated", "type": "date", "autofill": "today"},
                    {
                        "name": "visibility",
                        "label": "Visibility",
                        "type": "radio",
                        "options": [
                            {"value": "public", "label": "Public (all)"},
                            {"value": "restricted", "label": "Restricted (team only)"},
                            {"value": "private", "label": "Private (lead only)"},
                        ],
                    },
                    {"name": "access_notes", "label": "Access notes", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "notes",
                "title": "Internal notes",
                "fields": [
                    {"name": "internal_notes", "type": "textarea", "rows": 4},
                ],
            },
        ],
    },
    "UXR-009-template-5.3": {
        "title": "Research Portfolio View",
        "multi_instance": True,
        "instance_singular": "period",
        "instance_plural": "periods",
        "intro": "One entry per reporting period (typically quarterly or annual). Snapshots the whole portfolio: methods, product areas, gaps, themes, and what's planned next.",
        "sections": [
            {
                "id": "header",
                "title": "Period header",
                "fields": [
                    {"name": "period", "label": "Period", "type": "text", "placeholder": "2026 Q1–Q2"},
                    {"name": "generated_date", "label": "Generated", "type": "date", "autofill": "today"},
                    {"name": "compiler", "label": "Compiled by", "type": "text", "autofill": "project.owner"},
                ],
            },
            {
                "id": "summary",
                "title": "Portfolio summary",
                "fields": [
                    {"name": "total_studies", "label": "Total studies completed", "type": "text"},
                    {"name": "q1_count", "label": "Q1 count", "type": "text"},
                    {"name": "q2_count", "label": "Q2 count", "type": "text"},
                    {"name": "q3_count", "label": "Q3 count", "type": "text"},
                    {"name": "q4_count", "label": "Q4 count", "type": "text"},
                    {"name": "researchers_count", "label": "Researchers on team", "type": "text"},
                    {"name": "studies_per_researcher", "label": "Studies per researcher (avg)", "type": "text"},
                ],
            },
            {
                "id": "by_method",
                "title": "Research by method",
                "blurb": "One per line: method · count · % of total.",
                "fields": [
                    {"name": "by_method", "type": "textarea", "rows": 6, "placeholder": "Interview · 18 · 45%\nUsability testing · 12 · 30%\nField research · 6 · 15%\nOther · 4 · 10%"},
                ],
            },
            {
                "id": "by_product_area",
                "title": "Research by product area",
                "blurb": "One per line: product area · count · % of total.",
                "fields": [
                    {"name": "by_product_area", "type": "textarea", "rows": 6},
                ],
            },
            {
                "id": "by_type",
                "title": "Research by type",
                "fields": [
                    {"name": "generative_count", "label": "Generative (discovery)", "type": "text"},
                    {"name": "generative_pct", "label": "% of total", "type": "text"},
                    {"name": "evaluative_count", "label": "Evaluative (assessment)", "type": "text"},
                    {"name": "evaluative_pct", "label": "% of total", "type": "text"},
                ],
            },
            {
                "id": "top_topics",
                "title": "Top topics researched",
                "blurb": "One per line: topic · # studies · most recent study + date.",
                "fields": [
                    {"name": "top_topics", "type": "textarea", "rows": 5},
                ],
            },
            {
                "id": "participants",
                "title": "Participant engagement",
                "fields": [
                    {"name": "total_participants", "label": "Total participants", "type": "text"},
                    {"name": "avg_per_study", "label": "Average per study", "type": "text"},
                    {"name": "enterprise_count", "label": "Enterprise users", "type": "text"},
                    {"name": "smb_count", "label": "SMB users", "type": "text"},
                    {"name": "individual_count", "label": "Individual users", "type": "text"},
                    {"name": "internal_count", "label": "Internal stakeholders", "type": "text"},
                ],
            },
            {
                "id": "impact_highlights",
                "title": "Impact highlights",
                "fields": [
                    {"name": "studies_with_impact", "label": "Studies with documented impact (count + %)", "type": "text"},
                    {"name": "roadmap_changes", "label": "Studies that influenced roadmap decisions", "type": "text"},
                    {"name": "design_changes", "label": "Studies that drove design changes", "type": "text"},
                    {"name": "strategic_pivots", "label": "Studies that informed strategy", "type": "text"},
                    {"name": "user_metrics_improved", "label": "Studies with user-metric improvements", "type": "text"},
                    {"name": "business_metrics_improved", "label": "Studies with business-metric improvements", "type": "text"},
                    {"name": "impact_stories", "label": "Top impact stories (one per line)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "gaps",
                "title": "Research gaps identified",
                "fields": [
                    {"name": "under_researched", "label": "Under-researched areas (product/topic)", "type": "textarea", "rows": 3},
                    {"name": "under_represented_segments", "label": "Under-represented segments", "type": "textarea", "rows": 3},
                    {"name": "future_opportunities", "label": "Opportunities for future research", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "usage",
                "title": "Repository usage",
                "fields": [
                    {"name": "repo_views", "label": "Repository views", "type": "text"},
                    {"name": "most_viewed", "label": "Most viewed studies (one per line)", "type": "textarea", "rows": 3},
                    {"name": "top_searches", "label": "Top search terms", "type": "text"},
                ],
            },
            {
                "id": "portfolio_themes",
                "title": "Key themes across portfolio",
                "blurb": "Per theme: name · # studies · brief description.",
                "fields": [
                    {"name": "themes", "type": "textarea", "rows": 6},
                ],
            },
            {
                "id": "looking_ahead",
                "title": "Looking ahead",
                "fields": [
                    {"name": "planned_research", "label": "Planned research (one per line)", "type": "textarea", "rows": 3},
                    {"name": "current_team", "label": "Current team size", "type": "text"},
                    {"name": "estimated_capacity", "label": "Estimated capacity (studies / quarter)", "type": "text"},
                ],
            },
            {
                "id": "full_list",
                "title": "Full study list",
                "blurb": "Chronological list — one per line: date · study ID · study name · method · product area.",
                "fields": [
                    {"name": "full_list", "type": "textarea", "rows": 10},
                ],
            },
            {
                "id": "contact",
                "title": "Contact",
                "fields": [
                    {"name": "repo_link", "label": "Repository link", "type": "text"},
                    {"name": "contact", "label": "Contact (name + email)", "type": "text"},
                ],
            },
        ],
    },
    "UXR-009-template-5.4": {
        "title": "Repository Onboarding Guide",
        "intro": "Customize the org-specific bits (URLs, contacts, training info) so the guide is ready to hand to new team members. The rest is standard scaffolding from the SOP.",
        "sections": [
            {
                "id": "access",
                "title": "How to access",
                "fields": [
                    {"name": "repo_url", "label": "Repository URL", "type": "text"},
                    {"name": "login", "label": "Login (e.g. company SSO)", "type": "text"},
                    {"name": "homepage_link", "label": "Homepage", "type": "text"},
                    {"name": "recent_link", "label": "Recent research", "type": "text"},
                    {"name": "browse_topic_link", "label": "Browse by topic", "type": "text"},
                    {"name": "mobile_access", "label": "Mobile access (yes/no + how)", "type": "text"},
                ],
            },
            {
                "id": "contacts",
                "title": "Getting help",
                "fields": [
                    {"name": "ops_contact", "label": "Research Ops contact", "type": "text"},
                    {"name": "lead_contact", "label": "Research Lead contact", "type": "text", "autofill": "project.owner"},
                    {"name": "support_email", "label": "Support email", "type": "text"},
                    {"name": "slack_channel", "label": "Slack channel", "type": "text"},
                ],
            },
            {
                "id": "contribution",
                "title": "Contributing to repository",
                "fields": [
                    {"name": "id_contact", "label": "Who to contact for a new Study ID", "type": "text"},
                    {"name": "publish_window", "label": "Publish window after study completion", "type": "text", "placeholder": "Within 1 week"},
                    {"name": "broken_links_contact", "label": "Broken links — report to", "type": "text"},
                    {"name": "improvements_contact", "label": "Suggestions — email", "type": "text"},
                ],
            },
            {
                "id": "training",
                "title": "Training & support",
                "fields": [
                    {"name": "live_training", "label": "Live training schedule", "type": "text"},
                    {"name": "video_tutorials", "label": "Video tutorials link", "type": "text"},
                    {"name": "office_hours", "label": "Office hours", "type": "text"},
                ],
            },
            {
                "id": "policies",
                "title": "Local policies",
                "fields": [
                    {"name": "share_externally", "label": "Can content be shared externally?", "type": "textarea", "rows": 2, "placeholder": "Default: No, Internal Use Only."},
                    {"name": "update_cadence", "label": "Repository update cadence", "type": "text", "placeholder": "Continuous additions; quarterly curation"},
                    {"name": "raw_data_restrictions", "label": "Raw data restrictions", "type": "textarea", "rows": 2},
                    {"name": "archive_threshold", "label": "When studies become 'old' (verify relevance)", "type": "text", "placeholder": "Older than 2 years"},
                ],
            },
        ],
    },
    "UXR-009-template-5.5": {
        "title": "Repository Health Check",
        "multi_instance": True,
        "instance_singular": "check",
        "instance_plural": "checks",
        "intro": "Run quarterly. Each instance is one health check covering completeness, accuracy, taxonomy, usability, content quality, and archiving — with a priority action list at the end.",
        "sections": [
            {
                "id": "header",
                "title": "Check header",
                "fields": [
                    {"name": "check_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "reviewer", "label": "Reviewed by", "type": "text", "autofill": "project.owner"},
                    {"name": "period_covered", "label": "Period covered", "type": "text"},
                ],
            },
            {
                "id": "completeness",
                "title": "1. Completeness",
                "fields": [
                    {"name": "studies_completed", "label": "Studies completed in period", "type": "text"},
                    {"name": "entries_created", "label": "Entries created", "type": "text"},
                    {"name": "gap_missing", "label": "Gap (missing entries)", "type": "text"},
                    {"name": "sample_reviewed", "label": "Sample reviewed for field completeness", "type": "text"},
                    {"name": "field_id", "label": "Study ID present (N / total)", "type": "text"},
                    {"name": "field_title", "label": "Title present (N / total)", "type": "text"},
                    {"name": "field_date", "label": "Date present (N / total)", "type": "text"},
                    {"name": "field_lead", "label": "Research lead listed (N / total)", "type": "text"},
                    {"name": "field_method", "label": "Method documented (N / total)", "type": "text"},
                    {"name": "field_summary", "label": "Study summary complete (N / total)", "type": "text"},
                    {"name": "field_findings", "label": "Key findings documented (N / total)", "type": "text"},
                    {"name": "field_artifact", "label": "At least one artifact linked (N / total)", "type": "text"},
                    {"name": "field_tags", "label": "Tags applied (N / total)", "type": "text"},
                    {"name": "completeness_issues", "label": "Issues identified", "type": "textarea", "rows": 3},
                    {"name": "completeness_actions", "label": "Action items", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "accuracy",
                "title": "2. Accuracy",
                "fields": [
                    {"name": "links_tested", "label": "Links tested (N)", "type": "text"},
                    {"name": "links_working", "label": "Working links", "type": "text"},
                    {"name": "links_broken", "label": "Broken links", "type": "text"},
                    {"name": "broken_link_list", "label": "Broken links (one per line: entry · type · URL)", "type": "textarea", "rows": 4},
                    {"name": "contacts_checked", "label": "Contact info — entries checked", "type": "text"},
                    {"name": "contacts_outdated", "label": "Outdated contact info (count)", "type": "text"},
                    {"name": "info_verified", "label": "Study info verified (N entries)", "type": "text"},
                    {"name": "inaccuracies", "label": "Inaccuracies found", "type": "textarea", "rows": 3},
                    {"name": "accuracy_actions", "label": "Action items", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "tagging",
                "title": "3. Tagging & taxonomy",
                "fields": [
                    {"name": "total_tags", "label": "Total tags in system", "type": "text"},
                    {"name": "active_tags", "label": "Tags used in last 3 months", "type": "text"},
                    {"name": "stale_tags", "label": "Tags unused 6+ months", "type": "text"},
                    {"name": "orphan_tags", "label": "Orphan tags (used once) — list", "type": "textarea", "rows": 3},
                    {"name": "inconsistent_tags", "label": "Inconsistent tags (overlap / ambiguity)", "type": "textarea", "rows": 3},
                    {"name": "tags_action_merge", "label": "Merge", "type": "textarea", "rows": 2},
                    {"name": "tags_action_clarify", "label": "Clarify definitions", "type": "textarea", "rows": 2},
                    {"name": "tags_action_retire", "label": "Retire", "type": "textarea", "rows": 2},
                    {"name": "tags_action_add", "label": "Add new tags", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "usability",
                "title": "4. Usability",
                "fields": [
                    {"name": "search_tests", "label": "Search tests (one per line: term · expected · actual · pass?)", "type": "textarea", "rows": 5},
                    {"name": "search_issues", "label": "Search issues found", "type": "textarea", "rows": 3},
                    {"name": "nav_homepage_fast", "label": "Homepage loads quickly", "type": "checkbox"},
                    {"name": "nav_filters_work", "label": "Filters work correctly", "type": "checkbox"},
                    {"name": "nav_sort_works", "label": "Sort options function", "type": "checkbox"},
                    {"name": "nav_pages_fast", "label": "Study pages load quickly", "type": "checkbox"},
                    {"name": "nav_links_correct", "label": "Links navigate correctly", "type": "checkbox"},
                    {"name": "nav_issues", "label": "Navigation issues", "type": "textarea", "rows": 3},
                    {"name": "user_feedback_count", "label": "User feedback received this period (count)", "type": "text"},
                    {"name": "user_feedback_themes", "label": "Themes in feedback", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "analytics",
                "title": "5. Usage analytics",
                "fields": [
                    {"name": "total_views", "label": "Total views this period", "type": "text"},
                    {"name": "unique_users", "label": "Unique users", "type": "text"},
                    {"name": "avg_per_user", "label": "Average views per user", "type": "text"},
                    {
                        "name": "trend",
                        "label": "Trend",
                        "type": "radio",
                        "options": [
                            {"value": "increasing", "label": "Increasing"},
                            {"value": "stable", "label": "Stable"},
                            {"value": "decreasing", "label": "Decreasing"},
                        ],
                    },
                    {"name": "most_viewed", "label": "Most viewed studies (one per line)", "type": "textarea", "rows": 3},
                    {"name": "least_viewed", "label": "Least viewed (older than 3 months)", "type": "textarea", "rows": 3},
                    {"name": "top_searches", "label": "Top search terms", "type": "textarea", "rows": 2},
                    {"name": "zero_results", "label": "Zero-result searches (need attention)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "quality",
                "title": "6. Content quality",
                "fields": [
                    {"name": "summaries_reviewed", "label": "Study summaries reviewed", "type": "text"},
                    {"name": "summaries_well_written", "label": "Well-written (N / total)", "type": "text"},
                    {"name": "summaries_template", "label": "Follow template", "type": "text"},
                    {"name": "summaries_length", "label": "Appropriate length", "type": "text"},
                    {"name": "summaries_findings_clear", "label": "Findings clear", "type": "text"},
                    {"name": "quality_issues", "label": "Quality issues identified", "type": "textarea", "rows": 3},
                    {"name": "duplicates", "label": "Duplicate / very similar studies (list)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "archiving",
                "title": "7. Archiving",
                "fields": [
                    {"name": "candidates_old", "label": "Studies older than 5 years", "type": "text"},
                    {"name": "candidates_retired", "label": "Studies on retired products", "type": "text"},
                    {"name": "candidates_superseded", "label": "Superseded studies", "type": "text"},
                    {"name": "candidates_reviewed", "label": "Reviewed for archival", "type": "text"},
                    {"name": "archive_count", "label": "Archive (count)", "type": "text"},
                    {"name": "keep_count", "label": "Keep active", "type": "text"},
                    {"name": "delete_count", "label": "Delete", "type": "text"},
                ],
            },
            {
                "id": "impact",
                "title": "8. Impact tracking",
                "fields": [
                    {"name": "recent_with_impact", "label": "Recent studies (< 6 mo) with impact documented (N / total)", "type": "text"},
                    {"name": "older_with_impact", "label": "Older studies (6–18 mo) with impact documented", "type": "text"},
                    {"name": "needing_followup", "label": "Studies needing impact follow-up", "type": "text"},
                ],
            },
            {
                "id": "scores",
                "title": "Overall health scores",
                "fields": [
                    {"name": "score_completeness", "label": "Completeness /100", "type": "text"},
                    {"name": "score_accuracy", "label": "Accuracy /100", "type": "text"},
                    {"name": "score_usability", "label": "Usability /100", "type": "text"},
                    {"name": "score_quality", "label": "Quality /100", "type": "text"},
                    {"name": "score_overall", "label": "Overall average /100", "type": "text"},
                    {
                        "name": "health_status",
                        "label": "Health status",
                        "type": "radio",
                        "options": [
                            {"value": "excellent", "label": "Excellent (90–100)"},
                            {"value": "good", "label": "Good (75–89)"},
                            {"value": "fair", "label": "Fair (60–74)"},
                            {"value": "poor", "label": "Poor (<60)"},
                        ],
                    },
                ],
            },
            {
                "id": "actions",
                "title": "Priority action items",
                "fields": [
                    {"name": "actions_high", "label": "HIGH priority (within 1 week)", "type": "textarea", "rows": 4},
                    {"name": "actions_medium", "label": "MEDIUM priority (within 1 month)", "type": "textarea", "rows": 4},
                    {"name": "actions_low", "label": "LOW priority (within quarter)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "next",
                "title": "Next check & sign-off",
                "fields": [
                    {"name": "next_check_date", "label": "Next health check date", "type": "date"},
                    {"name": "reviewer_signoff", "label": "Reviewed by", "type": "text", "autofill": "project.owner"},
                    {"name": "reviewer_date", "label": "Sign-off date", "type": "date"},
                    {"name": "lead_signoff", "label": "Research Lead approval", "type": "text"},
                    {"name": "lead_signoff_date", "label": "Approval date", "type": "date"},
                ],
            },
        ],
    },
    "UXR-008-template-5.1": {
        "title": "Research Readout Presentation Outline",
        "intro": "One outline per study. Plan the slide flow, the time budget, and the messages you want to land. Use the Word export as a slide-deck skeleton.",
        "sections": [
            {
                "id": "header",
                "title": "Presentation header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "presentation_date", "label": "Date", "type": "date"},
                    {"name": "presenter", "label": "Presenter / research team", "type": "text", "autofill": "project.owner"},
                    {"name": "audience", "label": "Audience", "type": "text", "autofill": "project.stakeholder"},
                    {"name": "duration_total", "label": "Total duration", "type": "text", "placeholder": "60 min"},
                ],
            },
            {
                "id": "context",
                "title": "Context",
                "fields": [
                    {"name": "why_research", "label": "Why this research (business challenge, what prompted it)", "type": "textarea", "rows": 3},
                    {"name": "rq_primary", "label": "Primary research question", "type": "textarea", "rows": 2},
                    {"name": "rq_secondary", "label": "Secondary questions", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "approach",
                "title": "Approach",
                "fields": [
                    {"name": "method", "label": "Method", "type": "text"},
                    {"name": "method_why", "label": "Why this approach", "type": "textarea", "rows": 2},
                    {"name": "when_conducted", "label": "When conducted", "type": "text"},
                    {"name": "participants", "label": "Participants (who, how many, how recruited)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "findings",
                "title": "Key findings",
                "blurb": "3–5 findings. For each: statement, evidence, and a representative quote.",
                "fields": [
                    {"name": "findings_overview", "label": "Findings overview (one-line list)", "type": "textarea", "rows": 3},
                    {"name": "f1_statement", "label": "Finding 1 statement", "type": "textarea", "rows": 2},
                    {"name": "f1_evidence", "label": "Finding 1 supporting evidence", "type": "textarea", "rows": 3},
                    {"name": "f1_quote", "label": "Finding 1 quote", "type": "textarea", "rows": 2},
                    {"name": "f2_statement", "label": "Finding 2 statement", "type": "textarea", "rows": 2},
                    {"name": "f2_evidence", "label": "Finding 2 evidence", "type": "textarea", "rows": 3},
                    {"name": "f2_quote", "label": "Finding 2 quote", "type": "textarea", "rows": 2},
                    {"name": "f3_statement", "label": "Finding 3 statement", "type": "textarea", "rows": 2},
                    {"name": "f3_evidence", "label": "Finding 3 evidence", "type": "textarea", "rows": 3},
                    {"name": "f3_quote", "label": "Finding 3 quote", "type": "textarea", "rows": 2},
                    {"name": "f4_statement", "label": "Finding 4 statement (optional)", "type": "textarea", "rows": 2},
                    {"name": "f4_evidence", "label": "Finding 4 evidence", "type": "textarea", "rows": 3},
                    {"name": "f4_quote", "label": "Finding 4 quote", "type": "textarea", "rows": 2},
                    {"name": "f5_statement", "label": "Finding 5 statement (optional)", "type": "textarea", "rows": 2},
                    {"name": "f5_evidence", "label": "Finding 5 evidence", "type": "textarea", "rows": 3},
                    {"name": "f5_quote", "label": "Finding 5 quote", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "insights",
                "title": "Insights",
                "fields": [
                    {"name": "how_findings_connect", "label": "How findings connect (patterns, why they exist, what they mean)", "type": "textarea", "rows": 4},
                    {"name": "ux_implications", "label": "User experience implications", "type": "textarea", "rows": 3},
                    {"name": "business_implications", "label": "Business implications", "type": "textarea", "rows": 3},
                    {"name": "strategic", "label": "Strategic considerations", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "recommendations",
                "title": "Recommendations",
                "blurb": "3–5 prioritized recommendations. For each: what to do, why, expected impact, implementation considerations.",
                "fields": [
                    {"name": "rec_overview", "label": "Recommendations overview", "type": "textarea", "rows": 3},
                    {"name": "rec_1", "label": "Recommendation 1 (HIGH)", "type": "textarea", "rows": 4},
                    {"name": "rec_2", "label": "Recommendation 2 (HIGH)", "type": "textarea", "rows": 4},
                    {"name": "rec_3", "label": "Recommendation 3 (MEDIUM)", "type": "textarea", "rows": 4},
                    {"name": "rec_4", "label": "Recommendation 4 (optional)", "type": "textarea", "rows": 4},
                    {"name": "rec_5", "label": "Recommendation 5 (optional)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "next_steps",
                "title": "Next steps",
                "fields": [
                    {"name": "decisions_needed", "label": "Decisions needed", "type": "textarea", "rows": 3},
                    {"name": "action_items", "label": "Action items with owners and dates", "type": "textarea", "rows": 4},
                    {"name": "followup_research", "label": "Follow-up research needs", "type": "textarea", "rows": 2},
                    {"name": "materials_access", "label": "How to access materials", "type": "text"},
                ],
            },
            {
                "id": "timing",
                "title": "Time allocation",
                "fields": [
                    {"name": "t_context", "label": "Context & approach (min)", "type": "text", "placeholder": "5"},
                    {"name": "t_findings", "label": "Key findings (min)", "type": "text", "placeholder": "25"},
                    {"name": "t_insights", "label": "Insights (min)", "type": "text", "placeholder": "10"},
                    {"name": "t_recs", "label": "Recommendations (min)", "type": "text", "placeholder": "10"},
                    {"name": "t_next", "label": "Next steps (min)", "type": "text", "placeholder": "5"},
                    {"name": "t_qa", "label": "Q&A (min)", "type": "text", "placeholder": "15"},
                ],
            },
            {
                "id": "messages",
                "title": "Key messages & prep",
                "fields": [
                    {"name": "key_message_1", "label": "Primary takeaway", "type": "textarea", "rows": 2},
                    {"name": "key_message_2", "label": "Supporting message", "type": "textarea", "rows": 2},
                    {"name": "key_message_3", "label": "Call to action", "type": "textarea", "rows": 2},
                    {"name": "anticipated_questions", "label": "Anticipated questions and how you'll answer", "type": "textarea", "rows": 5},
                    {"name": "stakeholder_considerations", "label": "Stakeholder considerations (name · cares about · may resist · how to address)", "type": "textarea", "rows": 5},
                ],
            },
            {
                "id": "backup",
                "title": "Backup slides",
                "blurb": "What you might need but doesn't fit the main flow.",
                "fields": [
                    {"name": "backup_slides", "type": "textarea", "rows": 4},
                ],
            },
        ],
    },
    "UXR-008-template-5.2": {
        "title": "Executive Summary",
        "intro": "One page (two max) for executives who won't read the full report. Lead with the situation, end with what's at stake.",
        "sections": [
            {
                "id": "header",
                "title": "Header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "summary_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "research_team", "label": "Research team", "type": "text", "autofill": "project.owner"},
                ],
            },
            {
                "id": "situation",
                "title": "The situation",
                "blurb": "2–3 sentences establishing business context that prompted research.",
                "fields": [
                    {"name": "situation", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "approach",
                "title": "Research approach",
                "blurb": "1–2 sentences on method and participants.",
                "fields": [
                    {"name": "approach", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "findings",
                "title": "Key findings",
                "blurb": "3–5 bullet points — the most critical findings only.",
                "fields": [
                    {"name": "finding_1", "label": "Finding 1 (statement + evidence/prevalence)", "type": "textarea", "rows": 3},
                    {"name": "finding_2", "label": "Finding 2", "type": "textarea", "rows": 3},
                    {"name": "finding_3", "label": "Finding 3", "type": "textarea", "rows": 3},
                    {"name": "finding_4", "label": "Finding 4 (optional)", "type": "textarea", "rows": 3},
                    {"name": "finding_5", "label": "Finding 5 (optional)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "meaning",
                "title": "What it means",
                "blurb": "2–3 sentences on business implications.",
                "fields": [
                    {"name": "what_it_means", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "recommendations",
                "title": "Recommendations (prioritized)",
                "fields": [
                    {"name": "high_rec_1", "label": "HIGH priority — recommendation 1 (impact + rationale)", "type": "textarea", "rows": 3},
                    {"name": "high_rec_2", "label": "HIGH priority — recommendation 2", "type": "textarea", "rows": 3},
                    {"name": "medium_rec_1", "label": "MEDIUM priority — recommendation 1", "type": "textarea", "rows": 3},
                    {"name": "medium_rec_2", "label": "MEDIUM priority — recommendation 2", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "stakes",
                "title": "What's at stake",
                "fields": [
                    {"name": "if_we_act", "label": "If we act — expected positive outcomes", "type": "textarea", "rows": 4},
                    {"name": "if_we_dont", "label": "If we don't — expected negative outcomes", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "confidence",
                "title": "Confidence level",
                "fields": [
                    {
                        "name": "confidence",
                        "label": "Confidence",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "HIGH"},
                            {"value": "medium", "label": "MEDIUM"},
                            {"value": "low", "label": "LOW"},
                        ],
                    },
                    {"name": "confidence_reasons", "label": "We are confident because… (one reason per line)", "type": "textarea", "rows": 4},
                    {"name": "limitations", "label": "Limitations to note", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "next_steps",
                "title": "Next steps",
                "fields": [
                    {"name": "immediate", "label": "Immediate (decisions / actions with owner + date)", "type": "textarea", "rows": 4},
                    {"name": "thirty_days", "label": "30-day follow-ups", "type": "textarea", "rows": 3},
                    {"name": "longer_term", "label": "Longer-term research / implementation", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "materials",
                "title": "Full materials",
                "fields": [
                    {"name": "report_link", "label": "Complete research report", "type": "text"},
                    {"name": "deck_link", "label": "Detailed presentation", "type": "text"},
                    {"name": "researcher_contact", "label": "Researcher contact (name, email)", "type": "text"},
                ],
            },
        ],
    },
    "UXR-008-template-5.3": {
        "title": "Research Highlight One-Pager",
        "intro": "A single scannable page for sharing — Slack-friendly, attaches to emails, gets pinned to walls. Lead with the primary finding, end with how to learn more.",
        "sections": [
            {
                "id": "header",
                "title": "Header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "highlight_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "team", "label": "Team", "type": "text", "autofill": "project.owner"},
                ],
            },
            {
                "id": "primary",
                "title": "Primary finding",
                "blurb": "One sentence capturing the most important insight.",
                "fields": [
                    {"name": "primary_finding", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "research",
                "title": "The research",
                "fields": [
                    {"name": "method", "label": "Method", "type": "text"},
                    {"name": "participants", "label": "Participants (number + role description)", "type": "text"},
                    {"name": "when", "label": "When", "type": "text", "placeholder": "March 2026"},
                ],
            },
            {
                "id": "findings",
                "title": "Key findings",
                "blurb": "Three findings, each with a representative quote.",
                "fields": [
                    {"name": "f1_statement", "label": "Finding 1 (specific statement with evidence)", "type": "textarea", "rows": 2},
                    {"name": "f1_quote", "label": "Quote", "type": "textarea", "rows": 2},
                    {"name": "f2_statement", "label": "Finding 2", "type": "textarea", "rows": 2},
                    {"name": "f2_quote", "label": "Quote", "type": "textarea", "rows": 2},
                    {"name": "f3_statement", "label": "Finding 3", "type": "textarea", "rows": 2},
                    {"name": "f3_quote", "label": "Quote", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "meaning",
                "title": "What it means",
                "blurb": "2–3 sentence interpretation of implications.",
                "fields": [
                    {"name": "what_it_means", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "recommendations",
                "title": "Top recommendations",
                "fields": [
                    {"name": "rec_1", "label": "Recommendation 1 (HIGH) — what + brief rationale", "type": "textarea", "rows": 3},
                    {"name": "rec_2", "label": "Recommendation 2 (HIGH)", "type": "textarea", "rows": 3},
                    {"name": "rec_3", "label": "Recommendation 3 (MEDIUM)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "impact",
                "title": "Expected impact",
                "fields": [
                    {"name": "user_impact", "label": "User impact", "type": "textarea", "rows": 2},
                    {"name": "business_impact", "label": "Business impact", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "learn_more",
                "title": "Learn more",
                "fields": [
                    {"name": "report_link", "label": "Full report", "type": "text"},
                    {"name": "contact", "label": "Contact (name, email)", "type": "text"},
                ],
            },
        ],
    },
    "UXR-008-template-5.4": {
        "title": "Stakeholder Workshop Agenda",
        "multi_instance": True,
        "instance_singular": "workshop",
        "instance_plural": "workshops",
        "intro": "One entry per workshop. Cover the timing, the activities, and the decisions you want to come out with.",
        "sections": [
            {
                "id": "header",
                "title": "Workshop details",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "workshop_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "workshop_time", "label": "Time", "type": "text", "placeholder": "10:00 – 13:15"},
                    {"name": "duration", "label": "Total duration", "type": "text", "placeholder": "3 hours"},
                    {"name": "facilitator", "label": "Facilitator", "type": "text", "autofill": "project.owner"},
                    {"name": "scribe", "label": "Scribe", "type": "text"},
                ],
            },
            {
                "id": "purpose",
                "title": "Purpose & participants",
                "fields": [
                    {"name": "purpose", "label": "Purpose", "type": "textarea", "rows": 2, "placeholder": "Collaborative synthesis and decision-making based on research findings."},
                    {"name": "research_team", "label": "Research team", "type": "text"},
                    {"name": "product_design", "label": "Product / design", "type": "text"},
                    {"name": "engineering", "label": "Engineering", "type": "text"},
                    {"name": "stakeholders", "label": "Other stakeholders", "type": "text"},
                ],
            },
            {
                "id": "materials",
                "title": "Materials needed",
                "fields": [
                    {"name": "m_findings", "label": "Research findings presentation", "type": "checkbox"},
                    {"name": "m_quotes", "label": "Printed key quotes", "type": "checkbox"},
                    {"name": "m_board", "label": "Whiteboard or digital board (Miro/Mural)", "type": "checkbox"},
                    {"name": "m_stickies", "label": "Sticky notes and markers (if in-person)", "type": "checkbox"},
                    {"name": "m_preread", "label": "Pre-read: research summary sent 2 days before", "type": "checkbox"},
                    {"name": "m_other", "label": "Other materials", "type": "text"},
                ],
            },
            {
                "id": "agenda",
                "title": "Agenda blocks",
                "blurb": "Standard 3-hour shape — adjust to your session.",
                "fields": [
                    {"name": "block_intro", "label": "Introduction & context (15 min)", "type": "textarea", "rows": 3, "placeholder": "Goals, brief research overview, how today will work, ground rules"},
                    {"name": "block_findings", "label": "Key findings presentation (30 min)", "type": "textarea", "rows": 3, "placeholder": "Main findings, evidence, initial reactions"},
                    {"name": "block_break1", "label": "Break (15 min)", "type": "text"},
                    {"name": "block_insights", "label": "Insights exploration (30 min)", "type": "textarea", "rows": 4, "placeholder": "Small-group discussion: what surprised you, what confirms, what raises questions"},
                    {"name": "block_ideation", "label": "Collaborative ideation — How Might We (45 min)", "type": "textarea", "rows": 4, "placeholder": "Silent idea generation (10), share & group (15), discuss & prioritize (20)"},
                    {"name": "block_break2", "label": "Break (15 min)", "type": "text"},
                    {"name": "block_decisions", "label": "Decision-making — roadmap implications (30 min)", "type": "textarea", "rows": 4, "placeholder": "Immediate actions, roadmap impact, open questions"},
                    {"name": "block_close", "label": "Next steps & closing (15 min)", "type": "textarea", "rows": 3, "placeholder": "Recap decisions, action items with owners + dates, follow-up plans, thanks"},
                ],
            },
            {
                "id": "pre_workshop",
                "title": "Pre-workshop preparation",
                "fields": [
                    {"name": "pre_summary", "label": "Sent research summary 2 days before", "type": "checkbox"},
                    {"name": "pre_room", "label": "Booked room / set up video call", "type": "checkbox"},
                    {"name": "pre_materials", "label": "Prepared materials (presentation, supplies)", "type": "checkbox"},
                    {"name": "pre_board", "label": "Set up digital board if remote", "type": "checkbox"},
                    {"name": "pre_prints", "label": "Printed key quotes and findings", "type": "checkbox"},
                ],
            },
            {
                "id": "facilitation",
                "title": "Facilitation reminders",
                "fields": [
                    {"name": "facilitation_notes", "type": "textarea", "rows": 6, "placeholder": "Keep to time · encourage all voices · capture everything · stay neutral · focus on user needs (not solutions, initially) · create safe space for dissent"},
                ],
            },
            {
                "id": "post_workshop",
                "title": "Post-workshop tasks",
                "fields": [
                    {"name": "post_decisions", "label": "Documented decisions and action items", "type": "checkbox"},
                    {"name": "post_summary", "label": "Sent summary within 24 hours", "type": "checkbox"},
                    {"name": "post_followup", "label": "Followed up on action items", "type": "checkbox"},
                    {"name": "post_impact", "label": "Tracking impact of decisions made", "type": "checkbox"},
                ],
            },
            {
                "id": "outcomes",
                "title": "Outcomes captured",
                "fields": [
                    {"name": "decisions_made", "label": "Decisions made", "type": "textarea", "rows": 4},
                    {"name": "action_items", "label": "Action items (one per line · owner · date)", "type": "textarea", "rows": 4},
                    {"name": "open_questions", "label": "Open questions raised", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
    "UXR-008-template-5.5": {
        "title": "Research Impact Assessment",
        "intro": "Run this 1–3 months after the readout to see what the research actually changed. Captures both the soft impact (awareness, decisions) and hard impact (metrics, ROI).",
        "sections": [
            {
                "id": "header",
                "title": "Assessment header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "study_completed", "label": "Study completed", "type": "date"},
                    {"name": "primary_stakeholders", "label": "Primary stakeholder(s)", "type": "text", "autofill": "project.stakeholder"},
                    {"name": "assessor", "label": "Impact assessment by", "type": "text", "autofill": "project.owner"},
                    {"name": "assessment_date", "label": "Assessment date", "type": "date", "autofill": "today"},
                    {"name": "months_after", "label": "Months after research", "type": "text", "placeholder": "3"},
                ],
            },
            {
                "id": "overview",
                "title": "Research overview",
                "fields": [
                    {"name": "purpose", "label": "Purpose (what the research aimed to learn)", "type": "textarea", "rows": 2},
                    {"name": "finding_1", "label": "Finding 1", "type": "textarea", "rows": 2},
                    {"name": "finding_2", "label": "Finding 2", "type": "textarea", "rows": 2},
                    {"name": "finding_3", "label": "Finding 3", "type": "textarea", "rows": 2},
                    {"name": "rec_1", "label": "Recommendation 1 (with priority)", "type": "textarea", "rows": 2},
                    {"name": "rec_2", "label": "Recommendation 2", "type": "textarea", "rows": 2},
                    {"name": "rec_3", "label": "Recommendation 3", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "comm_activities",
                "title": "Communication activities",
                "fields": [
                    {"name": "readout_date", "label": "Primary readout date", "type": "date"},
                    {"name": "readout_attendees", "label": "Readout attendees (count + roles)", "type": "text"},
                    {"name": "readout_format", "label": "Format", "type": "text", "placeholder": "Presentation · workshop"},
                    {"name": "readout_duration", "label": "Duration (min)", "type": "text"},
                    {"name": "additional_shareouts", "label": "Additional shareouts (one per line: activity · date · attendees)", "type": "textarea", "rows": 4},
                    {"name": "materials_distributed", "label": "Materials distributed (full report views · exec summary · highlight · repository views)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "awareness",
                "title": "Awareness & understanding",
                "fields": [
                    {"name": "total_awareness", "label": "Total people who saw / heard research (approx)", "type": "text"},
                    {"name": "awareness_evidence", "label": "Evidence of awareness", "type": "textarea", "rows": 3},
                    {
                        "name": "understanding_quality",
                        "label": "Quality of Q&A / discussion",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "High"},
                            {"value": "medium", "label": "Medium"},
                            {"value": "low", "label": "Low"},
                        ],
                    },
                    {"name": "understanding_evidence", "label": "Evidence of understanding", "type": "textarea", "rows": 3},
                    {"name": "misunderstandings", "label": "Misunderstandings corrected", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "consideration",
                "title": "Consideration in decisions",
                "fields": [
                    {"name": "meetings_referenced", "label": "Meetings where research was referenced (one per line: meeting · date · how used)", "type": "textarea", "rows": 4},
                    {"name": "stakeholder_quotes", "label": "Stakeholder quotes (one per line)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "decision_1",
                "title": "Decision 1 influenced",
                "fields": [
                    {"name": "d1_description", "label": "Description of decision made", "type": "textarea", "rows": 2},
                    {
                        "name": "d1_influence",
                        "label": "Influence of research",
                        "type": "radio",
                        "options": [
                            {"value": "direct", "label": "Direct — primary factor"},
                            {"value": "strong", "label": "Strong — significant among several"},
                            {"value": "moderate", "label": "Moderate — one of many considerations"},
                            {"value": "weak", "label": "Weak — mentioned but other factors dominated"},
                            {"value": "none", "label": "No influence"},
                            {"value": "unknown", "label": "Unknown"},
                        ],
                    },
                    {"name": "d1_before", "label": "Before research (what was planned)", "type": "textarea", "rows": 2},
                    {"name": "d1_after", "label": "After research (what actually happened)", "type": "textarea", "rows": 2},
                    {"name": "d1_how", "label": "How research changed it", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "decision_2",
                "title": "Decision 2 influenced (optional)",
                "fields": [
                    {"name": "d2_description", "label": "Description", "type": "textarea", "rows": 2},
                    {
                        "name": "d2_influence",
                        "label": "Influence",
                        "type": "radio",
                        "options": [
                            {"value": "direct", "label": "Direct"},
                            {"value": "strong", "label": "Strong"},
                            {"value": "moderate", "label": "Moderate"},
                            {"value": "weak", "label": "Weak"},
                            {"value": "none", "label": "None"},
                        ],
                    },
                    {"name": "d2_before_after", "label": "Before → After", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "actions_taken",
                "title": "Actions taken (by recommendation)",
                "fields": [
                    {
                        "name": "rec1_status",
                        "label": "Recommendation 1 status",
                        "type": "radio",
                        "options": [
                            {"value": "completed", "label": "Completed"},
                            {"value": "in_progress", "label": "In progress"},
                            {"value": "planned", "label": "Planned"},
                            {"value": "not_pursued", "label": "Not pursued"},
                        ],
                    },
                    {"name": "rec1_action", "label": "Action taken (or reason not pursued)", "type": "textarea", "rows": 3},
                    {"name": "rec1_owner", "label": "Owner", "type": "text"},
                    {
                        "name": "rec2_status",
                        "label": "Recommendation 2 status",
                        "type": "radio",
                        "options": [
                            {"value": "completed", "label": "Completed"},
                            {"value": "in_progress", "label": "In progress"},
                            {"value": "planned", "label": "Planned"},
                            {"value": "not_pursued", "label": "Not pursued"},
                        ],
                    },
                    {"name": "rec2_action", "label": "Action taken", "type": "textarea", "rows": 3},
                    {"name": "rec2_owner", "label": "Owner", "type": "text"},
                    {
                        "name": "rec3_status",
                        "label": "Recommendation 3 status",
                        "type": "radio",
                        "options": [
                            {"value": "completed", "label": "Completed"},
                            {"value": "in_progress", "label": "In progress"},
                            {"value": "planned", "label": "Planned"},
                            {"value": "not_pursued", "label": "Not pursued"},
                        ],
                    },
                    {"name": "rec3_action", "label": "Action taken", "type": "textarea", "rows": 3},
                    {"name": "rec3_owner", "label": "Owner", "type": "text"},
                ],
            },
            {
                "id": "metrics",
                "title": "Measurable outcomes",
                "blurb": "Per metric: name · baseline · current · change · attribution to research.",
                "fields": [
                    {"name": "ux_metrics", "label": "User experience metrics", "type": "textarea", "rows": 5},
                    {"name": "business_metrics", "label": "Business metrics", "type": "textarea", "rows": 5},
                ],
            },
            {
                "id": "qualitative",
                "title": "Qualitative impact",
                "fields": [
                    {"name": "user_impact", "label": "User impact (how UX improved + examples / quotes)", "type": "textarea", "rows": 4},
                    {"name": "team_impact", "label": "Team impact (how research affected team thinking / process)", "type": "textarea", "rows": 4},
                    {"name": "org_impact", "label": "Organizational impact (cultural / strategic shifts)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "roi",
                "title": "Research ROI estimate",
                "fields": [
                    {"name": "research_hours", "label": "Research hours", "type": "text"},
                    {"name": "hourly_rate", "label": "Hourly rate", "type": "text"},
                    {"name": "incentives_cost", "label": "Participant incentives ($)", "type": "text"},
                    {"name": "tools_cost", "label": "Tools / resources ($)", "type": "text"},
                    {"name": "total_investment", "label": "Total investment ($)", "type": "text"},
                    {"name": "value_created", "label": "Value created (engineering time saved, support cost reduction, revenue impact, etc.)", "type": "textarea", "rows": 5},
                    {"name": "estimated_total_value", "label": "Estimated total value ($)", "type": "text"},
                    {"name": "roi_ratio", "label": "ROI ratio (value : investment)", "type": "text", "placeholder": "8:1"},
                ],
            },
            {
                "id": "lessons",
                "title": "Lessons learned",
                "fields": [
                    {"name": "worked_well", "label": "What worked well in communication (one per line)", "type": "textarea", "rows": 4},
                    {"name": "could_improve", "label": "What could improve", "type": "textarea", "rows": 4},
                    {"name": "increase_impact", "label": "How to increase impact next time", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "followup",
                "title": "Follow-up research needs",
                "fields": [
                    {"name": "immediate_needs", "label": "Immediate needs (follow-up questions raised)", "type": "textarea", "rows": 3},
                    {"name": "longer_term", "label": "Longer-term areas for future exploration", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "rating",
                "title": "Overall impact rating",
                "fields": [
                    {
                        "name": "rating",
                        "label": "Research impact",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "High"},
                            {"value": "medium", "label": "Medium"},
                            {"value": "low", "label": "Low"},
                            {"value": "too_early", "label": "Too early to tell"},
                        ],
                    },
                    {"name": "rating_justification", "label": "Justification (based on evidence above)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "signoff",
                "title": "Sign-off",
                "fields": [
                    {"name": "completed_by", "label": "Completed by", "type": "text", "autofill": "project.owner"},
                    {"name": "completed_date", "label": "Completed date", "type": "date"},
                    {"name": "reviewed_by", "label": "Reviewed by research lead", "type": "text"},
                    {"name": "reviewed_date", "label": "Review date", "type": "date"},
                ],
            },
        ],
    },
    "UXR-007-template-5.1": {
        "title": "Analysis Plan",
        "intro": "One per study. Locks in your approach, timeline, and deliverables before you dive into coding. Share with the team so everyone knows the shape of analysis.",
        "sections": [
            {
                "id": "header",
                "title": "Study details",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "analysis_lead", "label": "Analysis lead", "type": "text", "autofill": "project.owner"},
                    {"name": "analysis_team", "label": "Analysis team", "type": "text"},
                    {"name": "timeline_start", "label": "Start", "type": "date"},
                    {"name": "timeline_end", "label": "End", "type": "date"},
                ],
            },
            {
                "id": "questions",
                "title": "Research questions",
                "fields": [
                    {"name": "rq_1", "label": "Primary question", "type": "textarea", "rows": 2},
                    {"name": "rq_2", "label": "Secondary question", "type": "textarea", "rows": 2},
                    {"name": "rq_3", "label": "Additional questions", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "approach",
                "title": "Analysis approach",
                "fields": [
                    {"name": "method", "label": "Primary method", "type": "text", "placeholder": "Inductive thematic analysis"},
                    {"name": "rationale", "label": "Rationale (why this approach for this study)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "data",
                "title": "Data to analyze",
                "fields": [
                    {"name": "session_notes_count", "label": "Session notes (count)", "type": "text"},
                    {"name": "transcripts_count", "label": "Transcripts (count)", "type": "text"},
                    {"name": "summaries_count", "label": "Session summaries (count)", "type": "text"},
                    {"name": "journal", "label": "Research journal included?", "type": "checkbox"},
                    {"name": "other_data", "label": "Other data sources", "type": "text"},
                    {"name": "total_volume", "label": "Total volume", "type": "text", "placeholder": "12 sessions · 12 participants · 240 pages"},
                    {"name": "qc_documentation", "label": "All documentation complete per UXR-006", "type": "checkbox"},
                    {"name": "qc_anonymization", "label": "Anonymization complete per UXR-002", "type": "checkbox"},
                    {"name": "qc_access", "label": "All files accessible to analysis team", "type": "checkbox"},
                ],
            },
            {
                "id": "phases",
                "title": "Analysis process",
                "blurb": "Six phases with their owners and target dates.",
                "fields": [
                    {"name": "p1_familiarization_owner", "label": "Phase 1 — Familiarization · owner", "type": "text"},
                    {"name": "p1_familiarization_date", "label": "Phase 1 due", "type": "date"},
                    {"name": "p2_coding_owner", "label": "Phase 2 — Coding · owner", "type": "text"},
                    {"name": "p2_coding_date", "label": "Phase 2 due", "type": "date"},
                    {"name": "p3_patterns_owner", "label": "Phase 3 — Pattern identification · owner", "type": "text"},
                    {"name": "p3_patterns_date", "label": "Phase 3 due", "type": "date"},
                    {"name": "p4_themes_owner", "label": "Phase 4 — Theme development · owner", "type": "text"},
                    {"name": "p4_themes_date", "label": "Phase 4 due", "type": "date"},
                    {"name": "p5_insights_owner", "label": "Phase 5 — Insight synthesis · owner", "type": "text"},
                    {"name": "p5_insights_date", "label": "Phase 5 due", "type": "date"},
                    {"name": "p6_validation_owner", "label": "Phase 6 — Validation · owner", "type": "text"},
                    {"name": "p6_validation_date", "label": "Phase 6 due", "type": "date"},
                ],
            },
            {
                "id": "sessions",
                "title": "Collaborative sessions",
                "blurb": "One block per session: date · duration · participants · goal.",
                "fields": [
                    {"name": "collab_session_1", "label": "Session 1 — Initial review", "type": "textarea", "rows": 3},
                    {"name": "collab_session_2", "label": "Session 2 — Affinity mapping", "type": "textarea", "rows": 3},
                    {"name": "collab_session_3", "label": "Session 3 — Validation", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "tools",
                "title": "Tools",
                "fields": [
                    {"name": "tool_coding", "label": "Coding", "type": "text", "placeholder": "Excel · Notion · NVivo"},
                    {"name": "tool_collab", "label": "Collaboration", "type": "text", "placeholder": "Miro · Mural"},
                    {"name": "tool_docs", "label": "Documentation", "type": "text"},
                ],
            },
            {
                "id": "deliverables",
                "title": "Deliverables",
                "fields": [
                    {"name": "d_codebook", "label": "Codebook (final)", "type": "checkbox"},
                    {"name": "d_thematic_map", "label": "Thematic map", "type": "checkbox"},
                    {"name": "d_findings_doc", "label": "Key findings document", "type": "checkbox"},
                    {"name": "d_insights", "label": "Insights and recommendations", "type": "checkbox"},
                    {"name": "d_evidence", "label": "Evidence repository", "type": "checkbox"},
                    {"name": "d_audit_trail", "label": "Analysis audit trail", "type": "checkbox"},
                    {"name": "d_report", "label": "Final report (per UXR-008)", "type": "checkbox"},
                ],
            },
            {
                "id": "success",
                "title": "Success criteria",
                "fields": [
                    {"name": "sc_questions", "label": "All research questions answered with evidence", "type": "checkbox"},
                    {"name": "sc_validated", "label": "Findings validated and defensible", "type": "checkbox"},
                    {"name": "sc_meaningful", "label": "Insights are meaningful and actionable", "type": "checkbox"},
                    {"name": "sc_prioritized", "label": "Recommendations are specific and prioritized", "type": "checkbox"},
                    {"name": "sc_documented", "label": "Analysis process is documented", "type": "checkbox"},
                    {"name": "sc_ontime", "label": "Deliverables completed on time", "type": "checkbox"},
                ],
            },
            {
                "id": "risks",
                "title": "Risks & mitigation",
                "blurb": "One risk per line: risk · mitigation.",
                "fields": [
                    {"name": "risks", "type": "textarea", "rows": 4},
                ],
            },
        ],
    },
    "UXR-007-template-5.2": {
        "title": "Affinity Mapping Facilitation Guide",
        "intro": "Prep sheet for running a collaborative affinity mapping session. Fill it in once before the session so you can run it without thinking.",
        "sections": [
            {
                "id": "header",
                "title": "Session details",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "session_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "facilitator", "label": "Facilitator", "type": "text", "autofill": "project.owner"},
                    {"name": "scribe", "label": "Scribe", "type": "text"},
                    {"name": "participants", "label": "Participants", "type": "text"},
                ],
            },
            {
                "id": "materials",
                "title": "Materials",
                "fields": [
                    {"name": "m_stickies", "label": "Sticky notes (3–4 colors)", "type": "checkbox"},
                    {"name": "m_sharpies", "label": "Sharpies (1 per person)", "type": "checkbox"},
                    {"name": "m_wall", "label": "Large wall space or digital board ready", "type": "checkbox"},
                    {"name": "m_notes", "label": "Printed session notes available", "type": "checkbox"},
                    {"name": "m_timer", "label": "Timer", "type": "checkbox"},
                    {"name": "m_snacks", "label": "Snacks and water", "type": "checkbox"},
                    {"name": "m_camera", "label": "Camera for documentation", "type": "checkbox"},
                ],
            },
            {
                "id": "room",
                "title": "Room setup",
                "fields": [
                    {"name": "r_wall", "label": "Wall space cleared", "type": "checkbox"},
                    {"name": "r_tables", "label": "Tables for writing", "type": "checkbox"},
                    {"name": "r_notes", "label": "Notes accessible", "type": "checkbox"},
                    {"name": "r_breaks", "label": "Breaks planned", "type": "checkbox"},
                ],
            },
            {
                "id": "schedule",
                "title": "Schedule",
                "blurb": "Standard times — adjust to your session length.",
                "fields": [
                    {"name": "intro_min", "label": "Introduction", "type": "text", "placeholder": "5 min"},
                    {"name": "data_review_min", "label": "Data review", "type": "text", "placeholder": "10 min"},
                    {"name": "capture_min", "label": "Observation capture", "type": "text", "placeholder": "45–60 min"},
                    {"name": "silent_posting_min", "label": "Silent posting", "type": "text", "placeholder": "15 min"},
                    {"name": "break_min", "label": "Break", "type": "text", "placeholder": "10 min"},
                    {"name": "silent_grouping_min", "label": "Silent grouping", "type": "text", "placeholder": "30–45 min"},
                    {"name": "labeling_min", "label": "Group discussion & labeling", "type": "text", "placeholder": "45–60 min"},
                    {"name": "refinement_min", "label": "Refinement", "type": "text", "placeholder": "20–30 min"},
                    {"name": "docs_min", "label": "Documentation", "type": "text", "placeholder": "15 min"},
                    {"name": "closing_min", "label": "Closing", "type": "text", "placeholder": "5 min"},
                ],
            },
            {
                "id": "groundrules",
                "title": "Ground rules to communicate",
                "fields": [
                    {"name": "groundrules", "type": "textarea", "rows": 6, "placeholder": "One observation per sticky note · use participant quotes when possible · stay grounded in data · silent grouping before discussion · anyone can move any note · no judgment — all observations are valid"},
                ],
            },
            {
                "id": "voting",
                "title": "Optional dot voting",
                "fields": [
                    {"name": "voting_enabled", "label": "Include dot voting for priority themes", "type": "checkbox"},
                    {"name": "dots_per_person", "label": "Dots per person", "type": "text", "placeholder": "3"},
                ],
            },
            {
                "id": "post",
                "title": "Post-session tasks",
                "fields": [
                    {"name": "post_photos", "label": "Transfer photos to project folder", "type": "checkbox"},
                    {"name": "post_digital", "label": "Document themes in digital format", "type": "checkbox"},
                    {"name": "post_distribute", "label": "Distribute notes to team", "type": "checkbox"},
                    {"name": "post_followup", "label": "Schedule follow-up if needed", "type": "checkbox"},
                    {"name": "post_thanks", "label": "Thank participants", "type": "checkbox"},
                ],
            },
            {
                "id": "outcome",
                "title": "Outcome notes",
                "fields": [
                    {"name": "themes_identified", "label": "Themes identified (one per line)", "type": "textarea", "rows": 5},
                    {"name": "key_takeaways", "label": "Key takeaways from the session", "type": "textarea", "rows": 4},
                    {"name": "questions_raised", "label": "Questions raised for further analysis", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
    "UXR-007-template-5.3": {
        "title": "Theme Development Worksheet",
        "multi_instance": True,
        "instance_singular": "theme",
        "instance_plural": "themes",
        "intro": "One worksheet per theme. Use this to develop, validate, and document each theme before turning it into a finding or insight.",
        "sections": [
            {
                "id": "header",
                "title": "Theme header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "theme_number", "label": "Theme #", "type": "text"},
                    {"name": "analyst", "label": "Analyst", "type": "text", "autofill": "project.owner"},
                    {"name": "theme_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "working_name", "label": "Working theme name", "type": "text"},
                ],
            },
            {
                "id": "codes",
                "title": "Codes & patterns",
                "fields": [
                    {"name": "codes_included", "label": "Codes included (one per line: name · # instances)", "type": "textarea", "rows": 6},
                    {"name": "total_segments", "label": "Total coded segments", "type": "text"},
                    {"name": "patterns", "label": "Patterns represented (per pattern: name · description · frequency)", "type": "textarea", "rows": 6},
                ],
            },
            {
                "id": "statement",
                "title": "Theme statement",
                "blurb": "One or two sentences capturing what this theme is about.",
                "fields": [
                    {"name": "theme_statement", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "evidence",
                "title": "Supporting evidence",
                "fields": [
                    {"name": "prevalence_seen_in", "label": "Seen in (count)", "type": "text"},
                    {"name": "prevalence_total", "label": "Out of (total)", "type": "text"},
                    {"name": "quote_1", "label": "Quote 1", "type": "textarea", "rows": 2},
                    {"name": "quote_1_context", "label": "Context (participant + session)", "type": "text"},
                    {"name": "quote_2", "label": "Quote 2", "type": "textarea", "rows": 2},
                    {"name": "quote_2_context", "label": "Context", "type": "text"},
                    {"name": "quote_3", "label": "Quote 3", "type": "textarea", "rows": 2},
                    {"name": "quote_3_context", "label": "Context", "type": "text"},
                    {"name": "quote_4", "label": "Quote 4", "type": "textarea", "rows": 2},
                    {"name": "quote_4_context", "label": "Context", "type": "text"},
                    {"name": "quote_5", "label": "Quote 5", "type": "textarea", "rows": 2},
                    {"name": "quote_5_context", "label": "Context", "type": "text"},
                    {"name": "behavioral_evidence", "label": "Behavioral evidence (one per line, with participant)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "narrative",
                "title": "Narrative description",
                "blurb": "2–4 paragraphs telling the story of this theme.",
                "fields": [
                    {"name": "narrative_what", "label": "What is happening?", "type": "textarea", "rows": 4},
                    {"name": "narrative_why", "label": "Why is it happening? What drives this?", "type": "textarea", "rows": 4},
                    {"name": "narrative_impact", "label": "What does it mean for users? Impact?", "type": "textarea", "rows": 4},
                    {"name": "narrative_nuances", "label": "Nuances, variations, context", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "variations",
                "title": "Variations",
                "fields": [
                    {"name": "variations_segments", "label": "How does this theme appear across segments?", "type": "textarea", "rows": 3},
                    {"name": "variations_contexts", "label": "How does it vary across contexts?", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "negative",
                "title": "Contradictory / negative evidence",
                "fields": [
                    {"name": "contradictions", "label": "Data that doesn't fit this theme", "type": "textarea", "rows": 4},
                    {
                        "name": "how_addressed",
                        "label": "How addressed",
                        "type": "radio",
                        "options": [
                            {"value": "refine", "label": "Refine theme to accommodate"},
                            {"value": "boundary", "label": "Note as boundary condition"},
                            {"value": "sub_theme", "label": "Identify as separate sub-theme"},
                        ],
                    },
                ],
            },
            {
                "id": "relationships",
                "title": "Relationship to other themes",
                "fields": [
                    {"name": "relationships", "type": "textarea", "rows": 4, "placeholder": "Related to Theme X — nature of relationship\nContrasts with Theme Y — how they differ\nMay cause Theme Z — causal relationship"},
                ],
            },
            {
                "id": "insight_dev",
                "title": "Insight development",
                "blurb": "Move from observation to interpretation to insight.",
                "fields": [
                    {"name": "observation_level", "label": "Observation (what we observed — factual)", "type": "textarea", "rows": 3},
                    {"name": "interpretation", "label": "Interpretation (what it means — why)", "type": "textarea", "rows": 3},
                    {"name": "insight", "label": "Insight (higher-level understanding — 'this tells us that…')", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "implications",
                "title": "Implications",
                "fields": [
                    {"name": "user_impact", "label": "User impact", "type": "textarea", "rows": 3},
                    {"name": "business_impact", "label": "Business impact", "type": "textarea", "rows": 3},
                    {"name": "design_implications", "label": "Design implications", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "recommendations",
                "title": "Preliminary recommendations",
                "fields": [
                    {"name": "recommendations", "type": "textarea", "rows": 5, "placeholder": "Recommendation · priority (high/med/low) · rationale\n— one per line —"},
                ],
            },
            {
                "id": "confidence",
                "title": "Confidence assessment",
                "fields": [
                    {
                        "name": "evidence_strength",
                        "label": "Strength of evidence",
                        "type": "radio",
                        "options": [
                            {"value": "strong", "label": "Strong — consistent across majority; clear pattern"},
                            {"value": "moderate", "label": "Moderate — present in substantial portion; some variation"},
                            {"value": "emerging", "label": "Emerging — present but needs more data"},
                            {"value": "weak", "label": "Weak — limited evidence; tentative"},
                        ],
                    },
                    {
                        "name": "internal_coherence",
                        "label": "Internal coherence",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "High — theme is clear and distinct"},
                            {"value": "medium", "label": "Medium — identifiable but some overlap"},
                            {"value": "low", "label": "Low — theme needs refinement"},
                        ],
                    },
                    {
                        "name": "external_validity",
                        "label": "External validity",
                        "type": "radio",
                        "options": [
                            {"value": "generalizable", "label": "Likely generalizable"},
                            {"value": "context", "label": "Context-specific"},
                            {"value": "unknown", "label": "Unknown — need more data or different methods"},
                        ],
                    },
                ],
            },
            {
                "id": "validation",
                "title": "Validation checklist",
                "fields": [
                    {"name": "v_distinct", "label": "Theme is distinct from other themes", "type": "checkbox"},
                    {"name": "v_coherent", "label": "Theme is internally coherent", "type": "checkbox"},
                    {"name": "v_grounded", "label": "Theme is grounded in data with examples", "type": "checkbox"},
                    {"name": "v_addresses_rq", "label": "Theme addresses research questions", "type": "checkbox"},
                    {"name": "v_meaningful", "label": "Theme is meaningful (not obvious or trivial)", "type": "checkbox"},
                    {"name": "v_negative", "label": "Negative cases considered", "type": "checkbox"},
                    {"name": "v_variations", "label": "Variations across segments noted", "type": "checkbox"},
                    {"name": "v_relationships", "label": "Relationship to other themes identified", "type": "checkbox"},
                ],
            },
            {
                "id": "notes",
                "title": "Notes / questions",
                "fields": [
                    {"name": "notes", "type": "textarea", "rows": 4},
                ],
            },
        ],
    },
    "UXR-007-template-5.4": {
        "title": "Finding Validation Checklist",
        "multi_instance": True,
        "instance_singular": "finding",
        "instance_plural": "findings",
        "intro": "One per finding. Validate before reporting — make sure each finding will survive a skeptical stakeholder.",
        "sections": [
            {
                "id": "header",
                "title": "Finding header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "finding_number", "label": "Finding #", "type": "text"},
                    {"name": "validator", "label": "Validator", "type": "text", "autofill": "project.owner"},
                    {"name": "validation_date", "label": "Date", "type": "date", "autofill": "today"},
                ],
            },
            {
                "id": "statement",
                "title": "Finding statement",
                "fields": [
                    {"name": "finding_statement", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "strength",
                "title": "Evidence strength",
                "fields": [
                    {"name": "prevalence_count", "label": "How many participants/sessions showed this pattern (N)", "type": "text"},
                    {"name": "prevalence_total", "label": "Out of (total)", "type": "text"},
                    {
                        "name": "frequency_assessment",
                        "label": "Frequency assessment",
                        "type": "radio",
                        "options": [
                            {"value": "strong", "label": "Strong (>75% of participants)"},
                            {"value": "moderate", "label": "Moderate (50–75%)"},
                            {"value": "emerging", "label": "Emerging (25–50%)"},
                            {"value": "weak", "label": "Weak (<25%)"},
                        ],
                    },
                    {
                        "name": "consistency",
                        "label": "Consistency",
                        "type": "radio",
                        "options": [
                            {"value": "very", "label": "Very consistent — expressed similarly by all"},
                            {"value": "mostly", "label": "Mostly consistent — core similarity, some variation"},
                            {"value": "moderate", "label": "Moderate — recognizable pattern with variation"},
                            {"value": "inconsistent", "label": "Inconsistent — widely varied expressions"},
                        ],
                    },
                    {
                        "name": "intensity",
                        "label": "Intensity / impact",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "High — strongly emphasized; clearly important"},
                            {"value": "medium", "label": "Medium — notable but not primary focus"},
                            {"value": "low", "label": "Low — mentioned but not emphasized"},
                        ],
                    },
                    {"name": "intensity_evidence", "label": "Evidence of intensity (emotional response, time discussing, unsolicited mentions)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "quality",
                "title": "Evidence quality",
                "fields": [
                    {"name": "q_quotes", "label": "Have at least 3 verbatim quotes supporting this", "type": "checkbox"},
                    {"name": "q_behavioral", "label": "Have behavioral observations supporting this", "type": "checkbox"},
                    {"name": "q_contextual", "label": "Have contextual data explaining this pattern", "type": "checkbox"},
                    {"name": "q_multi_source", "label": "Multiple data sources support this (notes + transcript + observation)", "type": "checkbox"},
                    {"name": "q_context", "label": "Context preserved in interpretation", "type": "checkbox"},
                    {"name": "q_conditions", "label": "Conditions under which this occurs are documented", "type": "checkbox"},
                    {"name": "q_why", "label": "Understand why this pattern exists (not just that it does)", "type": "checkbox"},
                ],
            },
            {
                "id": "validity",
                "title": "Validity checks",
                "fields": [
                    {"name": "negative_searched", "label": "Actively searched for counter-examples", "type": "checkbox"},
                    {
                        "name": "contradictions_found",
                        "label": "Contradictions found?",
                        "type": "radio",
                        "options": [
                            {"value": "none", "label": "None found"},
                            {"value": "minor", "label": "Minor — do not invalidate finding"},
                            {"value": "significant", "label": "Significant — finding needs revision"},
                        ],
                    },
                    {"name": "contradiction_detail", "label": "Description of contradictory evidence (if any)", "type": "textarea", "rows": 3},
                    {
                        "name": "bias_direction",
                        "label": "Confirmation bias check",
                        "type": "radio",
                        "options": [
                            {"value": "contradicts", "label": "Contradicts my expectations (less bias risk)"},
                            {"value": "confirms", "label": "Confirms my expectations (examined extra carefully)"},
                        ],
                    },
                    {"name": "alternative", "label": "Alternative interpretation considered", "type": "textarea", "rows": 3},
                    {"name": "preferred_rationale", "label": "Why primary interpretation is preferred", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "alignment",
                "title": "Research question alignment",
                "fields": [
                    {
                        "name": "relevance",
                        "label": "Relevance",
                        "type": "radio",
                        "options": [
                            {"value": "primary", "label": "Directly addresses primary research question"},
                            {"value": "secondary", "label": "Addresses secondary research question"},
                            {"value": "tangential", "label": "Tangential — document but deprioritize"},
                            {"value": "off_topic", "label": "Off-topic — exclude from primary findings"},
                        ],
                    },
                    {"name": "rq_specified", "label": "Which research question", "type": "text"},
                ],
            },
            {
                "id": "actionability",
                "title": "Actionability",
                "fields": [
                    {
                        "name": "clarity",
                        "label": "Clarity",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — clear what we learned"},
                            {"value": "somewhat", "label": "Somewhat — needs clarification"},
                            {"value": "no", "label": "No — too vague or ambiguous"},
                        ],
                    },
                    {"name": "clarification_needed", "label": "If unclear, what needs clarification", "type": "textarea", "rows": 2},
                    {
                        "name": "meaningfulness",
                        "label": "Meaningfulness",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — reveals something new and important"},
                            {"value": "somewhat", "label": "Somewhat — some value but limited novelty"},
                            {"value": "no", "label": "No — states the obvious"},
                        ],
                    },
                    {"name": "why_matters", "label": "Why this matters", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "defensibility",
                "title": "Defensibility",
                "fields": [
                    {
                        "name": "traceability",
                        "label": "Traceability",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — have specific quotes and observations"},
                            {"value": "partial", "label": "Partially — some evidence but gaps"},
                            {"value": "no", "label": "No — would struggle to defend"},
                        ],
                    },
                    {"name": "evidence_location", "label": "Evidence location (link or reference)", "type": "text"},
                    {"name": "challenge_quotes", "label": "Can show multiple quotes supporting it", "type": "checkbox"},
                    {"name": "challenge_examples", "label": "Can explain the pattern with specific examples", "type": "checkbox"},
                    {"name": "challenge_consistency", "label": "Can demonstrate consistency across participants", "type": "checkbox"},
                    {"name": "challenge_contradictions", "label": "Can explain contradictory data and why finding still holds", "type": "checkbox"},
                ],
            },
            {
                "id": "overall",
                "title": "Overall validation",
                "fields": [
                    {
                        "name": "strength",
                        "label": "Strength of finding",
                        "type": "radio",
                        "options": [
                            {"value": "strong", "label": "Strong — well-supported, consistent, validated"},
                            {"value": "moderate", "label": "Moderate — supported but some limitations"},
                            {"value": "weak", "label": "Weak — limited support or significant issues"},
                        ],
                    },
                    {
                        "name": "confidence",
                        "label": "Confidence level",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "High — ready to communicate"},
                            {"value": "medium", "label": "Medium — communicate with caveats"},
                            {"value": "low", "label": "Low — needs more work or more data"},
                        ],
                    },
                    {
                        "name": "ready",
                        "label": "Ready to report",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — validated and ready"},
                            {"value": "revisions", "label": "With revisions"},
                            {"value": "no", "label": "No — more work needed"},
                        ],
                    },
                ],
            },
            {
                "id": "summary",
                "title": "Validation summary",
                "fields": [
                    {"name": "strengths", "label": "Strengths of this finding (one per line)", "type": "textarea", "rows": 4},
                    {"name": "limitations", "label": "Limitations to note", "type": "textarea", "rows": 4},
                    {"name": "caveats", "label": "Caveats for reporting", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "actions",
                "title": "Actions required",
                "fields": [
                    {"name": "a_validated", "label": "No action — finding validated", "type": "checkbox"},
                    {"name": "a_refine", "label": "Refine finding statement", "type": "checkbox"},
                    {"name": "a_evidence", "label": "Gather additional supporting evidence", "type": "checkbox"},
                    {"name": "a_negative", "label": "Conduct negative case analysis", "type": "checkbox"},
                    {"name": "a_discuss", "label": "Discuss with team", "type": "checkbox"},
                    {"name": "a_revisit", "label": "Revisit interpretation", "type": "checkbox"},
                    {"name": "a_flag", "label": "Flag as low confidence and note limitations", "type": "checkbox"},
                    {"name": "action_notes", "label": "Action notes", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
    "UXR-007-template-5.5": {
        "title": "Insight Development",
        "multi_instance": True,
        "instance_singular": "insight",
        "instance_plural": "insights",
        "intro": "One worksheet per insight. Move from observation up the pyramid to recommendation — and pressure-test that each insight is genuinely explanatory.",
        "sections": [
            {
                "id": "header",
                "title": "Insight header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "insight_number", "label": "Insight #", "type": "text"},
                    {"name": "analyst", "label": "Analyst", "type": "text", "autofill": "project.owner"},
                    {"name": "insight_date", "label": "Date", "type": "date", "autofill": "today"},
                ],
            },
            {
                "id": "statement",
                "title": "Insight statement",
                "blurb": "One clear sentence capturing the insight.",
                "fields": [
                    {"name": "insight_statement", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "pyramid",
                "title": "The analysis pyramid",
                "blurb": "From observation up to recommendation.",
                "fields": [
                    {"name": "observations", "label": "Observations (what we saw / heard — one per line)", "type": "textarea", "rows": 4},
                    {"name": "findings", "label": "Findings (pattern from analysis · prevalence · supporting quotes)", "type": "textarea", "rows": 5},
                    {"name": "insight_interpretation", "label": "Insight (interpretive explanation)", "type": "textarea", "rows": 4},
                    {"name": "recommendation_ref", "label": "Recommendation (developed separately — reference)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "components",
                "title": "Insight components",
                "fields": [
                    {"name": "what_happening", "label": "What is happening", "type": "textarea", "rows": 3},
                    {"name": "why_happening", "label": "Why it's happening (root causes, motivations, context)", "type": "textarea", "rows": 3},
                    {"name": "why_matters", "label": "Why it matters (impact on users, business, product)", "type": "textarea", "rows": 3},
                    {"name": "what_means", "label": "What it means (implications and opportunities)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "evidence",
                "title": "Supporting evidence",
                "fields": [
                    {"name": "themes_supporting", "label": "Themes/patterns supporting this insight (one per line with key evidence)", "type": "textarea", "rows": 5},
                    {"name": "quote_1", "label": "Strongest quote", "type": "textarea", "rows": 2},
                    {"name": "quote_1_context", "label": "Context (participant + why it matters)", "type": "text"},
                    {"name": "quote_2", "label": "Quote 2", "type": "textarea", "rows": 2},
                    {"name": "quote_2_context", "label": "Context", "type": "text"},
                    {"name": "quote_3", "label": "Quote 3", "type": "textarea", "rows": 2},
                    {"name": "quote_3_context", "label": "Context", "type": "text"},
                    {"name": "behavioral_evidence", "label": "Behavioral evidence", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "quality",
                "title": "Insight quality checks",
                "fields": [
                    {
                        "name": "explanatory",
                        "label": "Explanatory — does this explain WHY?",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — explains underlying reasons"},
                            {"value": "no", "label": "No — only describes WHAT"},
                        ],
                    },
                    {
                        "name": "non_obvious",
                        "label": "Non-obvious — is this revealing something new?",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — new understanding"},
                            {"value": "somewhat", "label": "Somewhat — confirms with new depth"},
                            {"value": "no", "label": "No — states the obvious"},
                        ],
                    },
                    {
                        "name": "actionable",
                        "label": "Actionable — does this suggest direction?",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — clear implications for action"},
                            {"value": "somewhat", "label": "Somewhat — general direction"},
                            {"value": "no", "label": "No — interesting but not actionable"},
                        ],
                    },
                    {
                        "name": "evidence_based",
                        "label": "Evidence-based — grounded in data?",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — multiple data points"},
                            {"value": "somewhat", "label": "Somewhat — some evidence but limited"},
                            {"value": "no", "label": "No — speculation"},
                        ],
                    },
                    {
                        "name": "connected",
                        "label": "Connected — links multiple data points?",
                        "type": "radio",
                        "options": [
                            {"value": "yes", "label": "Yes — synthesizes across themes/participants"},
                            {"value": "somewhat", "label": "Somewhat — limited connection"},
                            {"value": "no", "label": "No — single observation"},
                        ],
                    },
                ],
            },
            {
                "id": "stakeholders",
                "title": "Stakeholder relevance",
                "fields": [
                    {"name": "primary_stakeholder", "label": "Primary stakeholder (role)", "type": "text", "autofill": "project.stakeholder"},
                    {"name": "primary_why", "label": "Why they care", "type": "textarea", "rows": 2},
                    {"name": "secondary_stakeholders", "label": "Secondary stakeholders", "type": "text"},
                    {"name": "secondary_why", "label": "Why they care", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "implications",
                "title": "Implications",
                "fields": [
                    {"name": "ux_implications", "label": "User experience implications", "type": "textarea", "rows": 3},
                    {"name": "product_implications", "label": "Product implications", "type": "textarea", "rows": 3},
                    {"name": "business_implications", "label": "Business implications", "type": "textarea", "rows": 3},
                    {"name": "design_implications", "label": "Design implications", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "confidence",
                "title": "Confidence assessment",
                "fields": [
                    {
                        "name": "evidence_quality",
                        "label": "Evidence quality",
                        "type": "radio",
                        "options": [
                            {"value": "strong", "label": "Strong"},
                            {"value": "moderate", "label": "Moderate"},
                            {"value": "weak", "label": "Weak"},
                        ],
                    },
                    {
                        "name": "interpretive_confidence",
                        "label": "Interpretive confidence",
                        "type": "radio",
                        "options": [
                            {"value": "high", "label": "High"},
                            {"value": "medium", "label": "Medium"},
                            {"value": "low", "label": "Low"},
                        ],
                    },
                    {
                        "name": "generalizability",
                        "label": "Generalizability",
                        "type": "radio",
                        "options": [
                            {"value": "likely", "label": "Likely"},
                            {"value": "context", "label": "Context-specific"},
                            {"value": "unknown", "label": "Unknown"},
                        ],
                    },
                    {"name": "limitations", "label": "Limitations (boundaries, where it might not apply, what would increase confidence)", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "opportunities",
                "title": "Opportunities suggested",
                "blurb": "One per line: description · type (quick win / strategic / innovation) · potential impact · complexity.",
                "fields": [
                    {"name": "opportunities", "type": "textarea", "rows": 5},
                ],
            },
            {
                "id": "risks",
                "title": "Risks if unaddressed",
                "fields": [
                    {"name": "short_term_risks", "label": "Short-term risks", "type": "textarea", "rows": 3},
                    {"name": "long_term_risks", "label": "Long-term risks", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "related",
                "title": "Related insights",
                "fields": [
                    {"name": "complementary", "label": "Complementary insights (add dimension)", "type": "textarea", "rows": 2},
                    {"name": "contrasting", "label": "Contrasting insights (tension or different perspective)", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "communication",
                "title": "How to communicate this insight",
                "fields": [
                    {"name": "key_message", "label": "Key message (one sentence for executive summary)", "type": "textarea", "rows": 2},
                    {"name": "story_to_tell", "label": "Story to tell (narrative form)", "type": "textarea", "rows": 4},
                    {"name": "visual_opportunity", "label": "Visual opportunity (journey map, diagram, etc.)", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "validation",
                "title": "Validation",
                "fields": [
                    {"name": "peer_reviewer", "label": "Peer reviewer", "type": "text"},
                    {"name": "peer_review_date", "label": "Peer review date", "type": "date"},
                    {"name": "peer_feedback", "label": "Peer feedback incorporated", "type": "checkbox"},
                    {"name": "stakeholder_preview", "label": "Stakeholder previewed with", "type": "text"},
                    {"name": "stakeholder_preview_date", "label": "Stakeholder preview date", "type": "date"},
                    {"name": "stakeholder_resonated", "label": "Resonated with stakeholder", "type": "checkbox"},
                    {"name": "stakeholder_feedback", "label": "Stakeholder feedback summary", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "next",
                "title": "Next steps",
                "fields": [
                    {"name": "ns_recommendation", "label": "Develop into recommendation(s)", "type": "checkbox"},
                    {"name": "ns_visuals", "label": "Create supporting visuals", "type": "checkbox"},
                    {"name": "ns_report", "label": "Include in research report", "type": "checkbox"},
                    {"name": "ns_deepdive", "label": "Schedule deep-dive with stakeholder", "type": "checkbox"},
                    {"name": "ns_more_evidence", "label": "Gather additional evidence if needed", "type": "checkbox"},
                    {"name": "next_notes", "label": "Notes", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
    "UXR-006-template-5.3": {
        "title": "Contextual Inquiry Field Notes",
        "multi_instance": True,
        "instance_singular": "visit",
        "instance_plural": "visits",
        "intro": "One entry per site visit. Capture the environment, the workflow, and the artifacts as you see them — then refine after you leave.",
        "sections": [
            {
                "id": "header",
                "title": "Visit header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "session_number", "label": "Session #", "type": "text"},
                    {"name": "participant_id", "label": "Participant ID", "type": "text"},
                    {"name": "visit_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "location", "label": "Location", "type": "text", "placeholder": "Acme Industrial — Dayton plant, line 3"},
                    {"name": "activity", "label": "Activity observed", "type": "text"},
                    {"name": "start_time", "label": "Start", "type": "text", "placeholder": "08:30"},
                    {"name": "end_time", "label": "End", "type": "text", "placeholder": "11:00"},
                    {"name": "observer", "label": "Observer", "type": "text", "autofill": "project.owner"},
                ],
            },
            {
                "id": "pre_observation",
                "title": "Pre-observation interview",
                "fields": [
                    {"name": "pre_planned_work", "label": "What are you planning to work on today?", "type": "textarea", "rows": 2},
                    {"name": "pre_typical", "label": "Is this a typical day/shift?", "type": "textarea", "rows": 2},
                    {"name": "pre_goals", "label": "What are your main goals?", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "environment",
                "title": "Environmental context",
                "fields": [
                    {"name": "physical_setting", "label": "Physical setting (space type, layout, lighting, noise, people)", "type": "textarea", "rows": 4},
                    {"name": "tools_artifacts_visible", "label": "Tools & artifacts visible (physical, digital, info sources)", "type": "textarea", "rows": 4},
                    {"name": "workspace_organization", "label": "Workspace organization (sketch description)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "observation_log",
                "title": "Observation log",
                "blurb": "Chronological notes. One line per moment: time · activity · tools used · context/observations.",
                "fields": [
                    {"name": "observation_log", "type": "textarea", "rows": 14},
                ],
            },
            {
                "id": "workflow",
                "title": "Workflow diagram",
                "blurb": "Steps in sequence, decision points, branches.",
                "fields": [
                    {"name": "workflow", "type": "textarea", "rows": 6},
                ],
            },
            {
                "id": "artifacts",
                "title": "Artifacts captured",
                "blurb": "One artifact per block: name, type, content, how it's used, significance.",
                "fields": [
                    {"name": "artifacts", "type": "textarea", "rows": 8},
                ],
            },
            {
                "id": "questions_during",
                "title": "Questions asked during observation",
                "fields": [
                    {"name": "questions_during", "type": "textarea", "rows": 6, "placeholder": "Q: What are you doing now? / A: ...\nQ: Why did you do it that way? / A: ..."},
                ],
            },
            {
                "id": "debrief",
                "title": "Debrief interview",
                "fields": [
                    {"name": "d_typical", "label": "Was today typical? Anything different?", "type": "textarea", "rows": 2},
                    {"name": "d_challenging", "label": "What parts of what I observed are most challenging?", "type": "textarea", "rows": 3},
                    {"name": "d_works_well", "label": "What works well in your current process?", "type": "textarea", "rows": 3},
                    {"name": "d_change", "label": "If you could change anything, what?", "type": "textarea", "rows": 3},
                    {"name": "d_missed", "label": "What did I miss? What else should I know?", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "insights",
                "title": "Key insights & patterns",
                "fields": [
                    {"name": "pain_points", "label": "Pain points observed (one per line)", "type": "textarea", "rows": 4},
                    {"name": "workarounds", "label": "Workarounds & adaptations", "type": "textarea", "rows": 4},
                    {"name": "information_flow", "label": "Information flow (how info moves through the process)", "type": "textarea", "rows": 3},
                    {"name": "collaboration_points", "label": "Collaboration points (when/why participant interacted with others)", "type": "textarea", "rows": 3},
                    {"name": "efficiency", "label": "Efficiency & inefficiency (what works, what creates friction)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "reflections",
                "title": "Observer reflections",
                "fields": [
                    {"name": "surprises", "label": "Surprises", "type": "textarea", "rows": 3},
                    {"name": "connections", "label": "Connections to other sessions", "type": "textarea", "rows": 3},
                    {"name": "future_questions", "label": "Questions for future exploration", "type": "textarea", "rows": 3},
                    {"name": "design_implications", "label": "Design implications", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "post_session",
                "title": "Post-visit tasks",
                "fields": [
                    {"name": "ps_photos", "label": "Photos organized and labeled", "type": "checkbox"},
                    {"name": "ps_artifacts", "label": "Artifacts documented", "type": "checkbox"},
                    {"name": "ps_diagram", "label": "Workflow diagram created", "type": "checkbox"},
                    {"name": "ps_shared", "label": "Key insights shared with team", "type": "checkbox"},
                    {"name": "ps_digital", "label": "Field notes transferred to digital format", "type": "checkbox"},
                    {"name": "ps_followups", "label": "Follow-up questions noted", "type": "checkbox"},
                ],
            },
        ],
    },
    "UXR-006-template-5.4": {
        "title": "Post-Session Summary",
        "multi_instance": True,
        "instance_singular": "summary",
        "instance_plural": "summaries",
        "intro": "Complete within one hour of session end while details are fresh. Optimized for synthesis later — focus on the most important takeaways and the verbatim quotes that capture them.",
        "sections": [
            {
                "id": "header",
                "title": "Session header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "session_number", "label": "Session #", "type": "text"},
                    {"name": "participant_id", "label": "Participant ID", "type": "text"},
                    {"name": "session_date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "completed_by", "label": "Completed by", "type": "text", "autofill": "project.owner"},
                    {"name": "completed_time", "label": "Completed at", "type": "text", "placeholder": "11:45 (within 1 hr of session end)"},
                ],
            },
            {
                "id": "overview",
                "title": "Session overview",
                "fields": [
                    {"name": "duration_planned", "label": "Planned duration", "type": "text"},
                    {"name": "duration_actual", "label": "Actual duration", "type": "text"},
                    {
                        "name": "method",
                        "label": "Method",
                        "type": "radio",
                        "options": [
                            {"value": "interview", "label": "Interview"},
                            {"value": "usability", "label": "Usability test"},
                            {"value": "contextual", "label": "Contextual inquiry"},
                            {"value": "other", "label": "Other"},
                        ],
                    },
                    {"name": "moderator", "label": "Moderator", "type": "text", "autofill": "project.owner"},
                    {
                        "name": "location",
                        "label": "Location",
                        "type": "radio",
                        "options": [
                            {"value": "in_person", "label": "In-person"},
                            {"value": "remote", "label": "Remote"},
                        ],
                    },
                    {
                        "name": "quality",
                        "label": "Session quality",
                        "type": "radio",
                        "options": [
                            {"value": "excellent", "label": "Excellent"},
                            {"value": "good", "label": "Good"},
                            {"value": "fair", "label": "Fair"},
                            {"value": "poor", "label": "Poor"},
                        ],
                    },
                    {"name": "quality_notes", "label": "Notes on session quality", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "findings",
                "title": "Key findings",
                "blurb": "3–5 main takeaways. Lead each with the insight, then 1–2 sentences of context.",
                "fields": [
                    {"name": "finding_1", "label": "Finding 1", "type": "textarea", "rows": 3},
                    {"name": "finding_2", "label": "Finding 2", "type": "textarea", "rows": 3},
                    {"name": "finding_3", "label": "Finding 3", "type": "textarea", "rows": 3},
                    {"name": "finding_4", "label": "Finding 4 (optional)", "type": "textarea", "rows": 3},
                    {"name": "finding_5", "label": "Finding 5 (optional)", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "quotes",
                "title": "Notable quotes",
                "blurb": "Verbatim — capture what participants actually said.",
                "fields": [
                    {"name": "quote_1", "label": "Quote 1", "type": "textarea", "rows": 2},
                    {"name": "quote_1_context", "label": "Context", "type": "text"},
                    {"name": "quote_2", "label": "Quote 2", "type": "textarea", "rows": 2},
                    {"name": "quote_2_context", "label": "Context", "type": "text"},
                    {"name": "quote_3", "label": "Quote 3", "type": "textarea", "rows": 2},
                    {"name": "quote_3_context", "label": "Context", "type": "text"},
                    {"name": "quote_4", "label": "Quote 4", "type": "textarea", "rows": 2},
                    {"name": "quote_4_context", "label": "Context", "type": "text"},
                    {"name": "quote_5", "label": "Quote 5", "type": "textarea", "rows": 2},
                    {"name": "quote_5_context", "label": "Context", "type": "text"},
                ],
            },
            {
                "id": "surprises",
                "title": "Surprises & unexpected insights",
                "fields": [
                    {"name": "surprised", "label": "What surprised us", "type": "textarea", "rows": 3},
                    {"name": "contradicted", "label": "What contradicted our expectations", "type": "textarea", "rows": 3},
                    {"name": "unexpected_learn", "label": "What we didn't expect to learn", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "patterns",
                "title": "Patterns & connections",
                "fields": [
                    {"name": "relates_to", "label": "How this session relates to others", "type": "textarea", "rows": 3},
                    {"name": "patterns_confirmed", "label": "Patterns confirmed or strengthened", "type": "textarea", "rows": 3},
                    {"name": "patterns_new", "label": "New patterns emerging", "type": "textarea", "rows": 3},
                    {"name": "variations", "label": "Variations from previous sessions", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "behavioral",
                "title": "Behavioral observations",
                "fields": [
                    {"name": "key_behaviors", "label": "Key behaviors observed", "type": "textarea", "rows": 3},
                    {"name": "emotional", "label": "Emotional responses", "type": "textarea", "rows": 3},
                    {"name": "reactions", "label": "Notable reactions", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "context",
                "title": "Participant context",
                "fields": [
                    {"name": "background", "label": "Relevant background that affects interpretation", "type": "textarea", "rows": 3},
                    {"name": "circumstances", "label": "Unique circumstances to note", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "followups",
                "title": "Follow-up questions",
                "fields": [
                    {"name": "followup_raised", "label": "Questions this session raised", "type": "textarea", "rows": 3},
                    {"name": "followup_probe", "label": "Areas to probe more deeply", "type": "textarea", "rows": 3},
                    {"name": "followup_clarify", "label": "Clarifications needed", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "method_notes",
                "title": "Methodological notes",
                "fields": [
                    {"name": "worked", "label": "What worked well", "type": "textarea", "rows": 3},
                    {"name": "didnt_work", "label": "What didn't work well", "type": "textarea", "rows": 3},
                    {"name": "guide_adjustments", "label": "Suggested adjustments to guide", "type": "textarea", "rows": 3},
                    {"name": "timing_notes", "label": "Timing notes (sections long/short)", "type": "textarea", "rows": 2},
                    {"name": "technical_issues", "label": "Technical issues", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "implications",
                "title": "Implications",
                "fields": [
                    {"name": "immediate", "label": "Immediate implications", "type": "textarea", "rows": 3},
                    {"name": "product_impact", "label": "Potential impact on design / product", "type": "textarea", "rows": 3},
                    {"name": "deeper", "label": "Areas needing deeper exploration", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "next_steps",
                "title": "Next steps",
                "fields": [
                    {"name": "research_actions", "label": "Research actions (one per line)", "type": "textarea", "rows": 3},
                    {"name": "comm_actions", "label": "Communication actions", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "team",
                "title": "Research team notes",
                "fields": [
                    {"name": "team_notes", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "links",
                "title": "Document links",
                "fields": [
                    {"name": "session_notes_link", "label": "Detailed session notes", "type": "text"},
                    {"name": "recording_link", "label": "Recording", "type": "text"},
                    {"name": "transcript_link", "label": "Transcript", "type": "text"},
                    {"name": "photos_link", "label": "Photos / artifacts folder", "type": "text"},
                ],
            },
        ],
    },
    "UXR-006-template-5.5": {
        "title": "Research Journal Entry",
        "multi_instance": True,
        "instance_singular": "entry",
        "instance_plural": "entries",
        "intro": "Periodic check-in during fieldwork — what patterns are emerging, what's surprising you, what hypotheses you're building. Add an entry every few sessions or whenever your thinking shifts.",
        "sections": [
            {
                "id": "header",
                "title": "Entry header",
                "fields": [
                    {"name": "study_name", "label": "Study", "type": "text", "autofill": "project.name"},
                    {"name": "entry_date", "label": "Entry date", "type": "date", "autofill": "today"},
                    {"name": "sessions_to_date", "label": "Sessions completed to date", "type": "text"},
                    {"name": "entry_by", "label": "Journal entry by", "type": "text", "autofill": "project.owner"},
                    {"name": "sessions_covered", "label": "Sessions covered (IDs or date range)", "type": "text"},
                ],
            },
            {
                "id": "patterns",
                "title": "Patterns emerging across sessions",
                "fields": [
                    {"name": "strong_patterns", "label": "Strong patterns (seen in most/all sessions). Per pattern: evidence, strength, implications.", "type": "textarea", "rows": 6},
                    {"name": "emerging_patterns", "label": "Emerging patterns (seen in some sessions). Per pattern: evidence, confidence, what would confirm.", "type": "textarea", "rows": 6},
                    {"name": "variations", "label": "Variations between participants — what varies, what explains it, hypothesis why", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "hypotheses",
                "title": "Working hypotheses",
                "blurb": "Per hypothesis: evidence for, evidence against, confidence (high/medium/low), how to test.",
                "fields": [
                    {"name": "hypothesis_1", "label": "Hypothesis 1", "type": "textarea", "rows": 5},
                    {"name": "hypothesis_2", "label": "Hypothesis 2", "type": "textarea", "rows": 5},
                    {"name": "hypothesis_3", "label": "Hypothesis 3 (optional)", "type": "textarea", "rows": 5},
                ],
            },
            {
                "id": "reflexivity",
                "title": "Reflexivity & bias check",
                "fields": [
                    {"name": "expected_find", "label": "What I expected to find", "type": "textarea", "rows": 3},
                    {"name": "actually_finding", "label": "What I'm actually finding", "type": "textarea", "rows": 3},
                    {"name": "assumptions_challenged", "label": "Assumptions being challenged", "type": "textarea", "rows": 3},
                    {"name": "potential_biases", "label": "Potential biases in my interpretation", "type": "textarea", "rows": 3},
                    {"name": "perspective_check", "label": "Areas where I need to check my perspective", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "surprises",
                "title": "Surprises & novel insights",
                "fields": [
                    {"name": "surprised_me", "label": "What has surprised me (one per line)", "type": "textarea", "rows": 4},
                    {"name": "emerging_unexpected", "label": "What I didn't expect but is emerging", "type": "textarea", "rows": 4},
                    {"name": "questions_should_have_asked", "label": "Questions I didn't know to ask but should have", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "theme_quotes",
                "title": "Quotes that capture key themes",
                "fields": [
                    {"name": "theme_quotes", "label": "Theme · quote · participant. Group by theme.", "type": "textarea", "rows": 8},
                ],
            },
            {
                "id": "methodology",
                "title": "Methodological reflections",
                "fields": [
                    {"name": "working", "label": "What's working well", "type": "textarea", "rows": 3},
                    {"name": "not_working", "label": "What's not working", "type": "textarea", "rows": 3},
                    {"name": "adjustments", "label": "Adjustments made (date · what · why)", "type": "textarea", "rows": 4},
                    {"name": "guide_improvements", "label": "Guide / protocol improvements", "type": "textarea", "rows": 3},
                    {"name": "things_to_change", "label": "Things to do differently", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "questions",
                "title": "Questions & areas for deeper exploration",
                "fields": [
                    {"name": "questions_remaining", "label": "Questions remaining (one per line)", "type": "textarea", "rows": 4},
                    {"name": "questions_emerging", "label": "New questions emerging", "type": "textarea", "rows": 4},
                    {"name": "areas_more_depth", "label": "Areas needing more depth in remaining sessions", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "connections",
                "title": "Connections to existing knowledge",
                "fields": [
                    {"name": "prior_research", "label": "How findings relate to prior research", "type": "textarea", "rows": 3},
                    {"name": "other_studies", "label": "How findings relate to other studies we've done", "type": "textarea", "rows": 3},
                    {"name": "frameworks", "label": "Theories or frameworks that seem relevant", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "themes",
                "title": "Emerging themes & preliminary framework",
                "fields": [
                    {"name": "major_themes", "label": "Major themes (name · definition · evidence · sub-themes)", "type": "textarea", "rows": 8},
                    {"name": "organizing_framework", "label": "Potential organizing framework — how themes relate", "type": "textarea", "rows": 4},
                ],
            },
            {
                "id": "implications",
                "title": "Implications taking shape",
                "fields": [
                    {"name": "design_implications", "label": "Design implications", "type": "textarea", "rows": 3},
                    {"name": "product_implications", "label": "Product implications", "type": "textarea", "rows": 3},
                    {"name": "strategic_implications", "label": "Strategic implications", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "confidence",
                "title": "Confidence assessment",
                "fields": [
                    {"name": "confident_about", "label": "What I'm confident about", "type": "textarea", "rows": 3},
                    {"name": "uncertain_about", "label": "What I'm uncertain about", "type": "textarea", "rows": 3},
                    {"name": "need_more_data", "label": "What I need more data on", "type": "textarea", "rows": 3},
                    {"name": "saturation_estimate", "label": "When I think we'll reach saturation", "type": "text"},
                ],
            },
            {
                "id": "next_steps",
                "title": "Next steps",
                "fields": [
                    {"name": "remaining_sessions", "label": "For remaining sessions (one per line)", "type": "textarea", "rows": 3},
                    {"name": "analysis_tasks", "label": "For analysis", "type": "textarea", "rows": 3},
                    {"name": "team_actions", "label": "For team", "type": "textarea", "rows": 3},
                ],
            },
            {
                "id": "team_discussion",
                "title": "Team discussion points",
                "fields": [
                    {"name": "discussion_items", "label": "Items to discuss with team", "type": "textarea", "rows": 4},
                    {"name": "team_questions", "label": "Questions for team", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
    "UXR-003-template-5.4": {
        "title": "Recruitment Outreach Email",
        "intro": "Fill in the variables once; the Word export generates three ready-to-send email versions (cold-professional, warm-customer, reminder) with your values substituted.",
        "sections": [
            {
                "id": "header",
                "title": "Variables",
                "blurb": "These are the placeholders that get substituted across all three email versions.",
                "fields": [
                    {"name": "recipient_name", "label": "Recipient name", "type": "text", "placeholder": "Sarah"},
                    {"name": "researcher_name", "label": "Researcher (your name)", "type": "text", "autofill": "project.owner"},
                    {"name": "researcher_title", "label": "Researcher title", "type": "text", "placeholder": "UX Researcher"},
                    {"name": "company", "label": "Company", "type": "text"},
                    {"name": "topic", "label": "Research topic", "type": "text", "placeholder": "industrial inventory workflows"},
                    {"name": "challenge", "label": "Specific challenge (cold version)", "type": "text", "placeholder": "managing parts across multiple warehouses"},
                    {"name": "product", "label": "Product name (warm version)", "type": "text"},
                    {"name": "area", "label": "Specific area of interest (warm version)", "type": "text"},
                    {"name": "duration", "label": "Session duration", "type": "text", "placeholder": "30-minute"},
                    {"name": "incentive", "label": "Incentive", "type": "text", "placeholder": "$75 Amazon gift card"},
                    {"name": "date_range", "label": "Date range for sessions", "type": "text", "placeholder": "May 20–June 5"},
                    {"name": "screener_link", "label": "Screener link", "type": "text"},
                    {"name": "contact_email", "label": "Contact email", "type": "text"},
                    {"name": "days_since", "label": "Days since first email (reminder version)", "type": "text", "placeholder": "5"},
                ],
            },
        ],
    },
    "UXR-005-template-5.1": {
        "title": "Generative Interview Guide",
        "intro": "Build your interview script section by section. Fields autosave to the project. Export to Word for a printable guide you can take into sessions.",
        "sections": [
            {
                "id": "header",
                "title": "Study details",
                "fields": [
                    {"name": "study_name", "label": "Study name", "type": "text", "autofill": "project.name"},
                    {"name": "date", "label": "Date", "type": "date", "autofill": "today"},
                    {"name": "researcher", "label": "Researcher", "type": "text", "autofill": "project.owner"},
                    {"name": "document_id", "label": "Document ID", "type": "text"},
                    {"name": "version", "label": "Version", "type": "text", "placeholder": "1.0"},
                ],
            },
            {
                "id": "overview",
                "title": "Session overview",
                "fields": [
                    {"name": "purpose", "label": "Purpose", "type": "textarea", "rows": 3, "placeholder": "What this study aims to learn"},
                    {"name": "duration", "label": "Duration (minutes)", "type": "text", "placeholder": "60"},
                    {
                        "name": "format",
                        "label": "Session format",
                        "type": "radio",
                        "options": [
                            {"value": "remote", "label": "Remote"},
                            {"value": "in_person", "label": "In-person"},
                        ],
                    },
                    {"name": "rec_audio", "label": "Recording: Audio", "type": "checkbox"},
                    {"name": "rec_video", "label": "Recording: Video", "type": "checkbox"},
                    {"name": "rec_screen", "label": "Recording: Screen share", "type": "checkbox"},
                ],
            },
            {
                "id": "research_questions",
                "title": "Research questions",
                "blurb": "The questions your analysis will answer (these are different from your interview questions).",
                "fields": [
                    {"name": "rq_1", "label": "Research question 1", "type": "textarea", "rows": 2},
                    {"name": "rq_2", "label": "Research question 2", "type": "textarea", "rows": 2},
                    {"name": "rq_3", "label": "Research question 3", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "warmup",
                "title": "Warm-up (≈5 min)",
                "blurb": "Quick rapport-building questions before the real conversation.",
                "fields": [
                    {"name": "warmup_q1", "label": "Warm-up question 1", "type": "textarea", "rows": 2, "placeholder": "Can you tell me about your current role?"},
                    {"name": "warmup_q2", "label": "Warm-up question 2", "type": "textarea", "rows": 2, "placeholder": "What does a typical day look like for you?"},
                ],
            },
            {
                "id": "topic1",
                "title": "Topic area 1",
                "fields": [
                    {"name": "t1_name", "label": "Topic name", "type": "text"},
                    {"name": "t1_duration", "label": "Time (min)", "type": "text", "placeholder": "15"},
                    {"name": "t1_goal", "label": "What you want to learn (moderator goal)", "type": "textarea", "rows": 2},
                    {"name": "t1_q1", "label": "Question 1 (opening, narrative)", "type": "textarea", "rows": 2},
                    {"name": "t1_q2", "label": "Question 2", "type": "textarea", "rows": 2},
                    {"name": "t1_q3", "label": "Question 3", "type": "textarea", "rows": 2},
                    {"name": "t1_q4", "label": "Question 4 (if time permits)", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "topic2",
                "title": "Topic area 2",
                "fields": [
                    {"name": "t2_name", "label": "Topic name", "type": "text"},
                    {"name": "t2_duration", "label": "Time (min)", "type": "text", "placeholder": "15"},
                    {"name": "t2_goal", "label": "What you want to learn", "type": "textarea", "rows": 2},
                    {"name": "t2_q1", "label": "Question 1", "type": "textarea", "rows": 2},
                    {"name": "t2_q2", "label": "Question 2", "type": "textarea", "rows": 2},
                    {"name": "t2_q3", "label": "Question 3", "type": "textarea", "rows": 2},
                ],
            },
            {
                "id": "closing",
                "title": "Closing (≈5 min)",
                "fields": [
                    {"name": "closing_q1", "label": "Final wrap-up question", "type": "textarea", "rows": 2, "placeholder": "Anything important we didn't discuss?"},
                    {"name": "closing_q2", "label": "Anything you'd like to ask me?", "type": "textarea", "rows": 2},
                    {"name": "incentive", "label": "Incentive details (for closing script)", "type": "text"},
                ],
            },
            {
                "id": "notes",
                "title": "Moderator notes",
                "fields": [
                    {"name": "key_reminders", "label": "Key reminders to yourself", "type": "textarea", "rows": 3},
                    {"name": "sensitive_topics", "label": "Sensitive areas to navigate carefully", "type": "textarea", "rows": 2},
                ],
            },
        ],
    },
    "UXR-003-template-5.2": {
        "title": "Screener",
        "intro": "Design your participant screener. Export to Word for a clean spec you can drop into Typeform, Qualtrics, or Google Forms.",
        "sections": [
            {
                "id": "header",
                "title": "Study details",
                "fields": [
                    {"name": "study_name", "label": "Study name", "type": "text", "autofill": "project.name"},
                    {"name": "company", "label": "Company name (for intro)", "type": "text"},
                    {"name": "general_topic", "label": "General topic (don't reveal specifics)", "type": "text", "placeholder": "e.g. how teams plan inventory"},
                    {"name": "duration_minutes", "label": "Screener takes (min)", "type": "text", "placeholder": "5"},
                    {"name": "incentive", "label": "Incentive", "type": "text", "placeholder": "$75 Amazon gift card"},
                ],
            },
            {
                "id": "disqualifiers",
                "title": "Disqualification industries",
                "blurb": "Industries that signal a professional respondent or competitor employee.",
                "fields": [
                    {"name": "dq_industry_1", "label": "Industry 1", "type": "text", "placeholder": "Market research"},
                    {"name": "dq_industry_2", "label": "Industry 2", "type": "text", "placeholder": "Advertising / PR"},
                    {"name": "dq_industry_3", "label": "Industry 3", "type": "text", "placeholder": "UX design / user research"},
                    {"name": "dq_industry_4", "label": "Industry 4 (competitor)", "type": "text"},
                    {"name": "past_studies_threshold", "label": "Disqualify if participated in more than N studies in past 6 months", "type": "text", "placeholder": "3"},
                ],
            },
            {
                "id": "primary_criteria",
                "title": "Primary criteria",
                "blurb": "Must-have qualifications. Each question identifies who continues vs. who's thanked.",
                "fields": [
                    {"name": "pc_q1", "label": "Primary criterion 1 — question", "type": "textarea", "rows": 2, "placeholder": "How often do you use [system X] in your work?"},
                    {"name": "pc_q1_pass", "label": "Passing answers (continues)", "type": "text", "placeholder": "Daily, Several times a week, Weekly"},
                    {"name": "pc_q2", "label": "Primary criterion 2 — question", "type": "textarea", "rows": 2},
                    {"name": "pc_q2_pass", "label": "Passing answers", "type": "text"},
                    {"name": "pc_q3", "label": "Primary criterion 3 — question", "type": "textarea", "rows": 2},
                    {"name": "pc_q3_pass", "label": "Passing answers", "type": "text"},
                ],
            },
            {
                "id": "quotas",
                "title": "Quota / secondary criteria",
                "blurb": "Nice-to-have qualifications to ensure sample diversity.",
                "fields": [
                    {"name": "quota_q1", "label": "Quota dimension", "type": "text", "placeholder": "Company size"},
                    {"name": "quota_q1_options", "label": "Options (one per line, with target counts)", "type": "textarea", "rows": 3, "placeholder": "1–50 employees [5]\n51–500 employees [5]\n500+ employees [5]"},
                ],
            },
            {
                "id": "articulation",
                "title": "Articulation check",
                "blurb": "Open-ended question to filter for thoughtfulness (interviews only).",
                "fields": [
                    {"name": "articulation_q", "label": "Articulation question", "type": "textarea", "rows": 3, "placeholder": "In a few sentences, describe [task]. What makes it difficult?"},
                    {"name": "min_chars", "label": "Minimum response length", "type": "text", "placeholder": "50 characters"},
                ],
            },
            {
                "id": "logistics",
                "title": "Logistics",
                "fields": [
                    {"name": "session_type", "label": "Session type", "type": "text", "placeholder": "60-min remote interview"},
                    {"name": "date_range", "label": "Date range available", "type": "text"},
                    {"name": "needs_timezone", "label": "Collect timezone", "type": "checkbox"},
                    {"name": "needs_phone", "label": "Collect phone (optional)", "type": "checkbox"},
                ],
            },
            {
                "id": "messaging",
                "title": "Confirmation messages",
                "fields": [
                    {"name": "qualified_msg", "label": "Message for qualified respondents", "type": "textarea", "rows": 3},
                    {"name": "not_qualified_msg", "label": "Message for not-qualified", "type": "textarea", "rows": 3},
                ],
            },
        ],
    },
}


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
        "template_forms": TEMPLATE_FORMS,
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
  .mobile-header, .sidebar-backdrop { display: none; }
  @media (max-width: 880px) {
    .app { grid-template-columns: 1fr; }
    .sidebar {
      position: fixed !important;
      top: 0; left: 0; bottom: 0;
      width: 280px; max-width: 85vw;
      z-index: 100;
      transform: translateX(-100%);
      transition: transform .25s ease;
      box-shadow: 4px 0 20px rgba(0,0,0,.15);
    }
    .sidebar.open { transform: translateX(0); }
    .sidebar-backdrop {
      position: fixed; inset: 0;
      background: rgba(20,20,20,.4);
      z-index: 99;
      display: block;
      opacity: 0;
      pointer-events: none;
      transition: opacity .2s;
    }
    .sidebar-backdrop.open {
      opacity: 1;
      pointer-events: auto;
    }
    .mobile-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 16px;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      background: var(--bg);
      z-index: 50;
    }
    .hamburger {
      background: transparent;
      border: 1px solid var(--border-strong);
      color: var(--text);
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      display: grid;
      place-items: center;
      min-width: 36px;
      min-height: 36px;
    }
    .mobile-header-title {
      font-family: var(--serif);
      font-size: 15px;
      font-weight: 500;
      flex: 1;
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .main { padding: 18px 16px 64px; }
    .stat-row { flex-wrap: wrap; gap: 16px 24px; padding: 14px 0 18px; margin-bottom: 24px; }
    .stat .n { font-size: 22px; }
    .home-title { font-size: 30px; }
    .sop-title, .ph-title, .phase-title-detail { font-size: 28px; }
    .ph-header { flex-direction: column; gap: 8px; }
    .ph-actions { width: 100%; flex-wrap: wrap; }
    .sop-detail-grid { gap: 24px; }
    .toc { display: none; }
    .attach-head { padding: 12px; gap: 8px; }
    .attach-body { padding: 6px 14px 18px 14px; }
    .tform-section { padding: 16px 18px; }
    .tform-row { grid-template-columns: 1fr; }
    .guide-card { grid-template-columns: 44px 1fr auto; padding: 18px 18px; gap: 16px; }
    .guide-card-num { font-size: 28px; }
    .projects-grid { grid-template-columns: 1fr; }
    .next-action { padding: 16px 18px; gap: 14px; }
    .next-action-icon { width: 38px; height: 38px; font-size: 18px; }
    .next-action-title { font-size: 17px; }
    .ph-phase-grid { grid-template-columns: 1fr 1fr; }
    .artifact-row { flex-wrap: wrap; padding: 12px; gap: 8px; }
    .artifact-row-kind { width: auto; }
    .work-row { flex-wrap: wrap; gap: 8px; }
    .work-row-kind { width: auto; }
    .save-to-project { gap: 8px; }
    .save-status-label { font-size: 11px; }
    .attach-actions { flex-direction: column; align-items: stretch; gap: 10px; }
    .save-to-project { flex-wrap: wrap; }
  }
  @media (max-width: 480px) {
    .ph-phase-grid { grid-template-columns: 1fr; }
    .home-title { font-size: 26px; }
    .pf-form { padding: 22px 18px; }
  }

  /* Save toast (top right) */
  .save-toast {
    position: fixed;
    top: 16px;
    right: 16px;
    background: var(--surface);
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 12.5px;
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    gap: 8px;
    opacity: 0;
    transform: translateY(-6px);
    pointer-events: none;
    transition: opacity .2s, transform .2s;
    z-index: 200;
  }
  .save-toast.show {
    opacity: 1;
    transform: translateY(0);
  }
  .save-toast-dot {
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 50%;
    flex-shrink: 0;
  }

  /* Phase-complete celebration banner */
  .celebrate-toast {
    position: fixed;
    top: 22px;
    right: 22px;
    max-width: 360px;
    background: var(--accent);
    color: var(--surface);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 8px 28px rgba(0,0,0,.18);
    display: flex;
    align-items: center;
    gap: 14px;
    opacity: 0;
    transform: translateY(-12px) scale(.96);
    pointer-events: none;
    transition: opacity .25s, transform .25s;
    z-index: 220;
  }
  html[data-theme="dark"] .celebrate-toast { color: var(--bg); }
  .celebrate-toast.show {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  .celebrate-toast-icon {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: rgba(255,255,255,.18);
    display: grid; place-items: center;
    font-size: 20px;
    flex-shrink: 0;
  }
  html[data-theme="dark"] .celebrate-toast-icon { background: rgba(0,0,0,.18); }
  .celebrate-toast-title {
    font-family: var(--serif);
    font-size: 15px;
    font-weight: 500;
    line-height: 1.2;
  }
  .celebrate-toast-sub {
    font-size: 12.5px;
    opacity: .85;
    margin-top: 3px;
  }
  .celebrate-toast-cta {
    background: rgba(255,255,255,.18);
    border: none;
    color: inherit;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    margin-left: auto;
    flex-shrink: 0;
  }
  html[data-theme="dark"] .celebrate-toast-cta { background: rgba(0,0,0,.18); }
  .celebrate-toast-cta:hover { background: rgba(255,255,255,.28); }
  html[data-theme="dark"] .celebrate-toast-cta:hover { background: rgba(0,0,0,.28); }

  /* Undo toast (medium, has action button) */
  .undo-toast {
    position: fixed;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%) translateY(12px);
    background: var(--text);
    color: var(--surface);
    border-radius: 8px;
    padding: 10px 14px 10px 18px;
    box-shadow: 0 8px 28px rgba(0,0,0,.18);
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 13px;
    opacity: 0;
    pointer-events: none;
    transition: opacity .2s, transform .2s;
    z-index: 210;
  }
  html[data-theme="dark"] .undo-toast { color: var(--bg); }
  .undo-toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
    pointer-events: auto;
  }
  .undo-toast button {
    background: transparent;
    border: 1px solid color-mix(in srgb, var(--surface) 30%, transparent);
    color: var(--surface);
    padding: 4px 12px;
    border-radius: 4px;
    font-family: var(--sans);
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
  }
  html[data-theme="dark"] .undo-toast button { color: var(--bg); border-color: color-mix(in srgb, var(--bg) 30%, transparent); }
  .undo-toast button:hover { background: color-mix(in srgb, var(--surface) 14%, transparent); }

  /* Search result group headers */
  .search-group-header {
    font-family: var(--mono);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .14em;
    color: var(--text-faint);
    font-weight: 600;
    padding: 10px 22px 4px;
    margin-top: 2px;
  }
  .search-group-header:first-child { margin-top: 0; }
  .sr-only {
    position: absolute !important;
    width: 1px; height: 1px;
    padding: 0; margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border: 0;
  }

  /* Welcome banner on project home */
  .welcome-banner {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 16px 20px;
    margin-top: 24px;
    margin-bottom: 8px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
  }
  .welcome-banner-body { flex: 1; }
  .welcome-banner-title {
    font-family: var(--serif);
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 4px;
  }
  .welcome-banner-text {
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.5;
    margin: 0;
  }
  .welcome-banner-dismiss {
    background: transparent;
    border: none;
    color: var(--text-faint);
    cursor: pointer;
    padding: 2px 6px;
    font-size: 16px;
    line-height: 1;
  }
  .welcome-banner-dismiss:hover { color: var(--text); }

  /* Empty-state phase preview on dashboard */
  .phase-preview-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-top: 24px;
    margin-bottom: 8px;
  }
  @media (max-width: 600px) { .phase-preview-row { grid-template-columns: repeat(2, 1fr); } }
  .phase-preview {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 14px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .phase-preview-num {
    width: 26px; height: 26px;
    background: var(--accent-soft);
    color: var(--accent-ink);
    border-radius: 50%;
    display: grid; place-items: center;
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 600;
  }
  html[data-theme="dark"] .phase-preview-num { color: var(--accent); }
  .phase-preview-title {
    font-family: var(--serif);
    font-size: 13.5px;
    font-weight: 500;
    line-height: 1.25;
  }

  /* Phase-grouped artifacts on project home */
  .artifact-group {
    margin-bottom: 16px;
  }
  .artifact-group-header {
    font-family: var(--mono);
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: var(--text-faint);
    margin: 0 0 8px;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .artifact-group-list {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
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

  /* Next-action card on project home */
  .next-action {
    background: var(--accent-soft);
    border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin-bottom: 28px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 18px;
    transition: transform .15s, box-shadow .15s;
  }
  .next-action:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow);
  }
  .next-action-icon {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: var(--accent);
    color: var(--surface);
    display: grid; place-items: center;
    font-family: var(--serif);
    font-size: 22px;
    font-weight: 500;
    flex-shrink: 0;
  }
  html[data-theme="dark"] .next-action-icon { color: var(--bg); }
  .next-action-body { flex: 1; min-width: 0; }
  .next-action-eyebrow {
    font-family: var(--mono);
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: var(--accent-ink);
    margin-bottom: 4px;
    font-weight: 600;
  }
  html[data-theme="dark"] .next-action-eyebrow { color: var(--accent); }
  .next-action-title {
    font-family: var(--serif);
    font-size: 19px;
    font-weight: 500;
    letter-spacing: -.005em;
    color: var(--text);
    line-height: 1.25;
  }
  .next-action-sub {
    font-size: 12.5px;
    color: var(--text-muted);
    margin-top: 4px;
  }
  .next-action-arrow {
    color: var(--accent);
    font-size: 22px;
    flex-shrink: 0;
    transition: transform .15s;
  }
  .next-action:hover .next-action-arrow { transform: translateX(2px); }

  /* "Your work for this phase" section */
  .phase-work {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    margin-bottom: 28px;
  }
  .phase-work-eyebrow {
    font-family: var(--mono);
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: var(--accent);
    margin-bottom: 4px;
    font-weight: 600;
  }
  .phase-work-title {
    font-family: var(--serif);
    font-size: 19px;
    font-weight: 500;
    margin: 0 0 16px;
    letter-spacing: -.005em;
  }
  .phase-work-cta {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: var(--accent-soft);
    border-radius: 8px;
    cursor: pointer;
    color: var(--accent-ink);
    font-size: 13.5px;
    transition: background .15s;
  }
  html[data-theme="dark"] .phase-work-cta { color: var(--accent); }
  .phase-work-cta:hover { background: color-mix(in srgb, var(--accent) 15%, var(--surface)); }
  .phase-work-cta-arrow { margin-left: auto; font-size: 18px; }

  .work-row {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    gap: 14px;
    cursor: pointer;
    transition: padding-left .15s;
  }
  .work-row:hover { padding-left: 6px; }
  .work-row:last-child { border-bottom: none; }
  .work-row-kind {
    font-family: var(--mono);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: var(--text-faint);
    width: 86px;
    flex-shrink: 0;
  }
  .work-row-title { flex: 1; min-width: 0; font-size: 13.5px; }
  .work-row-status {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    flex-shrink: 0;
  }
  .status-not-started { background: var(--surface-2); color: var(--text-muted); }
  .work-row-progress {
    font-size: 11px;
    color: var(--text-faint);
    flex-shrink: 0;
  }
  .work-row-arrow {
    color: var(--text-faint);
    font-size: 14px;
    flex-shrink: 0;
  }
  .work-row:hover .work-row-arrow { color: var(--accent); }
  .phase-work-toggle {
    display: block;
    margin-top: 12px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 12.5px;
    cursor: pointer;
    padding: 0;
  }
  .phase-work-toggle:hover { color: var(--accent-ink); }
  html[data-theme="dark"] .phase-work-toggle:hover { color: var(--accent); }

  /* Back-to-phase link on SOP pages */
  .back-to-phase {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12.5px;
    color: var(--accent-ink);
    background: var(--accent-soft);
    padding: 5px 11px;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 8px;
    border: 1px solid transparent;
    transition: border-color .15s;
  }
  html[data-theme="dark"] .back-to-phase { color: var(--accent); }
  .back-to-phase:hover { border-color: var(--accent); }

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

  /* Active project banner in sidebar */
  .project-banner {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 14px;
    cursor: pointer;
    transition: border-color .15s;
  }
  .project-banner:hover { border-color: var(--border-strong); }
  .project-banner-label {
    font-size: 10px;
    color: var(--text-faint);
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 3px;
    font-weight: 600;
  }
  .project-banner-name {
    font-family: var(--serif);
    font-size: 14px;
    font-weight: 500;
    color: var(--text);
    line-height: 1.2;
    word-wrap: break-word;
  }
  .project-banner-switch {
    font-size: 11px;
    color: var(--text-faint);
    margin-top: 4px;
  }
  .project-banner.empty {
    background: transparent;
    border-style: dashed;
  }
  .project-banner.empty .project-banner-name {
    color: var(--text-muted);
    font-family: var(--sans);
    font-size: 12.5px;
    font-weight: 500;
  }

  /* Projects dashboard */
  .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 14px;
    margin-top: 24px;
  }
  .project-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    cursor: pointer;
    transition: border-color .15s, transform .15s, box-shadow .15s;
    position: relative;
  }
  .project-card:hover {
    border-color: var(--border-strong);
    transform: translateY(-1px);
    box-shadow: var(--shadow);
  }
  .project-card.active {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
  }
  .project-card-active-tag {
    position: absolute;
    top: 14px;
    right: 14px;
    font-family: var(--mono);
    font-size: 10px;
    color: var(--accent);
    letter-spacing: .08em;
    text-transform: uppercase;
    font-weight: 600;
  }
  .project-card-name {
    font-family: var(--serif);
    font-size: 19px;
    font-weight: 500;
    letter-spacing: -.01em;
    margin: 0 0 6px;
    padding-right: 60px;
  }
  .project-card-desc {
    color: var(--text-muted);
    font-size: 13px;
    margin: 0 0 12px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .project-card-meta {
    display: flex;
    gap: 10px;
    font-size: 11.5px;
    color: var(--text-faint);
    margin-bottom: 12px;
  }
  .project-card-progress {
    height: 4px;
    background: var(--surface-2);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 6px;
  }
  .project-card-progress-bar { height: 100%; background: var(--accent); transition: width .25s; }
  .project-card-phase {
    display: flex;
    justify-content: space-between;
    font-size: 11.5px;
    color: var(--text-muted);
  }

  .new-project-card {
    background: var(--surface);
    border: 2px dashed var(--border-strong);
    border-radius: var(--radius);
    padding: 28px;
    cursor: pointer;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    color: var(--text-muted);
    transition: border-color .15s, color .15s, background .15s;
  }
  .new-project-card:hover {
    border-color: var(--accent);
    color: var(--accent-ink);
    background: var(--accent-soft);
  }
  html[data-theme="dark"] .new-project-card:hover { color: var(--accent); }
  .new-project-plus {
    font-size: 32px;
    line-height: 1;
    font-weight: 300;
    font-family: var(--serif);
  }

  /* Project home view */
  .ph-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 24px;
    margin-bottom: 8px;
  }
  .ph-title {
    font-family: var(--serif);
    font-size: 40px;
    font-weight: 500;
    letter-spacing: -.02em;
    line-height: 1.05;
    margin: 0;
  }
  .ph-meta {
    color: var(--text-muted);
    font-size: 14px;
    margin-top: 6px;
  }
  .ph-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
    margin-top: 8px;
  }
  .ph-action-btn {
    background: transparent;
    border: 1px solid var(--border-strong);
    color: var(--text-muted);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12.5px;
    cursor: pointer;
    transition: border-color .15s, color .15s, background .15s;
  }
  .ph-action-btn:hover { border-color: var(--accent); color: var(--accent-ink); background: var(--accent-soft); }
  html[data-theme="dark"] .ph-action-btn:hover { color: var(--accent); }
  .ph-action-primary {
    background: var(--accent);
    color: var(--surface);
    border-color: var(--accent);
  }
  html[data-theme="dark"] .ph-action-primary { color: var(--bg); }
  .ph-action-primary:hover {
    background: color-mix(in srgb, var(--accent) 88%, black);
    color: var(--surface);
    border-color: var(--accent);
  }
  html[data-theme="dark"] .ph-action-primary:hover { color: var(--bg); }

  .ph-section {
    margin-top: 36px;
  }
  .ph-section-title {
    font-family: var(--serif);
    font-size: 20px;
    font-weight: 500;
    margin: 0 0 4px;
    letter-spacing: -.005em;
  }
  .ph-section-sub {
    color: var(--text-muted);
    font-size: 13.5px;
    margin: 0 0 18px;
  }
  .ph-phase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
  }
  .ph-phase-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    cursor: pointer;
    transition: border-color .15s, transform .15s;
  }
  .ph-phase-tile:hover { border-color: var(--border-strong); transform: translateY(-1px); }
  .ph-phase-tile.current { border-color: var(--accent); }
  .ph-phase-tile-num {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    letter-spacing: .08em;
  }
  .ph-phase-tile-title {
    font-family: var(--serif);
    font-size: 15px;
    font-weight: 500;
    margin: 4px 0 8px;
  }
  .ph-phase-tile-bar {
    height: 3px;
    background: var(--surface-2);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 4px;
  }
  .ph-phase-tile-bar > div { height: 100%; background: var(--accent); transition: width .25s; }
  .ph-phase-tile-pct { font-size: 11px; color: var(--text-faint); }

  .artifact-row {
    display: flex;
    align-items: center;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    gap: 14px;
    cursor: pointer;
    transition: background .15s;
  }
  .artifact-row:hover { background: var(--surface-2); }
  .artifact-row:last-child { border-bottom: none; }
  .artifact-row-kind {
    font-family: var(--mono);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: var(--text-faint);
    width: 80px;
    flex-shrink: 0;
  }
  .artifact-row-title { flex: 1; min-width: 0; font-size: 13.5px; }
  .artifact-row-title strong { font-weight: 500; }
  .artifact-row-status {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    flex-shrink: 0;
  }
  /* Status pills — colours meet WCAG AA contrast against their backgrounds */
  .status-todo { background: var(--surface-2); color: var(--text-muted); }
  .status-in-progress { background: #fde68a; color: #78350f; }
  html[data-theme="dark"] .status-in-progress { background: #4d3f1c; color: #fde68a; }
  .status-done { background: var(--accent-soft); color: var(--accent-ink); }
  html[data-theme="dark"] .status-done { color: var(--accent); }
  .artifact-row-date { font-size: 11px; color: var(--text-faint); flex-shrink: 0; }

  /* Create/edit project form */
  .pf-form {
    max-width: 540px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 32px;
    margin-top: 16px;
  }
  .pf-field { margin-bottom: 18px; }
  .pf-field label {
    display: block;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 6px;
    letter-spacing: .01em;
  }
  .pf-field input[type="text"],
  .pf-field input[type="date"],
  .pf-field textarea,
  .pf-field select,
  .form-input {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 8px 11px;
    border-radius: 6px;
    font-size: 14px;
    font-family: var(--sans);
    transition: border-color .15s, box-shadow .15s;
  }
  .pf-field textarea, textarea.form-input {
    resize: vertical;
    min-height: 80px;
    line-height: 1.5;
  }
  .pf-field input:focus, .pf-field textarea:focus, .form-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
  }
  .pf-field .hint { font-size: 11.5px; color: var(--text-faint); margin-top: 4px; }
  .pf-actions {
    display: flex;
    gap: 10px;
    margin-top: 22px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
  }
  .pf-btn-primary {
    background: var(--accent);
    color: var(--surface);
    border: 1px solid var(--accent);
    padding: 8px 18px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
  }
  html[data-theme="dark"] .pf-btn-primary { color: var(--bg); }
  .pf-btn-primary:hover { opacity: .9; }
  .pf-btn-secondary {
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border-strong);
    padding: 8px 18px;
    border-radius: 6px;
    font-size: 13px;
    cursor: pointer;
  }
  .pf-btn-secondary:hover { color: var(--text); border-color: var(--text-muted); }

  /* Save-to-project widget on artifacts */
  .save-to-project {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-right: auto;
  }
  .save-to-project select {
    background: var(--surface);
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12.5px;
    font-family: var(--sans);
  }
  .save-status-label {
    font-size: 11.5px;
    color: var(--text-faint);
  }

  /* Template form view */
  .tform-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin-bottom: 14px;
  }
  .tform-section-title {
    font-family: var(--serif);
    font-size: 17px;
    font-weight: 500;
    margin: 0 0 6px;
    letter-spacing: -.005em;
    display: flex;
    align-items: baseline;
    gap: 10px;
    justify-content: space-between;
  }
  .tform-section-count {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-faint);
    font-weight: 500;
    letter-spacing: .04em;
    flex-shrink: 0;
  }
  .tform-section-count.complete {
    color: var(--accent);
  }
  .tform-section-blurb {
    color: var(--text-muted);
    font-size: 13px;
    margin: 0 0 16px;
  }
  .tform-field { margin-bottom: 14px; }
  .tform-field:last-child { margin-bottom: 0; }
  .tform-field label {
    display: block;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 4px;
  }
  .tform-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
  }
  .tform-radio-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .tform-radio-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13.5px;
    transition: background .15s;
  }
  .tform-radio-option:hover { background: var(--surface-2); }
  .tform-radio-option.selected { background: var(--accent-soft); color: var(--accent-ink); }
  html[data-theme="dark"] .tform-radio-option.selected { color: var(--accent); }
  .tform-checkbox-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13.5px;
    cursor: pointer;
  }
  .tform-intro {
    background: var(--accent-soft);
    border-left: 3px solid var(--accent);
    padding: 14px 18px;
    border-radius: 6px;
    color: var(--accent-ink);
    margin-bottom: 18px;
    font-size: 13.5px;
    line-height: 1.5;
  }
  html[data-theme="dark"] .tform-intro { color: var(--text); }
  .tform-toggle {
    display: flex;
    gap: 6px;
    margin-bottom: 16px;
    font-size: 12px;
  }
  .tform-toggle button {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 5px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-family: var(--sans);
  }
  .tform-toggle button.active {
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent-ink);
  }
  html[data-theme="dark"] .tform-toggle button.active { color: var(--accent); }
  .tform-saved-note {
    font-size: 11.5px;
    color: var(--text-faint);
    margin-left: auto;
    align-self: center;
  }

  /* Multi-instance template UI */
  .instance-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .instance-empty {
    padding: 24px;
    text-align: center;
    background: var(--surface-2);
    border-radius: 8px;
    color: var(--text-muted);
    font-size: 13.5px;
  }
  .instance-card {
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--bg);
    overflow: hidden;
  }
  .instance-head {
    width: 100%;
    background: transparent;
    border: none;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    text-align: left;
    cursor: pointer;
    color: var(--text);
    transition: background .15s;
  }
  .instance-head:hover { background: var(--surface-2); }
  .instance-chev {
    color: var(--text-faint);
    transition: transform .2s;
    flex-shrink: 0;
  }
  .instance-card.open .instance-chev { transform: rotate(90deg); }
  .instance-label-input {
    background: transparent;
    border: none;
    color: var(--text);
    font-family: var(--serif);
    font-size: 15px;
    font-weight: 500;
    padding: 2px 4px;
    border-radius: 4px;
    flex: 1;
    min-width: 0;
  }
  .instance-label-input:hover { background: var(--surface); }
  .instance-label-input:focus { outline: 1px solid var(--accent); background: var(--surface); }
  .instance-meta {
    font-size: 11.5px;
    color: var(--text-faint);
    flex-shrink: 0;
  }
  .instance-status-pill {
    font-size: 10.5px;
    padding: 2px 8px;
    border-radius: 999px;
    flex-shrink: 0;
    font-weight: 500;
  }
  .instance-delete {
    background: transparent;
    border: 1px solid transparent;
    color: var(--text-faint);
    width: 24px; height: 24px;
    border-radius: 4px;
    cursor: pointer;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    transition: background .15s, color .15s, border-color .15s;
  }
  .instance-delete:hover {
    color: #b91c1c;
    border-color: var(--border-strong);
  }
  .instance-body {
    display: none;
    padding: 8px 16px 18px;
    border-top: 1px solid var(--border);
    background: var(--bg);
  }
  .instance-card.open .instance-body { display: block; }
  .instance-actions {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid var(--border);
  }
  .new-instance-btn {
    background: transparent;
    border: 1px dashed var(--border-strong);
    color: var(--text-muted);
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: border-color .15s, color .15s, background .15s;
    align-self: flex-start;
  }
  .new-instance-btn:hover {
    border-color: var(--accent);
    color: var(--accent-ink);
    background: var(--accent-soft);
  }
  html[data-theme="dark"] .new-instance-btn:hover { color: var(--accent); }

  /* Inline fill-in fields (replacing _____ underscore runs) */
  .inline-field {
    background: transparent;
    border: none;
    border-bottom: 1px solid var(--border-strong);
    padding: 1px 4px;
    font: inherit;
    color: var(--text);
    min-width: 80px;
    max-width: 320px;
    margin: 0 1px;
    transition: border-color .15s, background .15s;
  }
  .inline-field:focus {
    outline: none;
    border-bottom-color: var(--accent);
    background: var(--accent-soft);
  }
  html[data-theme="dark"] .inline-field:focus { background: color-mix(in srgb, var(--accent) 18%, var(--surface)); }
  .inline-field:disabled {
    border-bottom-style: dashed;
    color: var(--text-faint);
    background: transparent;
  }

  /* Editable table cells */
  .prose td[contenteditable="true"] {
    cursor: text;
    transition: background .15s, outline .15s;
    min-width: 40px;
  }
  .prose td[contenteditable="true"]:hover {
    background: var(--surface-2);
  }
  .prose td[contenteditable="true"]:focus {
    outline: 2px solid var(--accent);
    outline-offset: -2px;
    background: var(--accent-soft);
  }
  html[data-theme="dark"] .prose td[contenteditable="true"]:focus { background: color-mix(in srgb, var(--accent) 15%, var(--surface)); }

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
<div class="sidebar-backdrop" id="sidebar-backdrop" onclick="closeSidebar()"></div>
<div class="app">
  <header class="mobile-header">
    <button class="hamburger" onclick="openSidebar()" aria-label="Open navigation">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="mobile-header-title" id="mobile-title">SOP Library</div>
    <button class="hamburger" onclick="openSearch()" aria-label="Search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
    </button>
  </header>
  <aside class="sidebar" id="sidebar">
    <div class="brand" onclick="goHome(); closeSidebar();">
      <div class="brand-mark">UX</div>
      <div class="brand-name">SOP Library</div>
    </div>
    <div class="brand-sub">UX Research Operations</div>

    <div id="project-banner-slot"></div>

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

<div class="save-toast" id="save-toast" role="status" aria-live="off"><span class="save-toast-dot"></span><span id="save-toast-text">Saved</span></div>
<div class="celebrate-toast" id="celebrate-toast" role="status">
  <div class="celebrate-toast-icon">✓</div>
  <div>
    <div class="celebrate-toast-title" id="celebrate-toast-title">Phase complete</div>
    <div class="celebrate-toast-sub" id="celebrate-toast-sub"></div>
  </div>
  <button class="celebrate-toast-cta" id="celebrate-toast-cta" onclick="onCelebrateCta()">Open</button>
</div>
<div class="sr-only" id="sr-announcer" aria-live="polite" aria-atomic="true"></div>
<div class="undo-toast" id="undo-toast" role="status">
  <span id="undo-toast-text"></span>
  <button onclick="onUndoClick()" id="undo-toast-button">Undo</button>
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

// Render markdown for an artifact into Word-ready HTML, substituting any
// saved state (checklist state, text fields, table cells).
function markdownBodyHTML(markdown, artifactState) {
  const tmp = document.createElement('div');
  tmp.innerHTML = marked.parse(markdown);

  // 1. Checkboxes → Unicode glyphs honoring saved state
  const checklistState = artifactState?.checklistState;
  if (checklistState) {
    let idx = 0;
    tmp.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      const checked = checklistState[idx] === true;
      idx++;
      cb.outerHTML = checked ? '☑ ' : '☐ ';
    });
  } else {
    tmp.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      cb.outerHTML = cb.hasAttribute('checked') ? '☑ ' : '☐ ';
    });
  }

  // 2. Substitute filled-in text fields (underscore-run placeholders) in order
  const textFields = artifactState?.textFields;
  if (textFields && Object.keys(textFields).some(k => textFields[k])) {
    let fieldIdx = 0;
    const walker = document.createTreeWalker(tmp, NodeFilter.SHOW_TEXT, {
      acceptNode: (node) => {
        let p = node.parentNode;
        while (p && p !== tmp) {
          if (p.tagName && ['PRE', 'CODE', 'TH'].includes(p.tagName)) return NodeFilter.FILTER_REJECT;
          p = p.parentNode;
        }
        return /_{3,}/.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    const nodes = [];
    let n; while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(textNode => {
      textNode.nodeValue = textNode.nodeValue.replace(/_{3,}/g, () => {
        const val = textFields[fieldIdx];
        fieldIdx++;
        return val || '_______________';
      });
    });
  }

  // 3. Substitute filled-in table cells
  const tableCells = artifactState?.tableCells;
  if (tableCells) {
    tmp.querySelectorAll('table').forEach((table, ti) => {
      table.querySelectorAll('tbody tr').forEach((tr, ri) => {
        tr.querySelectorAll('td').forEach((td, ci) => {
          const cellKey = `t${ti}-r${ri}-c${ci}`;
          const saved = tableCells[cellKey];
          if (saved !== undefined && saved !== '') td.textContent = saved;
        });
      });
    });
  }

  let html = tmp.innerHTML;
  // Remove the bullet on task-list items so the box stands alone
  html = html.replace(/<li>(\s*☐|\s*☑)/g, '<li style="list-style:none; margin-left:-18pt;">$1');
  return html;
}

function downloadAsWord(title, sopId, markdown, artifactState) {
  const html = markdownBodyHTML(markdown, artifactState);
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
  saveBlobAsDoc(doc, title);
}

function saveBlobAsDoc(doc, title) {
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
function triggerDownload(key, instanceId) {
  const d = DOWNLOAD_REGISTRY.get(key);
  if (!d) return;
  const schema = DATA.template_forms[key];
  const proj = activeProject();
  let stored = null;
  let instanceLabel = '';
  if (instanceId) {
    const inst = getInstance(key, instanceId);
    if (inst) { stored = inst.data; instanceLabel = inst.label; }
  } else {
    stored = proj?.artifactStatus[key]?.data;
  }
  if (schema && stored && Object.values(stored).some(v => v !== '' && v !== false && v != null)) {
    const merged = {};
    schema.sections.forEach(s => s.fields.forEach(f => {
      const fill = autofillValue(f, proj);
      if (fill) merged[f.name] = fill;
    }));
    Object.assign(merged, stored);
    const titledMeta = {...d, title: instanceLabel ? `${d.title} — ${instanceLabel}` : d.title};
    downloadFilledForm(titledMeta, schema, proj, merged);
  } else {
    const artifactState = proj?.artifactStatus[key];
    const titlePrefix = proj ? proj.name + ' — ' : '';
    downloadAsWord(titlePrefix + d.title, d.sopId, d.markdown, artifactState);
  }
}

// Custom Word renderers for templates whose output is a formatted document
// (not a labelled list of fields).
const CUSTOM_WORD_RENDERERS = {
  'UXR-003-template-5.4': function(meta, schema, proj, data) {
    const v = (k, fallback = '') => (data[k] && String(data[k]).trim()) || fallback;
    const name = v('recipient_name', '[Name]');
    const yourName = v('researcher_name', '[Your name]');
    const title = v('researcher_title', '[Title]');
    const company = v('company', '[Company]');
    const topic = v('topic', '[topic]');
    const challenge = v('challenge', '[specific challenge]');
    const product = v('product', '[Product]');
    const area = v('area', '[specific area]');
    const duration = v('duration', '[duration]');
    const incentive = v('incentive', '[incentive]');
    const dateRange = v('date_range', '[date range]');
    const link = v('screener_link', '[Screener link]');
    const email = v('contact_email', '[email]');
    const daysSince = v('days_since', '[X]');
    const p = s => '<p>' + escapeHtml(s).replace(/\n/g, '<br>') + '</p>';
    return `
      <h2>Cold Outreach — Professional</h2>
      <p><strong>Subject:</strong> Your expertise on ${escapeHtml(topic)} — quick research opportunity</p>
      ${p(`Hi ${name},`)}
      ${p(`I'm ${yourName}, a ${title} at ${company}. We're conducting a study to better understand how professionals handle ${challenge}, and your experience would be incredibly valuable.`)}
      <p><strong>What's involved:</strong></p>
      <ul>
        <li>${escapeHtml(duration)} video conversation</li>
        <li>Discuss your experience with ${escapeHtml(topic)}</li>
        <li>${escapeHtml(incentive)} as a thank-you for your time</li>
      </ul>
      ${p(`Why you: [Brief personalization — their role, company, background]`)}
      ${p(`If you're interested, please complete this 3-minute screener: ${link}`)}
      ${p(`I'm scheduling sessions for ${dateRange}. Happy to answer any questions at ${email}.`)}
      ${p(`Thank you for considering,\n${yourName}\n${title}, ${company}`)}

      <h2 style="margin-top:32pt;">Warm Outreach — Customer</h2>
      <p><strong>Subject:</strong> Help shape the future of ${escapeHtml(product)} — research opportunity</p>
      ${p(`Hi ${name},`)}
      ${p(`I'm reaching out because you're a ${product} user, and we'd love to learn from your experience.`)}
      ${p(`We're conducting research to improve ${area}, and your insights would directly influence what we build next.`)}
      <p><strong>Details:</strong></p>
      <ul>
        <li>${escapeHtml(duration)} video conversation</li>
        <li>Share your workflow and challenges</li>
        <li>${escapeHtml(incentive)} thank-you gift</li>
      </ul>
      ${p(`Interested? Here's a quick screener: ${link}`)}
      ${p(`Feel free to reach out with any questions.`)}
      ${p(`Best,\n${yourName}\n${title}, ${company}`)}

      <h2 style="margin-top:32pt;">Reminder — First</h2>
      <p><strong>Subject:</strong> Quick reminder: research opportunity closing soon</p>
      ${p(`Hi ${name},`)}
      ${p(`Just a friendly reminder about the research opportunity I shared ${daysSince} days ago. We have a few spots remaining for ${dateRange}.`)}
      ${p(`Quick screener: ${link}`)}
      ${p(`Let me know if you have any questions!`)}
      ${p(yourName)}
    `;
  },
};

// Render a filled-form schema into Word-ready HTML body. Accepts an optional
// heading level so sections can demote (h2 → h3) when bundled into a readout.
function formBodyHTML(meta, schema, proj, data, opts) {
  const sectionTag = (opts && opts.sectionTag) || 'h2';
  const custom = CUSTOM_WORD_RENDERERS[Object.keys(DATA.template_forms).find(k => DATA.template_forms[k] === schema)];
  if (custom) return custom(meta, schema, proj, data);
  let body = '';
  schema.sections.forEach(s => {
    if (s.title) body += `<${sectionTag}>${escapeHtml(s.title)}</${sectionTag}>`;
    if (s.blurb) body += `<p style="color:#666;font-style:italic;">${escapeHtml(s.blurb)}</p>`;
    s.fields.forEach(f => {
      const v = data[f.name];
      if (f.type === 'radio') {
        const opt = (f.options || []).find(o => o.value === v);
        const label = opt ? opt.label : '—';
        body += `<p><strong>${escapeHtml(f.label || f.name)}:</strong> ${escapeHtml(label)}</p>`;
      } else if (f.type === 'checkbox') {
        body += `<p>${v === true ? '☑' : '☐'} ${escapeHtml(f.label || f.name)}</p>`;
      } else if (f.type === 'textarea') {
        const display = (v && String(v).trim()) || '—';
        body += `<p><strong>${escapeHtml(f.label || f.name)}:</strong></p><p style="margin-left:12px;">${escapeHtml(display).replace(/\n/g, '<br>')}</p>`;
      } else {
        const display = (v && String(v).trim()) || '—';
        body += `<p><strong>${escapeHtml(f.label || f.name)}:</strong> ${escapeHtml(display)}</p>`;
      }
    });
  });
  return body;
}

function downloadFilledForm(meta, schema, proj, data) {
  const body = formBodyHTML(meta, schema, proj, data);
  const today = new Date().toISOString().slice(0, 10);
  const projName = proj ? proj.name : '';
  const filename = (projName ? projName + ' — ' : '') + meta.title;
  const doc = `<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8"><title>${escapeHtml(filename)}</title>
<style>${WORD_CSS}</style></head>
<body>
<h1>${escapeHtml(schema.title || meta.title)}</h1>
<div class="meta">${projName ? `Project: ${escapeHtml(projName)} · ` : ''}Source: ${escapeHtml(meta.sopId)} · Exported ${today}</div>
${body}
</body></html>`;
  saveBlobAsDoc(doc, filename);
}

const DOWNLOAD_ICON = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>';

// ---- Project readout (one Word doc bundling every saved artifact) ----

function getArtifactMarkdown(key) {
  const m = key.match(/^(UXR-\d{3})-(checklist|template)-(.+)$/);
  if (!m) return null;
  const sop = SOPS[m[1]];
  const list = m[2] === 'checklist' ? sop?.checklists : sop?.templates;
  return list?.find(x => x.section === m[3]);
}

function artifactHasContent(val) {
  if (!val) return false;
  if (val.multi && val.instances) return val.instances.some(i => i.data && Object.values(i.data).some(v => v !== '' && v != null && v !== false));
  return !!(
    (val.data && Object.values(val.data).some(v => v !== '' && v != null && v !== false)) ||
    (val.checklistState && Object.values(val.checklistState).some(v => v === true)) ||
    (val.textFields && Object.values(val.textFields).some(v => v)) ||
    (val.tableCells && Object.values(val.tableCells).some(v => v))
  );
}

function renderInstanceBodyForReadout(key, schema, proj, inst) {
  // Merge autofills under the instance's data
  const merged = {};
  if (schema) {
    schema.sections.forEach(s => s.fields.forEach(f => {
      const fill = autofillValue(f, proj);
      if (fill) merged[f.name] = fill;
    }));
    Object.assign(merged, inst.data || {});
    return formBodyHTML({sopId: '', title: ''}, schema, proj, merged, {sectionTag: 'h4'});
  }
  return '';
}

function renderArtifactSectionForReadout(key, val, proj) {
  const meta = parseArtifactKey(key);
  if (!meta) return '';
  const item = getArtifactMarkdown(key);
  const schema = DATA.template_forms[key];
  const sopId = meta.sopId;
  const title = meta.label || item?.label || `${sopId} ${meta.section}`;

  let body = `
    <h3 style="margin-top:24pt;">${escapeHtml(title)}</h3>
    <p style="color:#999; font-size:10pt; margin-top:0;">${escapeHtml(sopId)} · ${escapeHtml(meta.section)} · ${meta.kind}</p>
  `;

  // Multi-instance: each instance gets its own subsection
  if (val.multi && Array.isArray(val.instances) && val.instances.length) {
    val.instances.forEach(inst => {
      if (!inst.data || !Object.values(inst.data).some(v => v !== '' && v != null && v !== false)) return;
      body += `<h4 style="margin-top:16pt;">${escapeHtml(inst.label || 'Entry')}</h4>`;
      body += renderInstanceBodyForReadout(key, schema, proj, inst);
    });
    return body;
  }

  // Single-instance with form data
  if (schema && val.data && Object.values(val.data).some(v => v !== '' && v != null && v !== false)) {
    const merged = {};
    schema.sections.forEach(s => s.fields.forEach(f => {
      const fill = autofillValue(f, proj);
      if (fill) merged[f.name] = fill;
    }));
    Object.assign(merged, val.data);
    body += formBodyHTML({sopId, title}, schema, proj, merged, {sectionTag: 'h4'});
    return body;
  }

  // Markdown-based artifact with checklist / text / table state
  if (item && (val.checklistState || val.textFields || val.tableCells)) {
    body += markdownBodyHTML(item.content, val);
    return body;
  }

  // Status-only — skip rendering content; surface the status
  body += `<p style="color:#666;">Status: ${escapeHtml((val.status || 'todo').replace('-', ' '))}</p>`;
  return body;
}

function compileProjectReadout() {
  const proj = activeProject();
  if (!proj) { alert('No active project.'); return; }
  const status = proj.artifactStatus || {};
  const haveAny = Object.values(status).some(artifactHasContent);
  if (!haveAny) {
    alert('Nothing to compile yet — fill in a few templates or check off some items first.');
    return;
  }

  // Group artifacts by guide phase (using SOP→phase map)
  const sopToPhase = {};
  DATA.guide_phases.forEach(ph => {
    ph.sops.forEach(s => {
      if (!sopToPhase[s]) sopToPhase[s] = ph;
    });
  });
  const grouped = new Map();
  Object.entries(status).forEach(([key, val]) => {
    if (!artifactHasContent(val)) return;
    const sopMatch = key.match(/^(UXR-\d{3})/);
    const ph = sopMatch ? sopToPhase[sopMatch[1]] : null;
    const groupId = ph ? ph.id : 'other';
    if (!grouped.has(groupId)) grouped.set(groupId, { phase: ph, items: [] });
    grouped.get(groupId).items.push({ key, val, updatedAt: val.updatedAt || '' });
  });
  // Sort items within each group by updatedAt desc
  grouped.forEach(g => g.items.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || '')));

  const today = new Date().toISOString().slice(0, 10);
  const todayDisplay = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });

  // Cover page
  let body = `<div style="text-align:center; padding: 80pt 40pt 60pt;">
    <div style="font-family: 'Cambria',Georgia,serif; font-size: 11pt; color: #666; letter-spacing: 2pt; text-transform: uppercase; margin-bottom: 24pt;">Research Readout</div>
    <h1 style="font-size: 32pt; margin: 0 0 14pt; line-height: 1.1;">${escapeHtml(proj.name)}</h1>
    ${proj.description ? `<p style="font-family: 'Cambria',Georgia,serif; font-size: 13pt; color: #444; max-width: 480pt; margin: 0 auto 28pt;">${escapeHtml(proj.description)}</p>` : ''}
    <table style="margin: 32pt auto 0; border: none; font-size: 11pt; color: #444;">
      ${proj.owner ? `<tr><td style="border:none; padding: 3pt 12pt 3pt 0; color:#888;">Owner</td><td style="border:none;">${escapeHtml(proj.owner)}</td></tr>` : ''}
      ${proj.stakeholder ? `<tr><td style="border:none; padding: 3pt 12pt 3pt 0; color:#888;">Stakeholder</td><td style="border:none;">${escapeHtml(proj.stakeholder)}</td></tr>` : ''}
      <tr><td style="border:none; padding: 3pt 12pt 3pt 0; color:#888;">Generated</td><td style="border:none;">${escapeHtml(todayDisplay)}</td></tr>
      <tr><td style="border:none; padding: 3pt 12pt 3pt 0; color:#888;">Completion</td><td style="border:none;">${projectOverallCompletion(proj)}%</td></tr>
    </table>
  </div>`;

  // Each phase
  DATA.guide_phases.forEach(ph => {
    const group = grouped.get(ph.id);
    if (!group || !group.items.length) return;
    body += `<div style="page-break-before: always;"></div>`;
    body += `<div style="font-family: 'Cambria',Georgia,serif; font-size: 10pt; color: #888; letter-spacing: 2pt; text-transform: uppercase; margin-bottom: 4pt;">Phase ${ph.number} of ${DATA.guide_phases.length}</div>`;
    body += `<h1 style="font-size: 26pt; margin: 0 0 6pt;">${escapeHtml(ph.title)}</h1>`;
    body += `<p style="color: #666; font-size: 12pt; margin: 0 0 18pt;">${escapeHtml(ph.blurb)}</p>`;
    group.items.forEach(({key, val}) => {
      body += renderArtifactSectionForReadout(key, val, proj);
    });
  });

  // Other artifacts (no phase membership)
  const other = grouped.get('other');
  if (other && other.items.length) {
    body += `<div style="page-break-before: always;"></div>`;
    body += `<h1 style="font-size: 26pt;">Additional artifacts</h1>`;
    other.items.forEach(({key, val}) => {
      body += renderArtifactSectionForReadout(key, val, proj);
    });
  }

  const filename = `${proj.name} — Project Readout — ${today}`;
  const doc = `<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8"><title>${escapeHtml(filename)}</title>
<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->
<style>${WORD_CSS}
  h3 { font-family: 'Cambria',Georgia,serif; font-size: 16pt; font-weight: 500; margin: 22pt 0 4pt; border-top: 1pt solid #ddd; padding-top: 14pt; }
  h4 { font-family: 'Cambria',Georgia,serif; font-size: 13pt; font-weight: 500; margin: 16pt 0 6pt; text-transform: none; letter-spacing: 0; color: #333; }
</style></head>
<body>${body}</body></html>`;
  saveBlobAsDoc(doc, filename);
}

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

// ---- Mobile sidebar drawer ----
function openSidebar() {
  document.getElementById('sidebar').classList.add('open');
  document.getElementById('sidebar-backdrop').classList.add('open');
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebar-backdrop').classList.remove('open');
}
// Close drawer after any nav click in the sidebar
document.addEventListener('click', (e) => {
  const onMobile = window.matchMedia('(max-width: 880px)').matches;
  if (!onMobile) return;
  const target = e.target.closest('.nav-link, .nav-phase-link, .mode-toggle button, .search-btn');
  if (target && target.closest('.sidebar')) {
    setTimeout(closeSidebar, 80);
  }
});

// ---- Save toast / a11y announcer ----
let _saveToastTimer = null;
function showSaveToast(text) {
  const t = document.getElementById('save-toast');
  if (!t) return;
  document.getElementById('save-toast-text').textContent = text || 'Saved';
  t.classList.add('show');
  clearTimeout(_saveToastTimer);
  _saveToastTimer = setTimeout(() => t.classList.remove('show'), 1800);
  const a = document.getElementById('sr-announcer');
  if (a) a.textContent = text || 'Saved';
}

let _celebrateRoute = null;
let _celebrateTimer = null;
function showPhaseComplete(completedPhase, nextPhase) {
  const t = document.getElementById('celebrate-toast');
  if (!t) return;
  const title = `Phase ${completedPhase.number}: ${completedPhase.title} complete`;
  const sub = nextPhase ? `Next up — Phase ${nextPhase.number}: ${nextPhase.title}` : 'You finished the project guide.';
  document.getElementById('celebrate-toast-title').textContent = title;
  document.getElementById('celebrate-toast-sub').textContent = sub;
  const cta = document.getElementById('celebrate-toast-cta');
  if (nextPhase) {
    cta.style.display = '';
    cta.textContent = `Open Phase ${nextPhase.number} →`;
    _celebrateRoute = `guide/${nextPhase.id}`;
  } else {
    cta.style.display = 'none';
    _celebrateRoute = null;
  }
  t.classList.add('show');
  clearTimeout(_celebrateTimer);
  _celebrateTimer = setTimeout(() => t.classList.remove('show'), 5000);
  const a = document.getElementById('sr-announcer');
  if (a) a.textContent = title + (nextPhase ? '. ' + sub : '');
}
function onCelebrateCta() {
  if (_celebrateRoute) {
    route(_celebrateRoute);
    document.getElementById('celebrate-toast').classList.remove('show');
  }
}

// ---- Undo-toast for soft delete ----
let _undoPending = null;
let _undoTimer = null;
function showUndoToast(message, undoFn) {
  const t = document.getElementById('undo-toast');
  document.getElementById('undo-toast-text').textContent = message;
  _undoPending = undoFn;
  t.classList.add('show');
  clearTimeout(_undoTimer);
  _undoTimer = setTimeout(() => {
    t.classList.remove('show');
    _undoPending = null;
  }, 8000);
  const a = document.getElementById('sr-announcer');
  if (a) a.textContent = message + ' — undo available for 8 seconds';
}
function onUndoClick() {
  if (_undoPending) {
    _undoPending();
    _undoPending = null;
  }
  document.getElementById('undo-toast').classList.remove('show');
  clearTimeout(_undoTimer);
}

// ---- Project state model ----
const PROJECTS_KEY = 'sop-projects-v1';
const LEGACY_CHECKLIST_KEY = 'sop-guide-checklist-state';

function loadProjectsState() {
  try {
    return JSON.parse(localStorage.getItem(PROJECTS_KEY) || '{"projects":[],"activeId":null}');
  } catch { return {projects:[], activeId:null}; }
}
function saveProjectsState(state) {
  localStorage.setItem(PROJECTS_KEY, JSON.stringify(state));
}
function createProject({name, description, owner, stakeholder}) {
  const now = new Date().toISOString();
  return {
    id: 'p-' + Math.random().toString(36).slice(2, 10),
    name: name || 'Untitled project',
    description: description || '',
    owner: owner || '',
    stakeholder: stakeholder || '',
    currentPhase: 'phase-1',
    createdAt: now,
    updatedAt: now,
    phaseChecks: {},
    artifactStatus: {},
  };
}
function activeProject() {
  const state = loadProjectsState();
  if (!state.activeId) return null;
  return state.projects.find(p => p.id === state.activeId) || null;
}
function setActiveProject(id) {
  const state = loadProjectsState();
  state.activeId = id;
  saveProjectsState(state);
}
function updateActiveProject(mutate) {
  const state = loadProjectsState();
  const p = state.projects.find(x => x.id === state.activeId);
  if (!p) return;
  mutate(p);
  p.updatedAt = new Date().toISOString();
  saveProjectsState(state);
}
function getArtifactState(key) {
  const p = activeProject();
  return (p && p.artifactStatus[key]) || null;
}
function setArtifactStatus(key, patch) {
  updateActiveProject(p => {
    const cur = p.artifactStatus[key] || {};
    p.artifactStatus[key] = {...cur, ...patch, updatedAt: new Date().toISOString()};
  });
}
function setArtifactData(key, data) {
  updateActiveProject(p => {
    const cur = p.artifactStatus[key] || {status: 'in-progress'};
    p.artifactStatus[key] = {...cur, data, status: cur.status === 'done' ? 'done' : 'in-progress', updatedAt: new Date().toISOString()};
  });
}

// ---- Multi-instance artifact helpers ----
function isMultiInstance(key) {
  return !!(DATA.template_forms[key] && DATA.template_forms[key].multi_instance);
}
function ensureMultiContainer(p, key) {
  let a = p.artifactStatus[key];
  if (a && a.multi) return a;
  if (a && !a.multi && (a.data || a.status)) {
    // Migrate the legacy single-instance into the first instance
    a = p.artifactStatus[key] = {
      multi: true,
      instances: [{
        id: 'i-' + Math.random().toString(36).slice(2, 8),
        label: 'Session 1',
        status: a.status || 'in-progress',
        data: a.data || {},
        updatedAt: a.updatedAt || new Date().toISOString(),
      }],
    };
    return a;
  }
  a = p.artifactStatus[key] = { multi: true, instances: [] };
  return a;
}
function getInstances(key) {
  const proj = activeProject();
  if (!proj) return [];
  const a = proj.artifactStatus[key];
  if (!a || !a.multi) return [];
  return a.instances || [];
}
function getInstance(key, instanceId) {
  return getInstances(key).find(i => i.id === instanceId) || null;
}
function createInstance(key) {
  if (!activeProject()) return null;
  let newId = 'i-' + Math.random().toString(36).slice(2, 8);
  updateActiveProject(p => {
    const a = ensureMultiContainer(p, key);
    const num = a.instances.length + 1;
    const schema = DATA.template_forms[key] || {};
    const singular = schema.instance_singular ? schema.instance_singular[0].toUpperCase() + schema.instance_singular.slice(1) : 'Entry';
    a.instances.push({
      id: newId,
      label: `${singular} ${num}`,
      status: 'in-progress',
      data: {},
      updatedAt: new Date().toISOString(),
    });
  });
  return newId;
}
function updateInstance(key, instanceId, mutator) {
  updateActiveProject(p => {
    const a = p.artifactStatus[key];
    if (!a || !a.instances) return;
    const inst = a.instances.find(i => i.id === instanceId);
    if (inst) { mutator(inst); inst.updatedAt = new Date().toISOString(); }
  });
}
function deleteInstance(key, instanceId) {
  updateActiveProject(p => {
    const a = p.artifactStatus[key];
    if (a && a.instances) a.instances = a.instances.filter(i => i.id !== instanceId);
  });
}

// Migrate legacy global checkbox state (from before per-project tracking) into a Default project.
(function migrateLegacy() {
  const state = loadProjectsState();
  if (state.projects.length > 0) return;
  let legacy = null;
  try { legacy = JSON.parse(localStorage.getItem(LEGACY_CHECKLIST_KEY) || '{}'); } catch { return; }
  if (!legacy || !Object.keys(legacy).length) return;
  const p = createProject({
    name: 'Default project',
    description: 'Migrated from earlier reference-mode checkbox progress. Rename or archive when you no longer need it.',
  });
  p.phaseChecks = legacy;
  state.projects.push(p);
  state.activeId = p.id;
  saveProjectsState(state);
})();

// Per-project phase-completion checkbox helpers
function loadPhaseChecks() {
  const p = activeProject();
  if (p) return p.phaseChecks || {};
  try { return JSON.parse(localStorage.getItem(LEGACY_CHECKLIST_KEY) || '{}'); }
  catch { return {}; }
}
function savePhaseChecks(state) {
  const proj = activeProject();
  if (proj) updateActiveProject(p => { p.phaseChecks = state; });
  else localStorage.setItem(LEGACY_CHECKLIST_KEY, JSON.stringify(state));
}

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
  const allSops = DATA.phases.flatMap(p => p.sops);
  nav.innerHTML = `<div class="nav-section-label">Standard Operating Procedures</div>` +
    allSops.map(s => `
      <a class="nav-link ${s.id===activeSopId?'active':''}" onclick="route('sop/${s.id}/procedure')">
        <span class="nav-id">${s.id.replace('UXR-','')}</span>${s.display}
      </a>
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
  location.hash = activeProject() ? 'project-home' : 'projects';
}

function parseHash() {
  const h = location.hash.replace(/^#/, '');
  if (!h) {
    return { view: 'projects' };
  }
  const [pathPart, anchor] = h.split('#');
  // Extract optional ?query=string from the path
  let path = pathPart;
  const query = {};
  const qIdx = path.indexOf('?');
  if (qIdx > -1) {
    const qs = path.slice(qIdx + 1);
    path = path.slice(0, qIdx);
    qs.split('&').forEach(p => {
      const [k, v] = p.split('=');
      if (k) query[k] = decodeURIComponent(v || '');
    });
  }
  const parts = path.split('/');
  if (parts[0] === 'projects' && parts[1] === 'new') return { view: 'project-new' };
  if (parts[0] === 'projects' && parts[1] === 'edit') return { view: 'project-edit' };
  if (parts[0] === 'projects') return { view: 'projects' };
  if (parts[0] === 'project-home') return { view: 'project-home' };
  if (parts[0] === 'guide' && parts[1]) return { view: 'phase', phaseId: parts[1], anchor };
  if (parts[0] === 'guide') return { view: 'guide-home' };
  if (parts[0] === 'library') return { view: 'library-home' };
  if (parts[0] === 'sop' && parts[1]) {
    return { view: 'sop', sopId: parts[1], tab: parts[2] || 'procedure', anchor, from: query.from || null };
  }
  return { view: 'projects' };
}

function currentMode(r) {
  if (r.view === 'projects' || r.view === 'project-new' || r.view === 'project-edit' || r.view === 'project-home') return 'projects';
  if (r.view === 'guide-home' || r.view === 'phase') return 'guide';
  return 'library';
}

function render() {
  const r = parseHash();
  const mode = currentMode(r);
  updateModeToggle(mode);
  renderProjectBanner();
  updateMobileTitle(r);

  if (r.view === 'projects') {
    renderEmptyNav();
    renderProjectsDashboard();
  } else if (r.view === 'project-new') {
    renderEmptyNav();
    renderProjectForm(null);
  } else if (r.view === 'project-edit') {
    renderEmptyNav();
    renderProjectForm(activeProject());
  } else if (r.view === 'project-home') {
    if (!activeProject()) { route('projects'); return; }
    renderEmptyNav();
    renderProjectHome();
  } else if (r.view === 'guide-home') {
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
    renderSop(r.sopId, r.tab, r.anchor, r.from);
  }
  if (!r.anchor) window.scrollTo({top: 0, behavior: 'instant'});
}
window.addEventListener('hashchange', render);

function renderEmptyNav() {
  document.getElementById('nav').innerHTML = '';
}

function updateMobileTitle(r) {
  const el = document.getElementById('mobile-title');
  if (!el) return;
  let title = 'SOP Library';
  if (r.view === 'projects') title = 'Projects';
  else if (r.view === 'project-home') title = activeProject()?.name || 'Project';
  else if (r.view === 'phase') {
    const ph = DATA.guide_phases.find(p => p.id === r.phaseId);
    title = ph ? `Phase ${ph.number}: ${ph.title}` : 'Phase';
  }
  else if (r.view === 'guide-home') title = 'Project Guide';
  else if (r.view === 'library-home') title = 'SOP Library';
  else if (r.view === 'sop') {
    const sop = SOPS[r.sopId];
    title = sop ? sop.display : 'SOP';
  }
  el.textContent = title;
}

function renderProjectBanner() {
  const wrap = document.getElementById('project-banner-slot');
  if (!wrap) return;
  const proj = activeProject();
  if (!proj) {
    wrap.innerHTML = `
      <div class="project-banner empty" onclick="route('projects')">
        <div class="project-banner-label">No project active</div>
        <div class="project-banner-name">Pick or create a project →</div>
      </div>`;
    return;
  }
  const pct = projectOverallCompletion(proj);
  wrap.innerHTML = `
    <div class="project-banner" onclick="route('project-home')">
      <div class="project-banner-label">Working on</div>
      <div class="project-banner-name">${escapeHtml(proj.name)}</div>
      <div class="project-banner-switch">${pct}% complete · <a onclick="event.stopPropagation(); route('projects');" style="color:var(--accent); cursor:pointer; text-decoration:underline;">switch</a></div>
    </div>`;
}

// ---- Phase-completion checkbox helpers (project-scoped) ----
function phaseCompletionPercent(phaseId) {
  const state = loadPhaseChecks();
  const phase = DATA.guide_phases.find(p => p.id === phaseId);
  if (!phase) return 0;
  const matches = phase.content.match(/^- \[[ x]\]/gm) || [];
  if (!matches.length) return 0;
  const phaseState = state[phaseId] || {};
  const checked = Object.values(phaseState).filter(v => v === true).length;
  return Math.round((checked / matches.length) * 100);
}
function bindPhaseCheckboxes(container, phaseId) {
  const state = loadPhaseChecks();
  const phaseState = state[phaseId] = state[phaseId] || {};
  container.querySelectorAll('input[type="checkbox"]').forEach((cb, idx) => {
    cb.disabled = false;
    cb.checked = phaseState[idx] === true;
    cb.addEventListener('change', () => {
      phaseState[idx] = cb.checked;
      savePhaseChecks(state);
      maybeAdvanceCurrentPhase();
      renderGuideNav(phaseId);
      renderProjectBanner();
      showSaveToast();
    });
  });
}
// ---- Artifact roll-up helpers (project + phase awareness) ----

// Status of an artifact in the active project, including multi-instance handling.
function artifactDisplayStatus(key) {
  const proj = activeProject();
  const state = proj?.artifactStatus?.[key];
  if (!state) return { status: 'not-started', statusLabel: 'Not started', progress: '' };

  if (state.multi) {
    const count = (state.instances || []).length;
    const done = (state.instances || []).filter(i => i.status === 'done').length;
    return {
      status: count > 0 ? (done === count ? 'done' : 'in-progress') : 'not-started',
      statusLabel: count === 0 ? 'Not started' : (done === count ? 'done' : 'in progress'),
      progress: count > 0 ? `${count} ${count === 1 ? 'entry' : 'entries'}${done > 0 ? ` · ${done} done` : ''}` : '',
    };
  }

  // Single-instance
  const status = state.status || 'in-progress';
  const parts = [];
  if (state.checklistState) {
    const completed = Object.values(state.checklistState).filter(v => v === true).length;
    const total = countChecklistItems(key);
    if (total > 0) parts.push(`${completed}/${total} items`);
  }
  if (state.textFields) {
    const filled = Object.values(state.textFields).filter(v => v).length;
    if (filled > 0) parts.push(`${filled} field${filled === 1 ? '' : 's'}`);
  }
  if (state.tableCells) {
    const cells = Object.values(state.tableCells).filter(v => v).length;
    if (cells > 0) parts.push(`${cells} cell${cells === 1 ? '' : 's'}`);
  }
  if (state.data) {
    const fields = Object.values(state.data).filter(v => v !== '' && v != null && v !== false).length;
    if (fields > 0) parts.push(`${fields} field${fields === 1 ? '' : 's'}`);
  }
  return { status, statusLabel: status.replace('-', ' '), progress: parts.join(' · ') };
}

// All templates + checklists from the SOPs referenced by a guide phase.
function artifactsForPhase(phaseId) {
  const phase = DATA.guide_phases.find(p => p.id === phaseId);
  if (!phase) return [];
  const out = [];
  phase.sops.forEach(sopId => {
    const sop = SOPS[sopId];
    if (!sop) return;
    sop.templates.forEach(t => out.push({
      key: `${sopId}-template-${t.section}`, sopId, kind: 'template',
      section: t.section, label: t.label,
    }));
    sop.checklists.forEach(c => out.push({
      key: `${sopId}-checklist-${c.section}`, sopId, kind: 'checklist',
      section: c.section, label: c.label,
    }));
  });
  return out;
}

// Compute "next action" for the active project — surface the most relevant artifact.
function computeNextAction() {
  const proj = activeProject();
  if (!proj) return null;
  const currentPhaseId = proj.currentPhase || 'phase-1';
  const phase = DATA.guide_phases.find(p => p.id === currentPhaseId);
  if (!phase) return null;

  const artifacts = artifactsForPhase(currentPhaseId);
  const started = artifacts.filter(a => {
    const s = proj.artifactStatus?.[a.key];
    return s && (s.status === 'in-progress' || (s.instances && s.instances.some(i => i.status === 'in-progress')));
  });
  if (started.length > 0) {
    const a = started[0];
    return {
      eyebrow: `Phase ${phase.number} · in progress`,
      title: 'Continue ' + a.label,
      sub: `${a.sopId} · ${a.kind}`,
      route: `sop/${a.sopId}/${a.kind}s?from=${currentPhaseId}#sec-${a.section.replace('.', '-')}`,
      number: phase.number,
    };
  }

  // Nothing in progress — recommend the phase starter
  if (phase.recommended_artifact) {
    const a = artifacts.find(x => x.key === phase.recommended_artifact);
    if (a) {
      return {
        eyebrow: `Phase ${phase.number} · recommended start`,
        title: phase.recommended_label || ('Start ' + a.label),
        sub: `${a.sopId} · ${a.kind}`,
        route: `sop/${a.sopId}/${a.kind}s?from=${currentPhaseId}#sec-${a.section.replace('.', '-')}`,
        number: phase.number,
      };
    }
  }

  // No recommendation — point at the phase completion checklist
  return {
    eyebrow: `Phase ${phase.number}`,
    title: phase.title,
    sub: 'Open the phase guide',
    route: `guide/${currentPhaseId}`,
    number: phase.number,
  };
}

// Auto-advance currentPhase when the active phase's checklist hits 100%, and
// celebrate the milestone (once per phase per project).
function maybeAdvanceCurrentPhase() {
  const proj = activeProject();
  if (!proj) return;
  const cur = proj.currentPhase || 'phase-1';
  const idx = DATA.guide_phases.findIndex(p => p.id === cur);
  if (idx === -1) return;
  const pct = phaseCompletionPercent(cur);
  if (pct !== 100) return;

  const completedPhase = DATA.guide_phases[idx];
  const nextPhase = idx < DATA.guide_phases.length - 1 ? DATA.guide_phases[idx + 1] : null;

  const celebrated = (proj.celebratedPhases || []).includes(cur);
  updateActiveProject(p => {
    p.celebratedPhases = p.celebratedPhases || [];
    if (!p.celebratedPhases.includes(cur)) p.celebratedPhases.push(cur);
    if (nextPhase) p.currentPhase = nextPhase.id;
  });
  if (!celebrated) showPhaseComplete(completedPhase, nextPhase);
}

function projectOverallCompletion(proj) {
  if (!proj) return 0;
  const phases = DATA.guide_phases;
  let total = 0, checked = 0;
  phases.forEach(ph => {
    const matches = (ph.content.match(/^- \[[ x]\]/gm) || []).length;
    total += matches;
    const phaseState = (proj.phaseChecks || {})[ph.id] || {};
    checked += Object.values(phaseState).filter(v => v === true).length;
  });
  return total ? Math.round((checked / total) * 100) : 0;
}

// ---- Projects dashboard ----
function renderProjectsDashboard() {
  const state = loadProjectsState();
  const projects = state.projects.slice().sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));
  const activeId = state.activeId;

  document.getElementById('main').innerHTML = `
    <div class="home-eyebrow">Your Research Projects</div>
    <h1 class="home-title">Start a project, or pick up where you left off.</h1>
    <p class="home-lede">
      Each project tracks its own phase progress, saved checklists, and filled-in templates.
      Everything lives in your browser — export to JSON if you need to move between devices.
    </p>

    ${projects.length === 0 ? `
      <div class="phase-preview-row" aria-hidden="true">
        ${DATA.guide_phases.map(ph => `
          <div class="phase-preview">
            <div class="phase-preview-num">${ph.number}</div>
            <div class="phase-preview-title">${ph.title}</div>
          </div>
        `).join('')}
      </div>
      <p style="color:var(--text-muted); font-size:13.5px; margin: 12px 0 24px;">Your project moves through five phases. Each phase suggests the right artifact to start, tracks what you've completed, and exports to Word when you're ready.</p>
      <div class="new-project-card" onclick="route('projects/new')" style="padding:48px 28px;">
        <div class="new-project-plus">+</div>
        <div style="font-family:var(--serif); font-size:18px; font-weight:500;">Create your first project</div>
        <div style="font-size:13px;">Or <a onclick="event.stopPropagation(); route('guide');" style="color:var(--accent); cursor:pointer; text-decoration:underline;">browse the reference library →</a></div>
      </div>
    ` : `
      <div class="projects-grid">
        <div class="new-project-card" onclick="route('projects/new')">
          <div class="new-project-plus">+</div>
          <div style="font-size:13.5px; font-weight:500;">New project</div>
        </div>
        ${projects.map(p => {
          const pct = projectOverallCompletion(p);
          const phase = DATA.guide_phases.find(ph => ph.id === p.currentPhase);
          const updated = formatRelative(p.updatedAt);
          return `
            <div class="project-card ${p.id===activeId?'active':''}" onclick="enterProject('${p.id}')">
              ${p.id===activeId ? '<div class="project-card-active-tag">Active</div>' : ''}
              <h3 class="project-card-name">${escapeHtml(p.name)}</h3>
              <p class="project-card-desc">${escapeHtml(p.description || (p.owner ? 'Owner: ' + p.owner : 'No description yet.'))}</p>
              <div class="project-card-progress"><div class="project-card-progress-bar" style="width:${pct}%"></div></div>
              <div class="project-card-phase">
                <span>${phase ? `Phase ${phase.number}: ${phase.title}` : 'Phase 1: Initiation'}</span>
                <span>${pct}%</span>
              </div>
              <div class="project-card-meta" style="margin-top:10px;">
                <span>${updated}</span>
                ${p.stakeholder ? `<span>·</span><span>${escapeHtml(p.stakeholder)}</span>` : ''}
              </div>
            </div>
          `;
        }).join('')}
      </div>

      <div style="margin-top:36px; color:var(--text-muted); font-size:13px;">
        Want to browse without a project? <a onclick="setActiveProject(null); render(); route('guide');" style="color:var(--accent); cursor:pointer; text-decoration:underline;">Reference mode →</a>
      </div>
    `}
  `;
}

function enterProject(id) {
  setActiveProject(id);
  route('project-home');
}

function dismissWelcome() {
  localStorage.setItem('sop-welcome-dismissed', '1');
  render();
}

function formatRelative(iso) {
  if (!iso) return 'just now';
  const then = new Date(iso).getTime();
  const diff = Date.now() - then;
  const min = 60 * 1000, hr = 60 * min, day = 24 * hr;
  if (diff < hr) return Math.max(1, Math.round(diff / min)) + ' min ago';
  if (diff < day) return Math.round(diff / hr) + ' hr ago';
  if (diff < 7 * day) return Math.round(diff / day) + ' days ago';
  return new Date(iso).toLocaleDateString();
}

// ---- New / edit project form ----
function renderProjectForm(existing) {
  const isEdit = !!existing;
  const p = existing || {name:'', description:'', owner:'', stakeholder:''};
  document.getElementById('main').innerHTML = `
    <div class="breadcrumb">
      <a onclick="route('projects')">Projects</a>
      <span class="sep">/</span>
      <span>${isEdit ? 'Edit project' : 'New project'}</span>
    </div>
    <h1 class="home-title" style="font-size:32px;">${isEdit ? 'Edit project' : 'Create a project'}</h1>
    <p class="home-lede" style="font-size:15px; max-width:560px;">
      Anything you fill in here can be changed later. The project lives in your browser.
    </p>

    <form class="pf-form" onsubmit="event.preventDefault(); submitProjectForm(${isEdit ? `'${p.id}'` : 'null'});">
      <div class="pf-field">
        <label for="pf-name">Project name *</label>
        <input id="pf-name" type="text" required value="${escapeHtml(p.name)}" placeholder="e.g. Q2 Industrial CPQ research">
      </div>
      <div class="pf-field">
        <label for="pf-desc">Description</label>
        <textarea id="pf-desc" placeholder="What's this study about?">${escapeHtml(p.description)}</textarea>
      </div>
      <div class="pf-field">
        <label for="pf-owner">Owner / lead researcher</label>
        <input id="pf-owner" type="text" value="${escapeHtml(p.owner)}" placeholder="Your name">
      </div>
      <div class="pf-field">
        <label for="pf-stakeholder">Stakeholder / sponsor</label>
        <input id="pf-stakeholder" type="text" value="${escapeHtml(p.stakeholder)}" placeholder="Who's the audience for findings?">
        <div class="hint">Often the requester from the Research Brief.</div>
      </div>

      <div class="pf-actions">
        <button type="submit" class="pf-btn-primary">${isEdit ? 'Save changes' : 'Create project'}</button>
        <button type="button" class="pf-btn-secondary" onclick="route('${isEdit ? 'project-home' : 'projects'}')">Cancel</button>
        ${isEdit ? `<button type="button" class="pf-btn-secondary" style="margin-left:auto; color:#b91c1c;" onclick="deleteCurrentProject()">Delete project</button>` : ''}
      </div>
    </form>
  `;
}

function submitProjectForm(existingId) {
  const name = document.getElementById('pf-name').value.trim();
  if (!name) return;
  const desc = document.getElementById('pf-desc').value.trim();
  const owner = document.getElementById('pf-owner').value.trim();
  const stakeholder = document.getElementById('pf-stakeholder').value.trim();
  const state = loadProjectsState();
  if (existingId) {
    const p = state.projects.find(x => x.id === existingId);
    if (p) {
      p.name = name; p.description = desc; p.owner = owner; p.stakeholder = stakeholder;
      p.updatedAt = new Date().toISOString();
      saveProjectsState(state);
    }
    route('project-home');
  } else {
    const p = createProject({name, description: desc, owner, stakeholder});
    state.projects.push(p);
    state.activeId = p.id;
    saveProjectsState(state);
    route('project-home');
  }
}

function deleteCurrentProject() {
  const proj = activeProject();
  if (!proj) return;
  const snapshot = JSON.parse(JSON.stringify(proj));
  const state = loadProjectsState();
  const idx = state.projects.findIndex(x => x.id === proj.id);
  state.projects = state.projects.filter(x => x.id !== proj.id);
  state.activeId = state.projects.length ? state.projects[0].id : null;
  saveProjectsState(state);
  route('projects');
  showUndoToast(`Deleted project "${snapshot.name}"`, () => {
    const s = loadProjectsState();
    // Restore at original index if possible
    s.projects.splice(Math.min(idx, s.projects.length), 0, snapshot);
    s.activeId = snapshot.id;
    saveProjectsState(s);
    route('project-home');
  });
}

// ---- Project home view ----
function renderProjectHome() {
  const p = activeProject();
  if (!p) { route('projects'); return; }
  const pct = projectOverallCompletion(p);
  const phase = DATA.guide_phases.find(ph => ph.id === p.currentPhase);

  const artifacts = [];
  Object.entries(p.artifactStatus || {}).forEach(([key, val]) => {
    const meta = parseArtifactKey(key);
    if (!meta) return;
    if (val.multi && val.instances) {
      val.instances.forEach(inst => {
        artifacts.push({ key, ...meta, status: inst.status, updatedAt: inst.updatedAt, instanceLabel: inst.label, instanceId: inst.id });
      });
    } else if (val.status || val.data || val.checklistState || val.textFields || val.tableCells) {
      const completed = val.checklistState ? Object.values(val.checklistState).filter(v => v === true).length : null;
      const total = val.checklistState ? countChecklistItems(key) : null;
      const filledFields = val.textFields ? Object.values(val.textFields).filter(v => v).length : 0;
      const editedCells = val.tableCells ? Object.values(val.tableCells).filter(v => v).length : 0;
      artifacts.push({ key, ...meta, ...val, checklistCompleted: completed, checklistTotal: total, filledFields, editedCells });
    }
  });
  artifacts.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));

  const next = computeNextAction();

  document.getElementById('main').innerHTML = `
    <div class="breadcrumb">
      <a onclick="route('projects')">Projects</a>
      <span class="sep">/</span>
      <span>${escapeHtml(p.name)}</span>
    </div>
    <div class="ph-header">
      <div>
        <h1 class="ph-title">${escapeHtml(p.name)}</h1>
        <div class="ph-meta">
          ${p.owner ? `Owner: ${escapeHtml(p.owner)} · ` : ''}
          ${p.stakeholder ? `Stakeholder: ${escapeHtml(p.stakeholder)} · ` : ''}
          ${pct}% complete · created ${formatRelative(p.createdAt)}
        </div>
        ${p.description ? `<p style="color:var(--text-muted); margin-top:12px; max-width:640px; font-size:14.5px;">${escapeHtml(p.description)}</p>` : ''}
      </div>
      <div class="ph-actions">
        <button class="ph-action-btn" onclick="route('projects/edit')">Edit</button>
        <button class="ph-action-btn" onclick="exportProjectJson()">Export JSON</button>
        <button class="ph-action-btn ph-action-primary" onclick="compileProjectReadout()" title="Bundle every filled-in artifact into one Word doc">Compile readout</button>
      </div>
    </div>

    ${!localStorage.getItem('sop-welcome-dismissed') ? `
      <div class="welcome-banner">
        <div class="welcome-banner-body">
          <div class="welcome-banner-title">Welcome to your project workspace</div>
          <p class="welcome-banner-text">
            The card below tells you what to do next. Phase tiles show where you are. Saved artifacts collect everything you've worked on — and every artifact exports to Word with your data filled in. Your work autosaves locally as you go.
          </p>
        </div>
        <button class="welcome-banner-dismiss" onclick="dismissWelcome()" aria-label="Dismiss welcome">×</button>
      </div>
    ` : ''}

    ${next ? `
      <div class="next-action" onclick="route('${next.route}')" style="margin-top:24px;">
        <div class="next-action-icon">${next.number}</div>
        <div class="next-action-body">
          <div class="next-action-eyebrow">${escapeHtml(next.eyebrow)}</div>
          <div class="next-action-title">${escapeHtml(next.title)}</div>
          ${next.sub ? `<div class="next-action-sub">${escapeHtml(next.sub)}</div>` : ''}
        </div>
        <span class="next-action-arrow">→</span>
      </div>
    ` : ''}

    <section class="ph-section">
      <h2 class="ph-section-title">Phase progress</h2>
      <p class="ph-section-sub">Click any phase to jump in. Completion is based on the phase-completion checklist.</p>
      <div class="ph-phase-grid">
        ${DATA.guide_phases.map(ph => {
          const phPct = phaseCompletionPercent(ph.id);
          return `
            <div class="ph-phase-tile ${ph.id===p.currentPhase?'current':''}" onclick="route('guide/${ph.id}')">
              <div class="ph-phase-tile-num">Phase ${ph.number}</div>
              <div class="ph-phase-tile-title">${ph.title}</div>
              <div class="ph-phase-tile-bar"><div style="width:${phPct}%"></div></div>
              <div class="ph-phase-tile-pct">${phPct}% complete</div>
            </div>
          `;
        }).join('')}
      </div>
    </section>

    <section class="ph-section">
      <h2 class="ph-section-title">Saved artifacts</h2>
      <p class="ph-section-sub">Checklists and templates you've worked on for this project.</p>
      ${artifacts.length === 0 ? `
        <div style="padding:24px; background:var(--surface-2); border-radius:8px; color:var(--text-muted); font-size:13.5px;">
          No artifacts yet. Open a checklist or template from a phase or SOP and use <strong>Save to project</strong> to track it here.
        </div>
      ` : renderArtifactsByPhase(artifacts)}
    </section>
  `;
}

function renderArtifactsByPhase(artifacts) {
  // Build a phase index: each SOP maps to its first guide phase
  const sopToPhase = {};
  DATA.guide_phases.forEach(ph => {
    ph.sops.forEach(s => {
      if (!sopToPhase[s]) sopToPhase[s] = ph;
    });
  });
  const groups = new Map();
  artifacts.forEach(a => {
    const ph = sopToPhase[a.sopId];
    const key = ph ? ph.id : 'other';
    if (!groups.has(key)) groups.set(key, { phase: ph, items: [] });
    groups.get(key).items.push(a);
  });
  // Sort: phase 1 → 5, then 'other'
  const ordered = DATA.guide_phases.map(ph => groups.get(ph.id)).filter(Boolean);
  if (groups.has('other')) ordered.push(groups.get('other'));

  const row = (a) => `
    <div class="artifact-row" onclick="route('sop/${a.sopId}/${a.kind}s#sec-${a.section.replace('.','-')}')">
      <div class="artifact-row-kind">${a.sopId} · ${a.section}</div>
      <div class="artifact-row-title">
        <strong>${escapeHtml(a.instanceLabel || a.label || (a.kind.charAt(0).toUpperCase() + a.kind.slice(1)))}</strong>
        <span style="color:var(--text-faint); margin-left:6px; font-size:11.5px;">${a.instanceLabel ? escapeHtml(a.label || a.kind) : a.kind}</span>
        ${a.checklistTotal ? `<span style="color:var(--text-faint); margin-left:8px; font-size:11.5px;">${a.checklistCompleted}/${a.checklistTotal} items</span>` : ''}
        ${a.filledFields ? `<span style="color:var(--text-faint); margin-left:8px; font-size:11.5px;">${a.filledFields} fields</span>` : ''}
        ${a.editedCells ? `<span style="color:var(--text-faint); margin-left:8px; font-size:11.5px;">${a.editedCells} cells</span>` : ''}
      </div>
      <span class="artifact-row-status status-${a.status || 'todo'}">${(a.status || 'todo').replace('-', ' ')}</span>
      <span class="artifact-row-date">${formatRelative(a.updatedAt)}</span>
    </div>
  `;

  return ordered.map(g => {
    const header = g.phase ? `Phase ${g.phase.number} · ${g.phase.title}` : 'Other SOPs';
    return `
      <div class="artifact-group">
        <div class="artifact-group-header">
          <span>${escapeHtml(header)}</span>
          <span style="font-family:var(--sans); text-transform:none; letter-spacing:0; color:var(--text-faint); font-size:11.5px;">${g.items.length} item${g.items.length === 1 ? '' : 's'}</span>
        </div>
        <div class="artifact-group-list">${g.items.map(row).join('')}</div>
      </div>
    `;
  }).join('');
}

function parseArtifactKey(key) {
  // e.g. "UXR-004-template-5.1" → { sopId: 'UXR-004', kind: 'template', section: '5.1', label: '...' }
  const m = key.match(/^(UXR-\d{3})-(checklist|template)-(.+)$/);
  if (!m) return null;
  const [, sopId, kind, section] = m;
  const sop = SOPS[sopId];
  const list = kind === 'checklist' ? sop?.checklists : sop?.templates;
  const item = list?.find(x => x.section === section);
  return { sopId, kind, section, label: item?.label };
}

function exportProjectJson() {
  const p = activeProject();
  if (!p) return;
  const blob = new Blob([JSON.stringify(p, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${p.name.replace(/[\\/:*?"<>|]+/g, '').replace(/\s+/g, ' ').trim()}.json`;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 100);
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
  const proj = activeProject();

  const main = document.getElementById('main');
  // Replace inline SOP links with project-aware ones (?from=phase-N)
  let content = phase.content.replace(
    /\(#sop\/(UXR-\d{3})\/(procedure|checklists|templates)\)/g,
    (_, sopId, tab) => `(#sop/${sopId}/${tab}?from=${phaseId})`
  );

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
        <span><strong>SOPs:</strong> ${phase.sops.map(s => `<a class="phase-pill" onclick="route('sop/${s}/procedure?from=${phaseId}')" style="margin-left:4px;">${s}</a>`).join('')}</span>
      </div>
    </div>
    ${proj ? renderPhaseWorkSection(phaseId) : ''}
    <div id="phase-body"><div class="prose">${renderMd(content)}</div></div>
  `;

  const body = document.getElementById('phase-body');
  bindPhaseCheckboxes(body, phaseId);

  if (anchor) {
    const el = document.getElementById(anchor);
    if (el) scrollToElement(el, false);
  }
}

function renderPhaseWorkSection(phaseId) {
  const phase = DATA.guide_phases.find(p => p.id === phaseId);
  const artifacts = artifactsForPhase(phaseId);
  const grouped = artifacts.map(a => ({ ...a, ...artifactDisplayStatus(a.key) }));
  const started = grouped.filter(a => a.status !== 'not-started');
  const available = grouped.filter(a => a.status === 'not-started');
  const recommendedKey = phase.recommended_artifact;
  const recommended = !started.length && recommendedKey
    ? grouped.find(a => a.key === recommendedKey)
    : null;

  if (!started.length && !recommended && !available.length) return '';

  const rowHtml = (a) => `
    <div class="work-row" onclick="route('sop/${a.sopId}/${a.kind}s?from=${phaseId}#sec-${a.section.replace('.', '-')}')">
      <div class="work-row-kind">${a.sopId} · ${a.section}</div>
      <div class="work-row-title">${escapeHtml(a.label)} <span style="color:var(--text-faint); font-size:11.5px; margin-left:4px;">${a.kind}</span></div>
      ${a.progress ? `<span class="work-row-progress">${a.progress}</span>` : ''}
      <span class="work-row-status status-${a.status}">${escapeHtml(a.statusLabel)}</span>
      <span class="work-row-arrow">→</span>
    </div>
  `;

  return `
    <section class="phase-work">
      <div class="phase-work-eyebrow">YOUR WORK FOR THIS PHASE</div>
      <h2 class="phase-work-title">${started.length ? started.length + ' in progress' : (recommended ? 'Start here' : 'Available artifacts')}</h2>
      ${recommended ? `
        <div class="phase-work-cta" onclick="route('sop/${recommended.sopId}/${recommended.kind}s?from=${phaseId}#sec-${recommended.section.replace('.', '-')}')">
          <div>
            <strong>${escapeHtml(phase.recommended_label || ('Start ' + recommended.label))}</strong>
            <div style="font-size:11.5px; opacity:.8;">${recommended.sopId} · ${recommended.kind}</div>
          </div>
          <span class="phase-work-cta-arrow">→</span>
        </div>
      ` : ''}
      ${started.length ? `<div style="margin-top: ${recommended ? '14px' : '0'};">${started.map(rowHtml).join('')}</div>` : ''}
      ${available.length ? `
        <details ${started.length === 0 && !recommended ? 'open' : ''}>
          <summary class="phase-work-toggle">${available.length} more available · click to expand</summary>
          <div style="margin-top:8px;">${available.map(rowHtml).join('')}</div>
        </details>
      ` : ''}
    </section>
  `;
}

// ---- Library home view ----
function renderLibraryHome() {
  const t = DATA.totals;
  const allSops = DATA.phases.flatMap(p => p.sops);
  document.getElementById('main').innerHTML = `
    <div class="home-eyebrow">UX Research Operations · SOP Library</div>
    <h1 class="home-title">Standard operating procedures.</h1>
    <p class="home-lede">
      Nine SOPs, ${t.checklists} checklists, and ${t.templates} templates covering the full research lifecycle —
      from informed consent through repository curation. Built for B2B teams where research evidence has to survive
      procurement, engineering, and the C-suite.
    </p>
    <div class="stat-row">
      <div class="stat"><div class="n">${t.sops}</div><div class="l">SOPs</div></div>
      <div class="stat"><div class="n">${t.checklists}</div><div class="l">Checklists</div></div>
      <div class="stat"><div class="n">${t.templates}</div><div class="l">Templates</div></div>
    </div>

    <div class="phase-cards">
      ${allSops.map(s => `
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
  `;
}

// ---- SOP detail view ----
function renderSop(sopId, tab, anchor, fromPhase) {
  const sop = SOPS[sopId];
  if (!sop) { goHome(); return; }
  const phase = DATA.phases.find(p => p.sops.some(s => s.id === sopId));
  const phaseRefs = sop.phase_refs || [];
  const guidePhase = fromPhase ? DATA.guide_phases.find(p => p.id === fromPhase) : null;

  document.getElementById('main').innerHTML = `
    ${guidePhase ? `
      <a class="back-to-phase" onclick="route('guide/${guidePhase.id}')">← Back to Phase ${guidePhase.number}: ${escapeHtml(guidePhase.title)}</a>
    ` : ''}
    <div class="breadcrumb">
      ${guidePhase ? `
        <a onclick="route('guide')">Project Guide</a>
        <span class="sep">/</span>
        <a onclick="route('guide/${guidePhase.id}')">Phase ${guidePhase.number}</a>
      ` : `
        <a onclick="route('library')">Library</a>
        <span class="sep">/</span>
        <span>${sop.id}</span>
      `}
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
    wireChecklistsInBody(body);
  } else if (tab === 'templates') {
    body.innerHTML = renderAttachments(sop.templates, 'template', sopId);
    toc.innerHTML = renderAttachmentToc(sop.templates);
    wireAttachments(anchor);
    wireChecklistsInBody(body);
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
    const formSchema = DATA.template_forms[key];
    const hasForm = kind === 'template' && !!formSchema;
    return `
    <div class="attach" id="sec-${item.section.replace('.','-')}" data-artifact-key="${key}">
      <button class="attach-head" onclick="this.parentElement.classList.toggle('open')">
        <span class="attach-section">${item.section}</span>
        <span class="attach-title">${item.label}</span>
        <span class="attach-chev">›</span>
      </button>
      <div class="attach-body">
        <div class="attach-content" data-key="${key}" data-kind="${kind}">
          ${hasForm ? renderTemplateBody(key, item, formSchema) : `<div class="prose">${renderMd(item.content)}</div>`}
        </div>
        <div class="attach-actions">
          ${saveToProjectControl(key)}
          <button class="word-btn" onclick="triggerDownload('${key}')">${DOWNLOAD_ICON} Open in Word</button>
        </div>
      </div>
    </div>
    `;
  }).join('')}</div>`;
}

// ---- Save-to-project control on each artifact ----
function saveToProjectControl(key) {
  const proj = activeProject();
  if (!proj) {
    return `<div class="save-to-project">
      <span class="save-status-label">Want to track this in a project? <a onclick="route('projects')" style="color:var(--accent); cursor:pointer; text-decoration:underline;">Pick a project →</a></span>
    </div>`;
  }
  // Multi-instance templates manage status per instance, so suppress top-level dropdown
  if (isMultiInstance(key)) {
    const count = getInstances(key).length;
    const schema = DATA.template_forms[key];
    const noun = count === 1 ? (schema.instance_singular || 'entry') : (schema.instance_plural || 'entries');
    return `<div class="save-to-project">
      <span class="save-status-label">${count} ${noun} in <strong>${escapeHtml(proj.name)}</strong></span>
    </div>`;
  }
  const cur = (proj.artifactStatus || {})[key] || {};
  const status = cur.status || '';
  const completion = checklistCompletion(key);
  const textCount = cur.textFields ? Object.keys(cur.textFields).filter(k => cur.textFields[k]).length : 0;
  const cellCount = cur.tableCells ? Object.keys(cur.tableCells).filter(k => cur.tableCells[k]).length : 0;
  const summaryParts = [];
  if (completion && completion.total > 0) summaryParts.push(`<strong>${completion.completed}/${completion.total}</strong> items checked`);
  if (textCount) summaryParts.push(`<strong>${textCount}</strong> field${textCount===1?'':'s'} filled`);
  if (cellCount) summaryParts.push(`<strong>${cellCount}</strong> cell${cellCount===1?'':'s'} edited`);
  return `<div class="save-to-project">
    <span class="save-status-label">Save to <strong>${escapeHtml(proj.name)}</strong>:</span>
    <select onchange="onArtifactStatusChange('${key}', this.value)">
      <option value="" ${!status?'selected':''}>— Not saved —</option>
      <option value="todo" ${status==='todo'?'selected':''}>To do</option>
      <option value="in-progress" ${status==='in-progress'?'selected':''}>In progress</option>
      <option value="done" ${status==='done'?'selected':''}>Done</option>
    </select>
    ${summaryParts.length ? `<span class="save-status-label">${summaryParts.join(' · ')}</span>` : ''}
    ${cur.updatedAt ? `<span class="save-status-label">Updated ${formatRelative(cur.updatedAt)}</span>` : ''}
  </div>`;
}

// ---- Interactive checklists, text fields, and table cells (project-scoped) ----
function wireChecklistsInBody(rootEl) {
  rootEl.querySelectorAll('.attach[data-artifact-key]').forEach(attach => {
    const key = attach.dataset.artifactKey;
    // Skip templates that have a real form — they manage their own state
    if (DATA.template_forms[key]) return;
    bindAttachChecklist(attach, key);
    bindAttachTextFields(attach, key);
    bindAttachTableCells(attach, key);
  });
}

// Walk text nodes in the attach body, replacing runs of 3+ underscores with
// inline <input> fields bound to project state. Skips code/pre/existing inputs.
function bindAttachTextFields(attach, key) {
  const content = attach.querySelector('.attach-content');
  if (!content) return;
  const proj = activeProject();
  const state = (proj && proj.artifactStatus[key]?.textFields) || {};

  const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
    acceptNode: (node) => {
      let p = node.parentNode;
      while (p && p !== content) {
        if (p.tagName && ['PRE', 'CODE', 'INPUT', 'TH'].includes(p.tagName)) return NodeFilter.FILTER_REJECT;
        p = p.parentNode;
      }
      return /_{3,}/.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  const targets = [];
  let n; while ((n = walker.nextNode())) targets.push(n);

  let counter = 0;
  targets.forEach(textNode => {
    const parts = textNode.nodeValue.split(/(_{3,})/);
    const frag = document.createDocumentFragment();
    let runningLabelHint = '';
    parts.forEach((part, partIdx) => {
      if (/^_{3,}$/.test(part)) {
        const idx = counter++;
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'inline-field';
        input.dataset.fieldIdx = String(idx);
        input.value = state[idx] || '';
        input.disabled = !proj;
        input.style.minWidth = Math.max(80, Math.min(280, part.length * 6)) + 'px';
        // Derive an accessible label from the most recent "Label:" pattern in
        // this text node, plus any prior siblings within the same line block.
        const preceding = (parts.slice(0, partIdx).join('') || '') + runningLabelHint;
        const labelText = deriveFieldLabel(preceding, textNode);
        input.setAttribute('aria-label', labelText || ('Field ' + (idx + 1)));
        input.title = labelText || ('Field ' + (idx + 1));
        if (proj) {
          input.addEventListener('blur', () => onTextFieldChange(key, idx, input.value));
        }
        frag.appendChild(input);
      } else {
        runningLabelHint = part;
        frag.appendChild(document.createTextNode(part));
      }
    });
    textNode.parentNode.replaceChild(frag, textNode);
  });
  attach.dataset.textFieldCount = String(counter);
}

// Pull the most recent "Label:" pattern out of a chunk of preceding text.
// Falls back to nearby <strong> text from the same paragraph.
function deriveFieldLabel(precedingText, anchorNode) {
  // Prefer "Some Label:" right before the underscore run
  const m = precedingText.match(/([A-Za-z][A-Za-z0-9 \-/&]{1,40}):\s*$/);
  if (m) return m[1].trim();
  // Walk up to the parent paragraph/list-item and look for a leading bold
  let p = anchorNode.parentNode;
  while (p && !['P', 'LI', 'TD', 'TH', 'DIV'].includes(p.tagName)) p = p.parentNode;
  if (p) {
    const strong = p.querySelector('strong, b');
    if (strong) return strong.textContent.replace(/[:：]\s*$/, '').trim();
    // Last resort: first 4 words of the block text
    const txt = p.textContent.replace(/_{3,}/g, '').trim();
    if (txt) return txt.split(/\s+/).slice(0, 4).join(' ');
  }
  return '';
}

function bindAttachTableCells(attach, key) {
  const proj = activeProject();
  const state = (proj && proj.artifactStatus[key]?.tableCells) || {};
  let cellCount = 0;
  attach.querySelectorAll('.attach-content table').forEach((table, ti) => {
    table.querySelectorAll('tbody tr').forEach((tr, ri) => {
      tr.querySelectorAll('td').forEach((td, ci) => {
        const cellKey = `t${ti}-r${ri}-c${ci}`;
        td.dataset.cellKey = cellKey;
        cellCount++;
        if (state[cellKey] !== undefined && state[cellKey] !== '') {
          td.textContent = state[cellKey];
        }
        if (proj) {
          td.contentEditable = 'true';
          td.addEventListener('blur', () => onTableCellChange(key, cellKey, td.textContent.trim()));
          td.addEventListener('keydown', e => {
            // Tab moves to next editable cell instead of leaving the form
            if (e.key === 'Tab') {
              e.preventDefault();
              const cells = Array.from(attach.querySelectorAll('.attach-content td[contenteditable="true"]'));
              const i = cells.indexOf(td);
              const next = cells[i + (e.shiftKey ? -1 : 1)];
              if (next) next.focus();
            }
          });
        }
      });
    });
  });
  attach.dataset.tableCellCount = String(cellCount);
}

function onTextFieldChange(key, idx, value) {
  if (!activeProject()) return;
  updateActiveProject(p => {
    const cur = p.artifactStatus[key] || {};
    cur.textFields = cur.textFields || {};
    if (value) cur.textFields[idx] = value;
    else delete cur.textFields[idx];
    cur.status = cur.status === 'done' ? 'done' : 'in-progress';
    cur.updatedAt = new Date().toISOString();
    p.artifactStatus[key] = cur;
  });
  refreshAttachSave(key);
}

function onTableCellChange(key, cellKey, value) {
  if (!activeProject()) return;
  updateActiveProject(p => {
    const cur = p.artifactStatus[key] || {};
    cur.tableCells = cur.tableCells || {};
    if (value) cur.tableCells[cellKey] = value;
    else delete cur.tableCells[cellKey];
    cur.status = cur.status === 'done' ? 'done' : 'in-progress';
    cur.updatedAt = new Date().toISOString();
    p.artifactStatus[key] = cur;
  });
  refreshAttachSave(key);
}

function refreshAttachSave(key) {
  const saveEl = document.querySelector(`.attach[data-artifact-key="${key}"] .save-to-project`);
  if (saveEl) saveEl.outerHTML = saveToProjectControl(key);
  renderProjectBanner();
  showSaveToast();
}

function bindAttachChecklist(attach, key) {
  const checkboxes = attach.querySelectorAll('.attach-content input[type="checkbox"]');
  if (!checkboxes.length) return;
  attach.dataset.checklistCount = String(checkboxes.length);
  const proj = activeProject();
  const state = (proj && proj.artifactStatus[key]?.checklistState) || {};
  checkboxes.forEach((cb, idx) => {
    cb.disabled = !proj;
    cb.checked = state[idx] === true;
    cb.dataset.checklistIdx = String(idx);
    if (proj) {
      cb.addEventListener('change', () => onChecklistCheckboxChange(key, idx, cb.checked));
    }
  });
}

function onChecklistCheckboxChange(key, idx, checked) {
  if (!activeProject()) return;
  const attach = document.querySelector(`.attach[data-artifact-key="${key}"]`);
  const total = parseInt(attach?.dataset.checklistCount || '0', 10);
  updateActiveProject(p => {
    const cur = p.artifactStatus[key] || {};
    cur.checklistState = cur.checklistState || {};
    cur.checklistState[idx] = checked;
    const completed = Object.values(cur.checklistState).filter(v => v === true).length;
    if (total > 0 && completed === total) cur.status = 'done';
    else if (cur.status !== 'done') cur.status = completed > 0 ? 'in-progress' : 'todo';
    cur.updatedAt = new Date().toISOString();
    p.artifactStatus[key] = cur;
  });
  const saveEl = document.querySelector(`.attach[data-artifact-key="${key}"] .save-to-project`);
  if (saveEl) saveEl.outerHTML = saveToProjectControl(key);
  renderProjectBanner();
  showSaveToast();
}

function countChecklistItems(key) {
  // Prefer the DOM (works after the accordion has been rendered)
  const attach = document.querySelector(`.attach[data-artifact-key="${key}"]`);
  if (attach?.dataset.checklistCount) return parseInt(attach.dataset.checklistCount, 10);
  // Fall back to counting markdown task-list items in the source content
  const m = key.match(/^(UXR-\d{3})-(checklist|template)-(.+)$/);
  if (!m) return 0;
  const sop = SOPS[m[1]];
  const list = m[2] === 'checklist' ? sop?.checklists : sop?.templates;
  const item = list?.find(x => x.section === m[3]);
  if (!item) return 0;
  return (item.content.match(/^\s*-\s+\[[ xX]\]/gm) || []).length;
}

function checklistCompletion(key) {
  const proj = activeProject();
  if (!proj) return null;
  const cur = proj.artifactStatus[key];
  if (!cur || !cur.checklistState) return null;
  const total = countChecklistItems(key);
  const completed = Object.values(cur.checklistState).filter(v => v === true).length;
  return { completed, total };
}

function onArtifactStatusChange(key, value) {
  if (!activeProject()) return;
  if (!value) {
    updateActiveProject(p => { delete p.artifactStatus[key]; });
  } else {
    setArtifactStatus(key, { status: value });
  }
  // Re-render just this attachment's actions area
  const el = document.querySelector(`.attach[data-artifact-key="${key}"] .save-to-project`);
  if (el) el.outerHTML = saveToProjectControl(key);
  renderProjectBanner();
  showSaveToast();
}

// ---- Template form renderer ----
function renderTemplateBody(key, item, schema) {
  const proj = activeProject();
  const useFormByDefault = !!proj;
  const stored = (proj && proj.artifactStatus[key]) || null;
  const showForm = stored?.view !== 'markdown' && useFormByDefault;

  // Multi-instance branch: instance list instead of single form
  if (schema.multi_instance && showForm) {
    return `
      <div class="tform-toggle">
        <button class="active" onclick="setTemplateView('${key}','form')">Entries</button>
        <button onclick="setTemplateView('${key}','markdown')">Source</button>
      </div>
      <div class="tform-body">
        ${schema.intro ? `<div class="tform-intro">${escapeHtml(schema.intro)}</div>` : ''}
        ${renderInstanceList(key, schema)}
      </div>
    `;
  }

  return `
    <div class="tform-toggle">
      <button class="${showForm?'active':''}" onclick="setTemplateView('${key}','form')">Fill in</button>
      <button class="${!showForm?'active':''}" onclick="setTemplateView('${key}','markdown')">Source</button>
    </div>
    <div class="tform-body">
      ${showForm ? renderForm(key, schema) : `<div class="prose">${renderMd(item.content)}</div>`}
    </div>
  `;
}

function setTemplateView(key, view) {
  if (activeProject()) {
    updateActiveProject(p => {
      p.artifactStatus[key] = p.artifactStatus[key] || {};
      p.artifactStatus[key].view = view;
    });
  }
  render();
}

// ---- Multi-instance list ----
function renderInstanceList(key, schema) {
  const instances = getInstances(key);
  const singular = schema.instance_singular || 'entry';
  const plural = schema.instance_plural || 'entries';
  if (!instances.length) {
    return `
      <div class="instance-empty">
        No ${plural} yet. Add one to start filling in.
      </div>
      <button class="new-instance-btn" onclick="addInstance('${key}')" style="margin-top:14px;">+ Add ${singular}</button>
    `;
  }
  return `
    <div class="instance-list">
      ${instances.map((inst, idx) => renderInstance(key, schema, inst, idx)).join('')}
    </div>
    <button class="new-instance-btn" onclick="addInstance('${key}')" style="margin-top:14px;">+ Add ${singular}</button>
  `;
}

function renderInstance(key, schema, inst, idx) {
  const open = inst.open ? 'open' : '';
  const status = inst.status || 'in-progress';
  return `
    <div class="instance-card ${open}" data-instance-id="${inst.id}">
      <button class="instance-head" onclick="toggleInstance('${key}', '${inst.id}', event)">
        <span class="instance-chev">›</span>
        <input class="instance-label-input" type="text" value="${escapeHtml(inst.label || '')}" onblur="renameInstance('${key}','${inst.id}', this.value)" onclick="event.stopPropagation()">
        <span class="instance-status-pill status-${status}">${status.replace('-', ' ')}</span>
        <span class="instance-meta">${formatRelative(inst.updatedAt)}</span>
        <button class="instance-delete" onclick="event.stopPropagation(); removeInstance('${key}', '${inst.id}')" title="Delete">×</button>
      </button>
      <div class="instance-body">
        ${renderForm(key, schema, inst.id)}
        <div class="instance-actions">
          <select onchange="onInstanceStatusChange('${key}','${inst.id}', this.value)">
            <option value="todo" ${status==='todo'?'selected':''}>To do</option>
            <option value="in-progress" ${status==='in-progress'?'selected':''}>In progress</option>
            <option value="done" ${status==='done'?'selected':''}>Done</option>
          </select>
          <button class="word-btn" onclick="triggerDownload('${key}', '${inst.id}')">${DOWNLOAD_ICON} Open in Word</button>
        </div>
      </div>
    </div>
  `;
}

function toggleInstance(key, instanceId, event) {
  // Don't toggle when clicking on the inline label input
  if (event && event.target && event.target.classList && event.target.classList.contains('instance-label-input')) return;
  updateInstance(key, instanceId, i => { i.open = !i.open; });
  const card = document.querySelector(`.instance-card[data-instance-id="${instanceId}"]`);
  if (card) card.classList.toggle('open');
}
function addInstance(key) {
  const id = createInstance(key);
  if (id) {
    updateInstance(key, id, i => { i.open = true; });
    rerenderAttach(key);
  }
}
function renameInstance(key, instanceId, newLabel) {
  updateInstance(key, instanceId, i => { i.label = newLabel.trim() || i.label; });
}
function removeInstance(key, instanceId) {
  const inst = getInstance(key, instanceId);
  if (!inst) return;
  const snapshot = JSON.parse(JSON.stringify(inst));
  deleteInstance(key, instanceId);
  rerenderAttach(key);
  showUndoToast(`Deleted "${snapshot.label}"`, () => {
    updateActiveProject(p => {
      const a = ensureMultiContainer(p, key);
      a.instances.push(snapshot);
    });
    rerenderAttach(key);
    renderProjectBanner();
  });
}

function rerenderAttach(key) {
  const attach = document.querySelector(`.attach[data-artifact-key="${key}"]`);
  if (!attach) return;
  const schema = DATA.template_forms[key];
  if (!schema) return;
  const body = attach.querySelector('.tform-body');
  if (body && schema.multi_instance) {
    body.innerHTML = (schema.intro ? `<div class="tform-intro">${escapeHtml(schema.intro)}</div>` : '') + renderInstanceList(key, schema);
  }
  const save = attach.querySelector('.save-to-project');
  if (save) save.outerHTML = saveToProjectControl(key);
  renderProjectBanner();
  showSaveToast();
}
function onInstanceStatusChange(key, instanceId, status) {
  updateInstance(key, instanceId, i => { i.status = status; });
  // Refresh the pill in place
  const card = document.querySelector(`.instance-card[data-instance-id="${instanceId}"]`);
  if (card) {
    const pill = card.querySelector('.instance-status-pill');
    if (pill) {
      pill.className = 'instance-status-pill status-' + status;
      pill.textContent = status.replace('-', ' ');
    }
  }
}

// ---- Form rendering (now instance-aware) ----
function getFormData(key, instanceId) {
  const proj = activeProject();
  if (!proj) return {};
  const a = proj.artifactStatus[key];
  if (!a) return {};
  if (instanceId) {
    const inst = (a.instances || []).find(i => i.id === instanceId);
    return (inst && inst.data) || {};
  }
  return a.data || {};
}

function renderForm(key, schema, instanceId) {
  const data = getFormData(key, instanceId);
  const intro = !instanceId && schema.intro ? `<div class="tform-intro">${escapeHtml(schema.intro)}</div>` : '';
  const sections = schema.sections.map(s => renderFormSection(key, s, data, instanceId)).join('');
  return intro + sections;
}

function autofillValue(field, proj) {
  if (!field.autofill || !proj) return '';
  if (field.autofill === 'project.name') return proj.name || '';
  if (field.autofill === 'project.owner') return proj.owner || '';
  if (field.autofill === 'project.stakeholder') return proj.stakeholder || '';
  if (field.autofill === 'project.description') return proj.description || '';
  if (field.autofill === 'today') return new Date().toISOString().slice(0, 10);
  return '';
}

function renderFormSection(key, section, data, instanceId) {
  const proj = activeProject();
  const instArg = instanceId ? `, '${instanceId}'` : '';
  const fieldsHtml = section.fields.map(f => {
    const stored = data[f.name];
    const value = stored !== undefined ? stored : autofillValue(f, proj);
    const id = `f-${key}-${instanceId || 'root'}-${f.name}`.replace(/[^a-z0-9-]/gi, '_');
    const onChange = `onFormFieldChange('${key}', '${f.name}', this${instArg})`;
    if (f.type === 'textarea') {
      return `<div class="tform-field">
        ${f.label ? `<label for="${id}">${escapeHtml(f.label)}</label>` : ''}
        <textarea id="${id}" class="form-input" rows="${f.rows || 3}" placeholder="${escapeHtml(f.placeholder || '')}" onblur="${onChange}">${escapeHtml(value || '')}</textarea>
      </div>`;
    }
    if (f.type === 'date') {
      return `<div class="tform-field">
        ${f.label ? `<label for="${id}">${escapeHtml(f.label)}</label>` : ''}
        <input id="${id}" type="date" class="form-input" value="${escapeHtml(value || '')}" onchange="${onChange}">
      </div>`;
    }
    if (f.type === 'checkbox') {
      const checked = stored === true ? 'checked' : '';
      return `<div class="tform-field">
        <label class="tform-checkbox-row" for="${id}">
          <input id="${id}" type="checkbox" ${checked} onchange="${onChange}">
          ${escapeHtml(f.label || '')}
        </label>
      </div>`;
    }
    if (f.type === 'radio') {
      return `<div class="tform-field">
        ${f.label ? `<label>${escapeHtml(f.label)}</label>` : ''}
        <div class="tform-radio-group">
          ${f.options.map(opt => `
            <label class="tform-radio-option ${value===opt.value?'selected':''}">
              <input type="radio" name="${id}" value="${opt.value}" ${value===opt.value?'checked':''} onchange="${onChange}">
              ${escapeHtml(opt.label)}
            </label>
          `).join('')}
        </div>
      </div>`;
    }
    // default text
    return `<div class="tform-field">
      ${f.label ? `<label for="${id}">${escapeHtml(f.label)}</label>` : ''}
      <input id="${id}" type="text" class="form-input" value="${escapeHtml(value || '')}" placeholder="${escapeHtml(f.placeholder || '')}" onblur="${onChange}">
    </div>`;
  }).join('');

  const multiCol = section.fields.length >= 2 && section.fields.every(f => f.type === 'text' || f.type === 'date');
  const inner = multiCol ? `<div class="tform-row">${fieldsHtml}</div>` : fieldsHtml;

  // Section completeness: count fields that have a non-empty value (including autofills)
  let filled = 0;
  section.fields.forEach(f => {
    const stored = data[f.name];
    const v = stored !== undefined ? stored : autofillValue(f, proj);
    if (v === true) filled++;
    else if (typeof v === 'string' && v.trim()) filled++;
  });
  const total = section.fields.length;
  const isComplete = filled === total && total > 0;
  const countLabel = total > 0 ? `<span class="tform-section-count ${isComplete ? 'complete' : ''}" aria-label="${filled} of ${total} fields filled">${filled}/${total}${isComplete ? ' ✓' : ''}</span>` : '';

  return `<div class="tform-section">
    ${section.title ? `<h3 class="tform-section-title">${escapeHtml(section.title)}${countLabel}</h3>` : ''}
    ${section.blurb ? `<p class="tform-section-blurb">${escapeHtml(section.blurb)}</p>` : ''}
    ${inner}
  </div>`;
}

function onFormFieldChange(key, fieldName, el, instanceId) {
  if (!activeProject()) return;
  let value;
  if (el.type === 'checkbox') value = el.checked;
  else value = el.value;
  updateActiveProject(p => {
    if (instanceId) {
      const a = p.artifactStatus[key];
      if (!a || !a.instances) return;
      const inst = a.instances.find(i => i.id === instanceId);
      if (!inst) return;
      inst.data = inst.data || {};
      inst.data[fieldName] = value;
      if (inst.status !== 'done') inst.status = 'in-progress';
      inst.updatedAt = new Date().toISOString();
    } else {
      const cur = p.artifactStatus[key] || {};
      cur.data = cur.data || {};
      cur.data[fieldName] = value;
      cur.status = cur.status === 'done' ? 'done' : 'in-progress';
      cur.updatedAt = new Date().toISOString();
      p.artifactStatus[key] = cur;
    }
  });
  if (instanceId) {
    // Update the instance status pill + timestamp in place
    const card = document.querySelector(`.instance-card[data-instance-id="${instanceId}"]`);
    if (card) {
      const inst = getInstance(key, instanceId);
      if (inst) {
        const pill = card.querySelector('.instance-status-pill');
        if (pill && pill.textContent.trim() !== inst.status.replace('-', ' ')) {
          pill.className = 'instance-status-pill status-' + inst.status;
          pill.textContent = inst.status.replace('-', ' ');
        }
        const meta = card.querySelector('.instance-meta');
        if (meta) meta.textContent = formatRelative(inst.updatedAt);
      }
    }
  } else {
    const el2 = document.querySelector(`.attach[data-artifact-key="${key}"] .save-to-project`);
    if (el2) el2.outerHTML = saveToProjectControl(key);
  }
  renderProjectBanner();
  showSaveToast();
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

  // Partition: results that match a saved artifact in the active project
  // float to the top under a 'Your work' header.
  const proj = activeProject();
  const yours = [];
  const reference = [];
  hits.forEach(h => {
    const d = h.doc;
    const artifactKey =
      d.kind === 'Checklist' ? `${d.sopId}-checklist-${d.section}` :
      d.kind === 'Template' ? `${d.sopId}-template-${d.section}` : null;
    if (proj && artifactKey && proj.artifactStatus?.[artifactKey]) yours.push(h);
    else reference.push(h);
  });
  // Cap total at 30, prioritising 'your work'
  const limited = [...yours.slice(0, 12), ...reference.slice(0, 30 - Math.min(yours.length, 12))];
  searchResults = limited;
  if (!searchResults.length) {
    results.innerHTML = `<div class="search-empty">No matches for "${escapeHtml(q)}".</div>`;
    return;
  }

  const yourCount = Math.min(yours.length, 12);
  const html = [];
  if (yourCount > 0) {
    html.push(`<div class="search-group-header">Your work · ${yourCount}</div>`);
    for (let i = 0; i < yourCount; i++) {
      html.push(renderSearchHit(limited[i], i, q));
    }
    html.push(`<div class="search-group-header">Library reference</div>`);
  }
  for (let i = yourCount; i < limited.length; i++) {
    html.push(renderSearchHit(limited[i], i, q));
  }
  results.innerHTML = html.join('');
}

function renderSearchHit(h, i, q) {
  return `
    <div class="search-result ${i===searchSelIdx?'sel':''}" data-i="${i}" onclick="goSearch(${i})">
      <div class="search-result-title">${escapeHtml(h.doc.title)}</div>
      <div class="search-result-meta">${h.doc.kind} · ${h.doc.sopId}${h.doc.section ? ' · ' + h.doc.section : ''} · ${h.doc.phase}</div>
      ${snippet(h.doc.raw, q) ? `<div class="search-result-snippet">${snippet(h.doc.raw, q)}</div>` : ''}
    </div>
  `;
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
