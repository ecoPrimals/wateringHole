# hotSpring Post-Interstadial Evolution Handoff

**Date**: 2026-05-11
**From**: hotSpring (v0.6.32, guideStone Level 6 CERTIFIED)
**For**: primalSpring (audit), upstream primal teams, sibling spring teams, projectNUCLEUS
**Phase**: Post-interstadial — Tier 4 IPC-first, foundation seeding, deep debt complete

---

## Purpose

This handoff documents hotSpring's evolution from the May 10 interstadial gate
through May 11, covering all changes, patterns discovered, composition evolution,
and items for upstream teams to absorb. primalSpring should audit this for
ecosystem-wide patterns and registry alignment.

---

## 1. What hotSpring Completed (May 10-11)

### Tier 4 IPC-First Rewiring (COMPLETE)

hotSpring is the first spring (with ludoSpring) to implement Tier 4:

- `barracuda` declared `optional = true` in workspace Cargo.toml
- 25+ library modules feature-gated behind `#[cfg(feature = "barracuda-local")]`
- `primal-proof` feature flag enables IPC-only builds without linking barracuda
- `CompositionContext` wired for all cross-primal calls
- Verified: `cargo check --lib --no-default-features --features primal-proof` passes

**Pattern for sibling springs:** The `primal-proof` feature flag pattern lets
any spring build an IPC-only binary that discovers and calls primals at runtime
without linking any local compute library. This is the path to true gate-agnostic
deployment.

### skunkBat Audit IPC (NEW)

- Added `src/ipc/skunkbat.rs` — Rust client for `security.audit_log`
- Cursor-based polling: `query_audit_log(since_seq, limit)` and `query_latest_audit(limit)`
- `AuditEvent` / `AuditLogResponse` structs with serde
- `check_audit_log()` for validation harnesses
- 6 new unit tests
- skunkBat was already in 4 deploy graphs; now has programmatic IPC access

**For skunkBat team:** When Phase 3 ships, audit events auto-forward to
rhizoCrypt DAG + sweetGrass braid. The `security.audit_log` cursor API
(since_seq + limit, capped at 1000) is clean and works well as a client
contract — no changes needed upstream.

### Foundation Seeding — Thread 2 (Plasma Physics)

- Created `data/targets/thread02_plasma_targets.toml`: 12 Sarkas Yukawa MD
  validation targets (energy drift, RDF, D*, viscosity, Daligault fit)
- All 12 targets `validated = true` with source paper and tolerance
- Thread 2 expression doc: `expressions/PLASMA_QCD_SOVEREIGN_GPU.md`
- Two foundation workloads: `hs-sarkas-md-validation.toml`, `hs-chuna-validation.toml`
- Validation run: `validation/plasma-20260511/` — 12/12 PASS
- `THREAD_INDEX.toml` Thread 2 upgraded "mapped" → "active"

**Pattern for sibling springs:** Any spring validating against public data
(NCBI, UniProt, PDB, FAO) should seed foundation with validation targets.
The TOML structure is: `[[targets]]` with `paper`, `expected_value`, `unit`,
`tolerance`, `source`, `spring`, `blake3`, `validated`, `notes`.

### Smart Refactoring

- `single_beta.rs` (826L → 553L): Extracted 273-line measurement loop into
  `measurement.rs` (423L). Structured `MeasurementResult` return with
  sub-functions for NPU reject prediction, anomaly detection, sub-model
  steering, and Polyakov readback.
- All files now under 800L threshold.

### Dead Code Cleanup

- 19 `dead_code` warnings eliminated by removing 3 superseded NPU handler
  files (709 lines total) — old `handlers_inference.rs`, `handlers_screening.rs`,
  `handlers_steering.rs` were remnants of prior refactor.

### UniBin Release Binary

- Built `hotspring_unibin` in release mode: 3.3M stripped binary
- Subcommands: `certify`, `validate`, `status`, `version`
- Ready for plasmidBin GitHub Releases
- NUCLEUS workload updated to use UniBin with `$SPRINGS_ROOT` paths

---

## 2. Patterns for Upstream Primals

### barraCuda

- **IPC absorption pattern:** hotSpring's 25+ feature-gated modules demonstrate
  how to make a compute library optional. Any module that calls barracuda
  directly gets `#[cfg(feature = "barracuda-local")]` on the import and a
  feature-gated wrapper function. The IPC fallback calls
  `primal_bridge::send_jsonrpc()` with the equivalent capability method.
- **No upstream changes needed** — barraCuda's dispatch contract is stable.

### biomeOS

- `composition.status` successfully wired — `{ active_users, primal_health,
  resource_pressure }` integrated into health monitoring paths.
- `method.register` successfully wired — hotSpring registers 13 physics/compute
  methods dynamically via biomeOS v3.51.
- **No gaps found.**

### bearDog

- TLS, sovereignty patterns absorbed.
- Receipt signing via `crypto.sign_ed25519` works reliably for provenance.
- **No gaps found.**

### toadStool

- Shader dispatch stable. Fleet queries stable.
- **Minor concern:** `$SPRINGS_ROOT` environment variable in NUCLEUS workload
  TOMLs — unclear if toadStool expands env vars in workload commands. If not,
  springs need wrapper scripts or absolute paths. See projectNUCLEUS Gap 8.

### coralReef

- 128 WGSL shaders compile cleanly via coralReef sovereign compiler.
- **SM35 + SM70 + SM120 WGSL→SASS validated.**
- AMD sovereign compiler: 24/24 QCD shaders pass.

### skunkBat

- `security.audit_log` API is clean: cursor-based, limit-capped, well-typed.
- **Suggestion for skunkBat team:** Consider adding a `category` filter parameter
  to `security.audit_log` so clients can poll by event type (e.g. only
  `access`, `auth`, `composition`) without client-side filtering.

### rhizoCrypt / loamSpine / sweetGrass (Provenance Trio)

- Provenance IPC wired via `src/ipc/provenance/` (rhizoCrypt DAG, loamSpine
  ledger, sweetGrass attribution braid).
- Receipt signing and submission tested in validation harness.
- **When foundation BLAKE3 hashing is live**, provenance trio integration
  should auto-submit content hashes on validation runs.

---

## 3. Patterns for Sibling Springs

### Three-Tier Validation Arc

hotSpring's validated pattern:
```
Published paper (Python/Fortran/C++)
  → Python control script (control/)
  → Rust CPU reproduction (barracuda/src/)
  → GPU sovereign dispatch (WGSL via wgpu)
  → NUCLEUS primal composition (IPC parity via CompositionContext)
  → Foundation geological layer (validated targets + provenance)
```

Each tier adds trust: Python proves the math, Rust proves the implementation,
NUCLEUS proves the composition, foundation proves the reproducibility.

### UniBin Subcommand Surface

Standardized across springs:
- `certify` — bare property certification (no primals needed)
- `validate --scenario <name>` — science validation against known targets
- `status` — health/version/capability summary
- `version` — semantic version + build info

### Deploy Graph Integration

hotSpring has 7 deploy graphs covering Tower/Node/Nest/Full NUCLEUS patterns.
Each graph has a `[nodes]` section listing required primals and a `[health]`
section with composition health checks. The pattern:

```toml
[nodes.hotspring]
role = "science"
capabilities = ["physics.yukawa_md", "compute.gpu_dispatch"]
health_check = "health.ping"
```

### Foundation Seeding Lifecycle

1. Spring validates against published data → tolerance-gated checks pass
2. Create `data/targets/threadNN_*.toml` with machine-readable targets
3. Create expression doc in `expressions/`
4. Create workload TOMLs in `workloads/<spring>/`
5. Create validation run directory with PROVENANCE_MANIFEST.md
6. Update THREAD_INDEX.toml

---

## 4. Current Metrics

| Metric | Value |
|--------|-------|
| Version | v0.6.32 |
| Lib tests | 1,025 (6 GPU/heavy-ignored) |
| Binaries | 155 |
| WGSL shaders | 128 |
| Experiments | 188 (001-143 archived) |
| Papers reproduced (CPU) | 25/25 |
| Papers reproduced (GPU) | 20/25 |
| Validation suites | 64/64 |
| Deploy graphs | 7 |
| Clippy warnings | 0 |
| `dead_code` warnings | 0 |
| `todo!`/`unimplemented!` | 0 |
| guideStone | Level 6 CERTIFIED |
| Certification | NUCLEUS Deployment Validation |
| primalSpring | v0.9.25 |
| Tier 4 | Complete (barracuda optional, primal-proof feature) |
| skunkBat | IPC wired (security.audit_log) |
| Foundation | Thread 2 active (12 targets, 12/12 PASS) |

---

## 5. Remaining Work (Not Blocking)

| Item | Priority | Owner |
|------|----------|-------|
| Update Live Science API counts after gate validation | P1 | projectNUCLEUS |
| Additional NUCLEUS workloads (nuclear EOS, spectral) | P1 | hotSpring |
| BLAKE3 content hashing for validation artifacts | P2 | hotSpring + rhizoCrypt |
| GPU parity for remaining 5/25 papers | P2 | hotSpring |
| Tier 4 WDM/NIF reproduction (Militzer, atoMEC) | P3 | hotSpring |
| Verify `$SPRINGS_ROOT` expansion with toadStool | P2 | projectNUCLEUS |

---

## 6. Composition Patterns for NUCLEUS Deployment via neuralAPI

hotSpring's science is deployed as a primal — discoverable at runtime via
biomeOS `lifecycle.register` + `capability.register`. The deployment path:

1. **Registration:** `niche.rs` declares `LOCAL_CAPABILITIES` (21 served) +
   `ROUTED_CAPABILITIES` (26 proxied). On startup, `register_with_target()`
   calls biomeOS with capability list.
2. **Discovery:** Other primals/springs call `capability.resolve(domain)` to
   find hotSpring at runtime — no hardcoded primal names.
3. **Routing:** `call_by_capability(domain, method, params)` routes via
   `CompositionContext` to any primal serving that capability.
4. **Dispatch:** 13 physics/compute methods fully dispatched via JSON-RPC
   server (`hotspring_primal.rs`) with `catch_unwind` safety.
5. **Deployment:** `biomeos deploy --graph graphs/<name>.toml` deploys the
   full composition stack. neuralAPI consumers call via biomeOS's HTTP/JSON
   gateway — no direct primal addressing needed.

The key insight: **primals only have self-knowledge and discover peers at
runtime.** Hardcoded primal names in routing code are a composition smell.

---

*hotSpring v0.6.32 — 1,025 tests, 155 binaries, 128 WGSL shaders, Level 6
CERTIFIED. Consumer GPUs reproduce HPC physics at paper parity. The full
science ladder runs on consumer hardware, composed via sovereign primal IPC.*
