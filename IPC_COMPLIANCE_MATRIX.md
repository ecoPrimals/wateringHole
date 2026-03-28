# IPC Compliance Matrix

**Version:** 1.2.0
**Date:** March 28, 2026
**Status:** Living document — updated as primals evolve
**Authority:** wateringHole (ecoPrimals Core Standards)

This matrix tracks each primal's alignment across the IPC interoperability
dimensions defined in `PRIMAL_IPC_PROTOCOL.md` v3.1, `UNIBIN_ARCHITECTURE_STANDARD.md`
v1.1, `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1, and
`SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2.

Data sourced from esotericWebb's first live multi-primal composition
(March 2026), direct inspection of each primal's source code, and
**live cross-hardware deployment testing** (March 27, 2026) across
x86_64 eastgate + aarch64 Pixel/GrapheneOS on iPhone hotspot.

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
| **rhizocrypt** | -- | HTTP POST (Axum) | **X** | TCP JSON-RPC is HTTP-wrapped only. Webb's raw newline client gets 400 Bad Request. Needs raw newline TCP listener. |
| **loamspine** | Newline | Newline | C | Accepts both raw newline and HTTP POST on JSON-RPC port. |
| **sweetgrass** | Newline | HTTP POST (Axum) | **P** | UDS is newline-conformant. TCP is HTTP-only. Sufficient for UDS composition. |
| **squirrel** | Newline (abstract) | -- | **P** | Newline framing correct, but socket is abstract-namespace only (see Discovery). No TCP listener. |
| **beardog** | Newline | Newline | C | Both transports use raw newline framing. |
| **songbird** | Newline | Newline | C | Standard newline framing on both transports. |
| **petaltongue** | Newline | -- | **P** | UDS newline-conformant. No TCP listener exposed via `--port`. |
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
| **rhizocrypt** | Calculated from tarpc port | N/A (TCP) | -- | -- | **P** | No UDS socket at all. TCP only. |
| **loamspine** | Not reached (crash) | ? | ? | -- | **X** | Crashes before socket bind (Tokio nested runtime). |
| **sweetgrass** | `/run/user/1000/biomeos/sweetgrass.sock` | Yes | Yes | No | **P** | Conformant path, no family suffix. Missing domain symlink. |
| **squirrel** | `@squirrel` (abstract) | **No** | No | No | **X** | Abstract namespace only. Invisible to `readdir()`. Not discoverable. |
| **beardog** | `/run/user/1000/biomeos/beardog.sock` | Yes | Yes | No | **P** | Conformant path, no family suffix. Missing domain symlink. |
| **songbird** | `/run/user/1000/biomeos/songbird.sock` | Yes | Yes | No | C | Registry primal, domain symlink not required. |
| **petaltongue** | `/run/user/1000/petaltongue/petaltongue-nat0-default.sock` | Yes | **No** | No | **X** | Custom directory, not in `biomeos/`. Non-discoverable. |
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
| **rhizocrypt** | ? | ? | ? | ? | ? | Not reachable via raw newline (HTTP-only). |
| **loamspine** | ? | ? | ? | ? | ? | Crashes on startup. |
| **sweetgrass** | Yes | ? | ? | -- | C | Responds to `health.liveness`. |
| **squirrel** | **No** | **No** | **No** | `system.health`, `system.status`, `system.ping` | **X** | Uses `system.*` domain exclusively. Non-conformant. |
| **beardog** | Yes | Yes | -- | -- | C | Canonical names. |
| **songbird** | `health` alias | -- | -- | `health` (short), HTTP `/health` | **P** | Responds to `health` (short name) and HTTP `/health`. Does not expose `health.liveness` by canonical name. Verified live (March 27). |
| **petaltongue** | ? | ? | ? | ? | ? | Not verified. |
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
| **rhizocrypt** | `server` | Yes | `--port` (tarpc), JSON-RPC on calculated port | **P** | `--port` is tarpc, not JSON-RPC. JSON-RPC port is derived (port + offset). |
| **loamspine** | `server` | No | `--jsonrpc-port` | **X** | No `--port` flag. Uses `--jsonrpc-port`. |
| **sweetgrass** | `server` | No | `--http-address` (addr:port) | **X** | No `--port` flag. Takes full address, not just port. |
| **squirrel** | `server` | Yes (ignored) | `--port` exists but UDS is primary | **P** | `--port` accepted but TCP not used when UDS is available. |
| **beardog** | `server` | No | `--listen` (addr:port) | **X** | No `--port` flag. Uses `--listen`. |
| **songbird** | `server` | ? | ? | ? | Not verified. |
| **petaltongue** | `server` | No | None | **X** | No port option at all. UDS only. |
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
| **beardog** | **No** | Hard-fails | **X** | Exits with error if `FAMILY_ID` and `NODE_ID` not set. |
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
| **beardog** | C | P | C | C (`--listen`) | X (FAMILY_ID) | C (TCP) | A++ | Close |
| **songbird** | C | C | P | C (`--listen`) | C | C (TCP) | A++ | Close |
| **squirrel** | P | X | X | C (`--port`) | C | C (abstract+HTTP) | A++ | Close |
| **toadstool** | P | ? | ? | X (not wired) | C | P (caps only) | A++ | Needs work |
| **nestgate** | X | P | ? | X (not wired) | C | X (no aarch64) | A++ (x86) | Needs work |
| **biomeos** | P | C | C | X (forces UDS) | C | X (UDS only) | A++ | Needs TCP mode |
| **petaltongue** | P | X | ? | X (none) | C | X (no aarch64) | A++ (x86) | Needs work |
| **sweetgrass** | P | P | C | X | C | ? | ? | Close |
| **rhizocrypt** | X | P | ? | P | C | ? | ? | Needs work |
| **loamspine** | C | X | ? | X | X (crash) | ? | ? | Blocked |
| **coralreef** | P | P | ? | X | C | ? | ? | Needs work |
| **skunkbat** | ? | ? | ? | ? | ? | ? | ? | Needs audit |

---

## Priority Actions

### Critical (blocks inter-primal composition)

1. **squirrel**: Add filesystem socket in `$XDG_RUNTIME_DIR/biomeos/squirrel.sock` alongside abstract socket. Add `health.liveness` / `health.readiness` / `health.check` method handlers.
2. **beardog**: Accept `--port` (alias for `--listen`, port-only). Default `FAMILY_ID` to `standalone` when unset.
3. **loamspine**: Fix Tokio nested runtime panic in `infant_discovery`. Add `--port` flag (alias for `--jsonrpc-port`).
4. **rhizocrypt**: Add newline-delimited TCP JSON-RPC listener (alongside HTTP Axum server).

### High (needed for standard compliance)

5. **petaltongue**: Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`. Add `--port` flag.
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
| **rhizocrypt** | HTTP POST (Axum) | Unknown | ? | HTTP-wrapped only |
| **loamspine** | N/A | Crashes on startup | **X** | Tokio nested runtime panic |
| **sweetgrass** | UDS JSON-RPC | `health.liveness` | C | |
| **petaltongue** | UDS JSON-RPC | Unknown | ? | |
| **coralreef** | HTTP (jsonrpsee) | Unknown | ? | |
| **biomeOS** | HTTP | `/health`, `health.liveness` | C | Full health suite |

**Recommendation**: All primals should expose `health.liveness` via raw TCP
newline-delimited JSON-RPC (primary) and optionally HTTP `/health` (convenience).
Validation tools (`validate_gate.sh`) currently brute-force three protocols; this
wastes round-trips and makes diagnostics ambiguous.

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
| **rhizocrypt** | ? | ? | Not tested. |
| **sweetgrass** | ? | ? | Not tested. |
| **coralreef** | ? | ? | Not tested. |

### Android/GrapheneOS Substrate

Tested on Pixel 8a with GrapheneOS via ADB (aarch64-linux-musl binaries).
**Updated March 28** with comprehensive findings from NUCLEUS + cross-gate deployment.

| Requirement | Standard | Status | Notes |
|-------------|----------|--------|-------|
| **TCP listener** | `--listen 0.0.0.0:PORT` | C (BearDog, Songbird) | TCP is the **universal mobile transport**. Every primal MUST support it. |
| **Abstract sockets** | `--abstract` flag | P (Squirrel C, BearDog P) | Squirrel's `@squirrel` works perfectly on GrapheneOS. BearDog logs filesystem path instead of abstract — functional but buggy. |
| **Filesystem UDS** | Default socket path | **X (all)** | SELinux on GrapheneOS denies `sock_file create` from `shell` context. Filesystem UDS is NOT viable on Android. |
| **Writable runtime dir** | `HOME`/`TMPDIR` writable | C | `cd /data/local/tmp/biomeos` before launch. Set `HOME`/`TMPDIR` env vars. |
| **No systemd** | No systemd assumptions | C | Startup via shell script (`deploy_pixel.sh`). |
| **Audit/PID files** | Directory configurable | P | BearDog writes `audit.log` to CWD — crashes on read-only fs. Needs `--audit-dir` or `BEARDOG_AUDIT_DIR`. |
| **SELinux** | Platform-aware IPC | Critical | `adb logcat` confirmed `avc: denied { create } ... tcontext=u:object_r:shell_data_file:s0 tclass=sock_file`. TCP and abstract sockets bypass this. |
| **ADB port forwarding** | Cross-gate access | C | `deploy_pixel.sh --local-port-offset N` for conflict avoidance. |
| **biomeOS orchestration** | `biomeos api --port` on mobile | **X** | biomeOS forces Unix socket even when `--port` specified. Needs TCP-only mode for mobile. |

### Per-Primal Mobile Transport Status (March 28, 2026)

| Primal | TCP | Abstract Socket | Filesystem UDS | Mobile Ready? |
|--------|-----|-----------------|----------------|---------------|
| **beardog** | C (`--listen`) | P (buggy log) | X (SELinux) | Yes (via TCP) |
| **songbird** | C (`--listen`) | ? | X (SELinux) | Yes (via TCP) |
| **squirrel** | C (`--port`) | C (`@squirrel`) | X (SELinux) | Yes (both) |
| **toadstool** | X (not wired) | ? | X (SELinux) | Partial (caps only) |
| **nestgate** | X (not wired) | ? | X (SELinux) | No (needs aarch64 build + TCP) |
| **biomeos** | X (forces UDS) | ? | X (SELinux) | No (needs TCP mode) |
| **petaltongue** | X (no flag) | ? | X (SELinux) | No (needs aarch64 + TCP) |

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
4. **beardog**: Default `FAMILY_ID` to `standalone` when unset. Current hard-fail breaks standalone startup.
5. **beardog**: Fix `--abstract` socket logging — logs filesystem path `@biomeos_beardog_*` instead of confirming abstract namespace bind.
6. **loamspine**: Fix Tokio nested runtime panic in `infant_discovery`. Add `--port` flag.
7. **rhizocrypt**: Add newline-delimited TCP JSON-RPC listener.

### High (needed for standard compliance and mobile deployment)

8. **beardog**: Add `--audit-dir` / `BEARDOG_AUDIT_DIR` to avoid CWD writes (read-only filesystem crash on Android).
9. **beardog**: Wire `birdsong.generate_encrypted_beacon` into server RPC handler.
10. **songbird**: Add `--dark-forest` CLI flag (env-only today, silent plaintext fallback).
11. **songbird**: Add `--pid-dir` or `SONGBIRD_PID_DIR` for Android/container substrates.
12. **toadstool**: Wire `--port` flag to actual server bind. Critical for mobile compute sharing.
13. **petaltongue**: Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock`. Add `--port`. Build aarch64 headless.
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
