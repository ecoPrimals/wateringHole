<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V51 — Hardened Composition Patterns (Cross-Ecosystem Handoff)

**Date**: 2026-04-11
**From**: healthSpring V51 (ecoBin 0.8.0, `infra/plasmidBin/healthspring/`)
**To**: All primals, all springs, biomeOS, primalSpring

---

## Summary

healthSpring V51 adopts hardened composition patterns from `primalSpring`,
`PRIMAL_IPC_PROTOCOL.md` v3.1, and `CAPABILITY_WIRE_STANDARD`. This handoff
documents the patterns implemented so other primals and springs can adopt them.

976 tests, 89 experiments (83 science + 6 Tier 4 composition), zero clippy
warnings (pedantic+nursery), zero unsafe. barraCuda v0.3.11.

---

## Patterns Implemented (available for ecosystem adoption)

### 1. TCP + UDS Dual Transport (PRIMAL_IPC_PROTOCOL v3.1)

healthSpring's primal binary now accepts `--port <u16>` to spawn a TCP listener
alongside the primary UDS listener. `HEALTHSPRING_PORT` env var fallback.
Newline-delimited JSON-RPC 2.0 over TCP.

**Adoption path**: Every primal supporting `plasmidBin` deployment should add
`--port` to their `serve` subcommand. `metadata.toml` declares `tcp_port_default`.

### 2. Domain Symlink Discovery

On bind, healthSpring creates `health.sock` → `healthspring-{family}.sock`.
biomeOS discovers health capabilities by probing `health.sock` instead of
iterating all sockets.

**Adoption path**: Each primal creates `{domain}.sock` symlink on bind.

### 3. Capability Wire Standard Compliance

- `capabilities.list` includes top-level `methods: [string]` array
- `identity.get` returns primal metadata (name, version, domain, license,
  architecture, composition model, particle profile, proto-nucleate)
- `health.check` lightweight probe (status, primal, version, domain, uptime)
- `health.readiness` includes `status: "healthy" | "degraded"` field

### 4. LOCAL vs ROUTED Capability Registration

Capabilities are registered with biomeOS as either:
- `served_locally: true` (in-process science dispatch)
- `served_locally: false, canonical_provider: "toadstool"` (proxied)

This follows primalSpring's `niche.rs` pattern.

### 5. BTSP Client Handshake Module

Pure-Rust BTSP client handshake (4-step: ClientHello → ServerChallenge →
ClientProof → ServerAccepted). Ready for BearDog BTSP endpoint availability.
No external dependencies.

### 6. Typed IPC Clients

`PrimalClient` wraps cross-primal communication with health probe fallback
chains and capability queries. `InferenceClient` provides typed Squirrel/
neuralSpring integration. Both replace raw `rpc::send`.

### 7. Structured Discovery

`DiscoveryResult` tracks socket path + how it was found (`DiscoverySource`:
EnvOverride, CapabilityProbe, WellKnownPath, XdgSocket, NotFound).

---

## Validation Ladder (reusable pattern)

healthSpring has proven a 5-tier validation ladder:

```
Tier 0: Python control     → peer-reviewed science (DOI-cited baselines)
Tier 1: Rust CPU            → faithful port (f64-canonical, tolerance-documented)
Tier 2: GPU parity          → barraCuda WGSL (CPU vs GPU bit-identical)
Tier 3: metalForge dispatch → NUCLEUS routing (cross-substrate, PCIe P2P)
Tier 4: Primal composition  → IPC dispatch parity (JSON-RPC wire = direct Rust)
```

At Tier 4, Python and Rust both become validation targets for the composition
layer. The science doesn't change — we validate that NUCLEUS composition
patterns faithfully reproduce it through IPC dispatch.

6 composition experiments (exp112–117, 144 checks) validate this surface.

---

## Remaining Primal Gaps

| Gap | Status | Blocker |
|-----|--------|---------|
| Ionic bridge enforcement | Blocked | BearDog `crypto.ionic_bond` |
| Inference canonical namespace | Partial | primalSpring/Squirrel alignment |
| Discovery method naming | V50 dual fallback | Songbird canonical names |
| Squirrel in deploy graph | V50 optional node | Squirrel ecoBin compliance |
| BTSP endpoint availability | Client ready | BearDog BTSP server |

---

## For Each Team

| Team | Action |
|------|--------|
| **primalSpring** | Confirm `discovery.find_by_capability` as canonical Songbird method; pick canonical inference namespace (`inference.*` vs `model.*`); consider `composition_validation` crate from healthSpring exp112–117 |
| **biomeOS** | healthSpring supports TCP + UDS; domain symlink ready; deploy graph unchanged |
| **barraCuda** | `TensorSession` still blocks local shader removal; `SovereignDevice` API confirmed |
| **coralReef** | Sovereign dispatch feature flag ready; awaiting device availability |
| **neuralSpring** | Squirrel optional node in deploy graph; `inference.*` capabilities needed |
| **BearDog** | BTSP client module ready in healthSpring; awaiting server endpoint |
| **All springs** | Adopt TCP `--port`, domain symlink, `identity.get`, LOCAL/ROUTED split, typed clients |
