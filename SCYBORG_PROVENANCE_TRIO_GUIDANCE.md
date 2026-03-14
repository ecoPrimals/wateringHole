# scyBorg — Provenance Trio Licensing Evolution Guidance

**Date**: March 13, 2026
**From**: ludoSpring (lysogeny strategy) + wateringHole (standards)
**To**: sweetGrass, rhizoCrypt, loamSpine teams
**License**: AGPL-3.0-or-later
**Status**: Guidance — describes target architecture for licensing support

---

## 1. What Is scyBorg?

scyBorg is the ecoPrimals triple-copyleft licensing framework:

```
scyBorg = AGPL-3.0 (code) + ORC (game mechanics) + CC-BY-SA 4.0 (creative content)
```

| Layer | License | Covers | Governing Body |
|-------|---------|--------|---------------|
| Software | AGPL-3.0-or-later | Engine, tools, shaders, math, infrastructure | FSF (nonprofit) |
| Mechanics | ORC | Rules, stat blocks, progression systems, encounter math | Open RPG Creative Foundation (nonprofit) |
| Creative | CC-BY-SA 4.0 | Art, worlds, narrative, characters, music, sound, maps | Creative Commons (nonprofit) |
| Reserved | ORC Reserved Material | Studio-specific branding, trademarks, trade dress | Creator retains |

No single entity can rug-pull any of these licenses. This is structural, not
contractual.

### Why the Provenance Trio Matters

The trio IS the enforcement mechanism:

- **sweetGrass** tracks *who created what* (the BY in CC-BY-SA)
- **rhizoCrypt** tracks *derivation chains* (the SA in CC-BY-SA)
- **loamSpine** issues *immutable license certificates* (the proof that terms apply)

Without the trio, scyBorg is just words in a LICENSE file. With the trio,
scyBorg is machine-verifiable, automatically attributed, and structurally
resistant to license violation.

---

## 2. Current State Assessment

### sweetGrass v0.7.3 (746 tests, 94% coverage)

**Already supports:**
- Agent attribution with 12 roles (Creator, Contributor, Publisher, Validator, etc.)
- W3C PROV-O export (JSON-LD with `wasAttributedTo`, `wasDerivedFrom`)
- Derivation chains via `AttributionCalculator` with recursive propagation
- Content-addressed artifacts via `ContentHash`
- Domain metadata on `ContributionRecord` and `SessionContribution`
- Privacy controls (5 GDPR-inspired levels)

**Needs for scyBorg:**
- `license` field on `Braid` and `ContributionRecord` (SPDX identifier)
- `content_category` enum: `Code`, `GameMechanics`, `CreativeContent`, `Reserved`
- `copyright_holder` field alongside `was_attributed_to`
- Attribution notice generation API (human + machine readable)

### rhizoCrypt v0.13.0-dev (862 tests, 87.8% coverage)

**Already supports:**
- Content-addressed DAG with multi-parent vertices
- Session scoping with lifecycle management
- Merkle tree integrity
- Dehydration to loamSpine
- `ProvenanceChain`, `VertexRef`, `SessionAttribution` types
- Vertex metadata (`HashMap<String, MetadataValue>`)

**Needs for scyBorg:**
- Implement `ProvenanceQueryable` trait (exists but is unimplemented)
- Add `provenance.*` JSON-RPC methods to rhizo-crypt-rpc
- License metadata on vertices: `license: Option<String>` in metadata
- Cross-session derivation links (for tracking derivative works across sessions)

### loamSpine v0.8.2 (744 tests, ~91% coverage)

**Already supports:**
- Immutable append-only ledger with DID-based ownership
- `CertificateType::SoftwareLicense` exists
- `CertificateType::Custom` with `type_uri` + `schema_version`
- Certificate mint, transfer, loan lifecycle
- Extensible metadata (`attributes: HashMap`)
- Temporal anchoring
- Trio commit flow (`TrioCommitRequest` / `TrioCommitReceipt`)

**Needs for scyBorg:**
- `CertificateType::CreativeWorkLicense` (or use `Custom` with defined schema)
- License certificate schema: SPDX expression, content category, copyright holder,
  rights (reproduce, adapt, distribute, commercial), share-alike flag
- License chain: work certificate → license certificate → terms
- Attribution notice entry type

---

## 3. Target Architecture

### Content Categories

Every artifact in the ecosystem should declare its content category:

```rust
pub enum ContentCategory {
    /// Source code, binaries, shaders, infrastructure.
    /// License regime: AGPL-3.0-or-later.
    Code,
    /// Game rules, stat blocks, progression math, encounter systems.
    /// License regime: ORC Licensed Material.
    GameMechanics,
    /// Art, worlds, narrative, characters, music, maps.
    /// License regime: CC-BY-SA 4.0.
    CreativeContent,
    /// Studio branding, trademarks, trade dress.
    /// License regime: ORC Reserved Material (creator retains).
    Reserved,
}
```

This enum should be shared across all three primals. Recommended location:
a new `scyborg-types` crate in `phase2/` or as a shared module in the trio.

### License Expression

Use SPDX license expressions for machine-readable license identification:

```rust
pub enum LicenseExpression {
    Spdx(String),    // e.g. "AGPL-3.0-or-later", "CC-BY-SA-4.0"
    Orc {
        licensed_material: bool,
        reserved_material: bool,
    },
    ScyBorg {
        code: String,           // SPDX for code layer
        mechanics: String,      // ORC designation
        creative: String,       // SPDX for creative layer
    },
}
```

### Derivation Tracking (Share-Alike Compliance)

CC-BY-SA requires that derivatives use the same license. rhizoCrypt's DAG
already models this — each vertex has parents. The missing piece is:

1. When a vertex is created, record the license of the source material
2. When a derived work is created, verify that the license is compatible
3. When a derived work is committed to loamSpine, the license certificate
   must inherit the share-alike obligation

This is NOT enforcement (we don't block incompatible licenses). This is
*evidence* — the derivation chain proves what license applies.

### Attribution Notice Generation

sweetGrass should be able to generate a complete attribution notice from a
braid. Given a content hash, produce:

```
This work incorporates contributions from:
- Alice (Creator, 45%) — CC-BY-SA 4.0
- Bob (Contributor, 30%) — CC-BY-SA 4.0
- Carol (Validator, 25%) — AGPL-3.0-or-later

Derived from:
- "Original Tileset" by Dave — CC-BY-SA 4.0 (loamSpine cert: did:key:z6Mk...)
- "Game Engine v2.1" — AGPL-3.0-or-later (commit: abc123)

License: CC-BY-SA 4.0 (share-alike inherited from "Original Tileset")
```

This is the BY and SA in CC-BY-SA, automated.

---

## 4. Evolution Path

### Phase 1: Schema Definition (No Breaking Changes)

Use existing extensible metadata to carry license information:

- sweetGrass: add `domain_key::LICENSE = "scyborg.license"` and
  `domain_key::CONTENT_CATEGORY = "scyborg.content_category"` constants.
  Carry license data in the existing `domain: HashMap<String, Value>`.
- rhizoCrypt: add license metadata via existing `metadata: HashMap` on vertices.
- loamSpine: define `CertificateType::Custom` schema for license certificates
  using the existing `type_uri` + `schema_version` mechanism.

This requires zero API changes and zero breaking changes. It works today.

### Phase 2: First-Class Types

Once the schema is validated through use in ludoSpring experiments:

- Add `ContentCategory` enum and `LicenseExpression` types as shared types
- Add `license` field to sweetGrass `Braid` and `ContributionRecord`
- Add `CertificateType::CreativeWorkLicense` to loamSpine
- Implement `ProvenanceQueryable` in rhizoCrypt

### Phase 3: Attribution Notice API

- sweetGrass `AttributionCalculator` gains `generate_notice()` method
- Integrates license information from braids and loamSpine certificates
- Produces human-readable and machine-readable (JSON-LD) attribution notices
- This is the "radiating attribution" from `SUNCLOUD_ECONOMIC_MODEL.md` made
  license-aware

### Phase 4: sunCloud Integration

- Attribution notices become the basis for value distribution
- License type affects distribution (CC-BY-SA share-alike = proportional to
  derivation chain length)
- Ties to the economic model in `LATENT_VALUE_ECONOMY.md`

---

## 5. Cross-Spring Impact

scyBorg licensing is not ludoSpring-specific. Every spring produces both
code and creative content:

| Spring | Code (AGPL-3.0) | Creative Content (CC-BY-SA) |
|--------|-----------------|---------------------------|
| ludoSpring | Game engines, validation binaries | Game designs, rulesets, specifications |
| wetSpring | Bioinformatics pipelines | Biological models, visualizations |
| hotSpring | Physics simulations | Validation reports, methodology |
| airSpring | Agricultural tools | Soil models, crop designs |
| neuralSpring | EGT solvers | Evolutionary models, strategy descriptions |
| healthSpring | Clinical tools | Patient journey models, outcome reports |

The provenance trio handles ALL of these. The license layer is universal.

---

## 6. What NOT to Build

- **Do NOT build license enforcement.** The trio provides *evidence*, not
  *enforcement*. If someone violates CC-BY-SA, the derivation chain in
  rhizoCrypt proves the violation. The license itself (backed by copyright law)
  is the enforcement mechanism.

- **Do NOT build a license compatibility checker.** AGPL-3.0 + ORC + CC-BY-SA
  are deliberately chosen to be non-conflicting. Complex compatibility logic
  is unnecessary and harmful. Keep it simple.

- **Do NOT couple license types to business logic.** License metadata is
  informational. It should not gate functionality. A vertex with `license: null`
  should work identically to one with `license: "AGPL-3.0-or-later"`.

---

## 7. Immediate Action Items

For each primal team, the minimum viable contribution to scyBorg:

### sweetGrass

1. Add `domain_key::LICENSE` and `domain_key::CONTENT_CATEGORY` constants
2. Document the schema for license metadata in the domain HashMap
3. Add an example in contribution tests showing license-carrying braids

### rhizoCrypt

1. Add `"scyborg.license"` and `"scyborg.content_category"` as recommended
   metadata keys in documentation
2. Implement `ProvenanceQueryable` for the main `RhizoCrypt` struct
3. Add `provenance.chain` JSON-RPC method

### loamSpine

1. Define a `CertificateType::Custom` schema for `type_uri = "scyborg:license"`
2. Document the schema fields: `spdx_expression`, `content_category`,
   `copyright_holder`, `share_alike`
3. Add an example in certificate tests showing license certificate minting

---

## References

- `ludoSpring/specs/LYSOGENY_CATALOG.md` — lysogeny target catalog
- `whitePaper/economics/LATENT_VALUE_ECONOMY.md` — latent value economy
- `whitePaper/economics/SUNCLOUD_ECONOMIC_MODEL.md` — radiating attribution
- `whitePaper/economics/LOAM_CERTIFICATE_LAYER.md` — certificate mesh
- `whitePaper/gen3/baseCamp/18_rpgpt_sovereign_rpg_engine.md` — ORC for rulesets
- ORC License: https://azoralaw.com/orclicense/
- CC-BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
- SPDX License List: https://spdx.org/licenses/
