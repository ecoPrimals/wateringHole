# projectNUCLEUS: Open Observer + pappusCast + Multi-Tier Testing + tunnelKeeper

**Date**: 2026-05-09
**From**: projectNUCLEUS (sporeGarden)
**For**: primalSpring, biomeOS, petalTongue, spring teams, primalPSing audit
**Phase**: 60 (enforced) — v0.9.25

---

## Summary

projectNUCLEUS evolves from gated four-tier access to an **open observer model** with
automated content propagation. The observer surface at `lab.primals.eco` is now the
default landing page — no credentials, no login. Reviewer and user tiers are gated by
Cloudflare Access + PAM. A new `pappusCast` daemon auto-propagates validated content
from the compute workspace to the observer surface. A comprehensive multi-tier test
suite validates all access levels. A new `tunnelKeeper` Rust crate begins the
Cloudflare interaction evolution toward pure Rust.

---

## 1. Open Observer Landing

### Architecture

```
[Browser] → lab.primals.eco
         → Cloudflare Tunnel
         → voila-redirect (port 8866) → redirect / → /voila/render/Welcome.ipynb
         → voila-public (port 8867) → renders notebooks from /home/irongate/shared/abg/public/
```

The observer surface is functionally the entire project exposed but not interactable.
Notebooks are rendered read-only with source stripped. Data explorers, validation
dashboards, science showcases, and onboarding notebooks are all visible.

### What changed

| Before | After |
|--------|-------|
| 4 tiers (admin/user/reviewer/observer) all behind JupyterHub login | 3 tiers: observer=open, reviewer/user=gated |
| File browser as landing page | Welcome.ipynb as curated index |
| Source code visible on public notebooks | Source stripped, internal dirs blocked |
| No notebook metadata enforcement | All notebooks have `metadata.title` |
| Live symlinks to workspace | Managed snapshot copies (pappusCast) |

### Hardening applied

- Source stripping active (`strip_sources=True` on public Voila)
- Internal directories (`.ipynb_checkpoints`, `__pycache__`, `.pappusCast`) blocked
- Admin/hub templates return 404
- Root path redirects to Welcome.ipynb
- Dedicated `voila` system user (UID 998) for notebook execution
- Page titles set on all 15+ public notebooks

---

## 2. pappusCast — Auto-Propagation Daemon

### Concept

Named for the dandelion pappus — the parachute that carries seeds to new ground.
ABG members' work in the shared workspace auto-propagates to the static observer
surface as validated snapshots.

### Tiered validation

| Tier | Trigger | Checks |
|------|---------|--------|
| **Light** | On any file change | JSON valid, kernel available, `metadata.title` present |
| **Medium** | Periodic | Light + execute as voila user, check for cell errors |
| **Heavy** | ~6 hours | Medium + diff against previous version, changelog entry, full regression |

### Adaptive rate limiting

```
publish_interval = min(BASE_MINUTES * max(1, active_users), MAX_MINUTES)
```

Queries JupyterHub API (`list:users`, `read:users:activity`) to count active users.
More users coding → longer delay between publishes → system not overloaded.

### Snapshot architecture

`public/` holds managed copies, not live symlinks. This ensures:
- Observer surface is stable even during active editing
- Validation gate prevents broken notebooks from reaching public
- Quarantine directory isolates failures
- Changelog tracks every publication event

### State tracking

```
public/.pappusCast/
├── last_publish.json    # File states, hashes, timestamps
├── changelog.jsonl      # Publication event log
├── hub_token            # JupyterHub API token (chmod 600)
└── quarantine/          # Failed notebook copies
```

### Evolution path

```
Python daemon (now) → Rust binary → pappusCast primal
```

Phase 1 (Python) validates the pattern. Phase 2 (Rust) follows the `darkforest`
model — rewrite as a modular Rust binary with structured output. Phase 3 (primal)
integrates with biomeOS composition for multi-gate propagation and Neural API
routing.

### systemd service

`pappusCast.service` — persistent, restarts on failure, starts after JupyterHub
and Voila.

---

## 3. Multi-Tier Test Suite

### Test scripts

| Script | Tier | What it validates |
|--------|------|------------------|
| `deploy/tier_test_observer.py` | Observer | Kernel consistency, metadata titles, notebook execution as voila user, HTTP behavior (redirect, source stripping, directory blocking) |
| `deploy/tier_test_reviewer.py` | Reviewer | Read access to shared dirs, notebook parsability, no-write enforcement, no compute environment |
| `deploy/tier_test_compute.py` | Compute | Venv existence, package imports (numpy, pandas, Bio, etc.), kernelspecs, workspace permissions, notebook execution |
| `deploy/tier_test_all.sh` | All | Unified runner, summary report, pappusCast health check |

### Issues found and fixed by test suite

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Getting-Started error on observer | `bioinfo` kernel not available to `voila` user | Changed to `python3`, graceful imports |
| 8 notebooks missing `metadata.title` | Not set during creation | Programmatically added titles |
| wetspring notebooks `FileNotFoundError` | Relative paths broke after symlink→snapshot | Converted to absolute paths |
| validation-dashboard `KeyError` | Status key case mismatch (lowercase vs uppercase) | `.upper()` normalization |
| wetspring-validation-viz `ModuleNotFoundError` | `pandas`/`scipy` not in jupyterhub env | Installed into conda env |
| Compute test `biopython` import | Wrong import name | Changed to `import Bio` |

---

## 4. tunnelKeeper — Rust Cloudflare Crate

### Architecture

```
validation/tunnelKeeper/
├── Cargo.toml          (tunnel-keeper v0.1.0)
└── src/
    ├── main.rs         CLI + runner
    ├── health.rs       Tunnel health checks, DNS resolution fallback
    └── config.rs       cloudflared config.yml parsing, validation
```

### What it does

- Programmatic tunnel health checks (DNS A record → HTTP connectivity)
- DNS resolution fallback chain: `getent` → `host` → `dig`
- Config file parsing and ingress route validation
- Structured JSON health output

### Integration

Wired into darkforest pen test as A6 (Tunnel Health). tunnelKeeper binary invoked
by darkforest for automated tunnel health verification.

### Evolution

tunnelKeeper may eventually absorb into songBird (when Songbird replaces cloudflared)
or remain as a standalone tunnel management binary during the sovereignty transition.

---

## 5. Composition Patterns for Upstream

### Open observer pattern

The open/gated split is a composition pattern applicable to any NUCLEUS deployment
that exposes science publicly:

```
Voila (open, unauthenticated) → rendered notebooks → public surface
  ↕ pappusCast (validated snapshots)
JupyterHub (gated, Cloudflare Access + PAM) → interactive workspace → compute surface
```

This pattern separates the **presentation surface** (read-only, rendered) from the
**compute surface** (interactive, authenticated). Content flows one direction through
a validation gate. The observer sees the science; the user does the science.

### Snapshot propagation pattern

Replace live symlinks with validated copies. Benefits:
- Stable public surface during active editing
- Validation gate prevents broken content from reaching audience
- Quarantine isolates failures without breaking the public view
- Changelog provides audit trail

### Adaptive rate limiting pattern

System load sensing via API queries (active user count) to dynamically adjust
background task frequency. Applicable to any batch process running alongside
interactive workloads.

### Multi-tier testing pattern

Tier-specific test suites that exercise each access level end-to-end:
- Run notebooks as the tier's system user
- Verify filesystem permissions match the tier's contract
- Check HTTP behavior from the tier's perspective
- Validate that tier boundaries hold under automation

---

## 6. Upstream Primal Evolution Targets

### For petalTongue

pappusCast is a calibration instrument for petalTongue's eventual role as the
sovereign replacement for both Voila (notebook rendering) and the observer surface.
Key capabilities needed from petalTongue:

- **Notebook rendering**: Execute `.ipynb` and serve HTML output
- **Source stripping**: Configurable code visibility
- **Directory listing with exclusions**: Block internal dirs
- **Root redirect**: Configurable landing page
- **Metadata-driven titles**: Read `metadata.title` for page headers

### For biomeOS

pappusCast's adaptive rate limiting queries JupyterHub API directly. In the primal
composition future, this should route through biomeOS Neural API:

```
pappusCast → biomeOS:composition.status → active_user_count
```

This replaces the direct JupyterHub API call with a composition-aware query that
works across multiple gates (Plasmodium).

### For songBird

tunnelKeeper's health checks and config parsing are songBird's eventual responsibility.
When Songbird replaces cloudflared, tunnelKeeper's logic absorbs into Songbird's
health monitoring subsystem.

---

## 7. Existing Upstream Gaps (unchanged)

These remain tracked in `PROJECTNUCLEUS_UPSTREAM_GAPS_CONSOLIDATED_MAY08_2026.md`:

| ID | What | Owner |
|----|------|-------|
| DF-2 | ToadStool `TOADSTOOL_AUTH_MODE` env var mapping | toadStool |
| DF-3 | songbird/squirrel silent on `auth.mode` TCP | Each team |
| U1 | primalSpring `CHECKSUMS` stale | primalSpring |
| U2 | 5 deploy graphs missing `by_capability` | primalSpring |
| U3 | 8 profile graphs missing `bonding_policy` | primalSpring |
| U5 | sweetGrass port 39085 vs 9850 | sweetGrass |
| JH-11 | Cross-primal token federation | biomeOS/primalSpring |

---

## 8. File Manifest

### projectNUCLEUS (changed/new since May 8)

| File | Change |
|------|--------|
| `README.md` | Updated for open observer, pappusCast, tunnelKeeper, 3-tier model |
| `PHASES.md` | Added Step 2b section, updated status |
| `specs/EVOLUTION_GAPS.md` | Added May 9 changelog entries |
| `deploy/pappusCast.py` | **NEW** — auto-propagation daemon |
| `deploy/tier_test_observer.py` | **NEW** — observer tier test suite |
| `deploy/tier_test_reviewer.py` | **NEW** — reviewer tier test suite |
| `deploy/tier_test_compute.py` | **NEW** — compute tier test suite |
| `deploy/tier_test_all.sh` | **NEW** — unified test runner |
| `deploy/cloudflare/access_setup.sh` | **NEW** — Cloudflare Access policy setup |
| `validation/tunnelKeeper/` | **NEW** — Rust crate for tunnel management |
| `validation/darkforest/src/pentest.rs` | Updated — A6 tunnel health integration |
| `.gitignore` | Added `deploy/tier_test_results/` |

### infra/wateringHole (changed)

| File | Change |
|------|--------|
| `GLOSSARY.md` | Added pappusCast, tunnelKeeper, darkforest, snapshot architecture, tiered validation |

---

**The observer surface is open. Content propagates like dandelion seeds — validated, adaptive, and autonomous.**
