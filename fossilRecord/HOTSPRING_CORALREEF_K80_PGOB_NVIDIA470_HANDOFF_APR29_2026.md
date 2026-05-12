# HOTSPRING × CORALREEF: K80 PGOB nvidia-470 Binary Analysis + GPU Solve Checkpoint

**Date**: 2026-04-29
**Spring**: hotSpring v0.6.32+
**Primals**: coralReef (coral-driver), toadStool, barraCuda
**Hardware**: RTX 5060 (Blackwell), Titan V (Volta), Tesla K80 (Kepler/GK210B)

---

## 1. Summary

Static binary analysis of nvidia-470.256.02's proprietary kernel module
(`nv-kernel.o_binary`) revealed a **PSW-only PGOB ungate sequence** that differs
fundamentally from Nouveau's `gk110_pmu_pgob()`. The nvidia-470 driver communicates
power-gate state solely through register `0x10a78c` (bits 0-1), completely skipping
the `0x0205xx` power domain register sequence that Nouveau uses. This finding has
been implemented in `coral-driver/pgob.rs` and tested on live hardware.

Live testing narrowed the K80 root cause to **PRI ring GPC enrollment** — the PRI
ring shows zero GPC stations even after both PGOB approaches succeed at the
register level.

---

## 2. nvidia-470 Binary Analysis Findings

### Source
- File: `NVIDIA-Linux-x86_64-470.256.02.run` → extracted `kernel/nvidia/nv-kernel.o_binary`
- Analysis: `objdump -d` searching for `0x10a78c` (PGOB PSW register)
- Documented: `agentReagents/tools/k80-sovereign/nvidia470_pgob_analysis.md`

### PGOB Register: 0x10a78c (PMU PGOB PSW Control)

| Bit | Name    | Description                                   |
|-----|---------|-----------------------------------------------|
| 0   | TRIGGER | Set to execute PSW command, then clear         |
| 1   | STATE   | 1 = request power-gated, 0 = request ungated  |

### Disassembled Functions

**`_nv029216rm` (PGOB Disable / Ungate GPCs)** — address `0x634010`:
```
1. val = read(0x10a78c)
2. write(0x10a78c, val & ~0x02)    # Clear bit 1 → request ungated
3. val = read(0x10a78c)
4. write(0x10a78c, val | 0x01)     # Set bit 0 → trigger PSW
5. val = read(0x10a78c)
6. write(0x10a78c, val & ~0x01)    # Clear bit 0 → release trigger
```

**`_nv029114rm` (PGOB Enable / Gate GPCs)** — address `0x633f30`:
```
1. val = read(0x10a78c)
2. write(0x10a78c, val | 0x02)     # Set bit 1 → request power-gated
3. val = read(0x10a78c)
4. write(0x10a78c, val | 0x01)     # Set bit 0 → trigger PSW
5. val = read(0x10a78c)
6. write(0x10a78c, val & ~0x01)    # Clear bit 0 → release trigger
```

### Difference from Nouveau

| Aspect             | Nouveau `gk110_pmu_pgob()`  | nvidia-470 `_nv029216rm`    |
|--------------------|-----------------------------|-----------------------------|
| PMC bit 12         | Toggled (disable/enable GR) | Not touched                 |
| PMC bit 27         | 0→1 transition required     | Not touched                 |
| 0x10a78c           | Set bit 1, pulse bit 0      | Clear bit 1, pulse bit 0   |
| 0x0206b4           | NOP mask sync               | Not touched                 |
| 0x0205xx steps     | 16-step power domain seq    | **Not used at all**         |
| PMC restore        | Clear bit 27, set bit 12    | Not touched                 |

---

## 3. Live Test Results (K80 die0, 0000:4c:00.0)

### nvidia470_pgob_disable (PSW-only)
```
psw_pre  = 0x00000000
pmu_cpuctl = 0x00000020  (HALTED — no firmware running)
psw_post = 0x00000000    (unchanged — PMU didn't process)
gpc0     = 0xbadf1100    (PRI fault: station not found)
```
**Result**: No effect. PMU halted means no firmware to process PSW commands.

### gk110_pgob_disable (Nouveau sequence)
```
0x0205xx steps: all 16 succeed (ok=true, bit 31 clears)
gpc0     = 0xbadf1100    (still PRI fault)
fuse_gpc = 0xbadf1002    (PRI fault)
top_num_gpcs = 0x00000005 (correct — 5 GPCs per K80 die)
```
**Result**: Power domain registers respond but PRI ring can't route to GPCs.

### Root Cause
```
pri_gpc_cnt = 0x00000000  → Zero GPC stations in PRI ring topology
```
The PRI ring was initialized but has no GPC entries. The GPCs aren't just
power-gated — they're **absent from the PRI routing table**.

---

## 4. Implementation in coral-driver

### New Functions (pgob.rs)

- `nvidia470_pgob_disable()` — PSW-only ungate, 3 read-modify-write steps
- `nvidia470_pgob_enable()` — PSW-only gate (inverse)
- Both log pre/post PSW state, PMU status, GPC0/GR_HUB diagnostics

### Integration (kepler_warm.rs)

- POST-done path: `nvidia470_pgob_disable` → check → fallback `gk110_pgob_disable`
- Cold-recovery path: same try-nvidia470-first, fallback-to-nouveau pattern

### Files Changed (coralReef)
- `crates/coral-driver/src/nv/vfio_compute/pgob.rs` — +80 lines (2 new functions)
- `crates/coral-driver/src/nv/vfio_compute/kepler_warm.rs` — modified 2 PGOB call sites

---

## 5. agentReagents / benchScale Artifacts

### Build Recipe
- `tools/k80-sovereign/build_nvidia470_kernel617.sh` — Compiles proprietary nvidia-470
  for kernel 6.17 in `/tmp` with Pop!_OS compat patches. Zero host contamination.
  Patches: `del_timer_sync`, `follow_pfn`, `__vma_start_write`, `drm_fb_create`.

### Binary Analysis Doc
- `tools/k80-sovereign/nvidia470_pgob_analysis.md` — Full disassembly findings,
  register bit definitions, comparison table vs Nouveau.

### VM Reagent Templates
- `templates/reagent-nvidia470-k80.yaml` — benchScale VM template for K80 mmiotrace
- Direct QEMU approach validated: host kernel + QCOW2 overlay + custom init.sh

---

## 6. Paths Forward (for coralReef team)

### Path A: PRI Ring GPC Enrollment
The PRI ring init (`pri.rs`) currently initializes the ring master but may not
enumerate GPC stations correctly on GK210B. The nvidia-470 driver likely programs
the PRI ring topology during its full init sequence (before PGOB). Investigate:
- Register `0x120070` (PRI_RING_GPC_NSTATIONS) — should be 5 for K80
- GPC PRI ring entries at `0x128000+` (per-GPC PRI config)
- Whether `nouveau_pri_ring_init` vs `vbios_pri_ring_init` properly discovers GPCs

### Path B: PMU Firmware for PSW Processing
The nvidia-470 PSW handshake requires a running PMU falcon with PGOB-aware firmware.
Options:
1. **Nouveau GK110 PMU firmware** — already extracted to `firmware/gk110/`. May not
   handle GK210B PGOB (same issue as `gk110_pmu_pgob` vs GK210B)
2. **nvidia-470 PMU firmware** — extract from binary blob. The `_nv029216rm` function
   expects the PMU to interpret PSW register writes as power management commands.
3. **Custom minimal PMU stub** — just enough to process PSW commands

### Path C: Combined (Most Likely)
1. Proper PRI ring init with GPC enumeration
2. PMU firmware boot (Nouveau or extracted)
3. PGOB PSW handshake (nvidia470_pgob_disable)
4. PRI ring re-init after PGOB (new stations online)

---

## 7. GPU Solve Status Matrix

| GPU          | Arch     | Sovereign Dispatch | Status                          |
|--------------|----------|-------------------|---------------------------------|
| RTX 5060     | Blackwell SM120 | ✅ LIVE     | Full QMD v5.0 + UVM + SASS     |
| Titan V      | Volta SM70      | ⏸️ Paused   | SEC2/ACR HS barrier; DRM path available |
| Tesla K80 d0 | Kepler GK210B   | ⚠️ Active   | PGOB analysis done; PRI ring enrollment needed |
| Tesla K80 d1 | Kepler GK210B   | ⏸️ Blocked  | Same root cause as d0           |

---

## 8. For barraCuda Team

No new absorption targets from this session. The K80 work is entirely in the
coral-driver layer (hardware init). Once K80 GPC ungating is solved and FECS boots,
the existing barraCuda shader inventory (128 WGSL shaders, all validated on SM35
via coralReef compiler) will dispatch directly.

---

## 9. For toadStool Team

The nvidia-470 binary analysis technique (static disassembly of `nv-kernel.o_binary`
with objdump + register offset search) is a powerful reverse-engineering tool that
should be documented as a standard reagent pattern. It bypasses the need for
mmiotrace/DRM interception entirely.

The `benchScale` VM approach (QEMU + VFIO passthrough + host kernel + custom init.sh)
works reliably for driver testing in isolation. Template stored in agentReagents.

---

## 10. Verification

```
# coralReef
cd primals/coralReef
cargo check --lib -p coral-driver         # zero errors
cargo test --test exp123k_k80_sovereign -p coral-driver --features vfio --no-run  # compiles

# hotSpring
cd springs/hotSpring
cargo check                               # zero errors
```
