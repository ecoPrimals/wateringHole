# ecoPrimals Ecosystem Blurb — Wave 157a Depot Ready

**Date**: Aug 7, 2026 9:24PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **13/15 PROD-CLEAN. DEPOT READY.** sweetGrass + coralReef fixed. toadStool shipped L3 migrations (−2 violations). biomeOS down to 4 (3 in test file + 1 boot rustix). 13/15 primals have zero production G68 violations. Depot rebuild unblocked.

---

## G68 FINAL AUDIT — sourDough scanner v2

| Primal | Level | Prod | Notes |
|--------|-------|------|-------|
| sourDough | **G68** | 0 | Reference + validator |
| nestGate | **G68** | 0 | |
| petalTongue | **G68** | 0 | |
| bingoCube | **G68** | 0 | |
| loamSpine | **G68** | 0 | |
| barraCuda | **G68** | 0 | |
| squirrel | **G68-prod** | 0 | 1 test assertion |
| bearDog | **G68-prod** | 0 | 1 test assertion |
| songBird | **G68-prod** | 0 | 1 test assertion |
| rhizoCrypt | **G68-prod** | 0 | 1 test assertion |
| skunkBat | **G68-prod** | 0 | 1 test assertion |
| sweetGrass | **G68-prod** | 0 | 1 test — **FIXED this round** |
| coralReef | **G68-prod** | 0 | — **FIXED this round** |
| biomeOS | partial | **4** | 3 L2 in test file + 1 L3 boot rustix |
| toadStool | partial | **25** | 24 L3 device rustix + 1 L2 |

**13/15 zero production violations. Depot rebuild unblocked.**

biomeOS: 3 of 4 are in `vm_federation_manager_tests/mod.rs` (test file — scanner should flag as test-only). The 1 real violation is `rustix` in `boot_logger/device_mgr.rs` (always Linux, non-blocking).

toadStool: 24/25 are L3 `rustix` imports in VFIO/DRM/V4L2/sandbox/akida-driver — inherent Linux kernel device interfaces. These need the G68 L3 backend trait pattern and are a long-term convergence, not a depot blocker.

---

## DEPOT STATUS

| Gate | Cross-arch | Depot ready? |
|------|-----------|-------------|
| 14/15 primals | **PASS** Windows | **YES** |
| toadStool | **FAIL** Windows (consumer crate gating) | Excluded from Windows depot |
| Phase A timer | **LIVE** on sporeGate | Cascade running autonomously |

**Action**: sporeGate can rebuild depot now. 13/15 prod-clean. 14/15 cross-arch.

---

## REMAINING — CLEAR BEFORE MAC + RISC-V

These 29 violations don't block depot but **must** be cleared. Every raw `rustix`/`PermissionsExt` left is a landmine for darwinGate (apple-darwin) and riscGate (RISC-V) — two glacial goals (G12, G42) that will fail immediately on unabstracted platform code. Clearing now avoids chasing the same debt later on unfamiliar architectures.

| Team | Violations | What | Target |
|------|-----------|------|--------|
| **biomeOS** | 4 (3 L2 + 1 L3) | `vm_federation_manager_tests` set_mode + boot `rustix` | `PlatformAccess::apply()` + backend trait |
| **toadStool** | 25 (24 L3 + 1 L2) | VFIO/DRM/V4L2/sandbox/akida `rustix` imports | L3 backend traits (DeviceFile pattern from S361/S362) |
| **toadStool** | — | Windows consumer crate gating (`select_backend` import) | Gate imports behind `#[cfg(unix)]` or feature flag |
| **sourDough** | minor | `vm_federation_manager_tests` flagged as prod, should be test | Scanner refinement |
| **primalSpring** | — | Phase C sync graph materialization | Handoff delivered |

---

## WAVE 157a EVOLUTION SUMMARY

| Metric | Start | End |
|--------|-------|-----|
| G68 compliant | 0/15 | **7/15** |
| G68 prod-clean | 0/15 | **13/15** |
| Production violations | ~205 | **29** (4 biomeOS + 25 toadStool) |
| Scanner versions | v1 (no prod/test split) | v2 (3 compliance levels) |
| Commits today | 0 | **69+** across 16 repos |
| barraCuda LOC removed | 0 | **−37,144** |
| Phase A timer | spec only | **LIVE** |
| Cross-arch | 14/15 | **14/15** (toadStool consumer crates) |

---

*Wave 157a — depot ready, convergence continuing. 13/15 prod-clean, 7/15 fully G68 compliant. 29 production violations remain (biomeOS 4, toadStool 25) — not blocking depot but must be cleared before darwinGate (G12) and riscGate (G42) expansion. Every unabstracted rustix/PermissionsExt is a landmine on new architectures. sporeGate rebuilds depot now. biomeOS + toadStool continue converging.*
