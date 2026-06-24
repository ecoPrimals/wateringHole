# ecoPrimals Ecosystem Blurb — Wave 127

**Date**: Jun 24, 2026 08:10 EDT | **Wave**: 127 | **From**: eastGate overwatch
**Cascade**: All repos at parity. golgi auto-relays every 15min.
**Posture**: Convergence + debt reduction. Operator bandwidth limited this week.

---

## You Are Here

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals (NUCLEUS) coordinated via WireGuard overlay + Forgejo.

**This week: convergence and debt. No new features. Stabilize, test, clean.**

---

## Gate Map

| Gate | WG IP | NUCLEUS | Tests | Role |
|------|-------|---------|-------|------|
| **golgi** | .1 | 18 svc | — | WG hub, Forgejo, depot, cascade timer |
| **sporeGate** | .2 | 13/13 | 833 (CM) | Build authority, Nest, firewall, public IP |
| **eastGate** | .5 | 13/13 | 1038 (PS) | Overwatch, primalSpring, Meta |
| **flockGate** | .6 | 13/13 | 8929+ (SB) | Tower, sporePrint |
| **ironGate** | .7 | 12/12 | 4619 (BC) | Node compute, GPU (RTX 5070) |

---

## What's Proven (no rework needed)

Everything below is stable. Teams should not revisit unless a regression is found.

- WireGuard 5-node mesh, ATT IP passthrough, Quorum Phase 1 (auto-cascade)
- Sovereign CI (14/14, dual-target musl+gnu), BLAKE3 depot verified
- relay.forward (cellMembrane → songBird E2E), agentic divergence policy
- GPU pipeline (LSTM f64, shader.compile.multi, SM120, quota-aware OOM)
- Network hardening (167k DNS blocklist, DoT, nftables, IPC audit clean)
- metalForge (7 probes, WiFi drift auto-remediation)
- GNU depot built and synced to golgi (Wave 126 — sporeGate P1 DONE)
- Force-with-lease graduated on relay ship (divergence fix operational)

---

## Convergence Tasks (this week)

Focus: close gaps, reduce debt, stabilize. No new features.

### sporeGate

| Task | Priority | Notes |
|------|----------|-------|
| ~~GNU depot build~~ | ~~P1~~ | ✅ DONE (15/15, synced to golgi) |
| Nest provenance depth (ledger → 5+) | P1 | Convergence: deepen existing ledger |
| cellMembrane debt: clippy pedantic sweep | P1 | 833 tests green, clean warnings |
| Depot integrity: scheduled BLAKE3 re-verify | P2 | Cron or timer |
| strandGate/southGate relay push | P2 | Opportunistic |

### flockGate

| Task | Priority | Notes |
|------|----------|-------|
| songBird mesh.init validation | P1 | WG auto-init registered, validate it works |
| bearDog BTSP: auth.trust_issuer to eastGate | P1 | Exchange one key pair as proof |
| skunkBat: audit existing methods, document gaps | P1 | Debt: know what's missing before wiring |
| sporePrint debt: dead pages, stale content | P2 | Content hygiene |

### ironGate

| Task | Priority | Notes |
|------|----------|-------|
| toadStool enrollment (biomeOS composition) | P1 | 12/12 → 13/13, convergence target |
| Validate gnu fetch from golgi depot | P1 | GNU depot is now live — test the fetch |
| barraCuda debt: clippy, test coverage gaps | P2 | 4619 tests, sweep for warnings |
| coralReef debt: SM120 edge cases, doc | P2 | 3631 tests, stabilize |

### eastGate

| Task | Priority | Notes |
|------|----------|-------|
| primalSpring debt sweep (KNOWN_DEBT.md) | P1 | 1038 tests, clean remaining debt |
| Cross-gate scenario: eastGate → sporeGate call | P1 | Validate relay.forward in primalSpring |
| BiomeOS composition test (local multi-service) | P2 | Validate deploy graph on eastGate |
| Overwatch: cascade, review, blurb (reduced cadence) | P2 | Operator limited this week |

---

## Active Impulses

None. Clean slate. Teams work from the task tables above.

---

## Code Metrics

| Repo | Tests | Trend |
|------|-------|-------|
| cellMembrane | 833 | ↑ from 810 (env_or rollout, TLS fix, relay graduation) |
| primalSpring | 1,038 | ↑ from 1017 (GPU dispatch, multigate, debt) |
| barraCuda | 4,619 | Stable (quota-aware OOM shipped) |
| coralReef | 3,631 | Stable (shader.compile.multi shipped) |
| songBird | 8,929+ | Stable (WG auto-init registered) |
| toadStool | 9,127 | Stable (S325) |
| biomeOS | 8,351 | Stable (v4.31) |

---

## Coordination

- **Cascade**: push to Forgejo → golgi relays → GitHub. Agentic divergence handles races.
- **This week**: convergence + debt. No new impulses unless critical.
- **Operator**: limited bandwidth (personal commitment). Hardware tasks deferred.
- **Teams**: work autonomously from task tables. Push results, overwatch reviews next cascade.

---

## Operator-Only (deferred this week)

| Action | Status |
|--------|--------|
| Flint 2 #2 install | Pending delivery |
| MikroTik CRS310 creds | When convenient |

---

*Convergence week. Stabilize what we have. Deepen, don't widen.*
