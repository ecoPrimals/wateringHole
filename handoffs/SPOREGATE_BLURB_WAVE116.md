# sporeGate Overwatch — Wave 116 Blurb

**Date**: Jun 18 2026 | **From**: eastGate overwatch
**Context**: 5/9 gates on sovereign relay. You are the reference enrolled gate (13/13, WG, cascade, SSH). Now: enroll the others and swap hub 2 WiFi.

---

## Priority 1: Gate Enrollment Pipeline

You are the template. Repeat what you did on yourself for each sovereign gate:

```
SSH enable → gate.preflight → membrane install → NUCLEUS 13/13 → systemd → WireGuard peer → cascade connect
```

### Immediate Targets

| Gate | SSH Status | Next Step | Notes |
|------|-----------|-----------|-------|
| **eastGate** (192.168.4.244) | ✅ Live, your key authorized | preflight + NUCLEUS deploy | 10G on CRS310. First enrollment target. |
| **ironGate** | Pending | Enable SSH (apt install openssh-server) | On sovereign relay. Need: identify OS via RustDesk, then SSH in. |
| **flockGate** | Pending | Enable SSH | WAN gate. WireGuard site-to-site via golgi (not through you). |

### Fresh Binary (P1 — cellMembrane team provides)

Your current membrane binary is stale. Coordinate with cellMembrane team to harvest fresh from pepti. New binary has:
- `gate.preflight` — pre-deployment scanner (interface detect, DNS, IP conflicts)
- `firewall.generate` — nftables from membrane composition (K-Derm plasma membrane)

---

## Priority 2: Flint 2 WiFi Swap (this weekend)

Eero bridge mode collapsed overnight. Operator ran a CAT6 from CRS310 as interim.

**Plan**: Replace Eero with GL.iNet Flint 2 (GL-MT6000) this weekend.

| Task | Who | When |
|------|-----|------|
| Physical swap (Eero out, Flint 2 in, CAT6 from Omada) | Operator | Weekend |
| Flint 2 initial setup: AP bridge mode, same SSID, transparent to your DHCP | You (SSH in after boot) | After physical install |
| swiftGate reconnect (was on Eero WiFi) → verify on Flint 2 | You | After AP live |
| Push sovereign relay config to swiftGate | You + operator | After WiFi confirmed |
| Update Omada SDN port map | You | After install |

**Flint 2 config goals** (OpenWrt):
- Mode: dumb AP (bridge, no DHCP, no NAT)
- WiFi: same SSID as Eero was broadcasting (seamless for humans)
- SSH enabled for remote management
- Future: VLAN-tagged SSIDs (compute vs guest)

---

## Priority 2: Remaining Relay Migration

3 gates still on public relay. After Flint 2 live:

| Gate | Access Path | Status |
|------|-------------|--------|
| **strandGate** | Omada wired (house2) | TODO — operator pushes config via RustDesk |
| **southGate** | Omada wired (house2) | TODO — operator pushes config via RustDesk |
| **swiftGate** | WiFi (was Eero, will be Flint 2) | BLOCKED until Flint 2 live |

Alternative: these gates are on your L2 — if they have SSH, you can push config directly without RustDesk.

---

## Priority 2: WireGuard Mesh Expansion

Current mesh: golgi (10.13.37.1), you (10.13.37.2), pepti (10.13.37.4).

| New Peer | Assigned IP | Via | Blocked On |
|----------|------------|-----|------------|
| eastGate | 10.13.37.3 | Direct SSH from you | Nothing — ready now |
| ironGate | 10.13.37.5 | After SSH enabled | SSH enablement |
| flockGate | 10.13.37.6 | Direct to golgi (WAN) | SSH enablement on flockGate |

---

## Omada SDN Management

SDN controller is live on your machine. Keep exploring:
- Label SFP+ ports with connected devices
- Check for firmware updates
- Prepare VLAN plan (compute / wifi / guest) — implement after enrollment wave stable
- Track clients: strandGate, southGate, fieldGate should be visible

---

## Key Infra

| Resource | Access |
|----------|--------|
| golgi | ssh root@157.230.3.183 (WG: 10.13.37.1) |
| pepti | ssh root@157.230.209.218 (WG: 10.13.37.4) |
| eastGate | ssh eastgate@192.168.4.244 |
| Omada SDN | http://localhost:8088 (on your machine) |
| Forgejo | https://git.primals.eco |
| Sovereign relay config | See RUSTDESK_CONFIG.md |

---

## What NOT to touch

- **northGate**: Windows hobby system. P3. Leave until NUCLEUS proven on all Linux gates.
- **fieldGate**: Dead CMOS. Operator will hardware-fix when time allows.
- **ATT passthrough**: Operator handles. Don't change WAN config without coordination.
