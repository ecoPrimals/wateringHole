# ludoSpring V49 — Deep Debt Resolution & Composition Patterns

**From:** ludoSpring team
**For:** primalSpring audit, all spring teams, primal teams, biomeOS/neuralAPI
**Date:** April 25, 2026

---

## Summary

ludoSpring V49 completes a systematic deep debt resolution pass:

- **799** workspace tests (100 experiments, zero failures)
- **Zero** clippy warnings, unsafe code, TODO/FIXME/HACK markers
- **Zero** external dependencies removable (base64 crate replaced with inline encoder)
- **Zero** hardcoded primal names in validation binaries (capability-based discovery)
- **15/15** MCP tools wired (was 13/15)
- **Typed `IpcError`** in all BTSP relay code (was `Result<_, String>`)
- Handler test extraction: `ipc/handlers/mod.rs` 818→169 lines

## Composition Patterns for Absorption

### 1. Capability Discovery (not name discovery)

ludoSpring's validation binaries now discover peer primals by querying their
`NicheDependency` table for capability strings (`"compute"`, `"tensor"`,
`"security"`) rather than hardcoded names (`"barracuda"`, `"beardog"`).

This aligns with biomeOS's `register_capabilities_from_graphs()` pattern where
a capability can be fulfilled by any primal that advertises it.

**Recommendation:** Add to `SPRING_COMPOSITION_PATTERNS` §13.

### 2. Inline Small-Surface Encoders

When a crate dependency exists for a single function call (e.g., `base64::encode`),
an inline implementation eliminates supply chain risk and compile time. ludoSpring's
20-line RFC 4648 encoder replaces the entire `base64` crate.

### 3. Handler Test Extraction Pattern

For dispatch modules with >200 lines of inline tests, use `#[path = "tests.rs"]`
to keep production code lean. ludoSpring demonstrated this reduces mod.rs from
818→169 lines while keeping tests colocated in the module tree.

**Recommendation:** Add to `SPRING_COMPOSITION_PATTERNS` §12.

### 4. Typed IPC Errors at Every Boundary

`Result<_, String>` in IPC code prevents smart retry decisions. ludoSpring's
BTSP module now uses `IpcError` with variants that encode:
- Retriability (`Connect`, `Timeout`)
- Recoverability (`NotFound`)
- Finality (`Serialization`, `RpcError`)

### 5. MCP Surface Completeness

Every `game.*` JSON-RPC method must have a corresponding MCP `tools.list`
descriptor and `tools.call` dispatch entry. ludoSpring was missing 2/15
(record_action, voice_check). This is now fixed.

**Recommendation:** Add an MCP completeness check to guideStone validation.

## NUCLEUS Cell Graph Status

`ludospring_cell.toml`: 14 nodes, all `security_model = "btsp"`.
BTSP relay: typed IpcError, 4-step BearDog handshake.
Interactive loop: `push_scene → petalTongue → interaction.poll → record_action`.
Live NUCLEUS validated: 54/54 guideStone checks (V47, confirmed stable through V49).

## For primalSpring Audit

### Clean codebase confirmation
- 0 `TODO`/`FIXME`/`HACK`/`XXX` in Rust source
- 0 `todo!`/`unimplemented!` macros
- 0 `#[allow(dead_code)]` in barracuda/src/
- 0 `.sh` scripts, 0 stray `.py`, 0 temp files
- 0 `Result<_, String>` in IPC modules (BTSP fully typed)
- All experiments inherit workspace lints
- All handoff history preserved in `wateringHole/handoffs/archive/`

### Open gaps (GAP-01–GAP-11)
All in `docs/PRIMAL_GAPS.md`. GAP-11 (barraCuda formulation divergence) is the
only open semantic gap. No new gaps introduced in V48–V49.

### Evolution requests for upstream primals
1. Absorb `base64_encode()` into `primalspring::composition` utility module
2. Update primalSpring examples to use `IpcError` instead of `Result<_, String>`
3. Document handler test extraction pattern in `SPRING_COMPOSITION_PATTERNS`
4. Add MCP completeness check to guideStone validation standard
