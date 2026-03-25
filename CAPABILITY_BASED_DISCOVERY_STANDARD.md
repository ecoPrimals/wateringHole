# Capability-Based Discovery Standard

**Version:** 1.1.0
**Date:** March 25, 2026 (updated from 1.0.0 March 18, 2026)
**Status:** Active — all primals and springs SHOULD adopt this

## Principle

> Primals discover and invoke each other by **capability domain**, not by name.
> No primal knows another primal exists. Complexity through coordination, not coupling.

This standard codifies the "loose coupling" pattern that wateringHole has advocated since the beginning. The Neural API provides the routing backbone — primals register capabilities, and consumers discover providers at runtime via semantic capability calls.

## The Problem with Identity-Based Discovery

```rust
// ❌ TIGHT COUPLING — primal knows another primal's identity
let beardog = discover_primal("beardog");
let mut client = PrimalClient::connect(&beardog.socket, "beardog");
client.call("chacha20_poly1305_encrypt", params)?;
```

This fails when:
- BearDog is renamed or replaced by a different security primal
- A spring provides the same capability (e.g. hardware security module)
- The ecosystem evolves to split responsibilities differently
- Multiple primals share a capability domain

## The Capability-Based Alternative

```rust
// ✅ LOOSE COUPLING — primal asks for a capability
let provider = discover_by_capability("security");
let mut client = connect_by_capability("security")?;
client.call("crypto.encrypt", params)?;

// ✅ BEST — use Neural API capability.call for full routing
let result = capability_call("crypto", "encrypt", &args);
```

The caller never knows (or needs to know) that BearDog handles crypto. If tomorrow a `hardware_security_module` primal replaces BearDog for encryption, the caller's code doesn't change.

## Discovery Tiers

### Capability-Based (preferred)

| Tier | Method | Source |
|------|--------|--------|
| 1 | `capability.call` via Neural API | Authoritative — Neural API routes, translates, and forwards |
| 2 | `discover_by_capability(cap)` → Neural API `capability.discover` | Runtime resolution via biomeOS |
| 3 | Capability-named socket (`$XDG_RUNTIME_DIR/biomeos/{domain}.sock`) | Filesystem convention |
| 4 | Socket registry capability scan | Shared registry file |

### Identity-Based (legacy fallback)

| Tier | Method | Source |
|------|--------|--------|
| 1 | `{PRIMAL}_ADDRESS` or `{PRIMAL}_SOCKET` env var | Explicit override |
| 2 | `$XDG_RUNTIME_DIR/biomeos/{primal}.sock` | XDG convention (no family suffix) |
| 3 | `$XDG_RUNTIME_DIR/biomeos/{primal}-{family}.sock` | Family-scoped variant |
| 4 | `{temp_dir}/biomeos/{primal}.sock` | Temp fallback |
| 5 | Primal manifest file | Written on startup |
| 6 | Socket registry by name | Shared registry file |

Identity-based discovery remains available for backward compatibility and for
deploy graphs (which need primal names for binary invocation). But **all runtime
capability invocation** should use the capability-based path.

### Filesystem Socket Requirements (v1.1)

**All discovery below Tier 2 relies on `readdir()` — the ability to list files
in `$XDG_RUNTIME_DIR/biomeos/`.** This means:

1. **Filesystem sockets are REQUIRED on Linux.** Primals MUST create a socket
   file at `$XDG_RUNTIME_DIR/biomeos/<primal>.sock`. Abstract namespace sockets
   (`@primal`) are invisible to the filesystem and MUST NOT be the only socket.

2. **Capability-domain symlinks are RECOMMENDED.** After binding the primal-named
   socket, primals SHOULD create a symlink named after their primary capability
   domain:

   ```
   $XDG_RUNTIME_DIR/biomeos/ai.sock       -> squirrel.sock
   $XDG_RUNTIME_DIR/biomeos/security.sock  -> beardog.sock
   $XDG_RUNTIME_DIR/biomeos/dag.sock       -> rhizocrypt.sock
   ```

   This enables Tier 3 capability-based discovery without Songbird or Neural API.
   Springs performing filesystem probing scan for `{domain}.sock` by iterating
   the known capability domains they require.

3. **Custom socket directories are non-conformant.** Sockets MUST live in
   `$XDG_RUNTIME_DIR/biomeos/`, not in primal-specific directories. A primal
   that only creates `/run/user/1000/myprimal/myprimal.sock` is invisible to
   discovery.

4. **Socket cleanup on shutdown.** Primals MUST remove their socket files
   (and symlinks) on graceful shutdown. Stale socket files pollute discovery.

## Neural API `capability.call` — The Loose Standard

This is the recommended way for primals to invoke capabilities across the ecosystem:

```json
{
  "jsonrpc": "2.0",
  "method": "capability.call",
  "params": {
    "capability": "crypto",
    "operation": "encrypt",
    "args": { "plaintext": "...", "key_id": "default" }
  },
  "id": 1
}
```

**Flow:**
1. Neural API receives `capability.call`
2. Looks up `crypto.encrypt` in `CapabilityTranslationRegistry`
3. Finds provider (e.g. `beardog`) and actual method (e.g. `chacha20_poly1305_encrypt`)
4. Discovers provider socket via `NeuralRouter`
5. Forwards JSON-RPC to the provider
6. Returns result to caller

The caller never sees the primal name, the socket path, or the actual method name.

## Semantic Method Naming

All capabilities follow `{domain}.{operation}[.{variant}]`:

| Semantic Name | Provider | Actual Method |
|---------------|----------|---------------|
| `crypto.encrypt` | beardog | `chacha20_poly1305_encrypt` |
| `discovery.find_primals` | songbird | `ipc.list` |
| `compute.dispatch.submit` | toadstool | `compute_submit` |
| `storage.store` | nestgate | `content_store` |
| `ai.query` | squirrel | `ai.query` |

Primals register their translations via `capability.register`:

```json
{
  "method": "capability.register",
  "params": {
    "primal": "beardog",
    "capability": "crypto",
    "socket": "/run/user/1000/biomeos/beardog-default.sock",
    "semantic_mappings": {
      "encrypt": "chacha20_poly1305_encrypt",
      "decrypt": "chacha20_poly1305_decrypt"
    }
  }
}
```

## What Primals MUST Do

1. **Register capabilities** with the Neural API on startup via `capability.register`
2. **Use `capability.call`** (or `discover_by_capability`) for all cross-primal invocation
3. **Never hardcode** another primal's name, socket path, or method name in production code
4. **Define `by_capability`** in deploy graph nodes so orchestration uses capability discovery
5. **Implement `identity.get`** for sourDough compliance (returns own identity, not others')
6. **Implement `capability.list`** to advertise what you provide

## What Primals SHOULD Do

1. **Prefer `capability.call`** over direct socket connections — it handles translation and routing
2. **Create capability-domain symlinks** (e.g. `security.sock -> beardog.sock`) alongside primal-named sockets, enabling Tier 3 filesystem discovery
3. **Degrade gracefully** when the Neural API is unavailable — fall back to filesystem probing
4. **Use `required_capabilities()`** instead of `required_primals()` for composition validation
5. **Clean up sockets and symlinks** on graceful shutdown to prevent stale discovery results

## Where Primal Names ARE Acceptable

| Context | Why | Example |
|---------|-----|---------|
| Deploy graph `binary` field | Need to invoke a specific binary | `binary = "beardog_primal"` |
| Deploy graph `name` field | Node identity within the graph | `name = "beardog"` |
| `identity.get` response | Self-knowledge, not knowledge of others | `{"id": "primalspring"}` |
| Registration payloads | Telling biomeOS who you are | `"primal": "beardog"` |
| Tests | Testing specific primals intentionally | `probe_primal("beardog")` |
| Logging | Diagnostic information | `info!(primal = "beardog")` |

## Migration Guide

### From identity-based to capability-based:

| Before | After |
|--------|-------|
| `discover_primal("beardog")` | `discover_by_capability("security")` |
| `connect_primal("beardog")` | `connect_by_capability("security")` |
| `probe_primal("beardog")` | `coordination.probe_capability {"capability": "security"}` |
| `AtomicType::required_primals()` | `AtomicType::required_capabilities()` |
| `validate_composition(Tower)` | `validate_composition_by_capability(Tower)` |

### primalSpring reference implementation:

primalSpring v0.3.2 demonstrates the full pattern:
- `ipc/discover.rs`: `discover_by_capability()`, `capability_call()`, `discover_capabilities_for()`
- `ipc/client.rs`: `connect_by_capability()`
- `coordination/mod.rs`: `required_capabilities()`, `validate_composition_by_capability()`
- `deploy.rs`: `probe_graph_node()` uses `by_capability` when present
- Server: `coordination.probe_capability`, `coordination.validate_composition_by_capability`

---

## Version History

### v1.1.0 (March 25, 2026)

**Filesystem Socket & Symlink Clarifications**

- Filesystem sockets in `$XDG_RUNTIME_DIR/biomeos/` are REQUIRED on Linux
- Abstract namespace sockets alone are insufficient for discovery
- Capability-domain symlinks formally RECOMMENDED
- Custom socket directories declared non-conformant
- Socket cleanup on shutdown added to SHOULD requirements
- Discovery tier table updated with `{PRIMAL}_ADDRESS` and non-family variants

Driven by esotericWebb's first live composition: squirrel's abstract-only socket
and petaltongue's custom directory were both invisible to filesystem-based
discovery probing.

### v1.0.0 (March 18, 2026)

Initial standard. Established capability-based discovery tiers, Neural API
`capability.call`, semantic method naming integration, and migration guide.
