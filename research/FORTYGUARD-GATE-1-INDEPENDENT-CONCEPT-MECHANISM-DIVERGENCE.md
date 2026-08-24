# FORTYGUARD_GATE_1_INDEPENDENT_CONCEPT_MECHANISM_DIVERGENCE

Status: `DIVERGENCE_COMPLETE_SELECTOR_NEXT`
Date: `2026-08-24`
Problem/job locked by human: `EV_CHARGING_NETWORK_THERMAL_CAPACITY_AND_DERATING_OPERATIONS`
Concept locked: `false`
Primary build system: `PBPD 0.5.0`
I23: `shadow challenger only`

## Independence protocol

The first-pass generators were separated by mechanism family and were not allowed to read one another's outputs before producing their own candidate. The goal was mechanism diversity, not agent-count theater.

Preserved rules:
- FIRST_PASS_INDEPENDENCE
- DISAGREEMENT_PRESERVATION
- AGENT_COUNT != DIVERSITY
- GENERATOR != SELECTOR
- NO_DEFAULT_FRANKENSTEIN_MERGE
- HUMAN_FINAL_AUTHORITY

All candidates solve the same locked job: help a charge-point/fleet charging operator make better capacity/allocation decisions during high heat by using FortyGuard temperature intelligence structurally rather than decoratively.

## Current evidence common to all candidates

- FortyGuard heatmap: 60/80/100 m cells plus `time_of_measure`, `exceedance`, `persistence`; async submit/poll architecture.
- FortyGuard forecast horizon documented up to +12 hours.
- DOE/NREL AFDC provides current U.S. station data and current EV charging-unit records including connector `power_kw` and port counts; many network feeds update daily.
- Manufacturer evidence confirms ambient-temperature derating is real and equipment-specific. ABB publishes products for which derating applies at high ambient temperature; Eaton specifies operating-temperature limits and derating behavior.
- A 2026 field study of a 50 kW DC fast charger in extreme desert heat reports severe thermal derating, with offered power reductions of roughly 35–40 kW under peak summer conditions and near-doubling of charge duration in the tested scenario.
- Targeted public GitHub/web searches on 2026-08-24 found no clearly documented FortyGuard Hackathon'26 repository centered on EV-charger thermal derating/capacity operations. Negative evidence is not exhaustive.

## Candidate A — THERMAL CAPACITY DISPATCH / JOB SCHEDULER

**Decision owner:** fleet charging manager / CPO operations manager.

**Decision:** which charging jobs should go to which site and time window so vehicles receive required energy before deadlines despite heat-driven capacity loss.

**Mechanism:**
1. ingest site/charger inventory and nameplate power;
2. bind each charger profile to an explicit manufacturer derating curve or operator-provided curve;
3. query FortyGuard for spatial temperature plus peak timing/persistence;
4. convert nameplate power into a time-indexed `expected_thermal_capacity_kw` under stated assumptions;
5. optimize vehicle/job assignments against energy needs and deadlines;
6. compare against a naive nameplate-capacity schedule and a generic city-weather baseline.

**FortyGuard dependency:** strong if local thermal differences or persistence change assignment/order. Generic weather collapses nearby stations toward the same thermal assumption.

**AI/decision mechanism:** constrained optimization / scheduling; optional explanation layer is subordinate to deterministic evidence.

**60–90 second judge proof:** show the same 5–10 charging jobs before/after heat intelligence. One or more assignments move because a station expected to deliver nameplate power is thermally constrained during the job window. Display: `150 kW nameplate -> 112.5 kW modeled thermal capacity -> job moved to Site B -> deadline preserved`.

**Data realism:** real FortyGuard; real AFDC station/power fields where used; manufacturer curve real; demo charging jobs may be synthetic/operator-input and must be labeled as such.

**Collision:** low visible direct collision; moderate adjacency to routing/fleet products, but mechanism is charging-capacity scheduling rather than coolest-route alerts.

**Critical risk:** requires enough real FortyGuard spatial/persistence spread to change at least one allocation. Manufacturer model identity must not be inferred from AFDC network metadata.

**Falsifier:** if FortyGuard does not change the schedule versus generic weather on a defensible hot-area test, sponsor causality is too weak.

---

## Candidate B — NETWORK THERMAL CAPACITY RESERVE

**Decision owner:** charging-network operations / capacity planning.

**Decision:** how much network charging capacity is actually dependable during a heat window and where to preserve/shift demand before correlated derating creates a local capacity cliff.

**Mechanism:** replace static nameplate MW with a time-indexed thermal reserve curve. Aggregate each site's thermally adjusted expected capacity to show network `nameplate MW`, `heat-adjusted MW`, `reserve margin`, and clusters at risk of simultaneous derating.

**FortyGuard dependency:** very strong if spatial + persistence data expose correlated hot clusters that city-level weather would hide.

**AI/decision mechanism:** network optimization / scenario analysis rather than alerts.

**Judge proof:** `3.2 MW installed` becomes `2.46 MW heat-adjusted between 14:00–17:00`; the system identifies which cluster causes the shortfall and what demand should be shifted.

**Data realism:** real locations/power fields possible from AFDC; charger-specific derating profile still requires operator/demo equipment profiles.

**Collision:** low direct collision; concept is more infrastructure/energy-system than route planning.

**Critical risk:** aggregate MW is powerful but more abstract; without real demand/load data the recommended shift may become scenario-based.

---

## Candidate C — THERMAL FAULT TRIAGE / RESIDUAL ANOMALY DETECTOR

**Decision owner:** CPO reliability / field maintenance manager.

**Decision:** when a charger is under-delivering, is the shortfall explainable by local thermal conditions or is it large enough to justify investigation/truck roll?

**Mechanism:** build an expected-power envelope from local FortyGuard temperature/persistence + equipment-specific derating curve. Compare operator/OCPP measured power against this envelope. `Observed loss - thermally expected loss = residual anomaly`.

**FortyGuard dependency:** moderate-to-strong for external predictive thermal context, but existing charger telemetry may include temperatures; sponsor causality is weaker for highly instrumented operators than in Candidate A/B.

**AI/decision mechanism:** evidence-grounded diagnostic classification; no failure prediction claim.

**Judge proof:** two 150 kW chargers both deliver 105 kW. Site A is 48°C and 105 kW falls inside its expected thermal band: no maintenance dispatch. Site B is 36°C and 105 kW is unexplained: investigate.

**Data realism:** requires operator telemetry. Hackathon demo could use explicitly synthetic/sample OCPP telemetry; this weakens external proof compared with A/B.

**Collision:** very low; highly distinctive.

**Critical risk:** cannot claim actual fault without diagnostic evidence; can only prioritize investigation. Thermal sensors already inside some chargers can reduce FortyGuard necessity.

---

## Candidate D — THERMAL HARDWARE FIT / PROCUREMENT ENGINE

**Decision owner:** charging infrastructure procurement / engineering.

**Decision:** which charger model/cooling configuration is thermally suitable for each site before capital is committed.

**Mechanism:** apply manufacturer-specific derating curves to FortyGuard historical/persistence profiles at proposed sites. Compare expected derating hours, usable power distribution and thermal-capacity loss across candidate hardware.

**FortyGuard dependency:** strong for site-specific historical thermal exposure; generic weather weakens site discrimination.

**AI/decision mechanism:** multi-criteria equipment selection / portfolio optimization.

**Judge proof:** same 180 kW purchase decision at two Phoenix-area sites yields different hardware recommendations because site thermal persistence differs; show expected usable-kW envelope by model.

**Data realism:** excellent — does not need live charging telemetry; manufacturer docs + FortyGuard + site locations are enough.

**Collision:** low, though it approaches sponsor quickstart parcel/site due-diligence patterns if presented primarily as a map/score.

**Critical risk:** less dynamic and less visibly “AI” than dispatch; must avoid becoming a static site-screening dashboard.

---

## Candidate E — THERMAL SLA / QUEUE TRUTH ENGINE

**Decision owner:** public CPO network operations/customer experience.

**Decision:** what charging throughput/ETA should be promised and where should drivers be routed when thermal derating changes expected service time.

**Mechanism:** convert thermally adjusted power into expected service time/queue throughput and expose heat-aware station availability promises.

**FortyGuard dependency:** moderate-to-strong.

**Judge proof:** station that looks available under nameplate power is removed from recommended routing because heat-adjusted service time breaks the SLA.

**Collision:** **medium-high** because public cool-route/fleet-alert products are already visible in the hackathon. Mechanism is more capacity/SLA oriented, but judge perception could collapse it into routing.

**Critical risk:** queue estimates require demand/session assumptions; collision and extra state reduce attractiveness.

---

## Candidate F — THERMAL RETROFIT PRIORITY

**Decision owner:** CPO infrastructure/asset manager.

**Decision:** which existing charging sites should receive cooling/shade/thermal-management investment first.

**Mechanism:** combine FortyGuard persistence with charger derating exposure, then optionally use satellite/street-view segmentation to characterize local physical context and rank retrofit candidates.

**FortyGuard dependency:** strong for exposure detection; attribution/mitigation benefit is less proven.

**Judge proof:** rank sites by modeled lost thermal capacity and show physical-context evidence around the top site.

**Collision:** low-to-medium.

**Critical risk:** without a defensible causal model linking a particular retrofit to a specific temperature reduction, the product can identify where to investigate but cannot honestly promise recovered kW/ROI. This limits the strongest possible claim.

---

## Selector input — preserved without merge

The selector receives all six candidates only after their first-pass mechanisms are frozen. It may choose one, reject all, or preserve a runner-up. It must not create a Frankenstein combination merely because features are complementary.

Selection dimensions:
- sponsor causality;
- consequence / business value;
- 60–90 second evaluator proof;
- technical defensibility and honesty boundary;
- real-data availability;
- innovation/distinction versus visible FortyGuard field;
- build scope before Aug 30;
- likelihood that the first FortyGuard probe can falsify or validate the core claim quickly.

`GENERATOR != SELECTOR`

`concept_locked: false`
