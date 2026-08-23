# FORTYGUARD_GATE_0_PROBLEM_LANDSCAPE_AND_COLLISION_MAP

Status: `IN_PROGRESS_INITIAL_LANDSCAPE_CAPTURED`
Date: `2026-08-23`
Concept locked: `false`
Primary objective: build the strongest possible FortyGuard Hackathon'26 submission.

## Evidence classes

- `OFFICIAL_VERIFIED`: directly supported by a current FortyGuard-owned source or FortyGuard-Tech repository.
- `THIRD_PARTY_VERIFIED`: supported by organizer-hosted platform or public participant material that transcribes/implements current rules; useful but not promoted to first-party fact.
- `INFERRED`: analytical conclusion from verified evidence.
- `UNRESOLVED`: current sources conflict or direct first-party confirmation is not accessible.

## Repository boundary

Requested target: `Faadil1/fortyguard-temperature-ai-2026`.
Current GitHub connector result: exact requested repository returns `404`; the accessible empty repository with admin/push permission is `Faadil1/Faadil1-fortyguard-temperature-ai-2026` on `main`.

Classification: `UNRESOLVED_REPOSITORY_NAME_MISMATCH`.

Until renamed/resolved, all build artifacts created by this conversation are written only to the accessible FortyGuard repository above, never to `Faadil1/pbpd-cowork-system`.

## PBPD / I23 authority lock

Read from branch `agent/pbpd-i23-outcome-intelligence` in `Faadil1/pbpd-cowork-system`:

- PBPD stable baseline: `pbpd-builder 0.5.0`.
- I23 Outcome Intelligence: shadow challenger only.
- One real product only; duplicate I23 build forbidden.
- Runtime integration of I23 forbidden during pilot.
- Stable PBPD mutation forbidden.
- Human final authority remains supreme.
- P02 result: stable 14/14, candidate 14/14, strict improvements 0, ties 14, regressions 0.
- P03 is open by explicit user authority.

Checkpoint 1 (problem/job selection) has **not** run because Gate 0 is not frozen and no problem has been selected.

---

# 1. Official/current rule verification

## OFFICIAL_VERIFIED

Current FortyGuard-owned sources support the following:

- Hackathon is currently active in August 2026 and is a global/virtual/free event.
- Teams are 1–3 people; solo participation is allowed.
- Seven challenge tracks exist.
- The event is supported by NVIDIA; current FortyGuard social material names judges/mentors from NVIDIA and Google and mentor participation spanning FortyGuard, NVIDIA, Google, Autodesk and climate-tech practitioners.
- The Temperature API is the central sponsor technology and current API regional coverage is United States only.
- Official API docs and the official `FortyGuard-Tech/temperature-api-quickstart` are live and explicitly position the quickstart as the hackathon starting point.

Official rule page: https://www.fortyguard.com/hackathon26
Official API docs: https://docs-api.fortyguard.com/
Official quickstart: https://github.com/FortyGuard-Tech/temperature-api-quickstart

## THIRD_PARTY_VERIFIED / ORGANIZER-HOSTED

The organizer-hosted Luma listing and multiple current public participant handbook/compliance transcriptions converge on:

- Build sprint: `2026-08-18` through `2026-08-30`.
- Submission deadline: `2026-08-30`, with current participant handbook transcriptions specifying `11:59 PM GST (UTC+4)` and no late entries.
- Judging window: `2026-09-01` through `2026-09-15`.
- Winner announcement: `2026-09-16`.
- Prize pool: `$6,000`: 1st `$3,000`, 2nd `$2,000`, 3rd `$1,000`; organizer-hosted listing also mentions an internship pathway/promotion for first place and completion certificates.
- Exact seven track names transcribed from the current page:
  1. Resilient Cities & Infrastructure
  2. Future Buildings & Energy
  3. Industrial & Enterprise
  4. Government & Environment
  5. Model Designing
  6. Agentic (API + Agentic)
  7. Data Analysis & Correlation
- Current participant material consistently says FortyGuard temperature data must be central, while external datasets are allowed if licenses are respected.
- Current participant handbook transcription says: live demo link, demo video <=3 minutes, written summary <=500 words, endpoints/measured result in summary, and judge repo access via collaborator `Hackathon-FG` / `hackathon@fortyguard.com`.
- Another current compliance transcription of the official site/form reports: public GitHub repository, working demo/prototype, repo, written summary, API-usage documentation, and current form video <=3 minutes.

Organizer-hosted listing: https://lu.ma/fortyguard-hackathon26
Public current handbook transcription example: https://github.com/Cool-Staff/heatsafe-web
Public current compliance transcription example: https://github.com/Damso74/fortyguard-heat-priority-engine/blob/main/docs/hackathon-compliance.md

## UNRESOLVED RULE ITEMS

1. **Live demo requirement:** current site FAQ transcription says required; an organizer email transcribed by another participant says live demo is not required; current participant handbook transcription says live demo link required. Build policy should satisfy the stricter union unless first-party clarification supersedes it.
2. **Video duration:** site panel has been transcribed as 2–5 minutes, while current form/handbook/email transcriptions say <=3 minutes. Build policy: target <=3 minutes.
3. **Judging rubric:** one current official-page transcription gives `Impact & Relevance 40% / Technical Execution 35% / Innovation 15% / Communication 10%`; another newer panel is transcribed as `Innovation / Technical Quality / Business Viability / Presentation` without weights. Treat the weighted rubric as not yet independently first-party verified; optimize for the union.
4. **Repository visibility/account:** current participant sources indicate public repo and collaborator access, but exact collaborator username differs across participant notes (`fortyguard` vs `Hackathon-FG`). Need direct handbook/form verification before submission.
5. **Eligibility exclusions:** global participation and team size are current first-party-supported, but age/employment/other legal exclusions have not been independently extracted from a current terms page.
6. **Deployment requirement:** live demo is operationally desirable for judging but its formal requirement status conflicts across current first/second-hand channels.
7. **NVIDIA GPU prize references:** visible participant posts mention GPUs, but no current direct official prize specification was captured; do not rely on it.

### Stale information explicitly rejected

A July 2026 press article reported an August 3–17 event/deadline. This conflicts with newer organizer/current participant evidence. It is treated as stale and not used for planning.

---

# 2. FortyGuard technical landscape

## OFFICIAL_VERIFIED capabilities

### Authentication

- Header-based API key: `api-key`.
- No OAuth flow is required in the official quickstart.

### Async lifecycle

All analysis endpoints use submit-then-poll:

`POST /v1/<analysis-endpoint>` -> `activity_id` -> `GET /v1/status/{activity_id}` until terminal state.

Official client handles polling; `wait=false` exposes the activity id for custom orchestration.

### Current analysis endpoints

1. `POST /v1/heatmap`
   - Polygon GeoJSON AOI.
   - Historical/current analysis; docs state forecast up to +12 hours.
   - Exposed granularity: 60 m / 80 m / 100 m.
   - `tcm`: temperature field in °C.
   - `time_of_measure`: UTC hour of peak.
   - `exceedance`: number of hours above/below a threshold.
   - `persistence`: longest continuous run above/below threshold.

2. `POST /v1/env_params`
   - Point environmental intelligence.
   - Includes heat index/apparent temperature, humidity, precipitation, cloud cover, wet bulb, AQI/pollutants, methane, CO2 and solar irradiance metrics (GHI/DNI/DHI), subject to plan.

3. `POST /v1/satellite` — Premium
   - Satellite imagery/segmentation and class coverage.
   - Useful for surface composition / vegetation / built-environment context.

4. `POST /v1/streetview` — Premium
   - Ground-level segmentation, including urban features/facades/vegetation/roads and viewing geometry.

5. `POST /v1/heat_intelligence` — Premium
   - Multi-dimensional heat-intelligence report/PDF workflow.

6. `GET /v1/status/{activity_id}`
   - Poll async analysis.

7. System usage endpoints
   - API-key usage/credit telemetry.

Official source: https://github.com/FortyGuard-Tech/temperature-api-quickstart
Docs: https://docs-api.fortyguard.com/

### Plans / quotas / coverage

Official docs currently list:

- Basic: 1,000,000 monthly credits; heatmap max area up to 10 mi².
- Premium: 5,000,000 monthly credits; heatmap max area up to 50 mi²; premium endpoints available.
- Current regional coverage: United States only.
- Failed async tasks do not consume credits; credits are deducted after Completed.
- No numeric requests-per-second rate limit was captured; docs expose HTTP 429 for rate-limit exceeded.

A participant-transcribed organizer email says hackathon participants receive Premium/all endpoints and keys valid through judging, but this remains `THIRD_PARTY_VERIFIED` until our own key/handbook confirms it.

### Data freshness / temporal limits

- Heatmap docs: history from `2019-01-01` to present and forecast up to +12 hours.
- Hackathon FAQ has been transcribed elsewhere as saying data from `2021-01-01`; conflict remains unresolved.
- `filter_type` documentation is inconsistent: endpoint/quickstart support 1–4 (including range of days <=1 month), while a limitations page has listed 1–3. Product design should stay within an overlap-safe path until empirical API proof or clarified docs.

### Important resolution/marketing discrepancy

FortyGuard marketing references temperature at approximately 2 m above ground and elsewhere uses “2-meter precision” language. The public heatmap API contract exposes 60/80/100 m grid granularity. **Do not claim a 2 m API grid.** Treat 2 m as measurement height/model-marketing context unless FortyGuard explicitly clarifies otherwise.

## Technically distinctive sponsor-causal capabilities

The strongest FortyGuard-specific primitives are not “temperature exists.” They are:

1. **Intra-city / intra-site thermal field** at 60–100 m cells, enabling decisions that differ within the same metro/site rather than by city forecast.
2. **Duration intelligence** via exceedance and persistence, enabling decisions based on exposure windows rather than peak temperature.
3. **Timing-of-peak intelligence** via `time_of_measure`, enabling sequencing/staging decisions.
4. **Physical-context attribution** via satellite + street-view segmentation, enabling a product to connect thermal outcomes with built/surface/vegetation context.
5. **Environmental context** via wet bulb, solar and air-quality parameters where a job truly depends on them.

Sponsor-causality principle for later gates:

> If a product still works almost equally well from a generic city weather feed, sponsor causality is weak. Favor jobs where spatial variation, persistence/exceedance, timing, or scene segmentation changes the actual action.

---

# 3. Competitive collision map

## Sponsor-supplied patterns: HIGH baseline collision

The official quickstart already ships narrative workflows for:

- real-estate portfolio heat-risk screening;
- urban-planner bus-stop cooling prioritization;
- public-parks heat-resilience audit;
- single-parcel heat due diligence;
- multi-parcel heat screening/ranked shortlist.

A submission close to these without a new decision mechanism is weakly differentiated by construction.

## Visible public hackathon projects

| Public project | Problem / user | Mechanism | FortyGuard dependency | AI / decision mechanism | Demo mechanism | Distinctive feature | Collision consequence |
|---|---|---|---|---|---|---|---|
| `thermal-sentinel-agent` | generic urban heat monitoring | detect heatwaves/anomalies + alerts + planning recs | heat data | agent/MCP | dashboard | agent wrapper | **HIGH** for generic monitor+alert+agent+dashboard |
| `heatops-autopilot` | multi-site operations managers | risk from temp + exceedance + persistence + work-hour overlap | strong | LangGraph on deterministic risk | dashboard + email | auditable deterministic score | **HIGH** for field/enterprise heat ops autopilot |
| `fortyguard-heat-priority-engine` | Phoenix transit operations | rank stops by exposure + local anomaly; missions/review/audit | very strong | deterministic Pareto/scenario analysis | connected operations workflow | sophisticated evidence/provenance | **VERY HIGH** for bus-stop/transit prioritization |
| `heatwatch-fortyguard` | city EOC / public works | HVI + thermal grid + dispatch + “Last Cold Hour” + community reports | strong | autonomous response agent | command center/API | deadline + community return loop | **VERY HIGH** for municipal command center/HVI/dispatch |
| `ThermaShift-AI` | outdoor workforce | hyperlocal polling + WBGT/work-rest + voice/SMS intervention | strong | safety engine + outbound voice AI | GIS + live call trigger | direct telephony action | **VERY HIGH** for worker heat safety/alerts |
| `heat-health-risk-predictor` | public health / neighborhoods | FortyGuard + CDC SVI + Random Forest + explainability | moderate/strong | supervised risk model | interactive map | spatial train/test split | **HIGH** for heat-health vulnerability dashboard |
| `HeatSentinel` | municipal resilience | heat + ACS + cooling centers + Response Gap score + agent | strong | deterministic score + agent | command center | resource-deficit prioritization | **VERY HIGH** for municipal vulnerability/resource allocation |
| `HeatSafe` (`heatsafe-web/api`) | route/fleet operations | coolest vs fastest route + Heat Exposure Index + fleet alerts | strong | route scoring + AI narration | map-first route comparison | route alternative | **HIGH** for cool-routing/fleet heat intelligence |
| `DC-Cooling-Copilot` | data-center/campus cooling | public repo visibly targets Northern Virginia/Phoenix with heatmap/env params and persistence work | likely strong | mechanism not fully documented | backend currently visible | data-center domain | **MEDIUM-HIGH** domain collision; mechanism still unresolved |
| `KanbanCTRL` (public participant post) | field teams | agentic heat operations -> autonomous planning/optimization | strong by stated intent | agentic planner | public build-in-progress | planning/optimization | **HIGH** for generic field-team autonomous planning |

Other public repositories exist but have insufficient documentation to classify mechanisms confidently; they remain `UNRESOLVED_VISIBLE_COMPETITOR` rather than guessed.

## Current high-collision mechanism families

Treat as red unless a later concept contains a genuinely different causal mechanism:

- heat monitoring + alerts + AI agent + dashboard;
- city heat map + vulnerability index + cooling-center/resource dispatch;
- outdoor-worker heat safety + work/rest + SMS/voice alerts;
- transit/bus-stop cooling or shade prioritization;
- generic heat-safe routing / coolest route / fleet alerting;
- real-estate portfolio heat scoring / parcel due diligence;
- generic data-center cooling copilot;
- “autonomous field-ops” where the agent simply watches thresholds and creates tasks.

Do not reject the domains categorically; reject or differentiate the **mechanism**.

---

# 4. Initial problem/job landscape — no concept selection

Scales: `H/M/L`; collision is worse when high.

| Problem family | Who has the problem? | Decision that changes | Cost of wrong/no decision | Why generic weather may be insufficient | FortyGuard materiality | Hackathon proofability | Current collision |
|---|---|---|---|---|---|---|---|
| Distribution-grid / transformer / substation thermal operations | utility operations / asset managers | where/when to derate, inspect, shift load or prioritize thermal-risk assets | outages, accelerated aging, capacity loss, truck rolls | one station/city forecast misses feeder/site microclimates and persistent hot pockets | **H** if thermal persistence materially changes capacity/maintenance decisions | **M-H** with public asset/network data + real thermal field | **L-M** visible FortyGuard collision |
| Industrial outdoor asset maintenance / plant-yard operations | reliability / maintenance planners | which asset/work package to service first and when | downtime, equipment derating/failure, unsafe work windows | plant/yard surfaces can differ materially over short distances and hours | **H** if asset scheduling uses cell-level persistence/timing | **H** if a finite asset set can be mapped and actions compared | **M**; generic field-ops agents already visible |
| Energy/building cooling-capacity allocation across campuses/portfolios | facilities / energy managers | where to pre-cool, shift load, stage cooling or spend retrofit effort | peak-demand cost, comfort/SLA breaches, equipment stress | portfolio/campus thermal conditions can diverge from reference station | **H** when cell-level exposure duration drives action | **H** for campus/portfolio demo | **M-H** because sponsor track + data-center/building interest |
| Logistics yards / loading docks / last-mile thermal exposure windows | fleet/yard/operations managers | stage trailers/vehicles, sequence loading, shift dwell or service window | product/asset damage, worker exposure, delay | yard/dock heat and persistence may differ spatially; city temp does not identify hotspots | **M-H** if decision is about spatial dwell/exposure rather than generic route alert | **H** with yard/stop set + timeline | **M-H**; cool-route/fleet + field ops already visible |
| Cold-chain last-mile exception prevention | pharma/food logistics | which delivery/transfer is at greatest ambient exposure risk and should be resequenced | spoilage, compliance failure, patient/product loss | local ambient exposure during handoff/dwell can vary | **M**: internal package sensors/refrigeration remain more direct than ambient API | **H** visually | **M**; sponsor causality must be proven carefully |
| Large venue / campus heat operations | venue/campus operations | gate/queue/staffing/shade/water/resource placement by hour/zone | medical incidents, abandonment, service failure | one forecast cannot resolve hot queues/paths/parking zones | **H** if zone-level peak timing/persistence drives operations | **H** 60–90 s before/after operational proof | **L-M** visible collision |
| Emergency responder staging/rehab during heat events | incident command / EMS/fire operations | where to stage rehab and rotate crews | responder illness, slower response | scene-level thermal field can differ from city weather | **M-H** with environmental params/persistence | **M-H** | **M-H** because municipal/worker safety collisions |
| Aviation ground operations | airport/ramp operations | gate/ramp task sequencing, equipment/crew staging | delays, worker/equipment heat stress | ramp/apron microclimate can differ within airport | **M-H** for ground ops; **L** for aircraft performance if FortyGuard is only a proxy | **M-H** | **L-M** visible collision |
| EV charging / charging-campus thermal operations | charging-network operator | where/when to throttle, maintain, add capacity or route service | derating, queue growth, charger failure | site thermal persistence can vary across a network | **H** if paired with charger utilization/thermal derating logic | **H** | **L-M** visible collision |
| Agriculture field operations | farm/irrigation manager | irrigation/work timing/zone prioritization | yield/water/labor loss | field microclimates matter, but crop/soil/ET data can dominate | **M** unless exact thermal field adds decision value beyond ag weather/remote sensing | **H** | **L-M** visible collision |
| Retail/parking/queue operations | store/campus operator | staffing, queue location, service timing | customer/worker discomfort, abandonment | local pavement/queue exposure differs from city station | **M** | **H** | **L** collision but consequence weaker |
| Healthcare/EMS demand staging | health system/EMS ops | where to stage outreach/ambulance/mobile resources | delayed response, service overload | neighborhood heat exposure differs | **M-H** | **M**; claims/privacy constraints | **H** because vulnerability/municipal response products |
| Data-center thermal operations | DC facilities/site planning | cooling reserve, maintenance/site/campus decisions | SLA risk, power/cooling cost, capacity loss | local ambient heat affects heat rejection/cooling efficiency | **H** | **H** | **H** now: public DC Cooling Copilot + FortyGuard's own current data-center thermal-screen work |
| Public transit / bus-stop interventions | transit agencies | which stops/routes need intervention | rider exposure, capital misallocation | stop-level thermal differences matter | **H** | **H** | **VERY HIGH**: official quickstart + sophisticated public entrant |
| Real-estate / parcel screening | owners/investors | which site/property to acquire/retrofit | capital risk/opex | parcel-level exposure matters | **H** | **H** | **VERY HIGH**: sponsor quickstart ships this workflow |
| Municipal HVI / cooling center response | city/EOC/public health | where to deploy interventions | health impact/resource waste | neighborhood heat field matters | **H** | **H** | **VERY HIGH** public entrant saturation |
| Outdoor-worker heat alerts | construction/agriculture/industrial supervisors | work/rest/hydration/stop-work timing | injury/fatality/productivity | site microclimate matters | **H** | **H** | **VERY HIGH** public entrant saturation |

## Initial high-potential problem families (UNLOCKED)

This is **not** a concept shortlist and not a selection. These are families worth deeper proof because they currently combine consequence, sponsor causality and lower mechanism collision:

1. **Distribution-grid / electrical-asset thermal operations** — strongest current blend of consequential decisions + spatial/persistence causality + comparatively low visible FortyGuard collision.
2. **Industrial outdoor-asset maintenance / plant-yard sequencing** — strong decision economics and demoability, but must avoid collapsing into generic worker-alert/field-agent mechanics.
3. **EV charging / distributed energy asset thermal operations** — asset derating/capacity/maintenance decisions can be directly temperature-sensitive and visually provable; external datasets need verification.
4. **Large venue / campus operational allocation** — strong 60–90 s proof surface and local thermal heterogeneity; impact/business seriousness needs stronger evidence before promotion.
5. **Energy/building portfolio/campus cooling allocation** — strong sponsor causality, but building/data-center space has increasing collision and sponsor-provided examples.
6. **Aviation ramp/ground operations** — potentially strong overlooked job if framed around ground assets/crew/sequence rather than aircraft-performance claims; needs domain validation.

### Watchlist, not rejected

- data centers: high value and sponsor causal, but current collision has increased materially;
- logistics/cold-chain: strong operational story, but sponsor causality must beat internal-sensor/weather substitutes;
- emergency response: high consequence but overlaps crowded municipal/worker-response mechanisms.

---

# 5. Gate 0 unknowns / falsifiers

Before landscape freeze:

1. Resolve direct current Participant Handbook / submission form requirements if accessible.
2. Confirm our hackathon registration/API plan and whether Premium/all endpoints are actually provisioned; never commit secrets.
3. Empirically verify API response schema, unit, granularity, temporal range, plan ceiling and async lifecycle once key is available.
4. Expand collision search specifically around top unlocked families (grid, industrial assets, EV charging, venue/campus, aviation ground ops) before calling them low-collision.
5. Gather external domain evidence for the top families: actual decision thresholds, economic/safety consequence, existing workaround and available demo datasets.
6. Run the first PBPD checkpoint **only after** this evidence is frozen: stable PBPD 0.5.0 problem/job recommendation first, then independent I23 shadow recommendation, then human decision.

# Exact next gate/action

`next_gate: FORTYGUARD_GATE_0_PROBLEM_LANDSCAPE_AND_COLLISION_MAP`

`next_action:` resolve the current rule/submission contradictions where possible, perform targeted external proof and collision research for the six unlocked families, verify accessible datasets and sponsor causality, then freeze Gate 0. Only after that run PBPD checkpoint 1 and start independent concept-mechanism divergence.
