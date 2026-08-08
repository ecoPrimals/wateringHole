# ecoPrimals Ecosystem Blurb — Wave 157a G68 Refined Audit

**Date**: Aug 7, 2026 8:47PM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **G68: 7/15 COMPLIANT, 5/15 PROD-CLEAN, 3 PARTIAL.** sourDough scanner refined (prod/test split, false positive exclusion). 38 production violations remain across 4 primals. 11/15 have zero production violations. Phase A cascade timer LIVE on sporeGate.

---

## G68 REFINED AUDIT — sourDough scanner v2 (prod/test split)

sourDough shipped scanner refinement (`531cf39`): separates production violations from test assertions, excludes contextual false positives (`tar::Header::set_mode`, etc.), three compliance levels.

| Primal | Level | Prod | Test | Notes |
|--------|-------|------|------|-------|
| sourDough | **G68** | 0 | 0 | Reference implementation |
| nestGate | **G68** | 0 | 0 | `nestgate-platform` owns L1/L2/L3 |
| petalTongue | **G68** | 0 | 0 | `platform_substrate` module |
| bingoCube | **G68** | 0 | 0 | Clean |
| loamSpine | **G68** | 0 | 0 | PlatformAccess adopted |
| barraCuda | **G68** | 0 | 0 | `platform_link()` adopted |
| **cellMembrane** | **G68** | 0 | 0 | Fully isomorphic cross-arch |
| squirrel | **G68-prod** | 0 | 1 | Prod clean, 1 test assertion |
| bearDog | **G68-prod** | 0 | 1 | Prod clean, 1 test assertion |
| songBird | **G68-prod** | 0 | 1 | Prod clean, 1 test assertion |
| rhizoCrypt | **G68-prod** | 0 | 1 | Prod clean, 1 test assertion |
| skunkBat | **G68-prod** | 0 | 1 | Prod clean, 1 test assertion |
| sweetGrass | partial | **1** | 2 | 1 `mode()` read in lifecycle.rs |
| coralReef | partial | **1** | 0 | 1 `mode()` read in newline_jsonrpc.rs |
| biomeOS | partial | **9** | 1 | 4 L1 symlinks + 3 L2 + 2 L3 in boot/rootfs |
| toadStool | partial | **27** | 0 | 15 L3 (VFIO/DRM/sandbox rustix), 1 L2 |

**Totals**: 38 production violations across 4 primals. **11/15 have zero production violations.**

---

## REMAINING PRODUCTION VIOLATIONS

### sweetGrass (1 prod) — trivial

`lifecycle.rs`: `mode()` read query → `query_access()`. One-line fix.

### coralReef (1 prod) — trivial

`newline_jsonrpc.rs`: `mode()` read query → `query_access()`. One-line fix.

### biomeOS (9 prod) — boot/rootfs module

- 4 L1: raw symlinks in `boot_logger/device_mgr.rs` + `rootfs/builder/install.rs` → `platform_link()`
- 3 L2: `mode()` in observability + 2 boot modules → `query_access()` / `PlatformAccess`
- 2 L3: raw `rustix` in `device_mgr.rs` + `init_filesystem.rs` → platform-gated backend

All in the `biomeos-boot` crate — the baremetal OS bootstrap path. biomeOS always runs on Linux, so these are non-blocking for deployment.

### toadStool (27 prod) — device backends

- 15 L3: raw `rustix` in VFIO (`cylinder/vfio/`), DRM (`display/drm/`), V4L2 (`display/v4l2/`), sandbox (`security/sandbox/linux/`) → backend traits
- 1 L2: `mode()` in `akida-driver/hybrid/selector.rs`
- These are inherently platform-specific device drivers. G68 L3 backend trait pattern applies.

---

## EVOLUTION SUMMARY — Aug 7, 2026

| Metric | Start of day | End of day |
|--------|-------------|------------|
| G68 compliant (scanner v1) | 3/15 | — |
| G68 compliant (scanner v2) | — | **7/15** |
| G68 prod-clean | — | **12/15** (incl. cellMembrane) |
| Production violations | ~205 (v1) | **38** (v2 refined) |
| Commits today | — | **69+** across 16 repos |
| barraCuda LOC removed | — | **−37,144** |

---

## WHO GETS THIS BLURB

| Team | What they action |
|------|------------------|
| **sweetGrass** | 1 prod fix (`lifecycle.rs` mode → query_access) |
| **coralReef** | 1 prod fix (`newline_jsonrpc.rs` mode → query_access) |
| **biomeOS** | 9 prod fixes in `biomeos-boot` (non-blocking for deployment) |
| **toadStool** | 27 prod fixes — L3 backend traits for VFIO/DRM/V4L2/sandbox |
| **All gate teams** | After sweetGrass + coralReef fix → depot rebuild → deploy |

---

## ORDERING

```
1. sweetGrass + coralReef: 1 fix each (trivial, ~5 min)
2. Depot rebuild on sporeGate (12/15 prod-clean)
3. Gate teams: deploy from golgi depot
4. biomeOS + toadStool: deep L3 work (non-blocking, independent)
5. Springs: tideGlass, hotSpring viz, esotericWebb, arXiv
```

---

## METRICS

| Metric | Value |
|--------|-------|
| G68 compliant (zero violations) | **7/15** |
| G68 prod-clean (zero prod) | **12/15** |
| G68 partial | **3/15** (sweetGrass 1, coralReef 1, biomeOS 9) |
| G68 heavy | **1/15** (toadStool 27 — L3 device backends) |
| Production violations | **38** (was 205 before scanner refinement) |
| Phase A cascade timer | **LIVE** on sporeGate |
| Cross-arch | **14/15 PASS** (toadStool consumer crates) |
| Glacial goals | **15 COMPLETE / 26 ACTIVE / 23 GLACIAL — 64 total** |
| Total tests | **~140K+** |
| P0/P1 | **ZERO** |

---

*Wave 157a — G68 refined audit. sourDough scanner v2 separates prod from test. 7/15 G68 compliant, 12/15 prod-clean (zero production violations). 38 prod violations remain across 4 primals: sweetGrass(1), coralReef(1), biomeOS(9), toadStool(27). Two trivial fixes unlock depot rebuild. Phase A LIVE. 69+ commits today across 16 repos. biomeOS Neural API orchestrates everything.*
