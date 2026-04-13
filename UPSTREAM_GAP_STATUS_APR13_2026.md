# Upstream Gap Status — April 13, 2026

**Source**: primalSpring Phase 41 gap registry (`docs/PRIMAL_GAPS.md`)
**Context**: Post-pull review of all 12 core primals + biomeOS after pre-downstream gap resolution sprint.

---

## Resolved This Sprint (12 items)

| Gap | Primal | Version | How |
|-----|--------|---------|-----|
| `inference.register_provider` wire method | Squirrel | alpha.49 | 5 wire tests, real handler path |
| Stable ecoBin binary | Squirrel | alpha.49 | 3.5MB static-pie, stripped, BLAKE3 |
| Ionic bond lifecycle (`crypto.ionic_bond.seal`) | BearDog | Wave 42 | propose→accept→seal, Ed25519, TTL |
| BTSP server endpoint (`btsp.server.*`) | BearDog | Wave 36 | 4 wire methods + session store |
| `health.check` accepts empty params | loamSpine | deep debt | `#[serde(default)]`, null→{} normalization |
| `EVENT_TYPE_REFERENCE.md` | rhizoCrypt | S40 | Canonical 27-variant spec |
| `capability.call` gate routing | biomeOS | v3.05 | Explicit error on unregistered gate |
| `--port` in api/nucleus modes | biomeOS | v3.05 | TCP alongside UDS for mobile |
| biomeOS DOWN during testing | biomeOS | v3.05 | Neural API co-launch in Nucleus Full |
| LD-10 BTSP guard line consumed | barraCuda | Sprint 42 | Replay consumed line |
| LD-05 TCP AddrInUse | barraCuda | Sprint 42 | Eliminated TCP sidecar in UDS mode |
| NG-08: Eliminate `ring` from production | NestGate | Session 43 | reqwest→ureq 3.3 + rustls-rustcrypto, pure Rust TLS |

---

## Remaining Open (11 items — zero high priority)

### Medium

| Gap | Owner | Notes |
|-----|-------|-------|
| BC-07: `SovereignDevice` into `Auto::new()` fallback | barraCuda | Possibly resolved Sprint 41 — needs verification |
| BC-08: `cpu-shader` default-on | barraCuda | Feature flag required, most compositions CPU-only |
| CR-01: `deny.toml` C/FFI ban list | coralReef | Most likely to pull GPU C deps |
| Multi-stage ML pipeline `shader.compile.wgsl` | coralReef | Wire contract delivered, pipeline untested |
| `storage.retrieve` for large/streaming tensors | NestGate | OPEN |
| Cross-spring persistent storage IPC | NestGate | OPEN |

### Low

| Gap | Owner | Notes |
|-----|-------|-------|
| `plasma_dispersion` feature-gate bug | barraCuda | neuralSpring-specific |
| 29 shader absorption candidates | barraCuda | neuralSpring pipeline |
| RAWR GPU kernel (CPU-only) | barraCuda | groundSpring-specific |
| Batched `OdeRK45F64` for Richards PDE | barraCuda | airSpring-specific |
| IPC timing for `shader.compile` | coralReef | Deployment timing |
| ~~Signed capability announcements~~ | BearDog | **RESOLVED** Wave 45 (SA-01, unified Ed25519 identity, schema_version 2) |

---

## Primal Health Summary (April 13, 2026)

| Primal | Version | Tests | Status |
|--------|---------|-------|--------|
| barraCuda | Sprint 42 Phase 6 | 3,834 pass (15 env-sensitive) | READY |
| BearDog | Wave 46 | 14,784 pass | READY |
| coralReef | Iter 80 | 169 pass (1 env-sensitive) | READY |
| loamSpine | deep debt pass 6 | 1,034 pass | READY |
| rhizoCrypt | S42 | 35 pass | READY |
| Songbird | Wave 137 | up to date | READY |
| NestGate | Session 43g | 291 pass (26 ignored) | READY (NG-08 resolved) |
| petalTongue | current | up to date | READY |
| Squirrel | alpha.51 | 735 pass | READY |
| sweetGrass | current | up to date | READY |
| toadStool | S203 | up to date | READY |
| biomeOS | v3.06 | 72 pass (1 env-sensitive) | READY |

**None of the remaining gaps block local primalSpring work or benchScale integration.**

---

**License**: CC-BY-SA 4.0
