# hotSpring v0.6.32 — Deep Debt Consolidation Handoff (May 12, 2026)

**From:** hotSpring  
**To:** primalSpring, upstream primals, sibling springs  
**Supersedes:** HOTSPRING_V0632_INTERSTADIAL_EUKARYOTIC_HANDOFF_MAY09_2026 (archive)  
**primalSpring pin:** v0.9.25  
**Test surface:** 579 (default / IPC-first) / 1,028 (barracuda-local) — zero clippy warnings

---

## What Changed Since May 11

### Code (commit 0f1adf7)

| Category | Change | Files |
|----------|--------|-------|
| **Magic number consolidation** | `CG_BACKOFF_CAP = 2000` unified from 3 local consts to `tolerances/lattice.rs` | `resident_cg.rs`, `resident_shifted_cg.rs`, `true_multishift_cg.rs` |
| **Timeout extraction** | `EMBER_ADOPT_TIMEOUT` (30 s), `EMBER_STATUS_TIMEOUT` (5 s), `GPU_POLL_INTERVAL` (200 ms), `TITAN_WARM_RECV_TIMEOUT` (120 s) | `fleet_ember.rs`, `bench/telemetry.rs`, `single_beta.rs` |
| **Path agnosticism** | `/proc/cpuinfo`, `/proc/meminfo`, `/proc/self/status` → env overrides `PROC_CPUINFO`, `PROC_MEMINFO`, `PROC_SELF_STATUS` | `bench/hardware.rs`, `bench/report.rs` |
| **Shared pattern extraction** | `BenchReport::save_and_print()` replaces duplicated discovery+save logic | `bench/report.rs`, `nuclear_eos_gpu.rs`, `sarkas_gpu.rs` |

### Docs

- `README.md`: stale historical test counts annotated, experiment table → "190 rows"
- `CHANGELOG.md`: new "Deep Debt Consolidation" unreleased section
- `PRIMAL_GAPS.md`: GAP-HS-086 (consolidation), last-audited date → May 12
- `experiments/README.md`: duplicate Exp 189 removed, paper count 22 → 25, Exp 181 → resolved
- `whitePaper/baseCamp/README.md`: date + lint hygiene status updated

---

## Audit Findings — What Is Clean

| Area | Status |
|------|--------|
| `#[allow]` attrs | **Zero** remaining — all `#[expect(..., reason = "...")]` |
| `#![allow]` attrs | **Zero** |
| `unsafe` code | All in `low_level/bar0.rs` (MMIO), `#![forbid(unsafe_code)]` on lib |
| Production mocks | **Zero** — no `Mock*`/`stub_*`/`Fake*` outside test modules |
| `todo!`/`unimplemented!` | **Zero** in lib code |
| EVOLUTION markers | 8 `#[expect(dead_code)]` — GPU pipeline wiring reservations (WGSL shaders exist but not hooked). Tracked via GAP-HS-027 (upstream TensorSession) |
| External deps | Mostly pure Rust. Only FFI: `wgpu` (necessary), `cudarc` (optional CUDA), `rustix` (optional syscalls) |

---

## Primal Interaction Summary

### Required primals (niche.rs)

| Primal | Role | Domain | Status |
|--------|------|--------|--------|
| **beardog** | security | `crypto` | Functional via IPC |
| **songbird** | discovery | `discovery` | Functional via IPC |
| **barracuda** | math | `math` | Functional (CPU and GPU paths) |

### Optional primals

| Primal | Domain | Gap | Notes |
|--------|--------|-----|-------|
| **coralreef** | `shader` | — | Sovereign compiler operational |
| **toadstool** | `compute` | GAP-HS-040 (timeouts mitigated) | Performance surface reporter |
| **nestgate** | `storage` | **High priority upstream** | Not live yet — blocks full data chains |
| **rhizocrypt** | `dag` | GAP-HS-039 (mitigated) | DAG timeouts in composition |
| **loamspine** | `ledger` | — | Ledger sealing available |
| **sweetgrass** | `attribution` | — | Provenance braids available |
| **squirrel** | `ai` | GAP-HS-001 | E2E inference pending |
| **petaltongue** | `visualization` | GAP-HS-042 (musl/winit) | Workaround documented |

### IPC Pattern

- **Transport:** Unix domain sockets, JSON-RPC 2.0, newline-delimited
- **Discovery:** `niche::socket_dirs()` (XDG-compliant), `$BIOMEOS_SOCKET_DIR` override
- **Standalone:** `HOTSPRING_NO_NUCLEUS=1` → graceful degradation, physics still works
- **Registration:** `register_with_target()` sends `lifecycle.register` + `capability.register` to biomeOS
- **Capabilities:** 18 local (physics/compute/health/MCP) + 23 routed (to canonical providers)

---

## What Upstream Primals Should Know

### nestGate — HIGH PRIORITY

hotSpring has storage as optional (`required: false`) but full data chains
(LTEE reproductions → lithoSpore → foundation) are blocked until nestGate
content hashing (BLAKE3) and provenance are live. The `storage.store`,
`storage.retrieve`, `storage.list` methods are declared in ROUTED_CAPABILITIES.

### barraCuda — EVOLUTION(B2) Deferred

GAP-HS-007/027: GPU HMC paths still use discrete `gpu_wilson_action` /
`gpu_kinetic_energy` readbacks instead of `TensorSession` for Metropolis
scalars. This is functional but not optimal. Waiting for `TensorSession`
API to stabilize upstream. Four EVOLUTION(B2) comments mark the sites.

### coralReef — SM Rebuild

K80 sovereign dispatch (GAP-HS-076) and Titan V FECS (GAP-HS-073) work via
warm-catch but need the coralReef SM rebuild for clean cold-boot paths.
`coralctl warm-catch <BDF>` is pure Rust and operational.

---

## What Sibling Springs Should Know

### Patterns for Adoption

1. **Tier 4 IPC-first defaults:** `default = []` in Cargo.toml, `barracuda-local` opt-in. All
   springs should build with zero primal library linking by default.
2. **`#[expect]` over `#[allow]`:** Use `#[expect(clippy::..., reason = "...")]` for all lint
   suppressions. The `reason` parameter documents why.
3. **Environment variable overrides:** All hardcoded sysfs/procfs paths should accept env var
   overrides for CI/cross-platform testing (`SYSFS_HWMON_DIR`, `PROC_CPUINFO`, etc.).
4. **`tolerances/` as single source of truth:** All named constants for validation thresholds,
   algorithm tuning, and cost estimates live in `barracuda/src/tolerances/`.
5. **3-tier compute ladder docs:** hotSpring workload TOMLs in projectNUCLEUS document
   `compute_tier` and `ladder` metadata for routing. Other springs should do the same.
6. **BenchReport::save_and_print():** Consolidates benchmark save logic. Use it instead of
   inlining `discovery::benchmark_results_dir()` + `save_json()`.

### LTEE Reproductions

hotSpring LTEE B2 (Anderson fitness) is COMPLETE — Tier 1 Python + Tier 2 Rust validation.
Expected values in `experiments/results/ltee/ltee_b2_anderson_expected.json` feed lithoSpore
module 7 (`ltee-anderson`). Pattern: Python baseline → expected JSON → Rust scenario in
`validation/scenarios/` → lithoSpore ingestion.

### projectNUCLEUS Workload TOMLs

6 hotSpring workload TOMLs created in `projectNUCLEUS/workloads/hotspring/`:
- `hotspring-md-validation.toml` (CPU tier)
- `hotspring-lattice-qcd.toml` (CPU tier)
- `hotspring-ltee-anderson.toml` (CPU tier)
- `hotspring-composition-health.toml` (CPU tier)
- `hotspring-gpu-sovereign-dispatch.toml` (GPU tier)
- `hotspring-sovereign-roundtrip.toml` (Sovereign tier)

Each documents `compute_tier`, `ladder = ["cpu", "gpu", "sovereign"]`, and `spring = "hotSpring"`.

---

## Open Gaps (13 of 86 total)

| Gap | Severity | Owner | Status |
|-----|----------|-------|--------|
| GAP-HS-001 | Medium | Squirrel/neuralSpring | E2E validation pending |
| GAP-HS-005 | Medium | BearDog/Songbird | **Blocked upstream** (ionic runtime GPU lease) |
| GAP-HS-007 | Low | barraCuda | **Deferred** (TensorSession) |
| GAP-HS-027 | Low | barraCuda | **Deferred** (TensorSession adoption) |
| GAP-HS-029 | Low | ecosystem docs | Fork isolation documentation |
| GAP-HS-030a | Low | toadStool/coralReef | **Deferred** (ember absorption) |
| GAP-HS-039 | Low | rhizoCrypt | DAG timeouts (mitigated locally) |
| GAP-HS-040 | Low | toadStool | Short timeouts (mitigated locally) |
| GAP-HS-041 | Low | barraCuda | `stats.entropy` (proxy used) |
| GAP-HS-042 | Low | petalTongue | musl/winit (workaround documented) |
| GAP-HS-047 | Low | hotSpring | **Deprioritized** |
| GAP-HS-056 | Low | hotSpring | Documented assessment |
| GAP-HS-080 | Low | primalSpring | Upstream scorecard |

---

## Paper Review Queue Status

- **25/25 CPU reproductions COMPLETE** (Tier 3a)
- **20/25 GPU reproductions** (Tier 3b — 5 remaining are CPU-natural physics)
- **Tier 3b Kokkos/LAMMPS:** Papers 43-45 COMPLETE
- **LTEE B9** (DFE/RMT): QUEUED — depends on B2 (met)
- **Papers 25-31** (Track 5 distributed computing): QUEUE
- **Papers 32-42** (WDM/OF-DFT extensions): reference/extend status

---

## Downstream Products

| Product | hotSpring Status | What They Get |
|---------|-----------------|---------------|
| **lithoSpore** | B2 ready | `ltee_b2_anderson_expected.json` for module 7 |
| **foundation** | Thread 2 active | Plasma/QCD, Anderson RMT contributions |
| **projectNUCLEUS** | 6 workload TOMLs | 3-tier compute ladder documentation |
