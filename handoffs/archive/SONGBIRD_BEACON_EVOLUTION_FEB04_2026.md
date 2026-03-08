# Songbird Discovery & Networking Evolution Handoff
## February 4, 2026

**From**: biomeOS Validation  
**To**: Songbird Maintainers  
**Priority**: HIGH - Blocks peer discovery and beacon exchange  
**Status**: Critical config bug + missing methods

---

## Executive Summary

Songbird is biomeOS's networking primal responsible for:
1. Peer-to-peer connectivity (BirdSong/Dark Forest)
2. Beacon exchange between nodes
3. Network discovery and routing

**Critical Issues Found**:
1. ❌ Wrong BearDog socket path (hardcoded `/tmp/neural-api-nat0.sock`)
2. ❌ Missing standard `health` and `identity` methods
3. ❌ Missing `rpc.discover` for capability discovery
4. ❌ Missing `beacon_exchange` for beacon meetings
5. ❌ Missing `encrypt_discovery` / `decrypt_discovery`

---

## Critical Bug: BearDog Socket Path

### Current (WRONG)

```rust
// Songbird's current code
const BEARDOG_SOCKET: &str = "/tmp/neural-api-nat0.sock";
```

### Required (Use XDG)

```rust
fn get_beardog_socket(family_id: &str) -> PathBuf {
    let xdg_runtime = std::env::var("XDG_RUNTIME_DIR")
        .unwrap_or_else(|_| format!("/run/user/{}", unsafe { libc::getuid() }));
    PathBuf::from(xdg_runtime)
        .join("biomeos")
        .join(format!("beardog-{}.sock", family_id))
}
```

**Or**: Use `rpc.discover` to dynamically find BearDog:

```rust
async fn find_beardog(&self) -> Result<PathBuf> {
    // Query biomeOS for BearDog location
    let response = self.call_biomeos("rpc.discover", json!({
        "capability": "beacon.get_id"
    })).await?;
    
    Ok(PathBuf::from(response["socket_path"].as_str().unwrap()))
}
```

---

## Methods to Implement

### 1. Standard Methods (Required for ALL Primals)

#### `health` - Health Check

```json
// Request
{"jsonrpc": "2.0", "method": "health", "params": {}, "id": 1}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "status": "healthy",
    "uptime_seconds": 3600,
    "peers_connected": 2,
    "beardog_connected": true
  },
  "id": 1
}
```

#### `identity` - Self-Identification

```json
// Request
{"jsonrpc": "2.0", "method": "identity", "params": {}, "id": 1}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "primal": "songbird",
    "version": "0.1.0",
    "family_id": "nat0",
    "capabilities": [
      "network.broadcast",
      "network.listen",
      "network.beacon_exchange",
      "encrypt_discovery",
      "decrypt_discovery"
    ]
  },
  "id": 1
}
```

#### `rpc.discover` - Capability Discovery

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "rpc.discover",
  "params": {},
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "methods": [
      {
        "name": "health",
        "params": [],
        "description": "Health check"
      },
      {
        "name": "network.beacon_exchange",
        "params": ["endpoint", "beacon_id", "beacon_seed_encrypted"],
        "description": "Exchange beacon seeds with peer"
      }
      // ... all methods
    ]
  },
  "id": 1
}
```

---

### 2. Network Methods (Songbird-Specific)

#### `network.beacon_exchange` - Exchange Beacons with Peer

**Purpose**: Perform beacon seed exchange during a "meeting"

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "network.beacon_exchange",
  "params": {
    "endpoint": "192.0.2.100:8080",
    "beacon_id": "our_beacon_id_here",
    "beacon_seed_encrypted": "encrypted_seed_for_peer"
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "peer_beacon_id": "peer_beacon_id_here",
    "peer_seed_encrypted": "encrypted_seed_from_peer",
    "peer_family_hint": "8ff3b864a4bc589a"
  },
  "id": 1
}
```

**Implementation**:
```rust
async fn beacon_exchange(&self, params: BeaconExchangeParams) -> Result<BeaconExchangeResponse> {
    // 1. Connect to peer's Songbird
    let peer_conn = self.connect(&params.endpoint).await?;
    
    // 2. Send our beacon info
    let request = ExchangeRequest {
        beacon_id: params.beacon_id,
        encrypted_seed: params.beacon_seed_encrypted,
    };
    
    // 3. Receive peer's beacon info
    let peer_response = peer_conn.exchange_beacons(request).await?;
    
    Ok(BeaconExchangeResponse {
        success: true,
        peer_beacon_id: peer_response.beacon_id,
        peer_seed_encrypted: peer_response.encrypted_seed,
        peer_family_hint: peer_response.family_hint,
    })
}
```

---

#### `network.broadcast` - Broadcast Discovery Message

**Purpose**: Broadcast an encrypted beacon to the network

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "network.broadcast",
  "params": {
    "payload_encrypted": "encrypted_beacon_broadcast",
    "ttl": 60,
    "channel": "dark_forest"
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "broadcast_id": "unique_id",
    "peers_reached": 3
  },
  "id": 1
}
```

---

#### `network.listen` - Listen for Broadcasts

**Purpose**: Listen for encrypted beacon broadcasts

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "network.listen",
  "params": {
    "channel": "dark_forest",
    "timeout_seconds": 30
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "broadcasts": [
      {
        "payload_encrypted": "encrypted_data",
        "received_at": "2026-02-04T12:00:00Z",
        "source_hint": "metadata_if_available"
      }
    ]
  },
  "id": 1
}
```

---

### 3. Encryption Methods (Wrapper for BearDog)

These methods call BearDog internally:

#### `encrypt_discovery` - Encrypt for Discovery Broadcast

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "encrypt_discovery",
  "params": {
    "payload": {"type": "beacon_announce", "beacon_id": "xxx"},
    "use_beacon_seed": true
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "encrypted_b64": "base64_encrypted_data"
  },
  "id": 1
}
```

**Implementation**:
```rust
async fn encrypt_discovery(&self, params: EncryptParams) -> Result<EncryptResponse> {
    // Call BearDog for actual encryption
    let beardog_socket = self.get_beardog_socket().await?;
    let beardog_response = self.call_primal(
        beardog_socket,
        "beacon.encrypt",
        json!({
            "plaintext_b64": base64::encode(serde_json::to_vec(&params.payload)?),
        })
    ).await?;
    
    Ok(EncryptResponse {
        encrypted_b64: beardog_response["ciphertext_b64"].as_str().unwrap().to_string()
    })
}
```

---

#### `decrypt_discovery` - Decrypt Discovery Broadcast

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "decrypt_discovery",
  "params": {
    "encrypted_b64": "encrypted_data_here",
    "known_beacon_seeds": ["seed1_hex", "seed2_hex"]
  },
  "id": 1
}

// Response (success)
{
  "jsonrpc": "2.0",
  "result": {
    "decrypted": true,
    "payload": {"type": "beacon_announce", "beacon_id": "xxx"},
    "matched_seed_index": 1
  },
  "id": 1
}

// Response (no matching seed)
{
  "jsonrpc": "2.0",
  "result": {
    "decrypted": false,
    "payload": null,
    "matched_seed_index": null
  },
  "id": 1
}
```

**Implementation**:
```rust
async fn decrypt_discovery(&self, params: DecryptParams) -> Result<DecryptResponse> {
    let beardog_socket = self.get_beardog_socket().await?;
    
    // Try each known beacon seed
    for (index, seed_hex) in params.known_beacon_seeds.iter().enumerate() {
        let result = self.call_primal(
            &beardog_socket,
            "beacon.try_decrypt",
            json!({
                "ciphertext_b64": params.encrypted_b64,
                "seed_hex": seed_hex
            })
        ).await?;
        
        if result["decrypted"].as_bool().unwrap_or(false) {
            return Ok(DecryptResponse {
                decrypted: true,
                payload: serde_json::from_slice(
                    &base64::decode(result["plaintext_b64"].as_str().unwrap())?
                )?,
                matched_seed_index: Some(index),
            });
        }
    }
    
    Ok(DecryptResponse {
        decrypted: false,
        payload: None,
        matched_seed_index: None,
    })
}
```

---

## Architecture: Songbird + BearDog Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                          biomeOS                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              BeaconGeneticsManager                         │ │
│  │  (Orchestrates meetings, manages address book)             │ │
│  └───────────────────────┬────────────────────────────────────┘ │
│                          │ capability.call()                    │
│                          ▼                                      │
│  ┌───────────────────────┴────────────────────────────────────┐ │
│  │           CapabilityTranslationRegistry                    │ │
│  │                                                            │ │
│  │  "beacon.*"     → BearDog                                  │ │
│  │  "network.*"    → Songbird                                 │ │
│  │  "encrypt_discovery" → Songbird (calls BearDog internally) │ │
│  └───────────────────────┬────────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
    ┌─────────────┐                 ┌─────────────┐
    │   BearDog   │◄───────────────►│  Songbird   │
    │             │  JSON-RPC       │             │
    │ • beacon.*  │                 │ • network.* │
    │ • lineage.* │                 │ • encrypt_  │
    │ • crypto.*  │                 │   discovery │
    └─────────────┘                 └─────────────┘
```

---

## Test Commands

After implementing, verify with:

```bash
FAMILY_ID=nat0
SOCKET="/run/user/$(id -u)/biomeos/songbird-$FAMILY_ID.sock"

# Test health
echo '{"jsonrpc":"2.0","method":"health","params":{},"id":1}' | nc -U $SOCKET

# Test identity  
echo '{"jsonrpc":"2.0","method":"identity","params":{},"id":1}' | nc -U $SOCKET

# Test rpc.discover
echo '{"jsonrpc":"2.0","method":"rpc.discover","params":{},"id":1}' | nc -U $SOCKET

# Test encrypt_discovery
echo '{"jsonrpc":"2.0","method":"encrypt_discovery","params":{"payload":{"test":"data"}},"id":1}' | nc -U $SOCKET

# Test beacon_exchange (requires peer)
echo '{"jsonrpc":"2.0","method":"network.beacon_exchange","params":{"endpoint":"peer:8080","beacon_id":"xxx"},"id":1}' | nc -U $SOCKET
```

---

## Integration Flow: USB ↔ Pixel Discovery

Once both BearDog and Songbird are evolved:

```
USB Device                                      Pixel Device
┌─────────────┐                                ┌─────────────┐
│ biomeOS     │                                │ biomeOS     │
│             │  1. Network broadcast          │             │
│ Songbird    │───────────────────────────────►│ Songbird    │
│             │                                │             │
│ BearDog     │  2. Encrypted beacon ID        │ BearDog     │
│             │◄───────────────────────────────│             │
│             │                                │             │
│             │  3. beacon_exchange (meeting)  │             │
│ Songbird    │◄──────────────────────────────►│ Songbird    │
│             │                                │             │
│ BearDog     │  4. Decrypt peer seed          │ BearDog     │
│             │◄───────────────────────────────│             │
│             │                                │             │
│             │  5. Verify lineage             │             │
│ BearDog     │◄──────────────────────────────►│ BearDog     │
│             │  (Same family? Accept)         │             │
└─────────────┘                                └─────────────┘
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `biomeOS/specs/BEACON_CAPABILITY_TRANSLATIONS.md` | Capability → method mapping |
| `biomeOS/specs/BIRDSONG_DARK_FOREST_PROTOCOL.md` | Network protocol spec |
| `biomeOS/crates/biomeos-spore/src/beacon_genetics/` | biomeOS beacon manager |
| `biomeOS/graphs/tower_atomic_bootstrap.toml` | Tower deployment (Songbird config) |

---

## Implementation Priority

1. **FIX FIRST**: BearDog socket path (config bug)
2. **THEN**: Standard methods (`health`, `identity`, `rpc.discover`)
3. **THEN**: Core network methods (`network.beacon_exchange`)
4. **THEN**: Encryption wrappers (`encrypt_discovery`, `decrypt_discovery`)
5. **FINALLY**: Full `network.broadcast` / `network.listen`

---

## Dependencies

Songbird depends on:
- **BearDog** implementing `beacon.*` methods (see `BEARDOG_BEACON_EVOLUTION_FEB04_2026.md`)
- Network stack for peer connectivity
- mDNS or similar for local peer discovery (optional, can use direct IP)

---

**Handoff Date**: February 4, 2026  
**Contact**: biomeOS Neural API team  
**Validation Script**: `biomeOS/scripts/validate_beacon_discovery.sh`
