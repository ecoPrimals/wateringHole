# Wave 114 — fieldGate Onboarding + RustDesk Relay + Network Segmentation

**Status**: ACTIVE | Wave 113 exit 5/6 (hardware enrollment pending — THIS WAVE CLOSES IT)
**Date**: June 15, 2026
**From**: eastGate overwatch

---

## Objective

Three threads converge: onboard `fieldGate` NUC (satisfies hardware enrollment criterion),
validate RustDesk relay as sovereignty layer, and codify network segmentation for the mesh.

---

## Thread 1: fieldGate NUC Onboarding (P1)

**Owner**: ops (physical) + cellMembrane/ironGate (bootstrap)

A fresh NUC with zero context. `gate.bootstrap` must work end-to-end.

| Phase | Owner | Task |
|-------|-------|------|
| Physical | ops | Rack, power, Cat6e cable, base OS, SSH reachable |
| Bootstrap | cellMembrane | `gate.bootstrap --gate fieldGate --profile canary-fieldmouse` |
| Validate | cellMembrane | 13/13 alive, mesh enrolled, cascade from VPS works |
| RustDesk | cellMembrane | Client installed, relay reachable via golgiBody-ext |

**Success**: fieldGate healthy in mesh = Wave 113 exit criterion #4 MET = Wave 113 CLOSED.

**Handoff**: [FIELDGATE_NUC_ONBOARDING_WAVE114_JUN15_2026.md](FIELDGATE_NUC_ONBOARDING_WAVE114_JUN15_2026.md)

---

## Thread 2: RustDesk Relay Validation (P2)

**Owner**: cellMembrane/ironGate

RustDesk is sovereignty infrastructure — used like Forgejo. Self-hosted relay validates
primal-native remote access solutions (songBird mesh, SSH tunnels) over time.

| Task | Status |
|------|--------|
| Verify hbbs-membrane + hbbr-membrane alive on golgiBody-ext (:21115-21117) | TODO |
| Add relay to cellMembrane health sweep (systemd alive + port probe) | TODO |
| LAN gates: P2P direct, relay fallback via VPS | TODO |
| WAN gates (flockGate): relay-only via golgiBody | TODO |
| Key distribution: relay public key during gate.bootstrap | TODO |
| projectNUCLEUS: ABG member compute access via relay | TODO |

---

## Thread 3: Network Segmentation (P2)

**Owner**: cellMembrane/ironGate

Routing policy codified. cellMembrane enforces based on gate `transport` field.

| Zone | Gates | Routing |
|------|-------|---------|
| Internal (LAN) | east, iron, field, north, strand, south, west | Direct LAN mesh. No inbound from WAN. |
| External (WAN) | flockGate | Via golgiBody relay ONLY. No direct LAN access. |
| Bridge (VPS) | golgiBody, golgiBody-ext, pepti | Relay hub. Forwards external↔internal. |
| Mobile | grapheneGate | LAN when home, relay when away. |

**Policy document**: [NETWORK_SEGMENTATION_POLICY_WAVE114_JUN15_2026.md](NETWORK_SEGMENTATION_POLICY_WAVE114_JUN15_2026.md)

| Task | Status |
|------|--------|
| Enforce flockGate external-only in mesh peering | TODO |
| Verify LAN gates have no WAN port exposure | TODO |
| Transport-aware mesh config in cellMembrane | TODO |
| RustDesk segmentation (P2P vs relay based on zone) | TODO |

---

## Thread 4: projectNUCLEUS Compute Access (P3)

**Owner**: cellMembrane/ironGate

ABG members need remote access to workload gates. Two patterns:

```
Desktop: ABG member → RustDesk relay → fieldGate intake → Cat6e → workload gate
SSH:     ABG member → golgiBody SSH → ProxyJump fieldGate → workload gate port
```

fieldGate serves as intake node (expendable NUC, absorbs external traffic).

| Task | Status |
|------|--------|
| SSH tunnel pattern documented | TODO |
| RustDesk relay path validated | TODO |
| fieldGate as intake node tested | TODO |
| Access provisioning guide updated | TODO |

---

## Per-Gate Assignment Summary

| Gate | Wave 114 Role |
|------|---------------|
| **fieldGate** | ONBOARDING TARGET — zero to 13/13 via gate.bootstrap |
| **ironGate** | cellMembrane evolution: bootstrap, relay health, segmentation enforcement |
| **eastGate** | Overwatch: blurb/FRAGO/handoff, validate post-bootstrap |
| **golgiBody-ext** | RustDesk relay host (hbbs/hbbr on :21115-21117) |
| **golgiBody** | Mesh relay hub, depot authority, songBird federation hub |
| **flockGate** | Segmentation validation target (external-only enforcement) |
| **grapheneGate** | Mobile zone testing (LAN vs WAN relay switching) |
| **ops** | Physical: NUC rack, power, cable, OS, SSH |

---

## Carry from Wave 113

These remain active alongside Wave 114 threads:

| Debt | Owner | Priority |
|------|-------|----------|
| Primal riboCipher signal compliance (6/15) | ALL primal teams | P2 |
| Primal health method compliance (10/15) | ALL primal teams | P2 |
| bearDog: accept prefix + health socket | bearDog team | P1 |
| toadStool: fix silent socket | toadStool team | P1 |
| neuralAPI capability registration | biomeOS team | P2 |
| Diderm leader election (long-term) | cellMembrane | P3 |
| freshness.mesh via songBird (long-term) | songBird + cellMembrane | P3 |

---

## Exit Criteria

| # | Criterion | How |
|---|-----------|-----|
| 1 | fieldGate 13/13 alive in mesh | gate.bootstrap + gate.status |
| 2 | RustDesk relay health-probed | cellMembrane health sweep includes relay |
| 3 | Segmentation enforced | flockGate cannot reach LAN directly |
| 4 | Wave 113 CLOSED | Hardware enrollment (fieldGate) satisfies last criterion |

**Wave 114 closes when fieldGate is healthy and relay + segmentation are validated.**
