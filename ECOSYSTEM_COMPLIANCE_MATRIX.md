# Ecosystem Compliance Matrix

**Version:** 1.0.0
**Date:** April 4, 2026
**Status:** Living document — updated as primals evolve
**Authority:** wateringHole (ecoPrimals Core Standards)
**Supersedes:** `IPC_COMPLIANCE_MATRIX.md` v1.6.0 (archived to `fossilRecord/`)

This matrix tracks every primal's alignment across all auditable dimensions
defined in the 31 active wateringHole standards. Each primal receives a letter
grade per tier (A–F) and a rollup grade across all applicable tiers.

Data sourced from: April 4, 2026 full ecosystem audit (14 primals),
`IPC_COMPLIANCE_MATRIX.md` v1.6.0, `PRIMAL_GAPS.md` live tracking,
esotericWebb and ludoSpring compositions (March–April 2026), and direct
source inspection via `rg`, `cargo`, and manual review.

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
| RC | rhizoCrypt | Encrypted Storage |
| SG | sweetGrass | Data / Indexing |
| LS | LoamSpine | Mesh Networking |
| BiC | bingoCube | Entropy / Game Math |
| SD | sourDough | CLI Scaffolding |

---

## Summary Table

| Primal | T1 Build | T2 UniBin | T3 IPC | T4 Discovery | T5 Naming | T6 Responsibility | T7 Workspace | T8 Presentation | T9 Deploy | Rollup |
|--------|----------|-----------|--------|--------------|-----------|-------------------|--------------|-----------------|-----------|--------|
| **BearDog** | C | A | A | B | B | B | A | C | A | **B** |
| **Songbird** | B | B | B | D | B | B | A | C | A | **C** |
| **NestGate** | B | D | C | C | B | B | A | A | D | **C** |
| **ToadStool** | D | C | C | D | D | B | A | D | C | **D** |
| **barraCuda** | F | -- | -- | -- | -- | A | A | C | -- | **D** |
| **coralReef** | C | A | A | B | A | A | A | B | C | **B** |
| **Squirrel** | B | C | C | D | B | C | A | B | A | **C** |
| **biomeOS** | B | C | B | A | A | B | A | B | C | **B** |
| **petalTongue** | A | B | B | C | A | A | A | C | C | **B** |
| **rhizoCrypt** | A | B | A | B | A | A | A | A | C | **A** |
| **sweetGrass** | B | C | C | B | B | A | A | A | D | **B** |
| **LoamSpine** | A | C | B | B | B | A | A | A | C | **B** |
| **bingoCube** | F | -- | -- | -- | -- | B | A | F | -- | **F** |
| **sourDough** | B | -- | -- | -- | -- | A | A | C | -- | **B** |

### Grade Distribution

| Grade | Count | Primals |
|-------|-------|---------|
| A | 1 | rhizoCrypt |
| B | 7 | BearDog, coralReef, biomeOS, petalTongue, sweetGrass, LoamSpine, sourDough |
| C | 3 | Songbird, NestGate, Squirrel |
| D | 2 | ToadStool, barraCuda |
| F | 1 | bingoCube |

---

## Tier 1: Build Quality

Source: `STANDARDS_AND_EXPECTATIONS.md`, `LICENSING_AND_COPYLEFT.md`

| Check | BD | SB | NG | TS | BC | CR | SQ | bOS | PT | RC | SG | LS | BiC | SD |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|
| `cargo fmt` | PASS | PASS | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| `cargo clippy -D warnings` | PASS | PASS | PASS | DEBT | DEBT | DEBT | PASS | PASS | PASS | DEBT | DEBT | PASS | DEBT | PASS |
| `cargo test --all-features` | DEBT | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| `cargo doc --no-deps` | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| Edition 2024 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| `forbid(unsafe_code)` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| `warn(missing_docs)` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| No TODO/FIXME/HACK | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| No files >1000 lines | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| No `.unwrap()` in lib | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| No commented-out code | DEBT | DEBT | PASS | DEBT | DEBT | DEBT | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS | PASS |
| License `AGPL-3.0-or-later` | DEBT | DEBT | DEBT | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | DEBT | PASS | DEBT | PASS |
| SPDX header on sources | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | DEBT |
| **Grade** | **C** | **B** | **B** | **D** | **F** | **C** | **B** | **B** | **A** | **A** | **B** | **A** | **F** | **B** |

### Tier 1 Detail

- **BearDog**: 1 env-dependent test failure (`dispatch_doctor_comprehensive` needs live primals). 71 commented-out code lines. License needs `-or-later`. SPDX says `-only`.
- **Songbird**: 28 commented-out code lines. License needs `-or-later`.
- **NestGate**: 1 file fmt deviation (`migration.rs:189`). License needs `-or-later`. `deny(unsafe_code)` at workspace + `forbid` per-crate in `code/crates/`.
- **ToadStool**: ~1,899 lines of fmt diff. Clippy: `manual_let_else` + deprecated `GenericArray::from_slice`. 485 `#[allow(` vs 126 `#[expect(`. License needs `-or-later`.
- **barraCuda**: **Compile failure** in `barracuda-naga-exec` (E0061 missing arg to `eval_math`). Blocks all tests. `executor.rs` at 1,097 lines (limit 1,000). 1 unfulfilled lint expectation.
- **coralReef**: Clippy: 7 errors (`items_after_statements`, `doc_markdown` in `coral-gpu` tests). 17 commented-out lines. License needs `-or-later`.
- **Squirrel**: 19 commented-out code lines. `unsafe_code = "forbid"` via workspace lints. `missing_docs = "warn"` via workspace lints. 5 `#[allow(` vs 289 `#[expect(`.
- **biomeOS**: `tools/` sub-crate still on edition 2021. 5 commented-out lines. License needs `-or-later`. `deny` workspace + `forbid` per-crate.
- **petalTongue**: Near-perfect. 1 commented-out line (negligible). License already `-or-later`.
- **rhizoCrypt**: Clippy: 5 `doc_markdown` in test file only. `deny(unsafe_code)` + `cfg_attr(not(test), forbid)`.
- **sweetGrass**: Clippy: 1 unused import in `tcp_jsonrpc.rs:123`. License needs `-or-later`. `.cargo/config.toml` target-dir issue.
- **LoamSpine**: Clean across all items. `forbid(unsafe_code)` at workspace level.
- **bingoCube**: Edition 2021. No `forbid(unsafe_code)`. No `warn(missing_docs)`. 15 clippy cast errors. No SPDX headers. License bare `AGPL-3.0`. No `deny.toml`.
- **sourDough**: No SPDX headers in source files. `forbid(unsafe_code)` + `missing_docs = "warn"` via workspace lints. `deny.toml` missing.

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
| musl-static cross-compile | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | DEBT | DEBT | DEBT | DEBT |
| No hardcoded paths | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **B** | **D** | **C** | **A** | **C** | **C** | **B** | **B** | **C** | **C** |

### Tier 2 Detail

- **BearDog**: Gold standard. `--port` + `--listen` both work. musl-static on x86_64 + aarch64. All checks pass.
- **Songbird**: `--listen` confirmed. `--port` not verified. musl-static both arches.
- **NestGate**: Subcommand is `daemon`, not `server`. `--port` exists but not functional. musl-static x86_64 works; aarch64 not built.
- **ToadStool**: `--port` exists but not wired to server bind. musl-static both arches.
- **coralReef**: `server --port` on coralreef-core and glowplug. Zero C deps. musl-static not yet verified.
- **Squirrel**: `--port` accepted but TCP not primary transport (UDS preferred). musl-static both arches.
- **biomeOS**: Orchestrator pattern — `neural-api`/`api` subcommand, not `server`. `--port` forces UDS in some modes.
- **petalTongue**: `server --port` functional. x86_64 musl works; aarch64 egui headless cross-compile pending.
- **rhizoCrypt**: `server` subcommand with `--port` (tarpc) and `--unix` (UDS). musl via CI cross-compile jobs.
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
| Domain symlink | PASS | DEBT | DEBT | DEBT | PASS | DEBT | N/A | DEBT | DEBT | DEBT | DEBT |
| No shared IPC crate | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Socket cleanup on shutdown | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **B** | **C** | **C** | **A** | **C** | **B** | **B** | **A** | **C** | **B** |

### Tier 3 Detail

- **BearDog**: Full compliance. `crypto.sock` → `beardog.sock` symlink. Both transports newline-framed.
- **Songbird**: Registry primal — domain symlink not strictly required but standard says create one. Missing.
- **NestGate**: TCP not functional (`--port` not wired). No domain symlink.
- **ToadStool**: TCP not wired. No domain symlink. Socket responds "Method not found" on S168 binary.
- **coralReef**: `shader.sock` + `device.sock` domain symlinks. Both transports. Dual-mode TCP.
- **Squirrel**: TCP not primary. Used to be abstract-only; filesystem socket now via `UniversalListener`. No domain symlink.
- **biomeOS**: Orchestrator — multiple sockets, different pattern. TCP forces UDS in API mode.
- **petalTongue**: Both transports work. No domain symlink.
- **rhizoCrypt**: Dual-mode TCP auto-detects newline vs HTTP. UDS at `biomeos/rhizocrypt.sock`. No domain symlink.
- **sweetGrass**: UDS newline-conformant. TCP is HTTP-only (Axum), not newline JSON-RPC. No domain symlink.
- **LoamSpine**: Both transports work. No domain symlink.

---

## Tier 4: Discovery / Self-Knowledge

Source: `CAPABILITY_BASED_DISCOVERY_STANDARD.md`, `PRIMAL_SELF_KNOWLEDGE_STANDARD.md`

N/A for library primals without IPC (barraCuda, bingoCube, sourDough as CLI — assessed as clean).

| Check | BD | SB | NG | TS | CR | SQ | bOS | PT | RC | SG | LS |
|-------|----|----|----|----|----|----|-----|----|----|----|----|
| `capability.register` / discoverable | DEBT | DEBT | DEBT | DEBT | DEBT | DEBT | PASS | DEBT | DEBT | DEBT | DEBT |
| `capability.list` implemented | DEBT | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `identity.get` implemented | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Health triad (`liveness`/`readiness`/`check`) | PASS | PASS | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Zero hardcoded primal names in routing | PASS | DEBT | DEBT | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | PASS |
| Zero primal-specific env vars for routing | PASS | DEBT | DEBT | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | PASS |
| Capability-domain env vars | PASS | DEBT | PASS | DEBT | PASS | DEBT | PASS | DEBT | PASS | PASS | PASS |
| Socket naming (domain stem primary) | PASS | DEBT | DEBT | DEBT | PASS | PASS | PASS | PASS | DEBT | DEBT | DEBT |
| **Grade** | **B** | **D** | **C** | **D** | **B** | **D** | **A** | **C** | **B** | **B** | **B** |

### Tier 4 Detail

Discovery debt is the largest cross-ecosystem gap. All non-biomeOS primals depend on biomeOS's
`discover_and_register_primals()` race condition (BM-04 resolved via `topology.rescan` + lazy discovery,
but primals still do not self-register).

- **BearDog**: Zero primal-name refs in routing. Zero primal-specific env vars. `capability.list` returns empty — needs method implementation. Discovery: **C** (compliant).
- **Songbird**: 935 refs / 178 files (was 2,558 — 63% reduction). 285 env refs / 68 files. Strongest improvement trajectory but still highest absolute debt. Discovery: **P→C**.
- **NestGate**: 192 refs / 22 files. 32 env refs / 9 files. Near-compliant — all primal-specific env vars eliminated. 7 config/discovery files remain. Discovery: **P→C**.
- **ToadStool**: 2,998 refs / 384 files. 168 env refs / 52 files. `health.liveness` returns "Method not found" on S168 binary. 0 capabilities visible. Discovery: **P** (improving).
- **coralReef**: 2 doc/attribution comments only. Zero routing violations. `shader.sock` + `device.sock` domain symlinks. Discovery: **C** (compliant).
- **Squirrel**: 1,789 refs / 215 files. 225 env refs / 38 files. Build fixed (alpha.36). Bulk is acceptable (logging, aliases, serde compat). Discovery: **P**.
- **biomeOS**: Zero primal-name refs in non-test code. `topology.rescan` + lazy discovery. Full capability suite. Discovery: **C** (gold standard).
- **petalTongue**: 982 refs / 125 files. 77 env refs / 15 files. Major renames landed. `capabilities.list` returns 41 methods. Discovery: **P→C** (improving).
- **rhizoCrypt**: Zero primal-name refs. Zero primal-specific env vars. Dual-mode TCP + UDS. No domain symlink. Discovery: **C**.
- **sweetGrass**: Zero primal-name refs. Zero primal-specific env vars. No domain symlink. Discovery: **C**.
- **LoamSpine**: Zero primal-name refs. Zero primal-specific env vars. 19 capabilities. No domain symlink. Discovery: **C**.

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
| **Grade** | **B** | **B** | **B** | **B** | **A** | **A** | **C** | **B** | **A** | **A** | **A** | **A** | **B** | **A** |

### Tier 6 Detail

- **BearDog**: AI/neural tree (~36 files, 11.9K LOC) feature-gated behind `ai` feature per responsibility matrix. `axum` in integration crate.
- **Songbird**: `sled` persistence in orchestrator/sovereign-onion (SB-03, now feature-gated). Pending NestGate storage API.
- **NestGate**: Crypto, discovery, network, MCP, orchestration — all documented in matrix. Crypto delegated to BearDog (NG-05 resolved). Overstep shedding accelerating.
- **Squirrel**: `sled`/`sqlx` persistence, `ed25519-dalek`/TLS — documented. Broader than "cache only" boundary.
- **biomeOS**: `redb` in `biomeos-graph` (metrics storage) — borderline operational state vs NestGate domain.
- **bingoCube**: Within domain (entropy/game math). No overstep detected.

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
| CHANGELOG.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | PASS |
| CONTEXT.md (<150 lines) | PASS | PASS | PASS | PASS | DEBT | DEBT | PASS | PASS | DEBT | PASS | PASS | PASS | DEBT | DEBT |
| PII scan clean | DEBT | DEBT | PASS | DEBT | PASS | DEBT | DEBT | DEBT | DEBT | PASS | PASS | PASS | PASS | PASS |
| `deny.toml` present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DEBT | DEBT |
| `#[expect(reason)]` not `#[allow()]` | DEBT | DEBT | PASS | DEBT | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | N/A | PASS |
| **Grade** | **C** | **C** | **A** | **D** | **C** | **B** | **B** | **B** | **C** | **A** | **A** | **A** | **F** | **C** |

### Tier 8 Detail

- **BearDog**: CONTEXT.md present (56 lines). 193 `#[allow(` vs 361 `#[expect(` — high allow count. PII hits in 2 test files (path patterns, not real secrets).
- **Songbird**: CONTEXT.md present (78 lines). 393 `#[allow(` vs 406 `#[expect(` — nearly 50/50 ratio. PII hits in 6 test files.
- **NestGate**: CONTEXT.md present (82 lines). Zero `#[allow(` (0/0). No PII hits. `deny.toml` present.
- **ToadStool**: CONTEXT.md present (36 lines). **485 `#[allow(`** vs 126 `#[expect(` — 79% `allow`. PII hits in 9 test files.
- **barraCuda**: No CONTEXT.md. Zero `#[allow(` — 100% `#[expect(` (0/102). No PII hits.
- **coralReef**: No CONTEXT.md. 4 `#[allow(` vs 168 `#[expect(` (98% `expect`). No PII hits.
- **Squirrel**: CONTEXT.md present (89 lines). 5 `#[allow(` vs 289 `#[expect(` (98% `expect`). PII hits in 3 files.
- **biomeOS**: CONTEXT.md present (75 lines). 4 `#[allow(` vs 361 `#[expect(` (99% `expect`). PII hits in 5 test files.
- **petalTongue**: No CONTEXT.md. 32 `#[allow(` vs 273 `#[expect(` (89% `expect`). PII hit in 1 file.
- **rhizoCrypt**: CONTEXT.md present (94 lines). Zero `#[allow(` (0/47). No PII hits.
- **sweetGrass**: CONTEXT.md present (76 lines). 2 `#[allow(` vs 51 `#[expect(` (96% `expect`). No PII hits.
- **LoamSpine**: CONTEXT.md present (70 lines). 1 `#[allow(` vs 58 `#[expect(` (98% `expect`). No PII hits.
- **bingoCube**: No CHANGELOG.md. No CONTEXT.md. No `deny.toml`. No lint attributes at all (0/0).
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
| musl-static x86_64 | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | DEBT | DEBT | DEBT |
| musl-static aarch64 | PASS | PASS | DEBT | PASS | DEBT | PASS | PASS | DEBT | DEBT | DEBT | DEBT |
| TCP listener for mobile | PASS | PASS | DEBT | DEBT | PASS | PASS | DEBT | PASS | PASS | DEBT | PASS |
| Abstract socket support | PASS | DEBT | DEBT | DEBT | PASS | PASS | DEBT | DEBT | DEBT | DEBT | DEBT |
| plasmidBin submission | PASS | PASS | PASS | PASS | DEBT | PASS | PASS | PASS | PASS | PASS | PASS |
| **Grade** | **A** | **A** | **D** | **C** | **C** | **A** | **C** | **C** | **C** | **D** | **C** |

### Tier 9 Detail

- **BearDog**: Both arches. TCP + abstract sockets. Crypto cross-arch deterministic. In plasmidBin (7.1M musl-static).
- **Songbird**: Both arches. TCP confirmed on Pixel. In plasmidBin (16M musl-static).
- **NestGate**: x86_64 musl works. aarch64 not built. TCP not wired. In plasmidBin (4.9M musl-static).
- **ToadStool**: Both arches. TCP not wired. In plasmidBin (16M musl-static, S168).
- **coralReef**: musl-static not verified for either arch. TCP works (--port). Not yet in plasmidBin.
- **Squirrel**: Both arches. TCP + abstract. `@squirrel` confirmed on GrapheneOS. In plasmidBin (5.8M).
- **biomeOS**: Both arches. Forces UDS even when `--port` specified (TCP-only mode needed). In plasmidBin (12M).
- **petalTongue**: x86_64 musl works. aarch64 egui headless pending. TCP via `--port`. In plasmidBin (30M).
- **rhizoCrypt**: musl CI jobs for both arches. TCP works (dual-mode). In plasmidBin (5.4M glibc — needs musl).
- **sweetGrass**: musl not tested. No TCP (HTTP-only). In plasmidBin (8.8M glibc — needs musl).
- **LoamSpine**: x86_64 source-built verified. aarch64 not tested. TCP works. In plasmidBin (6.9M glibc — needs musl).

---

## Top-3 Debt Items per Primal

| Primal | #1 | #2 | #3 |
|--------|----|----|-----|
| **BearDog** | License → `-or-later` | 193 `#[allow(` → `#[expect(` | 71 commented-out code lines |
| **Songbird** | Discovery: 935 primal-name refs | License → `-or-later` | 393 `#[allow(` → `#[expect(` |
| **NestGate** | `--port` not functional | License → `-or-later` | aarch64 musl not built |
| **ToadStool** | ~1,899 lines fmt debt | Discovery: 2,998 primal-name refs | 485 `#[allow(` → `#[expect(` |
| **barraCuda** | Compile failure (E0061) | `executor.rs` >1,000 lines | No CONTEXT.md |
| **coralReef** | 7 clippy errors in tests | License → `-or-later` | No CONTEXT.md |
| **Squirrel** | Discovery: 1,789 primal-name refs | Overstep: sled/sqlx/ed25519 beyond domain | 19 commented-out code lines |
| **biomeOS** | License → `-or-later` | `--port` forces UDS (TCP-only needed) | `tools/` edition 2021 |
| **petalTongue** | Discovery: 982 primal-name refs | No CONTEXT.md | 32 `#[allow(` → `#[expect(` |
| **rhizoCrypt** | musl binary is glibc (needs musl-static) | No domain symlink | 5 clippy `doc_markdown` in tests |
| **sweetGrass** | No `--port` (HTTP-only TCP) | License → `-or-later` | musl-static not tested |
| **LoamSpine** | No `--port` (uses `--jsonrpc-port`) | musl binary is glibc | No domain symlink |
| **bingoCube** | Edition 2021 + no `forbid(unsafe)` | No CHANGELOG / CONTEXT / deny.toml | 15 clippy cast errors |
| **sourDough** | No SPDX headers | No CONTEXT.md | No `deny.toml` |

---

## Rollup Methodology

The rollup grade is computed as the **modal grade** across applicable tiers, with Tier 1 (Build Quality)
and Tier 4 (Discovery) weighted as tie-breakers because they represent code health and ecosystem
interoperability respectively. An F in any critical tier (T1, T2, T3) caps the rollup at D.

---

## Cross-References

- `STANDARDS_AND_EXPECTATIONS.md` — primary standards index
- `PRIMAL_GAPS.md` (primalSpring) — per-primal gap registry with fix paths
- `PRIMAL_RESPONSIBILITY_MATRIX.md` — primal roles and domain boundaries
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` — capability-first routing
- `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` — self-knowledge boundaries
- `UNIBIN_ARCHITECTURE_STANDARD.md` — binary architecture
- `ECOBIN_ARCHITECTURE_STANDARD.md` — pure Rust, musl-static
- `PRIMAL_IPC_PROTOCOL.md` — wire framing, sockets
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — method naming
- `WORKSPACE_DEPENDENCY_STANDARD.md` — dependency management
- `PUBLIC_SURFACE_STANDARD.md` — presentation requirements

---

## Version History

### v1.0.0 (April 4, 2026)

**Initial Comprehensive Matrix — 9 Tiers, 14 Primals, 40+ Dimensions**

- Created from full wateringHole standards corpus review (31 active documents)
- Absorbed all data from `IPC_COMPLIANCE_MATRIX.md` v1.6.0 (archived)
- Incorporated April 4 ecosystem audit (fmt, clippy, tests, edition, license)
- Phase 2 checks: `forbid(unsafe)`, `warn(missing_docs)`, CONTEXT.md, `allow` vs `expect`,
  PII scan, workspace dependencies, commented-out code, SPDX headers, C deps via `cargo tree`
- Grade distribution: 1 A, 7 B, 3 C, 2 D, 1 F
- Top ecosystem gaps: discovery debt (5 primals), license alignment (8 primals),
  `#[allow(` migration (4 primals), domain symlinks (8 primals)
