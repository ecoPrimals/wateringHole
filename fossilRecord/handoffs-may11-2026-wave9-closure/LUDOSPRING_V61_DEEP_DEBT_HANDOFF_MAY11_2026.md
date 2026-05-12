# SPDX-License-Identifier: AGPL-3.0-or-later

# ludoSpring V61 — Deep Debt Resolution Handoff (May 11, 2026)

**From:** ludoSpring V61 (854 tests, 8 scenarios, zero clippy, zero unsafe)
**For:** primalSpring, barraCuda, sibling springs, projectNUCLEUS, foundation

---

## What changed (V60→V61)

1. **29 new constant-invariant tests** across 8 files:
   - 7 `tolerances/` modules (game, interaction, gpu, ipc, metrics, procedural, validation)
   - `certification/constants.rs` golden value verification
   - Tests validate: formula parity (Fitts/Hick/sigmoid vs. analytical), range invariants,
     ordering relationships (strict < analytical < noise coherence), base64 payload decode

2. **Hardcoded source strings evolved:** `skunkbat.rs` audit functions now use
   `crate::niche::NICHE_NAME` instead of literal `"ludospring"` — pattern for all springs

3. **PRIMAL_GAPS.md reconciled:**
   - GAP-12 (registry cross-sync 15 methods) → **RESOLVED V59** (28 game.* canonical, 413 total)
   - GAP-13 (barraCuda 0.3.13 build regression) → **RESOLVED V57** (gpu feature gate fix)
   - GAP-15 (gaming_niche missing Squirrel node) → **RESOLVED V56** (Squirrel added)
   - Remaining open: GAP-01 (coralReef partial), GAP-02 (flow IPC surface partial),
     GAP-04 (TensorSession partial), GAP-05 (provenance trio overlay), GAP-14 (low)

4. **854 workspace tests**, zero clippy warnings, zero fmt diffs, all files <800 lines

---

## Deep audit results (ecosystem patterns)

### What ludoSpring demonstrates as resolved at scale

| Category | Status | Pattern for adoption |
|----------|--------|---------------------|
| `unsafe` code | **Zero** (`#![forbid(unsafe_code)]`) | All springs should adopt workspace-level forbid |
| `TODO`/`FIXME`/`HACK` | **Zero** | Move to tracked issues or remove |
| Bare `#[allow()]` | **Zero** (all have `reason`) | Use `#[allow(..., reason = "...")]` or `#[expect]` |
| Mocks in production | **Zero** (all in `#[cfg(test)]`) | Production paths must be complete implementations |
| Files >800L | **Zero** (largest: `params.rs` at 758L) | Split when domain boundaries are natural |
| External C deps | **Zero in default builds** (`wgpu` optional behind `gpu` feature) | ecoBin compliant |
| Hardcoded primal names | **Zero** (capability-first discovery, `NICHE_NAME` for self-identity) | Pattern: `crate::niche::NICHE_NAME` |
| Hardcoded socket paths | **Zero in production** (test-only temp dirs) | Use discovery tiers |

### Dependency evolution path

| Dependency | Current | Evolution |
|------------|---------|-----------|
| `wgpu` | Optional, `gpu` feature only | → coralReef IPC when sovereign shader compiler matures |
| `tarpc` | Optional, `tarpc-ipc` feature | Keep as alternative to JSON-RPC |
| `barracuda` | Optional, `local` feature | IPC-first default achieved; library is opt-in fallback |
| `primalspring` | Optional, `guidestone` feature | Pinned v0.9.25 for composition API |

---

## For primalSpring

- **Registry drift:** Zero. All 28 `game.*` methods + health methods validated against 413 canonical.
  Bidirectional CI cross-sync test ensures this stays green.
- **Pattern to absorb:** Constant-invariant testing for tolerance modules — validates that
  centralized constants maintain expected mathematical relationships. Catches drift at compile time.
- **`NICHE_NAME` pattern:** All springs should derive audit/logging source identifiers from their
  niche constant, not string literals.

## For barraCuda

- **GAP-02 surface:** `math.flow.evaluate` and `math.engagement.composite` still missing from
  barraCuda's IPC surface. ludoSpring computes these locally; when available via IPC, the
  `crate::math` dual-path module routes transparently.
- **Perlin3d at lattice points:** `s_composition_gaps.rs` validates `noise.perlin3d(0,0,0) == 0.0`
  — ensure this property holds in barraCuda's implementation.
- **CPU benchmark parity:** `baselines/python/bench_cpu_parity.py` provides 4 wall-clock Python
  timings (perlin, fBm, raycaster, Fitts). Rust Criterion benchmarks in `benchmarks/` cover the
  same operations. barraCuda could absorb these as canonical CPU parity benchmarks.

## For skunkBat

- **ludoSpring now has a typed Rust IPC module** (`ipc/skunkbat.rs`): `audit_log`, `audit_session`,
  `audit_certification`, `audit_validation`, `query_audit_trail`. Graceful degradation when
  skunkBat is unreachable.
- **Query vs append:** `query_audit_trail` expects `security.audit_log` to support `since_seq` +
  `limit` query parameters. If skunkBat separates query from append, update the method name.

## For sibling springs

- **Tolerance constant-invariant tests:** Every spring has tolerance constants. Add tests that
  validate mathematical relationships between them (ordering, positivity, formula derivation).
  ludoSpring's pattern: `#[cfg(test)] #[allow(clippy::assertions_on_constants, reason = "...")]`
- **`NICHE_NAME` for audit sources:** Replace `"springname"` string literals with the niche constant.
- **PRIMAL_GAPS.md reconciliation:** Review your gap documents — many upstream gaps (GAP-06,
  GAP-12, GAP-13, JH-11) are now RESOLVED ecosystem-wide.

## For projectNUCLEUS

- Two ludoSpring workload TOMLs are gate-agnostic and ready:
  `ludospring-game-validation.toml` and `ludospring-composition-parity.toml`
- Release binary verified: `ludospring version` → 30 capabilities
- Awaiting plasmidBin publish for end-to-end NUCLEUS validation

## For foundation

- Thread 9 (Gaming/Creative) seeded:
  - 14 data sources in `data/sources/thread09_gaming.toml`
  - 13 validation targets in `data/targets/thread09_gaming_targets.toml`
  - THREAD_INDEX.toml updated: Thread 9 status → "active"

---

## Remaining evolution targets

1. **Close GAP-01:** coralReef sovereign shader compilation (currently embedded WGSL + toadStool)
2. **Close GAP-02:** barraCuda IPC surface for `math.flow.evaluate` and `math.engagement.composite`
3. **Close GAP-04:** TensorSession promotion beyond sigmoid + parity helpers
4. **Industry GPU benchmarks:** Roofline, Kokkos, MLPerf — queued in `docs/PAPER_QUEUE.md`
5. **Paper queue:** MDA (2004), Schell (2008), Bartle (1996), Deterding (2011) not yet reviewed
6. **BM-004/BM-005:** Matchmaking and chat throughput benchmarks — spec exists, not implemented

---

**License:** AGPL-3.0-or-later
