# Wave 111 — Gate Expansion + Federation Completion + Sandbox Graduation

**Date**: 2026-06-12 (ACTIVE — pre-wave sync complete, ready for distribution)
**From**: eastGate overwatch (cellMembrane)
**FRAGO**: `impulses/active/2026-06-11T21-30_eastGate__wave111-gate-expansion-federation-sandbox.toml`

---

## Wave 110 Exit (CLOSED)

All protocol-level convergence achieved:
- 13/13 HEALTH-01 GRADUATED
- 6/6 startup contract COMPLETE
- Depot rebuilt from HEAD (c8e0c94, 2026-06-11T19:58:49Z)
- Membrane parity 12/12 (origin = forgejo = local)
- Sandbox + canary pipeline SHIPPED
- BUILD-ELF-01 + harvest --all + dual checksum all wired
- PostPrimordial FULLY VALIDATED

**Wave 110 archive**: `handoffs/archive/wave110/`, `impulses/resolved/wave109-guidestone-deployment-convergence.toml`

---

## Wave 111 Mid-Wave Evolution (2026-06-12)

**Major cellMembrane evolution shipped (e230e10, ironGate):**
- **3-Tier Diesel Engine** fully operational: Ember (sandbox) → Cylinder (main) → Glowplug (canary)
- **gate.provision CLI**: DigitalOcean API v2 client — create/poll/destroy droplets, SSH bootstrap, mesh join
- **canary-fieldmouse.toml**: Full NUCLEUS 13/13 warm standby profile in plasmidBin
- **Deep debt**: cascade.rs 877L→390L (extracted post_sync.rs), all hardcoded primal names → capability-based discovery
- **Bash fallback removed**: gate/mod.rs pull()/check() now pure temporal.cascade/temporal.check
- **membrane.toml**: Updated from "Wave 63: Three-node diderm" → "Wave 111: 3-tier diesel engine"
- **Cargo clean**: 1.2GiB artifacts reclaimed, full rebuild 7.88s, zero warnings, 377 tests green
- **VPS Surface Minimization Plan**: Path from $24/mo to $6/mo relay-only (Phase 1 immediately actionable)

**songBird evolution (9903cf50, Wave 113):**
- **MESH-PARTITION-TOLERANCE**: Cross-gate reachability gossip, partition detection, graceful degradation
- **PEER-VERSION-MISMATCH**: Version negotiation, backward-compatible wire protocol, version_skew reporting
- 8918 total tests passing, zero clippy warnings

**Stream 6 Divergence Pressure: 13/16 SHIPPED** (was 10/16 at last blurb update)

---

## Wave 111 Theme

**Scale proven infrastructure to new topology. Complete federation. Push divergence hard to force robustness.**

Every primal speaks the same language. Every binary traces to provenance. Now we expand the mesh — and intentionally stress it. WAN deployment and eventual ionic/weak bonding interactions depend on reliability that only emerges from confronting real failure modes. Wave 111 applies divergence pressure so cellMembrane evolves the self-healing primitives that non-LAN bonds require.

---

## Remaining Work by Team

### cellMembrane (ops + infra)

| Item | Stream | Priority | Status |
|------|--------|----------|--------|
| **Dev gate cascade** (eastGate/ironGate/southGate freshness) | Gate Health | P2 | READY — depot fresh, cascade available |
| **westGate gate.bootstrap** (76TB ZFS, Nest Atomic) | Gate Expansion | P2 | READY — nest profile defined |
| **NUCs + Pixle spin-up** | Gate Expansion | P2 | PENDING — quick Linux nodes |
| **blueGate + swiftGate** (Windows targets) | Cross-Platform | P3 | PENDING — WSL2 or native validation |
| ~~gate.bootstrap sandbox integration~~ | Sandbox Grad | P3 | **DONE** (acab3f6) — Tower sandbox in phase 2 |
| ~~CASCADE-STALE-RECOVERY~~ | Divergence | P2 | **DONE** (acab3f6) — auto-stash + ff-only |
| ~~PARTIAL-FETCH-RESUME~~ | Divergence | P2 | **DONE** (acab3f6) — atomic temp+rename |
| ~~CANARY-STALENESS-AUDIT~~ | Divergence | P2 | **DONE** (e80993f) — refuse stale >168h, --refresh auto-prune |
| ~~CROSS-GATE-SKEW-REPORT~~ | Divergence | P2 | **DONE** (e80993f) — health.audit --mesh, provenance mismatch report |
| ~~WAN-TIMEOUT-GRACEFUL~~ | Divergence | P2 | **DONE** (e80993f) — SCP exponential backoff 2s/4s/8s, rollback on fail |
| **gate.provision** (DO API) | Provisioning | P2 | **DONE** (e230e10) — create/poll/destroy droplets, SSH bootstrap |
| **canary-fieldmouse profile** | Canary | P2 | **DONE** (cb62907) — NUCLEUS 13/13 warm standby |
| **VPS surface minimization** | Sovereignty | P2 | PLANNED — Phase 1 (NUC canary) immediately actionable |
| tolerances in deployment.toml | Deferred | P3 | PENDING — 4 named tolerances |
| northGate (gaming gate, family validation LAST) | Gate Expansion | LOW | LAST — spare compute only |
| qS signal graphs | Deferred | P3 | DEFERRED — not urgent until autonomous gates |

### songBird team

| Item | Stream | Priority | Status |
|------|--------|----------|--------|
| ~~**Federation status wire fix**~~ | Federation | P2 | **DONE** (f18aeb6b) — env var fallback wired |
| ~~**Federation auto-reconnect**~~ | Divergence | P2 | **DONE** (f18aeb6b) — peer health loop + backoff |
| ~~VPS rebuild + deploy~~ | Federation | P2 | **DONE** (3fc94365) — federation fix in depot, validated on flockGate |
| ~~flockGate handshake validation~~ | Federation | P2 | **DONE** (1faea88) — 64ms RTT, enabled=true, auto-reconnect functional |
| ~~MESH-PARTITION-TOLERANCE~~ | Divergence | P2 | **DONE** (9903cf50) — cross-gate reachability gossip, partition detection |
| ~~PEER-VERSION-MISMATCH~~ | Divergence | P3 | **DONE** (9903cf50) — version negotiation, backward-compatible wire |

### primalSpring team (parallel)

| Item | Stream | Priority | Status |
|------|--------|----------|--------|
| ~~S_VERSION_SKEW + S_CASCADE_REGRESSION + S_WAN_LATENCY_TOLERANCE~~ | Divergence | P2 | **DONE** — 3 scenarios shipped |
| ~~Deep debt (thiserror, module splits, hardcoding)~~ | Evolution | P2 | **DONE** — 1005 tests, 60 scenarios |
| s_gate_expansion_readiness + nest_atomic.toml | Gate Expansion | P3 | **DONE** — northGate/westGate prep |
| nucleus_launcher aarch64 cross-compile | Evolution | P3 | PENDING |
| Proto-nucleate manifest | Evolution | P3 | PENDING |
| BTSP cross-primal full chain | Evolution | LOW | Documented gaps, non-blocking |

### ops (hardware)

| Item | Stream | Priority | Status |
|------|--------|----------|--------|
| westGate hardware setup | Gate Expansion | P2 | PENDING — i7-4771 + 76TB ZFS |
| NUCs + Pixle power-on | Gate Expansion | P2 | PENDING — quick spin-up Linux nodes |
| blueGate + swiftGate access | Cross-Platform | P3 | PENDING — Windows machines |
| northGate (gaming, family) | Gate Expansion | LOW | LAST — spare compute when not in use |
| 10G backbone cables | Carry | LOW | Blocks high-throughput only |

---

## Remaining Work by Gate

### Priority 1: flockGate (WAN — Federation VALIDATED)

**64ms RTT confirmed.** Federation handshake validated 2026-06-12T14:07Z. Wire fix + auto-reconnect working. Remaining: VPS songBird rebuild to `fe47c012` for persistent relay + partition tolerance.

### Priority 2: Dev Gates (eastGate / ironGate / southGate — Cascade Freshness)

**Status**: All 13/13, meshed, healthy. Depot rebuilt — cascade available for freshness.
**Action**: `membrane temporal.cascade --with-restart` to pull fresh binaries from VPS.

### Priority 3: westGate (NEW — Nest Atomic 7/7)

**Hardware**: i7-4771, RTX 2070 Super, 76TB ZFS
**Profile**: `nest` (7 primals)
**Owner**: cellMembrane + ops

| Phase | Work | Depends on |
|-------|------|-----------|
| 1. Enrollment | `gate.bootstrap` nest profile | Hardware ready |
| 2. Binary fetch | 7/7: nestgate, songbird, biomeos, sweetgrass, loamspine, beardog, squirrel | Depot fresh ✅ |
| 3. Health sweep | 7/7 health probes pass | Binaries installed |
| 4. ZFS mount | ZFS pool + nestGate storage assignment | Hardware |
| 5. Mesh join | songBird :7700 enrollment | songBird alive |

### Priority 4: NUCs + Pixle (Small Linux Nodes)

**Hardware**: Intel NUCs + Pixle (small form factor)
**Profile**: TBD (subset or full)
**Owner**: cellMembrane + ops
**Status**: Can spin up before northGate. Quick enrollments using standard gate.bootstrap.

### Priority 5: blueGate + swiftGate (Windows Cross-Platform)

**Hardware**: Windows machines (accessible for deployment)
**Profile**: Cross-platform validation
**Owner**: cellMembrane + ops
**Status**: Testing ecoBin on Windows family gates. May use WSL2 or native port. Validates that the ecosystem tooling reaches non-Linux endpoints.

### Priority 6 (LAST): northGate (Gaming/Hobby — Family Validation)

**Hardware**: Ryzen 9950X3D, RTX 5090 (32GB), 96GB DDR5 — **Windows gaming gate**
**Profile**: `full` (13/13 primals)
**Purpose**: Exclusively a family gate validation case — spare compute only when not in use
**Owner**: cellMembrane + ops
**Status**: LAST priority. Not a dev or production node. Validates ecoBin on family hardware with spare compute utilization. Deploy after all other gates are stable.

### flockGate (WAN — Federation VALIDATED)

**Hardware**: ARM64 (existing, deployed)
**Status**: VALIDATED (1faea88). 64ms RTT, enabled=true, wire fix confirmed, auto-reconnect functional.
**Remaining**: Persistent relay (VPS songBird rebuild to `fe47c012` for partition tolerance).

| Action | Owner | Status |
|--------|-------|--------|
| ~~Wire fix (code)~~ | songBird team | **DONE** (f18aeb6b) — env var wired |
| ~~Partition tolerance~~ | songBird team | **DONE** (9903cf50) — gossip + version negotiation |
| ~~Depot rebuild~~ | ops | **DONE** (3fc94365) — federation fix in depot |
| ~~Federation validation~~ | ops | **DONE** — 64ms RTT, enabled=true, mesh.init succeeds |
| VPS rebuild to `fe47c012` (partition tolerance in depot) | ops | PENDING — persistent relay |

### grapheneGate (ARM — Existing, Maintenance)

**Status**: 13/13 deployed + alive. Binaries stale (Feb 2026 build). Depot now fresh — next cascade will update.

| Action | Owner | Status |
|--------|-------|--------|
| temporal.cascade --with-restart | ops | READY — fresh depot, tooling wired |

### eastGate / golgiBody / ironGate / southGate (LAN — Stable)

**Status**: All 13/13, meshed, healthy. No active work items. Gate cascade available for freshness.

---

## Remaining Work by Level

### Protocol Level — COMPLETE ✅

No remaining protocol work. All guideStone properties satisfied:
- P1 (Deterministic): gate.bootstrap pipeline proven
- P2 (Reference-Traceable): provenance.toml tracks all binaries
- P3 (Self-Verifying): BLAKE3 dual-verify, sandbox isolation proof
- P4 (Environment-Agnostic): musl-static, no runtime deps
- P5 (Tolerance-Documented): 6 named tolerances in primalSpring; 4 more pending codification

### Deployment Level — 1 item

1. ~~**Sandbox integration** into gate.bootstrap~~ — **DONE** (acab3f6 + e230e10)
2. **Tolerances** codified in deployment.toml (P3, cellMembrane) — PENDING

### Infrastructure Level — 6 items (priority order)

1. **flockGate WAN federation** (P2, songBird + ops) — highest priority
2. **Dev gate cascade** (P2, ops) — fresh binaries on working gates
3. **westGate bootstrap** (P2, cellMembrane + ops) — 76TB ZFS cold storage
4. **NUCs + Pixle spin-up** (P2, ops) — quick Linux nodes
5. **blueGate + swiftGate** (P3, ops) — Windows cross-platform validation
6. **northGate** (LOW, ops) — family gate, spare compute, LAST

### Deferred (autonomous gate prerequisites)

- qS signal graphs, rP impulse lifecycle, freshness mesh.publish (all P3, cellMembrane)

---

## Stream 6: Divergence Pressure — Force Robustness (NEW)

**Strategic intent**: Intentionally create divergence, staleness, and regression scenarios that force cellMembrane to evolve robust error recovery. LAN gates are forgiving (sub-ms, always-on). WAN gates, ionic bonds (Windows/family), and weak bonds (portable/cellular) expose every gap. Apply pressure NOW so we know what breaks BEFORE ionic/weak bonding is live.

> Every task below is designed to **break something** in a controlled way. The fix becomes a cellMembrane robustness primitive that ionic/weak bonding depends on.

### cellMembrane — Forced Robustness Evolution

| Task | Scenario | Status |
|------|----------|--------|
| ~~**CASCADE-STALE-RECOVERY**~~ | `temporal.cascade` on a gate 5+ commits behind, dirty worktree | **DONE** (acab3f6) — auto-stash, ff-only, pop |
| ~~**PARTIAL-FETCH-RESUME**~~ | Interrupt `plasmid.fetch` mid-download | **DONE** (acab3f6) — atomic write (temp+rename), .tmp cleanup, retry |
| ~~**CANARY-STALENESS-AUDIT**~~ | Canary pool holds binaries from 3 waves ago, trigger failover | **DONE** (e80993f) — refuse >168h stale, plasmid.canary.audit --refresh |
| ~~**CROSS-GATE-SKEW-REPORT**~~ | Newer songBird on VPS, older on eastGate — `membrane health.audit --mesh` | **DONE** (e80993f) — depot staleness + provenance mismatch report |
| ~~**WAN-TIMEOUT-GRACEFUL**~~ | Simulate flockGate WAN disconnect during `plasmid.refresh` | **DONE** (e80993f) — exponential backoff (2s/4s/8s), partial rollback |
| **SANDBOX-DEPENDENCY-CHAIN** | Sandbox primal requiring bearDog — bearDog not started in sandbox | PENDING |

Also shipped (cellMembrane `c8c2631`): pure Rust ELF validation (no external `file` command), constant extraction (magic numbers → named constants), zero production unwrap/expect/todo/allow/unsafe.

### songBird — Federation Robustness

| Task | Scenario | Status |
|------|----------|--------|
| ~~**FEDERATION-STATUS-WIRE**~~ | Wire env vars into `federation.status` response | **DONE** (f18aeb6b) — reads SONGBIRD_FEDERATION_ENABLED, PEERS, PORT |
| ~~**FEDERATION-RECONNECT**~~ | Kill VPS songBird, restart after 60s — auto-reconnect? | **DONE** (f18aeb6b) — spawn_peer_health_loop, 30s→300s backoff |
| ~~**MESH-PARTITION-TOLERANCE**~~ | VPS reachable from eastGate but not from flockGate | **DONE** (9903cf50) — reachability gossip, partition detection, graceful degradation |
| ~~**PEER-VERSION-MISMATCH**~~ | songBird v0.2.0 on one gate, v0.2.1 on another | **DONE** (9903cf50) — version negotiation, backward-compatible wire |

Also shipped (songBird `32a8d700`, Wave 112): dep hoisting, real health probes replacing stubs, env-only → TCP probes, security provider naming agnostic.

### primalSpring — Validation Scenarios for Divergence

| Task | Scenario | Status |
|------|----------|--------|
| ~~**S_VERSION_SKEW**~~ | Detect version skew across health responses from mesh | **DONE** — `s_version_skew_detection` + wetSpring `composition.mesh_health` |
| ~~**S_CASCADE_REGRESSION**~~ | Validate post-cascade state matches depot provenance | **DONE** — `s_cascade_provenance_match` scenario |
| ~~**S_WAN_LATENCY_TOLERANCE**~~ | Validate IPC works within tolerance over high-latency link | **DONE** — `s_wan_ipc_tolerance` with configurable threshold |

### biomeOS — Orchestration Under Divergence

| Task | Scenario | Status |
|------|----------|--------|
| ~~**DISCOVERY-STALE-PRUNE**~~ | Primal dies — biomeOS prunes registration | **DONE** (249bce28, v4.24) — unregister + prune_stale + capability.prune RPC + 60s sweep |
| ~~**ROUTING-PARTITION-AWARE**~~ | Primal on unreachable segment — routing degrades? | **DONE** (249bce28, v4.24) — all_circuits_open detection, mesh fallback before hard error |

Also shipped (biomeOS `8c310e1b`, v4.25): security fail-closed, real metrics, agnostic naming, router refactor. Neural router registry extracted (`neural_router/registry.rs`).

### ops — Intentional Divergence Creation

| Task | Scenario | Forces |
|------|----------|--------|
| **DEPLOY-THEN-STALE** | Deploy westGate, skip cascades for 2 waves — measure skew | Proves freshness audit catches real-world drift |
| **WINDOWS-ECOBIN-DIVERGENCE** | Deploy to blueGate (Windows/WSL2) — measure behavior delta | Cross-platform divergence detection |

---

## Success Criteria

**Core (Wave 111)**:
- [x] flockGate federation handshake validated — **64ms RTT, enabled=true** (1faea88). Persistent relay pending VPS rebuild.
- [ ] Dev gates cascaded to fresh depot binaries (eastGate, ironGate, southGate)
- [ ] westGate Nest Atomic 7/7 bootstrapped + ZFS active
- [x] federation.status reports `enabled: true` (wire fix shipped — f18aeb6b)
- [x] gate.bootstrap sandbox-validates before promotion (acab3f6 + e230e10)
- [x] At least 4 divergence scenarios (Stream 6) executed — **13/16 shipped**
- [x] cellMembrane: CASCADE-STALE-RECOVERY + PARTIAL-FETCH-RESUME — **DONE** (acab3f6)

**Extended**:
- [ ] NUCs + Pixle enrolled and meshed
- [ ] blueGate/swiftGate Windows cross-platform validation
- [ ] tolerances codified in deployment.toml
- [ ] nucleus_launcher aarch64 cross-compiled
- [x] primalSpring: `s_version_skew_detection` scenario shipping — **DONE**
- [x] biomeOS: stale registration pruning demonstrated — **DONE** (249bce28, v4.24)

**Last** (family validation):
- [ ] northGate NUCLEUS 13/13 — spare compute when not in use

---

## Active Documents

| Document | Purpose |
|----------|---------|
| This blurb | Wave 111 per-team/level/gate guidance |
| `impulses/active/...wave111-gate-expansion-federation-sandbox.toml` | Wave 111 FRAGO (13/16 Stream 6 shipped) |
| `handoffs/PREWAVE_SYNC_WAVE111_JUN12_2026.md` | Pre-wave sync state (freshness regenerated) |
| `handoffs/AAR_DIVERGENCE_PRESSURE_WAVE111_STREAM6_JUN12_2026.md` | Stream 6 results + 8 proven patterns |
| `handoffs/AAR_PIPELINE_ADHOC_PATTERNS_WAVE111_JUN12_2026.md` | Pipeline automation roadmap (P1/P2/P3 items) |
| `handoffs/CONVERGENCE_GATE_WAVE111_PATTERN_DEPRECATION_JUN12_2026.md` | When old patterns can be permanently deprecated |
| `handoffs/VPS_SURFACE_MINIMIZATION_EVOLUTION_JUN12_2026.md` | VPS sovereignty roadmap ($24→$6/mo) |
| `plasmidBin/profiles/canary-fieldmouse.toml` | Canary gate profile (Phase 1 ready) |
| `impulses/active/...wave107-healthspring-upstream-gaps.toml` | healthSpring upstream backlog (LOW) |
| `GLACIAL_SHIFT_READINESS.md` | Stadial entry tracking |

---

## Key Insight for Teams

**Federation is VALIDATED.** 64ms RTT confirmed on flockGate (2026-06-12T14:07Z). Wire fix, auto-reconnect, partition tolerance, and version negotiation all shipped. Persistent relay pending one more VPS rebuild to `fe47c012`.

**Depot rebuild worked.** songBird `3fc94365` was built, deployed, and validated on flockGate via WAN. The pipeline is proven end-to-end: code push → harvest on VPS → fetch on remote gate → health probe confirms.

**VPS surface minimization is planned and actionable.** Phase 1 (NUC replaces fieldMouse droplet → $12/mo savings) can execute immediately using `gate.bootstrap` with the new `canary-fieldmouse` profile. `gate.provision.destroy` decommissions the DO canary when ready.

**cellMembrane is now bash-free.** The dead `cascade-pull.sh` fallback is removed. All gate operations are pure Rust — temporal.cascade/temporal.check invocations only. The locally installed membrane binary on ironGate is older (pre-temporal.cascade); rebuild with `cargo install --path crates/membrane-shadow` to get the full diesel engine.

---

**Wave 111 scales guideStone convergence to new topology and stress-tests it. The protocol is proven, the membrane is bash-free and capability-driven, divergence pressure yielded 13/16 robustness primitives, and the VPS sovereignty path is documented. The single remaining blocker is operational: rebuild the depot and deploy fresh songBird to complete WAN federation. After that, gate expansion (westGate, NUCs, Pixle) proceeds from proven infrastructure.**
