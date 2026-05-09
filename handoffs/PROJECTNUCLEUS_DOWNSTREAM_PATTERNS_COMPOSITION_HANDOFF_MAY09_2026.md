# projectNUCLEUS: Downstream Patterns + NUCLEUS Composition via neuralAPI

**Date**: 2026-05-09
**From**: projectNUCLEUS (sporeGarden)
**For**: Spring teams, garden teams, primalSpring, biomeOS, downstream deployers
**Phase**: 60 (enforced) — v0.9.25

---

## Summary

This handoff documents composition patterns validated by projectNUCLEUS on ironGate
that are ready for downstream absorption by spring teams, garden teams, and future
NUCLEUS deployers. It also covers the neuralAPI integration path for biomeOS-orchestrated
deployment.

---

## 1. NUCLEUS Composition via neuralAPI from biomeOS

### Current deployment model

```
deploy.sh → systemd user services → per-primal env vars → health check polling
```

13 primals deployed as systemd units. biomeOS discovers running primals via
5-tier hierarchy (Songbird IPC → Neural API → UDS → socket registry → TCP).
`composition.reload` enables hot-swap of individual primals.

### Target deployment model (neuralAPI)

```
biomeOS → Neural API → composition.deploy(graph) → germinate primals → wire capabilities
```

The deploy graph (TOML DAG) is the deployment contract. biomeOS reads the graph,
germinates primals in dependency order, waits for health, and wires capability
routes. Resource envelopes enforce limits on every dispatch path.

### What projectNUCLEUS validated

| Pattern | Status | Evidence |
|---------|--------|----------|
| 13-primal full NUCLEUS composition | Operational | All primals healthy via systemd |
| Deploy graph germination order | Validated | BearDog first → rest in any order → biomeOS last |
| `composition.reload` hot-swap | Validated | Single primal restart without full composition teardown |
| Resource envelope enforcement | Validated | biomeOS v3.48 + ToadStool S232 enforce `timeout_ms`, `mem_mb`, `cpu_cores` |
| Neural API routing (170+ translations) | Validated | biomeOS routes semantic capability queries to correct primals |
| MethodGate + ionic tokens | Enforced | 10/13 primals confirmed enforced via TCP |
| Provenance pipeline | Operational | BLAKE3 → rhizoCrypt DAG → loamSpine ledger → sweetGrass braid |

### neuralAPI integration points for pappusCast

pappusCast currently queries JupyterHub API directly for active user counts. In
the primal composition future, this routes through biomeOS:

```
pappusCast → biomeOS:composition.status → { active_users, primal_health, resource_pressure }
```

This enables multi-gate propagation: pappusCast on gate A publishes to observer
surfaces on gates A, B, and C via Songbird transport + NestGate storage.

### Deploy graph for the observer composition

```toml
# Proposed: observer_surface.toml
[composition]
name = "observer-surface"
description = "Public science surface with auto-propagation"

[[primals]]
name = "voila"
role = "presentation"
depends_on = ["nestgate"]

[[primals]]
name = "pappusCast"
role = "propagation"
depends_on = ["voila", "jupyterhub"]

[[primals]]
name = "tunnelKeeper"
role = "tunnel-health"
depends_on = ["songbird"]
```

---

## 2. Patterns for Downstream Absorption

### Pattern: Open/Gated Access Split

**What**: Separate the presentation surface (read-only, open) from the compute
surface (interactive, authenticated). Content flows one direction through a
validation gate.

**Implementation**:
```
Voila (open) ←── pappusCast (validated snapshots) ←── JupyterHub (gated)
```

**Absorb if**: You have any NUCLEUS deployment that needs to expose science
publicly while maintaining compute isolation. Applies to: sporePrint
self-hosting, institutional lab deployments, conference demos.

### Pattern: Snapshot Propagation

**What**: Replace live symlinks/mounts with validated copies. The public surface
is decoupled from active editing.

**Implementation**:
- Source: `/home/irongate/shared/abg/{commons,showcase,data,pilot,validation}/`
- Destination: `/home/irongate/shared/abg/public/` (managed copies)
- Gate: pappusCast validates before copying (Light/Medium/Heavy tiers)

**Absorb if**: You run any system where live content could break the public view.
Also applicable to: deploy graph staging, plasmidBin binary staging.

### Pattern: Adaptive Rate Limiting via User Load

**What**: Background tasks (propagation, validation, indexing) dynamically adjust
frequency based on active user count.

**Implementation**:
```python
interval = min(BASE_MINUTES * max(1, active_users), MAX_MINUTES)
```

**Absorb if**: You run batch processes alongside interactive workloads. Also
applicable to: biomeOS tick model, skunkBat anomaly detection sampling rate.

### Pattern: Multi-Tier Testing

**What**: Tier-specific test suites exercise each access level end-to-end by
running as that tier's system user.

**Implementation**:
- `sudo -u voila jupyter nbconvert --execute` (observer tier)
- `sudo -u tamison python3 -c "import Bio"` (compute tier)
- `sudo -u abgreviewer test -w /home/irongate/shared/abg/data/` (reviewer tier)

**Absorb if**: You deploy any system with multiple access levels. The test suite
doubles as documentation of what each tier can and cannot do.

### Pattern: Python → Rust → Primal Evolution

**What**: New tooling starts as Python for rapid validation, rewrites to Rust for
performance and safety, then evolves into a primal for ecosystem integration.

**Evidence from projectNUCLEUS**:
| Tool | Phase | Current State |
|------|-------|---------------|
| darkforest | Rust (Phase 2) | 939KB binary, zero deps, structured JSON output |
| pappusCast | Python (Phase 1) | Validation base, systemd service, JupyterHub API |
| tunnelKeeper | Rust (Phase 2) | Crate in validation tree, integrated into darkforest |
| security_validation.sh | Archived | Replaced by darkforest Rust binary |
| darkforest_pentest.sh | Archived | Replaced by darkforest Rust binary |
| darkforest_fuzz.py | Archived | Replaced by darkforest Rust binary |

**Absorb if**: You're building any new tooling in the ecosystem. Start Python,
validate the pattern, then pass through the Rust compiler (our DNA synthase).

### Pattern: Cloudflare as Calibration Instrument

**What**: Use Cloudflare services (tunnel, access, DNS) as baseline calibration
targets for primal sovereignty replacements.

**Evidence**:
| Cloudflare Service | Primal Replacement | Calibration Data |
|--------------------|-------------------|-----------------|
| Tunnel (cloudflared) | Songbird NAT | 270ms p50, hourly baselines |
| Access (Zero Trust) | BearDog ionic tokens | Policy structure documented |
| TLS (edge) | BearDog X.509/ACME | TTFB, Lighthouse scores |
| DNS (NS) | knot-dns + Songbird | Resolution latency, DNSSEC |

**Absorb if**: You're working on any sovereignty replacement. Never remove the
external until the primal meets or exceeds Cloudflare's baselines.

---

## 3. Experiment Learnings for Spring Teams

### Path resolution in shared environments

wetSpring notebooks in `public/` originally used relative paths
(`Path('..') / 'experiments' / 'results'`) that broke when the public directory
transitioned from symlinks to snapshot copies. Fix: use absolute paths to data
sources, or resolve paths relative to a known environment variable.

**Spring action**: If your experiments reference data via relative paths, consider
anchoring to `$SPRING_DATA_ROOT` or an absolute path. Relative paths are fragile
when notebooks move between contexts (compute, public, sporePrint).

### Kernel consistency

Notebooks must specify a kernel that exists in every context where they'll render.
The `bioinfo` kernel is compute-only; `python3` is universal. If a notebook needs
packages only in `bioinfo`, it should gracefully degrade:

```python
try:
    import Bio
    HAS_BIO = True
except ImportError:
    HAS_BIO = False
```

**Spring action**: Audit your public-facing notebooks for kernel assumptions. If
they render on Voila (observer) or sporePrint, they need the `python3` kernel.

### Metadata enforcement

All notebooks in the public surface need `metadata.title` set. Without it, Voila
shows the filename (ugly, non-descriptive). pappusCast's Light validation rejects
notebooks without titles.

**Spring action**: Add `metadata.title` to all notebooks that might render publicly.

---

## 4. River Delta — Springs That Should Absorb This Work

| Spring | What to absorb | Why |
|--------|---------------|-----|
| **primalSpring** | Observer composition graph, pappusCast primal spec | primalSpring defines composition patterns; observer split is a new pattern |
| **healthSpring** | Multi-tier testing pattern | healthSpring's `primal-proof` feature gate parallels tier-specific testing |
| **ludoSpring** | Snapshot propagation pattern | ludoSpring's game state snapshots are architecturally similar |
| **wetSpring** | Path resolution fix, kernel consistency | wetSpring notebooks are the primary content in the observer surface |
| **neuralSpring** | Adaptive rate limiting pattern | neuralSpring's inference workloads need similar load-adaptive scheduling |
| **hotSpring** | Python→Rust evolution evidence | hotSpring is mid-rewiring (Tier 2→3); darkforest is proof the pattern works |

---

## 5. Upstream Primal Debt

### For primalSpring/primalPSing audit

| Item | Severity | Description |
|------|----------|-------------|
| Deploy graph for observer composition | Medium | No graph exists for the Voila + pappusCast + tunnelKeeper composition. Should be a first-class deploy graph |
| pappusCast primal spec | Low | When pappusCast evolves to Rust, it needs a primal spec: capability domains, IPC surface, health methods |
| tunnelKeeper absorption path | Low | tunnelKeeper should absorb into songBird or become a standalone primal |
| `composition.status` method | Medium | biomeOS needs a method that returns active user count, primal health, resource pressure — for adaptive daemons |

### For petalTongue

| Item | Severity | Description |
|------|----------|-------------|
| Notebook rendering | High | PT-1 through PT-5 remain the primary blocker for Voila sovereignty replacement |
| Source stripping config | Medium | petalTongue needs configurable code visibility (strip/show) |
| Metadata-driven titles | Low | Read `metadata.title` for page headers instead of filename |

### For biomeOS

| Item | Severity | Description |
|------|----------|-------------|
| `composition.status` | Medium | Expose active user count, resource pressure, primal health for adaptive processes |
| Multi-gate propagation | Low | pappusCast on gate A should propagate to observer surfaces on gates B, C via Songbird + NestGate |

---

**The patterns are validated. The river delta carries them downstream. Each spring absorbs what fits its evolution.**
