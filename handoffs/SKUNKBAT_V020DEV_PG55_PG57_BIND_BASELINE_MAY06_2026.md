# skunkBat v0.2.0-dev — PG-55 `--bind` + PG-57 Baseline Learning

**Date**: May 6, 2026
**Scope**: projectNUCLEUS Phase 2a penetration test gap resolution
**Build**: 345 tests passing, clippy clean, 44 source files (max 725 LOC)

---

## PG-55: `--bind` CLI Flag (HIGH → RESOLVED)

Added `--bind <host>` to the `server` subcommand per UniBin v1.1 pattern:

```
skunkbat server --bind 127.0.0.1 --port 9140
```

Precedence: `--bind` flag > `SKUNKBAT_LISTEN_ADDR` env > `0.0.0.0` default.

Enables localhost-only binding for hardened deployments where the pen test
flagged default `0.0.0.0` as exposing the JSON-RPC interface to all interfaces.

**Files**: `crates/skunk-bat-server/src/main.rs`

---

## PG-57: Baseline Learning (MEDIUM → RESOLVED)

The statistical profiler requires ≥10 observations before `is_established()`
returns `true`. Without a baseline, `detect_behavioral_anomalies()` returns
empty — explaining the 0 threats during the pen test.

### Solution

1. **`threats::baseline` module** — contains:
   - `normal_baseline()`: 12 representative inter-primal traffic observations
     (2–8 conn/s, 1–5 KB/s, ports 9140/UDS)
   - `pentest_attack_patterns()`: 7 malformed-payload + enumeration scenarios

2. **Auto-seeding at construction**: `ThreatDetector::new()` calls
   `profiler.seed_baseline(&baseline::normal_baseline())` so the behavioral
   detection gate is active from the first `detect()` call.

3. **`StatisticalProfiler::seed_baseline()`**: New public method to bulk-load
   observations into the rolling window.

### 7 Pen-Test Attack Patterns

| # | Pattern | Signature |
|---|---------|-----------|
| 1 | Port enumeration sweep | 150 conn/s, 20+ ports |
| 2 | Payload flood | 10 MB/s traffic volume |
| 3 | Malformed JSON-RPC burst | 500 conn/s, tiny payloads |
| 4 | Service enumeration | 45 conn/s, systematic port probing |
| 5 | Amplification attempt | 80 conn/s, 128 bytes volume |
| 6 | Slow-rate exhaustion | 25 conn/s sustained |
| 7 | Protocol confusion | 30 conn/s, non-standard ports |

Tests confirm ≥5/7 patterns trigger anomaly detection, and 0 false positives
on normal traffic.

**Files**:
- `crates/skunk-bat-core/src/threats/baseline.rs` (new)
- `crates/skunk-bat-core/src/threats/behavioral.rs` (seed_baseline method + tests)
- `crates/skunk-bat-core/src/threats/mod.rs` (auto-seed wiring)

---

## Incidental Fixes

- `examples/beardog_integration.rs` doc lint fix (backticks on `BearDog`)

---

## Remaining Gaps

- PG-55 is resolved for skunkBat. Other primals (Songbird HTTP, ToadStool,
  biomeOS, sweetGrass, petalTongue) still need their own `--bind` flags.
- Baseline learning is seeded with static observations. Future: runtime learning
  from actual traffic via `BaselineProfiler::update()` during operation.
- Thymic selection: still blocked on BearDog `lineage.list` full integration.

---

## Ecosystem Implications

- primalSpring can mark PG-55 (skunkBat) and PG-57 as RESOLVED
- No API changes — all additions are backward-compatible
- `baseline` module is `pub` for integration test use
