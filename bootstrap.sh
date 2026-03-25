#!/usr/bin/env bash
set -euo pipefail

# ecoPrimals Canonical Workspace Bootstrap
# See WORKSPACE_LAYOUT.md for the target structure.
#
# Usage:
#   bootstrap.sh [--dry-run] [--fresh]
#
# Modes:
#   (default)   Migrate existing repos from phase1/phase2/ecoSprings layout
#   --fresh     Clone all repos from GitHub into a clean workspace
#   --dry-run   Print what would happen without doing anything

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DRY_RUN=false
FRESH=false
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --fresh)   FRESH=true ;;
        --help|-h)
            echo "Usage: bootstrap.sh [--dry-run] [--fresh]"
            echo "  --dry-run   Print what would happen"
            echo "  --fresh     Clone all repos from GitHub (skip migration)"
            exit 0
            ;;
        *) echo "Unknown option: $arg"; exit 1 ;;
    esac
done

# Resolve workspace root.
# If this script lives at infra/wateringHole/bootstrap.sh, root is ../..
# If it lives at wateringHole/bootstrap.sh (pre-migration), root is ..
if [[ "$(basename "$(dirname "$SCRIPT_DIR")")" == "infra" ]]; then
    ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
    ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

echo "=== ecoPrimals Workspace Bootstrap ==="
echo "Root:    $ROOT"
echo "Mode:    $(${FRESH} && echo 'fresh clone' || echo 'migrate')"
echo "Dry run: $DRY_RUN"
echo ""

WARNINGS=()
MOVED=0
CLONED=0
SKIPPED=0

run() {
    if $DRY_RUN; then
        echo "  [dry-run] $*"
    else
        "$@"
    fi
}

ensure_dir() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        run mkdir -p "$dir"
    fi
}

# Move a repo from old location to new location.
# Preserves .git, handles case where source doesn't exist or target already exists.
move_repo() {
    local src="$1"
    local dst="$2"
    local label="$3"

    if [[ -d "$dst/.git" ]] || [[ -d "$dst" && -d "$dst/.git" ]]; then
        echo "  SKIP $label (already at $dst)"
        ((SKIPPED++)) || true
        return
    fi

    if [[ -L "$src" ]]; then
        echo "  SKIP $label (symlink at $src, removing)"
        run rm -f "$src"
        return
    fi

    if [[ ! -d "$src" ]]; then
        return
    fi

    if [[ ! -d "$src/.git" ]]; then
        echo "  SKIP $label ($src exists but is not a git repo)"
        return
    fi

    echo "  MOVE $src -> $dst"
    ensure_dir "$(dirname "$dst")"
    run mv "$src" "$dst"
    ((MOVED++)) || true
}

# Clone a repo if it doesn't already exist locally.
clone_repo() {
    local org="$1"
    local repo="$2"
    local dst="$3"

    if [[ -d "$dst/.git" ]]; then
        echo "  SKIP $org/$repo (already at $dst)"
        ((SKIPPED++)) || true
        return
    fi

    if [[ -d "$dst" ]]; then
        echo "  SKIP $org/$repo ($dst exists but no .git)"
        ((SKIPPED++)) || true
        return
    fi

    echo "  CLONE $org/$repo -> $dst"
    ensure_dir "$(dirname "$dst")"
    if $DRY_RUN; then
        echo "  [dry-run] gh repo clone $org/$repo $dst"
    else
        if ! gh repo clone "$org/$repo" "$dst" 2>/dev/null; then
            echo "  WARN: failed to clone $org/$repo (may not have access)"
            WARNINGS+=("Failed to clone $org/$repo")
            return
        fi
    fi
    ((CLONED++)) || true
}

# Scan for Cargo.toml files with relative path deps that may need updating.
warn_path_deps() {
    local dir="$1"
    local label="$2"
    if [[ ! -d "$dir" ]]; then return; fi

    local hits
    hits=$(grep -rl 'path\s*=\s*"\.\./' "$dir" --include='Cargo.toml' 2>/dev/null || true)
    if [[ -n "$hits" ]]; then
        WARNINGS+=("$label has Cargo.toml path dependencies that may need updating after migration:")
        while IFS= read -r f; do
            WARNINGS+=("  $f")
        done <<< "$hits"
    fi
}

# =========================================================================
# Step 1: Create target directories
# =========================================================================
echo "--- Creating target directories ---"
for d in primals springs gardens infra sort-after; do
    ensure_dir "$ROOT/$d"
done
echo ""

# =========================================================================
# Step 2: Migration (move existing repos)
# =========================================================================
if ! $FRESH; then
    echo "--- Migrating existing repos ---"

    # phase1/ primals (lowercase on disk)
    move_repo "$ROOT/phase1/beardog"   "$ROOT/primals/beardog"   "bearDog (phase1)"
    move_repo "$ROOT/phase1/nestgate"  "$ROOT/primals/nestgate"  "nestGate (phase1)"
    move_repo "$ROOT/phase1/songbird"  "$ROOT/primals/songbird"  "songBird (phase1)"
    move_repo "$ROOT/phase1/squirrel"  "$ROOT/primals/squirrel"  "squirrel (phase1)"
    move_repo "$ROOT/phase1/toadstool" "$ROOT/primals/toadstool" "toadStool (phase1)"

    # phase2/ primals
    move_repo "$ROOT/phase2/biomeOS"   "$ROOT/primals/biomeOS"   "biomeOS (phase2)"
    move_repo "$ROOT/phase2/loamSpine" "$ROOT/primals/loamSpine" "loamSpine (phase2)"
    move_repo "$ROOT/phase2/rhizoCrypt" "$ROOT/primals/rhizoCrypt" "rhizoCrypt (phase2)"
    move_repo "$ROOT/phase2/sweetGrass" "$ROOT/primals/sweetGrass" "sweetGrass (phase2)"

    # Top-level primals
    move_repo "$ROOT/barraCuda"    "$ROOT/primals/barraCuda"    "barraCuda (top-level)"
    move_repo "$ROOT/coralReef"    "$ROOT/primals/coralReef"    "coralReef (top-level)"
    move_repo "$ROOT/petalTongue"  "$ROOT/primals/petalTongue"  "petalTongue (top-level)"

    # ecoSprings/ -> springs/
    move_repo "$ROOT/ecoSprings/airSpring"     "$ROOT/springs/airSpring"     "airSpring"
    move_repo "$ROOT/ecoSprings/groundSpring"  "$ROOT/springs/groundSpring"  "groundSpring"
    move_repo "$ROOT/ecoSprings/healthSpring"  "$ROOT/springs/healthSpring"  "healthSpring"
    move_repo "$ROOT/ecoSprings/hotSpring"     "$ROOT/springs/hotSpring"     "hotSpring"
    move_repo "$ROOT/ecoSprings/ludoSpring"    "$ROOT/springs/ludoSpring"    "ludoSpring"
    move_repo "$ROOT/ecoSprings/neuralSpring"  "$ROOT/springs/neuralSpring"  "neuralSpring"
    move_repo "$ROOT/ecoSprings/primalSpring"  "$ROOT/springs/primalSpring"  "primalSpring"
    move_repo "$ROOT/ecoSprings/wetSpring"     "$ROOT/springs/wetSpring"     "wetSpring"

    # ecoSprings/ -> gardens/
    move_repo "$ROOT/ecoSprings/esotericWebb" "$ROOT/gardens/esotericWebb" "esotericWebb"

    # ecoSprings/barraCuda symlink cleanup
    if [[ -L "$ROOT/ecoSprings/barraCuda" ]]; then
        echo "  REMOVE symlink $ROOT/ecoSprings/barraCuda"
        run rm -f "$ROOT/ecoSprings/barraCuda"
    fi

    # Top-level infra
    move_repo "$ROOT/wateringHole" "$ROOT/infra/wateringHole" "wateringHole"
    move_repo "$ROOT/whitePaper"   "$ROOT/infra/whitePaper"   "whitePaper"
    move_repo "$ROOT/plasmidBin"   "$ROOT/infra/plasmidBin"   "plasmidBin"

    # Clean up empty old directories
    for d in phase1 phase2/archive phase2/rootpulse phase2 ecoSprings; do
        if [[ -d "$ROOT/$d" ]]; then
            remaining=$(find "$ROOT/$d" -mindepth 1 -maxdepth 1 -not -name '.*' 2>/dev/null | wc -l)
            if [[ "$remaining" -eq 0 ]]; then
                echo "  RMDIR $ROOT/$d (empty)"
                run rm -rf "$ROOT/$d"
            else
                echo "  KEEP  $ROOT/$d ($remaining items remaining)"
                WARNINGS+=("$d still has $remaining items after migration — inspect manually")
            fi
        fi
    done

    echo ""
fi

# =========================================================================
# Step 3: Clone missing repos
# =========================================================================
echo "--- Cloning missing repos ---"

# Primals (ecoPrimals org)
for repo in barraCuda bearDog biomeOS bingoCube coralReef loamSpine nestGate \
            petalTongue rhizoCrypt skunkBat songBird sourDough squirrel \
            sweetGrass toadStool; do
    # phase1 used lowercase names — check both
    lower=$(echo "$repo" | tr '[:upper:]' '[:lower:]')
    if [[ -d "$ROOT/primals/$repo/.git" ]] || [[ -d "$ROOT/primals/$lower/.git" ]]; then
        echo "  SKIP ecoPrimals/$repo (already present)"
        ((SKIPPED++)) || true
    else
        clone_repo "ecoPrimals" "$repo" "$ROOT/primals/$repo"
    fi
done

# Springs (syntheticChemistry org)
for repo in airSpring groundSpring healthSpring hotSpring ludoSpring \
            neuralSpring primalSpring wetSpring; do
    clone_repo "syntheticChemistry" "$repo" "$ROOT/springs/$repo"
done

# Gardens (sporeGarden org, plus blueFish from syntheticChemistry pending transfer)
clone_repo "sporeGarden" "esotericWebb" "$ROOT/gardens/esotericWebb"
clone_repo "syntheticChemistry" "blueFish" "$ROOT/gardens/blueFish"

# Infra (ecoPrimals org)
clone_repo "ecoPrimals" "wateringHole" "$ROOT/infra/wateringHole"
clone_repo "ecoPrimals" "whitePaper" "$ROOT/infra/whitePaper"
clone_repo "ecoPrimals" "plasmidBin" "$ROOT/infra/plasmidBin"
clone_repo "ecoPrimals" "sporePrint" "$ROOT/infra/sporePrint"

# Sort-after (syntheticChemistry org)
for repo in agentReagents benchScale ionChannel rustChip; do
    clone_repo "syntheticChemistry" "$repo" "$ROOT/sort-after/$repo"
done

echo ""

# =========================================================================
# Step 4: Warn about path dependencies
# =========================================================================
echo "--- Checking for path dependencies that need updating ---"
warn_path_deps "$ROOT/springs" "springs/"
warn_path_deps "$ROOT/gardens" "gardens/"
echo ""

# =========================================================================
# Summary
# =========================================================================
echo "=== Summary ==="
echo "Moved:   $MOVED"
echo "Cloned:  $CLONED"
echo "Skipped: $SKIPPED"

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    echo ""
    echo "=== Warnings ==="
    for w in "${WARNINGS[@]}"; do
        echo "  $w"
    done
fi

echo ""
echo "Layout:"
for d in primals springs gardens infra sort-after; do
    if [[ -d "$ROOT/$d" ]]; then
        count=$(find "$ROOT/$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
        echo "  $d/  ($count repos)"
    fi
done

echo ""
echo "Done. See WORKSPACE_LAYOUT.md for the canonical structure."
