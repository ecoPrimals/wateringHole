# Primal Emoji Standard

**Status:** Active
**Last Updated:** April 3, 2026
**Scope:** All ecoPrimals ecosystem entities — primals, springs, products, infra repos

---

## Purpose

Every entity in the ecoPrimals ecosystem has a canonical 2-emoji identity
derived from the semantic split of its camelCase name. The first emoji
represents the first word, the second represents the second word. This
mapping is the single source of truth — sporePrint, petalTongue, and any
future rendering surface references this standard.

Emojis serve as **semantic anchors** for wayfinding: they aid scanning,
reinforce the biological naming convention, and make the ecosystem
navigable at a glance. They are Tufte-approved — each justifies its space.

---

## Rules

1. **Two emojis per entity.** No more, no fewer.
2. **Derived from the camelCase split.** `barraCuda` → barra + Cuda → 🐟 + ⚡.
3. **Literal over metaphorical.** A toad is a toad, not a metaphor.
4. **Avoid ambiguity.** `toadStool` → 🐸🍄 (toad + mushroom), never a toad + a stool/chair.
5. **Springs share ♨️** as their second emoji — they are all "springs."
6. **This file is versioned.** Changes require a commit with rationale.

---

## Primals

| Entity | Split | Emoji | Rationale |
|--------|-------|:-----:|-----------|
| barraCuda | barra + Cuda | 🐟⚡ | Barracuda fish + lightning (CUDA speed) |
| toadStool | toad + Stool | 🐸🍄 | Toad + mushroom (toadstool = fungus) |
| coralReef | coral + Reef | 🪸🌊 | Coral + ocean wave |
| biomeOS | biome + OS | 🌿🖥️ | Ecosystem foliage + computer |
| bearDog | bear + Dog | 🐻🐕 | Bear + dog (amphicyonid) |
| nestGate | nest + Gate | 🪺🔒 | Nest + lock (security gateway) |
| songBird | song + Bird | 🎵🐦 | Musical note + bird |
| sweetGrass | sweet + Grass | 🍯🌾 | Honey sweetness + grain/grass |
| rhizoCrypt | rhizo + Crypt | 🌱🔐 | Root/seedling + encrypted lock |
| loamSpine | loam + Spine | 🪨📖 | Earth/stone + spine/book |
| petalTongue | petal + Tongue | 🌸👅 | Flower petal + tongue |
| Squirrel | squirrel + (brain) | 🐿️🧠 | Squirrel + brain (caching intelligence) |
| bingoCube | bingo + Cube | 🎲🧊 | Dice/chance + cube/ice |
| skunkBat | skunk + Bat | 🦨🦇 | Skunk + bat |

## Springs

All springs share ♨️ as their second emoji — they are validation
environments, hot springs of scientific rigor.

| Entity | Split | Emoji | Rationale |
|--------|-------|:-----:|-----------|
| wetSpring | wet + Spring | 💧♨️ | Water droplet + hot spring |
| hotSpring | hot + Spring | 🔥♨️ | Fire/heat + hot spring |
| airSpring | air + Spring | 🌬️♨️ | Wind/breeze + hot spring |
| neuralSpring | neural + Spring | 🧠♨️ | Brain/neural + hot spring |
| groundSpring | ground + Spring | ⛰️♨️ | Mountain/earth + hot spring |
| healthSpring | health + Spring | ❤️♨️ | Heart/health + hot spring |
| ludoSpring | ludo + Spring | 🎮♨️ | Game controller + hot spring |
| primalSpring | primal + Spring | 🧬♨️ | DNA/primal + hot spring |

## Products (sporeGarden)

| Entity | Split | Emoji | Rationale |
|--------|-------|:-----:|-----------|
| esotericWebb | esoteric + Webb | 🔮🕸️ | Crystal ball/arcane + web/spider silk |
| helixVision | helix + Vision | 🧬👁️ | DNA helix + eye/vision |

## Infrastructure Repos

| Entity | Split | Emoji | Rationale |
|--------|-------|:-----:|-----------|
| sporePrint | spore + Print | 🍄🖨️ | Mushroom spore + printer/imprint |
| wateringHole | watering + Hole | 💧🕳️ | Water + hole (gathering place) |
| whitePaper | white + Paper | 📄✍️ | Document + writing hand |

---

## Usage

### In Markdown (sporePrint, READMEs)

Inline with entity names in tables, headings, or first-mention prose:

```markdown
| 🐟⚡ | barraCuda | Pure mathematics — 806+ WGSL f64 shaders |
```

### In petalTongue (conversational / accessibility)

petalTongue resolves entity names to their emoji pairs for screen readers
and conversational display. The emoji pair is spoken as the entity name,
not the individual emoji descriptions.

### In Terminals / CLI

Optional — emoji rendering varies by terminal. Use only where the
terminal is known to support Unicode 15.0+.

---

## Evolution

This mapping is a living standard. Entities may be added as the ecosystem
grows. Existing mappings should only change with strong rationale (e.g.,
a better-supported emoji becomes available in a new Unicode version).

Changes to this file require:
- A commit message explaining the rationale
- Corresponding updates to sporePrint content that references the old emoji
- A version bump in petalTongue's emoji resolution table (when it exists)
