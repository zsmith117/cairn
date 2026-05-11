# UXR-009: Research Repository Standard Operating Procedure

**Document ID:** UXR-009
**Version:** 1.0
**Effective Date:** January 26, 2026
**Last Review:** January 26, 2026
**Document Owner:** UX Research Lead
**Classification:** Internal Use Only

---

## 1. Purpose

This Standard Operating Procedure establishes the requirements and procedures for maintaining a centralized UX research repository. It ensures that:

- Past research is discoverable and accessible when needed
- Research knowledge persists beyond individual researchers
- Teams can find and build on prior insights
- Research investment creates cumulative value over time
- Duplicate research is avoided through awareness of past work
- Research insights are democratized across the organization
- Meta-analysis across studies is possible
- Organizational memory is preserved as team members change
- Research portfolio and impact are visible to leadership
- Research function can demonstrate value through body of work

**Why This Matters:**

Research without a repository loses value over time. Poor knowledge management leads to:
- Rediscovering the same insights multiple times (wasted effort)
- Making decisions without awareness of relevant past research
- Loss of institutional knowledge when researchers leave
- Inability to see patterns across multiple studies
- Research living only in individual researcher's heads or hard drives
- New team members unable to learn from past work
- Stakeholders not knowing what research has been done
- Duplicate research on same topics (wasted resources)
- Missing opportunities to build on prior insights
- Inability to demonstrate research impact portfolio-wide
- Research perceived as one-off activities rather than systematic program

An effective repository transforms research from discrete projects into a cumulative knowledge asset that compounds in value over time.

---

## 2. Scope

**This SOP applies to:**

- All completed UX research studies
- Generative and evaluative research
- Interview-based studies
- Usability testing
- Field research and contextual inquiry
- Survey research (qualitative components)
- Concept testing and validation research
- Journey mapping and service design research
- Competitive and comparative research
- Any research activity producing reusable insights

**This SOP covers:**

- Repository structure and organization
- Taxonomy and tagging systems
- Entry creation and standards
- Search and discovery methods
- Access controls and permissions
- Curation and maintenance
- Integration with research workflow
- Cross-study synthesis and meta-analysis
- Archiving and retention
- Repository tools and platforms
- Measuring repository usage and value

**Out of scope:**

- Day-to-day project file management (see UXR-006)
- Detailed data retention schedules (see UXR-002)
- Raw data storage (covered by UXR-002; repository stores synthesized outputs)
- Code repositories for prototypes or tools
- Design file management (Figma, etc.)
- Non-research documentation

---

## 3. Definitions

| Term | Definition |
|------|------------|
| **Research Repository** | Centralized, searchable system for storing and accessing completed research |
| **Repository Entry** | Single record representing one research study with metadata, findings, and artifacts |
| **Research Artifact** | Tangible output from research (report, presentation, journey map, persona, etc.) |
| **Metadata** | Structured information about research (date, method, participants, tags, etc.) |
| **Taxonomy** | Hierarchical classification system for organizing research (categories, subcategories) |
| **Tag** | Keyword label applied to research to enable discovery |
| **Faceted Search** | Search that can be filtered by multiple dimensions (date, method, topic, etc.) |
| **Research Index** | Searchable catalog of all research entries |
| **Study Summary** | Brief overview of research study including key findings and artifacts |
| **Research Portfolio** | Complete collection of research studies over time |
| **Meta-Analysis** | Analysis across multiple studies to identify broader patterns |
| **Research Synthesis** | Integration of insights from multiple studies on related topics |
| **Findability** | Ease with which relevant research can be discovered when needed |
| **Curation** | Active maintenance of repository to ensure quality and relevance |
| **Archival** | Long-term preservation of research beyond active use |
| **Access Control** | Permissions determining who can view/edit repository content |
| **Knowledge Asset** | Research as reusable organizational resource with cumulative value |
| **Research Lineage** | Connection between related studies over time (follow-up, expansion, etc.) |
| **Discoverability** | Ability to find research through search, browsing, or recommendation |

---

## 4. Procedure

### 4.1 Repository Structure and Organization

#### 4.1.1 Repository Architecture

**Three-Layer Structure:**

```
LAYER 1: RESEARCH INDEX (Catalog View)
- List of all research studies
- Sortable and filterable
- Quick scan of portfolio

    ↓

LAYER 2: STUDY SUMMARIES (Overview)
- One-page summary per study
- Key findings, artifacts, metadata
- Enough to assess relevance

    ↓

LAYER 3: FULL MATERIALS (Deep Dive)
- Complete reports, presentations
- Raw materials (notes, transcripts)
- All artifacts and outputs
```

**Repository Organization Options:**

| Approach | Structure | Pros | Cons | When to Use |
|----------|-----------|------|------|-------------|
| **Chronological** | By date (year, quarter, month) | Easy to add; shows timeline | Hard to find by topic | Small volume; temporal patterns matter |
| **Topical** | By product area, feature, theme | Easy to find related research | Requires consistent categorization | Medium-large volume; topic-focused searches |
| **Methodological** | By research method | Easy to find method examples | Doesn't reflect content | Teaching; method comparison |
| **By Project** | By product/initiative | Aligns with org structure | Rigid; research spans projects | Project-driven organization |
| **Hybrid (Recommended)** | Metadata-driven with multiple views | Flexible; multiple access paths | Requires robust tagging | Most organizations |

**Recommended Hybrid Approach:**

- **Primary organization:** Metadata-driven (database or wiki)
- **Multiple views:** Sort/filter by date, topic, method, product area
- **Folder structure:** Chronological for simplicity
- **Discovery:** Through search and tags, not folder hierarchy

#### 4.1.2 Folder Structure (If File-Based)

```
/Research Repository
  /2024
    /Q1
      /UXR-2024-Q1-001_[Study Name]
        - 00_Study_Summary.pdf
        - 01_Research_Plan.pdf
        - 02_Research_Report.pdf
        - 03_Presentation.pdf
        - 04_Highlights.pdf
        /Raw_Materials
          /Session_Notes
          /Transcripts
          /Recordings (if retained)
        /Artifacts
          /Journey_Maps
          /Personas
          /Frameworks
      /UXR-2024-Q1-002_[Study Name]
        [Same structure]
    /Q2
      [Continue...]
  /2025
    /Q1
      [Continue...]

  /_Index
    - Research_Index.xlsx [or database]
    - Research_Portfolio_View.pdf
    - Tags_and_Taxonomy.xlsx

  /_Templates
    - Study_Summary_Template.docx
    - Repository_Entry_Template.docx

  /_Meta-Analysis
    /Cross-Study_Synthesis_[Topic]
```

#### 4.1.3 Database Structure (If Tool-Based)

**Recommended Fields:**

| Field Category | Fields | Purpose |
|----------------|--------|---------|
| **Identity** | Study ID, Study Name, Short Title | Unique identification |
| **Timing** | Start Date, End Date, Quarter, Year | Temporal organization |
| **Classification** | Method, Type (Generative/Evaluative), Product Area, Feature | Categorization |
| **People** | Research Lead, Team Members, Stakeholders | Attribution and contact |
| **Content** | Research Questions, Key Findings (summary), Top Recommendations | Quick overview |
| **Participants** | Sample Size, Participant Types, Segments | Scope understanding |
| **Tags** | Topics, Themes, User Needs, Pain Points | Discovery |
| **Artifacts** | Links to Report, Presentation, Raw Data, Other Outputs | Access |
| **Impact** | Decisions Influenced, Actions Taken, Metrics Changed | Value demonstration |
| **Related** | Related Studies, Follow-up Studies, Prerequisites | Lineage |
| **Status** | Published, Draft, Archived | Lifecycle |

---

### 4.2 Taxonomy and Tagging System

#### 4.2.1 Developing a Taxonomy

**Taxonomy Dimensions:**

```
DIMENSION 1: RESEARCH METHOD
- Interview (1-on-1)
- Usability Testing
- Field Research / Contextual Inquiry
- Focus Group
- Survey (Qualitative)
- Concept Testing
- Diary Study
- Card Sorting
- Tree Testing
- Other

DIMENSION 2: RESEARCH TYPE
- Generative (exploratory, discovery)
- Evaluative (assessment, validation)
- Formative (early-stage feedback)
- Summative (post-launch assessment)

DIMENSION 3: PRODUCT AREA
[Customize to your organization]
- Product A
- Product B
- Feature X
- Feature Y
- Platform
- Mobile App
- Web App

DIMENSION 4: USER SEGMENT
[Customize to your organization]
- Enterprise Users
- SMB Users
- Individual Users
- Administrators
- End Users
- Power Users
- Casual Users

DIMENSION 5: TOPIC/THEME
[Emerge from research over time]
- Onboarding
- Navigation
- Search
- Reporting
- Collaboration
- Integration
- Performance
- Mobile Experience
- Accessibility
- Pricing
- [Continuously expand]

DIMENSION 6: USER NEED/PAIN POINT
[Common across studies]
- Efficiency
- Control
- Flexibility
- Visibility
- Confidence
- Support
- Automation
- Customization
- Simplicity
- [Continuously expand]
```

**Taxonomy Development Process:**

| Phase | Activity | Timeline |
|-------|----------|----------|
| **Initial** | Create starter taxonomy based on org structure | Before repository launch |
| **Seed** | Tag first 10-20 studies | Month 1 |
| **Refine** | Observe what's working; adjust | Month 2-3 |
| **Stabilize** | Finalize core taxonomy | Month 4-6 |
| **Evolve** | Add new tags as needed; retire unused | Ongoing |

#### 4.2.2 Tagging Standards

**Tagging Principles:**

| Principle | Description | Example |
|-----------|-------------|---------|
| **Consistent** | Use same term for same concept | "Onboarding" not sometimes "Onboarding" and sometimes "Getting Started" |
| **Specific** | Specific enough to be useful | "Mobile Navigation" not just "Mobile" |
| **Limited** | 5-10 tags per study; not exhaustive | Select most relevant tags only |
| **Hierarchical** | Use parent categories when applicable | "Mobile > Mobile Navigation" |
| **Controlled** | Use predefined tags; don't free-form | Select from list, not type arbitrary |
| **Findable** | Think about how people will search | Use terms people actually use |

**Tag Types:**

```
REQUIRED TAGS (Every study must have):
- Method: [Single selection from list]
- Type: [Generative or Evaluative]
- Product Area: [Single or multiple]
- Quarter/Year: [Auto-generated from date]

RECOMMENDED TAGS (Apply when relevant):
- User Segment: [Who was studied]
- Topic/Theme: [What was studied - multiple OK]
- Feature: [Specific feature if applicable]

OPTIONAL TAGS (Apply if helpful):
- User Need: [Needs identified]
- Pain Point: [Problems uncovered]
- Opportunity: [Opportunities discovered]
- Related Initiative: [Business context]
```

**Tagging Workflow:**

```
STEP 1: Required Tags
Select method, type, product area when creating entry

STEP 2: Review Content
Read study summary and findings

STEP 3: Apply Topic Tags
Select 3-5 most relevant topic tags

STEP 4: Apply Descriptive Tags
Add user needs, pain points, opportunities if applicable

STEP 5: Check Consistency
Search for similar studies; use same tags for same concepts

STEP 6: Document New Tags
If creating new tag, document definition in taxonomy
```

---

### 4.3 Creating Repository Entries

#### 4.3.1 Entry Standards and Requirements

**Minimum Requirements for Repository Entry:**

```
REQUIRED FOR PUBLICATION:

STUDY INFORMATION:
[ ] Study ID assigned
[ ] Study name/title
[ ] Research lead identified
[ ] Dates (start and end)
[ ] Method documented

CONTENT:
[ ] Study summary completed (Template 5.1)
[ ] Key findings documented (minimum 3)
[ ] Research question(s) stated
[ ] Participant information (who, how many)

ARTIFACTS:
[ ] At least one shareable output
    Options: Report, Presentation, Highlight, Summary
[ ] Output is anonymized per UXR-002
[ ] Output is finalized (not draft)

METADATA:
[ ] Required tags applied
[ ] Product area specified
[ ] Contact person listed
```

**Quality Standards:**

| Standard | Requirement |
|----------|-------------|
| **Completeness** | All required fields populated |
| **Accuracy** | Information is correct and current |
| **Clarity** | Understandable without context |
| **Anonymization** | No PII in shareable materials per UXR-002 |
| **Accessibility** | Files are in accessible formats; links work |
| **Currency** | Information reflects final state of research |

#### 4.3.2 Study Summary Template

**Study Summary Structure:**

```
RESEARCH STUDY SUMMARY

Study ID: [UXR-YYYY-QN-###]
Study Title: [Descriptive title]
Short Title: [Abbreviated for lists]

===================================================================

STUDY INFORMATION

Research Lead: [Name]
Team Members: [Names]
Stakeholders: [Key stakeholders]
Date: [Month Year] or [Start Date] - [End Date]
Status: [Completed / Published]

===================================================================

RESEARCH OVERVIEW

Purpose:
[2-3 sentences: Why was this research conducted? What business need or question prompted it?]

Research Questions:
1. [Primary research question]
2. [Secondary question]
3. [Additional questions]

Method: [Interview / Usability Testing / etc.]
Participants: [N] [description of who participated]
Duration: [N] sessions over [timeframe]

===================================================================

KEY FINDINGS

1. [Finding 1 - one sentence headline]
   [1-2 sentences elaborating with evidence]

2. [Finding 2]
   [Elaboration]

3. [Finding 3]
   [Elaboration]

4. [Finding 4 if applicable]

5. [Finding 5 if applicable]

===================================================================

TOP RECOMMENDATIONS

1. [Recommendation 1] - Priority: [High/Medium/Low]
   [1 sentence rationale]

2. [Recommendation 2] - Priority: [High/Medium/Low]
   [Rationale]

3. [Recommendation 3] - Priority: [High/Medium/Low]
   [Rationale]

===================================================================

IMPACT

Decisions Influenced:
- [Decision or action taken based on research]
- [Another impact]

Outcomes:
- [Measurable outcome if available]

===================================================================

ARTIFACTS & MATERIALS

Available Materials:
- Research Report: [Link or location]
- Presentation: [Link]
- Research Highlights: [Link]
- Journey Map: [Link if applicable]
- Other: [Specify]

Raw Materials (Restricted Access):
- Session Notes: [Location]
- Transcripts: [Location]
- Recordings: [Location if retained]

===================================================================

METADATA

Product Area: [Area]
Feature: [Specific feature if applicable]
User Segment: [Who was studied]

Topics/Themes:
- [Tag 1]
- [Tag 2]
- [Tag 3]

Method: [Method]
Type: [Generative / Evaluative]

Related Studies:
- [Link to related prior research]
- [Link to follow-up research]

===================================================================

CONTACT

Questions about this research? Contact [Name], [Email]

===================================================================

[1-2 pages maximum]
```

#### 4.3.3 Entry Creation Workflow

**When to Create Entry:**

| Timing | Activity |
|--------|----------|
| **At study initiation** | Create draft entry with basic info; reserve Study ID |
| **During research** | Update with method, participant info as confirmed |
| **After analysis** | Add findings and recommendations |
| **After communication** | Link artifacts (reports, presentations) |
| **After publication** | Finalize and publish entry |
| **Ongoing** | Update with impact information as it becomes available |

**Entry Creation Process:**

```
STEP 1: CREATE DRAFT ENTRY (5 min)
- Assign Study ID
- Add title, lead, dates
- Mark as "Draft"

STEP 2: POPULATE DURING RESEARCH (10 min)
- Add method and participant details
- Link research plan
- Add stakeholder information

STEP 3: COMPLETE AFTER ANALYSIS (30-45 min)
- Write study summary
- Document key findings
- Add recommendations
- Apply tags

STEP 4: LINK ARTIFACTS (10 min)
- Upload or link report
- Upload or link presentation
- Link any other materials
- Verify all links work

STEP 5: PUBLISH (5 min)
- Verify all required fields complete
- Mark as "Published"
- Notify stakeholders of repository entry

STEP 6: UPDATE WITH IMPACT (Ongoing)
- Document decisions influenced
- Add outcome metrics
- Link follow-up research
```

---

### 4.4 Search and Discovery

#### 4.4.1 Search Methods

**Primary Search Approaches:**

| Method | When to Use | How It Works | Example |
|--------|-------------|--------------|---------|
| **Keyword Search** | Looking for specific topic | Search across titles, summaries, findings | "onboarding" returns all studies about onboarding |
| **Tag Filtering** | Known category | Filter by tags (method, topic, segment) | Filter to "Usability Testing" + "Mobile" |
| **Date Range** | Recent or historical | Filter by date/quarter/year | "Show me 2024 research" |
| **Product Area** | Specific product | Filter by product area | "All Product X research" |
| **Researcher** | By who conducted | Filter by research lead | "What has [Name] done?" |
| **Related Studies** | Connected research | Follow links between studies | "Follow-up to Study X" |
| **Full-Text Search** | Deep search in documents | Search within reports and presentations | "Export" finds all mentions in all documents |

**Search Interface Design:**

```
┌────────────────────────────────────────────────────────────┐
│  RESEARCH REPOSITORY                                       │
│                                                            │
│  Search: [___________________________________] [Search]    │
│                                                            │
│  Filter by:                                                │
│  Date:    [Dropdown: All, 2025, 2024, 2023, ...]          │
│  Method:  [Dropdown: All, Interview, Usability, ...]      │
│  Product: [Dropdown: All, Product A, Product B, ...]      │
│  Topic:   [Multi-select: Onboarding, Navigation, ...]     │
│                                                            │
│  [Clear Filters]                                           │
└────────────────────────────────────────────────────────────┘

Results: 24 studies found

[Study 1 Title] | [Date] | [Method] | [Lead]
Brief excerpt of findings...
[View Study] [View Report]

[Study 2 Title] | [Date] | [Method] | [Lead]
Brief excerpt of findings...
[View Study] [View Report]

[Continue...]
```

#### 4.4.2 Browsing and Navigation

**Browsing Views:**

| View | Purpose | Organization |
|------|---------|--------------|
| **Recent Studies** | See what's new | Chronological (newest first) |
| **By Product Area** | Domain-specific browsing | Grouped by product/feature |
| **By Topic** | Theme-based browsing | Grouped by common themes |
| **By Method** | Method examples | Grouped by research method |
| **Most Viewed** | Popular research | Sorted by view count |
| **Related to Current Work** | Contextual suggestions | Algorithm or manual curation |

**Navigation Patterns:**

```
HOMEPAGE:
- Search bar
- Quick links to popular topics
- Recent additions (last 6)
- Browse by: [Product] [Topic] [Method] [Date]

SEARCH RESULTS:
- List of matching studies
- Filters on left sidebar
- Sort options (relevance, date, title)
- Preview on hover

STUDY PAGE:
- Study summary at top
- Key findings highlighted
- Artifacts section with download links
- Related studies suggested at bottom
- "Cite this research" section

TOPIC PAGE:
- All studies tagged with this topic
- Synthesis across studies if available
- Common themes
- Gaps identified
```

#### 4.4.3 Improving Discoverability

**Discoverability Strategies:**

| Strategy | Implementation | Benefit |
|----------|----------------|---------|
| **Consistent Naming** | Follow naming convention for all studies | Predictable structure |
| **Rich Summaries** | Detailed study summaries with keywords | Surface in searches |
| **Multiple Tags** | 5-10 tags per study | Multiple paths to find |
| **Cross-Linking** | Link related studies explicitly | Follow research lineage |
| **Featured Research** | Highlight important studies on homepage | Raise visibility |
| **Email Digest** | Monthly/quarterly research roundup | Proactive awareness |
| **Slack Integration** | Post new research to relevant channels | Push notification |
| **Onboarding** | Show new team members how to use repository | Build search skills |

**Making Research "Stumble-able":**

People often find valuable research by accident. Enable this:

- **Homepage Rotation:** Feature different studies prominently
- **"You Might Also Like":** Suggest related research
- **Popular This Month:** Show what others are viewing
- **Random Serendipity:** "Surprise me" button for exploration
- **Visual Gallery:** Browse thumbnails of journey maps, frameworks
- **Thematic Collections:** Curated sets on specific topics

---

### 4.5 Access Control and Permissions

#### 4.5.1 Access Levels

**Recommended Access Tiers:**

| Level | Who | What They Can Access | What They Can Do |
|-------|-----|---------------------|------------------|
| **Public** | Anyone in organization | - Study summaries<br>- Final reports/presentations<br>- Published artifacts | - View<br>- Download<br>- Comment (if enabled) |
| **Restricted** | Research team + approved stakeholders | - Raw session notes<br>- Transcripts<br>- Personal participant data<br>- Preliminary findings | - View<br>- Download (with restrictions per UXR-002) |
| **Admin** | Research team | - All content<br>- Drafts<br>- Metadata | - Edit<br>- Publish<br>- Delete<br>- Manage permissions |

**Access Control by Content Type:**

| Content Type | Access Level | Rationale |
|--------------|--------------|-----------|
| **Study summaries** | Public | Broad awareness; no PII |
| **Final reports** | Public | Shareable insights; anonymized |
| **Presentations** | Public | Communication materials |
| **Highlights** | Public | Designed for wide distribution |
| **Journey maps, personas** | Public | Design assets for teams |
| **Session notes** | Restricted | May contain PII; per UXR-002 |
| **Transcripts** | Restricted | Contains PII; per UXR-002 |
| **Recordings** | Highly Restricted | PII; consent limitations |
| **Research plans (draft)** | Restricted | Work in progress |

#### 4.5.2 Anonymization Requirements

**All publicly accessible materials must be anonymized per UXR-002:**

```
ANONYMIZATION CHECKLIST FOR REPOSITORY:

[ ] Participant names replaced with IDs (P1, P2, etc.)
[ ] Company names removed or genericized
[ ] Colleague names removed
[ ] Specific locations removed (unless relevant and approved)
[ ] Email addresses removed
[ ] Phone numbers removed
[ ] Screenshots sanitized (no names, emails, PII visible)
[ ] Video clips redacted (faces blurred if needed)

ACCEPTABLE IN PUBLIC MATERIALS:
✓ Participant role/title (if not identifying)
✓ Industry vertical (if not identifying)
✓ Company size category (e.g., "Large enterprise")
✓ Geographic region (if not specific)
✓ Anonymized quotes with P[#] attribution
✓ Aggregated data (N=10 participants)
```

---

### 4.6 Curation and Maintenance

#### 4.6.1 Repository Curation Activities

**Ongoing Curation Tasks:**

| Activity | Frequency | Owner | Purpose |
|----------|-----------|-------|---------|
| **New entry review** | Per entry | Research Lead | Ensure quality and completeness |
| **Link checking** | Monthly | Research Ops | Fix broken links |
| **Duplicate review** | Quarterly | Research Lead | Consolidate or link duplicates |
| **Tag consolidation** | Quarterly | Research Lead | Merge similar tags; maintain taxonomy |
| **Usage analysis** | Quarterly | Research Lead | Understand what's being used |
| **Retired study archival** | Annual | Research Lead + Ops | Archive old/irrelevant research |
| **Full audit** | Annual | Research Lead | Comprehensive quality check |

#### 4.6.2 Quality Maintenance

**Repository Health Checks:**

```
QUARTERLY REPOSITORY HEALTH CHECK

COMPLETENESS:
[ ] All studies from quarter have entries
[ ] All required fields populated
[ ] All artifacts linked
[ ] All tags applied

ACCURACY:
[ ] Links work (sample 10% and test)
[ ] Study information current
[ ] Contact information accurate
[ ] Impact information updated

USABILITY:
[ ] Search returns relevant results
[ ] Filters work correctly
[ ] Navigation is intuitive
[ ] Load times acceptable

QUALITY:
[ ] Entries follow template
[ ] Summaries are well-written
[ ] Tagging is consistent
[ ] No duplicates

ISSUES IDENTIFIED:
[List problems found]

ACTIONS TAKEN:
[Remediation steps]

NEXT REVIEW: [Date]
```

#### 4.6.3 Tag Maintenance

**Tag Hygiene:**

| Issue | How to Address |
|-------|----------------|
| **Tag proliferation** | Review all tags quarterly; merge similar tags; establish approval for new tags |
| **Inconsistent terms** | Identify synonyms (e.g., "Getting Started" vs. "Onboarding"); standardize on one term; bulk update |
| **Orphan tags** | Tags used only once or twice; evaluate if needed; remove or merge |
| **Ambiguous tags** | Tags whose meaning is unclear; add definition; rename for clarity; provide examples |
| **Outdated tags** | Tags for retired products/features; archive tag; keep for historical studies but don't use for new |

**Tag Evolution Process:**

```
PROPOSING NEW TAG:

1. Check existing tags - does similar tag exist?
2. Document proposed tag definition
3. Identify studies that would use this tag
4. Submit to Research Lead for approval
5. If approved:
   - Add to taxonomy documentation
   - Apply to relevant existing studies
   - Available for future use

RETIRING TAG:

1. Identify tag to retire (unused, outdated, or redundant)
2. Document reason for retirement
3. Identify replacement tag if applicable
4. Bulk update affected studies
5. Archive tag (keep in taxonomy as "retired")
```

#### 4.6.4 Archiving Old Research

**Archival Policy:**

| Study Age | Status | Action |
|-----------|--------|--------|
| **0-2 years** | Current | Fully accessible; primary repository |
| **2-5 years** | Relevant | Accessible; note age in searches |
| **5+ years** | Historical | Archive or flag as historical; may be outdated |
| **Superseded** | Replaced | Link to newer research; flag as superseded |

**When to Archive:**

- Research is outdated (product has changed significantly)
- Research has been superseded by newer study on same topic
- Context no longer relevant (e.g., pre-pivot research)
- Stakeholders confirm research is no longer referenced

**Archival Process:**

```
STEP 1: IDENTIFY CANDIDATES
- Studies older than 5 years
- Studies on retired products/features
- Superseded research

STEP 2: REVIEW
- Is research still valuable?
- Does it provide historical context?
- Is it referenced in other studies?

STEP 3: DECIDE
- Archive (keep but flag as historical)
- Delete (if no longer valuable and no retention requirement)
- Keep active (if still relevant)

STEP 4: ARCHIVE
- Add "Archived" status
- Add note: "This research is from [date]. Context may have changed."
- Move to archive section or filter out of default searches
- Maintain links from other studies

STEP 5: DOCUMENT
- Record archival decision
- Document rationale
```

**Archival ≠ Deletion:**

- Archived research remains accessible for historical reference
- Useful for understanding decision context ("Why did we decide X back then?")
- Valuable for new team members learning organizational history
- Required for compliance/legal if retention policies mandate

---

### 4.7 Integration with Research Workflow

#### 4.7.1 Embedding Repository in Process

**Repository Touchpoints in Research Process:**

| Research Phase | Repository Activity |
|----------------|---------------------|
| **Planning (UXR-004)** | Search for related past research; build on prior insights |
| **Scoping** | Create draft repository entry; reserve Study ID |
| **Data Collection** | No interaction (focus on research) |
| **Analysis (UXR-007)** | Reference past research for comparison; meta-analysis |
| **Communication (UXR-008)** | Link outputs to repository entry |
| **Publication** | Finalize and publish repository entry |
| **Follow-up** | Update entry with impact information |

**Making Repository Part of Workflow:**

```
BEFORE RESEARCH:
✓ Search repository for related past research
✓ Note gaps that your research will fill
✓ Create draft repository entry with Study ID

AFTER RESEARCH:
✓ Write study summary
✓ Upload/link final artifacts
✓ Apply tags
✓ Publish entry
✓ Notify stakeholders

ONGOING:
✓ Update with impact information
✓ Link follow-up research
✓ Respond to questions about research
```

#### 4.7.2 Onboarding to Repository

**For New Team Members:**

```
REPOSITORY ORIENTATION CHECKLIST

WEEK 1: ACCESS & BASICS
[ ] Repository access granted
[ ] Quick tour of repository structure
[ ] Search practice: Find 3 studies relevant to your work
[ ] Review taxonomy and tagging system

WEEK 2: EXPLORATION
[ ] Browse recent research (last quarter)
[ ] Read 5 study summaries in your product area
[ ] Identify 2-3 themes you see across studies

WEEK 3: APPLICATION
[ ] Use repository to answer question or inform decision
[ ] Practice creating a draft study summary
[ ] Understand when and how to add research

WEEK 4: MASTERY
[ ] Help someone else find research
[ ] Identify gap in repository that could be filled
[ ] Provide feedback on repository usability
```

**For New Stakeholders:**

- Brief introduction to what repository contains
- Demo of how to search for relevant research
- Guidance on interpreting study summaries
- Contact for questions or deeper dives

#### 4.7.3 Promoting Repository Use

**Driving Adoption:**

| Strategy | Implementation | Goal |
|----------|----------------|------|
| **Make it default** | Link from every research output; "See all research in repository" | Habit formation |
| **Showcase wins** | Share examples: "Team X found research Y that informed decision Z" | Demonstrate value |
| **Executive visibility** | Share portfolio views with leadership quarterly | Top-down support |
| **Integrate in meetings** | Reference repository in planning meetings | Normalize usage |
| **Measure and celebrate** | Track usage; celebrate milestones (100th study!) | Positive reinforcement |
| **Make it easy** | One-click access; simple search; mobile-friendly | Remove friction |
| **Champions network** | Identify advocates who model usage | Peer influence |

**Measuring Adoption:**

| Metric | What It Measures | Target |
|--------|------------------|--------|
| **Search frequency** | How often repository is used | Increasing trend |
| **Studies accessed** | Breadth of usage | Most studies viewed at least once per year |
| **Repeat users** | Depth of usage | 80%+ of team uses monthly |
| **Time to find** | Efficiency | <5 minutes to find relevant research |
| **Impact stories** | Value delivered | 5+ examples per quarter of repository driving decisions |

---

### 4.8 Cross-Study Synthesis and Meta-Analysis

#### 4.8.1 Identifying Synthesis Opportunities

**When to Synthesize Across Studies:**

| Scenario | Synthesis Approach |
|----------|-------------------|
| **Multiple studies on same topic** | Synthesize findings across studies to form comprehensive view |
| **Related topics across studies** | Identify connections between seemingly separate findings |
| **Longitudinal patterns** | Track how insights evolve over time (e.g., annual studies) |
| **User segment patterns** | Compare findings across different user segments |
| **Product comparison** | Compare user experiences across products/features |
| **Method validation** | Compare findings from different methods on same topic |

**Triggers for Meta-Analysis:**

- Accumulated 3+ studies on related topics
- Stakeholder asking "What have we learned about X overall?"
- Planning new research - want to know what's already known
- Annual/quarterly review of research portfolio
- Major strategic planning requiring comprehensive view

#### 4.8.2 Conducting Meta-Analysis

**Meta-Analysis Process:**

```
STEP 1: IDENTIFY RELATED STUDIES (1 hour)
- Search repository by topic/tags
- Review studies for relevance
- Select studies to include in synthesis
- Document inclusion criteria

STEP 2: EXTRACT KEY INFORMATION (2-4 hours)
For each study:
- Research questions addressed
- Key findings
- Recommendations
- Context (when, who, method)
- Create comparison table

STEP 3: IDENTIFY PATTERNS (2-3 hours)
- What findings are consistent across studies?
- What findings contradict each other? Why?
- What patterns emerge that aren't visible in individual studies?
- What has changed over time?
- What gaps exist?

STEP 4: SYNTHESIZE INSIGHTS (2-3 hours)
- Write synthesis narrative
- Identify meta-insights (insights across studies)
- Develop recommendations based on body of work
- Note confidence level

STEP 5: DOCUMENT SYNTHESIS (2-3 hours)
- Create synthesis document
- Add to repository as special entry type
- Link to constituent studies
- Share with stakeholders

TOTAL TIME: ~10-15 hours for synthesis of 3-5 studies
```

**Meta-Analysis Template:**

```
CROSS-STUDY SYNTHESIS: [TOPIC]

Date: [Date]
Analyst: [Name]
Studies Included: [N] studies from [date range]

===================================================================

PURPOSE

Why this synthesis:
[What question or need prompted this meta-analysis]

Scope:
[What's included and excluded]

===================================================================

STUDIES INCLUDED

1. [Study ID] - [Study Name] ([Date])
   - Method: [Method]
   - Participants: [N, Type]
   - Key finding: [Brief summary]

2. [Study ID] - [Study Name] ([Date])
   [Same structure]

[Continue for all studies]

===================================================================

SYNTHESIS OF FINDINGS

CONSISTENT PATTERNS (across all or most studies):

PATTERN 1: [Pattern Name]
- Observed in: [Studies where seen]
- Evidence: [Summary of supporting findings]
- Strength: [High/Medium consistency]
- Implication: [What this means]

PATTERN 2: [Pattern Name]
[Same structure]

───────────────────────────────────────────────────────────────

EVOLVING PATTERNS (changed over time):

PATTERN: [What changed]
- Earlier studies ([dates]): [Finding]
- Recent studies ([dates]): [Finding]
- Change: [Description of evolution]
- Why: [Hypothesis about why changed]

───────────────────────────────────────────────────────────────

CONTRADICTORY FINDINGS:

CONTRADICTION: [What differs]
- Study X found: [Finding]
- Study Y found: [Contradictory finding]
- Possible explanations:
  - Context difference: [How contexts differed]
  - Method difference: [How methods differed]
  - Evolution: [If time-based]
- Resolution: [What we believe and why]

───────────────────────────────────────────────────────────────

GAPS IDENTIFIED:

- [Area not yet researched]
- [Question still unanswered]
- [User segment not included]

===================================================================

META-INSIGHTS

[Insights that emerge only from looking across studies]

INSIGHT 1:
[What we understand now that we couldn't see in individual studies]

INSIGHT 2:
[Another meta-level insight]

===================================================================

RECOMMENDATIONS

Based on cumulative research:

1. [Recommendation based on body of work]
   Priority: [High/Medium/Low]
   Rationale: [Why, based on multiple studies]

2. [Recommendation]
   [Details]

===================================================================

CONFIDENCE ASSESSMENT

What we're confident about:
- [Finding with high confidence across studies]

What needs more research:
- [Area with limited or contradictory evidence]

===================================================================

FUTURE RESEARCH NEEDS

Priority questions for future research:
1. [Question]
2. [Question]

Recommended approach:
[Suggested method/scope for future research]

===================================================================

REFERENCES

Full details available in repository:
- [Link to Study 1]
- [Link to Study 2]
- [Link to Study 3]

===================================================================
```

#### 4.8.3 Maintaining Synthesis Documents

**Synthesis Lifecycle:**

| Stage | Activity | Frequency |
|-------|----------|-----------|
| **Create** | Initial synthesis when threshold reached (3+ studies) | As needed |
| **Update** | Add new studies to synthesis | When significant new research completed |
| **Review** | Validate synthesis remains current | Annually |
| **Archive** | Move to historical if context changed significantly | As needed |

**Linking Synthesis to Studies:**

- Synthesis document is special repository entry
- Links bidirectionally to constituent studies
- Studies link back to synthesis ("Part of synthesis: [Topic]")
- Synthesis appears in search results for relevant topics

---

### 4.9 Special Considerations

#### 4.9.1 Repository for Different Team Sizes

**Small Team (1-3 Researchers):**

- **Simple solution:** Shared folder + Spreadsheet index
- **Tools:** Google Drive + Google Sheets
- **Structure:** Chronological folders with study summaries
- **Tags:** Basic categories only
- **Maintenance:** Ad hoc; minimal curation

**Medium Team (4-10 Researchers):**

- **Growing solution:** Dedicated tool or robust wiki
- **Tools:** Notion, Airtable, Confluence
- **Structure:** Database with metadata and tags
- **Tags:** Developed taxonomy with governance
- **Maintenance:** Quarterly curation; designated owner

**Large Team (10+ Researchers):**

- **Robust solution:** Enterprise research repository
- **Tools:** Dovetail, Productboard, custom database
- **Structure:** Full database with faceted search
- **Tags:** Comprehensive taxonomy; controlled vocabulary
- **Maintenance:** Research Ops role; ongoing curation

#### 4.9.2 Starting a Repository from Scratch

**Phase 1: Foundation (Month 1-2)**

```
STEP 1: DEFINE STRUCTURE
[ ] Choose platform/tool
[ ] Define folder structure or database schema
[ ] Create templates (study summary, entry format)
[ ] Establish naming conventions

STEP 2: BUILD TAXONOMY
[ ] List product areas
[ ] List common research methods
[ ] Brainstorm likely topics (will evolve)
[ ] Document tag definitions

STEP 3: SEED REPOSITORY
[ ] Identify 5-10 most important past studies
[ ] Create entries for seed studies
[ ] Apply initial tags
[ ] Test search and navigation

STEP 4: LAUNCH
[ ] Announce to team
[ ] Provide brief training
[ ] Make repository required for new research
[ ] Establish maintenance routine
```

**Phase 2: Growth (Month 3-6)**

- Add 2-3 studies per month
- Refine taxonomy based on actual usage
- Monitor search queries to identify missing tags
- Gather feedback; iterate on structure

**Phase 3: Maturity (Month 7-12)**

- Repository becomes default reference
- Curation routines established
- Usage metrics tracked
- Impact stories documented
- Continuous improvement based on learnings

#### 4.9.3 Migrating Existing Research

**Migration Strategy:**

| Priority | Studies to Migrate | Rationale |
|----------|-------------------|-----------|
| **High** | Last 12 months; high-impact studies | Recent and relevant |
| **Medium** | 1-2 years old; still relevant | Historical context; still referenced |
| **Low** | 2+ years old; broad topics | Nice to have; time permitting |
| **Skip** | Pre-pivot; obsolete; superseded | No longer relevant |

**Migration Process:**

```
EFFICIENT MIGRATION:

TIER 1: Full Migration (High priority)
- Complete study summary
- All artifacts linked
- Full tagging

TIER 2: Lightweight Entry (Medium priority)
- Basic study summary (abbreviated)
- Link to final report only
- Minimal tagging

TIER 3: Index Only (Low priority)
- Study name, date, lead
- Link to report
- No summary unless requested later

TIME ESTIMATES:
- Tier 1: 1 hour per study
- Tier 2: 20 minutes per study
- Tier 3: 5 minutes per study

APPROACH:
- Start with Tier 1 (most valuable)
- Batch Tier 2 migrations
- Tier 3 as time allows
- Don't let perfection block progress
```

#### 4.9.4 Remote and Distributed Teams

**Repository for Remote Teams:**

- **Cloud-based required:** No local file servers
- **Async-friendly:** Rich written documentation, not just recordings
- **Time zones:** Clear timestamps; "Recent" means different things
- **Notification strategy:** Alert channels without overwhelming
- **Video artifacts:** Short clips for key findings; full presentations available

**Enabling Global Access:**

- Ensure platform accessible from all locations
- Consider regional data storage if compliance requires
- Test access speeds from different regions
- Provide localized support/training if needed
- Time zone-aware notifications and digests

---

## 5. Templates and Tools

### Template 5.1: Study Summary Template

[See Section 4.3.2 for complete template]

---

### Template 5.2: Repository Entry Metadata Template

```
REPOSITORY ENTRY METADATA

===================================================================

STUDY IDENTIFICATION

Study ID: [UXR-YYYY-QN-###]
Study Name: [Full descriptive title]
Short Name: [Abbreviated title for lists - max 50 characters]
Alternate Names: [Any other names used, nicknames]

===================================================================

DATES

Start Date: [YYYY-MM-DD]
End Date: [YYYY-MM-DD]
Quarter: [Q1/Q2/Q3/Q4 YYYY]
Year: [YYYY]
Duration: [N weeks]

===================================================================

PEOPLE

Research Lead: [Name] <[email]>
Supporting Researchers: [Name1], [Name2]
Primary Stakeholder: [Name], [Title]
Other Stakeholders: [Name1], [Name2], [Name3]

===================================================================

CLASSIFICATION

Method: [Dropdown: Interview, Usability Testing, Field Research, Focus Group, Survey, Diary Study, Card Sorting, Tree Testing, Concept Testing, Other]

Research Type: [Dropdown: Generative, Evaluative, Formative, Summative]

Product Area: [Dropdown: Product A, Product B, Platform, etc.]

Feature: [Text: Specific feature if applicable]

User Segment: [Multi-select: Enterprise, SMB, Individual, Admin, End User, Power User, etc.]

===================================================================

RESEARCH OVERVIEW

Purpose: [Text area: 2-3 sentences]

Research Questions:
1. [Primary research question]
2. [Secondary question]
3. [Additional question]

Participants:
- Sample size: [N]
- Participant types: [Description]
- Recruitment method: [How recruited]
- Segments included: [Breakdown]

===================================================================

KEY FINDINGS (Summary)

Finding 1: [One sentence]
Finding 2: [One sentence]
Finding 3: [One sentence]
Finding 4: [One sentence]
Finding 5: [One sentence]

===================================================================

TOP RECOMMENDATIONS (Summary)

1. [Recommendation] - [Priority: High/Med/Low]
2. [Recommendation] - [Priority]
3. [Recommendation] - [Priority]

===================================================================

TAGS

Required:
- Method: [Auto-filled from above]
- Type: [Auto-filled from above]
- Product Area: [Auto-filled from above]

Topics/Themes (Multi-select):
- [ ] Onboarding
- [ ] Navigation
- [ ] Search
- [ ] Reporting
- [ ] Collaboration
- [ ] Integration
- [ ] Mobile Experience
- [ ] Accessibility
- [ ] Performance
- [ ] Other: [Specify]

User Needs Identified (Multi-select):
- [ ] Efficiency
- [ ] Control
- [ ] Flexibility
- [ ] Visibility
- [ ] Confidence
- [ ] Support
- [ ] Automation
- [ ] Customization
- [ ] Simplicity
- [ ] Other: [Specify]

===================================================================

ARTIFACTS & FILES

Study Summary: [Link/Upload]
Research Report: [Link/Upload]
Presentation: [Link/Upload]
Highlight Document: [Link/Upload]
Journey Map: [Link/Upload]
Personas: [Link/Upload]
Framework/Model: [Link/Upload]
Other Artifacts: [Link/Upload]

Raw Materials (Restricted):
Session Notes Folder: [Link]
Transcripts Folder: [Link]
Recordings Folder: [Link]
Research Plan: [Link]

===================================================================

IMPACT

Decisions Influenced:
- [Decision 1 with brief description]
- [Decision 2]

Actions Taken:
- [Action 1 - Status: Completed/In Progress/Planned]
- [Action 2 - Status]

Metrics Changed:
- [Metric]: [Before] → [After]
- [Metric]: [Before] → [After]

Impact Assessment: [Link to impact assessment if completed]

===================================================================

RELATIONSHIPS

Prior Research (Built on):
- [Link to Study ID] - [How related]

Follow-up Research (This led to):
- [Link to Study ID] - [How related]

Related Studies (Connected):
- [Link to Study ID] - [How related]

Part of Initiative: [Initiative name if applicable]

Included in Synthesis: [Link to cross-study synthesis]

===================================================================

STATUS & ACCESS

Status: [Dropdown: Draft, In Review, Published, Archived]
Publication Date: [YYYY-MM-DD]
Last Updated: [YYYY-MM-DD]

Visibility: [Dropdown: Public (All), Restricted (Team Only), Private (Lead Only)]

Access Notes: [Any special access considerations]

===================================================================

USAGE STATISTICS (Auto-tracked if platform supports)

Views: [N]
Downloads: [N]
Comments: [N]
Referenced in: [N other studies]

===================================================================

NOTES

Internal Notes: [Any additional context for research team]

===================================================================

CREATED BY: [Name]
CREATED DATE: [YYYY-MM-DD]
LAST MODIFIED BY: [Name]
LAST MODIFIED DATE: [YYYY-MM-DD]

===================================================================
```

---

### Template 5.3: Research Portfolio View Template

```
RESEARCH PORTFOLIO OVERVIEW

Period: [Date Range, e.g., "2024 Full Year" or "Q1-Q3 2024"]
Generated: [Date]

===================================================================

PORTFOLIO SUMMARY

Total Studies Completed: [N]
Studies by Quarter:
- Q1: [N]
- Q2: [N]
- Q3: [N]
- Q4: [N]

Research Team:
- Researchers: [N]
- Studies per researcher: [Average]

===================================================================

RESEARCH BY METHOD

| Method | Count | % of Total |
|--------|-------|------------|
| Interview | [N] | [%] |
| Usability Testing | [N] | [%] |
| Field Research | [N] | [%] |
| Focus Group | [N] | [%] |
| Other | [N] | [%] |
| TOTAL | [N] | 100% |

[Bar chart visualization]

===================================================================

RESEARCH BY PRODUCT AREA

| Product Area | Count | % of Total |
|--------------|-------|------------|
| Product A | [N] | [%] |
| Product B | [N] | [%] |
| Platform | [N] | [%] |
| Cross-product | [N] | [%] |
| TOTAL | [N] | 100% |

[Pie chart visualization]

===================================================================

RESEARCH BY TYPE

Generative (Discovery): [N] ([%])
Evaluative (Assessment): [N] ([%])

===================================================================

TOP TOPICS RESEARCHED

| Topic | # of Studies | Recent Study |
|-------|--------------|--------------|
| [Topic 1] | [N] | [Study Name, Date] |
| [Topic 2] | [N] | [Study Name, Date] |
| [Topic 3] | [N] | [Study Name, Date] |
| [Topic 4] | [N] | [Study Name, Date] |
| [Topic 5] | [N] | [Study Name, Date] |

===================================================================

PARTICIPANT ENGAGEMENT

Total Participants: [N]
Average per study: [N]

Participant Types:
- Enterprise users: [N]
- SMB users: [N]
- Individual users: [N]
- Internal stakeholders: [N]

===================================================================

IMPACT HIGHLIGHTS

Studies with Documented Impact: [N] ([%])

Decision Impact:
- Product roadmap changes: [N] studies influenced decisions
- Design changes implemented: [N] studies drove changes
- Strategic pivots: [N] studies informed strategy

Outcome Impact:
- User metrics improved: [N] studies
- Business metrics improved: [N] studies

Impact Stories:
1. [Brief impact story from study X]
2. [Brief impact story from study Y]
3. [Brief impact story from study Z]

===================================================================

RESEARCH GAPS IDENTIFIED

Under-researched Areas:
- [Product area or topic with limited research]
- [Another gap]

Under-represented Segments:
- [User segment not well studied]
- [Another segment]

Opportunities for Future Research:
- [Identified research need]
- [Another opportunity]

===================================================================

REPOSITORY USAGE

Repository Views: [N]
Most Viewed Studies:
1. [Study Name] - [N] views
2. [Study Name] - [N] views
3. [Study Name] - [N] views

Search Terms:
Top searches: [Term1], [Term2], [Term3]

===================================================================

KEY THEMES ACROSS PORTFOLIO

[Synthesis of patterns observed across multiple studies]

THEME 1: [Theme name]
- Observed in [N] studies
- [Brief description]

THEME 2: [Theme name]
- Observed in [N] studies
- [Brief description]

THEME 3: [Theme name]
- Observed in [N] studies
- [Brief description]

===================================================================

LOOKING AHEAD

Planned Research Next Quarter:
- [Planned study 1]
- [Planned study 2]
- [Planned study 3]

Research Capacity:
- Current team: [N] researchers
- Estimated capacity: [N] studies per quarter

===================================================================

FULL STUDY LIST

[Date] | [Study ID] | [Study Name] | [Method] | [Product Area]
[Continue chronologically for all studies in period]

===================================================================

For detailed information on any study, see Research Repository:
[Link to repository]

Questions? Contact: [Research Lead Name, Email]

===================================================================
```

---

### Template 5.4: Repository Onboarding Guide

```
RESEARCH REPOSITORY USER GUIDE

Welcome to the Research Repository!

===================================================================

WHAT IS THIS?

The Research Repository is our centralized library of all UX research.
It contains:
- Study summaries and findings from all research
- Reports, presentations, and artifacts
- Searchable by topic, date, product, method
- Impact tracking and follow-up research connections

===================================================================

WHY USE IT?

BEFORE starting new research:
- See what we already know (avoid duplicate work)
- Build on past insights (cumulative learning)
- Learn from methodology examples

WHEN making decisions:
- Find relevant research to inform choices
- Understand user needs and pain points
- Access evidence to support recommendations

FOR awareness:
- Stay current on research across organization
- Understand research history and evolution
- Learn about user segments and experiences

===================================================================

HOW TO ACCESS

URL: [Repository URL]
Login: [Your company credentials]

Quick links:
- Homepage: [URL]
- Recent Research: [URL]
- Browse by Topic: [URL]

Mobile access: [Yes/No - if yes, how]

===================================================================

HOW TO SEARCH

BASIC SEARCH:
1. Enter keywords in search box
2. Results show matching studies
3. Click study title to see details

Example: Search "onboarding" to find all onboarding research

FILTERED SEARCH:
1. Use filters on left sidebar:
   - Date range
   - Product area
   - Research method
   - Topics
2. Combine filters for specific results

Example: Filter to "Product A" + "2024" + "Usability Testing"

BROWSING:
- Browse by Topic: See all research on a theme
- Browse by Product: See all research for a product
- Browse by Date: See research chronologically
- Recent Studies: See what's new

===================================================================

UNDERSTANDING A STUDY ENTRY

When you open a study, you'll see:

STUDY SUMMARY (1-2 pages):
- Why research was done
- Who participated
- Key findings (3-5)
- Top recommendations
- Impact achieved

ARTIFACTS:
- Research Report (detailed findings)
- Presentation (stakeholder readout)
- Highlights (1-page visual summary)
- Other materials (journey maps, etc.)

METADATA:
- Tags showing topics covered
- Related studies
- Contact person for questions

===================================================================

COMMON USE CASES

"I'm planning research on [topic]. What do we already know?"
→ Search for [topic]
→ Review study summaries
→ Note what's known and what gaps exist
→ Reference past research in your plan

"I need to make a decision about [feature]. Is there research?"
→ Filter to [product] + [feature name]
→ Read relevant findings
→ Apply insights to decision
→ Document how research informed choice

"I'm new to the team. What research has been done on [product]?"
→ Filter to [product]
→ Sort by date
→ Read recent study summaries
→ Get up to speed quickly

"Someone asked if we've researched [topic]. Have we?"
→ Search [topic]
→ If results: "Yes, here's what we found..."
→ If no results: "Not yet, but we could explore it"

===================================================================

TIPS FOR EFFECTIVE USE

DO:
✓ Search before starting new research
✓ Use specific keywords (e.g., "mobile navigation" not just "mobile")
✓ Try multiple search terms if first attempt doesn't find what you need
✓ Read study summary before diving into full report
✓ Contact research lead if you have questions about a study
✓ Share relevant research with colleagues

DON'T:
✗ Assume we haven't researched something without searching
✗ Use outdated research without considering context (check date!)
✗ Cite research out of context (read the limitations)
✗ Download raw data without permission (restricted access)

===================================================================

UNDERSTANDING STUDY DATES

- Studies show date they were completed
- Consider context: product may have changed since
- Studies older than 2 years: verify relevance
- Studies marked "Archived": historical context only

===================================================================

INTERPRETING FINDINGS

CONFIDENCE LEVELS:
- Studies show how many participants (N=)
- Qualitative research: Patterns, not statistics
- "8 of 10 participants" = strong pattern
- "2 of 10 participants" = emerging insight or edge case

SCOPE:
- Each study has defined scope (who, what, when)
- Findings apply within that scope
- Don't overgeneralize beyond study boundaries

===================================================================

GETTING HELP

Questions about the repository?
- Contact: [Research Ops or Research Lead]
- Email: [Email]
- Slack: [Channel]

Questions about specific research?
- Contact person listed on each study entry
- They can provide context or deeper dives

Can't find what you're looking for?
- Ask in [Slack channel]
- Someone may know if research exists
- Or may confirm it's a gap worth exploring

===================================================================

CONTRIBUTING TO REPOSITORY

If you conduct research:
- Add entry per UXR-009 SOP
- Contact [Research Lead] for Study ID
- Complete study summary template
- Publish within 1 week of completing research

If you find issues:
- Broken links? Report to [Research Ops]
- Incorrect information? Contact study lead
- Suggestions for improvement? Email [Research Lead]

===================================================================

FAQ

Q: Can I download study materials?
A: Yes! Final reports, presentations, and artifacts are downloadable.
   Raw data (notes, transcripts) may be restricted.

Q: Can I share research outside the company?
A: No. Repository content is Internal Use Only per classification.

Q: How often is repository updated?
A: New research added continuously as studies complete.
   Curation happens quarterly.

Q: What if I need research we haven't done?
A: Great! This identifies a research need. Contact [Research Lead]
   to discuss commissioning new research.

Q: Can I request follow-up research?
A: Yes. If existing research raises questions, talk to [Research Lead]
   about follow-up studies.

===================================================================

TRAINING & SUPPORT

Live training: [Schedule if offered]
Video tutorials: [Link if available]
Office hours: [Research Lead] - [Schedule]

===================================================================

HAPPY RESEARCHING!

Remember: The repository is a treasure trove of user insights.
Use it to make better, more informed decisions.

Questions? We're here to help!
[Contact info]

===================================================================
```

---

### Template 5.5: Repository Health Check Template

```
REPOSITORY HEALTH CHECK

Date: [YYYY-MM-DD]
Reviewed by: [Name]
Period covered: [Date range]

===================================================================

1. COMPLETENESS

NEW ENTRIES:
[ ] All completed studies from period have entries
    Studies completed: [N]
    Entries created: [N]
    Gap: [N] missing

ENTRY FIELDS:
Sample reviewed: [N] entries (10% of total or 10 studies, whichever is larger)

[ ] Study ID present: [N/N]
[ ] Title present: [N/N]
[ ] Date present: [N/N]
[ ] Research lead listed: [N/N]
[ ] Method documented: [N/N]
[ ] Study summary complete: [N/N]
[ ] Key findings documented: [N/N]
[ ] At least one artifact linked: [N/N]
[ ] Tags applied: [N/N]

ISSUES IDENTIFIED:
[List incomplete entries]

ACTION ITEMS:
[Steps to complete missing entries]

===================================================================

2. ACCURACY

LINK CHECKING:
Sample tested: [N] links from [N] entries

Working links: [N] ([%])
Broken links: [N] ([%])

Broken links identified:
- [Entry] - [Link type] - [URL]
- [Entry] - [Link type] - [URL]

ACTION ITEMS:
[Fix broken links]

───────────────────────────────────────────────────────────────

CONTACT INFORMATION:
Sample checked: [N] entries

Current contact info: [N/N]
Outdated contact info: [N/N]

ACTION ITEMS:
[Update contact information]

───────────────────────────────────────────────────────────────

STUDY INFORMATION:
Sample verified: [N] entries

Accurate information: [N/N]
Inaccuracies found: [N/N]

Inaccuracies:
[List issues]

ACTION ITEMS:
[Corrections needed]

===================================================================

3. TAGGING & TAXONOMY

TAG USAGE:
Total tags in system: [N]
Tags used in last 3 months: [N]
Tags not used in 6+ months: [N]

Orphan tags (used once): [N]
- [Tag name]
- [Tag name]

Inconsistent tags identified:
- [Tag A] and [Tag B] seem to mean same thing - merge?
- [Tag C] is ambiguous - clarify definition?

ACTION ITEMS:
[ ] Merge tags: [List mergers]
[ ] Clarify definitions: [List tags needing clarity]
[ ] Remove unused tags: [List tags to retire]
[ ] Add new tags: [List new tags if needed]

───────────────────────────────────────────────────────────────

TAGGING CONSISTENCY:
Sample reviewed: [N] similar studies

[ ] Similar studies use similar tags
[ ] Tagging follows taxonomy
[ ] Required tags present

Inconsistencies found:
[List issues]

ACTION ITEMS:
[Re-tag studies for consistency]

===================================================================

4. USABILITY

SEARCH TESTING:
Test searches performed: [N]

| Search Term | Expected Result | Actual Result | Pass? |
|-------------|-----------------|---------------|-------|
| [Term 1] | [Expected] | [Actual] | [Y/N] |
| [Term 2] | [Expected] | [Actual] | [Y/N] |
| [Term 3] | [Expected] | [Actual] | [Y/N] |

Issues:
[List search problems]

ACTION ITEMS:
[Improvements to search or tagging]

───────────────────────────────────────────────────────────────

NAVIGATION:
[ ] Homepage loads quickly
[ ] Filters work correctly
[ ] Sort options function
[ ] Study pages load quickly
[ ] Links navigate correctly

Issues:
[List navigation problems]

ACTION ITEMS:
[Technical fixes needed]

───────────────────────────────────────────────────────────────

USER FEEDBACK:
Feedback received since last check: [N] pieces of feedback

Themes in feedback:
- [Theme 1]: [N] mentions
- [Theme 2]: [N] mentions

ACTION ITEMS:
[Respond to feedback]

===================================================================

5. USAGE ANALYTICS (if available)

TRAFFIC:
Total views this period: [N]
Unique users: [N]
Average views per user: [N]

Trend: [ ] Increasing [ ] Stable [ ] Decreasing

───────────────────────────────────────────────────────────────

MOST VIEWED:
1. [Study name] - [N] views
2. [Study name] - [N] views
3. [Study name] - [N] views

Least viewed (older than 3 months):
1. [Study name] - [N] views
2. [Study name] - [N] views
3. [Study name] - [N] views

───────────────────────────────────────────────────────────────

SEARCH ANALYTICS:
Top search terms:
1. [Term] - [N] searches
2. [Term] - [N] searches
3. [Term] - [N] searches

Zero-result searches (need attention):
- [Term] - [Why no results?]
- [Term] - [Why no results?]

ACTION ITEMS:
[Improve coverage of zero-result topics]

===================================================================

6. CONTENT QUALITY

STUDY SUMMARIES:
Sample reviewed: [N] summaries

[ ] Well-written: [N/N]
[ ] Follow template: [N/N]
[ ] Appropriate length: [N/N]
[ ] Findings clear: [N/N]

Issues:
[List quality problems]

ACTION ITEMS:
[Rewrite poor summaries; provide guidance to authors]

───────────────────────────────────────────────────────────────

DUPLICATES:
Duplicate or very similar studies identified: [N]

- [Study A] and [Study B] - [Relationship]

ACTION ITEMS:
[ ] Link as related studies
[ ] Add note about relationship
[ ] Consider if one should be archived

===================================================================

7. ARCHIVING

ARCHIVAL CANDIDATES:
Studies older than 5 years: [N]
Studies on retired products: [N]
Superseded studies: [N]

Total candidates for archival: [N]

REVIEWED FOR ARCHIVAL:
[N] studies reviewed

Decision:
- Archive: [N]
- Keep active: [N]
- Delete: [N]

ACTION ITEMS:
[Execute archival decisions]

===================================================================

8. IMPACT TRACKING

STUDIES WITH IMPACT DOCUMENTED:
Recent studies (< 6 months): [N/N] ([%])
Older studies (6-18 months): [N/N] ([%])

Studies needing impact follow-up: [N]

ACTION ITEMS:
[Contact leads to document impact]

===================================================================

OVERALL HEALTH SCORE

COMPLETENESS: [Score /100]
ACCURACY: [Score /100]
USABILITY: [Score /100]
QUALITY: [Score /100]

OVERALL: [Average score /100]

Health Status:
[ ] Excellent (90-100) - Minor maintenance only
[ ] Good (75-89) - Some improvements needed
[ ] Fair (60-74) - Significant improvements needed
[ ] Poor (<60) - Major issues requiring immediate attention

===================================================================

PRIORITY ACTION ITEMS

HIGH PRIORITY (Complete within 1 week):
1. [Action]
2. [Action]
3. [Action]

MEDIUM PRIORITY (Complete within 1 month):
1. [Action]
2. [Action]
3. [Action]

LOW PRIORITY (Complete within quarter):
1. [Action]
2. [Action]

===================================================================

NEXT HEALTH CHECK: [Date] (3 months from now)

===================================================================

REVIEWED BY: _____________________ DATE: _________

APPROVED BY RESEARCH LEAD: _____________________ DATE: _________

===================================================================
```

---

### 5.6 Recommended Tools

**Repository Platforms:**

| Tool | Best For | Pros | Cons | Cost |
|------|----------|------|------|------|
| **Notion** | Small-medium teams; flexible needs | Highly customizable; rich formatting; accessible | Requires setup; not purpose-built | $8-15/user/mo |
| **Airtable** | Structured data; teams wanting database | Database power; views; formulas; relatable | Learning curve; can get complex | $10-20/user/mo |
| **Confluence** | Teams already using Atlassian | Integrates with Jira; familiar to many; wiki structure | Can feel corporate; less visual | $5.50-10/user/mo |
| **Dovetail** | Research-specific needs; established teams | Purpose-built for research; great UX; tagging | Expensive; platform lock-in | Custom pricing |
| **Google Drive + Sheets** | Starting out; budget-conscious | Free; familiar; simple | Manual; limited search; no structure | Free |
| **SharePoint** | Enterprise; Microsoft ecosystem | Enterprise features; integration with MS tools | Clunky UX; steep learning curve | Included with M365 |
| **Custom Database** | Large teams; specific needs; have dev resources | Tailored to needs; full control | Requires development; maintenance | Dev cost |

**Comparison by Team Size:**

| Team Size | Recommended Tool | Why |
|-----------|------------------|-----|
| **1-3 researchers** | Google Drive + Google Sheets | Simple, free, sufficient for low volume |
| **4-8 researchers** | Notion or Airtable | Balance of power and simplicity; affordable |
| **9-15 researchers** | Dovetail or custom Notion setup | Purpose-built; handles volume; good ROI |
| **15+ researchers** | Dovetail, Productboard, or custom solution | Enterprise features; scalability; support |

**Supporting Tools:**

| Purpose | Tools |
|---------|-------|
| **File Storage** | Google Drive, Dropbox, SharePoint, Box |
| **Search Enhancement** | Dovetail, Algolia (if custom) |
| **Visualization** | Miro, Mural (for journey maps, frameworks) |
| **Access Control** | Built into platform; Google Workspace admin |
| **Analytics** | Google Analytics (if web-based); platform built-in |
| **Notifications** | Slack integration; email digests |

---

## 6. Responsibilities

### RACI Matrix

| Activity | Research Lead | Researcher (Lead) | Researcher (Supporting) | Research Operations | Stakeholder |
|----------|---------------|-------------------|------------------------|---------------------|-------------|
| Define repository structure | A/R | C | C | C | I |
| Develop taxonomy | A/R | C | C | C | - |
| Select repository tool | A/C | C | C | R | - |
| Set up repository | C | C | - | A/R | - |
| Create entry standards | A/R | C | C | C | - |
| Add new study entries | A | R | R | S | - |
| Write study summaries | A | R | R | - | - |
| Apply tags to studies | C | R/A | R | C | - |
| Link artifacts | I | R/A | R | S | - |
| Maintain repository | A/R | C | C | R | - |
| Curate and update entries | A/R | C | C | R | - |
| Manage taxonomy | A/R | C | C | C | - |
| Fix broken links | I | S | S | R/A | - |
| Archive old research | A/R | C | - | R | - |
| Train users on repository | A/R | R | R | R | - |
| Monitor usage | A/R | I | - | R | - |
| Conduct meta-analysis | A | R | C | - | C |
| Demonstrate repository value | A/R | C | - | C | I |

**R** = Responsible (does the work)
**A** = Accountable (ultimate ownership)
**C** = Consulted (provides input)
**I** = Informed (kept updated)
**S** = Supports (assists as needed)

### Role Definitions

**Research Lead:**

- Owns repository strategy and vision
- Defines structure and standards
- Develops and maintains taxonomy
- Conducts or oversees curation
- Ensures quality of entries
- Trains team on repository use
- Measures and demonstrates repository value
- Approves major changes to structure
- Champions repository adoption

**Researcher (Lead):**

- Creates repository entries for their studies
- Writes study summaries
- Applies tags according to taxonomy
- Links artifacts and materials
- Updates entries with impact information
- Contributes to meta-analysis
- Uses repository to inform new research
- Provides feedback on repository usability

**Researcher (Supporting):**

- Creates entries when leading research
- Uses repository for research planning
- Applies consistent tagging
- Provides feedback on findability

**Research Operations:**

- Sets up and maintains technical infrastructure
- Manages access and permissions
- Fixes technical issues (broken links, etc.)
- Supports curation activities
- Tracks usage analytics
- Provides technical training
- Manages tool subscriptions and renewals

**Stakeholder:**

- Uses repository to find research
- Provides feedback on utility
- May contribute to meta-analysis discussions
- Champions repository use in their organization

---

## 7. Quality Checks

### 7.1 Entry Quality Check

Before publishing an entry:

```
ENTRY QUALITY CHECKLIST

REQUIRED CONTENT:
[ ] Study ID assigned and correct format
[ ] Study title clear and descriptive
[ ] Date accurate (start and end if applicable)
[ ] Research lead identified
[ ] Method documented
[ ] Study summary complete and follows template
[ ] Key findings documented (minimum 3)
[ ] Research questions stated
[ ] Participant information included (who, how many)
[ ] At least one artifact linked (report, presentation, or summary)

QUALITY STANDARDS:
[ ] Summary is well-written and clear
[ ] Summary is 1-2 pages (not too long or short)
[ ] Findings are specific and evidence-based
[ ] Recommendations are actionable
[ ] No typos or grammatical errors

METADATA:
[ ] Required tags applied (method, type, product area)
[ ] Additional relevant tags applied (3-5 topic tags minimum)
[ ] Tags are consistent with taxonomy
[ ] Related studies linked if applicable

FILES & LINKS:
[ ] All links work (tested)
[ ] Files are properly named
[ ] Files are in accessible formats (PDF, PPT, not proprietary)
[ ] Anonymization complete per UXR-002 (no PII)

FINDABILITY:
[ ] Title uses keywords people would search for
[ ] Summary includes searchable terms
[ ] Tags enable discovery from multiple angles

READY TO PUBLISH: [ ] Yes [ ] No - Needs: _______________
```

### 7.2 Repository Health Check

Quarterly assessment:

```
QUARTERLY REPOSITORY HEALTH CHECK

(See Template 5.5 for complete checklist)

KEY METRICS TO ASSESS:

COMPLETENESS: ___/100
- All studies have entries
- All entries have required fields
- Artifacts are linked

ACCURACY: ___/100
- Links work
- Information is current
- Contact info accurate

USABILITY: ___/100
- Search returns relevant results
- Navigation is intuitive
- Load times acceptable

QUALITY: ___/100
- Summaries are well-written
- Tagging is consistent
- No duplicates

OVERALL HEALTH: ___/100

STATUS:
[ ] Excellent (90-100) [ ] Good (75-89)
[ ] Fair (60-74) [ ] Poor (<60)

ACTION PLAN:
[Priority improvements needed]

NEXT REVIEW: [Date]
```

### 7.3 Usage Quality Check

Monitor if repository is being used effectively:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Active users per month** | 80% of team | [N/N] | [Status] |
| **Searches per user per month** | 3+ | [N] | [Status] |
| **New entries per quarter** | = Studies completed | [N/N] | [Status] |
| **Studies with 0 views (>3 months old)** | <10% | [%] | [Status] |
| **Zero-result searches** | Decreasing | [Trend] | [Status] |
| **User satisfaction** | >4/5 | [Score] | [Status] |

**If Usage Is Low:**

- Survey team: Why aren't they using it?
- Check: Is it easy to access? Is search working?
- Train: Do people know how to use it?
- Promote: Are people aware of its value?
- Improve: Address identified barriers

---

## 8. Related Documents

| Document ID | Title | Relationship |
|-------------|-------|--------------|
| UXR-002 | Data Handling & Privacy | Data retention and anonymization requirements for repository |
| UXR-004 | Research Planning & Scoping | Search repository during planning to build on past research |
| UXR-006 | Note-Taking & Documentation | Documentation standards affect repository entry quality |
| UXR-007 | Analysis & Synthesis | Analysis outputs are primary content for repository |
| UXR-008 | Stakeholder Communication | Communication materials are artifacts stored in repository |

---

## 9. Revision History

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 2026-01-26 | [Name] | Initial release | [Name] |
| | | | | |

### Review Schedule

| Review Type | Frequency | Next Review | Owner |
|-------------|-----------|-------------|-------|
| Repository structure | Annual | 2027-01-26 | Research Lead |
| Taxonomy | Quarterly | 2026-04-26 | Research Lead |
| Entry standards | Semi-annual | 2026-07-26 | Research Lead |
| Tool assessment | Annual | 2027-01-26 | Research Operations |
| Usage and adoption | Quarterly | 2026-04-26 | Research Lead |

---

## 10. Appendix A: Quick Reference Card

### Repository Quick Start

**TO FIND RESEARCH:**
1. Go to [Repository URL]
2. Search by keyword OR filter by product/topic
3. Read study summary
4. Access full artifacts if needed
5. Contact study lead with questions

**TO ADD RESEARCH:**
1. Complete study summary (Template 5.1)
2. Request Study ID from Research Lead
3. Create repository entry with metadata
4. Upload/link artifacts
5. Apply 5-10 tags
6. Publish
7. Time: ~30-45 minutes

**TO MAINTAIN QUALITY:**
- Update entries when impact occurs
- Fix broken links when found
- Keep contact info current
- Archive outdated research
- Curate quarterly

---

### Repository Success Factors

**DISCOVERABILITY = **
- Clear naming
- Rich summaries
- Multiple relevant tags
- Cross-linking
- Good search

**USABILITY = **
- Easy access
- Fast search
- Intuitive navigation
- Complete summaries
- Working links

**VALUE = **
- Research informs decisions
- Prevents duplicate work
- Enables cumulative learning
- Demonstrates impact
- Preserved knowledge

---

## Appendix B: Common Repository Challenges

**CHALLENGE 1: Low Adoption**

❌ Problem: Team doesn't use repository; research stays in silos

✓ Solutions:
- Make repository required part of workflow
- Demonstrate value with success stories
- Integrate into meetings (project planning, retrospectives)
- Train new team members early
- Get executive champion
- Make it easier to use than alternatives

---

**CHALLENGE 2: Incomplete Entries**

❌ Problem: Studies added to repository but with minimal information

✓ Solutions:
- Clear minimum requirements
- Templates make it easy
- Peer review before publishing
- Research Lead spot checks
- Recognition for complete, high-quality entries
- Block on publishing: Can't publish incomplete entry

---

**CHALLENGE 3: Can't Find What You Need**

❌ Problem: Research exists but people can't find it

✓ Solutions:
- Improve tagging (more tags, better taxonomy)
- Use keywords in titles and summaries
- Cross-link related studies
- Featured research on homepage
- Train on effective searching
- Monitor zero-result searches; address gaps

---

**CHALLENGE 4: Taxonomy Chaos**

❌ Problem: Too many tags, inconsistent use, unclear definitions

✓ Solutions:
- Establish controlled vocabulary
- Document tag definitions
- Limit who can create new tags
- Regular tag consolidation
- Guidance on tagging
- Review and merge quarterly

---

**CHALLENGE 5: Outdated Information**

❌ Problem: Repository fills with old, irrelevant research

✓ Solutions:
- Regular archiving process
- Flag studies as "Historical"
- Update entry when context changes significantly
- Link to superseding research
- Periodic review of old studies
- Retention policy per UXR-002

---

**CHALLENGE 6: "Not Built Here" Syndrome**

❌ Problem: People only trust research they conducted themselves

✓ Solutions:
- Culture change: Research is team asset, not individual work
- Cross-functional involvement in research
- Transparency about methods and limitations
- Easy way to ask questions about past research
- Leadership modeling: Reference repository research
- Celebrate building on past research

---

**CHALLENGE 7: Repository Becomes Graveyard**

❌ Problem: Research added but never used; feels like compliance exercise

✓ Solutions:
- Proactively surface relevant research
- Monthly digest: "Research relevant to your work"
- Integrate in planning meetings
- Success stories of repository driving decisions
- Make research summaries compelling and actionable
- Reduce friction: Make it easier than alternatives

---

**CHALLENGE 8: Tool Limitations**

❌ Problem: Repository tool doesn't meet team needs

✓ Solutions:
- Assess needs; choose appropriate tool for team size/needs
- Customize within tool capabilities
- Workarounds for limitations (e.g., supplemental tools)
- Document feature requests
- Evaluate alternatives annually
- Sometimes simple is better than feature-rich

---

**CHALLENGE 9: Maintenance Burden**

❌ Problem: Repository requires too much upkeep; falls behind

✓ Solutions:
- Automate where possible (e.g., auto-tagging, auto-linking)
- Dedicated Research Ops role if volume justifies
- Distributed responsibility (everyone maintains their entries)
- Scheduled curation time (not ad hoc)
- Right-size: Don't over-engineer for small team
- Tool choice: Pick one with low maintenance overhead

---

**CHALLENGE 10: Knowledge Leaves with People**

❌ Problem: When researcher leaves, institutional knowledge goes too

✓ Solutions:
- THIS IS WHY REPOSITORY EXISTS
- Ensure all research documented before departure
- Knowledge transfer includes repository walkthrough
- Document context and decisions, not just findings
- Comprehensive study summaries
- Detailed methodology documentation
- Repository enables continuity

---

## Appendix C: FAQ

**Q: How quickly should I add research to the repository?**

A:
- **Target:** Within 1 week of completing research
- **Ideal:** Create draft entry at study start; publish when complete
- **Why:** Ensures research is captured while fresh; makes it available quickly

**Q: How much detail should study summaries include?**

A:
- **Target length:** 1-2 pages
- **Include:** Purpose, method, participants, 3-5 key findings, top recommendations, impact
- **Don't include:** Detailed methodology, all findings, every quote
- **Full report:** Link to full report for details; summary is overview only

**Q: What if I can't find research I know exists?**

A:
- **Try different search terms** (synonyms, related concepts)
- **Browse by related topics** or product areas
- **Filter by date** if you remember when it was done
- **Ask in Slack** - someone may know
- **Contact Research Lead** - they may know or help search
- **May indicate:** Tagging needs improvement

**Q: Should I add research from before the repository existed?**

A:
- **Yes**, prioritize recent and high-impact studies
- **Start with:** Last 12-24 months of research
- **Then:** Add older research as time allows or when referenced
- **Use tiered approach:** Full entry for priority; basic entry for others
- **Don't let perfection block:** Basic entry is better than none

**Q: What if research was inconclusive or didn't find clear answers?**

A:
- **Still add it!** Null results are valuable
- **Document:** What was learned, even if inconclusive
- **Note:** Areas of uncertainty or ambiguity
- **Value:** Prevents others from making same assumptions; shows gaps
- **Be honest:** "Research didn't provide clear answer on [X]"

**Q: Can I update an entry after it's published?**

A:
- **Yes,** entries should be living documents
- **Update when:**
  - Impact occurs (decision made, action taken)
  - Follow-up research conducted
  - Errors found
  - Additional artifacts created
- **Track changes:** Note what was updated and when
- **Version if major:** Significant changes may warrant version increment

**Q: Who can access the repository?**

A:
- **Depends on your organization's policy**
- **Typically:**
  - Study summaries and final outputs: Whole organization
  - Raw data (notes, transcripts): Research team only
  - Drafts: Research team only
- **Check:** Access control section (4.5) for your setup

**Q: How do I cite research from the repository?**

A:
- **Format:** [Study ID] - [Study Name] - [Research Lead] - [Date]
- **Example:** UXR-2024-Q2-003 - Mobile Navigation Study - J. Smith - June 2024
- **Link:** Provide repository link to entry
- **Context:** Note key finding being referenced

**Q: What if research contradicts what we previously found?**

A:
- **Both studies should be in repository**
- **Cross-link:** Note the contradiction in both entries
- **Explain:** Document possible reasons for difference (context, sample, time)
- **Investigate:** May warrant follow-up research to understand why
- **Value:** Contradictions are interesting and worthy of exploration

**Q: How long should we keep research in the repository?**

A:
- **Follow UXR-002 retention policies**
- **General guidance:**
  - Current research (0-2 years): Keep active
  - Relevant research (2-5 years): Keep, flag age
  - Historical (5+ years): Archive or flag as historical
  - Superseded: Link to newer research
- **Don't delete** unless required by policy; archive instead

**Q: Can I add research from other teams or external sources?**

A:
- **Internal research:** Yes, if you have permission
- **External research:** Maybe, consider:
  - Do you have rights to share it?
  - Is it relevant and credible?
  - Better to link than upload (copyright)
  - Note it's external research
- **Vendor research:** Only if you own it per contract

---

**Document Control:**
- This document is controlled. Printed copies are for reference only.
- Current version available at: [Insert location]
- Questions: Contact Research Lead

**Emergency Contact:**
- Repository access issues: Research Operations
- Adding research to repository: Research Lead
- Repository strategy: Research Lead
