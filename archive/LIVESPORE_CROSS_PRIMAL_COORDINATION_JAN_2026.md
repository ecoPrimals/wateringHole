# 🌱 LiveSpore Cross-Primal Coordination

**Date**: January 13, 2026  
**Initiative**: LiveSpore Multi-Callsign Tag System  
**Coordinating Primals**: BiomeOS → BearDog → Songbird  
**Status**: ✅ **ACTIVE - WEEK 1 IN PROGRESS**

---

## 🎯 EXECUTIVE SUMMARY

**What**: BearDog (security primal) identified that LiveSpore (BiomeOS self-replicating deployment) needs multi-callsign tag support for institutional NAT routing (e.g., universities, research institutions).

**Why**: Enable users to leverage institutional networks instead of cloud services, achieving:
- Zero cloud costs (use university/institution NAT)
- Full sovereignty (private routing encrypted for genetic family)
- Multi-identity per node (institutional + personal + federation)

**Who**: 
- **BiomeOS**: Upstream coordination, LiveSpore architecture
- **BearDog**: Genetic lineage, key derivation, genesis ceremony
- **Songbird**: Discovery protocol (BirdSong) evolution to v3.0

**When**: 6-week evolution (Jan 13 - Feb 24, 2026)

**Outcome**: Songbird ships BirdSong v3.0 with multi-tag support, enabling LiveSpore first-boot personalization.

---

## 🏗️ ARCHITECTURAL OVERVIEW

### The Multi-Callsign Tag System

**Current** (BirdSong v2.0):
```json
{
  "version": 2,
  "family_id": "your-family-id",  // ← Single tag (plaintext)
  "encrypted_payload": {
    "ciphertext": "<encrypted>",
    "nonce": "...",
    "algorithm": "ChaCha20-Poly1305"
  }
}
```

**Evolution** (BirdSong v3.0):
```json
{
  "version": 3,
  "tags": [  // ← Multiple public callsigns
    {
      "tag": "UNIV",
      "purpose": "Institutional",
      "priority": 100
    },
    {
      "tag": "researcher-personal",
      "purpose": "Personal",
      "priority": 90
    }
  ],
  "encrypted_payload": {
    "ciphertext": "<routing-metadata-encrypted-for-family>",
    "nonce": "...",
    "algorithm": "ChaCha20-Poly1305"
  },
  "sequence": 12345,       // ← NEW: Replay protection
  "sender_id": "node-001", // ← NEW: Sequence tracking
  "key_epoch": 42          // ← NEW: Key rotation support
}
```

**Inside Encrypted Payload** (only genetic family can decrypt):
```json
{
  "routing_metadata": {
    "primary_endpoint": "192.0.2.100:8080",  // Private!
    "nat_config": {
      "traversal_method": "Institutional"  // Use university network
    }
  },
  "identity_attestations": {
    "genetic_lineage": "<hash>",
    "family_id": "your-family-id"
  }
}
```

### Key Insight: Public Discovery + Private Routing

**Public** (visible to all):
- Tags: "UNIV", "Personal", "Federation"
- Purpose hints (for routing decisions)
- Priorities (which tag to prefer)

**Private** (encrypted for genetic family only):
- Actual IP addresses and ports
- NAT traversal configuration
- Identity attestations
- Genetic lineage proofs

**Result**: 
- ✅ Institutional networks see legitimate public tags
- ✅ Only genetic family can route to private endpoints
- ✅ Full sovereignty maintained

---

## USE CASE: University Graduate Student

**User**: Grad student at a research university with basement HPC

**Configuration**:
```yaml
tags:
  - tag: "UNIV"
    purpose: Institutional
    priority: 100
    routing:
      primary_endpoint: "192.0.2.100:8080"  # Encrypted!
      nat_config:
        traversal_method: Institutional
  
  - tag: "researcher-lab"
    purpose: Personal
    priority: 90
    routing:
      primary_endpoint: "192.0.2.100:8080"  # Same HPC, different tag
```

**Scenarios**:

1. **Researcher's Sibling (Same Genetic Family)**:
   - Sees tags: ["UNIV", "researcher-lab"]
   - Decrypts payload with genetic key
   - Reads routing: 192.0.2.100:8080
   - Connects via university network (priority 100)
   - Auto-trusted (same lineage)

2. **Random University Student**:
   - Sees tags: ["UNIV", "researcher-lab"]
   - Tries to decrypt with their genetic key ❌
   - Decryption fails (different lineage)
   - Ignores packet

3. **ML Federation Member**:
   - Researcher adds "ML-Federation" tag with different routing
   - Federation member decrypts with federation key ✅
   - Gets limited access (ML service only, not personal HPC)
   - Graduated trust (federation, not family)

**Result**:
- Zero cloud costs (uses university network)
- Full sovereignty (family-only routing)
- Multi-identity (institutional + personal + federation)
- University network sees legitimate institutional tag (allowed)

---

## 🤝 CROSS-PRIMAL RESPONSIBILITIES

### BiomeOS (Upstream Coordination)

**Provides**:
- ✅ LiveSpore architecture specification
- ✅ Primal aggregator API (list local primals)
- ✅ First-boot integration hooks

**Timeline**:
- Week 4-5: Joint testing with Songbird + BearDog
- Week 6: LiveSpore first-boot integration

**Status**: Coordinating, providing requirements

---

### BearDog (Security Primal)

**Provides to Songbird**:
1. ✅ **Concurrent Test Helpers** (Week 1 - ready now)
   - Location: `beardog/tests/support/concurrent_helpers.rs`
   - Proven to deliver 5x test speedup
   - Already production-tested in BearDog

2. ⏳ **Key Derivation API** (Week 3 - in development)
   ```rust
   POST /api/v1/lineage/derive-key
   {
     "genetic_lineage": "<hash>",
     "epoch": 12345,
     "purpose": "birdsong-encryption"
   }
   Response: {
     "key": "<32-byte-hex>",
     "epoch": 12345,
     "valid_until": 1735086400
   }
   ```
   - Needed by: January 27, 2026
   - Purpose: Enable BirdSong key rotation

3. ✅ **Genesis Integration** (Week 4 - already exists)
   - SoloKey witness verification
   - Hardware entropy collection
   - Genetic lineage generation

**Receives from Songbird**:
- BirdSong v3.0 specification (Week 2)
- Tag management API (Week 2-3)
- Joint testing participation (Week 5)

**Timeline**:
- Week 1: Provide `concurrent_helpers.rs` ✅
- Week 3: Ship key derivation API
- Week 4: Genesis ceremony integration
- Week 5: Joint testing
- Week 6: Production validation

**Status**: Actively supporting, on schedule

---

### Songbird (Discovery Primal)

**Evolution Work**:
1. **Week 1** (Jan 13-20): Concurrent test evolution
   - Copy BearDog's helpers
   - Replace 86 `sleep` calls
   - Replace 21 `Arc<Mutex>` instances
   - Target: 5x faster tests

2. **Weeks 2-3** (Jan 20 - Feb 3): BirdSong v3.0 multi-tag
   - Protocol evolution (tags support)
   - Routing metadata formalization
   - Tag management API
   - Maintain v2 compatibility

3. **Weeks 3-4** (Jan 27 - Feb 10): Security hardening
   - Key rotation (BearDog integration)
   - Replay protection (sequence numbers)
   - Rate limiting (adaptive beaconing)

4. **Weeks 4-5** (Feb 3-17): BiomeOS integration
   - Genesis ceremony CLI (tag configuration)
   - NUCLEUS metadata support
   - Joint testing

5. **Week 5** (Feb 10-17): Test coverage expansion
   - Multi-tag discovery tests
   - Security tests
   - Target: 90%+ coverage

6. **Week 6** (Feb 17-24): Production hardening
   - Performance benchmarks
   - Migration guide (v2 → v3)
   - Security audit
   - **SHIP: v3.23.0**

**Provides**:
- BirdSong v3.0 protocol (multi-tag discovery)
- Tag management API (runtime configuration)
- Production-grade security (rotation, replay protection)

**Receives**:
- BearDog's concurrent helpers (Week 1)
- Key derivation API (Week 3)
- BiomeOS aggregator API (Week 4)

**Timeline**: 6 weeks, shipping February 24, 2026

**Status**: ✅ Evolution approved, Week 1 in progress

---

## 📅 COORDINATED TIMELINE

### Week 1 (Jan 13-20): Foundation
- **Songbird**: Copy concurrent helpers, refactor tests
- **BearDog**: Provide helpers, start key derivation API
- **BiomeOS**: Review architecture, prepare aggregator
- **Milestone**: 5x faster Songbird tests

### Week 2 (Jan 20-27): Protocol Evolution
- **Songbird**: BirdSong v3.0 protocol design
- **BearDog**: Continue key derivation API
- **BiomeOS**: Finalize NUCLEUS metadata requirements
- **Milestone**: BirdSong v3.0 spec published

### Week 3 (Jan 27 - Feb 3): Multi-Tag Implementation
- **Songbird**: Implement multi-tag support + tag API
- **BearDog**: Ship key derivation API ⚠️ **CRITICAL**
- **BiomeOS**: Prepare aggregator integration
- **Milestone**: Multi-tag discovery working

### Week 4 (Feb 3-10): Security Hardening
- **Songbird**: Key rotation + replay protection
- **BearDog**: Validate key derivation integration
- **BiomeOS**: Genesis ceremony coordination
- **Milestone**: Production-grade security

### Week 5 (Feb 10-17): Integration & Testing
- **Songbird**: BiomeOS integration, test coverage
- **BearDog**: Joint testing, key rotation validation
- **BiomeOS**: NUCLEUS discovery testing
- **Milestone**: 90%+ coverage, all tests green

### Week 6 (Feb 17-24): Production Release
- **Songbird**: Performance benchmarks, migration guide, audit
- **BearDog**: Production validation
- **BiomeOS**: LiveSpore first-boot integration
- **Milestone**: 🎉 **Songbird v3.23.0 SHIPPED**

---

## 🚧 DEPENDENCIES & RISKS

### Critical Path

```
BearDog concurrent_helpers.rs (Week 1)
  ↓
Songbird concurrent evolution (Week 1)
  ↓
BearDog key derivation API (Week 3) ⚠️ CRITICAL
  ↓
Songbird key rotation (Week 3-4)
  ↓
BiomeOS + BearDog + Songbird joint testing (Week 5)
  ↓
Songbird v3.23.0 production release (Week 6)
```

### Key Dependencies

**⚠️ CRITICAL** - BearDog Key Derivation API (Week 3):
- Needed by: January 27, 2026
- Blocks: Songbird key rotation implementation
- **Mitigation**: Weekly syncs to track progress, BearDog commits to delivery

**MEDIUM** - BiomeOS Aggregator API:
- Needed by: February 3, 2026
- Blocks: NUCLEUS metadata integration
- **Mitigation**: API already exists, just needs documentation

**LOW** - Joint Testing Coordination (Week 5):
- Complexity: Multi-primal coordination
- **Mitigation**: Clear test scenarios, weekly syncs

### Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| BearDog key API delay | HIGH | LOW | Weekly syncs, early communication |
| Multi-tag complexity | MEDIUM | LOW | Songbird already 80% there |
| BiomeOS integration | MEDIUM | LOW | API already exists |
| Test coverage goals | LOW | LOW | Currently at 80%, need 90% |

---

## 📊 SUCCESS METRICS

### Quality Gates

**Week 1**:
- ✅ Test suite 5x faster
- ✅ Zero `sleep` in critical tests
- ✅ `Arc<RwLock>` replaces `Arc<Mutex>`

**Week 2-3**:
- ✅ BirdSong v3.0 spec published
- ✅ Multi-tag support working
- ✅ Tag management API functional
- ✅ v2 ↔ v3 compatibility verified

**Week 3-4**:
- ✅ Key rotation integrated with BearDog
- ✅ Replay protection working (sequence tracking)
- ✅ Rate limiting adaptive
- ✅ Security audit passed

**Week 4-5**:
- ✅ Genesis ceremony enhanced (tag configuration)
- ✅ NUCLEUS metadata auto-populated
- ✅ BiomeOS integration complete
- ✅ 90%+ test coverage achieved

**Week 6**:
- ✅ Performance benchmarks meet targets
- ✅ Migration guide published
- ✅ Final security audit passed
- ✅ **Songbird v3.23.0 shipped**

### Cross-Primal Health

**Communication**:
- ✅ Weekly sync meetings (all three primals)
- ✅ Shared documentation (wateringHole)
- ✅ Clear API contracts
- ✅ Transparent progress tracking

**Integration**:
- ✅ BearDog ↔ Songbird tests green
- ✅ BiomeOS ↔ Songbird tests green
- ✅ Multi-primal scenarios working
- ✅ LiveSpore first-boot simulated

**Architecture**:
- ✅ Capability-based discovery maintained
- ✅ Zero hardcoding preserved
- ✅ Sovereignty principles honored
- ✅ Genetic lineage integrity

---

## 📈 EXPECTED IMPACT

### For Users

**Before** (BirdSong v2.0):
- Single family_id per node
- Cloud routing required for many scenarios
- Manual NAT configuration
- No institutional network support

**After** (BirdSong v3.0):
- Multiple callsign tags (UNIV + Personal + Federation)
- Institutional NAT routing (zero cloud costs)
- Auto-configured routing per tag
- LiveSpore first-boot personalization

**User Story**:
> "I'm a grad student with a basement HPC. Before LiveSpore, I had to pay for cloud NAT or manually configure port forwarding. Now, I just add the university tag during first boot, and my family can reach my HPC through the university network. Zero cloud costs, full privacy (routing encrypted for family only), and the network sees a legitimate institutional tag. Sovereignty achieved!"

### For Ecosystem

**Architecture Evolution**:
- ✅ Multi-identity per node (institutional + personal + federation)
- ✅ Graduated information disclosure (tag-based routing)
- ✅ Production-grade security (key rotation, replay protection)
- ✅ Cross-primal coordination exemplary

**Quality Improvement**:
- Songbird: A- (87/100) → A+ (98/100) (+11 points)
- Test coverage: 80% → 90%+
- Test speed: 1x → 5x (400% faster)
- Security: Enhanced (key rotation, replay protection, rate limiting)

**Capability Expansion**:
- LiveSpore-ready (self-replicating deployment)
- NUCLEUS discovery (BiomeOS multi-primal aggregation)
- Multi-tag sovereignty (institutional NAT support)

---

## 🎯 COMMITMENT

**From All Three Primals**:

**BiomeOS commits to**:
- Coordinate LiveSpore architecture
- Provide primal aggregator API
- Joint testing in Week 5
- First-boot integration in Week 6

**BearDog commits to**:
- Provide `concurrent_helpers.rs` (Week 1) ✅
- Ship key derivation API (Week 3)
- Genesis ceremony integration (Week 4)
- Joint testing in Week 5

**Songbird commits to**:
- Ship BirdSong v3.0 (February 24, 2026)
- 90%+ test coverage
- Production-grade security
- LiveSpore support complete

**All Primals commit to**:
- Weekly sync meetings (Fridays)
- Transparent progress tracking
- Collaborative problem-solving
- Architectural integrity

---

## 📚 DOCUMENTATION

### Shared (wateringHole)

**Current**:
- `birdsong/BIRDSONG_PROTOCOL.md` - v2.0 spec
- `btsp/BEARDOG_TECHNICAL_STACK.md` - BearDog reference
- `INTER_PRIMAL_INTERACTIONS.md` - Coordination master plan

**Planned** (Week 2):
- `birdsong/BIRDSONG_V3_SPECIFICATION.md` - v3.0 spec
- `livespore/MULTI_CALLSIGN_ARCHITECTURE.md` - Tag system design
- `livespore/GENESIS_CEREMONY_FLOW.md` - First-boot flow

### Primal-Specific

**BearDog**:
- `specs/current/security/LIVESPORE_FINAL_ARCHITECTURE.md` ✅
- `specs/current/security/HOT_PLUG_HSM_UPGRADE_SPECIFICATION.md` ✅
- `docs/cross-primal/SONGBIRD_EVOLUTION_FOR_LIVESPORE.md` ✅

**Songbird**:
- `LIVESPORE_EVOLUTION_RESPONSE_JAN_13_2026.md` ✅ (1095 lines)
- `LIVESPORE_EXECUTIVE_SUMMARY_JAN_13_2026.md` ✅
- `docs/cross-primal/BEARDOG_COORDINATION_STATUS.md` ✅

**BiomeOS**:
- (To be provided)

---

## 🎊 CONCLUSION

**Status**: ✅ **CROSS-PRIMAL COORDINATION ACTIVE**

**Timeline**: 6 weeks (Jan 13 - Feb 24, 2026)

**Confidence**: HIGH
- BearDog's assessment accurate (Songbird 80% there)
- All teams aligned on architecture
- Dependencies manageable
- Timeline realistic

**Expected Outcome**:
- ✅ Songbird v3.23.0 with BirdSong v3.0 (A+ grade)
- ✅ LiveSpore first-boot personalization
- ✅ Multi-callsign institutional NAT support
- ✅ Production-grade security (rotation, replay protection)
- ✅ Cross-primal coordination exemplary

**First Milestone**: January 20, 2026 (concurrent evolution complete)  
**Final Milestone**: February 24, 2026 (Songbird v3.23.0 shipped)

🌱🐕🐦 **ecoPrimals Cross-Primal Excellence in Action!**

---

**Coordination Point**: wateringHole  
**Next Sync**: Friday, January 17, 2026  
**Contact**: Respective primal teams

*"Genetic lineage enables trust. Multiple callsigns enable sovereignty. Cross-primal coordination enables LiveSpore."* ✨

