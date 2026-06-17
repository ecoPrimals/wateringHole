# Wave 115 — Sovereign Mesh & Gate Hardening

**Status**: ACTIVE | **From**: eastGate overwatch | **Date**: 2026-06-16
**Last review**: Jun 17 16:15 EDT (Omada controller installed, eastGate SSH live — sporeGate overwatch)

---

## Objective

Agents work continuously on live systems. Evolve code, validate deployments,
harden mesh. Offline hardware returns when physical ops completes.

---

## Teams & Systems

### eastGate — primalSpring Evolution + NUCLEUS (this IDE)

| Focus | Detail |
|-------|--------|
| **primalSpring** | Validation scenarios, evolution modules, genetics compliance |
| **NUCLEUS** | Local 13/13 primals, atomic model tests, gate readiness |
| **Overwatch** | Cascade review, cross-team coordination, FRAGO/blurb updates |

### sporeGate Overwatch — LAN/WAN/VPS Topology Exploration (Cursor on NUC)

*Dedicated subteam like biomeGate (GPU eras) but for network sovereignty.*
*The sporeGate NUC IS the exploration ground for our LAN/WAN topology.*

| Focus | Detail |
|-------|--------|
| **Plasma membrane** | nftables from composition, NAT, DHCP, DNS, WireGuard overlay |
| **LAN fabric** | CRS310, Omada SX3008F, TL-SG605S, Eero mesh management |
| **Gate deployment** | `gate.preflight` → `sovereign-relay-push.sh` → NUCLEUS install |
| **Topology exploration** | Cytoplasm zones, multi-site links, VLAN segmentation |
| **Hardware solving** | Omada SDN mode, ATT passthrough, Eero bridge, cable runs |

### cellMembrane Team — Code + VPS (Cursor on sporeGate, separate IDE)

| Focus | Detail |
|-------|--------|
| **cellMembrane code** | firewall.rs, preflight, cascade, webhook, relay |
| **VPS management** | golgi (Forgejo, relay), pepti (builds, depot) |
| **Cascade pipeline** | Forgejo → GitHub sync, depot integrity, multi-arch harvest |
| **Sovereignty shadows** | Evolve S1-S4 tracks toward full sovereign |

### Infrastructure

| System | Owner | Status |
|--------|-------|--------|
| **golgi** | cellMembrane team (SSH) | HEALTHY — 13/13, relay, Forgejo |
| **pepti** | cellMembrane team (SSH) | Build authority, depot, both arches |
| **northGate** | sporeGate overwatch | RustDesk reachable, NUCLEUS pending |
| **House 2 gates** | sporeGate overwatch | ACCESSIBLE (Eero backhaul) |
| **flockGate** | sporeGate overwatch | WAN, public relay → sovereign push pending |
| **fieldGate** | — | OFFLINE (dead CMOS, hardware surgery) |
| **Omada SX3008F** | sporeGate overwatch | **UNBLOCKED** — see access instructions below |

---

## Ecosystem Snapshot (Jun 17 15:35 EDT — full cascade)

| Metric | Value |
|--------|-------|
| Genetics | **11/11 ✅** all primals accept mito-beacon |
| Depot x86_64 | **13/13** from HEAD (pepti Jun 16) |
| Depot aarch64 | **13/13** (pepti Jun 15) |
| VCS parity | **17/17** zero drift — all remotes synced |
| cellMembrane | **527 tests**, zero lint, async-first API, error module, hardcode elimination |
| WireGuard mesh | **3/3 nodes LIVE** — golgi (10.13.37.1) ↔ sporeGate (.2) ↔ pepti (.4) |
| golgi | **HEALTHY** — 13/13, relay, Forgejo, WireGuard hub |
| pepti | **HEALTHY** — build authority, WireGuard peer, depot |
| sporeGate | **13/13 ALIVE** — K-Derm nftables live, WireGuard, cytoplasm zones mapped |
| eastGate | **LIVE** — 10G SFP+, primalSpring + overwatch. **⚠️ SSH needs openssh-server** |
| northGate | RustDesk reachable — **⚠️ SSH needs openssh-server**, NUCLEUS pending |
| Omada SX3008F | **Data plane LIVE** (L2 works), mgmt plane unreachable (SDN mode) |
| House 2 | Devices on L2 — SSH required for remote management |
| Cytoplasm zones | **3 zones** defined: backbone, house2, eero_wifi (TOPOLOGY_MAP v4.0.0) |
| fieldGate | **OFFLINE** — DDR3 NUC, dead CMOS |

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

## Omada Access — SDN CONTROLLER INSTALLED (sporeGate Jun 17 16:10)

**Data plane WORKS** — devices behind Omada are reachable on 192.168.4.x. L2 forwarding confirmed.
**SDN Controller INSTALLED** — Omada Controller v5.15.24.19 running on sporeGate (Java 17 + MongoDB 7.0).
**Web UI**: `https://192.168.4.1:8043` (accessible from any LAN device).
**Status**: `configured: false` — needs initial browser wizard to create admin account and site.

**Likely cause**: Omada SX3008F is in "SDN Controller Managed" mode (factory default for
newer firmware). The standalone web UI is disabled when no controller is detected OR the
switch expects management on a dedicated VLAN/IP range.

**Resolution paths** (sporeGate overwatch to try):

```bash
# Path 1: Try management IP range (Omada defaults vary by firmware)
curl -kI https://10.0.4.1 2>&1 | head -5
curl -kI http://192.168.0.1 2>&1 | head -5  # some Omada default

# Path 2: Install TP-Link Omada SDN controller on sporeGate (discovers switches on L2)
# This gives full managed control — VLANs, port config, monitoring
# apt install default-jre && download Omada Controller .deb from TP-Link

# Path 3: Factory reset the Omada (press reset button 5s) to force standalone mode
# Then browse http://<dhcp-assigned-ip> with admin/admin

# Path 4: Connect laptop directly to Omada port, set static 192.168.0.x, try web UI
```

**Credentials confirmed** (from sticker, stored in `whitePaper/technical/HARDWARE_INVENTORY.md`):
- Default login: `admin` / `admin`
- MAC: EC-75-0C-4C-98-08
- Device Key: 1E73-A4FF-F547-8EC5-8000

### ATT BGW320-500 (when ready to eliminate double-NAT)

```bash
# Admin UI: http://192.168.1.254
# Device Access Code: #283>#66<>
# Goal: IP passthrough to sporeGate's enp1s0 MAC
# This makes sporeGate the SOLE boundary (true plasma membrane)
```

### SSH Enablement (OPERATOR — unblocks everything)

```bash
# On eastGate (this machine):
sudo apt install -y openssh-server

# On northGate (via RustDesk session):
sudo apt install -y openssh-server

# Then add sporeGate's pubkey to each:
# (sporeGate can push its key once SSH is listening)
```

---

## Waiting on Physical Ops (not blocking agent work)

| Item | Blocker | Action When Ready |
|------|---------|-------------------|
| Omada controller wizard | **Controller running, needs browser setup** | Browse `https://192.168.4.1:8043`, create admin, adopt SX3008F |
| Eero NAT collapse | Operator has Eero app access | See Eero Collapse Plan below |
| ATT IP passthrough | **UNBLOCKED** (Device Access Code available) | sporeGate: eliminate double-NAT |
| House 2 gate enrollment | **UNBLOCKED** (operator confirms access) | sporeGate: sovereign-relay-push.sh + NUCLEUS deploy |
| fieldGate | Dead CMOS, open-air NUC | Repurpose old-gen hardware when viable |
| Additional NUCs | Operator acquires from various gens | Plug into CRS310, bootstrap |

### Eero NAT Collapse Plan (Operator Task)

**Problem**: Eeros run their own DHCP/NAT on `10.0.7.0/24`, creating an invisible sub-membrane within the cytoplasm. WiFi clients can't reach LAN gates directly, and the zone model has a hidden NAT boundary.

**Goal**: Collapse to flat `192.168.4.x` so all WiFi clients get DHCP from sporeGate, same as wired gates. The `eero_wifi` zone becomes a pure L2 bridge, no NAT.

**Steps**:
1. Open the Eero app (phone, operator access required)
2. Set Eero network mode to **Bridge** (AP-only mode)
   - Settings → Advanced → DHCP & NAT → Bridge mode
   - This disables Eero's DHCP server and NAT
3. Eero will relay on CRS310's L2 fabric — WiFi clients get `192.168.4.x` from sporeGate DHCP
4. Verify: WiFi clients should get `192.168.4.1` as gateway and DNS
5. Update `TOPOLOGY_MAP.toml`: change `[cytoplasm.zones.eero_wifi]` status from `"collapsing"` to `"bridged"`, remove `nat_subnet`

**Risk**: Low. Eero bridge mode is documented and reversible via the app. If WiFi breaks, revert to router mode.

**Result**: Cytoplasm simplifies to two clean zones: `backbone` (CRS310) and `house2` (Omada). WiFi is transparent L2.

---

### Shipped (sporeGate confirmed Jun 16 22:48)

- [x] 13/13 primals alive + systemd persisted (membrane-nucleus.target)
- [x] Cascade verified: push/pull both remotes clean
- [x] VPS SSH: golgi confirmed, pepti confirmed (IP provided)
- [x] RustDesk sovereign relay configured + hairpin fixed
- [x] FAMILY_SEED + secrets installed
- [x] Mesh connected (1 peer reachable: golgiBody)
- [x] HPC characterization document filed

### Shipped (cellMembrane IDE Jun 17 15:10)

- [x] Hardcode elimination: 13 sites migrated to named constants (relay paths, Forgejo paths, caddy-tls, WAN/LAN ifaces, subnet, WG port, systemd dir, secrets path)
- [x] 9 new constants in `cellmembrane-types`: relay config, Forgejo paths, caddy unit, iface hints, subnet, systemd, secrets
- [x] Capability-derived: bootstrap relay dir + credentials use `binary_for(TurnServer)`
- [x] `songbird_unit` → `relay_unit` (agnostic naming in bootstrap)
- [x] `unreachable!()` → `expect()` in ribocipher HMAC-SHA256 init
- [x] +12 tests: gate/local (4), lib (5), ssh (3) → **527 tests**

### Shipped (cellMembrane IDE Jun 17 14:45)

- [x] Async-first API layer: `load_async()` + `load_from_workspace_async()` + `resolve_async()` + `read_freshness_wave_id_async()`
- [x] All dispatch boundaries now use native async I/O (manifest, identity, freshness, depot)
- [x] `dispatch_manifest` + `dispatch_identity` upgraded to `async fn`
- [x] 7 identity::resolve callers migrated to async (impulse/post, ack, sync + context/weave, clear + temporal)
- [x] depot `compute_blake3_file` — `tracing::warn` on read failure (was silent empty hash)
- [x] `gardens/cellMembrane` hardcoding eliminated from config.rs TOML search paths
- [x] Deep async I/O sweep: canary pool/remote registry → tokio::fs (12 async call sites), sandbox spin_up → tokio::fs, fetch checksums → spawn_blocking, health probe → spawn_blocking
- [x] `tracing-subscriber` wired in main.rs (WARN default, `RUST_LOG` override for operational logs)
- [x] Error observability: 8 high-risk silent error drops now surface via `tracing::warn!`/`debug!` (refresh rollback, caddy rollback, temporal recovery, depot sync)
- [x] `INFRA_WATERING_HOLE` / `INFRA_PLASMID_BIN` constants centralized (12 call sites migrated)
- [x] `binary_for()` hardcoded primal name fallbacks removed — registry-only
- [x] Display strings in health.rs/data.rs now capability-derived (no hardcoded `BearDog`/`NestGate`)
- [x] Clone elimination: identity.rs, gate.rs, preflight.rs
- [x] +20 tests: jsonrpc (4), error (9), impulse/parse (6), manifest (1) → **515 tests**
- [x] 515 tests, zero clippy (pedantic+nursery), zero fmt, zero doc warnings

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
| async I/O deep sweep | canary pool+remote registry→tokio::fs, sandbox spin_up→tokio::fs, fetch checksums→spawn_blocking, health probe→spawn_blocking |
| tracing-subscriber | CLI operational logs (WARN default, RUST_LOG override) |
| error observability | 8 high-risk silent error drops surfaced via tracing::warn!/debug! |
| constant centralization | SSH aliases, NestGate port, `INFRA_WATERING_HOLE`, `INFRA_PLASMID_BIN`, composition `parse_name()` |
| hardcode elimination | `binary_for()` registry-only, display names capability-derived, path fragments centralized |
| async-first API | `load_async()`, `load_from_workspace_async()`, `resolve_async()`, `read_freshness_wave_id_async()` |
| dispatch async upgrade | `dispatch_manifest` + `dispatch_identity` → `async fn`, all dispatch boundaries native async |
| test expansion (final) | 495 → 515 tests (jsonrpc, error, impulse/parse) |

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
| **Cytoplasm zones** | `TOPOLOGY_MAP.toml` now defines backbone (CRS310) + house2 (Omada) + eero_wifi zones with hub devices, uplinks, speeds |
| **Gate zone annotations** | 4 gate profiles (sporeGate, eastGate, fieldGate, northGate) annotated with `zone`, `hub_port`, `link_speed_mbps` |
| **GateProfile zone fields** | Surgical `manifest.rs` edit: 3 `Option` fields, serde-default, backward compatible, test passing |
| **Cytoplasm spec handoff** | `CYTOPLASM_ZONES_SPEC.md` → cellMembrane team: `CytoplasmZone` types, `topology.resolve`, zone-aware preflight |
| **Eero collapse plan** | NAT collapse documented — bridge mode via Eero app, flat 192.168.4.x for all WiFi clients |

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
