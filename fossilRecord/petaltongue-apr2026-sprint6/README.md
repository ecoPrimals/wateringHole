# petalTongue Sprint 6 Fossil Record

Archived April 12, 2026 during deep debt sprint.

## Contents

| File | Origin | Reason |
|------|--------|--------|
| `headless_main.rs` | `crates/petal-tongue-ui/src/headless_main.rs` | Orphan: not in module tree, not a `[[bin]]` target. Functionality superseded by root UniBin `petaltongue headless` subcommand and `petal-tongue-headless` crate. |
| `petal-tongue-ui-main.rs` | `crates/petal-tongue-ui/src/main.rs` | Duplicate CLI: alternate `petal-tongue` binary overlapping the official `petaltongue` UniBin. Not a declared `[[bin]]` target in workspace Cargo.toml. |
