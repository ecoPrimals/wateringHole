# NestGate v4.7.0-dev — Automation Overstep Shedding & primalSpring Audit Resolution

**Date**: April 4, 2026  
**Primal**: NestGate (Storage / Permanence)  
**Session**: 21  
**Trigger**: primalSpring downstream audit  

---

## Audit Input (primalSpring)

```
Quality: Clippy CLEAN, fmt PASS, 6,607 tests (2 flaky — pass on retry)
Discovery: 192 refs / 22 files, env vars 32 refs / 9 files — near-compliant
Open gaps: NG-01 (metadata backend wiring — Low), NG-03 (data.* stubs — Low)
Overstep: nestgate-security (crypto, partially delegated), nestgate-automation (orchestration),
          nestgate-mcp (AI). nestgate-network deprecated, discovery_mechanism deleted.
Action: Next shedding targets: nestgate-automation → biomeOS, nestgate-mcp → Squirrel.
```

---

## Actions Taken

### 1. nestgate-automation — Overstep Shedding

**Finding**: ~3,900 lines, 21 `.rs` files, but **zero production imports** from any consumer crate.

| Consumer | Dep kind | Actual Rust imports | Action |
|----------|----------|---------------------|--------|
| `nestgate-zfs` | normal | 0 in `src/`, 1 test import (`PerformanceExpectation`) | **Dep removed**; type inlined in test |
| `nestgate-api` | normal | 0 | **Dep removed** |
| `fuzz` | normal | 0 | **Dep removed** |
| Root workspace | dev-dep | 0 | Remains for workspace compilation |

**Result**: Entire crate deprecated with `#![deprecated(since = "4.7.0")]`. Zero consumers remain.
The crate stays in the workspace for now (fossil record / future deletion).

### 2. nestgate-mcp — Confirmed Removed

Already removed in a prior session. No directory, no workspace member, no imports anywhere.
The audit's mention is stale — `nestgate-mcp` does not exist in the tree.

### 3. Discovery Compliance (192 refs / 22 files)

All primal-name references audited and categorized:

| Category | Count | Status |
|----------|-------|--------|
| Config-layer service descriptors (deprecated, capability-backed) | ~50 | Acceptable |
| Documentation/comments (explaining anti-patterns or philosophy) | ~30 | Acceptable |
| Tests/E2E scenarios | ~80 | Acceptable |
| Local IPC convention (`biomeos` dir, `BIOMEOS_SOCKET_DIR`) | ~30 | Acceptable (wateringHole standard) |
| **Hardcoded remote routing** | **0** | **Clean** |

No `NESTGATE_BEARDOG`, `SONGBIRD_HOST/PORT`, or `BEARDOG_URL` env vars exist.

### 4. NG-01 & NG-03 — Confirmed Resolved

- **NG-01**: `FileMetadataBackend` fully implemented with multi-tier resolution (etcetera → XDG → HOME → /var/lib)
- **NG-03**: Pool handlers return `StatusCode::NOT_IMPLEMENTED` directing to ZFS REST API

### 5. Test Count Discrepancy

Our suite reports **12,240 passed, 0 failures, 471 ignored** (total 12,711).
The audit's 6,607 likely reflects a `--lib` or feature-subset run. No issue on our side.

---

## Verification

```
cargo fmt --all -- --check    → PASS
cargo clippy --workspace --all-features -- -D warnings → PASS (0 warnings)
cargo test --workspace        → 12,240 passed, 0 failed, 471 ignored
```

---

## Files Modified

- `code/crates/nestgate-zfs/Cargo.toml` — removed `nestgate-automation` dependency
- `code/crates/nestgate-api/Cargo.toml` — removed `nestgate-automation` dependency
- `fuzz/Cargo.toml` — removed `nestgate-automation` dependency
- `code/crates/nestgate-automation/Cargo.toml` — description updated to DEPRECATED
- `code/crates/nestgate-automation/src/lib.rs` — `#![deprecated]` added with biomeOS delegation note
- `code/crates/nestgate-zfs/tests/unit_tests/heuristic_tests.rs` — `PerformanceExpectation` inlined
- `STATUS.md` — updated date, automation status, gap table
- `CHANGELOG.md` — Session 21 entry

---

## Remaining Overstep Status

| Crate | Status | Notes |
|-------|--------|-------|
| `nestgate-mcp` | **Removed** | Deleted in prior session; MCP → biomeOS |
| `nestgate-automation` | **Deprecated** | Zero consumers; awaits full deletion |
| `nestgate-network` | **Deprecated** | Network discovery → orchestration provider |
| `nestgate-security` | **Active (delegating)** | `CryptoDelegate` wired to capability provider; crate provides delegation layer |
| `nestgate-discovery` | **Active (clean)** | `discovery_mechanism` deleted; capability/primal discovery retained |
