# projectNUCLEUS: Cell Membrane Architecture + Composition Patterns Handoff

**Date**: 2026-05-10
**From**: projectNUCLEUS (sporeGarden)
**For**: All primal teams, all spring teams, biomeOS, primalSpring
**Phase**: Post-interstadial — cell membrane model operational, zero open upstream gaps

---

## Summary

projectNUCLEUS has evolved through three hosting architectures in 5 days,
settling on a **cell membrane model** that cleanly separates external-facing
infrastructure from sovereign compute. This handoff documents the architecture,
the composition patterns that enabled it, and what each team should absorb.

---

## 1. Cell Membrane Architecture

### The Model

Biological cells accept that the external environment is uncontrolled. They
maintain total control inside, and use a selective membrane to interface.
projectNUCLEUS adopted this model for infrastructure:

```
┌─────────────────────────────────────────────────────┐
│ EXTRACELLULAR (uncontrolled, high-availability)     │
│   primals.eco → GitHub Pages + Cloudflare CDN       │
│   DNS → Cloudflare managed                          │
│   TLS → Cloudflare edge termination                 │
└─────────────────────┬───────────────────────────────┘
                      │ (no gate dependency)
┌─────────────────────┴───────────────────────────────┐
│ MEMBRANE (selective permeability)                    │
│   lab.primals.eco → Cloudflare Tunnel replica pool   │
│   git.primals.eco → Cloudflare Tunnel replica pool   │
│   gate_watchdog.sh → membrane health monitor         │
│   tunnelKeeper → replica count, colo, origin status  │
│   Sub-second failover across replica gates           │
└─────────────────────┬───────────────────────────────┘
                      │ (tunnel ingress → localhost)
┌─────────────────────┴───────────────────────────────┐
│ INTRACELLULAR (total sovereign control)             │
│   13 NUCLEUS primals on 127.0.0.1:9100-9900         │
│   JupyterHub (:8000), Observer (:8866), Forgejo     │
│   pappusCast, darkforest, provenance pipeline        │
│   ABG shared workspace, science workloads            │
└─────────────────────────────────────────────────────┘
```

### Why This Architecture

| Approach | Problem |
|----------|---------|
| Gate-only hosting (original) | Single point of failure; GitHub outage = site outage |
| Dual-hosted with DNS switching | Watchdog latency (minutes), user-visible "fluttering" |
| **Cell membrane** (current) | Public site always up (CDN); internal services failover via tunnel replicas |

### Key Insight

Accept that the extracellular world (CDN, DNS, TLS edge) is outside our
control. Inside the membrane, total sovereign control. The membrane boundary
is a clean delineation for:

- **skunkBat audit logging**: membrane state transitions are observable events
- **Future ionic bonding**: membrane channels become ion channels for scoped
  cross-gate capability sharing
- **Future weak bonding**: external API integrations enter through well-defined
  membrane receptors (not ad-hoc tunnel routes)

---

## 2. NUCLEUS Composition Patterns Validated in Production

### Pattern: Multi-Gate Membrane Replicas

Multiple gates run `cloudflared` as a tunnel replica. Cloudflare load-balances
across all replicas automatically (sub-second failover). No DNS changes needed.

```bash
# Provision a new membrane replica on a remote host
deploy/gate_provision.sh user@friend-machine

# Provision with full compute services
deploy/gate_provision.sh --full user@friend-machine
```

**Relevance to biomeOS**: This is a pre-primal implementation of Plasmodium
multi-gate coordination. When biomeOS implements Plasmodium natively, the
pattern is: discover membrane replicas via Songbird mesh, coordinate
capability routing via Neural API, and let Cloudflare handle the load
balancing until Songbird NAT replaces it.

### Pattern: Membrane Health Monitoring

`gate_watchdog.sh` runs as a systemd service, checking `lab.primals.eco` and
`git.primals.eco` every 30 seconds. It logs state transitions (healthy →
degraded → down) but does NOT take corrective action — the tunnel replicas
handle failover automatically.

**Relevance to skunkBat**: membrane state transitions should be forwarded to
skunkBat as `security.audit_log` events. This is the first real-world use case
for JH-5 cross-primal audit forwarding (Phase 3).

### Pattern: Gate-Agnostic Configuration

All paths, ports, and credentials are sourced from `deploy/nucleus_config.sh`
using `$GATE_HOME` as the anchor. No hardcoded usernames, home directories, or
machine names in runtime code.

```bash
source deploy/nucleus_config.sh
# $GATE_HOME, $ABG_SHARED, $OBSERVER_PORT, $CF_TUNNEL_ID, etc.
```

**Relevance to genomeBin**: This is the configuration model that genomeBin
should adopt. Self-extracting archives should source a gate-level config
rather than baking paths into the binary.

### Pattern: Static Observer Surface

The public observer surface is pre-rendered HTML (no kernel launches, no
compute per visit). pappusCast renders notebooks on a schedule, and
`observer_server.py` serves from disk.

**Relevance to petalTongue**: When petalTongue replaces the observer surface,
it should maintain this zero-compute-per-visit property. DataBinding channels
stream live data TO the page, but the initial page load is always a static
HTML file. This is the correct model for the extracellular surface.

---

## 3. neuralAPI Deployment via biomeOS

### Current State

biomeOS v3.51 provides the Neural API for capability-based routing. All 13
primals are discoverable and routable. Key capabilities used by projectNUCLEUS:

| Capability | Primal | How NUCLEUS Uses It |
|------------|--------|-------------------|
| `crypto.sign` | BearDog | Provenance pipeline (sweetGrass witness signatures) |
| `crypto.hash` | BearDog | BLAKE3 content hashing for all NCBI data |
| `storage.put`/`get` | NestGate | Content-addressed blob storage |
| `compute.dispatch` | ToadStool | Science workload execution |
| `composition.status` | biomeOS | Health monitoring (active gate) |
| `composition.reload` | biomeOS | Hot-swap single primal without restart |
| `method.register` | biomeOS | Dynamic method registration (v3.51) |
| `security.audit_log` | skunkBat | Ring buffer, 7 event kinds, cursor-based polling |
| `auth.public_key` | BearDog | Cross-primal token verification (JH-11) |

### Composition Deployment Pattern

```bash
# Deploy a composition to the active gate
deploy/deploy.sh --composition full --gate mygate

# Validate the composition
darkforest --suite full

# Check composition health
biomeos composition status
```

### What biomeOS Should Absorb

1. **`composition.deploy(graph)`**: projectNUCLEUS currently uses `deploy.sh` +
   systemd. biomeOS should absorb this into graph-driven germination using
   `primalSpring/graphs/fragments/*.toml` as templates.

2. **Membrane monitoring as a composition concern**: biomeOS should be aware
   of membrane health (currently `gate_watchdog.sh`). When biomeOS implements
   `composition.status` for cross-gate awareness, membrane health should be
   a first-class signal.

3. **Replica coordination via Plasmodium**: Multiple gates running tunnel
   replicas is a pre-primal implementation of Plasmodium. biomeOS should
   coordinate replica gates via Songbird mesh discovery.

---

## 4. Lessons Learned (for all teams)

### Architectural Lessons

| Lesson | Detail |
|--------|--------|
| **External dependencies are fine if they're extracellular** | Don't fight CDNs and managed DNS. Accept them as the external environment. Focus sovereignty on what's behind the membrane. |
| **Failover should be structural, not reactive** | DNS-swapping watchdogs are fragile. Tunnel replicas provide structural redundancy. Prefer N+1 replicas over monitoring + switching. |
| **The membrane boundary is the audit boundary** | Everything crossing the membrane is an observable event. This is where skunkBat monitoring belongs. |
| **Static surfaces are sovereign-friendly** | Zero-compute static HTML can survive any hosting model. Dynamic rendering is an intracellular concern. |
| **Pre-primal solutions validate primal architecture** | Bash scripts implementing Plasmodium patterns (gate_provision.sh) prove the architecture works before the primal code exists. |

### Code Quality Lessons

| Lesson | Detail |
|--------|--------|
| **Gate-agnostic from day one** | Hardcoded paths (`/home/irongate/...`) were the most common debt. Use `$GATE_HOME` everywhere. |
| **Env-var-driven with compiled fallback** | darkforest loads config from env, falls back to compiled defaults. This is the correct pattern for all primals. |
| **Error propagation, not panic** | `Result<T, E>` + `thiserror` + `?` operator. Zero `unwrap()` in production paths. tunnelKeeper exemplar. |
| **Slim dependencies** | tokio `rt-multi-thread,macros` (not full), `rand_core` (not `rand`). Every unnecessary feature is attack surface. |

### Deployment Lessons

| Lesson | Detail |
|--------|--------|
| **systemd for persistence** | Every persistent service has a `.service` unit. No screen/tmux/nohup. |
| **Provisioning is a one-command operation** | `gate_provision.sh` copies credentials, installs services, validates health. New replicas in minutes. |
| **Verification loops catch drift** | `tier_test_all.sh` + `sporeprint_verify.sh` + `darkforest --suite full` as daily validation. |

---

## 5. Per-Team Absorption Targets

### biomeOS

- Absorb `composition.deploy(graph)` for graph-driven germination
- Wire `composition.status` with membrane health signals
- Begin Plasmodium multi-gate coordination (Songbird mesh discovery)
- `method.register` now live — dynamic registration replaces static config

### Songbird

- Production STUN client for consumer NAT punch-through (Phase 3c target)
- Multi-gate mesh discovery for Plasmodium replica coordination
- Membrane channel encryption: Songbird replaces Cloudflare tunnel TLS

### BearDog

- ACME certificate issuance for sovereign TLS (Phase 3b)
- Token federation (JH-11) now live — validate cross-gate token verification
- HSM gating for production key material (H2-10)

### petalTongue

- `--docroot` web mode for static content serving (Phase 3a target)
- Zero-compute static HTML as default render mode
- DataBinding channels for live science visualization (streaming, not polling)

### NestGate

- Content-addressed storage for sporePrint content (Phase 3a)
- Collection/manifest concept for versioned site releases
- Blob store integration with petalTongue web mode

### skunkBat

- Absorb membrane state transitions as audit events
- Cross-primal audit forwarding (JH-5 Phase 3) — rhizoCrypt DAG + sweetGrass braid
- Dark Forest beacon coordination at membrane boundary

### Spring Teams (all)

- Wire `src/ipc/` directory with per-primal modules (ludoSpring exemplar)
- `primal-proof` Cargo feature for incremental rewiring (healthSpring exemplar)
- Document IPC mapping in `PRIMAL_PROOF_IPC_MAPPING.md` (hotSpring exemplar)
- petalTongue DataBinding channels for science output
- sweetGrass attribution braids for experiment provenance

---

## 6. Remaining Horizon Targets (from projectNUCLEUS)

These are unblocked and ready to advance during interstadial:

| Horizon | Target | Owner | Status |
|---------|--------|-------|--------|
| H2-05 | NestGate content pipeline | NestGate | Unblocked (NG-1→NG-4 shipped) |
| H2-06 | petalTongue web serving | petalTongue | Unblocked (PT-1→PT-5 shipped) |
| H2-10 | BearDog TLS termination | BearDog | Shipped |
| H2-11 | BearDog rate limiting | BearDog | Shipped |
| H2-13–16 | Songbird NAT chain | Songbird | Shipped |
| H2-19 | BTSP direct resolution | BearDog + Songbird | Future |
| H2-20 | Local recursive resolver | Infrastructure | Future |
| Plasmodium | Multi-gate coordination | biomeOS | Pattern validated (gate_provision.sh) |
| Tier 4 | Binary-only IPC (all springs) | All spring teams | Unblocked (JH-11 resolved) |

---

## References

- `projectNUCLEUS/specs/GATE_PORTABILITY.md` — cell membrane architecture (v0.3.0)
- `projectNUCLEUS/specs/TUNNEL_EVOLUTION.md` — membrane replacement plan
- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — sovereignty roadmap
- `infra/wateringHole/DOWNSTREAM_EVOLUTION_MAY2026.md` — spring evolution targets
- `infra/wateringHole/SPRING_NUCLEUS_AUDIT_MAY2026.md` — per-spring audit
- `infra/wateringHole/handoffs/PRIMALSPRING_POST_INTERSTADIAL_DOWNSTREAM_HANDOFF_MAY10_2026.md`

---

**The membrane is live. The compute is sovereign. The patterns are validated.
Now the primal stack absorbs and replaces the pre-primal scaffolding.**
