#!/usr/bin/env bash
# cascade-pull.sh — Gate-aware WaterFall sync (manifest-driven)
#
# Reads gate profiles and repo metadata from ecosystem_manifest.toml
# instead of hardcoded bash arrays. The manifest is the single source
# of truth for which repos each gate needs and how to reach them.
#
# Usage:
#   cascade-pull.sh --gate auto                        # auto-detect gate, pull from default
#   cascade-pull.sh --gate biomeGate --source forgejo  # explicit gate + source
#   cascade-pull.sh --gate auto --source auto          # try forgejo, fall back to origin
#   cascade-pull.sh --gate auto --dry-run              # show what would be pulled
#   cascade-pull.sh --gate auto --check                # parity check (no pull, report drift)
#   cascade-pull.sh --gate auto --parallel 4           # concurrent pulls (4 workers)
#   cascade-pull.sh --gate auto --clone-missing        # clone repos not yet local
#   cascade-pull.sh --ensure-remotes                   # add forgejo remotes to all repos
#
# Gate identity resolution (priority order):
#   1. --gate <name>           explicit CLI argument
#   2. GATE_NAME env var       environment override
#   3. $ECOPRIMALS_ROOT/.gate  persistent identity file (one line: gate name)
#   4. hostname prefix match   fallback heuristic
#
# Manifest: ecosystem_manifest.toml in the same directory as this script.
#
# Coordination domain: waterFall (SYNC / autonomic)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/ecosystem_manifest.toml"

# Symlink-safe root detection: resolve symlinks before walking up
_resolve_root() {
    local start="$SCRIPT_DIR"
    if command -v realpath >/dev/null 2>&1; then
        start="$(realpath "$SCRIPT_DIR")"
    elif command -v readlink >/dev/null 2>&1; then
        start="$(readlink -f "$SCRIPT_DIR" 2>/dev/null || echo "$SCRIPT_DIR")"
    fi
    cd "$start/../../.." 2>/dev/null && pwd
}

ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-$(_resolve_root)}"

if [[ ! -d "$ECOPRIMALS_ROOT/primals" ]]; then
    echo "ERROR: cannot find ecoPrimals root (tried $ECOPRIMALS_ROOT)"
    echo "Hint: set ECOPRIMALS_ROOT=/path/to/ecoPrimals or create a symlink"
    exit 1
fi

if [[ ! -f "$MANIFEST" ]]; then
    echo "ERROR: ecosystem_manifest.toml not found at $MANIFEST"
    exit 1
fi

# ── Rust membrane binary (temporal sync delegation) ──────────────────
# When the compiled membrane binary is available, temporal operations
# delegate to Rust instead of inline bash. The DAG walks are identical;
# Rust gives typed output and structured JSON for downstream tooling.

MEMBRANE_BIN=""
for candidate in \
    "$ECOPRIMALS_ROOT/target/release/membrane" \
    "$ECOPRIMALS_ROOT/gardens/cellMembrane/target/release/membrane" \
    "$(command -v membrane 2>/dev/null || true)"; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
        MEMBRANE_BIN="$candidate"
        break
    fi
done

# ── Manifest reader (Python 3.11+ tomllib, fallback to tomli) ────────

_py_read_manifest() {
    python3 -c "
import sys, json
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print('ERROR: need Python 3.11+ (tomllib) or pip install tomli', file=sys.stderr)
        sys.exit(1)

with open('$MANIFEST', 'rb') as f:
    m = tomllib.load(f)

cmd = sys.argv[1]

if cmd == 'gate_repos':
    gate = sys.argv[2]
    gates = m.get('gates', {})
    if gate not in gates:
        known = ', '.join(sorted(gates.keys()))
        print(f'ERROR: unknown gate \"{gate}\". Known: {known}', file=sys.stderr)
        sys.exit(1)
    for repo_key in gates[gate].get('repos', []):
        repo = m.get('repos', {}).get(repo_key, {})
        local_path = repo.get('local_path', '')
        if local_path:
            print(local_path)

elif cmd == 'known_gates':
    for g in sorted(m.get('gates', {}).keys()):
        print(g)

elif cmd == 'forgejo_url':
    repo_path = sys.argv[2]
    forgejo_ssh = m.get('sync', {}).get('forgejo_ssh', 'ssh://git@git.primals.eco:2222')
    for key, repo in m.get('repos', {}).items():
        if repo.get('local_path') == repo_path:
            fr = repo.get('forgejo_repo', '')
            if fr:
                print(f'{forgejo_ssh}/{fr}.git')
            break

elif cmd == 'github_url':
    repo_path = sys.argv[2]
    for key, repo in m.get('repos', {}).items():
        if repo.get('local_path') == repo_path:
            gr = repo.get('github_repo', '')
            if gr:
                print(f'https://github.com/{gr}.git')
            break

elif cmd == 'clone_url':
    repo_path = sys.argv[2]
    source = sys.argv[3] if len(sys.argv) > 3 else 'auto'
    forgejo_ssh = m.get('sync', {}).get('forgejo_ssh', 'ssh://git@git.primals.eco:2222')
    for key, repo in m.get('repos', {}).items():
        if repo.get('local_path') == repo_path:
            fr = repo.get('forgejo_repo', '')
            gr = repo.get('github_repo', '')
            if source == 'forgejo' and fr:
                print(f'{forgejo_ssh}/{fr}.git')
            elif source == 'origin' and gr:
                print(f'https://github.com/{gr}.git')
            elif source == 'auto':
                if fr:
                    print(f'{forgejo_ssh}/{fr}.git')
                elif gr:
                    print(f'https://github.com/{gr}.git')
            break

elif cmd == 'all_repos':
    for key, repo in m.get('repos', {}).items():
        lp = repo.get('local_path', '')
        if lp:
            print(lp)

elif cmd == 'repo_info':
    repo_path = sys.argv[2]
    for key, repo in m.get('repos', {}).items():
        if repo.get('local_path') == repo_path:
            info = {
                'key': key,
                'local_path': repo.get('local_path', ''),
                'forgejo_repo': repo.get('forgejo_repo', ''),
                'github_repo': repo.get('github_repo', ''),
                'sync_priority': repo.get('sync_priority', 'standard'),
                'default_branch': repo.get('default_branch', m.get('sync', {}).get('default_branch', 'main')),
            }
            print(json.dumps(info))
            break

elif cmd == 'manifest_version':
    meta = m.get('meta', {})
    print(f\"v{meta.get('version', '?')} wave {meta.get('wave', '?')} ({meta.get('total_repos', '?')} repos)\")
" "$@"
}

# ── Gate detection ────────────────────────────────────────────────────
# Priority: GATE_NAME env > .gate file > hostname heuristic

detect_gate() {
    if [[ -n "${GATE_NAME:-}" ]]; then
        echo "$GATE_NAME"
        return
    fi

    # .gate identity file — one line containing the gate name
    local gate_file="$ECOPRIMALS_ROOT/.gate"
    if [[ -f "$gate_file" ]]; then
        local gate_id
        gate_id=$(<"$gate_file")
        gate_id="${gate_id%%[[:space:]]}"  # trim whitespace
        if [[ -n "$gate_id" ]]; then
            echo "$gate_id"
            return
        fi
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
        flock*)  echo "flockGate" ;;
        swift*)  echo "swiftGate" ;;
        west*)   echo "westGate" ;;
        kin*)    echo "kinGate" ;;
        *)
            echo >&2 "WARNING: cannot auto-detect gate from hostname '$hostname'"
            echo >&2 "Fix: echo 'eastGate' > $ECOPRIMALS_ROOT/.gate"
            echo >&2 "  or: export GATE_NAME=eastGate"
            echo "unknown"
            ;;
    esac
}

# ── Clone missing repo ───────────────────────────────────────────────

clone_repo() {
    local repo_path="$1"
    local source="$2"
    local local_path="$ECOPRIMALS_ROOT/$repo_path"
    local parent_dir
    parent_dir=$(dirname "$local_path")

    local clone_url
    clone_url=$(_py_read_manifest clone_url "$repo_path" "$source")

    if [[ -z "$clone_url" ]]; then
        echo "CLONE_FAIL $repo_path (no URL in manifest)"
        return 1
    fi

    mkdir -p "$parent_dir"

    if git clone "$clone_url" "$local_path" 2>/dev/null; then
        # Add the other remote if we cloned from one source
        local forgejo_url github_url
        forgejo_url=$(_py_read_manifest forgejo_url "$repo_path")
        github_url=$(_py_read_manifest github_url "$repo_path")

        if [[ "$clone_url" == *"github.com"* ]] && [[ -n "$forgejo_url" ]]; then
            git -C "$local_path" remote add forgejo "$forgejo_url" 2>/dev/null || true
        elif [[ "$clone_url" == *"git.primals.eco"* ]] && [[ -n "$github_url" ]]; then
            git -C "$local_path" remote add origin "$github_url" 2>/dev/null || true
            git -C "$local_path" remote rename origin github 2>/dev/null || true
            git -C "$local_path" remote rename forgejo origin 2>/dev/null || true
        fi

        echo "CLONED $repo_path ($clone_url)"
        return 0
    else
        echo "CLONE_FAIL $repo_path ($clone_url)"
        return 1
    fi
}

# ── Parity check ──────────────────────────────────────────────────────

check_parity() {
    local repo_path="$1"
    local local_path="$ECOPRIMALS_ROOT/$repo_path"

    [[ -d "$local_path/.git" ]] || { echo "MISSING"; return; }

    local local_head
    local_head=$(git -C "$local_path" rev-parse HEAD 2>/dev/null || echo "none")

    local remote_head="unknown"
    local branch
    branch=$(git -C "$local_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

    if git -C "$local_path" remote get-url forgejo >/dev/null 2>&1; then
        git -C "$local_path" fetch forgejo "$branch" --quiet 2>/dev/null || true
        remote_head=$(git -C "$local_path" rev-parse "forgejo/$branch" 2>/dev/null || echo "unknown")
    elif git -C "$local_path" remote get-url origin >/dev/null 2>&1; then
        git -C "$local_path" fetch origin "$branch" --quiet 2>/dev/null || true
        remote_head=$(git -C "$local_path" rev-parse "origin/$branch" 2>/dev/null || echo "unknown")
    fi

    if [[ "$local_head" == "$remote_head" ]]; then
        echo "OK"
    elif [[ "$remote_head" == "unknown" ]]; then
        echo "NO_REMOTE"
    else
        local behind ahead
        behind=$(git -C "$local_path" rev-list --count "$local_head..$remote_head" 2>/dev/null || echo "?")
        ahead=$(git -C "$local_path" rev-list --count "$remote_head..$local_head" 2>/dev/null || echo "?")
        echo "DRIFT(behind=$behind,ahead=$ahead)"
    fi
}

# ── Temporal sync (waterFall Phase 1) ─────────────────────────────────
# Fetch ALL remotes, measure temporal position, classify convergence,
# pull from leader, push to followers. The DAG is the only clock.

temporal_check_repo() {
    local repo_path="$1"
    local local_path="$ECOPRIMALS_ROOT/$repo_path"

    [[ -d "$local_path/.git" ]] || { echo "MISSING"; return; }

    local branch
    branch=$(git -C "$local_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

    git -C "$local_path" fetch --all --quiet 2>/dev/null || true

    local remotes
    remotes=$(git -C "$local_path" remote 2>/dev/null)
    [[ -z "$remotes" ]] && { echo "NO_REMOTE"; return; }

    local matrix=""
    local has_leader=false
    local leader_remote=""
    local leader_behind=0
    local has_followers=false
    local all_parity=true

    for remote in $remotes; do
        local remote_ref="$remote/$branch"
        git -C "$local_path" rev-parse "$remote_ref" >/dev/null 2>&1 || continue

        local ahead behind
        ahead=$(git -C "$local_path" rev-list --count "$remote_ref..HEAD" 2>/dev/null || echo "0")
        behind=$(git -C "$local_path" rev-list --count "HEAD..$remote_ref" 2>/dev/null || echo "0")

        matrix="$matrix $remote(+$ahead,-$behind)"

        if [[ "$behind" -gt 0 ]]; then
            all_parity=false
            if [[ "$behind" -gt "$leader_behind" ]]; then
                leader_behind=$behind
                leader_remote=$remote
                has_leader=true
            fi
        fi
        if [[ "$ahead" -gt 0 ]]; then
            all_parity=false
            has_followers=true
        fi
    done

    if $all_parity; then
        echo "PARITY $matrix"
        return
    fi

    # Divergence: check if multiple remotes are ahead of each other
    local diverge_count=0
    for remote in $remotes; do
        local remote_ref="$remote/$branch"
        git -C "$local_path" rev-parse "$remote_ref" >/dev/null 2>&1 || continue

        local other_ahead=0
        for other in $remotes; do
            [[ "$other" == "$remote" ]] && continue
            local other_ref="$other/$branch"
            git -C "$local_path" rev-parse "$other_ref" >/dev/null 2>&1 || continue
            local cross
            cross=$(git -C "$local_path" rev-list --count "$other_ref..$remote_ref" 2>/dev/null || echo "0")
            if [[ "$cross" -gt 0 ]]; then
                other_ahead=$((other_ahead + 1))
            fi
        done
        if [[ "$other_ahead" -gt 0 ]]; then
            diverge_count=$((diverge_count + 1))
        fi
    done

    if [[ "$diverge_count" -gt 1 ]]; then
        echo "DIVERGE $matrix"
    elif $has_leader; then
        echo "CONVERGE $matrix -> pull $leader_remote"
    elif $has_followers; then
        echo "CONVERGE $matrix -> push followers"
    else
        echo "PARITY $matrix"
    fi
}

temporal_sync_repo() {
    local repo_path="$1"
    local local_path="$ECOPRIMALS_ROOT/$repo_path"

    [[ -d "$local_path/.git" ]] || { echo "SKIP $repo_path (not cloned)"; return 1; }

    local branch
    branch=$(git -C "$local_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

    git -C "$local_path" fetch --all --quiet 2>/dev/null || true

    local check_result
    check_result=$(temporal_check_repo "$repo_path")
    local pattern
    pattern=$(echo "$check_result" | awk '{print $1}')

    local action
    action=$(echo "$check_result" | sed -n 's/.*-> //p')

    case "$pattern" in
        PARITY)
            echo "OK $repo_path (parity)"
            return 0
            ;;
        CONVERGE)
            local remotes
            remotes=$(git -C "$local_path" remote 2>/dev/null)

            if [[ "$action" == "push followers" ]]; then
                local pushed=""
                for remote in $remotes; do
                    local remote_ref="$remote/$branch"
                    git -C "$local_path" rev-parse "$remote_ref" >/dev/null 2>&1 || continue
                    local ahead
                    ahead=$(git -C "$local_path" rev-list --count "$remote_ref..HEAD" 2>/dev/null || echo "0")
                    if [[ "$ahead" -gt 0 ]]; then
                        if git -C "$local_path" push "$remote" "$branch" --quiet 2>/dev/null; then
                            pushed="$pushed $remote"
                        fi
                    fi
                done
                if [[ -n "$pushed" ]]; then
                    echo "OK $repo_path (push$pushed)"
                else
                    echo "OK $repo_path (parity — push failed)"
                fi
                return 0
            fi

            local leader
            leader=$(echo "$action" | sed 's/pull //')
            if git -C "$local_path" pull "$leader" "$branch" --ff-only --quiet 2>/dev/null; then
                local pushed=""
                for remote in $remotes; do
                    [[ "$remote" == "$leader" ]] && continue
                    local remote_ref="$remote/$branch"
                    git -C "$local_path" rev-parse "$remote_ref" >/dev/null 2>&1 || continue
                    local ahead
                    ahead=$(git -C "$local_path" rev-list --count "$remote_ref..HEAD" 2>/dev/null || echo "0")
                    if [[ "$ahead" -gt 0 ]]; then
                        if git -C "$local_path" push "$remote" "$branch" --quiet 2>/dev/null; then
                            pushed="$pushed $remote"
                        fi
                    fi
                done
                if [[ -n "$pushed" ]]; then
                    echo "OK $repo_path (pull $leader, push$pushed)"
                else
                    echo "OK $repo_path (pull $leader)"
                fi
                return 0
            else
                echo "FAIL $repo_path (pull $leader failed — ff-only)"
                return 1
            fi
            ;;
        DIVERGE)
            echo "DIVERGE $repo_path — $check_result"
            return 1
            ;;
        MISSING)
            echo "SKIP $repo_path (not cloned)"
            return 1
            ;;
        *)
            echo "UNKNOWN $repo_path — $check_result"
            return 1
            ;;
    esac
}

# ── Parallel pull worker ──────────────────────────────────────────────

pull_one_repo() {
    local repo_path="$1"
    local source="$2"
    local local_path="$ECOPRIMALS_ROOT/$repo_path"

    if [[ ! -d "$local_path/.git" ]]; then
        echo "SKIP $repo_path"
        return 1
    fi

    local branch
    branch=$(git -C "$local_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

    local pull_source="$source"
    if [[ "$source" == "auto" ]]; then
        if git -C "$local_path" remote get-url forgejo >/dev/null 2>&1; then
            pull_source="forgejo"
        else
            pull_source="origin"
        fi
    fi

    if git -C "$local_path" pull "$pull_source" "$branch" --ff-only 2>/dev/null; then
        echo "OK $repo_path ($pull_source)"
        return 0
    else
        echo "FAIL $repo_path ($pull_source)"
        return 1
    fi
}

# ── Main ──────────────────────────────────────────────────────────────

GATE="auto"
# Resolve default source from manifest [sync].default_source, env, or fallback
_manifest_default_source() {
    python3 -c "
import sys
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        sys.exit(1)
with open('$MANIFEST', 'rb') as f:
    m = tomllib.load(f)
print(m.get('sync', {}).get('default_source', 'origin'))
" 2>/dev/null || echo "origin"
}
SOURCE="${CASCADE_SYNC_SOURCE:-$(_manifest_default_source)}"
DRY_RUN=false
ENSURE_REMOTES=false
CHECK_PARITY=false
CLONE_MISSING=false
PARALLEL=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        --gate)      GATE="$2"; shift 2 ;;
        --source)    SOURCE="$2"; shift 2 ;;
        --dry-run)   DRY_RUN=true; shift ;;
        --ensure-remotes) ENSURE_REMOTES=true; shift ;;
        --check)     CHECK_PARITY=true; shift ;;
        --clone-missing) CLONE_MISSING=true; shift ;;
        --parallel)  PARALLEL="$2"; shift 2 ;;
        -h|--help)
            cat <<'USAGE'
Usage: cascade-pull.sh [OPTIONS]

Options:
  --gate NAME|auto    Gate name or 'auto' for identity detection (default: auto)
  --source NAME       Pull source: origin | forgejo | auto | temporal (default: origin)
                      'auto' tries forgejo first, falls back to origin
                      'temporal' fetches all remotes, pulls from leader, pushes to followers
  --dry-run           Show what would be pulled without pulling
  --check             Parity check: fetch + compare without pulling
                      With --source temporal: shows per-remote temporal position matrix
  --clone-missing     Clone repos that aren't local yet (uses manifest URLs)
  --parallel N        Number of concurrent pull workers (default: 1)
  --ensure-remotes    Add forgejo remotes to all repos in gate profile
  -h, --help          Show this help

Gate Identity (priority order):
  1. --gate <name>            CLI argument
  2. GATE_NAME env var        Environment override
  3. $ECOPRIMALS_ROOT/.gate   Persistent identity file (one line: gate name)
  4. hostname prefix match    Fallback heuristic

  Create .gate file:  echo 'eastGate' > $ECOPRIMALS_ROOT/.gate

Environment:
  GATE_NAME            Override gate auto-detection
  CASCADE_SYNC_SOURCE  Default pull source (overridden by --source)
  ECOPRIMALS_ROOT      Path to ecoPrimals workspace root

Manifest: ecosystem_manifest.toml (same directory as this script)
Coordination domain: waterFall (SYNC / autonomic)
USAGE
            exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

MANIFEST_VER=$(_py_read_manifest manifest_version)
echo "=== WaterFall Cascade Pull ==="
echo "Manifest: $MANIFEST_VER"

if [[ "$GATE" == "auto" ]]; then
    GATE=$(detect_gate)
fi

# ── Ensure remotes mode ───────────────────────────────────────────────

if $ENSURE_REMOTES; then
    echo "Gate:    $GATE"
    echo "Mode:    ensure-remotes"
    echo ""
    ADDED=0
    EXISTED=0
    while IFS= read -r repo_path; do
        local_path="$ECOPRIMALS_ROOT/$repo_path"
        [[ -d "$local_path/.git" ]] || continue
        url=$(_py_read_manifest forgejo_url "$repo_path")
        [[ -z "$url" ]] && continue
        if ! git -C "$local_path" remote get-url forgejo >/dev/null 2>&1; then
            git -C "$local_path" remote add forgejo "$url"
            echo "  added: $repo_path → $url"
            ADDED=$((ADDED + 1))
        else
            EXISTED=$((EXISTED + 1))
        fi
    done < <(_py_read_manifest gate_repos "$GATE")
    echo ""
    echo "Added: $ADDED, Already existed: $EXISTED"
    exit 0
fi

# ── Load gate profile from manifest ──────────────────────────────────

mapfile -t REPOS < <(_py_read_manifest gate_repos "$GATE")
TOTAL=${#REPOS[@]}

echo "Gate:    $GATE"
echo "Source:  $SOURCE"
echo "Repos:   $TOTAL"
if [[ "$PARALLEL" -gt 1 ]]; then
    echo "Workers: $PARALLEL"
fi
if $CLONE_MISSING; then
    echo "Mode:    clone-missing enabled"
fi
echo ""

# ── Parity check mode ────────────────────────────────────────────────

if $CHECK_PARITY; then
    if [[ "$SOURCE" == "temporal" ]]; then
        if [[ -n "$MEMBRANE_BIN" ]]; then
            echo "--- Temporal Position Matrix (Rust membrane) ---"
            echo ""
            ECOPRIMALS_ROOT="$ECOPRIMALS_ROOT" "$MEMBRANE_BIN" temporal.check "${REPOS[@]}" 2>&1 | sed '/^\[$/,$d'
            echo ""
        else
            echo "--- Temporal Position Matrix (fetch all, no pull) ---"
            echo ""
            OK=0
            CONVERGE=0
            DIVERGE_COUNT=0
            MISSING=0
            NO_REMOTE=0
            for repo_path in "${REPOS[@]}"; do
                status=$(temporal_check_repo "$repo_path")
                pattern=$(echo "$status" | awk '{print $1}')
                detail=$(echo "$status" | cut -d' ' -f2-)
                case "$pattern" in
                    PARITY)   OK=$((OK + 1));              printf "  %-35s PARITY    %s\n" "$repo_path" "$detail" ;;
                    CONVERGE) CONVERGE=$((CONVERGE + 1));  printf "  %-35s CONVERGE  %s\n" "$repo_path" "$detail" ;;
                    DIVERGE)  DIVERGE_COUNT=$((DIVERGE_COUNT + 1)); printf "  %-35s DIVERGE   %s\n" "$repo_path" "$detail" ;;
                    MISSING)  MISSING=$((MISSING + 1));    printf "  %-35s MISSING\n" "$repo_path" ;;
                    NO_REMOTE) NO_REMOTE=$((NO_REMOTE + 1)); printf "  %-35s NO_REMOTE\n" "$repo_path" ;;
                    *)        printf "  %-35s %s\n" "$repo_path" "$status" ;;
                esac
            done
            echo ""
            echo "=== Temporal Summary ==="
            echo "Parity:     $OK / $TOTAL"
            [[ $CONVERGE -gt 0 ]]      && echo "Converge:   $CONVERGE (would pull leader, push followers)" || true
            [[ $DIVERGE_COUNT -gt 0 ]] && echo "Diverge:    $DIVERGE_COUNT (needs human review)"           || true
            [[ $MISSING -gt 0 ]]       && echo "Not cloned: $MISSING"                                      || true
            [[ $NO_REMOTE -gt 0 ]]     && echo "No remote:  $NO_REMOTE"                                    || true
        fi
    else
        echo "--- Parity Check (fetch + compare, no pull) ---"
        echo ""
        OK=0
        DRIFT=0
        MISSING=0
        NO_REMOTE=0
        for repo_path in "${REPOS[@]}"; do
            status=$(check_parity "$repo_path")
            case "$status" in
                OK)        OK=$((OK + 1));        printf "  %-40s %s\n" "$repo_path" "✓" ;;
                MISSING)   MISSING=$((MISSING + 1));  printf "  %-40s %s\n" "$repo_path" "NOT CLONED" ;;
                NO_REMOTE) NO_REMOTE=$((NO_REMOTE + 1)); printf "  %-40s %s\n" "$repo_path" "NO REMOTE" ;;
                *)         DRIFT=$((DRIFT + 1));     printf "  %-40s %s\n" "$repo_path" "$status" ;;
            esac
        done
        echo ""
        echo "=== Parity Summary ==="
        echo "In sync:    $OK / $TOTAL"
        [[ $DRIFT -gt 0 ]]     && echo "Drifted:    $DRIFT"     || true
        [[ $MISSING -gt 0 ]]   && echo "Not cloned: $MISSING (use --clone-missing to fix)" || true
        [[ $NO_REMOTE -gt 0 ]] && echo "No remote:  $NO_REMOTE" || true
    fi
    exit 0
fi

# ── Pull mode ─────────────────────────────────────────────────────────

PULLED=0
SKIPPED=0
FAILED=0
CLONED=0
MERGE_CONFLICTS=()
DIVERGED_REPOS=()

# ── Temporal pull mode ────────────────────────────────────────────────

if [[ "$SOURCE" == "temporal" ]]; then
    if [[ -n "$MEMBRANE_BIN" ]]; then
        echo "--- Temporal Sync (Rust membrane) ---"
        echo ""
        ECOPRIMALS_ROOT="$ECOPRIMALS_ROOT" "$MEMBRANE_BIN" temporal.sync "${REPOS[@]}" 2>&1 | sed '/^\[$/,$d'
        echo ""
        exit 0
    fi

    echo "--- Temporal Sync (fetch all, pull leader, push followers) ---"
    echo ""
    for repo_path in "${REPOS[@]}"; do
        local_path="$ECOPRIMALS_ROOT/$repo_path"

        if [[ ! -d "$local_path/.git" ]]; then
            if $CLONE_MISSING; then
                echo -n "  clone: $repo_path ... "
                result=$(clone_repo "$repo_path" "auto")
                case "$result" in
                    CLONED*) echo "ok"; CLONED=$((CLONED + 1)) ;;
                    *)       echo "FAILED"; SKIPPED=$((SKIPPED + 1)) ;;
                esac
            else
                echo "  SKIP (not cloned): $repo_path"
                SKIPPED=$((SKIPPED + 1))
            fi
            continue
        fi

        if $DRY_RUN; then
            status=$(temporal_check_repo "$repo_path")
            pattern=$(echo "$status" | awk '{print $1}')
            printf "  %-35s %s\n" "$repo_path" "$status"
            PULLED=$((PULLED + 1))
            continue
        fi

        echo -n "  sync: $repo_path ... "
        result=$(temporal_sync_repo "$repo_path" 2>&1) || true
        pattern=$(echo "$result" | head -1 | awk '{print $1}')
        detail=$(echo "$result" | head -1 | cut -d' ' -f2-)

        case "$pattern" in
            OK)      echo "$detail"; PULLED=$((PULLED + 1)) ;;
            DIVERGE) echo "DIVERGE — needs human review"; DIVERGED_REPOS+=("$repo_path"); FAILED=$((FAILED + 1)) ;;
            SKIP)    echo "$detail"; SKIPPED=$((SKIPPED + 1)) ;;
            *)       echo "$detail"; FAILED=$((FAILED + 1)) ;;
        esac
    done

    echo ""
    echo "=== Temporal Sync Summary ==="
    echo "Synced:     $PULLED / $TOTAL"
    [[ $CLONED -gt 0 ]]  && echo "Cloned:     $CLONED" || true
    [[ $SKIPPED -gt 0 ]] && echo "Skipped:    $SKIPPED" || true
    [[ $FAILED -gt 0 ]]  && echo "Failed:     $FAILED" || true

    if [[ ${#DIVERGED_REPOS[@]} -gt 0 ]]; then
        echo ""
        echo "=== Diverged Repos (quorumSignal review needed) ==="
        echo "These repos have unique commits on multiple remotes."
        echo "Resolve manually, then re-run temporal sync."
        for dr in "${DIVERGED_REPOS[@]}"; do
            echo "  $dr"
        done
    fi

    if [[ $SKIPPED -gt 0 ]] && ! $CLONE_MISSING; then
        echo ""
        echo "Hint: re-run with --clone-missing to clone skipped repos from manifest"
    fi
    exit 0
fi

# ── Legacy pull mode (origin/forgejo/auto) ────────────────────────────

if [[ "$PARALLEL" -gt 1 ]] && command -v xargs >/dev/null 2>&1; then
    export -f pull_one_repo
    export ECOPRIMALS_ROOT SOURCE

    TMPOUT=$(mktemp)
    trap 'rm -f "$TMPOUT"' EXIT

    printf '%s\n' "${REPOS[@]}" | \
        xargs -P "$PARALLEL" -I {} bash -c 'pull_one_repo "$@"' _ {} "$SOURCE" \
        >> "$TMPOUT" 2>&1 || true

    while IFS= read -r line; do
        case "$line" in
            OK*)   PULLED=$((PULLED + 1)); echo "  $line" ;;
            SKIP*) SKIPPED=$((SKIPPED + 1)); echo "  $line" ;;
            FAIL*) FAILED=$((FAILED + 1)); echo "  $line" ;;
        esac
    done < "$TMPOUT"
else
    for repo_path in "${REPOS[@]}"; do
        local_path="$ECOPRIMALS_ROOT/$repo_path"

        if [[ ! -d "$local_path/.git" ]]; then
            if $CLONE_MISSING; then
                echo -n "  clone: $repo_path ... "
                result=$(clone_repo "$repo_path" "$SOURCE")
                case "$result" in
                    CLONED*)
                        echo "ok"
                        CLONED=$((CLONED + 1))
                        ;;
                    *)
                        echo "FAILED"
                        SKIPPED=$((SKIPPED + 1))
                        ;;
                esac
            else
                echo "  SKIP (not cloned): $repo_path"
                SKIPPED=$((SKIPPED + 1))
            fi
            continue
        fi

        if $DRY_RUN; then
            echo "  WOULD PULL: $repo_path"
            PULLED=$((PULLED + 1))
            continue
        fi

        echo -n "  pull: $repo_path ... "
        branch=$(git -C "$local_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

        pull_source="$SOURCE"
        if [[ "$SOURCE" == "auto" ]]; then
            if git -C "$local_path" remote get-url forgejo >/dev/null 2>&1; then
                pull_source="forgejo"
            else
                pull_source="origin"
            fi
        fi

        pull_output=$(git -C "$local_path" pull "$pull_source" "$branch" --ff-only 2>&1) && {
            echo "ok ($pull_source)"
            PULLED=$((PULLED + 1))
        } || {
            if echo "$pull_output" | grep -q "Not possible to fast-forward"; then
                echo "MERGE NEEDED ($pull_source)"
                MERGE_CONFLICTS+=("$repo_path")
            elif echo "$pull_output" | grep -q "fix conflicts"; then
                echo "CONFLICT ($pull_source)"
                MERGE_CONFLICTS+=("$repo_path")
            else
                echo "FAILED ($pull_source)"
            fi
            FAILED=$((FAILED + 1))
        }
    done
fi

echo ""
echo "=== Summary ==="
echo "Pulled: $PULLED / $TOTAL"
[[ $CLONED -gt 0 ]]  && echo "Cloned: $CLONED" || true
[[ $SKIPPED -gt 0 ]] && echo "Skipped (not cloned): $SKIPPED" || true
[[ $FAILED -gt 0 ]]  && echo "Failed: $FAILED" || true

if [[ ${#MERGE_CONFLICTS[@]} -gt 0 ]]; then
    echo ""
    echo "=== Merge Conflicts ==="
    echo "These repos have local changes that diverge from remote."
    echo "For each, choose one of:"
    echo "  1. Commit local work, then:  git -C <path> pull --rebase <source> <branch>"
    echo "  2. Stash and pull:           git -C <path> stash && git -C <path> pull --ff-only <source> <branch>"
    echo "  3. Force-sync to remote:     git -C <path> reset --hard <source>/<branch>  (DESTROYS local changes)"
    echo ""
    for conflict_repo in "${MERGE_CONFLICTS[@]}"; do
        echo "  $conflict_repo"
    done
fi

if [[ $SKIPPED -gt 0 ]] && ! $CLONE_MISSING; then
    echo ""
    echo "Hint: re-run with --clone-missing to clone skipped repos from manifest"
fi
