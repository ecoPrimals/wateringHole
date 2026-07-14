# ecoPrimals Ecosystem Blurb — Wave 138b

**Date**: Jul 14, 2026 09:30 EDT | **Wave**: 138b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** SoloKey physically tested — CTAPHID handshake proven, P0 HID bug identified. FORGEJO-PERMS-RECUR permanently fixed (3-layer defense). primalSpring health restored (125 scenarios, 1,107 tests). wateringHole distilled (83 active docs, 945 fossilized). 3 carried items.

---

## This Cascade — Wave 138b Incoming

### SoloKey Physical Test (sporeGate — AAR shipped)

First hardware trust ceremony in the ecosystem. SoloKey Solo 2 plugged
into sporeGate NUC. Results:

| Step | Result |
|------|--------|
| Device discovery (`beardog.fido2.discover`) | **PASS** — Solo 2 at `/dev/hidraw4` |
| CTAPHID_INIT handshake | **PASS** — Channel 0x06, firmware 2.3.196, CBOR+WINK caps |
| MakeCredential write | **PASS** — 4 packets, 208 bytes CBOR delivered |
| MakeCredential response | **BLOCKED** — EAGAIN ×150, LED did not blink |
| Build system (`cargo build --features fido2`) | **PASS** — 30 FIDO2 tests green |

**Root cause**: `HIDRAW-REPORT-ID` — Linux hidraw requires 0x00 report ID
prefix on writes for FIDO2 devices. bearDog sends 64 raw bytes, kernel
expects 65 (0x00 + 64 payload). MakeCredential never reaches authenticator logic.

**P0 Fix**: Prepend 0x00 in `LinuxHidDevice::write()`. One-line fix, gated
on `has_report_id` flag from HID report descriptor.

### bearDog FIDO2 Fixes (2 commits absorbed)

- `CTAPHID_CBOR` command byte (0x90) for CTAP2 operations — was using MSG (0x83)
- EAGAIN retry with `POLL_INTERVAL_MS` constant (200ms) for user-presence touch
- Example compile fixes for test harness

### cellMembrane Debt Sprint (2 commits absorbed)

- `service.template` subcommand implemented (resolves BIOMEOS-TEMPLATE)
- `freshness.toml` constants migrated
- Visibility tightening round 2

### primalSpring Health Restore (sporeGate — AAR shipped)

- 20 phantom scenario registrations commented out (source files pending)
- Drift tolerance fixed for multi-gate freshness
- Stale socket guard for offline primals
- Suite: **1,107 passed / 0 failed / 2 ignored**

### FORGEJO-PERMS-RECUR Permanent Fix (sporeGate — AAR shipped)

Three-layer defense deployed to golgi:
1. `ExecStartPost` in `cascade-sense.service` — `chown -R git:git` after every cascade
2. `/etc/tmpfiles.d/forgejo-perms.conf` — enforce on every boot
3. `forgejo-perms.timer` — 6-hour safety net periodic enforcement

### wateringHole Distillation (eastGate)

- 980+ documents fossilized to `fossilRecord/wave138a_cleanup/`
- Active docs: **83** (down from 1,027)
- Root standards: **46** (down from 64)
- README index restructured into 10 clean categories

---

## Remaining — 3 items (was 4)

| ID | Owner | Priority | What |
|----|-------|----------|------|
| **HIDRAW-REPORT-ID** | bearDog | P0 | Prepend 0x00 report ID in HID writes — unblocks SoloKey ceremony |
| **NAPI-LIFECYCLE** | biomeOS | P2 | LifecycleManager registration |
| **SOCKET-DIR-UNIFY** | biomeOS | P2 | Socket dir consolidation |

**Resolved this wave**:
- ~~FORGEJO-PERMS-RECUR~~ — 3-layer permanent fix deployed to golgi
- ~~BIOMEOS-TEMPLATE~~ — `service.template` subcommand implemented in cellMembrane

---

## SoloKey Ceremony Path (from AAR)

```
DONE:   discover → CTAPHID_INIT → channel allocation → MakeCredential write
NEXT:   HIDRAW-REPORT-ID fix → MakeCredential response → user presence touch
THEN:   authenticate → entropy harvest → Loam Certificate mint
FUTURE: USB topology as deployment primitive (SoloKey + NPU + compute = NUCLEUS kit)
```

Additional bearDog items from physical test:
- `HID-BLOCKING-IO` (P1): Replace O_NONBLOCK with blocking I/O + spawn_blocking
- `CTAPHID-PING-DIAG` (P2): Add CTAPHID_PING for transport-level diagnostics
- `CTAP2-GETINFO-FIRST` (P2): Issue GetInfo before MakeCredential

---

## Gate Status

```
eastGate     — PRIMARY. Cascade absorbed. primalSpring 125 scenarios / 1,107 tests.
sporeGate    — NUCLEUS. SoloKey physically tested. Depot authority. FORGEJO-PERMS fixed.
golgiBody    — Outer membrane. Wildcard DNS. FORGEJO-PERMS 3-layer defense live.
flockGate    — bearDog FIDO2 + primalSpring scenarios.
ironGate     — ABG/NF compute. JupyterHub v5.4.5. 13/13 active.
grapheneGate — StrongBox target. Android compile unblocked.
```

---

## Evolution Path

```
NOW:    HIDRAW-REPORT-ID fix → SoloKey MakeCredential completes
        bearDog FIDO2 ceremony: register → authenticate → entropy → Loam cert
        Composition routing standard + pattern docs shipped

NEXT:   Hardware entropy ceremonies (SoloKey + Pixel StrongBox)
        primal.eco separation (private compositions, key ceremonies)
        tideGlass Phase 0 (Zenodo GPS archaeology)
        sporePrint: NF case study, collaborator profiles

FUTURE: NUCLEUS USB kit (SoloKey + NPU + compute)
        Universal substrate: NUCLEUS on any architecture
        nestgate.io federated data gateway
```

---

*Wave 138b: SoloKey physically tested — first hardware trust ceremony. Protocol handshake proven, P0 HID bug identified (one-line fix). FORGEJO-PERMS permanently fixed. primalSpring health restored. wateringHole distilled to 83 active docs. 3 items remain.*
