# Sovereign Compute — Ground Truth

**Last measured:** Aug 16, 2026 | **Gate:** biomeGate hotSpring

This file is the single answer to "what actually works." Cite it rather than
restating it. Docs drifted apart because the same claim was written in fifteen
places and re-checked in none.

Update this file when a measurement changes. If a claim elsewhere disagrees
with this file, this file is right and the claim is stale.

---

## The one-line answer

**No shader has ever executed on the sovereign path on any NVIDIA GPU.**

Verified GPU compute in this ecosystem runs through **wgpu/Vulkan with a vendor
driver present**. The sovereign VFIO path is wired end to end and reaches
hardware bring-up, but has never produced a numeric result.

---

## What "sovereign" means here

Sovereign means **no external non-Rust code in the runtime path**. That
standard is stricter than "no proprietary code":

| Component | Sovereign? | Why |
|-----------|-----------|-----|
| NVIDIA proprietary driver | No | Vendor blob |
| **nouveau** | **No** | Open source, but external C. Still vendor by this standard |
| wgpu / Vulkan / RADV | No | External, and requires a vendor driver beneath |
| toadStool VFIO + Rust falcon boot | Yes | The target |

nouveau being free software does not make it sovereign. It is a **stepping
stone**: useful to seed hardware and to study, and something the trio must
eventually replace by composition.

---

## Per-GPU state

| GPU | Arch | Best achieved | Blocker |
|-----|------|---------------|---------|
| Titan V | Volta GV100 | **Tier 1 warm infrastructure**, reproducible ×3, persists on vfio-pci | FECS dead (`fecs_pc=0xBADF5040`), GPCCS HS fuse-locked. Requires a nouveau warm handoff to reach even Tier 1 |
| Tesla K80 (×2 dies) | Kepler GK210 | Identity probe, PMC read, **PGRAPH ungate** — no seeder module | **Dies wedge to all-ones after `pgraph_reset` + rollback**, unrecoverable without reboot. Every other K80 symptom is this seen from another angle |
| RTX 5060 | Blackwell GB206 | Display GPU; compute via wgpu | Not a sovereign target — holds the display path |

### Tier ladder

| Tier | Meaning | Status |
|------|---------|--------|
| 0 | Cold — power cycle required | — |
| 1 | Warm infrastructure: VFIO, BAR0, DMA, PFIFO, channels, pushbuffers | **Titan V only, via nouveau seed** |
| 2 | Warm compute: FECS dispatches, GR executes shaders | **Not achieved on any GPU** |
| 3 | Full sovereign cold boot without vendor VBIOS | Research goal |

A previous "Tier 2 ACHIEVED via catalyst" claim was **withdrawn**: those runs
read PRI-faulted registers as live state, so `compute_ready` was a false
positive. Catalyst also means nvidia RM performed the init, so even a true
result there would not have been sovereign.

---

## What IS proven

| Result | Where | Path |
|--------|-------|------|
| SU(2) lattice QCD HMC, cross-vendor agreement **0.19%** (RTX 3090 vs RX 6950 XT) | strandGate | wgpu/Vulkan + vendor drivers |
| Plaquette within 0.1% of published values (β=6.0, 6.2); ΔH 0.97 | strandGate | wgpu/Vulkan |
| Node Atomic IPC composition, 746 pipelines/sec, 0 errors under load | strandGate | IPC, not silicon |
| coralReef compiles WGSL/SPIR-V → SASS + AMD GFX | CI | ~4,000 tests |
| Titan V Tier 1 warm infrastructure | biomeGate | VFIO after nouveau seed |

Historical AMD "E2E readback `out[0]=42`" came from the **coral-driver, excised
in coralReef Sprint 9**. It does not describe the current architecture.

---

## Blockers to sovereign dispatch, in dependency order

1. **Kepler PMC_ENABLE sequencing** — dies wedge to all-ones after
   `pgraph_reset` + rollback, unrecoverable without reboot. Sole K80 blocker.
2. **FECS microcode load via PIO** — the payoff of Kepler's unsigned falcons.
3. **PFIFO runlist** — `PFIFO_RUNLIST_BASE=0`, `GP_GET` never advances, so no
   work is consumed.
4. **FECS golden context** — `PENDING_CTX_RELOAD` stalls the scheduler.
5. **End-to-end proof** — barraCuda math → coralReef compile → toadStool VFIO
   dispatch → verified observable. A plan, not a result.

### Measured register facts (Aug 16, live dies)

`DEVINIT_STATUS` at `0x2240c` **is correct on Kepler** — a claim that it was a
Volta-only offset was raised and retracted the same day. Live values:

| GPU | `0x2240c` | `needs_post` | Correct? |
|-----|-----------|--------------|----------|
| K80 die 1 | `0x00000000` | true | yes — cold, needs POST |
| K80 die 2 | `0x00000000` | true | yes |
| Titan V | `0x00000002` | false | yes — POST done |

The all-ones that prompted the false claim was a **wedged die**, not a decode
failure. Reading one dead register on a dead device and inferring an
architecture-wide offset bug is the same sentinel-as-information mistake this
codebase has now made six times. Measure against a live device.

Volta's GPCCS fuse lock sits outside this chain and may be impassable. **Kepler
is the strategic path**: unsigned falcons, and its GR microcode is open and
in-tree rather than a signed blob. Solve the bootstrap where the hardware does
not fight, then carry it to Volta.

### Firmware reality

| Generation | GR firmware blobs in `linux-firmware` | Falcon signing |
|------------|---------------------------------------|----------------|
| Kepler (`gk*`) | **0** — ucode is open, compiled into nouveau | Unsigned |
| Volta (`gv100`) | 12 | Signed, GPCCS HS fuse |
| Pascal / Turing / Ampere | 84 / 65 / 25 | Signed |

---

## Writing rules

Learned the hard way, repeatedly, in a single day:

1. **Wiring is not a result.** "E2E" describes plumbing until a number comes
   back. Say which.
2. **Name the path.** A GPU result means nothing without stating whether it ran
   on wgpu, nouveau, or sovereign VFIO.
3. **Date and scope historical claims.** Excised subsystems keep their results
   alive in docs long after the code is gone.
4. **A measurement that agrees with expectation is not evidence it was taken.**
   Four false positives in one day were all plausible-looking numbers.
5. **Bring-up is not dispatch.** Reaching a tier says what is initialised.
