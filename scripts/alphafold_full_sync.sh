#!/bin/bash
# AlphaFold DB v6 — Full sovereign mirror via rsync
# Restart-safe: rsync resumes interrupted transfers automatically
# Run via systemd timer or cron for persistence across reboots
#
# Current state: 46/48 proteome tars (79 GB) already on ZFS
# Remaining: swissprot_cif_v6.tar (37 GB), swissprot_pdb_v6.tar (27 GB),
#            sequences.fasta (118 GB), accession_ids.csv (8.7 GB),
#            msa_depths.csv (3.8 GB), diffs.ndjson.gz (309 MB)
# Total remaining: ~195 GB
# Total when complete: ~274 GB, 1.65M+ structures

DEST="/mnt/nestgate/cold/zfs/data/alphafold"
RSYNC_SRC="rsync://ftp.ebi.ac.uk/pub/databases/alphafold"
LOG="/tmp/alphafold_sync.log"

mkdir -p "$DEST"

echo "$(date '+%Y-%m-%d %H:%M:%S') — AlphaFold full sync starting" | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Phase 1: v6 proteome + swissprot tars" | tee -a "$LOG"
rsync -av --progress --partial \
  "$RSYNC_SRC/v6/" \
  "$DEST/" \
  2>&1 | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Phase 2: sequences.fasta (118 GB)" | tee -a "$LOG"
rsync -av --progress --partial \
  "$RSYNC_SRC/sequences.fasta" \
  "$DEST/sequences.fasta" \
  2>&1 | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Phase 3: accession_ids.csv (8.7 GB)" | tee -a "$LOG"
rsync -av --progress --partial \
  "$RSYNC_SRC/accession_ids.csv" \
  "$DEST/accession_ids.csv" \
  2>&1 | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Phase 4: metadata files" | tee -a "$LOG"
rsync -av --progress --partial \
  "$RSYNC_SRC/msa_depths.csv" \
  "$DEST/msa_depths.csv" \
  2>&1 | tee -a "$LOG"

rsync -av --progress --partial \
  "$RSYNC_SRC/diffs.ndjson.gz" \
  "$DEST/diffs.ndjson.gz" \
  2>&1 | tee -a "$LOG"

rsync -av --progress --partial \
  "$RSYNC_SRC/download_metadata.json" \
  "$DEST/download_metadata.json" \
  2>&1 | tee -a "$LOG"

rsync -av --progress --partial \
  "$RSYNC_SRC/README.txt" \
  "$DEST/README.txt" \
  2>&1 | tee -a "$LOG"

rsync -av --progress --partial \
  "$RSYNC_SRC/CHANGELOG.txt" \
  "$DEST/CHANGELOG.txt" \
  2>&1 | tee -a "$LOG"

echo "$(date '+%Y-%m-%d %H:%M:%S') — AlphaFold sync complete" | tee -a "$LOG"
echo "Final size:" | tee -a "$LOG"
du -sh "$DEST" | tee -a "$LOG"
echo "File count:" | tee -a "$LOG"
ls "$DEST" | wc -l | tee -a "$LOG"
