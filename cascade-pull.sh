#!/usr/bin/env bash
# SPDX-License-Identifier: CC-BY-SA-4.0
#
# cascade-pull.sh — WaterFall: concurrent ecosystem-wide git pull orchestrated by wateringHole
#
# WaterFall pattern (K-Derm model): Forgejo in the periplasm mediates
# between gate cytoplasms. Evolution cascades down; gates push back up.
# See WATERFALL_PATTERN.md for the full pattern spec.
#
# Reads ecosystem_manifest.toml and freshness.toml to determine which
# repos need updating, then concurrently pulls them with per-repo
# failure isolation.
#
# Usage:
#   cascade-pull.sh                        # Pull all repos (from default_source)
#   cascade-pull.sh --gate eastGate        # Pull only repos for this gate
#   cascade-pull.sh --category primals     # Pull only primals
#   cascade-pull.sh --source forgejo       # Pull from Forgejo (periplasm)
#   cascade-pull.sh --source github        # Pull from GitHub (extracellular)
#   cascade-pull.sh --source auto          # Try forgejo, fall back to origin
#   cascade-pull.sh --ensure-remotes       # Add forgejo remotes from manifest
#   cascade-pull.sh --check                # Report drift without pulling
#   cascade-pull.sh --dry-run              # Show what would be pulled
#   cascade-pull.sh --publish-freshness    # Update freshness.toml from live state
#   cascade-pull.sh --parallel 8           # Limit concurrent pulls (default: 8)
#
# Prerequisites:
#   - bash 4+, git, python3 (ships with all gates)
#
# Environment:
#   ECOPRIMALS_ROOT        Override workspace root (default: auto-detect)
#   CASCADE_PARALLEL       Override parallelism (default: 8)
#   CASCADE_SYNC_SOURCE    Override default pull source (github|forgejo|auto)
#   GATE_NAME              Override gate identity (default: auto-detect from hostname)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

resolve_eco_root() {
    if [[ -n "${ECOPRIMALS_ROOT:-}" ]]; then
        echo "$ECOPRIMALS_ROOT"
    elif [[ -d "$SCRIPT_DIR/../../primals" ]]; then
        cd "$SCRIPT_DIR/../.." && pwd
    else
        echo "ERROR: Cannot determine ecoPrimals root. Set ECOPRIMALS_ROOT." >&2
        exit 1
    fi
}

ECO_ROOT="$(resolve_eco_root)"
MANIFEST="$SCRIPT_DIR/ecosystem_manifest.toml"
FRESHNESS="$SCRIPT_DIR/freshness.toml"

GATE=""
CATEGORY=""
CHECK_ONLY=false
DRY_RUN=false
PUBLISH_FRESHNESS=false
ENSURE_REMOTES=false
PARALLEL="${CASCADE_PARALLEL:-8}"
SELF_UPDATE=true
SOURCE="${CASCADE_SYNC_SOURCE:-}"

resolve_gate_from_hostname() {
    local host
    host=$(hostname -s 2>/dev/null || echo "unknown")
    case "$host" in
        east*|eastgate*|eastGate*)   echo "eastGate" ;;
        iron*|irongate*|ironGate*)   echo "ironGate" ;;
        south*|southgate*|southGate*) echo "southGate" ;;
        biome*|biomegate*|biomeGate*) echo "biomeGate" ;;
        strand*|strandgate*|strandGate*) echo "strandGate" ;;
        golgi*|vps*)                  echo "golgiBody" ;;
        *)                            echo "" ;;
    esac
}

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --gate NAME          Pull only repos assigned to this gate"
    echo "  --gate auto          Auto-detect gate from hostname or GATE_NAME env"
    echo "  --category CAT       Filter by category (primal|spring|garden|infra|root)"
    echo "  --source SOURCE      Pull source: github|forgejo|auto (default: manifest)"
    echo "  --ensure-remotes     Add forgejo remotes from manifest (no pull)"
    echo "  --check              Report drift without pulling"
    echo "  --dry-run            Show what would be pulled"
    echo "  --publish-freshness  Update freshness.toml from current HEADs"
    echo "  --parallel N         Max concurrent pulls (default: 8)"
    echo "  --no-self-update     Skip pulling wateringHole first"
    echo "  --help               Show this help"
    echo ""
    echo "Environment:"
    echo "  GATE_NAME            Override gate identity (skip hostname auto-detection)"
    echo "  ECOPRIMALS_ROOT      Override workspace root (default: auto-detect)"
    echo "  CASCADE_PARALLEL     Override parallelism (default: 8)"
    echo "  CASCADE_SYNC_SOURCE  Override default pull source"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --gate)       GATE="$2"; shift 2 ;;
        --category)   CATEGORY="$2"; shift 2 ;;
        --source)     SOURCE="$2"; shift 2 ;;
        --ensure-remotes) ENSURE_REMOTES=true; shift ;;
        --check)      CHECK_ONLY=true; shift ;;
        --dry-run)    DRY_RUN=true; shift ;;
        --publish-freshness) PUBLISH_FRESHNESS=true; shift ;;
        --parallel)   PARALLEL="$2"; shift 2 ;;
        --no-self-update) SELF_UPDATE=false; shift ;;
        --help)       usage; exit 0 ;;
        -*)           echo "Unknown option: $1"; usage; exit 1 ;;
        *)            echo "Unknown argument: $1"; usage; exit 1 ;;
    esac
done

if [[ ! -f "$MANIFEST" ]]; then
    echo "ERROR: ecosystem_manifest.toml not found at $MANIFEST"
    exit 1
fi

# Resolve --gate auto: GATE_NAME env > hostname detection
if [[ "$GATE" == "auto" ]]; then
    if [[ -n "${GATE_NAME:-}" ]]; then
        GATE="$GATE_NAME"
    else
        GATE=$(resolve_gate_from_hostname)
    fi
    if [[ -z "$GATE" ]]; then
        echo "WARNING: --gate auto could not detect gate (set GATE_NAME env). Pulling all repos."
    else
        echo "Gate auto-detected: $GATE"
    fi
fi

# Sync source and Forgejo SSH are resolved after _py_toml_import is defined below.

# ─── TOML Parsing via Python ────────────────────────────────────────────────

_py_toml_import() {
    cat << 'PYIMPORT'
try:
    import tomllib
    def load_toml(path):
        with open(path, "rb") as f:
            return tomllib.load(f)
except ModuleNotFoundError:
    try:
        import tomli
        def load_toml(path):
            with open(path, "rb") as f:
                return tomli.load(f)
    except ModuleNotFoundError:
        import toml
        def load_toml(path):
            return toml.load(path)
PYIMPORT
}

# Resolve sync source: CLI --source > env CASCADE_SYNC_SOURCE > manifest [sync].default_source
if [[ -z "$SOURCE" ]]; then
    SOURCE=$(python3 -c "
$(_py_toml_import)
data = load_toml('$MANIFEST')
print(data.get('sync', {}).get('default_source', 'github'))
" 2>/dev/null || echo "github")
fi

FORGEJO_SSH=$(python3 -c "
$(_py_toml_import)
data = load_toml('$MANIFEST')
print(data.get('sync', {}).get('forgejo_ssh', 'ssh://git@git.primals.eco:2222'))
" 2>/dev/null || echo "ssh://git@git.primals.eco:2222")

parse_repos() {
    local manifest_arg="$MANIFEST"
    local gate_arg="$GATE"
    local category_arg="$CATEGORY"
    python3 -c "
$(_py_toml_import)

data = load_toml('$manifest_arg')

gate = '$gate_arg'
category = '$category_arg'

repos = data.get('repos', {})
gate_repos = None
if gate:
    gate_repos = set(data.get('gates', {}).get(gate, {}).get('repos', []))

for name in sorted(repos):
    info = repos[name]
    if gate_repos is not None and name not in gate_repos:
        continue
    cat = info.get('category', '')
    if category and cat != category:
        continue
    lp = info.get('local_path', '')
    mem = info.get('membrane', 'trailing-mirror')
    ss = info.get('sync_source', 'github')
    fj = info.get('forgejo_repo', '')
    print(f'{name}\t{lp}\t{mem}\t{ss}\t{fj}')
"
}

parse_freshness_heads() {
    if [[ ! -f "$FRESHNESS" ]]; then
        return
    fi
    local freshness_arg="$FRESHNESS"
    python3 -c "
$(_py_toml_import)

data = load_toml('$freshness_arg')

for name, head in data.get('heads', {}).items():
    print(f'{name}\t{head}')
"
}

# ─── Ensure Remotes (add forgejo remote to all repos) ────────────────────────

if $ENSURE_REMOTES; then
    echo "ensure-remotes — adding forgejo remotes from manifest"
    echo "  Forgejo SSH: $FORGEJO_SSH"
    echo ""

    added=0; skipped=0; missing=0

    while IFS=$'\t' read -r name local_path membrane sync_source forgejo_repo; do
        repo_dir="$ECO_ROOT/$local_path"

        if [[ ! -d "$repo_dir/.git" ]]; then
            printf "  [%-20s] MISSING  %s\n" "$name" "$repo_dir"
            missing=$((missing + 1))
            continue
        fi

        if [[ -z "$forgejo_repo" ]]; then
            printf "  [%-20s] NO-FORGEJO-REPO  (skipping)\n" "$name"
            skipped=$((skipped + 1))
            continue
        fi

        # Build forgejo URL from SSH base + repo path
        forgejo_url="${FORGEJO_SSH}/${forgejo_repo}.git"

        # Check if forgejo remote already exists
        existing_url=$(cd "$repo_dir" && git remote get-url forgejo 2>/dev/null || echo "")

        if [[ "$existing_url" == "$forgejo_url" ]]; then
            printf "  [%-20s] EXISTS   forgejo -> %s\n" "$name" "$forgejo_repo"
            skipped=$((skipped + 1))
        elif [[ -n "$existing_url" ]]; then
            (cd "$repo_dir" && git remote set-url forgejo "$forgejo_url" 2>/dev/null)
            printf "  [%-20s] UPDATED  forgejo -> %s\n" "$name" "$forgejo_repo"
            added=$((added + 1))
        else
            (cd "$repo_dir" && git remote add forgejo "$forgejo_url" 2>/dev/null)
            printf "  [%-20s] ADDED    forgejo -> %s\n" "$name" "$forgejo_repo"
            added=$((added + 1))
        fi
    done < <(parse_repos)

    echo ""
    echo "Summary: $added added/updated, $skipped already configured, $missing not on disk"
    exit 0
fi

# ─── Publish Freshness ───────────────────────────────────────────────────────

if $PUBLISH_FRESHNESS; then
    echo "Publishing freshness.toml from live HEADs..."

    wave_id=0
    ssot=""
    if [[ -f "$FRESHNESS" ]]; then
        wave_id=$(python3 -c "
$(_py_toml_import)
d = load_toml('$FRESHNESS')
print(d.get('wave', {}).get('id', 0))
" 2>/dev/null || echo "0")
        ssot=$(python3 -c "
$(_py_toml_import)
d = load_toml('$FRESHNESS')
print(d.get('wave', {}).get('ssot', ''))
" 2>/dev/null || echo "")
    fi

    {
        cat <<'HEADER'
# SPDX-License-Identifier: CC-BY-SA-4.0
#
# freshness.toml — Ecosystem state snapshot at wave publish time
#
# Authority: primalSpring coordination (published each wave)
# Consumed by: cascade-pull --check, s_ecosystem_freshness scenario
#
# Regenerate: cascade-pull --publish-freshness

HEADER
        echo "[wave]"
        echo "id = $wave_id"
        echo "date = \"$(date +%Y-%m-%d)\""
        [[ -n "$ssot" ]] && echo "ssot = \"$ssot\""
        echo "publisher = \"cascade-pull\""
        echo ""
        echo "[heads]"

        GATE="" CATEGORY="" parse_repos | while IFS=$'\t' read -r name local_path _membrane _ss _fj; do
            repo_dir="$ECO_ROOT/$local_path"
            if [[ -d "$repo_dir/.git" ]]; then
                head=$(cd "$repo_dir" && git rev-parse HEAD 2>/dev/null || echo "unknown")
                echo "$name = \"$head\""
            fi
        done
    } > "$FRESHNESS.tmp"
    mv "$FRESHNESS.tmp" "$FRESHNESS"
    echo "freshness.toml updated (wave $wave_id, $(date +%Y-%m-%d))."
    exit 0
fi

# ─── Remote resolution (must be defined before self-update uses it) ──────────

resolve_pull_remote() {
    local repo_dir="$1" source="$2"
    case "$source" in
        github)
            echo "origin"
            ;;
        forgejo|auto)
            if (cd "$repo_dir" && git remote get-url forgejo >/dev/null 2>&1); then
                echo "forgejo"
            else
                echo "origin"
            fi
            ;;
        *)
            echo "origin"
            ;;
    esac
}

# ─── Self-update wateringHole first ──────────────────────────────────────────

if $SELF_UPDATE && ! $CHECK_ONLY && ! $DRY_RUN; then
    wh_dir="$ECO_ROOT/infra/wateringHole"
    if [[ -d "$wh_dir/.git" ]]; then
        local_remote=$(resolve_pull_remote "$wh_dir" "$SOURCE")
        local_branch=$(cd "$wh_dir" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
        echo "=== Self-update: pulling wateringHole from $local_remote ==="
        if [[ "$local_remote" != "origin" ]]; then
            (cd "$wh_dir" && git pull --ff-only "$local_remote" "$local_branch" 2>&1) && echo "  wateringHole updated" || echo "  WARNING: wateringHole pull failed (continuing with local state)"
        else
            (cd "$wh_dir" && git pull --ff-only 2>&1) && echo "  wateringHole updated" || echo "  WARNING: wateringHole pull failed (continuing with local state)"
        fi
        echo ""
    fi
fi

# ─── Build freshness cache file ──────────────────────────────────────────────

TMPDIR_RESULTS=$(mktemp -d)
trap 'rm -rf "$TMPDIR_RESULTS"' EXIT

FRESHNESS_CACHE="$TMPDIR_RESULTS/.freshness_cache"
if [[ -f "$FRESHNESS" ]]; then
    parse_freshness_heads > "$FRESHNESS_CACHE"
else
    touch "$FRESHNESS_CACHE"
fi

echo "cascade-pull — $(date -Iseconds)"
echo "  Root:     $ECO_ROOT"
echo "  Source:   $SOURCE"
[[ -n "$GATE" ]] && echo "  Gate:     $GATE"
[[ -n "$CATEGORY" ]] && echo "  Category: $CATEGORY"
$CHECK_ONLY && echo "  Mode:     CHECK (no pulls)"
$DRY_RUN && echo "  Mode:     DRY-RUN"
echo ""

# ─── Worker function (called in subshells) ───────────────────────────────────

process_repo() {
    local name="$1" local_path="$2" membrane="$3" sync_source="$4" forgejo_repo="${5:-}"
    local repo_dir="$ECO_ROOT/$local_path"
    local result_file="$TMPDIR_RESULTS/$name"

    if [[ ! -d "$repo_dir/.git" ]]; then
        printf "  [%-20s] MISSING  %s\n" "$name" "$repo_dir"
        echo "MISSING" > "$result_file"
        return
    fi

    local local_head
    local_head=$(cd "$repo_dir" && git rev-parse HEAD 2>/dev/null)

    if $CHECK_ONLY; then
        local expected
        expected=$(grep "^${name}	" "$FRESHNESS_CACHE" 2>/dev/null | cut -f2 || echo "")
        if [[ -z "$expected" ]]; then
            printf "  [%-20s] NO-REF   (not in freshness.toml)\n" "$name"
            echo "SKIPPED" > "$result_file"
        elif [[ "$local_head" == "$expected" ]]; then
            printf "  [%-20s] CURRENT  %s\n" "$name" "${local_head:0:12}"
            echo "CURRENT" > "$result_file"
        else
            printf "  [%-20s] STALE    local=%s expected=%s\n" "$name" "${local_head:0:12}" "${expected:0:12}"
            echo "STALE" > "$result_file"
        fi
        return
    fi

    if $DRY_RUN; then
        local remote
        remote=$(resolve_pull_remote "$repo_dir" "$SOURCE")
        printf "  [%-20s] WOULD-PULL  %s (remote: %s)\n" "$name" "$repo_dir" "$remote"
        echo "DRYRUN" > "$result_file"
        return
    fi

    local remote
    remote=$(resolve_pull_remote "$repo_dir" "$SOURCE")

    local branch
    branch=$(cd "$repo_dir" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

    local pull_output pull_ok=true
    if [[ "$remote" != "origin" ]]; then
        pull_output=$(cd "$repo_dir" && git pull --ff-only "$remote" "$branch" 2>&1) || pull_ok=false
    else
        pull_output=$(cd "$repo_dir" && git pull --ff-only "$remote" 2>&1) || pull_ok=false
    fi

    if $pull_ok; then
        local new_head
        new_head=$(cd "$repo_dir" && git rev-parse HEAD 2>/dev/null)
        if [[ "$new_head" == "$local_head" ]]; then
            printf "  [%-20s] CURRENT  %s\n" "$name" "${local_head:0:12}"
            echo "CURRENT" > "$result_file"
        else
            printf "  [%-20s] UPDATED  %s -> %s\n" "$name" "${local_head:0:12}" "${new_head:0:12}"
            echo "UPDATED" > "$result_file"
        fi
    else
        if echo "$pull_output" | grep -q "Not possible to fast-forward\|cannot fast-forward"; then
            printf "  [%-20s] DIVERGED %s (needs manual merge)\n" "$name" "${local_head:0:12}"
            echo "DIVERGED" > "$result_file"
        else
            printf "  [%-20s] FAILED   %s\n" "$name" "$(echo "$pull_output" | head -1)"
            echo "FAILED" > "$result_file"
        fi
    fi
}

export -f process_repo resolve_pull_remote
export ECO_ROOT TMPDIR_RESULTS CHECK_ONLY DRY_RUN FRESHNESS FRESHNESS_CACHE SOURCE

# ─── Run in parallel using background jobs ───────────────────────────────────

active_jobs=0
while IFS=$'\t' read -r name local_path membrane sync_source forgejo_repo; do
    process_repo "$name" "$local_path" "$membrane" "$sync_source" "$forgejo_repo" &
    active_jobs=$((active_jobs + 1))
    if [[ $active_jobs -ge $PARALLEL ]]; then
        wait -n 2>/dev/null || true
        active_jobs=$((active_jobs - 1))
    fi
done < <(parse_repos)

wait

# ─── Tally results ───────────────────────────────────────────────────────────

UPDATED=0; CURRENT=0; SKIPPED=0; MISSING=0; DIVERGED=0; FAILED=0

for f in "$TMPDIR_RESULTS"/*; do
    [[ -f "$f" ]] || continue
    case "$(cat "$f")" in
        UPDATED)  UPDATED=$((UPDATED + 1)) ;;
        CURRENT)  CURRENT=$((CURRENT + 1)) ;;
        MISSING)  MISSING=$((MISSING + 1)) ;;
        FAILED)   FAILED=$((FAILED + 1)) ;;
        DIVERGED) DIVERGED=$((DIVERGED + 1)) ;;
        STALE)    FAILED=$((FAILED + 1)) ;;
        SKIPPED)  SKIPPED=$((SKIPPED + 1)) ;;
        DRYRUN)   SKIPPED=$((SKIPPED + 1)) ;;
    esac
done

echo ""
echo "Summary:"
echo "  Updated:  $UPDATED"
echo "  Current:  $CURRENT"
echo "  Skipped:  $SKIPPED"
echo "  Missing:  $MISSING"
echo "  Diverged: $DIVERGED"
echo "  Failed:   $FAILED"

if [[ $FAILED -gt 0 || $DIVERGED -gt 0 ]]; then
    exit 1
fi
