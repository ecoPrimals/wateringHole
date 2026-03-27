# Dark Forest Beacon Genetics: Parallel Evolution Handoff

**Version**: 1.0.0  
**Date**: February 4, 2026  
**Type**: CROSS-PRIMAL EVOLUTION HANDOFF  
**Teams**: BearDog + Songbird (parallel evolution)

---

## Executive Summary

This handoff coordinates the parallel evolution of **BearDog** and **Songbird** to implement Dark Forest Beacon Genetics - a two-seed architecture that separates discovery visibility from permission verification.

**Both teams evolve simultaneously. This document ensures they evolve together.**

---

## The Problem We're Solving

### Current State (Leaky)

```
BirdSongPacket {
    "birdsong": "1.0",
    "family_id": "nat0",      ← PLAINTEXT! Attackers know who's talking
    "encrypted_payload": "..." ← Only this is encrypted
}
```

**Issue**: The `family_id` in plaintext defeats Dark Forest - attackers can see which families exist and who belongs to them.

### Target State (TRUE Dark Forest)

```
DarkForestBeacon {
    encrypted_blob: [noise to outsiders, signal to family]
    nonce: [24 bytes]
    timestamp: [replay protection]
}
```

**Goal**: Observers see only noise. No metadata leakage. Those with beacon genetics can decrypt and discover.

---

## Architecture Overview

### Two-Seed Model

```
┌────────────────────────────────────────────────────────────────────┐
│                    BEACON SEED (Discovery)                         │
│                                                                    │
│  Function: Who can see my beacons?                                │
│  Model: Social graph of meetings                                   │
│  Managed by: BearDog                                              │
│  Used by: Songbird (BirdSong broadcasts)                          │
│                                                                    │
│  Key insight: Beacon genetics are exchanged on "meeting"          │
│              Not strict inheritance - social visibility graph     │
└────────────────────────────────────────────────────────────────────┘
                              │
                              │ After beacon discovery
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                    LINEAGE SEED (Permissions)                      │
│                                                                    │
│  Function: What can they do after meeting?                        │
│  Model: Cryptographic family trust (existing)                     │
│  Managed by: BearDog (unchanged)                                  │
│  Used by: All primals for permission verification                 │
│                                                                    │
│  Key insight: Lineage is UNCHANGED - just decoupled from beacon  │
└────────────────────────────────────────────────────────────────────┘
```

---

## Current Implementation Status

### BearDog (`beardog-genetics/src/birdsong/`)

| Component | File | Status |
|-----------|------|--------|
| `BirdSongEncryption` | `encryption.rs` | ✅ ChaCha20-Poly1305 AEAD |
| `LineageKeyDerivation` | `key_derivation.rs` | ✅ HKDF from seed |
| `LineageHint` | `types.rs` | ✅ Root ID + depth ranges |
| `LineageProof` | `types.rs` | ✅ Path verification |
| `LineageChainManager` | `lineage_chain.rs` | ✅ Chain management |
| **BeaconSeed** | N/A | ❌ NOT YET IMPLEMENTED |
| **Meeting exchange** | N/A | ❌ NOT YET IMPLEMENTED |

### Songbird (`songbird-discovery/`)

| Component | File | Status |
|-----------|------|--------|
| `BirdSongPacket` | `birdsong_integration.rs` | ⚠️ Has plaintext `family_id` |
| `BirdSongProcessor` | `birdsong_integration.rs` | ✅ Encrypt/decrypt logic |
| `BirdSongEncryption` trait | `birdsong_integration.rs` | ✅ Provider abstraction |
| `BirdSongConfig` | `birdsong_integration.rs` | ✅ Mixed mode, fallback |
| `BearDogBirdSongProvider` | `beardog_birdsong_provider.rs` | ✅ BearDog integration |
| **Encrypted beacon format** | N/A | ❌ NOT YET IMPLEMENTED |
| **Multi-beacon decryption** | N/A | ❌ NOT YET IMPLEMENTED |

---

## Parallel Evolution Plan

### Phase 1: BearDog - Beacon Seed Foundation

**Owner**: BearDog Team  
**Dependency**: None (can start immediately)  
**Deliverables**: BeaconSeed struct + RPC methods

#### 1.1 Add BeaconSeed Structure

**Location**: `beardog-genetics/src/birdsong/beacon_seed.rs` (new file)

```rust
//! Beacon seed for discovery visibility (separate from lineage)

use chacha20poly1305::{aead::{Aead, KeyInit}, ChaCha20Poly1305, Nonce};
use rand::{rngs::OsRng, RngCore};
use serde::{Deserialize, Serialize};
use zeroize::Zeroizing;

/// Beacon seed for discovery encryption
/// 
/// Separate from lineage seed - controls WHO CAN SEE you,
/// not what they can do.
#[derive(Clone)]
pub struct BeaconSeed {
    /// Core seed material (32 bytes)
    seed: Zeroizing<[u8; 32]>,
    
    /// Beacon ID (public identifier derived from seed)
    beacon_id: BeaconId,
}

/// Public beacon identifier (safe to share)
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub struct BeaconId(pub [u8; 16]);

impl BeaconSeed {
    /// Generate new beacon seed
    pub fn generate() -> Self {
        let mut seed = [0u8; 32];
        OsRng.fill_bytes(&mut seed);
        let beacon_id = Self::derive_beacon_id(&seed);
        Self {
            seed: Zeroizing::new(seed),
            beacon_id,
        }
    }
    
    /// Derive from master secret (backward compatible)
    pub fn derive_from_master(master: &[u8; 64]) -> Self {
        use hkdf::Hkdf;
        use sha2::Sha256;
        
        let hk = Hkdf::<Sha256>::new(None, &master[..32]);
        let mut seed = [0u8; 32];
        hk.expand(b"ecoPrimals-beacon-v1", &mut seed).unwrap();
        
        let beacon_id = Self::derive_beacon_id(&seed);
        Self {
            seed: Zeroizing::new(seed),
            beacon_id,
        }
    }
    
    /// Get public beacon ID
    pub fn id(&self) -> &BeaconId {
        &self.beacon_id
    }
    
    /// Encrypt data for this beacon family
    pub fn encrypt(&self, plaintext: &[u8]) -> BeaconCiphertext {
        let key = self.derive_encryption_key();
        let cipher = ChaCha20Poly1305::new_from_slice(&key).unwrap();
        
        let mut nonce_bytes = [0u8; 12];
        OsRng.fill_bytes(&mut nonce_bytes);
        let nonce = Nonce::from_slice(&nonce_bytes);
        
        let ciphertext = cipher.encrypt(nonce, plaintext).unwrap();
        
        BeaconCiphertext {
            nonce: nonce_bytes,
            ciphertext,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        }
    }
    
    /// Try to decrypt beacon data
    pub fn try_decrypt(&self, encrypted: &BeaconCiphertext) -> Option<Vec<u8>> {
        let key = self.derive_encryption_key();
        let cipher = ChaCha20Poly1305::new_from_slice(&key).ok()?;
        let nonce = Nonce::from_slice(&encrypted.nonce);
        
        cipher.decrypt(nonce, encrypted.ciphertext.as_slice()).ok()
    }
    
    fn derive_beacon_id(seed: &[u8; 32]) -> BeaconId {
        use blake3::Hasher;
        let mut hasher = Hasher::new();
        hasher.update(seed);
        hasher.update(b"beacon-id-v1");
        let hash = hasher.finalize();
        let mut id = [0u8; 16];
        id.copy_from_slice(&hash.as_bytes()[..16]);
        BeaconId(id)
    }
    
    fn derive_encryption_key(&self) -> [u8; 32] {
        use hkdf::Hkdf;
        use sha2::Sha256;
        
        let hk = Hkdf::<Sha256>::new(None, self.seed.as_ref());
        let mut key = [0u8; 32];
        hk.expand(b"beacon-encrypt-v1", &mut key).unwrap();
        key
    }
}

/// Encrypted beacon data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BeaconCiphertext {
    pub nonce: [u8; 12],
    pub ciphertext: Vec<u8>,
    pub timestamp: u64,
}
```

#### 1.2 Add Beacon RPC Methods

**Location**: `beardog-tunnel/src/unix_socket_ipc/handlers/beacon_handler.rs` (new file)

```rust
// New RPC methods for beacon operations

/// beacon.generate - Generate new beacon seed
/// beacon.get_id - Get public beacon ID
/// beacon.encrypt - Encrypt data with beacon seed  
/// beacon.try_decrypt - Try to decrypt with beacon seed
/// beacon.list_known - List known beacon IDs (meetings)
/// beacon.add_known - Add a known beacon (meeting exchange)
```

**RPC Interface**:

```json
// beacon.encrypt
{
  "method": "beacon.encrypt",
  "params": {
    "plaintext": "<base64 data to encrypt>"
  }
}
// Returns: { "ciphertext": "<base64>", "nonce": "<base64>", "timestamp": 1234567890 }

// beacon.try_decrypt
{
  "method": "beacon.try_decrypt",
  "params": {
    "ciphertext": "<base64>",
    "nonce": "<base64>",
    "timestamp": 1234567890
  }
}
// Returns: { "plaintext": "<base64>" } or { "decrypted": false }

// beacon.try_decrypt_any (try all known beacons)
{
  "method": "beacon.try_decrypt_any",
  "params": {
    "ciphertext": "<base64>",
    "nonce": "<base64>",
    "timestamp": 1234567890
  }
}
// Returns: { "plaintext": "<base64>", "matched_beacon_id": "<hex>" } or { "decrypted": false }
```

#### 1.3 Environment Variables

```bash
# New variables
BEARDOG_BEACON_SEED=<hex>     # Beacon seed (discovery)
BEARDOG_LINEAGE_SEED=<hex>    # Lineage seed (permissions) - rename from BEARDOG_FAMILY_SEED

# Backward compatibility
BEARDOG_FAMILY_SEED=<hex>     # If set alone, derives both seeds from it
```

---

### Phase 2: Songbird - Dark Forest Beacons

**Owner**: Songbird Team  
**Dependency**: BearDog Phase 1 complete (beacon.encrypt/decrypt available)  
**Deliverables**: Encrypted beacon format, multi-beacon decryption

#### 2.1 New Beacon Format

**Location**: `songbird-discovery/src/dark_forest_beacon.rs` (new file)

```rust
//! Dark Forest Beacon - TRUE encrypted discovery

use serde::{Deserialize, Serialize};

/// Dark Forest beacon - completely encrypted
/// 
/// Unlike BirdSongPacket which has plaintext family_id,
/// this is fully encrypted. Observers see only noise.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DarkForestBeacon {
    /// Encrypted payload (opaque to outsiders)
    pub encrypted_payload: Vec<u8>,
    
    /// Nonce for decryption
    pub nonce: [u8; 12],
    
    /// Timestamp for replay protection
    pub timestamp: u64,
    
    /// Protocol version
    pub version: u8,
}

/// Payload inside encrypted beacon (only visible after decryption)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BeaconPayload {
    /// Beacon ID of sender
    pub beacon_id: Vec<u8>,
    
    /// Node ID
    pub node_id: String,
    
    /// Endpoints
    pub endpoints: Vec<String>,
    
    /// Capabilities hash (not full list - privacy)
    pub capabilities_hash: [u8; 32],
    
    /// Cluster ID if part of cluster
    pub cluster_id: Option<String>,
    
    /// Session ID (rotates)
    pub session_id: String,
}
```

#### 2.2 Multi-Beacon Decryption

**Location**: `songbird-discovery/src/birdsong_integration.rs` (modify)

```rust
impl BirdSongProcessor {
    /// Try to decrypt with all known beacon seeds
    /// 
    /// This is the key change: instead of checking plaintext family_id,
    /// we try decryption with each known beacon and see what works.
    pub async fn decrypt_dark_forest(
        &self,
        beacon: &DarkForestBeacon,
    ) -> Result<Option<(BeaconPayload, BeaconId)>> {
        // Get all known beacon seeds from BearDog
        let known_beacons = self.get_known_beacons().await?;
        
        // Try each known beacon
        for beacon_id in known_beacons {
            if let Some(payload) = self.try_decrypt_with_beacon(beacon, &beacon_id).await? {
                return Ok(Some((payload, beacon_id)));
            }
        }
        
        // Also try our own beacon seed
        if let Some(payload) = self.try_decrypt_with_own_beacon(beacon).await? {
            let our_id = self.get_our_beacon_id().await?;
            return Ok(Some((payload, our_id)));
        }
        
        // Can't decrypt - different beacon family (TRUE Dark Forest)
        Ok(None)
    }
    
    async fn try_decrypt_with_beacon(
        &self,
        beacon: &DarkForestBeacon,
        beacon_id: &BeaconId,
    ) -> Result<Option<BeaconPayload>> {
        // Call BearDog's beacon.try_decrypt RPC
        let response = self.beardog_client
            .call("beacon.try_decrypt", json!({
                "ciphertext": base64::encode(&beacon.encrypted_payload),
                "nonce": base64::encode(&beacon.nonce),
                "timestamp": beacon.timestamp,
                "beacon_id": hex::encode(beacon_id.0),
            }))
            .await?;
        
        if response["decrypted"].as_bool() == Some(true) {
            let plaintext = base64::decode(response["plaintext"].as_str().unwrap())?;
            let payload: BeaconPayload = serde_json::from_slice(&plaintext)?;
            Ok(Some(payload))
        } else {
            Ok(None)
        }
    }
}
```

#### 2.3 Broadcasting Dark Forest Beacons

**Location**: `songbird-discovery/src/anonymous/broadcaster.rs` (modify)

```rust
impl Broadcaster {
    /// Broadcast Dark Forest beacon (fully encrypted)
    pub async fn broadcast_dark_forest(&self) -> Result<()> {
        // Build payload
        let payload = BeaconPayload {
            beacon_id: self.get_beacon_id().await?.0.to_vec(),
            node_id: self.node_id.clone(),
            endpoints: self.get_endpoints(),
            capabilities_hash: self.hash_capabilities(),
            cluster_id: self.cluster_id.clone(),
            session_id: self.session_id.clone(),
        };
        
        // Encrypt with beacon seed via BearDog
        let encrypted = self.beardog_client
            .call("beacon.encrypt", json!({
                "plaintext": base64::encode(&serde_json::to_vec(&payload)?),
            }))
            .await?;
        
        // Create Dark Forest beacon
        let beacon = DarkForestBeacon {
            encrypted_payload: base64::decode(encrypted["ciphertext"].as_str().unwrap())?,
            nonce: base64::decode(encrypted["nonce"].as_str().unwrap())?
                .try_into()
                .unwrap(),
            timestamp: encrypted["timestamp"].as_u64().unwrap(),
            version: 2, // Version 2 = Dark Forest format
        };
        
        // Broadcast via UDP multicast
        self.multicast_send(&serde_json::to_vec(&beacon)?).await?;
        
        Ok(())
    }
}
```

---

### Phase 3: Meeting Exchange Protocol (Both Teams)

**Owner**: Both teams coordinate  
**Dependency**: Phase 1 + Phase 2 complete

#### 3.1 BearDog: Meeting Storage

```rust
// New RPC methods
"beacon.initiate_meeting"      // Generate meeting request
"beacon.complete_meeting"      // Process meeting response, store their beacon
"beacon.list_meetings"         // List all established meetings
"beacon.revoke_meeting"        // Remove a meeting (they can no longer see us)
```

#### 3.2 Songbird: Meeting Discovery Flow

```rust
// When we discover a new peer we want to meet:
// 1. Songbird sends meeting request to peer
// 2. Peer's Songbird asks their BearDog to process
// 3. BearDog exchanges beacon genetics
// 4. Both sides can now see each other's beacons
```

---

## Integration Points

### BearDog → Songbird Contract

**Songbird expects from BearDog**:

```rust
/// RPC methods Songbird will call
trait BeaconProvider {
    /// Encrypt discovery payload
    async fn beacon_encrypt(&self, plaintext: &[u8]) -> Result<BeaconCiphertext>;
    
    /// Try decrypt with our beacon seed
    async fn beacon_try_decrypt(&self, ciphertext: &BeaconCiphertext) -> Result<Option<Vec<u8>>>;
    
    /// Try decrypt with any known beacon seed
    async fn beacon_try_decrypt_any(&self, ciphertext: &BeaconCiphertext) 
        -> Result<Option<(Vec<u8>, BeaconId)>>;
    
    /// Get our beacon ID
    async fn beacon_get_id(&self) -> Result<BeaconId>;
    
    /// List known beacon IDs (peers we've met)
    async fn beacon_list_known(&self) -> Result<Vec<BeaconId>>;
}
```

### Songbird → BearDog Contract

**BearDog expects from Songbird**:

```rust
/// Events Songbird will send to BearDog
trait BeaconEvents {
    /// New peer discovered via beacon
    async fn on_peer_discovered(&self, beacon_id: BeaconId, payload: BeaconPayload);
    
    /// Meeting request received
    async fn on_meeting_request(&self, from: BeaconId, request: MeetingRequest);
    
    /// Meeting completed
    async fn on_meeting_complete(&self, with: BeaconId);
}
```

---

## Testing Strategy

### BearDog Unit Tests

```rust
#[test]
fn test_beacon_seed_generation() { ... }

#[test]
fn test_beacon_encrypt_decrypt_roundtrip() { ... }

#[test]
fn test_different_beacon_cannot_decrypt() { ... }

#[test]
fn test_beacon_id_derivation_deterministic() { ... }

#[test]
fn test_backward_compat_family_seed_derives_both() { ... }
```

### Songbird Unit Tests

```rust
#[test]
fn test_dark_forest_beacon_format() { ... }

#[test]
fn test_multi_beacon_decryption() { ... }

#[test]
fn test_unknown_beacon_returns_none() { ... }

#[test]
fn test_backward_compat_plaintext_fallback() { ... }
```

### Integration Tests (Cross-Primal)

```rust
#[tokio::test]
async fn test_dark_forest_discovery_e2e() {
    // 1. Start BearDog with beacon seed
    // 2. Start Songbird with Dark Forest enabled
    // 3. Songbird broadcasts Dark Forest beacon
    // 4. Another Songbird (same beacon genetics) receives and decrypts
    // 5. Third Songbird (different genetics) sees only noise
}

#[tokio::test]
async fn test_meeting_exchange_e2e() {
    // 1. Two nodes with different beacon seeds
    // 2. Initiate meeting
    // 3. Exchange beacon genetics
    // 4. Now both can see each other's beacons
}
```

---

## Migration Path

### Backward Compatibility

```
Phase 1: Dual format support
├── DarkForestBeacon (version: 2) → New encrypted format
├── BirdSongPacket (version: 1.0) → Legacy format with plaintext family_id
└── Songbird accepts both, broadcasts Dark Forest if available

Phase 2: Gradual migration
├── Default to Dark Forest when BearDog beacon.* available
├── Fallback to BirdSongPacket if not
└── Log deprecation warnings for legacy format

Phase 3: Legacy deprecation
├── BirdSongPacket deprecated
├── Warning on receive
└── Still accepted for compatibility

Phase 4: Full Dark Forest (optional)
├── DARK_FOREST_ONLY=true disables legacy
└── Only encrypted beacons accepted
```

---

## Environment Variables

### BearDog

```bash
# New (Dark Forest)
BEARDOG_BEACON_SEED=<hex>        # Separate beacon seed
BEARDOG_LINEAGE_SEED=<hex>       # Renamed from BEARDOG_FAMILY_SEED

# Backward compatible
BEARDOG_FAMILY_SEED=<hex>        # Derives both if alone
```

### Songbird

```bash
# New (Dark Forest)
SONGBIRD_DARK_FOREST=true        # Enable Dark Forest beacons
SONGBIRD_LEGACY_FALLBACK=true    # Accept legacy BirdSongPacket

# Existing (unchanged)
BIRDSONG_ENABLED=true
BIRDSONG_FALLBACK_PLAINTEXT=true
```

---

## Success Criteria

### BearDog Complete When:

- [ ] `BeaconSeed` struct implemented with encrypt/decrypt
- [ ] `beacon.*` RPC methods available
- [ ] `BEARDOG_BEACON_SEED` environment variable supported
- [ ] Backward compatible with `BEARDOG_FAMILY_SEED`
- [ ] Unit tests pass
- [ ] Builds on x86_64 and aarch64

### Songbird Complete When:

- [ ] `DarkForestBeacon` format implemented
- [ ] Multi-beacon decryption working
- [ ] Broadcasting Dark Forest beacons when BearDog available
- [ ] Fallback to legacy format when not
- [ ] Unit tests pass
- [ ] Integration tests with BearDog pass

### Cross-Primal Complete When:

- [ ] E2E test: Same beacon family discovers each other
- [ ] E2E test: Different beacon family sees noise
- [ ] E2E test: Meeting exchange works
- [ ] Both deploy to Pixel 8a successfully
- [ ] TRUE Dark Forest validated (network capture shows only encrypted blobs)

---

## Timeline Coordination

```
Week 1:
├── BearDog: BeaconSeed struct + encrypt/decrypt
├── Songbird: DarkForestBeacon format definition
└── Both: Agree on RPC interface

Week 2:
├── BearDog: beacon.* RPC methods
├── Songbird: Multi-beacon decryption logic
└── Both: Unit tests

Week 3:
├── BearDog: Environment variable support
├── Songbird: Broadcasting Dark Forest beacons
└── Both: Integration testing

Week 4:
├── Both: Cross-primal E2E tests
├── Both: Pixel deployment test
└── Both: Documentation update
```

---

## Contact Points

**BearDog Questions**: Check `beardog-genetics/src/birdsong/` for existing patterns

**Songbird Questions**: Check `songbird-discovery/src/birdsong_integration.rs` for existing patterns

**Cross-Primal Coordination**: Update `wateringHole/DARK_FOREST_BEACON_GENETICS_STANDARD.md`

---

## Appendix: Full Spec Reference

See: `/path/to/ecoPrimals/phase2/biomeOS/specs/DARK_FOREST_BEACON_GENETICS_SPEC.md`

---

**Handoff Status**: READY FOR PARALLEL IMPLEMENTATION

*"Beacon genetics is who you've met. Lineage is security. BearDog manages both seeds. Songbird uses them for TRUE Dark Forest discovery."*
