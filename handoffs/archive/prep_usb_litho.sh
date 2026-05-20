#!/usr/bin/env bash
# wetSpring → lithoSpore USB preparation script
# Copies experiment artifacts to a mounted USB drive for physical handoff
#
# Usage: ./prep_usb_litho.sh /media/southgate/LITHOSPORE
#
# Budget: ~64 GB USB
# Expected: ~14 GB Barrick + ~100 MB repo/docs = ~14.1 GB
# Remaining: ~50 GB for future Tenaillon batches

set -euo pipefail

USB="${1:?Usage: $0 /path/to/usb/mount}"
REPO="/home/southgate/Development/ecoPrimals/springs/wetSpring"
ECO="/home/southgate/Development/ecoPrimals"
WORKSPACE="/mnt/4tb-work/ecoPrimals/springs/wetSpring/datasets/ltee"

if [ ! -d "$USB" ]; then
    echo "ERROR: USB mount point $USB does not exist"
    exit 1
fi

echo "=== wetSpring → lithoSpore USB transfer ==="
echo "Target: $USB"
echo ""

# 1. Barrick 2009 full experiment
echo "[1/7] Barrick 2009 reads..."
mkdir -p "$USB/barrick_2009/reads"
rsync -ah --progress "$WORKSPACE/barrick_2009/reads/" "$USB/barrick_2009/reads/"

echo "[2/7] Barrick 2009 reference..."
mkdir -p "$USB/barrick_2009/reference"
rsync -ah --progress "$WORKSPACE/barrick_2009/reference/" "$USB/barrick_2009/reference/"

echo "[3/7] Barrick 2009 breseq output..."
mkdir -p "$USB/barrick_2009/breseq_output"
rsync -ah --progress "$WORKSPACE/barrick_2009/breseq_output/" "$USB/barrick_2009/breseq_output/"

# 2. Braids (portable provenance)
echo "[4/7] Provenance braids..."
mkdir -p "$USB/provenance/braids"
cp "$REPO/provenance/braids/"*.json "$USB/provenance/braids/"
# Also copy workspace braids if they differ
cp "$WORKSPACE/barrick_2009/provenance/braids/"*.json "$USB/provenance/braids/" 2>/dev/null || true

# 3. Source repo (no target/ or .git/)
echo "[5/7] wetSpring source..."
mkdir -p "$USB/wetSpring"
rsync -ah --progress \
    --exclude='target/' \
    --exclude='.git/' \
    --exclude='datasets/' \
    "$REPO/" "$USB/wetSpring/"

# 4. Release binaries
echo "[6/7] Pre-built binaries..."
mkdir -p "$USB/bin"
cp "$REPO/target/release/validate_sovereign_resequencing" "$USB/bin/" 2>/dev/null || echo "  (sovereign binary not found, skip)"
cp "$REPO/target/release/validate_breseq_barrick_2009" "$USB/bin/" 2>/dev/null || echo "  (breseq binary not found, skip)"

# 5. Ecosystem docs
echo "[7/7] Ecosystem context..."
mkdir -p "$USB/ecosystem/lithoSpore"
rsync -ah "$ECO/gardens/lithoSpore/" "$USB/ecosystem/lithoSpore/" --exclude='.git/'
mkdir -p "$USB/ecosystem/wateringHole/handoffs"
rsync -ah "$ECO/infra/wateringHole/handoffs/" "$USB/ecosystem/wateringHole/handoffs/"

# Tenaillon prototype braid (if available)
if ls "$WORKSPACE/tenaillon_2016/provenance/braids/"*.json 1>/dev/null 2>&1; then
    echo "[+] Tenaillon prototype braids found, copying..."
    cp "$WORKSPACE/tenaillon_2016/provenance/braids/"*.json "$USB/provenance/braids/"
fi
if ls "$REPO/provenance/braids/tenaillon"* 1>/dev/null 2>&1; then
    cp "$REPO/provenance/braids/tenaillon"*.json "$USB/provenance/braids/" 2>/dev/null || true
fi

echo ""
echo "=== Transfer complete ==="
du -sh "$USB"
echo ""
echo "Contents:"
du -sh "$USB"/*
echo ""
echo "Braids:"
ls -la "$USB/provenance/braids/"
