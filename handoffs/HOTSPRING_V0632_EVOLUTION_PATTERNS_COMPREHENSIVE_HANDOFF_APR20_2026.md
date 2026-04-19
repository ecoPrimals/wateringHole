# hotSpring v0.6.32 — Comprehensive Evolution Patterns Handoff

**Date:** April 20, 2026
**From:** hotSpring (guideStone Level 5 CERTIFIED, primalSpring v0.9.16)
**For:** Primal teams, sibling springs, primalSpring upstream, biomeOS/neuralAPI
**License:** AGPL-3.0-or-later

---

## Executive Summary

hotSpring is the first spring to reach guideStone Level 5 and the reference
implementation for the primalSpring Composition Standard. This handoff documents
every pattern learned during the evolution from Python baselines through Rust
validation to NUCLEUS primal composition — patterns that should be absorbed by
primals teams and adopted by sibling springs.

**Key numbers:** 985 lib tests, 166 binaries, 64/64 validation suites, 128 WGSL
shaders, 176+ experiments. Bare guideStone: 14/14 PASS (4 expected SKIP).
plasmidBin ecoBin: `hotspring_primal` (v0.6.32, x86_64 musl-static).

---

## 1. The Three-Tier Validation Arc

The central pattern hotSpring proved: **the same tolerance-driven, exit-code-gated
methodology that proves Rust matches Python also proves IPC-composed NUCLEUS
patterns match direct Rust execution.**

```
Tier 1: Python baselines (L1)
  │ 86/86 checks, 22 papers reproduced
  │ Tolerance: published reference ± sigma
  ▼
Tier 2: Rust proof (L2)
  │ 985 lib tests, 166 binaries, 64/64 suites
  │ Tolerance: EXACT (f64 bit-identity) or documented
  ▼
Tier 3: NUCLEUS primal composition (L5)
  │ hotspring_guidestone: 14/14 checks (bare)
  │ IPC parity: Rust baseline == primal IPC result ± tolerance
  │ Tolerance: IPC_ROUND_TRIP_TOL (1e-10) or domain-specific
  ▼
Deployed via plasmidBin ecoBin → biomeOS neuralAPI
```

**Why this matters for sibling springs:** Your Python→Rust parity is already
proven. The next step is proving the same science works when called through
NUCLEUS IPC. The guideStone is the binary that certifies this.

---

## 2. guideStone Pattern — What Worked

### Bare + Additive Decomposition

The guideStone binary runs in two modes:

1. **Bare mode** (no primals needed): Validates 5 intrinsic properties
   - Property 1: Deterministic Output — same binary, same results
   - Property 2: Reference-Traceable — every value has a paper/DOI
   - Property 3: Self-Verifying — BLAKE3 CHECKSUMS manifest
   - Property 4: Environment-Agnostic — musl-static, no sudo, no GPU required
   - Property 5: Tolerance-Documented — every threshold has a name and derivation

2. **NUCLEUS additive** (primals deployed): IPC parity checks
   - Scalar parity (stats.mean via barraCuda)
   - Vector parity (tensor.matmul via barraCuda)
   - SEMF end-to-end (physics.nuclear_eos via hotSpring-as-primal)
   - Crypto provenance witness (crypto.hash via BearDog)
   - Compute dispatch (compute.dispatch via toadStool)

**Pattern for adoption:** Start with bare mode (5 properties). It's cheap, runs
in CI, requires zero infrastructure. Add NUCLEUS additive later when plasmidBin
is available.

### Domain Science as Parity Target

hotSpring uses its own physics as the IPC parity baseline:

```rust
let local_be = semf_binding_energy(208, 82, &SLY4_PARAMS);
let ipc_be = ctx.call("compute", "physics.nuclear_eos", &params)?;
check_relative(&mut v, "parity:semf_pb208", ipc_be, local_be, 1e-10, "SLY4");
```

Every spring has equivalent domain science: wetSpring has phylogenetic distances,
neuralSpring has inference parity, ludoSpring has game math. The pattern is
identical: call by capability, compare against local Rust baseline.

### primalSpring Composition API Sufficiency

Everything needed for composition validation is in `primalspring::composition`:

| API | Purpose |
|-----|---------|
| `CompositionContext::from_live_discovery_with_fallback()` | Discover running primals |
| `validate_liveness()` | Check primals are alive |
| `validate_parity()` / `validate_parity_vec()` | Compare scalar/vector values |
| `primalspring::checksums::verify_manifest()` | BLAKE3 Property 3 |
| `primalspring::tolerances` | Ecosystem tolerance constants |
| `IpcError::is_connection_error()` | Graceful absent-primal handling |
| `IpcError::is_protocol_error()` | HTTP-on-UDS → SKIP (Songbird/petalTongue) |

No spring needs to build its own IPC infrastructure.

---

## 3. Tolerance Hierarchy — Critical for All Springs

hotSpring's tolerance architecture is the most battle-tested in the ecosystem:

```
EXACT (0.0)                    ← bit-identical (integer ops, hashes)
DETERMINISTIC (f64::EPSILON)   ← same binary, different run
CPU_GPU_PARITY (1e-12)         ← f64 vs WGSL shader
IPC_ROUND_TRIP_TOL (1e-10)     ← JSON serialization + IPC overhead
DOMAIN_SPECIFIC                ← SEMF (1e-10), plaquette (1e-12), etc.
```

**Key lesson:** IPC adds serialization noise. JSON-RPC round-trips through f64
introduce ~1e-12 error. Set `IPC_ROUND_TRIP_TOL` accordingly. Don't use
`EXACT` for IPC comparisons — they will fail.

**For primalSpring:** Consider publishing the tolerance hierarchy as part of
`GUIDESTONE_COMPOSITION_STANDARD.md` so all springs use consistent names.

---

## 4. Patterns for Primal Teams

### For barraCuda Team

hotSpring consumes 10 barraCuda capabilities over IPC:
- `tensor.create`, `tensor.matmul`, `tensor.scale`, `tensor.add`
- `stats.mean`, `stats.std_dev`
- `compute.dispatch`, `compute.df64`

**Observation:** The tensor API works well for scalar/vector parity. Consider
exposing a `tensor.dispatch_pipeline` for fused multi-op sequences (GAP-HS-027).
hotSpring's GPU HMC trajectory is the natural first test case — leapfrog + force
+ gauge update as a single session rather than 3 IPC round-trips.

### For BearDog Team

hotSpring uses `crypto.hash` for provenance witnesses. The BLAKE3 hash is
compared against local `primalspring::checksums` output.

**Known issue:** BearDog resets connections without BTSP handshake. hotSpring
handles this with `is_connection_error()` → SKIP. This is correct for validation
but means **no spring can use BearDog crypto over IPC without BTSP**.

**Recommendation:** Either (a) implement a BTSP-free "basic" mode for hash-only
operations, or (b) document the BTSP requirement in the capability registry so
springs know to expect connection reset on crypto calls.

### For toadStool Team

hotSpring validates `compute.dispatch` for GPU shader pipeline delegation.

**Observation:** The fork-isolation pattern from coral-driver (`fork_isolated_raw`
+ safe wrappers) is reusable for any hardware operation that might hang. This
should be standardized in `ECOBIN_ARCHITECTURE_STANDARD.md` (GAP-HS-029).

**Ember absorption:** Per NUCLEUS design, ember (per-GPU MMIO daemon) should
eventually be absorbed into toadStool. The sovereign_init pipeline, fork isolation,
and MMIO gateway modules are the primary absorption targets (GAP-HS-030).

### For Songbird / petalTongue Teams

Both primals speak HTTP framing on Unix domain sockets. This causes raw JSON-RPC
clients to get protocol errors. primalSpring v0.9.16 classifies this as
`is_protocol_error()` → SKIP (reachable but incompatible).

**Recommendation:** Either standardize HTTP-framed JSON-RPC on UDS as a valid
transport, or add a raw JSON-RPC mode to these primals for IPC-only callers.

### For biomeOS / neuralAPI

hotSpring's deploy graph (`graphs/hotspring_qcd_deploy.toml`) declares 10 primals
with tiered encryption (tower/node/nest) and spawn ordering. The `register_with_target()`
call sends `lifecycle.register` + `capability.register` to biomeOS on startup.

**Pattern for neuralAPI exposure:** Each spring serves capabilities via JSON-RPC.
neuralAPI should proxy these through biomeOS's graph, routing by capability domain.
hotSpring's 13 LOCAL_CAPABILITIES are all wired and dispatched — no stubs.

---

## 5. Active Gaps for Upstream

| Gap | Primal | Severity | Description |
|-----|--------|----------|-------------|
| GAP-HS-001 | Squirrel | Low | E2E validation pending neuralSpring native inference |
| GAP-HS-002 | biomeOS | Low | `by_domain()` migration in remaining call sites |
| GAP-HS-005 | BearDog/Songbird | Medium | IONIC-RUNTIME cross-family GPU lease not implemented |
| GAP-HS-006 | barraCuda/BearDog | Medium | BTSP stream encryption for IPC sessions |
| GAP-HS-027 | barraCuda | Low | TensorSession fused pipeline adoption |
| GAP-HS-028 | hotSpring | Low | LIME/ILDG zero-copy I/O |
| GAP-HS-029 | coralReef/toadStool | Low | Fork-isolation pattern not yet ecosystem-standardized |
| GAP-HS-030 | toadStool/coralReef | Medium | Ember absorption into toadStool (post sovereign-solve) |
| GAP-HS-031 | coralReef | Medium | Blackwell GPFIFO NOP timeout (compile works, dispatch TBD) |

---

## 6. Deployment Workflow (for Sibling Springs to Copy)

```bash
# 1. Build guideStone binary (add primalspring dep to Cargo.toml)
cargo run --release --bin myspring_guidestone

# 2. Bare mode validation (no NUCLEUS needed)
./scripts/validate-primal-proof.sh

# 3. Deploy NUCLEUS from plasmidBin
export FAMILY_ID="myspring-validation"
export BEARDOG_FAMILY_SEED="$(head -c 32 /dev/urandom | xxd -p)"
cd ../plasmidBin
./nucleus_launcher.sh --family-id "$FAMILY_ID" --composition niche-myspring

# 4. Full primal proof
FAMILY_ID="myspring-validation" ./scripts/validate-primal-proof.sh --full

# 5. Document gaps in docs/PRIMAL_GAPS.md
# 6. Hand back via wateringHole handoff
```

hotSpring's `scripts/validate-primal-proof.sh` can be copied and adapted by
any spring. The only spring-specific parts are the binary name and the
composition type.

---

## 7. plasmidBin Status

| Component | Status |
|-----------|--------|
| `hotspring_primal` (x86_64 musl-static) | Present in `infra/plasmidBin/hotspring/` |
| `metadata.toml` | Full schema: `[provenance]`, `[compatibility]`, `[builds]`, `[genomeBin]` |
| NUCLEUS primal binaries | Pending full depot (not yet fetched locally) |
| `nucleus_launcher.sh` | Pending in plasmidBin (documented in PLASMINBIN_DEPOT_PATTERN.md) |

**For plasmidBin maintainers:** The 14 primal binaries and `nucleus_launcher.sh`
need to be committed to the depot for springs to run full NUCLEUS validation.

---

## 8. What hotSpring Proved for the Ecosystem

1. **Consumer hardware runs HPC physics at paper parity.** 22 papers, 400+ checks,
   $0.30 total science cost. The scarcity was artificial.

2. **Python→Rust→Primal is a viable validation ladder.** Each tier catches different
   bugs: Python catches physics errors, Rust catches precision/performance errors,
   NUCLEUS catches composition/routing errors.

3. **guideStone bare mode runs in CI.** No infrastructure needed. 14 checks pass
   in <1 second. This should be in every spring's CI pipeline.

4. **The primalSpring composition API is sufficient.** Zero custom IPC code needed.
   `CompositionContext` + `validate_parity` + `check_skip` covers all cases.

5. **Tolerance documentation prevents false negatives.** Named tolerance constants
   with physical derivations eliminate "is this error real or expected?" questions.

6. **Protocol tolerance is necessary.** HTTP-on-UDS primals need `is_protocol_error()`
   classification, not failure. v0.9.16 got this right.

7. **BLAKE3 manifest verification is cheap and correct.** Property 3 with
   `primalspring::checksums::verify_manifest()` replaces manual file-exists checks.

---

## 9. Recommended primalSpring Evolution

For the upstream primalSpring audit, these patterns from hotSpring should be
considered for ecosystem standardization:

1. **Tolerance hierarchy document** — publish named tier definitions in the
   guideStone standard so all springs use consistent names.

2. **Fork-isolation as ecosystem pattern** — GAP-HS-029. Useful for any primal
   touching hardware (toadStool, coralReef, ember).

3. **Three-tier validation template** — a scaffold document for new springs
   showing Python→Rust→NUCLEUS with concrete code examples.

4. **`validate-primal-proof.sh` template** — a generic script that springs
   can copy, changing only the binary name and composition type.

5. **Capability registry TOML as canonical** — hotSpring has
   `config/capability_registry.toml` with bidirectional sync test. This should
   be an ecosystem pattern for all springs.

---

## References

- guideStone standard: `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` (v1.1.0)
- plasmidBin depot: `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md`
- Downstream manifest: `primalSpring/graphs/downstream/downstream_manifest.toml`
- Composition guidance: `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md`
- Gap registry: `hotSpring/docs/PRIMAL_GAPS.md`
- Previous handoffs: `infra/wateringHole/handoffs/HOTSPRING_V0632_*`
- Ecosystem alignment: `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md`
