# hotSpring v0.6.32 — Property 3 BLAKE3 CHECKSUMS + Deployment Patterns Handoff

**From:** hotSpring team (April 17, 2026)
**For:** primalSpring, sibling springs, per-primal teams
**Scope:** Property 3 closure, composition deployment patterns, active gaps, NUCLEUS deployment via neuralAPI/biomeOS

---

## Summary

hotSpring has reached **full guideStone Level 5 certification** with all 5 bare
properties passing. The critical milestone is **Property 3 (Self-Verifying)**
now producing 30/30 bare checks via BLAKE3 source-integrity verification, closing
the last SKIP that was present in previous handoffs.

**Key numbers:** 990 lib tests, 166 binaries, 64/64 validation suites, 128 WGSL
shaders, 176+ experiments. Bare guideStone: **30/30 PASS** (3 SKIP = expected
NUCLEUS liveness probes). primalSpring v0.9.17 absorbed.

---

## What Changed (Property 3 Closure)

### BLAKE3 CHECKSUMS Manifest

`validation/CHECKSUMS` now contains BLAKE3 hashes for **15 validation-critical
source files**, following primalSpring's source-integrity pattern:

- `barracuda/src/bin/hotspring_guidestone.rs` — the guideStone binary itself
- `barracuda/src/physics/{semf,mod,nuclear_matter,constants}.rs` — domain physics
- `barracuda/src/provenance.rs` — SLY4 parameters and DOI references
- `barracuda/src/niche.rs` — capability surface and self-knowledge
- `barracuda/src/tolerances/{mod,core,physics}.rs` — 308 named constants
- `barracuda/src/composition.rs` — NUCLEUS validation infrastructure
- `barracuda/src/validation/mod.rs` — ValidationResult framework
- `barracuda/src/lib.rs` — crate root
- `barracuda/Cargo.toml` — dependency configuration
- `scripts/validate-primal-proof.sh` — deployment validation script

`primalspring::checksums::verify_manifest()` reads this manifest at runtime
and BLAKE3-hashes each file against the stored digest. Tampered files produce
FAIL (non-zero exit). Missing files produce SKIP.

### deny.toml Dual-CWD Lookup

The guideStone binary now checks both `deny.toml` and `barracuda/deny.toml`,
so Property 3 passes whether run from the `barracuda/` crate root or the
repo root.

### Script Build/Run Split

`validate-primal-proof.sh` now:
1. **Builds** from `barracuda/` (`cargo build --release --bin hotspring_guidestone`)
2. **Runs** from the repo root (`$BARRACUDA/target/release/hotspring_guidestone`)

This ensures `validation/CHECKSUMS` resolves correctly relative to the project
root, matching how `verify_manifest()` computes the root path.

---

## Composition Deployment Patterns for Sibling Springs

### Three-Tier Validation Arc

```
Published paper (Python/FORTRAN/HPC)
  → Rust CPU reproduction (validated against reference)
    → NUCLEUS primal composition (IPC parity via guideStone)
```

This arc is fully proven in hotSpring. Sibling springs should replicate it:

1. **Domain baselines** — Python/HPC reference implementations with quantitative
   checks and tolerance definitions.
2. **Rust proof** — `cargo test --lib` reproduces domain baselines to documented
   tolerances (EXACT, DETERMINISTIC, IPC_ROUND_TRIP).
3. **guideStone binary** — Validates 5 bare properties (self-contained, no
   primals) then probes NUCLEUS IPC parity when primals are deployed.

### guideStone Property 3 Recipe

For any spring implementing Property 3:

1. Choose validation-critical source files (guideStone binary, domain modules,
   tolerances, Cargo.toml, deployment scripts).
2. Generate BLAKE3 hashes: `b3sum <files>` from repo root.
3. Write to `validation/CHECKSUMS` with project-root-relative paths.
4. Call `primalspring::checksums::verify_manifest(v, "validation/CHECKSUMS")`
   in the guideStone binary's Property 3 section.
5. Ensure the binary runs from the repo root (or wherever CHECKSUMS resolves).
6. Regenerate after any edit to checksummed files.

### Environment Variable Auto-Setup

`validate-primal-proof.sh` auto-derives required env vars when `FAMILY_ID` is set:

- `BEARDOG_FAMILY_SEED` — SHA-256 of `FAMILY_ID` if not already set
- `SONGBIRD_SECURITY_PROVIDER` — defaults to `"beardog"`
- `NESTGATE_JWT_SECRET` — random 32-byte Base64 if not already set

Sibling springs should adopt this pattern to avoid deployment failures
from missing env vars (a known v0.9.17 issue).

---

## Active Gaps for Upstream Teams

### Per-Primal Recommendations

| Primal | Gap | Recommendation |
|--------|-----|----------------|
| **barraCuda** | GAP-HS-006: BTSP session crypto | Phase 3 stream encryption for multi-process IPC |
| **barraCuda** | GAP-HS-007: TensorSession | Stabilize fused multi-op pipeline API for lattice workloads |
| **BearDog** | GAP-HS-005: IONIC-RUNTIME | Implement ionic bonding propose/accept/seal for cross-family GPU lease |
| **Squirrel** | GAP-HS-001: E2E validation | Deploy neuralSpring native inference so springs can validate parity |
| **coralReef** | GAP-HS-029: Fork isolation | Codify fork-isolated MMIO pattern in ecosystem standard |
| **toadStool** | GAP-HS-030: Ember absorption | Merge `coral-ember` survivability patterns (FdVault, warm cycle, bus master kill) |

### primalSpring Recommendations

1. **CHECKSUMS regeneration tooling** — Consider a `primalspring checksums generate`
   CLI subcommand that reads a config file listing which files to hash, rather than
   requiring springs to manually manage the manifest.

2. **Bare check count standardization** — With Property 3 now producing per-file
   checks, the bare check count varies by manifest size (hotSpring: 30, primalSpring: ~20).
   Consider documenting that bare checks = 5 properties × N (variable per spring).

3. **CWD-agnostic manifest resolution** — `verify_manifest()` computes `root`
   as `manifest.parent().parent()`. This works when the binary runs from the
   project root but not from subcrate directories. Consider accepting an explicit
   `root` parameter or auto-detecting via `CARGO_MANIFEST_DIR` at compile time.

4. **Deploy script template** — `validate-primal-proof.sh` is now the reference
   deployment script. Consider publishing a template in wateringHole for sibling
   springs: build from crate dir, run from root, auto-set env vars, detect bare
   vs NUCLEUS, interpret exit codes.

---

## NUCLEUS Deployment via neuralAPI / biomeOS

The deployment flow for hotSpring's QCD physics niche:

```
plasmidBin/genomeBin → nucleus_launcher.sh → primals on UDS
                                              ↓
hotspring_guidestone ──→ bare validation (30/30)
                    ──→ NUCLEUS discovery (tensor, security, compute)
                    ──→ IPC parity (scalar, vector, SEMF, crypto, compute)
                                              ↓
biomeOS deploy graph (graphs/hotspring_qcd_deploy.toml)
  → 10 primals, bonding policy, spawn order
  → hotspring_primal (order = 10) serves 13 physics/compute methods
  → neuralAPI exposes capabilities to external consumers
```

The `hotspring_primal` JSON-RPC server handles: `health.*`, `capability.*`,
`composition.*`, `physics.*`, `compute.*`, and `mcp.tools.list` — all 13
physics/compute methods fully dispatched. External consumers (neuralAPI, biomeOS)
interact via the capability surface; hotSpring never exposes raw library APIs.

**plasmidBin status:** `hotspring/metadata.toml` present with v0.6.32 provenance.
No `genomeBin/` directory or `nucleus_launcher.sh` yet — awaiting upstream
deployment infrastructure (v0.9.17 introduced the pattern but hotSpring hasn't
executed the full launcher workflow yet).

---

## Lessons Learned

1. **Property 3 needs project-root execution.** Binary CWD matters for relative
   path resolution. The build-from-subcrate/run-from-root pattern works but adds
   complexity. A compile-time embed of the manifest (via `include_str!`) would
   eliminate this at the cost of requiring rebuild on any checksummed file change.

2. **Test count drift is insidious.** Multiple docs cited "985 tests" while the
   actual count had drifted to 990. Centralizing the count (e.g. generating it
   from `cargo test --lib` output in CI) would prevent doc/reality divergence.

3. **Bare mode is the foundation.** 30/30 bare checks prove the guideStone is
   correct without any infrastructure. NUCLEUS is additive. This decomposition
   makes debugging deployment issues tractable — if bare passes but NUCLEUS fails,
   the issue is in primal IPC, not in domain science.

4. **SHA-256 → BLAKE3 was seamless.** The primalSpring checksums module made
   migration trivial — one API call replaces the entire manual verification flow.
   Springs should adopt this immediately rather than rolling their own.

---

*hotSpring v0.6.32 — guideStone Level 5 CERTIFIED, bare 30/30, 990 tests,
primalSpring v0.9.17. All gaps documented in `docs/PRIMAL_GAPS.md`. Fossil
record preserved in `ecoPrimals/` for evolutionary review.*
