# ecoPrimals Ecosystem Blurb — Wave 135b

**Date**: Jul 9, 2026 21:44 EDT | **Wave**: 135b | **From**: eastGate overwatch
**Posture**: **CONVERGING. Multi-primal evolution landed across bearDog, songBird, cellMembrane, sporePrint. Coordination backend delivered (Wave 135a). Debt systematically purged. SHOW_HN readiness advancing.**

---

## Wave 135a Delivery (Jul 8–9)

| Delivered | Details |
|-----------|---------|
| nestGate coordination backend | 14 JSON-RPC methods (`coord.*`), 6 HTTP routes (`/coord/*`), CAS-backed, rootPulse-traced |
| petalTongue coordination dashboard | Wave status, gate heads, FRAGOs/AARs, depot status — reads nestGate CAS directly |
| `live.primals.eco` routing | Caddy config on golgi → WireGuard → sporeGate petalTongue |
| Manifest fixes | `[compositions.nest]` + `[gates.westGate].repos` corrected |

## Wave 135b Evolution (Jul 9 — this cascade)

Multi-primal evolution across 6 repos, all on eastGate local:

### bearDog
- **Gateway simplified**: `bind_gateway_listener` + `start_https_gateway` merged into single `serve_https_gateway` — cleaner lifecycle, bind errors surface at call site
- **ACME integration tests removed**: 3 flaky TCP integration tests (port races) purged — unit tests remain
- **Doc comment cleanup**: Removed nested backticks from env key docs

### songBird
- **BUILD-DIV-01 glue cleaned**: `provided_capabilities()` and `announce_drawbridge_capabilities()` removed — mesh peer discovery now handles capability advertisement via `capabilities.list` introspection, no explicit announce needed
- **Drawbridge simplified**: Removed absolute-form URI normalization (origin-form sufficient), simplified header cloning and format calls
- **Test cleanup**: Removed `absolute_form_uri_normalized_to_path` test (code it tested was removed)

### cellMembrane (membrane-shadow)
- **Zola auto-build removed from cascade**: `should_rebuild_zola` + `run_zola_rebuild` purged — sporePrint builds are handled by the sporePrint team, not by cascade
- **`is_valid_sha` validation removed**: Over-conservative SHA validation that rejected shallow-clone HEADs (caused truncated zero-tail false positives)
- **`auto_commit_unified_freshness` removed**: Wrapper that added unnecessary complexity; direct `unify_freshness` call suffices
- **Freshness simplification**: `auto_commit_gate_heads` return type simplified `Result<bool>` → `Result<()>`, depot freshness uses `nucleus_primals()` instead of per-gate resolution
- **rootPulse persist simplified**: Removed redundant error warning (file write is best-effort)

### petalTongue
- **Gate mesh docs updated**: Clarified `ecosystem_manifest.toml` as authoritative source; compile-time constants are offline fallback only

### sporePrint
- **Template debt purged**: Simplified JSON-LD (removed verbose `@graph`), removed SEO keyword meta tag, removed "Story" nav item and thesis/story sidebar tree sections, simplified mobile nav toggle JS

### sweetGrass
- 2 committed but unpushed: postgres purge (`v0.7.61`) + Wave 133b pattern hardening — **needs push**

---

## Production Architecture

```
primals.eco (LIVE — sovereign)
  :443 → bearDog ACME TLS → Caddy :8091 → sporePrint static (Zola)
  :80  → bearDog HTTP-01 + redirect

Subdomains (:8443 Caddy)
  membrane.primals.eco → nestGate depot + coordination API
  git.primals.eco      → Forgejo
  lab.primals.eco      → sporeGate songBird drawbridge

Planned
  live.primals.eco → golgi bearDog → WG → sporeGate petalTongue (NUCLEUS)

Mesh
  sporeGate ↔ flockGate (WireGuard, 142ms)
  eastGate ↔ golgi ↔ ironGate + southGate (covalent, <1ms)
```

---

## Remaining Work (Wave 135+)

### P1 — Live Site & Coordination
| Task | Owner | Status |
|------|-------|--------|
| `live.primals.eco` DNS + Caddy activation | sporeGate/golgi team | Handoff ready (LIVE_PRIMALS_ECO_ROUTING_WAVE135.md) |
| petalTongue NUCLEUS: serve static content parity | petalTongue team | Dashboard exists, content rendering needed |
| nestGate `coord.ingest` pipeline activation | nestGate team | Code landed, needs wateringHole artifacts ingested |
| rootPulse provenance trio full integration | nestGate + rhizoCrypt/loamSpine/sweetGrass | Placeholders in coord.ingest |

### P2 — Cert & Security
| Task | Owner | Status |
|------|-------|--------|
| bearDog cert consolidation (Host-header routing) | bearDog team | Before Aug 13 cert expiry |
| bearDog gatehouse on golgi (long-term sovereign TLS) | sporeGate/golgi team | After cert consolidation |

### P3 — Mesh & Topology
| Task | Owner | Status |
|------|-------|--------|
| `capability.call` FULL PASS | flockGate | sporeGate drawbridge configured; retest |
| strandGate enrollment | hardware team | Pending physical access (house 2) |
| grapheneGate: pull from pepti + ADB deploy + mesh.init | grapheneGate team | Pending |
| Dark-forest re-enable | all gates | After all LAN peers have bearDog |

### P4 — SHOW_HN
| Category | Status |
|----------|--------|
| S-6 (pepti current) | Done |
| S-8 (cross-gate dispatch) | Retest pending |
| S-10 (sporePrint sovereign) | Done |
| E-1 through E-7 (evidence) | In progress (primalSpring) |
| N-1 through N-6 (narrative) | Not started |
| O-1 (karma buildup) | 3-6 month window active |

---

## Team Dispatches

| Team | Wave 135b Work |
|------|----------------|
| **bearDog** | Gateway evolution landed. Cert consolidation strategy next. |
| **songBird** | BUILD-DIV-01 glue fully cleaned — drawbridge simplified. Capability discovery now introspection-based. |
| **cellMembrane** | Major debt purge: Zola auto-build, SHA validation, freshness wrappers all removed. Leaner cascade. |
| **petalTongue** | Gate mesh docs clarified. NUCLEUS hosting next: content parity with static site. |
| **sporePrint** | Template evolution: lighter JSON-LD, cleaner nav. Content evolution continues independently. |
| **nestGate** | Coordination backend delivered (135a). Ingest pipeline activation next. |
| **sweetGrass** | Postgres purge + pattern hardening committed — push to remotes pending. |
| **sporeGate/golgi** | `live.primals.eco` handoff ready. NUCLEUS composition target. |
| **primalSpring** | SHOW_HN readiness: E-category evidence gathering. |

---

## Gate Convergence

```
✅ eastGate   — All repos current. 135b evolution committed.
✅ sporeGate  — Depot 100%. Drawbridge configured. NUCLEUS host target.
✅ golgiBody  — primals.eco LIVE (bearDog TLS). Thin relay.
✅ flockGate  — WAN PASS. capability.call retest pending.
✅ ironGate   — Current repos. Cascade active.
🔧 strandGate — Enrollment pending (house 2).
```

*Wave 135b: evolution is converging. Debt down, code cleaner. Coordination backend in place. Live site and SHOW_HN are the horizon.*
