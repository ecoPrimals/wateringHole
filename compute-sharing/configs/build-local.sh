#!/usr/bin/env bash
# /opt/depot/build-local.sh — Sovereign CI: build primals from local source repos
#
# Unlike pepti's build-primal.sh which clones from GitHub, this builds directly
# from local source repos at $ECOPRIMALS_ROOT/primals/. No network needed for builds.
#
# Usage:
#   ./build-local.sh --all                # Build all primals (musl, default)
#   ./build-local.sh skunkbat             # Build one primal
#   ./build-local.sh --all --sync         # Build all + rsync to golgi
#   ./build-local.sh --changed            # Build only primals with new commits since last build
#   ./build-local.sh --target gnu         # Build GPU primals as glibc (barracuda, coralreef)
#   ./build-local.sh --target all         # Build full musl set + gnu GPU primals
#   ./build-local.sh --target gnu barracuda  # Build one primal as glibc

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-$HOME/Development/ecoPrimals}"
CHECKSUMS_FILE="$SCRIPT_DIR/checksums.toml"
PROVENANCE_FILE="$SCRIPT_DIR/provenance.toml"

# Depot sync target — sourced from ecosystem_manifest.toml [gates.golgiBody] wg_ip.
# Prefer `membrane plasmid.harvest` for manifest-driven builds (replaces this script).
DEPOT_SYNC_HOST="${DEPOT_SYNC_HOST:-10.13.37.1}"
DEPOT_SYNC_USER="${DEPOT_SYNC_USER:-root}"
DEPOT_SYNC_PATH="/opt/ecoPrimals/plasmidBin"

# Target selection — musl (default, static), gnu (glibc, for GPU primals)
TARGET_MODE="musl"
TARGET_MUSL="x86_64-unknown-linux-musl"
TARGET_GNU="x86_64-unknown-linux-gnu"
TARGET="$TARGET_MUSL"
DEPOT_DIR="$SCRIPT_DIR/primals/$TARGET_MUSL"

# GPU primals that need glibc for dlopen(libvulkan.so)
GPU_PRIMALS=(barracuda coralreef)

# Ensure cargo is in PATH for non-login SSH sessions
[[ -f "$HOME/.cargo/env" ]] && source "$HOME/.cargo/env"

BUILD_ALL=false
BUILD_CHANGED=false
DO_SYNC=false
FILTER=""

declare -A PRIMAL_MAP=(
    [beardog]="bearDog"
    [songbird]="songBird"
    [toadstool]="toadStool"
    [barracuda]="barraCuda"
    [coralreef]="coralReef"
    [nestgate]="nestGate"
    [rhizocrypt]="rhizoCrypt"
    [loamspine]="loamSpine"
    [sweetgrass]="sweetGrass"
    [biomeos]="biomeOS"
    [squirrel]="squirrel"
    [petaltongue]="petalTongue"
    [skunkbat]="skunkBat"
)

declare -A BUILD_ARGS=(
    [biomeos]="-p biomeos-unibin"
    [skunkbat]="-p skunk-bat-server"
    [squirrel]="-p squirrel"
)

# Binary name overrides — what the release binary is actually called
declare -A BINARY_NAMES=(
    [beardog]="beardog"
    [songbird]="songbird"
    [toadstool]="toadstool"
    [barracuda]="barracuda"
    [coralreef]="coralreef"
    [nestgate]="nestgate"
    [rhizocrypt]="rhizocrypt"
    [loamspine]="loamspine"
    [sweetgrass]="sweetgrass"
    [biomeos]="biomeos"
    [squirrel]="squirrel"
    [petaltongue]="petaltongue"
    [skunkbat]="skunkbat"
)

passed=0
failed=0
skipped=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all)       BUILD_ALL=true; shift ;;
        --changed)   BUILD_CHANGED=true; shift ;;
        --sync)      DO_SYNC=true; shift ;;
        --target)
            shift
            case "${1:-}" in
                gnu)  TARGET_MODE="gnu"; TARGET="$TARGET_GNU"; DEPOT_DIR="$SCRIPT_DIR/primals/$TARGET_GNU" ;;
                musl) TARGET_MODE="musl"; TARGET="$TARGET_MUSL"; DEPOT_DIR="$SCRIPT_DIR/primals/$TARGET_MUSL" ;;
                all)  TARGET_MODE="all" ;;
                *)    echo "ERROR: --target must be 'musl', 'gnu', or 'all'"; exit 1 ;;
            esac
            shift ;;
        --help|-h)   echo "Usage: $0 [PRIMAL|--all|--changed] [--target musl|gnu|all] [--sync]"; exit 0 ;;
        -*)          echo "Unknown: $1"; exit 1 ;;
        *)           FILTER="$1"; shift ;;
    esac
done

if ! $BUILD_ALL && ! $BUILD_CHANGED && [[ -z "$FILTER" ]]; then
    echo "ERROR: Specify primal name, --all, or --changed"
    exit 1
fi

is_gpu_primal() {
    local id="$1"
    for gp in "${GPU_PRIMALS[@]}"; do
        [[ "$gp" == "$id" ]] && return 0
    done
    return 1
}

mkdir -p "$SCRIPT_DIR/primals/$TARGET_MUSL"
mkdir -p "$SCRIPT_DIR/primals/$TARGET_GNU"

build_one() {
    local id="$1"
    local build_target="${2:-$TARGET}"
    local build_depot_dir="$SCRIPT_DIR/primals/$build_target"
    local repo_name="${PRIMAL_MAP[$id]:-}"

    if [[ -z "$repo_name" ]]; then
        echo "  [$id] SKIP — unknown primal"
        ((skipped++)) || true
        return
    fi

    local src_dir="$ECOPRIMALS_ROOT/primals/$repo_name"
    if [[ ! -d "$src_dir" ]]; then
        echo "  [$id] SKIP — source not found at $src_dir"
        ((skipped++)) || true
        return
    fi

    if [[ ! -f "$src_dir/Cargo.toml" ]]; then
        echo "  [$id] SKIP — no Cargo.toml"
        ((skipped++)) || true
        return
    fi

    local extra_args="${BUILD_ARGS[$id]:-}"
    local start_time=$SECONDS

    echo -n "  [$id → $build_target] building from $repo_name ... "

    # shellcheck disable=SC2086
    if ! cargo build --release --target "$build_target" \
        --manifest-path "$src_dir/Cargo.toml" \
        $extra_args \
        2>"/tmp/build_${id}_${build_target##*-}.log"; then
        echo "FAIL ($(( SECONDS - start_time ))s) — see /tmp/build_${id}_${build_target##*-}.log"
        ((failed++)) || true
        return
    fi

    local bin_dir="$src_dir/target/$build_target/release"
    local expected_bin="${BINARY_NAMES[$id]:-$id}"
    local src_bin="$bin_dir/$expected_bin"

    if [[ -f "$src_bin" ]] && file "$src_bin" | grep -q "ELF"; then
        cp "$src_bin" "$build_depot_dir/$expected_bin"
        chmod +x "$build_depot_dir/$expected_bin"
        echo "OK ($(( SECONDS - start_time ))s)"
        ((passed++)) || true
    else
        # Fallback: scan for any matching ELF (handles renamed binaries)
        local found=false
        local elf_pattern="ELF"
        # For musl target, require static; for gnu, accept dynamic
        [[ "$build_target" == "$TARGET_MUSL" ]] && elf_pattern="ELF.*static"
        for bin in "$bin_dir"/*; do
            [[ -f "$bin" ]] && [[ -x "$bin" ]] || continue
            local bn; bn="$(basename "$bin")"
            case "$bn" in *.d|*.rlib|*.rmeta|*.so|build-script-*|*.a|*.o) continue ;; esac
            if file "$bin" | grep -q "$elf_pattern"; then
                cp "$bin" "$build_depot_dir/$id"
                chmod +x "$build_depot_dir/$id"
                found=true
                break
            fi
        done
        if $found; then
            echo "OK ($(( SECONDS - start_time ))s) [fallback name: $id]"
            ((passed++)) || true
        else
            echo "FAIL — no ELF binary found in $bin_dir"
            ((failed++)) || true
        fi
    fi
}

echo "=== sporeGate Sovereign CI — Local Build ==="
echo "Mode:    $TARGET_MODE"
echo "Source:  $ECOPRIMALS_ROOT/primals/"
echo "Depot:   $SCRIPT_DIR/primals/"
echo "Time:    $(date -Iseconds)"
echo ""

run_builds() {
    local build_target="$1"
    local filter_gpu="$2"  # "gpu_only", "non_gpu", or "all"

    echo "--- Target: $build_target ---"

    if $BUILD_ALL || $BUILD_CHANGED; then
        for id in "${!PRIMAL_MAP[@]}"; do
            case "$filter_gpu" in
                gpu_only)  is_gpu_primal "$id" || continue ;;
                non_gpu)   is_gpu_primal "$id" && continue ;;
                all)       ;;
            esac
            build_one "$id" "$build_target"
        done
    else
        build_one "${FILTER,,}" "$build_target"
    fi
}

case "$TARGET_MODE" in
    musl)
        run_builds "$TARGET_MUSL" "all"
        ;;
    gnu)
        if [[ -n "$FILTER" ]]; then
            run_builds "$TARGET_GNU" "all"
        else
            run_builds "$TARGET_GNU" "gpu_only"
        fi
        ;;
    all)
        run_builds "$TARGET_MUSL" "all"
        echo ""
        echo "=== GPU Primals (glibc) ==="
        run_builds "$TARGET_GNU" "gpu_only"
        ;;
esac

echo ""
echo "=== Build Summary ==="
echo "  Passed:  $passed"
echo "  Failed:  $failed"
echo "  Skipped: $skipped"

if [[ $passed -gt 0 ]]; then
    echo ""
    echo "=== Generating checksums.toml ==="
    {
        echo "# plasmidBin checksums — BLAKE3"
        echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "# Builder: sporeGate (sovereign CI)"
        echo ""
        for target_dir in "$SCRIPT_DIR/primals/"*/; do
            target_name="$(basename "$target_dir")"
            [[ -d "$target_dir" ]] || continue
            has_bins=false
            for bin in "$target_dir"*; do [[ -f "$bin" ]] && has_bins=true && break; done
            $has_bins || continue
            echo "[$target_name]"
            for bin in "$target_dir"*; do
                [[ -f "$bin" ]] || continue
                local_name="$(basename "$bin")"
                hash="$(b3sum --no-names "$bin")"
                size="$(stat -c %s "$bin")"
                echo "$local_name = { blake3 = \"$hash\", size = $size }"
            done
            echo ""
        done
    } > "$CHECKSUMS_FILE"
    echo "  Written: $CHECKSUMS_FILE"
fi

if $DO_SYNC && [[ $passed -gt 0 ]]; then
    echo ""
    echo "=== Syncing to golgi ($DEPOT_SYNC_HOST) ==="
    rsync -avz --checksum "$SCRIPT_DIR/primals/" "${DEPOT_SYNC_USER}@${DEPOT_SYNC_HOST}:${DEPOT_SYNC_PATH}/primals/"
    rsync -avz "$CHECKSUMS_FILE" "${DEPOT_SYNC_USER}@${DEPOT_SYNC_HOST}:${DEPOT_SYNC_PATH}/checksums.toml"
    echo "  Depot synced to golgi WAN endpoint"
fi

echo ""
echo "=== Done ==="
