# barraCuda v0.3.11 — ludoSpring V35 Gap Resolution

**Date:** March 30, 2026
**From:** barraCuda Sprint 23
**To:** ludoSpring, biomeOS, plasmidBin, primalSpring, esotericWebb
**Previous:** `LUDOSPRING_V35_PRIMAL_COMPOSITION_GAP_DISCOVERY_HANDOFF_MAR30_2026.md`
**Status:** P0 and P1 gaps resolved — barraCuda ready for composition experiments

---

## Summary

Resolves all barraCuda gaps identified by ludoSpring V35 primal composition
experiments (exp084, exp086). The binary is now composition-ready: UDS + TCP
dual transport, 30 JSON-RPC methods (up from 15), and proper ecosystem socket
path for biomeOS discovery.

---

## P0: Binary Ready for plasmidBin

### Socket path fixed
- `default_socket_path()` returns `$XDG_RUNTIME_DIR/biomeos/barracuda.sock`
  (was `barracuda-default.sock`)
- Matches `PRIMAL_IPC_PROTOCOL.md` discovery convention
- `BIOMEOS_FAMILY_ID` still supported for multi-family deployments (appends
  `-{family_id}` suffix when set to non-default value)

### Dual-transport startup
- `./barracuda server` → UDS only (local dev)
- `BARRACUDA_PORT=9010 ./barracuda server` → UDS + TCP:9010 (plasmidBin pattern)
- `./barracuda server --port 9010` → UDS + TCP:9010
- TCP spawns alongside UDS in the same process; both share the same primal

### Release binary
- 4.7MB stripped ELF x86-64
- Verified: `./barracuda version`, `./barracuda server --help`
- Ready for `harvest.sh` inclusion in next plasmidBin release

### plasmidBin integration
barraCuda is NOT yet in `ports.env`. Recommended addition:

```
BARRACUDA_PORT="${BARRACUDA_PORT:-9010}"
```

And in `port_for_primal()`:
```
barracuda)     echo "$BARRACUDA_PORT" ;;
```

---

## P1: 15 New IPC Methods (30 Total)

All methods follow `SEMANTIC_METHOD_NAMING_STANDARD.md` `{domain}.{operation}`
pattern with no primal prefix on the wire.

### Math & activation (CPU) — exp084 unblocked

| Method | Implementation | Notes |
|--------|---------------|-------|
| `math.sigmoid` | `barracuda::activations::sigmoid` batch | Numerically stable |
| `math.log2` | `f64::log2()` batch | Element-wise |
| `activation.fitts` | Fitts' law: `a + b * log2(2D/W)` | Configurable a, b |
| `activation.hick` | Hick's law: `a + b * log2(n+1)` | Configurable a, b |

### Statistics (CPU) — exp084 unblocked

| Method | Implementation |
|--------|---------------|
| `stats.mean` | `barracuda::stats::metrics::mean` |
| `stats.std_dev` | `barracuda::stats::correlation::std_dev` |
| `stats.weighted_mean` | Inline weighted average with validation |

### Noise & RNG (CPU) — exp084 unblocked

| Method | Implementation | Notes |
|--------|---------------|-------|
| `noise.perlin2d` | `barracuda::ops::procedural::perlin_noise::perlin_2d_cpu` | Pure f64 |
| `noise.perlin3d` | Z-axis interpolated 2D Perlin | Layered composition |
| `rng.uniform` | `barracuda::rng::uniform_f64_sequence` | Seedable, [min, max) |

### Tensor element-wise (GPU) — exp086 unblocked

| Method | GPU Op | Notes |
|--------|--------|-------|
| `tensor.add` | `Tensor::add` / `add_scalar` | Tensor-tensor or broadcast scalar |
| `tensor.scale` | `Tensor::mul_scalar` | Scalar multiply |
| `tensor.clamp` | `Clamp` WGSL shader | GPU-native clamp |
| `tensor.reduce` | CPU download + reduce | sum, mean, max, min |
| `tensor.sigmoid` | `Sigmoid` WGSL shader | GPU-native sigmoid |

### Capability discovery
- `capabilities.list` auto-advertises all 30 methods
- `discovery::capabilities()` derives domain list from `REGISTERED_METHODS`
- biomeOS can auto-discover barraCuda's full IPC surface without registration

---

## Deep Debt Resolution

### Lint migration complete
- Zero `#[allow(` remaining in both `barracuda` and `barracuda-core` crates
- All annotations use `#[expect(lint, reason = "...")]` or
  `#[cfg_attr(not(test), expect(...))]` for target-dependent dead code

### Audit results
- Zero TODO/FIXME/HACK in production code
- Zero `.unwrap()` in production code
- Zero production mocks (all test-isolated)
- `#![forbid(unsafe_code)]` in both main crates
- No files over 1000 lines
- ScyBorg triple license verified

---

## Quality Gates — All Green

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --all-features --all-targets -D warnings` | Pass (zero warnings) |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | Pass |
| `cargo deny check` | Pass (advisories, bans, licenses, sources) |
| `cargo test --all-features` | 3,808 pass, 0 fail |

---

## What ludoSpring Experiments Can Now Do

### exp084 (Math IPC) — all 12 methods now available
barraCuda serves `math.sigmoid`, `math.log2`, `stats.mean`, `stats.std_dev`,
`stats.weighted_mean`, `noise.perlin2d`, `noise.perlin3d`, `rng.uniform`,
`tensor.create`, `tensor.matmul`, `activation.fitts`, `activation.hick` over
JSON-RPC on UDS and TCP.

### exp086 (Tensor composition) — all 5 element-wise ops now available
`tensor.add`, `tensor.scale`, `tensor.clamp`, `tensor.reduce`,
`tensor.sigmoid` are wired through GPU WGSL ops. Each op is a composition
graph node consumable by biomeOS Neural API `by_capability` routing.

### exp087/088 (Neural API pipeline) — still blocked on biomeOS
barraCuda now exposes `capabilities.list` with all 30 methods, but
auto-discovery requires biomeOS to scan the socket directory. barraCuda's
responsibility is complete; biomeOS registration/discovery is the remaining
gap (see ludoSpring V35 Part 2).

---

## Remaining barraCuda Gaps (from V35)

| Gap | Status | Notes |
|-----|--------|-------|
| Not in plasmidBin release | **Binary ready** | Needs `harvest.sh` + `ports.env` entry |
| Math not on JSON-RPC | **Resolved** | 10 math/stats/noise/rng methods wired |
| Tensor ops missing from IPC | **Resolved** | 5 element-wise ops wired |
| Neural API registration | **barraCuda side done** | `capabilities.list` advertises all methods; biomeOS discovery is biomeOS's gap |

---

## Files Changed

### New files
- `crates/barracuda-core/src/ipc/methods/math.rs` — math, stats, noise, rng, activation handlers

### Modified files
- `crates/barracuda-core/src/ipc/methods/mod.rs` — 30 registered methods, updated dispatch
- `crates/barracuda-core/src/ipc/methods/tensor.rs` — 5 new tensor handlers
- `crates/barracuda-core/src/ipc/transport.rs` — socket path fix, `default_tcp_port()`
- `crates/barracuda-core/src/bin/barracuda.rs` — dual-transport startup, help text
- `crates/barracuda-core/src/ipc/methods_tests.rs` — updated method count assertion
- 14 files in `crates/barracuda/src/ops/` — `#[allow(` → `#[expect(` migration
- `crates/barracuda/src/device/driver_profile/workarounds.rs` — lint cleanup
- `crates/barracuda/examples/fhe_ntt_validation.rs` — lint cleanup
- `specs/BARRACUDA_SPECIFICATION.md` — updated IPC method table
- `specs/REMAINING_WORK.md` — new Sprint 23 achieved section
- `README.md` — updated metrics and sprint entry
