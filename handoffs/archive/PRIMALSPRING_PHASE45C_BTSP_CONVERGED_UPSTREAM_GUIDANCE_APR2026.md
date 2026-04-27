# primalSpring Phase 45c — BTSP Converged: Upstream Guidance

**From**: primalSpring v0.9.17 (Phase 45c)
**Date**: April 25, 2026
**Status**: 187/187 guidestone ALL PASS, 13/13 BTSP authenticated, 8 cellular graphs BTSP-enforced. biomeOS v3.25 absorbed.

---

## What Changed

Full NUCLEUS BTSP convergence is achieved. All 13 capabilities are
BTSP-authenticated. The graph, launcher, and guidestone have been
updated to reflect this as the permanent default posture.

### Local Changes (primalSpring)

1. **`nucleus_complete.toml`**: All nodes now declare `security_model = "btsp"`
   (was `tower_delegated`). Bonding policy upgraded: `nucleus_internal = "metallic"`
   (was `weak`), `encryption_tiers.nucleus = "btsp_authenticated"` (was `hmac_plain`).
   Added barraCuda and coralReef as explicit graph nodes. Added NestGate streaming
   ops (`store_blob`, `retrieve_blob`, `retrieve_range`, `object.size`, `namespaces.list`).

2. **`nucleus_launcher.sh`**: Post-Tower BTSP verification probe added. After all
   primals launch, the launcher probes each socket with a BTSP `ClientHello` and
   reports how many respond with a valid `ServerHello` challenge. This catches
   misconfigs before guidestone runs.

3. **`guidestone` Layer 1.5 enhanced**: Now validates `BtspEnforcer` trust model
   policy per tier — Tower requires Covalent bond (nuclear-tier genetics), Node/Nest/
   Provenance require Metallic bond (mito-beacon genetics). Each tier's minimum cipher
   and trust requirement is explicitly reported.

4. **`guidestone` Layer 7 enhanced**: Cellular deployment validation now checks that
   every node in a cell graph declares `security_model = "btsp"` or `"btsp_enforced"`.
   Cells with `tower_delegated` or missing security models will FAIL.

---

## What Each Team Needs to Do

### biomeOS — ALL RESOLVED (v3.25, April 25, 2026)

**1. Graph bootstrapping in UDS mode** — **RESOLVED**
biomeOS v3.25 added `register_capabilities_from_graphs()`: scans all `.toml` graphs
at startup (step 4c), extracts node capabilities and primal names, pre-registers
expected socket paths in the NeuralRouter. `capability.call` now resolves primals
even before live socket discovery runs.

**2. BTSP runtime escalation** — **RESOLVED**
biomeOS v3.25 added `btsp.escalate` JSON-RPC method: sets a runtime `AtomicBool`
flag making all subsequent UDS connections require BTSP. One-way transition
(cleartext → enforced). Called after Tower health is confirmed. `btsp.status`
reports current enforcement state. `accept_connections` checks both static
`btsp_enforce()` and runtime `btsp_escalated` on each accept.

**3. `capability_registry.toml` tensor translations** — **RESOLVED**
Already present in v3.24: `[domains.tensor]` + `[translations.tensor]` with 33
entries covering all barraCuda Sprint 44 methods.

### All primal teams — verify your BTSP posture

Pull the latest `nucleus_complete.toml` from primalSpring. Your node now declares
`security_model = "btsp"`. Verify:

1. Your BTSP relay responds to the socat probe:
```bash
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat -t3 - UNIX-CONNECT:/run/user/$(id -u)/biomeos/${PRIMAL}-${FAMILY_ID}.sock
```
Expected: JSON line with `challenge`, `server_ephemeral_pub`, `version`.

2. After a successful BTSP handshake, your connection stays alive for subsequent
   JSON-RPC calls (NDJSON). Do NOT drop the connection after `HandshakeComplete`.

3. If `btsp.negotiate` returns "Method not found" from BearDog, default to the
   client's `preferred_cipher` — do not abort the handshake.

4. `family_seed` in `btsp.session.create`: base64-encode the raw `FAMILY_SEED`
   env string (`BASE64.encode(raw.trim().as_bytes())`). Do NOT send raw hex.

### Downstream springs — what this means for you

Your compositions inherit BTSP by default via `primalspring::composition`. When
you call `CompositionContext::from_live_discovery_with_fallback()`, all capability
clients are BTSP-authenticated. No code changes needed.

Your cell graphs (in `graphs/cells/`) must now declare `security_model = "btsp"` on
every node. The guidestone Layer 7 check will FAIL if any node uses `tower_delegated`
or omits the security model.

---

## Reference

- BTSP relay pattern: `wateringHole/SOURDOUGH_BTSP_RELAY_PATTERN.md`
- BearDog wire contract: `wateringHole/handoffs/BTSP_WIRE_CONVERGENCE_APR24_2026.md`
- Graph reference: `primalSpring/graphs/nucleus_complete.toml`
- Guidestone standard: `wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md`
- Bonding model: `primalSpring/ecoPrimal/src/bonding/mod.rs` (`BtspEnforcer`, `TrustModel`)

---

**License**: AGPL-3.0-or-later
