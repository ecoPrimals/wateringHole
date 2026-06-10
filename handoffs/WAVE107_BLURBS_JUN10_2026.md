# Wave 107 Blurb — Zero P1, Zero Development Debt, Push to Stadial

**Date**: 2026-06-10
**From**: eastGate overwatch
**FRAGO**: `impulses/active/2026-06-09T23-15_eastGate__wave106-cross-topology-validation.toml`

**State**: ZERO P1. S1-S4 ALL GRADUATED. 4-gate mesh collective LIVE. Upstream primal evolution sprint complete (songBird M1 + barraCuda method.describe + socket cleanup 4/5 + biomeOS auto-register). **10 P2 / 20 LOW remain across all ecosystem levels** (see cross-level summary below). Priority cascade: fix primals (mountain) → primalSpring absorbs → gates rebuild → gardens automate.

---

## Cross-Level Remaining Work Summary

| Level | P2 | LOW | Key Next Action |
|-------|-----|-----|-----------------|
| **Primals** (mountain) | 3 | 1 | Fix CR-TARPC-01 + BM-UDS-01 + toadStool /tmp |
| **primalSpring** | 1 | 2 | Absorb primal fixes → grapheneGate 13/13 scenario |
| **Springs** | 1 | 15 | healthSpring signal dispatch live test on ironGate |
| **Gates** | 2 | 0 | flockGate power-on, grapheneGate aarch64 rebuild |
| **Gardens** | 3 | 2 | CM depot sync, NDK pipeline, BearDog ACME cutover |
| **TOTAL** | **10** | **20** | **Fix mountain first, everything else follows** |

Full breakdown: `WAVE107_REMAINING_SCOPE_BY_LEVEL_JUN10_2026.md`

---

## All Remaining Items (by priority)

### P2 — Primal Code (blocks grapheneGate 13/13)

| ID | Owner | Action |
|----|-------|--------|
| `CR-TARPC-01` | coralReef | Skip tarpc `bind()` when `PRIMAL_BIND_MODE=tcp_only`. JSON-RPC TCP :9730 works. |
| `BM-UDS-01` | biomeOS | Skip Neural API UDS `bind()` when `PRIMAL_BIND_MODE=tcp_only`. v4.18 fallback not wired into actual bind path. |
| `TOADSTOOL-SOCKET-CLEANUP` | toadStool | Migrate compute-tarpc.sock + toadstool-jsonrpc-port to 3-tier resolution. Blocks `ProtectSystem=strict`. |

### P2 — Gate Ops (blocks full validation)

| ID | Owner | Action |
|----|-------|--------|
| `FLOCKGATE-WAN-E2E` | flockGate ops | Power on → re-fetch from VPS → mesh.init to 157.230.3.183:7700 → verify 5/5. |
| `GRAPHENEGATE-REBUILD` | primalSpring + cellMembrane | aarch64 rebuild on peptidoglycan → push checksums.toml → `deploy_pixel.sh` → 13/13 alive. **Requires CR-TARPC-01 + BM-UDS-01 fixes first.** |

### P2 — Spring / Garden Evolution

| ID | Owner | Action |
|----|-------|--------|
| `GAP-47-SIGNAL-DISPATCH-LIVE` | healthSpring + biomeOS | Live test nest.store/nest.commit on ironGate biomeOS with signal graphs loaded. |
| `CM-VPS-DEPOT-SYNC` | cellMembrane | Automate golgiBody inner→outer membrane binary flow. |
| `NDK-CROSS-COMPILE` | cellMembrane | `aarch64-linux-android` target on peptidoglycan for native grapheneGate. |
| `BEARDOG-ACME-CUTOVER` | cellMembrane + bearDog | TlsProvider wired, awaiting BearDog ACME client to replace Caddy LE. |
| `GRAPHENEGATE-SCENARIO` | primalSpring | After primal fixes, run `--composition full` on Pixel 8, validate 13/13 in scenarios. |

### LOW

| ID | Owner | Action |
|----|-------|--------|
| `SKUNKBAT-TCP-9750` | skunkBat | Sole zero-port standard violation. |
| `SOURDOUGH-SEGFAULT` | sourDough | `validate depot` segfault. Manual `b3sum` fallback. |
| `NG-DOWNCAST-01` | nestGate | `is_platform_constraint()` downcast fails. Workaround: `NESTGATE_SOCKET=""`. |
| `PB-FORWARD-01` | cellMembrane | deploy_pixel.sh ADB port conflict — silent failure. |
| `INFERENCE-NAMESPACE` | ecosystem | Canonical namespace: `model.*` vs `inference.*` vs `ai.*`. |
| + 15 healthSpring upstream gaps | various | See healthSpring FRAGO. 2 MEDIUM, 13 LOW. All with stable workarounds. |

**Deployment standard**: `cellMembrane/AAR_CELLMEMBRANE_WAVE106_DETERMINISTIC_DEPLOYMENT_JUN10_2026.md` — 6 invariants, gate.bootstrap spec.

---

## Upstream Primal Evolution (shipped this wave)

| ID | Owner | What |
|----|-------|------|
| `SONGBIRD-IPC-RESOLVE-M1` | songBird | Topology-aware mesh routing — `ipc.resolve` returns MeshRelay TransportEndpoint (ff86204c) |
| `BARRACUDA-METHOD-DESCRIBE` | barraCuda | Runtime method introspection — 97 methods, v0.4.0 |
| `PRIMAL-SOCKET-CLEANUP` | sweetGrass, barraCuda, coralReef, squirrel | 4/5 primals zero `/tmp` artifacts (toadStool pending) |
| `BIOMEOS-AUTO-REGISTER` | biomeOS | NUCLEUS auto-registers launched primals with songBird (v4.19, 421433dc) |

---

## FRAGO Resolved This Wave (infra + gates)

| ID | Owner | What |
|----|-------|------|
| `NUCLEUS-SUPERVISION` | biomeOS | LifecycleManager auto-restarts (v4.17) |
| `MESH-PERSISTENCE` | songBird | peers.toml + auto-reconnect (1df7ef90) |
| `CASCADE-AUTO-FETCH` | cellMembrane | Post-cascade binary update (b6c9fa0) |
| `EASTGATE-FEDERATION-PORT` | songBird | Auto-promotes to 0.0.0.0 (1df7ef90) |
| `IRONGATE-MESH` | ironGate + cellMembrane | 3rd mesh node via VPS relay |
| `GATE-BOOTSTRAP` | cellMembrane | One-command gate enrollment (b6c9fa0) |
| `PLASMID-FETCH-FIX` | cellMembrane | VPS path normalization (b6c9fa0) |
| `WAVE107-DEPLOYMENT-HARDENING` | cellMembrane | gate.status, --dry-run, WAN checksums, atomic publish |
| `GRAPHENEGATE-UDS` → adopted | primalSpring | 13/13 TCP fallback (coralReef, nestGate, petalTongue) |

---

## Handoffs (active)

| Document | Team | Purpose |
|----------|------|---------|
| `cellMembrane/AAR_CELLMEMBRANE_WAVE106_DETERMINISTIC_DEPLOYMENT_JUN10_2026.md` | cellMembrane | Living standard — 6 deployment invariants, gate.bootstrap spec |
| `WAVE107_REMAINING_SCOPE_BY_LEVEL_JUN10_2026.md` | all | **Per-level remaining scope** — primals→springs→gates→gardens, abstractions, validation gates |

**Companion FRAGO**: `impulses/active/2026-06-10T14-20_ironGate__wave107-healthspring-upstream-gaps.toml` — 15 upstream gaps (2 MEDIUM, 13 LOW), zero healthSpring local debt.

**Archived** (to `archive/wave107/`): grapheneGate AAR (11/13), esotericWebb V14, neuralSpring V182, cellMembrane Wave 107 deployment hardening, southGate Wave 107 mesh AAR, plus 4 archived FRAGOs (wave104 cross-deployment, wave105 flockGate, wave106 flockGate AAR, wave106 strandGate ACK).

---

## Gate Status (from FRAGO validation matrix)

| Gate | FRAGO Status | Mesh | NUCLEUS |
|------|-------------|------|---------|
| eastGate | `lan_x86_64` PROVEN | 1 peer (VPS), federation :7700 | 23 RPC + 3 tarpc |
| golgiBody | `vps_nucleus` PROVEN | hub | 13/13 |
| ironGate | `lan_x86_64` PROVEN | VPS relay | 12/13 |
| strandGate | `lan_x86_64` PROVEN (ACK) | 2 peers | via bootstrap |
| southGate | `lan_x86_64` PROVEN (ACK) | 2 direct peers, 4.7ms | 13/13 + science pipeline |
| flockGate | `wan_x86_64` 4/5 | pending | 4/5 e2e |
| grapheneGate | `aarch64_musl` adopted | not initialized | 9/13 (needs rebuild) |

---

## Ecosystem Snapshot

| Metric | Value |
|--------|-------|
| P1 | **ZERO** |
| P2 remaining | **10** across all levels (3 primal code, 2 gate ops, 5 spring/garden evolution) |
| LOW remaining | **20** across all levels (5 ecosystem + 15 healthSpring upstream) |
| Sovereignty | **S1-S4 ALL GRADUATED** |
| Mesh | 4-gate collective (eastGate↔golgiBody↔ironGate+southGate) |
| Depot | 13/13 x86_64 BLAKE3 verified, 14/14 aarch64 built |
| Transport | 11/11 non-exempt complete |
| Cascade | 38/38 clean |
| Deployment | Deterministic — gate.bootstrap + gate.status + cascade auto-fetch + supervision |

---

## Abstractions Exposed by Pixel + flockGate WAN Deployments

### 1. Bind Abstraction (exposed by grapheneGate/Pixel 8)

Android SELinux denies UDS `bind()` in non-standard paths. The `PRIMAL_BIND_MODE` env + `bind_transport()` abstraction was created to handle this, but **2 primals have incomplete adoption**:

- **CR-TARPC-01**: coralReef's tarpc server unconditionally binds UDS. Must skip tarpc when `PRIMAL_BIND_MODE=tcp_only`.
- **BM-UDS-01**: biomeOS Neural API server binds UDS before checking `PRIMAL_BIND_MODE`. Must skip UDS when `tcp_only`.

**Evolution needed**: The bind abstraction works for JSON-RPC primals. tarpc (coralReef) and Neural API (biomeOS) need the same gate — check `PRIMAL_BIND_MODE` before *any* `bind()` call, not just the JSON-RPC listener.

### 2. WAN Depot + Checksum Verification (exposed by flockGate)

flockGate proved the WAN fetch path works (`plasmid.fetch --source wan`), but exposed:

- **CM-VPS-DEPOT-SYNC**: golgiBody inner→outer membrane binary flow is still manual. Needs automation so peptidoglycan builds → golgiBody-inner refreshes → golgiBody-ext WAN depot updates.
- **WAN checksum trust**: `caddy.depot.checksums` serves checksums over HTTPS, but there's no cryptographic provenance chain from peptidoglycan build to WAN consumer. The WAN client trusts TLS, not build provenance.

**Evolution needed**: Atomic inner→outer depot sync. Eventually provenance-signed checksums (BLAKE3 + Ed25519 from peptidoglycan) for WAN consumers.

### 3. Transport Topology Abstraction (exposed by multi-gate mesh)

songBird M1 (`ipc.resolve`) shipped topology-aware routing, but the abstraction still needs:

- **Quorum sensing** (gen5 roadmap): Current relay chain is nanowire (SSH point-to-point). Target is diffusion-based coordination where nodes sense and respond independently.
- **mDNS/LAN auto-discovery**: Wired in songBird discovery layer but not field-tested. Would eliminate explicit `mesh.init` seed swaps.
- **NAT traversal**: STUN/TURN shipped but not field-tested on residential NAT (flockGate uses VPS relay, not punch-through).

### 4. Socket Directory Abstraction (exposed by systemd hardening)

4/5 primals cleaned, but the pattern needs to become ecosystem-wide:

- **3-tier resolution**: `BIOMEOS_SOCKET_DIR` → `$XDG_RUNTIME_DIR/biomeos` → `/run/biomeos`
- **toadStool**: Last holdout with `/tmp` hardcoding. Blocks `ProtectSystem=strict`.
- **Future**: `SOCKET_DIR` should be injected by biomeOS at launch time, not discovered by each primal independently.

### 5. NDK/Android Cross-Compilation (exposed by grapheneGate ambitions)

aarch64-musl works but is not native Android:

- `aarch64-linux-android` target is documented but not built.
- StrongBox HSM integration (bearDog) needs Android NDK.
- grapheneGate as portable root of trust requires native Android binary distribution.

**Evolution needed**: NDK cross-compile pipeline on peptidoglycan. bearDog StrongBox is the forcing function.
