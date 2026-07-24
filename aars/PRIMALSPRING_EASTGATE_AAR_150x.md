# primalSpring eastGate AAR — Wave 150x

**Date**: July 24, 2026 | **Wave**: 150x | **From**: eastGate (10.13.37.5)
**Scope**: Dimensional review integration, Tower hardening scenarios, operator services, shadow deploy

---

## What Happened

eastGate integrated Wave 150x dimensional review findings into primalSpring. 14 new
stress/pen scenarios from the 4-team convergence sprint were staged, clippy-swept,
and committed. Operator services (tower.shadow timer, biomeos-beacon) were fixed and
activated. songBird binary rebuilt with `benchmark` subcommand. Shadow metrics now
collecting continuously from eastGate.

### Code Evolution — 14 Stress/Pen Scenarios

7 stress scenarios + 7 pen-test scenarios authored during the convergence sprint:

| Type | Scenarios |
|------|-----------|
| Stress | sustained-throughput, concurrent-dispatch, btsp-storm, failover-resilience, mesh-churn, uds-hop-cost, shadow-fidelity |
| Pen | malformed-rpc, enrollment-replay, capability-escalation, cipher-downgrade, uds-spoof, mesh-poison, relay-abuse |

30 known debt findings tracked across these scenarios. Teams evolve independently.

### Clippy Fixes

- Tautological boolean `has_turn_port || true` in `s_tower_pen_relay_abuse` — removed dead logic
- 5 `doc_markdown` warnings: backtick-wrapped `PostPrimordial`, `ChaCha20`, `node_id`, `public_key`, `Ed25519`

### Operator Services Activated

| Service | Before | After |
|---------|--------|-------|
| `tower-shadow.timer` | Not installed | ACTIVE — 60min interval, collecting Tower vs WG metrics |
| `biomeos-beacon` | DEAD (status=203, 29,081 restarts) | ACTIVE — `StartLimitIntervalSec` moved to `[Unit]`, `WorkingDirectory` fixed |
| `songbird-federation` | Running old binary (no benchmark) | Running new binary with `benchmark` subcommand |

### songBird Binary Upgrade

Rebuilt songBird from source to get the `benchmark` subcommand (v0.2.1 in depot
lacked it — shipped by sporeGate/cellMembrane team in their build but not propagated
to eastGate depot). New binary installed at `~/.local/bin/songbird` and
`infra/plasmidBin/primals/x86_64-unknown-linux-musl/songbird`.

### Shadow Benchmark — First eastGate Results

Benchmark from eastGate to sporeGate LAN (192.168.4.244 → 192.168.4.3):

| Metric | Tower | WireGuard | Ratio |
|--------|-------|-----------|-------|
| Latency (avg) | 0.72ms | 0.62ms | 1.16x (WG) |
| Throughput | 6.49 Gbps | 4.16 Gbps | **1.56x (Tower)** |
| Setup time | 0.28ms | 0.31ms | 0.92x (Tower) |

Tower wins throughput decisively. Latency slightly higher at 196KB payload size
(consistent with known userspace overhead — closes with larger payloads).

### Topology Update

- `mesh_topology.toml`: added `lan_addr` for eastGate (192.168.4.244) and sporeGate (192.168.4.3)
- grapheneGate services updated to reflect Tower LIVE (beardog, songbird, skunkbat)

### KNOWN_DEBT Calibration

Recalibrated for eastGate environment:
- `graphenegate-readiness`: 14 → 1 (only aggregate check fails on non-depot gates)
- `arch-fitness`: removed (passes on eastGate x86_64)
- All stress/pen scenario debts confirmed accurate on eastGate

---

## By The Numbers

| Metric | Value |
|--------|-------|
| Scenarios | 196 (all PASS with known debt) |
| Tests | 1240 pass, 0 fail |
| Clippy warnings | 0 |
| Commits today | 5 |
| Lines changed | +5,651 / -20 |
| Shadow results collected | 8 (first timer run) + continuous |
| Services active | 3/3 (tower-shadow, biomeos-beacon, songbird-federation) |

---

## LAN Topology Verified

```
eastGate (192.168.4.244) ←→ sporeGate (192.168.4.3)
  ICMP: 0.15ms RTT (MikroTik, same switch)
  Tower benchmark: 0.72ms latency, 6.49 Gbps throughput
  WG overlay: 78ms RTT (routes through golgiBody VPS)
```

The LAN path is 500x faster than the WG overlay for these two gates.

---

### Deep Debt Sweep (July 24, evening)

Comprehensive deep debt audit + idiomatic Rust 2024 evolution:

| Target | Action |
|--------|--------|
| `context_discovery.rs` | `map_or(true,...)` → `is_none_or()` (Rust 2024 stabilized) |
| `soundstage/channel.rs` | `Anchor` clone per event → `Arc<Anchor>` (zero-alloc) |
| `evolution/mod.rs` | Exported `preferred_address()` for downstream LAN-first routing |
| `ipc/protocol.rs` | `Cow<'static, str>` for JSON-RPC version (zero-alloc) |
| `evolution/gate.rs` | `MeshEntry::preferred_address()` + `has_tower()` |
| `capability_registry.toml` | K-Derm trust tiers + 4 missing methods (resolved 15 debt) |
| Cargo.lock | 26 transitive deps refreshed (patch-level) |
| KNOWN_DEBT | Recalibrated: 9 entries / 17 expected (was 10/20) |

**Audit results** (all clear):
- Zero unsafe code (`#![forbid(unsafe_code)]` + workspace deny lint)
- Zero panics in production, zero `todo!()`/`unimplemented!()`
- Zero `#[allow(dead_code)]`, zero production mocks
- Zero hardcoded primal names (typed `Primal` enum, TOML-driven registries)
- All 14 direct deps pure Rust (zero C/FFI)
- Largest production file: 666 lines (`neural_routing.rs`)
- 17 typed `thiserror` error enums (no `Box<dyn Error>`)

## What's Next (eastGate team)

| Priority | Task | Status |
|----------|------|--------|
| P1 | Remaining 17 debt findings | Blocked — all require songBird/bearDog code |
| P1 | iperf3 server LIVE | DONE — port 5201, all interfaces |
| P2 | sporePrint primal pipeline | Queued (design phase) |
| P2 | CredentialStore squirrel integration | Queued |
| P3 | biomeOS chimera Phase 0 (library extraction) | Can start now |

---

## Blockers

None. P0 CLEAR. All operator tasks DONE. All eastGate-actionable debt burned.
Remaining 17 known debt findings are upstream primal team items (songBird/bearDog).

---

*Wave 150x eastGate AAR (updated): deep debt sweep complete — zero unsafe, zero mocks,
zero hardcode, idiomatic Rust 2024 patterns, Arc<Anchor> zero-clone, Cow<str> zero-alloc,
LAN-first routing, K-Derm trust tiers. 196 scenarios, 1239 tests, 0 warnings.
v0.9.46. P0 CLEAR.*
