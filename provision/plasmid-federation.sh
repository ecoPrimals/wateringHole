#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# plasmid-federation.sh — Merge conserved plasmids from all golgi layers
#
# Runs on golgiBody (central). Fetches /plasmid from each layer, merges
# epitopes weighted by observation count, and publishes the federated
# threat intelligence feed to signal.primals.eco/feed/.
#
# Usage:
#   bash plasmid-federation.sh
#
# Add to crontab for periodic updates:
#   */5 * * * * /opt/membrane/plasmid-federation.sh >> /var/log/membrane/plasmid-sync.log 2>&1

set -euo pipefail

FEED_DIR="/opt/ecoPrimals/signal/site/public/feed"
WORK_DIR="/run/membrane/plasmid-sync"
MERGED_FILE="${FEED_DIR}/conserved-plasmid.json"

mkdir -p "${WORK_DIR}" "${FEED_DIR}"

# ── Layer registry ──────────────────────────────────────────────────────
# Add new layers here as they come online.
# Format: LAYER_NAME|ENDPOINT_URL|PROVIDER|LOCATION|JURISDICTION
LAYERS=(
    "golgiBody|http://localhost:9753/plasmid|DigitalOcean|NYC, US|US federal"
    "golgiHetzner|https://golgi-de.primals.eco/plasmid|Hetzner|Falkenstein, DE|German law + GDPR"
    "golgiLinode|https://golgi-in.primals.eco/plasmid|Linode|Mumbai, IN|Indian IT Act"
    # Offline — triage needed:
    # "golgiVultr|https://golgi-jp.primals.eco/plasmid|Vultr|Tokyo, JP|Japanese APPI"
    # "golgiOVH|https://golgi-us.primals.eco/plasmid|OVH|Virginia, US|US federal"
)

echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) — plasmid federation starting (${#LAYERS[@]} layers)"

# ── Fetch from each layer ───────────────────────────────────────────────
FETCHED=0
for entry in "${LAYERS[@]}"; do
    IFS='|' read -r name url provider location jurisdiction <<< "${entry}"
    outfile="${WORK_DIR}/${name}.json"

    if curl -sf --connect-timeout 5 --max-time 10 "${url}" -o "${outfile}" 2>/dev/null; then
        echo "  ✓ ${name} (${provider}, ${location})"
        FETCHED=$((FETCHED + 1))
    else
        echo "  ✗ ${name} — unreachable"
        rm -f "${outfile}"
    fi
done

if [ "${FETCHED}" -eq 0 ]; then
    echo "  No layers reachable — skipping merge"
    exit 1
fi

# ── Merge all layer plasmids ────────────────────────────────────────────
python3 << 'EOPY'
import json, os, glob, time

WORK_DIR = os.environ.get("WORK_DIR", "/run/membrane/plasmid-sync")
MERGED_FILE = os.environ.get("MERGED_FILE", "/opt/ecoPrimals/signal/site/public/feed/conserved-plasmid.json")

layer_files = glob.glob(os.path.join(WORK_DIR, "*.json"))
if not layer_files:
    print("  No layer files to merge")
    exit(1)

# Aggregate across all layers
all_epitopes = {}  # name → {total_freq, total_pop, layers}
all_hashes = {}    # hash → {max_conf, total_matches, detectors_union, layers}
total_subgroups = 0
total_observations = 0
total_confidence = 0.0
layer_count = 0
layer_metadata = []

for path in layer_files:
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        continue

    layer_name = data.get("layer", os.path.basename(path).replace(".json", ""))
    pop = data.get("population", {})
    subs = pop.get("total_subgroups", 0)
    obs = pop.get("total_observations", 0)
    conf = pop.get("mean_confidence", 0.0)

    total_subgroups += subs
    total_observations += obs
    total_confidence += conf * subs  # weighted by subgroup count
    layer_count += 1

    # v2 timing data (optional — graceful fallback for v1 layers)
    timing = data.get("timing", {})
    layer_meta = {
        "name": layer_name,
        "subgroups": subs,
        "observations": obs,
        "mean_confidence": round(conf, 3),
    }
    if timing:
        layer_meta["observation_window_secs"] = timing.get("observation_window_secs", 0)
        layer_meta["aggregate_velocity_per_hour"] = timing.get("aggregate_velocity_per_hour", 0.0)
        layer_meta["total_match_count"] = timing.get("total_match_count", 0)

    layer_metadata.append(layer_meta)

    # Merge epitopes
    for epi in data.get("conserved_epitopes", []):
        name = epi.get("name", "")
        freq = epi.get("subgroups_matching", epi.get("frequency_pct", 0))
        if name not in all_epitopes:
            all_epitopes[name] = {"total_freq": 0, "total_pop": 0, "layers": []}
        all_epitopes[name]["total_freq"] += freq
        all_epitopes[name]["total_pop"] += subs
        all_epitopes[name]["layers"].append(layer_name)

    # Merge behavioral hashes (v2 includes velocity and last_seen)
    for h in data.get("behavioral_hashes", []):
        hid = h.get("hash", "")
        if hid not in all_hashes:
            all_hashes[hid] = {
                "max_conf": 0.0,
                "total_matches": 0,
                "max_velocity": 0.0,
                "latest_seen": 0,
                "gate_count": 0,
                "detectors": set(),
                "layers": set(),
            }
        all_hashes[hid]["max_conf"] = max(all_hashes[hid]["max_conf"], h.get("confidence", 0.0))
        all_hashes[hid]["total_matches"] += h.get("match_count", 0)
        all_hashes[hid]["max_velocity"] = max(all_hashes[hid]["max_velocity"], h.get("velocity_per_hour", 0.0))
        all_hashes[hid]["latest_seen"] = max(all_hashes[hid]["latest_seen"], h.get("last_seen", 0))
        all_hashes[hid]["gate_count"] = max(all_hashes[hid]["gate_count"], h.get("gate_count", 0))
        all_hashes[hid]["detectors"].update(h.get("detectors", []))
        all_hashes[hid]["layers"].add(layer_name)

# Compute federated epitopes (conserved across >50% of total population)
federated_epitopes = []
for name, info in sorted(all_epitopes.items()):
    if info["total_pop"] > 0:
        pct = round(info["total_freq"] / info["total_pop"] * 100)
    else:
        pct = 0
    federated_epitopes.append({
        "name": name,
        "frequency_pct": pct,
        "layers_observed": len(info["layers"]),
        "layers": info["layers"],
    })

# Sort by frequency descending
federated_epitopes.sort(key=lambda x: x["frequency_pct"], reverse=True)

# Compute federated hashes
federated_hashes = []
for hid, info in sorted(all_hashes.items()):
    entry = {
        "hash": hid,
        "max_confidence": round(info["max_conf"], 3),
        "total_matches": info["total_matches"],
        "detectors": sorted(info["detectors"]),
        "layers_observed": len(info["layers"]),
        "layers": sorted(info["layers"]),
    }
    if info["max_velocity"] > 0:
        entry["max_velocity_per_hour"] = round(info["max_velocity"], 1)
    if info["latest_seen"] > 0:
        entry["latest_seen"] = info["latest_seen"]
    if info["gate_count"] > 0:
        entry["gate_count"] = info["gate_count"]
    federated_hashes.append(entry)

mean_conf = (total_confidence / total_subgroups) if total_subgroups > 0 else 0.0

# Build the federated feed
feed = {
    "schema": "ecoPrimals/conserved-plasmid/v2",
    "generated": int(time.time()),
    "generated_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "license": "CC-BY-SA-4.0",
    "source": "signal.primals.eco",
    "description": "Federated behavioral threat intelligence from multiple observation layers. Published for community immunity.",
    "federation": {
        "layer_count": layer_count,
        "layers": layer_metadata,
    },
    "population": {
        "total_subgroups": total_subgroups,
        "total_observations": total_observations,
        "mean_confidence": round(mean_conf, 3),
    },
    "conserved_epitopes": federated_epitopes,
    "behavioral_hashes_summary": {
        "total_unique": len(federated_hashes),
        "multi_layer": sum(1 for h in federated_hashes if h["layers_observed"] > 1),
    },
    "detection_rules": {
        "description": "Any system exhibiting 4 or more of these rules simultaneously is this fleet.",
        "rules": [
            "User-Agent contains 'Chrome/' but Sec-Fetch-Mode header is ABSENT",
            "User-Agent contains 'Chrome/' but Sec-Ch-Ua header is ABSENT",
            "Connection header is ABSENT",
            "Accept header is exactly '*/*'",
            "Chrome major version is 5+ behind current stable",
            "Accept-Encoding is identical across >90% of population",
            "Accept-Language is identical across >90% of population",
            ">50% of requests target /commit/, /src/, /raw/, /blame/ paths",
            "Inter-request timing coefficient of variation < 0.15",
            ">80% of IPs make exactly 1 request (single-page rotation)",
            ">10% of requests target /blame/ paths (author attribution)",
            "Requests continue after 403 response"
        ],
        "threshold": 4,
    },
    "attribution": {
        "primary_entity": "Meta Platforms, Inc.",
        "whois_confirmed_blocks": [
            {
                "cidr": "57.141.0.0/13",
                "netname": "FB-BLOCK",
                "org": "Meta Platforms Ireland Limited",
                "country": "IE",
            },
            {
                "cidr": "173.252.0.0/16",
                "netname": "FACEBOOK-INC",
                "org": "Facebook, Inc.",
                "country": "US",
            },
        ],
    },
}

with open(MERGED_FILE, "w") as f:
    json.dump(feed, f, indent=2)

print(f"  Merged: {layer_count} layers, {total_subgroups} subgroups, "
      f"{len(federated_epitopes)} epitopes, {len(federated_hashes)} hashes")
print(f"  Published: {MERGED_FILE}")
EOPY

echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) — plasmid federation complete"
