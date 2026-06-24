<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Flint 2 #2 — House 1 WiFi Provisioning Plan

**Date**: June 24, 2026
**Wave**: 126
**Hardware**: GL.iNet Flint 2 (GL-MT6000)
**Site**: House 1 (4422 Southgate Ave)
**Goal**: Own all radio. ATT BGW320 becomes pure ethernet WAN ingress.

---

## Physical Wiring — Redundant Topology

### Port Inventory

| Device | Port 1 | Port 2 | Notes |
|--------|--------|--------|-------|
| **sporeGate** | enp1s0 (2.5G) → ATT WAN | eno1 (2.5G) → CRS310 | Both 2.5G RJ45 |
| **Flint 2 #2** | WAN (2.5G) → CRS310 | LAN1 (2.5G) → ATT eth | Bridge + emergency |
| **ATT BGW320** | eth1 → sporeGate | eth2 → Flint 2 #2 LAN1 | Emergency kickstart |
| **CRS310** | ether → sporeGate | ether → Flint 2 #2 WAN | L2 backbone hub |

### Normal Operation (Sovereign)

```
ATT BGW320 (WiFi OFF, ethernet only)
    ├── eth1 → sporeGate enp1s0 (IP passthrough, primary WAN)
    │           └── eno1 → CRS310 ether8 (2.5G backbone uplink)
    │                   ├── etherX → Flint 2 #2 WAN (House 1 WiFi, bridge mode)
    │                   ├── sfp+1 → 10G AOC → Omada (House 2)
    │                   │       └── SG605S → Flint 2 #1 (House 2 WiFi)
    │                   ├── sfp+2 → eastGate (10G)
    │                   └── etherX → northGate (2.5G)
    │
    └── eth2 → Flint 2 #2 LAN1 (DORMANT — emergency bypass cable)
```

**Data path**: All traffic flows through sporeGate (NAT/DNS/firewall/DHCP).
Flint 2 #2 WAN port is the active uplink to CRS310. LAN1 port is cabled to
ATT but dormant (Flint 2 bridge mode only uses WAN port).

### Failure Modes & Recovery

#### Mode A: Flint 2 #2 Dies → WiFi Down, Wired Survives

| Step | Action |
|------|--------|
| 1 | Wired devices (northGate, eastGate, ironGate) unaffected |
| 2 | **Operator**: Re-enable ATT WiFi radios via `http://192.168.1.254` |
| 3 | WiFi clients connect to ATT SSID, get 192.168.1.x (temporary) |
| 4 | Internet works via ATT (bypasses sporeGate for WiFi clients) |
| 5 | Replace/reboot Flint 2 #2, disable ATT WiFi again |

**Recovery time**: ~2 min (operator-paced, ATT WiFi toggle)

#### Mode B: sporeGate Dies → Everything Down

| Step | Action |
|------|--------|
| 1 | All DHCP/DNS/NAT stops. Existing leases work briefly. |
| 2 | **Operator**: Re-enable ATT WiFi via physical access to BGW320 |
| 3 | ATT serves DHCP on 192.168.1.x to WiFi clients (internet works) |
| 4 | **Operator**: Switch Flint 2 #2 from bridge → router mode |
| 5 | Flint 2 #2 uses LAN1 port (cabled to ATT eth2) as WAN |
| 6 | Flint 2 serves DHCP to WiFi clients, NATs via ATT |
| 7 | Wired devices: connect laptop to CRS310, reconfigure gateway |
| 8 | Debug/fix sporeGate, restore sovereign config |

**Recovery time**: ~5 min for WiFi (Flint 2 mode switch), ~15 min for wired

#### Mode C: ATT Internet Dies → WAN Down

| Step | Action |
|------|--------|
| 1 | All gates lose internet. LAN/mesh still works. |
| 2 | **Operator**: USB hotspot from phone → sporeGate |
| 3 | Set hotspot route metric lower than ATT |
| 4 | Or: Flint 2 #2 has tethering capability (OpenWrt) |

**Recovery time**: ~2 min (plug phone USB)

#### Mode D: Full Dead (sporeGate + Flint 2 + ATT all down)

| Step | Action |
|------|--------|
| 1 | Power cycle ATT BGW320 (wait 3 min for sync) |
| 2 | Re-enable ATT WiFi if needed |
| 3 | Power cycle sporeGate (services auto-start via systemd) |
| 4 | Power cycle Flint 2 #2 |
| 5 | Verify: `ping 8.8.8.8`, check dnsmasq leases, WG handshake |

**Recovery time**: ~5 min (power cycle cascade)

### Emergency Bypass Cable

The **Flint 2 #2 LAN1 → ATT eth2** cable is the key redundancy wire. In
normal operation it's dormant. In emergency (Mode B), the operator switches
Flint 2 to router mode and this cable becomes the WAN uplink, bypassing
the dead sporeGate entirely.

This cable also allows the Flint 2 to be provisioned initially by
connecting it to ATT for internet access during setup, then switching to
bridge mode for sovereign operation.

---

## Step-by-Step

### Phase 1: ATT Gateway — Kill WiFi Radios

1. Access BGW320 admin: `http://192.168.1.254` (from sporeGate or northGate)
2. Navigate to **Home Network** → **Wi-Fi**
3. Disable **both** radios:
   - 2.4GHz: OFF
   - 5GHz: OFF
4. Save/Apply
5. Verify: no `ATT*` SSIDs visible on any device

**Impact**: House 1 WiFi users temporarily lose connectivity (daughters' devices).
Flint 2 #2 must be ready to take over immediately.

### Phase 2: Flint 2 #2 — Initial Setup

1. Unbox, connect power
2. Connect laptop/phone to Flint 2 default WiFi (GL-MT6000 setup AP)
3. Access admin panel at `192.168.8.1`
4. Set admin password
5. Configure as **Bridge Mode** (same as House 2 Flint 2 #1):
   - Mode: Bridge (not Router)
   - WAN port becomes LAN — receives DHCP from upstream (sporeGate)

### Phase 3: WiFi Configuration

Configure via admin panel or SSH to MediaTek `.dat` files:

| Setting | 2.4GHz | 5GHz |
|---------|--------|------|
| SSID | ApertureScience | ApertureScience |
| Password | exoticpanda714 | exoticpanda714 |
| Encryption | WPA2/WPA3 | WPA2/WPA3 |
| Channel | Auto (1/6/11) | Auto (36-48 or DFS) |
| Band width | 20/40MHz | 80MHz |
| Region | US | US |

**Must match House 2 Flint 2 #1 exactly** for seamless roaming between houses.

### Phase 4: Physical Connection

1. Run ethernet from CRS310 free port to Flint 2 #2 WAN port
2. Flint 2 #2 gets DHCP from sporeGate (bridge mode)
3. Verify: Flint 2 appears in dnsmasq leases

### Phase 5: sporeGate — DHCP + DNS

Add to `/etc/dnsmasq.conf`:

```
# Flint 2 #2 — House 1 WiFi AP
dhcp-host=<MAC>,192.168.4.251,flint2-hub1
address=/flint2-hub1.primals.local/192.168.4.251
```

(MAC obtained from Flint 2 #2 label or admin panel)

### Phase 6: Verify

1. Connect phone to ApertureScience at House 1
2. Confirm IP is `192.168.4.x` (from sporeGate, NOT 192.168.1.x)
3. Confirm `printer.primals.local` resolves
4. Confirm DNS blocklist active (test: `http://ads.example.com` → blocked)
5. Confirm internet works
6. Walk to House 2 — confirm seamless WiFi (same SSID, same password)

### Phase 7: Printer Migration

After ATT WiFi disabled, power-cycle the printer:
- It reconnects to ApertureScience (now served by Flint 2 #1 or #2)
- DHCP from sporeGate → gets `192.168.4.200` (reservation ready)
- Update dnsmasq: `printer.primals.local` → `192.168.4.200`

---

## Topology Updates Required

After successful provisioning:

1. **TOPOLOGY_MAP.toml**: Add `flint2_wifi_h1` zone, update backbone ports
2. **device_registry.toml** (metalForge): Add Flint 2 #2 device
3. **ECOSYSTEM_BLURB.md**: Update Flint 2 count, ATT WiFi disabled
4. **segments.backbone_legacy**: Mark as deprecated/empty (no more WiFi clients)
5. **freshness.toml**: Update notes

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Daughters lose WiFi during transition | Do Phase 1 + 4 together (< 5 min gap) |
| Flint 2 bridge mode doesn't work | Test bridge mode BEFORE disabling ATT WiFi |
| Wrong subnet IP | Verify dnsmasq lease before declaring success |
| CRS310 port unavailable | Check CRS310 port LEDs (no creds needed for L2) |
| Printer stays on 192.168.1.x | Power-cycle printer after ATT WiFi killed |

---

## Post-Provisioning State

```
ATT BGW320 (ethernet WAN only — WiFi OFF, DHCP only for passthrough)
    ├── eth1 → sporeGate enp1s0 ──→ eno1 → CRS310 (SOVEREIGN PATH)
    │                                        ├── Flint 2 #2 — House 1 WiFi
    │                                        ├── 10G trunk → Flint 2 #1 — House 2 WiFi
    │                                        ├── eastGate, northGate, ironGate
    │                                        └── Printer (192.168.4.200)
    │
    └── eth2 → Flint 2 #2 LAN1 (DORMANT emergency bypass cable)
```

**All radio owned. All DHCP sovereign. ATT is pure ethernet ingress.**
**Emergency bypass cable: Flint 2 → ATT direct, activates on sporeGate failure.**
