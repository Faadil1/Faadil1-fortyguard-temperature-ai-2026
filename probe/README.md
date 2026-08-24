# Gate 2 — FortyGuard EV Thermal Causality Probe

Status: `READY_FOR_REAL_API_KEY`

This probe exists to **kill or preserve** the selected concept before deep UI/product work.

Selected concept:

`THERMAL_CAPACITY_DISPATCH_JOB_SCHEDULER`

Core causal claim under test:

```text
FortyGuard hyperlocal ambient heat
→ declared EVSE derating curve
→ expected usable charging kW
→ changed feasible-site set / charging decision
```

## Non-negotiable evidence boundary

- `expected_thermal_capacity_kw` is **derived**, not observed charger output.
- AFDC/NLR supplies real EV charging-site locations/metadata; it does **not** establish that a station uses ABB equipment.
- The ABB Terra 184 heavy-duty profile is a declared scenario/equipment input for the first probe.
- FortyGuard heat is not charger-internal or connector temperature.
- Vehicle-side limits, connector limits, grid constraints, utilization and session telemetry are not silently modeled.
- Fixture mode is only a pipeline test and can never count as sponsor-causality evidence.

## Why Phoenix / 2024-07-05 first

The National Weather Service records 118°F at Phoenix Sky Harbor on 5 July 2024. An extreme but real historical day gives the first bounded probe a strong chance to cross documented equipment derating bands without inventing temperature data.

This is **causal-existence evidence**, not a claim that every Phoenix day produces the same result.

## Equipment profile used by the first probe

ABB Terra 184, heavy-duty operation, rated 150 kW in the North America operation/installation manual.

| Ambient temperature | Output factor |
| --- | ---: |
| ≤ 40°C | 100% |
| 41–45°C | 93% |
| 46–50°C | 80% |
| 51–55°C | 67% |
| >55°C | no inference — outside documented probe range |

The manual also warns that connector model/rating, the EV socket and ambient conditions can impose additional limitations; the probe therefore never describes its derived capacity as measured delivered power.

## Current FortyGuard schema/unit issue

Current first-party quickstart materials are not perfectly consistent:

- the current Python client docstring describes `tcm` tile readings as Fahrenheit;
- the implemented use-case design spec says cached heatmap GeoJSON hourly/summary values are Fahrenheit and converts them to Celsius;
- a README analytic-type table describes `tcm` as Celsius.

The probe preserves raw values and a unit-attestation record. It accepts Fahrenheit automatically only when the returned live schema matches the current SDK/spec contract or an explicit response field confirms the unit. Unknown schemas fail loudly instead of using numeric-magnitude guessing.

The same official quickstart use cases describe the heatmap-derived `peak_temp_c` as ambient air temperature at the point and feed it into `env_params`, supporting the semantic comparison to an EVSE ambient-temperature derating curve.

## AFDC / NLR

The U.S. alternative-fuel API moved from `developer.nrel.gov` to `developer.nlr.gov` in 2026. The probe uses the current NLR endpoint and `DEMO_KEY` by default (or `NLR_API_KEY` when supplied) to discover real available public EV charging locations with at least one ≥50 kW port.

The initial same-equipment scenario deliberately **does not** bind the AFDC-reported hardware to ABB.

## Run the zero-network fixture

```bash
python probe/thermal_causality_probe.py --mode fixture
```

Expected evidence class:

`SYNTHETIC_FIXTURE_PIPELINE_TEST_ONLY`

A fixture `PASS_STRONG` means only that the code can detect a known mechanical difference. It does **not** preserve the concept.

## Run the real kill-probe

Set the FortyGuard key locally. Do not commit it.

```bash
export FORTYGUARD_API_KEY='...'
python probe/thermal_causality_probe.py --mode live
```

Windows PowerShell:

```powershell
$env:FORTYGUARD_API_KEY='...'
python probe/thermal_causality_probe.py --mode live
```

Default live probe:

- center: Phoenix, AZ;
- date: `2024-07-05`;
- candidate times: `14:00,15:00,16:00`;
- max completed TCM calls: `3`;
- granularity: `100 m`;
- selected test AOI: capped at approximately `8 mi²`;
- same declared ABB Terra 184 heavy-duty profile across selected sites;
- stops additional calls as soon as `PASS_STRONG` is reached.

Example overrides:

```bash
python probe/thermal_causality_probe.py \
  --mode live \
  --date 2024-07-05 \
  --hours 14:00,15:00,16:00 \
  --granularity 100 \
  --site-count 6 \
  --max-aoi-sq-mi 8
```

## Gate meanings

### P1 — schema + unit

Hard fail if the live response does not expose a recognized TCM temperature field/unit contract without guessing.

### P2 — thermal differentiation

Strongest result: selected sites using the same declared equipment profile fall into at least two different documented derating bands.

This proves the local thermal field can create a materially different expected capacity state.

### P4 — decision delta

Before live data is seen, the probe fixes one-hour job requirements at:

`100, 110, 120, 130, 140, 145 kW`

For every requirement, it compares the feasible-site set under:

1. a **uniform AOI temperature** baseline; and
2. the **FortyGuard hyperlocal** temperature at each site.

The uniform AOI case is an internal isolation baseline and is never mislabeled as an external weather product.

A strong decision delta occurs when a non-degenerate feasible-site set changes because of thermal capacity, rather than a tie-break order changing.

## Verdicts

`PASS_STRONG`
: multiple documented derating bands are represented **and** at least one predeclared job's feasible-site set changes.

`PASS_THERMAL_DIFFERENTIATION_ONLY`
: material thermal-capacity differentiation exists, but the predeclared job set does not yet produce a decision change. Do not fabricate jobs; inspect whether the full scheduler still has a legitimate path.

`FAIL_NO_MATERIAL_DIFFERENTIATION`
: bounded live evidence does not support the concept's sponsor-causality premise for this test. Stop before deep build and reconsider the preserved alternatives.

## I23 shadow delta at Checkpoint 3

Stable PBPD and I23 agree on the core architecture and kill-probe.

I23 adds one material proof-path recommendation:

1. **Historical/replay mode** — frozen, reproducible causal proof.
2. **Prospective mode** — current/+12-hour run showing that the same pipeline can support a forward operational decision.

The prospective mode is added only after the historical causality probe passes and must not endanger submission readiness. Current weather is not a kill criterion because it may simply not be hot enough to cross a derating band.

This is recorded as `STRICT_IMPROVEMENT_CANDIDATE`, not an I23 promotion and not yet final outcome evidence.

## Output

Runtime output is written under `probe/output/` and should include:

- selected AFDC site snapshot;
- exact FortyGuard request payload;
- `activity_id`;
- raw terminal response;
- schema fingerprint/hash;
- raw and converted temperatures;
- equipment curve and binding declaration;
- site-level expected thermal capacities;
- uniform baseline;
- predeclared job sensitivity;
- causality verdict.

Do not commit API keys. Review real raw responses before committing any evidence snapshot.
