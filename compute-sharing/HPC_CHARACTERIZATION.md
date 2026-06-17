# HPC Characterization — Distributed Consumer/Hobbyist Cluster

**Date**: 2026-06-17 | **Wave**: 115
**Philosophy**: Build HPC from distributed LAN+WAN using consumer and hobbyist gear,
not enterprise/pro equipment. Sovereignty through commodity hardware.

---

## Core Router (Sovereignty Boundary)

| Attribute | Value |
|-----------|-------|
| **Device** | GMKtec NucBox M6 ("sporeGate") |
| **CPU** | AMD Ryzen 5 6600H (6C/12T, 3.3GHz base, 4.5GHz boost) |
| **RAM** | 28 GB DDR5 |
| **Storage** | 929 GB NVMe (866 GB free) |
| **NIC WAN** | 2.5G RJ45 (enp1s0) → ATT gateway |
| **NIC LAN** | 2.5G RJ45 (eno1) → CRS310 switch |
| **WiFi** | Wi-Fi 6E (wlp3s0) — OOB management fallback |
| **OS** | Pop!_OS 22.04 (systemd-networkd, nftables) |
| **Role** | NAT router, firewall, DHCP, DNS, NUCLEUS (13 primals), RustDesk |
| **Power** | ~45W TDP (laptop SoC, fanless viable) |

Headroom: 18 GB RAM available, 866 GB disk free, 12 threads mostly idle.
Can run additional workloads (Proxmox VMs, containers, build tasks).

---

## L2 Switch (Transport Backbone)

| Attribute | Value |
|-----------|-------|
| **Device** | MikroTik CRS310-8G+2S+IN |
| **CPU** | ARM (2 cores, 256 MB RAM) |
| **RouterOS** | 7.19.6 (stable) |
| **Ports** | 8x 2.5G RJ45 + 2x 10G SFP+ |
| **Mode** | Pure L2 bridge (no routing) |
| **Management** | 192.168.4.2 (SSH, HTTP, Winbox, REST API) |
| **Uptime** | ~18h (since last config change) |

### Port Allocation (current)

| Port | Status | Connected To | Speed |
|------|--------|--------------|-------|
| ether1 | **EMPTY** | — | 2.5G |
| ether2 | Active | Eero base station | 2.5G |
| ether3 | **EMPTY** | — | 2.5G |
| ether4 | **EMPTY** | — | 2.5G |
| ether5 | **EMPTY** | — | 2.5G |
| ether6 | **EMPTY** | — | 2.5G |
| ether7 | **EMPTY** | — | 2.5G |
| ether8 | Active | sporeGate (router uplink) | 2.5G |
| sfp-sfpplus1 | Active | Omada trunk (18 devices downstream) | 10G |
| sfp-sfpplus2 | Active | Galaxy server (.244) | 10G |

**Available**: 6x 2.5G RJ45 ports ready for NUCs/towers. Plug and play.

---

## Compute Nodes (Current)

### Galaxy Server (192.168.4.244)

| Attribute | Value |
|-----------|-------|
| **MAC** | 1c:86:0b:37:63:19 |
| **Connection** | sfp-sfpplus2 (dedicated 10G) |
| **Services** | Galaxy web UI (:8080), SFTP (:8022) |
| **Role** | Bioinformatics analysis platform |
| **Access** | SFTP only (mod_sftp), password required |
| **Status** | ALIVE, serving workloads |

### Debian Server (192.168.4.218)

| Attribute | Value |
|-----------|-------|
| **MAC** | 9c:6b:00:44:dd:60 |
| **Connection** | sfp-sfpplus1 (via Omada trunk) |
| **Services** | SSH (:22), HTTP (:80), HTTPS (:443) |
| **OS** | Debian 10 (buster), OpenSSH 7.9p1 |
| **Access** | Password auth required (no key access yet) |
| **Status** | ALIVE |

### eastGate (192.168.4.30) — OFFLINE

| Attribute | Value |
|-----------|-------|
| **Role** | Primary compute tower, overwatch/primalSpring |
| **Connection** | DISCONNECTED from CRS310 (was 10G SFP+) |
| **Status** | Alive remotely (pushing commits via VPS/relay) |
| **Note** | Needs physical reconnection to CRS310 |

### fieldGate (192.168.4.36) — OFFLINE

| Attribute | Value |
|-----------|-------|
| **Role** | Canary NUC, worker node |
| **Connection** | DISCONNECTED (was 2.5G RJ45) |
| **Status** | Powered off or disconnected |

---

## Network Equipment (Non-Compute)

### Omada Router (192.168.4.115 / 10.0.4.1)

| Attribute | Value |
|-----------|-------|
| **Vendor** | TP-Link Omada |
| **MAC** | c8:e3:06:c6:77:a1 |
| **Connection** | sfp-sfpplus1 (10G trunk) |
| **WAN IP** | 192.168.4.115 (from sporeGate DHCP) |
| **LAN IP** | 10.0.4.1 (internal DHCP for WiFi clients) |
| **Mode** | Router + NAT (clients get 10.0.x.x) |
| **Downstream** | All WiFi clients, APs, Eero satellite, IoT |
| **Controller** | Needs access (operator supplies password AM) |

### TP-Link AP (192.168.4.101)

| Attribute | Value |
|-----------|-------|
| **MAC** | c8:a3:e8:fb:94:49 |
| **Ports** | None open (adopted by Omada controller) |
| **Role** | WiFi access point (managed by Omada) |

### Eero Mesh

| Component | IP | Connection |
|-----------|-----|-----------|
| Base station | 192.168.1.115 | CRS310 ether2 (2.5G) |
| Satellite | 192.168.1.164 | Via Omada trunk (wireless backhaul) |
| **Mode** | Bridge to ATT subnet (192.168.1.x) |
| **Extends to** | Other property (friend's house) |

### ATT Gateway (192.168.1.254)

| Attribute | Value |
|-----------|-------|
| **Model** | BGW320 (fiber ONT + router) |
| **Mode** | NAT router (target: IP passthrough) |
| **WiFi SSID** | "Aperture Science" |
| **WAN** | Fiber (speed TBD — measured ~4 Mbps currently, likely throttled) |

---

## IoT / Surveillance

| IP | MAC | Type |
|----|-----|------|
| 192.168.4.133 | 78:76:89:96:e5:8b | Ring camera |
| 192.168.4.235 | 78:76:89:96:e6:7b | Ring camera |
| 192.168.4.152 | ac:80:0a:85:c6:e1 | nginx device (NVR? camera?) |

---

## Link Budget

```
Internet (ATT Fiber)
  │ ~4 Mbps measured (likely double-NAT throttled; expect 100+ after passthrough)
  ▼
ATT BGW320 ──1G──► sporeGate enp1s0 (2.5G capable, ATT port is 1G)
                    │
sporeGate eno1 ──2.5G──► CRS310 ether8
                          │
                ┌─────────┼──────────────────────────────┐
                │         │                              │
          ether2 (2.5G)   sfp+1 (10G)              sfp+2 (10G)
          Eero base       Omada trunk               Galaxy server
                          │
                   ┌──────┼───────┐
                   │      │       │
              APs  IoT   NAS    Eero satellite
              (WiFi clients on 10.0.x.x)
```

### Bottlenecks

1. **ATT → sporeGate**: 1G port on ATT (upgrade: passthrough + direct fiber)
2. **sporeGate → CRS310**: 2.5G (sufficient for NAT/firewall duties)
3. **CRS310 internal**: Wire-speed L2 switching (no CPU bottleneck)
4. **sfp+1 trunk**: 10G shared among ~18 devices (adequate)
5. **sfp+2 Galaxy**: Dedicated 10G (ideal for data-heavy bioinformatics)

### Expansion with 2.5G Links

With 6 empty 2.5G ports on the CRS310, adding NUCs is trivial:

```bash
# Each NUC gets:
# - 2.5G direct to CRS310 (no contention, dedicated wire)
# - DHCP from sporeGate (192.168.4.100-249 pool)
# - Full 2.5G to any other device on the switch
# - 10G aggregate backplane between all ports
```

For compute-heavy workloads between NUCs, the CRS310's switching fabric
handles multi-port simultaneous at wire speed (no NAT overhead — L2 only).

---

## Aggregate Compute (when all nodes are online)

| Node | CPU | Cores | RAM | Storage | Network |
|------|-----|-------|-----|---------|---------|
| sporeGate | Ryzen 5 6600H | 12T | 28 GB | 929 GB NVMe | 2.5G |
| eastGate | (tower, TBD) | ? | ? | ? | 10G SFP+ |
| fieldGate | (NUC, TBD) | ? | ? | ? | 2.5G |
| Galaxy | (server, TBD) | ? | ? | ? | 10G SFP+ |
| Debian (.218) | (server, TBD) | ? | ? | ? | via Omada |
| **Future NUCs** | varies | — | — | — | 2.5G each |

### WAN Compute (VPS)

| Node | CPU | RAM | Location | Role |
|------|-----|-----|----------|------|
| golgiBody | 1 vCPU | 2 GB | DO NYC1 | Relay, Forgejo, mesh hub |
| peptidoglycan | 2 vCPU | 4 GB | DO NYC1 | Build authority, cargo |

---

## Expansion Plan

### Phase 1: Plug existing (immediate)

- Reconnect eastGate to CRS310 sfp+ or 2.5G port
- Reconnect fieldGate to CRS310 2.5G port
- Use 2.5G Cat6 patch cables (short runs, you have these)

### Phase 2: Add NUCs (when hardware arrives)

- Each NUC gets: 2.5G NIC + Cat6 patch → CRS310 empty port
- Install Pop!_OS or Ubuntu → auto-DHCP from sporeGate
- Run `membrane gate.bootstrap <name>` → full primal team member in minutes

### Phase 3: Characterize existing servers

- Galaxy (.244): Get SSH access, document CPU/RAM/storage
- Debian (.218): Get credentials, assess capability
- These might be repurposable for HPC workloads

### Phase 4: Omada to bridge mode (unify subnet)

- Access Omada controller (need password)
- Switch from router+NAT to pure AP/bridge
- All WiFi clients join 192.168.4.0/22 directly
- Eliminates double-NAT for WiFi devices

### Phase 5: VLAN segmentation

- CRS310 supports VLANs via REST API
- Separate compute/IoT/guest traffic
- sporeGate does inter-VLAN routing (Ryzen has headroom)

---

## Design Principles (Consumer/Hobbyist HPC)

1. **Commodity hardware**: NUCs, mini-PCs, used towers. No rack servers needed.
2. **2.5G baseline**: All new connections at 2.5G minimum. 10G for data-heavy nodes.
3. **Flat L2 switching**: CRS310 does wire-speed L2. No per-port CPU penalty.
4. **Single sovereignty boundary**: Only sporeGate touches the internet. Everything else is internal.
5. **Plug and play**: New node = plug cable + wait for DHCP + run bootstrap.
6. **Reproducible**: All config is in Git. Clone a new gate from wateringHole docs.
7. **Fail gracefully**: If sporeGate dies, unplug it and plug ATT directly to CRS310.
8. **WAN mesh**: golgiBody relay connects all gates even when LAN is unreachable.
