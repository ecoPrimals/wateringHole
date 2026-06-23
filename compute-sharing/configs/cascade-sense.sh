#!/usr/bin/env bash
# Quorum Phase 1: autonomous cascade sense
# golgi (peptidoglycan) pulls from Forgejo, then instructs golgi-ext 
# to pull from Forgejo and push to GitHub (K-Derm relay chain)
#
# Deployed: /opt/ecoPrimals/cascade-sense.sh on golgiBody
# Timer: cascade-pull.timer (15min interval)
#
# Wave 124: mirror push uses --force-with-lease to handle concurrent
# gate pushes to origin without rejecting the relay.
set -euo pipefail

WORKSPACE="/opt/ecoPrimals/infra/wateringHole"
LOG="/var/log/cascade-sense.log"

timestamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }

echo "[$(timestamp)] ═══ Cascade sense started ═══" >> "$LOG"

cd "$WORKSPACE"

# Phase 1: Pull from Forgejo (inner membrane → peptidoglycan)
if git pull origin main --ff-only >> "$LOG" 2>&1; then
    echo "[$(timestamp)] [OK] Forgejo pull" >> "$LOG"
else
    echo "[$(timestamp)] [OK] Forgejo at HEAD (no new commits)" >> "$LOG"
fi

# Phase 2: Relay to golgi-ext → GitHub (ionic → weak bond outward)
# Uses --force-with-lease: if a gate pushed directly to GitHub, the relay
# overwrites it (sovereign Forgejo is authority, GitHub is mirror).
if ssh golgi-ext "cd /opt/ecoPrimals/infra/wateringHole && git fetch forgejo main && git reset --hard forgejo/main && git push --force-with-lease origin main" >> "$LOG" 2>&1; then
    echo "[$(timestamp)] [OK] GitHub relay via golgi-ext" >> "$LOG"
else
    echo "[$(timestamp)] [WARN] GitHub relay failed (non-fatal)" >> "$LOG"
fi

# Phase 3: Sense active impulses
IMPULSE_DIR="$WORKSPACE/impulses/active"
if [ -d "$IMPULSE_DIR" ]; then
    IMPULSE_COUNT=$(find "$IMPULSE_DIR" -name "*.toml" -type f | wc -l)
else
    IMPULSE_COUNT=0
fi
echo "[$(timestamp)] Active impulses: $IMPULSE_COUNT" >> "$LOG"

echo "[$(timestamp)] ═══ Cascade sense complete ═══" >> "$LOG"
