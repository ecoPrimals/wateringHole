# Domain Infrastructure

Last Updated: 2026-03-29

## Overview

Two domains serve the ecoPrimals ecosystem. Each has a distinct purpose and threat model.

| Domain | Purpose | Hosting | DNS | Registrar |
|--------|---------|---------|-----|-----------|
| nestgate.io | BirdSong beacon, Dark Forest rendezvous, STUN/NAT relay | Cloudflare Tunnel -> biomeOS Unix socket | Cloudflare (proxied) | Porkbun |
| primals.eco | Public ecosystem portal, documentation, binary distribution index | GitHub Pages (sporePrint) | Cloudflare (proxied) | Porkbun |

---

## nestgate.io — BirdSong Beacon

### Purpose

`nestgate.io` is the public entry point for the BirdSong beacon. It serves as a rendezvous
for STUN/NAT traversal and Dark Forest gated peer discovery. To any client without valid
mito beacon genetics, the endpoint returns noise (HTTP 403 with strict security headers).
Only family members holding the correct genetic material can decrypt the beacon and
establish connections.

### Architecture

```
Internet
  │
  ▼
Cloudflare Edge (TLS termination, DDoS protection)
  │  QUIC tunnel (X25519MLKEM768 + CurveP256)
  ▼
cloudflared (user systemd service on gate machine)
  │  Unix socket
  ▼
biomeOS API (axum, Dark Forest gated)
  ├── dark_forest_gate.rs    — rejects non-family connections
  ├── beacon_verification.rs — validates mito beacon genetics
  └── handlers/rendezvous.rs — STUN/NAT rendezvous endpoint
```

### DNS Records

All three subdomains are CNAME records pointing to the Cloudflare Tunnel UUID:

| Subdomain | Type | Target | Proxied |
|-----------|------|--------|---------|
| api.nestgate.io | CNAME | `<tunnel-uuid>.cfargotunnel.com` | Yes |
| tower.nestgate.io | CNAME | `<tunnel-uuid>.cfargotunnel.com` | Yes |
| beacon.nestgate.io | CNAME | `<tunnel-uuid>.cfargotunnel.com` | Yes |

All three route to the same biomeOS beacon. The Dark Forest gate at the application
layer differentiates behavior.

### Tunnel Configuration

The tunnel runs as a user-level systemd service (`cloudflared-beacon.service`) so it
can access the biomeOS Unix socket (which has 0600 owner-only permissions).

Config location: `~/.cloudflared/config.yml`

```yaml
tunnel: nestgate-api
credentials-file: <home>/.cloudflared/<tunnel-uuid>.json

ingress:
  - hostname: api.nestgate.io
    service: unix:<runtime>/biomeos/biomeos-api-<family-id>.sock
  - hostname: tower.nestgate.io
    service: unix:<runtime>/biomeos/biomeos-api-<family-id>.sock
  - hostname: beacon.nestgate.io
    service: unix:<runtime>/biomeos/biomeos-api-<family-id>.sock
  - service: http_status:404
```

The socket path includes the family_id (derived from `.family.seed`), making it
deterministic per deployment.

### Systemd Services

Two user-level services on the beacon machine:

1. `biomeos-beacon.service` — starts biomeOS API, creates the Unix socket
2. `cloudflared-beacon.service` — connects the socket to Cloudflare edge

Both are enabled with `loginctl enable-linger` so they persist after logout.

### Connection Priority (from .known_beacons.json)

1. IPv6 direct via `tower.nestgate.io` (0ms, no NAT)
2. IPv4 direct via `nestgate.io` A record
3. LAN via mDNS / Dark Forest broadcast
4. STUN hole-punch via Songbird IGD
5. Family relay via `tower.nestgate.io:3492/api/v1/rendezvous/beacon`
6. (Future) Pure Rust onion overlay

### Security Model

- Cloudflare provides TLS termination and DDoS protection at the edge
- The tunnel uses QUIC with post-quantum key exchange (X25519MLKEM768)
- biomeOS Dark Forest gate rejects all non-family connections at the application layer
- The endpoint is noise to scanners, bots, and any party without mito genetics
- Future: BirdSong TLS replaces Cloudflare for sovereign TLS termination

---

## primals.eco — Public Portal

### Purpose

`primals.eco` is the public-facing portal for the ecoPrimals ecosystem. It serves
documentation from the `sporePrint` repository, providing an on-ramp for researchers,
students, and collaborators to understand the project and fetch primal binaries.

### Architecture

```
Internet
  │
  ▼
Cloudflare Edge (TLS, CDN, DDoS protection)
  │
  ▼
GitHub Pages (ecoPrimals/sporePrint repository)
```

### DNS Records

| Record | Type | Target | Proxied |
|--------|------|--------|---------|
| primals.eco | A | 185.199.108.153 | Yes |
| primals.eco | A | 185.199.109.153 | Yes |
| primals.eco | A | 185.199.110.153 | Yes |
| primals.eco | A | 185.199.111.153 | Yes |
| www.primals.eco | CNAME | ecoprimals.github.io | Yes |

### GitHub Pages Configuration

- Repository: `ecoPrimals/sporePrint`
- Custom domain: `primals.eco`
- CNAME file in repo root
- HTTPS enforced

---

## LAN Cloud Strategy (Multi-Machine Beacon Resilience)

### Concept

The current setup runs the BirdSong beacon on a single machine (the gate). The LAN
cloud strategy distributes the beacon across multiple machines on the local network for
redundancy, security, and load distribution.

### Cloudflare Tunnel Replicas

`cloudflared` supports running the same tunnel on multiple machines simultaneously.
Cloudflare load-balances across active connectors and automatically fails over if one
goes offline.

To add a machine to the LAN cloud:

1. Copy the tunnel credentials JSON to the new machine's `~/.cloudflared/`
2. Copy or generate a matching `config.yml`
3. Install and start `cloudflared tunnel run nestgate-api`
4. Cloudflare detects the new connector and includes it in the rotation

### Beacon Role Differentiation

Each machine in the LAN cloud can serve a different role:

| Role | Description | Services |
|------|-------------|----------|
| Primary | Full beacon: biomeOS API + cloudflared + BearDog crypto | biomeos-beacon, cloudflared-beacon |
| Standby | Hot standby: biomeOS API + cloudflared (same tunnel) | biomeos-beacon, cloudflared-beacon |
| Relay | LAN-only relay: Songbird mesh + STUN | songbird only |

The `sovereign_tower_beacon.toml` graph can be parameterized with `BEACON_ROLE`
to differentiate behavior.

### Songbird LAN Mesh

Songbird's mDNS and Dark Forest broadcast already discover peers on the LAN. The
`.known_beacons.json` `family_relay` section describes the relay topology. When
multiple machines run Songbird, they form a mesh that provides:

- Redundant STUN relay for NAT traversal
- Distributed rendezvous for incoming family connections
- Failover if the primary beacon machine is offline

### Future: Threshold Beacon Material

BearDog's genetic crypto could support `k-of-n` threshold signing for the mito
beacon seed, where `k` machines must cooperate to decrypt incoming family connections.
This distributes trust across the LAN cloud so no single machine holds the full
beacon material.

---

## Operational Procedures

### Checking Service Status

```bash
systemctl --user status biomeos-beacon cloudflared-beacon
```

### Restarting the Beacon Stack

```bash
systemctl --user restart biomeos-beacon
systemctl --user restart cloudflared-beacon
```

### Verifying Public Endpoint

```bash
curl -s -o /dev/null -w "%{http_code}" https://api.nestgate.io/
# Expected: 403 (Dark Forest noise)
```

### Adding a New Machine to the LAN Cloud

1. Install `cloudflared` on the new machine
2. Copy `~/.cloudflared/<tunnel-uuid>.json` (credentials) from the primary
3. Copy `~/.cloudflared/config.yml` (adjust socket path if family_id differs)
4. Copy or build the biomeOS binary
5. Ensure `.family.seed` is available (same genesis seed for family membership)
6. Create and enable the systemd services
7. Verify with `cloudflared tunnel info nestgate-api` (should show multiple connectors)

### Rotating Tunnel Credentials

If tunnel credentials are compromised:

1. `cloudflared tunnel delete nestgate-api` (removes from Cloudflare)
2. `cloudflared tunnel create nestgate-api` (creates new tunnel with new credentials)
3. Update DNS CNAMEs: `cloudflared tunnel route dns nestgate-api api.nestgate.io`
4. Distribute new credentials JSON to all LAN cloud machines
5. Restart cloudflared on all machines

---

## What Is NOT Documented Here

- The tunnel credentials JSON and `cert.pem` (secrets, never committed)
- The Cloudflare account tag (discoverable via dashboard, not public)
- The `.family.seed` contents (genetic material, never committed)
- Individual machine IPs or hardware details (see `whitePaper/gen3/about/HARDWARE.md`)
