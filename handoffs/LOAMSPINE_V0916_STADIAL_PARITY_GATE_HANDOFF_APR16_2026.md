<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# LoamSpine v0.9.16 — Stadial Parity Gate Compliance

**Date**: April 16, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Previous handoff**: `LOAMSPINE_V0916_CRYPTO_WIRE_ADAPTER_HANDOFF_APR16_2026.md` (archived)

---

## What

**Stadial parity gate compliance** for loamSpine: remove blocked storage backends and dependency ghosts, upgrade DNS resolver stack, and verify policy (`cargo deny`), `dyn` audit, and test/quality metrics.

---

## Removed

| Area | Scope |
|------|--------|
| **sled** storage backend | ~500 lines production + ~891 lines test |
| **SQLite / rusqlite** storage backend | ~646 lines production + ~682 lines test |

---

## Upgraded

- **hickory-resolver** `0.24` → `0.26` (drops `async-trait` from **hickory-proto** in this path).

---

## Lockfile ghosts eliminated

`sled`, `libsqlite3-sys`, `rusqlite`, `instant`, `fxhash` removed from the dependency graph for this workspace.

---

## Remaining upstream (outside our control)

- **`async-trait`** still appears transitively via **hickory-net** `0.26` (not authored in loamSpine).
- **`ring`** only under optional features (not default production path).

---

## Policy & audits

- **`cargo deny check`**: **bans** and **advisories** both **PASS**.
- **`dyn` audit**: **72** total — **28** doc/comment, **37** `Pin<Box<dyn Future>>` (object safety), **7** `Arc<dyn>` finite-implementor. **Non-blocking.**

---

## Metrics

| Metric | Value |
|--------|--------|
| Tests | **1,442** |
| Rust source files | **178** |
| `clippy` warnings | **0** |
| `#[async_trait]` attributes in our code | **0** |
| Rust edition | **2024** |

---

## Status

**loamSpine clears the stadial gate** for **`sled`** and **`libsqlite3-sys`**. Transitive **`async-trait`** via **hickory-net** is **not under our control**; tracked as upstream-only.

---

*Previous handoffs archived in `handoffs/archive/LOAMSPINE_V0916_*`*

---

**License**: AGPL-3.0-or-later
