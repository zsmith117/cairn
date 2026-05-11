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
  .status-todo { background: var(--surface-2); color: var(--text-faint); }
  .status-in-progress { background: #fef3c7; color: #92400e; }
  html[data-theme="dark"] .status-in-progress { background: #443a1a; color: #fcd34d; }
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
    downloadAsWord(d.title, d.sopId, d.markdown);
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

function downloadFilledForm(meta, schema, proj, data) {
  const custom = CUSTOM_WORD_RENDERERS[Object.keys(DATA.template_forms).find(k => DATA.template_forms[k] === schema)];
  let body;
  if (custom) {
    body = custom(meta, schema, proj, data);
  } else {
    body = '';
    schema.sections.forEach(s => {
    if (s.title) body += `<h2>${escapeHtml(s.title)}</h2>`;
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
  }
  const today = new Date().toISOString().slice(0, 10);
  const projName = proj ? proj.name : '';
  const filename = (projName ? projName + ' — ' : '') + meta.title;
  const safeName = filename.replace(/[\\/:*?"<>|]+/g, '').replace(/\s+/g, ' ').trim() + '.doc';
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
  const blob = new Blob(['﻿', doc], { type: 'application/msword' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = safeName;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 100);
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
  location.hash = activeProject() ? 'project-home' : 'projects';
}

function parseHash() {
  const h = location.hash.replace(/^#/, '');
  if (!h) {
    // Default landing: dashboard always (per multi-project answer).
    return { view: 'projects' };
  }
  const [path, anchor] = h.split('#');
  const parts = path.split('/');
  if (parts[0] === 'projects' && parts[1] === 'new') return { view: 'project-new' };
  if (parts[0] === 'projects' && parts[1] === 'edit') return { view: 'project-edit' };
  if (parts[0] === 'projects') return { view: 'projects' };
  if (parts[0] === 'project-home') return { view: 'project-home' };
  if (parts[0] === 'guide' && parts[1]) return { view: 'phase', phaseId: parts[1], anchor };
  if (parts[0] === 'guide') return { view: 'guide-home' };
  if (parts[0] === 'library') return { view: 'library-home' };
  if (parts[0] === 'sop' && parts[1]) {
    return { view: 'sop', sopId: parts[1], tab: parts[2] || 'procedure', anchor };
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
    renderSop(r.sopId, r.tab, r.anchor);
  }
  if (!r.anchor) window.scrollTo({top: 0, behavior: 'instant'});
}
window.addEventListener('hashchange', render);

function renderEmptyNav() {
  document.getElementById('nav').innerHTML = '';
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
      renderGuideNav(phaseId);
      renderProjectBanner();
    });
  });
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
      <div class="new-project-card" onclick="route('projects/new')" style="margin-top:32px; padding:60px 28px;">
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
  if (!confirm(`Delete "${proj.name}"? This cannot be undone.`)) return;
  const state = loadProjectsState();
  state.projects = state.projects.filter(x => x.id !== proj.id);
  state.activeId = state.projects.length ? state.projects[0].id : null;
  saveProjectsState(state);
  route('projects');
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
    } else if (val.status || val.data) {
      artifacts.push({ key, ...meta, ...val });
    }
  });
  artifacts.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));

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
        <button class="ph-action-btn" onclick="route('guide/${p.currentPhase}')">Continue ${phase ? `Phase ${phase.number}` : ''} →</button>
        <button class="ph-action-btn" onclick="route('projects/edit')">Edit</button>
        <button class="ph-action-btn" onclick="exportProjectJson()">Export JSON</button>
      </div>
    </div>

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
      ` : `
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:8px; overflow:hidden;">
          ${artifacts.map(a => `
            <div class="artifact-row" onclick="route('sop/${a.sopId}/${a.kind}s')">
              <div class="artifact-row-kind">${a.sopId} · ${a.section}</div>
              <div class="artifact-row-title">
                <strong>${escapeHtml(a.instanceLabel || a.label || (a.kind.charAt(0).toUpperCase() + a.kind.slice(1)))}</strong>
                <span style="color:var(--text-faint); margin-left:6px; font-size:11.5px;">${a.instanceLabel ? escapeHtml(a.label || a.kind) : a.kind}</span>
              </div>
              <span class="artifact-row-status status-${a.status || 'todo'}">${(a.status || 'todo').replace('-', ' ')}</span>
              <span class="artifact-row-date">${formatRelative(a.updatedAt)}</span>
            </div>
          `).join('')}
        </div>
      `}
    </section>
  `;
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
  return `<div class="save-to-project">
    <span class="save-status-label">Save to <strong>${escapeHtml(proj.name)}</strong>:</span>
    <select onchange="onArtifactStatusChange('${key}', this.value)">
      <option value="" ${!status?'selected':''}>— Not saved —</option>
      <option value="todo" ${status==='todo'?'selected':''}>To do</option>
      <option value="in-progress" ${status==='in-progress'?'selected':''}>In progress</option>
      <option value="done" ${status==='done'?'selected':''}>Done</option>
    </select>
    ${cur.updatedAt ? `<span class="save-status-label">Updated ${formatRelative(cur.updatedAt)}</span>` : ''}
  </div>`;
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
  if (!confirm(`Delete "${inst.label}"? This cannot be undone.`)) return;
  deleteInstance(key, instanceId);
  rerenderAttach(key);
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

  return `<div class="tform-section">
    ${section.title ? `<h3 class="tform-section-title">${escapeHtml(section.title)}</h3>` : ''}
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
