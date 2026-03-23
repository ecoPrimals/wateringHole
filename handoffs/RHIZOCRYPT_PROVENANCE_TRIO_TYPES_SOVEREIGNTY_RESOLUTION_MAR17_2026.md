# rhizoCrypt: `provenance-trio-types` Sovereignty Resolution

**Date**: March 17, 2026
**For**: primalSpring, loamSpine, sweetGrass teams
**From**: rhizoCrypt team
**Re**: primalSpring coordination issue — `provenance-trio-types` resolution

---

## Decision: Option 2 — Inline Types (Sovereignty)

rhizoCrypt has chosen **Option 2: Inline the types** from the primalSpring
coordination issue. Each primal owns its own wire serialization types.
The shared contract is the **JSON schema on the wire**, not a shared
Rust crate.

This aligns with the core ecoPrimals sovereignty principle:

> *"Each primal stays sovereign. Orchestrate, don't embed."*

Compile-time coupling between primals is a boundary violation — it means
a change in one primal's types can break another primal's build. The
JSON-RPC wire format is the correct abstraction boundary.

---

## What rhizoCrypt Did

### Removed
- `provenance-trio-types` dependency from workspace `Cargo.toml`
- `provenance-trio-types` dependency from `rhizo-crypt-core/Cargo.toml`
- All `provenance_trio_types::` references in source code

### Added
- `crates/rhizo-crypt-core/src/dehydration_wire.rs` — rhizoCrypt-owned
  outbound wire types:
  - `DehydrationWireSummary` (maps to `contribution.record_dehydration` params)
  - `WireAgentRef` (per-agent participation detail)
  - `WireAttestationRef` (cryptographic attestation reference)
  - `WireOperationRef` (session operation reference)
- 3 roundtrip tests (minimal, full, extra-fields-tolerated)
- `From<&DehydrationSummary> for DehydrationWireSummary` conversion

### Wire Compatibility

The JSON output is **identical** to the previous `provenance-trio-types`
format. All field names, types, `#[serde(default)]`, and
`#[serde(skip_serializing_if)]` annotations are preserved. Receivers
(sweetGrass, any provenance endpoint) will see no wire-level change.

---

## Verification

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | 0 warnings |
| `cargo test --workspace --all-features` | **1330 tests**, 0 failures |
| `provenance-trio-types` in `Cargo.lock` | **Gone** |
| Cross-primal compile dependencies | **Zero** |

---

## Recommendation for loamSpine and sweetGrass

Each trio primal should do the same:

1. **Identify which types you import** from `provenance-trio-types`
2. **Define your own wire types** in an internal module (e.g., `wire.rs`)
3. **Match the JSON field names** exactly for wire compatibility
4. **Remove the path dependency** from your `Cargo.toml`
5. **Verify** with `cargo check` / `cargo test`

### Types used by each primal (from primalSpring's grep):

| Primal | Types Used | Direction |
|--------|-----------|-----------|
| **rhizoCrypt** | `DehydrationSummary`, `AgentRef`, `AttestationRef` | Produces (outbound) |
| **loamSpine** | `DehydrationSummary` | Consumes (inbound) |
| **sweetGrass** | `DehydrationSummary`, `PipelineRequest`, `PipelineResult` | Consumes + re-exports |

Each primal only needs to define the types it actually uses, with matching
serde annotations for the JSON fields it cares about. Forward-compatible
deserialization (`#[serde(default)]`) handles any fields the producer
adds that the consumer doesn't know about.

---

## For primalSpring

rhizoCrypt's dependency on `provenance-trio-types` is now eliminated.
Once loamSpine and sweetGrass do the same, the `phase2/provenance-trio-types/`
directory can be archived to the fossil record and all three trio
workspaces will build independently.

primalSpring's `capability.call` routing (`dag.*` → rhizoCrypt,
`commit.*` → loamSpine, `provenance.*` → sweetGrass) is correct and
unaffected — it was already wire-level only.

---

## The `provenance-trio-types` Crate

The crate at `phase2/provenance-trio-types/` can be:
- **Archived** to `ecoPrimals/archive/provenance-trio-types/` as fossil record
- **Deleted** once all three trio primals have inlined their types

It should **not** be maintained as a shared dependency going forward.
