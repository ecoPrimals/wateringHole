# primalSpring Post-Interstadial: Downstream Absorption Handoff

**Date**: 2026-05-10
**From**: primalSpring (ecosystem coordination)
**For**: projectNUCLEUS, all 8 spring teams, garden teams, downstream deployers
**Phase**: 60+ POST-INTERSTADIAL — zero open upstream gaps

---

## Purpose

This handoff captures the current state of primalSpring's eukaryotic evolution,
the resolution of all upstream gaps identified by projectNUCLEUS, and specific
guidance for downstream teams to absorb, evolve, and compose. It supersedes the
gap-tracking portions of the May 9 handoffs (now archived in
`handoffs/archive/post_interstadial_may2026/`).

---

## 1. What Changed Since May 9

### All upstream gaps resolved

| ID | What | Resolution |
|----|------|------------|
| JH-11 | Cross-primal token federation | bearDog Wave 99 `auth.public_key` (Ed25519 key distribution) + biomeOS v3.51 `BearDogVerifier` (IPC-based cross-primal verification) |
| GAP-03 | Cell graph live deploy not tested | biomeOS v3.51 `composition.deploy` route alias for `graph.execute` |
| GAP-06 | No UDS transport (rhizoCrypt) | rhizoCrypt S66 confirms UDS operational since S23, provenance trio integration test added |
| GAP-09 | Neural API registration endpoint | biomeOS v3.51 `method.register` endpoint for spring method registration |
| GAP-12 | ludoSpring IPC method registration | 28 `game.*` methods registered in primalSpring canonical registry (413 total, zero drift) |
| U1 | Stale CHECKSUMS | Regenerated with 25 tracked files, BLAKE3, `2026-05-10` |
| U2 | Doctest failure in scenarios | `ScenarioRegistry::new()` + `scenario.meta.id` fix, all 11 doctests pass |
| U3 | Scenario registry docs stale | Updated to reflect instance-method API |

### All 7 Tier 3 code quality items resolved

| Item | Owner | Resolution |
|------|-------|------------|
| coralReef tracing unification | coralReef | Switched to `#[instrument]` spans, `tracing::warn!` throughout |
| barraCuda `unwrap()` in IPC | barraCuda | `context()` / `map_err()` in all 5 network-touching modules |
| nestGate `unwrap()` in content paths | nestGate | Error propagation via `StorageError` enum |
| biomeOS mock isolation | biomeOS | `MockPrimalClient` behind `#[cfg(test)]`, no production leak |
| bearDog HSM feature-gate | bearDog | `#[cfg(feature = "hsm")]` on all PKCS#11 paths |
| petalTongue `#[allow]` reasons | petalTongue | Replaced with `#[expect(reason = "...")]` throughout |
| squirrel test split | squirrel | Large test files split into per-module `tests/` structure |

### Sovereignty horizons shipped

| Domain | What shipped | Who |
|--------|-------------|-----|
| TLS termination | rustls X.509, per-IP sliding-window rate limiter | bearDog Wave 100 (H2-10/H2-11) |
| NAT traversal | STUN wire-compliant, RFC 5766 TURN client, Cloudflare DDNS, 5-tier `ConnectionFallbackChain` | songbird Wave 196-197 (H2-13–H2-16) |
| Web sovereignty | `--docroot`, `WebServeConfig`, `--ipc`, `--workers`, NestGate content backend | petalTongue PT-1–PT-5, PT-13 |
| Notebook rendering | `.ipynb` → HTML with `metadata.title` + `strip_sources` | petalTongue |
| Token forwarding | `_bearer_token` propagated through all capability routing paths | biomeOS v3.50 |
| Composition status | `composition.status` → `{ active_users, primal_health, resource_pressure }` | biomeOS v3.51 |

---

## 2. primalSpring as Eukaryotic Exemplar

primalSpring v0.9.25 is the reference implementation for what every spring
should look like after completing eukaryotic evolution. All 8 springs have
completed this transition.

### Architecture

```
primalspring (UniBin)
├── certify     — run certification layers (absorbed guidestone)
├── validate    — execute validation scenarios
├── serve       — start JSON-RPC server
├── status      — report health/version/capabilities
└── version     — print version and build metadata
```

### Key metrics

| Metric | Value |
|--------|-------|
| Tests | 680 (632 passed + 48 ignored) |
| Clippy warnings | 0 |
| TODO/FIXME/HACK | 0 |
| Registered methods | 413 (canonical, zero drift) |
| Deploy graphs | 74 (TOML DAG format) |
| Experiments | 89 across 20 tracks |
| Certification layers | 8 (bare → cellular deployment) |
| Validation scenarios | `ScenarioRegistry` with `ScenarioMeta` (Tier 1 Rust + Tier 2 Live) |
| Tracked checksums | 25 files (BLAKE3) |
| `unsafe` code | Forbidden |
| `Result<_, String>` | Zero in production paths |
| `#[allow]` without reason | Zero (all `#[expect(reason = "...")]`) |

### Patterns to absorb

1. **`CompositionContext`** — modern API for primal discovery, IPC calls, and
   authenticated calls. Replaces `PrimalClient` / `AtomicHarness` / `discover_primal()`.
   `PrimalClient` is internal plumbing encapsulated inside `CompositionContext`.

2. **Two-tier validation** — Tier 1 scenarios are pure Rust structural checks
   (run in CI, `cargo test`). Tier 2 scenarios require live primals and test
   behavioral composition (run by NUCLEUS deployers).

3. **Scenario registry** — `validation/scenarios/` with `ScenarioMeta` (id,
   track, tier, description) and `ScenarioRegistry::new().filter_by_tier()`.

4. **Certification organelle** — `certification/` module with layered checks,
   replacing the standalone `guidestone` binary.

5. **Fossil record** — `fossilRecord/` with dated provenance READMEs preserving
   historical code/docs when superseded by modern patterns.

6. **Deploy graphs** — TOML DAGs in `graphs/` describing primal composition
   dependencies for `composition.deploy(graph)`.

---

## 3. Guidance for projectNUCLEUS

### What to absorb now

- **`composition.deploy(graph)`** — biomeOS v3.51 ships the route. Transition
  from `deploy.sh` → systemd to graph-driven germination. Use primalSpring's
  `graphs/fragments/{tower,node,nest}_atomic.toml` as templates.

- **`composition.status`** — biomeOS v3.51 provides `{ active_users,
  primal_health, resource_pressure }`. Wire into your monitoring/dashboard.

- **`method.register`** — biomeOS v3.51 enables dynamic method registration.
  New spring methods no longer need manual biomeOS configuration.

- **JH-11 token federation** — bearDog `auth.public_key` gives any primal
  Ed25519 key distribution. biomeOS `BearDogVerifier` provides IPC-based
  cross-primal token verification. `CompositionContext::call_authenticated()`
  threads bearer tokens through multi-capability graphs.

### Tier 4 rewiring (now unblocked)

JH-11 resolution unblocks Tier 4: IPC-first defaults for all inter-primal
communication. Springs should:
1. Add `barracuda` as `optional = true` with IPC-first default
2. Feature-gate any remaining library imports behind `#[cfg(feature = "local")]`
3. Wire `CompositionContext` for all cross-primal calls

### JH-5 audit forwarding (now unblocked)

skunkBat Phase 2 (local event instrumentation) is complete — all 7 event kinds
emit from live code paths. Phase 3 (forwarding via authenticated cross-primal
IPC to rhizoCrypt DAG + sweetGrass braid) is now unblocked. Every spring
should wire skunkBat into their deploy graphs now.

---

## 4. Guidance for Spring Teams

### All 8 springs: completed eukaryotic evolution

| Spring | Status | Key metric |
|--------|--------|-----------|
| primalSpring | v0.9.25, 680 tests, 413 methods, exemplar | Reference implementation |
| hotSpring | v0.6.32, 999+ tests, interstadial complete | Precision mixing validated |
| ludoSpring | v0.58, game math stable, 18 `game.*` registered | Tier 4 targeting |
| groundSpring | v0.58+, 16 MCP + 6 sync tests | MCP reference |
| neuralSpring | v0.82+, neural methods cross-synced | AI pipeline reference |
| healthSpring | v1.0+, 1,002 tests, CI cross-sync | Healthcare compliance reference |
| wetSpring | v3.46+, spectral/biodiversity validated | Environmental science reference |
| airSpring | v0.3+, atmospheric models | AWS-dependency cleanup target |

### What to do next

1. **Absorb `composition.status`** — wire into your health/monitoring paths
2. **Absorb `method.register`** — register spring-specific methods dynamically
3. **Target Tier 4 rewiring** — JH-11 is resolved; begin IPC-first migration
4. **Wire skunkBat audit logging** — prepare for JH-5 forwarding
5. **CI cross-sync** — validate local capability methods against primalSpring
   canonical 413 (`config/capability_registry.toml`)

### For airSpring specifically

Workspace-root `deny.toml` is still missing (only sub-crate deny files exist).
Add `aws-lc-sys` to the explicit ban list for Pure Rust alignment.

---

## 5. Composition Patterns for neuralAPI Deployment

### From systemd to graph-driven

```
Current:  deploy.sh → systemd → per-primal env vars → health polling
Target:   graph.toml → biomeOS composition.deploy(graph) → germinate → wire → health
```

### Deploy graph anatomy (from primalSpring exemplar)

```toml
# graphs/fragments/tower_atomic.toml
[composition]
name = "tower_atomic"
description = "BearDog + Songbird = Pure Rust HTTPS"

[[nodes]]
primal = "beardog"
capabilities = ["crypto.sign", "crypto.hash", "crypto.encrypt"]
health = "beardog.status"

[[nodes]]
primal = "songbird"
capabilities = ["tls.handshake", "discovery.mdns", "nat.traverse"]
health = "songbird.status"
depends_on = ["beardog"]

[[edges]]
from = "songbird"
to = "beardog"
via = "crypto.sign"
```

### neuralAPI routing chain

```
Caller → Neural API → capability discovery → primal routing → IPC dispatch → response
```

- Layer 1: Primals advertise capabilities at startup
- Layer 2: biomeOS Neural API indexes capabilities and maintains routing table
- Layer 3: Callers use `capability.call("domain", "method")` — never primal names
- Layer 4: biomeOS dispatches to the best available provider

### Resource envelope pattern

Every dispatch path supports resource envelopes:
```json
{
  "method": "compute.dispatch",
  "params": {
    "shader": "lattice_qcd_hmc",
    "envelope": {
      "timeout_ms": 30000,
      "mem_mb": 2048,
      "cpu_cores": 4
    }
  }
}
```

biomeOS enforces limits. ToadStool respects them. Springs compose with them.

---

## 6. Future Horizon (Not Blocking)

These items are hardening targets for the next stadial gate. None block current
interstadial goals.

| Item | Owner | Notes |
|------|-------|-------|
| Tor relay integration | songbird | Embedded Tor client for onion-routed federation |
| QUIC multi-path | songbird | Multi-path QUIC for redundant connectivity |
| Full `cloudflared` orchestration | songbird | Auto-managed Cloudflare tunnels |
| TURN refresh lifecycle | songbird | Long-lived relay session management |
| Plasmodium (multi-gate) | biomeOS | Cross-gate NUCLEUS bonding |
| PrimalClient full elimination | all springs | Tier 4 rewiring completes this |

---

## 7. Key File References

| What | Path |
|------|------|
| Canonical method registry | `primalSpring/config/capability_registry.toml` (413 methods) |
| Gap tracker (all resolved) | `primalSpring/docs/PRIMAL_GAPS.md` |
| Cross-spring scorecard | `primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` |
| Deploy graph fragments | `primalSpring/graphs/fragments/*.toml` |
| Scenario registry | `primalSpring/ecoPrimal/src/validation/scenarios/` |
| Certification organelle | `primalSpring/ecoPrimal/src/certification/` |
| NUCLEUS composition tools | `primalSpring/tools/composition_nucleus.sh` |
| Ecosystem evolution model | `infra/wateringHole/ECOSYSTEM_EVOLUTION_CYCLE.md` |
| Spring audit (7-dimension) | `infra/wateringHole/SPRING_NUCLEUS_AUDIT_MAY2026.md` |
| Archived closure handoffs | `infra/wateringHole/handoffs/archive/post_interstadial_may2026/` (19 files) |

---

*This handoff is the single downstream-facing document for the May 10, 2026
post-interstadial state. All gaps resolved. All sovereignty horizons advancing.
The ecosystem is ready for Tier 4 rewiring and JH-5 audit forwarding.*
