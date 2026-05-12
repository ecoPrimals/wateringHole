<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Iteration 66 — hotSpring Firmware Wiring + Coverage Push

**Date**: March 25, 2026
**Phase**: 10+ (Iter 66)
**Tests**: 4047 passing, 0 failed, ~121 ignored (hardware-gated)
**Coverage**: ~66% workspace line coverage (llvm-cov)

---

## Summary

Wired the mailbox/ring firmware probing systems into coral-glowplug and
coral-ember per hotSpring's GPU interaction model. Posted-command mailboxes
enable firmware engine interaction (FECS, GPCCS, SEC2, PMU). Multi-ring
buffers provide ordered, timed, fence-based GPU command submission. Ember
persists ring/mailbox metadata across glowplug restarts. coralctl gained
firmware subcommands for CLI-driven hardware probing. Coverage push added
91 new tests across codegen, ember, and glowplug.

## What Changed

### coral-glowplug — Mailbox System

- `MailboxSet` + `PostedCommand` + `Sequence` in `mailbox.rs`
- Per-engine mailboxes (FECS, GPCCS, SEC2, PMU) with configurable capacity
- `Sequence::from_raw()` constructor for JSON-RPC deserialization
- `DeviceSlot.mailboxes: MailboxSet` — per-device mailbox management
- JSON-RPC methods: `mailbox.create`, `mailbox.post`, `mailbox.poll`,
  `mailbox.complete`, `mailbox.drain`, `mailbox.stats`

### coral-glowplug — Multi-Ring System

- `MultiRing` + `Ring` + `RingPayload` in `ring.rs`
- Per-device ring buffers with fence-value tracking
- `DeviceSlot.rings: MultiRing` — per-device ring management
- JSON-RPC methods: `ring.create`, `ring.submit`, `ring.consume`,
  `ring.fence`, `ring.peek`, `ring.stats`

### coral-glowplug — RPC Handler Module

- `socket/handlers/mailbox_ring.rs` — dispatch function routing all
  `mailbox.*` and `ring.*` methods to `DeviceSlot` operations
- Helper functions: `find_device_mut`, `require_bdf`, `require_str`, `require_u64`
- 10 unit tests covering create, post, poll, submit, consume, fence, stats

### coral-ember — Ring-Keeper

- `RingMeta`, `MailboxMeta`, `RingMetaEntry` structs in `hold.rs`
  (serde-derived for JSON-RPC transport)
- `HeldDevice.ring_meta: RingMeta` — persistent metadata alongside VFIO fds
- JSON-RPC methods: `ember.ring_meta.get`, `ember.ring_meta.set`
- Monotonic version field for consistency checking
- All `HeldDevice` initializers updated (ipc.rs, swap.rs, tests)

### coralctl — Firmware Subcommands

- `handlers_firmware.rs` — RPC client functions for all mailbox/ring operations
- `MailboxPostParams` struct (clippy `too_many_arguments` compliance)
- CLI subcommands: `coralctl mailbox {create,post,poll,drain,stats}`,
  `coralctl ring {create,submit,consume,fence,peek,stats}`
- Hex-or-decimal parsing for register addresses/values

### Coverage Push

- `codegen/debug.rs`: 7 new tests (debug flags, env parsing)
- `codegen/ir/op_float/mod.rs`: 12 new tests (FP16 DisplayOp for
  OpHSet2, OpHSetP2, OpHMul2 dnz, OpHAdd2 ftz, OpHFma2 ftz+sat,
  OpHMnMx2 ftz, ImmaSize, HmmaSize)
- `ember/hold.rs`: 2 new tests (RingMeta default, serde roundtrip)
- `mailbox_ring.rs`: 10 new handler tests

### Quality Gates

- `cargo clippy --workspace --all-features -- -D warnings`: PASS (0 warnings)
- `cargo fmt --check`: PASS
- `cargo test --workspace`: 4047 passing, 0 failed
- All files under 1000 LOC

## hotSpring Integration Points

### For hotSpring GPU Firmware Probing

hotSpring can now interact with GPU engines via glowPlug's JSON-RPC socket:

1. **Create a mailbox**: `mailbox.create { bdf, engine: "fecs", capacity: 16 }`
2. **Post a command**: `mailbox.post { bdf, engine: "fecs", method: 0x10, data: 0x01, sub: 0, param: 0 }`
3. **Poll completion**: `mailbox.poll { bdf, engine: "fecs", seq: <returned_sequence> }`
4. **Complete (test/sim)**: `mailbox.complete { bdf, engine: "fecs", seq: <seq>, result: 0 }`

### For Ordered GPU Dispatch Testing

1. **Create a ring**: `ring.create { bdf, name: "gpfifo", capacity: 64 }`
2. **Submit entries**: `ring.submit { bdf, name: "gpfifo", data: [...], fence: 1 }`
3. **Consume by fence**: `ring.fence { bdf, name: "gpfifo", fence_value: 1 }`

### Restart Persistence

Ember preserves ring/mailbox configuration via `RingMeta`:

- Before glowplug shutdown: `ember.ring_meta.set { bdf, meta: { mailboxes: [...], rings: [...], version: N } }`
- After glowplug restart: `ember.ring_meta.get { bdf }` → reconstruct `MailboxSet` + `MultiRing`

## What's Next

- **Coverage 66% → 90%**: Largest gap remains coral-reef codegen (SM20 ALU,
  SM50/70 control, tex/surface ops, instruction latencies). These are complex
  compiler internals needing shader-level test cases.
- **Hardware validation**: Run mailbox/ring against live Titan V VFIO devices
  once hotSpring completes FECS/GPCCS warm boot.
- **Ring persistence E2E**: Validate full glowplug crash → ember restore →
  glowplug reconnect cycle with active rings.
- **Multi-ring dispatch**: Exercise concurrent rings (gpfifo + ce0) for
  overlapped compute + copy engine testing.

## Files Changed

| File | Change |
|------|--------|
| `crates/coral-glowplug/src/device/mod.rs` | Added `mailboxes`, `rings` fields to `DeviceSlot` |
| `crates/coral-glowplug/src/mailbox.rs` | Added `Sequence::from_raw()` |
| `crates/coral-glowplug/src/socket/handlers/mailbox_ring.rs` | New — RPC dispatch + tests |
| `crates/coral-glowplug/src/socket/handlers/mod.rs` | Registered `mailbox_ring` module |
| `crates/coral-glowplug/src/socket/mod.rs` | Route `mailbox.*`/`ring.*` methods + doc table |
| `crates/coral-glowplug/src/bin/coralctl/handlers_firmware.rs` | New — CLI RPC functions |
| `crates/coral-glowplug/src/bin/coralctl/main.rs` | Added `Mailbox`/`Ring` subcommands |
| `crates/coral-ember/src/hold.rs` | `RingMeta`, `MailboxMeta`, `RingMetaEntry` |
| `crates/coral-ember/src/lib.rs` | Re-exported new types |
| `crates/coral-ember/src/ipc.rs` | `ring_meta` init + get/set handlers |
| `crates/coral-ember/src/swap.rs` | `ring_meta` init |
| `crates/coral-ember/tests/ipc_dispatch.rs` | Updated `HeldDevice` inits |
| `crates/coral-reef/src/codegen/debug.rs` | 7 new tests |
| `crates/coral-reef/src/codegen/ir/op_float/mod.rs` | 12 new tests |
