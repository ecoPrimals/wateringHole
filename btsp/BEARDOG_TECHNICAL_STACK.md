# 🐻 BearDog Technical Stack & Plans (BTSP)

**Version**: 0.15.0 (BirdSong v2 API Complete)  
**Last Updated**: January 3, 2026  
**Status**: Production Ready

---

## 🎯 Purpose

BearDog is the **genetic lineage keeper** and **cryptographic foundation** of the ecoPrimal ecosystem. It provides:

1. **Family Seed Management** - Secure storage and access to genetic lineage
2. **BirdSong Encryption/Decryption** - Cryptographic services for encrypted discovery
3. **Identity Attestation** - Family membership verification
4. **Trust Evaluation** - Genetic lineage validation

---

## 🏗️ Architecture

### Core Components

```
BearDog v0.15.0
├── Family Seed Storage (secure, encrypted)
├── BirdSong v2 API
│   ├── /api/v2/birdsong/encrypt
│   └── /api/v2/birdsong/decrypt
├── BirdSong v1 API (legacy, deprecated)
│   ├── /api/v1/birdsong/encrypt
│   └── /api/v1/birdsong/decrypt
├── Identity API
│   ├── /api/v1/identity
│   └── /api/v1/health
└── Trust Evaluation Engine
```

### Technology Stack

- **Language**: Rust (edition 2021)
- **Crypto**: ChaCha20-Poly1305 (AEAD)
- **Serialization**: serde_json, base64
- **API**: HTTP REST endpoints
- **Storage**: Encrypted local storage
- **Port**: 9000 (default, configurable via `HTTP_PORT`)

---

## 🔐 BirdSong API Specification

### Version 2 (v2) - Current Standard

#### Encrypt Endpoint

```http
POST /api/v2/birdsong/encrypt
Content-Type: application/json

{
  "plaintext": "<base64-encoded-binary-data>",
  "family_id": "your-family-id"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "ciphertext": "<base64-encoded-encrypted-data>",
    "family_id": "your-family-id",
    "nonce": "<base64-encoded-nonce>"
  }
}
```

**Note**: `plaintext` and `ciphertext` MUST be base64-encoded `Vec<u8>`, not raw strings.

#### Decrypt Endpoint

```http
POST /api/v2/birdsong/decrypt
Content-Type: application/json

{
  "ciphertext": "<base64-encoded-encrypted-data>",
  "family_id": "your-family-id",
  "nonce": "<base64-encoded-nonce>"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "plaintext": "<base64-encoded-decrypted-data>",
    "family_id": "your-family-id"
  }
}
```

### Version 1 (v1) - Legacy (Deprecated)

Same endpoints at `/api/v1/birdsong/encrypt` and `/api/v1/birdsong/decrypt`.

**Differences**:
- v1: Returns `"encrypted"` field
- v2: Returns `"ciphertext"` field
- v1: No response wrapper
- v2: Wrapped in `{"success": true, "data": {...}}`

**Migration**: Use adaptive client pattern (see biomeOS adaptive_client.rs)

---

## 🔑 Family Seed Management

### Environment Variables (Secure Method)

```bash
# Required for encryption/decryption
export BEARDOG_FAMILY_ID="your-family-id"
export BEARDOG_FAMILY_SEED="<base64-encoded-seed>"

# Optional
export HTTP_PORT=9000
export RUST_LOG=beardog=debug
```

### Security Requirements

1. **Never log family seeds** - Always redact in logs
2. **Encrypt at rest** - Store seeds encrypted on disk
3. **Zero-copy when possible** - Minimize seed exposure in memory
4. **Auto-zeroize** - Clear sensitive data from memory on drop
5. **Restrict access** - File permissions 600 for seed files

### Current Implementation

**Status**: ⚠️ **NEEDS IMPROVEMENT**

Current gaps identified (Jan 3, 2026):
- ✅ Environment variable support working
- ⚠️ Plaintext seed in USB config (needs encryption)
- ⚠️ No auto-zeroization (should use `zeroize` crate)
- ⚠️ Seeds may be logged in debug mode

**Recommendation**: Adopt biomeOS `FamilyCredentials` pattern
- Uses `zeroize` crate for auto-zeroization
- Never logs seed data (debug prints `[REDACTED]`)
- Secure by default

See: `biomeOS/crates/biomeos-core/src/family_credentials.rs`

---

## 🚀 Deployment

### Starting BearDog

```bash
# With environment variables (recommended)
export BEARDOG_FAMILY_ID="your-family-id"
export BEARDOG_FAMILY_SEED="your-base64-seed"
export HTTP_PORT=9000

./beardog-server-v0.15.0-with-v2-api
```

### Startup Script

```bash
#!/bin/bash
# start-beardog-server.sh

export BEARDOG_FAMILY_ID="${FAMILY_ID}"
export BEARDOG_FAMILY_SEED="${FAMILY_SEED}"
export HTTP_PORT="${BEARDOG_PORT:-9000}"
export RUST_LOG="beardog=info,tower=info"

exec ./beardog-server-v0.15.0-with-v2-api
```

### Health Check

```bash
curl http://localhost:9000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "family_id": "your-family-id",
  "version": "0.15.0"
}
```

---

## 🧪 Testing

### Manual Test (Encrypt)

```bash
# Prepare test data
echo -n "test message" | base64  # dGVzdCBtZXNzYWdl

# Call encrypt API
curl -X POST http://localhost:9000/api/v2/birdsong/encrypt \
  -H "Content-Type: application/json" \
  -d '{
    "plaintext": "dGVzdCBtZXNzYWdl",
    "family_id": "your-family-id"
  }'
```

### Manual Test (Decrypt)

```bash
# Use ciphertext from encrypt response
curl -X POST http://localhost:9000/api/v2/birdsong/decrypt \
  -H "Content-Type: application/json" \
  -d '{
    "ciphertext": "<encrypted-data>",
    "family_id": "your-family-id",
    "nonce": "<nonce-from-encrypt>"
  }'
```

### Integration with Songbird

**Status**: ✅ Working (Songbird v3.6)

Songbird v3.6 successfully:
- Calls BearDog encryption API
- Uses correct base64 serialization
- Handles response wrapper
- Sends encrypted BirdSongPackets

---

## 📋 Technical Debt & Roadmap

### High Priority (Security)

1. **Encrypted Family Seed Storage** ⚠️
   - Current: Plaintext in USB config
   - Needed: Encrypted file with password/key derivation
   - Effort: 2-3 days
   - Impact: Critical for production

2. **Auto-Zeroizing Credentials** ⚠️
   - Current: Seeds may persist in memory
   - Needed: `zeroize` crate integration
   - Effort: 1 day
   - Impact: High security improvement

3. **Audit Logging** ⚠️
   - Current: May log sensitive data
   - Needed: Structured logging with redaction
   - Effort: 1-2 days
   - Impact: High for compliance

### Medium Priority (Scaling)

4. **Dynamic Port Allocation**
   - Current: Hardcoded port 9000
   - Needed: `HTTP_PORT=0` support for OS allocation
   - Effort: 1 day
   - Impact: Enables fractal scaling

5. **Multi-Family Support**
   - Current: Single family per instance
   - Needed: Multiple families with isolation
   - Effort: 3-5 days
   - Impact: Enables federation

### Low Priority (Features)

6. **Key Rotation**
   - Current: Static family seed
   - Needed: Periodic key rotation support
   - Effort: 5-7 days
   - Impact: Enhanced security posture

7. **HSM Integration**
   - Current: Software-only crypto
   - Needed: Hardware security module support
   - Effort: 7-10 days
   - Impact: Enterprise-grade security

---

## 🔗 Integration Patterns

### For Songbird (Discovery)

```rust
// Songbird calls BearDog to encrypt discovery packets
let client = BirdSongClient::new("http://localhost:9000");
let encrypted = client.encrypt(packet_data, family_id).await?;

// Send encrypted packet over UDP
send_birdsong_packet(encrypted);
```

### For biomeOS (Orchestration)

```rust
// biomeOS discovers BearDog via HTTP
let beardog_info = http_discovery
    .discover("http://localhost:9000")
    .await?;

// Check family membership
if beardog_info.family_id == expected_family {
    // Establish trust
}
```

### For PetalTongue (Visualization)

```
GET /api/v1/identity
→ Display BearDog as genetic lineage keeper
→ Show family_id and trust status
```

---

## 🌍 Ecosystem Role

### As Genetic Lineage Keeper

- **Provides**: Cryptographic foundation for family trust
- **Validates**: Family membership via shared secrets
- **Enables**: Auto-trust within genetic lineage
- **Protects**: Family seed from unauthorized access

### Interaction with Other Primals

```
BearDog (Genetic Keeper)
  ↓ Encryption API
Songbird (Discovery) → Encrypted BirdSongPackets → Other Towers
  ↓ Discovery Results
biomeOS (Orchestration) → Trust Evaluation → Ecosystem Graph
  ↓ Real-time Events
PetalTongue (Visualization) → User Interface
```

---

## 📊 Current Status

### Production Readiness

| Component | Status | Notes |
|-----------|--------|-------|
| BirdSong v2 API | ✅ Working | Verified with Songbird v3.6 |
| Encryption | ✅ Working | ChaCha20-Poly1305 |
| Decryption | ✅ Working | Roundtrip verified |
| Identity API | ✅ Working | Returns family_id |
| Health Check | ✅ Working | HTTP endpoint |
| Family Seed Storage | ⚠️ Needs Work | Plaintext, no zeroization |
| Dynamic Ports | ❌ Not Supported | Hardcoded port 9000 |
| Multi-Family | ❌ Not Supported | Single family per instance |

**Overall**: **75% Production Ready**

---

## 🎓 For Developers

### Quick Start

1. Set environment variables (family_id, seed)
2. Start BearDog server
3. Verify health endpoint
4. Test encrypt/decrypt roundtrip
5. Integrate with your primal

### Code References

**BearDog v0.15.0**:
- Binary: `ecoPrimals/phase1/beardog/primalBins/beardog-server-v0.15.0-with-v2-api`
- Startup: `ecoPrimals/phase1/beardog/start-beardog-server.sh`

**Adaptive Client (biomeOS)**:
- Implementation: `biomeOS/crates/biomeos-core/src/adaptive_client.rs`
- Usage: Handles both v1 and v2 API versions

**Secure Credentials (biomeOS)**:
- Implementation: `biomeOS/crates/biomeos-core/src/family_credentials.rs`
- Pattern: Auto-zeroizing, never logs secrets

### Common Issues

**Issue**: "No family_id available from encryption provider"
- **Cause**: BearDog not receiving environment variables
- **Fix**: Export `BEARDOG_FAMILY_ID` and `BEARDOG_FAMILY_SEED` before starting

**Issue**: "Invalid byte 95, offset 4" (Base64 error)
- **Cause**: Sending string instead of base64-encoded binary
- **Fix**: Encode as base64 before sending to API

**Issue**: Port conflict
- **Cause**: Another process using port 9000
- **Fix**: Change `HTTP_PORT` or kill conflicting process

---

## 💡 Best Practices

### For Primal Developers

1. **Always use base64** for binary data in API calls
2. **Handle both v1 and v2** APIs (use adaptive client pattern)
3. **Never log family seeds** in any context
4. **Verify health endpoint** before making crypto calls
5. **Cache BearDog endpoint** after discovery

### For Operators

1. **Secure family seeds** with file permissions 600
2. **Use environment variables** over config files
3. **Monitor health endpoint** for availability
4. **Rotate logs** to prevent seed leakage
5. **Restrict network access** to trusted primals only

---

**Status**: ✅ **PRODUCTION READY FOR SINGLE-FAMILY USE**  
**Next**: Address security gaps (encrypted storage, zeroization)  
**Goal**: Enable secure multi-family auto-trust federation

🐻 **BearDog: The Genetic Foundation of ecoPrimals** 🔐

