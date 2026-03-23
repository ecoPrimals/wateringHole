<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- ScyBorg Provenance: crafted by human intent, assisted by AI -->

# LoamSpine V0.9.5 — DispatchOutcome Wiring, Streaming Sync & Zero-Copy Evolution Handoff

**Primal**: LoamSpine  
**Version**: 0.9.5  
**Date**: March 17, 2026  
**Phase**: Deep Debt Resolution + Idiomatic Evolution + Ecosystem Pattern Wiring

---

## Summary

Following V0.9.4 (Pathway Learner metadata, manifest discovery, proptest, NeuralAPI IPC evolution), this session wires the V0.9.3 types (`DispatchOutcome`, `StreamItem`, `OrExit`) into production code paths, eliminates zero-copy debt in the sync module, smart-refactors `lifecycle.rs`, and expands storage error-path coverage.

---

## Changes Made

### 1. DispatchOutcome Wired into JSON-RPC Server

- `dispatch_typed` method on `LoamSpineJsonRpc`: wraps `dispatch()`, classifies `JsonRpcError` into `ProtocolError` (parse, method-not-found, invalid params) vs `ApplicationError` (domain errors with original code)
- `outcome_to_response` helper: maps `DispatchOutcome` variants back to JSON-RPC wire format
- `handle_request` updated to use `dispatch_typed` → `outcome_to_response` pipeline
- Ecosystem consistency with rhizoCrypt/airSpring dispatch patterns

### 2. StreamItem Wired into Sync Module

- `push_entries_streaming`: emits `Data`/`Progress`/`End`/`Error` stream items via `tokio::sync::mpsc::Sender<StreamItem>` during push operations
- `pull_entries_streaming`: same pattern for pull operations
- Doc comments use fully qualified paths (`crate::streaming::StreamItem::Progress`) for Rustdoc resolution

### 3. OrExit Tracing Evolution

- `eprintln!` in `OrExit` trait implementations (both `Result` and `Option`) replaced with `tracing::error!`
- Structured logging consistency — error context preserved in tracing spans

### 4. Zero-Copy Sync Evolution

- `pull_from_peer`: `entries_json.clone()` eliminated → `serde_json::Value::remove()` for ownership transfer from parsed JSON response
- `push_entries`: clone eliminated via try-then-own pattern — attempts network push with reference, takes ownership of entries vector only on failure for pending queue

### 5. Smart Refactor: lifecycle.rs

- `lifecycle.rs` (888 lines) → `lifecycle.rs` (442) + `lifecycle_tests.rs` (444)
- Test extraction uses `#[path = "lifecycle_tests.rs"]` pattern, consistent with `certificate.rs`

### 6. Storage Error-Path Coverage

4 new sled tests:
- `sled_list_spines_with_malformed_keys_skips_invalid`: non-16-byte keys skipped
- `sled_list_certificates_with_malformed_keys_skips_invalid`: non-16-byte keys skipped
- `sled_entry_index_missing_entry_skipped`: index→missing entry handled
- `sled_get_entries_for_spine_corrupted_entry_in_index`: corrupted bytes → error

### 7. Lint Refinement

- Removed unfulfilled `clippy::expect_used` and `clippy::panic` expectations from `jsonrpc/mod.rs`, `sync/mod.rs`, and `certificate.rs` test modules
- Only genuinely triggered lints retained in `#[expect]` attributes

---

## Metrics

| Metric | V0.9.4 | V0.9.5 |
|--------|--------|--------|
| Tests | 1,221 | 1,226 |
| Coverage (function) | 90.89% | 90%+ (TBD — storage error-path additions) |
| Coverage (line) | 88.74% | 88%+ (TBD) |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Source files | 123 | 125 |
| Max file size | 955 | 955 |
| Unsafe in production | 0 | 0 |

---

## Ecosystem Alignment

| Pattern | Source | Status |
|---------|--------|--------|
| `DispatchOutcome` wired | rhizoCrypt, airSpring | **V0.9.5** |
| `StreamItem` wired | rhizoCrypt, sweetGrass NDJSON | **V0.9.5** |
| `OrExit` → `tracing::error!` | Ecosystem tracing standard | **V0.9.5** |
| Zero-copy sync | Ecosystem zero-copy patterns | **V0.9.5** |
| Smart refactor `#[path]` | loamSpine certificate.rs | **V0.9.5** |
| `#[expect]` refinement | Ecosystem lint hygiene | **V0.9.5** |

---

## What Remains for V0.9.6+

1. **90%+ line coverage** — Continue storage backend error-path tests (redb, sqlite, cli_signer)
2. **Signing capability middleware** — Signature verification on RPC layer (capability-discovered)
3. **Showcase demos** — Expand from ~10% to full coverage
4. **Collision layer validation** — neuralSpring experiments (Python baseline)
5. **ChaosEngine** integration (rhizoCrypt, beardog patterns)
6. **ValidationHarness** for `loamspine doctor` subcommand
7. **LoamSpineClient trait** matching sweetGrass `anchor()`/`verify()`/`get_anchors()`
