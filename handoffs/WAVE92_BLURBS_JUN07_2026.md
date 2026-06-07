# Wave 92 Blurbs — Targeted by Team

**Date**: 2026-06-07
**From**: eastGate overwatch
**Cascade**: 38/38 parity | Depot: 13/13 rebuilt + pushed to VPS | Pipeline: validated

---

## Status

All Wave 91 blurbed items were responded to **same-day** by all three teams:

| Item | Owner | Status |
|------|-------|--------|
| BIO-ORPHAN-01 (NUCLEUS lifecycle) | biomeOS | **RESOLVED** — v4.13 supervisor + SIGTERM |
| CM-WEBHOOK-01 (webhook cascade) | cellMembrane | **RESOLVED** — webhook handler + HMAC + selective harvest |
| TransportEndpoint canonicalization | songBird | **SHIPPED** — types in songbird-types |

VPS deployment validated: 13/13 binaries rebuilt and pushed to golgiBody via
`membrane plasmid.harvest` + `plasmid.refresh`. Depot symlink fixed. Checksums synced.

---

## cellMembrane Team — P2 (pipeline hardening)

**VPS-BUILD-01**: The `plasmid-pipeline.service` on golgiBody attempts `cargo build`
but golgiBody is a 2GB/10GB droplet with **no Rust toolchain**. 5 primals fail
every 30-min cycle (songbird, loamspine, barracuda, biomeos, petaltongue).

The pipeline must not build on golgiBody. Two options:

1. **Preferred**: Pipeline fetches pre-built binaries from the gate depot
   (eastGate builds via `plasmid.harvest`, pushes via `plasmid.refresh`).
   The timer should run `plasmid.refresh` (pull from gate depot), not
   `plasmid.harvest` (build from source).

2. **Alternative**: Pipeline SSH-delegates builds to peptidoglycan (has Rust 1.96,
   4GB RAM, 79GB disk), then pulls the results to golgiBody.

Current workaround: eastGate runs `membrane plasmid.harvest && membrane plasmid.refresh`
manually. This works but is not zero-touch.

**Also**: `plasmid.status` reports beardog + skunkbat as "drifted" despite matching
provenance commits. Likely a stale freshness.toml on the VPS (Wave 67 vs current).
Low priority — cosmetic.

---

## songBird Team — P2 (next evolution gate)

**TransportEndpoint shipped** — thank you. Next step for Phase 2 M1:

Wire `ipc.resolve` to return `TransportEndpoint` instead of raw path strings.
This is the gate for all primals to begin transport injection. Once `ipc.resolve`
returns structured endpoints, `CompositionContext` in primalSpring can query
Songbird instead of probing sockets directly.

---

## strandGate — P1 Coordination

**2-gate mesh proof**: Both gates have Songbird :7700 LIVE. We need to coordinate:

1. `mesh.init` from one gate targeting the other
2. `discovery.peers` returns `peer_count >= 1`
3. `mesh.health_check` all_healthy
4. Cross-gate `capability.call` smoke test

This is the sole remaining P1 item and is coordination, not code.

---

## All Other Teams — NO ACTION

Mountain clear. All P1 and P2 code items resolved. 13/13 primals deployed
from plasmidBin depot on VPS. S4 auth gate review ends ~Jun 9 (automated).

---

## Remaining Work

| # | Item | Owner | Priority | Status |
|---|------|-------|----------|--------|
| 1 | 2-gate mesh proof | operators | P1 | UNBLOCKED — coordination |
| 2 | VPS-BUILD-01: pipeline builds on toolchain-less VPS | cellMembrane | P2 | Open |
| 3 | songBird ipc.resolve structured endpoints | songBird | P2 | Types shipped, wiring next |
| 4 | Transport injection (1/14 primals) | all primals | P2 | Blocked on ipc.resolve |
| 5 | S4 auth gate review | automated | P1 | Ends ~Jun 9 |
| 6 | VPS plasmid.status drift (cosmetic) | cellMembrane | P3 | beardog/skunkbat false drift |

---

*"All code items resolved. Pipeline proven gate-to-VPS. Mesh proof is next. Transport evolution has started."*
