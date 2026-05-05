# Primal Self-Knowledge Standard

**Version:** 1.1.0
**Date:** April 8, 2026
**Status:** Active — all primals and springs MUST adopt this
**Authority:** wateringHole (ecoPrimals Core Standards)
**Purpose:** Define the self-knowledge boundary for primals — what a primal
knows about itself, how it discovers and interacts with capabilities it does
not own, and the concrete naming conventions (sockets, env vars, config,
code) that make this work.

---

## Principle

> A primal knows only itself. Everything else is a capability.

No primal imports code from, hardcodes the name of, or assumes the existence
of any other primal. Inter-primal coordination happens at runtime through
capability discovery and JSON-RPC invocation. The Neural API routes requests
by capability domain; the caller never sees who provides the answer.

This standard unifies guidance previously spread across
`CAPABILITY_BASED_DISCOVERY_STANDARD.md`, `PRIMAL_IPC_PROTOCOL.md`,
`SEMANTIC_METHOD_NAMING_STANDARD.md`, `PRIMAL_RESPONSIBILITY_MATRIX.md`,
`UNIBIN_ARCHITECTURE_STANDARD.md`, and `SPOREGARDEN_DEPLOYMENT_STANDARD.md`
into one actionable reference.

---

## 1. The Self-Knowledge Boundary

### What a primal KNOWS (self)

| Knowledge | Example |
|-----------|---------|
| Own binary name | `beardog_primal` |
| Own capability domain(s) | `crypto.*`, `security.*` |
| Own socket path | `$BIOMEOS_SOCKET_DIR/security.sock` |
| Own configuration | `BEARDOG_KEY_DIR`, `BEARDOG_LOG_LEVEL` |
| Own version | `env!("CARGO_PKG_VERSION")` |
| Own identity | Response to `identity.get` |

### What a primal does NOT know (not-self)

| Forbidden Knowledge | Why |
|---------------------|-----|
| Another primal's name | Names change. Capabilities persist. |
| Another primal's binary | Binaries are deployment details. |
| Another primal's socket path | Paths are runtime-resolved. |
| Another primal's port or config key | Config belongs to the primal that owns it. |
| Another primal's internal method names | Use semantic `{domain}.{operation}` via Neural API. |

### Where primal names ARE acceptable

| Context | Why | Example |
|---------|-----|---------|
| `identity.get` response | Self-identification | `{"primal": "beardog", "version": "0.9.1"}` |
| `capability.register` payload | Telling biomeOS who you are on startup | `"primal": "beardog"` |
| Deploy graph `binary` / `name` fields | Orchestration needs binary names | `binary = "beardog_primal"` |
| Logging and diagnostics | Human-readable context | `info!(primal = "beardog", ...)` |
| Backward-compat aliases (Phase 1–2) | Migration path for legacy consumers | `#[serde(alias = "beardog_endpoint")]` |
| Tests that verify specific integration | Intentional primal-to-primal testing | `probe_primal("beardog")` |

---

## 2. Capability Domain Registry

Every inter-primal interaction is expressed in terms of capability domains.
This is the canonical vocabulary. Primals route by domain, not by name.

| Domain | Namespace | Socket Stem | Env Prefix | Owner | Role |
|--------|-----------|-------------|------------|-------|------|
| **Crypto** | `crypto.*` | `crypto` | `CRYPTO_` | BearDog | Encrypt, decrypt, sign, verify, hash, keypair generation |
| **Security** | `security.*` | `security` | `SECURITY_` | BearDog | TLS, authentication, certificate management |
| **Network** | `net.*` | `network` | `NETWORK_` | Songbird | Mesh, onion routing, peer discovery, encrypted transport |
| **Storage** | `storage.*` | `storage` | `STORAGE_` | NestGate | Key-value store, object storage, ZFS, archival |
| **Compute** | `compute.*`, `ember.*` | `compute` | `COMPUTE_` | toadStool | GPU dispatch, hardware inventory, ember management |
| **Shader** | `shader.*` | `shader` | `SHADER_` | coralReef | WGSL/SPIR-V compilation, shader validation |
| **Math** | `math.*` | `math` | `MATH_` | barraCuda | Tensor ops, activations, statistics, special functions |
| **AI** | `ai.*`, `context.*` | `ai` | `AI_` | Squirrel | Inference routing, model management, summarization |
| **Orchestration** | `capability.*`, `graph.*`, `topology.*`, `lifecycle.*` | `biomeos` | `BIOMEOS_` | biomeOS | Capability routing, graph deployment, lifecycle |
| **Visualization** | `visualization.*`, `interaction.*` | `visualization` | `VISUALIZATION_` | petalTongue | Rendering, dashboards, SVG/HTML export, interaction |
| **DAG** | `dag.*` | `dag` | `DAG_` | rhizoCrypt | Merkle proofs, causal DAGs, session-scoped provenance |
| **Ledger** | `entry.*`, `ledger.*` | `ledger` | `LEDGER_` | loamSpine | Append-only history, inclusion proofs |
| **Attribution** | `attribution.*` | `attribution` | `ATTRIBUTION_` | sweetGrass | Content braids, contribution tracking, convergence |
| **Identity** | `identity.*` | (self) | (self) | Every primal | `identity.get` — self-identification for sourDough compliance |

**Rules:**
- A primal OWNS one or more domains. It is the canonical provider.
- A primal DELEGATES domains it does not own via `capability.call`.
- A primal MUST NOT implement functionality in a domain it does not own
  (overstep). See `PRIMAL_RESPONSIBILITY_MATRIX.md` v3.0 for the full
  concern matrix.
- New domains are added to this table via wateringHole PR. The domain name
  becomes the socket stem, env prefix, and method namespace root.

---

## 3. Socket Naming Convention

### Primary rule

Primals bind their socket using their **capability domain stem**, not their
primal name:

```
$BIOMEOS_SOCKET_DIR/{domain}.sock
```

Where `BIOMEOS_SOCKET_DIR` defaults to `$XDG_RUNTIME_DIR/biomeos`.

**Examples:**

| Primal | Socket Path |
|--------|------------|
| BearDog | `$XDG_RUNTIME_DIR/biomeos/security.sock` |
| NestGate | `$XDG_RUNTIME_DIR/biomeos/storage.sock` |
| toadStool | `$XDG_RUNTIME_DIR/biomeos/compute.sock` |
| Squirrel | `$XDG_RUNTIME_DIR/biomeos/ai.sock` |
| Songbird | `$XDG_RUNTIME_DIR/biomeos/network.sock` |
| biomeOS | `$XDG_RUNTIME_DIR/biomeos/biomeos.sock` |

### Family-scoped variant (production mode)

When `FAMILY_ID` is set (and not `"default"`), the socket MUST be
family-scoped:

```
$BIOMEOS_SOCKET_DIR/{domain}-${FAMILY_ID}.sock
```

This is **production mode**. The family-scoped socket name serves as the
BTSP activation signal: when `FAMILY_ID` is set, all incoming connections
MUST authenticate via the BTSP handshake before any JSON-RPC methods are
exposed. See `BTSP_PROTOCOL_STANDARD.md` for the full protocol.

**Security invariant:** Hostile until proven otherwise. A connection to a
family-scoped socket that does not complete the BTSP handshake is refused.
Plaintext JSON-RPC is only available as a negotiated cipher suite
(`BTSP_NULL`) after successful authentication, when the `BondingPolicy`
allows it.

### Development mode

When `FAMILY_ID` is not set (or is `"default"`) and `BIOMEOS_INSECURE=1`:

```
$BIOMEOS_SOCKET_DIR/{domain}.sock
```

Raw cleartext JSON-RPC. No BTSP handshake. No authentication. This is
intended only for `cargo test`, local development, and primalSpring
experiments. Not deployable.

**Guard:** If both `FAMILY_ID` (non-default) and `BIOMEOS_INSECURE=1` are
set, the primal MUST refuse to start. You cannot claim a family AND skip
authentication.

### Legacy compatibility (deprecation path)

During migration, a primal MAY also bind or symlink the legacy primal-named
socket:

```
$BIOMEOS_SOCKET_DIR/{primal}.sock -> {domain}.sock
```

For example: `beardog.sock -> security.sock`. This enables consumers still
using identity-based discovery (Tier 5–6 in `CAPABILITY_BASED_DISCOVERY_STANDARD.md`)
to find the socket while they migrate. The symlink is the primal's
responsibility to create and clean up.

### Multi-domain primals

A primal that owns multiple domains (e.g., BearDog owns `crypto.*` and
`security.*`) creates one socket per primary domain, or a single socket
that handles both namespaces — the primal chooses. If a single socket, a
symlink for the secondary domain is RECOMMENDED:

```
$BIOMEOS_SOCKET_DIR/security.sock        (primary, BearDog listens here)
$BIOMEOS_SOCKET_DIR/crypto.sock -> security.sock   (symlink)
```

### Requirements

1. **Filesystem sockets are REQUIRED on Linux.** Abstract namespace sockets
   alone are invisible to `readdir()` discovery. See
   `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2.0 Section "Filesystem
   Socket Requirements."
2. **Sockets MUST live under `$BIOMEOS_SOCKET_DIR`.** Custom directories
   (e.g., `/run/user/1000/myprimal/`) are non-conformant.
3. **Clean up on shutdown.** Remove sockets and symlinks on graceful exit.
   Stale sockets pollute discovery.

---

## 4. Environment Variable Convention

### Capability-based env vars (for consumers)

Consumers discover providers via capability-domain env vars. These are set
by the orchestrator (biomeOS, deploy graph, sporeGarden) — not hardcoded
by the consuming primal.

| Pattern | Purpose | Example |
|---------|---------|---------|
| `{DOMAIN}_SOCKET` | UDS path to capability provider | `SECURITY_SOCKET=/run/user/1000/biomeos/security.sock` |
| `{DOMAIN}_ENDPOINT` | HTTP/TCP endpoint for capability | `COMPUTE_ENDPOINT=http://localhost:9001` |
| `{DOMAIN}_PORT` | TCP port for capability provider | `AI_PORT=8080` |

### Self-config env vars (for the primal itself)

A primal's own configuration uses its own name as prefix. These are the
primal's business — no other primal reads them.

| Pattern | Purpose | Example |
|---------|---------|---------|
| `{PRIMAL}_FAMILY_ID` | Override family identity | `BEARDOG_FAMILY_ID=cluster-7` |
| `{PRIMAL}_LOG_LEVEL` | Primal-specific log level | `NESTGATE_LOG_LEVEL=debug` |
| `{PRIMAL}_DATA_DIR` | Primal-specific data path | `NESTGATE_DATA_DIR=/var/lib/nestgate` |
| `{PRIMAL}_AUDIT_DIR` | Primal-specific audit path | `BEARDOG_AUDIT_DIR=/var/log/beardog/audit` |

### Identity env vars (UniBin standard)

Precedence for identity resolution:

1. `{PRIMAL}_FAMILY_ID` / `{PRIMAL}_NODE_ID` (primal-specific override)
2. `FAMILY_ID` / `NODE_ID` (composition-wide)
3. Default: `standalone` / hostname

### Legacy aliases (deprecated, read-only)

During migration, primals MAY read legacy env vars as fallback. The
capability-based name is always primary:

```rust
let endpoint = env::var("SECURITY_ENDPOINT")
    .or_else(|_| env::var("BEARDOG_ENDPOINT"))  // legacy compat
    .unwrap_or_default();
```

The legacy alias MUST NOT be the only way to configure a capability route.
Phase 3 (below) removes legacy aliases entirely.

### What is NOT allowed

| Anti-Pattern | Why | Fix |
|-------------|-----|-----|
| `BEARDOG_SOCKET` as primary discovery key | Consumer knows provider name | Use `SECURITY_SOCKET` |
| `TOADSTOOL_PORT` in non-toadStool code | Cross-primal name leak | Use `COMPUTE_PORT` |
| `SONGBIRD_ENDPOINT` in NestGate config | NestGate doesn't need to know Songbird | Use `NETWORK_ENDPOINT` |
| `SQUIRREL_SOCKET` anywhere except Squirrel | Self-knowledge violation | Use `AI_SOCKET` |

---

## 5. Code Organization Patterns

These patterns show how a primal structures its code to respect the
self-knowledge boundary. They are extracted from real ecosystem evolution
(Songbird wave 110, NestGate EnvSource, petalTongue CapabilityDiscovery).

### Pattern A: Provider trait — abstract the capability, not the primal

```rust
/// A primal that needs crypto defines this trait.
/// The implementation may connect to BearDog, a hardware security module,
/// or a test mock. The consuming primal never knows which.
pub trait SecurityProvider: Send + Sync {
    async fn sign(&self, data: &[u8]) -> Result<Signature>;
    async fn verify(&self, data: &[u8], signature: &Signature) -> Result<bool>;
    async fn encrypt(&self, plaintext: &[u8]) -> Result<Vec<u8>>;
}
```

### Pattern B: Tiered discovery function — env, then domain socket, then Neural API

```rust
use std::path::PathBuf;

/// Discover the socket for a capability domain.
///
/// Resolution order:
/// 1. Explicit env var (`{DOMAIN}_SOCKET`)
/// 2. Domain-named socket under biomeos directory
/// 3. Neural API `capability.discover` (if biomeOS is running)
pub fn discover_capability_socket(domain: &str) -> Option<PathBuf> {
    let env_key = format!("{}_SOCKET", domain.to_ascii_uppercase());
    if let Ok(path) = std::env::var(&env_key) {
        return Some(PathBuf::from(path));
    }

    let biomeos_dir = biomeos_socket_dir();
    let domain_socket = biomeos_dir.join(format!("{domain}.sock"));
    if domain_socket.exists() {
        return Some(domain_socket);
    }

    // Tier 3: Neural API capability.discover (async, omitted for brevity)
    None
}

fn biomeos_socket_dir() -> PathBuf {
    std::env::var("BIOMEOS_SOCKET_DIR")
        .map(PathBuf::from)
        .unwrap_or_else(|_| {
            let xdg = std::env::var("XDG_RUNTIME_DIR")
                .unwrap_or_else(|_| "/tmp".to_string());
            PathBuf::from(xdg).join("biomeos")
        })
}
```

### Pattern C: Config struct with serde aliases — capability-first, legacy-compat

```rust
#[derive(serde::Deserialize)]
pub struct ServiceEndpoints {
    /// Security capability endpoint (crypto, TLS, signing).
    #[serde(alias = "beardog_endpoint")]
    pub security_endpoint: String,

    /// Storage capability endpoint (persistence, archival).
    #[serde(alias = "nestgate_endpoint")]
    pub storage_endpoint: String,

    /// Compute capability endpoint (GPU dispatch).
    #[serde(alias = "toadstool_endpoint")]
    pub compute_endpoint: String,

    /// AI capability endpoint (inference, model management).
    #[serde(alias = "squirrel_endpoint")]
    pub ai_endpoint: String,
}
```

The struct field name uses capability language. The `alias` preserves
backward compatibility with existing config files and env vars.

### Pattern D: Test fixtures — capability-named with deprecated aliases

```rust
pub mod test_ports {
    pub fn security_provider_port() -> u16 { 17550 }
    pub fn storage_provider_port() -> u16 { 17551 }
    pub fn compute_provider_port() -> u16 { 17552 }
    pub fn ai_provider_port() -> u16 { 17553 }

    #[deprecated = "use security_provider_port()"]
    pub fn beardog_port() -> u16 { security_provider_port() }

    #[deprecated = "use storage_provider_port()"]
    pub fn nestgate_port() -> u16 { storage_provider_port() }
}
```

### Pattern E: Capability.call via Neural API — the production path

```rust
/// Route an operation through the Neural API. The caller never knows
/// which primal handles it.
pub async fn capability_call(
    neural_socket: &Path,
    capability: &str,
    operation: &str,
    args: serde_json::Value,
) -> Result<serde_json::Value> {
    let request = serde_json::json!({
        "jsonrpc": "2.0",
        "method": "capability.call",
        "params": {
            "capability": capability,
            "operation": operation,
            "args": args
        },
        "id": 1
    });
    // Send JSON-RPC over UDS, receive response...
    send_jsonrpc(neural_socket, &request).await
}

// Usage: the word "beardog" never appears
let signature = capability_call(
    &neural_socket,
    "crypto",
    "sign",
    json!({"data": base64_data}),
).await?;
```

### Pattern F: EnvSource injection — testable, concurrent-safe config

```rust
/// Inject environment variable source for testability.
/// Production: reads real env. Tests: reads from HashMap.
pub trait EnvSource: Send + Sync {
    fn var(&self, key: &str) -> Option<String>;
}

pub struct RealEnv;
impl EnvSource for RealEnv {
    fn var(&self, key: &str) -> Option<String> {
        std::env::var(key).ok()
    }
}

/// Discovery function parameterized over env source.
pub fn discover_capability_socket_with(
    domain: &str,
    env: &dyn EnvSource,
    exists: impl Fn(&std::path::Path) -> bool,
) -> Option<PathBuf> {
    let env_key = format!("{}_SOCKET", domain.to_ascii_uppercase());
    if let Some(path) = env.var(&env_key) {
        return Some(PathBuf::from(path));
    }
    // ...
    None
}
```

This pattern (adopted by NestGate wave EnvSource) eliminates direct
`env::var()` calls, enables pure-function testing, and allows concurrent
test execution without env var collisions.

---

## 6. Compliance Audit Checklist

These rules are machine-verifiable. `primalSpring` runs these audits on
every ecosystem review cycle.

### MUST NOT appear in production code

(Excludes tests, logging, deploy graphs, and `identity.get` / registration
payloads.)

| Violation | Pattern | Fix |
|-----------|---------|-----|
| Hardcoded primal name in discovery | `discover_primal("beardog")` | `discover_by_capability("security")` |
| Primal-specific env var for routing | `env::var("TOADSTOOL_PORT")` | `env::var("COMPUTE_PORT")` |
| Primal name in method namespace | `"barracuda.compute.dispatch"` | `"compute.dispatch"` |
| Primal-named struct for generic role | `struct ToadstoolCompute` | `struct ComputeProvider` |
| Primal-named socket literal | `"/tmp/beardog.sock"` | `discover_capability_socket("security")` |
| Primal-specific port constant | `const BEARDOG_PORT: u16 = 7555` | `const SECURITY_PORT: u16 = 7555` |

### MAY appear

| Context | Rule |
|---------|------|
| `primal_names` module | For logging context only — never in routing |
| Test fixtures | Legacy names allowed in backward-compat verification tests |
| Deploy graph `binary` / `name` fields | Required for binary invocation |
| Registration payloads | Telling biomeOS who you are on startup |
| Serde `alias` on config structs | Phase 1–2 migration (see below) |

### Audit commands

```bash
# Count primal-name references (should trend toward zero)
rg 'beardog|BearDog|bear_dog' --type rust crates/ -c | awk -F: '{s+=$2} END {print s}'
rg 'nestgate|NestGate|nest_gate' --type rust crates/ -c | awk -F: '{s+=$2} END {print s}'
rg 'toadstool|toadStool|toad_stool' --type rust crates/ -c | awk -F: '{s+=$2} END {print s}'
rg 'squirrel|Squirrel' --type rust crates/ -c | awk -F: '{s+=$2} END {print s}'

# Find primal-specific env vars in non-test production code
rg 'BEARDOG_|NESTGATE_|TOADSTOOL_|SQUIRREL_|SONGBIRD_|BARRACUDA_' \
   --type rust crates/ -g '!**/tests/**' -g '!**/test*'

# Find primal-named structs/functions used as generic roles
rg 'struct.*Toadstool|struct.*BearDog|struct.*NestGate|struct.*Squirrel|fn.*beardog|fn.*toadstool|fn.*nestgate|fn.*squirrel' \
   --type rust crates/ -g '!**/tests/**'
```

### Scoring

| Score | Meaning |
|-------|---------|
| **A** | Zero primal-name refs in production code (excluding acceptable contexts) |
| **B** | Capability-first with deprecated legacy aliases (Phase 1–2) |
| **C** | Mixed — some capability-based, some hardcoded |
| **D** | Primarily identity-based discovery |
| **F** | No capability-based patterns at all |

---

## 7. Migration Path

### Phase 1: Add capability-named companions (current phase for most primals)

- Add capability-based field names, function names, and env vars alongside
  legacy primal-named ones.
- Legacy names become `#[deprecated]` or `serde(alias)`.
- Socket: bind domain-named socket, create primal-named symlink.
- Score target: **B**

**Songbird is in late Phase 1** — 302 refs remain (down from 2,558), with
capability-first patterns in all major subsystems.

### Phase 2: Swap primary and alias

- Capability name is the only documented, public-facing name.
- Legacy primal name only appears in `#[deprecated]` aliases and serde
  compatibility.
- Socket: domain-named socket is primary, primal-named symlink is optional.
- Score target: **A** (with compat aliases)

### Phase 3: Remove deprecated aliases (coordinated)

- All legacy primal-name aliases removed across the ecosystem.
- Requires coordination: all consumers must have completed Phase 2.
- Socket: only domain-named sockets exist.
- Score target: **A** (clean)

### Migration is per-primal, not ecosystem-wide

Each primal migrates at its own pace. Phases are not synchronized. The
backward-compat tier in discovery (env fallback, primal-named sockets,
serde aliases) exists specifically to allow asymmetric migration.

---

## 8. Cross-References

This standard extends and unifies guidance from:

| Standard | Relationship |
|----------|-------------|
| `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2.0 | Extended: this standard adds concrete code patterns, env var conventions, and socket naming rules that the discovery standard references but does not define in detail. |
| `PRIMAL_IPC_PROTOCOL.md` v3.1.0 | Extended: socket path conventions and transport rules are preserved here with the addition of domain-based naming as primary. |
| `BTSP_PROTOCOL_STANDARD.md` v1.0.0 | Extended: FAMILY_ID → BTSP production mode convention defined here (§3), full protocol spec in BTSP standard. |
| `PRIMAL_RESPONSIBILITY_MATRIX.md` v3.0.0 | Aligned: the capability domain registry (Section 2) mirrors the matrix's primal directory and capability namespaces. |
| `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.0.0 | Aligned: the `{domain}.{operation}` method naming convention is how capability domains manifest on the wire. |
| `UNIBIN_ARCHITECTURE_STANDARD.md` | Extended: identity env var precedence (`{PRIMAL}_FAMILY_ID` -> `FAMILY_ID` -> default) is documented here in the self-config section. |
| `SPOREGARDEN_DEPLOYMENT_STANDARD.md` | Aligned: `BIOMEOS_SOCKET_DIR`, `FAMILY_ID`, and per-primal env overrides follow the same patterns. |

---

## Version History

### v1.1.0 (April 8, 2026)

**Secure Socket Architecture.** Added BTSP production mode to socket naming
convention (§3). When `FAMILY_ID` is set, sockets are family-scoped and BTSP
authentication is mandatory. Added `BIOMEOS_INSECURE` guard (refuse to start
when both `FAMILY_ID` and `BIOMEOS_INSECURE` are set). Added cross-reference
to `BTSP_PROTOCOL_STANDARD.md`. Driven by primalSpring Phase 26 — Secure
Socket Architecture plan, resolving GAP-MATRIX-11 and establishing
zero-knowledge local IPC foundation.

### v1.0.0 (April 4, 2026)

Initial standard. Codifies the self-knowledge boundary, capability domain
registry, socket naming, env var conventions, code patterns, compliance
audit checklist, and phased migration path. Driven by primalSpring Phase 23
audit cycle — Songbird's 88% discovery debt reduction (2,558 to 302 refs)
demonstrated both the feasibility and the need for a codified standard.
