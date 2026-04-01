# Primal Team Gap Blurbs — April 1, 2026

Per-primal copy/paste blurbs for teams with remaining gaps.
Append below the standard audit checklist.

Source: primalSpring Phase 23i deep validation + plasmidBin harvest.
13 gaps resolved this cycle. 19 open (0 Critical, 1 High, 9 Medium, 9 Low).

Clean primals (zero gaps): **biomeOS**, **bearDog**, **rhizoCrypt**, **loamSpine**, **sweetGrass**, **barraCuda**, **coralReef**.

---

## petalTongue

PT-05 (Medium): `visualization.showing` returns false when `RenderingAwareness` is not initialized — initialize a default on startup. PT-06 (Low): `callback_method` is stored but never invoked; proprioception is poll-only — implement callback dispatch. PT-07 (Low): No external event source in server mode — wire capability discovery into `DataService`. PT-04 (Low): No HTML export modality — accept SVG-in-HTML as sufficient for now. Deferred: `EguiShapes` variant for full native desktop UI. `capabilities.list` currently returns empty from the running binary — audit and wire. `identity.get` and `lifecycle.status` return Method not found — wire or remove from docs.

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
