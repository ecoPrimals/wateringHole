# biomeOS v2.46 — Spring Absorption + Ecosystem Alignment Handoff

**Date**: March 16, 2026
**From**: Spring Absorption Session
**To**: Next Session / Ecosystem
**Status**: COMPLETE
**Primal**: biomeOS (orchestrator)
**Version**: 2.45 → 2.46

---

## Summary

Absorbed proven patterns from 5 ecosystem springs into biomeOS: DispatchOutcome (airSpring), IpcError (healthSpring), typed capability SDK (groundSpring), #[expect] lint migration (neuralSpring/rhizoCrypt/ludoSpring), and tarpc 0.37 alignment with barraCuda/coralReef GPU stack.

---

## Absorptions

### 1. DispatchOutcome (from airSpring v0.8.3)
- Structured enum separating protocol vs application errors in Neural API dispatch
- Variants: Success, ApplicationError, MethodNotFound (-32601), InvalidRequest (-32600), ParseError (-32700)
- `into_response()` converts to JSON-RPC format
- `handle_request_json()` backward-compatible wrapper

### 2. IpcError (from healthSpring v28)
- Typed error enum for `AtomicClient::try_call()`: ConnectionFailed, Timeout, JsonRpcError, MissingResult, Serialization
- `is_method_not_found()` enables retry on alternate primals
- `is_timeout()` enables backoff logic

### 3. Typed Capability SDK (from groundSpring V108)
- `CapabilityClient` in biomeos-primal-sdk with domain-specific methods
- Crypto: sign, verify, hash
- HTTP: request through Songbird
- Storage: put, get, exists through NestGate
- Compute: execute through Toadstool
- Discovery: capability discovery, translation listing
- Health: per-primal health checks

### 4. #[expect] Migration (from neuralSpring V108, rhizoCrypt 0.13, ludoSpring V14)
- ~60 annotations migrated across 59 files
- Self-documenting reasons on every suppression
- Compiler warns when suppression is no longer needed

### 5. tarpc 0.37 (from barraCuda v0.3.5, coralReef Iter 49+)
- GPU stack version alignment
- No breaking changes; drop-in replacement

### 6. Hardcoded Cleanup
- Port 9000 → ports::NEURAL_API
- "songbird"/"beardog" → primal_names::* constants

---

## Metrics

| Metric | Before (v2.45) | After (v2.46) | Delta |
|--------|----------------|---------------|-------|
| Tests passing | 5,148 | 5,162 | +14 |
| tarpc version | 0.35 | 0.37 | Aligned with GPU stack |
| #[allow] annotations | ~70 | ~10 | -60 migrated to #[expect] |
| Hardcoded ports | 3 production | 0 production | Fixed |
| Hardcoded primal names | 2 production | 0 production | Fixed |

---

## Ecosystem Review Findings

### Springs Reviewed
- hotSpring (v0.6.31): GlowPlug daemon, FECS direct execution — GPU-specific, not applicable
- groundSpring (V108): Typed capability discovery, tolerance provenance — **absorbed**
- neuralSpring (V108/S157): Tower Atomic HTTP, #[expect] — **absorbed**
- wetSpring (V121): Songbird integration — already aligned
- airSpring (v0.8.3): DispatchOutcome, RpcTransport — **absorbed**
- healthSpring (V28): try_send/SendError — **absorbed**
- ludoSpring (V14): XDG discovery, #[expect] — **absorbed**

### Primals Reviewed
- Phase 1: beardog 0.9.0, songbird 0.2.2, nestgate 4.1.0-dev, toadstool S155b, squirrel 0.1.0-a7
- Phase 2: loamSpine 0.9.1, petalTongue 1.6.6, rhizoCrypt 0.13.0-dev, sweetGrass 0.7.15
- Tools: barraCuda 0.3.5, coralReef 0.1.0

### Key Observation
All springs independently converged on capability-based discovery: env → scan → XDG fallback. The typed SDK now codifies this as a first-class API.

---

## Verification

```bash
cargo fmt --check         # PASS
cargo clippy --workspace --all-features -- -D warnings  # PASS (0 warnings)
cargo test --workspace    # 5,162 passed, 0 failed
cargo doc --workspace --no-deps  # 0 warnings
```
