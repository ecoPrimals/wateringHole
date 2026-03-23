# 🌍 Semantic Method Naming Standard for Primal IPC

**Version**: 2.1.0  
**Date**: March 22, 2026  
**Status**: Official Ecosystem Standard  
**Authority**: wateringHole (ecoPrimals Core Standards)  
**Supersedes**: v2.0.0 (added cross-cutting health/capabilities canonical names)

---

## 🎯 PURPOSE

Establish semantic method naming conventions that enable **isomorphic evolution** - allowing primals to evolve, swap, and extend while maintaining ecosystem coherence.

**Key Principle**: Method names should describe **WHAT** (semantic intent), not **HOW** (implementation details).

---

## 📐 SEMANTIC NAMESPACE STRUCTURE

### Format: `{domain}.{operation}[.{variant}]`

**Components**:
1. **Domain**: Capability area (crypto, tls, http, storage, etc.)
2. **Operation**: What the method does (encrypt, decrypt, hash, etc.)
3. **Variant** (optional): Specific algorithm or mode

### Examples:

```json
// Cryptographic Operations
"crypto.generate_keypair"      // Semantic (what)
"crypto.x25519.generate"       // Specific (how)
"crypto.encrypt"               // Generic encryption
"crypto.aes128_gcm.encrypt"    // Specific algorithm

// TLS Operations
"tls.derive_secrets"           // TLS key derivation
"tls.sign_handshake"           // Sign handshake data
"tls.verify_certificate"       // Certificate validation

// HTTP Operations
"http.request"                 // Generic HTTP request
"http.get"                     // HTTP GET
"http.post"                    // HTTP POST

// Storage Operations
"storage.put"                  // Store data
"storage.get"                  // Retrieve data
"storage.delete"               // Remove data
```

---

## 🔄 EVOLUTION PATTERNS

### Pattern 1: Generic to Specific

**Level 1 - Semantic (stable)**:
```json
{"method": "crypto.encrypt", "params": {"algorithm": "aes-128-gcm", ...}}
```

**Level 2 - Algorithm-Specific (evolving)**:
```json
{"method": "crypto.aes128_gcm.encrypt", "params": {...}}
```

**Level 3 - Implementation-Specific (deprecated)**:
```json
// OLD - DO NOT USE
{"method": "aes128_gcm_encrypt", "params": {...}}
```

### Pattern 2: Version Evolution

```
v0.9:  "x25519_generate_ephemeral"           ❌ No namespace
v1.0:  "crypto.x25519_generate_ephemeral"    ✅ Domain namespace
v2.0:  "crypto.x25519.generate"              ✅ Hierarchical
v3.0:  "crypto.generate_keypair"             ✅ Fully semantic
       + params: {"algorithm": "x25519"}
```

**Migration Path**: Each version supports previous patterns during transition.

---

## 🌍 DOMAIN NAMESPACES

### Core Domains (Standardized)

#### 1. `crypto.*` - Cryptographic Operations

```json
// Key Management
"crypto.generate_keypair"      // Generate key pair
"crypto.derive_secret"         // Key exchange/derivation
"crypto.import_key"            // Import external key
"crypto.export_key"            // Export key

// Symmetric Encryption
"crypto.encrypt"               // Generic encryption
"crypto.decrypt"               // Generic decryption
"crypto.aes128_gcm.encrypt"    // AES-128-GCM specific
"crypto.aes256_gcm.encrypt"    // AES-256-GCM specific
"crypto.chacha20_poly1305.encrypt"  // ChaCha20-Poly1305

// Hashing
"crypto.hash"                  // Generic hash
"crypto.blake3.hash"           // BLAKE3 specific
"crypto.sha256.hash"           // SHA-256 specific
"crypto.hmac"                  // HMAC

// Signatures
"crypto.sign"                  // Generic signing
"crypto.verify"                // Generic verification
"crypto.ed25519.sign"          // Ed25519 specific
"crypto.ecdsa_p256.sign"       // ECDSA P-256 specific
```

#### 2. `tls.*` - TLS/SSL Operations

```json
"tls.derive_secrets"           // TLS key derivation
"tls.derive_handshake_secrets" // Handshake traffic keys
"tls.derive_application_secrets"  // Application traffic keys
"tls.compute_finished_verify_data"  // Finished message MAC
"tls.sign_handshake"           // Sign handshake context
"tls.verify_certificate"       // Verify cert chain
```

#### 3. `http.*` - HTTP/HTTPS Operations

```json
"http.request"                 // Generic HTTP request
"http.get"                     // HTTP GET
"http.post"                    // HTTP POST
"http.put"                     // HTTP PUT
"http.delete"                  // HTTP DELETE
"http.head"                    // HTTP HEAD
"http.patch"                   // HTTP PATCH
```

#### 4. `storage.*` - Data Storage Operations

```json
"storage.put"                  // Store object
"storage.get"                  // Retrieve object
"storage.delete"               // Delete object
"storage.list"                 // List objects
"storage.exists"               // Check existence
"storage.metadata"             // Get metadata
```

#### 5. `discovery.*` - Service Discovery

```json
"discovery.announce"           // Announce service
"discovery.query"              // Query for services
"discovery.heartbeat"          // Health check
"discovery.list"               // List all services
```

#### 6. `genetic.*` - Genetic Lineage Operations

```json
"genetic.derive_key"           // Derive from lineage
"genetic.mix_entropy"          // Mix entropy sources
"genetic.verify_lineage"       // Verify genetic proof
"genetic.generate_proof"       // Generate lineage proof
```

#### 7. `health.*` - Health and Liveness (Cross-Cutting)

Every primal MUST register these methods. They are the ecosystem's common
probe surface — primalSpring, biomeOS, and CI all depend on them.

| Canonical Name | Required Aliases | Response |
|----------------|-----------------|----------|
| `health.liveness` | `ping`, `health` | `{"status": "alive"}` |
| `health.readiness` | | `{"status": "ready", ...}` |
| `health.check` | `status`, `check` | `{"status": "healthy", ...}` |

#### 8. `capabilities.*` - Capability Enumeration (Cross-Cutting)

Every primal MUST register the canonical name AND accept the known aliases.
Consumers (primalSpring, biomeOS, Squirrel) SHOULD probe all three names
with fallback on `METHOD_NOT_FOUND`.

| Canonical Name | Required Aliases | Response |
|----------------|-----------------|----------|
| `capabilities.list` | `capability.list`, `primal.capabilities` | `[{"name": "...", ...}]` |

**Current ecosystem state** (March 2026):

| Primal | Method Registered | Aligned? |
|--------|------------------|----------|
| BearDog v0.9.0 | `capabilities.list` | Canonical |
| biomeOS v2.67 | `capability.list` | Alias — add `capabilities.list` |
| Squirrel alpha.17 | `capability.list` | Alias — add `capabilities.list` |
| Songbird wave60 | `primal.capabilities` | Alias — add `capabilities.list` |
| primalSpring v0.7.0 | `capabilities.list` (probes all 3 with fallback) | Canonical + tolerant |

**Why `capabilities.list` is canonical**: It follows the `{domain}.{operation}`
pattern (`capabilities` is the domain, `list` is the operation). The singular
`capability.list` reads as "list a single capability" which is semantically
different. BearDog (the most method-rich primal at ~91 crypto methods) already
uses the canonical form.

**Migration**: Primals should add `capabilities.list` as an alias alongside
their current name. No need to remove the current name — aliases are cheap
and prevent integration breakage.

#### 9. `lifecycle.*` - Primal Lifecycle

```json
"lifecycle.status"             // Current state + version
"lifecycle.shutdown"           // Graceful shutdown
```

---

## 🔧 IMPLEMENTATION GUIDELINES

### For Primal Developers

#### 1. Choose Semantic Names

**✅ Good** (semantic):
```rust
async fn handle_request(&self, method: &str) -> Result<Response> {
    match method {
        "crypto.generate_keypair" => self.generate_keypair(params),
        "crypto.encrypt" => self.encrypt(params),
        // Clear intent, algorithm specified in params
    }
}
```

**❌ Bad** (implementation-specific):
```rust
async fn handle_request(&self, method: &str) -> Result<Response> {
    match method {
        "x25519_keygen" => self.x25519_keygen(),  // Too specific
        "aes_enc" => self.aes_encrypt(),          // Unclear
    }
}
```

#### 2. Support Evolution

**Version N** (current):
```rust
match method {
    // New semantic name (preferred)
    "crypto.generate_keypair" => self.generate_keypair(params),
    
    // Old name (deprecated, but supported for transition)
    "x25519_generate_ephemeral" => {
        warn!("Deprecated method name, use 'crypto.generate_keypair'");
        self.generate_keypair(params)
    }
}
```

**Version N+1** (next):
```rust
match method {
    "crypto.generate_keypair" => self.generate_keypair(params),
    // Old name removed after transition period
}
```

#### 3. Document Capabilities

In your primal's documentation:

```toml
# Example: BearDog v0.18.0 capabilities

[capabilities.provided]
"crypto.generate_keypair" = "Generate X25519 keypair"
"crypto.derive_secret" = "ECDH key derivation"
"crypto.encrypt" = "Symmetric encryption (ChaCha20-Poly1305, AES-GCM)"
"crypto.hash" = "BLAKE3 hashing"
"tls.derive_secrets" = "TLS 1.3 key derivation"

[capabilities.deprecated]
"x25519_generate_ephemeral" = "Use crypto.generate_keypair instead"
"chacha20_poly1305_encrypt" = "Use crypto.encrypt with algorithm param"
```

---

## 🌐 NEURAL API TRANSLATION LAYER

### How biomeOS Bridges Evolution Gaps

During ecosystem evolution, primals may use different naming conventions. biomeOS Neural API provides **automatic translation**:

```toml
# graphs/tower_atomic_bootstrap.toml

[nodes.capabilities_provided]
# Semantic Name (what consumers call) → Actual Method (what provider implements)
"crypto.generate_keypair" = "crypto.x25519_generate_ephemeral"  # Current
# "crypto.generate_keypair" = "crypto.x25519.generate"          # Future
```

**How It Works**:

```
1. Songbird calls Neural API:
   {"method": "crypto.generate_keypair", "params": {...}}

2. Neural API looks up translation:
   "crypto.generate_keypair" → "crypto.x25519_generate_ephemeral" (BearDog v0.18)

3. Neural API routes to BearDog:
   {"method": "crypto.x25519_generate_ephemeral", "params": {...}}

4. BearDog executes and returns result

5. Neural API returns to Songbird
```

**Benefits**:
- ✅ Old primals work with new primals
- ✅ New primals work with old primals
- ✅ Ecosystem remains coherent during evolution
- ✅ No coordination required - update graphs only

---

## 📋 MIGRATION GUIDE

### For Existing Primals

**Phase 1: Add Semantic Aliases** (Week 1)
```rust
match method {
    // Keep old names working
    "x25519_generate_ephemeral" => self.generate_keypair(params),
    
    // Add new semantic names
    "crypto.generate_keypair" => self.generate_keypair(params),
}
```

**Phase 2: Deprecation Warnings** (Week 2-4)
```rust
match method {
    "x25519_generate_ephemeral" => {
        warn!("Method '{}' is deprecated. Use 'crypto.generate_keypair' instead.", method);
        self.generate_keypair(params)
    }
    "crypto.generate_keypair" => self.generate_keypair(params),
}
```

**Phase 3: Remove Old Names** (Month 2+)
```rust
match method {
    "crypto.generate_keypair" => self.generate_keypair(params),
    // Old names removed
}
```

### For New Primals

**Start with semantic names from day 1**:
```rust
match method {
    "crypto.generate_keypair" => self.generate_keypair(params),
    "crypto.encrypt" => self.encrypt(params),
    "crypto.hash" => self.hash(params),
    // All semantic, no legacy baggage
}
```

---

## ✅ COMPLIANCE CHECKLIST

### For Primal Authors

- [ ] All methods use domain namespaces (`crypto.*`, `tls.*`, `http.*`)
- [ ] Method names describe intent, not implementation
- [ ] Capabilities documented in README or CAPABILITIES.toml
- [ ] Deprecated methods supported with warnings during transition
- [ ] Integration tests use semantic names
- [ ] Graph mappings updated for Neural API translation

### For biomeOS Integration

- [ ] Graph includes `capabilities_provided` mappings
- [ ] Translation registry populated from graph
- [ ] Semantic → Actual method translation working
- [ ] Tests validate translation layer
- [ ] Documentation shows semantic examples

---

## 🎯 EXAMPLES: BEFORE & AFTER

### BearDog Evolution

**Before** (v0.9 - Pre-semantic):
```json
{"jsonrpc": "2.0", "method": "x25519_generate_ephemeral", "params": {}}
{"jsonrpc": "2.0", "method": "chacha20_poly1305_encrypt", "params": {...}}
{"jsonrpc": "2.0", "method": "blake3_hash", "params": {...}}
```

**After** (v0.18 - Semantic):
```json
{"jsonrpc": "2.0", "method": "crypto.x25519_generate_ephemeral", "params": {}}
{"jsonrpc": "2.0", "method": "crypto.chacha20_poly1305_encrypt", "params": {...}}
{"jsonrpc": "2.0", "method": "crypto.blake3_hash", "params": {...}}
```

**Future** (v1.0 - Fully Semantic):
```json
{"jsonrpc": "2.0", "method": "crypto.generate_keypair", "params": {"algorithm": "x25519"}}
{"jsonrpc": "2.0", "method": "crypto.encrypt", "params": {"algorithm": "chacha20_poly1305", ...}}
{"jsonrpc": "2.0", "method": "crypto.hash", "params": {"algorithm": "blake3", ...}}
```

### Songbird Evolution

**Before** (Direct BearDog calls):
```rust
// Tight coupling - knows BearDog's exact methods
let response = beardog.call_rpc("x25519_generate_ephemeral", params).await?;
```

**Interim** (Semantic names, direct):
```rust
// Semantic names, still direct
let response = beardog.call_rpc("crypto.x25519_generate_ephemeral", params).await?;
```

**After** (Neural API routing):
```rust
// Fully semantic via Neural API
let response = neural_api.call_capability("crypto.generate_keypair", params).await?;
// Neural API handles translation and routing
```

---

## 🔗 RELATED STANDARDS

- `PRIMAL_IPC_PROTOCOL.md` - Base IPC protocol
- `ECOBIN_ARCHITECTURE_STANDARD.md` - Pure Rust principles
- `UNIBIN_ARCHITECTURE_STANDARD.md` - Single binary pattern
- biomeOS `ISOMORPHIC_EVOLUTION.md` - Evolution principles
- biomeOS `NEURAL_API_ROUTING_SPECIFICATION.md` - Translation layer

---

## 📊 ADOPTION STATUS (Updated March 22, 2026)

| Primal | Version | Domain Methods | Cross-Cutting (`health.*`, `capabilities.*`) | Notes |
|--------|---------|---------------|----------------------------------------------|-------|
| **BearDog** | v0.9.0 | `crypto.*`, `tls.*`, `genetic.*`, `beacon.*` | `health.liveness` / `health.readiness` / `capabilities.list` — all canonical | Most compliant |
| **biomeOS** | v2.67 | `capability.*` routing via Neural API | `capability.list` (alias, not canonical) | Add `capabilities.list` alias |
| **Songbird** | wave60 | Mixed (`songbird.*` legacy + semantic) | `health` / `primal.capabilities` (alias, not canonical) | Add `health.liveness` / `capabilities.list` |
| **Squirrel** | alpha.17 | `ai.*`, `context.*`, `tool.*`, `capability.*` | `health.liveness` / `capability.list` (alias) | Add `capabilities.list` alias |
| **NestGate** | v2.1.0 | `storage.*` | Not verified | Needs audit |
| **ToadStool** | v0.1.0 | `compute.*` | Not verified | Needs audit |
| **primalSpring** | v0.7.0 | `coordination.*`, `composition.*`, `graph.*` | Canonical + probes all 3 aliases with fallback | Reference implementation |

---

## 🎉 BENEFITS

1. **Isomorphic Evolution**: Ecosystem structure preserved during change
2. **Provider Swappability**: Replace implementations without breaking consumers
3. **Clear Intent**: Method names self-documenting
4. **Forward Compatible**: New methods don't break old code
5. **Backward Compatible**: Old methods supported during transition
6. **Ecosystem Resilience**: Neural API bridges evolution gaps
7. **TRUE PRIMAL**: No hardcoded cross-primal dependencies

---

**Status**: Official Standard (v2.0.0)  
**Adoption**: Mandatory for new primals, recommended migration for existing  
**Enforcement**: Neural API translation layer bridges gaps during migration  
**Questions**: Post in wateringHole discussions

---

*"Semantic stability enables evolutionary freedom"* 🌍🦀

