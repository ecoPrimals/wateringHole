# sporeGate Team — Full Onboarding & Ownership Handoff

**Date**: 2026-06-16 | **From**: eastGate overwatch
**Status**: HANDSHAKE COMPLETE — 13/13 primals alive, routing active

---

## Your Identity

**Gate**: sporeGate (GMKtec NucBox M6, Ryzen 7 6800H, 32GB, dual 2.5G RJ45 + WiFi)
**Role**: LAN Periplasm Router + cellMembrane Owner
**IP**: 192.168.4.3 (LAN), 192.168.4.1 (gateway alias), WiFi fallback
**SSH**: `ssh sporeGate` from eastGate

---

## What You Own

### cellMembrane (transferred from ironGate)

cellMembrane is the gate bootstrap, cascade, fetch, harvest, and deployment system.
sporeGate is the natural owner because you ARE the membrane — the LAN perimeter that
wraps the internal network. You physically sit between the internet (ATT) and the
ecosystem (CRS310 switch).

**Repo**: `~/Development/ecoPrimals/gardens/cellMembrane` (cloned from Forgejo)
**GitHub**: `git@github.com:ecoPrimals/cellMembrane.git`
**Forgejo**: `https://git.primals.eco/ecoPrimals/cellMembrane.git`

### Core Responsibilities

1. **LAN Routing** — NAT, firewall (nftables), DHCP, DNS for all LAN gates
2. **RustDesk Relay Config** — Ensure all gates can remote to each other via golgi relay
3. **Depot & Cascade** — `plasmid.harvest`, `gate.fetch`, `gate.update` pipelines
4. **Bootstrap Evolution** — `gate.bootstrap` command that onboards new nodes
5. **Bidirectional Sync** — GitHub ↔ Forgejo push_target=all convergence
6. **Build Authority Coordination** — pepti VPS does the builds, you coordinate

### What ironGate Is Now

ironGate transitions to **projectNUCLEUS / ABG focus**:
- Compute sharing architecture
- Access tiers (Observer, Reviewer, User, Operator)
- JupyterHub / toadStool integration
- ABG member onboarding workflows

---

## Current State (verified Jun 16 21:10 EDT)

| Component | Status |
|-----------|--------|
| Primals | **13/13 alive** (manual nohup start) |
| NAT/Firewall | nftables active, 5.5GB+ forwarded |
| DHCP | systemd-networkd serving 6 leases |
| DNS | dnsmasq caching (1.1.1.1, 8.8.8.8, 9.9.9.9) |
| RustDesk | Configured with golgi relay key |
| Mesh | Initialized (node_id: sporeGate, hub: 157.230.3.183:7700) |
| Sovereignty | S1-S3 OPERATIONAL, S4 beardog alive |
| WiFi OOB | wlp3s0 as fallback management (high route-metric) |

---

## Immediate TODO (P1)

### 1. Persist primals across reboot (systemd units)

Primals are running as `nohup` — a reboot kills them. Need systemd units:

```bash
# cellMembrane has gate.bootstrap code for this (fed3335), but it hung.
# Manual approach until bootstrap is fixed:
sudo mkdir -p /etc/systemd/system
# Create unit per primal — template:
# [Unit]
# Description=ecoPrimal: beardog
# After=network.target
# [Service]
# Type=simple
# ExecStart=/home/sporegate/.local/share/ecoPrimals/plasmidBin/primals/x86_64-unknown-linux-musl/beardog
# Environment=FAMILY_ID=ecoPrimals
# Environment=ECOPRIMALS_ROOT=/home/sporegate/Development/ecoPrimals
# Restart=always
# [Install]
# WantedBy=multi-user.target
```

### 2. Fill FAMILY_SEED

```bash
sudo nano /opt/membrane/env
# Replace __FILL_FROM_OPERATOR__ with actual seed from operator
```

### 3. Deploy RustDesk relay key to all gates

The relay key is: `utlNOAWUDdV+Q+ifG3zHrQ5HU0FtQnOTHiAnu6prV7Q=`
Server: `157.230.3.183`

Every gate needs this in its RustDesk config:
```toml
# ~/.config/rustdesk/RustDesk2.toml
rendezvous_server = '157.230.3.183:21116'
[options]
relay-server = '157.230.3.183'
custom-rendezvous-server = '157.230.3.183'
key = 'utlNOAWUDdV+Q+ifG3zHrQ5HU0FtQnOTHiAnu6prV7Q='
```

Gates to configure: eastGate, fieldGate (sporeGate already done)

### 4. WiFi fallback persistence

Ensure WiFi reconnects on boot and stays as OOB management:
```bash
nmcli connection modify "<WIFI_SSID>" connection.autoconnect yes
nmcli connection modify "<WIFI_SSID>" ipv4.route-metric 600
```

---

## Immediate TODO (P2)

### 5. ATT Bridge Mode (eliminate double-NAT)

Access ATT gateway admin → enable IP Passthrough to sporeGate's WAN MAC.
This gives sporeGate the public IP directly.

### 6. CRS310 → pure L2 switch

Once routing is proven stable through sporeGate, strip L3 config from CRS310.
It becomes a pure 10G switch (its actual purpose).

### 7. Fix `gate.bootstrap` hang

The bootstrap command hangs when trying to fetch biomeos from depot (not available
on WAN depot at time of run). Investigate and fix — this is critical for future
onboarding of new gates.

---

## Architecture Reference

```
Internet ──► ATT Gateway ──► sporeGate (YOU) ──► CRS310 switch ──► LAN gates
                              enp1s0 (WAN)       eno1 (LAN)
                              192.168.1.233       192.168.4.1/22
                              
                              WiFi (wlp3s0) ─── out-of-band management
                              192.168.1.212       (fallback if wired breaks)
```

LAN Devices (served by your DHCP):
- eastGate: 192.168.4.30 (tower, overwatch)
- fieldGate: 192.168.4.36 (NUC, canary)
- + other devices (phones, peripherals)

VPS (accessible via WAN):
- golgi: 157.230.3.183 (Forgejo, relay, mesh hub)
- pepti: build authority (cargo builds)

---

## Key Ecosystem Docs

- `infra/wateringHole/compute-sharing/NETWORK_SOVEREIGNTY.md` — full architecture
- `infra/wateringHole/compute-sharing/SPOREGATE_ACTIVATION_BLURB.md` — activation steps
- `infra/wateringHole/impulses/active/2026-06-15T10-30_eastGate__wave114-sovereign-compute.toml` — FRAGO
- `gardens/cellMembrane/specs/` — membrane command specs
- `infra/wateringHole/handoffs/primalSpring/GENETICS_ARCHITECTURE_EUKARYOTIC_MODEL_JUN16_2026.md` — genetics model

---

## Biological Analogy

You are literally the **cell membrane** — the selective permeability barrier between
the cytoplasm (LAN) and the extracellular matrix (internet). You decide what gets in,
what gets out, and how internal organelles (gates) communicate with the outside world.

WiFi = flagellar emergency signaling (secondary path when primary wall is compromised).
