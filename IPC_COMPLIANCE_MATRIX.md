# IPC Compliance Matrix

**Version:** 1.0.0
**Date:** March 25, 2026
**Status:** Living document — updated as primals evolve
**Authority:** wateringHole (ecoPrimals Core Standards)

This matrix tracks each primal's alignment across the IPC interoperability
dimensions defined in `PRIMAL_IPC_PROTOCOL.md` v3.1, `UNIBIN_ARCHITECTURE_STANDARD.md`
v1.1, `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1, and
`SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2.

Data sourced from esotericWebb's first live multi-primal composition
(March 2026) and direct inspection of each primal's source code.

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
| **nestgate** | Newline | -- | **P** | Socket-only by default. `--port` exists but is non-functional. |
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
| **songbird** | `health` alias | -- | -- | `health` (short) | **P** | Responds to `health` but not verified for `health.liveness`. |
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
| **nestgate** | `daemon` | No (ignored) | `--port` exists but socket-only | **P** | Subcommand is `daemon`, not `server`. `--port` not functional. |
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

| Primal | Wire Framing | Socket Path | Health Names | `--port` | Standalone | Overall |
|--------|-------------|-------------|-------------|----------|-----------|---------|
| **rhizocrypt** | X | P | ? | P | C | Needs work |
| **loamspine** | C | X | ? | X | X | Blocked (crash) |
| **sweetgrass** | P | P | C | X | C | Close |
| **squirrel** | P | X | X | P | C | Needs work |
| **beardog** | C | P | C | X | X | Needs work |
| **songbird** | C | C | P | ? | C | Close |
| **petaltongue** | P | X | ? | X | C | Needs work |
| **nestgate** | P | P | ? | P | C | Close |
| **toadstool** | P | ? | ? | X | C | Needs audit |
| **coralreef** | P | P | ? | X | C | Needs work |
| **biomeOS** | P | C | C | -- | C | Conformant (orchestrator) |

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

## Related Standards

- `PRIMAL_IPC_PROTOCOL.md` v3.1 — Wire framing, socket paths, standalone startup
- `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1 — `--port` convention, standalone startup
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1 — Socket naming, symlinks, filesystem requirement
- `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2 — Health method names, capability enumeration
- `SPRING_INTEROP_LESSONS.md` — Practical learnings from Webb's composition
