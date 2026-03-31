# IPC Compliance Matrix

**Version:** 1.3.0
**Date:** March 31, 2026
**Status:** Living document — updated as primals evolve
**Authority:** wateringHole (ecoPrimals Core Standards)

This matrix tracks each primal's alignment across the IPC interoperability
dimensions defined in `PRIMAL_IPC_PROTOCOL.md` v3.1, `UNIBIN_ARCHITECTURE_STANDARD.md`
v1.1, `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1, and
`SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2.

Data sourced from esotericWebb's first live multi-primal composition
(March 2026), direct inspection of each primal's source code,
**live cross-hardware deployment testing** (March 27, 2026) across
x86_64 eastgate + aarch64 Pixel/GrapheneOS on iPhone hotspot,
**primalSpring Phase 23f** composition decomposition (7 subsystems,
89 deploy graphs, 32 gaps), and **ludoSpring V37.1** plasmidBin live
gap matrix (95/141 checks, experiments 084-098).

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
| **loamspine** | Newline | Newline | C | Accepts both raw newline and HTTP POST on JSON-RPC port. |
| **sweetgrass** | Newline | HTTP POST (Axum) | **P** | UDS is newline-conformant. TCP is HTTP-only. Sufficient for UDS composition. |
| **squirrel** | Newline (abstract) | -- | **P** | Newline framing correct, but socket is abstract-namespace only (see Discovery). No TCP listener. |
| **beardog** | Newline | Newline | C | Both transports use raw newline framing. |
| **songbird** | Newline | Newline | C | Standard newline framing on both transports. |
| **petaltongue** | Newline | Newline | C | UDS newline-conformant. TCP via `server --port <N>` (March 31). |
| **nestgate** | Newline | -- | **X** | Socket-only by default. `--port` exists but is non-functional. **musl-static binary segfaults (exit 139) on `--help`** — ecoBin non-compliant. glibc dynamic build works. |
| **toadstool** | Newline | -- | **P** | `--port` exists but is not forwarded to implementation. |
| **coralreef** | Newline | HTTP (jsonrpsee) | **P** | UDS is newline. TCP uses jsonrpsee HTTP framing. |
| **biomeOS** | -- | HTTP (multiple modes) | **P** | Not a simple `server --port` primal. Orchestrator, not peer. |

---

## Socket Path Conformance

Standard: filesystem socket at `$XDG_RUNTIME_DIR/biomeos/<primal>.sock`.
See `PRIMAL_IPC_PROTOCOL.md` Socket Path Convention and
`CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1.

| Primal | Socket Path | Filesystem? | In biomeos/? | Domain Symlink | Status | Notes |
|--------|-------------|-------------|-------------|----------------|--------|-------|
| **rhizocrypt** | `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock` | Yes | Yes | -- | **C** | `--unix [PATH]` flag; default ecosystem standard path. Fixed in v0.14.0-dev session 23. |
| **loamspine** | Not reached (crash) | ? | ? | -- | **X** | Crashes before socket bind (Tokio nested runtime). |
| **sweetgrass** | `/run/user/1000/biomeos/sweetgrass.sock` | Yes | Yes | No | **P** | Conformant path, no family suffix. Missing domain symlink. |
| **squirrel** | `@squirrel` (abstract) | **No** | No | No | **X** | Abstract namespace only. Invisible to `readdir()`. Not discoverable. |
| **beardog** | `/run/user/1000/biomeos/beardog.sock` | Yes | Yes | `crypto.sock` | C | Conformant path. Domain symlink `crypto.sock` → `beardog.sock` created at bind, cleaned on shutdown. |
| **songbird** | `/run/user/1000/biomeos/songbird.sock` | Yes | Yes | No | C | Registry primal, domain symlink not required. |
| **petaltongue** | `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock` | Yes | Yes | No | C | Conformant `biomeos/` path (March 31). |
| **nestgate** | `/run/user/1000/biomeos/nestgate.sock` | Yes | Yes | No | **P** | Conformant path. Missing domain symlink. |
| **toadstool** | ? | ? | ? | -- | ? | Not verified. |
| **coralreef** | `/run/user/1000/biomeos/coralreef.sock` + custom UDS | Yes | Yes | No | **P** | Conformant for primary. Missing domain symlink. |
| **biomeOS** | Multiple sockets | Yes | Yes | -- | C | Orchestrator, different pattern. |

---

## Health Method Names

Standard: `health.liveness`, `health.readiness`, `health.check` are
non-negotiable canonical names. See `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2.

| Primal | `health.liveness` | `health.readiness` | `health.check` | Other Health | Status | Notes |
|--------|-------------------|-------------------|-----------------|--------------|--------|-------|
| **rhizocrypt** | Yes | Yes | Yes | `health.metrics` | C | Reachable via both raw newline TCP and UDS. Fixed in v0.14.0-dev session 23. |
| **loamspine** | ? | ? | ? | ? | ? | Crashes on startup. |
| **sweetgrass** | Yes | ? | ? | -- | C | Responds to `health.liveness`. |
| **squirrel** | **No** | **No** | **No** | `system.health`, `system.status`, `system.ping` | **X** | Uses `system.*` domain exclusively. Non-conformant. |
| **beardog** | Yes | Yes | Yes | -- | C | Full canonical health suite: `health.liveness`, `health.readiness`, `health.check`. |
| **songbird** | `health` alias | -- | -- | `health` (short), HTTP `/health` | **P** | Responds to `health` (short name) and HTTP `/health`. Does not expose `health.liveness` by canonical name. Verified live (March 27). |
| **petaltongue** | Yes | Yes | Yes | `ping`, `health`, `status`, `check` aliases | C | Full health triad + aliases (March 31). |
| **nestgate** | ? | ? | ? | ? | ? | Not verified. |
| **toadstool** | ? | ? | ? | ? | ? | Not verified. |
| **coralreef** | ? | ? | ? | ? | ? | Not verified. |
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
| **coralreef** | `server` | No | `--rpc-bind` | **X** | Uses `--rpc-bind` for jsonrpsee HTTP, not raw newline. |
| **biomeOS** | `neural-api` / `api` | N/A | N/A | -- | Not a peer primal. |

---

## Standalone Startup

Standard: primals MUST start without `FAMILY_ID` / `NODE_ID` and without
Songbird / Neural API. See `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1.

| Primal | Starts Without Identity? | Defaults | Status | Notes |
|--------|-------------------------|----------|--------|-------|
| **rhizocrypt** | Yes | Standalone | C | |
| **loamspine** | No (crash) | N/A | **X** | Tokio nested runtime panic in `infant_discovery`. |
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
| **songbird** | C | C | P | C (`--listen`) | C | C (TCP) | A++ | Close |
| **squirrel** | P | X | X | C (`--port`) | C | C (abstract+HTTP) | A++ | Close |
| **toadstool** | P | ? | ? | X (not wired) | C | P (caps only) | A++ | Needs work |
| **nestgate** | X | P | ? | X (not wired) | C | X (no aarch64) | A++ (x86) | Needs work |
| **biomeos** | P | C | C | X (forces UDS) | C | X (UDS only) | A++ | Needs TCP mode |
| **petaltongue** | C | C | C | C (`--port`) | C | X (no aarch64) | A++ (x86) | Near-complete |
| **sweetgrass** | P | P | C | X | C | ? | ? | Close |
| **rhizocrypt** | C | C | C | C | C | ? | C | Conformant |
| **loamspine** | C | X | ? | X | X (crash) | ? | ? | Blocked |
| **coralreef** | P | P | ? | X | C | ? | ? | Needs work |
| **skunkbat** | ? | ? | ? | ? | ? | ? | ? | Needs audit |

---

## Priority Actions

### Critical (blocks inter-primal composition)

1. **squirrel**: Add filesystem socket in `$XDG_RUNTIME_DIR/biomeos/squirrel.sock` alongside abstract socket. Add `health.liveness` / `health.readiness` / `health.check` method handlers.
2. ~~**beardog**: Accept `--port` (alias for `--listen`, port-only). Default `FAMILY_ID` to `standalone` when unset.~~ **RESOLVED** (Wave 25+29: `--port` implemented, standalone defaults in `PrimalIdentity::from_env()`).
3. **loamspine**: Fix Tokio nested runtime panic in `infant_discovery`. Add `--port` flag (alias for `--jsonrpc-port`).
4. ~~**rhizocrypt**: Add newline-delimited TCP JSON-RPC listener (alongside HTTP Axum server).~~ **RESOLVED** — v0.14.0-dev session 23 (March 31, 2026).

### High (needed for standard compliance)

5. ~~**petaltongue**: Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`. Add `--port` flag.~~ **RESOLVED March 31** — socket at `biomeos/petaltongue.sock`, `server --port` wired, full health triad.
6. **sweetgrass**: Add `--port` flag (alias for port portion of `--http-address`).
7. **coralreef**: Add `--port` flag for raw newline TCP (alongside jsonrpsee HTTP).
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
| **squirrel** | HTTP JSON-RPC POST | `system.health` via HTTP POST | **X** | Non-standard method name, HTTP-only |
| **toadstool** | HTTP GET | `/health` (HTTP 200) | **P** | Not verified via JSON-RPC method name |
| **nestgate** | Raw TCP JSON-RPC | Not verifiable | **X** | musl binary segfaults; glibc binary uses raw TCP |
| **rhizocrypt** | Dual-mode TCP (newline + HTTP) + UDS | `health.liveness`, `health.readiness`, `health.check` | C | Dual-mode auto-detection. Fixed in v0.14.0-dev session 23. |
| **loamspine** | N/A | Crashes on startup | **X** | Tokio nested runtime panic |
| **sweetgrass** | UDS JSON-RPC | `health.liveness` | C | |
| **petaltongue** | UDS JSON-RPC (+ optional TCP) | `health.liveness`, `health.readiness`, `health.check` | C | Full health triad + aliases (March 31). |
| **coralreef** | HTTP (jsonrpsee) | Unknown | ? | |
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
| **squirrel** | No | Not discoverable | **No** (abstract socket) | **X** | Abstract socket invisible to filesystem scan |
| **petaltongue** | No | Not discoverable | **No** (wrong directory) | **X** | Socket not in `$XDG_RUNTIME_DIR/biomeos/` |
| **nestgate** | No | Race condition | Intermittent | **P** | Sometimes starts fast enough to be caught |
| **toadstool** | No | Race condition | Intermittent | **P** | Same timing issue |
| **sweetgrass** | No | Race condition | Intermittent | **P** | Same timing issue |
| **rhizocrypt** | N/A | N/A | **No** (TCP only, no UDS) | **X** | No socket to discover (RC-01) |
| **loamspine** | N/A | N/A | **No** (crashes) | **X** | Panics before any registration (LS-03) |
| **coralreef** | No | Race condition | Intermittent | **P** | Same timing issue |
| **barraCuda** | No | Race condition | Intermittent | **P** | Same timing issue |
| **biomeOS** | Self | N/A | **Yes** (5 methods) | C | Only biomeOS's own capabilities reliably visible |

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
| **loamspine** | ? | ? | Crashes on startup (Tokio issue, not musl-specific). |
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
6. **loamspine**: Fix Tokio nested runtime panic in `infant_discovery`. Add `--port` flag.
7. ~~**rhizocrypt**: Add newline-delimited TCP JSON-RPC listener.~~ **RESOLVED** — v0.14.0-dev session 23 (March 31, 2026).

### High (needed for standard compliance and mobile deployment)

8. ~~**beardog**: Add `--audit-dir` / `BEARDOG_AUDIT_DIR` to avoid CWD writes.~~ **RESOLVED** (Wave 26: `--audit-dir` CLI flag + `BEARDOG_AUDIT_DIR` env var, falls back to `$TMPDIR/beardog`).
9. ~~**beardog**: Wire `birdsong.generate_encrypted_beacon` into server RPC handler.~~ **RESOLVED** (Wave 26: `SecurityHandler` exposes `birdsong.generate_encrypted_beacon` JSON-RPC method).
10. **songbird**: Add `--dark-forest` CLI flag (env-only today, silent plaintext fallback).
11. **songbird**: Add `--pid-dir` or `SONGBIRD_PID_DIR` for Android/container substrates.
12. **toadstool**: Wire `--port` flag to actual server bind. Critical for mobile compute sharing.
13. ~~**petaltongue**: Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`. Add `--port`.~~ **RESOLVED March 31.** Build aarch64 headless still pending.
14. **sweetgrass**: Add `--port` flag (alias for port portion of `--http-address`).
15. **coralreef**: Add `--port` flag for raw newline TCP.

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

### v1.3.0 (March 31, 2026)

**petaltongue IPC Compliance Refresh + Composition Decomposition + ludoSpring V37.1 Gap Alignment**

- petaltongue socket path: X → C (`$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`)
- petaltongue wire framing: P → C (newline TCP via `server --port`)
- petaltongue health methods: ? → C (full `health.liveness` / `health.readiness` / `health.check` + aliases)
- petaltongue `--port`: X → C (`server --port <N>` binds newline TCP JSON-RPC)
- petaltongue health transport: ? → C (UDS + optional TCP)
- petaltongue mobile transport: X → C for TCP (`--port`); aarch64 build still pending
- petaltongue `capabilities.list`: expanded to 41 methods matching full RPC dispatch surface
- Marked petaltongue priority action items 5 and 13 as RESOLVED
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
