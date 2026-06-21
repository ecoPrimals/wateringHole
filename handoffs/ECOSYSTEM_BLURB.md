# ecoPrimals Ecosystem — Wave 120 Unified Blurb

**Date**: Jun 21, 2026 07:31 EDT | **From**: eastGate overwatch
**Wave**: 120 (Sovereign CI + Deployment Isomorphism)
**Cascade**: All repos at parity (origin + forgejo + sporeGate-direct)

---

## Gate Status

| Gate | NUCLEUS | WG | SSH | Role | Hardware |
|------|---------|-----|-----|------|----------|
| **sporeGate** | 13/13 | .2 | ✅ local | Nest provenance + overwatch + **BUILD AUTHORITY** | NUC Ryzen 5 6600H 27GB |
| **eastGate** | 13/13 | .5 | ✅ | Meta (orchestration/AI/viz) | NUC i7 64GB |
| **flockGate** | **13/13** | .6 | ✅ via golgi jump | Tower (trust/discovery/defense) | i9-13900K 62GB (WAN) |
| **ironGate** | — | — | BLOCKED | Node (compute trio) | Pop!_OS i9-12900K |
| **golgi** | 18 svc | .1 | ✅ | VPS hub, Forgejo, WG relay, WAN depot | DO droplet |
| ~~pepti~~ | — | — | — | **DECOMMISSIONED** Wave 120 | Destroyed ($24/mo saved) |

### Offline/Deferred Gates

| Gate | Status | Notes |
|------|--------|-------|
| strandGate | Omada-side, sovereign relay | sporeGate to push sovereign config via RustDesk |
| southGate | Omada-side, sovereign relay | Same |
| swiftGate | Was on Eero WiFi | Blocked until Flint 2 AP live |
| northGate | Windows (A5090) | Hobby/compute — P3 |
| fieldGate | Dead CMOS | Hardware triage low priority |

---

## Sovereign CI Pipeline (NEW — Wave 120)

```
Push to Forgejo (any primal repo)
  → post-receive.d/sovereign-ci (golgi)
  → sovereign-ci-trigger.sh (golgi)
  → SSH sporegate@10.13.37.2 (over WG)
  → /opt/depot/build-local.sh <primal> --sync
  → cargo build --release --target x86_64-unknown-linux-musl
  → /opt/depot/primals/x86_64-unknown-linux-musl/<binary>
  → rsync --checksum to golgi:/opt/ecoPrimals/plasmidBin/primals/
  → Caddy serves at membrane.primals.eco/depot/
  → WAN gates fetch HTTPS, LAN gates fetch direct from sporeGate
```

| Metric | pepti (old) | sporeGate (new) |
|--------|-------------|-----------------|
| Full build | 60–100 min | ~24 min |
| Incremental | 10–20 min | ~2–5 min |
| Cost | $24/mo | $0 (owned hardware) |
| LAN fetch | 30ms (WG overlay) | sub-1ms (direct) |

---

## Atomic Roles & Remaining Work

### flockGate — Tower Atomic (BearDog, Songbird, SkunkBat)

**Status**: 13/13 NUCLEUS. sporePrint 175 tests. Tower team active.

| Task | Priority | Status |
|------|----------|--------|
| BearDog: BTSP trust bootstrap over WAN mesh | P1 | Unblocked |
| Songbird: mesh.init topology-aware routing over WG | P1 | Unblocked |
| SkunkBat: threat detection + defense attestation | P1 | Unblocked |
| sporePrint evolution (v0.3.0 shipped, 222 pages live) | P2 | Ongoing |

### ironGate — Node Atomic (ToadStool, BarraCuda, CoralReef)

**Status**: SSH key auth needed. Assigned: **sporeGate overwatch** (RustDesk access live).

| Task | Priority | Status |
|------|----------|--------|
| RustDesk into ironGate → add SSH key | P0 | Assigned to sporeGate overwatch |
| Deploy NUCLEUS (same flockGate pattern) | P0 | After SSH |
| ToadStool fleet management (S321, 112 methods) | P1 | After NUCLEUS |
| BarraCuda tensor dispatch | P1 | After NUCLEUS |
| CoralReef shader pipelines | P1 | After NUCLEUS |

SSH key to add (via RustDesk terminal on ironGate at 192.168.4.169):
```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILU4i9hEtHJA02/JZ8XR/OHaR/bSiuAaDRMhdJX7zuRp sporegate-gate-v1" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### sporeGate — Nest Atomic + Build Authority + Overwatch

**Status**: Sovereign CI LIVE. Nest provenance END-TO-END. Depot integrity OK.

| Task | Priority | Status |
|------|----------|--------|
| Rootpulse→cascade (DAG→merkle→ledger→witness) | ✅ | Proven (ledger height 3) |
| Sovereign CI pipeline | ✅ | 13/13 primals, Forgejo hooks wired |
| Depot integrity (checksums.toml) | ✅ | 13 verified, 0 mismatch |
| golgi bridge services | ✅ | Fixed (0 failed units, 18 running) |
| ironGate SSH + NUCLEUS enrollment | P0 | Via RustDesk |
| mesh.init (topology-aware routing) | P2 | After ironGate |
| Flint 2 config (after physical install) | P2 | This weekend |
| Omada SX3008F management (http://192.168.4.111, admin/admin) | P2 | Access confirmed |
| strandGate/southGate sovereign relay push | P2 | Via RustDesk |
| pepti decommission | ✅ | DONE — droplet destroyed, $24/mo saved |

### eastGate — Meta Atomic (BiomeOS, Squirrel, PetalTongue)

**Status**: Full NUCLEUS reference. Overwatch + primalSpring evolution.

| Task | Priority | Status |
|------|----------|--------|
| primalSpring scenarios (87 → expand) | P1 | Active (963 lib tests) |
| Overwatch: cascade, review, fossilize, blurb | P1 | Continuous |
| BiomeOS neural-api evolution (8,351 tests, axum 0.8) | P2 | Deep debt done |
| Squirrel AI pipeline + provenance proxy + BTSP switch | P2 | Wired (Wave 119/120) |
| PetalTongue visualization + dashboard | P2 | Ready |

---

## Code Metrics

| Repo | Tests | Status | Latest |
|------|-------|--------|--------|
| **cellMembrane** | 731 | ✅ zero clippy | manifest-driven config gen, gate.validate trust barrier, nftables refactor, dep upgrades |
| **primalSpring** | 963 (87 scenarios) | ✅ | toadStool S321, deep debt sweep, typed errors |
| **sporePrint** | 183+ | ✅ | taxonomy audit, depot tests, tower primal metrics, last expect() eliminated |
| **biomeOS** | 8,351 | ✅ 88% cov | v4.31 structural refactoring |
| **songBird** | 8,929 | ✅ | WG mesh overlay, zero hardcoded names |

---

## VPS Health

| VPS | Disk | Services | Status |
|-----|------|----------|--------|
| golgi | 73% (2.3G free) | Forgejo, WG hub, relay, Caddy, depot (18 svc) | ✅ 0 failed — sole VPS |

pepti decommissioned Wave 120. $24/mo saved. 4-node mesh: golgi ↔ sporeGate ↔ eastGate ↔ flockGate.

---

## Deployment Isomorphism (NEW — Wave 120)

cellMembrane now supports identity-based service discovery and declarative config generation:

### Shipped (Tier 1+2)

| Command | What It Does |
|---------|--------------|
| `membrane topology.service <role>` | Find service by role, not host (returns gate + mesh IP + zone) |
| `membrane topology.roles` | List all role→gate mappings from manifest |
| `membrane wireguard.generate` | Produce wg-quick config from manifest peers |
| `membrane caddy.generate` | Render Caddyfile from manifest roles + topology |

**Upstream action done**: `roles` and `wg_ip` populated in `ecosystem_manifest.toml` for golgi, sporeGate, eastGate, flockGate, ironGate.

### Remaining (Tier 3 — self-healing mesh)

| Item | Priority | Notes |
|------|----------|-------|
| `gate.migrate <role> <from> <to>` | P2 | Orchestrated service migration |
| `gate.bootstrap --absorb <role>` | P2 | Node assumes role including creds |
| Credential portability (bearDog vault) | P2 | Keys stored by role-identity |
| DNS config generation | P3 | `gate.provision --dns` |

---

## Architecture (Post-Decommission)

```
Internet → ATT → sporeGate (NAT/FW/BUILD) → CRS310 (L2) → LAN gates
                      ↕ WireGuard (10.13.37.2)
               golgi VPS (10.13.37.1) — sole VPS
               ├── Forgejo (git.primals.eco)
               ├── WG Hub (4-node mesh)
               ├── Sovereign Relay (hbbs/hbbr)
               ├── Caddy TLS (membrane.primals.eco)
               └── WAN Depot (fed by sporeGate rsync)
```

---

## What's Proven (Wave 116–120 Wins)

- eastGate 13/13 NUCLEUS (user systemd, no sudo)
- sporeGate 13/13 NUCLEUS (system systemd) + **SOVEREIGN BUILD AUTHORITY**
- flockGate **13/13** NUCLEUS (same pattern, WAN gate, Tower team active)
- 4-node WireGuard mesh (golgi hub, pepti decommissioned)
- Nest provenance end-to-end: RhizoCrypt DAG → LoamSpine ledger → SweetGrass witness (height 3)
- Sovereign CI: push → Forgejo hook → sporeGate build → rsync → WAN depot
- Depot integrity: checksums.toml BLAKE3, 13/13 verified
- golgi bridges fixed: 0 failed units, 18 services
- Deep debt across all 13 primals (zero P1, zero known debt)
- sporePrint v0.3.0: 175 tests, 222 pages, P0+P1 shipped
- **pepti decommissioned**: $24/mo saved, build authority on owned hardware
- **Deployment isomorphism Tier 1+2**: identity-based discovery + declarative config gen

---

## Operator-Only (physical presence required)

| Action | Unblocks | When |
|--------|----------|------|
| Flint 2 physical install at Hub 2 | swiftGate, WiFi for Omada-side | This weekend |
| fieldGate CMOS repair | fieldGate enrollment | Low priority |

---

## Corrections (from sporeGate field report)

- Omada SX3008F management IP: **192.168.4.111** (not .115 as whitePaper stated)
- flockGate: now **13/13** (Tower team fixed NestGate + BiomeOS overnight)
