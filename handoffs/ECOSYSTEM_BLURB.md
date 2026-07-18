# ecoPrimals Ecosystem Blurb — Wave 149b

**Date**: Jul 18, 2026 09:05 EDT | **Wave**: 149b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 2 PRODUCTS LIVE. E2E STANDARD ADOPTED.**

**This cascade**: Full dimensional review completed across 7 projects (cellMembrane,
esotericWebb, footPrint, songBird, sporePrint, lithoSpore, primalSpring). Code
quality, debt, safety, file size, test coverage, hardcoded values, production
panics, live service usability all audited. Zero debt markers and zero unsafe
code ecosystem-wide. Key findings: songBird needs clippy + prod unwrap cleanup;
footPrint needs responsive design + accessibility; esotericWebb demo has missing
NPC bug. 18,000+ tests ecosystem-wide.

---

## Upstream Primal Demand Signal

Accumulated needs from all downstream consumers and dimensional review findings.
Each primal team: address your rows.

### songBird (CODE QUALITY — HIGH PRIORITY)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| 556 clippy warnings (pedantic+nursery) | ecosystem quality | **P1** | 170 in orchestrator alone. Top: missing `# Errors` docs (130), `const fn` candidates (87), doc backticks (67). |
| 81 production `unwrap()` calls | runtime safety | **P1** | 76 `writeln!` unwraps in `bin_interface/config.rs`, 5 `RwLock` unwraps in universal-ipc. |
| 2 files over 800 lines | code standards | **P1** | `drawbridge.rs` (1,019), `mesh_seed.rs` (834). Split required. |
| `cargo fmt` (10 files) | CI hygiene | P2 | Quick fix. |
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | Pending. |

### footPrint team (USABILITY — ALL P1 SHIPPED, P2/P3 IN PROGRESS)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| ~~Responsive design~~ | mobile users | — | **SHIPPED** (`7d21b0e`). 3 breakpoints (1024/768/480px), slide-out sidebar drawers, toolbar wraps, hamburger toggle. |
| ~~Accessibility pass~~ | all users | — | **SHIPPED** (`7d21b0e`). ARIA roles/labels/live regions, sr-only labels, aria-modal, aria-pressed, aria-expanded. |
| ~~ESLint gate (162 errors)~~ | code quality | — | **SHIPPED** (`7d21b0e`). 0 errors. Auto-fixed 80, manually fixed 93. Test files: non-null-assertion allowed. |
| ~~First-run guidance / onboarding~~ | new users | — | **SHIPPED** (`40b9cd5`). Welcome overlay with 4-step guide, known locations summary, localStorage gate. |
| ~~Replace `alert()`/`prompt()` with modals~~ | UX polish | — | **SHIPPED** (`40b9cd5`). Async modal.ts utility: `modalAlert`, `modalPrompt`, `modalConfirm`. Zero native dialogs. |
| ~~Favicon missing~~ | branding | — | **SHIPPED** (`40b9cd5`). SVG favicon in browser tabs. |
| ~~Location picker hides descriptions~~ | usability | — | **SHIPPED** (`40b9cd5`). Descriptions shown inline in dropdown options + title attribute. |
| ~~Coverage below thresholds~~ | test health | — | **SHIPPED** (`d792277`). 466 tests. Stmts 92.78%, branches 76.19%, lines 95.27%. All thresholds passing. |

### esotericWebb team (DEMO BUG + OPS)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Missing `aldric` NPC in demo | E2E validity | **P1** | `guided_tour.yaml` step 6 talks to `aldric`, but no `content/npcs/aldric.yaml` exists. Step passes via false-positive string match. |
| `cargo fmt` (3 files) | CI hygiene | P2 | `demo.rs`, `discovery.rs`, experiment file. |
| systemd persistence on flockGate | sporeGate ops | P1 | cellMembrane unit FIXED (`33aa33a`). Deploy: `systemctl enable --now esotericwebb-server`. |
| Caddy route `/webb/` on golgiBody | sporeGate ops | P1 | Caddy config FIXED. Route `/webb/` → `flockGate:8090`. |
| `content/README.md` for authors | author onboarding | P2 | New authors must find `specs/` docs — discoverable README in `content/` would help. |

### cellMembrane (FMT ONLY)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| `cargo fmt` (62 files) | CI hygiene | P2 | Style-only diffs. All other dimensions clean. |

### primalSpring (CODE QUALITY)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| 456 clippy warnings (pedantic+nursery) | code quality | P2 | 320 `doc_markdown` (batch-fixable), 19 `must_use_candidate`, 6 `expect_used`. |
| `cargo fmt` (54 files) | CI hygiene | P2 | 222 diff hunks across scenario files. |
| 4 production `unwrap()` calls | runtime safety | P2 | `s_protokarya_wan_deploy.rs` (1), `s_soundstage_ceremony_observation.rs` (3). |

### lithoSpore — **ALL CLEAR (Wave 149b AAR)**

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| ~~308 clippy warnings~~ | ~~code quality~~ | — | **RESOLVED** — workspace lints handle scientific casts; 4 real warnings fixed (`71438b8`). Clippy 0. |
| ~~ring C/asm dependency~~ | ~~ecoBin purity~~ | — | **RESOLVED** — ring dropped, ureq replaced with curl subprocess (`1191c6e`). BearDog owns crypto. |
| ~~USB round-trip validation~~ | ~~deployment~~ | — | **RESOLVED** — 6-step deploy-test cycle, 5 integration tests (`3c56fc4`). |

### sporePrint (CONTENT FRESHNESS)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| esotericWebb.md: body says live, metadata doesn't | content integrity | P2 | Add `maturity = "live"` to frontmatter + manifest entry. |

### squirrel

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Accept `null` params on health | esotericWebb | P1 | Open |

### nestGate

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | footPrint | P1 | Open |

### petalTongue

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | footPrint | P1 | Open |

### bearDog

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Confirm crypto JSON-RPC sigs | esotericWebb | P1 | Open |
| HSM → Android Keystore | grapheneGate | P2 | Open |

### sweetGrass

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Confirm `braid.create/query` | esotericWebb | P1 | Open |

### biomeOS

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| GAP-017: neural-api resurrection | esotericWebb | P2 | Open |
| GAP-018: executors not exposed | esotericWebb | P2 | Open |

### ALL primals (ecosystem convention)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| GAP-036: Socket naming convention | esotericWebb | P2 | Open |
| GAP-038: Stale UDS socket cleanup | esotericWebb | P2 | Open |

---

## Dimensional Scorecard (Wave 149b)

| Project | Clippy | Fmt | Debt | Unsafe | >800L | Tests | Prod unwrap | Usability |
|---------|--------|-----|------|--------|-------|-------|-------------|-----------|
| cellMembrane | 0 | 62 | 0 | 0 | 0 | 1,092 | 0 | — |
| esotericWebb | 0 | 3 | 0 | 0 | 0 | 472 | 0 | NPC bug |
| footPrint | **0** ESLint | — | 0 | — | 0 | **466** | — | **ALL CLEAR — UX + coverage complete** |
| songBird | **556** | 10 | 0 | 0 | **2** | 14,322 | **81** | — |
| sporePrint | — | — | 0 | — | 0 | 289 | — | Stale page |
| lithoSpore | **0** | 0 | 0 | 0 | 0 | **227** | 0 | **ALL CLEAR** |
| primalSpring | 456 | 54 | 0 | 0 | 0 | 1,274 | 4 | — |

**Ecosystem totals**: 18,000+ tests, 0 debt markers, 0 unsafe blocks.

---

## Path to Live — Downstream Projects

### footPrint → `primals.eco/footprint/` — **LIVE + ALL CLEAR**

All dimensional review items resolved: responsive design, accessibility, ESLint,
modals, welcome overlay, favicon, location picker, and test coverage (466 tests,
92.78% statements, 95.27% lines). Zero remaining gaps.

### esotericWebb → `primals.eco/webb/` — **V18, LIVE ON GATE, PERSISTENCE PENDING**

Demo scenario shipped but has `aldric` NPC false-positive bug. CLI/operator UX
is strong. No web frontend — terminal-only game via `preview` or JSON-RPC.

| Step | Status | Owner |
|------|--------|-------|
| 1-6. Binary, Caddy unit, songBird, composition, Forgejo | **ALL DONE** | — |
| 7. systemd enable on flockGate | **PENDING** | sporeGate ops |
| 8. Caddy route on golgiBody | **PENDING** | sporeGate ops |
| 9. E2E demo scenario | **SHIPPED** (V18) — aldric bug pending | esotericWebb |

### lithoSpore → CLI tool — **ALL 6 STEPS COMPLETE**

| Step | Status |
|------|--------|
| 1-5. Platform trait, pack/unpack, initioChem, deep debt | **ALL DONE** |
| 6. USB round-trip validation | **DONE** — 6-step deploy-test cycle (`3c56fc4`) |
| 7. ring dropped (ecoBin purity) | **DONE** — curl subprocess, ring banned in deny.toml (`1191c6e`) |
| 8. Clippy clean | **DONE** — workspace lints + 4 manual fixes (`71438b8`) |
| **Total** | **227 tests, 0 clippy, 0 fmt, 0 debt, 0 unsafe, 0 prod unwrap** |

### projectFOUNDATION → TBD (NOT STARTED)

---

## Ecosystem Test Health

| Project | Tests | Clippy | Fmt | Debt | Prod unwrap |
|---------|-------|--------|-----|------|-------------|
| cellMembrane | 1,092 | 0 | 62 | 0 | 0 |
| esotericWebb | 472 | 0 | 3 | 0 | 0 |
| footPrint | **466** | **0** ESLint | — | 0 | — |
| songBird | 14,322 | 556 | 10 | 0 | 81 |
| sporePrint | 289 | — | — | 0 | — |
| lithoSpore | **227** | **0** | 0 | 0 | 0 |
| primalSpring | 1,274 | 456 | 54 | 0 | 4 |

---

## Completed Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** |
| lithoSpore pack/unpack + initioChem | **SHIPPED** |
| **lithoSpore ring drop + USB round-trip + clippy clean** | **SHIPPED** (Wave 149b AAR) |
| **footPrint LIVE** | **LIVE** — known locations E2E shipped |
| **esotericWebb LIVE on flockGate** | **V18** — demo scenario shipped |
| **E2E Tutorial Standard adopted** | **SHIPPED** — both products compliant |
| songBird drawbridge + /jsonrpc + discovery | **SHIPPED** |
| sporePrint `live` maturity level | **SHIPPED** — 302 pages |
| Depot (59+ binaries, 4 arch) | **OPERATIONAL** |
| **Dimensional review (7 projects)** | **COMPLETE** — 0 debt, 0 unsafe, 18k+ tests |

---

## Canonical Port Map

| Port | Service | Gate | Protocol |
|------|---------|------|----------|
| 8080 | nestGate / petalTongue | sporeGate | HTTP (static + WS) |
| 8090 | footPrint | sporeGate | HTTP (API, behind drawbridge) |
| 8090 | esotericWebb | flockGate | HTTP (direct serve) |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [LIVE]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [V18, persistence pending]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR, 227 tests]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

*Wave 149b: Full 7-project dimensional review. 18,000+ tests, 0 debt markers,
0 unsafe code ecosystem-wide. Critical findings: songBird needs clippy cleanup
(556) + prod unwrap elimination (81) + file splits; footPrint needs responsive
design + accessibility pass + ESLint fix (162); esotericWebb demo has missing
aldric NPC (false-positive bug). All fmt drift is minor and auto-fixable.
sporePrint esotericWebb.md metadata stale. lithoSpore clippy RESOLVED
(0 warnings, workspace lints + 4 manual fixes). primalSpring has
clippy backlog (456) — mostly doc_markdown, batch-fixable.*
