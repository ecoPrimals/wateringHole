# cellMembrane — Wave 82c plasmidBin Ownership Sprint

**Date**: 2026-06-06  
**Gate**: ironGate  
**Context**: plasmidBin ownership transfer from primalSpring → cellMembrane

---

## Completed

### 1. `plasmid.refresh` Command (P1)

New `membrane plasmid.refresh` command added to the membrane CLI:

```
membrane plasmid.refresh [--primal NAME] [--source-dir DIR] [--dry-run]
```

Flow: locate local binary → SCP to VPS as `{name}.new` → `chmod+mv` atomic
replace → `systemctl restart {unit}` → report.

- Derives primal list from service registry (no hand-maintained list)
- Resolves source from `--source-dir`, `PLASMIDBIN_STAGING`, or default staging
- Uses `ServicePaths` for install paths
- Supports `--dry-run` for safe preview

### 2. SCP Transport (`ssh.rs`)

Added `scp_to()` function for file transfer to VPS, matching the existing
`exec()` pattern (respects `ShadowConfig` timeout and host).

### 3. `sources.toml` Review

All 13 primals + sourDough + esotericWebb are registered. Tag pattern is
consistent (`v{version}`). Private repos (bearDog, skunkBat) properly marked.
`build_args` correct for workspace crates (biomeos → `-p biomeos-unibin`,
skunkbat → `-p skunk-bat-server`).

### 4. UDS Health Probe Diagnosis (squirrel + petaltongue)

**Finding**: Both primals accept UDS connections and listen on STREAM sockets
(`ss -lxp` confirms PID binding). However, they never respond to any JSON-RPC
message (newline-delimited, length-prefixed, HTTP-wrapped — all tested).

For comparison: bearDog responds instantly on the same socket type with the
same framing.

**Root cause**: The upstream primal code has separate TCP and UDS server loops.
The UDS loop accepts connections but doesn't dispatch received data through
the JSON-RPC handler. The TCP handler (port 8080 for petaltongue) works fine.

**Upstream action needed**:
- squirrel: Wire UDS accepted connections into the same JSON-RPC dispatch as TCP
- petaltongue: Same issue, same fix pattern

**Workaround**: Health check via socket file existence (`SocketExists` method
in the service registry) works — the service IS running, just not responding
to IPC on UDS.

---

## Remaining (P2 — next wave)

- `plasmid.deploy` — Absorb full `deploy_membrane.sh deploy` flow into Rust CLI
- `plasmid.harvest` — Build single primal from source, checksum, store
- CI workflow wiring for cellMembrane org
- Peptidoglycan self-refresh via Forgejo releases

---

## Gate Status

- **13/13 primals ALIVE on VPS** (10 via UDS health, 2 via socket-exists, 1 TCP)
- **mesh.primal.eco** operational, TLS + proxy
- **All 5 domains** serving with sovereign TLS
- **plasmid.refresh** ready for next VPS binary push cycle
