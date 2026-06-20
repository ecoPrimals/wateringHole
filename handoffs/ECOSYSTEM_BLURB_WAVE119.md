# ecoPrimals Ecosystem — Wave 119 Unified Blurb

**Date**: Jun 20, 2026 | **From**: eastGate overwatch
**Wave**: 119 (Convergence & Final Enrollment)
**Cascade**: All repos at parity (origin + forgejo + sporeGate-direct)

---

## Gate Status

| Gate | NUCLEUS | WG | SSH | Role | Hardware |
|------|---------|-----|-----|------|----------|
| **sporeGate** | 13/13 | .2 | ✅ local | Nest provenance + overwatch | NUC (LAN firewall) |
| **eastGate** | 13/13 | .5 | ✅ | Meta (orchestration/AI/viz) | NUC i7 64GB |
| **flockGate** | 11/13 | .6 | ✅ via golgi jump | Tower (trust/discovery/defense) | i9-13900K 62GB (WAN) |
| **ironGate** | — | — | BLOCKED | Node (compute trio) | Pop!_OS, SSH not yet keyed |
| **golgi** | 13/13 | .1 | ✅ | VPS hub, Forgejo host, WG relay | DO droplet |
| **pepti** | 13/13 | .4 | ✅ | Build authority, depot | DO droplet |

### Offline/Deferred Gates

| Gate | Status | Notes |
|------|--------|-------|
| strandGate | Omada-side, sovereign relay | Needs push of sovereign RustDesk config |
| southGate | Omada-side, sovereign relay | Same |
| swiftGate | Was on Eero WiFi | Blocked until Flint 2 AP live |
| northGate | Windows (A5090) | Hobby/compute — after Linux NUCLEUS proven |
| fieldGate | Dead CMOS | Hardware triage when operator has time |

---

## Atomic Roles & Remaining Work

### flockGate — Tower Atomic (BearDog, Songbird, SkunkBat)

**Status**: 11/13 LIVE. Ready for Tower team IDE work.

| Task | Priority | Status |
|------|----------|--------|
| Open IDE, run `temporal.cascade` (6 repos drifted) | P0 | Ready |
| BearDog: BTSP trust bootstrap over WAN mesh | P1 | Unblocked |
| Songbird: mesh.init topology-aware routing over WG | P1 | Unblocked |
| SkunkBat: threat detection + defense attestation | P1 | Unblocked |
| Fix NestGate (add `NESTGATE_JWT_SECRET`, same as eastGate) | P2 | Pattern documented |
| Fix BiomeOS (use `neural-api` subcommand, same as eastGate) | P2 | Pattern documented |

### ironGate — Node Atomic (ToadStool, BarraCuda, CoralReef)

**Status**: SSH key auth needed. **Assigned: sporeGate overwatch** (RustDesk access live).

| Task | Priority | Status |
|------|----------|--------|
| RustDesk into ironGate → add SSH key | P0 | Assigned to sporeGate overwatch |
| Deploy NUCLEUS (same flockGate pattern) | P0 | After SSH |
| ToadStool fleet management (112 methods, S320+) | P1 | After NUCLEUS |
| BarraCuda tensor dispatch | P1 | After NUCLEUS |
| CoralReef shader pipelines | P1 | After NUCLEUS |

SSH key to add (via RustDesk terminal on ironGate):
```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILU4i9hEtHJA02/JZ8XR/OHaR/bSiuAaDRMhdJX7zuRp sporegate-gate-v1" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### sporeGate — Nest Atomic (NestGate, RhizoCrypt, LoamSpine, SweetGrass)

**Status**: Provenance pipeline END-TO-END PROVEN.

| Task | Priority | Status |
|------|----------|--------|
| Rootpulse→cascade workflow (DAG→merkle→ledger→witness) | ✅ | Wired and proven |
| Continue periodic ledger commits on each wave | P1 | Ongoing |
| checksums.toml for depot (fixes DEGRADED probe) | P2 | Need `plasmid.harvest` |
| Flint 2 physical swap (replaces Eero at Hub 2) | P2 | This weekend |
| ironGate enrollment (after operator keys) | P1 | Awaiting operator |
| Omada SX3008F config (http://192.168.4.115, admin/admin) | P2 | UNBLOCKED — creds in whitePaper |

### eastGate — Meta Atomic (BiomeOS, Squirrel, PetalTongue)

**Status**: Full NUCLEUS reference node. Overwatch + primalSpring evolution.

| Task | Priority | Status |
|------|----------|--------|
| primalSpring scenarios (85 → expand coverage) | P1 | Active |
| Overwatch: cascade, review, fossilize, blurb | P1 | Continuous |
| BiomeOS neural-api evolution (8,351 tests, axum 0.8) | P2 | Deep debt done |
| Squirrel AI pipeline + provenance tracking | P2 | Ready |
| PetalTongue visualization + dashboard | P2 | Ready |

---

## Code Metrics

| Repo | Tests | Status | Latest |
|------|-------|--------|--------|
| **cellMembrane** | 680 | ✅ zero clippy | rootpulse, webhook cascade, SSH consolidation |
| **primalSpring** | 959 (85 scenarios) | ✅ | deep debt sweep, toadStool S320+ |
| **sporePrint** | builds clean | ✅ | P0 sitemap, P1 glossary + deployment docs |
| **biomeOS** | 8,351 | ✅ 88% coverage | axum 0.8, module split, deep debt |

---

## VPS Health

| VPS | Disk | Key Service | Status |
|-----|------|-------------|--------|
| golgi | 73% (2.6G free) | Forgejo, WG hub, relay | ✅ HEALTHY (beardog+biomeos bridges FAILED — P2) |
| pepti | OK | Build depot, cascade hub | ✅ SSH→Forgejo FIXED (remote URLs corrected) |

---

## Cascade Topology

```
Gates → push to Forgejo (git.primals.eco:2222)
pepti → pull from Forgejo → build fresh binaries → depot
GitHub ← bidirectional sync with Forgejo (mirror)
sporeGate-direct ← LAN push from eastGate (validation)
```

---

## What's Proven (Wave 116–119 Wins)

- eastGate 13/13 NUCLEUS (user systemd, no sudo)
- sporeGate 13/13 NUCLEUS (system systemd)
- flockGate 11/13 NUCLEUS (same pattern, WAN gate)
- 5-node WireGuard mesh (golgi hub, all handshakes < 2min)
- Nest provenance end-to-end: RhizoCrypt DAG → LoamSpine ledger → SweetGrass witness
- pepti SSH→Forgejo fixed (wrong remote URLs, 37 repos corrected)
- Deep debt across all 13 primals (zero P1, zero known debt)
- sporePrint P0+P1 shipped (222 pages, K-Derm glossary, sovereign deployment)
- Cascade pipeline: Forgejo direct as production push path

---

## Agentic Tasks (assign to subteams)

These were previously "operator" but can be handled by agents with existing access:

| Task | Assign To | Access Path | Unblocks |
|------|-----------|-------------|----------|
| ironGate SSH key auth | sporeGate overwatch | RustDesk into ironGate (sovereign relay live) | Node atomic enrollment |
| flockGate: NestGate JWT secret | flockGate Tower team | SSH via golgi jump (`ssh flockgate`) | 12/13 → 13/13 |
| flockGate: BiomeOS `neural-api` unit fix | flockGate Tower team | SSH via golgi jump | 12/13 → 13/13 |
| flockGate: VCS cascade (6 repos drifted) | flockGate Tower team | SSH → `git fetch --all` per repo | Code parity |
| checksums.toml on depot | sporeGate overwatch | SSH to pepti (`ssh root@10.13.37.4`) | depot.integrity OK |
| golgi bridge services fix (beardog+biomeos) | sporeGate overwatch | SSH to golgi (`ssh root@10.13.37.1`) | VPS health |
| pepti fresh build from HEAD | sporeGate overwatch | SSH to pepti → `plasmid.harvest` | Fresh binaries in depot |
| strandGate sovereign relay push | sporeGate overwatch | RustDesk (on sovereign relay) | strandGate enrollment |
| southGate sovereign relay push | sporeGate overwatch | RustDesk (on sovereign relay) | southGate enrollment |
| Omada SX3008F management | sporeGate overwatch | http://192.168.4.115 — admin/admin | VLAN config, port control |

### ironGate Key Auth (sporeGate overwatch)

ironGate is on sovereign relay. RustDesk into it and run:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILU4i9hEtHJA02/JZ8XR/OHaR/bSiuAaDRMhdJX7zuRp sporegate-gate-v1" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Then from sporeGate: `ssh irongate@192.168.4.169` → deploy NUCLEUS (same flockGate pattern).

### flockGate 13/13 (flockGate Tower team)

Pattern proven on eastGate. From your IDE on flockGate:

```bash
# NestGate JWT:
openssl rand -base64 48 > ~/.config/membrane/nestgate-jwt-secret
chmod 600 ~/.config/membrane/nestgate-jwt-secret
echo "NESTGATE_JWT_SECRET=$(cat ~/.config/membrane/nestgate-jwt-secret)" > ~/.config/membrane/nestgate.env

# Create systemd unit for nestgate with --port 8092 --socket
# Create systemd unit for biomeos with 'neural-api' subcommand
# See eastGate pattern in ~/.config/systemd/user/membrane-nucleus@{nestgate,biomeos}.service
```

---

## Operator-Only (physical presence required)

| Action | Unblocks | When |
|--------|----------|------|
| Flint 2 physical install at Hub 2 | swiftGate, WiFi for Omada-side | This weekend |
| fieldGate CMOS repair | fieldGate enrollment | Low priority |

---

## What NOT to Touch

- **northGate**: Windows hobby (5090). P3. After Linux proven.
- **ATT passthrough**: Operator handles WAN config.
- **golgi Forgejo DB**: Fixed, don't touch unless breakage recurs.
