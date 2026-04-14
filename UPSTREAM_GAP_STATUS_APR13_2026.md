# Upstream Gap Status — April 13, 2026

**Source**: primalSpring Phase 41 gap registry (`docs/PRIMAL_GAPS.md`)
**Context**: Post-pull review of all 12 core primals + biomeOS after pre-downstream gap resolution sprint.

---

## Resolved This Sprint (20 items)

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
| BC-07: `SovereignDevice` `Auto::new()` fallback | barraCuda | Sprint 41 | 3-tier: wgpu GPU → CPU → SovereignDevice IPC |
| BC-08: `cpu-shader` default-on | barraCuda | Sprint 40 | Default feature, ecoBin computes without wgpu |
| BC-09: `--port` Docker TCP bind | barraCuda | Sprint 42 | `resolve_bind_host()` respects `BARRACUDA_IPC_HOST` for cross-container TCP |
| CR-01: `deny.toml` C/FFI ban list | coralReef | Iter 79 | ecoBin v3 ban, cudarc behind feature gate |
| Multi-stage ML pipeline `shader.compile.wgsl` | coralReef | Iter 80+ | 6 end-to-end tests, CompilationInfo IPC |
| Signed capability announcements (SA-01) | BearDog | Wave 45 | Ed25519 signed attestation on discover + register |
| `plasma_dispersion` feature-gate bug | barraCuda | Sprint 40 | Corrected to dual feature gate |
| CR-02: CLI bind gap (`--bind` / `CORALREEF_IPC_HOST`) | coralReef | Iter 80 | `--bind` flag + `CORALREEF_IPC_HOST` env var; `0.0.0.0` for Docker/benchScale |
| SQ-04: `--port` TCP bind hardcoded to 127.0.0.1 | Squirrel | alpha.52 | `--bind` CLI flag + `SQUIRREL_BIND`/`SQUIRREL_IPC_HOST` env vars. Docker: `--bind 0.0.0.0` |

---

## Remaining Open (6 items — zero high priority)

### Medium

| Gap | Owner | Notes |
|-----|-------|-------|
| `storage.retrieve` for large/streaming tensors | NestGate | OPEN |
| Cross-spring persistent storage IPC | NestGate | OPEN |
| ~~`TensorSession`/`BatchGuard` adoption by springs~~ | ~~barraCuda~~ | **RESOLVED** — Sprint 40 renamed, migration guide in BREAKING_CHANGES.md, Sprint 42 `tensor.batch.submit` IPC |

### Low

| Gap | Owner | Notes |
|-----|-------|-------|
| 29 shader absorption candidates | barraCuda | neuralSpring pipeline |
| ~~RAWR GPU kernel (CPU-only)~~ | ~~barraCuda~~ | **RESOLVED** — GPU shader `rawr_weighted_mean_f64.wgsl` + `RawrWeightedMeanGpu` exist |
| Batched `OdeRK45F64` for Richards PDE | barraCuda | airSpring-specific |

---

## Primal Health Summary (April 13, 2026)

| Primal | Version | Tests | Status |
|--------|---------|-------|--------|
| barraCuda | Sprint 42 Phase 8 | 4,393 pass (14 skipped) | READY |
| BearDog | Wave 47 | 37 pass | READY |
| coralReef | Iter 80 | 4,506 pass (153 hw-gated) | READY — `--bind` flag for benchScale |
| loamSpine | deep debt pass 6 | 1,034 pass | READY |
| rhizoCrypt | S42 | 35 pass | READY |
| Songbird | Wave 137 | up to date | READY |
| NestGate | Session 43g | 291 pass (26 ignored) | READY (NG-08 resolved) |
| petalTongue | current | up to date | READY |
| Squirrel | alpha.52 | 7,003 pass | READY — SQ-04 resolved (`--bind` flag for Docker TCP); 9 files smart-refactored, hardcoding eliminated |
| sweetGrass | current | up to date | READY |
| toadStool | S203 | up to date | READY |
| biomeOS | v3.15 | 7,784+ pass | READY — zero C deps (serde-saphyr), TCP cross-arch, dead code evolved, agnostic naming |

**None of the remaining gaps block local primalSpring work or benchScale integration.**

---

**License**: CC-BY-SA 4.0
