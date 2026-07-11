# ecoPrimals Ecosystem Blurb — Wave 136a

**Date**: Jul 10, 2026 21:38 EDT | **Wave**: 136a | **From**: eastGate overwatch
**Posture**: **HARDENING. Outer membrane security headers, 404 fix, fail2ban deployed. Cert auto-renewal confirmed. Warming event (public exposure) contained — cooling sprint in progress. Remaining gaps scoped into 136b-d.**

---

## Wave 136a Delivery (Jul 10)

### Security Hardening — Outer Membrane (sporeGate)

| Exposure | Fix | Status |
|----------|-----|--------|
| **EXP-01** No security headers | `(security_headers)` snippet on all 5 Caddy server blocks: HSTS preload (2yr), X-Frame DENY, nosniff, Permissions-Policy (camera/mic/geo denied), `-Server` | **LIVE** |
| **EXP-02** 404 catch-all | `handle_errors` with Zola `404.html`, `try_files` removed from all blocks | **LIVE** |
| **EXP-04** Forgejo SSH brute-force | `fail2ban` jail: port 2222, maxretry=3, ban 1h, findtime 600s | **CONFIGURED** |
| **EXP-03** Cert lifecycle | Caddy ACME auto-renewal confirmed: `primals.eco` renewed Jul 9 (→Oct 7), `membrane` renews ~Jul 14, `git` ~Jul 27 | **SELF-RESOLVING** |

### Infrastructure Evolution

| Delivered | Details |
|-----------|---------|
| `ironGate` heads published | Wave 136 — darkforest v3.0 scope, projectNUCLEUS `85a1471`, primalSpring `15394dd` |
| sporePrint auto-merge | groundSpring lab notebooks (29 experiments) synced to `primals.eco` |
| Caddy gzip encoding | Enabled on `primals.eco` and `membrane.primals.eco` |
| HTTP/3 confirmed | `alt-svc: h3=":443"` announced on all public domains |

### Test Suite Health

| Spring | Tests | Result |
|--------|-------|--------|
| primalSpring | 1,101 | **0 fail** |
| groundSpring | 1,047+ | **0 fail** |

---

## Remaining Gaps — Wave 136b-d Sprint (4-week timeline)

### Wave 136b — Hardening Continuation (Week 1-2)

| ID | Task | Owner | Priority |
|----|------|-------|----------|
| EXP-05 | Depot rate-limiting (abuse throttle on binary fetch) | sporeGate/golgi | HIGH |
| CSP-01 | Content-Security-Policy header for static sites | sporeGate/golgi | MEDIUM |
| EXP-07a | WireGuard peer key rotation policy (90-day cycle) | mesh team | HIGH |
| SIGN-01 | Code/content signing on cascade output (BLAKE3 + ed25519) | cellMembrane | HIGH |

### Wave 136c — Resilience & Pen Testing (Week 2-3)

| ID | Task | Owner | Priority |
|----|------|-------|----------|
| DF-3.0 | `darkforest` v3.0 — outer membrane scope expansion | projectNUCLEUS | MEDIUM |
| RF-01 | Cert revocation drill (Caddy failover to bearDog) | sporeGate | MEDIUM |
| RF-02 | WireGuard hub failover (golgi → ironGate promotion) | mesh team | MEDIUM |
| RF-03 | Forgejo corruption recovery (re-shallow + depot rebuild) | sporeGate | MEDIUM |
| EXP-06 | Lab auth-gate hardening (songBird drawbridge) | songBird team | HIGH |

### Wave 136d — Monitoring & Detection (Week 3-4)

| ID | Task | Owner | Priority |
|----|------|-------|----------|
| SKUNY-OM | `skunkBat` outer membrane extension (HTTP anomaly detection) | skunkBat team | MEDIUM |
| EXP-07b | Overlay IDS (WireGuard peer anomaly detection) | mesh team | MEDIUM |
| AUDIT-01 | Caddy access log → structured audit trail | sporeGate | LOW |
| ALERT-01 | Cert expiry alerting (7-day warning via rootPulse) | nestGate | LOW |

---

## Production Architecture (Post-Hardening)

```
primals.eco (LIVE — sovereign, hardened)
  :443 → Caddy (ACME TLS, H2+H3, security_headers)
       → sporePrint static (Zola, 301 pages)
       → proper 404 (no catch-all)

Subdomains (all hardened — same security_headers snippet)
  membrane.primals.eco → depot + nestGate coordination API
  git.primals.eco      → Forgejo (fail2ban on SSH:2222)
  lab.primals.eco      → sporeGate songBird drawbridge
  live.primals.eco     → petalTongue NUCLEUS (not yet active)

Mesh (4-gate collective)
  eastGate ↔ golgi ↔ ironGate + southGate (covalent, <1ms)
  sporeGate ↔ flockGate (WireGuard, 142ms)
```

---

## Exposure Triage Summary

```
PATCHED:     EXP-01, EXP-02, EXP-03 (auto), EXP-04
QUEUED:      EXP-05, EXP-06, EXP-07, CSP-01, SIGN-01
ACCEPTABLE:  EXP-08 (GitHub trailing shadow), EXP-09 (VPS provider risk),
             EXP-10 (registrar — DNSSEC mitigates), EXP-11 (AI crawlers — intentional)
THEORETICAL: EXP-12, EXP-13, EXP-14 (physical/crypto — defense exists)
```

---

## Site Content — primals.eco

| Section | Pages | Notes |
|---------|-------|-------|
| Philosophy | 14 | Incl. bibliography, atlasHugged stories |
| Thesis | 17 | Full 16-chapter academic work + references |
| Architecture | 24 | K-Derm, mesh, deployment, renvois |
| Lab | 34 | 29 experiments + 5 synthesis notebooks |
| Story | 3 | Builder narratives |
| Springs | 8 | Per-spring profiles |
| Technical | 8 | Deep-dives (GPU, neuro, sovereign) |
| Audience | 6 | Faculty, students, hardware, compliance |
| Guidestone | 5 | Verification artifacts |
| **Total** | **301** | All rendering properly, SEO-aligned titles |

---

## Team Dispatches

| Team | Wave 136a Status | Next |
|------|-----------------|------|
| **sporeGate/golgi** | Security headers + 404 + fail2ban deployed | Depot rate-limiting (136b), CSP |
| **darkforest** | v3.0 scope published, HEAD registered in ironGate | Outer membrane test suite (136c) |
| **skunkBat** | Inner membrane monitoring active | Extend to outer membrane HTTP (136d) |
| **songBird** | Drawbridge functional | Auth-gate hardening (136c) |
| **mesh team** | 4-gate collective stable | Peer rotation policy (136b), overlay IDS (136d) |
| **cellMembrane** | Cascade lean + working | Signing pipeline (136b) |
| **sporePrint** | 301 pages, auto-merge from groundSpring | Content evolution continues |
| **primalSpring** | 1,101 tests, SHOW_HN E-category | Evidence gathering continues |
| **groundSpring** | 1,047+ tests, lab notebooks live | Feeding sporePrint via auto-merge |

---

## Gate Convergence

```
✅ eastGate    — All repos current. Wave 136a coordinated.
✅ sporeGate   — Security hardened. Depot 100%. Site live.
✅ golgiBody   — Caddy hardened, certs auto-renewing, fail2ban active.
✅ flockGate   — WAN PASS. Peer rotation pending (136b).
✅ ironGate    — Heads published. darkforest v3.0 scope registered.
🔧 strandGate  — Enrollment pending (house 2).
📱 grapheneGate — Pending pepti pull + ADB deploy.
```

---

## Glacial Update

Criterion 8 ("Outer membrane hardened for public exposure") added to `GLACIAL_SHIFT_READINESS.md`.
Current state: **3/5 sub-criteria met** (headers, 404, fail2ban). Remaining: CSP, depot rate-limiting, signing.

*Wave 136a: Warming event contained. Critical exposures patched within hours of identification. Cooling sprint proceeds on 4-week cadence. System stable under public observation.*
