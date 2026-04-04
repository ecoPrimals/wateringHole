# sporeGarden Deployment Standard

**Purpose:** How gen4 products compose primals into deployable tools via the
BYOB (Bring Your Own Binaries) model.

**Last Updated:** March 29, 2026

---

## What is a sporeGarden Product?

A **sporeGarden product** is a gen4 artifact — a tool that end users actually
run. It composes primals into a user-facing experience. Products consume deployed
binaries via IPC; they never import primal source code.

| Layer | What | Example |
|-------|------|---------|
| gen2 | Primals (capabilities) | BearDog, Songbird, biomeOS |
| gen3 | Springs (validation) | primalSpring, wetSpring, ludoSpring |
| gen4 | Products (surface) | esotericWebb, helixVision |

Products live in the `sporeGarden/` GitHub organization.

---

## The BYOB Model

**Bring Your Own Binaries.** Products do not compile primals. They consume
pre-built ecoBin-compliant binaries from `plasmidBin/`.

### Binary Flow

```
Primal team builds    →  harvest.sh creates Release  →  plasmidBin/ (GitHub)
Product team fetches  →  fetch.sh populates local     →  product/plasmidBin/
Product deploys       →  biomeOS graph germinates     →  primals running
Product interacts     →  JSON-RPC via PrimalBridge    →  capabilities active
```

### Why BYOB?

1. **Zero source coupling:** Products never see primal internals
2. **Multi-arch:** plasmidBin carries x86_64 and aarch64 binaries
3. **Versioned:** Each release is checksummed and tagged
4. **Offline-capable:** Once fetched, binaries are local — no network needed at runtime

---

## esotericWebb as Reference Implementation

[esotericWebb](https://github.com/sporeGarden/esotericWebb) is the first gen4
product. It composes 8 primal domains into a CRPG engine.

### Product Structure

```
esotericWebb/
├── config/
│   └── primal_launch_profiles.toml   # How to invoke each binary
├── graphs/
│   └── esotericwebb_full.toml        # biomeOS deploy graph (Sequential, 8 phases)
├── niches/
│   └── esoteric-webb.yaml            # Niche metadata (organisms, interactions)
├── plasmidBin/                       # Fetched primal binaries (gitignored)
├── src/
│   └── bridge/                       # PrimalBridge: JSON-RPC client wrappers
└── content/                          # Product-specific content (narrative assets)
```

### Primal Domains Consumed

| Domain | Primal | Required | Role |
|--------|--------|----------|------|
| security | BearDog | yes | Crypto, signing, identity |
| discovery | Songbird | yes | Peer discovery, mesh |
| game | ludoSpring | yes | Game science (flow, DDA, sessions) |
| visualization | petalTongue | yes | Scene rendering, interaction |
| ai | Squirrel | yes | AI narration, inference |
| compute | ToadStool | no | GPU compute (graceful skip) |
| provenance | rhizoCrypt | no | Session DAG (graceful skip) |
| certificate | LoamSpine | no | Session certificates (graceful skip) |
| attribution | sweetGrass | no | Provenance attribution (graceful skip) |

### Graceful Degradation

Products **must** handle absent primals. esotericWebb's `PrimalBridge` checks
capability availability at startup and disables features when optional primals
are missing. The user experience degrades gracefully — the game works without
GPU compute or provenance, just with reduced features.

---

## Deploying a sporeGarden Product

### Step 1: Fetch Binaries

```bash
cd esotericWebb
./scripts/fetch_primals.sh    # Populates plasmidBin/ from GitHub Releases
```

Or manually:
```bash
cd plasmidBin
../../infra/plasmidBin/fetch.sh --arch x86_64
```

### Step 2: Deploy via biomeOS

```bash
biomeos deploy --graph graphs/esotericwebb_full.toml
```

biomeOS reads the graph, spawns primals in dependency order, waits for health
probes, and wires capabilities.

### Step 3: Start the Product

```bash
cargo run --release --bin esotericwebb -- server
```

The product discovers primals via socket discovery and begins issuing JSON-RPC
calls through the PrimalBridge.

---

## Environment Contract

Products and biomeOS share a minimal environment contract. These variables
control composition behavior.

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `FAMILY_ID` | Genetic lineage identifier for the deployment | `my-family-seed-hash` |

### Standard

| Variable | Description | Default |
|----------|-------------|---------|
| `BIOMEOS_SOCKET_DIR` | Socket directory for primal IPC | `$XDG_RUNTIME_DIR/biomeos` |
| `XDG_RUNTIME_DIR` | XDG runtime directory | `/run/user/$UID` |

### Per-Primal Overrides

| Variable | Description |
|----------|-------------|
| `BEARDOG_SOCKET` | Direct socket path for BearDog |
| `SONGBIRD_SOCKET` | Direct socket path for Songbird |
| `{PRIMAL}_SOCKET` | Pattern: direct socket path for any primal |
| `{PRIMAL}_TCP` | Pattern: direct TCP endpoint (host:port) |

### Dark Forest Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SONGBIRD_DARK_FOREST` | Enable Dark Forest beacon mode | `false` |
| `SONGBIRD_ACCEPT_LEGACY_BIRDSONG` | Accept legacy plaintext beacons | `false` |
| `SONGBIRD_DUAL_BROADCAST` | Broadcast both encrypted and legacy beacons | `false` |
| `BEARDOG_BEACON_SEED` | Path to beacon seed file | — |

---

## Relationship to biomeOS

biomeOS is the orchestrator. The product is the consumer. Their responsibilities
are cleanly separated:

| Responsibility | Owner |
|----------------|-------|
| Parse deploy graph | biomeOS |
| Germinate primals | biomeOS |
| Health probe primals | biomeOS |
| Register capabilities in Neural API | biomeOS |
| Socket discovery | biomeOS |
| Define deploy graph | Product |
| Define niche YAML | Product |
| Define launch profiles | Product |
| Issue capability calls via PrimalBridge | Product |
| Handle graceful degradation | Product |
| Fetch binaries from plasmidBin | Product |

The product provides the graph, niche, and launch config. biomeOS executes it.
The product then interacts with running primals via JSON-RPC.

---

## Creating a New sporeGarden Product

1. **Create the repository** in `sporeGarden/` org
2. **Define the niche YAML** — organisms, interactions, customization
3. **Define the deploy graph** — germination order, dependencies, capabilities
4. **Define launch profiles** — per-primal invocation config
5. **Write a PrimalBridge** — JSON-RPC client wrappers for consumed capabilities
6. **Handle degradation** — every optional primal has a fallback path
7. **Fetch binaries** — use `plasmidBin/fetch.sh` or write a product-specific script
8. **Test locally** — `biomeos deploy --graph ...` then exercise capabilities

### Quality Gates

- Product builds and runs with only `required: true` primals
- Product degrades gracefully when each optional primal is absent
- Product's deploy graph validates with `biomeos validate --graph ...`
- All PrimalBridge calls use semantic method names per `SEMANTIC_METHOD_NAMING_STANDARD.md`
- Product has zero primal source imports (BYOB compliance)

---

## Related Documents

- `COMPOSITION_PATTERNS.md` — Graph formats, niche YAML, launch profiles, socket discovery
- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC 2.0 wire protocol for primal communication
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — Method naming conventions
- `GEN4_BRIDGE.md` — How primals become products
- `ECOBIN_ARCHITECTURE_STANDARD.md` — Binary portability standard
- `GENOMEBIN_ARCHITECTURE_STANDARD.md` — Autonomous deployment wrapper
