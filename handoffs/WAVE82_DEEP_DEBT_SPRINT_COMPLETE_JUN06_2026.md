# Wave 82: Deep Debt Evolution Sprint — Complete

**Date**: 2026-06-06
**Author**: eastGate overwatch
**Sprint**: primalSpring Deep Debt Evolution (16 tasks, all complete)
**Test count**: 929 (up from 893)

---

## Sprint Results

All 16 tasks from the Deep Debt Evolution Sprint are complete. primalSpring
is now fully TOML-driven, type-safe, and shell-free for all core business
logic.

| Track | Tasks | Status |
|-------|-------|--------|
| 1. Type-safe dispatch | t1a, t1b, t1c, t1d | COMPLETE |
| 2. Shell absorption | t2a, t2b | COMPLETE |
| 3. TOML-driven config | t3a, t3b, t3c, t3d | COMPLETE |
| 4. Code quality | t4a, t4b, t4c | COMPLETE |
| 5. Pipeline & coverage | t5a, t5b, t5c | COMPLETE |

### Key deliverables

- **Zero string dispatch** — all method routing derived from `capability_registry.toml`
- **Zero hardcoded metadata** — ports, bind flags, VPS IPs, env keys all from TOML
- **Real health checks** — `health.drain` (AtomicU64 in-flight) and `health.readiness` (capability discovery)
- **Shell scripts deprecated** — `nucleus_composition_lib.sh` and `nucleus_crypto_bootstrap.sh` have comprehensive Rust replacement guides
- **Pure-Rust crypto bootstrap** — `certification/crypto_bootstrap.rs` provides three-tier HMAC-SHA256 key derivation
- **36 new tests** — env_keys, validation helpers, neural dispatch metrics, crypto bootstrap
- **Deploy pipeline hardened** — multi-binary workspace overrides, Rust self-refresh module with BLAKE3 verification
- **ureq pinned** — `=3.3.0`, `ring` wrapper-allowed in deny.toml for cross-membrane only

---

## plasmidBin Ownership Model

Formalized ownership for long-term binary distribution:

### cellMembrane team — owns binary distribution *evolution*

plasmidBin is a membrane artifact. cellMembrane owns:

- **plasmidBin CLI evolution** — `harvest`, `sync`, `fetch`, `verify`, `validate` subcommands
- **VPS deployment scripts** — `deploy_membrane.sh`, self-refresh orchestration
- **Source priority logic** — GitHub ↔ Forgejo ↔ VPS binary routing
- **Provenance chain** — checksums.toml, manifest.toml, BLAKE3 verification
- **Forgejo release publishing** — inner membrane binary distribution
- **GitHub release mirroring** — outer membrane binary distribution

### projectNUCLEUS — owns deployment *consumption* (long-term)

NUCLEUS consumes plasmidBin binaries to compose atomics:

- **nucleus_launcher** — which binaries to start, startup ordering, health sweep
- **CompositionContext** — capability requirements, liveness validation
- **Deploy graphs** — TOML compositions defining what gets deployed
- **Gate-level automation** — self-refresh *policy* (when to refresh, rollback)
- **Composition health** — verifying deployed NUCLEUS is healthy

### primalSpring — retains the *library surface*

primalSpring keeps the shared infrastructure but doesn't own execution:

- `deploy/self_refresh.rs` — Rust library for binary fetching (used by consumers)
- `config/capability_registry.toml` — canonical capability routing
- Deploy graph definitions and structural validation
- Certification and validation frameworks

### Handoff chain

```
primalSpring (evolution team)
  → defines capability requirements, deploy graphs, validation
  → hands off binary distribution concerns to ↓

cellMembrane (membrane team)
  → owns plasmidBin CLI evolution
  → owns VPS deployment scripts and self-refresh
  → owns source priority (GitHub ↔ Forgejo ↔ VPS)
  → owns provenance chain (checksums, manifest, BLAKE3)
  → hands off runtime deployment orchestration to ↓

projectNUCLEUS (long-term deployment owner)
  → owns nucleus_launcher, startup sequencing
  → owns composition validation
  → owns gate-level deployment automation
  → consumes plasmidBin as a dependency
```

---

## Remaining Work (primalSpring-specific)

| Item | Priority | Owner | Notes |
|------|----------|-------|-------|
| toadStool `--headless` regression | P0 | toadStool team | Blocks 13/13 ALIVE → mesh.init |
| Songbird test coverage (73% → 90%) | P2 | Songbird team | Coverage sprint, not blocking mesh |
| 3 springs missing `domain_profile.toml` | P2 | spring owners | hotSpring, ludoSpring, neuralSpring |
| `deploy_membrane.sh refresh` validation | P1 | cellMembrane | Full pipeline proof on VPS |

### What primalSpring does NOT need to do

- plasmidBin CLI changes → cellMembrane
- VPS binary management → cellMembrane
- Gate deployment automation → projectNUCLEUS
- Individual primal fixes → respective primal teams

---

## For the Record

929 tests. Zero clippy warnings. Zero C deps (default build). All 16 deep
debt tasks delivered. Shell scripts deprecated with comprehensive Rust
replacement guides. The codebase is now HPC mesh-ready.

*"Sixteen tasks. Nine hundred twenty-nine tests. Zero string dispatch. The mountain is clean."*
