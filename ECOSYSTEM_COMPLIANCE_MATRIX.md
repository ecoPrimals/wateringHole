# Ecosystem Compliance Matrix

**Version:** 2.12.0
**Date:** April 13, 2026
**Status:** Living document — updated as primals evolve
**Authority:** wateringHole (ecoPrimals Core Standards)
**Supersedes:** `IPC_COMPLIANCE_MATRIX.md` v1.6.0 (archived to `fossilRecord/`)

This matrix tracks every primal's alignment across all auditable dimensions
defined in the 31 active wateringHole standards. Each primal receives a letter
grade per tier (A–F) and a rollup grade across all applicable tiers.

Data sourced from: April 13, 2026 full NUCLEUS revalidation — **12/12 primals ALIVE**,
**19/19 exp094 composition parity PASS**, all LD-01 through LD-10 gaps RESOLVED.
All 12 core NUCLEUS primals plus biomeOS (13 binaries total) rebuilt as musl-static ecoBins and harvested to plasmidBin.
`nucleus_launcher.sh` Phase 5 registry seeding validates Songbird `ipc.resolve` for all 9 core primals.

**v2.12.0 changes**: Phase 40 — NUCLEUS Complete revalidation. All live deployment gaps resolved:
- **LD-01 through LD-10 ALL RESOLVED** — see `primalSpring/docs/PRIMAL_GAPS.md` for full history.
- **barraCuda** v0.3.12: JSON-RPC via BTSP guard line replay (LD-10). 32 wire methods. `math-{family}.sock` naming (LD-05).
- **ToadStool**: BTSP auto-detect on all transports (LD-04). health.liveness responds on current binary.
- **Songbird**: `ipc.resolve` returns `native_endpoint`/`virtual_endpoint` (LD-08). 79 methods.
- **rhizoCrypt** S37: UDS at `rhizocrypt-{family}.sock` (LD-06). 28 DAG methods.
- **loamSpine** v0.9.16: UDS-first, TCP opt-in via `--listen` (LD-09). 34 methods.
- **petalTongue** v1.6.6: `--socket` CLI flag for correct UDS path.
- **NestGate**: Persistent UDS connections (LD-02/LD-03). 30 storage methods.
- **exp094**: 19/19 PASS, 0 FAIL, 0 SKIP — full NUCLEUS composition parity validated.
- **primalSpring** v0.9.14: 443 lib tests pass, 13 FullNucleus capabilities, `IpcError::is_transport_mismatch()` for graceful transport handling.

**v2.7.1 changes**: skunkBat BearDog v0.9.0 alignment — BTSP handshake parameters
aligned with canonical `btsp.server.{create_session,verify,negotiate}` method names and
`SessionCreateParams`/`SessionVerifyParams`/`SessionNegotiateParams` type shapes. Challenge
generation delegated to BearDog (removed `rand_u128`). `consumed_capabilities` updated to
`btsp.server.verify`, `genetic.verify_lineage`, `capabilities.list`. Mock UDS provider tests
for full handshake path (`btsp.rs` 51% → 90%). Specs evolved: thymic selection, composable
primitives, threat detection all reference correct BearDog method names. Integration tests
wired for live BearDog binary. 171 tests, 89.6% line coverage, 28 files, 7,288 lines.

**v2.7.0 changes**: skunkBat deep debt evolution — IPC surface established:
JSON-RPC 2.0 server on TCP + UDS (skunk-bat-server UniBin with `server`/`health`/`scan`/`detect`
subcommands). BTSP Phase 1 complete (socket naming, `FAMILY_ID` scoping, `BIOMEOS_INSECURE` guard).
Wire Standard L2/L3 (`capabilities.list` + `identity.get`). Real JSON-RPC client for
ToadStool discovery and Songbird federation (UDS-first, TCP-fallback, capability-based).
Hardcoded primal names/ports eliminated. Production stubs evolved to complete implementations.
`VecDeque` rolling profiler, `/proc/loadavg` system load, `dispatch` smart-refactored.
Unused deps removed (toml, anyhow, chrono). 124+ tests, 0 warnings, 0 TODO/FIXME.
11 stale root docs archived to `fossilRecord/skunkBat/`. Root docs rewritten for current state.

**v2.6.0 changes**: NestGate deep debt Session 40 — primalSpring gap resolution:
NG-01 RESOLVED (FileMetadataBackend enforced in production), NG-03 RESOLVED (data.* wildcard
delegation, hardcoded NCBI/NOAA/IRIS removed), BTSP Phase 2 RESOLVED (server handshake wired
into both UDS listeners). `uzers` dep removed (→ rustix). 81 hardcoded `self.base_url` strings
eliminated. `tarpc_server` smart-refactored to directory module. Zero TODO/FIXME in production code.
Production stubs audit: clean, zero leakage.

**v2.5.0 changes**: primalSpring v0.9.3 live validation gap matrix harvested.

**v2.4.0 changes**: Fmt debt cleared — BearDog, Songbird, toadStool now PASS `cargo fmt --check`.
All 15 primals pass fmt. benchScale GAP-017 RESOLVED (biomeOS deploy script fixed:
`--graphs-dir`, `--port`, `--family-id` now passed; health check upgraded to 15s + 3 retries).
Trio witness evolution (WireWitnessRef) harvested to plasmidBin. barraCuda executor.rs split.

**v2.3.0 changes**: Full re-audit with `cargo fmt/clippy/test` across all 15 primals.
License alignment **COMPLETE** (all `-or-later`). 10 build/test debt items resolved.
toadStool clippy CLEAN (was FAIL), fmt 1 diff (was 1,899). bingoCube edition 2024
(was 2021), clippy CLEAN (was 15 errors). coralReef/rhizoCrypt/sweetGrass clippy CLEAN.
barraCuda E0061 FIXED. Discovery compliance re-scanned with broader methodology.

---

## Scoring System

| Grade | Meaning |
|-------|---------|
| **A** | Full compliance — all checks in this tier pass |
| **B** | Minor gaps — 1–2 non-critical items missing |
| **C** | Partial compliance — core functionality present but several items need attention |
| **D** | Significant debt — major items failing |
| **F** | Non-compliant — does not meet the tier's requirements |
| **--** | Not applicable (e.g. library primals without IPC daemons) |

Per-item detail uses: **PASS** / **DEBT** / **N/A**.

---

## Primal Abbreviations

| Abbr | Primal | Role |
|------|--------|------|
| BD | BearDog | Security / Crypto |
| SB | Songbird | Registry / Orchestration |
| NG | NestGate | Storage / Platform |
| TS | ToadStool | Compute / Sensors |
| BC | barraCuda | GPU Compute (library) |
| CR | coralReef | Shader / GPU Pipeline |
| SQ | Squirrel | AI / Coordination |
| bOS | biomeOS | Orchestrator / Neural API |
| PT | petalTongue | Visualization |
| RC | rhizoCrypt | Ephemeral DAG / Working Memory |
| SG | sweetGrass | Data / Indexing |
| LS | LoamSpine | Mesh Networking |
| BiC | bingoCube | Entropy / Game Math |
| SD | sourDough | CLI Scaffolding |

---

## Summary Table

| Primal | T1 Build | T2 UniBin | T3 IPC | T4 Discovery | T5 Naming | T6 Resp | T7 Workspace | T8 Present | T9 Deploy | T10 Live | Rollup |
|--------|----------|-----------|--------|--------------|-----------|---------|--------------|------------|-----------|----------|--------|
| **BearDog** | A ↑ | A | A | B | B | B | A | B | A | B | **B** |
| **Songbird** | A ↑↑ | B | A ↑ | C ↑↑ | B | B | A | B ↑ | A | B | **A** ↑↑ |
| **NestGate** | A ↑ | D | C | C | B | B | A | A | D | N/T | **C** |
| **ToadStool** | B ↑↑ | C | C | D | D | B | A | C ↑ | C | D | **C** ↑ |
| **barraCuda** | A | -- | -- | -- | -- | A | A | A | -- | -- | **A** |
| **coralReef** | A ↑ | A | A | B | A | A | A | B | C | N/T | **A** ↑ |
| **Squirrel** | A ↑ | C | C | D | B | C | A | B | A | C | **C** |
| **biomeOS** | A ↑ | C | B | A | A | B | A | B | C | N/T | **B** |
| **petalTongue** | A | B | B | C | A | A | A | C | C | N/T | **B** |
| **rhizoCrypt** | A | B | A | B | A | A | A | A | C | A ↑↑ | **A** ↑ |
| **sweetGrass** | A ↑ | C | C | B | B | A | A | A | D | C | **B** |
| **LoamSpine** | A | C | B | B | B | A | A | A | C | C ↑ | **B** ↑ |
| **bingoCube** | A | -- | -- | -- | -- | A | A | A ↑ | -- | -- | **A** |
| **sourDough** | A ↑ | -- | -- | -- | -- | A | A | B ↑ | -- | -- | **B** |
| **skunkBat** | A ↑ | A ↑ | A ↑ | B ↑ | A ↑ | A | A | A ↑ | -- | -- | **A** ↑ |

### Grade Distribution

| Grade | Count | Primals |
|-------|-------|---------|
| A | 6 ↑ | barraCuda, bingoCube, coralReef, skunkBat, rhizoCrypt, Songbird |
| B | 6 | BearDog, biomeOS, petalTongue, sweetGrass, LoamSpine, sourDough |
| C | 3 ↓ | NestGate, ToadStool, Squirrel |
| D | 1 | ToadStool |
| F | 0 | — |

---

## Tier 1: Build Quality

Source: `STANDARDS_AND_EXPECTATIONS.md`, `LICENSING_AND_COPYLEFT.md`

| Check | BD | SB | NG | TS | BC | CR | SQ | bOS | PT | RC | SG | LS | BiC | SD |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|
| `cargo fmt` | 1 diff | PASS ↑ | PASS | 1 diff ↑↑ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS ↑ | PASS | PASS |
| `cargo clippy -D warnings` | PASS | PASS | PASS | PASS ↑↑ | PASS | PASS ↑ | PASS | PASS | PASS | PASS ↑ | PASS ↑ | PASS | PASS ↑ | PASS |
| `cargo test --all-features` | PASS (14,787+) | PASS | PASS (11.7K) | PASS | PASS (4.4K) | PASS | PASS (6.9K) | PASS (7.6K) | PASS | PASS (1.4K) | PASS | PASS (1,507) | PASS | PASS |
| `cargo doc --no-deps` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Edition 2024 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS ↑ | PASS |
| `forbid(unsafe_code)` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `warn(missing_docs)` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No TODO/FIXME/HACK | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No files >1000 lines | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No `.unwrap()` in lib | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No commented-out code | PASS | PASS ↑ | PASS | DEBT | DEBT | DEBT | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS | PASS |
| License `AGPL-3.0-or-later` | PASS ↑ | PASS ↑ | PASS ↑ | PASS ↑ | PASS | PASS ↑ | PASS | PASS ↑ | PASS | PASS | PASS ↑ | PASS | PASS ↑ | PASS |
| SPDX header on sources | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT |
| **Grade** | **B** ↑ | **A** ↑↑ | **A** ↑ | **B** ↑↑ | **A** ↑ | **A** ↑ | **A** ↑ | **A** ↑ | **A** | **A** | **A** ↑ | **A** | **A** ↑ | **A** ↑ |

### Tier 1 Detail (April 6 re-audit, Songbird updated April 9)

- **BearDog**: **STADIAL GATE CLEARED — 13/13** (Wave 55) + **Deep debt clean** (Wave 67) + **Phase 45 audit resolved** (Wave 66) + **BTSP JSON-line UDS fix** (Wave 64). Wave 66: `crypto.public_key` method, IPC roundtrip proven (resolves primalSpring `crypto:ed25519_verify` SKIP). Wave 67: 0 hardcoded primal names, full audit clean. 96 crypto methods. 20 enum dispatch types. Zero `async-trait`/`tarpc`/`ring`/`sled`/`openssl`/`serde_yaml` in lockfile. All production files <800 LOC. 14,925+ tests, **90.51%** coverage. Clippy + rustdoc clean (`-D warnings`). Edition 2024.
- **Songbird**: Fmt **CLEAN** ↑ (was 2 diffs). Commented-out code **CLEAN** ↑ (Wave 124 scrub). 7,265+ lib tests, 0 failed. All 30 crates clippy pedantic+nursery zero warnings. 4 largest files smart-refactored (Wave 133). BTSP Phase 2 complete (Wave 132).
- **NestGate**: Fmt **PASS**. Clippy CLEAN. License `-or-later`. 11,856+ tests pass. BTSP Phase 2 wired. NG-01/NG-03 resolved. `uzers` → `rustix`. 81 hardcoded strings fixed. Zero TODO/FIXME.
- **ToadStool**: **Major turnaround.** Clippy **CLEAN** (was 2 errors). Fmt **1 diff** (was ~1,899). License updated to `-or-later`. `tar` dep updated.
- **barraCuda**: E0061 **FIXED** (Sprint 29). All files under 600 lines. Clippy clean. 4,393 tests pass. 32 IPC methods. Domain-based socket naming (math.sock). LD-05/LD-10 resolved. BTSP Phase 2. 12-axis deep debt: clean bill.
- **coralReef**: Clippy **CLEAN** (was 7 errors). 8 warnings resolved in `coral-gpu` tests. License updated to `-or-later`.
- **Squirrel**: Clippy CLEAN. fmt PASS. 6,868 tests pass. Commented-out code remains minor residual.
- **biomeOS**: v3.07 — 7,784 tests. All BM-01 through BM-11 RESOLVED. `graph.execute` cross-gate validation enforced (no silent local fallback). Songbird mesh state probing in `composition.health`. `PrimalOperationExecutor` migrated to native RPITIT async fn. `async-trait` removed from biomeos-types, moved to dev-deps in biomeos-api. Test extraction: 8 files >800 LOC → sibling test pattern (all <835 LOC). `--port` honored in api/nucleus modes (TCP+UDS). Zero-debt: 0 unsafe, 0 production mocks, 0 TODO/FIXME, 0 hardcoded primal names, 0 `#[allow(` in production.
- **petalTongue**: All clean. 1 flaky test (`test_resolve_instance_id_error_message_invalid` — passes on retry).
- **rhizoCrypt**: Clippy **CLEAN** (39 `doc_markdown` warnings resolved). All clean.
- **sweetGrass**: Clippy **CLEAN** (unused import fixed). License updated to `-or-later`. `.cargo/config.toml` target-dir still points to `/home/southgate/` (non-blocking).
- **LoamSpine**: Fmt **PASS**. v0.9.16 deep debt overhaul. 1,507 tests (zero flaky). BTSP challenge blake3+uuid entropy. btsp.rs smart-refactored (5 submodules). Storage test isolation fixed. Workspace deps centralized. Registry paths centralized. BTSP provider socket constant. jsonrpc/server.rs split (TCP + UDS). TCP_NODELAY on all TCP sockets. 8×5 concurrent UDS load test. All clean.
- **bingoCube**: Edition **2024** (was 2021). Clippy **CLEAN** (was 15 errors). `deny.toml` added. License updated to `-or-later`.
- **sourDough**: `deny.toml` **added** (was missing). All clean except SPDX on source files.

---

## Tier 2: UniBin / ecoBin

Source: `UNIBIN_ARCHITECTURE_STANDARD.md`, `ECOBIN_ARCHITECTURE_STANDARD.md`

N/A for library primals without IPC daemons (barraCuda, bingoCube, sourDough).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| Single binary | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `server` subcommand | PASS | PASS | DEBT | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS |
| `--port` binds TCP JSON-RPC | PASS | PASS | DEBT | DEBT | PASS | DEBT | DEBT | PASS | PASS | DEBT | DEBT |
| `--help` comprehensive | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `--version` supported | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Standalone startup | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Graceful degradation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Signal handling | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Zero application C deps | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| musl-static cross-compile | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | DEBT | PASS | DEBT | DEBT |
| No hardcoded paths | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **B** | **D** | **C** | **A** | **C** | **C** | **B** | **B** | **C** | **C** |

### Tier 2 Detail

- **BearDog**: Gold standard. `--port` + `--listen` both work. musl-static on x86_64 + aarch64. All checks pass.
- **Songbird**: `--listen` confirmed. `--port` not verified. musl-static both arches.
- **NestGate**: Subcommand is `daemon`, not `server`. `--port` exists but not functional. musl-static x86_64 works; aarch64 not built.
- **ToadStool**: `--port` exists but not wired to server bind. musl-static both arches.
- **coralReef**: `server --port` on coralreef-core and glowplug. Zero C deps. musl-static not yet verified.
- **Squirrel**: `--port` accepted but TCP not primary transport (UDS preferred). musl-static both arches.
- **biomeOS**: Orchestrator pattern — `neural-api`/`api`/`nucleus` subcommands. `--port` binds TCP alongside UDS (v3.05+), `--tcp-only` for pure TCP mode.
- **petalTongue**: `server --port` functional. x86_64 musl works; aarch64 egui headless cross-compile pending.
- **rhizoCrypt**: `server` subcommand with `--port` (tarpc) and `--unix` (UDS). musl-static x86_64 shipped (5.4M, Alpine runtime). aarch64 via CI cross-compile.
- **sweetGrass**: No `--port` flag (uses `--http-address` for full address). musl-static not tested.
- **LoamSpine**: No `--port` flag (uses `--jsonrpc-port`). Source-built binary verified; musl not yet.

---

## Tier 3: IPC Protocol

Source: `PRIMAL_IPC_PROTOCOL.md`

N/A for library primals (barraCuda, bingoCube, sourDough).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| Newline JSON-RPC on UDS | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | PASS |
| Newline JSON-RPC on TCP | PASS | PASS | DEBT | DEBT | PASS | DEBT | DEBT | PASS | PASS | DEBT | PASS |
| Socket at `biomeos/<primal>.sock` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No abstract-only sockets | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Domain symlink | PASS | PASS ↑ | DEBT | DEBT | PASS | DEBT | N/A | DEBT | DEBT | DEBT | DEBT |
| No shared IPC crate | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Socket cleanup on shutdown | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **A** ↑ | **C** | **C** | **A** | **C** | **B** | **B** | **A** | **C** | **B** |

### Tier 3 Detail

- **BearDog**: Full compliance. `crypto.sock` → `beardog.sock` symlink. Both transports newline-framed.
- **Songbird**: Domain symlink **PASS** ↑ (Wave 133): `network.sock` → `songbird.sock` created on bind, removed on shutdown. BTSP Phase 2 handshake on UDS accept when `FAMILY_ID` set (Wave 132). All 7 checks pass.
- **NestGate**: TCP not functional (`--port` not wired). No domain symlink.
- **ToadStool**: TCP not wired. No domain symlink. Socket responds "Method not found" on S168 binary.
- **coralReef**: `shader.sock` + `device.sock` domain symlinks. Both transports. Dual-mode TCP.
- **Squirrel**: TCP not primary. Used to be abstract-only; filesystem socket now via `UniversalListener`. No domain symlink.
- **biomeOS**: Orchestrator — multiple sockets, different pattern. TCP forces UDS in API mode.
- **petalTongue**: Both transports work. No domain symlink.
- **rhizoCrypt**: Dual-mode TCP auto-detects newline vs HTTP. UDS at `biomeos/rhizocrypt.sock`. No domain symlink.
- **sweetGrass**: UDS newline-conformant. TCP is HTTP-only (Axum), not newline JSON-RPC. No domain symlink.
- **LoamSpine**: Both transports work. Domain symlink **PASS** (v0.9.16): `ledger.sock` → `permanence.sock` created on bind, removed on shutdown. Legacy `loamspine.sock` symlink maintained. TCP opt-in via `--port`, UDS unconditional.

---

## Tier 4: Discovery / Self-Knowledge

Source: `CAPABILITY_BASED_DISCOVERY_STANDARD.md`, `PRIMAL_SELF_KNOWLEDGE_STANDARD.md`

N/A for library primals without IPC (barraCuda, bingoCube, sourDough as CLI — assessed as clean).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| `capability.register` / discoverable | PASS | DEBT | DEBT | DEBT | DEBT | DEBT | PASS | DEBT | DEBT | DEBT | DEBT |
| `capability.list` implemented | DEBT | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `identity.get` implemented | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Health triad (`liveness`/`readiness`/`check`) | PASS | PASS | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Zero hardcoded primal names in routing | PASS | DEBT | DEBT | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | PASS |
| Zero primal-specific env vars for routing | PASS | DEBT | DEBT | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | PASS |
| Capability-domain env vars | PASS | DEBT | PASS | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | PASS |
| Socket naming (domain stem primary) | PASS | PASS ↑ | DEBT | DEBT | PASS | PASS | PASS | PASS | DEBT | DEBT | DEBT |
| **Grade** | **B** | **C** ↑ | **C** | **D** | **B** | **D** | **A** | **C** | **B** | **B** | **B** |

### Tier 4 Detail

Discovery debt is the largest cross-ecosystem gap. All non-biomeOS primals depend on biomeOS's
`discover_and_register_primals()` race condition (BM-04 resolved via `topology.rescan` + lazy discovery,
but primals still do not self-register).

- **BearDog**: Zero primal-name refs in routing. Zero primal-specific env vars. `capability.register` **implemented** — dynamic `ipc.register` with Songbird on startup. `capability.list` returns full `methods` array + `provided_capabilities` (Wire L2 complete, Wave 30). `identity.get` implemented. BTSP handshake enforcement live (Wave 31). BD-01 **resolved** (per-field encoding hints + semantic aliases). Discovery: **C** (compliant).
- **Songbird**: 935 refs / 178 files (was 2,558 — 63% reduction). 285 env refs / 68 files. Socket naming now domain-stem primary (`network.sock` with `songbird.sock` legacy symlink). Strongest improvement trajectory. Discovery: **P→C**.
- **NestGate**: 192 refs / 22 files. 32 env refs / 9 files. Near-compliant — all primal-specific env vars eliminated. 7 config/discovery files remain. Discovery: **P→C**.
- **ToadStool**: 2,998 refs / 384 files. 168 env refs / 52 files. `health.liveness` returns "Method not found" on S168 binary. 0 capabilities visible. Discovery: **P** (improving).
- **coralReef**: 2 doc/attribution comments only. Zero routing violations. `shader.sock` + `device.sock` domain symlinks. Discovery: **C** (compliant).
- **Squirrel**: 1,789 refs / 215 files. 225 env refs / 38 files. Build fixed (alpha.36). Bulk is acceptable (logging, aliases, serde compat). Discovery: **P**.
- **biomeOS**: Zero primal-name refs in non-test code. `topology.rescan` + lazy discovery. Full capability suite. Discovery: **C** (gold standard).
- **petalTongue**: 982 refs / 125 files. 77 env refs / 15 files. Major renames landed. `capabilities.list` returns 41 methods. Discovery: **P→C** (improving).
- **rhizoCrypt**: Zero primal-name refs. Zero primal-specific env vars. Dual-mode TCP + UDS. No domain symlink. Discovery: **C**.
- **sweetGrass**: Zero primal-name refs. Zero primal-specific env vars. No domain symlink. Discovery: **C**.
- **LoamSpine**: Zero primal-name refs. Zero primal-specific env vars. 19 capabilities. Domain symlink `ledger.sock`. Wire L2+L3 complete (`methods`, `identity.get`, `provided_capabilities`, `consumed_capabilities`, `cost_estimates`, `operation_dependencies`). Discovery: **C** (compliant).

### Discovery Debt by Volume

| Primal | Primal-Name Refs | Files | Env-Var Refs | Files | Trend |
|--------|-----------------|-------|-------------|-------|-------|
| ToadStool | 2,998 | 384 | 168 | 52 | Improving |
| Squirrel | 1,789 | 215 | 225 | 38 | Build fixed |
| petalTongue | 982 | 125 | 77 | 15 | Improving |
| Songbird | 935 | 178 | 285 | 68 | Strongest trajectory |
| NestGate | 192 | 22 | 32 | 9 | Near-compliant |

---

## Tier 5: Semantic Naming

Source: `SEMANTIC_METHOD_NAMING_STANDARD.md`

N/A for library primals (barraCuda, bingoCube, sourDough).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| `domain.verb[.variant]` format | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No implementation-specific names | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Capabilities documented | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **B** | **B** | **B** | **D** | **A** | **B** | **A** | **A** | **A** | **B** | **B** |

### Tier 5 Detail

- **ToadStool**: S168 binary exposes 0 capabilities and returns "Method not found" for all methods. Source may be better (S173+ work), but not verified on live binary.
- Most primals use `domain.verb` naming correctly (`crypto.hash`, `storage.list`, `health.liveness`, etc.).
- Capability documentation varies — most primals list capabilities in README or via `capability.list` RPC.

---

## Tier 6: Responsibility / Overstep

Source: `PRIMAL_RESPONSIBILITY_MATRIX.md`

| Check | BD | SB | NG | TS | BC | CR | SQ | bOS | PT | RC | SG | LS | BiC | SD |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|
| No code imports from other primals | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No implementation outside owned domain | DEBT | DEBT | DEBT | PASS | PASS | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Correct delegation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No C deps in default build | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **B** | **B** | **B** | **B** | **A** | **A** | **C** | **B** | **A** | **A** | **A** | **A** | **A** | **A** |

### Tier 6 Detail

- **BearDog**: AI/neural tree (~36 files, 11.9K LOC) feature-gated behind `ai` feature per responsibility matrix. `axum` in integration crate.
- **Songbird**: `sled` persistence in orchestrator/sovereign-onion (SB-03, now feature-gated). Pending NestGate storage API.
- **NestGate**: Crypto, discovery, network, MCP, orchestration — all documented in matrix. Crypto delegated to BearDog (NG-05 resolved). Overstep shedding accelerating. NG-01 (metadata persistence) and NG-03 (data.* stubs) both resolved. BTSP Phase 2 handshake wired.
- **Squirrel**: `sled`/`sqlx` persistence, `ed25519-dalek`/TLS — documented. Broader than "cache only" boundary.
- **biomeOS**: `redb` in `biomeos-graph` (metrics storage) — borderline operational state vs NestGate domain.
- **bingoCube**: Strictly within domain (crypto commitment, entropy, reservoir computing). No overstep. No code imports from other primals.

---

## Tier 7: Workspace Dependencies

Source: `WORKSPACE_DEPENDENCY_STANDARD.md`

| Check | BD | SB | NG | TS | BC | CR | SQ | bOS | PT | RC | SG | LS | BiC | SD |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|
| `[workspace.dependencies]` in root | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Members use `{ workspace = true }` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No duplicate inline version pins | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** | **A** |

### Tier 7 Detail

All 14 primals use `[workspace.dependencies]` in their root `Cargo.toml` and member crates
reference dependencies via `{ workspace = true }`. `cargo tree --duplicates` not yet verified
across all primals.

---

## Tier 8: Presentation / Public Surface

Source: `PUBLIC_SURFACE_STANDARD.md`, `SPRING_PRIMAL_PRESENTATION_STANDARD.md`

| Check | BD | SB | NG | TS | BC | CR | SQ | bOS | PT | RC | SG | LS | BiC | SD |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|
| README.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| CHANGELOG.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| CONTEXT.md (<150 lines) | PASS | PASS | PASS | PASS | DEBT | DEBT | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | DEBT |
| PII scan clean | PASS | PASS ↑ | PASS | DEBT | PASS | DEBT | DEBT | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS |
| `deny.toml` present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT |
| `#[expect(reason)]` not `#[allow()]` | DEBT | DEBT | PASS | DEBT | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **C** | **B** ↑ | **A** | **D** | **C** | **B** | **B** | **B** | **C** | **A** | **A** | **A** | **A** | **C** |

### Tier 8 Detail

- **BearDog**: CONTEXT.md present (56 lines). 75 `#[allow(` vs 476 `#[expect(` — allow count reduced (193→75). PII scan **clean** (0 test files with PII patterns).
- **Songbird**: CONTEXT.md present (81 lines). PII scan **PASS** ↑ (Wave 133: 88 hits audited — all domain terms: email enum, password config, crypto keys; documented false positives). `#[expect(` migration ongoing: production code uses `#[expect(reason)]`, crate-root `#[allow]` blocks remain where `expect` causes unfulfilled-expectation. CHANGELOG updated through Wave 133.
- **NestGate**: CONTEXT.md present (82 lines). Zero `#[allow(` (0/0). No PII hits. `deny.toml` present.
- **ToadStool**: CONTEXT.md present (36 lines). **485 `#[allow(`** vs 126 `#[expect(` — 79% `allow`. PII hits in 9 test files.
- **barraCuda**: CONTEXT.md present (89 lines). Zero `#[allow(` — 100% `#[expect(` (0/102). No PII hits.
- **coralReef**: No CONTEXT.md. 4 `#[allow(` vs 168 `#[expect(` (98% `expect`). No PII hits.
- **Squirrel**: CONTEXT.md present (89 lines). 5 `#[allow(` vs 289 `#[expect(` (98% `expect`). PII hits in 3 files.
- **biomeOS**: CONTEXT.md present (75 lines). 4 `#[allow(` vs 361 `#[expect(` (99% `expect`). PII hits in 5 test files.
- **petalTongue**: No CONTEXT.md. 32 `#[allow(` vs 273 `#[expect(` (89% `expect`). PII hit in 1 file.
- **rhizoCrypt**: CONTEXT.md present (95 lines). Zero `#[allow(` (0/47). No PII hits. reqwest eliminated (session 28).
- **sweetGrass**: CONTEXT.md present (76 lines). 2 `#[allow(` vs 51 `#[expect(` (96% `expect`). No PII hits.
- **LoamSpine**: CONTEXT.md present (70 lines). 1 `#[allow(` vs 58 `#[expect(` (98% `expect`). No PII hits.
- **bingoCube**: v0.1.1 — CHANGELOG, CONTEXT.md, `deny.toml` all present. Edition 2024. `forbid(unsafe_code)`, `warn(missing_docs)`, clippy pedantic+nursery clean. SPDX headers on all 20 files. 54 tests passing. 0 `#[allow(` / uses `#[expect(` throughout.
- **sourDough**: No CONTEXT.md. No `deny.toml`. Zero `#[allow(` (0/6). No PII hits.

### PII Scan Notes

All PII hits appear to be path literals in test fixtures, email-pattern validators, or doc examples — not
real secrets. Manual review recommended but no immediate risk.

---

## Tier 9: Deployment / Mobile

Source: `IPC_COMPLIANCE_MATRIX.md` (substrate section), `ECOBIN_ARCHITECTURE_STANDARD.md`

N/A for library primals (barraCuda, bingoCube, sourDough).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| musl-static x86_64 | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | DEBT | DEBT |
| musl-static aarch64 | PASS | PASS | DEBT | PASS | DEBT | PASS | PASS | DEBT | DEBT | DEBT | DEBT |
| TCP listener for mobile | PASS | PASS | DEBT | DEBT | PASS | PASS | DEBT | PASS | PASS | DEBT | PASS |
| Abstract socket support | PASS | DEBT | DEBT | DEBT | PASS | PASS | DEBT | DEBT | DEBT | DEBT | DEBT |
| plasmidBin submission | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **A** | **D** | **C** | **C** | **A** | **C** | **C** | **B** | **D** | **C** |

### Tier 9 Detail

- **BearDog**: Both arches. TCP + abstract sockets. Crypto cross-arch deterministic. In plasmidBin (7.1M musl-static).
- **Songbird**: Both arches. TCP confirmed on Pixel. In plasmidBin (16M musl-static).
- **NestGate**: x86_64 musl works. aarch64 not built. TCP not wired. In plasmidBin (4.9M musl-static).
- **ToadStool**: Both arches. TCP not wired. In plasmidBin (16M musl-static, S168).
- **coralReef**: musl-static not verified for either arch (low priority — GPU primal). TCP works (--port). `genomebin/manifest.toml` current (Iter 80). `deny.toml` enforced (16-crate C/FFI ban). ecoBin ~6.5M.
- **Squirrel**: Both arches. TCP + abstract. `@squirrel` confirmed on GrapheneOS. In plasmidBin (5.8M).
- **biomeOS**: Both arches. `--port` binds TCP alongside UDS (v3.05+), `--tcp-only` for mobile/Android. In plasmidBin (13M).
- **petalTongue**: x86_64 musl works. aarch64 egui headless pending. TCP via `--port`. In plasmidBin (30M).
- **rhizoCrypt**: x86_64 musl-static shipped (5.4M, Alpine runtime). aarch64 via CI cross-compile. TCP works (dual-mode). In plasmidBin (musl-static).
- **sweetGrass**: musl not tested. No TCP (HTTP-only). In plasmidBin (8.8M glibc — needs musl).
- **LoamSpine**: x86_64 source-built verified. aarch64 not tested. TCP works. In plasmidBin (6.9M glibc — needs musl).

---

## Top-3 Debt Items per Primal

| Primal | #1 | #2 | #3 |
|--------|----|----|-----|
| **BearDog** | 75 `#[allow(` → `#[expect(` | `capability.list` Wire L3 polish | Tier 10: filesystem socket at expected family-scoped path |
| **Songbird** | Discovery: 935 primal-name refs | ~~License → `-or-later`~~ **DONE** | `#[allow(` migration (crate-root blocks remain by design) |
| **NestGate** | `--port` not functional | aarch64 musl not built | Coverage 80% → 90% target pending |
| **ToadStool** | ~~1,899 fmt~~ → **CLEAN** | Discovery: 2,998 primal-name refs | 485 `#[allow(` → `#[expect(` |
| **barraCuda** | — | — | — |
| **coralReef** | 7 clippy errors in tests | License → `-or-later` | No CONTEXT.md |
| **Squirrel** | Discovery: 1,789 primal-name refs | Overstep: sled/sqlx/ed25519 beyond domain | 19 commented-out code lines |
| **biomeOS** | 71 `#[async_trait]` blocked by dyn dispatch | `tools/` edition 2021 | — |
| **petalTongue** | Discovery: 982 primal-name refs | No CONTEXT.md | 32 `#[allow(` → `#[expect(` |
| **rhizoCrypt** | ~~Health triad missing~~ → **live-validated PASS** | ~~musl binary is glibc~~ → musl-static shipped | ~~reqwest~~ → hyper/tower (session 28) |
| **sweetGrass** | No `--port` (HTTP-only TCP) | Health triad HTTP-only (not newline) | License → `-or-later` |
| **LoamSpine** | — (LS-03 resolved v0.9.15) | `--port` alias shipped (v0.9.15) | musl binary is glibc |
| **bingoCube** | — (all debt resolved) | — | — |
| **sourDough** | No SPDX headers | No CONTEXT.md | No `deny.toml` |

---

## Rollup Methodology

The rollup grade is computed as the **modal grade** across applicable tiers, with Tier 1 (Build Quality)
and Tier 4 (Discovery) weighted as tie-breakers because they represent code health and ecosystem
interoperability respectively. An F in any critical tier (T1, T2, T3) caps the rollup at D.

---

## Ecosystem Tools

Ecosystem tools (gen2.5) are audited against Tiers 1, 6, 7, and 8 only — IPC, discovery,
semantic naming, and deployment tiers are N/A (tools are not long-running daemons). See
`PRIMAL_SPRING_GARDEN_TAXONOMY.md` § Tools for the formal definition.

### Tool Summary Table

| Tool | Location | Lines | T1 Build | T6 Responsibility | T7 Workspace | T8 Presentation | Coverage | Rollup |
|------|----------|-------|----------|--------------------|--------------|-----------------|----------|--------|
| **bingoCube** | `primals/` | 6,567 | A | A | A | A | 83.4% | **A** |
| **benchScale** | `infra/` | 22,868 | A | A | A | A | 61.9% | **A** |
| **agentReagents** | `infra/` | 6,288 | A | A | A | A | 60.2% | **A** |
| **rustChip** | `sort-after/` | 21,591 | A | A | A | A | 60.8% | **A** |

### Tool Detail

**bingoCube** (v0.1.1 — deep debt sprint complete):
- T1: Edition 2024, `AGPL-3.0-or-later`, `forbid(unsafe_code)`, clippy pedantic+nursery clean, 73 tests passing, SPDX on all files. **83.4% line coverage.**
- T8: CHANGELOG, CONTEXT.md, `deny.toml`, README with accurate AGPL wording. Internal docs removed. No `/home/` paths. `tarpaulin.toml` with `fail-under = 60.0`.
- Refactored: `shell.rs` split into `shell.rs` (789) + `snapshot.rs` (147) + `evolve.rs` (112).
- Public-ready: internal docs deleted, home paths scrubbed, path dep made optional, whitePaper license aligned, broken links fixed.

**benchScale** (v3.0.0 — deep debt sprint complete):
- T1: Edition 2024. `AGPL-3.0-or-later`. `deny(unsafe_code)` + `warn(missing_docs)`. fmt PASS. clippy PASS. Tests PASS (343 passed, 7 ignored). SPDX `-or-later` on all .rs files. `thiserror` upgraded to 2.0. **61.9% line coverage.**
- T8: README (license aligned), CHANGELOG, CONTEXT.md, `deny.toml` (C deps documented). All `#[allow(` → `#[expect(`. `tarpaulin.toml`.
- Unsafe evolution: `EnvGuard` RAII for env var tests, `LeaseList` safe abstraction for libvirt FFI, `libc::kill` → `nix::sys::signal::kill`.
- Refactored: `vm_lifecycle.rs` → `vm_state.rs` (83 lines extracted), `pipeline.rs` → `stages.rs` (731 lines extracted), `config_legacy.rs` → `config/legacy.rs`.
- Public-ready: archive paths scrubbed, license aligned, SPDX consistent, git authors verified.

**agentReagents** (deep debt sprint complete):
- T1: Edition 2024. `AGPL-3.0-or-later`. `forbid(unsafe_code)` + `warn(missing_docs)`. fmt PASS. clippy PASS. Tests PASS (89 passed). SPDX `-or-later`. **60.2% line coverage.**
- T8: README (license aligned, build requirements documented, security note for template passwords), CONTEXT.md, CHANGELOG, `deny.toml` (C deps documented). All `#[allow(` → `#[expect(`. `tarpaulin.toml`.
- Hardcoding evolution: `RegistrationSettings` capability-based pattern replaces hardcoded Songbird registration.
- Public-ready: archive paths scrubbed, path dep documented, template passwords documented.

**rustChip** (5-crate workspace — deep debt sprint + Grade A):
- T1: Edition 2024. `AGPL-3.0-or-later`. `forbid(unsafe_code)` via workspace lints (akida-driver excepted for VFIO/DMA). `warn(missing_docs)` workspace-wide (0 warnings). fmt PASS. clippy PASS (0 warnings, down from 828). Tests PASS (237 tests — 38 akida-chip, 146 akida-driver, 74 akida-models + integration + doctests). SPDX `-or-later`. `deny(unsafe_op_in_unsafe_fn)` enforced. **60.8% line coverage** (software-testable; hardware-only VFIO/mmap excluded via `tarpaulin.toml`).
- T8: README, CHANGELOG, CONTEXT.md, `deny.toml` (C deps documented), `tarpaulin.toml`. All `#[allow(` → `#[expect(`. 31 unsafe blocks with `// SAFETY:` docs.
- Refactored: `vfio/mod.rs` split into `ioctls.rs` (273) + `container.rs` (116), `hybrid/mod.rs` → `software.rs` (79).
- Mock evolution: `create_stub_model` → `create_reference_model`, `SoftSystemBackend` → `SoftwareBackend`, cross-primal refs documented as ecosystem context.

### Tool Debt Summary

| Tool | Remaining Debt |
|------|---------------|
| **bingoCube** | No remaining debt — all tiers A. Coverage 83.4%. Public-ready. |
| **benchScale** | `missing_docs` warnings (22K lines — gradual effort). Coverage 61.9% — aim for 90%. Public-ready. |
| **agentReagents** | `missing_docs` warnings. Path dep on benchScale (documented). Coverage 60.2% — aim for 90%. Public-ready (requires benchScale sibling). |
| **rustChip** | `akida-driver` legitimate unsafe (VFIO/DMA) — documented with SAFETY comments and `deny(unsafe_op_in_unsafe_fn)`. Hardware-only code excluded from CI coverage. Coverage 60.8%. |

---

## Tier 10: Live Deployment (plasmidBin)

Source: `DEPLOYMENT_VALIDATION_STANDARD.md`, plasmidBin revalidation (April 13, 2026)

**12/12 primals ALIVE** via `nucleus_launcher.sh`. All rebuilt as musl-static x86_64 and
harvested to plasmidBin. ecoBin compliance: all static ELF, stripped, blake3 checksummed,
zero dynamic dependencies. **19/19 exp094 composition parity PASS.**
All primals now support UDS (including rhizoCrypt S37, loamSpine v0.9.16, petalTongue v1.6.6).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| fetch.sh checksum verified | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| nucleus_launcher.sh launches | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| health.liveness responds | PASS | PASS | PASS | PASS ↑ | PASS | PASS | PASS | PASS | PASS | PASS | PASS ↑ |
| health.readiness responds | PASS | PASS | PASS | PASS ↑ | PASS | PASS | PASS | PASS | PASS | PASS | PASS ↑ |
| health.check responds | PASS | PASS | PASS | PASS ↑ | PASS | PASS | PASS | PASS | PASS | PASS | PASS ↑ |
| UDS socket at standard path | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS ↑ | PASS ↑ | PASS | PASS ↑ |
| ipc.resolve discoverable | PASS | PASS | PASS | PASS | PASS | PASS | N/A | N/A | PASS | PASS | PASS |
| exp094 parity PASS | PASS | PASS | PASS | PASS | PASS | N/A | N/A | N/A | PASS | PASS | PASS |
| **Grade** | **A** ↑ | **A** ↑ | **A** ↑ | **A** ↑↑ | **A** ↑ | **A** ↑ | **A** ↑ | **A** ↑ | **A** | **A** ↑ | **A** ↑↑ |

**All primals Grade A on Tier 10.** Phase 5 registry seeding ensures Songbird `ipc.resolve`
returns endpoints for all 9 core NUCLEUS primals.

### Tier 10 Detail (April 13 — NUCLEUS Complete)

All 12 primals started via `nucleus_launcher.sh`, health-checked, and validated with exp094.

- **BearDog** v0.9.0: 100 methods. UDS at `beardog-{family}.sock`. TCP JSON-RPC gold standard. exp094: crypto.hash parity, base64 deterministic. **Grade A.**
- **Songbird** v0.2.1: 79 methods. `ipc.resolve` returns `native_endpoint`/`virtual_endpoint` for all 9 NUCLEUS primals (Phase 5 seeding). exp094: resolve_security/compute/storage/method_catalog all PASS. **Grade A.**
- **NestGate** v0.1.0: 30 methods. Persistent UDS connections (LD-02/LD-03 resolved). exp094: storage.store/storage.retrieve roundtrip PASS. **Grade A** ↑.
- **ToadStool** v0.1.0: 163 methods. BTSP auto-detect on all transports (LD-04 resolved). `health.liveness` now responds correctly. exp094: compute_dispatch_alive PASS. **Grade A** ↑↑.
- **barraCuda** v0.3.12: 32 methods (JSON-RPC via BTSP guard line replay — LD-10 resolved). `math-{family}.sock` naming (LD-05 resolved). exp094: stats.mean parity PASS. **Grade A** ↑.
- **coralReef** v0.1.0: 10 methods. `shader.compile.capabilities` returns supported architectures. exp094: shader_supported_archs + shader_wgsl_supported PASS. **Grade A** ↑.
- **Squirrel** v0.1.0: 30 methods. inference.complete/embed/models. UDS at `squirrel-{family}.sock`. **Grade A** ↑.
- **biomeOS** v0.1.0: Neural API substrate. Graph orchestration. **Grade A** ↑.
- **petalTongue** v1.6.6: `--socket` CLI flag for correct UDS path (was missing). **Grade A** ↑.
- **rhizoCrypt** v0.14.0-dev: 28 DAG methods. UDS at `rhizocrypt-{family}.sock` (LD-06 resolved). exp094: dag_alive PASS. **Grade A.**
- **sweetGrass** v0.7.27: 32 braid/anchoring methods. exp094: attribution_alive PASS. **Grade A** ↑.
- **LoamSpine** v0.9.16: 34 methods. UDS-first, TCP opt-in via `--listen` (LD-09 resolved). exp094: ledger_alive PASS. **Grade A** ↑↑.

### Transport Diversity (Live Observed — April 13)

```
beardog:     UDS newline JSON-RPC + TCP newline JSON-RPC (benchscale COMPLIANT)
songbird:    UDS newline JSON-RPC + HTTP TCP (discovery)
toadstool:   UDS newline JSON-RPC (BTSP auto-detect) + tarpc UDS
barracuda:   UDS JSON-RPC (BTSP guard line replay) + tarpc UDS
coralreef:   UDS newline JSON-RPC
squirrel:    UDS newline JSON-RPC
nestgate:    UDS newline JSON-RPC (persistent connections)
rhizocrypt:  UDS newline JSON-RPC + tarpc TCP + HTTP JSON-RPC TCP
sweetgrass:  UDS newline JSON-RPC + HTTP REST + HTTP JSON-RPC
loamspine:   UDS newline JSON-RPC + TCP opt-in (domain symlink, Wire L2+L3)
petaltongue: UDS newline JSON-RPC (--socket flag)
biomeos:     UDS newline JSON-RPC + TCP (--port) + HTTP JSON-RPC (cross-gate)
```

All 12 primals now support newline-delimited JSON-RPC on UDS — the canonical
transport for local NUCLEUS composition.

---

## Cross-References

- `STANDARDS_AND_EXPECTATIONS.md` — primary standards index
- `PRIMAL_GAPS.md` (primalSpring) — per-primal gap registry with fix paths
- `PRIMAL_RESPONSIBILITY_MATRIX.md` — primal roles and domain boundaries
- `PRIMAL_SPRING_GARDEN_TAXONOMY.md` — primal/spring/garden/tool taxonomy
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` — capability-first routing
- `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` — self-knowledge boundaries
- `UNIBIN_ARCHITECTURE_STANDARD.md` — binary architecture
- `ECOBIN_ARCHITECTURE_STANDARD.md` — pure Rust, musl-static
- `PRIMAL_IPC_PROTOCOL.md` — wire framing, sockets
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — method naming
- `WORKSPACE_DEPENDENCY_STANDARD.md` — dependency management
- `PUBLIC_SURFACE_STANDARD.md` — presentation requirements
- `DEPLOYMENT_VALIDATION_STANDARD.md` — runtime deployment contract

---

## Version History

### v2.12.0 (April 13, 2026)

**Phase 40 — NUCLEUS Complete: 12/12 ALIVE, 19/19 exp094 PASS**

- **Tier 10 promoted to ALL A**: Every primal starts, health-checks, and passes exp094 composition parity.
- **LD-01 through LD-10 ALL RESOLVED** upstream — see `primalSpring/docs/PRIMAL_GAPS.md`.
- **barraCuda** v0.3.12: JSON-RPC via BTSP guard line (LD-10), `math-{family}.sock` naming (LD-05), 32 methods.
- **ToadStool**: BTSP auto-detect (LD-04), health.liveness now responds. Grade D→A on Tier 10.
- **NestGate**: Persistent UDS (LD-02/LD-03). storage roundtrip PASS.
- **Songbird**: `ipc.resolve` with `native_endpoint`/`virtual_endpoint` (LD-08). Phase 5 seeding validates all 9 core primals.
- **rhizoCrypt** S37: UDS at standard path (LD-06). 28 DAG methods.
- **loamSpine** v0.9.16: UDS-first, TCP opt-in (LD-09). Grade F→A.
- **petalTongue** v1.6.6: `--socket` CLI flag.
- **primalSpring** v0.9.14: 443 lib tests, 13 FullNucleus capabilities, `IpcError::is_transport_mismatch()`, exp094 19/19.
- **plasmidBin** v4.1.0: Fresh checksums, binary sizes updated, Phase 5 documentation.
- All 12 primals support newline-delimited JSON-RPC on UDS.

### v2.7.0 (April 9, 2026)

**skunkBat Deep Debt Evolution — IPC Surface Established**

- skunkBat: All `--` tiers promoted. T1 A (fmt/clippy/test/doc/deny PASS, Edition 2024, `forbid(unsafe_code)`, SPDX, zero TODO/FIXME, all files <1000L). T2 **A** (UniBin: `server`/`health`/`scan`/`detect` subcommands, `--port`, standalone, graceful degradation, signal handling, zero C deps). T3 **A** (newline JSON-RPC on TCP + UDS, `security.sock` domain symlink, socket cleanup on shutdown). T4 **B** (`capabilities.list` + `identity.get` implemented, health triad, zero hardcoded primal names, capability-domain env vars; `capability.register` not yet self-registering). T5 **A** (`domain.verb` naming throughout). T8 **A** (README rewritten, CONTEXT.md current, `deny.toml`, zero PII, zero `#[allow(`). Rollup: **A**.
- BTSP Phase 1 complete: `FAMILY_ID` socket scoping, `BIOMEOS_SOCKET_DIR` + `XDG_RUNTIME_DIR` fallback, `BIOMEOS_INSECURE` guard.
- Wire Standard L2/L3: `capabilities.list` returns primal/version/methods envelope with `provided_capabilities` and `protocol`/`transport`. `identity.get` returns primal/version/domain/capabilities.
- JSON-RPC client (`rpc.rs`): UDS-first, TCP-fallback, shared by ToadStool discovery + Songbird federation.
- Hardcoding eliminated: `SKUNKBAT_PORT` env var, capability-domain symlinks (`discovery.sock`, `federation.sock`), `DISCOVERY_ENDPOINT`/`FEDERATION_ENDPOINT` env vars.
- Production stubs evolved: `toadstool.rs` and `songbird.rs` rewritten from placeholders to real JSON-RPC IPC clients with graceful degradation.
- Smart refactoring: `dispatch.rs` extracted `try_serialize`/`serialize`/`dispatch_respond` helpers. `VecDeque` rolling window profiler. `/proc/loadavg` system load normalized by CPU count.
- Unused deps removed: `toml`, `anyhow`, `chrono`. `async-trait` retained (justified: dyn-dispatch async).
- 11 stale Dec 2025 root docs archived to `fossilRecord/skunkBat/dec-2025-root-docs/`. README, CONTEXT.md, specs index rewritten.
- 124+ tests, 12 examples, 0 clippy warnings, `cargo deny check` PASS.

### v2.6.0 (April 9, 2026)

**Songbird Waves 131–133: BTSP Phase 2, Deep Debt Sweep, Compliance Uplift**

- Songbird: T1 B→**A** (fmt CLEAN, commented-out code CLEAN). T3 B→**A** (domain symlink `network.sock` → `songbird.sock` on bind/shutdown). T4 D→**C** (socket naming PASS). T8 C→**B** (PII scan: 88 hits audited, all false positives documented). Rollup B→**A**.
- BTSP Phase 2 complete: `perform_server_handshake` wired into UDS accept path when `FAMILY_ID` set. Crypto delegated to security provider via `btsp.session.create/verify/negotiate`.
- SB-02 (ring ghost) resolved: lockfile-only via optional `k8s` feature. SB-03 (sled) confirmed resolved: feature-gated non-default.
- 4 largest production files smart-refactored: `ipc/types.rs` 778→7 modules, `env_config.rs` 764→9 modules, `tarpc_server.rs` 702→3 modules, `manager.rs` 711→6 modules. All under 400L.
- `parking_lot` removed, `colored` 2→3.1. `#[allow(`→`#[expect(` migration for production lints. 7,265+ lib tests, 0 failed.

### v2.5.5 (April 8, 2026)

**barraCuda Sprint 37: Deep Debt — Test Module Refactor & Code Cleanup**

- barraCuda: `methods_tests.rs` (951L) smart-refactored into 6 domain-focused test modules (largest 193L). `buffer_test.rs` println removed. `nadam_gpu.rs` stale comment removed. `force_interpolation.rs` indexed loop → iterator. 12-axis deep debt audit: clean bill on all axes. Zero files >800 lines. 4,207 tests, all quality gates green.

### v2.5.4 (April 8, 2026)

**barraCuda Sprint 36: Domain-Based Socket Naming & Flaky Test Serialization**

- barraCuda: Socket naming evolved from `barracuda.sock` to `math.sock` per `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §3 (domain stem, not primal name). Legacy symlink for backward compat. Domain field in `identity.get`: `"compute"` → `"math"`. `three_springs_tests` serialized in gpu-serial nextest group (Mesa llvmpipe SIGSEGV). BTSP Phase 2 blocked on BearDog session RPC completion. 4,207 tests, all quality gates green.

### v2.5.3 (April 8, 2026)

**barraCuda Sprint 35: Deep Debt — Typed Errors, thiserror & Transport Refactor**

- barraCuda: `validate_insecure_guard` evolved from `Result<(), String>` to typed `BarracudaCoreError::Lifecycle` (last production `Result<_, String>` eliminated). `PppmError` evolved to `#[derive(thiserror::Error)]`. `transport.rs` smart-refactored (866→490 LOC via test extraction). 12-axis deep debt audit: clean bill. All production files under 800 lines. 4,207 tests, all quality gates green.

### v2.5.2 (April 8, 2026)

**barraCuda BTSP Phase 1 + GAP-MATRIX Resolution**

- barraCuda: BTSP Phase 1 socket naming complete — `FAMILY_ID` socket scoping (3-tier env precedence), `BIOMEOS_SOCKET_DIR` support, `BIOMEOS_INSECURE` guard. Resolves GAP-MATRIX-12. plasmidBin metadata updated to v0.3.11 (resolves GAP-MATRIX-06). 4,207 tests (was 4,187). BTSP Phase 2+: BearDog `btsp.session.*` now available (Wave 31) — integrate handshake in barraCuda listener.

### v2.5.1 (April 8, 2026)

**Wire Standard L2 Adoptions**

- barraCuda: Wire Standard L2 compliant — `capabilities.list` returns `{primal, version, methods}` envelope with `provided_capabilities`, `consumed_capabilities`, `protocol`, `transport`. `identity.get` implemented. 31 methods (was 30). Both JSON-RPC and tarpc wired. (Library primal — matrix IPC tiers remain N/A but server mode is L2 compliant.)

### v2.2.0 (April 5, 2026)

**Tier 10: Live Deployment — plasmidBin runtime validation**

- Added Tier 10: Live Deployment tier sourced from `DEPLOYMENT_VALIDATION_STANDARD.md`
- Data from plasmidBin v2026.03.25 end-to-end validation (fetch → start → probe)
- 10 binaries fetched, 7 started, 5 healthy, 1 partial (rhizoCrypt — since promoted to A via S28–S30 deep debt/BTSP work), 1 crash (LoamSpine — resolved v0.9.15)
- Transport diversity documented: 5 distinct patterns across 7 tested primals
- Only BearDog fully passes `benchscale validate ipc` on TCP
- LoamSpine F → resolved: tokio nesting crash fixed in v0.9.15; re-validation pending
- Summary table expanded from 9 to 10 tiers
- Rollup adjusted: ~~rhizoCrypt A → B~~ → **A** (live-validated: identity.get + Format E capabilities + health triad + UDS + newline TCP), LoamSpine B → C (crash — now resolved, pending re-validation)

### v2.1.0 (April 5, 2026)

**rustChip B → A: 828→0 clippy, 0→237 tests, 60.8% coverage**

- rustChip: B → A — 828 clippy warnings resolved (cast allows for numeric code, source fixes), 237 tests added (was 0), 60.8% coverage (hardware-only VFIO/mmap excluded), `tarpaulin.toml` with fail-under=60.0
- All 4 ecosystem tools now at Grade A

### v2.0.0 (April 5, 2026)

**Deep Debt Resolution + Public Readiness Sprint**

- bingoCube: A (maintained) — public-readiness scrub, 83.4% coverage, shell.rs refactored, internal docs removed
- benchScale: B → A — public-readiness scrub, 61.9% coverage (was 35.5%), unsafe evolution (EnvGuard, LeaseList, nix kill), thiserror 2.0, large file refactoring, all #[allow( → #[expect(
- agentReagents: B → A — public-readiness scrub, 60.2% coverage (was 7.1%), capability-based RegistrationSettings, all #[allow( → #[expect(
- rustChip: B (maintained) — 31 unsafe SAFETY docs, deny(unsafe_op_in_unsafe_fn), large file refactoring, mock/stub renaming
- All 3 public-bound tools (bingoCube, benchScale, agentReagents) now at Grade A with >=60% test coverage
- tarpaulin.toml fail-under=60.0 added to all 3 public-bound repos
- C dependencies documented in deny.toml across all tools

### v1.1.0 (April 4, 2026)

**Tool Taxonomy + Full Tool Compliance Sprint**

- bingoCube: F → A (edition 2024, license `-or-later`, `forbid(unsafe)`, clippy pedantic+nursery clean, 54 tests, SPDX, CHANGELOG, CONTEXT.md, `deny.toml`)
- benchScale: C → B (license `-or-later`, fmt fixed, clippy clean, 401 tests passing, 18 doctests fixed, `deny.toml`, SPDX updated)
- agentReagents: D → B (license `-or-later`, fmt clean, clippy clean, 52 tests passing, CHANGELOG + `deny.toml`, SPDX updated)
- rustChip: C → B (edition 2024, workspace lints, `forbid(unsafe)`, clippy clean, `#[allow(` → `#[expect(`, CONTEXT.md + `deny.toml`)
- All 4 tools now grade B or above
- Added Ecosystem Tools section with Tier 1/6/7/8 audit data
- Cross-references updated with `PRIMAL_SPRING_GARDEN_TAXONOMY.md`

### v1.0.0 (April 4, 2026)

**Initial Comprehensive Matrix — 9 Tiers, 14 Primals, 40+ Dimensions**

- Created from full wateringHole standards corpus review (31 active documents)
- Absorbed all data from `IPC_COMPLIANCE_MATRIX.md` v1.6.0 (archived)
- Incorporated April 4 ecosystem audit (fmt, clippy, tests, edition, license)
- Phase 2 checks: `forbid(unsafe)`, `warn(missing_docs)`, CONTEXT.md, `allow` vs `expect`,
  PII scan, workspace dependencies, commented-out code, SPDX headers, C deps via `cargo tree`
- Grade distribution: 2 A, 7 B, 3 C, 1 D, 1 F
- Top ecosystem gaps: discovery debt (5 primals), license alignment (8 primals),
  `#[allow(` migration (4 primals), domain symlinks (8 primals)
