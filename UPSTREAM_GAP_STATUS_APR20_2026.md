# Upstream Gap Status — April 2026 (Updated)

**Source**: primalSpring Phase 45 gap registry (`docs/PRIMAL_GAPS.md`)
**Context**: Post-pull review of barraCuda (Sprint 44c), NestGate (Session 43k), biomeOS (v3.08). Phase 45 gap #6 resolved. **Phase 45b**: BTSP escalation exposed 5 new upstream gaps — primals lack server-side BTSP handshake. **loamSpine BTSP gap RESOLVED (April 21); provider socket wiring fix (April 22).** Guidestone 162/166 (4 expected FAIL).

---

## Resolved This Sprint (30 items)

| Gap | Primal | Version | How |
|-----|--------|---------|-----|
| `inference.register_provider` wire method | Squirrel | alpha.49 | 5 wire tests, real handler path |
| Stable ecoBin binary | Squirrel | alpha.49 | 3.5MB static-pie, stripped, BLAKE3 |
| Ionic bond lifecycle (`crypto.ionic_bond.seal`) | BearDog | Wave 42 | propose→accept→seal, Ed25519, TTL |
| BTSP server endpoint (`btsp.server.*`) | BearDog | Wave 36 | 4 wire methods + session store |
| `health.check` accepts empty params | loamSpine | deep debt | `#[serde(default)]`, null→{} normalization |
| `EVENT_TYPE_REFERENCE.md` | rhizoCrypt | S40 | Canonical 27-variant spec |
| `capability.call` gate routing | biomeOS | v3.05 | Explicit error on unregistered gate |
| `--port` in api/nucleus modes | biomeOS | v3.05 | TCP alongside UDS for mobile |
| biomeOS DOWN during testing | biomeOS | v3.05 | Neural API co-launch in Nucleus Full |
| LD-10 BTSP guard line consumed | barraCuda | Sprint 42 | Replay consumed line |
| LD-05 TCP AddrInUse | barraCuda | Sprint 42 | Eliminated TCP sidecar in UDS mode |
| NG-08: Eliminate `ring` from production | NestGate | Session 43 | reqwest→ureq 3.3 + rustls-rustcrypto, pure Rust TLS |
| BC-07: `SovereignDevice` `Auto::new()` fallback | barraCuda | Sprint 41 | 3-tier: wgpu GPU → CPU → SovereignDevice IPC |
| BC-08: `cpu-shader` default-on | barraCuda | Sprint 40 | Default feature, ecoBin computes without wgpu |
| CR-01: `deny.toml` C/FFI ban list | coralReef | Iter 79 | ecoBin v3 ban, cudarc behind feature gate |
| Multi-stage ML pipeline `shader.compile.wgsl` | coralReef | Iter 80+ | 6 end-to-end tests, CompilationInfo IPC |
| Signed capability announcements (SA-01) | BearDog | Wave 45 | Ed25519 signed attestation on discover + register |
| `plasma_dispersion` feature-gate bug | barraCuda | Sprint 40 | Corrected to dual feature gate |
| `storage.retrieve` for large/streaming tensors | NestGate | Session 43h | `store_blob`, `retrieve_blob`, `retrieve_range`, `object.size` on isomorphic IPC |
| Cross-spring namespace isolation | NestGate | Session 43h | Optional `namespace` on all `storage.*`, `storage.namespaces.list` |
| Zero `Box<dyn Error>` in production | NestGate | Session 43k | Last `ConfigError::ParseError` typed; zero `async-trait` |
| `capability_registry.toml` + Wire L3 | NestGate | Session 43e | 12 capability groups, `consumed_capabilities`, `normalize_method()` |
| `tensor.batch.submit` (fused pipeline) | barraCuda | Sprint 42 Ph8 | 32nd JSON-RPC method; batch pre-validation |
| TCP bind-before-discovery | barraCuda | Sprint 42 Ph5 | `try_bind_tcp` / `serve_tcp_listener`; UDS mode no longer starts TCP |
| `TENSOR_WIRE_CONTRACT.md` response standardization | barraCuda | Sprint 42 | `{status, result_id, shape, elements}` for typed extractors |
| Zero C dependencies | biomeOS | v3.08 | `gethostname` → `rustix::system::uname()` |
| `graph.execute` cross-gate semantics | biomeOS | v3.07 | Aligns with `capability.call` gate semantics |
| `PrimalOperationExecutor` native async | biomeOS | v3.07 | Off `async_trait` to native RPITIT |
| `composition.health` mesh probing | biomeOS | v3.07 | Probes Songbird `mesh.status` |
| Large-file cleanup / test extraction | biomeOS | v3.06 | All production files <835 LOC |

---

## Remaining Open (13 items)

### Critical — BTSP Server Handshake Gaps (NEW — April 2026)

primalSpring's incremental BTSP escalation (Layer 1.5) exposed that 5 primals
do not implement the 4-step BTSP server handshake (ClientHello → ServerHello →
ChallengeResponse → HandshakeComplete) on their primary JSON-RPC sockets.
These primals **pass cleartext validation** and **seed fingerprint verification** —
their binaries are authentic. The gap is wire-level encrypted channel support.

| Gap | Owner | Behavior | Impact |
|-----|-------|----------|--------|
| **BTSP server on security socket** | BearDog | Treats `ClientHello` as invalid JSON-RPC → Parse error → connection close | Tower security not BTSP-authenticated |
| **BTSP server on discovery socket** | Songbird | HTTP-framed UDS, no BTSP listener | Tower discovery not BTSP-authenticated |
| **BTSP server on DAG socket** | rhizoCrypt | No BTSP server implementation | Provenance DAG not BTSP-authenticated |
| ~~**BTSP server on commit socket**~~ | sweetGrass | **RESOLVED** — first-line auto-detect: length-prefixed BTSP + JSON-line BTSP (primalSpring-compatible) + JSON-RPC three-way multiplexing. `perform_server_handshake_jsonline` with BearDog delegation. | ~~Provenance commit not BTSP-authenticated~~ |
| ~~**BTSP server on provenance socket**~~ | loamSpine | **RESOLVED** — NDJSON auto-detect in UDS accept loop; `perform_ndjson_server_handshake` compatible with primalSpring wire format. Provider-delegated crypto. | ~~Provenance attestation not BTSP-authenticated~~ |

**What upstream needs to do**: Implement the 4-step handshake protocol as a pre-JSON-RPC
negotiation layer. See `primalSpring/ecoPrimal/src/btsp/` for the client-side reference
implementation. The handshake uses HMAC-SHA256 with `FAMILY_SEED` key derivation, followed
by optional ChaCha20-Poly1305 encrypted channel. The simplest approach: detect first byte
`{` with `"type":"ClientHello"` and branch to BTSP before JSON-RPC dispatch.

**primalSpring workaround**: `upgrade_btsp_clients()` uses a reactive two-pass strategy —
cleartext probe first, BTSP escalation only for capabilities that reject cleartext.
Guidestone Layer 1.5 reports these as expected FAILs (5/166 checks).

### High — Architectural

| Gap | Owner | Notes |
|-----|-------|-------|
| **biomeOS must route through Tower Atomic** | biomeOS | biomeOS does its own socket forwarding + method translation. Should delegate to Songbird mesh relay + BearDog BTSP. Any HTTP outside Tower pulls in C deps. See: `BIOMEOS_DOCKER_SOCKET_ALIGNMENT_GUIDANCE_APR13_2026.md` |
| **biomeOS needs its own Tower Atomic** | biomeOS | For biomeOS to participate in encrypted NUCLEUS, it needs BTSP client/server capability — currently starts with `BIOMEOS_BTSP_ENFORCE=0` (cleartext bootstrap). Long-term: biomeOS evolves its own Tower or delegates all transport to Songbird/BearDog. |

### Medium — Graph / Registry Updates

| Gap | Owner | Notes |
|-----|-------|-------|
| `nucleus_complete.toml` missing NestGate streaming ops | biomeOS | Need `store_blob`, `retrieve_range`, `object.size`, `namespaces.list` (Session 43) |
| `nucleus_complete.toml` missing barraCuda/coralReef as separate nodes | biomeOS | Only registered in `tower_atomic_bootstrap.toml` optional section; no `tensor.batch.submit` |
| `capability_registry.toml` has no `[translations.tensor]` | biomeOS | barraCuda's 39 JSON-RPC methods (Sprint 44: +7 linalg/spectral/stats/tensor) have no translation entries |
| `BatchGuard` migration guide | primalSpring | **DONE** — `docs/BATCHGUARD_MIGRATION_GUIDE.md` written; springs can adopt |
| Graph `transport` metadata: no TCP/Tower fallback | biomeOS | Graphs say `uds_only` with no acknowledgment of Docker/TCP deployment mode |

### Low

| Gap | Owner | Notes |
|-----|-------|-------|
| ~~29 shader absorption candidates~~ | barraCuda | **RESOLVED** (Sprint 43) — 18/18 barraCuda candidates confirmed upstream |
| ~~RAWR GPU kernel~~ | barraCuda | **RESOLVED** (Sprint 40) — `RawrWeightedMeanGpu` already exists |
| ~~Phase 45 gap #6: tensor.create/matmul GPU-only~~ | barraCuda | **RESOLVED** (Sprint 44c) — CPU fallback for all 7 handle-based tensor ops via `CpuTensor` store |
| Batched `OdeRK45F64` for Richards PDE | barraCuda | airSpring-specific, low priority |

---

## Primal Health Summary (April 21, 2026 — Post Phase 45 Audit)

| Primal | Version | Tests | Status |
|--------|---------|-------|--------|
| barraCuda | Sprint 44d | 4,393+ pass | READY — 39 JSON-RPC methods, CPU tensor fallback, wire contract updated |
| BearDog | Wave 62 | 37 pass | READY — `crypto.sign` returns `public_key`, Ed25519 standardized to standard base64 |
| coralReef | Iter 84+ | 856 pass (2 env-sensitive) | READY |
| loamSpine | 0.9.16 | 1,454 pass | READY — BTSP NDJSON wire-format aligned (Phase 45b), family-qualified socket naming, stadial gate cleared |
| rhizoCrypt | S45.1 | 35 pass | READY — first-byte `{` auto-detect, BTSP liveness passthrough |
| Songbird | Wave 151 | up to date | READY — `ipc.resolve` capability-first with primal-name fallback, `ipc.resolve_by_name` alias |
| NestGate | Session 43k | 11,816 pass (451 ignored) | READY — 47 UDS methods, 80% coverage, zero async-trait |
| petalTongue | current | up to date | READY |
| Squirrel | alpha.51 | 735 pass | READY |
| sweetGrass | current | 1,446 pass | READY — `detect_protocol` first-line auto-detect, `family_seed` relay aligned with `beardog_types`, `BraidSignature` removed (v0.7.29 target), env vars fully centralized |
| toadStool | S175 | 7,818 lib pass | READY |
| biomeOS | v3.22 | 7,784 pass | READY — dual-protocol auto-detect on UDS (HTTP + JSON-RPC), zero C deps |

**The primary architectural gap is biomeOS's forwarding model.** biomeOS does its own
socket forwarding and method name translation instead of routing through Tower Atomic.
This causes socket path mismatches, protocol mismatches, and domain-prefix errors in
Docker. The fix: biomeOS delegates transport to Songbird (mesh relay) and BearDog (BTSP).
Tower Atomic is the communication substrate — the electron of the ecosystem.

**biomeOS v3.09 gap status (April 14, 2026 revalidation):**

biomeOS v3.09 commit `41084b38` claims all 5 gaps fixed. **Code-level fixes confirmed:**
1. **BTSP client** — `btsp_client.rs` exists with 4-step handshake. `AtomicClient::call_btsp()` wired.
2. **Method-prefix fix** — `capability.call` multi-segment operation logic updated.
3. **Socket directory scan** — `get_socket_directories()` scans `/tmp/biomeos-{FAMILY_ID}` and `/tmp/biomeos-default/`.
4. **`ipc.resolve`** — Wired. Returns `"requires primal_id or capability parameter"` (alive).
5. **`graph.list` path fix** — Returns `[]` instead of error (path resolves).

**Runtime behavior: fixes don't activate.** Root cause: **graph bootstrapping gap**. biomeOS
starts with `--graphs-dir /opt/ecoprimals/graphs --tcp-only`, the TOML files are present,
but `graph.list` returns `[]`. Without loaded graphs, biomeOS's route table is empty — it
can't resolve capabilities, doesn't know beardog is BTSP-secured, and `ipc.resolve` returns
"Primal not found." The method-prefix fix may also depend on translation rules from loaded graphs.
`graph.load` via TCP returns "Failed to forward to neural-api socket" (self-forwarding loop).

**Remaining upstream blocker: biomeOS graph bootstrapping in `--tcp-only` mode.**
biomeOS must either auto-scan TOML on startup or wire `graph.load` as a local handler
(not forwarded through its own UDS). Everything else is code-complete.

primalSpring workaround remains: `CompositionContext` with `DirectTcp` + `HttpTcp` routes
bypasses biomeOS forwarding. `is_gateway_forwarding_error()` classifies failures as upstream.

The graph/registry gaps (missing tensor translations, NestGate streaming ops) are
straightforward additions that biomeOS team can absorb from our updated
`nucleus_complete.toml` and `BATCHGUARD_MIGRATION_GUIDE.md`.

---

## primalSpring Local Validation Status (April 13, 2026 — Post-Cleanup)

**Full NUCLEUS Docker lab**: 11 primals deployed, 465 unit tests pass, 0 clippy warnings.

| Experiment | Result | Notes |
|------------|--------|-------|
| exp030 (Covalent Bond) | **12/12 ALL PASS** (4 skipped) | beardog BTSP correctly skipped |
| exp031 (Ionic Bond) | **4/4 ALL PASS** (2 skipped) | beardog BTSP correctly skipped |
| exp032 (Plasmodium) | **9/9 ALL PASS** (3 skipped) | songbird HTTP fallback |
| exp074 (Cross-Gate) | **10/10 ALL PASS** (5 skipped) | songbird HTTP, biomeos TCP, 137 caps |
| exp075 (Neural API) | **8/8 ALL PASS** (4 skipped) | biomeOS forwarding gaps labeled UPSTREAM |
| exp094 (Composition Parity) | **5/5 ALL PASS** (18 skipped) | all 18 skips are upstream biomeOS/NestGate gaps |

All 48 local checks pass. 36 upstream-dependent checks properly skipped with `UPSTREAM:` labels.

---

**License**: CC-BY-SA 4.0
