<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 91: Coverage Expansion + Modernization Audit

**Date**: May 4–5, 2026
**From**: coralReef team
**To**: primalSpring, all downstream springs

---

## Summary

Coverage expansion for previously-untested `capture.rs` module. Zero-alloc performance evolution on hot paths. Full modernization audit confirms codebase is fully evolved to modern idiomatic Rust with zero remaining debt patterns. primalSpring Phase 59 audit: port 9730 confirmed, no new debt.

## Coverage Expansion

### coral-glowplug `capture.rs` (7 new tests)

`TrainingRecipe` load/save/flat_writes previously had zero test coverage. Added:
- `training_recipe_roundtrip_json` — full JSON serialize/deserialize cycle
- `training_recipe_load_nonexistent_returns_error` — typed `TrainingRecipeError::Read`
- `training_recipe_load_invalid_json_returns_parse_error` — typed `TrainingRecipeError::Parse`
- `flat_writes_aggregates_all_domains` — verifies multi-domain flattening
- `flat_writes_empty_recipe` — empty recipe edge case
- `training_dir_env_override` — environment variable resolution
- `recipe_path_for_chip_formats_correctly` — chip-to-path formatting

## Zero-Alloc Performance Evolution (May 5)

| Change | Location | Impact |
|--------|----------|--------|
| `aperture_name: String` → `Cow<'static, str>` | `mmu_oracle/capture.rs` | Eliminates heap alloc per PDE/PTE decode |
| `format!("{req}\n")` → `write_rpc_line()` | `coral-glowplug/ember.rs` | Eliminates 7 String allocs per JSON-RPC session |
| `Vec::with_capacity(n)` | `diff_snapshots`, `device_open` | Pre-sizes known-bound vectors |

## Modernization Audit (All Clear)

| Pattern | Status |
|---------|--------|
| `async_trait` | Zero (native async traits since Rust 1.75) |
| `lazy_static` | Zero (`OnceLock`/`LazyLock` everywhere) |
| `Box<dyn Error>` in production | Zero (typed `thiserror` errors) |
| `Result<_, String>` in lib code | Zero (only `coral_probe.rs` binary tool) |
| `#[allow(dead_code)]` without reason | Zero (all use `#[expect(dead_code, reason = "...")]`) |
| `.clone()` hotspots | All in SSA compiler IR passes — necessary and idiomatic |
| `Arc<Mutex<>>` | 4 instances in coral-glowplug — correct (short critical sections, no `.await` under lock) |
| Hardcoded paths | All have env var overrides |
| Mocks in production | Zero (all `#[cfg(test)]`-gated) |
| `unsafe` leakage | Zero outside `coral-driver` |
| TODO/FIXME/HACK/DEBT | Zero in `.rs` code |

## Test Results

- **4686 passing**, 0 failures, 160 ignored (hardware-gated)
- Zero clippy warnings (pedantic + nursery)
- Zero fmt drift

## primalSpring Phase 58 Items — Status

| Item | Priority | Status |
|------|----------|--------|
| Phase 3 AEAD transport | HIGH | **Verified** (Iter 90: integration test proves full encrypted frame loop reachable) |
| Coverage ~65% → 90% | MEDIUM | In progress — ceiling limited by hardware-gated paths (~82% non-hardware) |
| `coral-gpu` sovereign path | LOW | In progress — not blocking compositions |

## Downstream Impact

- No API changes
- No breaking changes
- Test count increment from 4634 → 4686
