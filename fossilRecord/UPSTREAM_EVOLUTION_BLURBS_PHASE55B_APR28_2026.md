# Upstream Evolution Blurbs — Phase 55b (April 28, 2026)

Per-primal actionable evolution asks from primalSpring v0.9.21 composition
validation. Each blurb is self-contained — forward it to the primal team.

---

## BearDog — RESOLVED (W74 shipped P1)

**Latest**: W74 — lazy purpose-key derivation in `secrets.retrieve` +
`crypto.encrypt`/`crypto.decrypt` with `purpose` param. W72 shipped
`crypto.derive_purpose_key` + `crypto.sign_registration`.

**What shipped (W74)**: Exactly what was asked. `secrets.retrieve` with
`nucleus:{family}:purpose:{name}` auto-derives and caches keys from
`FAMILY_SEED`. `crypto.encrypt`/`crypto.decrypt` accept `purpose` param,
resolve the key, return NUCLEUS standard envelope. Compatible with NestGate
encrypt-at-rest and Squirrel inference encryption.

**What's still needed**: Two consumers — NestGate and Squirrel — have client
stubs ready for purpose-key encrypted storage and inference payloads. They call:

```
secrets.retrieve("nucleus:{family}:purpose:storage")   ← NestGate
secrets.retrieve("nucleus:{family}:purpose:inference")  ← Squirrel
crypto.encrypt(data, purpose="storage")                 ← NestGate (future)
crypto.decrypt(envelope, purpose="inference")            ← Squirrel (future)
```

BearDog already has `secrets.store`/`retrieve` and `chacha20_poly1305_encrypt`/
`decrypt`. The delta:

1. **Lazy purpose-key derivation in `secrets.retrieve`**: When a key matching
   `nucleus:{family}:purpose:{name}` is requested and doesn't exist, derive it
   via `crypto.derive_purpose_key` from the family key and auto-store. This
   removes the dependency on `nucleus_crypto_bootstrap.sh` having run first.

2. **`crypto.encrypt` / `crypto.decrypt` with `purpose` param**: Look up the
   purpose key from secrets, use it as the ChaCha20-Poly1305 key. Wire format:
   ```json
   {"method":"crypto.encrypt","params":{"data":"<b64>","purpose":"storage","algorithm":"chacha20-poly1305"}}
   ```
   Returns the standard envelope: `{"v":1,"ct":"...","n":"...","alg":"chacha20-poly1305"}`

**Why it matters**: This is the single change that lights up end-to-end
encryption across the NUCLEUS. NestGate's native encrypt-at-rest resolves keys
via `secrets.retrieve` — lazy derivation means zero manual key setup. Squirrel's
inference payloads encrypt automatically when `FAMILY_ID` is present.

**Effort estimate**: Small — the building blocks exist. It's routing + one
derivation check in `secrets.retrieve` + purpose parameter in encrypt/decrypt.

---

## rhizoCrypt — Tower Crypto Delegation (P2) — **RESOLVED (S52/S54)**

**Latest**: S54 — 1,546 tests (all-features), 93.88% coverage, 0 clippy warnings,
167 `.rs` files, ~49,900 lines. Deep debt audit clean across 8 categories.

**Signing delegation already shipped (S52)**: `sign_vertex_if_available()` calls
`crypto.sign_ed25519` via capability-discovered signing provider on every
`dag.event.append`. Lazy discovery, graceful degradation. This is the **same
pattern** loamSpine uses for `entry.append` and sweetGrass uses for `braid.create`.

**Hash delegation declined (S54)**: BLAKE3 is deterministic (no key material) —
delegating it adds zero cryptographic value while imposing a 1000x+ IPC penalty
on the hottest path (~80ns local → ~100-500μs over UDS). The audit trail concern
is already addressed: Ed25519 vertex signatures attest to the content (including
its BLAKE3 hash). Neither loamSpine nor sweetGrass delegates hashing — both
delegate only signing. See `specs/CRYPTO_MODEL.md` for the canonical two-tier
model: local hashing for data integrity, delegated signing for attestation.

**DAG payload encryption**: Valid future item, but low priority — rhizoCrypt is
ephemeral by design (data discarded by default). Noted in roadmap.

**Correction**: The original blurb stated "rhizoCrypt is the last Nest primal
without Tower crypto delegation" — this was inaccurate. S52 (April 28) shipped
vertex signing delegation before Phase 55b was published. All three Nest primals
now delegate signing identically.

---

## sweetGrass — Anchor Signing via Tower (P3, incremental)

**Latest**: v0.7.28 — BearDog crypto signing delegation shipped. `braid.create`
now signs via `crypto.sign` Ed25519 when `BEARDOG_SOCKET` is set. Tower-tier
witnesses with `did:key:z6Mk...` agent DID. 1,461 tests.

**What you shipped that works**: Braid signing delegation is exactly what was
asked. Absorbed and documented. The `CryptoDelegate` module is clean — socket
resolution chain, graceful fallback, test coverage.

**What's still useful (incremental, not blocking)**:

1. **`anchoring.anchor` Tower signing**: The `anchoring.anchor` operation
   currently uses local signing. When Tower is available, delegate to
   `crypto.sign_ed25519` for ecosystem-wide trust. Same pattern as
   `braid.create` — you already have `CryptoDelegate`.

2. **Hash delegation**: `braid.compute_signing_hash` uses in-process SHA-256.
   Consider delegating to `crypto.sha256` or `crypto.blake3_hash` when Tower
   is available, for audit trail consistency.

These are incremental — sweetGrass already has the core delegation pattern
working. No blockers, no urgency.

**Effort estimate**: Trivial — reuse `CryptoDelegate` in the anchor handler.

---

## loamSpine — BTSP Encrypted Channels (P4, ecosystem-wide frontier)

**Latest**: v0.9.16 — Tower-signed ledger entries shipped. `entry.append` and
`session.commit` sign via `crypto.sign_ed25519` when `BEARDOG_SOCKET` is set.
Deep debt audit clean across all 10 dimensions. 1,509 tests. Max production
file 605L.

**What you shipped that works**: Tower signing is absorbed and documented.
The correction to the Phase 55 handoff is noted — entries ARE now signed.
The deep debt audit is exemplary.

**What's still a frontier**: BTSP encrypted tunnels. As your handoff correctly
notes: "no primal actively establishes persistent BTSP tunnels — this is the
next evolution frontier." This is ecosystem-wide, not loamSpine-specific.

**When to act**: When any primal pioneers persistent BTSP tunnels (likely
BearDog or Songbird as the Tower pair), loamSpine should adopt encrypted
ledger replication. Until then, the signed-but-unencrypted channel is the
correct posture.

**Effort estimate**: Medium — BTSP tunnel establishment requires
`btsp.tunnel.establish` + message framing. This is new ground for the
ecosystem, not a debt item.

---

## ToadStool — Self-Registration via DISCOVERY_SOCKET (P5)

**Latest**: Display Phase 2 — graphics node handoff (Apr 26). 7,818 lib tests.

**What's needed**: Squirrel now resolves capabilities via `DISCOVERY_SOCKET`
(`discovery.find_provider` as Method 2). For this to work without the
composition launcher doing registration on behalf of primals, ToadStool should
self-register at startup.

**Pattern**:
```rust
if let Ok(socket) = std::env::var("DISCOVERY_SOCKET") {
    let _ = rpc_call(&socket, "ipc.register", json!({
        "primal_id": "toadstool",
        "capabilities": ["compute.dispatch", "compute.capabilities"],
        "endpoint": format!("unix://{}", own_socket_path)
    }));
}
```

If `DISCOVERY_SOCKET` is absent, continue in standalone mode. If the
registration call fails, log and continue — non-fatal.

**Why it matters**: Dynamic NUCLEUS membership. Currently the composition
launcher registers all 12 primals with Songbird. Self-registration means
primals can join a running NUCLEUS without a restart/re-launch cycle.

**Also relevant**: barraCuda v0.3.12 Sprint 46 already wired `DISCOVERY_SOCKET`
for *resolving* capabilities (Songbird async fallback in `btsp.rs`). The delta
for ToadStool is the reverse direction — *announcing* capabilities to Songbird.

**Effort estimate**: Trivial — one JSON-RPC call at startup. Fire-and-forget.

---

## barraCuda — RESOLVED (Sprint 47 shipped self-registration)

**Latest**: v0.3.12 Sprint 47 — Songbird self-registration shipped.
`register_with_songbird()` sends `ipc.register` with 11 capability tags
(`tensor`, `math`, `stats`, `linalg`, `ml`, `spectral`, `activation`,
`noise`, `rng`, `fhe`, `device`) on all startup paths. Fire-and-forget,
graceful degradation. 272+ tests.

---

## coralReef — No Outstanding Asks (tracking)

**Latest**: Iter 86 — smart file refactoring (all production under 800L),
safety audit (SAFETY comments on all ~80 unsafe blocks in `coral-driver`).
4,701 tests. Zero clippy warnings.

**Status**: Clean. No outstanding composition asks from primalSpring. coralReef's
primary capabilities are consumed via tarpc (not JSON-RPC), so the composition
layer interacts with it indirectly through barraCuda's shader delegation.

**Future consideration**: If coralReef gains JSON-RPC methods beyond health
probes, self-registration with Songbird would follow the same pattern.

---

## petalTongue — No Outstanding Asks (tracking)

**Latest**: v1.6.6 Phase 55 — `AWAKENING_ENABLED=false` composition control,
scene signing via BearDog Ed25519 delegation, `sensor.stream.subscribe` discrete
event isolation.

**Status**: All three Phase 55 asks addressed. Scene signing is Tower-delegated.
Sensor streams support composition-controlled awakening. No remaining debt
from the composition perspective.

---

## Songbird — No Outstanding Asks (RESOLVED)

**Latest**: W178 — 20+ `Result<_, String>` → `anyhow::Result` across 6 crates.
W177 — signed IPC registrations (Ed25519 via BearDog). 7,692 tests.

**Status**: Clean. Songbird is the discovery backbone. Signed registrations
and anyhow error honesty are the standard other primals build on.

---

## biomeOS — No Outstanding Asks (RESOLVED)

**Latest**: v3.30 — deep debt cleanup (events refactor, thiserror, JWT
hardening, `skip_signature_check`, `#[expect(reason)]`). 7,814+ tests.

**Status**: Clean. biomeOS is the composition substrate. v3.30 absorbed.

---

## NestGate — No Outstanding Asks (RESOLVED)

**Latest**: v0.4.70 S48 — native encrypt-at-rest (ChaCha20-Poly1305), auth
mode bypass (`NESTGATE_AUTH_MODE=beardog`), emoji purge. 8,840 tests.

**Status**: Clean. Both Phase 55 asks (encrypt-at-rest + auth bypass) shipped.
Future: HTTP object encryption, key rotation, streaming encryption per S48 scope.

---

## Squirrel — No Outstanding Asks (RESOLVED)

**Latest**: v0.1.0 sessions AN/AO — HTTP providers, `DISCOVERY_SOCKET`
resolution, crypto foundation, lying stub elimination. 7,182 tests, 90.1%
coverage.

**Status**: Clean. All three Phase 55 asks resolved. Crypto foundation awaits
BearDog purpose-key RPC (P1) for end-to-end wiring.

---

## Summary Scoreboard

| Primal | Debt | Priority | Effort |
|--------|------|----------|--------|
| BearDog | **RESOLVED** W74 — lazy purpose-key derivation + purpose encrypt/decrypt shipped | P1 → Done | — |
| rhizoCrypt | **RESOLVED** — vertex signing delegated (S52); hash delegation declined | P2 → Done | — |
| sweetGrass | Anchor signing + hash delegation (incremental) | P3 | Trivial |
| loamSpine | BTSP encrypted channels (ecosystem frontier) | P4 | Medium (new ground) |
| ToadStool | DISCOVERY_SOCKET self-registration | P5 | Trivial |
| barraCuda | **RESOLVED** Sprint 47 — Songbird self-registration shipped | P5 → Done | — |
| coralReef | None | — | — |
| petalTongue | None | — | — |
| Songbird | None | — | — |
| biomeOS | None | — | — |
| NestGate | None | — | — |
| Squirrel | None | — | — |
