# Live Topology — sporeGate Sovereign LAN

**Last verified**: 2026-06-16 20:54 EDT
**Status**: All subnets routing, IPv4 NAT active, IPv6 forwarding disabled

---

## Physical Chain

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET (WAN)                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │ Fiber
                                ▼
┌───────────────────────────────────────┐
│  ATT Gateway (BGW320)                 │
│  192.168.1.254  MAC ec:c3:02:e1:11:81 │
│  Mode: NAT router (target: passthrough│
│  WiFi: ATT native (fallback only)     │
└───────────────────┬───────────────────┘
                    │ RJ45 1G (LAN port)
                    ▼
┌───────────────────────────────────────┐
│  sporeGate (GMKtec NucBox M6)         │
│  WAN: enp1s0 = 192.168.1.233 (DHCP)  │
│  LAN: eno1   = 192.168.4.1/22        │
│  NAT + Firewall + DHCP + DNS          │
│  OS: Pop!_OS 22.04                    │
└───────────────────┬───────────────────┘
                    │ RJ45 2.5G
                    ▼
┌───────────────────────────────────────┐
│  MikroTik CRS310-8G+2S+IN            │
│  Pure L2 Bridge (no routing)          │
│  Management: 192.168.4.2             │
│  8x 2.5G RJ45 + 2x 10G SFP+         │
└──┬─────────┬─────────┬───────────────┘
   │         │         │
   │ 10G     │ 2.5G    │ 2.5G
   │ SFP+    │ RJ45    │ RJ45
   ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌─────────────────────┐
│eastGate│ │  NUCs  │ │ Omada Router         │
│(tower) │ │(future)│ │ 192.168.4.115        │
│.4.30   │ │        │ │ Internal: 10.0.4.1   │
│ ⚠ down │ │        │ │ NATs clients → .4.115│
└────────┘ └────────┘ └──────────┬──────────┘
                                  │ (wired or wireless backhaul)
                                  ▼
                       ┌─────────────────────┐
                       │  Eero Mesh (bridge)  │
                       │  Other-house WiFi    │
                       │  Clients: 10.0.x.x  │
                       │  (via Omada DHCP)    │
                       └─────────────────────┘
```

---

## Subnet Map

| Subnet | CIDR | Gateway | DHCP Server | Purpose |
|--------|------|---------|-------------|---------|
| Sovereign LAN | 192.168.4.0/22 | 192.168.4.1 (sporeGate) | sporeGate | All wired devices, towers, NUCs |
| ATT Legacy | 192.168.1.0/24 | 192.168.1.254 (ATT) | ATT | Eero clients pending migration |
| Omada Internal | 10.0.4.0/22 | 10.0.4.1 (Omada) | Omada | WiFi clients behind Omada NAT |
| Management | — | — | — | CRS310: .4.2, Omada: .4.115 |

---

## Active Devices (verified 2026-06-16)

| IP | MAC | Identity | Connection |
|----|-----|----------|------------|
| 192.168.4.1 | sporeGate eno1 | **Router/Gateway** | — |
| 192.168.4.2 | (CRS310) | **L2 Switch** | Direct to sporeGate |
| 192.168.4.101 | c8:a3:e8:fb:94:49 | Unknown (TP-Link?) | CRS310 2.5G |
| 192.168.4.115 | c8:e3:06:c6:77:a1 | **Omada Router** | CRS310 → 10G |
| 192.168.4.133 | 78:76:89:96:e5:8b | Unknown | CRS310 |
| 192.168.4.149 | 68:54:5a:d0:69:a2 | Unknown | CRS310 |
| 192.168.4.189 | 04:27:28:7c:62:d6 | Unknown | CRS310 |
| 192.168.4.223 | 48:5f:2d:2c:76:e0 | Unknown | CRS310 |
| 192.168.4.235 | 78:76:89:96:e6:7b | Unknown | CRS310 |
| 192.168.4.244 | 1c:86:0b:37:63:19 | Unknown | CRS310 |
| 192.168.4.248 | b8:78:26:38:3b:0d | Unknown | CRS310 |
| 192.168.4.249 | 10:f6:0a:54:57:cc | Unknown | CRS310 |
| 192.168.1.115 | bc:fc:e7:ea:d9:34 | Eero/ATT client | Bridge via CRS310 |
| 192.168.1.164 | 1c:86:0b:37:63:70 | Eero/ATT client | Bridge via CRS310 |

---

## How to Add a NUC

Any NUC plugged into the CRS310 (or any port downstream of sporeGate) will:

1. Get a DHCP lease from sporeGate: `192.168.4.100–249`
2. Get DNS: `192.168.4.1`
3. Get internet via sporeGate NAT
4. Be reachable from all other LAN devices

```bash
# On the new NUC, after plugging in:
ip addr show           # Verify 192.168.4.x address
ping 192.168.4.1       # Verify gateway
ping 8.8.8.8           # Verify internet
ssh sporegate@192.168.4.1  # SSH to sporeGate

# To give it a static lease (optional):
# On sporeGate, add to /etc/systemd/network/20-lan.network [DHCPServer]:
#   [DHCPServerStaticLease]
#   MACAddress=xx:xx:xx:xx:xx:xx
#   Address=192.168.4.XX
```

---

## How to Add a Router / AP

To add another router (e.g., second Omada, or a travel router):

**Option A: Bridge mode (transparent, inherits sporeGate DHCP)**
- Plug into CRS310
- Disable DHCP on the new router
- Set to bridge/AP-only mode
- Clients get 192.168.4.x directly from sporeGate

**Option B: NAT mode (own subnet, isolated WiFi)**
- Plug WAN port into CRS310
- Router gets 192.168.4.x from sporeGate DHCP
- Router runs its own DHCP (e.g., 10.0.x.x, 172.16.x.x)
- Router NATs client traffic → appears as single IP to sporeGate
- This is how the Omada currently works

**Option C: VLAN (future, after CRS310 VLAN config)**
- Assign a VLAN to specific CRS310 ports
- sporeGate manages inter-VLAN routing
- Requires CRS310 VLAN configuration via REST API

---

## How to Extend to Another Property

The current Eero mesh extends to another house. To add more locations:

1. **Wired backhaul** (best): Run ethernet between properties → plug into CRS310
2. **Wireless bridge** (current): Eero mesh or point-to-point bridge → Omada handles NAT
3. **WireGuard tunnel** (remote): NUC at remote site → VPN to sporeGate → appears on LAN

---

## Key Routing Rules

| Traffic | Path | Mechanism |
|---------|------|-----------|
| 192.168.4.x → internet | eno1 → enp1s0 → ATT | IPv4 masquerade |
| 192.168.1.x → internet | eno1 → enp1s0 → ATT | Proxy ARP + masquerade |
| 10.0.x.x → internet | Omada NATs → 192.168.4.115 → sporeGate | Double NAT |
| IPv6 (any) | **BLOCKED** | No IPv6 forwarding (causes iPhone stalls) |
| LAN ↔ LAN | Direct via CRS310 bridge | L2 switching |

---

## Known Issues

- [ ] **eastGate down** — 192.168.4.30 unreachable (physical check needed)
- [ ] **ATT still in NAT mode** — double NAT until passthrough enabled
- [ ] **IPv6 disabled** — will re-enable when proper prefix delegation is set up
- [ ] **Omada management** — need to access controller to map devices/SSIDs
- [ ] **Device identification** — many MACs unidentified (need nmap scan or DHCP hostname logging)

---

## Future Evolution

| Phase | Action | Benefit |
|-------|--------|---------|
| Omada access | Log into controller, map SSIDs/VLANs | Full visibility |
| ATT passthrough | Eliminate double-NAT | Public IP on sporeGate |
| DHCP hostnames | Enable `--dhcp-fqdn` in dnsmasq | Auto-identify devices |
| VLAN segmentation | CRS310 VLANs + Omada VLANs | Traffic isolation |
| WireGuard to golgiBody | Encrypted tunnel to VPS | Sovereign mesh |
| Add NUCs | Plug and play (DHCP) | More compute |
| Proxmox on sporeGate | VM/container orchestration | Cloneable gate |
