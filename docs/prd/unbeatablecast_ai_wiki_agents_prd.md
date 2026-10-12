# Product Requirements Document: UnbeatableCast AI Wiki Intelligence System

**Status:** Draft for planning and review
**Version:** 0.1
**Date:** October 12, 2026
**Product type:** Internal, human-supervised AI research and wiki-maintenance workflow
**Primary property:** [UnbeatableCast Wiki](https://unbeatablecast.fandom.com/wiki/UnbeatableCast_Wiki)

## 1. Executive Summary

The UnbeatableCast AI Wiki Intelligence System will ingest authorized episode content from a Pokémon tabletop role-playing podcast, produce detailed, source-linked narrative records, track characters, Pokémon, locations, organizations, relationships, and story events across episodes, and recommend specific updates to the community wiki.

The system's initial role is **research and editorial assistance**, not autonomous publication. Each suggested wiki change must be grounded in identifiable episode evidence, compared with the current wiki, and approved by a human reviewer before being published.

The architecture will use a combination of deterministic software for discovery, retrieval, storage and scheduling; existing integrations such as RSS feeds, YouTube APIs and transcript-capable MCP services; and specialized AI workflows for interpretation, continuity, wiki comparison and validation. GitHub Copilot Agent Skills may document repeatable procedures and connect to MCP tools in VS Code. The system must not assume Spotify or YouTube provide unrestricted audio or transcript access.

## 2. Problem Statement

Tabletop RPG podcasts create large volumes of evolving narrative information over many episodes. Manual maintenance of a fandom wiki is time-consuming, particularly when updates require recalling when a character learned something, when a Pokémon joined or left a team, or how an event connects to a larger arc. Episode blurbs are insufficient to reconstruct canon. Transcripts introduce additional problems: uncertain speaker attribution, incorrect names, out-of-character discussion and speculative statements mistaken for established facts.

There is no reliable, centralized workflow to connect episodes with evidence-backed story records and actionable wiki changes.

## 3. Goals and Success Criteria

### 3.1 Goals

1. Discover and catalog published episodes without duplicate processing across Spotify, YouTube and podcast RSS listings.
2. Obtain available and permitted transcript or audio inputs with timestamps and provenance.
3. Produce detailed, chronological notes that preserve meaningful scenes, actions and outcomes.
4. Maintain a cross-episode knowledge base of entities, relationships, facts and changes over time.
5. Detect wiki content that is missing, outdated, incomplete or potentially inconsistent with episode evidence.
6. Deliver clear page-specific change proposals, with sources and human approval controls.
7. Support historical backfill and ongoing new-episode processing with observable job status and retry handling.

### 3.2 Proposed pilot acceptance targets

These are initial targets to validate during the pilot, not measured results.

| Metric                          | Proposed acceptance target | Measurement                                                                                        |
| ------------------------------- | -------------------------: | -------------------------------------------------------------------------------------------------- |
| Factual precision               |                       ≥95% | Human audit of sampled extracted claims against episode audio                                      |
| Major-event recall              |                       ≥90% | Comparison with human-created event checklist                                                      |
| Evidence traceability           |                       100% | Every proposed factual wiki addition has an episode/source reference and timestamp where available |
| Wiki recommendation usefulness  |                       ≥80% | Human reviewer rates proposals useful/actionable                                                   |
| Unsupported factual publication |                          0 | Editorial audit of approved/published changes                                                      |
| Duplicate processing            |     0 avoidable duplicates | Unique episode identity and ingest logs                                                            |

Record cost per episode, processing duration, transcript availability, speaker accuracy and rate of human corrections as additional pilot observations rather than hard launch gates.

## 4. Scope

### In scope — MVP

- Discover episodes and metadata through a verified RSS feed and/or official platform discovery interfaces.
- Associate corresponding Spotify and YouTube listings with one canonical episode record.
- Retrieve existing transcripts where access is available and permitted; flag unavailable content.
- Support ingestion of authorized audio for transcription if necessary.
- Segment transcripts into scenes and extract narrative events and changes.
- Track recurring characters, Pokémon, locations, organizations and arcs.
- Maintain source-level evidence, ambiguity classifications and historical state.
- Read relevant public wiki pages where permitted; compare them to verified findings.
- Produce Markdown episode notes and human-reviewable wiki change proposals.
- Run a three-episode pilot followed by an incremental historical backfill.

### Out of scope — MVP

- Publishing directly to Fandom without human approval.
- Bypassing paywalls, DRM, platform protections or service restrictions.
- Republishing complete copyrighted transcripts or audio.
- Training or fine-tuning models on the show's content without appropriate rights.
- Replacing community editors' editorial judgment or determining disputed canon unilaterally.
- A custom web dashboard, advanced graph database, or autonomous multi-server deployment unless the pilot reveals a need.
- Generation of fan fiction, invented dialogue or unsupported lore.

## 5. Users and Stakeholders

| Role                            | Needs                                                                                     |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| Wiki editor/reviewer            | Evidence-backed drafts, clear diffs, manageable approval process                          |
| Podcast researcher              | Detailed episode timeline, relationships, character histories, source lookup              |
| System operator                 | Processing status, error reports, duplicate prevention, configuration and cost visibility |
| Wiki administrators/community   | Appropriate attribution, respectful editing volume, editorial conventions and rollback    |
| Podcast creators/rights holders | Compliance with audio/transcript rights and accurate representation of their content      |

The pilot assumes one operator/reviewer; multi-editor permissions may be added later.

## 6. Product Principles

1. **Evidence before edits.** Each factual assertion traces to a supported source, ideally an exact timestamp.
2. **Never infer canon from speculation.** Character beliefs, player hypotheses and jokes must be labeled accurately.
3. **Preserve history.** Do not overwrite an earlier character or Pokémon state without recording when and why it changed.
4. **Human editorial control.** No automatic publishing in MVP.
5. **Reusable integrations first.** Prefer RSS, existing services and maintained MCP tools over custom scraping.
6. **Graceful degradation.** Missing transcripts yield an explicit blocked/pending status, not a fabricated summary.
7. **Idempotent processing.** Reprocessing the same episode should not create duplicate records or wiki proposals.
8. **Portable prompts and schemas.** Keep business logic independent of one LLM or IDE vendor wherever practical.

## 7. End-to-End Workflow

1. **Discover:** Poll or manually query verified RSS and supported platform endpoints for new episodes.
2. **Resolve identity:** Match listings into one canonical episode using stable IDs, normalized titles, dates and duration tolerances; flag uncertain matches.
3. **Acquire inputs:** Retrieve accessible captions/transcripts or authorized audio, retain provenance, and record rights/access status.
4. **Transcribe/normalize:** When needed, run speech recognition and diarization; normalize names using a maintained glossary without concealing uncertain corrections.
5. **Segment:** Split a timestamped transcript into overlapping analysis windows or scene boundaries; account for context between segments.
6. **Extract:** Capture scenes, factual claims, character actions, Pokémon changes, locations, battles and unresolved threads.
7. **Reconcile:** Resolve entities against the knowledge base, apply historical changes, and identify inconsistencies or uncertain claims.
8. **Compare:** Read relevant wiki pages, inspect sections/templates, and identify missing or outdated content.
9. **Verify:** Check proposed claims against evidence and downgrade or reject unsupported statements.
10. **Review:** Produce Markdown notes and page-specific change proposals for human approval.
11. **Publish (manual MVP):** Reviewer transfers approved copy into the wiki; record published revision or link if available.
12. **Monitor:** Persist processing status, retries, errors and outcomes.

## 8. Logical Agents and Responsibilities

The following are _logical responsibilities_. MVP may implement them as skills or steps in one orchestration workflow, not necessarily seven independently running agents.

| Component             | Responsibilities                                                                                  | Primary output                                   |
| --------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Orchestrator          | Control execution order, retries, state and reporting                                             | Episode job record                               |
| 1. Episode Ingestion  | Discover, match and catalog episodes; acquire authorized sources                                  | Canonical episode metadata and source references |
| 2. Transcription      | Normalize available transcripts or generate from permitted audio, with timestamps and diarization | Transcript segments and quality flags            |
| 3. Narrative Analysis | Extract detailed scenes, entities, events and consequences                                        | Structured episode/event notes                   |
| 4. Continuity & Lore  | Compare with history, update candidate states and identify contradictions                         | Time-aware entity changes and continuity report  |
| 5. Wiki Analysis      | Inspect relevant wiki pages and recommend concrete changes                                        | Page-specific proposed edits                     |
| 6. Fact Verification  | Validate evidence, uncertainty and consistency                                                    | Verified or flagged recommendations              |

### 8.1 Agent 1 — Episode Ingestion requirements

**Functional requirements**

- **ING-01:** Discover an episode from a verified public podcast RSS feed, if available.
- **ING-02:** Capture canonical episode identifier, series, arc, episode number, title, description, release date/time, duration and available platform URLs.
- **ING-03:** Link the Spotify entry, YouTube video and RSS item to a single canonical record.
- **ING-04:** Detect duplicate records and uncertain matches; require review when matching confidence is insufficient.
- **ING-05:** Attempt transcript retrieval only through appropriate authorized mechanisms.
- **ING-06:** Preserve transcript source, language, availability, timestamp coverage and quality indicators.
- **ING-07:** Where transcript is unavailable, set `needs_transcription` or `blocked_source_access` rather than inventing content.
- **ING-08:** Support re-runs, incremental ingestion, source changes and a persistent status record.
- **ING-09:** Record the source's applicable rights/permission status and retention policy.

**Output contract (conceptual)**

- Canonical `episode_id`
- Title, arc, episode sequence, publication date, duration, description
- External identifiers (RSS GUID, Spotify episode ID, YouTube video ID)
- Platform/source URLs
- Transcript/audio reference with access classification
- Source provenance and last-checked timestamp
- Workflow state, warnings and duplicate/matching confidence

### 8.2 Agent 2 — Transcription requirements

- **TRN-01:** Accept existing transcripts or audio provided through authorized access.
- **TRN-02:** Preserve time-linked chunks; support approximate timestamps when sentence-level timing is unavailable.
- **TRN-03:** Distinguish speaker ID from fictional character identity; allow unresolved speaker labels.
- **TRN-04:** Separate in-character speech, out-of-character conversation, GM narration and mechanics when supported by the evidence.
- **TRN-05:** Use a glossary of recurring names, Pokémon, locations and system terms.
- **TRN-06:** Record uncertain words, missing segments and transcription quality warnings.

### 8.3 Agent 3 — Narrative Analysis requirements

- **NAR-01:** Produce ordered scene notes and an episode recap grounded in transcript passages.
- **NAR-02:** Extract named and unresolved characters, Pokémon, locations and factions.
- **NAR-03:** Track captures, evolutions, trades, team changes, battles, injuries, gains/losses of items, travel, alliances and revealed information when present.
- **NAR-04:** Connect each event to participating entities and evidence.
- **NAR-05:** Preserve quotes only where necessary and within appropriate usage limits; primarily paraphrase.
- **NAR-06:** Distinguish statements of fact from beliefs, speculation, plans and out-of-character chatter.

### 8.4 Agent 4 — Continuity & Lore requirements

- **CON-01:** Resolve name variants and aliases to established entities while preserving uncertainty.
- **CON-02:** Track time-varying status and prior history rather than overwriting earlier facts.
- **CON-03:** Separate publication/recording order from in-universe chronology.
- **CON-04:** Track what a character knows versus what the audience/GM knows, where relevant.
- **CON-05:** Surface apparent contradictions and retcons for human review.
- **CON-06:** Maintain unresolved plot threads and mark resolution only when supported.

### 8.5 Agent 5 — Wiki Analysis requirements

- **WIK-01:** Retrieve relevant pages through accessible, permitted wiki interfaces, ideally MediaWiki's API.
- **WIK-02:** Inventory existing categories, templates and editorial conventions before proposing changes.
- **WIK-03:** Match verified findings to existing pages and specific sections.
- **WIK-04:** Recommend new pages only when subject significance and wiki conventions warrant them.
- **WIK-05:** Output proposed insertion/replacement text, evidence, rationale and potential conflicting current content.
- **WIK-06:** Maintain the wiki page revision identifier consulted to avoid stale comparisons.
- **WIK-07:** Do not submit unapproved edits during MVP.

### 8.6 Agent 6 — Fact Verification requirements

- **VER-01:** Independently verify that each recommendation's evidence supports its claims.
- **VER-02:** Confirm that speculative, believed or ambiguous statements are not presented as established canon.
- **VER-03:** Identify speaker/name ambiguity and incompatible evidence.
- **VER-04:** Produce explicit pass, needs-review or rejected status per proposed claim/edit.
- **VER-05:** Reject proposed changes lacking an auditable episode source.

## 9. Existing Tooling and Integration Assessment

Tools below are **candidates for evaluation**, not yet validated against the podcast's feed or video catalog. Repository maintenance, license terms, platform policy compatibility, rates and actual functionality must be checked during discovery.

| Integration/tool                                                                                            | Candidate use                                                                                  | Caveats / decision                                                                            |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Podcast RSS (feed URL to be verified)                                                                       | Primary episode discovery, GUIDs, titles, dates, descriptions and potentially audio enclosures | Prefer if catalog is comprehensive; permission to retrieve/store audio must still be assessed |
| YouTube Data API                                                                                            | Find channel uploads/playlists and retrieve video metadata                                     | API does not generally provide arbitrary public-video transcript text                         |
| Spotify Web API                                                                                             | Cross-reference show/episode metadata and platform URLs                                        | Not a general-purpose audio or transcript download API; optional if RSS suffices              |
| [TranscriptFetch MCP server](https://github.com/TranscriptFetch/mcp-server)                                 | Candidate YouTube discovery/transcript connector                                               | Third-party dependency; evaluate pricing, policy compliance and accuracy                      |
| [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) | Candidate focused transcript MCP server                                                        | Check maintenance, reliability, caption availability and allowed access                       |
| [toorop/youtube-transcript-mcp](https://github.com/toorop/youtube-transcript-mcp)                           | Candidate transcript alternative                                                               | Evaluate underlying yt-dlp approach against platform terms and rights                         |
| [github/awesome-copilot](https://github.com/github/awesome-copilot)                                         | Patterns for Copilot agents and skills                                                         | Resource catalog rather than a verified podcast ingestion solution                            |
| GitHub Copilot Agent Skills                                                                                 | Reusable instructions for ingestion/analysis workflows                                         | Not a substitute for runtime tools, ingestion database or scheduled execution                 |
| MediaWiki API / Fandom-supported editing interfaces                                                         | Read wiki pages and eventually support approved editing                                        | Confirm Fandom availability, restrictions and permissions before use                          |

**Preferred ingestion starting stack:** verified RSS catalog + official YouTube metadata discovery + one tested transcript MCP option + a Copilot ingestion skill. Add Spotify API only if its data fills a real gap. Add speech-to-text processing when licensed source audio is available and transcripts are missing or unreliable.

**Tool selection gate:** test at least three representative episodes (older, recent, challenging dialogue). Check transcript access, timestamp precision, name accuracy, total cost, rate limits, rights compliance and failure modes before committing to any provider.

## 10. Knowledge Base and Data Model

A relational database (SQLite for pilot; PostgreSQL if scale/concurrency warrants) is the recommended source of structured truth. Original transcript references and source metadata should be preserved separately. Full-text search is initially sufficient; embeddings/vector search may be introduced if factual retrieval quality requires it.

### 10.1 Core records

| Record              | Key attributes                                                                                       |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| Episode             | Internal ID, arc, number, title, publication date, external IDs, processing status                   |
| Source              | Platform, URL, source identifier, retrieved-at, rights/access state, language                        |
| Transcript segment  | Episode ID, start/end timestamp, speaker label, text, confidence/uncertainty                         |
| Scene               | Episode ID, time span, location, participants, narrative summary                                     |
| Entity              | Unique ID, type (character, Pokémon, place, organization, item), aliases, identity confidence        |
| Event               | Event type, description, chronology, episode/time, participants, consequences                        |
| Entity relationship | Subject, predicate, object, validity period, evidence                                                |
| Fact/claim          | Structured assertion, modality, certainty, supporting source, approval status                        |
| State change        | Entity, changed attribute, old/new values, effective episode/time, evidence                          |
| Wiki page snapshot  | Page identifier, revision, retrieved-at, sections/templates of interest                              |
| Wiki edit proposal  | Page, target section, proposed text/diff, claims, validation status, approval and published revision |
| Workflow job        | Episode, stage, run/version, timestamps, status, retries, error details                              |

### 10.2 Canon and epistemic classifications

- **Confirmed canon:** Established by directly supported in-world events or authoritative narrative statements.
- **Character belief:** A character's stated perspective, not necessarily objective truth.
- **Speculation:** Player or character theory, prediction or unresolved possibility.
- **Out-of-character:** Discussion of gameplay, plans or meta-commentary, not necessarily an in-world action.
- **Unclear/disputed:** Insufficient or contradictory evidence; do not assert as canon.

Store exact source references for assertions, including episode, time span, transcript version and (when possible) audio reference. A model-generated confidence score is advisory and cannot replace verification.

### 10.3 Identity and time

- One canonical episode may have multiple platform sources.
- One entity may have multiple names or aliases; ambiguous matches remain unresolved.
- Separate the date a statement was made, the in-world time it describes, and the date it was published.
- Preserve conflicting claims rather than destructively reconciling them.
- A current-state view should be derived from supported historical changes.

## 11. Output Artifacts

### 11.1 Episode Research Notes (Markdown)

Each processed episode should yield:

- Identifying details (arc, episode, date, sources and transcript quality)
- Short executive recap
- Chronological scene-by-scene notes with source times
- Important character developments
- Pokémon captures/evolutions/team changes and battles where applicable
- Key NPCs, organizations, locations and item changes
- Continuity connections and unresolved threads
- Confirmed facts, ambiguous claims and issues requiring human review
- References to the underlying evidence

### 11.2 Wiki Update Report (Markdown)

Each recommendation includes:

- Proposed target wiki page and section (or reason for a new page)
- Type: add, revise, remove, create, or needs-review
- Proposed wiki-ready wording or structured edit description
- Rationale and why the current page is incomplete/outdated
- Supporting episode ID, timestamps and relevant passages
- Confirmation status and material uncertainty
- Wiki revision read and proposed edit status
- Approver decision, notes and published revision when applicable

The recommendation report should avoid implying a change occurred until publication is verified.

## 12. Review, Approval, and Publication

### MVP workflow

1. Show all proposed edits grouped by wiki page.
2. Provide source references and source-context snippets for each substantive claim.
3. Allow reviewer to accept, reject or request correction.
4. Preserve decision history and resulting edited text.
5. Support manual copy into Fandom; record publication confirmation only after verification.

### Future assisted editing

Automated submission may be considered after successful accuracy and reliability assessment, with explicit human approval for each change set, authenticated authorized access, page revision checks, rate limits, audit logs and rollback capability.

Wiki editors' local policies, license/attribution rules and community expectations override automation convenience.

## 13. Reliability, Security, Rights, and Nonfunctional Requirements

- **Traceability:** Every factual recommendation has a verifiable source and workflow version.
- **Privacy and credentials:** Keep API keys and account tokens out of Git; use secret management and least privileges.
- **Copyright and terms:** Verify permitted podcast audio/transcript acquisition, retention and model-processing rights. Do not bypass protections or redistribute transcripts wholesale.
- **Robustness:** Each stage can retry independently; failures cannot silently skip missing episodes.
- **Observability:** Capture source status, job timing, cost estimate, token/audio usage, errors and retry history.
- **Idempotency:** Key records by stable IDs and deduplicate cross-platform entries.
- **Versioning:** Record prompt/skill version, model/service version and transcript version so outputs can be audited.
- **Change control:** Maintain a searchable history of reviewer decisions and any wiki edits.
- **Quality:** Detect long silent/missing segments, hallucinated citations and low-confidence speaker attribution.
- **Retention:** Define authorized retention and deletion practices for audio, transcripts and derived records.
- **Budget controls:** Use processing limits and report costs; exact cost targets are TBD after provider testing.

## 14. Repository and Skills Organization (Proposed)

This structure represents planning boundaries only; no agents or scripts are required at this stage.

```text
unbeatablecast-agents/
├── .github/
│   ├── agents/
│   │   ├── episode-ingestion.agent.md
│   │   ├── narrative-analysis.agent.md
│   │   ├── continuity-review.agent.md
│   │   └── wiki-review.agent.md
│   └── skills/
│       ├── podcast-episode-ingestion/SKILL.md
│       ├── transcript-analysis/SKILL.md
│       ├── pokemon-tracking/SKILL.md
│       ├── continuity-tracking/SKILL.md
│       ├── evidence-validation/SKILL.md
│       └── wiki-change-proposals/SKILL.md
├── .vscode/
│   └── mcp.json                # Non-secret MCP configuration
├── docs/
│   ├── product-requirements.md
│   ├── data-model.md
│   ├── canon-guidelines.md
│   ├── wiki-conventions.md
│   └── pilot-evaluation.md
└── schemas/                   # Future record and output schemas
```

Skills specify _how_ to do repeatable tasks and required evidence/output standards; MCP servers provide external capabilities. A job runner and persistent datastore will still be needed for unattended scheduled processing. GitHub Copilot sessions alone should not be assumed to provide a continuously running ingestion service.

## 15. Delivery Plan

### Phase 0 — Source and wiki discovery

**Deliverables:** verified RSS source and complete catalog estimate; Spotify/YouTube account/channel associations; sample video coverage; transcript availability assessment; review of wiki structures, community conventions and rights/access requirements.

**Exit criterion:** an approved, documented source-access strategy with no unresolved critical permissions issue.

### Phase 1 — Three-episode pilot

**Deliverables:** ingestion of three consecutive or otherwise representative episodes; canonical matching; transcript acquisition or authorized transcription; detailed notes; structured events; human-reviewable wiki change reports; evaluation scores.

**Exit criterion:** pilot meets acceptable accuracy and traceability thresholds or identifies specific remediations.

### Phase 2 — Historical backfill

**Deliverables:** chronological, incremental processing of the archive by story arc; entity glossary updates; continuity reviews at arc boundaries; remediation of historical contradictions.

**Exit criterion:** target historical catalog processed with an auditable coverage report and manageable unresolved-review queue.

### Phase 3 — New-episode operations

**Deliverables:** scheduled discovery, incremental processing, alerting on source failures, cost tracking and regular reviewer reports.

**Exit criterion:** reliable handling of new releases without duplicates or unnoticed failures.

### Phase 4 — Optional assisted wiki editing

**Deliverables:** authenticated approved-edit submission, stale-revision detection, logging and rollback process.

**Exit criterion:** wiki administrators' support and documented successful supervised trial.

## 16. Risks and Mitigations

| Risk                                     | Impact                       | Proposed mitigation                                                           |
| ---------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------- |
| Missing or blocked YouTube captions      | No transcript available      | Authorized audio/transcription fallback; explicit blocked state               |
| Third-party MCP server breaks            | Ingestion disruption         | Interchangeable providers, tested fallback, version pinning                   |
| Inaccurate names and speaker attribution | Wrong character history      | Entity glossary, uncertain labels and review checkpoints                      |
| Out-of-character speech treated as canon | False wiki facts             | Canon classifications, specialized verification                               |
| Cross-platform duplicate episodes        | Duplicate event records      | Canonical ID, aliases and idempotent operations                               |
| Historical contradictions and retcons    | Confused timelines           | Evidence-preserving, temporal claims model                                    |
| Incomplete or inaccessible wiki API      | Poor comparison              | Manual page export or approved alternative access; do not bypass restrictions |
| Copyright/platform rules                 | Compliance risk              | Check rights and terms; minimize stored/copied source text                    |
| Excessive operating cost                 | Project becomes uneconomical | Sample benchmarking, staged processing, caching, quotas                       |
| Incorrect wiki publication               | Community trust impact       | Human approval, revision comparison, audit trail                              |

## 17. Dependencies and Open Questions

Before implementation, answer or validate:

1. What is the **official RSS feed URL**, and does it contain the full historical archive?
2. Which Spotify show and YouTube channel/playlist entries are official? Are their catalogs complete and equivalent?
3. Are captions present and obtainable for representative old and new YouTube episodes? Are timestamps and speaker details adequate?
4. Has the podcast publisher authorized downloading, storing and transcribing episode audio if needed?
5. What are the wiki's current page categories, templates and policies for citations, bot contributions and editorial approval?
6. What is the expected cadence of new episodes, and how quickly must recommendations be ready?
7. Who is the initial human reviewer and who can publish to the wiki?
8. Which model/transcription providers meet budget, accuracy, rights and data-retention requirements?
9. What processing/storage budget and local-versus-cloud deployment constraints apply?
10. How should ambiguous speaker identities, alternate versions of episodes, retcons and disputed canon be adjudicated?

## 18. Initial Product Decisions and Recommended Defaults

| Decision                   | Initial recommendation                                                                        |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| Publishing                 | Human-review-only; manual edits for MVP                                                       |
| Backfill                   | Chronological, arc by arc                                                                     |
| Analysis detail            | Scene-level notes and source-linked events                                                    |
| Ingestion source           | Verified RSS for catalog; YouTube for video discovery/transcript evaluation; Spotify optional |
| Implementation environment | Develop in VS Code/GitHub Copilot, with portable skills and interchangeable MCP tools         |
| Database                   | SQLite pilot; consider PostgreSQL later                                                       |
| Search                     | Full-text first; optional semantic/vector search later                                        |
| Agent topology             | One orchestrator with specialized steps/skills before independent autonomous agents           |
| Storage of media           | Only where rights/access allow; retain source references by default                           |
| Validation                 | Evidence-based checks and human approval before wiki publication                              |

## 19. Definition of Done for MVP

The MVP is complete when a reviewer can select an episode, obtain a source-grounded detailed recap and structured event record, inspect correctly linked historical character/Pokémon changes, view targeted wiki recommendations with supporting citations and uncertainties, and approve or reject them without any automatic wiki publishing. The workflow must detect duplicates, show blocked/failed source states, preserve processing provenance, and demonstrate acceptable quality on the documented three-episode pilot.

---

## References for Further Evaluation

- [UnbeatableCast Wiki](https://unbeatablecast.fandom.com/wiki/UnbeatableCast_Wiki)
- [TranscriptFetch MCP Server](https://github.com/TranscriptFetch/mcp-server)
- [YouTube Transcript MCP Server — kimtaeyoon83](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript)
- [YouTube Transcript MCP Server — toorop](https://github.com/toorop/youtube-transcript-mcp)
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
- [YouTube Data API documentation](https://developers.google.com/youtube/v3)
- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api)
- [MediaWiki API documentation](https://www.mediawiki.org/wiki/API:Main_page)

**Note:** External tool support and platform policies must be rechecked at implementation time. This document is a planning artifact and does not assert that any proposed MCP connector has been successfully tested against UnbeatableCast.
