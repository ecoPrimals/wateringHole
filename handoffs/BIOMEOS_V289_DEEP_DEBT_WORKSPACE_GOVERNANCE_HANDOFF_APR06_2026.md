<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# biomeOS v2.88–v2.89 — primalSpring Audit Response & Deep Debt / Workspace Governance

**Date:** April 6, 2026
**From:** biomeOS v2.87 → v2.89
**To:** All downstream primals and springs
**Status:** Complete — pushed to `master`

---

## Summary

biomeOS v2.88–v2.89 spans two evolution phases: **v2.88** addresses the primalSpring audit (test fixtures, license alignment, Rust toolchain, and workspace dependency centralization), and **v2.89** completes deep-debt workspace governance (minimal intentional local pins, UI crate metadata alignment, large-file refactors, targeted tests, and library `eprintln` verification) while holding all quality gates.

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| **v2.89** | Apr 6 | Workspace dep governance finalized (22→2 local pins); `biomeos-ui` workspace metadata aligned; `socket_providers.rs` 884→484, `protocol.rs` 878→448; targeted tests for 5 untested production files; library `eprintln` audit (3 acceptable); 7,607 tests, clippy/fmt PASS |
| **v2.88** | Apr 6 | primalSpring audit response — vm_federation TEST-NET fixes, AGPL-3.0-or-later + `rust-version` 1.87, ~150 local dep pins → `workspace = true` per `WORKSPACE_DEPENDENCY_STANDARD.md` |

---

## v2.88 — primalSpring Audit Response

### Test fixtures (vm_federation)

- Four `vm_federation` test failures fixed by replacing reserved **192.0.2.x** (TEST-NET) addresses with **192.168.x** private LAN ranges suitable for fixture networking.

### License and toolchain

- License migrated **AGPL-3.0-only → AGPL-3.0-or-later** across all `Cargo.toml` files per **scyBorg** standard.
- **`rust-version` 1.87** added at the workspace level and propagated to member crates.

### Workspace dependencies

- Approximately **150** local dependency pins migrated to **`workspace = true`** per **`WORKSPACE_DEPENDENCY_STANDARD.md`**.

---

## v2.89 — Deep Debt Evolution

### Workspace dependency governance

- Local version pins reduced from **22 → 2**, retaining only **intentional publishing** versions where required.

### `biomeos-ui` alignment

- Workspace metadata aligned: **version**, **authors**, **license**, **rust-version**, and **dependencies** consistent with the rest of the workspace.

### Large-file refactors

| File | Before | After |
|------|--------|-------|
| `socket_providers.rs` | 884 | 484 |
| `protocol.rs` | 878 | 448 |

### Tests and static checks

- Targeted test coverage added for **five** previously untested production files.
- **Library `eprintln` audit:** **three** occurrences reviewed and verified **acceptable** (see non-blocking notes for CLI pattern).
- **7,607** tests — **0** failures, **0** ignored; **`cargo clippy`** PASS; **`cargo fmt`** PASS.

---

## Quality Gates

| Gate | Target / result |
|------|-----------------|
| **TODO / FIXME / HACK / stubs** | **0** |
| **`unsafe` blocks** | **0** |
| **Deprecated APIs** | **0** |
| **Identity-based routing** | **0** — capability-compliant |
| **Coverage** | **90%+** |
| **Test suite** | Fully concurrent — **0** `#[serial]` / `serial_test`, **0** ignored |
| **Edition / Rust** | Edition **2024**, **`rust-version` 1.87** |
| **License** | **AGPL-3.0-or-later** |

---

## Remaining Non-Blocking Notes

- **Two crates** retain **local version pins** on purpose for publishing: **genomebin-v3** `3.0.0`, **genome-factory** `1.0.0`.
- **31 duplicate dependency roots** — mostly **transitive** splits (e.g. **linux-raw-sys**, **rustix**, **getrandom**, **rand** version lines).
- **149** `localhost` / **127.0.0.1** references in **non-test** code are **legitimate** configuration defaults and bind addresses.
- **`or_exit.rs`** uses **`eprintln`** for the **CLI fatal-exit** pattern — **intentional** and distinct from library logging policy.

---

## For Downstream Primals

1. **License** is **AGPL-3.0-or-later** workspace-wide; align crate metadata and compliance notices accordingly.
2. **Prefer `workspace = true`** for shared deps; only pin versions where publishing or policy explicitly requires it.
3. **Capability-based discovery** remains the routing model — no regression on identity-based paths in production.

---

## Verification

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features -q
```

---

*© 2025–2026 ecoPrimals — AGPL-3.0-or-later / CC-BY-SA-4.0 / ORC*
