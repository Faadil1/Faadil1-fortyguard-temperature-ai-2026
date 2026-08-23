# FORTYGUARD_GATE_0_PROBLEM_LANDSCAPE_AND_COLLISION_MAP — FREEZE

Status: `FROZEN`
Date: `2026-08-23`
Concept locked: `false`
Problem/job selected: `false` — selection occurs at PBPD/I23 checkpoint 1 after this freeze.

## Freeze rule

Gate 0 freezes the evidence landscape, not a product concept. Independent concept generation remains forbidden until checkpoint 1 selects a problem/job family.

## Current rules / technical baseline

- Official FortyGuard schedule currently shows build sprint Aug 18–30, project submission Aug 30, judging Sept 1–15, winners Sept 16.
- FortyGuard current public material confirms the event is fully online/free and teams are 1–3.
- Submission details still contain public-source contradictions. Build policy remains the strict union: public repo, working prototype, public/live demo, demo video <=3 minutes, concise written summary, explicit FortyGuard API-use documentation, and judge collaborator access. Exact collaborator identity and whether live demo is formally mandatory remain unresolved.
- Current API contract: `api-key` authentication; async submit -> `activity_id` -> status polling; `/v1/heatmap` at 60/80/100m; `tcm`, `time_of_measure`, `exceedance`, `persistence`; `/v1/env_params`; Premium satellite/streetview segmentation and heat-intelligence report.
- Current Heatmap docs support dates from 2019-01-01 and forecast up to +12 hours. The limitations page still conflicts with endpoint docs on `filter_type=4`; build paths should remain overlap-safe until our own key proves behavior.
- Do not translate FortyGuard marketing references to 2m / 10m² into an API-grid claim. The hackathon build will use the documented 60/80/100m heatmap contract unless empirical proof says otherwise.

## Collision freeze

### Red / saturated mechanisms

- generic heat monitor + alerts + AI agent + dashboard
- municipal HVI + cooling-resource dispatch
- outdoor worker WBGT/work-rest + SMS/voice alerts
- transit/bus-stop cooling prioritization
- coolest-route / fleet heat alerts
- real-estate portfolio or parcel screening
- generic data-center cooling copilot
- generic field-ops threshold agent

### Sponsor-supplied patterns

The official FortyGuard quickstart itself already supplies real-estate portfolio heat risk, bus-stop cooling prioritization, public-parks heat resilience, single-parcel due diligence, and multi-parcel screening. Close variants have high collision even before considering other participants.

### Targeted negative collision evidence

Current GitHub/public searches found no clearly documented FortyGuard Hackathon'26 repository specifically centered on:

- distribution-transformer / substation thermal-headroom operations;
- EV charging-network thermal derating / capacity operations;
- aviation-ramp asset thermal operations.

This is negative evidence only, not proof that no competitor exists.

## Problem/job evidence matrix

Scoring is 1–5 where 5 is strongest, except collision where 5 is most crowded/worst.

| Family | Consequence | FortyGuard causality | External proof | Public/demo data | 60–90s judge proof | Collision | Build risk |
|---|---:|---:|---:|---:|---:|---:|---:|
| Distribution grid / transformer thermal operations | 5 | 5 | 5 | 2 | 4 | 2 | 4 |
| EV charging-network thermal capacity / derating operations | 4 | 5 | 5 | 5 | 5 | 1 | 2 |
| Industrial outdoor asset maintenance / yard sequencing | 4 | 4 | 3 | 2 | 3 | 3 | 4 |
| Large venue / campus operational allocation | 3 | 4 | 2 | 4 | 4 | 2 | 3 |
| Building/campus cooling allocation | 4 | 3 | 5 | 4 | 4 | 3 | 2 |
| Aviation ramp / ground operations | 4 | 3 | 4 | 3 | 4 | 2 | 3 |
| Data centers | 5 | 5 | 5 | 3 | 4 | 4 | 3 |

## Family findings

### A. Distribution-grid / transformer thermal operations

**Who:** utility asset manager, distribution operations lead, smart-grid manager.

**Decision:** where and when to reduce/redistribute load, inspect, derate, prioritize maintenance, or treat a transformer/substation zone as thermally constrained.

**Why it matters:** ORNL/DOE evidence shows persistent high ambient temperature can cause transformer derating, accelerated insulation aging, shortened lifetime, and abrupt failure. DOE's 2024 transformer resilience report likewise states transformer cooling requirements depend on load and ambient temperature and that prolonged high-temperature operation accelerates aging.

**FortyGuard causality:** exceptionally strong. FortyGuard itself explicitly markets utilities and smart-grid managers around localized thermal stress across substations/transformer zones, proactive load balancing, predictive maintenance and reduced transformer overheating.

**Why generic weather is insufficient:** this job becomes specifically FortyGuard-causal only when assets in the same utility territory receive different decisions because local heat field, persistence, or peak timing differs. A citywide forecast does not provide that spatial allocation signal.

**Main weakness:** public operational asset/load data are sparse or sensitive. HIFLD has a substation dataset but access is marked restricted-public. A credible demo may therefore require public coarse assets or an explicitly synthetic feeder/load layer, which weakens proof if handled poorly.

**Collision:** low among visible FortyGuard builds, but FortyGuard's own commercial positioning means judges will expect domain correctness.

### B. EV charging-network thermal capacity / derating operations

**Who:** charge-point operator, fleet charging operator, charging-network operations manager, site-reliability manager.

**Decision:** which charging sites should receive vehicles/load, where nominal charger power should be treated as thermally derated, when to shift charging, and which sites need cooling/shade/maintenance attention before a heat window.

**External causal proof:** charger thermal derating is not hypothetical. ABB Terra documentation gives steady-state output derating by ambient temperature: 100% through 35°C, 90% at 36–40°C, 85% at 41–45°C, 75% at 46–50°C, and 65% at 51–55°C for documented models. Eaton Green Motion documentation similarly specifies thermal derating, including 75% output at 55°C for listed models. A 2026 field study of a commercial fast charger in hot-arid conditions reports severe charger-side thermal derating and substantially longer charging sessions under peak summer heat.

**Public/demo data:** DOE/NREL AFDC publishes downloadable and API-accessible U.S. charging-station data with network, station and port information, refreshed through network APIs/CSV/manual sources. This gives a current, legitimate real asset layer without exposing sensitive grid infrastructure.

**FortyGuard causality:** strong if the product compares nearby charging sites using FortyGuard's local thermal field and duration/persistence to predict effective rather than nameplate charging capacity before derating occurs. Generic city weather cannot distinguish nearby sites; onboard charger telemetry is reactive and may not provide forward spatial planning across an entire network.

**60–90 second proof:** unusually strong. A judge can see multiple nearby stations with similar nominal power but different FortyGuard heat/persistence; translate manufacturer thermal curves into expected available power; then show a network/fleet decision change. The proof is numeric and visually attributable to FortyGuard.

**Collision:** no clearly documented FortyGuard Hackathon'26 EV-charger thermal-derating project found in targeted searches. Negative evidence only.

**Main weakness:** temperature cannot be treated as the sole cause of actual delivered charging power. Vehicle battery state, charger design, connector temperature, utilization and internal telemetry also matter. Any model must be explicitly `expected thermal headroom / derating`, not a claim of observed charger output unless measured data exists.

### C. Industrial outdoor assets / plant-yard sequencing

FortyGuard itself frames plant/HSE users around outdoor field zones and adaptive scheduling. That confirms sponsor fit, but visible participant worker-safety products already occupy much of the obvious mechanism. Asset-reliability decisions remain viable only if tied to an equipment-specific thermal limit rather than another worker alert system. Public operational data are weak. Keep as secondary.

### D. Large venue / campus operational allocation

Highly visual and public-site data are accessible, but consequence and willingness-to-pay evidence are weaker than grid/charging. Without a tightly defined resource-allocation decision it risks becoming another heat map. Keep as secondary.

### E. Building/campus cooling allocation

DOE evidence shows predictive pre-cooling and demand shifting can generate real savings and reduce peaks. However this also demonstrates a causality weakness: generic local weather forecasts already enable the job. FortyGuard would need intra-campus spatial differentiation, persistence or built-context attribution to materially change control. Strong engineering fallback, weaker sponsor exclusivity than A/B.

### F. Aviation ramp / ground operations

ICAO material confirms extreme heat affects airport infrastructure, HVAC loads, personnel and aircraft performance, and may force scheduling changes. However aircraft takeoff-performance decisions depend on certified aviation weather observations, making FortyGuard a questionable replacement. Ground-equipment/crew mechanisms drift toward saturated worker-safety patterns. Deprioritize unless a new asset-specific mechanism emerges later.

### G. Data centers

High consequence and direct FortyGuard commercial fit, but visible `DC-Cooling-Copilot` competition plus FortyGuard's own explicit data-center positioning materially increase collision. Keep as fallback, not preferred first problem family.

## Freeze conclusion

Two problem families survive Gate 0 as true finalists:

1. `EV_CHARGING_NETWORK_THERMAL_CAPACITY_AND_DERATING_OPERATIONS`
2. `DISTRIBUTION_GRID_TRANSFORMER_THERMAL_HEADROOM_AND_ASSET_OPERATIONS`

The first has the best combination of sponsor causality, quantitative external proof, current public asset data, low visible collision and 60–90 second demo clarity.

The second has greater infrastructure consequence and the strongest direct alignment with FortyGuard's own utility/smart-grid positioning, but carries materially higher data and domain-model risk inside the remaining hackathon window.

Secondary reserve families:

- building/campus cooling allocation;
- industrial asset reliability/maintenance sequencing;
- large venue/campus allocation.

Deprioritized for this build unless new evidence appears:

- aviation ramp/ground operations;
- generic logistics/cool routing;
- public-health municipal command centers;
- worker alerting;
- transit stop prioritization;
- real-estate screening;
- generic data-center cooling.

## Gate 0 decision

`FORTYGUARD_GATE_0_PROBLEM_LANDSCAPE_AND_COLLISION_MAP = FROZEN`

`concept_locked = false`

`problem_job_selected = false`

Exact next action: run PBPD 0.5.0 checkpoint 1 recommendation first against this frozen landscape; preserve it before running I23 shadow; then compare, record human authority, and only after the problem/job decision begin independent concept-mechanism divergence.
