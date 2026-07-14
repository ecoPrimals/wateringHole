# ecoPrimals Ecosystem Blurb — Wave 138b

**Date**: Jul 14, 2026 12:00 EDT | **Wave**: 138b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** First FIDO2 credential minted. Tap-sequence entropy ceremony built. SoloKeys are human proximity sensors and genetic generators at this layer. 2 items remain.

---

## This Cascade — SoloKey Ceremony Breakthrough

### First Credential Minted (bearDog)

```
rp_id:     primals.eco
algorithm: ES256 (P-256 / ECDSA)
storage:   SoloKey Solo 2 secure element — private key never leaves chip
```

Four bugs fixed to get here: HIDRAW-REPORT-ID (0x00 prefix), CTAPHID_MSG vs CBOR
(0x83 → 0x90), InvalidOption (`up:true` invalid for MakeCredential), EAGAIN busy-poll
(300 attempts / 60s window).

### Tap-Sequence Entropy Ceremony (bearDog — NEW)

`beardog.fido2.ceremony` — multi-tap entropy harvest via IPC:

```
Layer 1: Transport timing — nanosecond capture of EAGAIN/keepalive/response
Layer 2: Ceremony orchestrator — N GetAssertion calls with fresh OS-RNG challenges
Layer 3: IPC + BLAKE3 mixing — per-tap (challenge + signature + reaction_ns + jitter)
```

Returns 32 bytes of Tier 3 entropy: BLAKE3 keyed hash mixing OS RNG (Tier 1),
hardware signature nonce (Tier 2), and human tap timing (Tier 3).

### SoloKey as Human Proximity Sensor

At this layer, SoloKeys are **human proximity sensors and genetic generators** —
the tap proves a human is physically present, and the timing jitter generates
entropy unique to that human-device interaction. This tests the full system
interaction chain before later evolution locks keys to specific identities.
The user is their own key in later stages.

**Biological model**: Genetic diversity from multiple independent randomness sources:
- Tier 1 (OS): Environmental noise (thermal, interrupt timing)
- Tier 2 (Hardware): Internal mutation (hardware RNG in secure element)
- Tier 3 (Human): Selection pressure (human temporal signature)

No single compromised source can predict the seed.

### SoloKey Firmware Issue Discovered (ERR_CHANNEL_BUSY)

After CTAP2 timeout (no touch within 30s), SoloKey enters permanent
`ERR_CHANNEL_BUSY (0x06)` — requires physical unplug/replug. USB reset
does not clear. Confirmed with `python-fido2` reference library.
Mitigation: `CTAPHID_CANCEL (0x91)` sent during init.

---

## Teams, Code, and Goals

### bearDog team (crypto / hardware trust)
**Code**: `primals/bearDog` — `beardog-hid`, `beardog-tunnel`, `beardog-security`

| Goal | Status | Next |
|------|--------|------|
| **First credential** | MINTED (primals.eco, ES256) | Authenticate → GetAssertion signature |
| **Tap-sequence ceremony** | BUILT (3-layer: transport timing, orchestrator, BLAKE3 mixing) | Live 3-5 tap test after replug |
| **HIDRAW-REPORT-ID** | RESOLVED (0x00 prefix) | — |
| **Loam Certificate seeding** | Design: Tier 1+2+3 → BLAKE3 keyed hash → Loam cert seed | After ceremony validated |
| **ERR_CHANNEL_BUSY** | Discovered + CTAPHID_CANCEL mitigation | Ceremony UX must account for replug |

### biomeOS team (orchestration)
**Code**: `primals/biomeOS`

| Goal | Status | Next |
|------|--------|------|
| **NAPI-LIFECYCLE** | `lifecycle.status` count=0 (P2) | Wire registration |
| **SOCKET-DIR-UNIFY** | Mixed socket dirs (P2) | Consolidate to `/run/membrane/` |

### All other teams — no changes this cascade (status unchanged from prior blurb)

---

## Remaining — 2 items

| ID | Owner | P | What |
|----|-------|---|------|
| **NAPI-LIFECYCLE** | biomeOS | 2 | LifecycleManager registration |
| **SOCKET-DIR-UNIFY** | biomeOS | 2 | Socket dir → `/run/membrane/` only |

**Resolved this wave**:
- ~~HIDRAW-REPORT-ID~~ — 0x00 report ID prefix in HID writes
- ~~FORGEJO-PERMS-RECUR~~ — 3-layer permanent fix deployed to golgi
- ~~BIOMEOS-TEMPLATE~~ — `service.template` subcommand implemented

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit

```
DONE    beardog.fido2.discover → SoloKey enumeration
DONE    CTAPHID_INIT handshake (firmware 2.3.196, CBOR+WINK)
DONE    HIDRAW-REPORT-ID fix (0x00 prefix)
DONE    First credential minted (primals.eco, ES256)
DONE    Tap-sequence ceremony built (3-layer entropy)
NOW     Authenticate: GetAssertion → verify credential works
NOW     Live tap-sequence test (3-5 taps after replug)
NEXT    Entropy harvest: Tier 1+2+3 → BLAKE3 → Loam cert seed
NEXT    Pixel StrongBox ceremony (ADB, Titan M2)
GOAL    SoloKey = human proximity sensor + genetic generator
        User is their own key. USB kit deploys NUCLEUS identity.
```

### Track 2: K-Derm Extrication → Sovereign Membrane Parity

```
DONE    *.primals.eco wildcard DNS
DONE    FORGEJO-PERMS 3-layer defense
DONE    100% Rust deployment pipeline
DONE    BIOMEOS-TEMPLATE resolved
NOW     primal.eco separation (inner membrane)
GOAL    Full sovereign membrane parity
```

### Track 3: Live Compositions → External Science Production

```
DONE    footPrint GIS at primals.eco/footprint/
DONE    JupyterHub at lab.primals.eco
DONE    Composition routing standard shipped
NOW     ABG user accounts, tideGlass Phase 0
GOAL    External science through sovereign compositions
```

---

## primalSpring Scenarios to Write (from ceremony exploration)

| Scenario | Validates |
|----------|-----------|
| `s_fido2_register_e2e` | MakeCredential → valid credential_id + COSE key |
| `s_fido2_authenticate_e2e` | GetAssertion signature verifies against registered key |
| `s_fido2_entropy_mixing` | Tier 1+2+3 mixed, output passes NIST SP 800-22 basics |
| `s_fido2_tap_timing_entropy` | Nanosecond timing capture, non-zero values |
| `s_fido2_ceremony_chain` | register → authenticate → entropy → Loam cert seed |
| `s_fido2_timeout_tolerance` | UserActionTimeout handled gracefully |

Mock (CI) + Live (gate with SoloKey) dual-mode via `/dev/hidraw` detection.

---

## Gate Status

```
eastGate     — PRIMARY. Cascade absorbed. bearDog ceremony code merged.
sporeGate    — NUCLEUS. SoloKey plugged. First credential minted. Depot authority.
golgiBody    — Outer membrane. Wildcard DNS. FORGEJO-PERMS 3-layer defense.
flockGate    — bearDog FIDO2 + primalSpring scenarios.
ironGate     — ABG/NF compute. JupyterHub. 13/13 active.
grapheneGate — StrongBox target. Android compile unblocked.
```

---

*Wave 138b: first FIDO2 credential minted on primals.eco. Tap-sequence entropy ceremony built — SoloKeys as human proximity sensors and genetic generators. 4 bugs fixed. Tier 3 human entropy model designed. ERR_CHANNEL_BUSY firmware issue discovered. 2 items remain.*
