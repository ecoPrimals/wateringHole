# petalTongue v1.6.6 — TRUE PRIMAL Name Evolution & Deep Debt Completion

**Date**: May 3, 2026
**Version**: 1.6.6
**Primal**: petalTongue
**Session Type**: TRUE PRIMAL compliance — hardcoded primal name elimination

---

## Summary

Systematic evolution of all hardcoded primal names in production code to
capability-based language. petalTongue now has zero hardcoded references to
specific primals (BearDog, ToadStool, Songbird, rhizoCrypt, sweetGrass,
loamSpine) in production code — only test fixtures and historical code
provenance comments retain specific names.

This follows the BTSP Phase 3 transport switch (previous handoff) and
completes the TRUE PRIMAL compliance sweep.

## Audit Results (Clean)

| Dimension | Status |
|-----------|--------|
| TODOs / FIXMEs / HACKs | Zero |
| Large files (>800L) | Zero (max 714L) |
| Unsafe code blocks | Zero (`forbid(unsafe_code)`) |
| `Result<_, String>` in production | Zero |
| Direct C dependencies | Zero |
| Production `#[allow(unwrap_used)]` | Zero (all in `#[cfg(test)]`) |
| Mock leaks into production | Zero (properly feature-gated) |
| Hardcoded primal names in prod | **Zero** (was 20+, now eliminated) |

## Changes (25+ files)

### BTSP Module — "BearDog" → "security provider"

| File | Change |
|------|--------|
| `btsp/types.rs` | `EnforceBearDog` → `EnforceProvider`; doc/log messages evolved |
| `btsp/server.rs` | "delegates crypto to BearDog" → "delegates crypto to the security provider" |
| `btsp/json_line.rs` | "Call BearDog" → "Call provider"; log messages evolved |
| `btsp/phase3.rs` | "Per BearDog W81" → "Per ecosystem standard (W81)" |
| `btsp/error.rs` | "BearDog security provider" → "security provider" |
| `btsp/client.rs` | "BearDog BTSP provider" → "BTSP security provider" |
| `btsp/mod.rs` | Module doc evolved |
| `btsp/tests.rs` | `EnforceBearDog` → `EnforceProvider` in match arms |

### Audio Backends — "ToadStool" → capability language

| File | Change |
|------|--------|
| `audio/backends/mod.rs` | "ToadStool `audio.play`" → "`audio.play` capability provider" |
| `audio/backends/socket.rs` | Stub docs evolved to capability-based |
| `audio/backends/direct.rs` | Stub docs evolved to capability-based |
| `audio/backends/network.rs` | Runtime log "until ToadStool" → "until audio.* capability is wired" |

### Provenance Trio — capability-first documentation

| File | Change |
|------|--------|
| `provenance_trio.rs` | Field docs, module docs, inline comments: rhizoCrypt → `dag.session`, sweetGrass → `braid.create`, loamSpine → `spine.create` |
| `lib.rs` (ipc) | Re-export comment evolved |

### HTTP/TLS Delegation — "Songbird" → provider language

| File | Change |
|------|--------|
| `http_client.rs` | "Songbird handles" → "TLS provider handles" |
| `https_client.rs` | "delegated to Songbird" → "delegated to TLS-capable provider" |
| `connect.rs` | "TLS delegated to Songbird" → "TLS delegated to ecosystem provider" |
| `biomeos_client.rs` | "Songbird handles that" → "delegated to ecosystem provider" |
| `stream.rs` | Comment evolved |

### Other Production Code

| File | Change |
|------|--------|
| `unix_socket_server.rs` | "delegated to BearDog" → "delegated to the security provider" |
| `scene_signer.rs` | "BearDog" → "security provider" / "provider delegation" |
| `visualization/mod.rs` | "toadStool Phase 2" → "display capability Phase 2" |

### Root Documentation

| File | Change |
|------|--------|
| `README.md` | BTSP row updated from Phase 2/BearDog to Phase 3/ChaCha20-Poly1305 |
| `CHANGELOG.md` | Added TRUE PRIMAL Name Evolution + BTSP Phase 3 entries |
| `CONTEXT.md` | All primal name references evolved to capability-based language |
| `trust.rs` | "temporary" comment → proper `from_capability_spec()` guidance |

## What Was Preserved

- **Test fixtures**: Primal names in test data (e.g., "songbird", "toadstool"
  in TUI tests, IPC integration tests) — these are legitimate test topology data.
- **`#[cfg(feature = "test-fixtures")]` constants**: `BEARDOG` and `SONGBIRD` in
  `capability_names.rs` — properly gated, doc explains they're fixture identities.
- **Historical attribution**: "absorbed from rhizoCrypt v0.13" in resilience.rs,
  pattern credits in ipc_errors.rs — code provenance markers, not runtime deps.

## Verification

```
cargo clippy --workspace --all-features: 0 warnings
cargo doc --workspace --no-deps -D warnings: 0 warnings
cargo test --workspace --all-features: 2,261+ passed, 0 failed
```

## Debris/Archive Review

- No stale temp files, `.bak`, `.orig`, `.swp` found
- No orphaned scripts, Dockerfiles, or `.env` files
- `sandbox/` and `showcase/` are structured demo infrastructure — intentionally kept
- `graphs/petaltongue_deploy.toml` and `niche.yaml` are deployment artifacts — kept
- CI workflows (ci.yml + notify-plasmidbin.yml) both active
- Zero TODO/FIXME/HACK markers in any source file

## Downstream Impact

- **primalSpring**: petalTongue now fully compliant with TRUE PRIMAL self-knowledge
  principle. No production code references specific external primals by name.
- **Ecosystem**: All 13/13 primals have BTSP Phase 3 transport switch. petalTongue's
  BTSP code now uses generic "security provider" terminology matching the
  capability-based discovery model.

---

*Ref: `PETALTONGUE_V166_BTSP_PHASE3_TRANSPORT_SWITCH_HANDOFF_MAY03_2026.md` for Phase 3 details*
*Ref: `PETALTONGUE_V166_DEEP_DEBT_SWEEP_IDIOMATIC_EVOLUTION_HANDOFF_MAY03_2026.md` for initial debt sweep*
