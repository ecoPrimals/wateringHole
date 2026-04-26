# Novel Ferment Transcript (NFT) — Provenance Trio Architecture Guidance

**Date**: March 13, 2026
**From**: ludoSpring (fermenting system, exp061) + wateringHole (standards)
**To**: sweetGrass, rhizoCrypt, loamSpine, BearDog teams
**License**: AGPL-3.0-or-later
**Status**: Guidance — describes target architecture for cryptographically-bound provenance objects

---

## 1. What Is a Novel Ferment Transcript?

A **Novel Ferment Transcript** (NFT) is a memory-bound digital object whose value
accumulates through use. Like a biological culture that transforms raw sugars into
wine, a digital object is transformed by play, trade, discovery, and lending into
something with authentic, verifiable history.

```
NFT = loamSpine Certificate (ownership + persistent identity)
    + rhizoCrypt DAG (action history — ephemeral, dehydrates to permanence)
    + sweetGrass Braids (PROV-O attribution — who did what, when, why)
    + BearDog Signatures (cryptographic proof of every operation)
    + Optional: Public Chain Anchor (ETH/BTC hash for global persistence)
```

This is NOT a cryptocurrency token. It is a provenance record. It has no inherent
exchange rate, cannot be subdivided into fungible units, has no gas fees, and is
not dependent on any blockchain for normal operation.

### The Biological Analogy

Fermentation transforms raw materials through microbial activity into something
more complex and valuable. The process accumulates character. It cannot be reversed —
you cannot un-ferment.

A Novel Ferment Transcript transforms raw data (mint) through use (game actions,
trades, scientific observations) into something with accumulated meaning. The
provenance DAG is the culture. The loamSpine certificate is the vessel. The
history cannot be forged — you cannot un-ferment.

---

## 2. The Cryptographic Chain

Every operation on a Novel Ferment Transcript produces three cryptographic artifacts,
all signed by BearDog:

```
                    BearDog Ed25519 signs every operation
                              │
                              ▼
    ┌─────────────────────────────────────────────────┐
    │                  OPERATION                       │
    │  (mint, trade, loan, achieve, inspect, consume)  │
    └───────┬──────────────┬──────────────┬───────────┘
            │              │              │
            ▼              ▼              ▼
     rhizoCrypt       loamSpine      sweetGrass
     DAG vertex       Spine entry    Attribution braid
     (ephemeral)      (permanent)    (PROV-O semantic)
            │              │              │
            └──dehydrate──►│              │
                           │◄──anchor─────┘
                           │
                           ▼
                 Optional: public chain anchor hash
                 (ETH, BTC, or any append-only ledger)
```

### Layer Responsibilities

| Layer | What It Provides | Lifetime | Signed By |
|-------|-----------------|----------|-----------|
| **rhizoCrypt** | Content-addressed DAG of every action | Session (ephemeral, dehydrates) | BearDog Ed25519 |
| **loamSpine** | Immutable certificate + spine entries | Permanent (local) | BearDog Ed25519 |
| **sweetGrass** | W3C PROV-O attribution braids | Permanent (local) | BearDog Ed25519 |
| **Public anchor** | 32-byte hash on global ledger | Permanent (global) | Chain consensus |

### What BearDog Signing Provides

Without BearDog, the fermenting system is just data structures. With BearDog:

1. **Every DAG vertex is signed** — you cannot insert a fake game action
2. **Every certificate operation is signed** — you cannot forge a transfer
3. **Every braid is signed** — you cannot claim false attribution
4. **The entire chain is verifiable** — given any anchor point, the full
   history can be cryptographically validated back to genesis

BearDog's Ed25519 signatures are the same strength as SSH keys and Tor hidden
services. No blockchain required for cryptographic binding.

---

## 3. The Dehydration-to-Anchor Pattern

Normal operation is entirely local and zero-cost:

```
rhizoCrypt session (ephemeral)
    │
    ├── vertex: mint sword (tick 0)
    ├── vertex: equip sword (tick 1)
    ├── vertex: kill boss with sword (tick 47)
    ├── vertex: trade sword to Bob (tick 102)
    │
    └── DEHYDRATE ──► loamSpine (permanent, local)
                          │
                          ├── entry: CertificateMint
                          ├── entry: CertificateTradeOffer
                          ├── entry: CertificateTradeAccept
                          ├── entry: CertificateTransfer
                          │
                          └── OPTIONAL ANCHOR ──► Public chain
                                                    │
                                                    └── 32-byte hash proving
                                                        the spine state at
                                                        this point in time
```

The anchor is just a hash. It proves that a specific loamSpine state existed at
a specific time. Anyone with the local spine data can verify it against the anchor.

### When to Anchor

Anchoring is optional and application-specific:

| Context | Anchor Frequency | Why |
|---------|-----------------|-----|
| Trading card game | On trade/tournament result | Prove card history to buyers |
| Scientific sample | On custody transfer | Legal chain-of-custody |
| In-game cosmetic | Never (or on sale) | History is local until monetized |
| Medical record | On every access | Regulatory compliance |
| Digital art | On creation + each sale | Provenance for collectors |

### Multi-Chain Anchoring

The anchor mechanism is chain-agnostic. A single spine state can anchor to
multiple chains simultaneously for redundancy:

```
loamSpine state hash ──► Ethereum (global, expensive, slow)
                    ──► Bitcoin (global, expensive, slow)
                    ──► Solana (global, cheap, fast)
                    ──► Custom primal chain (sovereign, free, fast)
```

No smart contracts needed. The anchor is a raw hash published to any
append-only data store.

---

## 4. Cross-Domain Applications

The same provenance architecture serves every domain. Only the vocabulary changes:

### Gaming: Collectibles and In-Game Items

```
Physical trading card ←──same cert──► Digital twin in game
                                │
                                ├── rhizoCrypt: tournament history, play records
                                ├── loamSpine: ownership chain, cosmetic metadata
                                ├── sweetGrass: artist attribution, designer credit
                                └── Anchor: public proof of provenance for resale
```

**Value proposition**: The card that won the tournament finals has verifiable
history. Not "one of 1000" but "the ONE that survived the championship."
Value from significance, not scarcity.

### Science: Sample Chain-of-Custody

```
Field sample ←──same cert──► Lab analysis record
                         │
                         ├── rhizoCrypt: collection → transport → process → analyze
                         ├── loamSpine: custody transfers, condition changes
                         ├── sweetGrass: researcher attribution, lab credit
                         └── Anchor: regulatory compliance proof
```

**Value proposition**: Unbroken, cryptographically-verified chain from field
to publication. The same fraud detection that catches item duping in games
catches sample tampering in labs.

### Sensitive Data: Medical Records

```
Patient record ←──same cert──► Treatment history
                           │
                           ├── rhizoCrypt: access DAG (who viewed what, when)
                           ├── loamSpine: consent certificates, access grants
                           ├── sweetGrass: provider attribution, referral chain
                           └── Anchor: HIPAA audit trail
```

**Value proposition**: The patient owns their record (DID-based). Providers
get loaned access via certificate lending. Every access is a DAG vertex.
The attribution chain enables radiating attribution for research contributions.

### Digital Art and Creative Works

```
Digital artwork ←──same cert──► Exhibition history
                            │
                            ├── rhizoCrypt: creation process, remix history
                            ├── loamSpine: ownership, licensing, exhibition
                            ├── sweetGrass: creator + collaborator attribution
                            └── Anchor: provenance for collectors
```

**Value proposition**: The artwork carries its entire creative history. Every
collaborator in the attribution chain receives credit. scyBorg licensing
(CC-BY-SA) is machine-verifiable.

---

## 5. Relationship to sunCloud and Radiating Attribution

The Novel Ferment Transcript is the concrete mechanism for the sunCloud
economic model's "radiating attribution":

1. **An object is created** — the mint braid records the creator
2. **The object accumulates history** — every action adds to the attribution chain
3. **The object generates value** — through sale, exhibition, citation, or use
4. **Value radiates back** — sunCloud consults the sweetGrass chain and distributes
   proportionally to every contributor

The public chain anchor is the trigger. When an NFT is anchored, the attribution
chain becomes publicly attestable, which activates the radiating distribution
mechanism. Without the anchor, attribution exists but has no public proof.

### What This Is NOT

- **NOT a currency** — the object itself has no exchange rate
- **NOT a speculation vehicle** — value comes from history, not artificial scarcity
- **NOT blockchain-dependent** — normal operation is local, anchor is optional
- **NOT gas-fee-burdened** — mint, trade, lend are zero-cost local operations
- **NOT wallet-dependent** — identity is DID-based, not wallet-based

---

## 6. Trio Evolution Priorities for NFT Support

### BearDog (Immediate)

1. **Expose `sign_certificate` RPC method** for loamSpine entry signing
2. **Expose `sign_vertex` RPC method** for rhizoCrypt DAG vertex signing
3. **Expose `sign_braid` RPC method** for sweetGrass braid signing
4. These may already exist via generic `crypto.sign_ed25519` — document the
   canonical signing flow for NFT operations

### rhizoCrypt (Short-term)

1. **Implement `ProvenanceQueryable` trait** — needed for timeline reconstruction
2. **Cross-session derivation links** — an object's history may span multiple
   sessions. The dehydration hash links sessions.
3. **BearDog-signed vertices** — wire BearDog signing into vertex creation

### loamSpine (Short-term)

1. **`CertificateType::NovelFermentTranscript`** — or use `Custom` with defined
   schema: `type_uri = "ecoPrimals:nft"`, schema includes cosmetic metadata,
   rarity, history summary hash
2. **Trading protocol** — `CertificateTradeOffer`, `CertificateTradeAccept`,
   `CertificateTradeReject`, `CertificateTradeCancel` entry types (DONE in
   loam-spine-core v0.8.2, implemented during exp061)
3. **Public chain anchor entry type** — `PublicChainAnchor { chain, tx_hash,
   state_hash }` for recording the optional global anchor
4. **Owner inventory query** — `list_by_owner(did)` for "show me everything
   Alice owns"

### sweetGrass (Short-term)

1. **Object Memory API** — `append_object_event`, `get_object_timeline`,
   `export_prov_timeline` (DONE in sweet-grass-core v0.7.3, implemented
   during exp061)
2. **License-aware attribution** — scyBorg license metadata on braids (from
   `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md`)
3. **Radiating attribution calculation** — given an NFT's timeline, compute
   the proportional contribution of each agent

### biomeOS (Medium-term)

1. **`provenance_node_atomic.toml`** — unified deployment graph for Tower +
   Trio (DONE, created during exp061 Phase 0)
2. **NFT lifecycle orchestration** — graph nodes for mint → trade → anchor
   workflow
3. **plasmidBin binaries** — trio binaries available for local deployment

---

## 7. Validated in ludoSpring

### exp061: Fermenting System (Core NFT Lifecycle)

```bash
cargo run -p ludospring-exp061 -- validate   # 89/89 checks
```

**8 validation sections, 89 checks:**

| Section | Checks | What It Proves |
|---------|--------|---------------|
| Cosmetic Schema | 10 | Rarity, skin, color, material, wear — round-trip |
| Certificate Lifecycle | 17 | mint → inspect → trade → loan → return → consume |
| Trading Protocol | 14 | offer, accept, reject, cancel, atomic swap |
| Object Memory | 7 | Per-object event timeline, cross-object queries |
| Trio Integration | 13 | rhizoCrypt DAG + loamSpine certs + sweetGrass braids |
| Ownership Enforcement | 5 | Only owners trade/loan, only borrowers return |
| Full Scenario | 10 | Two players, rich history, swap, consume |
| Composable IPC | 13 | JSON-RPC wire format for live trio services |

The trading protocol entry types (`CertificateTradeOffer/Accept/Reject/Cancel`)
and the object memory API (`ObjectMemory`, `ObjectEvent`) were implemented in
the provenance trio codebases during this experiment.

### exp062-066: Cross-Spring Provenance Experiments (228 checks)

```bash
cargo run -p ludospring-exp064                # 39/39 BearDog-signed chain
cargo run -p ludospring-exp062                # 39/39 Field sample provenance
cargo run -p ludospring-exp063                # 35/35 Consent-gated medical access
cargo run -p ludospring-exp065                # 74/74 Cross-domain fraud unification
cargo run -p ludospring-exp066                # 41/41 Radiating attribution calculator
```

| Experiment | Checks | What It Proves |
|-----------|--------|---------------|
| exp064: BearDog-Signed Chain | 39/39 | Ed25519 signing on every trio operation (vertex, cert, braid). Chain verification detects tamper at exact position. IPC wire format for `crypto.sign_ed25519` / `crypto.verify_ed25519`. |
| exp062: Field Sample Provenance | 39/39 | wetSpring scaffold — full sample lifecycle (Collect → Publish). 6 fraud types (PhantomSample, DuplicateAccession, BrokenColdChain, UnauthorizedAccess, MislabeledSpecimen, ContaminationGap). DAG isomorphism with extraction shooter exp053. |
| exp063: Consent-Gated Medical Access | 35/35 | healthSpring scaffold — patient-owned records (loamSpine certs). Consent as scoped lending. 5 fraud types. Zero-knowledge access proofs via BearDog selective disclosure. PROV-O audit trail. |
| exp065: Cross-Domain Fraud Unification | 74/74 | Same `GenericFraudDetector` code across gaming/science/medical. 5 generic fraud types. >80% structural similarity. The universality claim from Paper 18 is proven computationally. |
| exp066: Radiating Attribution Calculator | 41/41 | sunCloud value distribution. Walk sweetGrass attribution chain, compute proportional credit. Decay models (linear, exponential). Role weighting (Creator > Contributor > Validator). Conservation: shares sum to 1.0. |

**Total validated: 317 checks across 6 experiments (exp061-066), 0 failures.**

See `whitePaper/gen3/baseCamp/21_sovereign_sample_provenance.md` (Paper 21) and
`whitePaper/gen3/baseCamp/22_zero_knowledge_medical_provenance.md` (Paper 22).

---

## 8. References

- `ludoSpring/experiments/exp061_fermenting/` — core NFT lifecycle
- `ludoSpring/experiments/exp062_field_sample_provenance/` — wetSpring scaffold
- `ludoSpring/experiments/exp063_consent_gated_medical/` — healthSpring scaffold
- `ludoSpring/experiments/exp064_beardog_signed_chain/` — BearDog signing protocol
- `ludoSpring/experiments/exp065_cross_domain_fraud/` — cross-domain fraud unification
- `ludoSpring/experiments/exp066_radiating_attribution/` — sunCloud attribution calculator
- `phase2/biomeOS/graphs/provenance_node_atomic.toml` — deployment graph
- `wateringHole/SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — licensing layer
- `whitePaper/economics/LATENT_VALUE_ECONOMY.md` — latent value economy
- `whitePaper/economics/SUNCLOUD_ECONOMIC_MODEL.md` — radiating attribution
- `whitePaper/economics/LOAM_CERTIFICATE_LAYER.md` — certificate mesh
- `whitePaper/gen3/baseCamp/20_novel_ferment_transcript_economics.md` — NFT economics paper
- `whitePaper/gen3/baseCamp/21_sovereign_sample_provenance.md` — sample provenance paper
- `whitePaper/gen3/baseCamp/22_zero_knowledge_medical_provenance.md` — medical provenance paper
