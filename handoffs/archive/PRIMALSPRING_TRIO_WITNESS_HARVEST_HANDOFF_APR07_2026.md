# Trio Witness Harvest — primalSpring Handoff

**Date**: 2026-04-07
**From**: primalSpring
**To**: wetSpring, ludoSpring, all springs consuming provenance
**Version**: trio witness evolution (rhizoCrypt 0.14.0-dev, loamSpine 0.9.16, sweetGrass 0.7.27)

---

## What changed in the trio

The provenance trio (`rhizoCrypt`, `loamSpine`, `sweetGrass`) evolved from a
crypto-only attestation model to a generalized **witness** model. Every
provenance event — whether a BearDog Ed25519 signature, a Blake3 hash
observation, a game checkpoint, or a conversation marker — flows through the
same `WireWitnessRef` wire type.

### Wire type: `WireWitnessRef`

| Field         | Type              | Required | Default       | Purpose                                    |
|---------------|-------------------|----------|---------------|--------------------------------------------|
| `agent`       | `String`          | yes      | —             | Who/what produced this witness              |
| `kind`        | `String`          | yes      | `"signature"` | Discriminant: signature, hash, checkpoint…  |
| `evidence`    | `String`          | yes      | `""`          | The payload (sig bytes, hash, marker text)  |
| `witnessed_at`| `u64`             | yes      | `0`           | Nanosecond Unix timestamp                   |
| `encoding`    | `String`          | yes      | `"hex"`       | How `evidence` is encoded (hex/base64/utf8/none) |
| `algorithm`   | `Option<String>`  | no       | `None`        | Crypto algorithm when `kind=signature`      |
| `tier`        | `Option<String>`  | no       | `None`        | Trust tier: local, gate, federation, open   |
| `context`     | `Option<String>`  | no       | `None`        | Freeform metadata (experiment ID, thread…)  |

### Key renames from prior wire format

| Before               | After              |
|----------------------|--------------------|
| `WireAttestationRef` | `WireWitnessRef`   |
| `signature` (field)  | `evidence`         |
| `attested_at`        | `witnessed_at`     |
| `attestations` (vec) | `witnesses`        |
| `Attestation` (sweetGrass) | `Witness`    |

### Non-crypto witness kinds

| `kind`        | `encoding` | `tier` | Example use                              |
|---------------|------------|--------|------------------------------------------|
| `"signature"` | base64/hex | local  | BearDog Ed25519 signature                |
| `"hash"`      | hex/utf8   | open   | Blake3 content hash observation          |
| `"checkpoint"`| none       | open   | Game state tick or pipeline stage marker |
| `"marker"`    | none       | open   | Conversation turn, workflow step         |
| `"timestamp"` | none       | open   | Pure temporal witness (no payload)       |

---

## BearDog-to-witness mapping

BearDog's `crypto.sign_ed25519` returns `{ signature: base64, algorithm: "Ed25519", key_id }`.
Map this to `WireWitnessRef`:

| BearDog field        | WireWitnessRef field | Value                |
|----------------------|----------------------|----------------------|
| `signature` (base64) | `evidence`          | verbatim base64      |
| `"Ed25519"`          | `algorithm`         | `"ed25519"`          |
| *(implied)*          | `encoding`          | `"base64"`           |
| *(implied)*          | `tier`              | `"local"`            |
| *(caller sets)*      | `kind`              | `"signature"`        |
| *(caller sets)*      | `agent`             | `"beardog:<gate_id>"`|
| *(caller sets)*      | `context`           | experiment/pipeline ID |

**Verification path**: caller extracts `evidence` from witness, passes it as
`signature` (base64) to `crypto.verify_ed25519` along with the original
message (base64) and public key (base64). BearDog returns `{ valid: bool }`.

**Remaining gap**: BearDog does not accept an `encoding` hint on the verify
request. If a witness has `encoding: "hex"` (e.g. from rhizoCrypt's internal
signing path), the caller must decode hex → raw bytes → base64 before calling
BearDog. A future BearDog evolution should accept encoding on the verify wire.

---

## Anderson QS provenance story — reference pipeline

This is the concrete reference pattern for wetSpring and any spring building
reproducible science pipelines.

### Pipeline flow

```
1. INGEST
   NCBI/EPA data → NestGate blob store
   → rhizoCrypt: kind:"hash", evidence:<blake3>, encoding:"hex", tier:"open"
     (content hash observation — no crypto, just a record that this data arrived)

2. PROCESS
   science.diversity → science.qs_model → science.anderson
   → each step appends a vertex to the rhizoCrypt DAG session
   → kind:"checkpoint", context:"anderson:diversity:step1"

3. SIGN
   Pipeline completes → rhizoCrypt dehydrates (merkle root of DAG)
   → BearDog signs the merkle root
   → kind:"signature", evidence:<base64>, encoding:"base64",
     algorithm:"ed25519", tier:"local"

4. COMMIT
   loamSpine permanent commit with all witnesses attached
   → immutable record including hash witnesses + signature witness

5. ATTRIBUTE
   sweetGrass braid retains witnesses on EcoPrimalsAttributes.witnesses
   → attribution record: who ran the pipeline, when, what data, what results

6. REPRODUCE
   Recipient reads braid → follows lineage through trio:
   - sweetGrass: who attributed this?
   - loamSpine: what was committed?
   - rhizoCrypt: what was the DAG? verify merkle root
   - BearDog: verify the signature witness
   Every step is provable. Hand to someone, they can re-enter and examine.
```

### What this enables

- **Reproducibility**: Every computation step has a witness. Re-run the
  pipeline, get the same DAG, same merkle root, same content hashes.
- **Rigor**: Signed witnesses prove who computed what and when. Unsigned
  witnesses (checkpoints, hashes) provide the audit trail.
- **Portability**: The witness wire type is primal-agnostic. Any spring can
  emit witnesses, any consumer can read them. BearDog signs when crypto is
  needed; the trio records regardless.

---

## What springs need to update

### wetSpring

`ipc/provenance.rs` currently builds attestation-style metadata. Adopt the
`WireWitnessRef` wire type:

- Rename `attestation` references to `witness`
- Use `kind` to discriminate hash observations vs signatures
- Set `encoding` explicitly on every witness (base64 for BearDog, hex for
  blake3, none for checkpoints)
- Add `context` for pipeline step identification

### All springs

- When emitting provenance metadata, construct `WireWitnessRef`-shaped JSON
- When verifying, dispatch by `kind` and `encoding`:
  - `kind: "signature"` → call BearDog verify (decode per `encoding`)
  - `kind: "hash"` → recompute hash and compare `evidence`
  - `kind: "checkpoint"` / `"marker"` / `"timestamp"` → audit trail only

---

## plasmidBin status

Trio binaries harvested to `infra/plasmidBin/primals/` (x86_64-linux-gnu for
loamSpine/sweetGrass, x86_64-linux-musl for rhizoCrypt). Checksums updated in
`checksums.toml`. Manifest versions bumped. Doctor script verifies trio
checksums. rhizoCrypt musl-static shipped (April 2026); loamSpine and sweetGrass
musl-static builds tracked but not yet available.

### Validation

`exp089_beardog_witness_roundtrip` in primalSpring validates:
1. Offline witness JSON round-trip (all field types preserved)
2. Non-crypto witness variants (checkpoint, marker, hash, timestamp)
3. Live BearDog sign → witness wrap → BearDog verify (when BearDog available)

---

## Files changed

**Trio primals** (committed separately in each primal repo):
- `rhizoCrypt/crates/rhizo-crypt-core/src/dehydration_wire.rs` — `WireWitnessRef`
- `rhizoCrypt/crates/rhizo-crypt-core/src/dehydration.rs` — `From` impl
- `loamSpine/crates/loam-spine-core/src/trio_types.rs` — `WireWitnessRef`
- `sweetGrass/crates/sweet-grass-core/src/dehydration.rs` — `Witness`
- `sweetGrass/crates/sweet-grass-core/src/braid/types.rs` — `EcoPrimalsAttributes.witnesses`
- `sweetGrass/crates/sweet-grass-service/src/handlers/jsonrpc/contribution.rs`

**primalSpring**:
- `experiments/exp089_beardog_witness_roundtrip/` — validation binary
- `config/capability_registry.toml` — BearDog crypto capabilities + witness mapping

**infra/plasmidBin**:
- `checksums.toml` — trio blake3 hashes (x86_64-linux-gnu)
- `manifest.toml` — trio version bumps
- `doctor.sh` — trio in checksum verification loop
- `deploy_gate.sh` — provenance + nucleus-full compositions documented

**infra/wateringHole**:
- `ATTESTATION_ENCODING_STANDARD.md` — rewritten as witness standard
- `SPRING_PROVENANCE_PATTERN.md` — updated cross-references
