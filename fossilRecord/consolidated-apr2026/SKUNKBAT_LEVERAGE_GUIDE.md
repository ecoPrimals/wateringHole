<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# skunkBat Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: April 2026
**Primal**: skunkBat v0.1.0 (Edition 2024)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how skunkBat can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers.
Each primal in the ecosystem produces an equivalent guide. Together,
these guides form a combinatorial recipe book for emergent behaviors.

skunkBat provides **composable anomaly detection** through five primitive
domains: baseline profiling, metadata analysis, graduated response,
lineage challenge, and health sensing. These are useful far beyond
security — any observable metric from any primal can be baselined and
monitored for anomalies.

**Philosophy**: Know yourself, not your enemy. Learn what "self" looks
like (via BearDog lineage) and flag everything else. Metadata only —
content inspection is structurally impossible.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}` per the Semantic Method Naming
Standard.

### Baseline Domain

| Method | What It Does |
|--------|-------------|
| `baseline.observe` | Record a metric observation into the rolling window |
| `baseline.query` | Retrieve current baseline statistics (mean, sigma, percentiles) |
| `baseline.anomaly` | Check a value against the baseline, return deviation |
| `baseline.reset` | Clear the rolling window and start fresh |

### Metadata Domain

| Method | What It Does |
|--------|-------------|
| `metadata.classify` | Classify a connection's metadata pattern |
| `metadata.fingerprint` | Generate a metadata fingerprint for a connection |

### Response Domain

| Method | What It Does |
|--------|-------------|
| `response.evaluate` | Given evidence, recommend a response level |
| `response.escalate` | Move an entity to a higher response level |
| `response.deescalate` | Move an entity to a lower response level |
| `response.status` | Query current response level for an entity |

### Lineage Domain

| Method | What It Does |
|--------|-------------|
| `lineage.challenge` | Challenge an entity to present lineage proof |
| `lineage.verify` | Verify a presented lineage proof (delegates to BearDog) |

### Health Domain

| Method | What It Does |
|--------|-------------|
| `health.system` | Current system load (CPU, memory) — cross-platform |
| `health.network` | Network connection summary |
| `health.resource` | Resource utilization breakdown |
| `health.check` | Service health with status, version, uptime |

### Standard

| Method | What It Does |
|--------|-------------|
| `capability.list` | List all capabilities with per-method cost and dependency hints |
| `identity.get` | Return primal identity, version, bond type |

**Transport**: JSON-RPC 2.0 over TCP and UDS. BTSP Phase 2 with first-byte
peek (`{` → plain JSON-RPC for biomeOS composition bypass).

---

## 1. skunkBat Standalone

These patterns use skunkBat alone — no other primals required.

### 1.1 General-Purpose Anomaly Detection

The baseline profiler works for ANY time-series, not just security metrics.
Feed metric observations, let the rolling window learn "normal," then
check values for anomalies.

```
baseline.observe { domain: "compile_time", value: 142.0 }
baseline.observe { domain: "compile_time", value: 138.0 }
... (learning phase — configurable window size)

baseline.anomaly { domain: "compile_time", value: 14200.0 }
  → { deviation: 8.2, sigma: 17.3, assessment: "critical" }

baseline.query { domain: "compile_time" }
  → { mean: 140.0, sigma: 2.1, p95: 143.8, observations: 1024 }
```

**Spring applications**:

| Spring | What to Baseline |
|--------|-----------------|
| hotSpring | Lattice QCD iteration times, EOS parameter sweep rates |
| neuralSpring | Training loss convergence rates, gradient norms |
| wetSpring | Pipeline stage durations, sequence quality distributions |
| airSpring | ET0 computation times, sensor reading frequencies |
| groundSpring | Calibration chain latencies, measurement drift rates |
| healthSpring | PK/PD model runtimes, clinical pipeline throughputs |
| ludoSpring | Frame render times, player interaction rates, DDA adjustment frequencies |
| primalSpring | Primal test suite runtimes, compilation times across ecosystem |

### 1.2 Graduated Response as Workflow Engine

The response state machine works for any progressive action sequence:

| Security Use | General Use |
|-------------|-------------|
| Monitor → Warn → Throttle → Quarantine → Block | Observe → Provision → Scale → Throttle → Shed |
| Threat escalation | Resource scaling |
| Intrusion response | User onboarding |
| Federation quarantine | Experiment gating |

```
response.evaluate { evidence: { deviation: 3.2, domain: "gpu_util" } }
  → { level: "warn", confidence: 0.7 }

response.escalate { entity: "node-x", from: "warn", to: "throttle" }
  → { acknowledged: true }

response.status { entity: "node-x" }
  → { level: "throttle", since: "2026-04-16T10:30:00Z", escalation_count: 1 }
```

### 1.3 Cross-Platform Health Sensing

`health.system` provides real system load via `/proc/loadavg` (Linux) or
`uptime` (fallback). Any primal or spring can call it for scheduling
decisions without implementing platform detection.

```
health.system {}
  → { load_1m: 0.42, load_5m: 0.38, cpu_count: 8 }

health.resource {}
  → { cpu_pct: 42.0, memory_pct: 67.2, disk_pct: 31.0 }
```

---

## 2. Named Trio Compositions

### 2.1 Security Trio (skunkBat + BearDog + Songbird)

The core security composition. BearDog provides genetic identity (the MHC
system). Songbird provides federation metadata (the lymphatic network).
skunkBat provides self/non-self discrimination (the thymus).

```
                  BearDog
                (identity)
                    │
         lineage.verify / btsp.session.verify
                    │
    ┌───────────────▼───────────────┐
    │         skunkBat              │
    │   (thymic selection)          │
    │   positive + negative select  │
    │   → mature detector pool      │
    └───────────────┬───────────────┘
                    │
         baseline.observe / baseline.anomaly
                    │
                    ▼
                 Songbird
              (federation)
         peer metadata, topology
```

**Pattern**: BearDog defines "self" (family roster). Songbird provides
the federation graph. skunkBat trains detectors against self and deploys
them to monitor the federation for non-self entities.

**Spring applications**: Any spring running federated workloads. hotSpring
distributing QCD across the mesh. neuralSpring federated model training.
wetSpring multi-site microbiome studies.

### 2.2 Sovereign Integrity Trio (skunkBat + sweetGrass + LoamSpine)

Anomaly detection with full provenance and permanence.

```
skunkBat detects anomaly
    → sweetGrass records anomaly marker in attribution braid
    → LoamSpine commits anomaly record permanently
```

Every security event becomes a signed, attributed, permanently committed
record. Auditable security history with cryptographic provenance.

---

## 3. skunkBat + Other Primals

### 3.1 skunkBat + BearDog: Thymic Selection

The foundational composition. BearDog provides the genetic identity
system; skunkBat performs thymic education against it.

```
lineage.challenge { peer_id: "did:eco:unknown" }
  → BearDog: btsp.session.verify
  → { verified: false }
  → response.evaluate → Quarantine

lineage.challenge { peer_id: "did:eco:family-member" }
  → BearDog: btsp.session.verify
  → { verified: true, bond_type: "covalent" }
  → pass (self — never flag)
```

**Novel**: Thymic probe generation — pseudorandom detectors trained against
BearDog's family roster. See `THYMIC_SELECTION_SPEC.md`.

### 3.2 skunkBat + Songbird: Federation Health Monitor

```
baseline.observe { domain: "peer_msg_rate", value: messages_per_sec }
baseline.observe { domain: "peer_latency", value: avg_latency_ms }

baseline.anomaly { domain: "peer_msg_rate", value: 50x_normal }
  → { deviation: 12.0, pattern: "flood_or_spoof" }
response.evaluate → Quarantine (isolate peer, maintain mesh)
```

**Applications**: Detecting compromised federation peers, DDoS via
federation channel, peer spoofing.

### 3.3 skunkBat + ToadStool: Compute Resource Guardian

```
baseline.observe { domain: "gpu_util", value: utilization_pct }
baseline.observe { domain: "dispatch_rate", value: dispatches_per_sec }

baseline.anomaly { domain: "gpu_util", value: 100.0 for 2_hours }
  → { pattern: "unscheduled_compute" }
response.evaluate → Warn (alert biomeOS)
```

**Applications**: Cryptomining detection, runaway workloads, hardware
failure early warning, cost overrun prevention.

### 3.4 skunkBat + NestGate: Storage Exfiltration Detection

```
baseline.observe { domain: "storage_get_rate", value: gets_per_sec }
baseline.observe { domain: "bytes_out", value: total_bytes }

baseline.anomaly { domain: "storage_get_rate", value: bulk_sequential }
  → { pattern: "bulk_exfiltration" }
response.evaluate → Quarantine (pause gets, alert owner)
```

**Applications**: Data exfiltration detection, backup verification (expected
bulk reads vs unexpected), storage abuse.

### 3.5 skunkBat + coralReef: Compiler Sensing

Shader compilation has observable metadata patterns: compile time
distributions, input/output size ratios, instruction mix fingerprints.

```
baseline.observe { domain: "shader_compile_ms", value: compile_time }
baseline.observe { domain: "shader_ratio", value: spirv_bytes / wgsl_bytes }
baseline.observe { domain: "instruction_count", value: ops }

baseline.anomaly { domain: "shader_compile_ms", value: 100x_normal }
  → { deviation: 6.1, pattern: "resource_exhaustion" }
response.evaluate → Throttle (rate-limit compilation requests)
```

**Applications**: Compiler abuse detection (pathological shaders exhausting
GPU compile resources), compilation regression detection, NVVM bypass
integrity.

### 3.6 skunkBat + barraCuda: Kernel Execution Guardian

```
baseline.observe { domain: "kernel_runtime_ms", value: execution_time }
baseline.observe { domain: "kernel_memory_mb", value: vram_allocated }

baseline.anomaly { domain: "kernel_memory_mb", value: 10x_normal }
  → { pattern: "memory_abuse" }
response.evaluate → Throttle
```

**Applications**: VRAM exhaustion prevention, kernel timing attacks,
abnormal memory allocation patterns.

### 3.7 skunkBat + rhizoCrypt: DAG Session Anomaly Monitoring

```
baseline.observe { domain: "vertex_rate", value: vertices_per_min }
baseline.observe { domain: "agent_count", value: unique_agents }

baseline.anomaly { domain: "vertex_rate", value: 10x_spike }
  → { deviation: 8.2, source: "unknown_agent" }
response.evaluate → Quarantine (isolate session for review)
```

**Applications**: Unauthorized DAG modifications in clinical data
(healthSpring), automation errors in experiment pipelines (any spring),
injected vertices in collaborative sessions.

### 3.8 skunkBat + LoamSpine: Ledger Integrity Sentinel

```
baseline.observe { domain: "commit_rate", value: commits_per_hour }
baseline.observe { domain: "commit_size", value: avg_payload_bytes }

baseline.anomaly { domain: "commit_rate", value: 1000x_normal }
  → { pattern: "ledger_flood" }
response.evaluate → Block (with user authority)
```

**Applications**: Ledger spam detection (storage exhaustion via flood),
commit pattern verification, permanence abuse prevention.

### 3.9 skunkBat + sweetGrass: Anomaly Markers in Braids

When skunkBat detects an anomaly during a provenance-tracked session,
the anomaly assessment becomes metadata in sweetGrass attribution braids.

```
sweetGrass: provenance.create_braid {
    session_id,
    anomaly_markers: [
        { detector: "skunkbat", deviation: 4.2, domain: "vertex_rate", time: "..." }
    ]
}
```

**Applications**: Auditable anomaly history in scientific provenance
chains, regulatory compliance (clinical trials, environmental monitoring),
fair attribution that includes integrity assessments.

### 3.10 skunkBat + Squirrel: AI Behavior Profiling

```
baseline.observe { domain: "inference_rate", value: requests_per_min }
baseline.observe { domain: "token_volume", value: avg_tokens_per_request }
baseline.observe { domain: "model_distribution", value: model_id_entropy }

baseline.anomaly { domain: "inference_rate", value: 100x_normal }
  → { pattern: "api_abuse" }
response.evaluate → Throttle
```

**Applications**: API abuse detection, unauthorized model access,
cost-control guardrails, prompt injection detection (anomalous token
patterns).

### 3.11 skunkBat + petalTongue: Anomaly Dashboards

petalTongue renders skunkBat's baseline and anomaly data as live
interactive visualizations.

```
baseline.query { domain: "all" }
  → { domains: [{ name: "gpu_util", mean: 42, sigma: 8.3, ... }, ...] }
response.status { entity: "all" }
  → { entities: [{ id: "node-x", level: "monitor", ... }, ...] }
```

**Applications**: Security operations center (SOC) dashboard, ecosystem
health overview, spring experiment monitoring, real-time anomaly alerting.

### 3.12 skunkBat + biomeOS: Alert Routing and Response Coordination

biomeOS receives `response.evaluate` outputs and coordinates ecosystem-wide
response via the Neural API. skunkBat suggests; biomeOS orchestrates.

```
skunkBat: response.evaluate → { level: "quarantine", entity: "peer-x" }
biomeOS:  Neural API routes quarantine to Songbird (federation isolation)
          + NestGate (storage access pause) + ToadStool (compute suspension)
```

---

## 4. Novel Multi-Primal Compositions

### 4.1 Provenance-Backed Anomaly Chain

**Primals**: skunkBat + rhizoCrypt + LoamSpine + sweetGrass + BearDog

Every anomaly detection event becomes a signed, attributed, permanently
committed record in the provenance chain.

```
1. skunkBat:   baseline.anomaly → detection event
2. BearDog:    crypto.sign { data: detection_hash }
3. rhizoCrypt: dag.append_vertex { payload: signed_detection }
4. rhizoCrypt: dag.dehydrate → summary
5. LoamSpine:  commit.session { dehydrated_summary }
6. sweetGrass: provenance.create_braid { session_id, anomaly_markers }
```

Auditable, tamper-evident security history. Every anomaly traceable from
detection through permanent record.

### 4.2 Defended Inference Trio

**Primals**: skunkBat + Squirrel + BearDog

AI inference requests are lineage-verified (BearDog) and behaviorally
profiled (skunkBat). Only family members get inference access. Behavioral
anomalies trigger throttling before resource exhaustion.

```
1. BearDog:    lineage.verify { peer_id }   → family confirmed
2. skunkBat:   baseline.observe { inference_rate }
3. Squirrel:   ai.inference { prompt }       → result
4. skunkBat:   baseline.anomaly check (continuous)
5. If anomaly: response.evaluate → Throttle before Squirrel is overwhelmed
```

### 4.3 Sovereign Compute Integrity Pipeline

**Primals**: skunkBat + barraCuda + coralReef + ToadStool + sweetGrass

Full pipeline monitoring from shader authoring through compilation through
dispatch through result, with anomaly markers in provenance braids.

```
1. barraCuda:  Author WGSL kernel
2. skunkBat:   baseline.observe { domain: "kernel_complexity", value: op_count }
3. coralReef:  shader.compile → SPIR-V
4. skunkBat:   baseline.observe { domain: "compile_time", value: ms }
5. ToadStool:  compute.submit → GPU dispatch
6. skunkBat:   baseline.observe { domain: "dispatch_time", value: ms }
7. sweetGrass: provenance.create_braid { pipeline steps + anomaly markers }
```

Every stage monitored for anomalies. Hardware fingerprints captured.
Reproducibility provable. Integrity assessable.

### 4.4 Federated Experiment Guardian

**Primals**: skunkBat + Songbird + rhizoCrypt + BearDog

Multi-site experiments (clinical trials, weather monitoring, federated
ML) use skunkBat to monitor federation health and session integrity
simultaneously.

```
Site A: rhizoCrypt session (primary) → vertices accumulate
Site B: rhizoCrypt mirror slice → synchronized replica
skunkBat @ each site:
  baseline.observe { vertex_rate, agent_count, peer_latency }
  Cross-site anomaly: Site B vertex rate diverges from Site A
  → { pattern: "mirror_desync" } → Warn
```

---

## 5. Spring Recipe Cards

### hotSpring

- Baseline QCD iteration times per lattice size
- Detect anomalous EOS parameter sweep durations (hardware failure)
- Monitor GPU utilization during long-running Yukawa calculations
- Anomaly markers in lattice QCD provenance braids

### neuralSpring

- Baseline training loss convergence rates per model architecture
- Detect gradient explosion/vanishing via anomalous norm patterns
- AI inference profiling for multi-model routing efficiency
- Federation health monitoring for distributed training

### wetSpring

- Baseline 16S rRNA pipeline stage durations
- Detect anomalous community diversity shifts (contamination signal)
- Multi-GPU sequence alignment resource guardian
- HIPAA compliance: anomaly markers in clinical microbiome braids

### airSpring

- Baseline ET0 computation times per station
- Detect sensor dropout patterns (timing anomalies)
- Irrigation model resource guardian (seasonal compute spikes)
- Federation health for multi-station weather networks

### groundSpring

- Baseline calibration chain latencies per instrument
- Detect measurement drift (gradual baseline shift)
- Cross-vendor ULP certification anomaly detection
- Sensor network federation health

### healthSpring

- Baseline PK/PD model runtimes per patient cohort
- Detect anomalous dosing calculation patterns
- Clinical trial federation guardian (multi-site integrity)
- HIPAA-compliant anomaly audit trail via provenance chain

### ludoSpring

- Baseline frame render times per scene complexity
- Detect DDA adjustment anomalies (over-tuning)
- Player interaction rate profiling (bot detection)
- Multi-GPU game asset pipeline guardian

### primalSpring

- Baseline primal test suite runtimes across ecosystem
- Detect compilation time regressions per primal
- Cross-primal CI health monitoring
- Ecosystem-wide coverage trend anomaly detection

---

## 6. What skunkBat Does NOT Do

| Concern | Who Handles It | skunkBat's Role |
|---------|---------------|-----------------|
| Cryptography | BearDog | Consumes lineage verification |
| Networking / TLS | Songbird | Monitors federation metadata |
| Storage | NestGate | Monitors access patterns |
| Compute dispatch | ToadStool | Monitors resource patterns |
| Shader compilation | coralReef | Monitors compilation patterns |
| GPU kernels | barraCuda | Monitors kernel execution patterns |
| Permanence | LoamSpine | Monitors commit patterns |
| Attribution | sweetGrass | Provides anomaly markers for braids |
| Ephemeral state | rhizoCrypt | Monitors DAG session patterns |
| AI inference | Squirrel | Monitors inference patterns |
| Visualization | petalTongue | Provides anomaly data for dashboards |
| Orchestration | biomeOS | Receives alerts, coordinates response |
| Scaffolding | sourDough | No interaction |
| **Content inspection** | **Nobody** | **Architecturally impossible** |

skunkBat observes metadata from every primal composition but never touches
content. It is the immune system watching vital signs without reading mail.

---

## References

- `skunkBat/specs/THYMIC_SELECTION_SPEC.md` — Thymic model specification
- `skunkBat/specs/COMPOSABLE_PRIMITIVES_SPEC.md` — Primitive decomposition
- `skunkBat/specs/THREAT_DETECTION_SPEC.md` — Core threat detection (5 types)
- `skunkBat/RECONNAISSANCE_NOT_SURVEILLANCE.md` — Ethical framework
- `wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming
- `gen3/primals/12_skunkbat.md` — Primal profile
- `gen3/primals/INTERACTIONS.md` — Interaction matrix
