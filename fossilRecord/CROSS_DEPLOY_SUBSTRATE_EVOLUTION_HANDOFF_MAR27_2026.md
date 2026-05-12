# Cross-Deploy Substrate Evolution Handoff

**Date**: March 27, 2026
**From**: primalSpring (cross-hardware deployment testing)
**To**: All primal teams (BearDog, Songbird, NestGate, Squirrel, ToadStool, biomeOS)
**Scope**: Per-primal action items from live deployment on x86_64 + aarch64 Pixel/GrapheneOS

---

## Summary

Live cross-hardware deployment testing (eastgate x86_64 + Pixel aarch64 on
iPhone hotspot via ADB) exposed concrete friction in every foundation primal.
This handoff provides specific, actionable items each team can begin
immediately. Items are prioritized by deployment impact.

### What Was Tested

- Built musl-static binaries for x86_64 and aarch64 via `build_ecosystem_musl.sh`
- Harvested into plasmidBin with checksums and multi-arch directory layout
- Deployed Tower (BearDog + Songbird) locally on eastgate (x86_64)
- Deployed Tower to Pixel/GrapheneOS via ADB (`deploy_pixel.sh`)
- Initialized Dark Forest seeds (`seed_workflow.sh init`, `add-node`)
- Validated both gates for health, identity, and crypto determinism
- Tested genetic crypto (BLAKE3, HMAC-SHA256, X25519) cross-architecture
- Attempted BirdSong encrypted beacon generation via RPC

### What Worked

- musl-static binaries are genuinely portable (one binary, any Linux, zero deps)
- Cross-compilation toolchain (`aarch64-linux-gnu-gcc` as musl linker) works
- BearDog crypto primitives produce **identical results on x86_64 and aarch64**
- Songbird TCP transport works on Android
- ADB push deployment pattern is viable for mobile substrates
- `plasmidBin` harvest/fetch/validate pipeline handles multi-arch correctly
- Deploy graph TOML format is expressive and human-readable

### What Broke

- NestGate musl binary segfaults (exit 139)
- BearDog hard-fails without `FAMILY_ID`/`NODE_ID`
- BearDog `--abstract` flag creates filesystem path, not abstract socket
- BearDog writes `audit.log` to CWD, crashes on read-only filesystem
- Songbird PID file to CWD, crashes on read-only filesystem
- `birdsong.generate_encrypted_beacon` RPC method not wired
- Dark Forest requires 4-6 env vars with no CLI flag and silent plaintext fallback

---

## Per-Primal Action Items

### NestGate — P0 (Blocked)

NestGate is the only foundation primal that **cannot be deployed** via plasmidBin.

**Issue 1: musl-static segfault (P0)**

The musl-static binary segfaults immediately on any invocation:

```
$ ./primals/nestgate --help
Segmentation fault (core dumped)    # exit 139
```

The glibc dynamic build works perfectly:

```
$ ./target/release/nestgate --help
NestGate - Sovereign Storage System
Usage: nestgate [OPTIONS] <COMMAND>
Commands: daemon, status, health, version, service, storage, doctor, config, zfs, monitor, discover
```

Diagnosis steps:
1. Build with `RUST_BACKTRACE=1` and test the musl binary
2. Binary-search workspace crates: build `nestgate-core` alone as musl, then `nestgate-bin`
3. Likely culprits (crates that use libc under the hood): `mdns-sd v0.17`, `uzers v0.11`, `sysinfo v0.30`
4. Test with features disabled: `--no-default-features` on each internal crate
5. Check if `mdns-sd` uses DNS resolution that assumes glibc's `getaddrinfo`

**Issue 2: Version inconsistency**

| Source | Version |
|--------|---------|
| Root `Cargo.toml` | 0.1.0 |
| `nestgate-bin/Cargo.toml` | 2.1.0 |
| `README.md` | 4.1.0-dev |

Reconcile to a single version.

**Issue 3: `--port` non-functional**

Per IPC Compliance Matrix, `--port` flag exists in CLI parser but does not bind
a TCP listener. This is a UniBin v1.1 violation (`server --port <PORT>` is MANDATORY).

**Issue 4: `daemon` vs `server`**

Main subcommand is `daemon`. UniBin standard expects `server`. Add `server` as
an alias (clap supports `#[command(alias = "server")]`).

**Issue 5: No `deny.toml`**

NestGate has no `cargo-deny` configuration. All other primals have supply chain
auditing. Add `deny.toml` aligned with ecosystem patterns.

**Priority sequence**: Fix musl segfault first (everything else is blocked).
Then wire `--port`, alias `server`, add `deny.toml`.

---

### BearDog — P1 (High Priority, Partially Working)

BearDog's crypto foundation is solid and cross-arch deterministic. The issues
are all in the server CLI and runtime assumptions.

**Issue 1: Standalone startup failure (P1, UniBin v1.1 violation)**

```
$ beardog server --listen 0.0.0.0:9100
Error: FAMILY_ID environment variable not set
```

Fix: When `FAMILY_ID` or `NODE_ID` is unset, default to `standalone` / hostname.
Check precedence: `BEARDOG_FAMILY_ID` > `FAMILY_ID` > `"standalone"`.

**Issue 2: Abstract socket bug (P1, Android deployment blocker)**

The `--abstract` flag is supposed to create a Linux abstract namespace socket
(`\0biomeos_beardog`). Instead, BearDog treats the name as a filesystem path:

```
Failed to bind socket on Unix (filesystem): @biomeos_beardog_6df362cb
```

Fix: When `--abstract` is set, create the socket with a null byte prefix:
```rust
let addr = std::os::unix::net::SocketAddr::from_abstract_name(name)?;
```

**Issue 3: CWD audit log (P1, read-only filesystem crash)**

BearDog writes `audit.log` to the current working directory. On Android
(`/data/local/tmp/plasmidBin/primals/`), this is read-only.

Fix: Add `--audit-dir <PATH>` flag and `BEARDOG_AUDIT_DIR` env. Default to
`$XDG_RUNTIME_DIR/biomeos/beardog/` on Linux, `$TMPDIR` on Android.

**Issue 4: Seed lifecycle CLI (P1, deployment friction)**

There is no programmatic way to generate, export, or verify trust seeds:

```bash
# These should exist but don't:
beardog seed generate --family-name "eastgate-family"
beardog seed export --format base64
beardog seed verify
```

Currently bridged by `plasmidBin/seed_workflow.sh` which calls `beardog entropy`
and `beardog key generate/derive`, but this is fragile.

**Issue 5: `birdsong.generate_encrypted_beacon` RPC not wired (P2)**

The `birdsong` CLI command for encrypted beacon generation exists, but the
corresponding JSON-RPC method is not registered in the server's RPC handler:

```json
{"jsonrpc":"2.0","method":"birdsong.generate_encrypted_beacon","params":{"beacon_seed":"..."},"id":1}
// Response: Method not found
```

Fix: Register the method in the server's RPC dispatch table alongside the
existing `crypto.*` methods.

**What works well**: All `crypto.*` RPC methods (BLAKE3, HMAC-SHA256, X25519,
ChaCha20-Poly1305, Ed25519, ECDSA, HKDF, Argon2id) work perfectly and produce
deterministic results across x86_64 and aarch64.

---

### Songbird — P1 (High Priority, Close to Compliant)

Songbird is the closest to full deployment compliance. Issues are CLI ergonomics
and runtime path assumptions.

**Issue 1: Dark Forest env-only (P1)**

Dark Forest mode requires 4-6 environment variables with no CLI flag:

```bash
export SONGBIRD_DARK_FOREST=true
export SONGBIRD_AUTO_DISCOVERY=true
export SONGBIRD_SECURITY_PROVIDER=beardog
export BEARDOG_SOCKET=/run/user/1000/biomeos/beardog.sock
```

If any variable is missing or misconfigured, Songbird silently falls back to
plaintext beacons — a security issue with no diagnostic warning.

Fix:
1. Add `--dark-forest` CLI flag that sets the above variables
2. When `--dark-forest` is set, validate that `BEARDOG_SOCKET` is reachable
3. If dark forest is configured but BearDog is unreachable, emit a WARNING (not silent fallback)

**Issue 2: PID file directory (P1, Android crash)**

Songbird writes PID files to CWD. On Android's read-only filesystem, this fails.

Fix: Add `--pid-dir <PATH>` flag and `SONGBIRD_PID_DIR` env. Default to
`$XDG_RUNTIME_DIR/biomeos/songbird/`.

**Issue 3: Health method naming (P2)**

Songbird exposes `health` (short name) and HTTP `/health`. Per Semantic Method
Naming Standard v2.2, the canonical names are `health.liveness`,
`health.readiness`, `health.check`.

Fix: Add aliases so `health.liveness` resolves to the existing health handler.

**Issue 4: `--listen addr:port` (P2)**

Songbird uses `--port PORT` for the HTTP server. For deployment script
consistency, add `--listen addr:port` as an alias (BearDog pattern).

---

### Squirrel — P2 (Medium Priority)

**Issue 1: Abstract-only socket (P2)**

Squirrel creates only an abstract namespace socket (`@squirrel`), which is
invisible to `readdir()`. Filesystem-based discovery tools (including biomeOS
capability scanning) cannot find it.

Fix: Create a filesystem socket at `$XDG_RUNTIME_DIR/biomeos/squirrel.sock`
alongside the abstract socket.

**Issue 2: Non-standard health method names (P2)**

Squirrel uses `system.health`, `system.status`, `system.ping` instead of the
standard `health.liveness`, `health.readiness`, `health.check`.

Fix: Add aliases via `normalize_method()` (Squirrel already has this function).

**Issue 3: `--port + --bind` should be `--listen` (P2)**

Squirrel takes `--port` and `--bind` as separate flags. Converge to `--listen
addr:port` (BearDog pattern) with backward-compatible aliases.

---

### ToadStool — P2 (Medium Priority)

**Issue 1: `--port` not wired (P2)**

The `--port` flag exists in the CLI parser but is not forwarded to the server
implementation. The listener never binds TCP.

Fix: Wire the parsed port value to the actual server bind call.

**Issue 2: Health method verification (P2)**

Health methods need verification. Ensure `health.liveness`, `health.readiness`,
`health.check` are registered (not just HTTP `/health`).

---

### biomeOS — P2 (Enabler Role)

biomeOS is not a peer primal for deployment — it is the orchestrator. These
items enable it to drive cross-deploy workflows:

**Issue 1: Deploy graph execution (P2)**

Deploy graph TOMLs (e.g., `three_node_covalent_cross_network.toml`) describe
multi-node compositions but are currently consumed only by deploy scripts.
`biomeos deploy --graph <path>` should execute them natively.

**Issue 2: Absorb deploy script patterns (P3)**

The patterns in `deploy_pixel.sh` (ADB push, abstract sockets, port forwarding)
and `bootstrap_gate.sh` (clone + fetch + start) should evolve into biomeOS
subcommands:

```bash
biomeos deploy --target pixel --graph tower.toml --dark-forest
biomeos deploy --target ssh://user@host --graph tower.toml --bootstrap
```

**Issue 3: neural-api-server in plasmidBin (P2)**

neural-api-server should be in the plasmidBin harvest map and included in
NUCLEUS compositions. It is the primal that enables agentic composition.

---

## CLI Convergence Standard

The #1 deployment friction is inconsistent CLI flags. Each primal uses different
flags for the same concept, forcing deploy scripts to maintain per-primal case
blocks:

| Concept | Recommended | BearDog | Songbird | Squirrel | ToadStool | NestGate |
|---------|------------|---------|----------|----------|-----------|----------|
| TCP bind | `--listen addr:port` | `--listen` (correct) | `--port` | `--port --bind` | `--port` | segfaults |
| Unix socket | `--socket path` | `--socket` | `--socket` | `-s/--socket` | `--socket` | env only |
| Family ID | `--family-id id` | `--family-id` | env only | env only | `--family-id` | env only |
| Abstract socket | `--abstract` | `--abstract` (broken) | N/A | N/A | N/A | N/A |
| Dark Forest | `--dark-forest` | N/A | env only | N/A | N/A | N/A |
| Server mode | `server` | `server` | `server` | `server` | `server` | `daemon` |

When all primals converge on the recommended column, the per-primal case blocks
in `start_primal.sh`, `deploy_gate.sh`, `deploy_pixel.sh`, and
`bootstrap_gate.sh` collapse to a single generic invocation:

```bash
$PRIMAL server --listen 0.0.0.0:$PORT --socket $SOCKET --family-id $FAMILY_ID
```

---

## Substrate Requirements Summary

### Linux Desktop (x86_64)

Standard environment. Filesystem UDS, systemd lifecycle, `$XDG_RUNTIME_DIR`.
All primals should work here without modification.

### Linux Server/Remote (x86_64, bootstrapped)

Same as desktop but no display server, no development tools. Binaries fetched
from plasmidBin via `fetch.sh`. Requires:
- Firewall configuration (ports 9100, 9200 minimum)
- Out-of-band seed distribution
- `bootstrap_gate.sh` handles setup

### Android/GrapheneOS (aarch64, ADB)

Constrained environment with specific requirements:
- **No systemd**: Primals run as foreground processes via ADB shell
- **SELinux**: Filesystem UDS may be blocked. Abstract sockets (`\0name`) bypass.
- **Read-only CWD**: `/data/local/tmp/plasmidBin/primals/` is not writable for data.
  Must set `HOME=/data/local/tmp/biomeos`, `TMPDIR=/data/local/tmp/biomeos`.
- **No package manager**: All binaries are musl-static, pushed via `adb push`.
- **Port forwarding**: `adb forward tcp:PORT tcp:PORT` bridges device to host.
  Use `--local-port-offset` when host ports conflict.
- **Shell**: `/system/bin/sh` (not bash). Scripts must be POSIX-compatible.

### Future: macOS, Windows, Container

Not yet tested. musl-static is Linux-only. macOS requires native compilation.
Windows requires cross-compilation to `x86_64-pc-windows-gnu` or native build.
Container substrates should work with current musl binaries but need lifecycle
management via the container runtime instead of systemd/ADB.

---

## Dark Forest Deployment Checklist

For any new gate joining a Dark Forest mesh:

1. Initialize family seeds on the primary gate:
   ```bash
   ./seed_workflow.sh init --family-name "family-name"
   ./seed_workflow.sh add-node --node-id <gate-name>
   ```

2. Distribute beacon seed to the new gate (out-of-band):
   ```bash
   ./seed_workflow.sh distribute --node-id <gate-name>
   ```

3. Start primals with Dark Forest configuration:
   ```bash
   export SONGBIRD_DARK_FOREST=true
   export SONGBIRD_AUTO_DISCOVERY=true
   export SONGBIRD_SECURITY_PROVIDER=beardog
   export BEARDOG_SOCKET=$XDG_RUNTIME_DIR/biomeos/beardog.sock
   ```

4. Validate:
   ```bash
   ./validate_gate.sh <gate-ip> --birdsong
   ./validate_mesh.sh --gates "gate1=ip1,gate2=ip2" --birdsong-exchange
   ```

---

## Genetic Crypto Verification

Cross-architecture determinism was confirmed for all tested primitives:

| Primitive | x86_64 Result | aarch64 Result | Match |
|-----------|---------------|----------------|-------|
| BLAKE3(`"hello"`) | `ea8f163d...` | `ea8f163d...` | Yes |
| HMAC-SHA256(`"key"`, `"data"`) | `5031fe3d...` | `5031fe3d...` | Yes |
| X25519 key exchange | Shared secret matches | Shared secret matches | Yes |

This confirms the RustCrypto suite produces identical results across
architectures — the genetic trust model's cryptographic foundation is sound.

---

## Standards Referenced

- `UNIBIN_ARCHITECTURE_STANDARD.md` v1.2 — Binary naming, `--port`, standalone startup, substrate requirements
- `ECOBIN_ARCHITECTURE_STANDARD.md` v3.0 — Pure Rust, musl-static, cross-compilation
- `PRIMAL_IPC_PROTOCOL.md` v3.1 — Wire framing, socket paths, JSON-RPC 2.0
- `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.2 — Health method names, capability enumeration
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.1 — Socket naming, filesystem requirement
- `IPC_COMPLIANCE_MATRIX.md` v1.1 — Per-primal compliance tracking
- `GATE_DEPLOYMENT_STANDARD.md` — Gate types, substrates, deployment patterns
- `birdsong/DARK_FOREST_BEACON_GENETICS_STANDARD.md` — Two-seed trust model

---

## Open Questions

1. Should `--dark-forest` become a UniBin v1.3 MANDATORY flag for all primals
   that participate in BirdSong? Or remain Songbird-specific?
2. Should biomeOS expose a `biomeos gate add --adb` subcommand for mobile gates?
3. NestGate's musl segfault may require dropping or feature-gating `mdns-sd`.
   Is mDNS discovery still needed if Songbird handles all discovery?
4. Should abstract sockets be the default on Android (auto-detected via
   `uname -o` or `/system/build.prop`)?
