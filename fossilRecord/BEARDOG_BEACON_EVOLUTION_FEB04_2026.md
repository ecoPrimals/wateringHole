# BearDog Beacon Methods Evolution Handoff
## February 4, 2026

**From**: biomeOS Validation  
**To**: BearDog Maintainers  
**Priority**: HIGH - Blocks beacon genetics discovery  
**Status**: Methods defined in biomeOS, need implementation in BearDog

---

## Executive Summary

biomeOS has implemented `BeaconGeneticsManager` which orchestrates "meetings" (beacon seed exchanges) using `capability.call`. The capability translations route to BearDog, but **BearDog doesn't implement the required methods**.

### Current State

```
biomeOS: capability.call("beacon.get_id", {})
    ↓
CapabilityTranslationRegistry: "beacon.get_id" → BearDog socket
    ↓
BearDog: {"error": "Method not found: beacon.get_id"} ❌
```

### Required State

```
biomeOS: capability.call("beacon.get_id", {})
    ↓
BearDog: {"result": {"beacon_id": "d03029e5..."}} ✅
```

---

## Methods to Implement

### 1. `beacon.get_id` - Get Beacon ID

**Purpose**: Return this node's beacon ID (derived from beacon seed)

```json
// Request
{"jsonrpc": "2.0", "method": "beacon.get_id", "params": {}, "id": 1}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "beacon_id": "d03029e5c5cd0c3b44e2e316118943d8bfee887fd589d20b647ee5a16eb462f1"
  },
  "id": 1
}
```

**Implementation**:
```rust
fn beacon_get_id(&self) -> Result<BeaconIdResponse> {
    let beacon_id = self.beacon_seed
        .as_ref()
        .map(|s| s.derive_id())
        .unwrap_or_else(|| self.generate_beacon_id());
    
    Ok(BeaconIdResponse { beacon_id })
}
```

---

### 2. `beacon.get_seed` - Get Beacon Seed (for sharing)

**Purpose**: Return the beacon seed in hex format for sharing during meetings

```json
// Request
{"jsonrpc": "2.0", "method": "beacon.get_seed", "params": {}, "id": 1}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "seed_hex": "a1b2c3d4e5f6..."
  },
  "id": 1
}
```

**Security Note**: This seed is meant to be shared with peers during meetings. It's NOT the lineage seed.

---

### 3. `beacon.encrypt` - Encrypt with Beacon Seed

**Purpose**: Encrypt data using this node's beacon seed (ChaCha20-Poly1305)

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "beacon.encrypt",
  "params": {
    "plaintext_b64": "SGVsbG8gV29ybGQ=",
    "seed_hex": null  // Optional: use own seed if null
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "ciphertext_b64": "encrypted_data_here",
    "nonce_b64": "random_nonce_here"
  },
  "id": 1
}
```

---

### 4. `beacon.decrypt` - Decrypt with Beacon Seed

**Purpose**: Decrypt data using this node's beacon seed

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "beacon.decrypt",
  "params": {
    "ciphertext_b64": "encrypted_data_here",
    "nonce_b64": "nonce_here",
    "seed_hex": null  // Optional: use own seed if null
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "plaintext_b64": "SGVsbG8gV29ybGQ="
  },
  "id": 1
}
```

---

### 5. `beacon.try_decrypt` - Try Decrypt with Specific Seed

**Purpose**: Attempt to decrypt using a provided seed (for trying met beacons)

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "beacon.try_decrypt",
  "params": {
    "ciphertext_b64": "encrypted_beacon_here",
    "seed_hex": "peer_seed_from_meeting"
  },
  "id": 1
}

// Response (success)
{
  "jsonrpc": "2.0",
  "result": {
    "decrypted": true,
    "plaintext_b64": "decoded_payload"
  },
  "id": 1
}

// Response (failure - wrong seed)
{
  "jsonrpc": "2.0",
  "result": {
    "decrypted": false,
    "plaintext_b64": null
  },
  "id": 1
}
```

**Use Case**: biomeOS loops through all met beacon seeds to find which one decrypts an incoming broadcast.

---

### 6. `beacon.generate` - Generate New Beacon

**Purpose**: Generate a new beacon seed (for first-time setup)

```json
// Request
{"jsonrpc": "2.0", "method": "beacon.generate", "params": {}, "id": 1}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "beacon_id": "new_beacon_id_here",
    "seed_hex": "new_seed_hex_here"
  },
  "id": 1
}
```

---

### 7. `lineage.verify` - Verify Family Lineage

**Purpose**: Verify if a peer belongs to the same genetic lineage

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "lineage.verify",
  "params": {
    "peer_lineage_hint": "8ff3b864a4bc589a",
    "challenge": "random_challenge_b64"
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "verified": true,
    "same_family": true,
    "relationship": "sibling"  // or "parent", "child", "cousin"
  },
  "id": 1
}
```

---

## Crypto Primitives (May Already Exist)

These may already be implemented - verify and expose via JSON-RPC:

| Method | Purpose | Status |
|--------|---------|--------|
| `crypto.encrypt` | ChaCha20-Poly1305 encrypt | Check if exists |
| `crypto.decrypt` | ChaCha20-Poly1305 decrypt | Check if exists |
| `crypto.blake3_hash` | BLAKE3 hash | Check if exists |
| `crypto.derive_child_seed` | HKDF seed derivation | Check if exists |

---

## Data Structures

### BeaconSeed

```rust
/// Beacon seed for Dark Forest discovery
pub struct BeaconSeed {
    /// 32-byte seed material
    seed: [u8; 32],
}

impl BeaconSeed {
    /// Generate new random beacon seed
    pub fn generate() -> Self;
    
    /// Create from hex string
    pub fn from_hex(hex: &str) -> Result<Self>;
    
    /// Export to hex string
    pub fn to_hex(&self) -> String;
    
    /// Derive beacon ID (BLAKE3 hash of seed)
    pub fn derive_id(&self) -> String;
    
    /// Encrypt payload with this seed
    pub fn encrypt(&self, plaintext: &[u8]) -> Result<(Vec<u8>, Vec<u8>)>;
    
    /// Decrypt payload with this seed
    pub fn decrypt(&self, ciphertext: &[u8], nonce: &[u8]) -> Result<Vec<u8>>;
    
    /// Try to decrypt (returns None on failure, not error)
    pub fn try_decrypt(&self, ciphertext: &[u8]) -> Option<Vec<u8>>;
}
```

---

## Storage Considerations

BearDog should store beacon seeds:
- Own beacon seed (persistent)
- Lineage seed (from family, never shared raw)
- Met beacon seeds could be stored by BearDog OR delegated to biomeOS

**Recommended**: BearDog manages own seed, biomeOS manages address book (`.known_beacons.json`)

---

## Test Commands

After implementing, verify with:

```bash
FAMILY_ID=nat0
SOCKET="/run/user/$(id -u)/biomeos/beardog-$FAMILY_ID.sock"

# Test beacon.get_id
echo '{"jsonrpc":"2.0","method":"beacon.get_id","params":{},"id":1}' | nc -U $SOCKET

# Test beacon.generate
echo '{"jsonrpc":"2.0","method":"beacon.generate","params":{},"id":1}' | nc -U $SOCKET

# Test beacon.encrypt
echo '{"jsonrpc":"2.0","method":"beacon.encrypt","params":{"plaintext_b64":"SGVsbG8="},"id":1}' | nc -U $SOCKET

# Test lineage.verify
echo '{"jsonrpc":"2.0","method":"lineage.verify","params":{"peer_lineage_hint":"8ff3b864a4bc589a"},"id":1}' | nc -U $SOCKET
```

---

## Integration with biomeOS

Once implemented, biomeOS `BeaconGeneticsManager` will work:

```rust
// biomeOS orchestrates meetings using BearDog primitives
async fn initiate_meeting(&mut self, peer: &str) -> Result<BeaconId> {
    // Step 1: Get our beacon ID
    let our_id = self.capability_caller
        .call("beacon.get_id", json!({})).await?;
    
    // Step 2: Get our seed for exchange
    let our_seed = self.capability_caller
        .call("beacon.get_seed", json!({})).await?;
    
    // Step 3: Exchange via Songbird
    let peer_data = self.capability_caller
        .call("network.beacon_exchange", json!({
            "endpoint": peer,
            "beacon_id": our_id,
            "seed_encrypted": our_seed
        })).await?;
    
    // Step 4: Store peer's seed locally
    self.store_met_beacon(peer_data)?;
    
    Ok(peer_data.beacon_id)
}
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `biomeOS/specs/BEACON_CAPABILITY_TRANSLATIONS.md` | Capability → method mapping |
| `biomeOS/specs/BEACON_GENETICS_BUILD_SPEC.md` | Full beacon genetics spec |
| `biomeOS/crates/biomeos-spore/src/beacon_genetics/` | biomeOS implementation |
| `biomeOS/livespore-usb/.known_beacons.json` | Sample address book |

---

**Handoff Date**: February 4, 2026  
**Contact**: biomeOS Neural API team  
**Validation Script**: `biomeOS/scripts/validate_beacon_discovery.sh`
