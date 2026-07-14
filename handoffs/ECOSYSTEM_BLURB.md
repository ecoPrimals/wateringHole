# ecoPrimals Ecosystem Blurb — Wave 138b

**Date**: Jul 14, 2026 09:30 EDT | **Wave**: 138b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** 3 items remain. SoloKey physically tested (P0 HID fix identified). FORGEJO-PERMS permanently fixed. wateringHole distilled to 83 active docs.

---

## Teams, Code, and Goals

### bearDog team (crypto / hardware trust)
**Code**: `primals/bearDog` — `beardog-hid`, `beardog-tunnel`, `beardog-security`
**Gate**: sporeGate (physical SoloKey) + flockGate (scenarios)

| Goal | Status | Next |
|------|--------|------|
| **SoloKey FIDO2 ceremony** | CTAPHID handshake proven, MakeCredential blocked by `HIDRAW-REPORT-ID` (P0) | Fix report ID prefix → complete register → authenticate → entropy harvest |
| **Loam Certificate from hardware** | Code path wired (`beardog.fido2.entropy` IPC) | Blocked on SoloKey ceremony completion |
| **Pixel StrongBox entropy** | Android compile fixed, Titan M2 StrongBox API scaffolded | Physical test after SoloKey ceremony |
| **HID transport hardening** | EAGAIN retry + CTAPHID_CBOR command byte fixed | `HID-BLOCKING-IO` (P1): blocking I/O + spawn_blocking |

### cellMembrane team (deployment / operations)
**Code**: `gardens/cellMembrane` — `membrane-shadow`, `membrane-nucleus`
**Gate**: sporeGate + golgi (provisioning)

| Goal | Status | Next |
|------|--------|------|
| **100% Rust deployment** | Complete (bash fossilized Wave 137b) | Maintain |
| **service.template subcommand** | Implemented this wave (resolves BIOMEOS-TEMPLATE) | — |
| **FORGEJO-PERMS permanent fix** | 3-layer defense deployed to golgi | Monitor (6hr timer enforces) |
| **Composition provisioning** | `provision-golgi.sh` with wildcard DNS + security headers | Add new Caddy blocks as compositions deploy |

### biomeOS team (orchestration / Neural API)
**Code**: `primals/biomeOS` — Neural API, LifecycleManager, coordination patterns
**Gate**: sporeGate (systemd) + eastGate (primalSpring validation)

| Goal | Status | Next |
|------|--------|------|
| **Neural API deployment authority** | 12/12 complete, 48 primals on sporeGate | Maintain |
| **LifecycleManager registration** | `lifecycle.status` count=0 (NAPI-LIFECYCLE, P2) | Wire registration for primal lifecycle supervision |
| **Socket dir unification** | Mixed `/run/membrane/` and `/run/biomeos/` (SOCKET-DIR-UNIFY, P2) | Consolidate to single dir, unblock songBird TLS delegation |

### songBird team (networking / mesh / drawbridge)
**Code**: `primals/songBird` — mesh federation, drawbridge routing, TLS
**Gate**: all gates (mesh peer)

| Goal | Status | Next |
|------|--------|------|
| **3-gate WireGuard mesh** | eastGate ↔ sporeGate ↔ golgi operational | Expand to ironGate, strandGate |
| **Drawbridge capability routing** | DRAWBRIDGE-CAP resolved (runtime cap merge + fallback + resolve) | Route new compositions as they deploy |
| **Composition proxy** | footPrint (10 GIS hosts), JupyterHub, Forgejo proxied | tideGlass, helixVision when ready |

### primalSpring team (validation / scenarios)
**Code**: `springs/primalSpring` — ecoPrimal validation suite
**Gate**: eastGate (primary) + flockGate (scenarios)

| Goal | Status | Next |
|------|--------|------|
| **Scenario coverage** | 125 active + 22 commented (source files landed, compilation pending) | Enable scenarios as compilation fixes land |
| **Test health** | 1,107 passed / 0 failed / 2 ignored | Maintain zero-fail |
| **Hardware trust validation** | `s_fido2_entropy_ceremony`, `s_hardware_trust_pipeline`, `s_keygen_interaction_surface` registered | Wire to live SoloKey after HIDRAW fix |

### sporePrint team (public site / content)
**Code**: `infra/sporePrint` — Zola static site at `primals.eco`
**Gate**: golgi (Caddy serving)

| Goal | Status | Next |
|------|--------|------|
| **Public site live** | `primals.eco` + `primals.eco/footprint/` live | NF case study, tideGlass product page, collaborator profiles |
| **Content pipeline** | `membrane content.rebuild` implemented | sporePrint content for pre-grant pipeline methodology |

### overwatch (eastGate — coordination / wateringHole)
**Code**: `infra/wateringHole`, `infra/whitePaper`
**Gate**: eastGate

| Goal | Status | Next |
|------|--------|------|
| **wateringHole ownership** | Distilled: 83 active docs, 945 fossilized, 10-category index | Maintain, fossilize as waves close |
| **Composition routing standard** | Shipped (whitePaper gen5 + wateringHole) | Evolve as compositions deploy |
| **Collaborator activation** | ABG (producing), Gonzales (engaged), Jones (active), Chuna (delivery-ready) | ABG accounts (REALWORLD), tideGlass Phase 0, sporePrint content |

---

## Three Tracks → Glacial Goals

### Track 1: Hardware Trust → NUCLEUS USB Kit
**Teams**: bearDog, primalSpring, eastGate overwatch
**Code**: `beardog-hid`, `beardog-tunnel`, primalSpring scenarios
**Path**:

```
DONE    beardog.fido2.entropy IPC wired
DONE    SoloKey CTAPHID handshake proven (firmware 2.3.196)
NOW     HIDRAW-REPORT-ID fix (P0, one-line)
NEXT    MakeCredential → authenticate → entropy harvest
THEN    Loam Certificate from hardware credential
THEN    Pixel StrongBox ceremony (ADB, Titan M2)
GOAL    USB topology as deployment primitive
        SoloKey + NPU + compute = NUCLEUS kit
        Any node gets hardware-attested identity from ceremony
```

### Track 2: K-Derm Extrication → Sovereign Membrane Parity
**Teams**: cellMembrane, songBird, sporePrint
**Code**: `cellMembrane`, `songBird`, `provision-golgi.sh`
**Path**:

```
DONE    *.primals.eco wildcard DNS
DONE    FORGEJO-PERMS 3-layer defense
DONE    100% Rust deployment pipeline
DONE    BIOMEOS-TEMPLATE resolved
NOW     primal.eco separation (inner membrane for private compositions)
NEXT    bearDog gatehouse cutover (sovereign TLS authority)
GOAL    Outer membrane (primals.eco) fully sovereign
        Inner membrane (primal.eco) for key ceremonies + private data
        No external dependency for core operations
```

### Track 3: Live Compositions → External Science Production
**Teams**: sporePrint, songBird, overwatch, collaborators
**Code**: `protists/footPrint`, `protists/tideGlass`, JupyterHub, sporePrint
**Path**:

```
DONE    footPrint GIS at primals.eco/footprint/
DONE    JupyterHub at lab.primals.eco
DONE    Composition routing standard + pattern shipped
DONE    ABG access guide shipped
NOW     ABG user accounts (REALWORLD)
NOW     tideGlass Phase 0 (Zenodo GPS archaeology)
NEXT    NF Data Portal ingestion → NestGate CAS
NEXT    sporePrint: NF case study, collaborator profiles
GOAL    External science ships through sovereign compositions
        Collaborators consume compositions, never see primals
        Data feeds register with drawbridge, cross-feed via mesh
```

### Glacial Goal: Universal Substrate Evolution
**All teams**

```
DONE    x86_64 musl-static ecobins (35 binaries)
DONE    aarch64 cross-compile (pepti warehouse)
DONE    Android compile unblocked (grapheneGate)
NEXT    RISC-V, Windows, WASM, macOS Silicon
GOAL    NUCLEUS deploys on any architecture
        Any substrate, any gate, same sovereign infrastructure
```

---

## Remaining — 3 items

| ID | Owner | P | What |
|----|-------|---|------|
| **HIDRAW-REPORT-ID** | bearDog | 0 | 0x00 report ID prefix in HID writes — unblocks SoloKey |
| **NAPI-LIFECYCLE** | biomeOS | 2 | LifecycleManager registration |
| **SOCKET-DIR-UNIFY** | biomeOS | 2 | Socket dir → `/run/membrane/` only |

---

*Wave 138b: 7 teams, 3 tracks, 1 glacial goal. SoloKey one byte from ceremony. FORGEJO-PERMS permanently fixed. wateringHole distilled. 3 items remain.*
