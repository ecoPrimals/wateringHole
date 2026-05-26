# Wave 54 — cellMembrane + Deployment Handoff

**Date**: 2026-05-26  
**From**: primalSpring (coordination)  
**To**: cellMembrane team, gate operators  
**Context**: PostPrimordial complete. Primal mountain debt clearing in Wave 53.
This handoff prepares cellMembrane and gate operators for Wave 54 deployment
stabilization. Glacial shift wave plan at `wateringHole/GLACIAL_SHIFT_WAVE_PLAN.md`.

---

## Upstream Status: CLEAR

- plasmidBin pipeline: `validate` 100/100, `doctor` 35/35, all 14 binaries
  checksummed. `fetch --all --force` pulls complete NUCLEUS.
- K-Derm topology + bonding model standards published to wateringHole.
- primalSpring v0.9.30: 92 experiments, 175/193 certify, zero debt.
- sourDough v0.3.0 harvested and verified.

---

## cellMembrane Action Items

### 1. Second CI Runner on eastGate (HIGH — eliminates SPOF)

ironGate runner is the single point of failure. Deploy a second
`actions-runner` on eastGate. Workflow configs already default to
`self-hosted, linux, x86_64`.

### 2. VPS Nest Expansion (GLACIAL BLOCKER 1)

Deploy Nest primals on `membrane-relay` VPS (157.230.3.183):
- rhizoCrypt (ephemeral DAG)
- loamSpine (permanent ledger)
- sweetGrass (attribution/PROV-O)
- NestGate (network/egress)

Use `plasmidbin fetch --all --force` on VPS, then start Nest primals.
This transforms the VPS from Tower-only to Tower+Nest — enabling
provenance and storage on the outer membrane.

### 3. Sovereign DNS (GLACIAL BLOCKER 2)

Deploy knot-dns on VPS (Channel 1). Replace Cloudflare DNS delegation
for `primals.eco` zone. This is the DNS sovereignty milestone.

### 4. K-Derm Wire Contract (NEW)

Publish to `wateringHole/`:
- `membrane.toml` canonical schema
- Layer placement per primal (which K-Derm layer each primal occupies)
- `BoundaryPolicy` set (what crosses each layer boundary)
- Channel protein definitions

primalSpring will consume `cellmembrane-types` (`EnvelopeTopology`,
`BondType`, `ChannelProtein`) for deploy-graph validation and add an
`s_kderm_boundary` scenario.

---

## Gate Operator Action Items

### SouthGate (after Wave 53 Songbird fix)

Fresh NUCLEUS redeploy:
```
plasmidbin fetch --all --force
plasmidbin launch
```
Target: 13/13 primals, all sockets healthy.
Verify: `SONGBIRD_PEERS=192.168.1.144:7700` (eastGate mesh seed).

### BiomeGate

Restart Songbird with federation:
```
SONGBIRD_FEDERATION_PORT=7700 SONGBIRD_PEERS=192.168.1.144:7700 \
  plasmidbin start songbird
```
Push from 6–9 primals to full 13/13. Verify federation handshake
with eastGate.

---

## Cephalization Prep (primalSpring-owned, FYI to biomeOS)

primalSpring will prototype primal-scoped socket directories (exp113):
- `biomeos/beardog/crypto.sock` instead of `biomeos/crypto.sock`
- Backward compat via symlinks
- Phase A: beardog/ (5 sockets) + barracuda/ (5 sockets)

biomeOS Neural API will need to learn primal-scoped socket discovery
in a future wave. No action needed from biomeOS now — primalSpring
will validate routing first.

---

## Timeline

Wave 54 begins after Wave 53 primal mountain work completes (SouthGate
stability is the gate). Estimated: 1–2 sprints.

Respond with status ack to `wateringHole/handoffs/`.
