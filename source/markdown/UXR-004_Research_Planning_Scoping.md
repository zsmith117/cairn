# UXR-004: Research Planning & Scoping Standard Operating Procedure

**Document ID:** UXR-004
**Version:** 1.0
**Effective Date:** January 22, 2026
**Last Review:** January 22, 2026
**Document Owner:** UX Research Lead
**Classification:** Internal Use Only

---

## 1. Purpose

This Standard Operating Procedure establishes the requirements and procedures for planning and scoping UX research studies. It ensures that:

- Research objectives are clearly defined and aligned with business needs
- Study scope is appropriately sized and documented before execution begins
- Stakeholder expectations are set and managed throughout the research process
- Research methods are selected based on objectives, constraints, and context
- Timelines and resources are realistically estimated
- Scope changes are managed through a controlled process
- Downstream processes (recruitment, consent, data handling) are properly prepared

**Why This Matters:**

Effective planning is the foundation of successful research. Poor planning leads to:
- Scope creep that extends timelines and consumes unbudgeted resources
- Misaligned expectations between researchers and stakeholders
- Wrong method selection that fails to answer research questions
- Rushed recruitment with unqualified participants
- Findings that don't inform the decisions they were intended to support
- Wasted investment when research doesn't drive action

---

## 2. Scope

**This SOP applies to:**

- All UX research studies requiring formal planning documentation
- Generative research (discovery, exploratory, foundational)
- Evaluative research (usability testing, concept testing)
- Quantitative research (surveys, analytics studies)
- Mixed-methods research combining multiple approaches
- Field studies and site visits
- Longitudinal studies (diary studies, panels)

**This SOP covers:**

- Research request intake and initial assessment
- Defining research objectives and questions
- Method selection and justification
- Participant requirements definition
- Timeline and resource planning
- Stakeholder alignment and expectation setting
- Research plan documentation
- Scope change management

**Out of scope:**

- Quick pulse checks (<3 participants, informal feedback)
- Desk research and secondary research (literature reviews, competitive analysis)
- A/B testing and experimentation (see Product Analytics processes)
- Research that uses only existing data (no new data collection)
- Ad-hoc stakeholder conversations not formally scoped as research

---

## 3. Definitions

| Term | Definition |
|------|------------|
| **Research Objective** | A clear statement of what the research aims to learn or accomplish, tied to a business or design decision |
| **Research Question** | A specific question that the research will answer, derived from the research objective |
| **Hypothesis** | A testable prediction about what the research will find, used primarily in evaluative research |
| **Research Brief** | A concise document (typically 1 page) summarizing the research request and initial assessment |
| **Research Plan** | A comprehensive document detailing all aspects of a planned study, serving as the contract between researcher and stakeholders |
| **Study Scope** | The defined boundaries of a research study, including what will and will not be investigated |
| **Scope Creep** | Uncontrolled expansion of study scope beyond original boundaries without corresponding adjustments to timeline or resources |
| **Research Method** | The systematic approach used to collect data (e.g., interviews, usability testing, surveys) |
| **Triangulation** | Using multiple methods, sources, or researchers to validate findings and increase confidence |
| **Saturation** | The point at which additional data collection yields diminishing new insights |
| **Research Sponsor** | The executive or leader who authorizes and funds the research |
| **Decision Stakeholder** | The person or team who will use the research findings to make decisions |
| **Feasibility Assessment** | An evaluation of whether a proposed study can be executed given constraints |
| **Study Protocol** | The detailed procedures for conducting the research, including scripts, guides, and tasks |
| **Analysis Plan** | A pre-defined approach for how data will be analyzed after collection |
| **Deliverables** | The tangible outputs of research (reports, presentations, artifacts) provided to stakeholders |

---

## 4. Procedure

### 4.1 Research Request Intake

#### 4.1.1 Receiving Research Requests

Research requests can be submitted through:
- Formal intake form (preferred)
- Stakeholder meetings or planning sessions
- Slack/email requests (document immediately)
- Researcher identification during product team participation

**Initial Information to Capture:**

| Field | Purpose | Example |
|-------|---------|---------|
| Requester name and role | Point of contact | PM, Design Lead |
| Business context | Why this research matters | Launching Q2, retention declining |
| Decision to be made | What will change based on findings | Feature prioritization, design direction |
| Target users | Who we need to understand | Enterprise admins, new users |
| Timeline expectations | When decisions need to be made | Before sprint planning (Feb 15) |
| Prior research | What's already known | Did interviews 6 months ago |
| Constraints | Budget, access, timeline limits | Limited customer access |

#### 4.1.2 Initial Triage

Upon receiving a request, assess within 48 hours:

**Triage Decision Matrix:**

| Urgency | Strategic Value | Decision |
|---------|-----------------|----------|
| High (blocking decision) | High | Fast-track; prioritize resources |
| High | Low | Quick method; manage expectations |
| Low | High | Standard planning; queue appropriately |
| Low | Low | Defer or decline; explain rationale |

**Questions to Answer:**

1. Is this a research question? (vs. already known, or a design/product decision)
2. Do we have existing research that answers this?
3. Is this feasible given our constraints?
4. Who needs to be involved in planning?
5. What is the appropriate scope for this request?

#### 4.1.3 Creating the Research Brief

For requests that proceed, create a one-page Research Brief:

```
RESEARCH BRIEF

Date: _______________
Requester: _______________
Researcher: _______________

BACKGROUND
[2-3 sentences on context and why this research is needed]

BUSINESS DECISION
[Specific decision this research will inform]

INITIAL RESEARCH QUESTIONS
1. _______________
2. _______________
3. _______________

PRELIMINARY APPROACH
- Method consideration: _______________
- Participants: _______________
- Estimated timeline: _______________

CONSTRAINTS
- Timeline: _______________
- Budget: _______________
- Access: _______________

NEXT STEPS
[ ] Stakeholder alignment meeting scheduled
[ ] Full research plan development
[ ] Proceed directly to execution (small study)
```

---

### 4.2 Defining Research Objectives

#### 4.2.1 Understanding Business Context

Before defining research objectives, understand:

**Questions to Ask Stakeholders:**

| Question | Why It Matters |
|----------|----------------|
| What decision will this research inform? | Focuses the research on actionable outcomes |
| What happens if we don't do this research? | Assesses value and urgency |
| What do you think you already know? | Identifies assumptions to validate |
| What would change your mind? | Reveals what findings matter |
| Who else cares about this? | Identifies additional stakeholders |
| When do you need to decide? | Sets timeline constraints |
| What's the budget/resource reality? | Sets scope constraints |

#### 4.2.2 Crafting Research Objectives

**Research Objective Structure:**

Good research objectives follow this pattern:

> **Understand** [what aspect] **of** [target users] **in order to** [business/design decision]

**Examples:**

| Poor Objective | Better Objective |
|----------------|------------------|
| "Understand user needs" | "Understand how warehouse managers prioritize tasks in order to redesign the daily dashboard" |
| "Test the new design" | "Evaluate whether the new checkout flow reduces errors for first-time users to decide on launch readiness" |
| "Learn about users" | "Understand the workflow and pain points of procurement managers in order to identify automation opportunities" |

**Objective Quality Checklist:**

- [ ] Tied to a specific decision or action
- [ ] Identifies the target user/participant
- [ ] Scoped to what can be learned in this study
- [ ] Measurable or observable outcomes
- [ ] Not answerable by existing data alone

#### 4.2.3 Developing Research Questions

Translate objectives into specific research questions:

**From Objective to Questions:**

| Objective | Research Questions |
|-----------|-------------------|
| Understand how warehouse managers prioritize tasks | - What factors influence task prioritization decisions? |
| | - What information do managers need to make priority decisions? |
| | - How do current tools support or hinder prioritization? |
| | - What workarounds exist for prioritization gaps? |

**Research Question Hierarchy:**

| Type | Description | Example |
|------|-------------|---------|
| **Primary Questions** | Must answer to meet objective | "What are the key pain points in the returns workflow?" |
| **Secondary Questions** | Important but not essential | "How do pain points vary by retailer size?" |
| **Exploratory Questions** | Nice to know if time permits | "How do expectations of Gen Z differ from older cohorts?" |

#### 4.2.4 Formulating Hypotheses (When Appropriate)

Use hypotheses primarily for evaluative research:

**When to Use Hypotheses:**

- Usability testing with specific success criteria
- Concept testing with prediction of preference
- Validation research testing assumptions
- A/B comparative testing

**Hypothesis Structure:**

> **We believe that** [proposed change/concept] **will** [expected outcome] **because** [rationale based on prior research/data]

**Example:**

> We believe that adding progress indicators to the checkout flow will reduce abandonment by 15% because prior research showed users were uncertain about how many steps remained.

---

### 4.3 Method Selection

#### 4.3.1 Method Selection Criteria

Select methods based on:

| Factor | Consideration |
|--------|---------------|
| Research questions | What type of data answers these questions? |
| Available time | Which methods fit the timeline? |
| Budget | What can we afford? |
| Participant access | Who can we realistically reach? |
| Existing knowledge | Do we need exploration or validation? |
| Decision context | What evidence will stakeholders trust? |

#### 4.3.2 Method Options and Use Cases

**Core Research Methods:**

| Method | Best For | Output | Typical Timeline | Participants |
|--------|----------|--------|------------------|--------------|
| **Stakeholder Interviews** | Defining scope, understanding context | Internal alignment | 1-2 weeks | 5-10 |
| **User Interviews** | Deep understanding, generative insights | Behavioral insights, needs | 2-4 weeks | 8-15 |
| **Contextual Inquiry** | Understanding workflows in context | Process maps, pain points | 3-6 weeks | 6-12 |
| **Usability Testing** | Evaluating designs, finding issues | Issue list, success rates | 1-3 weeks | 5-8 per design |
| **Concept Testing** | Validating ideas early | Concept feedback, preference | 1-2 weeks | 6-10 |
| **Card Sorting** | Information architecture | Category structures | 1-2 weeks | 15-30 |
| **Surveys** | Quantifying attitudes, behaviors | Statistical data | 2-4 weeks | 100-500+ |
| **Diary Studies** | Longitudinal behavior, real context | Behavior patterns over time | 3-8 weeks | 10-20 |
| **Field Studies/Site Visits** | Industrial environments, complex contexts | Contextual understanding | 4-8 weeks | 4-8 sites |
| **Focus Groups** | Exploring reactions, group dynamics | Discussion themes | 2-3 weeks | 6-8 per group |

#### 4.3.3 Mixed Methods Considerations

Consider combining methods when:
- Research questions span "what" (quantitative) and "why" (qualitative)
- Findings need validation from multiple angles
- Stakeholders require different types of evidence
- Complex behaviors need both depth and breadth

**Common Mixed Method Approaches:**

| Approach | Methods Combined | Use Case |
|----------|------------------|----------|
| **Exploratory Sequential** | Interviews → Survey | Understand deeply, then quantify |
| **Explanatory Sequential** | Survey → Interviews | Identify patterns, then explain |
| **Convergent** | Usability + Interviews (parallel) | Evaluate what + understand why |
| **Embedded** | Diary Study + Periodic Interviews | Track behavior + check in for depth |

#### 4.3.4 B2B and Industrial Research Considerations

When selecting methods for B2B/industrial contexts:

| Consideration | Implication |
|---------------|-------------|
| Limited participant pool | Maximize learning per participant; consider longitudinal relationships |
| Complex buying decisions | Include multiple roles/stakeholders in sample |
| Long sales cycles | Align research with customer relationship touchpoints |
| Domain expertise required | Budget for researcher preparation time |
| Site access complexity | Plan longer timelines; coordinate with account teams |
| Proprietary information | Select methods that respect confidentiality constraints |

**For field research and site visits**, see UXR-001 Section 4.5.1 for safety requirements and advance coordination procedures.

---

### 4.4 Defining Participant Requirements

#### 4.4.1 Identifying Target Population

Document the target population by answering:

| Question | Documentation |
|----------|---------------|
| Who are the intended users of this product/feature? | User type(s) and context |
| What behaviors or experiences must participants have? | Required experience level |
| What segments or variations matter for this research? | Quota categories |
| Who should be excluded and why? | Exclusion criteria |
| How representative does the sample need to be? | Generalizability requirements |

#### 4.4.2 Setting Recruitment Criteria

Translate target population into recruitment criteria:

See UXR-003 Section 4.1 for detailed guidance on:
- Defining primary (must-have) vs. secondary (nice-to-have) criteria
- Creating exclusion criteria
- Developing screener questionnaires

**Criteria Definition in Research Plan:**

Include in the research plan:
- Primary criteria (non-negotiable)
- Secondary criteria (preferred)
- Quota requirements (distribution targets)
- Exclusion criteria (disqualifying factors)
- Rationale for each criterion

#### 4.4.3 Determining Sample Size

Base sample size on method and research goals:

See UXR-003 Section 4.1.2 for detailed sample size recommendations by method.

**Sample Size Decision Factors:**

| Factor | Larger Sample | Smaller Sample |
|--------|---------------|----------------|
| Population variability | High variation expected | Homogeneous population |
| Confidence requirements | Quantitative precision needed | Qualitative depth sufficient |
| Resource availability | Budget and time allow | Constrained resources |
| Analysis needs | Subgroup comparisons planned | Overall patterns sufficient |

---

### 4.5 Planning Timeline and Resources

#### 4.5.1 Timeline Estimation

**Research Phase Durations:**

| Phase | Activities | Typical Duration |
|-------|------------|------------------|
| **Planning** | Stakeholder alignment, research plan, materials | 1-2 weeks |
| **Recruitment** | Sourcing, screening, scheduling | 1-3 weeks |
| **Execution** | Data collection sessions | 1-3 weeks |
| **Analysis** | Synthesis, pattern identification | 1-2 weeks |
| **Reporting** | Documentation, presentation | 1 week |
| **Buffer** | Delays, rework, additional sessions | 0.5-1 week |

**Timeline Quick Estimates:**

| Study Type | Minimum Timeline | Standard Timeline |
|------------|------------------|-------------------|
| Quick usability test (5 participants) | 2 weeks | 3 weeks |
| User interviews (10 participants) | 3 weeks | 4-5 weeks |
| Survey (200 responses) | 2 weeks | 3-4 weeks |
| Field study (4 sites) | 6 weeks | 8-10 weeks |
| Mixed methods | 5 weeks | 8-12 weeks |

**Timeline Risk Factors:**

| Risk Factor | Impact | Mitigation |
|-------------|--------|------------|
| Hard-to-recruit participants | +1-2 weeks | Start recruitment early; use multiple sources |
| Stakeholder availability | +1 week | Schedule alignment meetings early |
| Complex logistics (travel, sites) | +2-4 weeks | Build extra buffer; have backup plans |
| Holiday/vacation periods | +1-2 weeks | Check calendars; adjust expectations |
| New method for team | +1 week | Build in learning time |

#### 4.5.2 Resource and Budget Planning

**Standard Resource Requirements:**

| Resource | Consideration |
|----------|---------------|
| Researcher time | Primary resource; protect capacity |
| Participant incentives | Budget based on method and sample |
| Recruitment costs | Panel fees, agency fees if applicable |
| Tools and software | Recording, analysis, survey platforms |
| Travel and logistics | For field research, in-person sessions |
| Transcription | If verbatim transcripts needed |
| External support | Moderator, note-taker, translator |

**Budget Estimation Template:**

| Category | Item | Quantity | Unit Cost | Total |
|----------|------|----------|-----------|-------|
| Incentives | Participant thank-you | [N] | $[X] | $ |
| Recruitment | Panel/agency fees | [N] | $[X] | $ |
| Tools | Survey platform | 1 | $[X] | $ |
| Travel | Site visits | [N] trips | $[X] | $ |
| Other | [Specify] | | | $ |
| **Total** | | | | **$** |

#### 4.5.3 Risk Identification

Document risks during planning:

| Risk Category | Example Risks | Probability | Impact | Mitigation |
|---------------|---------------|-------------|--------|------------|
| Recruitment | Can't find enough qualified participants | Medium | High | Start early; multiple sources; adjust criteria |
| Timeline | Stakeholder delays in review | Medium | Medium | Set clear deadlines; escalation path |
| Budget | Incentives higher than estimated | Low | Medium | Research market rates early; get approval |
| Quality | Participants don't match criteria | Low | High | Robust screening; verification |
| Scope | New questions emerge mid-study | High | Medium | Scope change process; backlog additions |
| External | Customer unavailable (B2B) | Medium | High | Over-recruit; backup participants |

---

### 4.6 Stakeholder Alignment

#### 4.6.1 Identifying Stakeholders

Map stakeholders for each study:

| Stakeholder Type | Role in Research | Typical Representatives |
|------------------|------------------|------------------------|
| **Research Sponsor** | Authorizes, funds, accountable for action | VP/Director, Business Owner |
| **Decision Stakeholders** | Will use findings to make decisions | PM, Design Lead, Engineering Lead |
| **Subject Matter Experts** | Provide context, review materials | Domain experts, current team |
| **Informed Stakeholders** | Need awareness of findings | Adjacent teams, leadership |
| **Gatekeepers** | Control access to participants | Account managers, CS, partners |

#### 4.6.2 Aligning on Expectations

**Pre-Study Alignment Checklist:**

| Topic | Aligned? | Documentation |
|-------|----------|---------------|
| Research objectives | [ ] | Research plan section |
| Research questions | [ ] | Research plan section |
| Method and approach | [ ] | Research plan section |
| Timeline and milestones | [ ] | Research plan section |
| Deliverables and format | [ ] | Research plan section |
| Decision process | [ ] | Meeting notes |
| Roles and responsibilities | [ ] | Research plan section |
| Communication cadence | [ ] | Research plan section |

**Stakeholder Alignment Meeting Agenda:**

1. Research background and business context (5 min)
2. Research objectives and questions (10 min)
3. Proposed approach and method (10 min)
4. Timeline and milestones (5 min)
5. Roles and expectations (5 min)
6. Questions and concerns (10 min)
7. Confirm approval and next steps (5 min)

#### 4.6.3 Managing Stakeholder Conflicts

When stakeholders have conflicting priorities:

| Conflict Type | Resolution Approach |
|---------------|---------------------|
| Different research questions | Prioritize by decision urgency; scope secondary questions for later |
| Method disagreement | Present trade-offs objectively; defer to researcher expertise |
| Timeline pressure | Show impact of compression on quality; offer alternatives |
| Budget constraints | Propose scaled approaches; clarify what can't be done |
| Scope expansion requests | Use scope change process; discuss trade-offs |

**Escalation Path:**

If conflicts cannot be resolved at working level:
1. Document the conflict and positions
2. Present options with trade-offs to research sponsor
3. Request a decision with clear rationale
4. Document the decision and proceed

---

### 4.7 Creating the Research Plan Document

#### 4.7.1 Research Plan Components

**Required Sections:**

| Section | Contents |
|---------|----------|
| **Overview** | Study name, researcher, sponsor, dates |
| **Background** | Business context, prior research, why now |
| **Research Objectives** | What we aim to learn and why |
| **Research Questions** | Specific questions to answer |
| **Method** | Approach, rationale for selection |
| **Participants** | Target population, criteria, sample size |
| **Timeline** | Key milestones and dates |
| **Deliverables** | What stakeholders will receive |
| **Resources** | Budget, tools, support needed |
| **Risks** | Identified risks and mitigations |
| **Stakeholders** | Who is involved and how |
| **Approval** | Sign-off from sponsor |

**Optional Sections (As Needed):**

- Hypotheses (for evaluative research)
- Stimulus materials description
- Analysis plan
- Ethical considerations
- Logistics details (for field research)

#### 4.7.2 Research Plan Approval Process

**Approval Workflow:**

```
[Draft Plan] → [Peer Review] → [Stakeholder Review] → [Sponsor Approval] → [Execution]
                  (1-2 days)       (2-3 days)          (1-2 days)
```

**Approval Thresholds:**

| Study Type | Approval Required |
|------------|-------------------|
| Quick study (<5 participants, <1 week) | Research Lead awareness |
| Standard study | Research Lead + Sponsor approval |
| Large study (>$5K, >20 participants) | Research Lead + Sponsor + Resource approval |
| Field research/site visits | Research Lead + Sponsor + Safety review |
| External participants (new segment) | Research Lead + Legal review |

---

### 4.8 Scope Change Management

#### 4.8.1 Identifying Scope Changes

Scope changes include:

| Change Type | Examples |
|-------------|----------|
| **Question expansion** | Adding new research questions |
| **Participant changes** | Different criteria, more participants |
| **Method addition** | Adding a survey to interview study |
| **Timeline extension** | Additional sessions, delayed start |
| **Deliverable changes** | New output formats, additional analyses |

**Triggers for Scope Change Assessment:**

- Stakeholder requests mid-study
- Findings suggest new directions
- Recruitment difficulties requiring criteria changes
- External events changing context
- Resource availability changes

#### 4.8.2 Evaluating Scope Changes

**Scope Change Assessment Questions:**

| Question | Assessment |
|----------|------------|
| Does this change the research objectives? | If yes, requires sponsor approval |
| What is the impact on timeline? | Quantify delay |
| What is the impact on budget? | Quantify cost |
| What is the impact on quality? | Assess trade-offs |
| Can this be addressed in a follow-up study? | Consider deferral |
| What is the cost of NOT making this change? | Assess value of change |

**Decision Framework:**

| Timeline Impact | Budget Impact | Decision |
|-----------------|---------------|----------|
| None | None | Researcher discretion |
| <20% | <20% | Research Lead approval |
| 20-50% | 20-50% | Sponsor approval required |
| >50% | >50% | Replan as new study |

#### 4.8.3 Documenting Scope Changes

For approved changes, document:

```
SCOPE CHANGE RECORD

Study: _______________
Date: _______________
Change #: _______________

CHANGE DESCRIPTION
[What is being changed]

RATIONALE
[Why this change is needed]

IMPACT ASSESSMENT
- Timeline: [Impact]
- Budget: [Impact]
- Quality: [Impact]

APPROVAL
Approved by: _______________
Date: _______________

UPDATED PLAN REFERENCE
[Link or location of updated plan]
```

---

### 4.9 Connecting to Downstream Processes

#### 4.9.1 Recruitment Planning Handoff

When research plan is approved, prepare for recruitment:

**Information to Hand Off:**

| Item | Reference |
|------|-----------|
| Recruitment criteria (primary, secondary, exclusion) | Research plan Section [X] |
| Sample size and quotas | Research plan Section [X] |
| Session format and duration | Research plan Section [X] |
| Timeline for recruitment completion | Research plan Section [X] |
| Incentive amount and type | Research plan Section [X] |
| Special requirements (B2B, site visits) | Research plan Section [X] |

See UXR-003 Section 4.1 for recruitment and screening procedures.

#### 4.9.2 Consent Planning

Plan consent requirements during research planning:

| Consideration | Action | Reference |
|---------------|--------|-----------|
| Consent form selection | Identify appropriate template | UXR-001 Section 4.1 |
| Recording consent | Determine if recording needed | UXR-001 Section 4.1.2 |
| Photo/video release | Add if capturing images | UXR-001 Section 4.1.4 |
| NDA requirements (B2B) | Assess proprietary information | UXR-001 Section 4.1.5 |
| Remote consent process | Plan for remote participants | UXR-001 Section 4.2 |

#### 4.9.3 Data Handling Planning

Plan data handling requirements:

| Consideration | Action | Reference |
|---------------|--------|-----------|
| Data classification | Determine sensitivity level | UXR-002 Section 4.1 |
| Storage requirements | Identify appropriate storage | UXR-002 Section 4.2 |
| Retention period | Document in research plan | UXR-002 Section 4.5 |
| Access controls | Identify who needs access | UXR-002 Section 4.3 |
| Deletion plan | Plan end-of-study cleanup | UXR-002 Section 4.10 |

---

## 5. Templates and Tools

### Template 5.1: Research Brief Template

```
RESEARCH BRIEF

Project: _______________
Date: _______________
Requester: _______________
Researcher: _______________

BACKGROUND
[What's happening that prompts this research request?]
_______________________________________________
_______________________________________________

BUSINESS DECISION
This research will inform the decision to:
_______________________________________________

KEY QUESTIONS
What do we need to learn?
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

WHAT WE THINK WE KNOW
[Current assumptions or hypotheses]
- _______________________________________________
- _______________________________________________

TIMELINE
Decision needed by: _______________
Research completion target: _______________

CONSTRAINTS
- Budget: _______________
- Participant access: _______________
- Other: _______________

EXISTING RESEARCH
[ ] Checked repository - relevant studies: _______________
[ ] No prior research found

PRELIMINARY ASSESSMENT
Recommended approach: _______________
Estimated effort: [ ] Small (1-2 weeks) [ ] Medium (3-5 weeks) [ ] Large (6+ weeks)

NEXT STEPS
[ ] Proceed to full research plan
[ ] Need more information: _______________
[ ] Defer: _______________
[ ] Decline (reason): _______________

APPROVED TO PROCEED: _______________ DATE: _______________
```

---

### Template 5.2: Research Plan Template

```
RESEARCH PLAN

Study Name: _______________
Study Code: _______________
Version: _______________
Date: _______________

STUDY TEAM
- Lead Researcher: _______________
- Supporting Researcher(s): _______________
- Research Sponsor: _______________
- Key Stakeholders: _______________

1. BACKGROUND AND CONTEXT
[Why is this research being conducted? What business context drives it?]
_______________________________________________
_______________________________________________

Prior research:
- [Study name, date, key findings]
- [Study name, date, key findings]

2. RESEARCH OBJECTIVES
This research aims to:
1. _______________________________________________
2. _______________________________________________

In order to inform the decision to:
_______________________________________________

3. RESEARCH QUESTIONS

Primary Questions (must answer):
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Secondary Questions (important):
4. _______________________________________________
5. _______________________________________________

Exploratory Questions (if time permits):
6. _______________________________________________

4. HYPOTHESES (if applicable)
- H1: _______________________________________________
- H2: _______________________________________________

5. METHODOLOGY

5.1 Method Selection
Method: _______________
Rationale: _______________________________________________

5.2 Participant Requirements

Target Population:
_______________________________________________

Recruitment Criteria:

| Criterion Type | Criteria |
|----------------|----------|
| Must Have | |
| Nice to Have | |
| Quotas | |
| Exclusions | |

Sample Size: _______________ participants
Rationale: _______________________________________________

5.3 Session Details
- Format: [ ] Remote [ ] In-person [ ] Field visit
- Duration: _______________ minutes
- Recording: [ ] Audio [ ] Video [ ] Screen [ ] None
- Tools: _______________

6. TIMELINE

| Milestone | Target Date |
|-----------|-------------|
| Plan approved | |
| Recruitment begins | |
| Recruitment complete | |
| Sessions begin | |
| Sessions complete | |
| Analysis complete | |
| Findings delivered | |

7. DELIVERABLES

| Deliverable | Format | Audience | Date |
|-------------|--------|----------|------|
| | | | |

8. RESOURCES AND BUDGET

| Category | Item | Cost |
|----------|------|------|
| Incentives | | |
| Recruitment | | |
| Tools | | |
| Travel | | |
| **Total** | | |

9. RISKS AND MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| | | | |

10. COMMUNICATION PLAN
- Status updates: _______________
- Stakeholder check-ins: _______________
- Issue escalation: _______________

11. ETHICAL CONSIDERATIONS
- Consent approach: _______________
- Data handling: _______________
- Participant considerations: _______________

APPROVALS

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Research Lead | | | |
| Research Sponsor | | | |
| Other (if required) | | | |
```

---

### Template 5.3: Method Selection Decision Matrix

```
METHOD SELECTION MATRIX

Study: _______________
Date: _______________

RESEARCH QUESTIONS SUMMARY
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

CONSTRAINTS
- Timeline: _______________
- Budget: _______________
- Participant access: _______________
- Other: _______________

METHOD EVALUATION

| Criterion | Weight | User Interviews | Usability Testing | Survey | Field Study |
|-----------|--------|-----------------|-------------------|--------|-------------|
| Answers RQ1 | 5 | | | | |
| Answers RQ2 | 5 | | | | |
| Answers RQ3 | 5 | | | | |
| Fits timeline | 4 | | | | |
| Fits budget | 3 | | | | |
| Participant feasibility | 4 | | | | |
| Stakeholder confidence | 3 | | | | |
| **Weighted Total** | | | | | |

Scoring: 1 = Poor fit, 2 = Partial fit, 3 = Good fit

SELECTED METHOD: _______________

RATIONALE
_______________________________________________
_______________________________________________

ALTERNATIVE CONSIDERED
_______________________________________________

APPROVED BY: _______________ DATE: _______________
```

---

### Template 5.4: Stakeholder Alignment Checklist

```
STAKEHOLDER ALIGNMENT CHECKLIST

Study: _______________
Researcher: _______________
Date: _______________

STAKEHOLDER MAP

| Stakeholder | Role | Level of Involvement | Aligned? |
|-------------|------|---------------------|----------|
| | Sponsor | High | [ ] |
| | Decision Stakeholder | High | [ ] |
| | Subject Matter Expert | Medium | [ ] |
| | Informed | Low | [ ] |

ALIGNMENT TOPICS

| Topic | Discussion Date | Agreement Documented |
|-------|-----------------|---------------------|
| Research objectives | | [ ] |
| Research questions | | [ ] |
| Method selection | | [ ] |
| Timeline | | [ ] |
| Deliverables | | [ ] |
| Budget/resources | | [ ] |
| Roles and responsibilities | | [ ] |
| Communication cadence | | [ ] |
| Decision process for findings | | [ ] |

OUTSTANDING CONCERNS

| Concern | Owner | Resolution Plan | Due Date |
|---------|-------|-----------------|----------|
| | | | |

ALIGNMENT CONFIRMATION

All key stakeholders aligned on research plan: [ ] Yes [ ] No

If no, escalation plan:
_______________________________________________

Research Sponsor Sign-off: _______________ Date: _______________
```

---

### Template 5.5: Timeline Planning Template

```
RESEARCH TIMELINE PLANNER

Study: _______________
Start Date: _______________
Target End Date: _______________

PHASE PLANNING

| Phase | Activities | Duration | Start | End | Dependencies |
|-------|------------|----------|-------|-----|--------------|
| Planning | | | | | |
| Recruitment | | | | | |
| Pilot | | | | | |
| Execution | | | | | |
| Analysis | | | | | |
| Reporting | | | | | |
| Buffer | | | | | |

KEY MILESTONES

| Milestone | Date | Owner | Status |
|-----------|------|-------|--------|
| Research plan approved | | | |
| Materials ready | | | |
| Recruitment launched | | | |
| All sessions scheduled | | | |
| Pilot complete | | | |
| 50% sessions complete | | | |
| All sessions complete | | | |
| Analysis complete | | | |
| Stakeholder readout | | | |
| Final deliverables | | | |

CALENDAR CONSIDERATIONS

| Consideration | Dates | Impact |
|---------------|-------|--------|
| Holidays | | |
| Team PTO | | |
| Stakeholder availability | | |
| Product milestones | | |
| Other research competing | | |

TIMELINE RISKS

| Risk | Impact | Mitigation |
|------|--------|------------|
| | | |

PLANNED BY: _______________ DATE: _______________
```

---

### Template 5.6: Risk Assessment Template

```
RESEARCH RISK ASSESSMENT

Study: _______________
Assessed by: _______________
Date: _______________

RISK IDENTIFICATION

| ID | Risk Description | Category | Trigger |
|----|------------------|----------|---------|
| R1 | | | |
| R2 | | |  |
| R3 | | | |
| R4 | | | |
| R5 | | | |

Categories: Recruitment, Timeline, Budget, Quality, Scope, External, Technical

RISK ASSESSMENT

| ID | Probability | Impact | Risk Level | Score |
|----|-------------|--------|------------|-------|
| R1 | L/M/H | L/M/H | | |
| R2 | | | | |
| R3 | | | | |
| R4 | | | | |
| R5 | | | | |

Risk Level: Low (1-2), Medium (3-4), High (5-6)
Score: Probability (L=1, M=2, H=3) x Impact (L=1, M=2, H=3)

MITIGATION PLANS

| ID | Risk | Mitigation Strategy | Owner | Status |
|----|------|---------------------|-------|--------|
| R1 | | | | |
| R2 | | | | |
| R3 | | | | |

CONTINGENCY PLANS (for High risks)

| ID | Risk | Contingency Plan |
|----|------|------------------|
| | | |

RISK MONITORING

Review frequency: [ ] Weekly [ ] Bi-weekly [ ] At milestones

APPROVED BY: _______________ DATE: _______________
```

---

### Template 5.7: Scope Change Request Log

```
SCOPE CHANGE LOG

Study: _______________
Researcher: _______________

| Change # | Date Requested | Description | Requested By | Impact (Timeline/Budget/Quality) | Decision | Approved By | Date |
|----------|----------------|-------------|--------------|----------------------------------|----------|-------------|------|
| SC-001 | | | | | Approved/Denied/Deferred | | |
| SC-002 | | | | | | | |
| SC-003 | | | | | | | |

SCOPE CHANGE DETAIL

Change #: _______________
Date: _______________

CHANGE DESCRIPTION
_______________________________________________
_______________________________________________

RATIONALE
Why is this change being requested?
_______________________________________________

IMPACT ASSESSMENT

| Dimension | Current Plan | With Change | Delta |
|-----------|--------------|-------------|-------|
| Timeline | | | |
| Budget | | | |
| Sample size | | | |
| Deliverables | | | |

ALTERNATIVES CONSIDERED
1. _______________________________________________
2. _______________________________________________

RECOMMENDATION
[ ] Approve - benefits outweigh costs
[ ] Deny - costs outweigh benefits
[ ] Defer - address in follow-up study

DECISION
_______________________________________________

Approved by: _______________
Date: _______________
```

---

### Template 5.8: Research Planning Kickoff Agenda

```
RESEARCH PLANNING KICKOFF

Study: _______________
Date: _______________
Attendees: _______________

AGENDA

1. Welcome and Introductions (5 min)
   - Researcher introduction
   - Attendee introductions and roles

2. Background and Context (10 min)
   - Business context and problem statement
   - What prompted this research
   - Prior research and existing knowledge

3. Research Objectives Discussion (15 min)
   - What do we need to learn?
   - What decisions will this inform?
   - What would change based on findings?

4. Research Questions Development (15 min)
   - What specific questions need answering?
   - Prioritization: must-know vs. nice-to-know
   - What questions are OUT of scope?

5. Target Participants Discussion (10 min)
   - Who do we need to talk to?
   - Any access constraints?
   - Recruitment approach

6. Methodology Discussion (10 min)
   - Proposed approach
   - Trade-offs and alternatives
   - Questions about method

7. Timeline and Deliverables (10 min)
   - Key milestones
   - Decision timeline
   - Deliverable format preferences

8. Roles and Responsibilities (5 min)
   - Who does what
   - Communication plan
   - Review process

9. Questions and Concerns (10 min)
   - Open discussion
   - Risk identification

10. Next Steps and Close (5 min)
    - Action items
    - Next meeting

TOTAL TIME: ~90 minutes

PRE-MEETING PREPARATION
Researcher:
- [ ] Draft research brief
- [ ] Review existing research
- [ ] Prepare preliminary approach

Stakeholders:
- [ ] Review research brief
- [ ] Come prepared to discuss questions
- [ ] Identify any constraints

POST-MEETING ACTION ITEMS

| Action | Owner | Due |
|--------|-------|-----|
| | | |
```

---

### 5.9 Recommended Tools

| Function | Tools | Notes |
|----------|-------|-------|
| Research plan documentation | Google Docs, Notion, Confluence | Use templates for consistency |
| Timeline planning | Google Sheets, Monday.com, Asana | Track milestones and dependencies |
| Stakeholder communication | Slack, email, Loom | Use async for updates, sync for alignment |
| Method selection | Decision matrix template | Structured comparison |
| Risk tracking | Spreadsheet, project management tool | Regular review cadence |
| Scope tracking | Change log template | Document all changes |
| Research repository | Notion, Dovetail, Google Drive | Store completed plans |

---

## 6. Responsibilities

### RACI Matrix

| Activity | Research Lead | Researcher | Research Ops | Stakeholder |
|----------|---------------|------------|--------------|-------------|
| Receive research request | I | R | S | R |
| Initial triage | A | R | C | I |
| Create research brief | A | R | - | C |
| Define research objectives | A | R | - | C |
| Develop research questions | A | R | - | C |
| Select method | A | R | C | I |
| Define participant requirements | A | R | S | C |
| Plan timeline and resources | A | R | S | C |
| Conduct stakeholder alignment | A | R | - | R |
| Create research plan | A | R | S | C |
| Approve research plan | A | R | - | R |
| Manage scope changes | A | R | I | C |
| Hand off to recruitment | I | R | R | - |
| Plan consent approach | A | R | S | - |
| Plan data handling | A | R | S | - |

**R** = Responsible (does the work)
**A** = Accountable (ultimate ownership)
**C** = Consulted (provides input)
**I** = Informed (kept updated)
**S** = Supports (assists as needed)

### Role Definitions

**Research Lead:**
- Approves research priorities and resource allocation
- Reviews research plans for quality and alignment
- Resolves escalated stakeholder conflicts
- Ensures consistency across research portfolio
- Approves scope changes exceeding thresholds

**Researcher:**
- Receives and triages research requests
- Develops research objectives and questions with stakeholders
- Selects appropriate methods and designs studies
- Creates comprehensive research plans
- Manages stakeholder expectations and alignment
- Identifies and mitigates risks
- Manages scope changes within thresholds
- Hands off to downstream processes appropriately

**Research Operations:**
- Supports resource and timeline planning
- Facilitates scheduling and logistics
- Maintains templates and tools
- Tracks research portfolio status
- Supports recruitment handoff

**Stakeholder (Sponsor/Decision-Maker):**
- Provides business context and requirements
- Participates in objective and question development
- Reviews and approves research plan
- Approves scope changes
- Commits to acting on findings

---

## 7. Quality Checks

### 7.1 Research Brief Quality Check

Before proceeding from brief to full plan:

| Check | Pass? |
|-------|-------|
| Business decision clearly articulated | [ ] |
| Initial research questions documented | [ ] |
| Timeline expectations captured | [ ] |
| Constraints identified | [ ] |
| Existing research checked | [ ] |
| Appropriate to proceed (vs. defer/decline) | [ ] |

### 7.2 Research Objectives Quality Check

| Check | Pass? |
|-------|-------|
| Tied to specific decision or action | [ ] |
| Identifies target user/participant | [ ] |
| Scoped to what can be learned in this study | [ ] |
| Measurable or observable outcomes | [ ] |
| Not answerable by existing data alone | [ ] |
| Agreed upon by stakeholders | [ ] |

### 7.3 Research Questions Quality Check

| Check | Pass? |
|-------|-------|
| Questions directly support objectives | [ ] |
| Questions are answerable with planned method | [ ] |
| Questions are prioritized (primary/secondary) | [ ] |
| No leading or biased questions | [ ] |
| Scope is contained (not too many questions) | [ ] |

### 7.4 Method Selection Quality Check

| Check | Pass? |
|-------|-------|
| Method can answer research questions | [ ] |
| Method fits timeline constraints | [ ] |
| Method fits budget constraints | [ ] |
| Participants can be recruited for this method | [ ] |
| Team has capability to execute method | [ ] |
| Rationale documented | [ ] |

### 7.5 Research Plan Completeness Check

Before seeking approval:

| Section | Complete? | Quality Reviewed? |
|---------|-----------|-------------------|
| Background and context | [ ] | [ ] |
| Research objectives | [ ] | [ ] |
| Research questions | [ ] | [ ] |
| Method and rationale | [ ] | [ ] |
| Participant requirements | [ ] | [ ] |
| Timeline | [ ] | [ ] |
| Deliverables | [ ] | [ ] |
| Resources and budget | [ ] | [ ] |
| Risks and mitigations | [ ] | [ ] |
| Stakeholder roles | [ ] | [ ] |
| Approval signatures | [ ] | [ ] |

### 7.6 Stakeholder Alignment Check

Before beginning execution:

| Check | Pass? |
|-------|-------|
| All key stakeholders identified | [ ] |
| Alignment meeting conducted | [ ] |
| Objectives agreed | [ ] |
| Questions agreed | [ ] |
| Timeline agreed | [ ] |
| Deliverables agreed | [ ] |
| Roles and responsibilities clear | [ ] |
| Sponsor approval documented | [ ] |

### 7.7 Post-Study Planning Retrospective

After study completion, assess planning effectiveness:

| Question | Assessment | Learnings |
|----------|------------|-----------|
| Did objectives remain relevant? | | |
| Did questions get answered? | | |
| Was method appropriate? | | |
| Was timeline realistic? | | |
| Was budget accurate? | | |
| Were risks identified and managed? | | |
| Were stakeholders appropriately engaged? | | |
| What would we do differently? | | |

---

## 8. Related Documents

| Document ID | Title | Relationship |
|-------------|-------|--------------|
| UXR-001 | Informed Consent & Ethics | Consent planning during research planning |
| UXR-002 | Data Handling & Privacy | Data classification and handling planning |
| UXR-003 | Participant Recruitment & Screening | Recruitment criteria handoff |
| UXR-005 | Interview/Moderation Guide Development | Materials development after planning |
| UXR-006 | Note-Taking & Documentation | Documentation approach planning |
| UXR-007 | Analysis & Synthesis | Analysis plan development |
| UXR-008 | Stakeholder Communication | Deliverable planning and stakeholder alignment |

---

## 9. Revision History

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 2026-01-22 | [Name] | Initial release | [Name] |
| | | | | |

### Review Schedule

| Review Type | Frequency | Next Review | Owner |
|-------------|-----------|-------------|-------|
| Content accuracy | Annual | 2027-01-22 | Research Lead |
| Process updates | Semi-annual | 2026-07-22 | Research Lead |
| Template review | Annual | 2027-01-22 | Research Ops |
| Stakeholder feedback | Semi-annual | 2026-07-22 | Research Lead |

---

## Appendix A: Quick Reference Card

### Research Planning Quick Checklist

**Before Planning:**
- [ ] Research request received and documented
- [ ] Initial triage completed
- [ ] Research brief created
- [ ] Decision to proceed confirmed

**During Planning:**
- [ ] Business context understood
- [ ] Research objectives defined
- [ ] Research questions developed
- [ ] Method selected
- [ ] Participants defined
- [ ] Timeline created
- [ ] Budget estimated
- [ ] Risks identified
- [ ] Research plan drafted

**Before Execution:**
- [ ] Stakeholders aligned
- [ ] Research plan approved
- [ ] Recruitment criteria handed off
- [ ] Consent approach planned
- [ ] Data handling planned

### Research Objective Formulas

**Generative Research:**
> **Understand** [behavior/need/problem] **of** [user type] **in order to** [inform design/strategy]

**Evaluative Research:**
> **Evaluate** [design/concept] **with** [user type] **to determine** [success criteria/decision]

**Validation Research:**
> **Validate** [assumption/hypothesis] **about** [user type] **to confirm/refute** [belief]

### Timeline Quick Reference

| Study Type | Planning | Recruitment | Execution | Analysis | Total |
|------------|----------|-------------|-----------|----------|-------|
| Quick usability (5 users) | 0.5 wk | 1 wk | 1 wk | 0.5 wk | 3 wks |
| User interviews (10 users) | 1 wk | 1.5 wks | 1.5 wks | 1 wk | 5 wks |
| Survey (200 responses) | 1 wk | 0.5 wk | 1.5 wks | 1 wk | 4 wks |
| Field study (4 sites) | 2 wks | 3 wks | 3 wks | 2 wks | 10 wks |

---

## Appendix B: FAQ/Troubleshooting

**Q: Stakeholders want research faster than realistic timeline allows**

A:

- Clearly explain what can be done in the requested timeline
- Offer scaled alternatives (fewer participants, simpler method)
- Show trade-offs: speed vs. quality vs. scope
- Document the agreed approach and limitations
- If pushed to compromise quality unacceptably, escalate to Research Lead

**Q: Stakeholders have conflicting priorities for research questions**

A:

- Prioritize questions by decision urgency
- Identify which questions must be answered vs. nice-to-know
- Consider if conflicting questions can be separate studies
- Escalate to research sponsor for prioritization decision
- Document the prioritization rationale

**Q: Scope keeps expanding during the study**

A:

- Use scope change process for all additions
- Document impact on timeline, budget, quality
- Offer to add questions to a follow-up study backlog
- Get explicit approval for scope changes
- If uncontrolled, pause and realign with stakeholders

**Q: Not sure if a study needs formal planning**

A:

- If <3 participants and <1 week, probably informal
- If involves external participants, use formal planning
- If involves stakeholder decisions, use formal planning
- If involves travel or significant budget, use formal planning
- When in doubt, create at minimum a research brief

**Q: Budget is insufficient for the proposed study**

A:

- Propose scaled alternatives (fewer participants, remote vs. in-person)
- Identify what can be cut vs. what is essential
- Consider phased approach (do critical part now, remainder later)
- Document limitations of reduced scope
- Seek additional budget approval if study is high priority

**Q: Can't access the users we need for the research**

A:

- Explore alternative recruitment channels
- Consider proxy participants (similar role, different company)
- Use existing customer relationships creatively
- Partner with sales/CS for warm introductions
- Adjust timeline to allow for longer recruitment
- Be transparent with stakeholders about limitations

---

**Document Control:**
- This document is controlled. Printed copies are for reference only.
- Current version available at: [Insert location]
- Questions: Contact Research Lead

**Emergency Contact:**
- Planning issues: Research Lead
- Stakeholder conflicts: Research Lead
- Resource constraints: Research Operations
