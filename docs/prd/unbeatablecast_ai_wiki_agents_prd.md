# Product Requirements Document: UnbeatableCast AI Wiki Intelligence System

**Status:** Draft for planning and review
**Version:** 0.2
**Date:** October 12, 2026
**Product type:** Internal, human-supervised AI research and wiki-maintenance workflow
**Primary property:** [UnbeatableCast Wiki](https://unbeatablecast.fandom.com/wiki/UnbeatableCast_Wiki)

## 1. Executive Summary

The UnbeatableCast AI Wiki Intelligence System will ingest authorized episode content from a Pokémon tabletop role-playing podcast, produce detailed, source-linked narrative records, track characters, Pokémon, locations, organizations, relationships, and story events across episodes, and recommend specific updates to the community wiki.

The system's initial role is **research and editorial assistance**, not autonomous publication. Each suggested wiki change must be grounded in identifiable episode evidence, compared with the current wiki, and approved by a human reviewer before being published.

The architecture will use deterministic software for discovery, retrieval and record keeping; the official [UnbeatableCast YouTube channel](https://www.youtube.com/@UnbeatableCast) as the primary episode catalog and evidence reference; Spotify links as corresponding alternate audio-listening sources; and RSS as supplemental metadata where available. In the pilot, a human will start each run from VS Code/GitHub Copilot. Transcript acquisition will try accessible YouTube captions first, then evaluate no-extra-cost alternatives; episodes without a suitable source remain explicitly blocked. The system must not assume Spotify or YouTube provide unrestricted audio or transcript access.

## 2. Problem Statement

Tabletop RPG podcasts create large volumes of evolving narrative information over many episodes. Manual maintenance of a fandom wiki is time-consuming, particularly when updates require recalling when a character learned something, when a Pokémon joined or left a team, or how an event connects to a larger arc. Episode blurbs are insufficient to reconstruct canon. Transcripts introduce additional problems: uncertain speaker attribution, incorrect names, out-of-character discussion and speculative statements mistaken for established facts.

There is no reliable, centralized workflow to connect episodes with evidence-backed story records and actionable wiki changes.

## 3. Goals and Success Criteria

### 3.1 Goals

1. Discover and catalog published episodes from the official YouTube channel, linking corresponding Spotify audio versions and using RSS as a supplemental source where useful.
2. Obtain available and permitted transcript or audio inputs with timestamps and provenance.
3. Produce detailed, chronological notes that preserve meaningful scenes, actions and outcomes.
4. Maintain a cross-episode knowledge base of entities, relationships, facts and changes over time.
5. Detect wiki content that is missing, outdated, incomplete or potentially inconsistent with episode evidence.
6. Deliver clear page-specific change proposals, with sources and human approval controls.
7. Validate whether historical backfill is worthwhile after the pilot, and support observable, manually started episode processing with retry handling.

### 3.2 Proposed pilot acceptance targets

These are initial targets to validate during the pilot, not measured results.

| Metric                          | Proposed acceptance target | Measurement                                                                                        |
| ------------------------------- | -------------------------: | -------------------------------------------------------------------------------------------------- |
| Factual precision               |                       ≥95% | Human audit of sampled extracted claims against episode audio                                      |
| Major-event recall              |                       ≥90% | Comparison with human-created event checklist                                                      |
| Evidence traceability           |                       100% | Every proposed factual wiki addition has an episode/source reference and timestamp where available |
| Wiki recommendation usefulness  |                       ≥80% | Human reviewer rates proposals useful/actionable                                                   |
| Unsupported factual wiki edits |                          0 | Editorial audit of approved/published Fandom changes                                                |
| Duplicate processing            |     0 avoidable duplicates | Unique episode identity and ingest logs                                                            |

Record cost per episode, processing duration, transcript availability, speaker accuracy and rate of human corrections as additional pilot observations rather than hard launch gates.

## 4. Scope

### In scope — MVP

- Discover and catalog episodes from the official UnbeatableCast YouTube channel as the primary source.
- Associate each YouTube episode with its corresponding Spotify audio listing when available; use RSS as a supplemental metadata and cross-check source.
- Prefer accessible YouTube captions; evaluate free alternatives for transcription if captions are missing or inadequate, and flag unavailable content.
- Retain transcript source material in the project workspace for internal analysis, subject to applicable source, provider, and repository access terms.
- Segment transcripts into scenes and extract narrative events and changes.
- Track recurring characters, Pokémon, locations, organizations and arcs.
- Maintain source-level evidence, ambiguity classifications and historical state.
- Read relevant public wiki pages where permitted; compare them to verified findings.
- Produce Markdown episode notes and human-reviewable wiki change proposals.
- Run a three-episode pilot; decide whether to backfill the archive after evaluating pilot results.

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
5. **YouTube-first discovery.** Use the official YouTube channel as the primary episode catalog; link Spotify audio versions and use RSS as a supplemental source. Prefer official interfaces and maintained integrations over custom scraping.
6. **Graceful degradation.** Missing transcripts yield an explicit blocked/pending status, not a fabricated summary.
7. **Idempotent processing.** Reprocessing the same episode should not create duplicate records or wiki proposals.
8. **Portable prompts and schemas.** Keep business logic independent of one LLM or IDE vendor wherever practical.
9. **No incremental spend.** Use existing Copilot credits and no-extra-cost tools; stop with an explicit blocked status rather than incur a charge.

## 7. End-to-End Workflow

1. **Discover:** The operator manually starts a run from VS Code/GitHub Copilot and checks the official UnbeatableCast YouTube channel; consult RSS and Spotify as supplemental sources.
2. **Resolve identity:** Create one canonical episode record anchored by its YouTube video ID, link the corresponding Spotify episode and any RSS item using stable IDs, normalized titles, dates and duration tolerances, and flag uncertain matches.
3. **Acquire inputs:** Try accessible YouTube captions first, then a tested no-extra-cost transcription option when needed. Retain provenance and record access status. Channel presence does not guarantee caption availability or permission to retrieve or process content.
4. **Transcribe/normalize:** When needed, use the selected no-extra-cost option for speech recognition and diarization; normalize names using a maintained glossary without concealing uncertain corrections.
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
| 2. Transcription      | Normalize accessible captions or use a tested, permitted, no-extra-cost fallback, with timestamps and diarization | Transcript segments and quality flags            |
| 3. Narrative Analysis | Extract detailed scenes, entities, events and consequences                                        | Structured episode/event notes                   |
| 4. Continuity & Lore  | Compare with history, update candidate states and identify contradictions                         | Time-aware entity changes and continuity report  |
| 5. Wiki Analysis      | Inspect relevant wiki pages and recommend concrete changes                                        | Page-specific proposed edits                     |
| 6. Fact Verification  | Validate evidence, uncertainty and consistency                                                    | Verified or flagged recommendations              |

### 8.1 Agent 1 — Episode Ingestion requirements

**Functional requirements**

- **ING-01:** Discover episodes from the official UnbeatableCast YouTube channel as the primary catalog; use RSS and Spotify as supplemental sources.
- **ING-02:** Capture canonical episode identifier, series, arc, episode number, title, description, release date/time, duration and available platform URLs.
- **ING-03:** Anchor the canonical episode record on its YouTube video ID and link the corresponding Spotify audio entry and RSS item when available.
- **ING-04:** Detect duplicate records and uncertain matches; require review when matching confidence is insufficient.
- **ING-05:** Prefer accessible YouTube captions; use a free transcription alternative only after evaluating its access method, terms, cost, and data handling.
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

- **TRN-01:** Prefer available YouTube captions; accept other transcripts or audio only through a tested, permitted, no-extra-cost path.
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
| Official [UnbeatableCast YouTube channel](https://www.youtube.com/@UnbeatableCast) + YouTube Data API        | Primary episode discovery and video reference; retrieve channel uploads/playlists and metadata | Verify catalog coverage during discovery. The official [captions download API](https://developers.google.com/youtube/v3/docs/captions/download) requires permission to edit the video; it is not a general public-video transcript API. |
| Spotify Web API                                                                                             | Link the corresponding Spotify audio version to each canonical YouTube episode                 | Secondary listening source, not the episode catalog or transcript source; not a general-purpose audio or transcript download API |
| Podcast RSS (feed URL to be verified)                                                                       | Supplemental metadata, stable GUIDs, publication details and potentially audio enclosures      | Use for cross-checking or filling metadata gaps; permission to retrieve/store audio must still be assessed |
| [Xenova Whisper Web](https://github.com/xenova/whisper-web)                                                  | Candidate browser-based, open-source speech-to-text fallback                                  | MIT-licensed application code; evaluate the hosted demo's current availability, model licensing, CPU runtime, and data handling before use. Do not assume demo uploads remain local. |
| [github/awesome-copilot](https://github.com/github/awesome-copilot)                                         | Patterns for Copilot agents and skills                                                         | Resource catalog rather than a verified podcast ingestion solution                            |
| GitHub Copilot Agent Skills                                                                                 | Reusable instructions for ingestion/analysis workflows                                         | Not a substitute for transcript acquisition or a continuously running ingestion service       |
| MediaWiki API / Fandom-supported editing interfaces                                                         | Read wiki pages and eventually support approved editing                                        | Confirm Fandom availability, restrictions and permissions before use                          |

**Preferred pilot stack:** official YouTube channel catalog + Spotify episode links for alternate listening + supplemental RSS metadata where available + accessible YouTube captions + a Copilot-driven workflow. If captions are missing or inadequate, benchmark a no-install browser-based Whisper option and other no-extra-cost alternatives whose terms and data handling are acceptable. Do not add paid APIs, paid overages, or services requiring billing setup. If no suitable no-cost source is available, mark the episode blocked and report why.

**Tool selection gate:** test the first three episodes listed below. Check caption availability, timestamp precision, name accuracy, CPU runtime, no-cost limits, model/service terms, data handling and failure modes before selecting a fallback. The owner reports a Copilot “Plus” plan; verify its exact account plan and use only included AI credits. Disable additional paid usage so runs stop when the included allowance is exhausted.

## 10. Knowledge Base and Data Model

Human-readable Markdown and JSON files in the project repository are the recommended canonical knowledge base for the pilot, making episode records, entity histories and review changes easy to inspect in Git. Keep full transcripts in the project's source-material area rather than embedding them in generated notes. Repository visibility and access must be set appropriately before storing them. A local SQLite index may be added later as a rebuildable convenience if cross-episode queries become cumbersome; it is not the initial source of truth. Full-text search is initially sufficient; embeddings/vector search may be introduced if factual retrieval quality requires it.

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
- Scene-by-scene notes focused on meaningful actions and outcomes, with timestamped YouTube links as the primary evidence references
- Short executive recap
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

Recommendations may cover existing or new pages for characters, Pokémon, episodes, locations, organizations, and items. Propose broadly during the pilot, but flag material uncertainty and avoid implying a wiki change occurred until publication is verified. Public repository drafts must be labeled `AI-generated; unreviewed` until a human has reviewed them.

## 12. Review, Approval, and Publication

### MVP workflow

1. Generate Markdown episode notes and wiki proposals, with a separate pull request for each episode.
2. Provide source references and source-context snippets for each substantive claim.
3. Label proposals as AI-generated and unreviewed; the sole pilot operator reviews the output and records corrections, approval, or rejection.
4. Preserve decision history and resulting edited text.
5. Keep Fandom publication manual. The operator transfers approved copy into the wiki and records publication only after verification.

The pilot is manually started from VS Code/GitHub Copilot. New-episode processing has a target turnaround of one week after the operator starts a run; automated polling and background scheduling are deferred.

### Future assisted editing

Automated submission may be considered after successful accuracy and reliability assessment, with explicit human approval for each change set, authenticated authorized access, page revision checks, rate limits, audit logs and rollback capability.

Wiki editors' local policies, license/attribution rules and community expectations override automation convenience.

## 13. Reliability, Security, Rights, and Nonfunctional Requirements

- **Traceability:** Every factual recommendation has a verifiable source and workflow version.
- **Privacy and credentials:** Keep API keys and account tokens out of Git; use secret management and least privileges.
- **Source and service terms:** Verify access, retention, and processing terms for episode material and selected tools. Do not bypass platform protections. Keep source transcripts in the project workspace, with repository visibility set appropriately before storage; do not present them as public outputs.
- **Robustness:** Each stage can retry independently; failures cannot silently skip missing episodes.
- **Observability:** Capture source status, job timing, cost estimate, token/audio usage, errors and retry history.
- **Idempotency:** Key records by stable IDs and deduplicate cross-platform entries.
- **Versioning:** Record prompt/skill version, model/service version and transcript version so outputs can be audited.
- **Change control:** Maintain a searchable history of reviewer decisions and any wiki edits.
- **Quality:** Detect long silent/missing segments, hallucinated citations and low-confidence speaker attribution.
- **Retention:** Retain transcripts in the project source-material area for internal evidence verification; define deletion and repository-access controls before ingesting the pilot.
- **Budget controls:** No separate paid APIs, paid overages, or tools requiring billing setup. Use accessible captions first, then only no-extra-cost transcription options; stop and report a blocked episode if none works. Use only the owner's included Copilot allowance and disable additional paid usage.
- **Resource limits:** The operator's machine is CPU-only. Avoid requiring local software installation for the pilot; benchmark browser-based options and report runtime before selecting a fallback.

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
├── data/
│   ├── episodes/                # Markdown notes and JSON event records
│   ├── entities/                # Canonical entity and state-history records
│   └── source-material/         # Retained transcripts; protect with appropriate repo access
└── schemas/                   # Future record and output schemas
```

Skills specify _how_ to do repeatable tasks and required evidence/output standards; MCP servers provide external capabilities. A job runner and persistent datastore will still be needed for unattended scheduled processing. GitHub Copilot sessions alone should not be assumed to provide a continuously running ingestion service.

## 15. Delivery Plan

### Phase 0 — Source and wiki discovery

**Deliverables:** verify official YouTube channel association and catalog coverage; map the supplied Spotify show to YouTube episodes; check the first three episodes for accessible captions; benchmark no-cost transcript options and Copilot credit use; inspect wiki structures and conventions; set repository visibility and source-material handling.

**Exit criterion:** a documented no-extra-cost source and processing path for the pilot, with repository access and tool terms checked.

### Phase 1 — Three-episode pilot

**Pilot episodes, in original release order:**

1. [Episode 1](https://youtu.be/eEmoq6v2M9M)
2. [Episode 2](https://youtu.be/15PJ3PBhcEw)
3. [Episode 3](https://youtu.be/03TuT2XpAwk)

**Spotify show:** [UnbeatableCast](https://open.spotify.com/show/0nZ5jCbpDj3LKS7ICAqi4S)

**Deliverables:** one pull request per episode containing labeled Markdown notes, JSON/Markdown knowledge records, and human-reviewable proposals across relevant page types; timestamped YouTube references; human audit and corrections.

**Exit criterion:** the sole operator evaluates the provisional accuracy and traceability goals, documents corrections, and identifies remediations. If no free and suitable transcript path is available, record the episode as blocked rather than incur a charge.

### Phase 2 — Historical backfill

Whether to backfill the full archive or selected arcs will be decided after the pilot. If approved, process chronologically by story arc, update the entity glossary, and review continuity at arc boundaries.

**Exit criterion:** to be set after the pilot.

### Phase 3 — New-episode operations

Scheduled discovery is deferred. Initially, the operator manually starts processing after a new YouTube release, targeting a report within one week. Reconsider scheduling only after the pilot.

**Exit criterion:** reliable manual processing without duplicates or unnoticed failures.

### Phase 4 — Optional assisted wiki editing

**Deliverables:** authenticated approved-edit submission, stale-revision detection, logging and rollback process.

**Exit criterion:** wiki administrators' support and documented successful supervised trial.

## 16. Risks and Mitigations

| Risk                                     | Impact                       | Proposed mitigation                                                           |
| ---------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------- |
| Missing or blocked YouTube captions      | No transcript available      | Try a tested no-extra-cost fallback; otherwise set an explicit blocked state  |
| Free transcription option is too slow or limited | Pilot delay or unusable output | Benchmark the first three episodes and report runtime/limits before choosing a fallback |
| Copilot credits are exhausted            | Processing pauses or unexpected cost | Disable extra paid usage; stop at the included allowance and retry after reset |
| Inaccurate names and speaker attribution | Wrong character history      | Entity glossary, uncertain labels and review checkpoints                      |
| Out-of-character speech treated as canon | False wiki facts             | Canon classifications, specialized verification                               |
| Cross-platform duplicate episodes        | Duplicate event records      | Canonical ID, aliases and idempotent operations                               |
| Historical contradictions and retcons    | Confused timelines           | Evidence-preserving, temporal claims model                                    |
| Incomplete or inaccessible wiki API      | Poor comparison              | Manual page export or approved alternative access; do not bypass restrictions |
| Copyright/platform rules                 | Compliance risk              | Verify source-handling requirements; keep retained transcripts in the project source-material area and out of generated public outputs |
| Repository access is too broad for source material | Unintended transcript exposure | Set repository visibility/access appropriately before retaining transcripts; label generated drafts clearly |
| Incorrect wiki publication               | Community trust impact       | Human approval, revision comparison, audit trail                              |

## 17. Dependencies and Open Questions

Before implementation, validate:

1. Whether the YouTube channel's full archive, including older or special episodes, is complete.
2. Caption availability and quality for the three supplied pilot episodes; benchmark the no-install Whisper Web candidate and any other no-extra-cost option for CPU runtime, timestamp quality, and data handling.
3. The exact Copilot plan associated with the owner's “Copilot Plus” account and how to disable any paid usage beyond included credits.
4. Repository visibility and access controls for retained source transcripts before pilot ingestion.
5. Current wiki page categories, templates, citation conventions, and community policies.
6. Whether to backfill the full archive or selected story arcs after pilot evaluation.

## 18. Initial Product Decisions and Recommended Defaults

| Decision                   | Current decision                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Pilot episodes             | First three episodes in original release order; URLs listed in Phase 1                                                      |
| Episode discovery          | Official YouTube channel is primary; Spotify audio links are secondary; RSS is supplemental                                |
| Evidence links             | Timestamped YouTube links are primary; show Spotify as an alternate listening link                                         |
| Pilot detail and coverage  | Scene-by-scene meaningful actions/outcomes; propose broadly across relevant page types, including new pages when useful     |
| Pilot operator/reviewer    | Owner is sole operator and reviewer; ambiguous canon is flagged for human adjudication                                      |
| Pilot execution            | Manually started from VS Code/GitHub Copilot; no background schedule; target report within one week of a run                |
| Pilot outputs              | Markdown and JSON in Git; one pull request per episode; drafts labeled AI-generated and unreviewed                          |
| Fandom publication         | Manual human review and publication only; no automatic wiki edits                                                          |
| Knowledge base             | Markdown/JSON is canonical; consider a derived local SQLite index only if needed                                           |
| Transcript source          | YouTube captions first; evaluate free fallback only if missing/inadequate; block an episode if no suitable free path exists |
| Source retention           | Retain transcripts in the project source-material area; set repository visibility/access appropriately before ingestion    |
| Cost                       | No additional paid services or paid overages; use only included Copilot credits and no billing setup for transcription      |
| Pilot evaluation           | Owner audits all three episodes and records corrections against provisional PRD targets                                    |
| Historical backfill        | Decide scope after the pilot                                                                                                 |
| Agent topology             | One orchestrator with specialized steps/skills before independent autonomous agents                                        |
| Search                     | Full-text first; optional semantic/vector search later                                                                      |

## 19. Definition of Done for MVP

The MVP is complete when the sole operator can manually process the first three episodes, obtain scene-level source-grounded notes and Markdown/JSON event records, inspect linked historical character/Pokémon changes, and review one clearly labeled pull request per episode containing timestamped YouTube evidence and wiki proposals. The workflow must link Spotify audio versions where matched, detect duplicates, show blocked/failed transcript states, preserve processing provenance, stay within the no-extra-cost constraint, and support human-only Fandom publication. The operator audits the pilot against the provisional targets; archive backfill and scheduled processing remain future decisions.

---

## References for Further Evaluation

- [UnbeatableCast Wiki](https://unbeatablecast.fandom.com/wiki/UnbeatableCast_Wiki)
- [UnbeatableCast YouTube channel](https://www.youtube.com/@UnbeatableCast)
- [UnbeatableCast Spotify show](https://open.spotify.com/show/0nZ5jCbpDj3LKS7ICAqi4S)
- [Xenova Whisper Web](https://github.com/xenova/whisper-web)
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
- [YouTube Data API documentation](https://developers.google.com/youtube/v3)
- [YouTube captions download API](https://developers.google.com/youtube/v3/docs/captions/download)
- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api)
- [GitHub Copilot plans](https://docs.github.com/en/copilot/get-started/plans)
- [GitHub Copilot individual usage and billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing)
- [MediaWiki API documentation](https://www.mediawiki.org/wiki/API:Main_page)

**Note:** External tool support and platform policies must be rechecked at implementation time. Whisper Web and any free hosted service remain candidates, not validated transcript sources. Copilot plan names, allowances and billing controls can change; verify the account's current plan and disable additional paid usage before the pilot.
