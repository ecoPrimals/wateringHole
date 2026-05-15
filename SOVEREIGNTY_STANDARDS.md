<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Sovereignty Standards — Ecosystem Behaviors for Sovereign Evolution

**Date**: May 15, 2026
**Status**: Active
**Authority**: WateringHole Consensus
**Audience**: All primals, all compositions, all deployments

---

## Purpose

This document defines the **standards and behaviors** that govern the
ecoPrimals ecosystem's progressive sovereignty evolution. Every primal,
composition, and deployment inherits these constraints. They are not
aspirational — they are enforced by validation tooling (darkforest,
benchScale, deploy graphs, composition validators).

---

## Core Principles

### 1. Stability First, Sovereignty Second

External services are **calibration instruments**, not enemies. Each
provides production-grade baselines (latency, availability, throughput,
error rates, security). No external dependency is removed until its
primal replacement **proves parity or superiority** under real load.

**Priority order** (from `SOVEREIGNTY_VALIDATION_PROTOCOL.md`):
1. **Stability / Security** — system stays up, data stays safe
2. **Sovereign solutions** — replace externals with primals
3. **Rust** — prefer Rust implementations for auditability
4. **Primal composition** — prefer composed primals over monoliths

### 2. Calibrate → Shadow → Cutover

Every sovereignty replacement follows a three-step protocol:

1. **Calibrate**: Capture baseline metrics from the external service
   (p50/p95/p99 latency, uptime %, error rates, throughput). Minimum
   7-day capture window.
2. **Shadow**: Run the primal replacement in parallel. Same traffic,
   separate port. Log both paths. Compare metrics daily.
3. **Cutover**: Switch traffic to the primal replacement only when
   shadow metrics meet or exceed baselines. Keep the external as
   fallback for 7 days post-cutover.

**No big-bang migrations.** Each step is independently reversible.

### 3. Gate as Source, VPS as Touchpoint

The gate hardware is the source of truth. The VPS is a touchpoint —
it terminates TLS, relays traffic, and caches content, but it owns
nothing. All state lives inside the gate's intracellular membrane.

| Layer | What | Trust | Example |
|-------|------|-------|---------|
| **Intracellular** | Gate hardware, full NUCLEUS, all data | Covalent (full trust) | Active gate, 13 primals |
| **Inner membrane** | VPS touchpoint — relay, TLS, cache | Controlled (we own it, provider has hypervisor) | cellMembrane fieldMouse |
| **Outer membrane** | GitHub mirror, CDN fallback | Observed (no trust, public) | primals.eco on GitHub Pages |
| **Extracellular** | External APIs, registries, DNS | Weak (Dark Forest principle) | crates.io, NCBI, Let's Encrypt |

---

## Bonding Model in Infrastructure

The four-bond model from chemistry maps to infrastructure trust:

### Covalent (Shared Seed, Full Trust)
- **Scope**: All content, all methods, all state
- **Auth**: BearDog family seed, BTSP mutual auth
- **Where**: LAN cluster (active gate ↔ strandGate), covalent gate mesh
- **Routing**: Direct dispatch, zero relay overhead
- **Example**: Two machines in the same basement sharing a family seed

### Ionic (Scoped Token, Metered Access)
- **Scope**: Scoped by capability token (e.g., `compute.*` but not `storage.*`)
- **Auth**: BearDog Ed25519-signed ionic tokens with expiry + JTI
- **Where**: ABG collaborators, friend's GPU, JupyterHub users
- **Routing**: Authenticated BTSP tunnel, resource envelopes enforced
- **Example**: A collaborator running notebooks through JupyterHub

### Metallic (Delocalized, Institutional)
- **Scope**: Fleet-wide capability sharing, no single-point trust
- **Auth**: Institutional certificate chain + BTSP overlay
- **Where**: University HPC (ICER), datacenter fleets
- **Routing**: biomeOS mesh routing, sunCloud economics
- **Example**: ICER cluster nodes joining as metallic compute providers

### Weak (Pre-Trust, External)
- **Scope**: Read-only public data, health checks, ACME challenges
- **Auth**: None (or Let's Encrypt ACME)
- **Where**: CDN fallback, Dark Forest beacons, initial contact
- **Routing**: VPS cache serves, no gate involvement
- **Example**: A browser hitting primals.eco for the first time

---

## Content-Aware Routing Standard

All membrane deployments must implement content-aware routing. Requests
are classified by type and routed to the appropriate backend:

| Content Class | Backend | Rationale |
|---------------|---------|-----------|
| ACME challenges | VPS local | Must be served from the IP the cert is for |
| Health/status | VPS local | Always available, zero gate dependency |
| Static assets (CSS/JS/images) | VPS cache (NestGate) | Cached locally, webhook-invalidated |
| Git operations | Gate (BTSP tunnel) | Authenticated, stateful |
| API/RPC | Gate (BTSP tunnel) | Authenticated, requires primal access |
| Auth flows | Gate (BTSP tunnel) | BearDog handles all identity |
| Large downloads (>50MB) | Songbird P2P | Avoid VPS bandwidth costs |
| Fallback | GitHub CDN | Last resort, always available |

**Cache policy**: 256MB max per VPS, 1-hour TTL, webhook-based invalidation
from gate NestGate. Cache misses proxy to gate via BTSP tunnel.

**Cost awareness**: Prefer P2P for large transfers. VPS bandwidth is metered.

---

## Membrane Channel Standards

Three channels define the cell's external interfaces (see
`MEMBRANE_CHANNEL_ARCHITECTURE.md` for full specification):

### Channel 1: Signal (DNS)
- **Process**: knot-dns on VPS
- **Port**: 53
- **Trust**: Lowest — public data
- **Status**: PENDING (DoT intermediate active, sovereign DNS not started)

### Channel 2: Relay (NAT Traversal)
- **Process**: Songbird TURN relay on VPS
- **Port**: 3478
- **Trust**: Credential-authenticated (HMAC)
- **Status**: LIVE (157.230.3.183)

### Channel 2b: Remote Access (RustDesk)
- **Process**: hbbs/hbbr on VPS
- **Ports**: 21115-21117
- **Trust**: Key-authenticated (ed25519)
- **Status**: LIVE

### Channel 3: Surface (TLS)
- **Process**: Caddy (transitional) → Songbird (sovereign)
- **Ports**: 80 (ACME/health), 443 (TLS termination)
- **Trust**: ACME cert (Let's Encrypt), content-aware routing
- **Status**: SHADOW (HTTP health on :80, TLS blocks ready for DNS grey-cloud)

**Primal role clarification**:
- **Songbird** handles TLS termination (long-term sovereign TLS)
- **BearDog** handles cryptographic identity (key management, BTSP, encryption)
- **Caddy** is transitional — used until Songbird absorbs TLS capability

---

## Credential Management Standard

### At Rest
All credentials on external substrate (VPS) must be encrypted at rest:
- **Method**: BearDog AES-256-GCM with Argon2id KDF
- **Key storage**: BearDog keyring (`beardog key generate`)
- **Format**: `.age` files (e.g., `/opt/membrane/credentials.age`)
- **Verification**: darkforest MEM-15 checks encryption at rest

### In Transit
- **BTSP Phase 3 AEAD** for all inter-primal communication
- **TLS** for browser-facing connections
- **SSH key-only** for VPS management (no passwords)

### Rotation
- Cookie secrets: monthly via `rotate_cookie_secret.sh`
- SSH keys: via `deploy_membrane.sh keys {add,revoke}`
- Ionic tokens: scoped expiry (purpose-based via `auth.issue_session`)

---

## VPS Deployment Standard

### Sizing
| Phase | SKU | RAM | Services | Cost |
|-------|-----|-----|----------|------|
| 0.5 (relay-only) | s-1vcpu-512mb-10gb | 512MB | Songbird + RustDesk | ~$4/mo |
| 1.0 (Tower) | s-1vcpu-2gb | 2GB | + BearDog + SkunkBat + Caddy | ~$12/mo |
| 2.0 (full membrane) | s-2vcpu-4gb | 4GB | + knot-dns + NestGate cache | ~$24/mo |

### Service Persistence
- All services managed by systemd with `Restart=always`
- Runtime directories via `tmpfiles.d/membrane.conf` (survives reboots)
- All primal ports on `127.0.0.1` except explicit public listeners
- Logs via journald (persistent to `/var/log/journal/`)

### Security Baseline
Validated by `darkforest_membrane.sh` (MEM-01 through MEM-15):
- SSH: key-only, fail2ban, multi-gate managed
- Firewall: UFW deny-default + targeted allows
- Services: no unnecessary packages (exim4, droplet-agent, snapd purged)
- Credentials: 600 permissions, root-owned, encrypted where possible
- Binary integrity: BLAKE3 checksums (when b3sum installed)

---

## Forgejo as Primary Git Host

### Standard
- **Forgejo is source of truth** for all ecoPrimals repositories
- **GitHub is the push mirror** (outer membrane) — public visibility, CDN
- **Dual-push workflow**: `git push forgejo && git push origin`
- **Credential caching**: `.netrc` with API token (chmod 600)

### Organization Mapping
| Forgejo Org | GitHub Org | Repo Count |
|-------------|-----------|------------|
| sporeGarden | sporeGarden | 5 |
| ecoPrimals | ecoPrimals | 19 |
| syntheticChemistry | syntheticChemistry | 8 |

### Migration Path
1. **Current**: Forgejo primary, GitHub mirror, manual dual-push
2. **Next**: Forgejo Actions for CI (74 workflow files to port)
3. **Future**: GitHub becomes read-only mirror (Forgejo webhook push)

---

## Validation Standards

### Dark Forest Glacial Gate (deploy graph validation)
All deploy graphs must pass `dark_forest_gate_local.sh` (33 checks, 5 pillars):
- `secure_by_default = true` in `[graph.metadata]`
- All nodes reference valid plasmidBin binaries
- Dependency ordering is acyclic
- Port assignments are unique
- Auth mode defaults to `enforced`

### Membrane Audit (VPS validation)
`darkforest_membrane.sh` validates MEM-01 through MEM-15:
- SSH hardening, firewall posture, credential permissions
- Service inventory, listener audit, binary integrity
- Credential encryption at rest

### Sovereignty Parity (shadow run validation)
benchScale scenarios validate replacement parity:
- `btsp_tls_parity.sh` — BearDog TLS vs Cloudflare TLS
- `songbird_nat_parity.sh` — Songbird TURN vs cloudflared
- `nestgate_content_parity.sh` — NestGate+petalTongue vs GitHub Pages
- `dot_sovereign_parity.sh` — knot-dns vs Cloudflare DNS

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-15 | Initial version — sovereignty standards codified from ecosystem practice |
