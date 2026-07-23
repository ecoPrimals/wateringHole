# ecoPrimals Ecosystem Blurb — Wave 150w

**Date**: Jul 23, 2026 13:50 EDT | **Wave**: 150w | **From**: eastGate overwatch
**Posture**: **`tower.shadow` SHIPPED. songBird P0s FIXED. Shadow deploy UNBLOCKED.**

---

## LATEST — Gate Team Progress (Jul 23 afternoon)

### cellMembrane team (sporeGate) — P0 RESOLVED

**Shipped `membrane tower.shadow`** — 1,204 lines, 14 tower tests, 0 warnings.

```
membrane tower.shadow --enable [--interval N]   # Install systemd timer
membrane tower.shadow --disable                 # Remove timer
membrane tower.shadow.status                    # Timer + results
membrane tower.status                           # Stack health (3/3 LIVE)
membrane tower.benchmark [--peer ADDR]          # Immediate benchmark
```

Shadow timer active on sporeGate at 60min interval across all mesh peers.
Depot binary updated. Available for all gates.

Also completed:
- `BUILD_AUTHORITY=1` activated (songbird-gateway restarted)
- Sovereign CI hook confirmed on 29 repos
- petalTongue v1.7.0 deployed (Wave 150u)

### songBird team (flockGate) — P0s RESOLVED

- **Mesh enrollment FIXED** — stale peers replaced, 3/3 online (sporeGate, eastGate, golgiBody)
- **`songbird.sock` FIXED** — proper UDS socket file, not directory
- **Capability routing PROVEN LIVE** — `capability.call` routes to correct providers. **Exploration Domain 1 confirmed.**
- **Drawbridge 502 ROOT-CAUSED** — `CapabilityProxyRouter` can't proxy HTTP→JSON-RPC. Needs code change (eastGate).
- Shipped `mesh.prune_stale` RPC + socket dir guard + drawbridge diagnostics (184 lines)
- Cascade synced 37/39 repos

### skunkBat team (flockGate)

- Deep debt sweep: error surfacing, timeout unification, named constants (11 files)

### sporeGate ops AAR corrections

- petalTongue v1.7.0 already deployed (was listed as P1 — now done)
- TURN relay already LIVE since Jul 12 (was listed as blocker — never was)
- Direct LAN peering: sporeGate↔eastGate unreachable despite same /22 subnet — likely different VLAN/switch segment

---

## P0 — REMAINING (eastGate code tasks)

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 1 | **Drawbridge JSON-RPC→HTTP translation** | eastGate / songBird | `CapabilityProxyRouter` needs to speak JSON-RPC to backends and translate to HTTP responses. Root-caused by flockGate. |
| 2 | **`checksums.toml` format migration** | eastGate / cellMembrane | New membrane expects struct entries, depot has plain strings. depot.integrity DEGRADED on flockGate. |
| 3 | **Enable `tower.shadow` on flockGate + golgiBody** | sporeGate topology | Binary is in depot. Install and `membrane tower.shadow --enable` on remaining gates. |

---

## P1 — TOPOLOGY (sporeGate team)

All hardware, networking, and physical topology owned by sporeGate.

| # | Task | Detail |
|---|------|--------|
| 1 | **MikroTik LAN peering** (sporeGate ↔ eastGate) | Both wired into same MikroTik. 192.168.4.3↔192.168.4.30 unreachable — check firewall rules, allow songBird ports (:7700, :7780) between LAN IPs. Unlocks sub-1ms benchmarks. |
| 2 | **songBird LAN peer discovery** | Add `lan_addr` to `peers.toml` enrollment so songBird tries LAN path (priority 0) before WG overlay. songBird already prefers `EndpointType::Local` over all other paths. |
| 3 | **10G backbone cabling** | 4 towers NIC'd (northGate, southGate, eastGate, westGate). Cabling sole blocker for ≥1Gbps sustained. |
| 4 | iperf3 sustained throughput baseline | Deferred until LAN peering established. |
| 5 | Gate enrollment (southGate, strandGate) | USB staged. Physical access required. |

---

## P1 — EXPLORATION (primalSpring teams across all 3 gates)

Tower already **2x WG throughput on WAN**. Capability routing **proven live** on flockGate.

| # | Domain | Scenario | Status |
|---|--------|----------|--------|
| 1 | **Capability-aware routing** | `s_tower_capability_routing` | **PROVEN LIVE** (flockGate) |
| 2 | Multi-stack routing | `s_tower_multi_stack` | Structural GREEN |
| 3 | Large data transfer | `s_tower_large_data` | Structural GREEN |
| 4 | Secure compute mesh | `s_tower_secure_compute` | Structural GREEN |
| 5 | Distributed compute | `s_tower_compute_mesh` | Structural GREEN |
| 6 | Edge/SFF profile | `s_tower_edge_profile` | Structural GREEN |

### Why Tower exceeds WG

| WireGuard | Tower Atomic |
|-----------|-------------|
| All packets same tunnel | Routes by capability — knows *what* the traffic is |
| One tunnel per peer | N stacks per relay, each tuned for a traffic class |
| Fixed MTU (1420) | Negotiable framing — jumbo on 10G, chunked on WAN |
| Just a pipe | Compute-aware: workloads route to right substrate |

---

## P2 — Queued

| # | Task | Owner |
|---|------|-------|
| 1 | sporePrint primal pipeline | eastGate |
| 2 | CredentialStore squirrel integration | eastGate |
| 3 | bingoCube WASM WebGL widget | eastGate |
| 4 | Android Keystore + grapheneGate test | bearDog (flockGate) |
| 5 | Promote 6 pseudoSpores | lithoSpore |
| 6 | footPrint declarative source registry | flockGate |

## P3 / Future

| # | Task |
|---|------|
| 1 | Phase 3 cutover — Tower replaces WG |
| 2 | rootPulse sovereign VCS |
| 3 | pseudoSpore Explorer |
| 4 | SHOW_HN readiness |

---

## WHAT'S DONE

| Achievement | Wave |
|-------------|------|
| `membrane tower.shadow` shipped, P0 blocker RESOLVED | 150w |
| songBird P0s fixed: mesh enrollment, socket, prune_stale | 150w |
| skunkBat deep debt sweep | 150w |
| Capability routing proven LIVE (Domain 1 of 6) | 150w |
| Tower 2x WG throughput on WAN, sovereign CI 43/43 | 150w |
| Tower Atomic PHASE 1 PASS — full WG parity LAN + WAN | 150w |
| Sovereign depot pipeline (4 phases + deep debt sweep) | 150w |
| petalTongue v1.7.0 deployed on sporeGate + flockGate | 150u |
| Benchmark harness shipped, TURN relay LIVE | 150v |
| Standards reorg, DNSSEC 3/3, Sovereignty roadmap | 150s-u |
| Scene unification, NUCLEUS, Silicon Atheism P2, CAC 6/6 | ≤150i |

---

## TEAM TOPOLOGY

```
eastGate (.5)    — primalSpring code hub (scenarios, integration, overwatch)
sporeGate (.2)   — cellMembrane + topology (build, membrane, hardware, networking)
flockGate (.6)   — songBird + Tower Atomic primals (transport, crypto, protocol)
golgiBody (.1)   — hub infrastructure (TURN relay, depot, CI hooks)

Experiment coordination:
  primalSpring on sporeGate — topology ops, benchmark execution, AARs
  primalSpring on flockGate — WAN peer, Tower primal validation
  primalSpring on eastGate  — code evolution, scenario authorship
```

```
golgiBody (10.13.37.1) — hub, VPS, TURN relay, CI 29/43, depot
  ├─ sporeGate (10.13.37.2) — cellMembrane, BUILD_AUTHORITY=1, shadow ACTIVE
  ├─ eastGate  (10.13.37.5) — primalSpring code hub, Akida NPU
  ├─ flockGate (10.13.37.6) — songBird 3/3 online, capability routing LIVE
  ├─ ironGate  (10.13.37.7) — [DOWN]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]
```

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic | **EXCEEDS on WAN. Shadow mode ACTIVE.** |
| **REPLACE** | Zola | petalTongue + nestGate CAS | petalTongue deployed, pipeline design pending |
| **LATE-STAGE** | Forgejo | rootPulse | Post-rootPulse |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk | Outer membrane stays |

---

*Wave 150w: `tower.shadow` SHIPPED by cellMembrane (sporeGate). songBird P0s
FIXED by flockGate team (mesh enrollment, socket, prune_stale). Capability
routing proven LIVE — Domain 1 of 6 confirmed. Shadow deploy UNBLOCKED.
Remaining P0: drawbridge JSON-RPC→HTTP translation, checksums.toml format.
Topology (sporeGate): MikroTik LAN peering + 10G cabling + gate enrollment.
43/43 converged.*
