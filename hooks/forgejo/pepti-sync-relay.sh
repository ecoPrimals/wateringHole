#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# pepti-sync-relay.sh — Peptidoglycan sync relay (metallic bond mediator)
#
# Runs on peptidoglycan. Triggered by Forgejo post-receive webhook on
# golgiBody-inner. Pulls from Forgejo (metallic bond inward), runs the
# impulse cascade, then pushes to golgiBody-ext (ionic bond outward).
#
# K-Derm flow:
#   golgiBody-inner (cis) ──metallic──→ peptidoglycan ──ionic──→ golgiBody-ext (trans)
#
# Peptidoglycan is the structural sync hub: it mediates between the
# receiving face (cis/inner) and the shipping face (trans/outer) of the
# Golgi apparatus diderm envelope.
#
# Webhook config (Forgejo repo settings → Webhooks on golgiBody-inner):
#   URL: http://peptidoglycan:3001/hooks/pepti-sync-relay
#   Method: POST
#   Content type: application/json
#   Trigger: Push events
#   Branch filter: main

set -euo pipefail

ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-/opt/ecoPrimals}"
MEMBRANE_BIN="${MEMBRANE_BIN:-$(command -v membrane 2>/dev/null || echo "")}"
GOLGI_EXT_HOST="${GOLGI_EXT_HOST:-golgi-ext}"
LOG_TAG="pepti-sync-relay"

log() { logger -t "$LOG_TAG" "$@" 2>/dev/null || echo "[$LOG_TAG] $*"; }

# ── Step 1: Pull from Forgejo (metallic bond inward) ─────────────────

log "=== Sync relay triggered ==="

cd "$ECOPRIMALS_ROOT/infra/wateringHole"
git pull --ff-only forgejo main --quiet 2>/dev/null || {
    log "WARN: wateringHole pull failed — may be up to date"
}

# ── Step 2: Impulse cascade (if membrane available) ──────────────────

if [[ -x "$MEMBRANE_BIN" ]]; then
    PENDING=$("$MEMBRANE_BIN" potential.sense --count 2>/dev/null || echo "0")
    if [[ "$PENDING" -gt 0 ]]; then
        log "Detected $PENDING pending impulse(s)"
        "$MEMBRANE_BIN" potential.sense 2>/dev/null | while read -r line; do
            log "  impulse: $line"
        done
    else
        log "Resting potential (no pending impulses)"
    fi
fi

# ── Step 3: Push to golgiBody-ext (ionic bond outward) ───────────────
#
# SSH to golgiBody-ext and trigger a pull from Forgejo. The outer
# membrane then pushes to GitHub (extracellular weak bond).

log "Relaying to golgiBody-ext (outer membrane)..."

ssh -o ConnectTimeout=5 -o BatchMode=yes "$GOLGI_EXT_HOST" \
    "cd /opt/ecoPrimals/infra/wateringHole && git pull --ff-only origin main --quiet 2>/dev/null; \
     /opt/ecoPrimals/infra/wateringHole/hooks/forgejo/ext-github-push.sh 2>&1" \
    2>/dev/null && {
    log "Relay to golgiBody-ext complete"
} || {
    log "WARN: relay to golgiBody-ext failed — GitHub mirror may lag"
}

log "=== Sync relay finished ==="
