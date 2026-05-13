# Sovereign Compute Evolution Pass — hotSpring Hardware Findings

**Date**: May 13, 2026 (updated: post-excision alignment audit)
**From**: hotSpring (hardware validation spring)
**For**: coralReef, toadStool, hotSpring
**Context**: Ownership audit + warm dispatch validation on local compute trio (Titan V, K80, RTX 5060)

---

## Post-Excision State (May 13, 2026 update)

coralReef **Sprint 9** fully excised `coral-ember`, `coral-glowplug`, `coral-gpu`,
and `coral-driver` source. coralReef is now a **pure compiler primal** (7 crates).
hotSpring's `coral-gpu` path dependency is broken and has been commented out.
The `sovereign-dispatch` feature is now a stub until toadStool Phase C/D provides
the replacement. 590/590 hotSpring lib tests pass. barraCuda v0.4.0 provides the
IPC replacement via `sovereign_dispatch_wire.rs` → `compute.dispatch.submit`.

**This means the toadStool Phase C work is now the critical path** — there is
no coralReef fallback for hardware lifecycle anymore. The diesel engine stack
exists only in git history.

---

## What hotSpring Proved on Hardware

Titan V (GV100, SM70) warm VFIO dispatch pipeline:

| Step | Result |
|------|--------|
| VFIO warm open (`from_vfio_warm_with_sm`) | PASS |
| WGSL compile: write_constant (192 bytes, 22 GPRs) | PASS |
| WGSL compile: wilson_plaquette_f64 (6000 bytes, 38 GPRs) | PASS |
| WGSL compile: su3_gauge_force_f64 (20096 bytes, 54 GPRs) | PASS |
| Dispatch + readback (GPFIFO → compute → DMA) | FAIL — FECS compute context not initialized |

The full path works from WGSL source through coral-reef compiler to native
Volta SASS binary. The gap is between "firmware loaded" and "compute context
ready to accept GPFIFO submissions."

---

## coralReef — Evolution Directives (updated post-excision)

### E1–E2: SUPERSEDED — Diesel stack excised (Sprint 9)

coralReef Sprint 9 excised `coral-ember`, `coral-glowplug`, `coral-gpu`, and
`coral-driver` source entirely. The cylinder translation fix (E1) and warm API
(E2) from the original evolution pass were **absorbed into toadStool's
responsibility** during Sprint 8 handoff. The code exists in coralReef git
history and in hotSpring's handoff docs for toadStool to reference.

### E3: FECS cold silicon init — compute context bringup (RESOLVED upstream)

coralReef Sprint 5–7 shipped comprehensive FECS cold silicon work:
- Sprint 5: PIO falcon boot, firmware-available check, boot_gr_falcons
- Sprint 6: Structured error handling — falcon_boot returns Err on timeout/halt
- Sprint 7: **Cold-silicon stability proof** — `boot_gr_falcons_with_recovery()`
  retries up to 3x with PMC GR engine reset between attempts. `GrBootOutcome`
  enum for structured result. `pmc_gr_reset()` for dedicated PMC GR engine reset.
  `sovereign_gr_boot_with_recovery()` public API on NvVfioComputeDevice.

**Note**: This code was excised from coralReef in Sprint 9 and is now
**toadStool's responsibility** to absorb as part of Phase C. The algorithm
and patterns exist in coralReef git history for reference.

**Remaining gap**: hotSpring's dispatch readback still failed after warm open.
This may be a toadStool Phase C/D integration issue rather than a missing
algorithm — the FECS recovery code exists but needs to be wired into
toadStool's warm pipeline and dispatch path.

### E4: Excision COMPLETE (Sprint 9)

coralReef has already excised (not soft-deprecated — fully removed):
- `crates/coral-ember/` — deleted
- `crates/coral-glowplug/` — deleted
- `crates/coral-gpu/` — deleted
- `crates/coral-driver/` — source deleted, only `firmware/` directory remains

**coralReef retains** (7 workspace crates): `coral-reef` (compiler), `coral-reef-isa`,
`coral-reef-stubs`, `coral-reef-bitview`, `coralreef-core` (service layer),
`nak-ir-proc`, `primal-rpc-client`. Plus `coral-kmod` (C, out-of-workspace).

**Impact on hotSpring**: `coral-gpu` path dependency broken. Commented out in
Cargo.toml. `sovereign-dispatch` feature is now a stub. 590/590 lib tests pass.

**coralReef's only remaining action**: Continue compiler evolution (PTX/SM120,
naga::Module ingest, compile deadline). Hardware lifecycle is 100% toadStool's.

---

## toadStool — Evolution Directives (CRITICAL PATH — coralReef excised)

**coralReef Sprint 9 excised the diesel engine stack.** There is no fallback.
toadStool is now the sole owner of GPU hardware lifecycle. Phase C is blocking.

toadStool's own `PHASE_C_CORAL_DRIVER_SPLIT_PLAN.md` documents the absorption
boundary. S245–S249 landed cylinder foundation types/traits. S237 absorbed ember
(Phase A). S239 absorbed glowplug (Phase B). What remains is the daemon runtime.

### E1: Phase C — Daemon Runtime Absorption (P0)

hotSpring audited `toadstool daemon` and found it lacks the diesel engine
runtime that coral-glowplug provided. Specific parity gaps:

| Gap | Current State | Needed |
|-----|--------------|--------|
| `device.swap` RPC | Not wired in JSON-RPC handler | Wire to `GlowPlugClient::swap_device_orchestrated` |
| `device.warm_catch` RPC | Missing entirely | Port from coral-ember `handlers_warm_catch.rs` |
| Cylinder subprocess | No crate, no process isolation | Create `toadstool-cylinder`, port `cylinder.rs` |
| VFIO fd holding | `VfioResourceHandle` is metadata-only | Real `OwnedFd` through swap cycles |
| Warm pipeline | `warm_cycle_performed` always false | Nouveau round-trip + livepatch + FECS preservation |
| SwapOrchestrator completeness | Quiesce/persist/restore are stubs | Real implementations |
| CLI commands | No warm-fecs, swap, status, health | Port coralctl's ~20 subcommands |
| systemd service | None | `toadstool.service` (same caps as coral-glowplug.service) |

### E2: Phase C Execution Plan (from hotSpring)

hotSpring created a detailed 7-item execution plan:

1. **C1**: Create `toadstool-cylinder` crate (~4k LOC) — port cylinder.rs
2. **C2**: Absorb coral-driver hardware modules (~15k LOC) — per split plan
3. **C3**: Wire daemon RPC surface (~2k LOC) — device.swap, warm_catch, health
4. **C4**: VFIO fd holding (~1k LOC) — real OwnedFd in VfioResourceHandle
5. **C5**: Warm pipeline (~2k LOC) — warm-fecs, warm-catch, livepatch control
6. **C6**: CLI parity (~3k LOC) — toadstool swap/warm-fecs/status/health
7. **C7**: systemd service — toadstool.service replacing coral-glowplug.service

**Execution order**: C1+C2 parallel → C3 → C4 → C5 → C6 → C7

**Reference**: `springs/hotSpring/wateringHole/handoffs/HOTSPRING_PHASE_C_EXECUTION_PLAN_MAY12_2026.md`

Note: S245-S249 have already landed significant Phase C work (cylinder
foundation, DRM, AMD, NVIDIA non-GSP, VFIO foundation, 415 cylinder tests).
The E1 gaps above are what remains after that progress.

### E3: hotSpring Validation Contract

For each Phase C deliverable, hotSpring will validate:

- `validate_vfio_sovereign` — warm open + compile + dispatch + readback
- `s_vfio_dispatch` scenario — harness integration (17 scenarios total)
- coralctl parity: `toadstool warm-fecs` produces same warm state as `coralctl`
- K80 warm-catch with --memory-type gddr5
- RTX 5060 dispatch via toadStool IPC (Phase D)
- 590/590 lib tests pass throughout

hotSpring is the hardware validation authority for sovereign compute.
Pattern: toadStool lands code, hotSpring validates on hardware, gaps flow back.

---

## hotSpring — Self-Evolution Notes (updated post-excision)

### Current status

- 590/590 lib tests, 17 validation scenarios (14 default + 3 feature-gated)
- `coral-gpu` dependency commented out (coralReef Sprint 9 excision)
- `sovereign-dispatch` feature is stub — bins/scenarios gated but won't compile
- Titan V: warm open + 3 shader compiles PASS, dispatch readback pending
- K80: in D3cold, needs warm-catch cycle
- RTX 5060: DRM dispatch operational (existing wgpu path)
- GAP-HS-094 through GAP-HS-096 documented and handed off
- barraCuda v0.4.0 provides `sovereign_dispatch_wire.rs` + `precision.route`

### Remaining local work

1. **Rewire sovereign-dispatch to toadStool** — when toadStool Phase C lands,
   replace `coral_gpu::GpuContext` usage in `bin_helpers/coral_sovereign/`,
   `validate_vfio_sovereign`, `s_vfio_dispatch` with toadStool's dispatch API
   (or barraCuda's `sovereign_dispatch_wire` → `compute.dispatch.submit`)
2. **Validate toadStool Phase C deliverables** — as toadStool lands C1-C7,
   validate each on local hardware (Titan V, K80, RTX 5060)
3. **FECS dispatch readback** — re-validate after toadStool absorbs the FECS
   recovery code from coralReef git history
4. **K80 warm-catch cycle** — once toadStool warm pipeline is wired
5. **Fleet discovery migration** — `fleet_client.rs` `/run/coralreef/` →
   `/run/toadstool/`, `coral-ember-fleet.json` → toadStool equivalent
6. **PRIMAL_ALIASES** — `primal_bridge.rs` drop `coral-glowplug`, add toadStool
7. **Evolution pass B9** — next LTEE guideStone module queued

### Upstream dependency map (post-excision)

```
hotSpring (barracuda)
├── barraCuda v0.4.0 (precision.route, sovereign_dispatch_wire) ✓
├── coralReef (compiler only: shader.compile IPC) ✓
├── toadStool (compute.dispatch.submit IPC) — CRITICAL PATH
│   ├── Phase A ember absorption ✓
│   ├── Phase B glowplug absorption ✓
│   ├── Phase C coral-driver + cylinder + daemon runtime ← BLOCKING
│   └── Phase D local dispatch ← after C
└── coral-gpu (REMOVED — was VFIO dispatch) ✗ commented out
```

---

## Evolution Pattern

```
hotSpring solves locally on hardware
  → hands patterns upstream (this document)
    → primals absorb and abstract
      → hotSpring resolves with their new abstraction
        → evolution
```

coralReef is now a **pure compiler primal** — shader compilation only.
toadStool owns **all hardware lifecycle** — the diesel engine, VFIO,
warm/cold boot, dispatch. hotSpring validates the composition on real
hardware and feeds gaps back through this cycle.

barraCuda provides the **shared ontology** — precision tiers, dispatch wire
protocol, physics domain routing. It speaks the contract that binds
coralReef (compile) → toadStool (dispatch) → hardware.
