#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# impulse-relay-hook.sh — Impulse detection and relay (standalone)
#
# Detects pending impulses in impulses/active/ and relays them via
# songbird mesh.publish for near-realtime propagation.
#
# K-Derm deployment: runs on peptidoglycan as part of pepti-sync-relay.sh.
# Can also run standalone on any node with membrane binary and wateringHole.
#
# For the full K-Derm diderm flow, use pepti-sync-relay.sh instead —
# it calls this script as part of the metallic→ionic relay chain.

set -euo pipefail

ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-/home/git/ecoPrimals}"
WATERINGHOLE="$ECOPRIMALS_ROOT/infra/wateringHole"
MEMBRANE_BIN="${MEMBRANE_BIN:-$(command -v membrane 2>/dev/null || echo "")}"
LOG_TAG="impulse-relay"

log() { logger -t "$LOG_TAG" "$@" 2>/dev/null || echo "[$LOG_TAG] $*"; }

if [[ ! -x "$MEMBRANE_BIN" ]]; then
    log "ERROR: membrane binary not found"
    exit 1
fi

# Pull latest wateringHole to get new impulses
cd "$WATERINGHOLE"
git pull --ff-only --quiet origin main 2>/dev/null || true

# Count pending impulses
PENDING=$("$MEMBRANE_BIN" potential.sense --count 2>/dev/null || echo "0")

if [[ "$PENDING" -gt 0 ]]; then
    log "Detected $PENDING pending impulse(s) — relaying"

    # Sense and log each impulse
    "$MEMBRANE_BIN" potential.sense 2>/dev/null | while read -r line; do
        log "  $line"
    done

    # Attempt songbird mesh relay (graceful — no failure if songbird is offline)
    if "$MEMBRANE_BIN" potential.check 2>/dev/null; then
        log "Impulse relay complete (mesh healthy)"
    else
        log "WARN: mesh relay unavailable — impulses will propagate on next cascade-pull"
    fi
else
    log "No pending impulses (resting potential)"
fi
