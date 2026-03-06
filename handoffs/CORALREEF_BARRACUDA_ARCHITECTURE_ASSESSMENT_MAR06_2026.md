# coralReef ↔ barraCuda Architecture Assessment

**Date**: March 6, 2026
**Author**: coralReef deep audit session
**Status**: Active assessment — for inter-primal discussion

---

## Question

Should barraCuda and coralReef remain separate primals, merge into one
(e.g. "reefShark"), or evolve their boundary?

## Recommendation: Stay Separate

**barraCuda and coralReef should remain distinct primals** with a clean
IPC boundary. A merge ("reefShark") would violate the single-responsibility
principle that makes the ecoPrimals architecture work.

---

## Analysis

### What Each Primal Owns

| Concern | barraCuda | coralReef |
|---------|-----------|-----------|
| **Primary role** | GPU math engine — shader authoring + dispatch | GPU compiler — SPIR-V/WGSL → native binary |
| **Input** | Domain equations, precision requirements | SPIR-V/WGSL bytecode |
| **Output** | WGSL shaders, dispatch results | SASS/native GPU binary |
| **f64 strategy** | Precision selection (Native/Hybrid/DF64) | f64 transcendental lowering (DFMA hardware path) |
| **Optimization** | naga IR level (FMA fusion, dead expr) | NAK SSA IR level (RA, scheduling, encoding) |
| **Hardware** | Agnostic (via wgpu/coralDriver) | Vendor-specific (SM20–SM120, future AMD/Intel) |
| **Dependencies** | naga, wgpu (dispatch), 708 WGSL shaders | naga (frontend only), zero runtime deps |
| **User domain** | Scientists, engineers, ML practitioners | Compiler engineers, driver developers |

### Why They Shouldn't Merge

1. **Different lifecycles.** barraCuda's shader library changes with every
   new physics model or ML operation. coralReef changes with GPU architecture
   releases (SM130, RDNA5, Xe3). These cadences are independent.

2. **Different deployment targets.** barraCuda runs on end-user machines
   where shaders are authored and dispatched. coralReef could run as a
   compile server, a CI tool, or embedded in a driver — places where
   barraCuda's 708 WGSL shaders and wgpu dependency are unnecessary weight.

3. **The compiler is a capability, not a feature.** Per ecoPrimals
   architecture, primals discover capabilities at runtime. barraCuda should
   discover "I can compile SPIR-V to SASS" as a capability provided by
   coralReef, not as a built-in. This enables:
   - Upgrading the compiler without redeploying barraCuda
   - Running the compiler on a different machine (compile farm)
   - Swapping coralReef for a vendor SDK compiler if needed

4. **Clean IPC boundary already exists.** Both primals implement
   JSON-RPC 2.0 + tarpc. The integration point is:
   ```
   barraCuda → SPIR-V → tarpc.compiler.compile() → coralReef → SASS
   ```
   This is already designed; it just needs wiring.

5. **Sovereign compute evolution.** The SOVEREIGN_COMPUTE_EVOLUTION.md
   roadmap envisions a stack where each layer is independently replaceable:
   ```
   barraCuda (math) → coralReef (compile) → coralDriver (dispatch) → GPU
   ```
   Merging the first two layers defeats the purpose.

### Where Overlap Exists (and How to Resolve)

| Overlap | Resolution |
|---------|------------|
| f64 polynomial coefficients | coralReef has absorbed these. barraCuda should remove its copy and consume coralReef's results via IPC. |
| WGSL polyfill injection | When barraCuda routes through coralReef, coralReef handles f64 lowering in hardware. barraCuda disables polyfill injection for that path. |
| naga dependency | Both depend on naga, but at different layers. barraCuda uses naga for WGSL→SPIR-V; coralReef uses naga for SPIR-V→IR. No conflict. |
| `Fp64Strategy` | barraCuda owns the strategy decision; coralReef's `CompileOptions::fp64_software` is the switch. barraCuda maps its strategy to this flag. |

### Integration Architecture (Next Step)

```
┌─────────────────────────────────────────────────────┐
│ barraCuda                                           │
│                                                     │
│  WGSL shader ──→ naga ──→ SPIR-V                   │
│       │                      │                      │
│       │    ┌─────────────────┼──── IPC boundary ──┐ │
│       │    │                 ▼                     │ │
│       │    │  coralReef                            │ │
│       │    │  tarpc.compiler.compile(spir-v)       │ │
│       │    │       │                               │ │
│       │    │       ▼                               │ │
│       │    │  SASS binary ←──── returned via IPC   │ │
│       │    └───────────────────────────────────────┘ │
│       │                                             │
│       ▼                                             │
│  coralDriver.dispatch(sass_binary)  [Phase 7]      │
│       │                                             │
│       ▼                                             │
│  GPU execution + results                            │
└─────────────────────────────────────────────────────┘
```

### What Would "reefShark" Be?

If we *did* merge, "reefShark" would be a compile-and-dispatch primal:
WGSL → SASS → GPU execution. This sounds appealing but:

- It re-creates the monolithic CUDA toolkit pattern we're trying to escape
- It makes the binary massive (708 shaders + entire compiler)
- It can't be deployed as a compile-only service
- It conflates "compile" and "dispatch" capabilities in one primal

**Verdict:** reefShark is not recommended. If a convenience facade is
desired, it should be a thin orchestrator primal that delegates to both
barraCuda and coralReef via IPC — not a merge.

---

## Action Items

### For coralReef
1. Expose `compiler.compile` tarpc endpoint (already done)
2. Add `compiler.compile_wgsl` endpoint for direct WGSL path
3. Publish capability advertisement: `shader.compile.nvidia.sm70-sm120`

### For barraCuda
1. Add `ComputeDispatch::CoralReef` variant
2. Discover coralReef via capability scan (`shader.compile.*`)
3. Route `SovereignCompiler` output to coralReef when available
4. Disable WGSL f64 polyfill injection when coralReef handles f64

### For wateringHole
1. Add coralReef to `PRIMAL_REGISTRY.md`
2. Document the compile IPC contract in `INTER_PRIMAL_INTERACTIONS.md`
3. Add `shader.compile` to `SEMANTIC_METHOD_NAMING_STANDARD.md`

---

*barraCuda is the brain (what to compute). coralReef is the hands
(how to compile it). They work together but are different organs.*
