#!/usr/bin/env python3
"""Bounded sponsor-causality probe for FortyGuard Hackathon'26.

Purpose
-------
Try to falsify the selected concept *before* deep product/UI work:

    FortyGuard hyperlocal ambient heat
      -> declared EVSE derating curve
      -> expected usable kW
      -> changed feasible-site set / charging decision

This is not a charger telemetry model. `expected_thermal_capacity_kw` is a derived
scenario quantity under an explicitly declared equipment profile.

Modes
-----
fixture : zero-network, synthetic pipeline/schema test. Never sponsor evidence.
live    : AFDC/NLR real charging-site locations + real FortyGuard heatmap calls.

No third-party Python packages are required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

FORTYGUARD_BASE_URL = "https://api.fortyguard.com"
AFDC_BASE_URL = "https://developer.nlr.gov/api/alt-fuel-stations/v1/nearest.json"

# ABB Terra 184 heavy-duty operation: 150 kW rating; official North America
# manual section 10.14.3/10.14.4. The equipment identity is a SCENARIO INPUT.
# It is never inferred from an AFDC station record.
EQUIPMENT_PROFILE = {
    "id": "ABB_TERRA_184_HEAVY_DUTY_SCENARIO",
    "nameplate_kw": 150.0,
    "source": "ABB Terra 94/104/124/184 North America operation/installation manual, section 10.14",
    "binding": "SCENARIO_INPUT_NOT_AFDC_EQUIPMENT_ASSERTION",
    "bands": [
        {"max_temp_c": 40.0, "factor": 1.00, "label": "<=40C / 100%"},
        {"max_temp_c": 45.0, "factor": 0.93, "label": "41-45C / 93%"},
        {"max_temp_c": 50.0, "factor": 0.80, "label": "46-50C / 80%"},
        {"max_temp_c": 55.0, "factor": 0.67, "label": "51-55C / 67%"},
    ],
    "above_55c": "OUT_OF_DOCUMENTED_RANGE_NO_CAPACITY_INFERENCE",
}

# Predeclared before any live thermal result. This prevents designing one magic
# job after seeing the data. Each job is a one-hour average-power requirement.
JOB_SENSITIVITY_KW = [100.0, 110.0, 120.0, 130.0, 140.0, 145.0]

# Current official quickstart sources conflict in prose. The current SDK
# docstring + its implemented use-case design spec describe raw TCM tile values
# as Fahrenheit; README tables elsewhere describe TCM as Celsius. We therefore
# accept F automatically only for a matching known TCM schema, record that
# provenance, and refuse unknown schemas rather than infer from magnitude.
KNOWN_TCM_RAW_UNIT = "F"
KNOWN_TCM_UNIT_ATTESTATION = (
    "official_quickstart_current_client_docstring_plus_use_case_design_spec; "
    "README_conflict_recorded"
)


@dataclass
class Site:
    id: str
    name: str
    latitude: float
    longitude: float
    source: str
    afdc_id: int | None = None
    afdc_network: str | None = None
    afdc_reported_max_power_kw: float | None = None
    equipment_profile: str = EQUIPMENT_PROFILE["id"]
    equipment_binding: str = EQUIPMENT_PROFILE["binding"]


@dataclass
class SiteThermalResult:
    site_id: str
    site_name: str
    latitude: float
    longitude: float
    map_method: str
    raw_temperature: float
    raw_unit: str
    temperature_c: float
    derating_band: str
    output_factor: float | None
    expected_thermal_capacity_kw: float | None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 90.0,
) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    hdrs = {"Accept": "application/json"}
    if payload is not None:
        hdrs["Content-Type"] = "application/json"
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def bbox_area_sq_mi(sites: Iterable[Site], buffer_m: float = 250.0) -> float:
    sites = list(sites)
    if not sites:
        return 0.0
    lats = [s.latitude for s in sites]
    lons = [s.longitude for s in sites]
    mid_lat = mean(lats)
    miles_per_lat_deg = 69.0
    miles_per_lon_deg = 69.0 * math.cos(math.radians(mid_lat))
    buffer_mi = buffer_m / 1609.344
    height = (max(lats) - min(lats)) * miles_per_lat_deg + 2 * buffer_mi
    width = (max(lons) - min(lons)) * miles_per_lon_deg + 2 * buffer_mi
    return max(0.0, height) * max(0.0, width)


def build_bbox_aoi(sites: list[Site], buffer_m: float = 250.0) -> dict[str, Any]:
    lats = [s.latitude for s in sites]
    lons = [s.longitude for s in sites]
    mid_lat = mean(lats)
    dlat = buffer_m / 111_320.0
    dlon = buffer_m / (111_320.0 * max(0.2, math.cos(math.radians(mid_lat))))
    south, north = min(lats) - dlat, max(lats) + dlat
    west, east = min(lons) - dlon, max(lons) + dlon
    ring = [[west, south], [east, south], [east, north], [west, north], [west, south]]
    return {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"purpose": "bounded_fortyguard_causality_probe"},
            "geometry": {"type": "Polygon", "coordinates": [ring]},
        }],
    }


def max_afdc_power_kw(record: dict[str, Any]) -> float | None:
    values: list[float] = []
    for unit in record.get("ev_charging_units") or []:
        connectors = unit.get("connectors") or {}
        if isinstance(connectors, dict):
            for connector in connectors.values():
                if isinstance(connector, dict):
                    value = connector.get("power_kw")
                    if isinstance(value, (int, float)):
                        values.append(float(value))
                elif isinstance(connector, list):
                    for item in connector:
                        if isinstance(item, dict) and isinstance(item.get("power_kw"), (int, float)):
                            values.append(float(item["power_kw"]))
    return max(values) if values else None


def fetch_afdc_sites(
    center_lat: float,
    center_lon: float,
    radius_mi: float,
    limit: int,
) -> list[Site]:
    params = {
        "api_key": os.getenv("NLR_API_KEY", "DEMO_KEY"),
        "latitude": center_lat,
        "longitude": center_lon,
        "radius": radius_mi,
        "fuel_type": "ELEC",
        "access": "public",
        "status": "E",
        "ev_power_kw_min": 50,
        "limit": min(limit, 200),
    }
    url = AFDC_BASE_URL + "?" + urllib.parse.urlencode(params)
    data = http_json("GET", url)
    sites: list[Site] = []
    for rec in data.get("fuel_stations", []):
        lat, lon = rec.get("latitude"), rec.get("longitude")
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            continue
        sites.append(Site(
            id=f"afdc-{rec.get('id')}",
            name=str(rec.get("station_name") or f"AFDC {rec.get('id')}"),
            latitude=float(lat),
            longitude=float(lon),
            source="DOE_AFDC_NLR",
            afdc_id=rec.get("id") if isinstance(rec.get("id"), int) else None,
            afdc_network=rec.get("ev_network"),
            afdc_reported_max_power_kw=max_afdc_power_kw(rec),
        ))
    if len(sites) < 3:
        raise RuntimeError(f"AFDC returned only {len(sites)} usable >=50 kW public EV sites in the search radius")
    return sites


def select_spatial_sites(
    candidates: list[Site],
    center_lat: float,
    center_lon: float,
    count: int,
    max_aoi_sq_mi: float,
) -> list[Site]:
    # Start near the center, then greedily add the point farthest from the
    # selected set while keeping the buffered bounding AOI under the area cap.
    remaining = list(candidates)
    first = min(remaining, key=lambda s: haversine_m(center_lat, center_lon, s.latitude, s.longitude))
    selected = [first]
    remaining.remove(first)
    while remaining and len(selected) < count:
        ranked = sorted(
            remaining,
            key=lambda s: min(haversine_m(s.latitude, s.longitude, q.latitude, q.longitude) for q in selected),
            reverse=True,
        )
        chosen = None
        for cand in ranked:
            trial = selected + [cand]
            if bbox_area_sq_mi(trial) <= max_aoi_sq_mi:
                chosen = cand
                break
        if chosen is None:
            break
        selected.append(chosen)
        remaining.remove(chosen)
    if len(selected) < 3:
        raise RuntimeError("Could not select at least 3 spatially distinct sites under the AOI area cap")
    return selected


def submit_and_wait_fortyguard(payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    headers = {"api-key": api_key}
    submit = http_json("POST", f"{FORTYGUARD_BASE_URL}/v1/heatmap", headers=headers, payload=payload)
    try:
        activity_id = submit["data"]["activity_id"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(f"Unexpected FortyGuard submit response: {submit}") from exc

    deadline = time.monotonic() + 600
    while True:
        try:
            status = http_json("GET", f"{FORTYGUARD_BASE_URL}/v1/status/{activity_id}", headers=headers)
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and time.monotonic() < deadline:
                time.sleep(3)
                continue
            raise
        data = status.get("data", status)
        state = str(data.get("status", "")).lower()
        if state in {"completed", "succeeded"}:
            return {
                "activity_id": activity_id,
                "submit_response": submit,
                "terminal_status_response": status,
                "result": data.get("result", data),
            }
        if state in {"failed", "error"}:
            raise RuntimeError(f"FortyGuard activity {activity_id} failed: {data}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"FortyGuard activity {activity_id} timed out with state={state!r}")
        time.sleep(3)


def normalize_feature_collection(result: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    obj: Any = result
    # Handle a few wrappers without inventing missing semantics.
    if isinstance(obj, dict) and isinstance(obj.get("result"), dict):
        obj = obj["result"]
    map_data = obj.get("map_data") if isinstance(obj, dict) else None
    stats = obj.get("stats_data", {}) if isinstance(obj, dict) else {}
    if isinstance(map_data, str):
        map_data = json.loads(map_data)
    if map_data is None and isinstance(obj, dict) and obj.get("type") == "FeatureCollection":
        map_data = obj
    if not isinstance(map_data, dict) or not isinstance(map_data.get("features"), list):
        keys = sorted(obj.keys()) if isinstance(obj, dict) else [type(obj).__name__]
        raise RuntimeError(f"No recognized FeatureCollection in FortyGuard result. Top-level keys={keys}")
    return map_data["features"], stats if isinstance(stats, dict) else {}


def recursive_unit_candidates(obj: Any, prefix: str = "") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            lk = str(key).lower()
            if ("unit" in lk or "temperature" in lk) and isinstance(value, str):
                found.append((path, value))
            found.extend(recursive_unit_candidates(value, path))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj[:20]):
            found.extend(recursive_unit_candidates(value, f"{prefix}[{idx}]"))
    return found


def resolve_tcm_unit(features: list[dict[str, Any]], stats: dict[str, Any]) -> tuple[str, str]:
    for path, value in recursive_unit_candidates(stats):
        v = value.strip().lower().replace("°", "")
        if v in {"f", "fahrenheit", "degf", "degrees_fahrenheit"}:
            return "F", f"explicit_stats_field:{path}={value}"
        if v in {"c", "celsius", "degc", "degrees_celsius"}:
            return "C", f"explicit_stats_field:{path}={value}"

    sample_props = {}
    for feat in features:
        props = feat.get("properties")
        if isinstance(props, dict) and props:
            sample_props = props
            break
    known_summary = {"average_temperature", "min_temperature", "max_temperature"} & set(sample_props)
    known_hourly = any(f"{h:02d}" in sample_props for h in range(24))
    if known_summary or known_hourly:
        return KNOWN_TCM_RAW_UNIT, KNOWN_TCM_UNIT_ATTESTATION
    raise RuntimeError(
        "Temperature unit cannot be attested from an explicit field or the current known TCM schema. "
        f"Sample property keys={sorted(sample_props)[:50]}"
    )


def polygon_centroid(feature: dict[str, Any]) -> tuple[float, float]:
    geom = feature.get("geometry") or {}
    coords = geom.get("coordinates") or []
    if geom.get("type") == "Polygon" and coords and coords[0]:
        ring = coords[0]
        lons = [p[0] for p in ring if len(p) >= 2]
        lats = [p[1] for p in ring if len(p) >= 2]
        return mean(lats), mean(lons)
    if geom.get("type") == "Point" and len(coords) >= 2:
        return float(coords[1]), float(coords[0])
    raise RuntimeError(f"Unsupported feature geometry for centroid: {geom.get('type')}")


def point_in_ring(lat: float, lon: float, ring: list[list[float]]) -> bool:
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        intersects = ((yi > lat) != (yj > lat)) and (
            lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-15) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def feature_contains(feature: dict[str, Any], lat: float, lon: float) -> bool:
    geom = feature.get("geometry") or {}
    if geom.get("type") != "Polygon":
        return False
    coords = geom.get("coordinates") or []
    return bool(coords and coords[0] and point_in_ring(lat, lon, coords[0]))


def feature_temperature_raw(feature: dict[str, Any], requested_hour: int) -> tuple[float, str]:
    props = feature.get("properties") or {}
    hour_key = f"{requested_hour:02d}"
    if isinstance(props.get(hour_key), (int, float)):
        return float(props[hour_key]), f"properties.{hour_key}"
    for key in ("average_temperature", "temperature", "value"):
        if isinstance(props.get(key), (int, float)):
            return float(props[key]), f"properties.{key}"
    raise RuntimeError(f"No recognized numeric TCM temperature field; keys={sorted(props)[:50]}")


def map_site_to_temperature(
    site: Site,
    features: list[dict[str, Any]],
    requested_hour: int,
) -> tuple[float, str, str]:
    for feat in features:
        if feature_contains(feat, site.latitude, site.longitude):
            value, field = feature_temperature_raw(feat, requested_hour)
            return value, "point_in_tile", field
    nearest = min(
        features,
        key=lambda f: haversine_m(site.latitude, site.longitude, *polygon_centroid(f)),
    )
    value, field = feature_temperature_raw(nearest, requested_hour)
    return value, "nearest_centroid_fallback", field


def to_celsius(value: float, unit: str) -> float:
    if unit == "C":
        return value
    if unit == "F":
        return (value - 32.0) * 5.0 / 9.0
    raise ValueError(unit)


def derating_for_temp_c(temp_c: float) -> tuple[float | None, str]:
    if temp_c < -35.0:
        return None, "BELOW_DOCUMENTED_RANGE"
    for band in EQUIPMENT_PROFILE["bands"]:
        if temp_c <= band["max_temp_c"]:
            return float(band["factor"]), str(band["label"])
    return None, "ABOVE_55C_OUT_OF_DOCUMENTED_RANGE"


def analyze_features(
    sites: list[Site],
    features: list[dict[str, Any]],
    stats: dict[str, Any],
    requested_hour: int,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    unit, unit_source = resolve_tcm_unit(features, stats)
    site_results: list[SiteThermalResult] = []
    source_fields: set[str] = set()
    for site in sites:
        raw_temp, method, field = map_site_to_temperature(site, features, requested_hour)
        source_fields.add(field)
        temp_c = to_celsius(raw_temp, unit)
        factor, band = derating_for_temp_c(temp_c)
        capacity = None if factor is None else EQUIPMENT_PROFILE["nameplate_kw"] * factor
        site_results.append(SiteThermalResult(
            site_id=site.id,
            site_name=site.name,
            latitude=site.latitude,
            longitude=site.longitude,
            map_method=method,
            raw_temperature=round(raw_temp, 4),
            raw_unit=unit,
            temperature_c=round(temp_c, 4),
            derating_band=band,
            output_factor=factor,
            expected_thermal_capacity_kw=None if capacity is None else round(capacity, 3),
        ))

    valid_caps = [r.expected_thermal_capacity_kw for r in site_results if r.expected_thermal_capacity_kw is not None]
    valid_factors = [r.output_factor for r in site_results if r.output_factor is not None]
    valid_temps = [r.temperature_c for r in site_results]
    uniform_temp_c = mean(valid_temps)
    uniform_factor, uniform_band = derating_for_temp_c(uniform_temp_c)
    uniform_capacity = None if uniform_factor is None else EQUIPMENT_PROFILE["nameplate_kw"] * uniform_factor

    band_count = len({r.derating_band for r in site_results if r.output_factor is not None})
    capacity_spread_kw = (max(valid_caps) - min(valid_caps)) if len(valid_caps) >= 2 else 0.0
    capacity_spread_pct_nameplate = 100 * capacity_spread_kw / EQUIPMENT_PROFILE["nameplate_kw"]

    job_sensitivity = []
    decision_changes = 0
    for required_kw in JOB_SENSITIVITY_KW:
        local_feasible = sorted(r.site_id for r in site_results if r.expected_thermal_capacity_kw is not None and r.expected_thermal_capacity_kw >= required_kw)
        uniform_feasible = sorted(r.site_id for r in site_results if uniform_capacity is not None and uniform_capacity >= required_kw)
        changed = local_feasible != uniform_feasible
        if changed:
            decision_changes += 1
        job_sensitivity.append({
            "required_average_kw": required_kw,
            "uniform_feasible_site_ids": uniform_feasible,
            "hyperlocal_feasible_site_ids": local_feasible,
            "feasible_set_changed": changed,
        })

    different_documented_bands = band_count >= 2
    material_capacity_spread = capacity_spread_pct_nameplate >= 7.0 - 1e-9
    strong_scheduler_delta = decision_changes > 0

    return {
        "evidence_class": provenance.get("evidence_class"),
        "provenance": provenance,
        "schema_fingerprint": {
            "feature_count": len(features),
            "sample_property_keys": sorted((features[0].get("properties") or {}).keys()) if features else [],
            "temperature_source_fields_used": sorted(source_fields),
            "sha256": canonical_hash({"features": features, "stats": stats}),
        },
        "unit_attestation": {"raw_unit": unit, "source": unit_source},
        "equipment_profile": EQUIPMENT_PROFILE,
        "sites": [asdict(s) for s in sites],
        "site_thermal_results": [asdict(r) for r in site_results],
        "uniform_aoi_baseline": {
            "temperature_c": round(uniform_temp_c, 4),
            "derating_band": uniform_band,
            "output_factor": uniform_factor,
            "expected_capacity_kw_per_scenario_site": None if uniform_capacity is None else round(uniform_capacity, 3),
            "note": "Internal hyperlocal-isolation baseline; not labeled external/generic weather.",
        },
        "job_sensitivity": job_sensitivity,
        "metrics": {
            "local_temperature_min_c": round(min(valid_temps), 4),
            "local_temperature_max_c": round(max(valid_temps), 4),
            "local_temperature_spread_c": round(max(valid_temps) - min(valid_temps), 4),
            "documented_derating_band_count": band_count,
            "capacity_spread_kw": round(capacity_spread_kw, 3),
            "capacity_spread_pct_of_nameplate": round(capacity_spread_pct_nameplate, 3),
            "predeclared_job_cases_with_feasible_set_change": decision_changes,
        },
        "gates": {
            "P1_unit_and_schema_attested": True,
            "P2_different_documented_derating_bands": different_documented_bands,
            "P2_material_capacity_spread": material_capacity_spread,
            "P4_non_tie_feasible_set_change": strong_scheduler_delta,
        },
        "causality_verdict": (
            "PASS_STRONG" if different_documented_bands and strong_scheduler_delta
            else "PASS_THERMAL_DIFFERENTIATION_ONLY" if different_documented_bands or material_capacity_spread
            else "FAIL_NO_MATERIAL_DIFFERENTIATION"
        ),
        "claim_boundary": {
            "expected_thermal_capacity_is_derived": True,
            "actual_delivered_power_claim": False,
            "afdc_station_implies_abb_hardware": False,
            "connector_vehicle_grid_limits_fully_modeled": False,
            "failure_prediction": False,
        },
    }


def make_fixture() -> tuple[list[Site], list[dict[str, Any]], dict[str, Any]]:
    # Deliberately synthetic and visibly labeled. Values span documented ABB
    # bands so P0 can prove the pipeline detects a decision delta mechanically.
    base_lat, base_lon = 33.4484, -112.0740
    sites = [
        Site(f"fixture-{i+1}", f"Synthetic Site {i+1}", base_lat + i * 0.004, base_lon + (i % 2) * 0.004, "SYNTHETIC_FIXTURE")
        for i in range(6)
    ]
    temps_c = [39.0, 41.0, 44.0, 47.0, 50.0, 52.0]
    features: list[dict[str, Any]] = []
    for site, temp_c in zip(sites, temps_c):
        temp_f = temp_c * 9 / 5 + 32
        d = 0.002
        ring = [
            [site.longitude - d, site.latitude - d],
            [site.longitude + d, site.latitude - d],
            [site.longitude + d, site.latitude + d],
            [site.longitude - d, site.latitude + d],
            [site.longitude - d, site.latitude - d],
        ]
        features.append({
            "type": "Feature",
            "properties": {
                "14": round(temp_f, 3),
                "average_temperature": round(temp_f, 3),
                "fixture_only": True,
            },
            "geometry": {"type": "Polygon", "coordinates": [ring]},
        })
    return sites, features, {"fixture": True}


def run_fixture(output_dir: Path) -> int:
    sites, features, stats = make_fixture()
    report = analyze_features(
        sites,
        features,
        stats,
        requested_hour=14,
        provenance={
            "evidence_class": "SYNTHETIC_FIXTURE_PIPELINE_TEST_ONLY",
            "captured_at": utc_now(),
            "billable_fortyguard_calls": 0,
            "sponsor_causality_evidence": False,
        },
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "fixture-report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print_report(report, path)
    return 0


def run_live(args: argparse.Namespace, output_dir: Path) -> int:
    api_key = os.getenv("FORTYGUARD_API_KEY")
    if not api_key:
        print("BLOCKED: FORTYGUARD_API_KEY is not set. Do not paste it into source control.", file=sys.stderr)
        return 3

    candidates = fetch_afdc_sites(args.center_lat, args.center_lon, args.afdc_radius_mi, args.afdc_limit)
    sites = select_spatial_sites(candidates, args.center_lat, args.center_lon, args.site_count, args.max_aoi_sq_mi)
    aoi = build_bbox_aoi(sites)
    area = bbox_area_sq_mi(sites)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "selected-sites.json").write_text(
        json.dumps({"sites": [asdict(s) for s in sites], "approx_aoi_sq_mi": area, "aoi": aoi}, indent=2),
        encoding="utf-8",
    )

    hours = [h.strip() for h in args.hours.split(",") if h.strip()]
    if len(hours) > args.max_tcm_calls:
        hours = hours[: args.max_tcm_calls]

    all_reports = []
    for hour_text in hours:
        hour = int(hour_text.split(":", 1)[0])
        payload = {
            "polygon_aoi": aoi,
            "date_time": {
                "start_date": args.date,
                "start_time": hour_text,
                "filter_type": 1,
            },
            "granularity": args.granularity,
            "analytic_type": "tcm",
        }
        captured_at = utc_now()
        live = submit_and_wait_fortyguard(payload, api_key)
        raw_path = output_dir / f"fortyguard-{args.date}-{hour_text.replace(':','')}-raw.json"
        raw_envelope = {
            "captured_at": captured_at,
            "request_payload": payload,
            "response": live,
        }
        raw_path.write_text(json.dumps(raw_envelope, indent=2), encoding="utf-8")

        features, stats = normalize_feature_collection(live["result"])
        report = analyze_features(
            sites,
            features,
            stats,
            requested_hour=hour,
            provenance={
                "evidence_class": "REAL_FORTYGUARD_API_PLUS_REAL_AFDC_SITE_LOCATIONS_WITH_SCENARIO_EQUIPMENT_PROFILE",
                "captured_at": captured_at,
                "fortyguard_activity_id": live["activity_id"],
                "fortyguard_request_sha256": canonical_hash(payload),
                "raw_response_file": raw_path.name,
                "afdc_source": AFDC_BASE_URL,
                "afdc_equipment_identity_claimed": False,
                "billable_fortyguard_calls_this_sample": 1,
            },
        )
        report_path = output_dir / f"causality-{args.date}-{hour_text.replace(':','')}-report.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        all_reports.append({"hour": hour_text, "report_file": report_path.name, "verdict": report["causality_verdict"], "metrics": report["metrics"]})
        print_report(report, report_path)
        if report["causality_verdict"] == "PASS_STRONG":
            print("Kill-probe strong pass reached; stopping additional TCM calls to protect credits.")
            break

    summary = {
        "run_at": utc_now(),
        "date": args.date,
        "requested_hours": hours,
        "actual_calls": len(all_reports),
        "approx_aoi_sq_mi": round(area, 3),
        "reports": all_reports,
        "overall": "PASS_STRONG" if any(r["verdict"] == "PASS_STRONG" for r in all_reports)
                   else "PASS_THERMAL_DIFFERENTIATION_ONLY" if any(r["verdict"] == "PASS_THERMAL_DIFFERENTIATION_ONLY" for r in all_reports)
                   else "FAIL_NO_MATERIAL_DIFFERENTIATION",
    }
    (output_dir / "live-run-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\nLIVE OVERALL:", summary["overall"])
    return 0 if summary["overall"].startswith("PASS") else 2


def print_report(report: dict[str, Any], path: Path) -> None:
    m = report["metrics"]
    print("\n=== FortyGuard thermal causality probe ===")
    print("Evidence:", report["evidence_class"])
    print("Unit:", report["unit_attestation"]["raw_unit"], "|", report["unit_attestation"]["source"])
    print(f"Local temperature spread: {m['local_temperature_spread_c']} °C")
    print(f"Documented derating bands represented: {m['documented_derating_band_count']}")
    print(f"Expected capacity spread: {m['capacity_spread_kw']} kW ({m['capacity_spread_pct_of_nameplate']}% nameplate)")
    print(f"Predeclared job cases with feasible-set change: {m['predeclared_job_cases_with_feasible_set_change']}")
    print("Verdict:", report["causality_verdict"])
    print("Report:", path)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Bounded FortyGuard -> EVSE thermal-capacity causality probe")
    p.add_argument("--mode", choices=["fixture", "live"], default="fixture")
    p.add_argument("--date", default="2024-07-05")
    p.add_argument("--hours", default="14:00,15:00,16:00")
    p.add_argument("--center-lat", type=float, default=33.4484)
    p.add_argument("--center-lon", type=float, default=-112.0740)
    p.add_argument("--afdc-radius-mi", type=float, default=4.0)
    p.add_argument("--afdc-limit", type=int, default=80)
    p.add_argument("--site-count", type=int, default=6)
    p.add_argument("--max-aoi-sq-mi", type=float, default=8.0)
    p.add_argument("--granularity", type=int, choices=[60, 80, 100], default=100)
    p.add_argument("--max-tcm-calls", type=int, default=3)
    p.add_argument("--output-dir", default="probe/output")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    if args.mode == "fixture":
        return run_fixture(output_dir)
    return run_live(args, output_dir)


if __name__ == "__main__":
    raise SystemExit(main())
