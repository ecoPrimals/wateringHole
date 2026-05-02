# Squirrel v0.1.0 — Deep Debt: Marketplace & Distribution Honesty

**Date**: April 30, 2026
**Session**: AS
**Status**: RESOLVED

## Scope

Comprehensive deep debt audit covering all production code. Identified and
resolved remaining lying stubs in marketplace, distribution, and ecosystem
manager.

## Audit Results (clean)

- **0 unsafe** in production code
- **0 panic!** in production code
- **0 .unwrap()** in production code
- **0 todo!()** / **0 unimplemented!()** anywhere
- **0 stale TODO/FIXME/HACK comments** in production
- **1 production file** over 800 lines (`tarpc_server.rs` at 817L — delegation layer, appropriate)
- **No scripts, Dockerfiles, or non-Rust debris**
- **Dependencies**: 47 external, all current; dual versions (`tokio-serde`, `thiserror`, `tower`) are unavoidable tarpc transitives
- **Hardcoded names**: Only in intentional registries (`primal_names.rs`) and documentation; runtime uses capability-based discovery

## Lying Stubs Eliminated

### Marketplace (`crates/core/plugins/src/web/marketplace.rs`)

| Function | Before | After |
|----------|--------|-------|
| `get_installations` | Fabricated fake completed installation with random UUIDs | Empty list with "not yet wired" note |
| `get_installation_status` | Fabricated 75% progress for any ID | 404 Not Found |
| `cancel_installation` | Claimed success without logic | 404 Not Found |

### Distribution (`crates/core/plugins/src/distribution/mod.rs`)

| Function | Before | After |
|----------|--------|-------|
| `verify_plugin_package` | Always `Ok(true)` (dangerous!) | Error: no verification backend |
| `remove_repository` | Silent no-op `Ok(())` | Error: no persistent backend |
| `enable_repository` | Silent no-op `Ok(())` | Error: no persistent backend |
| `disable_repository` | Silent no-op `Ok(())` | Error: no persistent backend |
| `refresh_repositories` | Silent no-op `Ok(())` | Error: no repositories configured |
| `uninstall_plugin` | Silent no-op `Ok(())` | Error: no distribution backend |

### Ecosystem (`crates/main/src/ecosystem/manager.rs`)

| Function | Before | After |
|----------|--------|-------|
| `discover_services` | Empty `Ok(Vec::new())` while logging "use CapabilityResolver" | `Err(OperationFailed)` with deprecation message |

## Tests Updated

3 tests updated to expect deprecation errors for `discover_services`.

## Metrics

- **Tests**: 7,189 passing (0 failures)
- **Quality gates**: `fmt` ✓, `clippy 0 warnings` ✓, `test` ✓, `deny` ✓
