# projectNUCLEUS — Membrane VPS Deployment Handoff

**Date**: May 14, 2026  
**From**: primalSpring (ecosystem coordination)  
**For**: projectNUCLEUS (deployment & ops ownership)  
**Registry**: 418-method capability registry  

---

## Summary

The first sovereign membrane channel is **live on DigitalOcean**. primalSpring
built the tooling, deployed Channel 2 (Relay), and validated it. Ownership
now transfers to projectNUCLEUS for ongoing ops, the NAT shadow run, and
deployment of Channels 1 and 3.

---

## What's Deployed

| Item | Value |
|------|-------|
| **VPS** | `membrane-relay`, 157.230.3.183, Debian 12 x64, nyc1, ~$4/mo |
| **Channel 2** | Songbird v0.2.1 TURN relay on UDP :3478 |
| **Firewall** | UFW active, default-deny, ports 22/53/80/443/3478 |
| **SSH** | Key-only (password auth disabled), key: `ecoPrimal` |
| **Binary source** | Pulled from GitHub Releases `v2026.05.13` (not SCP'd) |
| **Credentials** | Generated on-VPS at `/etc/songbird/relay-credentials` |
| **systemd** | `songbird-relay.service` enabled, auto-restart on failure |

### Client Config (for NAT shadow run)

```bash
export SONGBIRD_TURN_SERVER=157.230.3.183:3478
export SONGBIRD_TURN_USERNAME=nucleus-relay
export SONGBIRD_TURN_KEY=210bcbb59980af265e48c7caaab525c6c4e88b74f9c3ca9e5d9f5b8d3a42f559
```

---

## Tooling Shipped (in plasmidBin)

### `deploy_membrane.sh`

Four modes:

```bash
./deploy_membrane.sh provision --region nyc1     # Create droplet + deploy
./deploy_membrane.sh deploy root@<ip>            # Deploy to existing VPS
./deploy_membrane.sh status root@<ip>            # Health check
./deploy_membrane.sh teardown --name membrane-relay  # Destroy droplet
```

All modes support `--dry-run`. Binary is pulled from GitHub Releases on the
VPS itself — no local machine dependency. This validates our plasmidBin
distribution pipeline end-to-end.

### `membrane/songbird-relay.service`

Security-hardened systemd unit: `NoNewPrivileges`, `ProtectSystem=strict`,
`MemoryMax=128M`, `CPUQuota=50%`.

---

## Secrets & API Key Sharing

### Current State

| Secret | Location | Access |
|--------|----------|--------|
| DO API token | Operator's `~/.config/doctl/token` (chmod 600) | Operator only |
| TURN credentials | VPS `/etc/songbird/relay-credentials` | Root on VPS only |
| SSH private key | Operator's `~/.ssh/id_ed25519` | Same key as GitHub + LAN gates |

### Sharing Strategy

**Phase 0 (now): Operator-held.** The DO API token lives on the operator's
machine. `deploy_membrane.sh` uses `doctl` which reads from its own auth
context. TURN credentials are generated on-VPS and never leave it.

**Phase 1 (near-term): BearDog `secrets.store` delegation.** BearDog owns
`secrets.store` and `secrets.retrieve` in the capability registry. The
composition bootstrap can store the DO API token purpose-encrypted via
BearDog, retrievable by authorized primals (biomeOS for auto-provisioning).
This requires:
- BearDog implementing `secrets.store`/`secrets.retrieve` with per-purpose
  encryption (the wire contract exists, implementation is in progress)
- A BTSP session between the operator's machine and the composition

**Phase 2 (stadial): Zero operator secrets.** The DO API token is stored
in BearDog's encrypted secret store, accessible only through BTSP-authenticated
sessions. biomeOS can provision/teardown membrane channels autonomously.
The operator's only role is initial token provisioning and rotation.

### What BearDog Can Do Today

| Capability | Status |
|------------|--------|
| `crypto.sign` / `crypto.verify` | **Shipped** — ed25519, production-ready |
| `crypto.encrypt` / `crypto.decrypt` | **Shipped** — symmetric + asymmetric |
| `btsp.server.*` / `btsp.client.*` | **Shipped** — session establishment |
| `secrets.store` / `secrets.retrieve` | **Wire contract defined**, implementation pending in NestGate |
| BTSP credential delegation | **Protocol exists**, tooling integration pending |

**Bottom line**: BearDog can encrypt/decrypt and establish BTSP sessions today.
The `secrets.store`/`secrets.retrieve` flow requires NestGate integration (it's
NestGate that persists, BearDog that encrypts). For now, operator-held tokens
with `chmod 600` is the practical approach.

---

## What projectNUCLEUS Owns Now

| Responsibility | Detail |
|----------------|--------|
| VPS uptime | Monitor `membrane-relay` droplet, respond to outages |
| NAT shadow run | Configure clients with TURN credentials, validate two-NAT relay |
| Credential rotation | Regenerate TURN credentials periodically |
| Channel 1 (DNS) | Deploy `knot-dns` when ready (port 53 already open) |
| Channel 3 (Surface) | Deploy `beardog-tls` + `nestgate` when ready (ports 80/443 open) |
| Scaling | Evaluate Model B (multi-VPS) if single box hits limits |
| DO token rotation | Rotate via DO dashboard, update `~/.config/doctl/token` |

### Operational Commands

```bash
# Status check
./deploy_membrane.sh status root@157.230.3.183

# SSH to VPS
ssh root@157.230.3.183

# View relay logs
ssh root@157.230.3.183 "journalctl -u songbird-relay -f"

# Restart relay
ssh root@157.230.3.183 "systemctl restart songbird-relay"

# Update binary (re-fetches from GitHub Releases)
./deploy_membrane.sh deploy root@157.230.3.183

# Teardown (destroys droplet — requires confirmation)
./deploy_membrane.sh teardown
```

---

## Cross-References

- `wateringHole/MEMBRANE_CHANNEL_ARCHITECTURE.md` — full architecture doc
- `wateringHole/CAPABILITY_WIRE_STANDARD.md` — SP-01, GD-01 conventions
- `wateringHole/NUCLEUS_TWO_TIER_CRYPTO_MODEL.md` — BearDog secrets delegation model
- `wateringHole/SECRETS_AND_SEEDS_STANDARD.md` — no-static-secrets principle
- `wateringHole/handoffs/SONGBIRD_WAVE202_RELAY_OPS_DEPLOYMENT_MAY12_2026.md` — relay readiness
- `plasmidBin/deploy_membrane.sh` — deployment script
- `plasmidBin/membrane/songbird-relay.service` — systemd unit
