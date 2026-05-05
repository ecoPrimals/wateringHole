SPDX-License-Identifier: AGPL-3.0-or-later

# Witness standard: self-describing provenance events

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Date** | 2026-04-06 |
| **Status** | Canonical |

## Principle: the trio tracks events, not crypto

The provenance trio (`rhizoCrypt`, `loamSpine`, `sweetGrass`) records that
**something occurred**. That something may be cryptographically signed,
hash-observed, checkpointed, marked, or simply timestamped. The trio is
agnostic to algorithms, encodings, and whether cryptography is involved at all.

A session with zero signatures is valid provenance. A game state with only
checkpoint witnesses is valid provenance. A conversation web with only marker
witnesses is valid provenance.

## Each primal stands alone

Provenance is the trio's most tightly coupled niche, but each primal has
independent uses across any biome:

| Primal | Core function | Example solo uses |
|--------|--------------|-------------------|
| `rhizoCrypt` | Ephemeral DAG sessions | Game state history, conversation webs, experiment branches |
| `loamSpine` | Permanent append-only ledger | Audit logs, commit chains, anchor receipts |
| `sweetGrass` | Attribution braids | Co-authorship, team play, collaborative editing |

The trio composes into `RootPulse`, NUCLEUS science pipelines, and any
future lineage-bearing workflow via Neural API graphs. But each primal
ingests and outputs anything — the biome dictates the content.

## `BearDog` is the crypto authority (when crypto is involved)

When a witness *is* cryptographic (`kind: "signature"`), signing and
verification route through `BearDog` (`crypto.sign`, `crypto.verify`).
External crypto providers (public chains, HSMs, notaries) are also valid.
The trio never decodes, validates, or transforms evidence.

When a witness is *not* cryptographic, no crypto provider is needed.

## Wire type: `WireWitnessRef`

Each trio primal owns its own copy (primal sovereignty). The JSON shape is
the contract.

### Rust struct (canonical shape)

```rust
pub struct WireWitnessRef {
    pub agent: String,
    #[serde(default = "default_witness_kind")]
    pub kind: String,
    #[serde(default)]
    pub evidence: String,
    #[serde(default)]
    pub witnessed_at: u64,
    #[serde(default = "default_witness_encoding")]
    pub encoding: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub algorithm: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tier: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub context: Option<String>,
}
```

### Signed witness (crypto)

```json
{
  "agent": "did:key:z6MkAlice",
  "kind": "signature",
  "evidence": "deadbeef01234567...",
  "witnessed_at": 1712000000000000000,
  "encoding": "hex",
  "algorithm": "ed25519",
  "tier": "local"
}
```

### Game checkpoint (no crypto)

```json
{
  "agent": "ludospring:engine",
  "kind": "checkpoint",
  "evidence": "",
  "witnessed_at": 1712000000000000000,
  "encoding": "none",
  "tier": "open",
  "context": "game:tick:4200"
}
```

### Conversation marker

```json
{
  "agent": "did:key:z6MkBob",
  "kind": "marker",
  "evidence": "",
  "witnessed_at": 1712000000000000000,
  "encoding": "none",
  "tier": "open",
  "context": "conversation:thread:abc:turn:17"
}
```

### Hash observation

```json
{
  "agent": "wetspring:pipeline",
  "kind": "hash",
  "evidence": "blake3:abc123...",
  "witnessed_at": 1712000000000000000,
  "encoding": "utf8",
  "context": "experiment:run:7:output_hash"
}
```

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `agent` | string | yes | — | DID or identifier of the witnessing agent/system |
| `kind` | string | no | `"signature"` | What this witness represents |
| `evidence` | string | no | `""` | Evidence payload (opaque) |
| `witnessed_at` | u64 | no | `0` | Nanoseconds since epoch |
| `encoding` | string | no | `"hex"` | How the evidence payload is encoded |
| `algorithm` | string | no | `null` | Crypto algorithm (when `kind` = `"signature"`) |
| `tier` | string | no | `null` | Provenance tier |
| `context` | string | no | `null` | Freeform context for the witness |

### `kind` values

| Value | Description | Needs crypto? |
|-------|-------------|---------------|
| `"signature"` | Cryptographic signature over data | Yes |
| `"hash"` | Hash observation — witnessed a hash at a point in time | No |
| `"checkpoint"` | State snapshot — game tick, model weights, editor state | No |
| `"marker"` | Boundary or event marker — conversation turn, session boundary | No |
| `"timestamp"` | Bare time witness — attests only that an event occurred | No |
| *(extensible)* | Any string meaningful to the producing biome | Varies |

### `encoding` values

| Value | Description |
|-------|-------------|
| `"hex"` | Hexadecimal (lowercase). Default — `rhizoCrypt`/`BearDog` convention |
| `"base64"` | Standard Base64 (RFC 4648 §4) |
| `"base64url"` | URL-safe Base64 (RFC 4648 §5) |
| `"multibase"` | Self-identifying per [Multibase spec](https://github.com/multiformats/multibase) |
| `"utf8"` | Plain text (hash strings, human-readable tokens) |
| `"none"` | No encoding — evidence is empty or not applicable |

### `tier` values

| Value | Description |
|-------|-------------|
| `"local"` | `BearDog` on the same gate |
| `"gateway"` | `BearDog` on a remote gate |
| `"anchor"` | Public chain timestamp service |
| `"external"` | Third-party HSM or notary |
| `"open"` | No cryptographic backing — unsigned witness |

### `algorithm` values (when `kind` = `"signature"`)

| Value | Description |
|-------|-------------|
| `"ed25519"` | Ed25519 (RFC 8032). `BearDog` default |
| `"ed25519-birdsong"` | Ed25519 with Birdsong key exchange extension |
| `"ecdsa-p256"` | ECDSA over P-256 (NIST). Common for external anchors |
| *(extensible)* | Any string recognized by the target verifier |

## Container field: `witnesses`

On parent wire types (`DehydrationWireSummary`, `WireDehydrationSummary`,
`DehydrationSummary`, `EcoPrimalsAttributes`), the container field is
**`witnesses: Vec<WireWitnessRef>`** (or the primal's local witness type).

## Composition flow

```text
Producer (any system)
  ├── BearDog signs          → kind: "signature", evidence: hex sig, algorithm: ed25519
  ├── Game engine             → kind: "checkpoint", evidence: "", context: "tick:42"
  ├── Conversation system     → kind: "marker", evidence: "", context: "thread:abc"
  ├── Science pipeline        → kind: "hash", evidence: "blake3:...", context: "run:7"
  └── External anchor         → kind: "signature", evidence: base64url sig, algorithm: ecdsa-p256
         ↓
trio (carries witnesses, never interprets)
  rhizoCrypt → loamSpine → sweetGrass
         ↓
Consumer (when verification needed)
  └── reads kind + encoding + algorithm → routes to BearDog or external verifier
```

## Rules

1. **Producers set metadata.** The system creating the witness populates
   `kind`, `encoding`, and any relevant optional fields.
2. **Trio passes through.** `rhizoCrypt`, `loamSpine`, and `sweetGrass` carry
   witnesses opaquely. They never decode, validate, or transform evidence.
3. **Crypto is one kind of witness.** The trio does not assume crypto. A
   session with zero signatures is valid provenance.
4. **Individual primal use.** Each trio primal functions independently across
   biomes. A game engine may use `rhizoCrypt` alone for state history with
   checkpoint witnesses and no signatures.
5. **`BearDog` is the crypto starting point.** When `kind` = `"signature"`,
   verification routes to `BearDog`. For non-crypto witnesses, no verifier
   is needed.
6. **The encoding is provenance.** Different evidence payloads use different
   encodings. The metadata distinguishes them — the trio does not normalize.

## Related documents

- `SPRING_PROVENANCE_PATTERN.md` — tiered provenance API responses
- `DEPLOYMENT_AND_COMPOSITION.md` §The Composition Principle
- `CAPABILITY_DOMAIN_REGISTRY.md` — `crypto.*` domain
- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC wire conventions
