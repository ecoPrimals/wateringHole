# Primal Responsibility Matrix — Cross-Primal Concern Ownership

**Date:** March 31, 2026
**Source:** ludoSpring V35.3 ecosystem evolution review + soft overstep audit; **V37.1 live plasmidBin gap matrix** (95/141 = 67.4%); primalSpring Phase 23f composition decomposition (7 subsystems, 32 gaps); toadStool S169 overstep cleanup (-10,659 lines)
**Purpose:** Define which primal OWNS each concern domain, which primals should DELEGATE, and where OVERSTEP has been identified. This matrix governs boundary evolution and informs deploy graph design.
**Note:** coralReef/glowplug dispatch boundary is deferred — actively in GPU development. toadStool S169 removed 30+ overstepping methods (Squirrel AI, coralReef shader compile, biomeOS discovery/deploy, songBird HTTP).

---

## Atomic Compositions (reference)

| Composition | Members | Purpose |
|-------------|---------|---------|
| **Tower Atomic** | bearDog + songBird | Security + Network foundation |
| **Node Atomic** | Tower + toadStool (+ barraCuda for math, coralReef for shader compilation) | Adds compute/hardware dispatch |
| **Nest Atomic** | Tower + nestGate | Adds storage/permanence |
| **NUCLEUS Complete** | Tower + Node + Nest + Squirrel | Full deployment: all 3 atomics + AI |
| **Meta-tier** | biomeOS, Squirrel, petalTongue | Orchestration, AI, Visualization — interact with and extend all atomics, not bound to any single one |

---

## Concern Matrix

Legend:
- **OWNS** — This primal is the canonical provider for this concern
- **DELEGATES** — This primal should call the owner via IPC for this concern
- **OVERSTEP** — This primal currently implements this concern locally but should delegate
- **EXTENDS** — Meta-tier primal that augments this concern across all atomics
- **N/A** — Not relevant to this primal
- **(deferred)** — Boundary under active development, not yet adjudicated

| Concern | bearDog | songBird | nestGate | toadStool | coralReef | barraCuda | biomeOS | Squirrel | petalTongue | rhizoCrypt | loamSpine | sweetGrass |
|---------|---------|----------|----------|-----------|-----------|-----------|---------|----------|-------------|------------|-----------|------------|
| **Crypto / Signing** | **OWNS** | OVERSTEP | OVERSTEP | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Network / Transport** | N/A | **OWNS** | OVERSTEP | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Discovery / Registry** | OVERSTEP | DELEGATES | OVERSTEP | ~~OVERSTEP~~ **RESOLVED (S169)** | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A |
| **Storage / Permanence** | N/A | OVERSTEP | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **AI / MCP** | OVERSTEP | N/A | OVERSTEP | ~~OVERSTEP~~ **RESOLVED (S169)** | N/A | N/A | N/A | **OWNS** / EXTENDS | N/A | N/A | N/A | N/A |
| **Compute / GPU dispatch** | N/A | N/A | N/A | **OWNS** | (deferred) | DELEGATES | N/A | N/A | N/A | N/A | N/A | N/A |
| **Shader Compilation** | N/A | N/A | N/A | DELEGATES | **OWNS** (deferred) | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Math / Numerical** | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A |
| **Orchestration** | N/A | N/A | OVERSTEP | ~~OVERSTEP~~ **RESOLVED (S169)** | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A |
| **Visualization** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** / EXTENDS | N/A | N/A | N/A |
| **Hardware Inventory** | N/A | N/A | N/A | **OWNS** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **DAG / Provenance** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A | N/A |
| **Ledger / History** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** | N/A |
| **Attribution** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | **OWNS** |
| **Capability Registration** | DELEGATES | DELEGATES | DELEGATES | DELEGATES | DELEGATES | DELEGATES | **OWNS** | DELEGATES | DELEGATES | **GAP** (RC-01) | **GAP** (LS-03) | DELEGATES |

---

## Overstep Detail by Primal

### nestGate (ancestor primal — most overstep)

As the oldest primal, nestGate accumulated functionality that now belongs to specialized primals.

| Overstep Area | Crate / Module | Dependencies to Shed | Delegate To |
|--------------|----------------|---------------------|-------------|
| **Crypto** | `nestgate-security` | `aes-gcm`, `argon2`, `ed25519-dalek`, `hmac`, `sha2`, `md5`, JWT, certificates | bearDog via `crypto.*` IPC |
| **Discovery** | `nestgate-discovery` | mDNS, Consul, K8s discovery, capability/service/network discovery | biomeOS Neural API + songBird |
| **Network** | `nestgate-network` | `axum`, `tower`, `reqwest`, `rustls`, load balancer, routing, QoS, HTTP server | songBird via `network.*` IPC |
| **AI / MCP** | `nestgate-mcp` | MCP protocol integration | Squirrel via biomeOS Neural API |
| **Orchestration** | `nestgate-automation` | "Intelligent automation and ecosystem integration" | biomeOS Neural API graph execution |
| **ecoBin violation** | `nestgate-installer` | `reqwest` + `rustls` pulls `aws-lc-rs` (C dependency) | Remove C dep; use songBird for HTTP |

**Priority:** High — nestGate's core domain is storage/permanence (Nest Atomic). Crypto, discovery, network, and orchestration should all flow through Tower Atomic peers (bearDog, songBird) and biomeOS.

### bearDog

| Overstep Area | Module | Delegate To |
|--------------|--------|-------------|
| **HTTP REST API** | `beardog-integration` | songBird (network transport is songBird's domain) |
| **TCP JSON-RPC server** | `beardog-ipc` | Standard UDS JSON-RPC per wateringHole conventions |
| **mDNS/DNS-SD discovery** | `beardog-discovery` | biomeOS Neural API capability registration |
| **AI-driven optimization** | `beardog-utils/ai_optimization` | Squirrel via biomeOS |
| **Deployment orchestration** | `beardog-deploy`, `beardog-production` | biomeOS deploy graphs |

**Priority:** Medium — bearDog's core domain is crypto/signing. Transport, discovery, AI, and deployment are outside its boundary.

### songBird

| Overstep Area | Module / Dep | Status | Delegate To |
|--------------|-------------|--------|-------------|
| **Application crypto** | JWT, checkpoints, discovery, rendezvous | ✅ Delegated (Wave 89) | bearDog via `crypto.hmac.sha256`, `crypto.sha256`, `crypto.aead_encrypt/decrypt` — local fallback + `tracing::warn!` |
| **TLS record crypto** | `songbird-tls` record layer | ✅ Delegated (Wave 89) | bearDog via `crypto.aead_encrypt/decrypt` — returns `CryptoUnavailable` when bearDog absent |
| **TLS handshake crypto** | `sha2` in TLS transcript | ⚡ Kept | TLS-internal (acceptable per matrix guidance) |
| **Transport cert gen** | `ed25519-dalek` in QUIC/TLS cert gen | ⚡ Kept | Transport bootstrap (acceptable per matrix guidance) |
| **Embedded persistence** | `sled` database in orchestrator | ⏳ Pending | nestGate via `storage.*` IPC (blocked on nestGate storage API) |

**Priority:** Low — application-level crypto now delegates to bearDog. TLS internals retain local crypto deps (acceptable). sled persistence pending nestGate.

### toadStool

**S169 (March 31, 2026) — MAJOR OVERSTEP CLEANUP COMPLETED**

toadStool S169 removed 30+ overstepping JSON-RPC methods and shed 10,659 lines.
The following overstep areas are now **RESOLVED**:

| Overstep Area | S169 Status | What Happened |
|--------------|-------------|---------------|
| ~~Discovery relay~~ | **RESOLVED** | `science_domains.rs` forwarding removed. Primals register with biomeOS directly. |
| ~~Shader compile proxy~~ | **RESOLVED** | `shader.compile.*` methods removed. Springs call coralReef directly. `shader.dispatch` kept (legitimate). |
| ~~AI / Ollama inference~~ | **RESOLVED** | `inference.*` methods + Ollama handler removed. Springs route to Squirrel. |
| ~~HTTP server~~ | **RESOLVED** | axum/tower HTTP stack removed. Daemon now uses pure JSON-RPC over UDS. |
| ~~Network~~ | **RESOLVED** | `hyper` in `toadstool-distributed` removed. |
| ~~barraCuda capability advertising~~ | **RESOLVED** | No longer advertises math capabilities for barraCuda. |
| ~~Python FFI~~ | **RESOLVED** | `pyo3`/`pyo3-asyncio` removed from workspace. ecoBin compliant. |
| ~~Science domain relay~~ | **RESOLVED** | `science.compute.*`, `science.gpu.*`, `ecology.*` relay methods removed. |

**Remaining items:**

| Overstep Area | Crate / Module | Delegate To |
|--------------|----------------|-------------|
| **coralReef discovery** | Internal hardcoded URL | Needs socket directory scan or capability.discover (gap TS-01) |
| **Security sandbox** | `toadstool-security-sandbox` | bearDog (if crypto) or OS-level sandboxing |

**Priority:** Low — S169 resolved the major overstep. Only coralReef discovery (TS-01) and sandbox boundary remain.

### rhizoCrypt (CRITICAL gaps)

**Core domain**: DAG provenance — ephemeral workspace, session-scoped directed acyclic graphs, Merkle proofs.

| Gap | Severity | Impact | Fix Path |
|-----|----------|--------|----------|
| **RC-01: TCP-only transport** | CRITICAL | Blocks 4 ludoSpring experiments (+9 checks), blocks all Trio compositions via UDS | Add `--unix [PATH]` CLI flag, default `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`. Follow BearDog/sweetGrass pattern. |
| Non-conformant wire framing | High | HTTP-wrapped JSON-RPC only (Axum). Raw newline client gets 400. | Add raw newline TCP JSON-RPC listener alongside Axum. |

**No overstep identified** — rhizoCrypt is focused on its DAG domain.

### loamSpine (CRITICAL gap)

**Core domain**: Immutable linear history — append-only ledger, inclusion proofs, certificates.

| Gap | Severity | Impact | Fix Path |
|-----|----------|--------|----------|
| **LS-03: Startup panic** | CRITICAL | Cannot start at all. Blocks exp095 (+6 checks), blocks all Trio compositions. | Replace `block_on()` with `spawn` in `infant_discovery.rs:233`. The async context already exists. |
| Socket path unknown | High | Crashes before socket bind, so path conformance untested. | Once panic is fixed, ensure `$XDG_RUNTIME_DIR/biomeos/loamspine.sock`. |

**No overstep identified** — loamSpine is focused on its ledger domain.

### sweetGrass

**Core domain**: Semantic attribution — content braids, contribution tracking, convergence.

**No overstep identified, no critical gaps.** UDS conformant at `/run/user/1000/biomeos/sweetgrass.sock`.
Missing: `--port` flag (uses `--http-address` instead), domain symlink.

### barraCuda

**Core domain**: Math / numerical — tensor operations, activation functions, statistics, noise, special functions.

| Gap | Severity | Impact | Fix Path |
|-----|----------|--------|----------|
| **BC-01: Fitts formula** | High | Returns Welford `log2(D/W)` instead of Shannon `log2(2D/W+1)`. 4 checks fail in ludoSpring exp089. | Add `variant` parameter (default: `"shannon"`). |
| **BC-02: Hick formula** | Medium | Uses `log2(n+1)` (includes no-choice) vs standard `log2(n)`. | Add `include_no_choice` parameter (default: `false`). |
| **BC-03: Perlin3D lattice** | Medium | `perlin3d(0,0,0)` returns -0.11 instead of 0. Breaks invariant. | Fix gradient interpolation at integer lattice boundaries. |
| **BC-04: No plasmidBin binary** | Medium | Must be started from source build. | Publish ecoBin to `plasmidBin/barracuda/`. |

**No overstep identified** — barraCuda owns math exclusively.

### coralReef (deferred)

coralReef and its `glowplug` engine are actively under GPU development. The dispatch boundary between coralReef (shader compilation) and toadStool (hardware dispatch) is not yet finalized.

**Known items** (not yet adjudicated):
- Ships a full sovereign GPU driver and dispatch stack (`coral-driver`, `coral-gpu`)
- Direct device access and lifecycle management (may overlap toadStool)
- `coral-glowplug` and `coral-ember` implement execution as well as compilation

**Action:** Revisit once coralReef GPU development stabilizes. The compile-vs-dispatch boundary will be clarified by coralReef + toadStool teams.

---

## Guidance for Deploy Graph Design

When composing primals via biomeOS deploy graphs:

1. **Crypto operations** → route through `crypto.*` capability (bearDog)
2. **Network transport** → route through `network.*` capability (songBird)
3. **Storage** → route through `storage.*` capability (nestGate)
4. **Math/Tensor** → route through `math.*`/`tensor.*` capability (barraCuda)
5. **GPU dispatch** → route through `compute.*` capability (toadStool)
6. **Shader compilation** → route through `shader.*` capability (coralReef)
7. **AI/ML** → route through `ai.*` capability (Squirrel)
8. **Visualization** → route through `viz.*` capability (petalTongue)
9. **Discovery** → biomeOS Neural API handles capability registration and routing; primals register on startup, not via peer relay

Deploy graphs should **never** route a concern to a primal that is listed as OVERSTEP for that concern. If the owning primal is unavailable, the graph node should use `required = false` for graceful degradation rather than falling back to an overstepping primal.

---

## Evolution Actions

### Tier 1 — Critical (blocks live compositions)

| Primal | Action | Impact on Deploy Graphs |
|--------|--------|------------------------|
| **rhizoCrypt** | Add `--unix` UDS socket (RC-01). Add raw newline TCP framing. | Unblocks provenance_pipeline.toml, session_provenance.toml, 4 ludoSpring experiments (+9 checks). |
| **loamSpine** | Fix `block_on()` startup panic (LS-03). Ensure standard socket path. | Unblocks provenance_pipeline.toml, exp095/096 (+6 checks). Must start before session graphs can deploy. |
| **biomeOS** | Fix capability registration timing (BM-04): `capability.list` only shows 5 self-capabilities, misses all external primals. Add `topology.rescan` or lazy discovery on `capability.call` miss. Fix probe response format (BM-05). | Unblocks 3 checks. Critical for all multi-primal composition graphs — currently primals starting after biomeOS are invisible to Neural API routing. |
| **bearDog** | Default `FAMILY_ID` to `standalone` when unset. Add `--port` alias for `--listen`. | Blocks standalone startup in any graph without env setup. |

### Tier 2 — High (needed for full composition validation)

| Primal | Action | Impact on Deploy Graphs |
|--------|--------|------------------------|
| **nestGate** | Shed crypto → bearDog IPC, shed discovery → biomeOS, shed network → songBird, shed MCP → Squirrel, fix `aws-lc-rs` C dep. Wire `--port` to TCP bind. | Graphs currently routing storage through nestGate are fine; crypto/discovery/network nodes need rerouting. |
| **barraCuda** | Fix Fitts formula (BC-01, add `variant` param), Hick formula (BC-02, add `include_no_choice` param), Perlin3D lattice (BC-03), publish ecoBin to plasmidBin (BC-04). | Fixes 4 ludoSpring checks. Needed for accurate game science validation. |
| **toadStool** | Fix coralReef discovery (TS-01): stop using hardcoded URL, use socket scan or `capability.discover`. Wire `--port` to server bind. | S169 resolved major overstep. Remaining items are discovery + TCP. |
| **petalTongue** | Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock` (PT-01). Add `--port` flag. Add WebSocket push for real-time dashboard. | Blocks standard discovery of render subsystem. Current non-standard path requires custom socket resolution. |
| **Squirrel** | Add filesystem socket alongside abstract (SQ-01). Add `health.liveness`/`health.readiness`/`health.check`. Wire Ollama provider routing. | Abstract-only socket invisible to `readdir()`. Blocks standard composition discovery. |

### Tier 3 — Medium (improves ecosystem coherence)

| Primal | Action | Impact on Deploy Graphs |
|--------|--------|------------------------|
| **bearDog** | Shed HTTP REST, standardize UDS JSON-RPC, shed mDNS discovery → biomeOS, shed AI optimization → Squirrel | Transport nodes should use songBird for HTTP. |
| **songBird** | ✅ App crypto delegated to bearDog (JWT, checkpoint, discovery, rendezvous, TLS record); ✅ `health.liveness/readiness/check` canonical names wired; ⏳ sled → nestGate pending nestGate API. | Minimal graph impact — songBird's network role is correct; lowest debt primal. |
| **sweetGrass** | Add `--port` flag (alias for port portion of `--http-address`). Add domain symlink. | Low impact — already conformant on UDS. |
| **coralReef** | ~~Add `--port` for raw newline TCP~~ **RESOLVED** (Iter 70h). ~~Domain symlinks~~ **RESOLVED** (`shader.sock` + `device.sock`). Compile-vs-dispatch boundary documented (`DISPATCH_BOUNDARY.md`); `device.dispatch` marked transitional in `capabilities.list`. | GPU development ongoing; dispatch handoff to toadStool deferred. |

---

## Cross-Referencing Composition Gaps

The responsibility matrix directly informs which gaps block specific compositions.
See `primalSpring/docs/PRIMAL_GAPS.md` for the full 32-gap registry.

| Composition | Blocked By | Gap ID |
|-------------|-----------|--------|
| C1: Render Standalone | petalTongue socket path, WebSocket push | PT-01, PT-02 |
| C2: Narration AI | Squirrel Ollama routing, filesystem socket | SQ-01, SQ-02 |
| C3: Session | esotericWebb scene format | EW-03 |
| C5: Persistence | nestGate overstep (crypto/network shed) | — |
| C6: Proprioception | petalTongue proprioception events | PT-05 |
| C7: Full Interactive | biomeOS capability registration (BM-04) | BM-04 |
| Provenance Pipeline | rhizoCrypt UDS (RC-01), loamSpine panic (LS-03) | RC-01, LS-03 |
| Game Science | barraCuda formulas (BC-01/02/03) | BC-01, BC-02, BC-03 |
| Session Provenance | RC-01, LS-03 | RC-01, LS-03 |

### Projected Composition Health After Resolution

If Tier 1 + Tier 2 gaps are resolved:
- **67.4% → 92.2%** (ludoSpring live validation: 95/141 → ~130/141)
- **Compositions C1-C7**: All 7 compositions reach full pass
- **Provenance trio**: Unblocked for session provenance and RootPulse workflows

---

## Versioning

This matrix will be updated as primals evolve and shed overstep. Each update should reference the ludoSpring composition experiment results that motivated it.

- **V1 (March 30, 2026)**: Initial matrix from ludoSpring V35.3 ecosystem evolution review
- **V2 (March 31, 2026)**: Expanded with primalSpring Phase 23f composition findings (32 gaps), ludoSpring V37.1 plasmidBin gap matrix, toadStool S169 overstep resolution, added rhizoCrypt/loamSpine/sweetGrass/barraCuda sections, tiered evolution actions, composition cross-references
