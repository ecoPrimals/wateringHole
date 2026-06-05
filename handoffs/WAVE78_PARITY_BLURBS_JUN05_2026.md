# Wave 78 Parity Blurbs — Lagging Codebases

**Date**: 2026-06-05 | **Source**: eastGate overwatch ecosystem survey
**Purpose**: Copy-paste context for bringing lagging codebases to Wave 78 parity.

---

## Songbird Team — Coverage Sprint (P1)

**Gap**: 73.41% line coverage vs 90% stadial target. Largest quantitative gap
across all 14 primals. Every other primal with significant code surface is at
80%+ (bearDog 90.5%, squirrel 90.1%, sweetGrass 91.7%).

**SB-TLS-01/02**: RESOLVED — thank you. Symmetric mesh TLS origination unblocked.

**Next P0**: Wire `auth.exchange_trust` call after BTSP handshake in `mesh.init`
flow. bearDog Wave 140 delivered the endpoint. Pattern:

```rust
// After BTSP handshake succeeds, call on remote bearDog:
rpc.call("auth.exchange_trust", json!({
    "public_key": local_beardog_public_key_b64,
    "gate_id": local_node_id,
    "family_id": local_family_id,
}));
// Response includes remote_did + local_public_key — register locally
```

**Also needed**: `config/capability_registry.toml` for machine-readable capability
declaration. 7/14 primals have this. Pattern: see bearDog or biomeOS registries.

**Also**: README version/wave drift — README says v0.2.8-wave76, CHANGELOG says
v0.2.9-wave79. Sync banner.

---

## airSpring Team — Wave 78 Alignment (P2)

**Gap**: Last evolved Wave 60 (May 29) — 7 days behind Wave 78. Not on the
Wave 76/77 parity sprint. Code quality is solid (1,446 tests, zero clippy,
pedantic+nursery clean, `domain_profile.toml` present, guideStone L4).

**Ask**: Absorb Wave 76-78 trust patterns:
1. Verify `CONSUMED_CAPABILITIES` includes cross-gate trust methods
2. Absorb bearDog `auth.exchange_trust` awareness if using mesh
3. Update `docs/PRIMAL_GAPS.md` to reflect any resolved gaps from upstream
4. Bump wave marker in README/CHANGELOG

**Open gaps** (from your `docs/PRIMAL_GAPS.md`):
- AG-006: coralReef compile IPC
- AG-007: toadStool typed dispatch
- AG-009: petalTongue IPC
- AG-010: barraCuda TensorSession
- AG-011: Anderson WGSL
- AG-021: Akida NPU driver

**Priority**: LOW for mesh — airSpring is not on the critical mesh path.
Freshening pass when team capacity permits.

---

## groundSpring Team — Wave 78 Alignment (P2)

**Gap**: Last evolved Wave 63 (May 30) — 6 days behind. Code quality solid
(1,123 Rust + 455 Python tests, zero clippy, `domain_profile.toml` present,
guideStone L4).

**Ask**: Same trust pattern absorption as airSpring. Squirrel integration
already wired (Wave 63). Main work is wave marker freshening and verifying
gap registry reflects upstream resolutions.

**Priority**: LOW for mesh — groundSpring is not on the critical mesh path.

---

## hotSpring Team — Root domain_profile.toml (P2)

**Current**: L6 certified, sovereign compute reference, v0.6.32, S284.
Separate wave numbering (sovereign-compute track). Functionally the most
mature spring but uses embedded compchem profiles, not a root
`domain_profile.toml`.

**Ask**: Create root `domain_profile.toml` for ecosystem classification.
Pattern: see airSpring or wetSpring profiles. This enables `litho emit-pseudospore`
integration and ecosystem tooling discovery.

**Priority**: LOW — not blocking mesh or deployment.

---

## ludoSpring Team — Doc Freshening (P2)

**Current**: V82, Wave 76, 995 tests, guideStone L4, all 16 gaps resolved.
Composition-only spring (no spring binary in plasmidBin).

**Ask**:
1. `CONTEXT.md` stale (still says V78/982 tests) — sync with README (V82/995)
2. Create `domain_profile.toml` for ecosystem classification
3. Wave marker freshening to 78

**Priority**: LOW — ludoSpring is not on the mesh path.

---

## neuralSpring Team — domain_profile.toml + southGate (P1)

**Current**: V179, Wave 76, 930+ tests, guideStone L5, IPC-first.
southGate deployment with wetSpring.

**Ask**:
1. Create root `domain_profile.toml` (missing — pattern: airSpring/wetSpring)
2. southGate health stabilization — discovery.peers showing empty on cold starts
3. Wave marker freshening to 78

**Priority**: MEDIUM — southGate mesh stability is on the critical path for
3-gate Plasmodium collective.

---

## Primal Teams — capability_registry.toml Adoption (P2)

6 primals lack machine-readable `config/capability_registry.toml`. This file
enables primalSpring's `DOMAIN_OWNER_MAP` auto-discovery and ecosystem tooling.

**Pattern**: See `bearDog/config/capability_registry.toml` or
`biomeOS/config/capability_registry.toml`.

**Format**:
```toml
[capabilities.your_domain]
owner = "your_primal_name"
methods = [
    "your_domain.method_one",
    "your_domain.method_two",
]
```

| Primal | Priority | Notes |
|--------|----------|-------|
| songBird | MEDIUM | Has `consumed_capabilities` in code, needs TOML |
| toadStool | MEDIUM | Has `provided_capabilities` in handlers, needs TOML |
| barraCuda | LOW | Inline in `primal.rs` |
| coralReef | LOW | Self-knowledge in code |
| loamSpine | LOW | `CONSUMED_CAPABILITIES` in `niche.rs` |
| skunkBat | LOW | `CONSUMED_CAPABILITIES` in `dispatch.rs` |

---

## Coverage Sprint Candidates (Stadial Target: 90%)

| Primal | Current | Gap | Priority |
|--------|---------|-----|----------|
| songBird | 73% | -17% | P1 (largest gap) |
| barraCuda | 81% | -9% (needs real GPU) | P2 (hardware-gated) |
| nestGate | 84% | -6% | P2 |
| toadStool | 84% | -6% (hardware paths) | P2 |
| petalTongue | 85% | -5% | P2 |

---

## Summary — What Blocks Forward Progress

1. **BD-TRUST-01 mesh.init integration** (Songbird) — auto-join for 3+ gate mesh
2. **southGate health stabilization** (wetSpring/neuralSpring) — 11/13 → 13/13
3. **Caddy reverse proxy wiring** (cellMembrane/operator) — content layer functional
4. **westGate hardware** (physical — waiting on arrival)

Everything else (coverage, domain_profile.toml, registry TOML, doc freshening)
is hygiene that can happen in parallel and doesn't block mesh deployment.
