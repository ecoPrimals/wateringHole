# Sovereign Compute — Ground Truth

**Last measured:** Aug 17, 2026 (midday) | **Gate:** biomeGate hotSpring

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

### Vendor tools in the *observation* path (Aug 17)

The same standard applies to how we describe hardware, not only how we drive it.
GPU detection shelled out to `nvidia-smi`, `rocm-smi`, and `lspci` until Aug 17.
That was not merely inelegant — it was **blind to the sovereign configuration**:
`nvidia-smi` reports only devices bound to the proprietary driver, so it saw one
of biomeGate's four GPUs and missed the unbound Titan V and both `vfio-pci` K80
dies.

Detection is now native sysfs/procfs and vendor-agnostic. What each source can
answer:

| Attribute | Native source | Vendor tool still needed |
|-----------|---------------|--------------------------|
| Presence, BDF, vendor/device/class | sysfs cached attributes | no |
| Bound driver + version | `driver/module/version` | no — same string `nvidia-smi` prints |
| Model name | `pci.ids`, then kernel's `Model:` line | no |
| Liveness (responding vs wedged) | live config space vendor ID | no |
| **VRAM total** | `mem_info_vram_total` | **amdgpu only**; none for NVIDIA |
| **VRAM used/free** | — | **yes** — `nvidia-smi`, the last remaining use |

Cached sysfs identity survives a device going silent, so a wedged GPU reports as
*"Tesla K80 at 0000:4b:00.0, not responding"* rather than vanishing. Do **not**
substitute the BAR1 aperture for VRAM capacity: measured here a 12 GB K80 die
presents a 16 GiB BAR and an unbound Titan V presents 256 MiB.

See `BIOMEGATE_VENDOR_TOOL_EXCISION_AAR_AUG17_2026.md`.

---

## Per-GPU state

| GPU | Arch | Best achieved | Blocker |
|-----|------|---------------|---------|
| Titan V | Volta GV100 | **Tier 1 warm infrastructure**, reproducible ×3, persists on vfio-pci | FECS dead (`fecs_pc=0xBADF5040`), GPCCS HS fuse-locked. Requires a nouveau warm handoff to reach even Tier 1 |
| Tesla K80 (×2 dies) | Kepler GK210 | Cold bring-up completes with the die alive (×4); VBIOS read off PROM and now **decodes at 0% unknown**, yielding 303 register writes | **Applying the decoded script to a die** — untested. Wedge causes fixed Aug 16; both dies `Responding` and unbound as of the Aug 17 reboot |
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

1. ~~**Kepler PMC_ENABLE sequencing**~~ — **resolved Aug 16 evening.** The
   wedge was not PMC sequencing. It was `FalconDiagnostic::probe` writing
   `0x1854` (a PBUS register) to un-shadow PROM, on a ring answering
   `0xbad0011f`. Three of five die-losses came through that one write. Cold
   bring-up now completes with the die alive, reproducible ×4. See
   `BIOMEGATE_K80_WEDGE_AAR_AUG16_2026.md`.
2. ~~**Kepler VBIOS opcode coverage**~~ — **resolved Aug 17, offline.** It was
   a misparse, as suspected, but not a script-table offset. Two payload-length
   bugs, either of which desyncs the walk permanently:
   `ram_restrict_group_count` read BIT 'M' as a pointer to the rammap table
   instead of reading the count out of the 'M' entry itself (v2 → `+0`), and
   opcode `0x8F` used a 6-byte header with the count at `+5` where the header
   is 7 bytes and `+5` is the address stride. Measured on the K80 ROM:

   | group count | `0x8F` header | unknown |
   |-------------|---------------|---------|
   | 4 (fallback) | 6-byte | **76%** — the reported failure |
   | 8 (correct) | 6-byte | 40% |
   | 8 (correct) | 7-byte | **0%** — 2 of 381 opcodes |

   The scripts now yield **303 register writes** into the framebuffer, clock,
   display, PMC and thermal trees. **This is a parse result, not a bring-up
   result** — none of those writes has been applied to a die.
3. **Apply the decoded script to a K80 die** — *current K80 blocker.* The
   interpreter will now arm writes, having previously refused. Whether those
   303 writes POST the GPU is untested and is the next hardware experiment.
4. **FECS microcode load via PIO** — the payoff of Kepler's unsigned falcons.
5. **PFIFO runlist** — `PFIFO_RUNLIST_BASE=0`, `GP_GET` never advances, so no
   work is consumed.
6. **FECS golden context** — `PENDING_CTX_RELOAD` stalls the scheduler.
7. **End-to-end proof** — barraCuda math → coralReef compile → toadStool VFIO
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

### VBIOS source reality (Aug 16, measured)

The K80 has exactly one VBIOS source, and it is not the obvious one.

| Source | K80 | Note |
|--------|-----|------|
| PCI expansion ROM BAR | **absent** | config offset `0x30` reads `0x00000000` |
| ACPI `_ROM` | **absent** | no sysfs entry |
| PRAMIN VBIOS shadow | unavailable cold | requires a POST that has not happened |
| PROM at `BAR0+0x300000` | **works** | `0xeb7baa55` — `0xAA55` signature present |

Critically, **PROM decodes without un-shadowing it first**. Clearing bit 0 of
`0x1854` is an optimization, not a precondition — measured `0xeb7baa55` at the
aperture while `0x1854` itself read `0xbad0011f`. Read PROM; do not write
`0x1854` unless the ring is healthy.

Any plan that assumes `/sys/bus/pci/devices/*/rom` is dead on arrival for Tesla
parts.

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
6. **A component must not depend on what it reports about.** Detection that
   asked the vendor driver could not see GPUs not using it, and reported that
   blindness as fact rather than as the limit of the instrument.
7. **When a device cannot answer, say so.** A filter that silently drops
   non-responders deletes the most important thing you know. `Unknown` is not
   `Ok`.
8. **Audit the write-up as a measurement.** Rules 1–7 got applied to code and
   hardware and never to the numbers in the AAR. A "216 tests recovered" figure
   that matched nothing reached four documents in an hour (Aug 17). Every number
   in a handoff needs a command that regenerates it, run before commit.
9. **Ask what a headline figure excludes.** "8,521 lib tests, 0 failures" is
   accurate and is 39% of this repo's test functions; CI's `--lib` never runs
   the other ~13,102. A true number can still mislead about coverage.
