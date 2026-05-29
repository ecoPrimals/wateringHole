#!/usr/bin/env bash
# cascade-pull.sh — Gate-aware WaterFall sync
#
# Pulls only the repos your gate needs from the configured source
# (Forgejo or GitHub). Each gate has a profile that filters the
# ecosystem's 38 repos down to what's relevant.
#
# Usage:
#   cascade-pull.sh --gate auto                    # auto-detect gate, pull from default
#   cascade-pull.sh --gate biomeGate --source forgejo  # explicit gate + source
#   cascade-pull.sh --gate auto --dry-run          # show what would be pulled
#   cascade-pull.sh --ensure-remotes               # add forgejo remotes to all repos
#
# Gate auto-detection: uses hostname prefix (biome*, iron*, south*, strand*, east*)
# Override: set GATE_NAME=biomeGate in environment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# scripts/ is under infra/wateringHole/ — go up 3 levels to ecoPrimals root
ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-$(cd "$SCRIPT_DIR/../../.." 2>/dev/null && pwd)}"

if [[ ! -d "$ECOPRIMALS_ROOT/primals" ]]; then
    echo "ERROR: cannot find ecoPrimals root (tried $ECOPRIMALS_ROOT)"
    echo "Set ECOPRIMALS_ROOT=/path/to/ecoPrimals"
    exit 1
fi

# ── Gate profiles ──────────────────────────────────────────────────────
# Each gate pulls only the repos it needs.

declare -A GATE_PROFILES

# Core repos every gate needs (space-separated string for associative array values)
CORE="infra/wateringHole infra/plasmidBin primals/bearDog primals/songBird primals/toadStool primals/barraCuda primals/coralReef primals/nestGate primals/rhizoCrypt primals/loamSpine primals/sweetGrass primals/biomeOS primals/squirrel primals/petalTongue springs/primalSpring"

GATE_PROFILES[eastGate]="$CORE primals/bingoCube infra/agentReagents infra/benchScale infra/sporePrint infra/whitePaper springs/hotSpring springs/wetSpring springs/neuralSpring springs/healthSpring springs/groundSpring springs/airSpring springs/ludoSpring gardens/foundation gardens/projectNUCLEUS gardens/lithoSpore"

GATE_PROFILES[ironGate]="$CORE springs/healthSpring springs/ludoSpring infra/sporePrint gardens/foundation gardens/projectNUCLEUS gardens/lithoSpore"

GATE_PROFILES[southGate]="$CORE springs/wetSpring springs/neuralSpring gardens/foundation"

GATE_PROFILES[biomeGate]="$CORE springs/hotSpring infra/agentReagents gardens/foundation gardens/lithoSpore"

GATE_PROFILES[strandGate]="$CORE springs/hotSpring springs/wetSpring infra/agentReagents gardens/foundation gardens/lithoSpore gardens/projectNUCLEUS"

GATE_PROFILES[golgiBody]="infra/wateringHole infra/plasmidBin primals/bearDog primals/songBird primals/toadStool primals/barraCuda primals/coralReef primals/nestGate primals/rhizoCrypt primals/loamSpine primals/sweetGrass primals/biomeOS primals/squirrel primals/petalTongue primals/skunkBat gardens/cellMembrane gardens/projectNUCLEUS"

# ── Remote URL mapping ────────────────────────────────────────────────

forgejo_url() {
    local repo_path="$1"
    local name
    name=$(basename "$repo_path")

    case "$repo_path" in
        primals/*|infra/wateringHole|infra/plasmidBin|infra/sporePrint|infra/whitePaper)
            echo "ssh://git@git.primals.eco:2222/ecoPrimals/${name}.git" ;;
        infra/agentReagents|infra/benchScale)
            echo "ssh://git@git.primals.eco:2222/syntheticChemistry/${name}.git" ;;
        springs/*)
            echo "ssh://git@git.primals.eco:2222/syntheticChemistry/${name}.git" ;;
        gardens/*)
            echo "ssh://git@git.primals.eco:2222/sporeGarden/${name}.git" ;;
        *)
            echo "" ;;
    esac
}

# ── Gate detection ────────────────────────────────────────────────────

detect_gate() {
    if [[ -n "${GATE_NAME:-}" ]]; then
        echo "$GATE_NAME"
        return
    fi

    local hostname
    hostname=$(hostname -s 2>/dev/null || echo "unknown")

    case "$hostname" in
        biome*)  echo "biomeGate" ;;
        iron*)   echo "ironGate" ;;
        south*)  echo "southGate" ;;
        strand*) echo "strandGate" ;;
        east*)   echo "eastGate" ;;
        golgi*|membrane*|vps*) echo "golgiBody" ;;
        *)
            echo >&2 "WARNING: cannot auto-detect gate from hostname '$hostname'"
            echo >&2 "Set GATE_NAME=biomeGate (or your gate) in environment"
            echo "unknown"
            ;;
    esac
}

# ── Main ──────────────────────────────────────────────────────────────

GATE="auto"
SOURCE="${CASCADE_SYNC_SOURCE:-origin}"
DRY_RUN=false
ENSURE_REMOTES=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --gate)      GATE="$2"; shift 2 ;;
        --source)    SOURCE="$2"; shift 2 ;;
        --dry-run)   DRY_RUN=true; shift ;;
        --ensure-remotes) ENSURE_REMOTES=true; shift ;;
        -h|--help)
            echo "Usage: cascade-pull.sh [--gate auto|NAME] [--source forgejo|origin] [--dry-run] [--ensure-remotes]"
            exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ "$GATE" == "auto" ]]; then
    GATE=$(detect_gate)
fi

if $ENSURE_REMOTES; then
    echo "=== Ensuring forgejo remotes ==="
    for repo_path in ${GATE_PROFILES[eastGate]}; do
        local_path="$ECOPRIMALS_ROOT/$repo_path"
        [[ -d "$local_path/.git" ]] || continue
        url=$(forgejo_url "$repo_path")
        [[ -z "$url" ]] && continue
        if ! git -C "$local_path" remote get-url forgejo >/dev/null 2>&1; then
            git -C "$local_path" remote add forgejo "$url"
            echo "  added: $repo_path → $url"
        fi
    done
    echo "Done."
    exit 0
fi

PROFILE="${GATE_PROFILES[$GATE]:-}"
if [[ -z "$PROFILE" ]]; then
    echo "ERROR: unknown gate '$GATE'. Known: ${!GATE_PROFILES[*]}"
    exit 1
fi

# Count repos
read -ra REPOS <<< "$PROFILE"
TOTAL=${#REPOS[@]}

echo "=== WaterFall Cascade Pull ==="
echo "Gate:   $GATE"
echo "Source: $SOURCE"
echo "Repos:  $TOTAL"
echo ""

PULLED=0
SKIPPED=0
FAILED=0

for repo_path in "${REPOS[@]}"; do
    local_path="$ECOPRIMALS_ROOT/$repo_path"

    if [[ ! -d "$local_path/.git" ]]; then
        echo "  SKIP (not cloned): $repo_path"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    if $DRY_RUN; then
        echo "  WOULD PULL: $repo_path"
        PULLED=$((PULLED + 1))
        continue
    fi

    echo -n "  pull: $repo_path ... "
    if git -C "$local_path" pull "$SOURCE" --ff-only 2>/dev/null; then
        echo "ok"
        PULLED=$((PULLED + 1))
    else
        echo "FAILED (try manual merge)"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "=== Summary ==="
echo "Pulled: $PULLED / $TOTAL"
[[ $SKIPPED -gt 0 ]] && echo "Skipped (not cloned): $SKIPPED" || true
[[ $FAILED -gt 0 ]] && echo "Failed: $FAILED" || true
