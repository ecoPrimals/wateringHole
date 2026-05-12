# HOTSPRING V0632 — Composition Audit, Primal Evolution & NUCLEUS Deployment Handoff

| Field | Value |
|-------|-------|
| Date | 2026-04-11 |
| From | hotSpring v0.6.32 (composition audit + remediation session) |
| To | barraCuda, toadStool, primalSpring, biomeOS, coralReef, BearDog, Songbird, NestGate, rhizoCrypt, loamSpine, sweetGrass, Squirrel, neuralSpring, all spring teams |
| License | AGPL-3.0-or-later |
| Supersedes | HOTSPRING_V0632_COMPOSITION_EVOLUTION_HANDOFF_APR11_2026 (archive that — this is the comprehensive post-audit version) |

---

## 1. What Happened

A full composition audit was conducted against hotSpring's codebase, specs,
docs, and the ecosystem standards at `ecoPrimals/infra/wateringHole/`. The
audit evaluated completion status, code quality, validation fidelity,
barraCuda dependency health, GPU evolution readiness, primal composition
readiness, test coverage, ecosystem standards compliance, and primal
coordination.

**All identified remediation items were executed in-session.** This handoff
documents what was found, what was fixed, what was learned, and what each
primal and spring team should absorb.

### The Three-Tier Validation Arc

```
Tier 1: Published science (Python/HPC)  →  Rust reproduction
Tier 2: Rust CPU baselines              →  GPU (barraCuda WGSL)
Tier 3: Rust + Python baselines         →  NUCLEUS IPC composition
```

The same tolerance-driven, exit-code-gated methodology that proved Rust
matches Python now proves IPC-composed NUCLEUS patterns match direct Rust
execution. Python was the validation target for Rust; now both Python and
Rust are validation targets for the primal composition layer.

---

## 2. What Was Fixed (Audit Remediation)

### P0 — Composition Integrity

| Fix | Detail |
|-----|--------|
| Socket naming mismatch | `hotspring_primal` now calls `niche::resolve_server_socket()` for family-scoped names (`hotspring-physics-{family_id}.sock`) — was hardcoded `hotspring-physics.sock` |
| biomeOS registration not wired | `register_with_target()` now called on server startup after socket bind — previously existed but was never invoked |
| barraCuda pin drift | `Cargo.toml` reconciled from `fbad3c0a` to `b95e9c59` matching CHANGELOG v0.6.32 |

### P1 — Wire Protocol Alignment

| Fix | Detail |
|-----|--------|
| DAG method names | `dag_provenance.rs` → `dag.session.create`, `dag.event.append`, `dag.merkle.root` (was `dag.create_session` etc.) |
| Crypto method name | `receipt_signing.rs` → `crypto.sign_ed25519` (was `crypto.sign`) |
| Capability validation stale names | `validate_nucleus_*` binaries use canonical names from `capability_registry.toml` |
| Physics dispatch honesty | Registered-but-pending methods return structured `-32001` (was generic `-32601`) |
| `discover_capabilities()` duplication | Delegates to `niche::all_capabilities()` as single source of truth |

### P2 — Code Quality

| Fix | Detail |
|-----|--------|
| `validation.rs` over 1000 LOC | Split into `validation/` module: `harness.rs` (515), `telemetry.rs` (116), `composition.rs` (301), `tests.rs` (313), `mod.rs` |
| `--family-id` CLI silently ignored | Now sets `FAMILY_ID` env var correctly |

### P3 — New Artifacts

| Artifact | Purpose |
|----------|---------|
| `graphs/hotspring_qcd_deploy.toml` | Deploy graph for biomeOS — 10 primals, bonding policy, spawn order |
| `validate_squirrel_roundtrip` binary | End-to-end Squirrel inference validation (models, complete, embed) |
| Root `CHANGELOG.md` | Spring-level changelog complementing crate-level `barracuda/CHANGELOG.md` |

---

## 3. For barraCuda Team

### Pin Status

hotSpring pins barraCuda at **v0.3.11** (`b95e9c59`). Pin is reconciled
across `Cargo.toml`, `CHANGELOG.md`, `README.md`, and `ABSORPTION_MANIFEST.md`.

### TensorSession Adoption (GAP-HS-027, Deferred)

hotSpring's GPU HMC trajectory (leapfrog + force + gauge update + CG solve)
chains ~20 fused GPU dispatches per trajectory. This is the ideal consumer
for `TensorSession` when the API stabilizes for lattice workloads. The gap
is deferred — hotSpring will wire when ready.

**Action for barraCuda:** When `TensorSession` API is stable, hotSpring's
`gpu_hmc/mod.rs` is the reference consumer. Consider a joint session.

### Absorption Queue (unchanged, still ready)

| Module | Type | Checks |
|--------|------|--------|
| `lattice/dirac.rs` | Dirac SpMV + WGSL | 8/8 |
| `lattice/cg.rs` | CG solver + 3 WGSL | 9/9 |
| `lattice/pseudofermion/` | Pseudofermion HMC | 7/7 |
| `md/reservoir/` | ESN + WGSL | NPU-validated |
| `physics/screened_coulomb.rs` | Sturm eigensolve | 23/23 |
| `physics/hfb_deformed_gpu/` | Deformed HFB + 5 WGSL | GPU-validated |

### `plaquette_variance` Delegation — Proven Pattern

This is the reference Write→Absorb→Lean cycle: hotSpring proved the math →
handed off with tolerance spec → barraCuda absorbed → hotSpring rewired →
local code deleted. Other springs should follow for their domain math.

---

## 4. For toadStool Team

### Discovery via Capability

hotSpring discovers toadStool via `by_domain("compute")`, falling back to
name-based `toadstool` lookup. `PrimalBridge` scans `$XDG_RUNTIME_DIR/biomeos/`
at startup.

### Socket Convention

`{primal}-{family_id}.sock` in `$XDG_RUNTIME_DIR/biomeos/` (fallback:
`/tmp/biomeos/`). hotSpring's `niche::resolve_server_socket()` and
`resolve_neural_api_socket()` follow this pattern.

### Scheduling Metadata

`niche.rs` exports `operation_dependencies()` and `cost_estimates()` for
biomeOS work placement. Springs that don't export these will be scheduled
blind — biomeOS can't optimize without cost hints.

---

## 5. For primalSpring Team

### Proto-Nucleate Health

hotSpring reads `hotspring_qcd_proto_nucleate.toml` — 10 primals declared.
All IPC calls use canonical capability names from the proto-nucleate
(verified via `config/capability_registry.toml` bidirectional sync test).

### Deploy Graph Created

`graphs/hotspring_qcd_deploy.toml` translates the proto-nucleate into a
deployable graph with:
- Spawn order (security → discovery → compute → math → storage → provenance → AI)
- Health checks per primal
- Bonding policy (covalent intra-atomic, metallic cross-atomic, ionic cross-family)
- Encryption tiers (BTSP per boundary)
- Fragment metadata (tower/node/nest/meta-tier/nucleus booleans)

### Gaps Handed Back

Active gaps requiring ecosystem evolution:

| ID | Gap | Severity | Owner |
|----|-----|----------|-------|
| GAP-HS-001 | Squirrel inference round-trip (Ollama→native WGSL ML) | Low | neuralSpring |
| GAP-HS-002 | Full by_capability migration in remaining bin/ targets | Low | hotSpring |
| GAP-HS-005 | IONIC-RUNTIME cross-family GPU lease (multi-family metallic fleet) | Medium | BearDog/primalSpring |
| GAP-HS-006 | BTSP session crypto for barraCuda IPC | Medium | barraCuda/BearDog |
| GAP-HS-026 | Physics dispatch not wired in server (returns -32001) | Medium | hotSpring |
| GAP-HS-027 | TensorSession adoption (deferred, waiting on API) | Low | barraCuda |
| GAP-HS-028 | LIME/ILDG zero-copy I/O (memmap2 or streaming parsers) | Low | hotSpring |

### Resolved Gaps (25 total)

See `hotSpring/docs/PRIMAL_GAPS.md` for the full resolved table with dates
and resolution details (GAP-HS-003 through GAP-HS-025 plus 9 unnamed fixes).

---

## 6. For biomeOS Team

### Neural API Methods

hotSpring's `hotspring_primal.rs` JSON-RPC server exposes:

| Method | Purpose |
|--------|---------|
| `health.liveness` | Alive check |
| `health.readiness` | Ready check with dependency probes |
| `capability.list` | LOCAL (21) + ROUTED (26) capabilities |
| `composition.health` | Atomic tier health (Tower/Node/Nest/NUCLEUS) |
| `mcp.tools.list` | 5 MCP tool definitions for AI/LLM |
| `physics.*` (9 methods) | Registered-but-pending (-32001), wiring incrementally |
| `compute.*` (4 methods) | Registered-but-pending (-32001) |

### Deployment Flow

```
biomeOS reads proto-nucleate
  → spawns primals in germination order
    → hotspring_primal starts → register_with_target() → lifecycle.register + capability.register
      → biomeOS confirms capabilities → routes requests to hotspring socket
        → composition validators run → science probes verify IPC parity
          → Neural API exposes capabilities to other springs and clients
```

### Scheduling Hints

`niche.rs::operation_dependencies()` and `cost_estimates()` provide per-operation
metadata (GPU/memory/latency). biomeOS should consume these for `neuralAPI.schedule`.

---

## 7. For coralReef Team

- 128 WGSL shaders validated (AGPL-3.0-only)
- AMD sovereign compiler: 24/24 QCD shaders → native GFX10.3 ISA
- NVIDIA GPFIFO: RTX 3090 pipeline operational
- All shader compilation routes through toadStool `WgslOptimizer` + `GpuDriverProfile`
- Lattice QCD shaders (Dirac, CG, pseudofermion, gradient flow) are next absorption targets for barraCuda; once absorbed, coralReef benefits from standardized patterns

---

## 8. For BearDog / Songbird / Provenance Trio

### Method Name Alignment

hotSpring now uses canonical wire names throughout:
- `crypto.sign_ed25519` (was `crypto.sign`)
- `crypto.verify_ed25519` (was `crypto.verify`)
- `dag.session.create` (was `dag.create_session`)
- `dag.event.append` (was `dag.append_event`)
- `dag.merkle.root` (was `dag.dehydrate`)
- `discovery.find_primals` (was `net.discovery`)

**Action for BearDog/Songbird:** Verify these match your actual method dispatch.
If there's a canonical registry, hotSpring's `config/capability_registry.toml`
should stay in sync.

### IONIC-RUNTIME (GAP-HS-005)

Cross-family GPU lease via BearDog's `crypto.sign_contract` and ionic
propose/accept/seal — blocked on BearDog implementation. This blocks
multi-family metallic fleet pooling (CERN-style deployment).

---

## 9. For Squirrel / neuralSpring Team

### Squirrel Integration Status

- `squirrel_client.rs` wired — routes `inference.complete`, `inference.embed`, `inference.models`
- `validate_squirrel_roundtrip` binary validates the round-trip when Squirrel is available
- Falls back gracefully when Squirrel is unavailable (skip-pass, exit 2)
- Squirrel is optional in the proto-nucleate (`required = false`, `spawn = false`)

**Action for neuralSpring:** When native WGSL ML inference replaces Ollama
fallback, hotSpring's `validate_squirrel_roundtrip` will confirm parity
automatically. No hotSpring code changes needed.

---

## 10. For All Spring Teams — What We Learned

### Pattern 1: Three-Tier Validation Is One Methodology

The tolerance-driven, exit-code-gated validation that proved Rust matches
Python also proves NUCLEUS IPC matches Rust. No new methodology was invented.
The `ValidationHarness` (physics) and `CompositionResult` (NUCLEUS) use the
same discipline: hardcoded expected values, explicit pass/fail, centralized
tolerances, exit 0/1 (2 for all-skipped).

### Pattern 2: Capability Wire Names Must Match Registry

The audit found 6 stale method names in IPC calls (`crypto.sign` vs
`crypto.sign_ed25519`, etc.). These cause silent failures — the IPC call
reaches the primal but the method doesn't dispatch. Every spring should:
1. Maintain a `config/capability_registry.toml`
2. Write a bidirectional sync test (registry ↔ code)
3. Use canonical names from the proto-nucleate, not informal names

### Pattern 3: Socket Naming Must Use niche.rs

Socket paths were hardcoded in the server but computed in `niche.rs`. The
mismatch meant biomeOS couldn't find the socket. **One source of truth for
socket paths: `niche::resolve_server_socket()`.** Every spring server must
call this, not hardcode paths.

### Pattern 4: Registration Must Actually Happen

`register_with_target()` existed but was never called on startup. The spring
was invisible to biomeOS. **Registration is not optional — it must be wired
into the server startup path, not left as dead code.**

### Pattern 5: Honest Error Codes for Pending Dispatch

When a spring advertises capabilities via `capability.list` but hasn't wired
the dispatch, it must return a structured error code (we chose `-32001:
Registered but dispatch pending`), not the generic `-32601: Method not found`.
This lets biomeOS distinguish "capability exists, implementation coming" from
"wrong primal".

### Pattern 6: File Size Limits Force Good Architecture

The 1000 LOC limit forced splitting `validation.rs` (1392 lines) into 4
focused modules. Each module is now independently testable and readable.
The same happened with `brain_rhmc.rs` → `brain_persistence.rs`.

### Pattern 7: Deploy Graphs Are the Deployment Contract

Proto-nucleates define WHAT composes. Deploy graphs define HOW to deploy.
Every spring should have `graphs/{spring}_deploy.toml` that biomeOS can
consume. Without it, biomeOS doesn't know spawn order, health checks,
or bonding policy.

### Pattern 8: Pin Reconciliation Is a Real Problem

The barraCuda git rev in `Cargo.toml` drifted from the one documented in
`CHANGELOG.md`. Pin drift causes silent behavior changes. **Pins should be
verified as part of any audit.** Consider a CI check.

### Pattern 9: Standalone Mode Is Essential for CI

`HOTSPRING_NO_NUCLEUS=1` lets all physics run locally without biomeOS.
Registration skips, IPC returns `None`, composition checks emit honest skips.
Without standalone mode, CI would need a full NUCLEUS deployment for every test.

### Pattern 10: Science Probes Are Composition Unit Tests

`validate_science_probes()` compares IPC-composed results against local Rust
baselines. Every spring should have domain-specific probes that validate the
IPC-composed stack produces numerically identical results to standalone code.

---

## 11. NUCLEUS Deployment Pattern via Neural API

The complete composition deployment, as validated by hotSpring:

```
1. biomeOS reads proto-nucleate graph
     └─ discovers 10 primals with explicit by_capability domains

2. biomeOS reads deploy graph
     └─ determines spawn order, health probes, bonding policy

3. Spawn primals in germination order:
     security (BearDog) → discovery (Songbird) → compute (toadStool)
     → math (barraCuda) → shader (coralReef) → storage (NestGate)
     → provenance (rhizoCrypt, loamSpine, sweetGrass) → AI (Squirrel)
     → spring (hotSpring)

4. Each primal starts → register_with_target() → biomeOS confirms

5. biomeOS exposes capabilities via Neural API
     └─ semantic routing: "lattice QCD" → hotSpring → physics.lattice_hmc
     └─ capability routing: "math.tensor" → barraCuda
     └─ cross-spring: "inference.complete" → Squirrel → neuralSpring

6. Composition validators run:
     validate_nucleus_tower  (BearDog + Songbird)
     validate_nucleus_node   (Tower + toadStool + barraCuda + coralReef)
     validate_nucleus_nest   (Tower + NestGate + trio)
     validate_nucleus_composition (all four tiers)

7. Science probes verify IPC parity:
     probe_compute_health    → toadStool dispatch matches local Rust
     probe_math_capability   → barraCuda ops match local Rust
     probe_provenance_trio   → rhizoCrypt/loamSpine/sweetGrass liveness

8. Steady state: biomeOS routes work, springs validate continuously
```

This pattern is general. Any spring can adopt it by:
1. Reading its proto-nucleate
2. Creating a deploy graph
3. Implementing `niche.rs` with LOCAL/ROUTED capabilities
4. Writing composition validators
5. Writing domain-specific science probes
6. Registering with biomeOS on startup

---

## 12. Composition Maturity Summary

| Metric | Value |
|--------|-------|
| Spring version | v0.6.32 |
| Evolution stage | **composing** |
| Lib tests | 985 |
| Binaries | 140 |
| WGSL shaders | 128 |
| Composition binaries | 4 (Tower/Node/Nest/NUCLEUS) |
| Science probes | 3 (compute/math/provenance) |
| Proto-nucleate primals | 10 |
| Deploy graph | Yes (`graphs/hotspring_qcd_deploy.toml`) |
| Capability registry | Yes (`config/capability_registry.toml`, sync-tested) |
| biomeOS registration | Yes (`register_with_target()`, wired to startup) |
| Standalone mode | Yes (`HOTSPRING_NO_NUCLEUS=1`) |
| Squirrel integration | Yes (optional, graceful fallback) |
| Active gaps | 7 |
| Resolved gaps | 25+ |

---

*hotSpring v0.6.32 — Python validates Rust. Rust validates NUCLEUS.
Peer-reviewed science runs on consumer hardware, composed via sovereign
primal IPC. The pattern is proven. The ecosystem evolves.*
