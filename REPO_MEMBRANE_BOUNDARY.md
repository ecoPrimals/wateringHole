<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Repo Membrane Boundary — Git Host Classification

**Date**: May 17, 2026
**Status**: Active
**Authority**: WateringHole Consensus
**Related**: `SOVEREIGNTY_STANDARDS.md`, `MEMBRANE_CHANNEL_ARCHITECTURE.md`

---

## Purpose

This document classifies every ecoPrimals repository by its membrane
boundary — where it should live (inner membrane only, dual-push, or
outer membrane only) and why. The classification drives push policy,
CI strategy, and contamination prevention.

---

## Membrane Model

| Layer | Git Host | Trust | Push Policy |
|-------|----------|-------|-------------|
| **Inner membrane** | Forgejo (`git.primals.eco:3000`) | Covalent — full trust, private by default | `git push forgejo` only |
| **Dual-push** | Forgejo primary + GitHub mirror | Controlled — Forgejo canonical, GitHub for public visibility | `git push forgejo && git push origin` |
| **Outer membrane** | GitHub only | Observed — public archive, CDN, Pages | `git push origin` only |

---

## Repository Classification

### Inner Membrane Only (Forgejo-only)

These repos contain operational data, credentials, or sensitive
infrastructure details that must not exist on external substrate.

| Repo | Org | Content | Rationale |
|------|-----|---------|-----------|
| `cellMembrane` | sporeGarden | VPS deployment, SSH key mgmt, TURN credentials, RustDesk keys | Operational secrets — inner membrane only |
| *(future)* | — | Any new credential/secret/operational repos | Default to inner-only for ops repos |

**Current gap**: `cellMembrane` is currently private on GitHub. It
should be moved to Forgejo-only once Forgejo is operationally primary.
See "Decision: cellMembrane" below.

### Dual-Push (Forgejo Primary, GitHub Mirror)

Public code repos where Forgejo is the source of truth and GitHub
provides external visibility, CDN, and community access.

**Gardens (sporeGarden org):**

| Repo | GitHub Visibility | Content |
|------|-------------------|---------|
| `projectNUCLEUS` | Public | Sovereignty layer, deployment infrastructure |
| `projectFOUNDATION` | Public | Knowledge layer, thread lineage, validation evidence |
| `lithoSpore` | Public | Verification chassis, USB-deployable validation |
| `esotericWebb` | Public | UI/agentic interaction layer |

**Springs (syntheticChemistry org):**

| Repo | GitHub Visibility | Content |
|------|-------------------|---------|
| `primalSpring` | Public | Coordination spring, composition validation |
| `wetSpring` | Public | Breseq/LTEE science validation |
| `hotSpring` | Public | GPU compute validation |
| `groundSpring` | Public | Geospatial validation |
| `airSpring` | Public | Atmospheric/ADS-B validation |
| `neuralSpring` | Public | Neural/AI validation |
| `ludoSpring` | Public | Game engine validation |
| `healthSpring` | Public | Health/clinical validation |

**Primals (ecoPrimals org):**

| Repo | GitHub Visibility | Content |
|------|-------------------|---------|
| `bearDog` | Public | Security, crypto, BTSP identity |
| `songBird` | Public | Discovery, routing, federation |
| `toadStool` | Public | Compute dispatch |
| `nestGate` | Public | Storage, content serving |
| `squirrel` | Public | AI/MCP orchestration |
| `rhizoCrypt` | Public | Provenance DAG |
| `loamSpine` | Public | Provenance spine |
| `sweetGrass` | Public | Provenance braid |
| `biomeOS` | Public | Orchestration layer |
| `petalTongue` | Public | Storytelling/UI bridge |
| `skunkBat` | Public | Defense/audit |
| `barraCuda` | Public | GPU compute dispatch |
| `coralReef` | Public | Distributed compute mesh |
| `bingoCube` | Public | Validation framework |
| `sourDough` | Public | Starter culture/bootstrap |

**Infrastructure (ecoPrimals org):**

| Repo | GitHub Visibility | Content |
|------|-------------------|---------|
| `plasmidBin` | Public | Binary depot, deploy scripts |
| `wateringHole` | Public | Ecosystem standards/docs |
| `whitePaper` | Public | Research documentation |

### Outer Membrane Only (GitHub-only)

Repos that exist solely for external visibility and don't need
inner membrane presence.

| Repo | Org | Content | Rationale |
|------|-----|---------|-----------|
| `fossilRecord` | ecoPrimals | Archived documentation | Public archive — no development, read-only fossil record |
| `sporePrint` | ecoPrimals | GitHub Pages deployment | Generated site — the deployment target IS GitHub Pages |

---

## Contamination Risk Matrix

| Risk | Vector | Repos Affected | Mitigation |
|------|--------|----------------|------------|
| API keys pushed to GitHub | Accidental `git add` of `.env` files | All primals, especially `squirrel` | `.gitignore` patterns cover `.env`, `*.env`, `.env.*` — verified ecosystem-wide |
| Operational secrets on GitHub | `cellMembrane` is on GitHub (private) | `cellMembrane` | Move to Forgejo-only (pending decision) |
| Local experiments leak to GitHub | Developer pushes WIP with sensitive data | Any repo | Pre-push hook checking for sensitive patterns (future) |
| Forgejo/GitHub divergence | Forgetting dual-push, one host falls behind | All dual-push repos | `forgejo_mirror.sh --push-all` periodic sweep |

### .env Audit Summary (May 17, 2026)

| File | Git-Tracked | Content | Risk |
|------|-------------|---------|------|
| `squirrel/.env` | No (gitignored) | JWT_SECRET | None — local only |
| `squirrel/mcp-config.env` | No (gitignored) | OpenAI/Anthropic/HuggingFace API keys | None — local only |
| `bearDog/production.env` | Yes | Template config (no real secrets) | None — placeholder values |
| `songbird/config/production.env` | No (gitignored) | Template DB URL with placeholder password | None — local only |
| `hotSpring/metalForge/*.env` | Yes | GPU/hardware config | None — no secrets |
| `plasmidBin/ports.env` | Yes | Port assignments | None — no secrets |
| `ecoPrimals/.env.test` | Yes | Test env vars (RUST_LOG, timeouts) | None — no secrets |

---

## Forgejo Operational Status

### Current Reality (May 2026)

Forgejo is **declared primary** but **operationally secondary**:

- Every local clone has `origin` → `github.com` — no `forgejo` remote
- `forgejo_mirror.sh` exists but hasn't been run on dev machines
- No automatic sync — dual-push is policy, not enforcement
- All CI runs on GitHub Actions (`notify-sporeprint.yml`, etc.)
- Forgejo is reachable at `git.primals.eco:3000` behind tunnel

### Migration Path

1. **Current**: GitHub-only development, Forgejo aspirational
2. **Near-term**: Run `forgejo_mirror.sh` to add `forgejo` remotes,
   begin dual-push for active repos
3. **Mid-term**: Port `notify-sporeprint.yml` to Forgejo Actions,
   validate CI parity
4. **Long-term**: Forgejo becomes true primary, GitHub auto-mirrored
   via post-receive hook or Forgejo's built-in mirror

---

## Decision: cellMembrane Placement

**Context**: `cellMembrane` is the only private repo in the
`sporeGarden` GitHub org. It contains VPS IP addresses, SSH key
management procedures, TURN credential paths, and RustDesk key
material. Its `.gitignore` correctly excludes `.age`, `.pem`, `id_*`,
`.key`, and token files.

**Options**:

1. **Forgejo-only** (recommended): Remove from GitHub entirely. All
   access via Forgejo tunnel. Cleaner sovereignty posture — ops data
   never touches external substrate.

2. **Keep GitHub private**: Convenient for cross-machine pulls without
   tunnel. Relies on GitHub's private repo access controls.

**Recommendation**: Move to Forgejo-only when Forgejo is confirmed
operationally stable (reachable, backups working). Until then, GitHub
private is acceptable as a transitional state.

---

## Push Policy Enforcement

### Manual (current)

```bash
# Dual-push workflow
git push forgejo main
git push origin main

# Or use forgejo_mirror.sh for batch
FORGEJO_TOKEN=<token> bash forgejo_mirror.sh --push-all
```

### Automated (future)

A pre-push hook can enforce the membrane boundary:

```bash
# .git/hooks/pre-push (inner-only repos)
remote="$1"
if [[ "$remote" == "origin" ]]; then
  echo "ERROR: This repo is inner-membrane-only. Push to forgejo instead."
  exit 1
fi
```

A Forgejo post-receive hook can auto-mirror to GitHub for dual-push
repos, eliminating the need for manual dual-push.

---

## Cross-References

- `SOVEREIGNTY_STANDARDS.md` — Forgejo as Primary Git Host section
- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — Physical channel architecture
- `projectNUCLEUS/deploy/forgejo_mirror.sh` — Dual-push tooling
- `CELLMEMBRANE_FIELDMOUSE_DEPLOYMENT.md` — fieldMouse VPS specification
- `cellMembrane/README.md` — Operational repo documentation

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-17 | Initial version — repo membrane boundary classification from infrastructure review |
