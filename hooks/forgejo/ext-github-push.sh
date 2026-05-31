#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ext-github-push.sh — golgiBody-ext GitHub push (trans face shipping)
#
# Runs on golgiBody-ext (outer membrane / trans face). Receives sync
# from peptidoglycan (ionic bond) and pushes to GitHub (weak bond).
#
# K-Derm position: outer membrane → extracellular
# Bond type: weak (passive diffusion to public internet)
#
# This is the shipping face of the Golgi apparatus — it holds the
# GitHub SSH credentials and is the only node that writes extracellularly.
#
# Called by: pepti-sync-relay.sh on peptidoglycan (via SSH)
# Can also be run manually: ./ext-github-push.sh [repo_path...]
#
# Without arguments, pushes all repos listed in the manifest that have
# github_repo configured. With arguments, pushes only those repos.

set -euo pipefail

ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-/opt/ecoPrimals}"
WATERINGHOLE="$ECOPRIMALS_ROOT/infra/wateringHole"
LOG_TAG="ext-github-push"

log() { logger -t "$LOG_TAG" "$@" 2>/dev/null || echo "[$LOG_TAG] $*"; }

# If specific repo paths given, push those; otherwise push wateringHole
if [[ $# -gt 0 ]]; then
    REPOS=("$@")
else
    REPOS=("infra/wateringHole")
fi

PUSHED=0
FAILED=0
SKIPPED=0

for repo_path in "${REPOS[@]}"; do
    local_path="$ECOPRIMALS_ROOT/$repo_path"

    if [[ ! -d "$local_path/.git" ]]; then
        log "SKIP $repo_path (not cloned on outer membrane)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    cd "$local_path"
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

    # Ensure github remote exists
    if ! git remote get-url github >/dev/null 2>&1; then
        if ! git remote get-url origin >/dev/null 2>&1; then
            log "SKIP $repo_path (no github or origin remote)"
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
        # origin on golgiBody-ext should point to GitHub
        REMOTE="origin"
    else
        REMOTE="github"
    fi

    # Check if we're ahead
    git fetch "$REMOTE" --quiet 2>/dev/null || true
    remote_ref="$REMOTE/$branch"
    if ! git rev-parse "$remote_ref" >/dev/null 2>&1; then
        log "SKIP $repo_path ($remote_ref not found)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    ahead=$(git rev-list --count "$remote_ref..HEAD" 2>/dev/null || echo "0")
    if [[ "$ahead" -eq 0 ]]; then
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    if git push "$REMOTE" "$branch" --quiet 2>/dev/null; then
        log "PUSHED $repo_path (+$ahead commits → GitHub)"
        PUSHED=$((PUSHED + 1))
    else
        log "FAIL $repo_path (push to GitHub failed)"
        FAILED=$((FAILED + 1))
    fi
done

if [[ $PUSHED -gt 0 || $FAILED -gt 0 ]]; then
    log "Summary: pushed=$PUSHED failed=$FAILED skipped=$SKIPPED"
fi
