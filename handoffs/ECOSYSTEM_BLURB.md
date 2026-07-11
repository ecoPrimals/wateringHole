# ecoPrimals Ecosystem Blurb — Wave 136b

**Date**: Jul 11, 2026 02:15 EDT | **Wave**: 136b | **From**: eastGate overwatch
**Posture**: **HARDENED. Outer membrane sprint complete (9/14 exposures closed). ALL 8 GLACIAL CRITERIA CLEAR. skunkBat HTTP detection live. darkforest v3.0 active. Cooling sprint continues — remaining items are defense-in-depth.**

---

## Wave 136a Sprint — COMPLETE (Jul 10)

Full outer membrane hardening sprint delivered across 4 gates in parallel:

### Exposure Matrix — Closed (9/14)

| ID | What | How | Gate |
|----|------|-----|------|
| EXP-01 | Security headers | HSTS preload (2yr), X-Frame DENY, nosniff, Permissions-Policy, `-Server` on all 5 Caddy blocks | sporeGate |
| EXP-02 | 404 catch-all | `handle_errors` with Zola `404.html`, `try_files` SPA fallback removed | sporeGate |
| EXP-03 | Cert lifecycle | Caddy ACME auto-renewal confirmed for all 5 domains | sporeGate |
| EXP-04 | Forgejo SSH brute-force | fail2ban: port 2222, maxretry=3, ban 1h (already banning IPs) | sporeGate |
| EXP-05 | Depot rate-limiting | iptables: 50 new HTTPS conn/10s per source IP | sporeGate |
| CSP-01 | Content-Security-Policy | `(csp_static)` for Zola, `(csp_proxy)` for Forgejo/lab | sporeGate |
| AUDIT-01 | Access logs | Caddy JSON → `/var/log/caddy/`, 50MiB roll, 30d | sporeGate |
| EXP-07a | WireGuard key audit | `wg-key-audit` tool, 90d rotation policy, 4 peers healthy | sporeGate |
| RF-01 | Cert renewal drill | ACME storage validated, all domain certs confirmed | sporeGate |

### Primal Evolution

| Primal | Commit | What |
|--------|--------|------|
| skunkBat | `f9154a8` | Outer membrane HTTP anomaly detection: `HttpObservation`, `ThreatType::HttpAnomaly`, `advisory_check_http()`, HTTP metrics. 553 tests. |
| songBird | `eb4d0bed` | EXP-06: drawbridge auth-gate hardening (bearer tokens, trusted peers, public paths) |
| cellMembrane | `c1fa85a` | SIGN-01: depot signing pipeline (BLAKE3 + ed25519). Security sprint: fetch verification, headers, cert monitoring. |
| nestGate | `84a8712d` | Coord handler cleanup |
| primalSpring | `e0593a5` | `s_outer_membrane_posture` scenario — 129 scenarios, 1102 tests, 0 fail |
| projectNUCLEUS | `d35df65` | darkforest v3.0 — TLS + outer membrane pen-testing live |

### Exposure Matrix — Remaining

```
ACCEPTABLE (4): EXP-08 (GitHub shadow), EXP-09 (VPS), EXP-10 (registrar), EXP-11 (AI crawlers)
THEORETICAL (3): EXP-12 (physical), EXP-13 (BTSP), EXP-14 (darkForest beacon)
DEFENSE-IN-DEPTH (2):
  EXP-06  Lab auth-gate — songBird drawbridge auth (code landed, Caddy layer pending)
  SIGN-01 Cascade output signing — pipeline landed, activation pending
```

---

## Glacial Shift — ALL 8 CRITERIA CLEAR

Criterion 8 added in Wave 136: outer membrane hardened for public exposure.
**5/5 sub-criteria now met**: headers, 404, fail2ban, CSP, rate-limiting.
SIGN-01 and EXP-06 are defense-in-depth, not stadial blockers.

**The system is now stadial-ready across all criteria.**

---

## Production Architecture (Hardened)

```
Internet → golgi :443
  │
  ├── iptables: 50 new conn/10s per IP
  │
  ├── Caddy (ACME TLS, H2+H3, gzip)
  │   ├── All blocks: security_headers (HSTS, X-Frame, nosniff, -Server)
  │   │
  │   ├── primals.eco      (csp_static) → sporePrint (301 pages, 404.html)
  │   ├── www.primals.eco   → 301 redirect
  │   ├── membrane.*        (csp_static) → depot + nestGate coordination API
  │   ├── lab.*             (csp_proxy)  → WG → songBird drawbridge :7780
  │   ├── git.*             (csp_proxy)  → Forgejo :3000
  │   └── live.*            (csp_proxy)  → WG → petalTongue :9900
  │
  ├── fail2ban: sshd + forgejo-ssh (port 2222, 3-try ban)
  ├── JSON access logs → /var/log/caddy/ (50MiB × 5, 30d)
  └── WireGuard :51820 → 4 peers (90d rotation)

Mesh: eastGate ↔ golgi ↔ ironGate + southGate | sporeGate ↔ flockGate (WAN)
```

---

## Wave 136b Scope

| ID | Task | Owner | Priority |
|----|------|-------|----------|
| SIGN-01 | Cascade signing activation (ed25519 key deploy + verify) | cellMembrane + sporeGate | HIGH |
| EXP-06 | Lab auth-gate at Caddy layer (basic_auth or mTLS on lab.primals.eco) | sporeGate | HIGH |
| SKUNY-INGEST | Wire Caddy JSON logs → skunkBat `baseline.observe` | skunkBat team | MEDIUM |
| DF-REPORT | darkforest v3.0 outer membrane execution report | projectNUCLEUS | MEDIUM |
| SITE-REBUILD | Deploy content.rebuild fix to golgi (Zola auto-build after cascade) | sporeGate | HIGH |

---

## Test Suite Health

| Spring/Primal | Tests | Scenarios | Status |
|---------------|-------|-----------|--------|
| primalSpring | 1,102 | 129 | **GREEN** |
| groundSpring | 1,047+ | — | **GREEN** |
| skunkBat | 553 | — | **GREEN** |

---

## Team Dispatches

| Team | Status | Next |
|------|--------|------|
| **sporeGate/golgi** | Sprint complete: 9 exposures closed, infra hardened | SIGN-01 activation, EXP-06 Caddy auth, site rebuild deploy |
| **skunkBat** | HTTP anomaly detection live (553 tests) | Caddy log ingestion pipeline |
| **darkforest** | v3.0 outer membrane pen-test active | Execution report |
| **songBird** | Auth-gate code landed | Caddy integration for lab.primals.eco |
| **cellMembrane** | SIGN-01 pipeline + content.rebuild landed | Deploy signing keys, deploy rebuilt membrane to golgi |
| **sporePrint** | 301 pages live, auto-merge from groundSpring | Content evolution continues |
| **primalSpring** | 1,102 tests, outer membrane scenario landed | SHOW_HN E-category evidence |
| **nestGate** | Coordination backend operational | Cert expiry alerting (136d) |

---

## Gate Convergence

```
✅ eastGate    — Overwatch consolidated. All repos current. 136b coordinated.
✅ sporeGate   — Security hardened (9/14 closed). Depot 100%. Site live.
✅ golgiBody   — Caddy hardened, certs renewing, fail2ban active, rate-limited.
✅ flockGate   — WAN PASS. Outer membrane validation confirmed remotely.
✅ ironGate    — darkforest v3.0 active. Heads published.
🔧 strandGate  — Enrollment pending (house 2).
📱 grapheneGate — Pending pepti pull + ADB deploy.
```

*Wave 136b: Warming event fully contained. ALL 8 stadial criteria clear. Outer membrane hardened. Cooling sprint continues for defense-in-depth. System stable under public observation.*
