# biomeOS — Desktop Substrate Evolution (Phase 56)

**From**: primalSpring v0.9.23 Phase 56
**To**: biomeOS team
**Date**: April 28, 2026
**Priority**: Evolution guidance for Desktop NUCLEUS mode + application session management
**Specs**: `primalSpring/specs/DESKTOP_NUCLEUS_DEPLOYMENT.md`, `DESKTOP_SESSION_MODEL.md`

---

## Summary

primalSpring Phase 55c validated the full 12-primal Desktop NUCLEUS — 28/30
validation checks pass, all crypto tiers operational, all upstream asks
resolved. The composition is currently shell-driven (`composition_nucleus.sh`).

Phase 56 evolves biomeOS into the **native Desktop substrate**: biomeOS owns
the full primal lifecycle, discovery registration, and application session
management. The shell scripts become a convenience fallback.

---

## Ask 1: `NucleusMode::Desktop` (P0)

### What

Extend `NucleusMode` in `crates/biomeos/src/modes/nucleus.rs` with a
`Desktop` variant that spawns all 12 primals (not just 5).

### Current State

```rust
NucleusMode::Full => vec![BEARDOG, SONGBIRD, NESTGATE, TOADSTOOL, SQUIRREL],
```

### Target State

```rust
NucleusMode::Desktop => vec![
    BEARDOG, SONGBIRD,                           // Tower (Phase 1)
    NESTGATE, SQUIRREL,                          // Nest (Phase 2)
    TOADSTOOL, BARRACUDA, CORALREEF,             // Node (Phase 3)
    RHIZOCRYPT, LOAMSPINE, SWEETGRASS,           // Provenance (Phase 4)
    PETALTONGUE,                                 // Meta (Phase 5)
],
```

### Implementation Notes

- Add `Desktop` (or `desktop` alias) to the `NucleusMode` enum and `Cli::Nucleus`
- Add primal constants for the 7 missing primals (barraCuda, coralReef, rhizoCrypt,
  loamSpine, sweetGrass, petalTongue, and their slug variants)
- Each phase waits for the previous phase's primals to be healthy before starting
  the next phase (existing `LifecycleManager` health wait pattern)
- Launch profiles for all 12 primals should be in `config/nucleus_launch_profiles.toml`

### Environment Wiring per Primal

These env vars must be set per primal (derived from `composition_nucleus.sh`):

| Primal | Key Environment Variables |
|--------|--------------------------|
| BearDog | `BEARDOG_FAMILY_SEED`, `FAMILY_ID`, `BEARDOG_NODE_ID` |
| Songbird | `SONGBIRD_SECURITY_PROVIDER={beardog_sock}`, `BTSP_PROVIDER_SOCKET`, `SONGBIRD_DISCOVERY_MODE=disabled` |
| NestGate | `NESTGATE_SOCKET`, `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `NESTGATE_AUTH_MODE=beardog`, `FAMILY_SEED` |
| Squirrel | `SQUIRREL_SOCKET`, `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `LOCAL_AI_ENDPOINT`, `FAMILY_SEED` |
| ToadStool | `TOADSTOOL_SOCKET`, `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `TOADSTOOL_FAMILY_ID`, `NESTGATE_SOCKET` |
| barraCuda | `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `BARRACUDA_FAMILY_ID`, `FAMILY_SEED` |
| coralReef | `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `CORALREEF_FAMILY_ID`, `FAMILY_SEED` |
| rhizoCrypt | `RHIZOCRYPT_SOCKET`, `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `FAMILY_SEED` |
| loamSpine | `LOAMSPINE_SOCKET`, `BEARDOG_SOCKET`, `RHIZOCRYPT_SOCKET`, `DISCOVERY_SOCKET`, `BIOMEOS_FAMILY_ID` |
| sweetGrass | `SWEETGRASS_SOCKET`, `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `FAMILY_SEED` |
| petalTongue | `PETALTONGUE_SOCKET`, `BEARDOG_SOCKET`, `DISCOVERY_SOCKET`, `DISPLAY`, `AWAKENING_ENABLED=false` |

All primals also get `BIOMEOS_SOCKET_DIR` and `BTSP_PROVIDER_SOCKET={beardog_sock}`.

---

## Ask 2: Songbird Registration Loop (P0)

### What

After each primal passes its health check, biomeOS should call `ipc.register`
on Songbird with the primal's capabilities and socket endpoint.

### Why

Today `composition_nucleus.sh` does this registration. biomeOS nucleus mode
trusts socket-env topology but does not call `ipc.register`. This means
`capability.call` and `ipc.resolve` do not work until primals self-register
(only 3 of 12 primals self-register today).

### Implementation

After spawning a primal and confirming health:

```rust
let payload = json!({
    "jsonrpc": "2.0",
    "method": "ipc.register",
    "params": {
        "primal_id": primal_name,
        "capabilities": capability_list,
        "endpoint": format!("unix://{}", socket_path),
    },
    "id": 1,
});
// Send to Songbird socket
```

Capability lists per primal are defined in the spec `DESKTOP_NUCLEUS_DEPLOYMENT.md`.

**Optimization**: Before registering, check `ipc.resolve` for the primal's
primary capability. If it resolves to the correct socket, skip registration
(the primal self-registered).

---

## Ask 3: petalTongue Live Mode Handling (P1)

### What

petalTongue in `live` mode needs special treatment:
- Do **not** use `setsid` (GUI needs the controlling terminal's display)
- Set `DISPLAY` env var (default `:1` or inherited)
- Pass `live` subcommand instead of `server`
- Set `AWAKENING_ENABLED=false`

### CLI Flag

```
biomeos nucleus --mode desktop --petaltongue-live   (default: true)
biomeos nucleus --mode desktop --no-petaltongue     (headless)
```

### Implementation

In `build_primal_command_with()` for petalTongue, check `--petaltongue-live`:
- If true: subcommand = `live`, no setsid, inherit DISPLAY
- If false: subcommand = `server`, normal setsid

---

## Ask 4: Family Seed Persistence (P1)

### What

biomeOS should persist the family seed to `{SOCKET_DIR}/.family.seed` (mode
0600) on first startup, and read it back on subsequent startups.

### Why

This allows `stop` + `start` without losing the cryptographic identity.
The `detect_ecosystem` codepath already detects pre-existing sockets — it
should also detect and reuse an existing family seed.

### Implementation

```rust
let seed_path = socket_dir.join(".family.seed");
let family_seed = if let Ok(existing) = fs::read_to_string(&seed_path) {
    existing.trim().to_string()
} else {
    let new_seed = generate_random_hex(32);
    fs::write(&seed_path, &new_seed)?;
    fs::set_permissions(&seed_path, Permissions::from_mode(0o600))?;
    new_seed
};
```

---

## Ask 5: Capability Domain Symlinks (P2)

### What

Create symbolic links in the socket directory for capability-based filesystem
discovery. These are the fallback path when Songbird is unavailable.

### Implementation

After all primals are healthy, create symlinks:

```
security-{family}.sock -> beardog-{family}.sock
crypto-{family}.sock   -> beardog-{family}.sock
compute-{family}.sock  -> toadstool-{family}.sock
tensor-{family}.sock   -> barracuda-{family}.sock
...
```

Full mapping in `DESKTOP_NUCLEUS_DEPLOYMENT.md`.

---

## Ask 6: Application Session API (P2 — Future)

### What

New Neural API methods for application lifecycle management:

| Method | Description |
|--------|-------------|
| `app.launch` | Deploy graph + create petalTongue session + start continuous loop |
| `app.list` | List running application sessions |
| `app.suspend` | Pause a session's tick loop |
| `app.resume` | Resume a paused session |
| `app.terminate` | Stop session, flush provenance, cleanup |
| `app.focus` | Set which session receives sensor input |
| `app.info` | Detailed session telemetry |

These methods compose existing biomeOS capabilities:
- `graph.deploy` / `graph.execute` for graph lifecycle
- `graph.start_continuous` / `pause` / `resume` / `stop` for tick loops
- petalTongue `visualization.session.create/destroy` for display surfaces

The full API spec is in `DESKTOP_SESSION_MODEL.md`.

### Implementation Path

1. Add `app` namespace to `ROUTE_TABLE` in `neural_api_server/routing.rs`
2. Create `handlers/app/mod.rs` with session state management
3. Bind sessions to `ContinuousSession` + petalTongue session IDs
4. Application graphs discovered from `graphs/desktop/` directory

---

## Validation

primalSpring will validate the biomeOS Desktop mode evolution through:

- `desktop_nucleus.sh validate` — extended with biomeOS-native path checks
- exp085 (`agentic_loop_substrate`) — full three-way loop via biomeOS
- Composition health endpoints (`composition.desktop_health`)
- Graph template compatibility (`nucleus_desktop_cell.toml`)

---

## Timeline Suggestion

| Priority | Ask | Effort Estimate |
|----------|-----|----------------|
| P0 | `NucleusMode::Desktop` (12 primals) | Medium — extend existing `primals()` + profiles |
| P0 | Songbird registration loop | Small — one loop after health wait |
| P1 | petalTongue live handling | Small — conditional subcommand + env |
| P1 | Family seed persistence | Small — file read/write |
| P2 | Capability symlinks | Small — loop + symlink creation |
| P2 | Application session API | Large — new handler module + session state |
