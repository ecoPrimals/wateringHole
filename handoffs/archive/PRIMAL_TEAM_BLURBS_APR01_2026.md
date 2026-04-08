# Primal Team Gap Blurbs — April 1, 2026

Per-primal copy/paste blurbs for teams with remaining gaps.
Append below the standard audit checklist.

Source: primalSpring Phase 23i deep validation + plasmidBin harvest.
13 gaps resolved this cycle. 19 open (0 Critical, 1 High, 9 Medium, 9 Low).

Clean primals (zero gaps): **biomeOS**, **bearDog**, **rhizoCrypt**, **loamSpine**, **sweetGrass**, **barraCuda**, **coralReef**.

---

## petalTongue

**All primalSpring gaps resolved** (PT-04, PT-05, PT-06, PT-07, capabilities.list, identity.get, lifecycle.status). Deep debt evolution completed Apr 1: zero-copy IPC (serde_json::to_vec on all 7 hot paths), blake3 provenance hash (pure Rust), centralized discovery timeouts (12 constants), hardcoded primal names → capability_names constants (7 files), TUI devices wired to real PrimalInfo, songbird/paint/graph deduplication, 12 docs reconciled to tarpc-primary. Deferred: EguiShapes variant, full Cow<str> IPC evolution, aarch64 CI. Quality: 5,845+ tests, 0 failures, clippy clean (pedantic+nursery), cargo deny clean.

---

## NestGate

NG-01 (Medium): IPC adapter uses in-memory `HashMap`, not the real `nestgate-core` storage backend — wire real persistence into RPC handlers so `storage.list`/`storage.get` use durable state. NG-04 (Medium): `aws-lc-rs` C dependency still present via `nestgate-installer` → `reqwest` → `rustls` — ecoBin violation, switch to pure Rust TLS or delegate HTTP fetch to songBird. NG-05 (Medium): `CryptoDelegate` pattern started but `nestgate-security` still has full crypto stack (`aes-gcm`, `argon2`, `ed25519-dalek`, `hmac`, `sha2`, JWT) — complete delegation to bearDog via `crypto.*` IPC. NG-02 (Low): No dedicated game session API — add `session.save`/`session.load` convenience methods. NG-03 (Low): `data.*` handlers conflate live feeds with storage — namespace clearly. `health` responds but canonical `health.liveness`/`health.readiness`/`health.check` triad not verified — audit and wire.

---

## Squirrel

SQ-02 (Medium): `LOCAL_AI_ENDPOINT` env var is read by `AIProviderConfig::from_env()` but `AiRouter::new_with_discovery` does not use it — this is the last blocker for Ollama routing. `ai.query` fails with "No providers available" because the router only discovers from `AI_HTTP_PROVIDERS`, `AI_PROVIDER_SOCKETS`, and biomeOS/toadStool socket probes. Wire `LOCAL_AI_ENDPOINT` into `AiRouter` discovery so `ai.query` routes to Ollama at `localhost:11434`. SQ-03 (Low): `deprecated-adapters` feature flag gate poorly documented. Socket is at `/run/user/1000/squirrel/squirrel.sock` not `biomeos/` — move to conformant path. `ai_router: false` in readiness, 0 providers — the router needs wiring before readiness can report true.

---

## toadStool

TS-01 (Medium): coralReef discovery uses hardcoded URL — replace with socket directory scan or `capability.discover` via biomeOS. The plasmidBin binary is S168 (pre-S169 cleanup). Live testing confirms: `health.liveness` → "Method not found", `capabilities.list` returns 0 capabilities, all RPC methods fail. The S169 source exists in the repo (-10,659 lines of overstep removed) but has not been built and deployed. Rebuild from S169 source and harvest to plasmidBin. Wire `--port` to actual server bind (currently accepted but ignored).

---

## songBird

SB-02 (Low): Optional `ring-crypto` feature flag still exists in `songbird-quic` — QUIC crate now uses `BearDogQuicCrypto` provider which is correct, but the `ring` fallback feature should be removed or clearly marked opt-in-only for environments without bearDog. SB-03 (Low): Embedded `sled` persistence in `songbird-orchestrator` and `songbird-sovereign-onion` — should migrate to nestGate via `storage.*` IPC (blocked on NG-01 real persistence). Lowest-debt primal overall — 14 capabilities, 338K+ seconds uptime, stable.

---

*Cross-cutting (not primal-specific): XC-01 — no standard `DataBinding` construction library. XC-03 — no composition health aggregator.*
