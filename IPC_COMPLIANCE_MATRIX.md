# IPC Compliance Matrix

**Version:** 1.6.0
**Date:** April 3, 2026
**Status:** Living document — updated as primals evolve
**Authority:** wateringHole (ecoPrimals Core Standards)

This matrix tracks each primal's alignment across the IPC interoperability
dimensions defined in `PRIMAL_IPC_PROTOCOL.md` v3.1, `UNIBIN_ARCHITECTURE_STANDARD.md`
v1.1, `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2, and
`SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2.

Cross-references: `PRIMAL_RESPONSIBILITY_MATRIX.md` v3.0 (primal roles,
capability domains, overstep detail).

Data sourced from esotericWebb's first live multi-primal composition
(March 2026), direct inspection of each primal's source code,
**live cross-hardware deployment testing** (March 27, 2026) across
x86_64 eastgate + aarch64 Pixel/GrapheneOS on iPhone hotspot,
**primalSpring Phase 23f** composition decomposition (7 subsystems,
89 deploy graphs, 32 gaps), **ludoSpring V37.1** plasmidBin live
gap matrix (95/141 checks, experiments 084-098), and **primalSpring
Phase 23o** full audit cycle (April 3, 2026).

---

## Legend

| Symbol | Meaning |
|--------|---------|
| C | Conformant |
| P | Partial — works but deviates from standard |
| X | Non-conformant — breaks interop |
| ? | Not yet verified |
| -- | Not applicable |

---

## Wire Framing

Standard: newline-delimited JSON-RPC (`\n`-terminated) on at least one
transport (UDS or TCP). See `PRIMAL_IPC_PROTOCOL.md` v3.1 Wire Framing.

| Primal | UDS Framing | TCP Framing | Status | Notes |
|--------|-------------|-------------|--------|-------|
| **rhizocrypt** | Newline | Newline + HTTP POST (dual-mode, first-byte peek) | **C** | Dual-mode TCP auto-detects raw newline vs HTTP POST per connection. UDS uses newline framing. Fixed in v0.14.0-dev session 23. |
| **loamspine** | Newline | Newline | C | UDS newline-conformant (verified April 1). TCP JSON-RPC dual-mode. v0.9.15 starts cleanly. |
| **sweetgrass** | Newline | HTTP POST (Axum) | **P** | UDS is newline-conformant. TCP is HTTP-only. Sufficient for UDS composition. |
| **squirrel** | Newline (abstract) | -- | **P** | Newline framing correct, but socket is abstract-namespace only (see Discovery). No TCP listener. |
| **beardog** | Newline | Newline | C | Both transports use raw newline framing. |
| **songbird** | Newline | Newline | C | Standard newline framing on both transports. |
| **petaltongue** | Newline | Newline | C | UDS newline-conformant. TCP via `server --port <N>` (March 31). |
| **nestgate** | Newline | -- | **X** | Socket-only by default. `--port` exists but is non-functional. **musl-static binary segfaults (exit 139) on `--help`** — ecoBin non-compliant. glibc dynamic build works. |
| **toadstool** | Newline | -- | **P** | `--port` exists but is not forwarded to implementation. |
| **coralreef** | Newline | Newline + HTTP (dual-mode) | **C** | UDS is newline. `--port` binds raw newline TCP. `--rpc-bind` for jsonrpsee HTTP (separate). Both coralreef-core and glowplug support `--port`. |
| **biomeOS** | -- | HTTP (multiple modes) | **P** | Not a simple `server --port` primal. Orchestrator, not peer. |

---

## Socket Path Conformance

Standard: filesystem socket at `$XDG_RUNTIME_DIR/biomeos/<primal>.sock`.
See `PRIMAL_IPC_PROTOCOL.md` Socket Path Convention and
`CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1.

| Primal | Socket Path | Filesystem? | In biomeos/? | Domain Symlink | Status | Notes |
|--------|-------------|-------------|-------------|----------------|--------|-------|
| **rhizocrypt** | `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock` | Yes | Yes | -- | **C** | `--unix [PATH]` flag; default ecosystem standard path. **RC-01 RESOLVED** (v0.14.0-dev s23). Live verified April 1. |
| **loamspine** | `/run/user/1000/biomeos/loamspine.sock` | Yes | Yes | No | **C** | **LS-03 RESOLVED** (v0.9.15). Conformant `biomeos/` path. Infant discovery fails gracefully. |
| **sweetgrass** | `/run/user/1000/biomeos/sweetgrass.sock` | Yes | Yes | No | **P** | Conformant path, no family suffix. Missing domain symlink. |
| **squirrel** | `$XDG_RUNTIME_DIR/biomeos/squirrel.sock` + `@squirrel` (abstract) | Yes | Yes | No | **C** | `UniversalListener` (alpha.25b): abstract → filesystem → TCP fallback. Filesystem socket now discoverable. |
| **beardog** | `/run/user/1000/biomeos/beardog.sock` | Yes | Yes | `crypto.sock` | C | Conformant path. Domain symlink `crypto.sock` → `beardog.sock` created at bind, cleaned on shutdown. |
| **songbird** | `/run/user/1000/biomeos/songbird.sock` | Yes | Yes | No | C | Registry primal, domain symlink not required. |
| **petaltongue** | `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock` | Yes | Yes | No | C | Conformant `biomeos/` path (March 31). |
| **nestgate** | `/run/user/1000/biomeos/nestgate.sock` | Yes | Yes | No | **P** | Conformant path. Missing domain symlink. |
| **toadstool** | `/run/user/1000/biomeos/toadstool.sock` + `.jsonrpc.sock` | Yes | Yes | No | **P** | Socket created at conformant path, but responds "Method not found" to all methods (S168 binary). |
| **coralreef** | `/run/user/1000/biomeos/coralreef-core-{family}.sock` | Yes | Yes | `shader.sock`, `device.sock` | **C** | coralreef-core creates `shader.sock` symlink; glowplug creates `device.sock` symlink. |
| **biomeOS** | Multiple sockets | Yes | Yes | -- | C | Orchestrator, different pattern. |

---

## Health Method Names

Standard: `health.liveness`, `health.readiness`, `health.check` are
non-negotiable canonical names. See `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2.

| Primal | `health.liveness` | `health.readiness` | `health.check` | Other Health | Status | Notes |
|--------|-------------------|-------------------|-----------------|--------------|--------|-------|
| **rhizocrypt** | Yes | Yes | Yes | `health.metrics` | C | Reachable via both raw newline TCP and UDS. Fixed in v0.14.0-dev session 23. |
| **loamspine** | Yes | ? | ? | -- | **C** | `health.liveness` confirmed via UDS (April 1). |
| **sweetgrass** | Yes | ? | ? | -- | C | Responds to `health.liveness`. |
| **squirrel** | Yes | Yes | ? | `system.health` (legacy alias) | **C** | `health.liveness` + `health.readiness` added (alpha.25b). Legacy `system.*` kept as aliases. |
| **beardog** | Yes | Yes | Yes | -- | C | Full canonical health suite: `health.liveness`, `health.readiness`, `health.check`. |
| **songbird** | Yes | ? | ? | `health` (short alias), HTTP `/health` | **C** | `health.liveness` canonical name added (wave89-90) via `json_rpc_method.rs` normalization. |
| **petaltongue** | Yes | Yes | Yes | `ping`, `health`, `status`, `check` aliases | C | Full health triad + aliases (March 31). |
| **nestgate** | ? | ? | ? | `health` (short) | **P** | `health` responds OK. Canonical `health.liveness` not verified. 25 capabilities via `discover_capabilities`. |
| **toadstool** | No | No | No | -- | **X** | S168 binary: `health.liveness` → "Method not found". 0 capabilities. Needs S169 rebuild. |
| **coralreef** | Yes | Yes | Yes | `capabilities.list` | **C** | Canonical health methods on coralreef-core, glowplug, and ember. |
| **biomeOS** | Yes | Yes | Yes | -- | C | Full health suite. |

---

## Server `--port` Support

Standard: `server --port <PORT>` binds newline-delimited TCP JSON-RPC.
See `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1.

| Primal | Subcommand | `--port` Works? | Actual Flag | Status | Notes |
|--------|-----------|-----------------|-------------|--------|-------|
| **rhizocrypt** | `server` | Yes | `--port` (tarpc), `--unix [PATH]` (UDS), JSON-RPC on calculated port | **C** | `--port` for tarpc, JSON-RPC derived (port + offset). `--unix` for UDS. |
| **loamspine** | `server` | No | `--jsonrpc-port` | **X** | No `--port` flag. Uses `--jsonrpc-port`. |
| **sweetgrass** | `server` | No | `--http-address` (addr:port) | **X** | No `--port` flag. Takes full address, not just port. |
| **squirrel** | `server` | Yes (ignored) | `--port` exists but UDS is primary | **P** | `--port` accepted but TCP not used when UDS is available. |
| **beardog** | `server` | Yes | `--port` (alias), `--listen` (addr:port) | C | `--port PORT` binds `0.0.0.0:PORT`. `--listen addr:port` for full control. Both use newline JSON-RPC. |
| **songbird** | `server` | ? | ? | ? | Not verified. |
| **petaltongue** | `server` | Yes | `--port <PORT>` | C | `server --port <N>` binds newline TCP JSON-RPC (March 31). |
| **nestgate** | `daemon` | No (ignored) | `--port` exists but socket-only | **X** | Subcommand is `daemon`, not `server`. `--port` not functional. musl binary segfaults before CLI parsing. |
| **toadstool** | `server` | No (ignored) | `--port` exists but not wired | **X** | Flag present but not forwarded to server implementation. |
| **coralreef** | `server` | Yes | `--port` (newline TCP), `--rpc-bind` (HTTP) | **C** | coralreef-core: `server --port` for newline TCP; glowplug: `--port` for newline TCP. `--rpc-bind` is separate HTTP endpoint. |
| **biomeOS** | `neural-api` / `api` | N/A | N/A | -- | Not a peer primal. |

---

## Standalone Startup

Standard: primals MUST start without `FAMILY_ID` / `NODE_ID` and without
Songbird / Neural API. See `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1.

| Primal | Starts Without Identity? | Defaults | Status | Notes |
|--------|-------------------------|----------|--------|-------|
| **rhizocrypt** | Yes | Standalone | C | |
| **loamspine** | Yes | Standalone | **C** | **LS-03 RESOLVED** (v0.9.15). Infant discovery fails gracefully, continues without. |
| **sweetgrass** | Yes | Standalone | C | |
| **squirrel** | Yes | Standalone | C | |
| **beardog** | Yes | `standalone` / `default` | C | `PrimalIdentity::from_env()` defaults `FAMILY_ID` to `standalone` and `NODE_ID` to `default` when unset. |
| **songbird** | Yes | Standalone | C | |
| **petaltongue** | Yes | Standalone | C | |
| **nestgate** | Yes | Standalone | C | |
| **toadstool** | Yes | Standalone | C | |
| **coralreef** | Yes | Standalone | C | |
| **biomeOS** | Yes | Standalone | C | |

---

## Summary Scorecard

| Primal | Wire Framing | Socket Path | Health Names | `--port` / `--listen` | Standalone | Mobile | ecoBin | Overall |
|--------|-------------|-------------|-------------|----------------------|-----------|--------|--------|---------|
| **beardog** | C | C | C | C (`--port` + `--listen`) | C (standalone) | C (TCP + abstract) | A++ | **Conformant** |
| **songbird** | C | C | C | C (`--listen`) | C | C (TCP) | A++ | **Conformant** |
| **squirrel** | P | C | C | C (`--port`) | C | C (abstract+filesystem+HTTP) | A++ | **Close** |
| **toadstool** | P | P | X (S168) | X (not wired) | C | P (caps only) | A++ | Needs S169 rebuild |
| **nestgate** | X | P | ? | X (not wired) | C | X (no aarch64) | A++ (x86) | Needs work |
| **biomeos** | P | C | C | C (`--tcp-only`) | C | P (TCP mode new) | A++ | **Near-complete** |
| **petaltongue** | C | C | C | C (`--port`) | C | X (no aarch64) | A++ (x86) | Near-complete |
| **sweetgrass** | P | P | C | X | C | ? | ? | Close |
| **rhizocrypt** | C | C | C | C | C | ? | C | Conformant |
| **loamspine** | C | C | C | X (`--jsonrpc-port`) | C | ? | ? | **Close** |
| **coralreef** | C | C | C | C | C | ? | ? | **Conformant** |
| **sourdough** | -- | -- | -- | -- | -- | -- | -- | CLI tool — no IPC daemon |
| **skunkbat** | ? | ? | ? | ? | ? | ? | ? | Needs audit |

---

## Capability-Based Discovery Compliance (April 3, 2026 — primalSpring full audit)

Standard: Primals discover and invoke each other by **capability domain**, not
by name. No primal-specific env vars, socket names, or method namespaces in
production routing code. See `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2.

| Primal | Foreign Names (files/refs) | Primal-Specific Env Vars (files/refs) | Status | Trend | Notes |
|--------|---------------------------|---------------------------------------|--------|-------|-------|
| **beardog** | 0 | 0 | **C** | — | Self-refs only. |
| **biomeos** | 0 non-test | 0 non-test | **C** | — | RESOLVED (v2.87). |
| **rhizocrypt** | 0 | 0 | **C** | — | |
| **loamspine** | 0 | 0 | **C** | — | |
| **sweetgrass** | 0 | 0 | **C** | — | |
| **nestgate** | 7 files (config/discovery) | 0 (was `NESTGATE_BEARDOG_URL` etc.) | **P→C** | ↑ | a75e9f2a: major modularization, primal env vars eliminated. 7 config/discovery files remain. |
| **petaltongue** | ~20 files | 24 refs / 10 files | **P** | — | Wave 97 removed `SongbirdClient`. IPC/core/UI layers still have `TOADSTOOL_`/`BARRACUDA_`/`SONGBIRD_` env refs. |
| **toadstool** | ~30 files | `SONGBIRD_*`, `BEARDOG_SOCKET` in fallbacks | **P** | ↑ | S172-5 targeted discovery. Compliance claim overstated — fallback/compat paths still hardcode. |
| **squirrel** | 78 files / ~230 non-test refs | 0 primary; `SONGBIRD_*` as `.or_else()` fallbacks only | **P** | ↑ | Build FIXED (alpha.32). All actionable coupling migrated: `register_orchestration_service`, `delegate_to_http_proxy`, `metric_names::orchestration`, `ServiceMeshIntegration`, `ConfigBuilder::orchestration()`. Remaining refs: `primal_names` (logging), deprecated aliases, serde aliases, env fallbacks, doc history. |
| **songbird** | 230 files / 1472 refs | 63 files / 291 refs (capability-first + fallback) | **P** | ↑↑ | Wave 102: `beardog_*`→`security_*`, `squirrel_*`→`coordination_*`, `nestgate`→`storage_provider`, `toadstool`→`compute_provider`. 42% ref reduction. fmt PASS. |
| **sourdough** | 1 string (cosmetic) | 0 | **C** | — | CLI scaffolding tool. 1 "BearDog" string in genomebin.rs (non-routing). |
| **coralreef** | ? | ? | ? | — | Not audited. |

### Discovery Compliance Priority (updated April 3 — primalSpring audit)

1. ~~**biomeOS**~~ — **RESOLVED** (v2.87).
2. **Songbird** — **1472 refs in 230 files** (was 2558/321 — 42% reduction in wave 102). Key renames: `beardog_*`→`security_*`, `squirrel_*`→`coordination_*`, `nestgate`→`storage_provider`, `toadstool`→`compute_provider`. fmt PASS. Still highest debt but trajectory is strong. Remaining: 805 beardog refs (171 files), 130 toadstool (47), 96 squirrel (39), 53 nestgate (20).
3. ~~**Squirrel** — 322 refs in 96 files. Build broken.~~ **BUILD FIXED** (alpha.32). All actionable coupling migrated. ~230 non-test refs remain (logging, aliases, fallbacks, docs — all acceptable).
4. **toadStool** — S173 deep debt execution: 8 large files smart-refactored, DMA unsafe consolidated into hw-safe (101→89 blocks), hardcoded literals eliminated, deployment stubs→capability socket verification, +79 tests. S172-5/6 addressed naming; S173 addressed structural debt. Status: **P→C** (capability-first discovery in all paths; legacy env vars retained as Tier 2+ fallbacks only).
5. **petalTongue** — 24 env refs in IPC/core/UI. Focused sprint could clear this.
6. **NestGate** — **Near-compliant.** 7 files in config/discovery, zero primal env vars. Best improvement this cycle.

---

## Priority Actions

### Critical (blocks inter-primal composition)

1. **squirrel**: Add filesystem socket in `$XDG_RUNTIME_DIR/biomeos/squirrel.sock` alongside abstract socket. Add `health.liveness` / `health.readiness` / `health.check` method handlers.
2. ~~**beardog**: Accept `--port` (alias for `--listen`, port-only). Default `FAMILY_ID` to `standalone` when unset.~~ **RESOLVED** (Wave 25+29: `--port` implemented, standalone defaults in `PrimalIdentity::from_env()`).
3. ~~**loamspine**: Fix Tokio nested runtime panic in `infant_discovery`.~~ **RESOLVED** (v0.9.15: infant discovery fails gracefully). Remaining: Add `--port` flag (alias for `--jsonrpc-port`).
4. ~~**rhizocrypt**: Add newline-delimited TCP JSON-RPC listener (alongside HTTP Axum server).~~ **RESOLVED** — v0.14.0-dev session 23 (March 31, 2026).

### High (needed for standard compliance)

5. ~~**petaltongue**: Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`. Add `--port` flag.~~ **RESOLVED March 31** — socket at `biomeos/petaltongue.sock`, `server --port` wired, full health triad.
6. **sweetgrass**: Add `--port` flag (alias for port portion of `--http-address`).
7. ~~**coralreef**: Add `--port` flag for raw newline TCP (alongside jsonrpsee HTTP).~~ **RESOLVED** — Iter 70h (March 31, 2026). coralreef-core `server --port` and glowplug `--port` both bind newline TCP. Domain symlinks `shader.sock` + `device.sock` installed.
8. **toadstool**: Wire `--port` flag to actual server bind.
9. **nestgate**: Wire `--port` to actual TCP bind. Accept `server` as alias for `daemon`.

### Recommended (improves ecosystem coherence)

10. All primals with conformant sockets: create capability-domain symlinks.
11. All primals: verify and add `health.liveness` / `health.readiness` / `health.check`.
12. All primals: audit `capabilities.list` canonical name (see `SEMANTIC_METHOD_NAMING_STANDARD.md`).

---

## Health Check Transport Protocol

Standard: Primals should expose health over a consistent protocol. Currently
three different protocols are in use, forcing multi-protocol probing in
validation scripts. Verified via live cross-hardware testing (March 27, 2026).

| Primal | Primary Health Protocol | Endpoint | Status | Notes |
|--------|------------------------|----------|--------|-------|
| **beardog** | Raw TCP JSON-RPC | `health.liveness` via newline JSON-RPC | C | Clean, standards-compliant |
| **songbird** | HTTP GET | `/health` (HTTP 200) | **P** | Works, but not JSON-RPC. Short name `health` via RPC. |
| **squirrel** | UDS JSON-RPC | `health.liveness` via UDS | **C** | Canonical names (alpha.25b). Filesystem socket via `UniversalListener`. |
| **toadstool** | HTTP GET | `/health` (HTTP 200) | **P** | Not verified via JSON-RPC method name |
| **nestgate** | UDS JSON-RPC | `health` (short), 25 capabilities via `discover_capabilities` | **P** | Socket at `biomeos/nestgate.sock`. `storage.list` works. |
| **rhizocrypt** | Dual-mode TCP (newline + HTTP) + UDS | `health.liveness`, `health.readiness`, `health.check` | C | Dual-mode auto-detection. Fixed in v0.14.0-dev session 23. |
| **loamspine** | UDS JSON-RPC | `health.liveness` | **C** | **LS-03 RESOLVED** (v0.9.15). 19 capabilities. |
| **sweetgrass** | UDS JSON-RPC | `health.liveness` | C | |
| **petaltongue** | UDS JSON-RPC (+ optional TCP) | `health.liveness`, `health.readiness`, `health.check` | C | Full health triad + aliases (March 31). |
| **coralreef** | Newline TCP + HTTP (jsonrpsee) + UDS | `health.liveness`, `health.readiness`, `health.check` | **C** | All three canonical methods on all components. `--port` for newline TCP, `--rpc-bind` for HTTP. |
| **biomeOS** | HTTP | `/health`, `health.liveness` | C | Full health suite |

**Recommendation**: All primals should expose `health.liveness` via raw TCP
newline-delimited JSON-RPC (primary) and optionally HTTP `/health` (convenience).
Validation tools (`validate_gate.sh`) currently brute-force three protocols; this
wastes round-trips and makes diagnostics ambiguous.

---

## Capability Registration Compliance

Standard: Primals register capabilities at startup via biomeOS Neural API
(`capability.register`) or are discovered by biomeOS's `discover_and_register_primals()`.
See `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1.

**CRITICAL GAP (BM-04)**: biomeOS `discover_and_register_primals()` runs ONCE
at startup with a 500ms timeout. Primals starting after biomeOS (typical in
graph deployments) miss this window. `capability.list` only returns 5 biomeOS
self-capabilities, omitting all external primal capabilities.

| Primal | Self-Registers? | Discovered by biomeOS? | Visible in `capability.list`? | Status | Notes |
|--------|----------------|----------------------|------------------------------|--------|-------|
| **beardog** | No | Race condition | **No** (starts after biomeOS) | **X** | Needs biomeOS rescan or self-registration |
| **songbird** | No | Race condition | **No** (starts after biomeOS) | **X** | Same timing issue |
| **squirrel** | No | Discoverable (filesystem) | **Pending rescan** | **P** | `UniversalListener` now creates filesystem socket (alpha.25b). Needs biomeOS rescan to register. |
| **petaltongue** | No | Discoverable | **Pending rescan** | **P** | Socket now at `biomeos/petaltongue.sock`. Needs biomeOS rescan to register. |
| **nestgate** | No | Race condition | Intermittent | **P** | Sometimes starts fast enough to be caught |
| **toadstool** | No | Race condition | Intermittent | **P** | Same timing issue |
| **sweetgrass** | No | Race condition | Intermittent | **P** | Same timing issue |
| **rhizocrypt** | No | Discoverable (UDS) | **Pending rescan** | **P** | **RC-01 RESOLVED** (v0.14.0-dev s23). Socket at `biomeos/rhizocrypt.sock` with `--unix`. Needs biomeOS rescan to register. |
| **loamspine** | No | Discoverable (UDS) | **Pending rescan** | **P** | **LS-03 RESOLVED** (v0.9.15). Socket at `biomeos/loamspine.sock`. Needs biomeOS rescan to register. |
| **coralreef** | No | Race condition | Intermittent | **P** | Same timing issue |
| **barraCuda** | No | Race condition | Intermittent | **P** | Same timing issue |
| **biomeOS** | Self | N/A | **Yes** (all via rescan) | **C** | v2.81: `topology.rescan` + lazy discovery on miss. All primal capabilities now discoverable. |

**Fix options** (any one would resolve BM-04):
1. `topology.rescan` JSON-RPC method — trigger a re-scan of the socket directory on demand
2. Lazy discovery on `capability.call` miss — if a `capability.call` targets an unregistered method, scan and retry
3. Primal self-registration — primals call `capability.register` on startup (requires SDK change)

**Impact**: Resolving BM-04 unblocks 3 composition checks and enables reliable
multi-primal capability routing for all 7 decomposed compositions.

---

## Substrate Compliance (Cross-Hardware)

Standard: ecoBin v3.0 requires pure Rust, musl-static cross-compilation, and
platform-agnostic IPC. Live testing (March 27, 2026) on x86_64 Linux and
aarch64 Android/GrapheneOS revealed substrate-specific compliance gaps.

### musl-static Binary Health

| Primal | x86_64 musl | aarch64 musl | Notes |
|--------|-------------|-------------|-------|
| **beardog** | C | C | Works on both. `--listen` TCP + `--abstract` sockets. Crypto deterministic cross-arch. |
| **songbird** | C | C | Works on both. `--listen` TCP confirmed functional on Pixel. 14 capabilities match cross-arch. |
| **squirrel** | C | C | Works on both. Abstract socket `@squirrel` confirmed functional on GrapheneOS. HTTP `--port` works. |
| **toadstool** | C | C | Works on both. Executes on Pixel but server mode needs `biome.yaml`. |
| **nestgate** | C | ? | **Fixed March 28** — musl-static binary now works on x86_64 (was segfaulting). aarch64 musl build not yet available. Team evolving cross-compile. |
| **biomeos** | C | C | **New March 28** — both arches in plasmidBin. aarch64 binary runs on Pixel but `api` mode still forces Unix socket (TCP gap). |
| **petaltongue** | C | ? | x86_64 musl stripped and functional. aarch64 not yet built (egui headless cross-compile pending). |
| **loamspine** | C | ? | **LS-03 RESOLVED** (v0.9.15). Starts cleanly. Source-built binary verified. |
| **rhizocrypt** | CI (cross-compile job) | CI (cross-compile job) | musl cross-compile CI for x86_64 + aarch64. |
| **sweetgrass** | ? | ? | Not tested. |
| **coralreef** | ? | ? | Not tested. |

### Android/GrapheneOS Substrate

Tested on Pixel 8a with GrapheneOS via ADB (aarch64-linux-musl binaries).
**Updated March 28** with comprehensive findings from NUCLEUS + cross-gate deployment.

| Requirement | Standard | Status | Notes |
|-------------|----------|--------|-------|
| **TCP listener** | `--listen 0.0.0.0:PORT` | C (BearDog, Songbird) | TCP is the **universal mobile transport**. Every primal MUST support it. |
| **Abstract sockets** | `--abstract` flag | C (Squirrel C, BearDog C) | Squirrel's `@squirrel` works on GrapheneOS. BearDog abstract logging fixed (Wave 30). |
| **Filesystem UDS** | Default socket path | **X (all)** | SELinux on GrapheneOS denies `sock_file create` from `shell` context. Filesystem UDS is NOT viable on Android. |
| **Writable runtime dir** | `HOME`/`TMPDIR` writable | C | `cd /data/local/tmp/biomeos` before launch. Set `HOME`/`TMPDIR` env vars. |
| **No systemd** | No systemd assumptions | C | Startup via shell script (`deploy_pixel.sh`). |
| **Audit/PID files** | Directory configurable | C | BearDog `--audit-dir` / `BEARDOG_AUDIT_DIR` (Wave 26). Falls back to `$TMPDIR/beardog` when unset. |
| **SELinux** | Platform-aware IPC | Critical | `adb logcat` confirmed `avc: denied { create } ... tcontext=u:object_r:shell_data_file:s0 tclass=sock_file`. TCP and abstract sockets bypass this. |
| **ADB port forwarding** | Cross-gate access | C | `deploy_pixel.sh --local-port-offset N` for conflict avoidance. |
| **biomeOS orchestration** | `biomeos api --port` on mobile | **X** | biomeOS forces Unix socket even when `--port` specified. Needs TCP-only mode for mobile. |

### Per-Primal Mobile Transport Status (March 28, 2026)

| Primal | TCP | Abstract Socket | Filesystem UDS | Mobile Ready? |
|--------|-----|-----------------|----------------|---------------|
| **beardog** | C (`--port` / `--listen`) | C (`--abstract`, fixed logging) | X (SELinux) | Yes (TCP + abstract) |
| **songbird** | C (`--listen`) | ? | X (SELinux) | Yes (via TCP) |
| **squirrel** | C (`--port`) | C (`@squirrel`) | X (SELinux) | Yes (both) |
| **toadstool** | X (not wired) | ? | X (SELinux) | Partial (caps only) |
| **nestgate** | X (not wired) | ? | X (SELinux) | No (needs aarch64 build + TCP) |
| **biomeos** | X (forces UDS) | ? | X (SELinux) | No (needs TCP mode) |
| **petaltongue** | C (`--port`) | ? | X (SELinux) | Partial (x86_64 TCP ready, aarch64 pending) |

### Genetic Crypto Cross-Architecture Determinism

Verified March 27, 2026 — BearDog crypto primitives produce identical results
on x86_64 and aarch64:

| Primitive | Cross-Arch Deterministic | Notes |
|-----------|-------------------------|-------|
| BLAKE3 hash | Yes | Same input produces same hash on both architectures |
| HMAC-SHA256 | Yes | Keyed MAC deterministic |
| X25519 key exchange | Yes | Key pairs and shared secrets match |
| ChaCha20-Poly1305 | Yes (expected) | Not yet tested cross-gate; same algorithm, deterministic |

---

## Priority Actions (Updated March 28, 2026)

### Critical (blocks cross-hardware deployment)

1. **biomeos**: Implement TCP-only API mode (`biomeos api --port PORT --tcp-only`). Currently forces Unix socket even when `--port` specified. Blocks mobile orchestration.
2. **biomeos**: Honor `gate` parameter in `capability.call` for cross-gate routing. Currently always routes to local primary endpoint.
3. **nestgate**: Build aarch64-unknown-linux-musl binary. Wire `--port` to actual TCP bind. Accept `server` as alias for `daemon`.
4. ~~**beardog**: Default `FAMILY_ID` to `standalone` when unset.~~ **RESOLVED** (Wave 25: `PrimalIdentity::from_env()` defaults).
5. ~~**beardog**: Fix `--abstract` socket logging.~~ **RESOLVED** (Wave 30: logs `abstract_name` with `"bound to abstract namespace"` message).
6. ~~**loamspine**: Fix Tokio nested runtime panic in `infant_discovery`.~~ **RESOLVED** (v0.9.15). Add `--port` flag.
7. ~~**rhizocrypt**: Add newline-delimited TCP JSON-RPC listener.~~ **RESOLVED** — v0.14.0-dev session 23 (March 31, 2026).

### High (needed for standard compliance and mobile deployment)

8. ~~**beardog**: Add `--audit-dir` / `BEARDOG_AUDIT_DIR` to avoid CWD writes.~~ **RESOLVED** (Wave 26: `--audit-dir` CLI flag + `BEARDOG_AUDIT_DIR` env var, falls back to `$TMPDIR/beardog`).
9. ~~**beardog**: Wire `birdsong.generate_encrypted_beacon` into server RPC handler.~~ **RESOLVED** (Wave 26: `SecurityHandler` exposes `birdsong.generate_encrypted_beacon` JSON-RPC method).
10. **songbird**: Add `--dark-forest` CLI flag (env-only today, silent plaintext fallback).
11. **songbird**: Add `--pid-dir` or `SONGBIRD_PID_DIR` for Android/container substrates.
12. **toadstool**: Wire `--port` flag to actual server bind. Critical for mobile compute sharing.
13. ~~**petaltongue**: Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`. Add `--port`.~~ **RESOLVED March 31.** Build aarch64 headless still pending.
14. **sweetgrass**: Add `--port` flag (alias for port portion of `--http-address`).
15. ~~**coralreef**: Add `--port` flag for raw newline TCP.~~ **RESOLVED** — Iter 70h (March 31, 2026).

### Recommended (improves ecosystem coherence)

16. All primals: converge on `--listen addr:port` as the canonical TCP bind flag (BearDog/Songbird pattern).
17. All primals: expose `health.liveness` via raw TCP newline JSON-RPC.
18. All primals: report transport protocol in `capabilities.list` response.
19. **squirrel**: Add filesystem socket alongside abstract. Alias `system.*` to `health.*`.
20. All primals: ensure `cargo build --release --target x86_64-unknown-linux-musl` produces ecoBin (static, stripped) and submit to plasmidBin via `harvest.sh`.

---

## Related Standards

- `PRIMAL_IPC_PROTOCOL.md` v3.1 — Wire framing, socket paths, standalone startup
- `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1 — `--port` convention, standalone startup
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1 — Socket naming, symlinks, filesystem requirement
- `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2 — Health method names, capability enumeration
- `SPRING_INTEROP_LESSONS.md` — Practical learnings from Webb's composition
- `GATE_DEPLOYMENT_STANDARD.md` — Gate hardware, substrate, and deployment requirements
- `ECOBIN_ARCHITECTURE_STANDARD.md` v3.0 — Pure Rust, musl-static, cross-compilation
- `CROSS_DEPLOY_SUBSTRATE_EVOLUTION_HANDOFF_MAR27_2026.md` — Per-primal deployment action items

---

## Version History

### v1.6.0 (April 3, 2026)

**Phase 23o: Responsibility Matrix Restructure + sourDough Integration**

- Added sourDough to scorecard and discovery compliance tables (CLI tool — no IPC daemon, discovery **C**)
- Cross-reference to `PRIMAL_RESPONSIBILITY_MATRIX.md` v3.0 (restructured with Primal Directory, Interaction Rules, Capability Routing Guide)
- Updated `CAPABILITY_BASED_DISCOVERY_STANDARD.md` reference to v1.2

### v1.4.3 (April 3, 2026)

**toadStool S173 Deep Debt Execution**

- toadStool discovery compliance: **P → C** — S173 completed structural debt beyond S172-5/6 naming
- 8 production files >650 LOC smart-refactored into cohesive submodules
- Unsafe consolidated: akida-driver/nvpmu DMA → hw-safe LockedMemory + vfio_dma (101→89 blocks)
- Hardcoded literals eliminated: `"0.0.0.0"` → constant, `"/dev/dri/card0"` → constant, `"coralreef"` scan → capability-first `"shader"` scan
- Deployment no-ops → capability socket verification (`$XDG_RUNTIME_DIR/biomeos/{capability}.sock`)
- +79 tests across 5 modules; `config` 0.14→0.15 (eliminated base64 duplication)
- All quality gates green: clippy, fmt, doc, tests

### v1.4.2 (April 3, 2026)

**Squirrel Build Fix & Capability-Domain Decoupling Wave 2**

- Squirrel build FIXED (alpha.32): `MockAIClient` cfg gate resolved, E0282 inference error fixed
- Squirrel discovery compliance: **X → P** — all actionable coupling migrated to capability-domain
  - `register_songbird_service` → `register_orchestration_service`
  - `delegate_to_songbird` → `delegate_to_http_proxy`
  - `metric_names::songbird` → `metric_names::orchestration`
  - `SongbirdIntegration` → `ServiceMeshIntegration`
  - `ConfigBuilder::songbird()` → `ConfigBuilder::orchestration()`
- Remaining ~230 non-test refs are all acceptable (logging, deprecated aliases, serde compat, env fallbacks, docs)
- Discovery compliance priority #3 (Squirrel) marked RESOLVED

### v1.4.1 (April 2, 2026)

**toadStool Capability-Based Discovery Compliance — S172-5/6**

- toadStool discovery compliance: **X → C** — all ~105 foreign primal references evolved
- S172-5: struct fields, DNS defaults, socket names renamed to capability-domain with `#[serde(alias)]` backward compat
- S172-6: all `env::var()` chains evolved to capability-domain-first ordering
- Legacy primal-named env vars retained as Tier 2+ fallbacks only, never primary lookup

### v1.3.2 (April 1, 2026)

**Deep Per-Primal Validation — LS-03 RESOLVED, 11 Gaps Total Resolved**

- loamSpine LS-03 RESOLVED (v0.9.15): infant discovery now fails gracefully, UDS at `biomeos/loamspine.sock`, `health.liveness` ✅, 19 capabilities
- loamSpine scorecard: Blocked → Close (wire C, socket C, health C, standalone C, only `--port` alias missing)
- toadStool socket verified: creates `biomeos/toadstool.sock` + `.jsonrpc.sock` but S168 binary returns "Method not found" for all methods, 0 capabilities
- NestGate health verified: `health` responds OK, 25 capabilities via `discover_capabilities`, `storage.list` works with `family_id` param
- bearDog: `capabilities.list` returns empty (0 methods) — needs audit; `crypto.hash` requires base64 input
- petalTongue: `capabilities.list` returns empty (0 methods) — older binary; `identity.get`/`lifecycle.status` not found
- biomeOS: `topology.rescan` → "Method not found" (running v2.80 binary, not v2.81); but `capability.discover` routes correctly to all primals (crypto→bearDog, storage→nestGate, viz→petalTongue, ai→Squirrel, game→ludoSpring)
- Squirrel: `ai_router: false` in readiness, 0 providers, socket at `/squirrel/squirrel.sock` not `biomeos/`
- rhizoCrypt RC-01 confirmed: dual-mode TCP works (raw newline + HTTP), 4 domains/26 methods, but still NO UDS socket
- Updated capability registration: loamSpine X → P (discoverable after LS-03 fix)
- 1 critical blocker remains: RC-01 (rhizoCrypt UDS)

### v1.3.1 (March 31, 2026)

**Post Full-Ecosystem Pull — 10 Gaps Resolved**

- biomeOS v2.81: BM-04 RESOLVED (topology.rescan + lazy discovery on miss), BM-05 RESOLVED (multi-shape probe), TCP-only CLI (`--tcp-only`), cross-gate capability.call routing, 7,212 tests
- squirrel alpha.25b: SQ-01 RESOLVED (filesystem socket via UniversalListener), health.liveness/readiness canonical names
- songbird wave89-90: health.liveness canonical name added via json_rpc_method.rs normalization, QUIC crypto delegation to BearDog
- barraCuda Sprint 25 / v0.3.11: BC-01/02/03 RESOLVED (Fitts/Hick variant params, Perlin3D lattice fix)
- Updated summary scorecard: beardog + songbird Conformant, squirrel Close, biomeOS Near-complete
- Updated capability registration table: biomeOS C, squirrel P, petalTongue P
- Projected validation: 67.4% → 83.7% current, 95.0% with RC-01 + LS-03
- 2 critical blockers remain: rhizoCrypt RC-01 (TCP-only) and loamSpine LS-03 (startup panic)

### v1.3.0 (March 31, 2026)

**petaltongue IPC Compliance Refresh + coralReef IPC Compliance + Composition Decomposition + ludoSpring V37.1 Gap Alignment**

- petaltongue socket path: X → C (`$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`)
- petaltongue wire framing: P → C (newline TCP via `server --port`)
- petaltongue health methods: ? → C (full `health.liveness` / `health.readiness` / `health.check` + aliases)
- petaltongue `--port`: X → C (`server --port <N>` binds newline TCP JSON-RPC)
- petaltongue health transport: ? → C (UDS + optional TCP)
- petaltongue mobile transport: X → C for TCP (`--port`); aarch64 build still pending
- petaltongue `capabilities.list`: expanded to 41 methods matching full RPC dispatch surface
- Marked petaltongue priority action items 5 and 13 as RESOLVED
- coralReef Wire Framing: P → C — `--port` binds raw newline TCP on coralreef-core and glowplug
- coralReef Socket Path: P → C — `shader.sock` + `device.sock` domain symlinks installed
- coralReef Health Methods: ? → C — all three canonical methods on all components
- coralReef `--port` Support: X → C — coralreef-core `server --port` and glowplug `--port`
- coralReef Summary Scorecard: Conformant (was Needs work)
- coralReef Health Transport: newline TCP + HTTP + UDS, all canonical methods
- Resolved priority actions #7 and #15 (coralReef `--port`)
- Updated summary scorecard and per-primal mobile transport table
- Added Capability Registration Compliance section (BM-04: biomeOS discovery timing)
- Added all 12 primals to capability registration table
- Documented 3 fix options for biomeOS capability discovery
- Integrated primalSpring Phase 23f findings (32 gaps across 7 compositions)
- Integrated ludoSpring V37.1 live plasmidBin gap matrix (95/141 = 67.4%)
- Cross-references PRIMAL_RESPONSIBILITY_MATRIX.md V2 tiered evolution actions
- Updated data source header with primalSpring and ludoSpring validation rounds
### v1.2.0 (March 28, 2026)

**Cross-Gate Federation + plasmidBin Overhaul**

- Updated NestGate x86_64 musl status: FIXED (was segfaulting, now ecoBin A++)
- Added biomeOS to musl-static binary health table (both arches)
- Added petaltongue x86_64 musl status (functional, stripped)
- Added Per-Primal Mobile Transport Status table
- Updated Android/GrapheneOS substrate section with comprehensive findings
- Confirmed Squirrel abstract socket (`@squirrel`) works on GrapheneOS
- Identified biomeOS TCP-only mode as critical gap for mobile orchestration
- Identified biomeOS `capability.call` gate routing as critical for federation
- Updated all priority actions to reflect March 28 state
- plasmidBin now contains 7 x86_64 + 5 aarch64 ecoBin-compliant binaries

### v1.1.0 (March 27, 2026)

**Cross-Hardware Deployment Testing**

- Added Health Check Transport Protocol section
- Added Substrate Compliance section (musl-static, Android/GrapheneOS)
- Added Genetic Crypto Cross-Architecture Determinism table
- Updated NestGate status: musl binary segfaults (X, was P)
- Updated Songbird health method from live probing
- Expanded priority actions with deployment-specific items (19 total)
- Data now includes live testing on x86_64 + aarch64 Pixel/GrapheneOS

### v1.0.0 (March 25, 2026)

**Initial Matrix from esotericWebb Composition**

- Wire framing, socket path, health method, `--port`, standalone compliance
- Summary scorecard and priority actions
