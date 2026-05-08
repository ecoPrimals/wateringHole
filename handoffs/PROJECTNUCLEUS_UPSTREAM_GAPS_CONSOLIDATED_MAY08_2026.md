# projectNUCLEUS → primalSpring: Consolidated Upstream Gaps (May 8, 2026)

**Date**: 2026-05-08
**From**: projectNUCLEUS (ironGate)
**For**: primalSpring, all primal teams
**Context**: Phase 60 absorbed, MethodGate enforced, 265 PASS / 0 FAIL / 0 KNOWN_GAP

---

## Tier 1 — Security Blockers (action now)

### DF-2: toadstool MethodGate env var mapping

**Severity**: Medium
**Owner**: toadStool team

toadstool reads `TOADSTOOL_AUTH_MODE=enforced` from environment but `auth.mode`
RPC reports `"mode":"permissive"`. Either the env var name doesn't match the
internal config key, or the MethodGate implementation doesn't wire the env
to the gate mode.

**Evidence**: Deployed with `export TOADSTOOL_AUTH_MODE=enforced`, queried
`auth.mode` on TCP port 9200 — response: `{"mode":"permissive"}`.
All other primals with TCP `auth.mode` report `"enforced"` correctly.

**Fix**: Verify the env var name ToadStool expects (may be `TOADSTOOL_AUTH_MODE`,
`PRIMALSPRING_AUTH_MODE`, or a toadstool-specific key). Wire it to the gate.

---

### DF-3: songbird / squirrel silent on `auth.mode` via TCP

**Severity**: Low (informational)
**Owner**: songbird, squirrel teams

These primals don't respond to `auth.mode` JSON-RPC over TCP. They may only
expose it on UDS/IPC, which is fine — but downstream deployers can't verify
enforcement mode without shell access to the UDS socket.

**Note**: petaltongue is also "silent" on TCP, but for a stricter reason —
it rejects ALL unauthenticated TCP connections at the BTSP transport layer
(PT-09 enforcement). This is correct behavior and does not need a fix.

**Suggestion**: If TCP `auth.mode` is intentionally omitted, document that
in the primal's README. If unintentional, wire it.

---

## Tier 2 — Functional Blockers (Phase 3 prerequisites)

### U1: primalSpring CHECKSUMS stale after Phase 59 refactoring

**Severity**: Medium
**Owner**: primalSpring

7 of 18 checksums in `validation/CHECKSUMS` fail after the Phase 59 split of
`composition/mod.rs`, `deploy/mod.rs`, `coordination/mod.rs`, `btsp/mod.rs`
into submodules. guidestone reports TAMPER on clean checkout.

**Fix**: Regenerate `validation/CHECKSUMS` with `b3sum`. Consider CI hook.

### U2: Multi-node deploy graphs missing `by_capability` on operation nodes

**Severity**: Medium
**Owner**: primalSpring

5 of 18 deploy graphs fail guidestone structural validation because operation
nodes (e.g., `mesh_init`, `stun_discover`) set `transport = "uds_only"` but
lack `by_capability`. UDS discovery requires `by_capability` to find sockets.

**Affected**: `basement_hpc_covalent.toml`, `friend_remote_covalent.toml`,
`data_federation_cross_site.toml`, `idle_compute_federation.toml`,
`three_node_covalent_cross_network.toml`

### U3: Profile graphs missing `[graph.bonding_policy]`

**Severity**: Low
**Owner**: primalSpring

8 profile graphs have `security_model = "btsp"` but no `[graph.bonding_policy]`.
guidestone flags as structural inconsistency. Templates, so low blast radius.

### U5: sweetGrass TCP port confusion (39085 vs 9850)

**Severity**: Low
**Owner**: sweetGrass team

Historical HTTP endpoint was 39085, canonical BTSP TCP port is 9850.
projectNUCLEUS has aligned to 9850. Upstream docs and integration scripts
may still reference 39085.

---

## Tier 3 — Code Quality (primal team backlog, no blockers)

From the deep debt audit (`validation/PRIMAL_DEEP_DEBT_HANDBACK.md`):

| Priority | Primal | Issue | Impact |
|----------|--------|-------|--------|
| 1 | coralReef | `eprintln!` → `tracing` in coral-driver | Production log filtering |
| 2 | barraCuda | `unwrap()` → `?` in session/ops | Panic risk in long-running compute |
| 3 | nestGate | `unwrap()` → `?` in rpc/discovery | Service reliability |
| 4 | biomeOS | Mock helpers mixed with production code | Build hygiene |
| 5 | bearDog | HSM mock not feature-gated | Build size |
| 6 | petalTongue | Bare `#[allow]` without reason | Ecosystem lint target |
| 7 | squirrel | 1105-line test file | Maintainability |

### U4: Capability taxonomy inconsistency (`dag` vs `provenance`)

rhizoCrypt referenced as both `by_capability = "dag"` and `"provenance"`.
`routing.rs` maps both to rhizoCrypt so runtime works, but standardizing
on `"dag"` would eliminate ambiguity. projectNUCLEUS has aligned to `"dag"`.

---

## Tier 4 — Long-Term Architecture (flag only, not actionable yet)

### JH-11: Cross-primal token federation

**Severity**: Medium (deferred)
**Owner**: primalSpring / biomeOS team

beardog-issued ionic tokens are not verifiable by other primals. Each
primal's MethodGate validates independently — there is no shared public
key distribution or trust chain.

**Current workaround**: biomeOS composition forwarding with `_resource_envelope`
carries auth context across primals. Direct cross-primal RPC with bearer
tokens does not work.

**This is correctly deferred** — it requires federation infrastructure
(key distribution, trust anchors) that belongs in a later Phase. Flagging
so it's tracked. No action until Tier 1 and Tier 2 are clear.

### JH-5 cross-primal forwarding

skunkBat audit log events should eventually flow into rhizoCrypt DAG and
sweetGrass braids for provenance-tracked security monitoring. Currently
local ring buffer only. Deferred until JH-11 federation path is clearer.

---

## What's Working (no action needed)

| Item | Status |
|------|--------|
| JH-0: MethodGate | **ENFORCED** on 10/13 primals, 3 silent/BTSP-gated |
| JH-1: Ionic tokens | **LIVE** — Ed25519, scope-checked, expiry-verified |
| JH-2: Resource envelopes | **ENFORCED** — biomeOS + ToadStool |
| JH-3: Composition reload | **RESOLVED** |
| JH-4: Session UX | **RESOLVED** |
| JH-5: Audit log | **Phase 2 COMPLETE** — local ring buffer |
| DF-1: Binding | **RESOLVED** — all 14 ports on 127.0.0.1 |
| GAP-11: barraCuda | **CLOSED** — 18/18 methods |
| PG-55→PG-62 | **ALL RESOLVED** by Phase 60 |
| plasmidBin sync | 13/13 checksum-verified, `sync.sh` operational |
| 5-layer validation | **265 PASS, 0 FAIL, 0 KNOWN_GAP** |

---

## References

- `projectNUCLEUS/validation/REVALIDATION_PHASE60_MAY08_2026.md`
- `projectNUCLEUS/validation/PRIMAL_DEEP_DEBT_HANDBACK.md`
- `projectNUCLEUS/validation/UPSTREAM_GAPS_HANDBACK_MAY06_2026.md`
- `wateringHole/handoffs/PROJECTNUCLEUS_PHASE60_ENFORCED_MODE_HANDOFF_MAY08_2026.md`
