---
name: risk-retrospective
description: "Create concise, evidence-based security risk retrospectives and decision documents that frame risks, present options, and drive stakeholder decisions. Use when Codex is asked for a risk retrospective, risk assessment, security decision doc, post-mortem, debrief, event analysis, accepted-risk writeup, security trade-off memo, incident writeup, or leadership-facing risk document."
---

# Risk Retrospective Skill

Generate concise, evidence-based security risk documents that serve developers, security engineers, and executives. The target audience assumes no prior knowledge but allows drill-down. Target ~800-1000 words (~2 pages).

## Codex Notes
Use local files, pasted content, browser/web sources, and available connectors as evidence. Do not assume Gemini MCP tools exist. If a Google Docs, Slack, ticket, Jira, Linear, or internal-doc connector is unavailable, ask the user for exported text, screenshots, or permalinks. Preserve raw source URLs in citations.

## Workflow

Follow these 6 phases in order. Skip phases that aren't needed based on available context.

### Phase 1: Tracking & Work Item Pull
Look for case/ticket identifiers in the user's input:
* Work items (bugs or user stories): W-XXXXXXXX format or full URLs (example.thisisthebug.com)
* Other ticket systems (JIRA, etc.)

If W-numbers or work item URLs are found:
1. Call `the relevant ticket/work-item connector if available` for each W-number
2. Extract: title, severity, description, dates, assignee, status
3. Note any linked items or parent epics - call `the relevant ticket/work-item connector if available` for parent epics to understand the broader initiative
4. Store extracted data you'll weave it into the document

Populate the Tracking field in the header table with whatever case/ticket IDs you find. If no tracking IDs are provided, skip to Phase 2.

### Phase 2: Assess Completeness
Score the user's input against these 6 dimensions:
1. **Risk description** - What is the specific risk or vulnerability?
2. **Business context** - Why does this feature/system/decision matter to the business?
3. **Severity signals** - Any data on likelihood, impact, or prior incidents?
4. **Options considered** - Has the user thought about alternatives?
5. **Stakeholders** - Who needs to decide, and who is affected?
6. **Timeline** - Key dates (discovery, deadlines, milestones)?

If 4+ dimensions are present, skip to Phase 5 (Draft). Otherwise, proceed to Phase 3.

### Phase 3: Interview
Ask all missing questions in a single batch message. Acknowledge what you already know before asking. Do not ask questions one at a time that wastes the user's time. Frame questions clearly so a non-technical stakeholder could answer them.

**Example batch:**
* "I have a good understanding of the risk and business context from the work item ticket. To complete the document, I need a few more pieces:"
* "What options has the team discussed so far? (e.g., mitigate now, defer, accept)"
* "Who are the key decision-makers? (e.g., VP Engineering, CISO)"
* "Are there any hard deadlines driving this decision?"

### Phase 4: Research & Document Spidering
Spider aggressively into linked documents and resources to build a complete picture. This is the most critical research phase - incomplete context produces weak risk documents.

**Google Docs Deep Spidering (CRITICAL)**
When the user provides links to Google Docs or you discover them in other sources:
1. Use `available document connector` to pull the full content of every linked Google Doc
2. Use `available document connector comments tool` to read comment threads these often contain key decisions, objections, and stakeholder positions
3. IMPORTANT: Scan the content of every retrieved Google Doc for links to OTHER Google Docs, and pull those too. Documents frequently link to design docs, PRDs, prior retrospectives, meeting notes, and decision logs. These linked-within-linked documents are essential context that gets missed if you only fetch the top-level doc. Continue spidering until you've exhausted linked Google Docs (up to a reasonable depth of ~3 levels).
4. Use `available document search connector` to find related docs when you have enough context to form good search queries (e.g., project names, feature names, team names discovered in the docs)

**Slack Context Gathering**
Actively search Slack for relevant context using `available search connector` with sources: ["slack"]:
1. When the user provides Slack channel names or links - search those channels for relevant discussions
2. When you discover #channel-name references in Google Docs or other sources these are signals that relevant conversations happened there. Search Slack for those channel discussions.
3. Search by topic use project names, feature names, risk keywords, and people's names discovered during research to find relevant Slack threads
4. Slack threads often contain informal decisions, escalation context, and stakeholder opinions that never make it into formal docs this is high-value context for risk retrospectives

**General Research**
1. Use `available search connector` (with broader sources) to find related internal docs, prior retrospectives, or security advisories
2. Look for OWASP, NIST, or CWE references relevant to the risk category

Stay on scope. Spider for evidence and context that directly supports the risk document. Don't add content just because you found it every piece of spidered information should serve a specific section of the retrospective. Avoid unnecessary fluff from tangential documents.

### Phase 5: Draft
Generate the document using the template at references/template.md (read it before drafting).
Apply these writing rules:
* Factual and evidence-based throughout. Every claim needs a source or observable basis.
* Opinions belong ONLY in one place: the "Security Directive" section. Everywhere else, state facts.
* No hedging. Don't write "it could potentially maybe cause issues." State what is known, what is unknown, and cite your sources.
* Accessible to non-technical readers. Define jargon on first use. A VP who hasn't read the code should understand the risk after reading the Executive Summary.
* Use tables for structured data (risk ratings, option comparisons). Use numbered lists for sequential events (timeline).
* Target ~800-1000 words. This is a 2-page document, not a thesis. Be concise.
* Code snippets only when essential to understanding the risk - under 5 lines, with context.

### Phase 5.5: Humanizer Pass
Risk retrospectives are leadership-facing documents. Before presenting the draft to the user, invoke the humanizer skill on the draft to strip AI tells (inflated symbolism, rule-of-three padding, em-dash overuse, vague attributions, etc.).

Constraints on the humanizer pass:
* Preserve all evidence. Every cited fact, work item W-number, date, severity rating, and source link stays exactly as drafted.
* Humanizer changes voice and phrasing only. Preserve structure. Section headings, the risk-rating table, the options table, the timeline numbered list, and the empty Decision Log section all stay intact.
* Preserve the Security Directive. That section is the one place opinions live; the recommended option and its rationale must remain identifiable after the pass.
* Reject scope creep. Humanizer must not introduce new claims, options, stakeholders, or speculation. If a humanizer edit would add unsourced content, drop that edit.
* If the humanizer skill is unavailable, note this when presenting the draft and proceed to Phase 6 without the pass.

### Phase 6: Review
Present the draft to the user. Ask specifically:
* "Does the option framing accurately represent the trade-offs your team discussed?"
* "Do the severity ratings feel right based on what you've seen?"
* "Is there anyone missing from the stakeholders or decision log?"

### Phase 7: Offer Google Doc
After the user approves the Markdown draft, offer to create an external document only if a compatible connector is available in the current Codex session. If no connector is available, save or present Markdown as the primary deliverable.

## Risk Rating Methodology
Use an OWASP + NIST hybrid approach with 4 dimensions:

| Dimension | Question | Scale |
| :--- | :--- | :--- |
| Likelihood | How probable is exploitation or occurrence? | Low / Medium / High / Critical |
| Technical Impact | What's the worst technical outcome? (data loss, system compromise, etc.) | Low / Medium / High / Critical |
| Business Impact | What's the business consequence? (revenue, reputation, compliance, customers) | Low / Medium / High / Critical |
| Overall Severity | Derived from the above three | Low / Medium / High / Critical |

Each rating gets a 1-sentence rationale. No bare ratings without explanation.

**Deriving Overall Severity:**
* If any dimension is Critical → Overall is Critical (unless strong mitigating controls exist, then High)
* If 2+ dimensions are High → Overall is High
* If Business Impact is High but Technical Impact is Low → Overall is Medium (the business cares but the attack surface is limited)
* Otherwise take the most common rating among the three
* Always explain your reasoning when the derivation isn't obvious

## Anti-Patterns to Reject
When drafting or reviewing, actively check for and fix these problems:
* **FUD (Fear, Uncertainty, Doubt):** Inflating risk to push a preferred outcome. The document should inform decisions, not manipulate them.
* **Buried recommendation:** The recommended option must be in the clearly labeled "Security Directive" section, not hidden in paragraph 7.
* **Missing "accept the risk" option:** Every risk document must include this option. Stakeholders always have the right to knowingly accept a risk.
* **Undated timeline entries:** Every timeline item needs a date (exact or approximate). "Earlier this year" is not a date.
* **Verbose timeline:** Only include critical milestones - risk discovery, case/ticket changes, escalations, incidents, key decisions. Minor document edits and comment updates do not warrant timeline entries.
* **Pre-filled decision log:** The Decision Log should be empty in the initial draft. It gets filled in after stakeholders read the document and make decisions.
* **Wall of text:** If any section has more than 5 consecutive lines of prose, convert it to a table, bullet list, or numbered list.

## Quality Checklist
Verify all of these before presenting the document to the user:
- [ ] Executive Summary is 3-5 sentences
- [ ] Risk Assessment table has all 4 dimensions with rationale
- [ ] At least 3 options presented (including "Accept the risk")
- [ ] Timeline entries all have dates
- [ ] Decision Log section is present but empty (to be filled after stakeholder review)
- [ ] No opinions appear outside the Security Directive section
- [ ] Work item W-numbers cited in References (if applicable)
- [ ] Document is under ~1000 words
