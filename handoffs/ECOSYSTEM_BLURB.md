# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 17:45 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** `*.primals.eco` wildcard DNS active. FP-API GIS proxy live. Terminology hardened. 3 items remain. 7,750+ tests / 0 fail.

---

## Remaining — 3 items

### P1

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **DRAWBRIDGE-CAP** | songBird | Drawbridge routes not advertising as capabilities. Blocks `capability.call` for bridged services. | 2-4hr |
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. Last piece for lifecycle authority. | 4-8hr |

### P2

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation for HTTPS outbound. | 2-4hr |

---

## Resolved This Wave — Discussion Items

| Item | Resolution |
|------|-----------|
| ~~CERT-OWNER~~ | **Terminology conflation, not ownership issue.** "Certificate" was conflating two systems: **Loam Certificates** (intracellular provenance artifacts — loamSpine `certificate.mint`, NFTs) and **TLS credentials** (drawbridge transport — Caddy/ACME, golden cage). loamSpine ownership was always correct. Glossary updated with full Loam Certificate entry, boundary distinction, and bond-type mapping. |
| ~~VERSION-SKEW~~ | **Differential evolution is intentional.** Archaea, microbes, algae evolved at different rates — version depth reflects internal evolution pressure, not cross-system maturity. No primal is 1.0 yet. Glossary updated with versioning philosophy and team guidance. |
| ~~PEPTI-TARGETS~~ | **Elevated to next glacial goal: Universal Substrate Evolution.** Multi-arch depot parity (Android NDK, RISC-V, Windows, WASM, macOS Silicon) is the post-stadial evolution target. Every architecture that runs a NUCLEUS is a potential sovereign node. Glacial readiness updated with full target matrix. |

---

## Wave 137b Closures (cumulative)

| Item | Resolved By |
|------|-------------|
| ~~DNS-WILDCARD~~ | Operator — `*.primals.eco` wildcard A record, 5 individual records removed |
| ~~FP-API-CADDY-DEPLOY~~ | sporeGate — 10 GIS proxy routes live via Caddy snippet, CSP tightened |
| ~~SONGBIRD-LOCAL~~ | songBird — drawbridge cleanup + `to_lowercase()` elimination (17 files) |
| ~~DEPOT-CHECKSUM~~ | sporeGate — jellyfish triage, native BLAKE3, depot restructured |
| ~~CERT-OWNER~~ | Terminology fix — glossary Loam Certificate vs TLS credential distinction |
| ~~VERSION-SKEW~~ | Documented as intentional differential evolution — glossary + team guidance |
| ~~PEPTI-TARGETS~~ | Elevated to next glacial goal — universal substrate evolution |

---

## Domain Identity

- **`primals.eco`** — ecosystem platform (depot, forge, compositions, public tools)
- **`primal.eco`** — personal sovereign substrate (sporePrint, mesh, HPC)
- **`nestgate.io`** — federated data gateway (CAS backbone, drawbridge weak bonds for NCBI, PubMed, USGS)

Wildcard `*.primals.eco` → Caddy routing. New subdomains need only a Caddy block.

---

## Gate Status

```
eastGate     — Overwatch. 13 primals. songBird v0.2.1 (2 peers). All tasks DONE.
sporeGate    — NUCLEUS. live.primals.eco + FP-API GIS proxy live. Depot 35/35.
golgiBody    — Full mirror. Wildcard DNS. Forgejo healthy.
flockGate    — 144 scenarios / 1,190 tests. footPrint wiring handoff active.
ironGate     — Node atomic. Own overwatch.
```

**Active Handoffs**: `SCRIPT_JELLYFISH_TRIAGE_AAR_137b.md`, `FOOTPRINT_PRIMAL_WIRING_HANDOFF_137b.md`

**Next Glacial Goal**: Universal Substrate Evolution — multi-arch NUCLEUS deployments across Android, RISC-V, Windows, WASM, macOS.

---

*Wave 137b: 3 P1/P2 items remain. All discussion items resolved (terminology, versioning, substrate targets). Glossary and glacial readiness updated. All repos clean. 7,750+ tests / 0 fail.*
