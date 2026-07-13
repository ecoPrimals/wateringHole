# ecoPrimals Ecosystem Blurb — Wave 137b

**Date**: Jul 13, 2026 13:30 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** Phase 1 Neural API authority: 12/12. All 8 glacial criteria CLEAR. Two public surfaces live. 3-gate WG mesh. Depot pipeline 100% Rust. 7,750+ tests / 0 fail.

---

## Dimensional Review

### Temporal

- **Wave**: 137b (Jul 13, 2026)
- **Velocity**: 30+ items delivered this wave. Phase 1 COMPLETE in ~48hr sprint.
- **Active evolution**: songBird refactoring (allocation elimination, 17 files). primalSpring scenario thickening (9 scenarios committed today). footPrint API abstraction layer (274 LOC + 136 LOC tests). projectNUCLEUS synced.
- **Wave history**: 136a (security hardening) → 136b (footPrint integration, K-Derm reaffirmation) → 137a (Neural API activation, FP-DEPLOY, SKUNKY-DEPLOY) → 137b (mesh bidirectional, depot signing, live.primals.eco, jellyfish triage).

### Ecological

- **13 primals** running on eastGate (systemd-managed, all active)
- **48 primals** registered in Neural API on sporeGate (156 capability translations)
- **35 depot binaries** across 3 architectures (x86_64-musl, aarch64-musl, x86_64-gnu)
- **Compositions**: footPrint (GIS SPA), sporePrint (static site), petalTongue NUCLEUS (TOPO-VIS)
- **Test health**: primalSpring 144 scenarios / 1,190 tests (flockGate), groundSpring 1,047+, all 0 fail

### Hardware / Topology

```
eastGate     — i9-12900, RTX 4070 + Akida, 32GB. Overwatch. 13 primals. songBird mesh (2 peers).
sporeGate    — Build authority. Forgejo primary. Neural API systemd. petalTongue :9900. Depot signed.
golgiBody    — DO NYC1 VPS. Thin relay. Caddy (primals.eco, live.primals.eco, membrane, git). Full Forgejo mirror (21 repos).
flockGate    — i9-13900K, RTX 3070 Ti, 64GB. NYC WAN. JupyterHub data plane proven (202ms). footPrint owner.
ironGate     — i9-14900K, RTX 5070, 96GB. Node atomic. Own overwatch agent. JupyterHub v5.4.5.
grapheneGate — Pixel 8a. 13/13 TCP-only. Portable root of trust.
strandGate   — Dual EPYC 7452, 256GB ECC. Offline (enrollment pending).
```

**WireGuard overlay**: eastGate (10.13.37.3, 35ms) ↔ golgi (10.13.37.1) ↔ sporeGate (10.13.37.2, 71ms). flockGate (10.13.37.6, 29ms to golgi).

### Sovereignty / Membranes

**K-Derm three-layer topology (confirmed Wave 136b):**
1. **Capsule** (Cloudflare) — DDoS, CDN, external TLS. Intentionally maintained as drawbridge.
2. **Sovereign Outer** (Caddy + bearDog ACME + skunkBat) — HSTS preload, CSP, fail2ban, rate-limiting, security headers.
3. **Inner** (primals, mesh, UDS IPC, riboCipher) — Zero commercial services in data path.

**DNS**: `primals.eco` (Cloudflare, DNSSEC enabled). `primal.eco` + `nestgate.io` (sovereign knot-dns). DNSSEC active on all.

**Sovereignty shadows**: S1-S4 ALL GRADUATED. S4 auth gate PASSED (Jun 9).

### Depot / Build Pipeline

```
membrane plasmid.harvest → membrane depot.integrity (BLAKE3) → membrane sign.activate (Ed25519) → rsync → plasmid.fetch (verify) → deploy
```

- **100% Rust** — zero bash in build/sign/verify/deploy path
- **`require-signed`** active system-wide (sporeGate + golgi)
- **SIGN-VERIFY-ON-FETCH** implemented (`89bf12f`): fetch → verify → deploy, reject unsigned
- **2,801 lines of bash** fossilized (6 scripts retired)
- **14 evolution targets** identified for next wave (7 have Rust equivalents ready)

### Website / Public Surface

| URL | What | Status |
|-----|------|--------|
| `primals.eco` | sporePrint (301 pages) + footPrint SPA (`/footprint/`) | **LIVE**, TLS/HTTP2, full security headers |
| `live.primals.eco` | petalTongue TOPO-VIS dashboard (7 peers, SSE, API) | **LIVE**, TLS/HTTP2, Caddy reverse proxy to sporeGate:9900 |
| `membrane.primals.eco` | Depot (35 binaries), membrane API | **LIVE** |
| `git.primals.eco` | Forgejo (21 repos full-depth) | **LIVE**, fail2ban SSH protection |
| `lab.primals.eco` | JupyterHub v5.4.5 (ironGate) | **LIVE** via drawbridge relay |

### Security

- **Outer membrane**: HSTS preload (2yr), CSP, X-Frame DENY, nosniff, Permissions-Policy, fail2ban (Forgejo SSH), JSON access logs, cert auto-renewal
- **Depot trust**: Ed25519 signatures, BLAKE3 checksums, `require-signed` enforced
- **Mesh auth**: riboCipher on UDS sockets, Neural API handshake enforcement
- **Live threat data**: 122 unique IPs, 317 SSH brute-force attempts absorbed (7-day window on golgi)
- **skunkBat**: HTTP anomaly detection live (dry-run mode)

### Glacial

**ALL 8 CRITERIA CLEAR FOR STADIAL ENTRY** (unchanged since Wave 111 for criteria 1-7, criterion 8 met Wave 136b, reinforced 137b with SIGN-01 enforcement).

SHOW_HN publication rubric established (`whitePaper/gen5/thesis/SHOW_HN_PUBLICATION.md`). sporePrint drafting publication. 3-6 month karma buildup window provides natural pacing.

---

## Remaining Work — 5 items + 3 discussion

### P1 — Next capabilities

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **FP-API-CADDY-DEPLOY** | sporeGate / golgi | Deploy flockGate's `fp-api-caddy.caddyfile` (130 LOC, 10 GIS hosts) to golgi. footPrint gets full GIS proxy. | 30min |
| **DRAWBRIDGE-CAP** | songBird | Drawbridge routes not advertising as capabilities. Blocks `capability.call` for bridged services. | 2-4hr |
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. Last piece for lifecycle authority. | 4-8hr |

### P2 — Hardening

| ID | Owner | What | Effort |
|----|-------|------|--------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. Unblocks songBird TLS delegation for HTTPS outbound. | 2-4hr |
| **SOCKET-UMASK** | biomeOS | Primals should `fchmod` sockets after bind. | 2hr |

### Discussion

| ID | What |
|----|------|
| **VERSION-SKEW** | 3 version ranges (0.1-0.2, 0.4-0.9, 0.14). Harmonization strategy needed. |
| **CERT-OWNER** | Certificate shows `loamspine`, expected `beardog`. Cosmetic but confusing. |
| **PEPTI-TARGETS** | Missing depot: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`. Future ecoBin matrix. |

### Next Wave — Jellyfish Evolution

From `SCRIPT_JELLYFISH_TRIAGE_AAR_137b.md`: 7 scripts (2,546 LOC) replaceable by existing `membrane` CLI commands. 14 scripts (5,836 LOC) need new Rust commands across cellMembrane, biomeOS, songBird, and sourDough teams.

---

## Active Handoffs

| Handoff | Owner | Status |
|---------|-------|--------|
| `SCRIPT_JELLYFISH_TRIAGE_AAR_137b.md` | All teams | Evolution roadmap — 14 scripts across 4 teams |
| `FOOTPRINT_PRIMAL_WIRING_HANDOFF_137b.md` | songBird, nestGate, petalTongue | API abstraction complete — per-primal wiring instructions |

**Archive**: 438 fossilized handoffs/AARs in `archive/`.

---

*Wave 137b: PUBLIC + SOVEREIGN. All 8 glacial criteria CLEAR. 5 items remain (all independently actionable) + 3 discussion. Two public surfaces live. Depot pipeline fully sovereign Rust. 30+ items delivered this wave. 7,750+ tests / 0 fail.*
