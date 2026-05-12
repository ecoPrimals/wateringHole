# Nest Atomic Readiness — Handoff for nestgate + toadstool teams

**Date**: 2026-03-21  
**From**: primalSpring v0.5.0  
**To**: nestgate team, toadstool team  
**Status**: Tower Fully Utilized (41/41) — Ready for Nest Atomic

## Context

primalSpring has validated Tower Atomic at full utilization. All 41 gates pass,
all 19 integration tests run in parallel (~1 second), all 4 new experiments pass.
Tower is stable and ready to serve as the foundation for Nest Atomic.

## What nestgate Needs to Provide

For Nest Atomic integration, nestgate needs:

1. **UniBin binary** in `plasmidBin/primals/nestgate` that supports:
   - `server` subcommand with `--socket <path>` for Unix socket IPC
   - `health.liveness` JSON-RPC method
   - `capabilities.list` JSON-RPC method
   - Storage capability methods (TBD: `storage.put`, `storage.get`, `storage.list`, etc.)

2. **biomeOS integration**: Socket path following `biomeos/nestgate-{family_id}.sock` convention

3. **Capability registration**: Either self-register with Neural API via `capability.register`
   or have translations added to `biomeOS/config/capability_registry.toml`

## What toadstool Needs to Provide

For Node Atomic (after Nest is stable):

1. **UniBin binary** in `plasmidBin/primals/toadstool` with same standard IPC interface
2. **Compute capability methods** (TBD: `compute.execute`, `compute.status`, etc.)

## What primalSpring Has Ready

- **Harness support**: `AtomicHarness` can already spawn any primal with a `plasmidBin` binary
- **Launch profile**: Add a `[profiles.nestgate]` section to `primal_launch_profiles.toml`
  (already has a placeholder)
- **Socket nucleation**: Deterministic socket path assignment for nestgate
- **Test infrastructure**: Integration test pattern established (see `tower_*` tests)
- **Deploy graph**: Will create `nest_atomic_bootstrap.toml` once nestgate binary is available
- **Gate framework**: Will define storage gates (Gate 12+) for Nest Atomic

## Key Patterns to Follow

### Socket Discovery
- Use `NESTGATE_SOCKET` env var OR `XDG_RUNTIME_DIR/biomeos/nestgate-{family_id}.sock`
- Primals discover each other via socket paths, not hardcoded addresses

### Health Standard
- `health.liveness` must return `{"status": "healthy"}` within 5 seconds
- `capabilities.list` must return a JSON array of capability strings

### IPC Protocol
- JSON-RPC 2.0 over Unix socket, newline-delimited
- Methods: `health.liveness`, `capabilities.list`, plus domain-specific methods

### Ephemeral Ports
- If nestgate binds TCP, support `--port 0` for test isolation (songbird pattern)
- Or skip TCP entirely for IPC-only mode

## What We Learned That's Relevant

1. **Socket path length**: Keep family IDs short. `SUN_LEN` limit (108 chars on Linux)
   causes failures with long paths like `/tmp/primalspring-harness-exp063-rendezvous-123456/biomeos/...`
2. **Port contention**: If your primal binds TCP, support ephemeral ports for parallel testing
3. **petalTongue integration**: `PETALTONGUE_SOCKET` env var, not `--socket` flag
4. **BirdSong API**: `generate_encrypted_beacon` requires `node_id` field, `decrypt_beacon`
   expects `encrypted_beacon` as a string (not a JSON object)
5. **Grammar of Graphics**: PascalCase enums (`Cartesian`, `Bar`, `X`, `Y`)
6. **Federation stubs**: songbird's `federation.peers` and `federation.status` are stubs
   returning empty results — wire to actual federation when ready

## Timeline

1. nestgate provides UniBin binary → primalSpring creates Nest Atomic tests
2. Nest Atomic gates defined and validated
3. toadstool provides UniBin binary → primalSpring creates Node Atomic tests
4. Node Atomic gates defined and validated
5. Full NUCLEUS composition validated
