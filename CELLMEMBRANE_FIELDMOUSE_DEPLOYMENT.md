<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# cellMembrane — fieldMouse Tower on External Substrate

**Date**: May 14, 2026
**Status**: Active
**Authority**: WateringHole Consensus
**Deployment Class**: fieldMouse
**Composition**: Tower (BearDog + Songbird + SkunkBat)
**Substrate**: DigitalOcean VPS (external, non-family)

---

## What Is cellMembrane

The cellMembrane is the first production **fieldMouse** deployment: a minimal
Tower atomic running on external substrate (DigitalOcean VPS) that provides
NUCLEUS with its three membrane channels — Signal (DNS), Relay (NAT), and
Surface (TLS).

cellMembrane is not a gate, not a niche, and does not run biomeOS. It is a
static, hardened composition deployed via `plasmidBin/deploy_membrane.sh`.
It maps exactly to the fieldMouse definition in the glossary:

> The **minimal deployable structure** for the ecoPrimals ecosystem. A
> fieldMouse is the smallest stripped system — as few as a single atomic or
> chimera — purpose-built for a constrained deployment niche.

The "constrained niche" here is **external substrate** — infrastructure the
operator does not physically own, where the substrate provider (DigitalOcean)
has theoretical root-level access to the hardware.

---

## Dark Forest Principle

The cellMembrane operates under the Dark Forest constraint: the substrate
provider is treated as a **non-family observer**. Everything on disk is either:

1. **Public** — binaries (static musl ELFs from plasmidBin), systemd units,
   firewall rules. Nothing here is secret.
2. **Encrypted** — credentials, identity material, state. Encrypted at rest
   such that the provider sees only noise.

This derives from the mitobeacon pattern (Dark Forest Beacon Genetics
Standard): "Observers without beacon genetics: [noise]". DigitalOcean lacks
the beacon genetics (FAMILY_SEED) required to decrypt anything meaningful.

### What the provider sees

| Category | On disk | Provider observes |
|----------|---------|-------------------|
| Binaries | `/opt/membrane/beardog`, `songbird`, `skunkbat` | Stripped static ELFs — public, published in plasmidBin |
| systemd units | `/etc/systemd/system/*.service` | Service definitions — public templates |
| Firewall | UFW rules | Port list — standard TURN relay + SSH |
| TURN credentials | `/etc/songbird/relay-credentials` | HMAC shared secret — **to be encrypted at rest** |
| Tower identity | `/opt/membrane/tower.env` | FAMILY_SEED, GATE_ID — **encrypted at rest** |
| Network traffic | Relay bytes on :3478 | BTSP-encrypted opaque bytes — noise |
| Logs | journald | Operational metadata — no inner secrets |

### Encryption-at-rest roadmap

| Phase | Mechanism | Status |
|-------|-----------|--------|
| **Now** | `age` + SSH ed25519 key encryption via `share_credentials.sh` | Active |
| **Mid term** | BearDog `secrets.store`/`secrets.retrieve` — credentials never stored as files | Pending BearDog Vault |
| **Long term** | Autonomous rotation by cellMembrane BearDog — operator only provisions FAMILY_SEED | Future |

---

## Composition

cellMembrane runs the **Tower atomic** — the same three primals that handle
trust, discovery, and defense inside NUCLEUS, turned outward to face the
public internet.

| Primal | Role | systemd unit | Socket/Port |
|--------|------|-------------|-------------|
| BearDog | BTSP handshake, crypto identity, secrets delegation | `beardog-membrane.service` | `/run/membrane/beardog.sock` |
| Songbird | TURN relay (Channel 2), discovery | `songbird-relay.service` | `:3478` (UDP/TCP) |
| SkunkBat | Defense audit, threat assessment | `skunkbat-membrane.service` | `/run/membrane/skunkbat.sock` |

### Why Tower (not Node, not Nest)

The cellMembrane is a **function tower** — it provides network presence,
crypto identity, and perimeter defense. It does not store data (Nest) and
does not dispatch compute (Node). If a future cellMembrane needs data
persistence (e.g., NestGate for content serving on Channel 3), the Nest
atomic can be added without restructuring.

### Deployment ordering

On external substrate, BearDog must boot **first**:

1. `beardog-membrane.service` — establishes crypto identity from FAMILY_SEED
2. `songbird-relay.service` — starts relay, credentials validated by BearDog
3. `skunkbat-membrane.service` — begins defense audit with Tower identity

This differs from internal gates where biomeOS orchestrates boot order.
On the cellMembrane, systemd dependency ordering (`After=beardog-membrane.service`)
enforces the sequence.

---

## Hardening Profile

The cellMembrane runs with a minimal attack surface:

### Firewall (UFW)

Only ports required by active channels are open:

| Port | Protocol | Purpose |
|------|----------|---------|
| 22 | TCP | SSH management (key-only, fail2ban protected) |
| 3478 | TCP + UDP | Channel 2: Relay (TURN) |

Ports 53, 80, 443 are **closed** until Channels 1 and 3 are deployed.

### Services removed

| Service | Reason |
|---------|--------|
| exim4 | Mail server running as root with no purpose — purged |
| droplet-agent | DigitalOcean monitoring agent — opaque root-level software (optional removal) |

### Services added

| Service | Purpose |
|---------|---------|
| fail2ban | SSH brute-force protection (systemd backend, 5-attempt threshold, 1h ban) |
| journald persistence | Logs survive reboots (`/var/log/journal/`) |

### systemd hardening (all units)

All primal services run with:
- `NoNewPrivileges=true`
- `PrivateTmp=true`
- `ProtectSystem=strict`
- `ProtectHome=true`
- `ReadWritePaths=/run/membrane` (sockets only)
- `ReadOnlyPaths=/opt/membrane` (binaries + config)
- `MemoryMax` / `CPUQuota` resource limits

---

## BingoCube Verification (Future)

The cellMembrane is a natural target for **BingoCube** zero-knowledge access
control. Instead of sharing credentials directly, a remote gate proves
knowledge of a shared commitment via progressive reveal:

1. Operator provisions a BingoCube commitment on the cellMembrane
2. Remote gate (ironGate) requests access by revealing a subcube
3. cellMembrane BearDog verifies `verify_subcube()` — correct reveal grants
   a time-limited BTSP session
4. No credentials are ever transmitted — only commitment proofs

This pattern eliminates the need for `age`-encrypted credential sharing
entirely. The cellMembrane BearDog holds the commitment; the remote gate
holds the preimage. Neither alone is useful to the substrate provider.

---

## Escalation Ladder

```
Phase 0: Relay only (Songbird on :3478)
  └── Current operational state
  └── TURN credentials in plaintext on disk (to be encrypted)

Phase 1: Tower composition (BearDog + Songbird + SkunkBat)
  └── Adds crypto identity, defense audit
  └── deploy_membrane.sh --composition tower

Phase 2: Encrypted-at-rest
  └── BearDog Vault encrypts all credentials on disk
  └── Provider sees only noise (Dark Forest)
  └── age-based sharing replaced by BTSP delegation

Phase 3: BingoCube challenge
  └── Zero-knowledge access control
  └── No credential files exist — only commitment proofs
  └── ironGate verifies via progressive reveal

Phase 4: Full autonomy
  └── cellMembrane BearDog rotates credentials autonomously
  └── Operator's only role: initial FAMILY_SEED + domain registration
  └── biomeOS on ironGate auto-provisions membrane channels
```

---

## Topology Reference

The cellMembrane corresponds to the `ecoprimals-fieldmouse-chimera.yaml`
topology from benchScale, adapted for external substrate:

```
fieldMouse-cellMembrane
├── Tower atomic (chimera)
│   ├── BearDog  — crypto, BTSP, secrets
│   ├── Songbird — relay, discovery
│   └── SkunkBat — defense, audit
├── Substrate: DigitalOcean VPS (nyc1)
├── Channels: 2 active (Relay), 1+3 future
└── Owner: projectNUCLEUS (ops), primalSpring (tooling)
```

---

## Cross-References

- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — full three-channel architecture
- `GLOSSARY.md` — fieldMouse definition
- `birdsong/DARK_FOREST_BEACON_GENETICS_STANDARD.md` — mitobeacon / Dark Forest encryption
- `plasmidBin/deploy_membrane.sh` — deployment script (supports `--composition tower`)
- `plasmidBin/membrane/share_credentials.sh` — `age`-based credential sharing
- `plasmidBin/membrane/*.service` — systemd unit templates
- `handoffs/PROJECTNUCLEUS_MEMBRANE_VPS_HANDOFF_MAY14_2026.md` — ownership handoff
- `benchScale/topologies/ecoprimals-fieldmouse-chimera.yaml` — reference topology
