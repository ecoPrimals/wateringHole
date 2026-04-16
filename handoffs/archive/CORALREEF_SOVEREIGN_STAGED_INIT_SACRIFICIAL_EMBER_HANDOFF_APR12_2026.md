# coralReef Handoff: Staged Sovereign Init + Sacrificial Ember Architecture (April 12, 2026)

**From:** hotSpring (sovereign compute hardening sprint)
**To:** All primal teams (coralReef, toadStool, barraCuda), all spring teams
**Status:** Ember zero-MMIO hold + per-stage fork isolation deployed. Stages 0-5 hardware-proven. Falcon boot blocked by memory controller sleep.

---

## What Changed

### 1. Zero-MMIO Startup (coral-ember)

Ember no longer touches BAR0 at startup. The `post_swap_quiesce` call that mapped BAR0 and wrote registers during device acquisition has been removed from `startup.rs`, `lib.rs`, and `swap_bind.rs`. Ember acquires VFIO file descriptors only. All BAR0 mapping and I/O is deferred to explicit RPC calls.

**Why:** Reading BAR0 on a cold or partially-initialized GPU causes a PCIe bus hang that propagates past fork isolation and locks the entire system. The AMD NBIO/data fabric stalls all CPU cores when a PCIe device fails to respond.

**Impact on all teams:** Any code that opens VFIO directly and maps BAR0 can lock the system. Always route through ember RPCs.

### 2. Per-Stage Fork Isolation (coral-ember `sovereign_init` RPC)

The `ember.sovereign.init` RPC now runs each SovereignInit stage as a separate fork-isolated child process with an individual timeout:

| Stage | Timeout | Operation |
|-------|---------|-----------|
| probe | 3s | Read-only: BOOT0, PMC_ENABLE, DEVINIT status |
| hbm2 | 10s | Cold-only HBM2 training via VBIOS interpreter |
| pmc | 5s | PMC engine ungating |
| topology | 5s | GPC/TPC/SM/FBP/PBDMA enumeration (read-only) |
| pfb | 5s | Memory controller (FBPA) configuration |
| pri_ring_reset | 5s | PRI ring fault drain + GR engine reset |
| falcons | 15s | SEC2 -> ACR -> FECS/GPCCS boot solver |
| gr | 10s | GR engine register init + FECS method probe |
| pfifo | 5s | PFIFO/PBDMA discovery |

If any stage hangs, ember kills only that child and returns a structured result with `halted_at` set to the failing stage name. The system stays alive.

**Previous behavior:** Single fork child with 60s timeout. A hang at any stage killed the entire init attempt with no diagnostic granularity.

### 3. PRI Ring Reset Stage (coral-driver `sovereign_init.rs`)

New `reset_pri_ring()` method added to `SovereignInit`. After PMC engine ungating, stale PRI ring faults cause falcon registers to read `0xbad00100` (PRI error). This stage:
1. Toggles GR engine (PMC bit 12) off/on
2. Sends PRI ring master enumerate command (0x12004C = 0x4)
3. Drains all pending PRI faults (up to 10 ACK cycles)
4. Verifies falcon register accessibility (FECS 0x409100 should NOT be 0xbad00100)

### 4. Warm Detection Relaxed

After nouveau teardown, PMC_ENABLE shows minimal bits (e.g., 0x40000020 = 2 bits) because nouveau gates most engines. The old threshold (`count_ones() >= 4`) rejected this as "cold." Changed to: any non-zero PMC bit or DEVINIT status bit means "warm enough to proceed."

### 5. coralctl Display Updated

`coralctl sovereign init` now correctly parses the staged response shape: iterates the `stages` array, shows per-stage status (OK/FAIL/TIMEOUT/BLOCKED), write counts, topology detail, and halt location.

### 6. Direct-VFIO Examples Warned

`sovereign_compute_e2e.rs`, `sovereign_replay.rs`, and `warm_handoff_vfio.rs` now print safety warnings on startup that they bypass ember's fork-isolated safety layer and can lock the system.

---

## Hardware Validation Results (April 12, 2026)

Titan V (GV100) after nouveau warm cycle:

```
probe:          OK  PMC_ENABLE=0x40000020 (2 bits), warm=true
hbm2:           OK  DEVINIT done, HBM2 trained
pmc:            OK  5 writes, engines ungated
topology:       OK  1 GPC, 16 SM, 12 FBP, 4 PBDMA
pfb:            OK  Memory controller configured
pri_ring_reset: OK  PRI faults cleared, falcon regs accessible
falcons:        TIMEOUT  SEC2 trap (exci=0x041f0000)
```

System remained alive and responsive throughout. Falcon timeout sacrificed only the child process.

---

## Remaining Gap: Falcon Boot (FBP=0)

After nouveau unbinds, the GPU memory controller goes to sleep (FBP=0 in topology despite reporting FBP=12 during topology read). Falcon firmware upload requires VRAM access via PRAMIN, which fails without active memory partitions.

**Two paths forward:**
1. Capture hot state before nouveau unbinds (FBP=12 while nouveau active)
2. Wake memory controller in PFB stage via VBIOS DEVINIT interpreter

---

## What Each Team Should Know

### coralReef (primary owner)

- **`sovereign_init.rs`** now has 9 stages including `reset_pri_ring()` — absorb into production `init_all()`
- **Zero-MMIO hold** in ember startup/swap is the new standard — never map BAR0 eagerly
- **Per-stage fork isolation** pattern should be used for any new BAR0-touching RPC
- **`handlers_sovereign.rs`** in coralctl is aligned to the new staged JSON response shape
- **Next:** resolve FBP=0 gap (memory controller wake) to unblock falcon boot

### toadStool (hardware abstraction)

- **Sacrificial child pattern** is reusable for any hardware probe that might hang: fork, timeout, kill, report
- **PRI ring reset** is GPU-specific but the "drain hardware faults before probing" pattern is universal
- When toadStool absorbs glowplug/ember, the staged fork isolation architecture transfers directly
- **Capability discovery** (topology stage) follows toadStool's runtime probe pattern

### barraCuda (GPU compute)

- No changes to the compute dispatch path — barraCuda dispatches via DRM, which is separate from the VFIO init pipeline
- **Awareness:** the sovereign VFIO path (for future driverless compute) routes through ember RPCs, never direct VFIO access
- When sovereign init completes fully, `open_sovereign()` returns a device barraCuda can dispatch to

### biomeOS / Neural API

- **Sovereign compute capability** should route through `coralctl sovereign init` / ember RPCs
- **`capability.call`** for GPU init should target the ember socket, not direct VFIO
- The staged response JSON shape provides per-stage health that Neural API can use for routing decisions (e.g., avoid GPUs where topology reports FBP=0)

### All spring teams

- **Direct VFIO access from user code is now explicitly dangerous** — examples carry runtime warnings
- **Ember is the mandatory intermediary** for all GPU hardware interaction in production
- If you need GPU register access (e.g., for experiments), use `ember.mmio.read` / `ember.mmio.write` RPCs
- The "ember sacrifices rather than locks" principle applies to any spring composing GPU compute

---

## NUCLEUS Composition Pattern

Sovereign GPU compute fits the NUCLEUS Tower model:

```
NUCLEUS Tower: Sovereign Compute
├── BearDog     (firmware blob authentication — future)
├── Songbird    (fleet discovery, ember socket routing)
├── NestGate    (register snapshot storage, journal)
├── ToadStool   (hardware probe, capability discovery)
├── coralReef   (shader compilation + GPU lifecycle via ember/glowplug)
├── barraCuda   (math shaders, precision routing)
└── biomeOS     (Neural API orchestration, capability.call routing)
```

Neural API deployment: TOML graph defines the sovereign compute workflow. `capability.call("compute.dispatch.sovereign", {bdf, shader})` routes through biomeOS -> coralReef -> ember -> fork-isolated GPU init -> dispatch.

---

## Files Changed

| Repository | Key Files | Change |
|------------|-----------|--------|
| coralReef / coral-ember | `startup.rs`, `lib.rs`, `swap_bind.rs` | Zero-MMIO startup (removed `post_swap_quiesce`) |
| coralReef / coral-ember | `ipc/handlers_mmio/firmware.rs` | Per-stage fork-isolated `sovereign_init` RPC |
| coralReef / coral-driver | `nv/vfio_compute/sovereign_init.rs` | `reset_pri_ring()` stage, relaxed warm detection |
| coralReef / coral-glowplug | `bin/coralctl/handlers_sovereign.rs` | Staged response display rewrite |
| coralReef / coral-driver | `examples/sovereign_compute_e2e.rs`, `sovereign_replay.rs`, `warm_handoff_vfio.rs` | Safety warnings |

---

## References

- hotSpring `whitePaper/baseCamp/sovereign_gpu_compute.md` Phase 21 — full staged init detail
- hotSpring `experiments/164_SOVEREIGN_COMPUTE_DISPATCH_PROVEN.md` — the DRM dispatch that proves the pipeline
- hotSpring `experiments/165_SOVEREIGN_INIT_PIPELINE.md` — the 8-stage SovereignInit architecture
- infra `whitePaper/gen3/baseCamp/14_sovereign_compute_hardware.md` — Current State (April 12, 2026) section
