# UXR-002: Data Handling & Privacy Standard Operating Procedure

**Document ID:** UXR-002
**Version:** 1.0
**Effective Date:** January 15, 2026
**Last Review:** January 15, 2026
**Document Owner:** UX Research Lead
**Classification:** Internal Use Only

---

## 1. Purpose

This Standard Operating Procedure establishes the requirements and procedures for handling research data in compliance with privacy regulations (GDPR, CCPA) and organizational security policies. It ensures the protection of research participant information while maintaining the integrity and usefulness of research data for product decisions.

**Objectives:**
- Protect participant privacy and personal information throughout the research lifecycle
- Ensure compliance with GDPR, CCPA, and applicable industry regulations
- Establish clear data classification, handling, and retention standards
- Define procedures for responding to data subject requests and security incidents
- Address B2B-specific considerations including proprietary information and NDA requirements
- Enable consistent, auditable data practices across the research team

---

## 2. Scope

**This SOP applies to:**
- All UX research data collected from human participants
- All research team members, contractors, and vendors with data access
- All research methods generating participant data (interviews, surveys, usability tests, field studies, diary studies)
- Both digital and physical data storage
- Data from consumer and B2B research participants

**This SOP covers:**
- Personal and business participant data
- Research recordings (audio, video, screen capture)
- Survey responses and behavioral data
- Observational notes and photographs
- Proprietary business information shared during research
- Third-party tools and cloud storage platforms

**Out of scope:**
- Product analytics and telemetry data (see Data Analytics SOP)
- Marketing research conducted by other departments
- Customer support interaction logs

---

## 3. Definitions

| Term | Definition |
|------|------------|
| **Personal Data (PII)** | Any information relating to an identified or identifiable natural person: name, email, phone, IP address, employee ID, voice/image recordings, location data |
| **Sensitive Personal Data** | Special category data requiring additional protections: health information, biometric data, racial/ethnic origin, political opinions, religious beliefs, sexual orientation, trade union membership |
| **Confidential Business Information** | Proprietary data shared by B2B participants: trade secrets, financial data, unreleased product information, internal processes, competitive intelligence |
| **Data Subject** | The individual whose personal data is being processed (research participant) |
| **Data Controller** | The organization determining purposes and means of processing (our company) |
| **Data Processor** | Third parties processing data on our behalf (research tools, transcription services) |
| **Processing** | Any operation on personal data: collection, recording, storage, analysis, sharing, deletion |
| **Consent** | Freely given, specific, informed, and unambiguous indication of agreement to data processing |
| **Data Subject Request (DSR)** | Formal request from individual to access, correct, delete, or port their data |
| **Data Breach** | Security incident leading to accidental or unlawful destruction, loss, alteration, unauthorized disclosure, or access to personal data |
| **Pseudonymization** | Processing personal data so it cannot be attributed to a specific person without additional information kept separately |
| **Anonymization** | Irreversibly processing data so individuals cannot be identified directly or indirectly |
| **Retention Period** | Defined timeframe for keeping data before mandatory deletion |
| **NDA** | Non-Disclosure Agreement governing confidential information handling |

---

## 4. Procedure

### 4.1 Data Classification

**Step 1: Classify all research data at project initiation**

Before collecting any data, complete the Data Classification Assessment for the study:

**Classification Levels:**

| Level | Description | Examples | Handling Requirements |
|-------|-------------|----------|----------------------|
| **Level 1: Public** | Non-sensitive, aggregated, anonymized | Published research summaries, anonymized statistics | Standard security, no special handling |
| **Level 2: Internal** | Business information, pseudonymized data | Coded transcripts, aggregated survey data, journey maps | Access controls, secure storage |
| **Level 3: Confidential PII** | Identifiable personal data | Contact lists, consent forms, recordings with faces/voices | Encryption, limited access, retention limits |
| **Level 4: Restricted** | Sensitive personal data OR highly confidential business info | Health-related research, financial data, trade secrets | Maximum security, explicit consent, strict access, audit logging |

**Step 2: Document classification in Research Data Inventory**

For each study, record:
- Data types collected
- Classification level for each type
- Storage location
- Access permissions
- Retention period
- Deletion date

---

### 4.2 Data Collection

**Step 3: Obtain valid consent before any data collection**

**Consent Requirements (GDPR Article 7, CCPA 1798.100):**

- [ ] Consent is freely given (no coercion, real choice to decline)
- [ ] Consent is specific (identifies exact purposes and data types)
- [ ] Consent is informed (participant understands what they are agreeing to)
- [ ] Consent is unambiguous (clear affirmative action, no pre-checked boxes)
- [ ] Consent is documented (signed form or recorded verbal agreement)
- [ ] Consent covers all processing activities (recording, analysis, storage, sharing)
- [ ] Consent explains data retention periods
- [ ] Consent describes participant rights (access, deletion, withdrawal)
- [ ] For sensitive data: explicit consent obtained with specific justification

**For B2B Research - Additional Requirements:**
- [ ] Participant has authority to share organizational information
- [ ] Company NDA in place if proprietary information will be discussed
- [ ] Consent clarifies what information can/cannot be shared externally
- [ ] Participant acknowledges any recording of confidential business information

**Step 4: Collect only necessary data (data minimization)**

Before each study, answer:
- What data is essential for the research objectives?
- Can we achieve objectives with less identifying information?
- Can we pseudonymize data during collection rather than after?

**Prohibited data collection without explicit approval:**
- Government ID numbers (SSN, passport, driver's license)
- Financial account numbers
- Passwords or authentication credentials
- Health/medical information (unless study purpose requires it)
- Biometric data for identification purposes
- Data from minors under 16 (GDPR) or 13 (COPPA)

**Step 5: Implement secure collection methods**

| Collection Method | Security Requirements |
|-------------------|----------------------|
| Video calls | Use approved platforms only (see Section 5), enable waiting rooms, use unique meeting IDs |
| Screen recording | Notify participant before starting, pause for sensitive information entry |
| Surveys | Use approved survey tools with encryption, avoid collecting IP unless necessary |
| In-person | Secure recording devices, no cloud auto-sync, physical consent forms locked |
| Field studies | Photograph/video consent from all visible individuals, facility photo release |
| Diary studies | Encrypted submission channels, remind participants not to share others' PII |

---

### 4.3 Data Storage and Access Controls

**Step 6: Store data in approved locations only**

**Approved Storage Locations:**

| Data Classification | Approved Storage | Prohibited Storage |
|--------------------|------------------|-------------------|
| Level 1: Public | Company cloud drive, shared folders | Personal devices |
| Level 2: Internal | Research team drive, approved tools | Personal cloud storage, email attachments |
| Level 3: Confidential PII | Encrypted research repository, approved tools with BAA | Shared drives without access controls, local unencrypted storage |
| Level 4: Restricted | Encrypted repository with audit logging, limited access folder | Any shared location, any tool without security certification |

**Storage Security Requirements:**
- All PII stored in cloud systems with SOC 2 Type II certification
- Encryption at rest (AES-256 minimum)
- Encryption in transit (TLS 1.2 minimum)
- Multi-factor authentication for all access
- Geographic data residency compliance (EU data stays in EU for GDPR)

**Step 7: Implement access controls**

**Access Control Matrix:**

| Role | Level 1 | Level 2 | Level 3 | Level 4 |
|------|---------|---------|---------|---------|
| Research Lead | Full | Full | Full | Full |
| Researcher | Full | Full | Full | Project-specific approval |
| Research Contractor | Project-specific | Project-specific | Supervised only | No access |
| Design/Product Team | Full | View reports | Anonymized only | No access |
| External Stakeholders | Approved reports | No access | No access | No access |

**Access Provisioning Process:**
1. Research Lead approves access requests
2. Document access grant in Access Log
3. Use role-based permissions (not individual file sharing)
4. Review access quarterly, remove when project ends
5. Immediately revoke access when team members leave

**Step 8: Secure file naming and organization**

**File Naming Convention (no PII in filenames):**
```
[ProjectCode]_[DataType]_[Date]_[Sequence].[ext]

Examples:
PRJ2026-014_Interview_20260115_P01.mp4
PRJ2026-014_Transcript_20260115_P01.docx
PRJ2026-014_Survey_20260120_Raw.csv
```

**Folder Structure:**
```
/Research Projects
  /[Year]
    /[Project Code] - [Project Name]
      /01_Planning (protocols, guides)
      /02_Consent (signed forms - Level 3)
      /03_Raw Data (recordings, exports - Level 3-4)
      /04_Analysis (coded transcripts - Level 2-3)
      /05_Outputs (reports, presentations - Level 1-2)
      /06_Participant Log (link table - Level 3)
```

---

### 4.4 Pseudonymization and Anonymization

**Step 9: Pseudonymize data immediately after collection**

**Pseudonymization Process:**
1. Create Participant Code Key (separate, secured document linking codes to identities)
2. Replace names with codes in all working documents: P01, P02, etc.
3. Remove or code company names for B2B: "Company A," "Large Manufacturer"
4. Store Participant Code Key separately from research data
5. Restrict Code Key access to Research Lead and primary researcher only

**B2B Pseudonymization Considerations:**
- Code industry-specific details that could identify company
- Remove product names, project names, specific locations
- Generalize company size/revenue to ranges
- Code competitor names mentioned in sessions

**Step 10: Anonymize data for long-term retention and sharing**

**Anonymization Checklist (before sharing or archiving):**
- [ ] Remove all direct identifiers (names, emails, employee IDs)
- [ ] Remove or generalize indirect identifiers (job title + company + location = identifiable)
- [ ] Remove or blur faces in photos/videos
- [ ] Remove or distort voices in audio
- [ ] Remove metadata containing identifiers (file properties, GPS data)
- [ ] Generalize demographic details (age ranges, region vs. city)
- [ ] Remove unique verbatim quotes that could identify individuals
- [ ] For B2B: remove project names, specific product details, unique processes

**Anonymization is irreversible - verify you no longer need identified data before anonymizing**

---

### 4.5 Data Retention and Deletion

**Step 11: Apply retention periods based on data type**

**Standard Retention Schedule:**

| Data Type | Retention Period | Justification | Deletion Trigger |
|-----------|------------------|---------------|------------------|
| Consent forms | Duration of data retention + 3 years | Legal compliance, audit trail | 3 years after all associated data deleted |
| Contact information | Project duration + 30 days | Follow-up, incentive delivery | 30 days after final participant contact |
| Raw recordings (video/audio) | 12 months from collection | Analysis, verification | Automatic deletion at 12 months |
| Transcripts (identified) | 18 months from collection | Extended analysis, quotes | Automatic deletion at 18 months |
| Transcripts (pseudonymized) | 3 years from collection | Longitudinal analysis, reanalysis | Automatic deletion at 3 years |
| Survey responses (identified) | 18 months from collection | Follow-up analysis | Automatic deletion at 18 months |
| Survey responses (anonymized) | 7 years | Trend analysis, benchmarking | Business need review at 7 years |
| Analysis files | 3 years from project completion | Reference, similar projects | Automatic deletion at 3 years |
| Final reports (anonymized) | Indefinite | Organizational knowledge | N/A |
| Participant Code Key | Same as longest-retained associated data | Re-identification if legally required | When all associated data deleted |

**B2B/Industrial Research Adjustments:**
- NDA-covered data: Retain per NDA terms (often 3-5 years), then delete
- Proprietary process documentation: Delete within 6 months unless anonymized
- Competitive intelligence: Delete within 12 months, never include in shared reports

**Step 12: Execute deletion procedures**

**Deletion Checklist:**

1. **Identify all data locations:**
   - [ ] Primary storage repository
   - [ ] Backup systems
   - [ ] Research tool platforms (survey tools, transcription services)
   - [ ] Communication tools (email, Slack) - remove attachments/references
   - [ ] Personal devices (if any local copies exist)
   - [ ] Physical documents

2. **Execute deletion:**
   - [ ] Delete files from primary storage
   - [ ] Empty trash/recycle bin
   - [ ] Request deletion from third-party processors (per DPA)
   - [ ] Shred physical documents (cross-cut shredder)
   - [ ] Delete local copies from any devices
   - [ ] Remove data from backups within 90 days (or document exception)

3. **Document deletion:**
   - [ ] Record deletion date in Data Inventory
   - [ ] Record deletion method
   - [ ] Retain deletion record for audit (5 years)
   - [ ] Update Participant Code Key (mark as deleted)

**Automated Deletion:**
- Set calendar reminders at data collection for retention deadlines
- Use cloud storage retention policies where available
- Quarterly audit of data approaching retention limits

---

### 4.6 GDPR Compliance Requirements

**Step 13: Maintain GDPR compliance for EU participants**

**GDPR Principles (Article 5) Checklist:**

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| Lawfulness, fairness, transparency | Valid legal basis, honest about processing | Consent forms, privacy notices |
| Purpose limitation | Collect for specified purposes only | Document purpose in study protocol |
| Data minimization | Collect only what's necessary | Pre-study data necessity review |
| Accuracy | Keep data accurate, allow corrections | Participant review process, correction procedures |
| Storage limitation | Don't keep longer than necessary | Retention schedule, deletion procedures |
| Integrity and confidentiality | Secure processing | Encryption, access controls, security tools |
| Accountability | Demonstrate compliance | Documentation, audits, training |

**Legal Basis for Processing (choose one per study):**
- **Consent** (most common for research) - documented, withdrawable
- **Legitimate interest** - must document assessment, balance against participant rights
- **Contract** - if research is part of contracted service

**Required Documentation:**
- [ ] Privacy notice provided to participants before consent
- [ ] Record of processing activities maintained
- [ ] Data Protection Impact Assessment for high-risk processing
- [ ] Data Processing Agreements with all vendors

**EU Data Residency:**
- Store EU participant data in EU data centers OR
- Ensure adequate transfer mechanisms (Standard Contractual Clauses, adequacy decisions)
- Document transfer safeguards

---

### 4.7 CCPA Compliance Requirements

**Step 14: Maintain CCPA compliance for California residents**

**CCPA Rights (must honor for California residents):**

| Right | Description | Response Deadline |
|-------|-------------|-------------------|
| Right to Know | What personal information is collected, used, shared | 45 days |
| Right to Delete | Request deletion of personal information | 45 days |
| Right to Opt-Out | Decline sale of personal information | Immediate |
| Right to Non-Discrimination | Equal service regardless of privacy choices | Ongoing |
| Right to Correct | Request correction of inaccurate information | 45 days |
| Right to Limit | Limit use of sensitive personal information | Immediate |

**CCPA-Specific Requirements:**
- [ ] Privacy notice includes CCPA-required disclosures
- [ ] "Do Not Sell My Personal Information" option (if applicable)
- [ ] Designated methods for submitting requests
- [ ] Verification procedures for requestors
- [ ] Response within 45 days (one 45-day extension permitted)

**Note:** UX research typically does not "sell" personal information under CCPA definition. However, sharing with third-party processors requires disclosure.

---

### 4.8 Handling Data Subject Requests

**Step 15: Respond to access, correction, and deletion requests**

**Data Subject Request (DSR) Response Procedure:**

**Day 0: Request received**
1. Log request in DSR Tracking Log (date, requestor, request type, source)
2. Acknowledge receipt within 3 business days
3. Assign request owner (Research Lead or designated handler)

**Days 1-5: Verification**
4. Verify requestor identity:
   - Match email/name to participant records
   - If uncertain, request additional verification (last study participated in, approximate date)
   - Do not disclose whether individual is in database until verified
5. Determine applicable regulations (GDPR, CCPA, other)
6. Confirm request scope (all data or specific study)

**Days 5-15: Data compilation**
7. Search all data storage locations for requestor's data:
   - Research repository
   - Survey tools
   - Transcription services
   - Consent form storage
   - Communication records
8. Compile data inventory for requestor

**Days 15-30: Response preparation**
9. Prepare response based on request type:

| Request Type | Response Actions |
|--------------|------------------|
| **Access** | Compile readable report of all data held, purposes, recipients, retention |
| **Correction** | Update inaccurate data, document changes |
| **Deletion** | Execute deletion procedure (Step 12), document completion |
| **Portability** | Export data in common format (CSV, JSON) |
| **Withdrawal of consent** | Stop processing, retain only legally required data, document |

**Day 30-45: Deliver response**
10. Send response to verified requestor
11. Log completion in DSR Tracking Log
12. Retain response record for 3 years

**GDPR Timeline:** 30 days (extendable to 90 days for complex requests with notification)
**CCPA Timeline:** 45 days (extendable to 90 days with notification)

**Exceptions - When requests may be declined:**
- Cannot verify requestor identity
- Request is manifestly unfounded or excessive
- Data required for legal claims or compliance
- Deletion would impair research integrity for other participants (anonymize instead)

Always document reason for any declined request and inform requestor of appeal rights.

---

### 4.9 Data Breach Response

**Step 16: Follow breach response protocol if incident occurs**

**What Constitutes a Breach:**
- Unauthorized access to participant data (hacking, stolen credentials)
- Accidental disclosure (email to wrong recipient, unprotected file sharing)
- Lost or stolen devices containing research data
- Ransomware or malware affecting data systems
- Vendor breach affecting our participant data
- Physical theft of documents containing PII

**Immediate Response (0-24 hours):**

1. **CONTAIN** - Stop ongoing breach
   - [ ] Revoke compromised credentials
   - [ ] Disconnect affected systems
   - [ ] Preserve evidence (do not delete logs)
   - [ ] Isolate affected data

2. **ASSESS** - Determine scope
   - [ ] What data was affected?
   - [ ] How many participants impacted?
   - [ ] What is the risk of harm?
   - [ ] Is data still accessible to unauthorized parties?

3. **ESCALATE** - Notify required parties
   - [ ] Research Lead immediately
   - [ ] Legal/Compliance team immediately
   - [ ] IT Security team immediately
   - [ ] Senior leadership per company policy

**24-72 Hour Response:**

4. **INVESTIGATE** - Document incident details
   - [ ] Complete Breach Incident Report
   - [ ] Timeline of events
   - [ ] Root cause analysis
   - [ ] Data types and volume affected
   - [ ] Participants affected (by region/jurisdiction)

5. **DETERMINE NOTIFICATION REQUIREMENTS**

| Jurisdiction | Authority Notification | Individual Notification |
|--------------|----------------------|------------------------|
| GDPR (EU) | 72 hours if risk to rights | Without undue delay if high risk |
| CCPA (California) | Per state requirements | If unencrypted PII affected |
| Other | Per applicable law | Based on risk assessment |

**Notification required if:**
- Unencrypted PII was accessed
- Risk of identity theft, fraud, or discrimination
- Sensitive personal data involved
- Large number of individuals affected

6. **NOTIFY** - If required
   - [ ] Draft notification with Legal approval
   - [ ] Notify supervisory authority (GDPR: 72 hours)
   - [ ] Notify affected individuals (clear, plain language)
   - [ ] Include: what happened, data affected, actions taken, protective steps for individuals, contact information

**Post-Incident (1-4 weeks):**

7. **REMEDIATE**
   - [ ] Implement fixes to prevent recurrence
   - [ ] Update security controls
   - [ ] Retrain team if human error involved
   - [ ] Update procedures if process gap identified

8. **DOCUMENT**
   - [ ] Complete final Breach Report
   - [ ] Document all notifications sent
   - [ ] Record remediation actions
   - [ ] Retain records for 5 years minimum

---

### 4.10 B2B and Industrial Research Considerations

**Step 17: Apply additional safeguards for B2B research**

**Proprietary Information Handling:**

| Information Type | Safeguards |
|------------------|------------|
| Trade secrets | Classify as Level 4, encrypt, limit access to primary researcher only |
| Unreleased products | No photos without explicit consent, redact from notes within 24 hours |
| Financial data | Never record specific figures, use ranges or relative terms |
| Competitive intelligence | Anonymize immediately, never attribute to source company |
| Manufacturing processes | No detailed documentation unless essential, delete after analysis |
| Internal communications | Do not request, stop participant if they share |

**NDA Requirements:**
- Establish company-level NDA before recruiting from organization
- Review NDA terms for data handling requirements
- Apply stricter retention if NDA specifies
- Include NDA reference in study documentation
- Ensure all team members with access have signed NDA

**Multi-Stakeholder Data Separation:**
- Maintain separate files for different participant companies
- Never share Company A's data with Company B
- Aggregate competitive insights only in anonymized reports
- Brief stakeholders without revealing specific sources

**Industrial Environment Considerations:**
- Do not photograph safety-sensitive areas without approval
- Remove/blur proprietary equipment in images
- Obtain facility photo release separate from individual consent
- Coordinate with participant's legal/compliance team for sensitive sites

**Step 18: Manage third-party vendor and tool compliance**

**Vendor Assessment Requirements:**

Before using any tool that processes participant data:

1. **Security certification check:**
   - [ ] SOC 2 Type II certification
   - [ ] ISO 27001 certification (preferred for EU)
   - [ ] GDPR compliance attestation (for EU data)

2. **Data Processing Agreement (DPA):**
   - [ ] Signed DPA in place
   - [ ] DPA includes Standard Contractual Clauses (for international transfers)
   - [ ] DPA specifies data handling, retention, deletion obligations
   - [ ] DPA includes breach notification requirements

3. **Tool configuration:**
   - [ ] Encryption enabled
   - [ ] MFA required
   - [ ] Data residency appropriate to participants
   - [ ] Auto-deletion configured per retention schedule
   - [ ] Access limited to authorized team members

**Approved Tool Categories and Requirements:**

| Tool Category | Security Requirements | Examples of Compliant Options |
|---------------|----------------------|------------------------------|
| Video conferencing | End-to-end encryption available, waiting rooms, recording controls | Zoom (Enterprise), Microsoft Teams, Google Meet |
| Transcription | BAA available, delete-after-processing option, no human review without consent | Otter.ai (Business), Rev (Enterprise), Descript |
| Survey | GDPR mode, IP anonymization option, data export/deletion | Qualtrics, Typeform (Business), Alchemer |
| Repository | Encryption, granular permissions, audit logs | Dovetail, Condens, Notion (Enterprise) |
| File storage | Encryption, sharing controls, retention policies | Google Workspace, Microsoft 365, Dropbox Business |
| Scheduling | Minimal data collection, calendar integration security | Calendly (Teams), Cal.com, Microsoft Bookings |

---

## 5. Templates and Tools

### Template 5.1: Research Data Inventory

```
RESEARCH DATA INVENTORY

Project Code: [PRJ2026-XXX]
Project Name: [Name]
Research Lead: [Name]
Last Updated: [Date]

DATA COLLECTED:

| Data Type | Classification | Storage Location | Access Level | Collection Date | Retention Period | Deletion Date | Status |
|-----------|---------------|------------------|--------------|-----------------|------------------|---------------|--------|
| Consent forms | Level 3 | /Research/2026/PRJ-XXX/02_Consent | Research Lead + PM | 2026-01-15 | 3 years post-data deletion | 2032-01-15 | Active |
| Video recordings | Level 3 | /Research/2026/PRJ-XXX/03_Raw | Research team | 2026-01-15 | 12 months | 2027-01-15 | Active |
| Transcripts | Level 3 | /Research/2026/PRJ-XXX/04_Analysis | Research team | 2026-01-20 | 18 months | 2027-07-20 | Active |
| Survey responses | Level 2 | Qualtrics Project #123 | Research team | 2026-01-10 | 18 months | 2027-07-10 | Active |
| Participant Code Key | Level 3 | /Research/2026/PRJ-XXX/06_Participant Log | Research Lead only | 2026-01-10 | Same as recordings | 2027-01-15 | Active |
| Final report | Level 1 | /Research/2026/PRJ-XXX/05_Outputs | All approved viewers | 2026-02-15 | Indefinite | N/A | Active |

THIRD-PARTY PROCESSORS:
| Vendor | Data Shared | DPA Status | Data Location |
|--------|-------------|------------|---------------|
| Zoom | Recordings | Signed 2025-03-01 | US |
| Otter.ai | Audio for transcription | Signed 2025-03-01 | US |

NOTES:
[Any special handling requirements, NDA references, etc.]
```

---

### Template 5.2: Data Retention Schedule

```
DATA RETENTION SCHEDULE
Version: 1.0
Effective: [Date]
Owner: Research Lead

STANDARD RETENTION PERIODS:

| Data Category | Data Type | Retention Start | Retention Period | Deletion Method | Legal Basis |
|---------------|-----------|-----------------|------------------|-----------------|-------------|
| CONTACT DATA |
| | Participant names | Collection | Project + 30 days | Secure delete | Consent |
| | Email addresses | Collection | Project + 30 days | Secure delete | Consent |
| | Phone numbers | Collection | Project + 30 days | Secure delete | Consent |
| | Employer/title | Collection | Project + 30 days | Anonymize or delete | Consent |
| CONSENT RECORDS |
| | Signed consent forms | Collection | All data retention + 3 years | Secure delete | Legal obligation |
| | Consent withdrawal records | Receipt | 7 years | Secure delete | Legal obligation |
| RAW RESEARCH DATA |
| | Video recordings | Collection | 12 months | Secure delete | Consent |
| | Audio recordings | Collection | 12 months | Secure delete | Consent |
| | Screen recordings | Collection | 12 months | Secure delete | Consent |
| | Photos (identified) | Collection | 12 months | Secure delete | Consent |
| PROCESSED DATA |
| | Transcripts (identified) | Creation | 18 months | Secure delete | Consent |
| | Transcripts (pseudonymized) | Creation | 3 years | Secure delete | Legitimate interest |
| | Survey responses (identified) | Collection | 18 months | Secure delete | Consent |
| | Survey responses (anonymized) | Anonymization | 7 years | Business review | Legitimate interest |
| | Coded analysis files | Creation | 3 years | Secure delete | Legitimate interest |
| OUTPUTS |
| | Anonymized reports | Publication | Indefinite | N/A | Legitimate interest |
| | Highlight reels (faces blurred) | Creation | 3 years | Secure delete | Consent |
| B2B SPECIFIC |
| | NDA-covered materials | Collection | Per NDA terms | Secure delete | Contract |
| | Proprietary process notes | Collection | 6 months | Secure delete | Consent |
| ADMINISTRATIVE |
| | Data inventory records | Creation | 7 years | Archive | Legal obligation |
| | DSR response records | Response date | 3 years | Archive | Legal obligation |
| | Breach records | Incident date | 5 years | Archive | Legal obligation |

QUARTERLY REVIEW DATES: March 31, June 30, September 30, December 31

DELETION METHODS:
- Secure delete: Permanent deletion from all storage locations including backups
- Anonymize: Remove/generalize all identifying information, retain anonymized version
- Archive: Move to secure archive with restricted access
- Business review: Assess continued business need, delete if no longer required
```

---

### Template 5.3: Data Subject Request Log

```
DATA SUBJECT REQUEST TRACKING LOG

| Request ID | Date Received | Requestor Name | Request Type | Verification Status | Jurisdiction | Response Due | Assigned To | Status | Completion Date | Notes |
|------------|---------------|----------------|--------------|---------------------|--------------|--------------|-------------|--------|-----------------|-------|
| DSR-2026-001 | 2026-01-10 | [Name] | Deletion | Verified 2026-01-11 | GDPR | 2026-02-09 | [Name] | Complete | 2026-01-25 | All data deleted per request |
| DSR-2026-002 | 2026-01-15 | [Name] | Access | Pending verification | CCPA | 2026-03-01 | [Name] | In Progress | - | Awaiting identity confirmation |

REQUEST TYPES:
- Access: Provide copy of all personal data held
- Deletion: Delete all personal data
- Correction: Correct inaccurate personal data
- Portability: Provide data in portable format
- Withdrawal: Stop processing based on consent
- Restriction: Limit processing

STATUS OPTIONS:
- Received: Request logged, not yet started
- Verification: Confirming requestor identity
- In Progress: Compiling data or executing request
- Pending Legal: Requires legal review
- Complete: Response sent to requestor
- Declined: Request declined (document reason)
```

---

### Template 5.4: Breach Incident Report

```
BREACH INCIDENT REPORT

INCIDENT IDENTIFICATION
Report Number: BIR-[YEAR]-[XXX]
Date Discovered: [Date/Time]
Date Reported: [Date/Time]
Reported By: [Name/Role]
Report Completed By: [Name/Role]
Report Date: [Date]

INCIDENT SUMMARY
Brief Description:
[Narrative description of what happened]

INCIDENT CLASSIFICATION
[ ] Unauthorized access
[ ] Unauthorized disclosure
[ ] Data loss
[ ] Data theft
[ ] System compromise
[ ] Vendor breach
[ ] Physical security breach
[ ] Other: _______________

SCOPE ASSESSMENT

Data Types Affected:
[ ] Names
[ ] Contact information (email, phone)
[ ] Recordings (audio/video)
[ ] Survey responses
[ ] Transcripts
[ ] Photos/images
[ ] Consent forms
[ ] Financial information
[ ] Sensitive personal data (specify): _______________
[ ] Confidential business information
[ ] Other: _______________

Volume:
- Number of records affected: [Number]
- Number of individuals affected: [Number]
- Number of organizations affected (B2B): [Number]

Geographic Scope:
[ ] EU residents affected (GDPR applies)
[ ] California residents affected (CCPA applies)
[ ] Other jurisdictions: _______________

TIMELINE OF EVENTS
| Date/Time | Event |
|-----------|-------|
| | Breach occurred (estimated) |
| | Breach discovered |
| | Initial containment actions |
| | Escalation to leadership |
| | Investigation initiated |
| | Containment confirmed |
| | [Add rows as needed] |

RISK ASSESSMENT
Likelihood of harm to individuals:
[ ] Low - Data encrypted, quickly contained, limited sensitivity
[ ] Medium - Some identifying data exposed, containment uncertain
[ ] High - Sensitive data exposed, prolonged access, identity theft risk

Type of potential harm:
[ ] Identity theft
[ ] Financial loss
[ ] Reputational harm
[ ] Discrimination
[ ] Physical safety
[ ] Emotional distress
[ ] Competitive harm (B2B)
[ ] Other: _______________

CONTAINMENT ACTIONS TAKEN
[ ] Compromised credentials revoked
[ ] Affected systems isolated
[ ] Security patches applied
[ ] Access logs preserved
[ ] Vendor notified
[ ] Other: _______________

NOTIFICATION DETERMINATION

Supervisory Authority Notification Required:
[ ] Yes - High risk to individuals
[ ] No - Low risk, unlikely to result in harm
Justification: _______________

Individual Notification Required:
[ ] Yes - High risk to individuals
[ ] No - Risk mitigated, encrypted data, low likelihood of harm
Justification: _______________

Notifications Sent:
| Recipient | Date Sent | Method | Content Summary |
|-----------|-----------|--------|-----------------|
| | | | |

ROOT CAUSE ANALYSIS
Primary Cause:
[ ] Human error
[ ] Technical vulnerability
[ ] Process failure
[ ] Vendor failure
[ ] Malicious attack
[ ] Other: _______________

Contributing Factors:
[Describe underlying factors that enabled the incident]

REMEDIATION ACTIONS
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| | | | |

LESSONS LEARNED
[What will we do differently to prevent recurrence?]

APPROVALS
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Research Lead | | | |
| Legal/Compliance | | | |
| IT Security | | | |
```

---

### Template 5.5: Third-Party Vendor Assessment Checklist

```
THIRD-PARTY VENDOR DATA PROCESSING ASSESSMENT

VENDOR INFORMATION
Vendor Name: _______________
Service/Tool: _______________
Assessment Date: _______________
Assessed By: _______________
Next Review Date: _______________

PURPOSE OF PROCESSING
Data types to be processed:
[ ] Participant contact information
[ ] Recordings (audio/video)
[ ] Survey responses
[ ] Transcripts
[ ] Session recordings
[ ] Behavioral data
[ ] Other: _______________

Processing purpose: _______________

SECURITY CERTIFICATIONS
[ ] SOC 2 Type II (date: _______)
[ ] ISO 27001 (date: _______)
[ ] GDPR compliance attestation
[ ] HIPAA compliance (if applicable)
[ ] Other: _______________

Certification documentation on file: [ ] Yes [ ] No

DATA PROTECTION AGREEMENT
[ ] Data Processing Agreement (DPA) signed
[ ] Standard Contractual Clauses included (for international transfers)
[ ] Business Associate Agreement (if health data)

DPA signed date: _______________
DPA expiration: _______________

TECHNICAL SECURITY CONTROLS
[ ] Encryption at rest (specify standard: _______)
[ ] Encryption in transit (TLS version: _______)
[ ] Multi-factor authentication available
[ ] Role-based access controls
[ ] Audit logging enabled
[ ] Data export capability
[ ] Data deletion capability
[ ] Backup and recovery procedures

DATA LOCATION AND TRANSFERS
Primary data storage location: _______________
Backup locations: _______________
Sub-processors used: _______________

Data transfers outside EEA: [ ] Yes [ ] No
If yes, transfer mechanism: _______________

RETENTION AND DELETION
Vendor retention period: _______________
Deletion on request: [ ] Yes [ ] No
Deletion method: _______________
Deletion verification provided: [ ] Yes [ ] No

BREACH NOTIFICATION
Breach notification timeframe: _______________
Notification method: _______________
Contact for breach reports: _______________

ASSESSMENT RESULT
[ ] Approved for use
[ ] Approved with conditions: _______________
[ ] Not approved - Reason: _______________

APPROVAL
Approved by: _______________
Date: _______________
```

---

### Template 5.6: Data Classification Assessment

```
DATA CLASSIFICATION ASSESSMENT

Project Code: _______________
Project Name: _______________
Assessment Date: _______________
Assessed By: _______________

For each data type collected, assess classification level:

Level 1 - Public: Non-sensitive, aggregated, anonymized
Level 2 - Internal: Business information, pseudonymized data
Level 3 - Confidential PII: Identifiable personal data
Level 4 - Restricted: Sensitive personal data OR highly confidential business info

| Data Type | Specific Data Elements | Contains PII? | Sensitive Category? | B2B Confidential? | Classification Level | Justification |
|-----------|----------------------|---------------|--------------------|--------------------|---------------------|---------------|
| Survey responses | [List fields] | [ ] Yes [ ] No | [ ] Yes [ ] No | [ ] Yes [ ] No | Level ___ | |
| Interview recordings | | [ ] Yes [ ] No | [ ] Yes [ ] No | [ ] Yes [ ] No | Level ___ | |
| Transcripts | | [ ] Yes [ ] No | [ ] Yes [ ] No | [ ] Yes [ ] No | Level ___ | |
| Observational notes | | [ ] Yes [ ] No | [ ] Yes [ ] No | [ ] Yes [ ] No | Level ___ | |
| Photos/screenshots | | [ ] Yes [ ] No | [ ] Yes [ ] No | [ ] Yes [ ] No | Level ___ | |
| [Add rows as needed] | | | | | | |

SENSITIVE DATA CATEGORIES (check if applicable):
[ ] Health or medical information
[ ] Racial or ethnic origin
[ ] Political opinions
[ ] Religious or philosophical beliefs
[ ] Trade union membership
[ ] Genetic or biometric data
[ ] Sexual orientation
[ ] Financial account details
[ ] Government IDs

If any sensitive categories checked, Level 4 classification applies. Obtain explicit consent.

B2B CONFIDENTIALITY ASSESSMENT:
[ ] Trade secrets may be discussed
[ ] Unreleased products/features may be shown
[ ] Internal financial information may be shared
[ ] Competitive information may be revealed
[ ] NDA required: [ ] Yes [ ] No (NDA reference: _______________)

If any B2B boxes checked, consider Level 4 classification for relevant data.

HIGHEST CLASSIFICATION LEVEL FOR PROJECT: Level ___

HANDLING REQUIREMENTS:
[Based on highest classification, document required storage, access controls, and retention]

Approved By: _______________
Date: _______________
```

---

## 6. Responsibilities

### RACI Matrix

| Activity | Research Lead | Researcher | Research Ops | Legal/Compliance | IT Security |
|----------|---------------|------------|--------------|------------------|-------------|
| Data classification | A | R | C | C | I |
| Consent collection | A | R | S | C | - |
| Data storage management | A | R | R | I | C |
| Access control management | R/A | I | R | I | C |
| Retention monitoring | A | R | R | C | I |
| Deletion execution | A | R | R | I | I |
| DSR response | A | R | S | C | I |
| Breach response | R | R | S | A | R |
| Vendor assessment | A | I | R | C | R |
| Policy updates | A | C | C | R | C |
| Training delivery | A | - | R | C | C |
| Compliance audits | A | R | R | R | R |

**R** = Responsible (does the work)
**A** = Accountable (ultimate ownership)
**C** = Consulted (provides input)
**I** = Informed (kept updated)
**S** = Supports (assists as needed)

### Role Definitions

**Research Lead:**
- Ultimate accountability for research data compliance
- Approves data classification decisions for new studies
- Manages access permissions and approves access requests
- Leads breach response coordination
- Reviews and approves DSR responses
- Ensures team training completion
- Conducts quarterly compliance reviews

**Researcher:**
- Classifies data at project initiation (with Lead approval)
- Collects valid consent for all participants
- Implements proper data handling throughout study
- Pseudonymizes and anonymizes data per procedures
- Executes data deletion at retention expiry
- Reports potential breaches immediately
- Completes annual data protection training

**Research Operations (if applicable):**
- Maintains data inventory and retention schedules
- Monitors retention deadlines and deletion compliance
- Manages vendor relationships and DPA renewals
- Supports DSR response data compilation
- Maintains templates and documentation
- Coordinates training logistics

**Legal/Compliance:**
- Advises on regulatory requirements and updates
- Reviews consent forms and privacy notices
- Approves breach notification content
- Provides guidance on DSR response
- Conducts or supports compliance audits

**IT Security:**
- Maintains secure storage infrastructure
- Supports breach investigation and containment
- Advises on tool security requirements
- Conducts security reviews of new tools
- Manages access control systems

---

## 7. Quality Checks

### 7.1 Pre-Study Compliance Check

Before launching any study, verify:

| Check | Requirement | Verified |
|-------|-------------|----------|
| Data classification | Assessment completed for all data types | [ ] |
| Consent form | Reviewed, includes all required elements | [ ] |
| Legal basis | Documented in study protocol | [ ] |
| Storage location | Approved location identified, access configured | [ ] |
| Retention period | Defined and documented in Data Inventory | [ ] |
| Tool compliance | All tools have current DPA, security certified | [ ] |
| B2B requirements | NDA in place if proprietary info expected | [ ] |
| Training | All team members current on data protection | [ ] |

### 7.2 Monthly Data Hygiene Review

| Review Item | Actions | Status |
|-------------|---------|--------|
| Data Inventory accuracy | Verify all active projects documented | [ ] |
| Retention compliance | Check for data past retention date | [ ] |
| Access appropriateness | Review who has access to active projects | [ ] |
| Deletion backlog | Execute any pending deletions | [ ] |
| Tool audit | Verify tool access lists are current | [ ] |

### 7.3 Quarterly Compliance Audit

| Audit Area | Assessment Criteria | Finding | Action Required |
|------------|---------------------|---------|-----------------|
| Consent documentation | All studies have complete consent records | | |
| Data inventory completeness | All data sources documented | | |
| Retention compliance | No data held beyond retention period | | |
| Access control review | Access limited to authorized personnel | | |
| Vendor DPA status | All DPAs current and complete | | |
| Training completion | All team members trained within 12 months | | |
| DSR response timeliness | All requests responded within deadline | | |
| Incident documentation | Any incidents properly documented | | |

### 7.4 Annual Privacy Impact Assessment

For ongoing research programs or new high-risk studies:

| Assessment Element | Considerations | Assessment |
|--------------------|----------------|------------|
| Data flows | Map all data collection, storage, sharing, deletion | |
| Risk identification | What could go wrong? What are the impacts? | |
| Risk mitigation | What controls reduce identified risks? | |
| Proportionality | Is data collection proportionate to objectives? | |
| Individual rights | How are participant rights supported? | |
| Compliance gaps | What gaps exist in current practices? | |
| Remediation plan | What improvements are needed? | |

### 7.5 Compliance Metrics Dashboard

Track monthly:

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Studies with complete Data Inventory | 100% | | |
| Data deleted within 30 days of retention expiry | 100% | | |
| DSRs responded within deadline | 100% | | |
| Team members with current training | 100% | | |
| Vendors with current DPA | 100% | | |
| Security incidents reported | 0 | | |
| Consent documentation completeness | 100% | | |

---

## 8. Related Documents

| Document ID | Document Title | Relationship |
|-------------|----------------|--------------|
| UXR-001 | Informed Consent & Ethics SOP | Consent collection procedures |
| UXR-003 | Participant Recruitment & Screening SOP | Participant data collection |
| [LEGAL-XXX] | Privacy Policy | Public-facing privacy commitments |
| [LEGAL-XXX] | Data Processing Agreement Template | Vendor agreements |
| [SEC-XXX] | Information Security Policy | Organizational security requirements |
| [SEC-XXX] | Incident Response Plan | Company-wide breach response |
| [HR-XXX] | Data Protection Training Requirements | Training compliance |

### External References

| Reference | Description | URL |
|-----------|-------------|-----|
| GDPR Full Text | General Data Protection Regulation | gdpr-info.eu |
| CCPA Full Text | California Consumer Privacy Act | oag.ca.gov/privacy/ccpa |
| ICO Guidance | UK Information Commissioner's Office research guidance | ico.org.uk |
| EDPB Guidelines | European Data Protection Board guidance | edpb.europa.eu |
| IAPP Resources | International Association of Privacy Professionals | iapp.org |

---

## 9. Revision History

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 2026-01-15 | [Name] | Initial release | [Name] |
| | | | | |
| | | | | |

### Review Schedule

| Review Type | Frequency | Next Review | Owner |
|-------------|-----------|-------------|-------|
| Content accuracy | Annual | 2027-01-15 | Research Lead |
| Regulatory updates | Quarterly | 2026-04-15 | Legal/Compliance |
| Template updates | Semi-annual | 2026-07-15 | Research Ops |
| Procedure audit | Annual | 2027-01-15 | Research Lead |

### Change Request Process

1. Submit change request to Research Lead with:
   - Section requiring change
   - Proposed revision
   - Rationale for change
   - Impact assessment
2. Research Lead reviews with Legal/Compliance if regulatory impact
3. Approved changes incorporated within 30 days
4. Team notified of updates via email and team meeting
5. Training updated if procedures change significantly

---

## Appendix A: Quick Reference Card

### Data Classification Quick Guide

| If data includes... | Classify as... | Key requirements |
|---------------------|----------------|------------------|
| Only anonymized/aggregated info | Level 1 | Standard handling |
| Coded data, no direct identifiers | Level 2 | Access controls, secure storage |
| Names, emails, faces, voices | Level 3 | Encryption, limited access, retention limits |
| Health, finances, trade secrets | Level 4 | Maximum security, explicit consent, audit logging |

### Retention Quick Reference

| Data Type | Keep for | Then |
|-----------|----------|------|
| Contact info | Project + 30 days | Delete |
| Recordings | 12 months | Delete |
| Identified transcripts | 18 months | Delete |
| Anonymized reports | Indefinitely | Retain |

### DSR Response Quick Guide

| Request type | Deadline (GDPR) | Deadline (CCPA) |
|--------------|-----------------|-----------------|
| Any request | 30 days | 45 days |
| Complex request | 90 days (with notice) | 90 days (with notice) |

### Breach Response Quick Actions

1. STOP - Contain the breach
2. ESCALATE - Notify Research Lead, Legal, IT Security
3. ASSESS - Scope, risk, jurisdictions
4. DOCUMENT - Complete Breach Report
5. NOTIFY - Authority (72hrs GDPR), individuals (if high risk)

---

## Appendix B: Annual Training Requirements

All research team members must complete:

| Training | Frequency | Duration | Delivery |
|----------|-----------|----------|----------|
| Data protection fundamentals | Annual | 2 hours | Online + quiz |
| GDPR/CCPA requirements | Annual | 1 hour | Online + quiz |
| Breach response procedures | Annual | 30 minutes | Team meeting |
| Tool-specific security | At onboarding + updates | 30 minutes each | Self-guided |
| B2B confidentiality handling | Annual | 1 hour | Team meeting |

Training completion tracked in HR system. Non-compliance results in suspended data access until training completed.

---

**Document Control:**
- This document is controlled. Printed copies are for reference only.
- Current version available at: [Insert location]
- Questions: Contact Research Lead

**Emergency Contact:**
- Data breach suspected: Immediately contact Research Lead + IT Security
- After hours: [Emergency contact procedure]
