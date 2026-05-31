#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# setup-push-mirrors.sh — Configure Forgejo → GitHub push mirrors for all repos
#
# Run on golgiBody VPS after verifying SSH access to GitHub.
# Creates push mirrors using the membrane CLI for every repo in the manifest.
# Push mirrors sync on every commit (sync_on_commit = true) and also
# periodically (interval = 8h0m0s as fallback).
#
# Prerequisites:
#   - membrane binary installed on VPS
#   - Forgejo API token configured (FORGEJO_TOKEN env or config)
#   - SSH key from golgiBody registered on GitHub
#     (Forgejo generates an Ed25519 keypair per push mirror when use_ssh=true)
#
# Usage:
#   ECOPRIMALS_ROOT=/home/git/ecoPrimals ./setup-push-mirrors.sh [--dry-run]

set -euo pipefail

ECOPRIMALS_ROOT="${ECOPRIMALS_ROOT:-/home/git/ecoPrimals}"
MANIFEST="$ECOPRIMALS_ROOT/infra/wateringHole/ecosystem_manifest.toml"
MEMBRANE_BIN="${MEMBRANE_BIN:-$(command -v membrane 2>/dev/null || echo "")}"
DRY_RUN="${1:-}"

if [[ ! -x "$MEMBRANE_BIN" ]]; then
    echo "ERROR: membrane binary not found" >&2
    exit 1
fi

if [[ ! -f "$MANIFEST" ]]; then
    echo "ERROR: manifest not found at $MANIFEST" >&2
    exit 1
fi

echo "=== Forgejo → GitHub Push Mirror Setup ==="
echo "Manifest: $MANIFEST"
echo ""

# Parse repos from manifest (org/name + github_repo)
# Uses membrane manifest.repos to get the list
REPOS=$("$MEMBRANE_BIN" manifest.repos --json 2>/dev/null | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
if isinstance(data, dict) and 'data' in data:
    data = data['data']
if isinstance(data, list):
    for r in data:
        org = r.get('org', '')
        name = r.get('name', '')
        gh = r.get('github_repo', '')
        fj = r.get('forgejo_repo', '')
        membrane = r.get('membrane', '')
        if fj and gh and membrane != 'outer-only':
            print(f'{fj}|git@github.com:{gh}.git')
" 2>/dev/null || true)

if [[ -z "$REPOS" ]]; then
    echo "Falling back to manual repo list extraction..."
    # Fallback: extract from TOML directly
    REPOS=$(python3 -c "
import tomllib, pathlib
m = tomllib.loads(pathlib.Path('$MANIFEST').read_text())
for name, r in m.get('repos', {}).items():
    org = r.get('org', '')
    gh = r.get('github_repo', '')
    fj = r.get('forgejo_repo', '')
    membrane = r.get('membrane', '')
    if fj and gh and membrane != 'outer-only':
        print(f'{fj}|git@github.com:{gh}.git')
" 2>/dev/null || true)
fi

TOTAL=0
CREATED=0
SKIPPED=0
FAILED=0

while IFS='|' read -r forgejo_repo github_url; do
    [[ -z "$forgejo_repo" ]] && continue
    TOTAL=$((TOTAL + 1))

    # Check if push mirror already exists
    EXISTING=$("$MEMBRANE_BIN" mirror.push-list "$forgejo_repo" --json 2>/dev/null | \
        python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('data',d) if isinstance(d,dict) else d))" 2>/dev/null || echo "0")

    if [[ "$EXISTING" -gt 0 ]]; then
        echo "  SKIP  $forgejo_repo (already has push mirror)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        echo "  [DRY] $forgejo_repo → $github_url"
        continue
    fi

    if "$MEMBRANE_BIN" mirror.push-create "$forgejo_repo" "$github_url" >/dev/null 2>&1; then
        echo "  OK    $forgejo_repo → $github_url"
        CREATED=$((CREATED + 1))
    else
        echo "  FAIL  $forgejo_repo → $github_url"
        FAILED=$((FAILED + 1))
    fi
done <<< "$REPOS"

echo ""
echo "=== Summary ==="
echo "Total: $TOTAL | Created: $CREATED | Skipped: $SKIPPED | Failed: $FAILED"
