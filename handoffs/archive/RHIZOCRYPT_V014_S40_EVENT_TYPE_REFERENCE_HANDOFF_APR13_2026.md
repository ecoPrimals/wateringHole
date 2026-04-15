# rhizoCrypt v0.14.0-dev — S40 Event Type Reference Handoff

**Date**: April 13, 2026
**Session**: 40
**Focus**: Canonical `dag.event.append` EventType documentation for domain springs

---

## Context

primalSpring identified during NUCLEUS validation (Phases 39–41) that domain springs
(wetSpring, hotSpring, groundSpring, airSpring, etc.) need canonical documentation of
`dag.event.append` event type variants. primalSpring created a 27-variant reference in
`graphs/downstream/README.md`, but noted the canonical docs should live upstream in
rhizoCrypt's own repo.

**Problem**: primalSpring's downstream reference had inaccurate field names for most
variants (e.g., `data_id` instead of `schema`, `experiment_id` instead of `protocol`,
`item_id` instead of `item_type`). Domain springs following the downstream docs would
build against wrong wire contracts.

## Resolution

### Created: `specs/EVENT_TYPE_REFERENCE.md`

Canonical 27-variant wire format reference with:
- Correct Rust field names matching `pub enum EventType` in `event.rs`
- JSON wire examples for every variant (externally-tagged serde format)
- Sub-enum documentation (`SessionOutcome`, `AgentRole`, `LeaveReason`, `SliceMode`, `ResolutionType`)
- Domain mapping table (which variants belong to which domain)
- Guidance for domain springs (when to use built-in vs `Custom`, metadata patterns)

### Enhanced: `crates/rhizo-crypt-core/src/event.rs`

- Module docs now describe the 27-variant / 7-domain structure
- Wire format documentation (externally-tagged JSON representation)
- `EventType` doc comment references the spec

### Updated: `specs/00_SPECIFICATIONS_INDEX.md`

- Added `EVENT_TYPE_REFERENCE.md` to the Protocol Specifications section

## Key Field Corrections vs primalSpring Downstream

| Variant | primalSpring Field | Actual Field |
|---------|-------------------|-------------|
| `DataCreate` | `data_id`, `description` | `schema: Option<String>` |
| `AgentAction` | `agent_id`, `action`, `description` | `action: String` |
| `ExperimentStart` | `experiment_id`, `description` | `protocol: String` |
| `AgentJoin` | `agent_id` | `role: AgentRole` |
| `AgentLeave` | `agent_id` | `reason: LeaveReason` |
| `Combat` | `participants` | `target: Did`, `outcome: String` |
| `ItemLoot` | `item_id` | `item_type: String` |
| `Result` | `result_id` | `confidence_percent: u8` |
| `Custom` | `kind`, `data` | `domain: String`, `event_name: String` |

Domain springs should now reference `rhizoCrypt/specs/EVENT_TYPE_REFERENCE.md`
as the authoritative source for `dag.event.append` wire contracts.
