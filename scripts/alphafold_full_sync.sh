#!/bin/bash
# AlphaFold DB — COMPLETE sovereign mirror v1 through v6 via rsync
# Restart-safe: rsync resumes interrupted transfers automatically
# Run via systemd timer for persistence across reboots
#
# Archive: v1 (20 proteomes) → v2 (49) → v3 (51) → v4 (53) → v5 (50) → v6 (49)
# Plus: sequences.fasta (118 GB), accession_ids.csv (8.7 GB), metadata
# Estimated total: ~500 GB across all versions

DEST="/mnt/nestgate/cold/zfs/data/alphafold"
RSYNC_SRC="rsync://ftp.ebi.ac.uk/pub/databases/alphafold"
LOG="/tmp/alphafold_sync.log"

mkdir -p "$DEST/v1" "$DEST/v2" "$DEST/v3" "$DEST/v4" "$DEST/v5" "$DEST/v6"

echo "$(date '+%Y-%m-%d %H:%M:%S') — AlphaFold FULL archive sync starting (v1-v6)" | tee -a "$LOG"

for VER in v1 v2 v3 v4 v5 v6; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') — Syncing $VER proteome tars" | tee -a "$LOG"
  rsync -av --progress --partial \
    "$RSYNC_SRC/$VER/" \
    "$DEST/$VER/" \
    2>&1 | tee -a "$LOG"
done

echo "$(date '+%Y-%m-%d %H:%M:%S') — Syncing sequences.fasta (118 GB)" | tee -a "$LOG"
rsync -av --progress --partial \
  "$RSYNC_SRC/sequences.fasta" \
  "$DEST/sequences.fasta" \
  2>&1 | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Syncing accession_ids.csv (8.7 GB)" | tee -a "$LOG"
rsync -av --progress --partial \
  "$RSYNC_SRC/accession_ids.csv" \
  "$DEST/accession_ids.csv" \
  2>&1 | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Syncing remaining metadata" | tee -a "$LOG"
for F in msa_depths.csv diffs.ndjson.gz download_metadata.json README.txt CHANGELOG.txt; do
  rsync -av --progress --partial \
    "$RSYNC_SRC/$F" \
    "$DEST/$F" \
    2>&1 | tee -a "$LOG"
done

echo "$(date '+%Y-%m-%d %H:%M:%S') — AlphaFold FULL archive sync complete" | tee -a "$LOG"
echo "=== Summary ===" | tee -a "$LOG"
for VER in v1 v2 v3 v4 v5 v6; do
  echo "$VER: $(du -sh "$DEST/$VER" 2>/dev/null | cut -f1) ($(ls "$DEST/$VER" 2>/dev/null | wc -l) files)" | tee -a "$LOG"
done
echo "Total: $(du -sh "$DEST" | cut -f1)" | tee -a "$LOG"
