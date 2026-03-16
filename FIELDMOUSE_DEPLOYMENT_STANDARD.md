# fieldMouse Deployment Standard — Minimal Deployable Structure

**Status**: ECOSYSTEM STANDARD  
**Version**: 0.1.0  
**Date**: March 2, 2026  
**Authority**: wateringHole (ecoPrimals Core Standards)  
**Compliance**: All sub-NUCLEUS embedded/edge deployments  

---

## Purpose

This standard defines **fieldMouse**: the smallest deployable unit in the
ecoPrimals ecosystem. Where a gate runs a full NUCLEUS and a niche composes
primals via biomeOS deploy graphs, a fieldMouse strips to the absolute minimum —
as few as a single atomic or chimera — purpose-built for a constrained deployment
niche.

fieldMouse is not a primal. It is a **deployment class**.

---

## Core Properties

Every fieldMouse deployment, regardless of subtype, satisfies these invariants:

| Property | Requirement |
|----------|-------------|
| **Minimal** | Smallest subset of atomics/chimeras that fulfills the niche — no unused primals |
| **Embedded-first** | Targets constrained hardware: RISC-V, ARM (aarch64/armv7), microcontrollers, SoCs |
| **ecoBin compliant** | Pure Rust, zero C deps, cross-compiles with `cargo build --target` |
| **Mesh-native** | Connects to the broader ecosystem via songBird (UDP/TCP) or serial fallback |
| **Provenance-aware** | Signs all emitted data via bearDog — no unsigned bytes leave a fieldMouse |
| **Self-describing** | Responds to `health.check` and `capability.list` like any primal |
| **Deterministic boot** | Single static binary, no runtime dependency resolution, no deploy graph |

---

## Position in the Evolutionary Ladder

```
NUCLEUS     (full primal composition — gate, all atomics + Squirrel)
  ↓
Niche       (biomeOS deploy graph — selected primals, BYOB composition)
  ↓
fieldMouse  (minimal atomic/chimera — embedded, sensor, edge, no biomeOS)
```

A fieldMouse **does not run biomeOS**. It has no deploy graph, no Neural API
router, no capability discovery layer. It is a static composition — the exact
set of primals is compiled in. biomeOS on a gate discovers fieldMouse nodes
on the mesh via songBird beacons and treats them as remote capability providers.

---

## Anatomy of a fieldMouse

### Minimum Viable fieldMouse

The smallest possible fieldMouse is a **Tower Atomic chimera** — bearDog + songBird
fused into a single binary. This provides:

- Cryptographic identity (Ed25519 signing, BLAKE3 hashing)
- Mesh connectivity (BirdSong beacon, mDNS, UDP/TCP)
- Provenance (every message signed)

From this base, additional capabilities are added by composing more atomics:

| fieldMouse Class | Composition | Use Case |
|------------------|-------------|----------|
| **Tower** | bearDog + songBird | Identity + mesh node, relay, beacon |
| **Sensor** | Tower + domain logic | Data acquisition (pH, temp, GPS, flow) |
| **Edge** | Tower + toadStool + barraCuda | On-device compute (Akida NPU, GPU SoC) |
| **Store** | Tower + nestGate | Content-addressed local cache + mesh sync |
| **Lab** | Tower + nestGate + domain spring | Instrument data pipeline (pipette, sequencer) |

### Chimera Fusion

fieldMouse deployments are **chimeras** — multiple primals fused into a single
binary with a unified API surface. Unlike a niche (multiple binaries coordinated
by biomeOS), a fieldMouse chimera is one binary, one process, one socket.

The chimera binary exposes a merged JSON-RPC namespace:

```
crypto.sign       → bearDog
mesh.beacon       → songBird
sensor.read       → domain logic
provenance.stamp  → bearDog + sweetGrass (if present)
```

---

## Hardware Targets

fieldMouse targets hardware that cannot run a full NUCLEUS. The ecoBin standard
already guarantees cross-compilation; fieldMouse adds embedded-specific constraints.

### Reference Targets

| Target | Architecture | RAM | Example Hardware | fieldMouse Class |
|--------|-------------|-----|------------------|-----------------|
| **RISC-V MCU** | rv32imac / rv64gc | 256KB–4MB | ESP32-C3, Milk-V Duo | Tower |
| **ARM Cortex-M** | thumbv7em | 256KB–1MB | STM32F4, nRF52840 | Tower, Sensor |
| **Raspberry Pi Zero** | aarch64 | 512MB | Pi Zero 2 W | Tower, Sensor, Store |
| **Raspberry Pi 4/5** | aarch64 | 2–8GB | Pi 4B, Pi 5 | Any class up to Edge |
| **Coral Dev Board** | aarch64 + Edge TPU | 1–4GB | Google Coral, Akida | Edge |
| **NVIDIA Jetson** | aarch64 + GPU | 4–16GB | Jetson Nano/Orin | Edge |
| **Lab SoC** | aarch64 / x86_64 | 1–8GB | Custom, BeagleBone AI | Lab |

### Build Targets

```bash
# RISC-V (ESP32-C3, bare metal)
cargo build --target riscv32imc-unknown-none-elf --release

# ARM Cortex-M (STM32, bare metal)
cargo build --target thumbv7em-none-eabihf --release

# Raspberry Pi (Linux)
cargo build --target aarch64-unknown-linux-musl --release

# ARMv7 (older Pi, BeagleBone)
cargo build --target armv7-unknown-linux-musleabihf --release
```

All targets use `musl` for Linux (static linking, no glibc dependency) or
bare-metal targets for microcontrollers.

---

## Data Model

Every fieldMouse emits **fieldMouse frames** — the atomic unit of data from a
fieldMouse deployment. A frame is a signed JSON-RPC notification:

```json
{
  "jsonrpc": "2.0",
  "method": "fieldmouse.frame",
  "params": {
    "device_id": "fm-soil-probe-017",
    "timestamp_utc": "2026-03-02T14:23:07.003Z",
    "location": { "lat": 42.7325, "lon": -84.5555, "alt_m": 256.3 },
    "readings": {
      "ph": 6.8,
      "moisture_pct": 34.2,
      "temp_c": 12.1
    },
    "provenance": {
      "signer": "ed25519:fm-soil-probe-017",
      "signature": "base64:...",
      "hash": "blake3:..."
    }
  }
}
```

Frames are:

- **Signed at source** — bearDog signs before transmission
- **Timestamped** — monotonic + wall clock
- **Geotagged** — GPS when available, configured fallback otherwise
- **Schema-flexible** — `readings` is domain-specific, no fixed schema
- **Streamable** — NDJSON over songBird, serial, or TCP

A gate receiving fieldMouse frames can ingest them into nestGate (storage),
stamp them via sweetGrass (attribution), and commit them via loamSpine
(permanence) — the full provenance trio, applied to edge data.

---

## fieldMouse Subtypes

fieldMouse is a deployment class, not a single product. Subtypes are defined
by the intersection of **hardware target** and **domain function**.

### Environmental Monitoring

| Subtype | Sensors | Target | Use Case |
|---------|---------|--------|----------|
| **fm-soil** | pH, moisture, temp, conductivity | RISC-V / Pi Zero | Soil microbiome, agriculture |
| **fm-air** | PM2.5, O3, NO2, CO, temp, humidity | ARM Cortex-M / Pi | Air quality, pollution monitoring |
| **fm-water** | pH, dissolved O2, turbidity, temp | Pi Zero / custom | Stream/well monitoring |
| **fm-geo** | GPS, accelerometer, magnetometer | RISC-V | Drift tracking, geological survey |

### Lab Instruments

| Subtype | Function | Target | Use Case |
|---------|----------|--------|----------|
| **fm-pipette** | Volume, sample ID, timestamp, provenance | Pi Zero / custom SoC | Wet lab data streaming |
| **fm-sequencer** | MinION data relay, basecall streaming | Pi 4/5 + Akida | Field genomics |
| **fm-plate** | Well position, OD reading, timestamp | Pi / BeagleBone | HTS plate reader interface |
| **fm-incubator** | Temp, CO2, humidity, door events | RISC-V / Pi Zero | Culture monitoring |

### Edge Compute

| Subtype | Function | Target | Use Case |
|---------|----------|--------|----------|
| **fm-classify** | Real-time inference on streaming data | Coral / Akida / Jetson | Microbial classification |
| **fm-anomaly** | Outlier detection on sensor streams | Pi 4 + NPU | Environmental anomaly |
| **fm-compress** | Local data reduction before uplink | Any ARM | Bandwidth-constrained sites |

---

## Mesh Integration

fieldMouse nodes are **leaf nodes** in the ecoPrimals mesh. They do not route
traffic or coordinate other primals. They emit data and respond to queries.

```
┌──────────────┐
│    Gate       │  (NUCLEUS — full ecosystem)
│   biomeOS     │
│   songBird    │◄──── BirdSong mesh ────►┌─────────────┐
│   nestGate    │                          │ fieldMouse   │
│   sweetGrass  │                          │ (fm-soil)    │
│   loamSpine   │                          │ Tower chimera│
└──────────────┘                          └─────────────┘
       ▲                                         ▲
       │              BirdSong mesh              │
       ▼                                         ▼
┌──────────────┐                          ┌─────────────┐
│ fieldMouse   │                          │ fieldMouse   │
│ (fm-pipette) │                          │ (fm-classify)│
│ Lab chimera  │                          │ Edge chimera │
└──────────────┘                          └─────────────┘
```

### Discovery

1. fieldMouse boots and generates a BirdSong beacon using its family seed
2. Gates on the same mesh decrypt the beacon, confirming family membership
3. biomeOS registers the fieldMouse as a remote capability provider
4. Frames stream to the gate(s) for provenance trio processing

### Offline Operation

fieldMouse nodes MUST operate when disconnected from the mesh:

- Continue collecting and signing data locally
- Buffer frames in a circular log (size configurable per subtype)
- Sync buffered frames when mesh connectivity resumes
- Never discard provenance — local signatures are valid offline

---

## Naming Convention

fieldMouse subtypes follow the pattern:

```
fm-<domain>[-<specialization>]
```

Examples: `fm-soil`, `fm-air-indoor`, `fm-pipette`, `fm-sequencer-minion`,
`fm-classify-akida`, `fm-water-stream`.

The `fm-` prefix is mandatory and identifies the deployment as a fieldMouse
class in logs, mesh discovery, and provenance chains.

---

## Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| **ecoBin** | fieldMouse binaries ARE ecoBins — Pure Rust, cross-compilable |
| **UniBin** | fieldMouse chimeras follow UniBin subcommand structure |
| **genomeBin** | NOT required — fieldMouse deploys are typically flashed or scp'd |
| **GATE_DEPLOYMENT_STANDARD** | Gates receive fieldMouse data; fieldMouse is not a gate |
| **SPRING_AS_NICHE_DEPLOYMENT** | Springs can include fieldMouse firmware as build artifacts |
| **PRIMAL_IPC_PROTOCOL** | fieldMouse uses JSON-RPC 2.0 but over constrained transports |
| **CROSS_SPRING_DATA_FLOW** | fieldMouse frames feed into cross-spring data pipelines |

---

## What fieldMouse Is NOT

- **Not a primal** — it's a deployment class
- **Not a niche** — no biomeOS, no deploy graph, no runtime composition
- **Not a gate** — no NUCLEUS, no local primal orchestration
- **Not a product** — it's a standard for building minimal ecoPrimals deployments
- **Not optional** — any ecoPrimals deployment below niche-scale IS a fieldMouse

---

## Evolution Path

fieldMouse deployments can grow:

```
fieldMouse (Tower chimera)
  → add nestGate (Store class)
  → add barraCuda (Edge class)
  → add biomeOS (now it's a Niche, not a fieldMouse anymore)
  → add all primals (now it's a NUCLEUS)
```

The boundary is clear: **if biomeOS is running, it's a niche. If not, it's a
fieldMouse.** This is the defining distinction. fieldMouse is sovereign at the
atomic level. Niches are sovereign at the composition level.
