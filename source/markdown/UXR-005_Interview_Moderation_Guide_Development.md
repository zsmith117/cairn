# UXR-005: Interview/Moderation Guide Development Standard Operating Procedure

**Document ID:** UXR-005
**Version:** 1.0
**Effective Date:** January 23, 2026
**Last Review:** January 23, 2026
**Document Owner:** UX Research Lead
**Classification:** Internal Use Only

---

## 1. Purpose

This Standard Operating Procedure establishes the requirements and procedures for developing interview and moderation guides for UX research studies. It ensures that:

- Research sessions are structured to consistently address research questions
- Questions are designed to elicit rich, unbiased responses from participants
- Moderators have clear guidance for conducting sessions effectively
- Sessions remain within planned time constraints
- Knowledge is transferable when multiple researchers conduct sessions
- Session quality is maintained across different moderators
- Guide content supports downstream analysis and synthesis

**Why This Matters:**

The quality of a research guide directly impacts the quality of research insights. Poor guides lead to:
- Missing critical information that was supposed to be learned
- Leading questions that bias participant responses
- Incomplete coverage of research questions
- Sessions running over time or finishing too early
- Inconsistent data collection across sessions
- Difficulty analyzing and synthesizing findings
- Knowledge gaps when someone other than the guide author moderates
- Stakeholder skepticism about research rigor

A well-developed guide is the researcher's roadmap, ensuring every session contributes meaningfully to answering the research questions.

---

## 2. Scope

**This SOP applies to:**

- User interviews (1-on-1 depth interviews)
- Contextual inquiry interviews (field research)
- Usability testing moderation guides
- Focus group moderation guides
- Concept testing interviews
- Stakeholder interviews
- Expert interviews
- Diary study check-in interviews
- Any structured research conversation with participants

**This SOP covers:**

- Guide structure and organization
- Question development best practices
- Writing unbiased, effective questions
- Timing and flow planning
- Pilot testing and refinement
- Guide documentation and version control
- Adaptation during sessions
- Collaboration on guide development

**Out of scope:**

- Quantitative survey design (see separate survey SOP when developed)
- Unstructured informal conversations (no guide needed)
- Quantitative task protocol design for metrics-focused testing
- Analytics instrumentation
- A/B testing experimental design

---

## 3. Definitions

| Term | Definition |
|------|------------|
| **Interview Guide** | A structured document outlining topics, questions, and flow for a qualitative research interview |
| **Moderation Guide** | A document providing structure and scripted content for moderating sessions (usability tests, focus groups) |
| **Discussion Guide** | Another term for interview guide, emphasizing conversational nature |
| **Protocol** | The complete set of procedures and scripts for a research session, including guide plus logistics |
| **Screening Criteria** | Requirements participants must meet; documented in UXR-003 |
| **Warm-up Questions** | Initial easy questions to build rapport and ease participant into conversation |
| **Main Questions** | Core questions directly addressing research questions |
| **Probing Questions** | Follow-up questions to elicit depth, examples, or clarification |
| **Laddering** | Technique of asking "why" repeatedly to uncover underlying motivations |
| **Neutral Prompt** | A question phrased to avoid suggesting a desired response |
| **Leading Question** | A biased question that suggests an answer (should be avoided) |
| **Open-ended Question** | Questions that invite expansive responses, not yes/no |
| **Closed-ended Question** | Questions with finite answers (yes/no, multiple choice) - use sparingly |
| **Transition** | A scripted statement moving between guide sections |
| **Script** | Word-for-word text to be read (consent, instructions) |
| **Pilot Session** | Practice session to test and refine guide before main data collection |
| **Moderator Notes** | Annotations in guide providing tips, rationale, or reminders for the moderator |
| **Stimulus** | Materials shown to participants (prototypes, concepts, products) |
| **Think-Aloud Protocol** | Technique where participants verbalize thoughts while performing tasks |
| **Session Flow** | The ordered sequence of activities and topics in a session |

---

## 4. Procedure

### 4.1 Preparing to Develop the Guide

#### 4.1.1 Review Research Plan

Before drafting the guide, ensure you have:

**Required Inputs:**

| Input | Source | What You Need |
|-------|--------|---------------|
| Research objectives | UXR-004 Research Plan | What the study aims to learn |
| Research questions | UXR-004 Research Plan | Specific questions to answer |
| Participant profile | UXR-004 Research Plan | Who you'll be talking to |
| Method | UXR-004 Research Plan | Interview type and format |
| Session duration | UXR-004 Research Plan | Time constraint for guide |
| Stimulus materials | UXR-004 Research Plan | What will be shown/tested |

**Reference Documents:**

- Prior research on similar topics (to build on existing knowledge)
- Prior interview guides (for format and question ideas)
- Product/feature documentation (to understand what you're researching)
- Stakeholder input (assumptions to validate, areas of concern)

#### 4.1.2 Translate Research Questions to Interview Questions

Research questions are not interview questions. Translation is required.

**Translation Framework:**

| Research Question | Interview Questions |
|-------------------|---------------------|
| What are the main pain points in the workflow? | - Walk me through how you currently [do this task]<br>- What parts of that process work well?<br>- What parts are frustrating or difficult?<br>- Tell me about a recent time when [problem occurred] |
| How do users make prioritization decisions? | - How do you decide what to work on first?<br>- Walk me through the last time you had to prioritize competing requests<br>- What information do you need to make that decision?<br>- What makes prioritization easy or difficult? |
| What features would improve the experience? | - If you could change one thing about how you do this, what would it be?<br>- What do you wish this tool could do that it can't today?<br>- How are you working around current limitations? |

**Key Principles:**

- Research questions guide what to explore; interview questions are what you actually ask
- Interview questions should elicit stories, behaviors, and examples, not hypotheticals
- Break broad research questions into multiple specific interview questions
- Focus on past behavior and real experiences, not opinions or predictions

#### 4.1.3 Determine Guide Structure Type

Select the appropriate guide structure based on method:

| Method | Typical Structure | Characteristics |
|--------|-------------------|-----------------|
| **Generative Interviews** | Warm-up → Topic blocks → Closing | Flexible, exploratory, topic-based |
| **Usability Testing** | Intro → Tasks → Debrief → Demographics | Task-focused, structured, evaluative |
| **Contextual Inquiry** | Intro → Observation → Debrief | Observation-heavy, adaptive |
| **Concept Testing** | Warm-up → Concept exposure → Reaction → Comparison | Stimulus-driven, structured response |
| **Stakeholder Interviews** | Background → Topic exploration → Future vision | Strategic, flexible |
| **Focus Groups** | Intro → Individual priming → Group discussion → Activities | Group dynamics, facilitated |

---

### 4.2 Developing the Interview Guide Structure

#### 4.2.1 Standard Interview Guide Sections

**Complete Guide Structure:**

```
INTERVIEW GUIDE: [STUDY NAME]
Version: X.X | Date: YYYY-MM-DD

SESSION OVERVIEW
[Summary for moderator: purpose, duration, special notes]

---

0. PRE-SESSION SETUP
   [Checklist for before participant arrives]

1. INTRODUCTION (X minutes)
   [Welcome, consent, expectations]

2. WARM-UP (X minutes)
   [Easy questions, build rapport]

3. MAIN TOPIC AREA 1 (X minutes)
   [Primary questions on first major topic]

4. MAIN TOPIC AREA 2 (X minutes)
   [Primary questions on second major topic]

[Additional topic areas as needed]

5. CLOSING (X minutes)
   [Final questions, demographics, thanks]

---

TOTAL TIME: X minutes
BUFFER: X minutes

---

MODERATOR NOTES
[Key things to remember, common pitfalls]
```

#### 4.2.2 Introduction Section

The introduction sets the tone and ensures compliance.

**Introduction Components:**

```
1. INTRODUCTION (5-7 minutes)

[SCRIPT - Read verbatim]

"Thank you for joining today. I'm [NAME], a UX researcher at [COMPANY].
Today we're going to talk about [TOPIC] to help us improve [PRODUCT/AREA].

Before we start, I want to set some expectations:

- This conversation should take about [X] minutes
- There are no right or wrong answers - I want to understand your honest
  experience
- I'm not testing you; I'm learning from you
- You can decline to answer any question
- You can take a break or stop at any time
- [If recording:] I'd like to record this session for note-taking purposes.
  The recording will only be used by our research team and will be deleted
  after [TIMEFRAME].

Do you have any questions before we begin?"

[CONSENT PROCESS - Per UXR-001]
[Confirm verbal consent and recording permission]

"Great. Let's get started."
```

**Moderator Notes for Introduction:**
- Speak conversationally, not robotically
- Make eye contact
- Confirm recording is working before proceeding
- Address any concerns before continuing

#### 4.2.3 Warm-Up Section

Warm-up questions build rapport and ease participants into conversation.

**Warm-Up Characteristics:**

| Good Warm-up Questions | Poor Warm-up Questions |
|------------------------|------------------------|
| Easy to answer | Difficult or sensitive |
| Build rapport | Directly on research topic |
| Low stakes | High cognitive load |
| Conversational | Formal or technical |
| Establish participant as expert | Position researcher as expert |

**Example Warm-Up Section:**

```
2. WARM-UP (3-5 minutes)

"I'd like to start by learning a bit about your role and background."

- Can you tell me about your current role?
  [Listen for: job title, responsibilities, team structure]

- How long have you been in this role?
  [Listen for: experience level, tenure]

- What does a typical day or week look like for you?
  [Listen for: workflow, priorities, context]

[MODERATOR NOTE: Keep this brief; don't let it run long. You're building
rapport, not gathering deep data yet.]
```

**Warm-Up Best Practices:**

- Allocate 3-5 minutes for warm-up (10% of session)
- Use open-ended questions
- Show genuine interest
- Don't probe deeply here; save it for main sections
- Use participant's answers to personalize later questions

#### 4.2.4 Main Topic Sections

Main sections address research questions directly.

**Topic Section Template:**

```
3. [TOPIC NAME] (X minutes)

[MODERATOR NOTE: Goal for this section is to understand [SPECIFIC OBJECTIVE]]

[TRANSITION]
"Now I'd like to talk about [TOPIC]..."

PRIMARY QUESTIONS:

1. [Opening question - broad and narrative]
   [Listen for: key points you're trying to learn]

   PROBES:
   - [Probe for depth]
   - [Probe for examples]
   - [Probe for frequency]

2. [Follow-up question - more specific]
   [Listen for: specific aspects]

   PROBES:
   - [If they mention X, ask about Y]
   - "Can you give me an example of that?"
   - "How often does that happen?"

3. [Additional question as time allows]
   [Listen for: nice-to-know information]

[MODERATOR NOTE: If time is short, prioritize questions 1-2]
```

**Structuring Topic Flow:**

| Approach | Description | When to Use |
|----------|-------------|-------------|
| **Chronological** | Follow participant's process from start to end | Understanding workflows, journeys |
| **General to Specific** | Start broad, narrow focus | Exploratory research |
| **Specific to General** | Start with behavior, zoom out to context | Focused on particular problem |
| **Comparative** | Compare multiple options, approaches, or time periods | Concept testing, before/after |

#### 4.2.5 Closing Section

The closing ensures you capture anything missed and leaves participants positively.

**Closing Section Template:**

```
5. CLOSING (5 minutes)

[TRANSITION]
"We're coming to the end of our time. I have just a few final questions."

FINAL QUESTIONS:

1. Is there anything about [TOPIC] that we haven't discussed that you
   think is important for me to understand?

   [MODERATOR NOTE: Often surfaces unexpected insights]

2. If you could change one thing about [TOPIC/PRODUCT], what would it be?

   [MODERATOR NOTE: Gets prioritized wish]

3. Is there anything you'd like to ask me?

   [MODERATOR NOTE: Address questions appropriately]

DEMOGRAPHICS (if not collected in screening):
- [Demographic question 1]
- [Demographic question 2]

[SCRIPT]
"Thank you so much for your time and insights today. This has been really
helpful. Your feedback will help us [IMPACT].

[If incentive:] You should receive [INCENTIVE] within [TIMEFRAME].

If you have any questions later, feel free to reach out to [CONTACT].

Thanks again!"

[POST-SESSION]
- Stop recording
- Save notes/recording immediately
- Complete post-session reflection
```

---

### 4.3 Writing Effective Questions

#### 4.3.1 Question Types and When to Use Them

**Question Type Framework:**

| Question Type | Purpose | Example | When to Use |
|---------------|---------|---------|-------------|
| **Behavioral** | Understand what people actually do | "Walk me through the last time you [did X]" | Primary question type; foundation of qualitative research |
| **Experience** | Understand subjective experience | "How did that make you feel?" | After behavioral questions to add depth |
| **Causal** | Understand reasoning | "What led you to make that decision?" | When understanding motivation |
| **Comparative** | Understand preferences, differences | "How does X compare to Y?" | Concept testing, competitive analysis |
| **Hypothetical** | Explore possibilities (use sparingly) | "What would you do if [scenario]?" | Only after grounding in real behavior |
| **Projective** | Surface subconscious attitudes | "How would you describe this to a colleague?" | When direct questions aren't working |

#### 4.3.2 Writing Neutral, Unbiased Questions

**Avoiding Leading Questions:**

| Leading (Bad) | Neutral (Good) |
|---------------|----------------|
| "Don't you find this feature frustrating?" | "How do you feel about this feature?" |
| "How much do you love this design?" | "What's your reaction to this design?" |
| "What problems do you have with X?" | "Tell me about your experience with X" |
| "Our customers say this is confusing. Do you agree?" | "How easy or difficult was this to understand?" |
| "Why is this so much better than the old way?" | "How does this compare to what you did before?" |

**Question Quality Checklist:**

- [ ] Asks one thing at a time (not compound)
- [ ] Doesn't suggest a desired answer
- [ ] Uses participant's language, not internal jargon
- [ ] Open-ended (invites narrative)
- [ ] Focused on real experience, not opinion or prediction
- [ ] Clear and unambiguous

#### 4.3.3 Crafting Open-Ended Questions

**Effective Opening Words:**

| Opening | Effect | Example |
|---------|--------|---------|
| "Tell me about..." | Invites narrative | "Tell me about the last time you had to [do X]" |
| "Walk me through..." | Elicits detailed process | "Walk me through how you decided which option to choose" |
| "How do you..." | Focuses on behavior | "How do you keep track of your tasks?" |
| "What..." | Broad exploration | "What happens when you need to [do X]?" |
| "Describe..." | Invites rich detail | "Describe your typical workflow for [task]" |
| "Can you help me understand..." | Shows curiosity | "Can you help me understand why that matters?" |

**Words to Avoid:**

| Avoid | Why | Alternative |
|-------|-----|-------------|
| "Do you...?" | Invites yes/no | "How do you...?" or "Tell me about..." |
| "Would you...?" | Hypothetical, not behavioral | "Have you...?" or "When was the last time you...?" |
| "Don't you...?" | Leading, suggests answer | Neutral phrasing |
| "Why don't you...?" | Defensive | "What prevents you from...?" |

#### 4.3.4 Developing Probe Questions

Probes help you dig deeper after initial responses.

**Types of Probes:**

| Probe Type | Purpose | Examples |
|------------|---------|----------|
| **Clarification** | Ensure understanding | - "Can you explain what you mean by [term]?"<br>- "I want to make sure I understand..." |
| **Example** | Get concrete instances | - "Can you give me an example?"<br>- "Tell me about a specific time when that happened" |
| **Detail** | Add specificity | - "What did you do next?"<br>- "What did that look like?" |
| **Frequency** | Understand patterns | - "How often does that happen?"<br>- "Is that typical?" |
| **Emotion** | Understand impact | - "How did that make you feel?"<br>- "What was that experience like?" |
| **Contrast** | Understand differences | - "How is that different from [alternative]?"<br>- "Was that usual or unusual?" |
| **Causation** | Understand reasoning | - "What led to that?"<br>- "Why did you choose that option?" |
| **Impact** | Understand consequences | - "What happened as a result?"<br>- "How did that affect your work?" |

**The Laddering Technique:**

Ask "why" progressively to uncover root motivations:

```
Researcher: "Tell me why you prefer that approach"
Participant: "It's faster"

Researcher: "Why does speed matter in this case?"
Participant: "I have to get through 50 of these per day"

Researcher: "Help me understand why that volume exists"
Participant: "Our SLA requires 24-hour response time"

[Now you understand the root driver]
```

**Probe Best Practices:**

- Have probes ready but adapt based on responses
- Don't probe everything; focus on areas relevant to research questions
- Use silence; wait 3-5 seconds after a response before probing
- Use minimal encouragers: "uh-huh," "tell me more," "interesting"
- Probe for real examples; avoid accepting generalizations

#### 4.3.5 Timing and Question Allocation

**Time Budgeting:**

For a 60-minute interview:

| Section | Time Allocation | Percentage |
|---------|-----------------|------------|
| Introduction & Consent | 5-7 min | 10% |
| Warm-up | 3-5 min | 5-10% |
| Main Topics | 40-45 min | 70-75% |
| Closing | 5 min | 5-10% |
| Buffer | 5 min | 5-10% |

**Questions Per Section:**

| Section Duration | Primary Questions | Including Probes |
|------------------|-------------------|------------------|
| 10 minutes | 2-3 | 5-8 total |
| 15 minutes | 3-4 | 8-12 total |
| 20 minutes | 4-5 | 10-15 total |

**Time Allocation Principles:**

- Prioritize essential questions first in each section
- Mark "if time permits" questions clearly
- Allocate more time to most important research questions
- Include buffer time for tangents and unexpected insights
- Plan what to cut if running short on time

---

### 4.4 Special Guide Types

#### 4.4.1 Usability Testing Moderation Guides

Usability test guides focus on task completion and observation.

**Usability Guide Structure:**

```
USABILITY TESTING GUIDE: [STUDY NAME]

SESSION OVERVIEW
- Duration: 60 minutes
- Tasks: [N] tasks
- Think-aloud protocol
- [Device/platform]

---

1. INTRODUCTION (5 min)
   [Standard intro + think-aloud instruction]

   "As you use [product], please think out loud - tell me what you're
   looking at, what you're trying to do, what you're thinking. This helps
   me understand your experience."

2. WARM-UP TASK (5 min)
   [Simple practice task to get comfortable with think-aloud]

   Practice Task: [Easy task]
   Goal: Get participant comfortable with think-aloud

3. TASK 1: [TASK NAME] (10 min)

   SCENARIO:
   "Imagine you need to [context]. Please show me how you would [task goal]."

   SUCCESS CRITERIA:
   - [ ] [Criterion 1]
   - [ ] [Criterion 2]

   OBSERVE:
   - Where do they start?
   - What path do they take?
   - Where do they hesitate?
   - What errors occur?

   NOTES:
   - Don't help unless they ask or are completely stuck (5 min)
   - If stuck, provide hint: [specific hint]
   - If still stuck after hint, move on

   POST-TASK QUESTIONS:
   - "How easy or difficult was that?" (1-5 scale)
   - "What made it easy/difficult?"
   - [Any specific questions about observed behavior]

[Repeat for each task]

4. DEBRIEF (10 min)

   - "Overall, what did you think of [product]?"
   - "What worked well?"
   - "What was frustrating or confusing?"
   - "How does this compare to [current method]?"
   - "Anything else?"

5. CLOSING (5 min)
   [Standard closing]
```

**Usability Testing Best Practices:**

- Keep tasks realistic and specific
- Avoid giving hints too quickly; struggle reveals problems
- Observe carefully; take notes on behavior, not just outcomes
- Ask post-task questions immediately after each task
- Use think-aloud; remind participants if they go silent
- Stay neutral; don't react to success or failure

#### 4.4.2 Contextual Inquiry Guides

Contextual inquiry happens in the participant's environment.

**Contextual Inquiry Guide Structure:**

```
CONTEXTUAL INQUIRY GUIDE: [STUDY NAME]

SESSION OVERVIEW
- Location: [Participant's workplace/environment]
- Duration: 90-120 minutes
- Focus: Observing [workflow/activity] in context

---

1. INTRODUCTION (10 min)
   [Standard intro + explanation of observation]

   "I'm here to observe how you normally do [activity]. Please work as you
   usually would. I'll watch and ask questions as we go. Feel free to tell
   me to be quiet if I'm interrupting at a bad time."

2. INITIAL INTERVIEW (15 min)
   [Context-setting questions before observation]

   - "Before we start, can you tell me what you're planning to work on today?"
   - "Walk me through what a typical [day/session] looks like"
   - "What are the main things you're trying to accomplish?"

3. OBSERVATION (60-90 min)
   [Watch and ask questions in real-time]

   WHAT TO OBSERVE:
   - Physical workspace and tools
   - Workflow and sequence
   - Information sources consulted
   - Interruptions and distractions
   - Workarounds and adaptations
   - Tools and artifacts used
   - Collaboration and communication

   QUESTIONS TO ASK DURING OBSERVATION:
   - "What are you doing now?"
   - "Why did you do it that way?"
   - "What are you looking for?"
   - "What happens next?"
   - "Is this typical or unusual?"

   [MODERATOR NOTE: Take photos of workspace, artifacts, tools (with permission)]

4. DEBRIEF (15 min)
   [After observation, ask follow-up questions]

   - "Was that typical of how you usually work?"
   - "What was different today?"
   - "What parts of what I observed are most challenging?"
   - "What would make this easier?"
   - "What did I miss?"

5. CLOSING (5 min)
   [Standard closing + logistics]
```

**Contextual Inquiry Best Practices:**

- Observe first, ask second
- Take photos and videos (with consent) for documentation
- Note environmental factors (space, tools, noise, interruptions)
- Ask "why" and "what" questions during observation
- Don't interrupt during critical moments
- Capture artifacts (forms, tools, workarounds)
- Coordinate site visits in advance per UXR-001 Section 4.5.1

#### 4.4.3 Concept Testing Guides

Concept testing evaluates reactions to stimulus materials.

**Concept Testing Guide Structure:**

```
CONCEPT TESTING GUIDE: [STUDY NAME]

SESSION OVERVIEW
- Concepts: [N] concepts to test
- Order: [Randomize or fixed]
- Comparative evaluation

---

1. INTRODUCTION (5 min)
   [Standard intro]

2. WARM-UP (5 min)
   [Context about current experience, needs]

3. CONCEPT PRESENTATION & TESTING (35 min)

   [FOR EACH CONCEPT:]

   CONCEPT [X]: [NAME] (12 min)

   [PRESENTATION]
   "I'm going to show you [concept]. Take a moment to look it over."

   [Show concept - allow 60-90 seconds of silent review]

   INITIAL REACTION:
   - "What's your first reaction?"
   - "In your own words, what is this?"
   - "Who is this for?"

   [LISTEN: Did they understand it correctly?]

   DETAILED EXPLORATION:
   - "What appeals to you about this?"
   - "What concerns do you have?"
   - "How would this fit into your [workflow/life]?"
   - "What's missing?"
   - "How does this compare to what you do today?"

   LIKELIHOOD:
   - "How likely would you be to [use/buy/try] this?" (1-5 scale)
   - "What would make you more likely?"
   - "What would prevent you from [using/buying/trying] it?"

4. COMPARATIVE EVALUATION (10 min)

   [Show all concepts together]

   - "Now that you've seen all [N] options, which appeals most to you?"
   - "Why that one?"
   - "Rank these from most to least appealing"
   - "What would you take from each concept to create the ideal solution?"

5. CLOSING (5 min)
   [Standard closing]
```

**Concept Testing Best Practices:**

- Randomize concept order across participants to avoid order bias
- Allow silent review before asking questions
- Test understanding before evaluating appeal
- Ask about behavior and context, not just opinions
- Compare concepts relative to each other
- Probe on both positives and concerns

---

### 4.5 Pilot Testing and Refinement

#### 4.5.1 Conducting Pilot Sessions

Before main data collection, pilot test your guide.

**Pilot Session Goals:**

| Goal | What to Test |
|------|--------------|
| **Timing** | Does the guide fit within session duration? |
| **Comprehension** | Do participants understand questions? |
| **Flow** | Does the sequence feel natural? |
| **Coverage** | Do questions address research questions? |
| **Probes** | Are planned probes sufficient? |
| **Logistics** | Do tech, consent, recording work smoothly? |

**Pilot Participants:**

| Option | Pros | Cons | When to Use |
|--------|------|------|-------------|
| **Internal team members** | Easy access, fast feedback | Not representative | Early draft testing |
| **Research panel participants** | Representative | Uses participant budget | Final pilot |
| **Friendly external contacts** | Somewhat representative, willing to give feedback | Limited availability | Mid-stage refinement |

**Pilot Session Protocol:**

```
1. CONDUCT SESSION
   - Run guide as planned for real session
   - Note timing for each section
   - Observe where you or participant struggled

2. DEBRIEF WITH PILOT PARTICIPANT
   - "How was that experience for you?"
   - "Were any questions confusing?"
   - "Did anything feel repetitive?"
   - "Were there things you wanted to talk about but we didn't cover?"
   - "Was the length appropriate?"

3. IMMEDIATE REFLECTION
   - What worked well?
   - What needs revision?
   - What was surprising?
   - What timing adjustments needed?
```

#### 4.5.2 Refining Based on Pilot Feedback

**Common Pilot Findings and Fixes:**

| Finding | Fix |
|---------|-----|
| Running over time | Cut lower-priority questions; tighten probes |
| Finishing too early | Add depth questions; expand key sections |
| Questions confusing | Simplify language; add context |
| Questions too similar | Consolidate redundant questions |
| Missing key topics | Add questions; adjust flow |
| Wrong question order | Resequence for natural flow |
| Participant discomfort | Soften sensitive questions; improve transition |
| Not addressing research questions | Refocus questions on objectives |

**Revision Process:**

1. Document pilot findings immediately
2. Revise guide within 24 hours while fresh
3. Increment version number and note changes
4. If major changes, conduct another pilot
5. If minor changes, proceed to main sessions
6. Share revised guide with team before first real session

---

### 4.6 Guide Documentation and Version Control

#### 4.6.1 File Naming and Organization

**File Naming Convention:**

```
[Study Code]_[Guide Type]_v[X.X]_[Date].doc

Examples:
- UXR-2026-Q1-001_Interview_Guide_v1.0_2026-01-15.doc
- UXR-2026-Q1-001_Interview_Guide_v1.1_2026-01-18.doc
- UXR-2026-Q1-002_Usability_Guide_v1.0_2026-01-20.doc
```

**Storage Location:**

| File Type | Location | Access |
|-----------|----------|--------|
| Working drafts | Researcher's drive | Researcher only |
| Current version | Study folder (shared) | Study team |
| Final version | Research repository | Entire UXR team |
| Templates | Templates folder | Entire UXR team |

#### 4.6.2 Version Control

**Versioning Schema:**

| Version Change | When to Increment |
|----------------|-------------------|
| **Major version** (1.0 → 2.0) | Significant restructuring; major question changes; post-pilot revision |
| **Minor version** (1.0 → 1.1) | Small question edits; wording changes; timing adjustments; typo fixes |

**Version History Documentation:**

Include in guide header:

```
VERSION HISTORY

v1.0 (2026-01-15) - Initial draft
v1.1 (2026-01-18) - Added probes to Section 3 based on team feedback
v2.0 (2026-01-20) - Major restructuring based on pilot session;
                     shortened Section 4, expanded Section 3
v2.1 (2026-01-21) - Minor wording clarifications
```

#### 4.6.3 Sharing and Collaboration

**Review Process:**

```
[Draft Complete] → [Peer Review] → [Stakeholder Review] → [Pilot] → [Final]
                    (1 day)         (1-2 days)             (1 day)
```

**Review Focus by Stakeholder:**

| Reviewer | Review Focus |
|----------|-------------|
| **Peer Researcher** | Question quality, flow, coverage of research questions, timing realism |
| **Research Lead** | Alignment with research plan, rigor, knowledge transfer potential |
| **Subject Matter Expert** | Terminology accuracy, relevance of topics, missing areas |
| **Product Stakeholder** | Coverage of key areas, alignment with decisions needed |

**Incorporating Feedback:**

- Accept, reject, or modify suggestions thoughtfully
- Document major decisions ("why we chose not to ask about X")
- Ensure final guide still reflects your voice as moderator
- Balance stakeholder desires with research best practices
- Researcher has final say on question quality

---

### 4.7 Using the Guide During Sessions

#### 4.7.1 Guide as Tool, Not Script

**Using the Guide Effectively:**

| Do | Don't |
|----|-------|
| Use as a roadmap and reference | Read robotically from guide |
| Maintain eye contact with participant | Read every word verbatim (except scripts) |
| Follow the spirit of questions, not exact wording | Skip sections because you "feel" you have enough |
| Adapt based on participant responses | Ask questions participant already answered |
| Probe when interesting topics emerge | Stick rigidly to guide when flexibility is needed |
| Keep guide visible for checking coverage | Hide guide like you're not allowed to use it |

**Balancing Structure and Flexibility:**

- Follow the structure (section order, time allocation)
- Adapt the execution (wording, probing depth)
- If participant naturally covers Topic B while discussing Topic A, don't force back to sequence
- Circle back to ensure all key questions are eventually addressed

#### 4.7.2 Adapting in Real-Time

**When to Deviate from the Guide:**

| Situation | Adaptation |
|-----------|------------|
| Participant gives rich tangent related to research questions | Let it flow; adjust subsequent questions to avoid repetition |
| Running short on time | Cut "nice to have" questions; focus on essentials |
| Question doesn't apply to this participant | Skip or modify to be relevant |
| Participant already answered upcoming question | Note it's covered; move on |
| Unexpected insight emerges | Probe deeper even if not in guide |
| Participant is tired or distracted | Take a break; shorten remaining sections |

**Mid-Session Time Management:**

Check time at section transitions:

```
If ahead of schedule:
- Probe more deeply
- Include "if time permits" questions
- Let participant elaborate

If on schedule:
- Continue as planned

If behind schedule:
- Cut lowest-priority questions
- Tighten probes
- Move to closing on time
```

#### 4.7.3 Note-Taking While Moderating

See UXR-006 for detailed note-taking procedures.

**Quick Reference:**

- Use guide margins for quick notes
- Mark when key quotes occur for transcription
- Note body language, tone, hesitations
- Flag unexpected insights for post-session reflection
- Mark sections that felt too long/short for future adjustment

---

### 4.8 Iterating the Guide Across Sessions

#### 4.8.1 Learning from Early Sessions

After first 2-3 sessions, reflect on guide performance:

**Post-Session Reflection Questions:**

| Question | Assessment |
|----------|------------|
| Did we answer the research questions? | Yes / Partially / No |
| Which guide sections worked well? | [List] |
| Which sections need improvement? | [List] |
| What questions didn't yield useful responses? | [List] |
| What unexpected topics emerged? | [List] |
| Were probes sufficient? | Yes / No |
| Was timing accurate? | Yes / Too long / Too short |
| What should we adjust? | [Actions] |

#### 4.8.2 Making Mid-Study Adjustments

**When to Revise Mid-Study:**

| Situation | Action | Version Change |
|-----------|--------|----------------|
| Minor wording clarification | Revise immediately | Minor version increment |
| Adding probe questions | Revise immediately | Minor version increment |
| Question consistently doesn't work | Replace or remove | Minor version increment |
| Missing a critical research question | Add question | Major version increment + note why |
| Timing adjustments | Revise immediately | Minor version increment |

**Documentation of Changes:**

```
MID-STUDY ADJUSTMENT LOG

Date: 2026-01-18
After Session: 3 of 12
Change: Added probe question in Section 3
Reason: Participants mentioning [topic] but not elaborating without prompt
Impact: None; added depth to existing section
New Version: v2.1
```

**Communication:**

- If multiple moderators, notify team of changes immediately
- Document reason for change
- If major change, reassess whether early data is still comparable

---

### 4.9 Special Considerations

#### 4.9.1 B2B and Industrial Research

When interviewing industrial or B2B users:

| Consideration | Implication for Guide |
|---------------|----------------------|
| **Domain expertise** | Use correct terminology; avoid sounding ignorant |
| **Time constraints** | Respect busy schedules; keep to promised time |
| **Confidentiality** | Avoid questions about proprietary processes; stay in scope |
| **Technical depth** | Prepare to go deep on technical topics; have expert probes ready |
| **Organizational context** | Ask about decision-making structures, stakeholders, approval processes |
| **Multi-role perspectives** | Design guides to work across different roles (manager, operator, purchaser) |

**Stakeholder/Expert Interview Adjustments:**

- Frame questions as learning from their expertise
- Ask about industry context, not just their company
- Include "what do you see others in the industry doing?" questions
- Ask about future trends and vision
- Respect their time and knowledge level

#### 4.9.2 Sensitive Topics

When researching sensitive topics:

| Topic Type | Guide Considerations |
|------------|---------------------|
| **Personal/emotional** | Build trust gradually; save sensitive questions for later; offer option to skip |
| **Embarrassing failures** | Frame as learning opportunity; normalize the experience |
| **Criticism of employer** | Ensure confidentiality; frame as general feedback, not blame |
| **Health/medical** | Per UXR-001, assess if specialized consent needed; allow participants to control disclosure |
| **Financial** | Ask ranges or comparative rather than specific amounts |
| **Controversial** | Acknowledge multiple perspectives; stay neutral |

**Techniques for Sensitive Questions:**

- Normalize: "Many people find that..."
- Depersonalize: "Some users have mentioned... does that resonate with you?"
- Offer opt-out: "This next question is about [topic]. You're welcome to skip it if you prefer."
- Third-person projection: "How do you think most people in your role would feel about...?"

#### 4.9.3 Remote vs. In-Person Adaptations

**Remote Session Adjustments:**

| Consideration | Guide Adjustment |
|---------------|------------------|
| **Tech setup time** | Add 3-5 minutes for tech troubleshooting |
| **Screen sharing** | Include explicit instructions for screen sharing |
| **Reduced rapport** | Extend warm-up slightly; be extra warm and personable |
| **Harder to read body language** | Ask more explicit check-in questions; probe more |
| **Distractions** | Acknowledge possibility; include "are you in a place where you can focus?" |
| **Zoom fatigue** | Consider shorter sessions or scheduled breaks |

**In-Person Session Adjustments:**

| Consideration | Guide Adjustment |
|---------------|------------------|
| **Physical space** | Note seating arrangement, privacy needs |
| **Stimulus materials** | Plan for physical materials (prototypes, printouts) |
| **More natural conversation** | Can be less structured; rely more on conversational flow |
| **Body language visible** | Can probe based on observed reactions |

---

## 5. Templates and Tools

### Template 5.1: Generative Interview Guide Template

```
INTERVIEW GUIDE: [STUDY NAME]

Document ID: [ID]
Version: [X.X]
Date: [YYYY-MM-DD]
Researcher: [Name]

===================================================================

SESSION OVERVIEW

Purpose: [Brief description of what this study aims to learn]
Duration: [X] minutes
Recording: [ ] Audio [ ] Video [ ] Screen
Format: [ ] Remote [ ] In-person

Research Questions Being Addressed:
1. [Research question 1]
2. [Research question 2]
3. [Research question 3]

===================================================================

MATERIALS NEEDED

[ ] Consent form (UXR-001)
[ ] Recording device/software
[ ] [Stimulus materials, if any]
[ ] [Other materials]

===================================================================

PRE-SESSION CHECKLIST

[ ] Recording equipment tested
[ ] Stimulus materials ready
[ ] Consent form ready
[ ] Quiet space confirmed
[ ] Reviewed participant screening info

===================================================================

GUIDE

---

1. INTRODUCTION (5 minutes)

[SCRIPT - Read verbatim]

"Hi [NAME], thank you for joining me today. I'm [YOUR NAME], a UX
researcher at [COMPANY].

Today we're going to talk about [TOPIC]. I'm hoping to learn from your
experience with [AREA] to help us improve [PRODUCT/SERVICE].

A few things to set expectations:
- This should take about [X] minutes
- There are no right or wrong answers - I want to hear about your real
  experience
- You can decline to answer any question or take a break at any time
- Everything you share will be kept confidential
- [If recording:] I'd like to record our conversation for note-taking
  purposes. The recording will only be used by our research team and will
  be deleted within [TIMEFRAME].

Do you have any questions before we start?"

[CONSENT PROCESS]
- Confirm verbal consent: "Do I have your consent to proceed?"
- If recording: "Do I have your consent to record?"
- Start recording

"Great, let's begin."

---

2. WARM-UP (5 minutes)

"Let me start by learning a bit about you and your background."

Q1: Can you tell me about your current role?
    [Listen for: job title, responsibilities, tenure]

Q2: What does a typical day or week look like for you?
    [Listen for: workflow, priorities, context]

Q3: [Additional warm-up question specific to your topic]
    [Listen for: relevant context]

[MODERATOR NOTE: Keep warm-up brief. Build rapport, don't go deep yet.]

---

3. MAIN TOPIC AREA 1: [TOPIC NAME] (15 minutes)

[MODERATOR NOTE: Goal is to understand [SPECIFIC OBJECTIVE]]

[TRANSITION]
"Now I'd like to talk about [TOPIC]..."

Q1: [Opening question - broad, narrative]
    [Listen for: key points]

    Probes:
    - [Probe for depth]
    - [Probe for example]
    - [Probe for frequency]

Q2: [Follow-up question]
    [Listen for: specific aspects]

    Probes:
    - "Can you give me an example?"
    - "How often does that happen?"

Q3: [Additional question]
    [Listen for: additional dimensions]

Q4: [If time permits]
    [Listen for: nice-to-know info]

---

4. MAIN TOPIC AREA 2: [TOPIC NAME] (15 minutes)

[MODERATOR NOTE: Goal is to understand [SPECIFIC OBJECTIVE]]

[TRANSITION]
"Let's shift to talking about [TOPIC]..."

Q1: [Opening question]
    [Listen for: key points]

    Probes:
    - [Probe as needed]

Q2: [Follow-up question]
    [Listen for: specific aspects]

Q3: [Additional question]
    [Listen for: additional dimensions]

---

5. CLOSING (5 minutes)

[TRANSITION]
"We're coming to the end of our time. I just have a few final questions."

Q1: Is there anything about [MAIN TOPIC] that we haven't discussed that
    you think is important for me to understand?

Q2: If you could change one thing about [TOPIC/PRODUCT], what would it be?

Q3: Is there anything you'd like to ask me?

[DEMOGRAPHICS - if not collected in screening]
- [Demographic question 1]
- [Demographic question 2]

[SCRIPT]
"Thank you so much for your time today. Your insights have been really
helpful and will help us [IMPACT].

[If incentive:] You should receive [INCENTIVE TYPE] within [TIMEFRAME].

If you have any questions later, you can reach me at [CONTACT].

Thanks again!"

[POST-SESSION]
- Stop recording
- Save recording immediately
- Complete post-session notes (see UXR-006)
- Note any guide adjustments needed

===================================================================

TIMING SUMMARY

Section                  | Planned Time | Actual Time
-------------------------|--------------|-------------
Introduction             | 5 min        |
Warm-up                  | 5 min        |
Topic Area 1             | 15 min       |
Topic Area 2             | 15 min       |
Closing                  | 5 min        |
Buffer                   | 5 min        |
TOTAL                    | 50 min       |

===================================================================

MODERATOR NOTES

Key reminders:
- [Important things to remember]
- [Common pitfalls to avoid]
- [Areas to probe deeply]

Sensitive topics:
- [Any sensitive areas and how to handle]

===================================================================
```

---

### Template 5.2: Usability Testing Guide Template

```
USABILITY TESTING GUIDE: [STUDY NAME]

Document ID: [ID]
Version: [X.X]
Date: [YYYY-MM-DD]
Researcher: [Name]

===================================================================

SESSION OVERVIEW

Purpose: Evaluate [product/feature] usability
Duration: 60 minutes
Tasks: [N] tasks
Protocol: Think-aloud
Device: [Desktop/Mobile/Tablet]
Format: [ ] Remote [ ] In-person

===================================================================

MATERIALS NEEDED

[ ] Consent form
[ ] Recording equipment (screen + audio)
[ ] [Product/prototype] ready
[ ] Task scenarios printed/ready
[ ] Post-task rating scales

===================================================================

PRE-SESSION CHECKLIST

[ ] Recording equipment tested
[ ] Product/prototype accessible
[ ] Screen sharing working (if remote)
[ ] Consent form ready
[ ] Task scenarios ready

===================================================================

1. INTRODUCTION (5 minutes)

[SCRIPT]

"Hi [NAME], thanks for joining me today. I'm [YOUR NAME], a UX researcher
at [COMPANY].

Today I'm going to ask you to try out [PRODUCT/FEATURE]. I want to see
how it works for someone like you. This helps us understand what's working
well and what we can improve.

Important things to know:
- We're testing the product, not you. There are no wrong answers.
- Some things might work easily, some might not. That's exactly what we
  need to learn.
- As you work, please think out loud - tell me what you're looking at,
  what you're trying to do, what you're thinking. This helps me understand
  your experience.
- I won't be able to help much during the tasks, because I want to see how
  the product works on its own. But I'll check in with you after each task.
- This should take about 60 minutes.

Do you have any questions?"

[CONSENT PROCESS]
[Start recording]

"Let me show you how the think-aloud process works..."

---

2. THINK-ALOUD PRACTICE (5 minutes)

"Before we start with the actual tasks, let's practice thinking aloud with
something simple."

PRACTICE TASK:
"Can you search Google for [SIMPLE TOPIC] and tell me what you see?"

[OBSERVE: Are they verbalizing their thoughts?]

[If silent, prompt]: "Remember to tell me what you're thinking as you work"

"Great! That's exactly the kind of thing I'm looking for. Now let's move
to the actual tasks."

---

3. WARM-UP (5 minutes)

"Before we start the tasks, a couple quick questions:"

Q1: Have you used [PRODUCT TYPE] before?
    [Listen for: experience level, current tools]

Q2: [Context-setting question about their needs/goals]
    [Listen for: context for interpreting task performance]

---

4. TASK 1: [TASK NAME] (10 minutes)

SCENARIO:
"Imagine [SCENARIO CONTEXT]. Please show me how you would [TASK GOAL]."

[HAND PARTICIPANT SCENARIO CARD OR SHARE SCREEN WITH SCENARIO]

SUCCESS CRITERIA:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

OBSERVE:
- Starting point
- Path taken
- Hesitations
- Errors
- Time to completion
- Completion: [ ] Success [ ] Partial [ ] Failure

NOTES:
- Don't help unless they're completely stuck (wait 5 minutes)
- If stuck for 5 min, provide hint: [SPECIFIC HINT]
- If still stuck after hint, move on

[Let participant work - stay mostly silent except to prompt think-aloud]

POST-TASK QUESTIONS:

Q1: "How easy or difficult was that task?"
    [ ] Very easy [ ] Easy [ ] Neutral [ ] Difficult [ ] Very difficult

Q2: "What made it [easy/difficult]?"
    [Listen for: specific usability issues or successes]

Q3: [Any specific question about observed behavior]
    [Listen for: clarification on what you observed]

[Repeat sections for each task]

---

5. TASK 2: [TASK NAME] (10 minutes)

[Same structure as Task 1]

---

6. TASK 3: [TASK NAME] (10 minutes)

[Same structure as Task 1]

---

7. DEBRIEF (10 minutes)

"Great, we're done with the tasks. Now I have some questions about your
overall experience."

Q1: Overall, what did you think of [PRODUCT]?
    [Listen for: general impression]

Q2: What worked well?
    [Listen for: positive aspects]

Q3: What was frustrating or confusing?
    [Listen for: pain points]

Q4: How does this compare to [CURRENT TOOL/METHOD]?
    [Listen for: comparative feedback]

Q5: Would you use this if it were available?
    [ ] Definitely [ ] Probably [ ] Maybe [ ] Probably not [ ] Definitely not

    "Why/why not?"

Q6: Is there anything else you'd like to tell me?
    [Listen for: anything missed]

---

8. CLOSING (5 minutes)

[STANDARD CLOSING]

===================================================================

TASK SUMMARY

Task | Success | Time | Difficulty (1-5) | Notes
-----|---------|------|------------------|------
  1  |         |      |                  |
  2  |         |      |                  |
  3  |         |      |                  |

===================================================================

ISSUES LOG

Issue # | Task | Severity | Description
--------|------|----------|-------------
   1    |      |          |
   2    |      |          |
   3    |      |          |

Severity: Critical / Serious / Minor

===================================================================
```

---

### Template 5.3: Contextual Inquiry Guide Template

```
CONTEXTUAL INQUIRY GUIDE: [STUDY NAME]

Document ID: [ID]
Version: [X.X]
Date: [YYYY-MM-DD]
Researcher: [Name]

===================================================================

SESSION OVERVIEW

Purpose: Observe [WORKFLOW/ACTIVITY] in context
Duration: 90-120 minutes
Location: Participant's workplace
Focus: Real work observation

===================================================================

MATERIALS NEEDED

[ ] Consent form
[ ] Recording device (audio + camera for photos)
[ ] Photo release form (UXR-001)
[ ] Notebook for sketching/notes
[ ] Business cards
[ ] Safety gear (if industrial setting)

===================================================================

PRE-VISIT COORDINATION

Per UXR-001 Section 4.5.1:
[ ] Site visit approved by account team
[ ] Safety requirements reviewed
[ ] Schedule confirmed with participant
[ ] Backup participant identified
[ ] Emergency contact information
[ ] Site-specific protocols reviewed

===================================================================

1. INTRODUCTION (10 minutes)

[SCRIPT]

"Hi [NAME], thank you for having me here today. I'm [YOUR NAME], a
researcher at [COMPANY].

As we discussed, I'm here to observe and learn about how you [DO ACTIVITY].
My goal is to understand your real workflow so we can make [PRODUCT] work
better for people in your role.

Here's how this will work:
- I'll observe you as you work normally. Please don't change what you do
  for me.
- I'll ask questions as we go. Feel free to tell me if I'm interrupting
  at a bad time.
- I'd like to take photos of your workspace and tools (with your
  permission). No photos of people without permission.
- This will take about [X] hours.
- Everything I observe stays confidential.

Do you have any questions?"

[CONSENT PROCESS]
[PHOTO RELEASE if taking photos of workspace]

"Before we start observing, I have a few quick questions..."

---

2. INITIAL CONTEXT INTERVIEW (15 minutes)

Q1: Before we start, can you tell me what you're planning to work on today?
    [Listen for: today's context]

Q2: Walk me through what a typical [day/shift/session] looks like for you
    [Listen for: normal workflow, variations]

Q3: What are the main things you're trying to accomplish in your role?
    [Listen for: goals, success criteria]

Q4: What tools and systems do you use?
    [Listen for: technology, physical tools, information sources]

Q5: [Any other context-setting questions specific to your focus]

"Great, I'm ready to observe. Please go ahead and work as you normally
would."

---

3. OBSERVATION (60-90 minutes)

[MODERATOR NOTES]

WHAT TO OBSERVE:
- Physical workspace layout
- Tools and artifacts used
- Information sources consulted
- Sequence of activities
- Decision points
- Interruptions and how handled
- Workarounds and adaptations
- Communication and collaboration
- Time spent on different activities
- Pain points and frustrations
- Successful/efficient moments

DOCUMENTATION:
- Take field notes continuously
- Sketch workflows, layouts, artifacts
- Photo workspace, tools, artifacts (with permission)
- Note quotes that capture experience
- Track time spent on different activities

QUESTIONS TO ASK DURING OBSERVATION:

[Ask these in real-time as you observe:]

- "What are you doing now?"
- "What are you looking for?"
- "Why did you do it that way?"
- "What happens next?"
- "Is this typical?"
- "What would you normally do here?" [if they're modifying for you]
- "Where did you get that information?"
- "What are you thinking about?"
- "What's this tool/artifact?"
- "Why do you keep that there?"

WHEN TO STAY SILENT:
- During concentrated work
- During customer/stakeholder interactions
- During safety-critical activities
- When participant indicates they need focus

WHAT TO CAPTURE:

Physical Environment:
- [ ] Workspace photos (wide angle)
- [ ] Tool close-ups
- [ ] Information artifacts (forms, notes, displays)
- [ ] Workspace organization
- [ ] Environmental factors (noise, lighting, space)

Workflow:
- [ ] Sequence diagram of activities
- [ ] Decision points
- [ ] Information flow
- [ ] Handoffs and collaboration points
- [ ] Time allocation

Artifacts:
- [ ] Forms and documents used
- [ ] Tools and equipment
- [ ] Workarounds and adaptations
- [ ] Personal organization systems

---

4. DEBRIEF INTERVIEW (15 minutes)

[After observation period]

"Thank you for letting me observe. That was really helpful. I have a few
follow-up questions."

Q1: Was today typical of how you usually work, or was anything different?
    [Listen for: unusual circumstances]

Q2: Of everything I observed, what parts are most challenging or
    frustrating?
    [Listen for: prioritized pain points]

Q3: What parts of your workflow work really well?
    [Listen for: what to preserve]

Q4: If you could change anything about [TOOLS/PROCESS], what would it be?
    [Listen for: wish list]

Q5: What did I miss? What happens that I didn't see today?
    [Listen for: other scenarios, edge cases]

Q6: [Follow-up on specific things you observed]
    [Listen for: clarification]

---

5. CLOSING (5 minutes)

[STANDARD CLOSING]

"Is it okay if I follow up via email if I have clarification questions?"
[Get contact information]

"Would you be willing to talk again in the future for follow-up research?"
[ ] Yes [ ] No

[POST-SESSION]
- Organize photos immediately
- Transfer field notes to digital while fresh
- Sketch workflow diagrams
- Note key insights

===================================================================

OBSERVATION NOTES

Time | Activity Observed | Tools Used | Notes
-----|-------------------|------------|------
     |                   |            |
     |                   |            |

===================================================================

ARTIFACTS CAPTURED

Artifact | Type | Photo # | Description
---------|------|---------|-------------
         |      |         |
         |      |         |

===================================================================

WORKFLOW DIAGRAM

[Sketch workflow sequence here or attach separately]

===================================================================
```

---

### Template 5.4: Guide Review Checklist

```
INTERVIEW/MODERATION GUIDE REVIEW CHECKLIST

Study: _______________
Guide Version: _______________
Reviewer: _______________
Date: _______________

===================================================================

ALIGNMENT WITH RESEARCH PLAN

[ ] Guide addresses all primary research questions
[ ] Guide aligns with stated research objectives
[ ] Method is appropriate for research questions
[ ] Participant profile matches planned criteria
[ ] Session duration is realistic

Comments:
_______________________________________________

===================================================================

STRUCTURE AND FLOW

[ ] Introduction section is complete (welcome, consent, expectations)
[ ] Warm-up section builds rapport effectively
[ ] Main sections are logically ordered
[ ] Transitions between sections are smooth
[ ] Closing section is complete (final questions, thanks, logistics)
[ ] Overall flow feels natural

Comments:
_______________________________________________

===================================================================

QUESTION QUALITY

[ ] Questions are open-ended (not yes/no)
[ ] Questions are neutral (not leading)
[ ] Questions focus on behavior, not just opinions
[ ] Questions ask one thing at a time (not compound)
[ ] Questions use clear, simple language
[ ] Questions avoid jargon (unless appropriate for audience)
[ ] Questions elicit examples and stories

Comments:
_______________________________________________

===================================================================

PROBES AND FOLLOW-UPS

[ ] Key questions have probes prepared
[ ] Probes dig deeper into important areas
[ ] Probes help get examples and specifics
[ ] Moderator has flexibility to adapt

Comments:
_______________________________________________

===================================================================

TIMING

[ ] Time allocated to each section
[ ] Time allocations are realistic
[ ] Priorities are marked (essential vs. nice-to-have)
[ ] Buffer time included
[ ] Guide fits within planned session duration

Total time planned: _____ minutes
Session duration: _____ minutes

Comments:
_______________________________________________

===================================================================

MODERATOR SUPPORT

[ ] Moderator notes explain goals of each section
[ ] "Listen for" cues help moderator know what's important
[ ] Scripts are clearly marked
[ ] Special instructions are clear
[ ] Guide is easy to follow while moderating

Comments:
_______________________________________________

===================================================================

LOGISTICS AND COMPLIANCE

[ ] Consent process included (per UXR-001)
[ ] Recording permissions addressed
[ ] Materials list is complete
[ ] Pre-session checklist included
[ ] Demographics collection addressed (if needed)
[ ] Incentive logistics covered

Comments:
_______________________________________________

===================================================================

USABILITY OF GUIDE DOCUMENT

[ ] Version number and date clearly visible
[ ] Sections are numbered/labeled clearly
[ ] Formatting makes it easy to scan during session
[ ] Font size is readable
[ ] Sufficient white space for notes

Comments:
_______________________________________________

===================================================================

OVERALL ASSESSMENT

[ ] Ready to pilot
[ ] Ready for use (minor revisions)
[ ] Needs revision before pilot
[ ] Needs major rework

STRENGTHS:
_______________________________________________
_______________________________________________

AREAS FOR IMPROVEMENT:
_______________________________________________
_______________________________________________

SPECIFIC SUGGESTIONS:
_______________________________________________
_______________________________________________

===================================================================

REVIEWER SIGNATURE: _______________  DATE: _______________
```

---

### 5.5 Recommended Tools

| Function | Tools | Notes |
|----------|-------|-------|
| Guide creation | Google Docs, Microsoft Word | Enable commenting for collaboration |
| Version control | Google Drive version history, Dropbox | Automatic version tracking |
| Collaboration | Google Docs comments, Notion | Real-time review and feedback |
| Template storage | Shared drive, Notion | Centralized template library |
| Session timer | Phone timer, online timer | Keep track during sessions |
| Reference during session | Tablet or printed guide | Easy to reference while moderating |

---

## 6. Responsibilities

### RACI Matrix

| Activity | Research Lead | Researcher (Lead) | Researcher (Supporting) | Stakeholder |
|----------|---------------|-------------------|------------------------|-------------|
| Review research plan inputs | I | R | S | I |
| Draft interview guide | A | R | C | I |
| Develop questions | A | R | C | C |
| Peer review guide | R | C | R | - |
| Stakeholder review | I | R | C | R |
| Approve guide | A | R | - | C |
| Pilot test guide | I | R | S | - |
| Revise based on pilot | I | R | C | - |
| Use guide in sessions | - | R | R | - |
| Document mid-study changes | I | R | S | - |
| Archive final guide | A | R | - | - |

**R** = Responsible (does the work)
**A** = Accountable (ultimate ownership)
**C** = Consulted (provides input)
**I** = Informed (kept updated)
**S** = Supports (assists as needed)

### Role Definitions

**Research Lead:**
- Reviews guides for quality and rigor
- Approves guides before pilot
- Provides methodology guidance
- Ensures consistency across studies
- Maintains template library

**Researcher (Lead):**
- Drafts the interview guide
- Translates research questions to interview questions
- Conducts peer review process
- Pilots and refines guide
- Makes mid-study adjustments
- Archives final guide

**Researcher (Supporting):**
- Provides peer review feedback
- May assist with guide development
- Uses guide when moderating sessions
- Suggests improvements

**Stakeholder:**
- Reviews guide for coverage of key topics
- Provides domain expertise for question development
- Approves guide coverage (not question wording)
- Does not dictate question wording or research method

---

## 7. Quality Checks

### 7.1 Pre-Pilot Quality Check

Before piloting, verify:

| Check | Pass? |
|-------|-------|
| All research questions from plan are addressed | [ ] |
| Questions are open-ended | [ ] |
| Questions are neutral (not leading) | [ ] |
| Questions focus on behavior and experience | [ ] |
| Time allocations are included | [ ] |
| Timing totals to session duration | [ ] |
| Probes are prepared for key questions | [ ] |
| Introduction includes consent process | [ ] |
| Closing includes thank you and logistics | [ ] |
| Moderator notes are helpful | [ ] |
| Guide is easy to follow | [ ] |
| Version number and date are visible | [ ] |

### 7.2 Post-Pilot Quality Check

After piloting, assess:

| Check | Pass? | Notes |
|-------|-------|-------|
| Timing was accurate | [ ] | |
| Questions were understood | [ ] | |
| Flow felt natural | [ ] | |
| Covered all research questions | [ ] | |
| Probes were sufficient | [ ] | |
| No major issues or confusion | [ ] | |
| Ready for real sessions | [ ] | |

### 7.3 Mid-Study Quality Check

After 3-5 sessions, reflect:

| Check | Assessment | Action Needed |
|-------|------------|---------------|
| Are we answering the research questions? | [ ] Yes [ ] No [ ] Partially | |
| Is timing working out? | [ ] Yes [ ] No | |
| Are questions yielding useful responses? | [ ] Yes [ ] No [ ] Some | |
| Are probes sufficient? | [ ] Yes [ ] No | |
| Do we need to adjust the guide? | [ ] Yes [ ] No | |

---

## 8. Related Documents

| Document ID | Title | Relationship |
|-------------|-------|--------------|
| UXR-001 | Informed Consent & Ethics | Consent process in guide introduction |
| UXR-002 | Data Handling & Privacy | Recording and data handling considerations |
| UXR-003 | Participant Recruitment & Screening | Participant criteria inform question targeting |
| UXR-004 | Research Planning & Scoping | Research plan provides inputs for guide |
| UXR-006 | Note-Taking & Documentation | How to take notes during sessions |
| UXR-007 | Analysis & Synthesis | Guide structure enables analysis |
| UXR-008 | Stakeholder Communication | Guide review and stakeholder involvement |

---

## 9. Revision History

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 2026-01-23 | [Name] | Initial release | [Name] |
| | | | | |

### Review Schedule

| Review Type | Frequency | Next Review | Owner |
|-------------|-----------|-------------|-------|
| Content accuracy | Annual | 2027-01-23 | Research Lead |
| Template updates | Semi-annual | 2026-07-23 | Research Lead |
| Question bank | Annual | 2027-01-23 | Research Lead |
| Tool recommendations | Annual | 2027-01-23 | Research Operations |

---

## Appendix A: Quick Reference Card

### Guide Development Quick Checklist

**Before You Start:**
- [ ] Review research plan
- [ ] Understand research questions
- [ ] Know participant profile
- [ ] Check session duration

**While Drafting:**
- [ ] Structure: Intro → Warm-up → Main → Closing
- [ ] Translate research questions to interview questions
- [ ] Write open-ended, neutral questions
- [ ] Add probes for key questions
- [ ] Allocate time to each section
- [ ] Include moderator notes

**Before Pilot:**
- [ ] Peer review complete
- [ ] Stakeholder review complete
- [ ] Timing adds up correctly
- [ ] Consent process included
- [ ] Materials list complete

**After Pilot:**
- [ ] Debrief with pilot participant
- [ ] Revise based on feedback
- [ ] Update version number
- [ ] Share revised guide with team

### Question Quality Quick Check

Good questions are:
- **Open-ended**: "Tell me about..." not "Do you...?"
- **Neutral**: No suggested answers
- **Behavioral**: Focus on what people do, not opinions
- **Clear**: Simple language
- **Focused**: One thing at a time

Avoid:
- Yes/no questions
- Leading questions
- Hypotheticals (mostly)
- Jargon
- Compound questions

---

## Appendix B: Example Question Bank

### Behavioral Questions

**Understanding Current Process:**
- "Walk me through the last time you [did activity]"
- "Tell me about a typical [day/session/project]"
- "How do you currently [accomplish task]?"
- "Show me how you [do something]"

**Understanding Decision-Making:**
- "Walk me through how you decided to [make choice]"
- "What factors did you consider when [deciding]?"
- "Tell me about a time when you had to [make difficult decision]"

**Understanding Problems:**
- "What's frustrating about [activity]?"
- "Tell me about a recent time when [problem occurred]"
- "What makes [activity] difficult?"
- "Walk me through what happens when [problem scenario]"

### Experience Questions

**Understanding Feelings:**
- "How did that make you feel?"
- "What was that experience like?"
- "How do you feel about [thing]?"

**Understanding Reactions:**
- "What's your reaction to this?"
- "What stands out to you?"
- "What surprises you?"

### Causal Questions

**Understanding Motivations:**
- "What led you to [decision/action]?"
- "Why did you choose [option]?"
- "What made you decide to [action]?"
- "Help me understand why that matters"

**Understanding Reasoning:**
- "What made you think of that approach?"
- "What was going through your mind when [action]?"

### Comparative Questions

**Understanding Preferences:**
- "How does [A] compare to [B]?"
- "What do you prefer about [option]?"
- "Which of these appeals more to you?"

**Understanding Changes:**
- "How is that different from what you did before?"
- "What's changed since [time period]?"
- "How does this compare to your expectations?"

### Probing Questions

**Getting Examples:**
- "Can you give me an example?"
- "Tell me about a specific time when that happened"
- "What did that look like?"

**Getting Details:**
- "What happened next?"
- "Walk me through that step"
- "Tell me more about that"
- "What do you mean by [term]?"

**Understanding Frequency:**
- "How often does that happen?"
- "Is that typical or unusual?"
- "When does that occur?"

**Understanding Context:**
- "What else was happening at that time?"
- "Who else was involved?"
- "Where were you when this happened?"

### Closing Questions

**Capturing Missed Information:**
- "What haven't we talked about that's important?"
- "What should I have asked that I didn't?"
- "Is there anything else I should know?"

**Understanding Priorities:**
- "If you could change one thing, what would it be?"
- "What's most important to you about [topic]?"
- "What matters most when [activity]?"

---

## Appendix C: FAQ/Troubleshooting

**Q: How long should my interview guide be?**

A:
- As long as necessary, no longer
- Typical length: 3-5 pages for 60-minute interview
- Focus on clarity over brevity
- Include white space for notes

**Q: Should I write out every question word-for-word?**

A:
- Yes for scripts (intro, consent)
- Yes for key questions you want consistent across sessions
- Include variations or alternative wordings as moderator notes
- Give yourself flexibility in probes

**Q: What if stakeholders want to add lots of questions?**

A:
- Explain time constraints
- Prioritize together: essential vs. nice-to-have
- Offer to do a second study for lower-priority questions
- Remember: researcher has final say on question quality

**Q: Should I stick to the guide rigidly during sessions?**

A:
- No - guide is a tool, not a script
- Follow the structure; adapt the execution
- If participant naturally covers a topic, don't force it again
- Prioritize research questions over exact question sequence

**Q: What if I realize mid-study that a question isn't working?**

A:
- Revise immediately for subsequent sessions
- Document the change and reason
- Increment version number
- Notify other moderators if multi-moderator study
- Note change when analyzing data

**Q: How much detail should I include in moderator notes?**

A:
- Enough that someone else could moderate using your guide
- Include: section goals, what to listen for, common pitfalls
- Don't overdo it - notes shouldn't overwhelm the questions
- Focus on things that aren't obvious

**Q: Do I need to pilot test every guide?**

A:
- Yes for major studies, new methods, or complex topics
- Optional for very simple studies or familiar methods
- At minimum, read through with a colleague
- When in doubt, pilot

**Q: What if my pilot reveals major problems with the guide?**

A:
- This is exactly why you pilot!
- Revise substantially; consider it a new major version
- Pilot again if changes are significant
- Don't proceed to real sessions until guide works

---

**Document Control:**
- This document is controlled. Printed copies are for reference only.
- Current version available at: [Insert location]
- Questions: Contact Research Lead

**Emergency Contact:**
- Guide development questions: Research Lead
- Template access: Research Operations
- Method questions: Research Lead
