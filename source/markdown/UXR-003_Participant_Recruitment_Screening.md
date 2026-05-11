# UXR-003: Participant Recruitment & Screening Standard Operating Procedure

**Document ID:** UXR-003
**Version:** 1.0
**Effective Date:** January 16, 2026
**Last Review:** January 16, 2026
**Document Owner:** UX Research Lead
**Classification:** Internal Use Only

---

## 1. Purpose

This Standard Operating Procedure establishes the requirements and procedures for recruiting and screening research participants. It ensures that:

- Research studies include participants who accurately represent target user populations
- Recruitment methods are consistent, ethical, and compliant with privacy regulations
- Screening criteria are clearly defined and applied uniformly
- Participant experience is professional and respectful from first contact
- Recruitment timelines and costs are predictable and manageable
- B2B and industrial research recruitment challenges are addressed systematically

**Why This Matters:**

Participant recruitment is the most frequent research activity and has the highest variation risk. Poor recruitment leads to:
- Invalid findings based on unrepresentative participants
- Wasted research sessions with unqualified participants
- Inconsistent data quality across studies
- Budget overruns from no-shows and rescreens
- Damaged relationships with customers and partners (B2B)

---

## 2. Scope

**This SOP applies to:**
- All participant recruitment for UX research studies
- Internal recruitment (employees, existing customers)
- External recruitment (prospects, general population, industry professionals)
- Self-service recruitment (panels, intercepts, social media)
- Agency and vendor-assisted recruitment
- B2B recruitment through account relationships
- Field research participant identification

**This SOP covers:**
- Defining recruitment criteria and screener development
- Recruitment source selection and management
- Screening and qualification procedures
- Scheduling and confirmation processes
- No-show prevention and management
- Incentive determination and delivery
- Participant database and panel management
- Vendor and agency relationships

**Out of scope:**
- Consent procedures (see UXR-001)
- Data handling for participant information (see UXR-002)
- Research study design and planning (see UXR-004)
- Incentive accounting and tax reporting (see Finance policies)

---

## 3. Definitions

| Term | Definition |
|------|------------|
| **Participant** | An individual who takes part in a research study, providing data through interviews, testing, surveys, or observation |
| **Target Population** | The complete group of people about whom the research aims to draw conclusions |
| **Sample** | The subset of the target population actually included in the study |
| **Recruitment Criteria** | Specific characteristics that define who qualifies for a study (includes/excludes) |
| **Screener** | A questionnaire used to determine if potential participants meet recruitment criteria |
| **Qualification Rate** | Percentage of screened individuals who meet study criteria |
| **Show Rate** | Percentage of scheduled participants who attend their session |
| **Panel** | A database of individuals who have agreed to be contacted for research opportunities |
| **Intercept** | Recruitment method that approaches potential participants in context (in-product, on-site) |
| **Snowball Recruitment** | Using existing participants to refer additional qualified participants |
| **Professional Respondent** | Someone who participates in research studies frequently, potentially biasing results |
| **Articulation Ability** | A participant's capacity to verbally express thoughts, experiences, and reasoning |
| **Gatekeeper** | In B2B research, the person who controls access to potential participants within an organization |
| **Warm Introduction** | Recruitment initiated through an existing relationship (account manager, colleague) |
| **Cold Outreach** | Recruitment initiated without prior relationship |
| **Incentive** | Compensation provided to participants for their time and contribution |
| **Honorarium** | Alternative term for incentive, often used in B2B or professional contexts |
| **Over-recruit** | Scheduling more participants than needed to account for no-shows |

---

## 4. Procedure

### 4.1 Defining Recruitment Criteria

#### 4.1.1 Identify Target Population

Before recruiting, clearly document the target population for the study:

**Step 1: Answer these questions in the study protocol:**

| Question | Example Answer |
|----------|----------------|
| Who are the intended users of this product/feature? | Warehouse managers at distribution centers |
| What behaviors or experiences must participants have? | Currently use inventory management software daily |
| What decisions will this research inform? | Redesign of cycle count workflow |
| What segments or variations matter? | Company size (SMB vs. Enterprise), industry vertical |
| Who should be excluded and why? | Competitors, recent research participants, non-decision-makers |

**Step 2: Define primary and secondary criteria**

| Criteria Type | Description | Example |
|---------------|-------------|---------|
| **Must-Have (Primary)** | Non-negotiable requirements; participants without these are disqualified | Uses inventory software daily, decision-making authority |
| **Nice-to-Have (Secondary)** | Preferred characteristics that improve sample quality | 5+ years experience, specific industry |
| **Quota Criteria** | Characteristics to distribute across sample | 50% SMB / 50% Enterprise, geographic mix |
| **Exclusion Criteria** | Characteristics that disqualify participants | Works for competitor, participated in research <6 months |

#### 4.1.2 Determine Sample Size and Composition

**Recommended Sample Sizes by Method:**

| Research Method | Typical Sample | Notes |
|-----------------|----------------|-------|
| Generative interviews | 8-12 participants | Aim for saturation; add more if new themes emerge |
| Usability testing | 5-8 participants per user type | 5 users find ~85% of usability issues |
| Concept testing | 6-10 participants | Enough for pattern identification |
| Diary studies | 10-15 participants | Account for dropout (~20-30%) |
| Surveys (qualitative) | 50-100 responses | For open-ended analysis |
| Surveys (quantitative) | 200+ responses | For statistical significance |
| Focus groups | 6-8 per group, 2-3 groups | Multiple groups reduce group-think bias |
| Field studies | 4-8 sites | Depth over breadth |

**Sample Composition Considerations:**

- Include variation relevant to research questions
- Balance between homogeneity (comparable responses) and heterogeneity (diverse perspectives)
- For B2B: Consider role diversity within same organization vs. across organizations
- Document rationale for sample decisions in study protocol

#### 4.1.3 Develop Screening Questionnaire

**Screener Structure:**

```
1. Introduction (who is conducting, purpose, time estimate, incentive)
2. Disqualification questions (ask early to save time)
3. Primary criteria questions (must-have requirements)
4. Secondary criteria questions (nice-to-have, quotas)
5. Professional respondent check
6. Availability and logistics
7. Contact information collection
```

**Screener Best Practices:**

| Do | Don't |
|----|-------|
| Ask behavioral questions ("How often do you...") | Ask leading questions ("Do you like using...") |
| Use ranges for frequency/quantity questions | Use exact numbers that reveal the "right" answer |
| Randomize answer options where appropriate | Always put desired answer in same position |
| Include attention check questions | Assume all respondents read carefully |
| Ask disqualifying questions early | Waste unqualified respondents' time |
| Mask the purpose to avoid bias | Make qualifying criteria obvious |
| Test screener before launch | Launch without pilot testing |

**Professional Respondent Detection:**

Include questions to identify professional respondents:

- "How many research studies have you participated in during the past 6 months?" (Exclude if >3)
- "Do you or anyone in your household work in market research, advertising, or [relevant industry]?"
- Check response patterns for inconsistency
- For panels: Review participation history

---

### 4.2 Selecting Recruitment Sources

#### 4.2.1 Evaluate Recruitment Source Options

**Recruitment Source Comparison:**

| Source | Best For | Pros | Cons | Typical Cost | Lead Time |
|--------|----------|------|------|--------------|-----------|
| **Customer database** | Existing user research | Known users, accessible, low cost | May be biased toward satisfied users | Low (incentive only) | 1-2 weeks |
| **In-product intercept** | Active user feedback | In-context, high relevance | Interrupts workflow, limited depth | Low | 1-2 weeks |
| **Research panel (owned)** | Repeat research needs | Pre-qualified, fast | Requires maintenance, panel fatigue | Low | 1 week |
| **Research panel (vendor)** | General population, scale | Large reach, fast | Quality varies, expensive | $50-150/participant | 1-2 weeks |
| **Recruitment agency** | Hard-to-reach, B2B | Professional, handles logistics | Expensive, less control | $200-500+/participant | 2-4 weeks |
| **Social media** | Consumer, niche communities | Targeted, organic | Quality control difficult | Low-Medium | 1-2 weeks |
| **Industry events/associations** | B2B professionals | Targeted audience | Limited availability | Medium | 2-4 weeks |
| **Account team referrals** | Enterprise customers | Warm introduction, trusted | Limited pool, relationship risk | Low | 2-4 weeks |
| **Snowball referrals** | Niche populations | Access hard-to-reach | Homogeneous sample risk | Low-Medium | 2-4 weeks |
| **Employees** | Internal tools, early feedback | Accessible, no incentive needed | Not representative of customers | None | 1 week |

#### 4.2.2 B2B Recruitment Strategies

**Enterprise Customer Recruitment:**

| Approach | When to Use | Process |
|----------|-------------|---------|
| **Account team introduction** | Strategic accounts, sensitive topics | 1. Brief account team on study 2. They identify/introduce contacts 3. Researcher follows up |
| **Customer success referral** | Active accounts, relationship-based | 1. CS identifies engaged users 2. Warm handoff to research 3. Direct researcher contact |
| **Direct outreach (existing)** | Transactional relationships, large customer base | 1. Pull contact list 2. Email with context 3. Screener link |
| **Direct outreach (prospect)** | Non-customers, competitive research | 1. Purchase/source list 2. Cold email sequence 3. Screener qualification |
| **Event recruitment** | Industry professionals, networking | 1. Attend/sponsor events 2. In-person screening 3. Schedule follow-up |
| **Partner referral** | Ecosystem research, channel users | 1. Brief partner 2. They recruit from customers 3. Coordinate scheduling |

**Navigating Gatekeepers:**

When recruiting within B2B organizations:

1. **Identify the gatekeeper**: Usually IT, procurement, legal, or executive assistant
2. **Provide clear documentation**: Study purpose, time commitment, data handling
3. **Offer organizational benefit**: Share anonymized findings, early feature access
4. **Respect approval processes**: Allow time for internal review
5. **Get written approval**: Email confirmation from authorized person
6. **Coordinate scheduling**: Work with admin assistants for executive participants

**Multi-Stakeholder Recruitment:**

For studies requiring multiple roles from same organization:

- Recruit coordinator/champion first who can facilitate other introductions
- Clarify which roles are needed and minimum/maximum per organization
- Schedule sessions to minimize organizational burden
- Consider whether participants should be interviewed together or separately
- Document organizational relationships in participant tracking

**Consent for B2B Research with Proprietary Information:**

When recruiting B2B participants where proprietary or confidential business information may be discussed:

1. Use the **Enhanced Consent with NDA Provisions** template from UXR-001 Section 5.3
2. Establish company-level NDA before recruiting individual participants if required
3. Clarify with participants what information can/cannot be shared
4. Brief participants that they should not share information their employer considers confidential unless authorized

See UXR-001 Section 4.1.5 for guidance on checking existing customer agreements before recruitment.

#### 4.2.3 Industrial and Field Research Recruitment

**Site Visit Recruitment Process:**

1. **Identify target facilities** through customer records, industry directories, or referrals
2. **Initial contact** with site leadership (plant manager, operations director)
3. **Explain value proposition**: Why should they allow researchers on-site?
4. **Address concerns**: Safety, confidentiality, disruption to operations
5. **Negotiate access**: Which areas, which times, which personnel
6. **Obtain formal approval**: Written confirmation, any required waivers
7. **Coordinate logistics**: PPE, escorts, parking, check-in procedures
8. **Identify specific participants** for interviews/observation with site coordinator

**Site Recruitment Value Propositions:**

| Stakeholder | What They Care About | Your Offer |
|-------------|---------------------|------------|
| Executive sponsor | Business results, innovation | Early access to improvements, benchmarking insights |
| Operations manager | Efficiency, minimal disruption | Flexible scheduling, clear protocols |
| IT/Security | Data protection, system access | Data handling documentation, limited scope |
| HR/Legal | Employee protection, liability | Consent procedures, voluntary participation |
| Individual participants | Time, recognition, value | Respect for expertise, voice in product decisions |

---

### 4.3 Executing Recruitment

#### 4.3.1 Recruitment Outreach

**Email Outreach Template Structure:**

```
Subject: [Specific, benefit-oriented] - e.g., "Share your expertise on inventory management"

1. Who you are and why contacting them
2. What you're asking (specific activity and time)
3. What's in it for them (incentive, impact, early access)
4. Next step (clear CTA - screener link, reply, calendar link)
5. Opt-out and questions
```

**Outreach Best Practices:**

| Element | Recommendation |
|---------|----------------|
| Subject line | Specific and relevant, avoid "research study" which triggers spam filters |
| Sender | Individual name, not generic team address |
| Personalization | Reference their role, company, or how you found them |
| Length | Under 150 words for initial outreach |
| CTA | Single, clear action (not multiple options) |
| Mobile | Ensure readable on mobile devices |
| Timing | Tuesday-Thursday, 9-11am or 1-3pm recipient's timezone |
| Follow-up | 1-2 follow-ups spaced 3-5 days apart, then stop |

**Outreach Sequence (Cold):**

| Touch | Timing | Content Focus |
|-------|--------|---------------|
| Email 1 | Day 0 | Introduction, value proposition, screener link |
| Email 2 | Day 4 | Brief reminder, emphasize deadline or limited spots |
| Email 3 | Day 8 | Final reminder, alternative contact method |
| Stop | Day 10 | No further contact without response |

**Response Rate Benchmarks:**

| Audience | Expected Response Rate | Expected Qualification Rate |
|----------|------------------------|----------------------------|
| Existing customers (warm) | 15-25% | 40-60% |
| Existing customers (cold email) | 5-15% | 30-50% |
| Panel members | 10-20% | 50-70% |
| Cold prospect outreach | 2-5% | 20-40% |
| LinkedIn outreach | 5-10% | 30-50% |
| In-product intercept | 1-5% | 60-80% |

#### 4.3.2 Screening Process

**Screening Workflow:**

```
[Outreach] → [Screener Completion] → [Qualification Review] → [Selection] → [Invitation + Consent Sent] → [Scheduling] → [Consent Verified] → [Session]
```

**Consent Integration Note:** Consent form must be sent with the invitation email and verified as received/signed before the session begins. See UXR-001 Section 4.2 for detailed consent procedures. Track consent status in your participant log alongside recruitment status.

**Step 1: Collect Screener Responses**

- Use approved survey tool (Typeform, Qualtrics, Google Forms)
- Set expected completion time in introduction
- Include progress indicator
- Mobile-optimize all screeners
- Log completion rates and drop-off points

**Step 2: Review and Qualify Responses**

- Review responses within 24-48 hours of submission
- Score against criteria (Qualified / Not Qualified / Maybe)
- Check for response consistency and quality
- Flag potential professional respondents
- Document qualification decisions

**Qualification Decision Matrix:**

| Meets Primary Criteria | Meets Secondary Criteria | Response Quality | Decision |
|------------------------|--------------------------|------------------|----------|
| Yes | Yes | Good | Qualified - Priority |
| Yes | Partial | Good | Qualified - Standard |
| Yes | No | Good | Qualified - If needed |
| Yes | Any | Poor (inconsistent, minimal) | Review carefully |
| No | Any | Any | Not Qualified |

**Step 3: Select Final Participants**

Consider:
- Sample composition goals (quotas, diversity)
- Scheduling constraints
- Geographic distribution
- Over-recruitment needs (typically 10-20% extra)

**Step 4: Communicate Decisions**

| Decision | Communication | Timing |
|----------|---------------|--------|
| Qualified - Invite | Scheduling link + study details | Within 48 hours |
| Qualified - Waitlist | Thank you + waitlist status | Within 48 hours |
| Not Qualified | Thank you + brief reason (optional) | Within 1 week |
| No Response needed | No communication | N/A |

#### 4.3.3 Scheduling and Confirmation

**Scheduling Best Practices:**

| Practice | Rationale |
|----------|-----------|
| Offer specific time slots (not open calendar) | Reduces back-and-forth, maintains control |
| Include timezone clearly | Prevents confusion for remote sessions |
| Buffer 15-30 min between sessions | Allows for overrun and note-taking |
| Avoid Monday mornings, Friday afternoons | Lower show rates |
| Limit advance booking to 2 weeks | Longer lead times increase no-shows |
| Send calendar invite immediately | Gets session on participant's calendar |

**Confirmation Sequence:**

| Communication | Timing | Content |
|---------------|--------|---------|
| Initial confirmation | Immediately after scheduling | Date, time, duration, format, prep instructions |
| Calendar invite | Immediately | With video link or location, contact info |
| Reminder 1 | 2-3 days before | Confirm attendance, reiterate details |
| Reminder 2 | Day before or morning of | Final reminder, contact for issues |
| Post-session | Same day or next day | Thank you, incentive delivery info |

**Confirmation Email Must Include:**

- [ ] Date and time with timezone
- [ ] Duration
- [ ] Format (video call, phone, in-person location)
- [ ] Video conferencing link or address
- [ ] Researcher name and contact info
- [ ] What to prepare (if anything)
- [ ] Consent form (attached or linked) per UXR-001
- [ ] Cancellation/reschedule instructions

---

### 4.4 Managing No-Shows and Cancellations

#### 4.4.1 No-Show Prevention Strategies

**High-Impact Prevention Tactics:**

| Tactic | Impact | Implementation |
|--------|--------|----------------|
| Multiple reminders | High | Automated sequence at booking, 2-3 days, 1 day, 2 hours |
| Calendar invite | High | Send immediately with all details |
| Confirmation reply request | Medium | Ask participant to reply confirming attendance |
| Short lead time | Medium | Schedule within 1-2 weeks when possible |
| Flexible rescheduling | Medium | Make it easy to reschedule rather than no-show |
| Appropriate incentive | Medium | Incentive should match time and effort |
| Personal connection | Medium | Phone call confirmation for high-value sessions |
| SMS reminders | High | Add SMS for critical sessions (with consent) |

#### 4.4.2 Over-Recruitment Guidelines

**Standard Over-Recruitment Rates:**

| Participant Type | Expected Show Rate | Over-Recruit By |
|------------------|-------------------|-----------------|
| Customers (engaged) | 85-90% | 10-15% |
| Customers (general) | 75-85% | 15-20% |
| Panel participants | 70-80% | 20-25% |
| Cold recruited | 60-75% | 25-35% |
| B2B professionals | 80-90% | 10-15% |
| Field/site visits | 90-95% | 5-10% |

**Example Calculation:**

- Need: 10 completed sessions
- Expected show rate: 75%
- Calculation: 10 / 0.75 = 13.3
- Schedule: 14 participants (round up)
- If all show: Conduct all sessions or offer rescheduling to later study

#### 4.4.3 Handling No-Shows

**When Participant Doesn't Appear:**

1. **Wait 10 minutes** past scheduled start time
2. **Attempt contact** via email and phone
3. **Document** no-show in participant tracker
4. **Send follow-up** offering reschedule (once)
5. **Update status** and adjust recruitment if needed

**No-Show Follow-Up Email:**

```
Subject: Missed our session - reschedule?

Hi [Name],

We missed you at our scheduled session today at [time]. I hope everything is okay.

If you'd still like to participate, I have availability at:
- [Time 1]
- [Time 2]

If these don't work or you're no longer able to participate, just let me know.

Best,
[Researcher]
```

**When Participant Cancels:**

| Timing | Response | Incentive |
|--------|----------|-----------|
| 24+ hours notice | Thank, offer reschedule, backfill | None |
| <24 hours notice | Thank, offer reschedule if possible | None |
| Repeated cancellations | Remove from study | None |
| Emergency circumstance | Offer flexibility, reschedule | Partial at discretion |

---

### 4.5 Incentive Management

#### 4.5.1 Determining Appropriate Incentives

**Incentive Calculation Factors:**

| Factor | Higher Incentive | Lower Incentive |
|--------|------------------|-----------------|
| Time required | Longer sessions | Shorter sessions |
| Task difficulty | Complex tasks, preparation needed | Simple tasks |
| Participant type | Hard-to-reach, executives, specialists | General population |
| Recruitment source | Cold outreach | Engaged customers |
| Method | In-person, site visits | Remote, async |
| Topic sensitivity | Personal, professional risk | General, low-stakes |

**Standard Incentive Ranges:**

| Session Type | Duration | Consumer | Professional/B2B |
|--------------|----------|----------|------------------|
| Survey | 5-10 min | $5-15 | $10-25 |
| Survey | 15-30 min | $15-30 | $25-75 |
| Remote interview | 30 min | $50-75 | $100-150 |
| Remote interview | 60 min | $75-125 | $150-300 |
| Remote usability test | 30-45 min | $50-100 | $100-200 |
| In-person session | 60 min | $100-150 | $200-400 |
| Diary study | 1 week | $100-200 | $200-400 |
| Site visit participation | Half day | N/A | $300-500 |
| Focus group | 90 min | $100-175 | $200-350 |

**B2B Incentive Considerations:**

| Consideration | Guidance |
|---------------|----------|
| Corporate policies | Many companies prohibit employees accepting gifts >$25-50 |
| Alternative incentives | Charity donation, product credits, early access |
| Role level | Executives may prefer no incentive or charity donation |
| Relationship context | Customers may participate without incentive for relationship value |
| Documentation | Some companies require gift disclosure; provide receipts |

#### 4.5.2 Incentive Delivery

**Incentive Delivery Methods:**

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| Digital gift card (email) | Fast, easy, trackable | Impersonal, spam filters | Remote research, quick turnaround |
| Physical gift card | Tangible, immediate | Logistics, inventory | In-person research |
| Direct payment (PayPal, Venmo) | Flexible, fast | Tax implications, setup | Repeat participants, larger amounts |
| Prepaid debit card | Universal acceptance | Fulfillment complexity | High-value, diverse participants |
| Check | Traditional, documented | Slow, requires address | Large amounts, corporate requirements |
| Charity donation | Altruistic option | No direct benefit to participant | B2B, executives, sensitive contexts |
| Product/service credits | Brand alignment | Limited appeal | Existing customers |

**Delivery Timeline:**

| Timing | Method | Standard |
|--------|--------|----------|
| Immediate | Digital gift card | Within 24 hours of session completion |
| Same day | In-person | Hand delivered at session end |
| Standard | Any | Within 5 business days |
| Maximum | Any | Within 10 business days |

**Communicate incentive timeline in scheduling confirmation.**

#### 4.5.3 Incentive for Partial Participation

| Scenario | Incentive Recommendation |
|----------|-------------------------|
| Completes full session | Full incentive |
| Ends early (participant choice) | Full incentive if meaningful data collected |
| Ends early (technical issues) | Full incentive + offer to reschedule |
| Disqualified mid-session | Partial incentive (50%) or small thank-you |
| No-show, later completes | Full incentive for completed session |
| No-show, no reschedule | No incentive |

---

### 4.6 Participant Database and Panel Management

#### 4.6.1 Participant Database Requirements

**What to Track (per UXR-002 data handling requirements):**

| Field | Purpose | Retention |
|-------|---------|-----------|
| Participant ID | Unique identifier | Duration of database |
| Contact info | Scheduling, incentive delivery | Active + 6 months |
| Screener responses (qualified) | Qualification, future matching | 12 months |
| Screener responses (not qualified) | Future recruitment, dispute resolution | 90 days |
| Study participation | Prevent over-sampling | 24 months |
| Incentives received | Compliance, tracking | 24 months |
| Consent status | Compliance | Per UXR-001 |
| Communication preferences | Respect preferences | Duration of record |
| Do Not Contact flag | Respect opt-outs | Permanent |
| Quality notes | Future recruitment decisions | 24 months |

**Non-Qualified Respondent Data Handling:**

Screener responses from individuals who do not qualify contain PII and must be handled per UXR-002:

- **Retention:** 90 days maximum (allows for dispute resolution and study completion)
- **Storage:** Same security requirements as qualified participant data (Level 3 per UXR-002 Section 4.1)
- **Deletion:** Automatically delete after 90 days or at study completion, whichever is later
- **Exception:** If respondent opts into research panel, retain per panel member policies
- **Data Subject Requests:** Non-qualified respondents retain rights to access/deletion per UXR-002 Section 4.8

**Participant Database Tools:**

| Complexity | Recommended Tools |
|------------|-------------------|
| Simple (1-2 researchers) | Airtable, Notion, Google Sheets (encrypted) |
| Medium (small team) | Airtable, Dovetail, User Interviews |
| Complex (research ops) | Great Question, Respondent, Rally UXR |

#### 4.6.2 Research Panel Management

**Panel Health Metrics:**

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Active members (contacted in 12 mo) | >60% of total | Re-engagement campaign or removal |
| Response rate to invitations | >15% | Improve targeting, refresh panel |
| Qualification rate | >40% | Update profiles, better matching |
| Show rate | >80% | Improve reminders, incentives |
| Opt-out rate per campaign | <5% | Reduce frequency, improve relevance |

**Panel Maintenance Activities:**

| Activity | Frequency | Purpose |
|----------|-----------|---------|
| Profile update request | Annual | Keep screening data current |
| Engagement survey | Semi-annual | Understand panel experience |
| Inactive member cleanup | Quarterly | Remove unengaged members |
| New member recruitment | Ongoing | Replace attrition, grow coverage |
| Duplicate detection | Quarterly | Maintain data integrity |

**Preventing Panel Fatigue:**

- Limit contact to 1-2 invitations per month per member
- Track cumulative participation; rotate active participants
- Vary study types offered to same participants
- Provide feedback on how input was used
- Consider "rest periods" for frequent participants

#### 4.6.3 Handling Participant Relationship Issues

**Problematic Participant Behaviors:**

| Behavior | Response | Documentation |
|----------|----------|---------------|
| Professional respondent suspected | Exclude from current study, flag in database | Note in participant record |
| Dishonest screener responses | Disqualify, consider database removal | Document discrepancies |
| Abusive or inappropriate conduct | End session, permanent Do Not Contact | Incident report |
| Repeated no-shows (3+) | Remove from active recruitment | Note in participant record |
| Requests excessive contact | Honor preferences, reduce outreach | Update communication preferences |
| Incentive disputes | Review policy, resolve fairly | Document resolution |

**Participant Feedback Handling:**

- Thank participants who provide feedback on research experience
- Address legitimate concerns promptly
- Escalate serious issues to Research Lead
- Document feedback for process improvement
- Do not retaliate against participants who complain

---

### 4.7 Vendor and Agency Management

#### 4.7.1 Selecting Recruitment Vendors

**Vendor Evaluation Criteria:**

| Criteria | Weight | Questions to Ask |
|----------|--------|------------------|
| Audience access | High | Do they have access to your target population? |
| Quality controls | High | How do they prevent fraud and professional respondents? |
| Recruitment speed | Medium | Typical turnaround for your audience type? |
| Pricing model | Medium | Per recruit, project-based, or subscription? |
| Geographic coverage | Medium | Can they recruit in your target regions? |
| B2B capability | High (if B2B) | Experience with professional/executive recruitment? |
| Data handling | High | GDPR/CCPA compliance, data security certifications? |
| Communication | Medium | Responsiveness, transparency, reporting? |
| Flexibility | Low | Ability to handle custom requirements? |

**Common Recruitment Vendors:**

| Vendor Type | Examples | Best For |
|-------------|----------|----------|
| Panel aggregators | Respondent, User Interviews, Prolific | General audiences, fast recruitment |
| B2B specialists | GLG, NewtonX, Cascade Insights | Executives, industry professionals |
| Full-service agencies | Fieldwork, Focus Pointe, Schlesinger | Complex studies, in-facility research |
| Niche panels | Various specialty panels | Specific industries or conditions |

#### 4.7.2 Working with Recruitment Vendors

**Briefing Vendors:**

Provide in writing:
- [ ] Detailed recruitment criteria (screener)
- [ ] Number of participants needed
- [ ] Timeline (start recruiting, sessions complete by)
- [ ] Session format and duration
- [ ] Incentive amount (who pays - you or vendor?)
- [ ] Geographic requirements
- [ ] Any exclusions (competitors, recent research)
- [ ] Data handling requirements
- [ ] Quality requirements (verification, fraud checks)

**Managing Vendor Relationships:**

| Activity | Frequency | Purpose |
|----------|-----------|---------|
| Kick-off call | Per project | Align on requirements, timeline |
| Progress updates | 2-3x/week during recruitment | Monitor progress, adjust as needed |
| Participant reviews | Before session confirmation | Verify qualification, approve |
| Post-project debrief | Per project | Quality review, feedback |
| QBR (Quarterly Business Review) | Quarterly | Relationship health, improvements |

**Vendor Quality Issues:**

| Issue | Response |
|-------|----------|
| Low qualification rate | Review screener clarity, discuss targeting |
| Suspected fraud | Request verification, reject questionable recruits |
| Slow recruitment | Discuss barriers, adjust timeline or criteria |
| Poor participant quality | Document issues, provide feedback, consider alternate vendor |
| Data handling concerns | Stop work, escalate to legal/compliance |

---

## 5. Templates and Tools

### Template 5.1: Recruitment Criteria Definition

```
RECRUITMENT CRITERIA DEFINITION

Study Name: _______________
Study Code: _______________
Target Sample Size: _______________
Researcher: _______________
Date: _______________

PRIMARY CRITERIA (Must Have - all must be met):
1. _______________
2. _______________
3. _______________

SECONDARY CRITERIA (Nice to Have - preferred):
1. _______________
2. _______________

QUOTA CRITERIA (Distribution targets):
| Attribute | Target Distribution |
|-----------|---------------------|
| | |
| | |

EXCLUSION CRITERIA (Automatic disqualification):
1. Participated in research within [X] months
2. Works for competitor: [list competitors]
3. Works in market research, UX, or advertising
4. _______________
5. _______________

SAMPLE COMPOSITION GOALS:
[ ] Variation in _______________
[ ] Mix of _______________
[ ] Representation from _______________

ARTICULATION REQUIREMENTS:
[ ] Standard - Can express basic preferences and experiences
[ ] High - Must provide detailed explanations and reasoning
[ ] Expert - Subject matter expertise expected

APPROVED BY: _______________ DATE: _______________
```

---

### Template 5.2: Screener Template

```
SCREENER: [STUDY NAME]

---
PAGE 1: INTRODUCTION
---

Thank you for your interest in participating in a research study conducted by [Company].

This brief survey will help us determine if you're a good fit for an upcoming study about [general topic - don't reveal specifics].

The survey takes approximately [X] minutes.

If you qualify and participate, you will receive [incentive] for your time.

Your responses are confidential and used only to determine study eligibility.

[ ] I understand and wish to continue
[ ] I do not wish to participate

---
PAGE 2: DISQUALIFICATION SCREENING
---

Q1. Do you or anyone in your immediate household work in any of the following industries?
[ ] Market research
[ ] Advertising or public relations
[ ] UX design or user research
[ ] [Relevant competitor industry]
[ ] None of the above ← CONTINUE

[If any except "None" selected → Thank and close]

Q2. Have you participated in a paid research study in the past [3/6] months?
[ ] Yes → How many? _____ [If >3, Thank and close]
[ ] No ← CONTINUE

Q3. Do you currently work for [Company] or any of its subsidiaries?
[ ] Yes → [Thank and close OR route to employee track]
[ ] No ← CONTINUE

---
PAGE 3: PRIMARY CRITERIA
---

Q4. [Primary criterion 1 - behavioral question]
Example: "How often do you use inventory management software in your work?"
[ ] Daily ← QUALIFIES
[ ] Several times a week ← QUALIFIES
[ ] Weekly ← QUALIFIES
[ ] Less than weekly → [Thank and close]
[ ] Never → [Thank and close]

Q5. [Primary criterion 2]
[Include qualification logic]

Q6. [Primary criterion 3]
[Include qualification logic]

---
PAGE 4: SECONDARY CRITERIA / QUOTAS
---

Q7. [Quota criterion - e.g., company size]
[ ] 1-50 employees [QUOTA: 5]
[ ] 51-500 employees [QUOTA: 5]
[ ] 500+ employees [QUOTA: 5]

Q8. [Secondary criterion - nice to have]

Q9. [Industry/segment if relevant]

---
PAGE 5: ARTICULATION CHECK (for interviews)
---

Q10. In a few sentences, describe [relevant task/challenge]. What makes it difficult or time-consuming?

[Open text - minimum 50 characters]
[Review for articulation ability, relevance, thoughtfulness]

---
PAGE 6: LOGISTICS
---

Q11. This study involves a [60-minute video interview / 30-minute usability session / etc.].
Are you able to participate during [date range]?
[ ] Yes ← CONTINUE
[ ] No → [Offer waitlist or thank and close]

Q12. What is your general availability? (Select all that apply)
[ ] Weekday mornings (9am-12pm)
[ ] Weekday afternoons (12pm-5pm)
[ ] Weekday evenings (5pm-8pm)
[ ] Weekends

Q13. What timezone are you in?
[Dropdown of timezones]

---
PAGE 7: CONTACT INFORMATION
---

Q14. First name: _______________
Q15. Last name: _______________
Q16. Email address: _______________
Q17. Phone number (optional, for reminders): _______________

Privacy notice: Your information will be used only to contact you about this study and will be handled per our privacy policy [link]. You can withdraw at any time by contacting [email].

---
THANK YOU PAGE (Qualified)
---

Thank you for completing the screener! Based on your responses, you may be a good fit for our study.

We will review your responses and contact you within [X business days] if you are selected to participate.

---
THANK YOU PAGE (Not Qualified)
---

Thank you for your interest in our research study.

Based on your responses, you are not a fit for this particular study. We appreciate your time and may contact you about future opportunities if you've opted in to our research panel.
```

---

### Template 5.3: Participant Tracking Spreadsheet

```
PARTICIPANT TRACKING LOG

Study: _______________
Researcher: _______________

| ID | Name | Email | Phone | Screener Date | Qualified | Consent Sent | Consent Signed | Invited | Scheduled | Confirmed | Attended | Incentive Sent | Notes |
|----|------|-------|-------|---------------|-----------|--------------|----------------|---------|-----------|-----------|----------|----------------|-------|
| P01 | | | | | Y/N | [Date] | Y/N | Y/N | [DateTime] | Y/N | Y/N | [Date] | |
| P02 | | | | | | | | | | | | | |

**Consent Status Key:**
- Consent Sent: Date consent form was emailed/provided to participant
- Consent Signed: Y = Signed form received, N = Pending, X = Declined (remove from study)

**Important:** Do not proceed to session if Consent Signed = N or X. See UXR-001 for consent requirements.

QUOTA TRACKING:

| Quota Criterion | Target | Scheduled | Completed |
|-----------------|--------|-----------|-----------|
| | | | |

SUMMARY METRICS:

| Metric | Count |
|--------|-------|
| Total screener responses | |
| Qualified | |
| Invited | |
| Scheduled | |
| Confirmed | |
| Completed | |
| No-shows | |
| Cancellations | |

Qualification Rate: ____%
Show Rate: ____%
```

---

### Template 5.4: Recruitment Outreach Email

**Subject Lines (A/B test):**
- Share your perspective on [topic] - [incentive] thank you
- [Company] research: Your expertise needed
- Quick feedback opportunity - [duration] for [incentive]

---

**Cold Outreach - Professional:**

Subject: Your expertise on [topic] - quick research opportunity

Hi [Name],

I'm [Your Name], a researcher at [Company]. We're conducting a study to better understand how [role/industry] professionals handle [specific challenge], and your experience would be incredibly valuable.

**What's involved:**
- [Duration] video conversation
- Discuss your experience with [topic]
- [Incentive] as a thank-you for your time

**Why you:** [Brief personalization - their role, company, background]

If you're interested, please complete this 3-minute screener: [Link]

I'm scheduling sessions for [date range]. Happy to answer any questions at [email] or [phone].

Thank you for considering,
[Your Name]
[Title, Company]

---

**Warm Outreach - Customer:**

Subject: Help shape the future of [Product] - research opportunity

Hi [Name],

I'm reaching out because you're a [Product] user, and we'd love to learn from your experience.

We're conducting research to improve [specific area], and your insights would directly influence what we build next.

**Details:**
- [Duration] video conversation
- Share your workflow and challenges
- [Incentive] thank-you gift

Interested? Here's a quick screener: [Link]

Feel free to reach out with any questions.

Best,
[Your Name]
UX Researcher, [Company]

---

**Reminder - First:**

Subject: Quick reminder: Research opportunity closing soon

Hi [Name],

Just a friendly reminder about the research opportunity I shared [X days ago]. We have a few spots remaining for [dates].

Quick screener: [Link]

Let me know if you have any questions!

[Your Name]

---

### Template 5.5: Confirmation Email

Subject: Confirmed: Research session [Date] at [Time]

Hi [Name],

Great news - you're confirmed for our research session!

**Session Details:**
- **Date:** [Day, Date]
- **Time:** [Time] [Timezone]
- **Duration:** [X] minutes
- **Format:** [Video call via Zoom / In-person at address]
- **Link:** [Video link if applicable]

**What to expect:**
[Brief description of what will happen during the session]

**Please prepare:**
- [Any preparation needed - or "No preparation needed"]
- Quiet space with stable internet (for video calls)

**Attached:** Consent form - please review before our session

**Questions or need to reschedule?**
Contact me at [email] or [phone]

Looking forward to speaking with you!

[Your Name]
[Title, Company]

---

### Template 5.6: Vendor Briefing Document

```
RECRUITMENT BRIEFING

Project: _______________
Date: _______________
Researcher: _______________

OVERVIEW
Study objective: _______________
Methodology: _______________
Timeline: Recruiting [date] - Sessions complete by [date]

REQUIREMENTS
Number of participants needed: _______________
Session format: [Video call / In-person / etc.]
Session duration: _______________
Session dates/times available: _______________

RECRUITMENT CRITERIA

Must Have (all required):
1. _______________
2. _______________
3. _______________

Must NOT Have (exclude if any):
1. _______________
2. _______________

Quotas (if applicable):
| Attribute | Number Needed |
|-----------|---------------|
| | |

PARTICIPANT QUALITY REQUIREMENTS
- [ ] Must pass articulation check
- [ ] Verification required: [phone / LinkedIn / employment]
- [ ] No professional respondents (max [X] studies in [Y] months)

LOGISTICS
Incentive amount: _______________
Incentive paid by: [ ] Us [ ] Vendor
Timezone requirements: _______________
Language requirements: _______________

DATA HANDLING
- Screener data shared with research team: [ ] Yes [ ] No
- Participant PII handling: [Requirements per UXR-002]
- Data deletion requirement: [Timeframe]

COMMUNICATION
Primary contact: _______________
Reporting frequency: _______________
Approval required before confirming: [ ] Yes [ ] No

SCREENER
[ ] Attached
[ ] To be provided by [date]
[ ] Vendor to draft based on above criteria

APPROVED BY: _______________ DATE: _______________
```

---

### 5.7 Recommended Tools

| Function | Tools | Notes |
|----------|-------|-------|
| Screener surveys | Typeform, Qualtrics, Google Forms | Use branching logic for qualification |
| Scheduling | Calendly, Cal.com, Microsoft Bookings | Include buffer time, timezone handling |
| Participant database | Airtable, Notion, Great Question | Secure storage, access controls per UXR-002 |
| Panel management | Great Question, User Interviews, Rally | Built-in compliance features |
| Digital incentives | Tremendous, Tango Card, Amazon | Bulk sending, tracking, international support |
| Email outreach | Mail merge, HubSpot, Research-specific tools | Track opens/responses |
| Video conferencing | Zoom, Microsoft Teams, Google Meet | Recording capability, waiting rooms |
| Recruitment vendors | Respondent, User Interviews, GLG | Evaluate per Section 4.7 |

---

## 6. Responsibilities

### RACI Matrix

| Activity | Research Lead | Researcher | Research Ops | Account Team | Vendor |
|----------|---------------|------------|--------------|--------------|--------|
| Define recruitment criteria | A | R | C | C | I |
| Develop screener | A | R | S | - | I |
| Select recruitment source | A | R | C | C | - |
| Execute outreach (internal) | I | R | S | S | - |
| Execute outreach (vendor) | A | C | R | - | R |
| Screen and qualify | A | R | S | - | S |
| Schedule participants | I | R | R | - | - |
| Send confirmations | I | R | R | - | - |
| Manage no-shows | I | R | S | - | - |
| Deliver incentives | A | R | R | - | - |
| Maintain participant database | A | R | R | - | - |
| Manage vendor relationships | A | I | R | - | - |
| Resolve participant issues | A | R | S | C | - |

**R** = Responsible (does the work)
**A** = Accountable (ultimate ownership)
**C** = Consulted (provides input)
**I** = Informed (kept updated)
**S** = Supports (assists as needed)

### Role Definitions

**Research Lead:**
- Approves recruitment criteria for alignment with research objectives
- Sets quality standards for participant selection
- Approves vendor selection and contracts
- Resolves escalated participant issues
- Monitors recruitment metrics and quality

**Researcher:**
- Defines recruitment criteria based on study needs
- Develops and tests screener questionnaire
- Executes or coordinates recruitment activities
- Reviews and qualifies screener responses
- Schedules and confirms participants
- Delivers incentives per timeline
- Maintains accurate participant tracking
- Handles day-to-day participant communication

**Research Operations:**
- Manages participant database infrastructure
- Maintains panel health and recruitment tools
- Coordinates vendor relationships and contracts
- Supports scheduling and logistics
- Tracks recruitment metrics across studies
- Ensures compliance with data handling requirements

**Account Team (for B2B):**
- Provides warm introductions to customer contacts
- Advises on account relationship sensitivity
- Approves contact with strategic accounts
- Facilitates gatekeeper navigation

**Recruitment Vendor:**
- Sources and screens participants per brief
- Provides qualified participant recommendations
- Manages scheduling logistics (if contracted)
- Reports on recruitment progress
- Maintains data handling compliance

---

## 7. Quality Checks

### 7.1 Pre-Recruitment Checklist

Before launching recruitment:

- [ ] Recruitment criteria documented and approved
- [ ] Sample size and composition defined
- [ ] Screener developed and tested
- [ ] Recruitment source(s) selected
- [ ] Outreach messages drafted
- [ ] Scheduling tool configured
- [ ] Confirmation sequence prepared
- [ ] Incentive amount approved and funded
- [ ] Incentive delivery method ready
- [ ] Participant tracking set up
- [ ] Consent form ready (per UXR-001)
- [ ] Data handling compliant (per UXR-002)

### 7.2 Screener Quality Review

Before launching screener:

| Check | Pass? |
|-------|-------|
| Disqualifying questions appear early | [ ] |
| No leading questions that reveal "right" answer | [ ] |
| Answer options are mutually exclusive | [ ] |
| Professional respondent check included | [ ] |
| Articulation question included (for interviews) | [ ] |
| Mobile-friendly format | [ ] |
| Completion time tested and accurate | [ ] |
| Branching logic works correctly | [ ] |
| Privacy notice and consent included | [ ] |
| Thank you pages appropriate for qualified/not qualified | [ ] |

### 7.3 Recruitment Progress Monitoring

Track daily during active recruitment:

| Metric | Target | Day 1 | Day 3 | Day 5 | Final |
|--------|--------|-------|-------|-------|-------|
| Outreach sent | [X] | | | | |
| Screener starts | [X] | | | | |
| Screener completes | [X] | | | | |
| Qualified | [X] | | | | |
| Scheduled | [X] | | | | |
| Confirmed | [X] | | | | |

**Action Triggers:**
- Qualification rate <30%: Review screener, adjust criteria or targeting
- Response rate <5%: Adjust outreach, try alternate source
- Schedule rate <70% of qualified: Improve follow-up, adjust times offered

### 7.4 Post-Session Quality Check

After each session:

| Check | Completed? |
|-------|------------|
| Participant attended | [ ] |
| Participant met stated criteria | [ ] |
| Participant able to articulate relevant experience | [ ] |
| Session yielded useful data | [ ] |
| Incentive sent/delivered | [ ] |
| Participant record updated | [ ] |
| Any quality notes recorded | [ ] |

### 7.5 Post-Study Recruitment Review

After recruitment completes:

| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Total participants completed | [X] | | |
| Qualification rate | >40% | | |
| Show rate | >80% | | |
| Sample composition met | Y/N | | |
| Avg. time from outreach to scheduled | <7 days | | |
| Avg. time from screener to session | <14 days | | |
| Cost per completed participant | $[X] | | |
| Participant quality rating (1-5) | >4 | | |

**Lessons Learned:**
- What worked well?
- What would we do differently?
- Updates needed to criteria, screener, or process?

---

## 8. Related Documents

| Document ID | Title | Relationship |
|-------------|-------|--------------|
| UXR-001 | Informed Consent & Ethics | Consent procedures for recruited participants |
| UXR-002 | Data Handling & Privacy | Participant data storage and handling |
| UXR-004 | Research Planning & Scoping | Study design informs recruitment criteria |
| [FIN-XXX] | Research Incentive Policy | Incentive approvals and accounting |
| [LEGAL-XXX] | Vendor Contracts | Recruitment vendor agreements |
| [SEC-XXX] | Third-Party Data Policy | Vendor data handling requirements |

---

## 9. Revision History

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 2026-01-16 | [Name] | Initial release | [Name] |
| | | | | |

### Review Schedule

| Review Type | Frequency | Next Review | Owner |
|-------------|-----------|-------------|-------|
| Content accuracy | Annual | 2027-01-16 | Research Lead |
| Process updates | Semi-annual | 2026-07-16 | Research Ops |
| Tool/vendor review | Annual | 2027-01-16 | Research Ops |
| Compliance check | Annual | 2027-01-16 | Research Lead |

---

## Appendix A: Quick Reference Card

### Recruitment Timeline Quick Guide

| Task | Standard Timeline |
|------|-------------------|
| Define criteria | Study planning phase |
| Build screener | 1-2 days |
| Launch recruitment | 1-2 weeks before sessions |
| Screen responses | Within 48 hours of receipt |
| Invite qualified participants | Within 48 hours of qualification |
| Send confirmation | Immediately after scheduling |
| Send reminder 1 | 2-3 days before session |
| Send reminder 2 | Day before or morning of |
| Deliver incentive | Within 5 business days of session |

### Over-Recruitment Quick Reference

| If you need | And expect show rate of | Then schedule |
|-------------|------------------------|---------------|
| 5 | 80% | 6-7 |
| 8 | 80% | 10 |
| 10 | 75% | 13-14 |
| 12 | 75% | 16 |
| 15 | 70% | 21-22 |

### Incentive Quick Reference

| Session Type | Duration | Standard Range |
|--------------|----------|----------------|
| Survey | 10-15 min | $10-25 |
| Remote interview | 30 min | $75-150 |
| Remote interview | 60 min | $125-300 |
| Usability test | 45 min | $75-150 |
| In-person | 60 min | $150-300 |
| Diary study | 1 week | $150-300 |

---

## Appendix B: Common Problems and Solutions

**Q: Not getting enough screener responses**

A: Check:
- Subject line effectiveness (A/B test)
- Outreach timing (Tue-Thu optimal)
- Targeting accuracy (right audience?)
- Value proposition clarity (what's in it for them?)
- Try alternate recruitment source

**Q: High screener completion but low qualification rate**

A: Check:
- Criteria too restrictive?
- Targeting reaching wrong audience?
- Screener questions revealing "right" answers?
- Consider loosening secondary criteria

**Q: Qualified participants not scheduling**

A: Check:
- Follow-up timing (within 48 hours?)
- Availability options sufficient?
- Incentive competitive?
- Scheduling friction (too many steps?)
- Add phone follow-up for high-value participants

**Q: High no-show rate**

A: Check:
- Confirmation sequence complete?
- Lead time too long? (>2 weeks increases no-shows)
- Reminders being received? (check spam)
- Incentive motivating enough?
- Add calendar invite immediately
- Consider SMS reminders

**Q: Participants don't match screener responses**

A: Check:
- Screener questions ambiguous?
- Professional respondent gaming screener?
- Add verification step (phone screen, LinkedIn check)
- Include consistency checks in screener
- Brief vendor on quality issues

**Q: B2B recruitment taking too long**

A: Check:
- Warm introduction available? (ask account team)
- Gatekeeper blocking? (provide more documentation)
- Offer organizational benefit (findings, early access)
- Extend timeline or reduce sample
- Try alternate recruitment source

---

**Document Control:**
- This document is controlled. Printed copies are for reference only.
- Current version available at: [Insert location]
- Questions: Contact Research Lead

**Emergency Contact:**
- Recruitment issues: Research Operations or Research Lead
- Vendor issues: Research Operations
