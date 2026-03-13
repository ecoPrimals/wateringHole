# SweetGrass v0.7.0 — Contribution API Handoff

**Date**: March 12, 2026
**From**: SweetGrass (v0.7.0)
**To**: rhizoCrypt, biomeOS, LoamSpine, ludoSpring, wetSpring teams
**License**: AGPL-3.0-only

---

## Summary

SweetGrass v0.7.0 introduces the **inter-primal contribution recording API** —
the missing link that lets other primals send structured attribution data to
sweetGrass for provenance braid creation.

Two new JSON-RPC 2.0 methods are available:

| Method | Purpose |
|--------|---------|
| `sweetgrass.recordContribution` | Record a single contribution from any primal |
| `sweetgrass.recordSession` | Record a batch of contributions from a session dehydration |

---

## For rhizoCrypt Team

### Dehydration Flow

When rhizoCrypt dehydrates a session, it should send a `sweetgrass.recordSession`
call with the session metadata and per-participant contributions:

```json
{
  "jsonrpc": "2.0",
  "method": "sweetgrass.recordSession",
  "params": {
    "session_id": "rhizo-session-uuid",
    "source_primal": "rhizoCrypt",
    "niche": "rootpulse",
    "session_start": 1710000000000000000,
    "session_end": 1710003600000000000,
    "loam_entry": "spine-id|entry-hash",
    "contributions": [
      {
        "agent": "did:key:z6MkAlice",
        "role": "Creator",
        "content_hash": "sha256:abc123",
        "size": 4096,
        "description": "Created module foo"
      },
      {
        "agent": "did:key:z6MkBob",
        "role": "Reviewer",
        "content_hash": "sha256:def456",
        "size": 128,
        "description": "Reviewed module foo"
      }
    ]
  },
  "id": 1
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "session_id": "rhizo-session-uuid",
    "braids_created": 2,
    "braid_ids": ["urn:braid:uuid:...", "urn:braid:uuid:..."]
  },
  "id": 1
}
```

### Integration Points

- **Transport**: JSON-RPC 2.0 over TCP or Unix socket (sweetGrass listens on `HTTP_LISTEN`)
- **Discovery**: Use Songbird `Capability::Attribution` to find sweetGrass at runtime
- **Timing**: Call after dehydration, before or after LoamSpine commit (both work)
- **Failure**: If sweetGrass is unavailable, queue contributions for retry (graceful degradation)

---

## For biomeOS Team

### Neural API Translations

Add these capability translations:

| Capability | Method | Provider |
|-----------|--------|----------|
| `attribution.record` | `sweetgrass.recordContribution` | sweetGrass |
| `attribution.recordSession` | `sweetgrass.recordSession` | sweetGrass |

### RootPulse Commit Graph

The commit workflow graph should include sweetGrass between rhizoCrypt and LoamSpine:

```
rhizoCrypt.dehydrate → sweetgrass.recordSession → loamspine.commit
```

In TOML graph format:

```toml
[[nodes]]
id = "dehydrate"
capability = "session.dehydrate"

[[nodes]]
id = "attribute"
capability = "attribution.recordSession"
depends_on = ["dehydrate"]

[[nodes]]
id = "commit"
capability = "history.commit"
depends_on = ["attribute"]
```

### Niche Manifest Update

In `niches/rootpulse/rootpulse-niche.yaml`, sweetGrass capabilities should include:

```yaml
sweetGrass:
  version: ">=0.7.0"
  capabilities:
    - semantic-attribution
    - braiding
    - contribution-tracking
    - session-recording  # NEW
```

---

## For wetSpring Team

### Chemistry Domain Keys

SweetGrass now supports extensible domain metadata. Use these well-known keys
in the `domain` field of `ContributionRecord`:

| Key | Purpose |
|-----|---------|
| `chemistry.molecule` | Molecule identifier |
| `chemistry.basis_set` | Basis set used (e.g., "6-31G*") |
| `chemistry.functional` | DFT functional (e.g., "B3LYP") |
| `chemistry.campaign` | DftCampaign identifier |

Example:

```json
{
  "agent": "did:key:z6MkResearcher",
  "role": "Creator",
  "content_hash": "sha256:dft-result-hash",
  "domain": {
    "chemistry.molecule": "caffeine",
    "chemistry.basis_set": "6-31G*",
    "chemistry.functional": "B3LYP",
    "chemistry.campaign": "campaign-2026-q1"
  }
}
```

### Chemistry Braid Relations

The wetSpring V87 handoff specified these relation types:
- `DependsOn`, `ValidatedBy`, `ComputedWith`, `TrainedOn`

These are supported via `ActivityType::Custom { type_uri }` in sweetGrass.
Use URIs like `ecop:DependsOn`, `ecop:ValidatedBy`, etc.

---

## For ludoSpring Team

### Game Domain Keys

| Key | Purpose |
|-----|---------|
| `game.engagement` | Engagement score or metrics |
| `game.player` | Player identifier |
| `game.session_type` | Type of game session |

Use these in the `domain` field when recording player attribution or engagement tracking.

---

## Data Types

### ContributionRecord

```rust
pub struct ContributionRecord {
    pub agent: Did,
    pub role: AgentRole,
    pub content_hash: String,
    pub mime_type: String,       // default: "application/octet-stream"
    pub size: u64,               // default: 0
    pub timestamp: u64,          // nanos since epoch, 0 = now
    pub description: Option<String>,
    pub source_primal: Option<String>,
    pub session_id: Option<String>,
    pub domain: HashMap<String, Value>,  // extensible metadata
}
```

### SessionContribution

```rust
pub struct SessionContribution {
    pub session_id: String,
    pub source_primal: String,
    pub niche: Option<String>,
    pub contributions: Vec<ContributionRecord>,
    pub session_start: Option<u64>,
    pub session_end: Option<u64>,
    pub loam_entry: Option<String>,
    pub domain: HashMap<String, Value>,
}
```

### Available Agent Roles

Creator, Contributor, Curator, Reviewer, Approver, Publisher,
DataProvider, Annotator, Trainer, Validator, Observer, Sponsor

---

## SweetGrass v0.7.0 Metrics

| Metric | Value |
|--------|-------|
| Version | 0.7.0 |
| Tests | 553 passing |
| Crates | 9 |
| Protocols | JSON-RPC 2.0 + tarpc + REST |
| License | AGPL-3.0-only |
| ecoBin | Compliant (zero C deps in production) |
| UniBin | `sweetgrass server`, `sweetgrass status` |
| Zero-copy | BraidId, Did use Arc<str> |

---

## Supersedes

This is the first sweetGrass handoff to wateringHole. Previous sweetGrass
status was documented in phase2/archive/.
