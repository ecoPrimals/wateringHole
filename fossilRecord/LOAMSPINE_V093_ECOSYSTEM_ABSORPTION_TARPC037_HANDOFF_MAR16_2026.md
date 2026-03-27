<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- ScyBorg Provenance: crafted by human intent, assisted by AI -->

# LoamSpine V0.9.3 — Ecosystem Absorption & tarpc 0.37 Handoff

**Primal**: LoamSpine  
**Version**: 0.9.3  
**Date**: March 16, 2026  
**Phase**: Cross-Spring Absorption + Trio Alignment

---

## Summary

Following the V0.9.2 structured IPC session, this handoff covers full ecosystem absorption: tarpc 0.37 alignment, `DispatchOutcome<T>`, `OrExit<T>`, IPC convenience methods, NDJSON `StreamItem`, and `deny.toml` evolution.

---

## Changes Made

### 1. tarpc 0.34 → 0.37

Bumped across three sessions (0.34 → 0.35 → 0.37). Now aligned with biomeOS V2.47, rhizoCrypt 0.13.0-dev, and sweetGrass 0.7.18. No API breakage.

### 2. `DispatchOutcome<T>` (rhizoCrypt alignment)

New typed dispatch result in `loam-spine-core::error`:

```
DispatchOutcome::Ok(T)
DispatchOutcome::ApplicationError { code: i64, message: String }
DispatchOutcome::ProtocolError(LoamSpineError)
```

Methods: `is_ok()`, `is_application_error()`, `into_result()`.

Separates JSON-RPC application errors from transport/protocol failures, enabling smarter retry and observability.

### 3. `OrExit<T>` Trait (wetSpring V123 alignment)

Zero-panic startup validation:
- `Result<T, E>.or_exit("context")` → prints `fatal: context: error` and exits
- `Option<T>.or_exit("context")` → prints `fatal: context` and exits

### 4. IPC Convenience Methods

- `extract_rpc_error(&response) -> Option<(i64, String)>` — centralized JSON-RPC error extraction
- `LoamSpineError::is_method_not_found()` — detects JSON-RPC -32601

`neural_api.rs` transport refactored to use `extract_rpc_error()` instead of inline pattern.

### 5. NDJSON `StreamItem` (rhizoCrypt/sweetGrass alignment)

New `streaming.rs` module with:

```
StreamItem::Data { payload }
StreamItem::Progress { processed, total }
StreamItem::End
StreamItem::Error { message, recoverable }
```

Methods: `data()`, `end()`, `progress()`, `error()`, `fatal()`, `to_ndjson_line()`, `parse_ndjson_line()`, `is_end()`, `is_fatal()`.

### 6. `deny.toml` Evolution

- `wildcards = "allow"` → `"warn"` (ecosystem standard)
- Added advisory ignores for tarpc 0.37 transitive deps (RUSTSEC-2024-0384, -2025-0057, -2025-0141, -2026-0007)
- Banned `aws-lc-sys`, `zstd-sys`, `lz4-sys`, `libsqlite3-sys` (ecoBin)

---

## Metrics

| Metric | V0.9.2 | V0.9.3 |
|--------|--------|--------|
| Tests | 1,190 | 1,206 |
| Coverage (function) | 91.01% | 91.03% |
| Coverage (line) | 88.84% | 88.91% |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| tarpc | 0.35 | 0.37 |
| Source files | 121 | 122 |
| New types | IpcPhase, Ipc | +DispatchOutcome, OrExit, StreamItem |

---

## Ecosystem Alignment Matrix

| Pattern | Source | Status |
|---------|--------|--------|
| `IpcErrorPhase` / `IpcPhase` | rhizoCrypt, healthSpring | V0.9.2 |
| `DispatchOutcome<T>` | rhizoCrypt, airSpring | **V0.9.3** |
| `OrExit<T>` | wetSpring V123, rhizoCrypt | **V0.9.3** |
| `extract_rpc_error()` | rhizoCrypt | **V0.9.3** |
| `StreamItem` NDJSON | rhizoCrypt, sweetGrass | **V0.9.3** |
| `socket_env_var()` | sweetGrass V0.7.17 | V0.9.2 |
| tarpc 0.37 | biomeOS, rhizoCrypt, sweetGrass | **V0.9.3** |
| `deny.toml wildcards=warn` | groundSpring, wetSpring | **V0.9.3** |
| `#[expect(reason)]` | ecosystem standard | V0.9.2 (16 migrated) |
| `provenance-trio-types` v0.1.1 | ecosystem | V0.9.2 |
| `capabilities` key in response | neuralSpring S156 | V0.9.2 |

---

## What Remains for V0.9.4+

1. **Wire `DispatchOutcome`** into JSON-RPC dispatch (currently defined but not yet used in `jsonrpc/mod.rs`)
2. **Wire `OrExit`** into `main.rs` startup validation
3. **Wire `StreamItem`** into provenance trio pipeline coordination
4. **Certificate activity type alignment** with sweetGrass (`CertificateMint`/`Transfer`/`Loan`/`Return`)
5. **`LoamSpineClient` trait** matching sweetGrass `anchor()`/`verify()`/`get_anchors()`
6. **Storage backend error-path coverage** for line coverage lift
7. **Cross-primal e2e tests** — rhizoCrypt ↔ loamSpine ↔ sweetGrass trio integration
