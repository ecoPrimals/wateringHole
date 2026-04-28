# Collectible Composition Pattern — Provenance Trio for Digital Assets

**From**: primalSpring v0.9.17 (Phase 45c — Graphics Node)
**Date**: April 26, 2026
**For**: All spring teams + garden teams (especially ludoSpring, esotericWebb)

---

## Overview

Digital collectibles (items, achievements, certificates, game assets) are
a composition-level pattern built on the existing provenance trio IPC
methods. **No new primal code is needed.** This document defines the
convention for mapping the trio's existing capabilities to a collectible
lifecycle.

---

## The Provenance Trio

| Primal | Role | Key Methods |
|--------|------|-------------|
| **rhizoCrypt** | Working memory — ephemeral DAG of game events | `dag.session.create`, `dag.event.append`, `dag.event.append_batch`, `dag.vertex.get`, `dag.vertex.query`, `dag.vertex.children`, `dag.frontier.get`, `dag.genesis.get`, `dag.merkle.root`, `dag.merkle.proof`, `dag.merkle.verify`, `dag.slice.checkout`, `dag.dehydration.trigger` |
| **loamSpine** | Permanent ledger — immutable records + certificates | `spine.create`, `spine.seal`, `entry.append`, `entry.get`, `entry.get_tip`, `certificate.mint`, `certificate.transfer`, `certificate.loan`, `certificate.return`, `certificate.get`, `proof.generate_inclusion`, `proof.verify_inclusion`, `anchor.publish`, `anchor.verify` |
| **sweetGrass** | Provenance — attribution chains + PROV-O export | `braid.create`, `braid.commit`, `braid.query`, `anchoring.anchor`, `anchoring.verify`, `provenance.graph`, `provenance.export_provo`, `attribution.chain`, `attribution.calculate_rewards`, `contribution.record`, `pipeline.attribute` |

---

## Collectible Lifecycle — Method Mapping

### Phase 1: Create

A collectible is born when a game event (loot drop, crafting, achievement)
triggers a mint. The composition calls three primals in sequence.

```
Step 1: Record the creation event
  → rhizoCrypt: dag.event.append
    {
      "session_id": "<active game session>",
      "event_type": "ItemLoot",
      "metadata": [
        {"key": "item_id", "value": "sword-of-truth-001"},
        {"key": "rarity", "value": "legendary"},
        {"key": "source", "value": "boss-drop:dragon-king"},
        {"key": "player_id", "value": "<player DID>"}
      ]
    }

Step 2: Mint a certificate of ownership
  → loamSpine: certificate.mint
    {
      "spine_id": "<game collectibles spine>",
      "certificate_type": "collectible",
      "owner": "<player DID>",
      "payload": "<BLAKE3 hash of item metadata>"
    }

Step 3: Record provenance
  → sweetGrass: contribution.record
    {
      "hash": "<certificate hash>",
      "agent": "<player DID>",
      "action": "create",
      "source": "game:boss-drop"
    }
```

### Phase 2: Track / Interact

During gameplay, events involving the collectible are appended to the
session DAG. This creates an auditable history.

```
Player equips item:
  → rhizoCrypt: dag.event.append
    { "event_type": "Custom",
      "domain": "collectible", "event_name": "equip",
      "metadata": [{"key": "item_id", "value": "sword-of-truth-001"}] }

Player uses item in combat:
  → rhizoCrypt: dag.event.append
    { "event_type": "GameEvent",
      "metadata": [
        {"key": "item_id", "value": "sword-of-truth-001"},
        {"key": "action", "value": "attack"},
        {"key": "damage", "value": "142.5"}
      ] }
```

### Phase 3: Transfer

When a collectible changes ownership (trade, gift, marketplace sale),
the composition calls the trio to record the transfer.

```
Step 1: Transfer certificate
  → loamSpine: certificate.transfer
    {
      "certificate_id": "<cert-uuid>",
      "from": "<seller DID>",
      "to": "<buyer DID>"
    }

Step 2: Record transfer event
  → rhizoCrypt: dag.event.append
    { "event_type": "ItemTransfer",
      "metadata": [
        {"key": "item_id", "value": "sword-of-truth-001"},
        {"key": "from", "value": "<seller DID>"},
        {"key": "to", "value": "<buyer DID>"},
        {"key": "price", "value": "500 gold"}
      ] }

Step 3: Update attribution chain
  → sweetGrass: contribution.record
    {
      "hash": "<certificate hash>",
      "agent": "<buyer DID>",
      "action": "transfer",
      "source": "game:marketplace"
    }
```

### Phase 4: Loan / Borrow

For temporary ownership (rental, borrowing in co-op):

```
Loan out:
  → loamSpine: certificate.loan
    { "certificate_id": "<cert-uuid>", "borrower": "<borrower DID>" }

Return:
  → loamSpine: certificate.return
    { "certificate_id": "<cert-uuid>" }
```

### Phase 5: Verify / Audit

Query the collectible's full history and prove authenticity.

```
View ownership chain:
  → sweetGrass: attribution.chain
    { "hash": "<certificate hash>" }
  Returns: ordered list of agents and actions

View full provenance graph:
  → sweetGrass: provenance.graph
    { "hash": "<certificate hash>" }
  Returns: entity/activity/agent graph (W3C PROV model)

Export as PROV-O (for external audit):
  → sweetGrass: provenance.export_provo
    { "hash": "<certificate hash>" }
  Returns: RDF/Turtle provenance document

Verify Merkle inclusion:
  → rhizoCrypt: dag.merkle.proof
    { "session_id": "<session>", "vertex_id": "<event vertex>" }
  → rhizoCrypt: dag.merkle.verify
    { "root": "<root hash>", "proof": "<proof>", "vertex_id": "<id>" }

Verify on permanent ledger:
  → loamSpine: proof.generate_inclusion
    { "spine_id": "<spine>", "entry_id": "<entry>" }
  → loamSpine: proof.verify_inclusion
    { "proof": "<proof>", "root": "<root>" }
```

### Phase 6: Persist / Archive

When a game session ends, flush ephemeral state to permanence.

```
Dehydrate session:
  → rhizoCrypt: dag.dehydration.trigger
    { "session_id": "<session>" }

Commit to permanent ledger:
  → loamSpine: permanence.commit_session
    { "session_id": "<dehydrated session>" }

Anchor for external verification:
  → loamSpine: anchor.publish
    { "spine_id": "<spine>", "anchor_type": "periodic" }
  → sweetGrass: anchoring.anchor
    { "hash": "<anchor hash>", "target": "ledger" }
```

---

## Visualization via petalTongue

The collectible pattern maps naturally to petalTongue visualization bindings.

### Inventory display

Push an inventory view using `visualization.render`:

```json
{
  "method": "visualization.render",
  "params": {
    "session_id": "inventory-001",
    "title": "Player Inventory",
    "bindings": [
      {
        "channel_type": "bar",
        "id": "item-stats",
        "label": "Equipped Items",
        "categories": ["Sword of Truth", "Shield of Light", "Helm of Wisdom"],
        "values": [142.5, 85.0, 45.0],
        "unit": "power"
      },
      {
        "channel_type": "gauge",
        "id": "inventory-count",
        "label": "Inventory Slots",
        "value": 12.0,
        "min": 0.0,
        "max": 20.0,
        "unit": "items",
        "normal_range": [0.0, 15.0],
        "warning_range": [15.0, 18.0]
      }
    ],
    "domain": "collectibles"
  }
}
```

### Provenance timeline

Use `visualization.render.grammar` for a declarative provenance timeline:

```json
{
  "method": "visualization.render.grammar",
  "params": {
    "session_id": "provenance-timeline",
    "expressions": [
      {
        "data": [
          {"timestamp": 1714150000, "agent": "player-A", "action": "create", "label": "Minted"},
          {"timestamp": 1714153600, "agent": "player-A", "action": "equip", "label": "Equipped"},
          {"timestamp": 1714160800, "agent": "player-B", "action": "transfer", "label": "Traded"},
          {"timestamp": 1714164400, "agent": "player-B", "action": "equip", "label": "Equipped"}
        ],
        "geometry": "point",
        "aesthetics": {
          "x": {"field": "timestamp", "role": "X"},
          "y": {"field": "agent", "role": "Y"},
          "color": {"field": "action", "role": "Color"},
          "label": {"field": "label", "role": "Label"}
        }
      }
    ]
  }
}
```

---

## Cell Graph Requirements

Any cell graph using the collectible pattern must include the provenance
trio with expanded capabilities. The minimum trio capabilities for
collectibles are:

```toml
# rhizoCrypt — working memory
capabilities = [
    "dag.session.create",
    "dag.event.append",
    "dag.event.append_batch",
    "dag.vertex.get",
    "dag.vertex.query",
    "dag.merkle.root",
    "dag.merkle.proof",
    "dag.merkle.verify",
    "dag.dehydration.trigger",
]

# loamSpine — permanent ledger
capabilities = [
    "spine.create",
    "entry.append",
    "entry.get",
    "certificate.mint",
    "certificate.transfer",
    "certificate.loan",
    "certificate.return",
    "certificate.get",
    "proof.generate_inclusion",
    "anchor.publish",
    "permanence.commit_session",
]

# sweetGrass — provenance
capabilities = [
    "braid.create",
    "braid.commit",
    "anchoring.anchor",
    "anchoring.verify",
    "provenance.graph",
    "provenance.export_provo",
    "attribution.chain",
    "contribution.record",
    "pipeline.attribute",
]
```

---

## Validation Capabilities for Downstream Manifests

Springs using the collectible pattern should add these to their
`validation_capabilities` in `downstream_manifest.toml`:

```toml
validation_capabilities = [
    # ... existing science capabilities ...
    # Collectible lifecycle (provenance trio)
    "dag.session.create",
    "dag.event.append",
    "dag.merkle.proof",
    "certificate.mint",
    "certificate.transfer",
    "certificate.get",
    "provenance.graph",
    "attribution.chain",
    "contribution.record",
]
```

---

**References**:
- rhizoCrypt handler: `rhizoCrypt/crates/rhizo-crypt-rpc/src/jsonrpc/handler/mod.rs`
- loamSpine API: `loamSpine/crates/loam-spine-api/src/jsonrpc/mod.rs`
- sweetGrass handlers: `sweetGrass/crates/sweet-grass-service/src/handlers/jsonrpc/mod.rs`
- ludoSpring cell: `primalSpring/graphs/cells/ludospring_cell.toml`
- esotericWebb cell: `primalSpring/graphs/cells/esotericwebb_cell.toml`
- Downstream manifest: `primalSpring/graphs/downstream/downstream_manifest.toml`

License: AGPL-3.0-or-later
