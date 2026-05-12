# primalSpring Phase 45b — BTSP Escalation & Entropy Hierarchy Handoff

**Date**: April 2026
**From**: primalSpring v0.9.17 (Phase 45b)
**For**: Primal teams (BearDog, Songbird, rhizoCrypt, sweetGrass, loamSpine, biomeOS) + all spring teams
**License**: AGPL-3.0-or-later

---

## What Happened

primalSpring implemented **incremental BTSP escalation** with machine-level
entropy (mito tier) for portable validation. The guidestone binary now reports
**161/166 checks passing** against a live 12-primal NUCLEUS. The 5 FAILs are
legitimate upstream gaps — primals that should enforce BTSP but don't yet
implement the server-side handshake protocol.

---

## What Changed

### 1. Entropy Hierarchy (Mito Tier)

Machine-level entropy for portable validation:
- `MitoSeed`: deterministic, clonable from `FAMILY_SEED` or `.family.seed`
- Proves group membership for BTSP Phase 1 handshake key derivation
- Published seed fingerprints (BLAKE3) in `plasmidBin/manifest.toml`
- Nuclear tier (future): human entropy mixed, sovereign identity

### 2. Incremental BTSP Escalation

Security builds incrementally from cleartext:

| Phase | State | What Changes |
|-------|-------|--------------|
| Bootstrap | Cleartext | biomeOS starts `BIOMEOS_BTSP_ENFORCE=0` |
| Tower BTSP | Encrypted | BearDog + Songbird authenticate |
| Node/Nest | Delegated | ToadStool, barraCuda, coralReef, NestGate trust Tower |
| Provenance | Encrypted | rhizoCrypt, sweetGrass, loamSpine authenticate |
| Full NUCLEUS | Encrypted | All capabilities authenticated or delegated |

### 3. Guidestone Layer 1.5

Reports per-atomic security posture:
- Tower: BTSP expected (currently FAIL — upstream gap)
- Node: tower_delegated (PASS — cleartext OK)
- Nest: tower_delegated (PASS — cleartext OK)
- Provenance: BTSP expected (currently FAIL — upstream gap)
- biomeOS substrate: Neural API liveness + graph executor validated

### 4. Seed Provenance (Layer 0.5)

Public BLAKE3 fingerprints verify binary authenticity before any IPC.
Every primal in `plasmidBin/manifest.toml` has a `seed_fingerprint` entry.
Layer 0.5 runs before discovery — untampered binaries safe for use.

---

## What Primal Teams Need to Do

### BearDog (Tower — security)

**Gap**: `ClientHello` JSON treated as invalid JSON-RPC → Parse error → connection close.

**Fix**: On the primary UDS socket, detect first-byte `{` with `"type":"ClientHello"` and
branch to the BTSP handshake flow before JSON-RPC dispatch. BearDog already has `btsp_client.rs`
client-side code — the server needs the mirror: accept `ClientHello`, respond `ServerHello`,
validate `ChallengeResponse`, complete with `HandshakeComplete`. HMAC-SHA256 with
`FAMILY_SEED` key derivation. See `primalSpring/ecoPrimal/src/btsp/` for reference.

### Songbird (Tower — discovery)

**Gap**: HTTP-framed UDS with no BTSP listener.

**Fix**: Songbird's UDS socket speaks HTTP. Either add a BTSP upgrade mechanism
(WebSocket-style handshake before HTTP) or expose a separate BTSP-authenticated socket
for secure discovery. The simpler path: add a `/btsp` HTTP endpoint that upgrades
the connection to the encrypted channel post-handshake.

### rhizoCrypt (Provenance — DAG)

**Gap**: No BTSP server on DAG socket.

**Fix**: Same first-byte detect pattern as BearDog. rhizoCrypt already has
`PeekedStream`-style auto-detect — extend it to recognize BTSP `ClientHello`.

### sweetGrass (Provenance — commit)

**Gap**: No BTSP server on commit socket.

**Fix**: sweetGrass has `PeekedStream` first-byte auto-detect on UDS + TCP.
Extend to recognize BTSP `ClientHello` alongside JSON-RPC `{`.

### loamSpine (Provenance — provenance) — **RESOLVED**

~~**Gap**: No BTSP server on provenance socket.~~

**RESOLVED** (April 21 + 22) — UDS accept loop auto-detects primalSpring-style NDJSON BTSP
(`{"protocol":"btsp","version":1,...}\n`). Routes to `perform_ndjson_server_handshake`
(newline-delimited JSON with `session_id` in `ServerHello`). Provider-delegated crypto
unchanged. Existing length-prefixed BTSP path preserved for Phase 2 clients. 12 + 2 tests.

**Provider socket wiring** (April 22): Static BTSP mode (`btsp_config` is `Some`) now
peeks first byte via `BufReader::fill_buf()` instead of bypassing NDJSON detection.
Provider socket resolved from `btsp_config` first, falling back to env vars. JSON-RPC
connections pass through auto-detect even when BTSP is configured.
`perform_server_handshake` refactored to split reader/writer for BufReader compatibility.

**HandshakeComplete wire fix** (April 15): `HandshakeComplete` was missing
`"status":"ok"` discriminator field. primalSpring uses this field to identify the
message type. Without it, clients timed out. Fixed in both framed and NDJSON paths.
Resolves Phase 45c "incomplete handshake" gap. 1 new test (1,503 total).

**Step 3→4 verification relay** (April 23): All three BearDog relay calls aligned with
`beardog_types::btsp::rpc` contract. `btsp.session.create` sends `family_seed` (base64
from `FAMILY_SEED`/`BEARDOG_FAMILY_SEED` env) instead of `family_seed_ref`. Challenge
generated by BearDog, not loamSpine — `generate_challenge()` removed. `btsp.session.verify`
uses `session_token`/`response`/`preferred_cipher` instead of `session_id`/`client_response`/
`server_ephemeral_pub`/`challenge`. `btsp.negotiate` uses `session_token`/`cipher` instead
of `session_id`/`preferred_cipher`/`bond_type`. `resolve_family_seed()` added. 5 new tests
(1,502 total). Same pattern as sweetGrass April 22 fix.

### biomeOS (Substrate)

**Gap**: Starts in cleartext mode (`BIOMEOS_BTSP_ENFORCE=0`). Cannot participate
in encrypted NUCLEUS without its own Tower Atomic capability.

**Evolution path**: biomeOS routes through Tower Atomic for all transport.
Short-term: cleartext bootstrap is correct (Tower isn't alive when biomeOS starts).
Long-term: biomeOS either implements BTSP client/server directly or delegates
all IPC transport to Songbird mesh relay + BearDog BTSP.

---

## What Spring Teams Need to Know

### Encrypted by Default (When Upstream Is Ready)

Once the 5 primal teams implement BTSP server handshake, the NUCLEUS will be
encrypted by default with zero changes needed in spring code. The escalation
is transparent — `upgrade_btsp_clients()` handles it automatically.

### Seed Fingerprints for Your GuideStone

If you're building a domain guideStone, you can use Layer 0.5 as-is:
```rust
use primalspring::composition::CompositionContext;
// CompositionContext::from_running() already verifies seed fingerprints
```

### Your BTSP Reporting

Your guidestone inherits Layer 1.5 BTSP reporting through `CompositionContext`.
The `btsp_state()` map tells you which capabilities are authenticated:
```rust
for (cap, authenticated) in ctx.btsp_state() {
    if *authenticated {
        // BTSP-encrypted channel
    } else {
        // cleartext or tower-delegated
    }
}
```

### The Three-Tier Composition Pattern Still Applies

- **Tier 1 (LOCAL)**: Your Rust math. Always green. No IPC needed.
- **Tier 2 (IPC-WIRED)**: Call primals by capability. `check_skip()` when absent.
- **Tier 3 (FULL NUCLEUS)**: Deploy from plasmidBin, run guideStone externally.
  BTSP escalation is automatic when `FAMILY_SEED` is set.

---

## Key References

| Document | Location |
|----------|----------|
| BTSP client reference | `primalSpring/ecoPrimal/src/btsp/` |
| Seed provenance tool | `primalSpring/tools/gen_seed_fingerprints.sh` |
| Layer 1.5 implementation | `primalSpring/ecoPrimal/src/bin/primalspring_guidestone/main.rs` |
| Reactive BTSP upgrade | `primalSpring/ecoPrimal/src/composition/mod.rs` (`upgrade_btsp_clients`) |
| Transport BTSP tracking | `primalSpring/ecoPrimal/src/ipc/transport.rs` |
| Upstream gap status | `infra/wateringHole/UPSTREAM_GAP_STATUS_APR20_2026.md` |
| GuideStone standard | `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` |
| Composition guidance | `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` |

---

## Guidestone Readiness — Updated

| Spring | gS Level | BTSP Impact | Next Step |
|--------|----------|-------------|-----------|
| primalSpring | 4 (161/166 live) | 5 FAIL = upstream gaps | Certifying base for all |
| hotSpring | 5 (certified) | Inherits Layer 1.5 on next pull | Template for others |
| ludoSpring | 4 (active partner) | Composition-first, petalTongue GUI | Evolving with primalSpring |
| wetSpring | 3 (bare works) | Deploy NUCLEUS, begin Tier 2 | Pull and validate |
| neuralSpring | 2 (scaffold) | Wire bare property checks | Pull and validate |
| healthSpring | 2 (scaffold) | Wire bare property checks | Pull and validate |
| airSpring | 0 | Start with guideStone scaffold | Pull primalSpring first |
| groundSpring | 0 | Start with guideStone scaffold | Pull primalSpring first |
