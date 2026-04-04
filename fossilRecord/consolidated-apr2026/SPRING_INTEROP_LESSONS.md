# Spring Interop Lessons

**Version:** 1.0.0
**Date:** March 25, 2026
**Status:** Living document
**Authority:** wateringHole (ecoPrimals Core Standards)

Practical learnings from the first live multi-primal composition using
esotericWebb as the first garden to attempt live composition. These lessons
apply to both springs and gardens composing primals into working systems.

---

## Context

esotericWebb is a narrative game engine (garden, gen4) that consumes capabilities
from across the primal ecosystem: AI (squirrel), visualization (petaltongue),
provenance (sweetgrass, rhizocrypt), security (beardog), storage (nestgate), and
mesh networking (loamspine). It was the first garden to attempt live composition
with all plasmidBin primals simultaneously.

The composition succeeded partially — Webb connected to sweetgrass and
petaltongue, ran a game session with live cross-primal calls, and degraded
gracefully when other primals were unreachable. The experience exposed
systematic interop gaps that have since been codified in updated wateringHole
standards.

---

## What Worked

### Graceful degradation

Webb's `PrimalBridge` wraps every cross-primal call with circuit breakers and
retry policies. When a primal is unreachable or returns an error, the bridge
returns a sensible default and sets `degraded: true` in the response. The game
continues with reduced functionality rather than crashing.

This is the right pattern. Springs SHOULD treat all primal calls as fallible
and design for partial availability from the start.

### Capability-based discovery with filesystem probing

Webb discovers primals by scanning `$XDG_RUNTIME_DIR/biomeos/` for
domain-named sockets (`ai.sock`, `provenance.sock`). This worked for primals
that placed conformant filesystem sockets. It also supports environment
variable overrides (`SQUIRREL_ADDRESS`, etc.) for explicit configuration.

### plasmidBin as sterile transfer surface

Pre-built binaries from `plasmidBin` eliminated the need to clone and build
each primal's private source code. The `fetch.sh` / `harvest.sh` workflow
with checksummed `manifest.lock` provided a clean, repeatable way to get
the right binaries to the right place.

### newline-delimited JSON-RPC over raw streams

Webb's `PrimalClient` sends one JSON object per line, terminated by `\n`,
over `UnixStream` or `TcpStream`. This is simple, debuggable (pipe through
`jq`), and fast. It worked immediately with primals that use the same framing.

---

## What Didn't Work (And Why)

### 1. HTTP-wrapped JSON-RPC on TCP

**Symptom:** Webb sends raw newline JSON-RPC to rhizocrypt's TCP port and gets
back `HTTP/1.1 400 Bad Request`.

**Root cause:** rhizocrypt serves JSON-RPC behind Axum (HTTP). Webb's client
doesn't speak HTTP — it writes raw JSON to the socket. The standard never
specified which framing to use, so both approaches were valid.

**Fix:** `PRIMAL_IPC_PROTOCOL.md` v3.1 now mandates newline-delimited framing
as the canonical inter-primal surface. HTTP is for external APIs.

**Lesson for spring developers:** If you're building a JSON-RPC client, use
raw newline framing. If a primal only speaks HTTP JSON-RPC, that's a
compliance gap in the primal, not your client.

### 2. Abstract namespace sockets

**Symptom:** squirrel reports binding to `/run/user/1000/biomeos/squirrel.sock`
in logs, but `ls /run/user/1000/biomeos/` shows no such file. Webb's
discovery finds nothing. `ss -xlp` reveals squirrel is listening on `@squirrel`
(Linux abstract namespace).

**Root cause:** Abstract namespace sockets exist only in the kernel, not the
filesystem. `readdir()` cannot see them. Any discovery that probes for socket
files will miss them entirely.

**Fix:** `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1 now requires filesystem
sockets on Linux. Abstract sockets are acceptable as an additional transport
but MUST NOT be the only one.

**Lesson for spring developers:** Always probe with filesystem operations
(`readdir`, `stat`). Don't try to discover abstract sockets — if a primal
only has abstract sockets, that's a compliance gap.

### 3. Custom socket directories

**Symptom:** petaltongue creates its socket at
`/run/user/1000/petaltongue/petaltongue-nat0-default.sock`. Webb's discovery
scans `$XDG_RUNTIME_DIR/biomeos/` and doesn't find it.

**Root cause:** Each primal chose its own convention before the standard existed.

**Fix:** Sockets MUST live in `$XDG_RUNTIME_DIR/biomeos/`. Domain symlinks
(e.g., `visualization.sock -> petaltongue.sock`) enable capability-based
filesystem discovery.

**Lesson for spring developers:** Only scan `$XDG_RUNTIME_DIR/biomeos/`.
If a primal isn't there, it's non-conformant. You can support env var
overrides (`{PRIMAL}_ADDRESS`) as escape hatches for non-conformant primals.

### 4. Inconsistent `--port` flags

**Symptom:** Webb's `PrimalLauncher` spawns primals with
`{binary} server --port {port}`. This fails for loamspine (`--jsonrpc-port`),
sweetgrass (`--http-address`), beardog (`--listen`), petaltongue (no port
flag at all), and nestgate (`daemon` subcommand).

**Root cause:** Each primal invented its own CLI interface.

**Fix:** `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1 now mandates `--port <PORT>`
on the `server` subcommand. Additional flags are acceptable, but `--port` is
the universal entry point.

**Lesson for spring developers:** Use `{binary} server --port {port}` as the
canonical launch command. If a primal doesn't support it, file a compliance
issue. In the meantime, maintain a launcher config that maps primal names to
their actual CLI invocations.

### 5. Hard-fail on missing environment variables

**Symptom:** beardog exits immediately with `FAMILY_ID environment variable
must be set` when launched without identity variables.

**Root cause:** beardog was designed for full ecosystem operation with biomeOS
managing identity. It never anticipated standalone or spring-driven startup.

**Fix:** `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1 now requires standalone
startup with sensible defaults.

**Lesson for spring developers:** Set `FAMILY_ID=standalone` and
`NODE_ID=local` as fallback environment variables when launching primals.
This works for primals that require them and is ignored by primals that don't.

### 6. Non-standard health method names

**Symptom:** Webb probes `health.liveness` on squirrel and gets
`METHOD_NOT_FOUND`. Squirrel only responds to `system.health`.

**Root cause:** Squirrel predates the semantic method naming standard and
uses its own `system.*` convention.

**Fix:** `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2 reinforces `health.*` as
non-negotiable. `system.*` is not a valid substitute.

**Lesson for spring developers:** Always probe `health.liveness`. If it
returns `METHOD_NOT_FOUND`, the primal is non-conformant. You MAY fall back
to `system.health`, `ping`, or `health` as a courtesy, but log a warning.

### 7. Tokio nested runtime panic

**Symptom:** loamspine crashes on startup with `Cannot start a runtime from
within a runtime` at `infant_discovery.rs:233`.

**Root cause:** Code calls `block_on()` inside an async context. This is a
code bug, not a standards issue.

**Lesson for spring developers:** Not much you can do here. Degrade
gracefully and note it in the compliance matrix. The primal team needs to fix
it.

---

## The Sterile Transfer Surface Pattern

The successful composition pattern that emerged:

```
plasmidBin/
  fetch.sh              # Download checksummed binaries
  manifest.lock         # Pinned versions + checksums
  <primal>/
    metadata.toml       # Provenance, capabilities, compatibility
    <binary>            # The executable

$XDG_RUNTIME_DIR/biomeos/
  <primal>.sock         # Primal-named filesystem socket
  <domain>.sock         # Capability-domain symlink -> primal.sock

Spring startup:
  1. fetch.sh (get binaries)
  2. Launch primals: {binary} server --port {port}
  3. Wait for health.liveness on each
  4. Discover by capability domain (filesystem scan or env vars)
  5. Compose (capability calls through PrimalBridge)
  6. Degrade gracefully on any failure
```

This is analogous to aseptic technique in microbiology — clean transfer
surfaces, verified provenance, and graceful handling of contamination.

---

## Recommendations for Spring Developers

1. **Design for partial availability.** Wrap every primal call with circuit
   breakers and return sensible defaults. Never let a single primal failure
   crash your spring.

2. **Use capability-based discovery.** Scan for domain-named sockets, not
   primal-named ones. This decouples your spring from specific primals.

3. **Support env var overrides.** `{PRIMAL}_ADDRESS` lets operators configure
   non-conformant primals without code changes.

4. **Set identity fallbacks when launching.** Always provide
   `FAMILY_ID=standalone NODE_ID=local` when spawning primals.

5. **Validate with `health.liveness` before use.** Don't assume a primal is
   ready just because the process started. Wait for a successful health probe.

6. **Log interop failures clearly.** When a primal is unreachable or
   non-conformant, log exactly what happened (method name, transport, error)
   so it's easy to diagnose and file upstream.

7. **Pin your primals.** Use `plasmidBin/manifest.lock` to pin exact versions.
   Primal APIs can change between versions, and capability drift is real.

8. **Test with mock primals.** For unit and integration tests, implement a
   minimal JSON-RPC responder that handles `health.liveness` and your required
   capability methods. esotericWebb's `e2e_ipc.rs` demonstrates this pattern.

---

## Related Standards

- `PRIMAL_IPC_PROTOCOL.md` v3.1 — Wire framing, socket paths, standalone startup
- `UNIBIN_ARCHITECTURE_STANDARD.md` v1.1 — `--port` convention, standalone startup
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1 — Socket naming, symlinks
- `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2 — Health method names
- `IPC_COMPLIANCE_MATRIX.md` — Per-primal interop status
- `PLASMIBIN_DISTRIBUTION.md` (in esotericWebb `specs/`) — Binary distribution strategy
