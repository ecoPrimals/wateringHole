#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# impulse-relay-hook.sh — Forgejo post-receive webhook handler
#
# Deployed on golgiBody VPS. Triggered by Forgejo webhook on push to
# wateringHole repo. Detects new impulses in impulses/active/ and
# relays them via songbird mesh.publish for near-realtime propagation.
#
# Webhook config (Forgejo repo settings → Webhooks):
#   URL: http://localhost:3001/hooks/impulse-relay
#   Method: POST
#   Content type: application/json
#   Trigger: Push events
#   Branch filter: main
#
# This script is called by a lightweight HTTP listener (e.g. webhook daemon)
# that receives the Forgejo push payload.

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
