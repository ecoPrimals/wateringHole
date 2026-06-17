# Wave 115 — Sovereign Mesh & Gate Hardening

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-16
**Last review**: Jun 17 13:45 EDT

---

## Objective

Agents work continuously on live systems. Evolve code, validate deployments,
harden mesh. Offline hardware returns when physical ops completes.

---

## Live Systems (agents always working)

| System | IDE | Local Teams | Focus |
|--------|-----|-------------|-------|
| **eastGate** | Cursor (this) | overwatch + primalSpring + NUCLEUS | Validate ecosystem, evolve primalSpring, run local primals |
| **sporeGate** | Cursor on NUC | cellMembrane IDE + LAN hardware | Code evolution, VPS mgmt, LAN routing, cascade, depot |
| **golgi** | managed by sporeGate SSH | — | Forgejo, relay, mesh hub (13/13 alive) |
| **pepti** | managed by sporeGate SSH | — | Build authority, depot generation |

## Offline / Pending (not blocking)

| System | Status | Returns When |
|--------|--------|--------------|
| **fieldGate** | DDR3 NUC, dead CMOS, open-air surgery | Operator finishes hardware. Old-gen repurpose TBD. |
| **northGate** | RustDesk reachable, NUCLEUS pending | sporeGate team deploys when ready |
| **Omada** | Controller access pending | Operator provides password (soon) |
| **flockGate** | WAN, on public relay | sporeGate migrates via SSH from golgi |

---

## Ecosystem Snapshot (Jun 17 09:45 EDT)

| Metric | Value |
|--------|-------|
| Genetics | **11/11 ✅** all primals accept mito-beacon |
| Depot x86_64 | **13/13** from HEAD (pepti Jun 16) |
| Depot aarch64 | **13/13** (pepti Jun 15) |
| VCS parity | **17/17** zero drift — both remotes synced |
| cellMembrane | **495 tests**, zero lint, nftables gen, gate.preflight, async I/O sweep shipped |
| golgi | **HEALTHY** — 13/13, relay ACTIVE, depot serving |
| sporeGate | **13/13 ALIVE** — systemd persisted, cascade verified, VPS SSH confirmed |
| eastGate | **LIVE** — 10G SFP+ to CRS310, primalSpring + overwatch |
| northGate | RustDesk reachable — NUCLEUS deploy pending (sporeGate) |
| fieldGate | **OFFLINE** — DDR3 NUC, dead CMOS, hardware surgery |

---

## Active Work (live systems — agents always evolving)

### eastGate — Overwatch + primalSpring

- [ ] primalSpring validation scenarios (bootstrap readiness, genetics compliance)
- [ ] NUCLEUS local execution and testing
- [ ] Ecosystem convergence monitoring (cascade drift detection)
- [ ] Review incoming evolution from sporeGate + cellMembrane teams
- [ ] Coordinate cross-team alignment via FRAGO updates

### sporeGate — cellMembrane Code + VPS + LAN

*Two concerns: code evolution (cellMembrane IDE) and LAN hardware (sporeGate NUC)*

#### Code (cellMembrane IDE on sporeGate)

- [ ] Cascade pipeline: wire webhook.rs to push to GitHub (partial Forgejo handler exists)
- [ ] GitHub → Forgejo sync (bidirectional event-driven cascade)
- [ ] `plasmid.harvest` multi-arch pipeline (pepti=x86_64, need aarch64 path)
- [ ] Consolidate golgi's 3 depot paths → single canonical
- [ ] Replace `deploy_membrane.sh` → Rust `plasmid.refresh`
- [ ] `membrane gate.discover` + `remote.configure` (greenfield commands)
- [ ] Pepti: deploy Tower Atomic for self-validation

#### LAN Hardware (sporeGate NUC)

- [x] **K-Derm plasma membrane convergence**: `firewall.generate --plasma-membrane` ships nftables from `FirewallRuleset::for_composition()` ✅
- [ ] northGate NUCLEUS deploy (SSH in, install, start primals, mesh)
- [ ] WireGuard overlay activation (golgi hub first, then site routers)
- [ ] Multi-site topology evolution (House 2 link when ready)
- [ ] ATT BGW320 IP passthrough (eliminate double-NAT when admin access available)

---

## Sovereign Relay Push (remote, no physical access)

All Omada-side devices and flockGate are still on the public relay. Fix remotely:

| Path | Method | Script |
|------|--------|--------|
| **LAN wired (Omada side)** | SSH from sporeGate (same L2, 192.168.4.x) | `sovereign-relay-push.sh lan` or `discover` |
| **flockGate (WAN)** | SSH hop through golgi | `sovereign-relay-push.sh wan` |
| **WiFi clients (Eero)** | Use existing public relay connection to push sovereign config | Manual RustDesk session → run config command |

**Key insight**: Omada is L2 — it doesn't block anything. sporeGate can SSH directly to
any wired device. The public relay is a bootstrap path: use it to eliminate itself.

Script: `wateringHole/compute-sharing/sovereign-relay-push.sh [lan|discover|wan|all]`

---

## Waiting on Physical Ops (not blocking agent work)

| Item | Blocker | Action When Ready |
|------|---------|-------------------|
| Omada controller audit | admin/admin (confirmed from sticker) — no blocker! | sporeGate: log in, verify no VLAN isolation |
| Eero bridge mode | Eero app access | Collapse WiFi to 192.168.4.x (sporeGate DHCP for all) |
| fieldGate | Dead CMOS, open-air NUC | Repurpose old-gen hardware when viable |
| ATT IP passthrough | Gateway admin access (#283>#66<>) | sporeGate: eliminate double-NAT |
| Additional NUCs | Operator acquires from various gens | Plug into CRS310, bootstrap |

---

### Shipped (sporeGate confirmed Jun 16 22:48)

- [x] 13/13 primals alive + systemd persisted (membrane-nucleus.target)
- [x] Cascade verified: push/pull both remotes clean
- [x] VPS SSH: golgi confirmed, pepti confirmed (IP provided)
- [x] RustDesk sovereign relay configured + hairpin fixed
- [x] FAMILY_SEED + secrets installed
- [x] Mesh connected (1 peer reachable: golgiBody)
- [x] HPC characterization document filed

### Shipped (cellMembrane IDE Jun 17 13:45)

- [x] K-Derm nftables generation: `FirewallRuleset::to_nftables_script()` — full `nft -f` idempotent output
- [x] `NftablesConfig` struct: WAN/LAN ifaces, NAT masquerade, DHCP, trusted LAN, WireGuard overlay, IPv6 forward drop
- [x] `membrane firewall.generate` dispatch — `--format nftables|ufw`, `--plasma-membrane`, `--wan/--lan/--subnet` flags
- [x] `membrane gate.preflight` — pre-deployment scanner (interface detection, IP conflicts, port 53, NM, IPv6)
- [x] Interface auto-detection by driver/speed/carrier via sysfs + ip-json, WAN/LAN role classification
- [x] SSH alias centralization: `DEFAULT_SSH_ALIAS` / `DEFAULT_SSH_ALIAS_EXT` / `DEFAULT_PEPTI_SSH_ALIAS`
- [x] `DEFAULT_NESTGATE_PORT` constant extracted
- [x] `MembraneComposition::parse_name()` for CLI parsing
- [x] Async I/O sweep: sandbox teardown, canary kill, fetch, harvest, refresh, impulse archive → tokio::fs/spawn_blocking
- [x] 495 tests (was 487), zero clippy, zero fmt, zero doc warnings

### Shipped (cellMembrane IDE Jun 17 07:39)

- [x] Deep debt evolution (86e9435): 412 tests passing, 60 net new
- [x] Zero clippy pedantic+nursery, zero fmt, zero doc warnings
- [x] ~70 eprintln! → tracing structured logging
- [x] SPDX headers on all specs + scripts + systemd units
- [x] `ring` banned in deny.toml, cargo-deny CI gate added
- [x] Hardcoded ports/paths → capability-based registry lookups
- [x] ribocipher constants public with ALL arrays
- [x] gate/bootstrap.rs refactored (split extra_exec_args + generate_unit_content)
- [x] All files under 800 LOC, all `as` casts → try_from/millis_u64
- [x] Zero-copy temporal layer (bf54650): Arc manifest, Cow defaults, pre-computed refs
- [x] sporeGate Forgejo remote fixed (HTTPS → SSH, host key added)

---

## cellMembrane Code Evolution SHIPPED (Wave 113–115)

| What | Detail |
|------|--------|
| bootstrap refactor | `gate/bootstrap.rs` 861L → 555L: `nucleus.rs` (228L), `mesh.rs` (138L) extracted |
| spawn_blocking | All sync fs phases (permissions, identity, install, nucleus, mobility, deploy) moved to `spawn_blocking` via `blocking_phase` helper |
| per-phase timeouts | 120s `tokio::time::timeout` on every bootstrap phase |
| identity detection | `identity.git` phase detects missing git config + SSH key |
| depot.integrity | `membrane depot.integrity` command: BLAKE3 checksums generate/verify |
| safe casts | All `as` casts → `usize::try_from()` / `usize::from()` / `.to_le_bytes()[0]` |
| zero .expect() | All production `.expect()` → proper error handling |
| env-driven config | SSH user (`MEMBRANE_PROVISION_SSH_USER`), Caddy admin (`CADDY_ADMIN_ENDPOINT`), config/socket/install paths |
| lint tightening | `option_if_let_else` promoted from allow → warn, all instances resolved |
| zero-copy | `Arc<EcosystemManifest>` in cascade, `Cow<'static, str>` relay defaults, pre-computed remote refs |
| SPDX headers | All .rs, .sh, .md, .service, .timer, .target files carry SPDX license identifier |
| cargo-deny CI | `deny.toml` with ring ban + Forgejo CI job |
| test expansion | 416 → 495 tests (nucleus, mesh, verify, service, types, resolve, nftables, preflight) |
| dependency audit | All pure Rust except ring (via reqwest→rustls), feature-gated, tracked |
| K-Derm nftables | `to_nftables_script()` + `NftablesConfig` (NAT, DHCP, WireGuard, IPv6 drop, trust-LAN) |
| gate.preflight | Pre-deployment scanner: interface detect, IP conflicts, port 53, NM, IPv6 forwarding |
| async I/O sweep | sandbox/canary/fetch/harvest/refresh/impulse archive → tokio::fs + spawn_blocking |
| constant centralization | SSH aliases, NestGate port, composition `parse_name()` |

---

## Shipped This Wave (so far)

| What | Detail |
|------|--------|
| sporeGate FULL ONBOARD | 13/13 systemd persisted, cascade verified, VPS SSH, mesh, secrets |
| RustDesk relay | golgi hbbs/hbbr ACTIVE, hairpin NAT fixed, one-command config |
| MikroTik gates connected | eastGate, northGate, sporeGate all on sovereign relay |
| Team split | sporeGate=LAN hardware, cellMembrane IDE=code+VPS, ironGate=ABG |
| VPS access | sporeGate SSH to golgi + pepti confirmed |
| Dual-channel handoff | USB kit + Git push active |
| Full documentation | AAR, topology, onboarding blurb, FRAGO response from sporeGate |
| **Hardware inventory** | All LAN devices cataloged in `whitePaper/technical/HARDWARE_INVENTORY.md` with K-Derm layer mapping |
| **K-Derm ↔ hardware** | Physical topology mapped to envelope model — sporeGate = plasma membrane, L2 fabric = cytoplasm |

---

## Carry (Wave 116+)

| Debt | Owner | Priority |
|------|-------|----------|
| ATT passthrough (double NAT) | sporeGate (hardware) | P2 |
| aarch64 fresh harvest | cellMembrane team (pepti) | P2 |
| IPv6 with proper NAT66/PD | sporeGate (hardware) | P3 |
| VLAN segmentation | sporeGate (hardware) | P3 |
| Version tag hygiene | cellMembrane team | P3 |
| Nuclear lineage per-user | bearDog/overwatch | P3 |
| LAN-local hbbs relay | sporeGate (hardware) | P3 |

---

## Architecture (K-Derm Envelope)

The physical topology maps 1:1 to the K-Derm cell envelope model
(`whitePaper/technical/HARDWARE_INVENTORY.md` has full device specs + PII).

```
 EXTRACELLULAR     Internet (Dark Forest, weak bonds)
       │
 WAN boundary      ATT BGW320-500 (192.168.1.254) ─── Fiber ONT
       │
 OUTER MEMBRANE    golgi (Forgejo, hbbs/hbbr relay)
                   pepti (build authority, depot)
       │
 PERIPLASM         WireGuard overlay (10.13.37.0/24), cascade pipeline
       │
 ╔══════════════════════════════════════════════════════════════╗
 ║ PLASMA MEMBRANE   sporeGate nftables/NAT/DHCP/DNS          ║
 ║                   FirewallRuleset::for_composition()        ║
 ║                   Channel proteins = nftables rules         ║
 ╚══════════════════════════════════════════════════════════════╝
       │
 CYTOPLASM         CRS310 (L2 backbone, 10G) ─┬─ sfp+1 → Omada SX3008F (L2+)
                                              ├─ sfp+2 → eastGate (10G compute)
                                              ├─ ether2 → Eero 6 (WiFi bridge)
                                              └─ ether8 ← sporeGate eno1

                   TL-SG605S-M2 (2.5G expansion, off Omada)
                   All NUCLEUS processes (13 primals per gate)
```

**sporeGate team**: Plasma membrane (nftables), LAN hardware, routing, DHCP, Omada/Eero, gate deploys
**cellMembrane team**: Code evolution, VPS (golgi+pepti), cascade pipeline, depot, Forgejo
**Co-evolution**: sporeGate deploys what cellMembrane builds. `firewall.rs` generates nftables from composition → sporeGate applies them live.

RustDesk relay: `157.230.3.183` | One-command config:
```
pkexec rustdesk --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"
```
