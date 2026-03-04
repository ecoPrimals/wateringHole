# Genomic Vault — Organ Model Cross-Spring Handoff

**Date:** March 1, 2026
**From:** wetSpring V85 (Exp259, local implementation validated)
**To:** BearDog, NestGate, Songbird, biomeOS, all Springs

---

## The Principle

Genomic data is an organ. It belongs to the individual.

You cannot take a person's kidney without their explicit, informed, revocable
consent. The same must be true for their genomic data. The current industry
treats DNA like a commodity — 23andMe's bankruptcy put 15 million people's
genomes on the liquidation table. That is organ harvesting from the living.

ecoPrimals treats it differently: **no pipeline can touch genomic data without
a signed, time-bounded, revocable consent ticket.**

---

## What wetSpring Built (Exp259, 30/30 checks)

wetSpring implemented the vault protocol locally in pure Rust (sovereign,
zero external deps) so that specific primals can absorb what works. This
follows the Write → Absorb → Lean cycle used for ToadStool shader evolution.

### Consent Ticket (`vault::consent`)

```rust
ConsentTicket {
    id: [u8; 32],              // BLAKE3 of contents
    owner_id: String,           // lineage identifier
    scope: ConsentScope,        // what's authorized
    grantee: String,            // who can access
    issued_at: u64,             // UNIX timestamp
    duration: Duration,         // validity window
    revoked: bool,              // owner can revoke at any time
    signature: [u8; 64],        // Ed25519 (BearDog absorb target)
}
```

**Scope hierarchy** (higher = more sensitive):
| Level | Scope | Sensitivity |
|-------|-------|-------------|
| 1 | `DiversityAnalysis`, `AndersonClassification` | Aggregated metrics only |
| 2 | `FullPipeline` (implies level 1) | Multiple analyses |
| 3 | `ExportAggregated` | Results leave the vault |
| 4 | `Custom` | User-defined |
| 5 | `ReadRawSequences` | Most sensitive — actual sequence data |

**Validated properties:**
- Time-bounded: tickets expire
- Revocable: owner can revoke at any time
- Scope-limited: `FullPipeline` does NOT imply `ReadRawSequences`
- Owner-bound: cross-owner access is rejected
- Signed: Ed25519 placeholder for BearDog absorption

### Encrypted Storage (`vault::storage`)

```
plaintext → sovereign_hash → content_hash
plaintext → sovereign_encrypt(key, nonce) → ciphertext
ciphertext → NestGate storage.store_blob (absorb target)
```

**Validated properties:**
- Round-trip: encrypt → decrypt = original
- Content-addressed: stored by plaintext hash
- Wrong key: integrity check fails (no silent corruption)
- Cross-owner: rejected at the ticket level
- Unauthorized: always fails

### Provenance Chain (`vault::provenance`)

```
Entry_0 (parent=0x00) → Entry_1 (parent=hash_0) → Entry_2 (parent=hash_1) → ...
```

Each entry records: operation, actor, consent ticket ID, data hash, node ID,
timestamp, Ed25519 signature (BearDog absorb target).

**Validated properties:**
- Merkle-linked: each entry's parent is the previous entry's hash
- Tamper-evident: modifying any entry breaks the chain
- Filterable: by actor, by consent ticket ID
- Append-only: no delete, no modify

---

## Absorb Targets

### BearDog (Priority: HIGH)

| Capability | Current (wetSpring local) | Target (BearDog) |
|------------|--------------------------|-------------------|
| Hashing | Sovereign hash (simplified) | BLAKE3 (`beardog-security`) |
| Encryption | Sovereign XOR-rotate | ChaCha20-Poly1305 (`encryption.encrypt`) |
| Signing | Zeroed placeholder | Ed25519 (`genetic.sign_lineage_certificate`) |
| Key derivation | Direct key param | `genetic.derive_lineage_key` from family seed |

**IPC methods to wire:**
- `encryption.encrypt` / `encryption.decrypt` — replace sovereign cipher
- `genetic.derive_lineage_key` — derive vault key from lineage seed
- `genetic.sign_lineage_certificate` — sign consent tickets and provenance entries

### NestGate (Priority: HIGH)

| Capability | Current (wetSpring local) | Target (NestGate) |
|------------|--------------------------|-------------------|
| Blob storage | In-memory `HashMap` | `storage.store_blob` (ZFS CAS) |
| Blob retrieval | In-memory `HashMap` | `storage.retrieve_blob` |
| Listing | In-memory iteration | `storage.list` |
| Provenance | In-memory `Vec` | Append-only CAS (new capability) |

**New NestGate capability needed:**
- `provenance.append` — store provenance entries in append-only CAS
- `provenance.chain` — retrieve the full chain for a data hash
- `provenance.verify` — server-side chain integrity verification

### Songbird (Priority: MEDIUM)

| Capability | Current (wetSpring local) | Target (Songbird) |
|------------|--------------------------|-------------------|
| Consent creation | Direct constructor | `POST /consent/request` |
| Consent approval | Implicit in constructor | `PUT /consent/:id` (approve/deny) |
| Consent query | Direct field check | `GET /consent/:id` |
| Consent revocation | `ticket.revoke()` | `PUT /consent/:id` with `action: deny` |

**Enhancement needed:**
- Scope-aware consent: Songbird should understand `ConsentScope` sensitivity
- Notification: owner should be notified when consent is requested
- Audit: consent decisions should feed into the provenance chain

### biomeOS (Priority: MEDIUM)

**New Neural API capabilities:**
- `vault.store` — route to NestGate with BearDog encryption
- `vault.retrieve` — route to NestGate with BearDog decryption
- `vault.consent.request` — route to Songbird
- `vault.provenance.append` — route to NestGate CAS
- `vault.provenance.verify` — route to NestGate

**NUCLEUS Vault Atomic:**
- `biomeos nucleus start --mode vault` — BearDog + NestGate + consent layer
- No ToadStool, no Songbird network discovery, no external connectivity
- Pure encrypted storage and consent management

---

## Data Flow

```
                  Consent
Owner ──────────→ Songbird ──────→ ConsentTicket (signed by BearDog)
                                        │
                                        ▼
Raw FASTQ ──→ BearDog encrypt ──→ NestGate store_blob ──→ ZFS (Westgate)
                  │                       │
                  │                       ▼
                  │               ProvenanceEntry (signed, chained)
                  │
                  ▼
            content_hash (returned to owner)

Later:
Owner + ConsentTicket + content_hash
  → NestGate retrieve_blob → BearDog decrypt → plaintext → pipeline
  → ProvenanceEntry (who accessed, when, what they computed)
```

---

## What This Enables

1. **Home genomics**: MinION sequences in the basement, encrypted on local ZFS,
   never leaves without explicit consent. The individual owns their genome
   the way they own their liver.

2. **Research consent**: "I consent to Shannon diversity analysis of my 16S data
   for 30 days by this specific NUCLEUS node." Not "I agree to your Terms of
   Service." Explicit, time-bounded, scope-limited, revocable.

3. **Audit trail**: Every operation on genomic data is recorded in a tamper-evident
   chain. If your data was accessed, you know who, when, what, and where.

4. **Cross-gate security**: When LAN mesh is active, genomic data on Westgate
   (Nest) is encrypted to the owner's lineage key. Even if the physical drive
   is stolen, the data is unreadable without the BearDog family seed.

---

## Experiment Chain

```
Exp203-208 (IPC validated)
  → Exp256 (EMP atlas, 30K samples)
    → Exp257 (NUCLEUS data pipeline, three-tier routing)
      → Exp258 (Tower-Node, all primals READY)
        → Exp259 (Genomic Vault, 30/30 checks) ← YOU ARE HERE
          → BearDog absorbs signing + encryption
            → NestGate absorbs CAS + provenance
              → Songbird absorbs consent workflow
                → biomeOS absorbs vault.* routing
                  → NUCLEUS Vault Atomic
```

---

## Files Created

| Location | File | Purpose |
|----------|------|---------|
| wetSpring | `barracuda/src/vault/mod.rs` | Vault module root |
| wetSpring | `barracuda/src/vault/consent.rs` | Consent ticket protocol (20 tests) |
| wetSpring | `barracuda/src/vault/provenance.rs` | Provenance chain (5 tests) |
| wetSpring | `barracuda/src/vault/storage.rs` | Encrypted vault storage (7 tests) |
| wetSpring | `barracuda/src/bin/validate_genomic_vault.rs` | Exp259 binary (30 checks) |
| ecoPrimals | `wateringHole/handoffs/GENOMIC_VAULT_ORGAN_MODEL_HANDOFF_MAR01_2026.md` | This document |
