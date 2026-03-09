# petalTongue @ wateringHole

Cross-primal integration documentation for petalTongue.

**Updated**: March 8, 2026

---

## Integration Status

petalTongue v1.3.0 (17 crates, edition 2024):
- 1,309 tests passing, 0 failures
- `#![forbid(unsafe_code)]` on 5 crates (core, telemetry, primitives, animation, headless)
- JSON-RPC 2.0 over Unix sockets (primary IPC)
- tarpc binary RPC (secondary, zero-copy `bytes::Bytes`)
- HTTP fallback for browser/external clients
- Capability-based discovery via Songbird
- healthSpring `DataChannel` types (TimeSeries, Distribution, Bar, Gauge)
- Multi-modal rendering: egui GUI, ratatui TUI, audio sonification, SVG, PNG, headless

### Grammar of Graphics Evolution (In Progress)

petalTongue is evolving from fixed widgets to a **Grammar of Graphics** engine.
Any primal can send a grammar expression via JSON-RPC, and petalTongue will render
it across all available modalities. This replaces per-domain ad-hoc rendering with
a single composable pipeline.

**If your primal has data that humans need to understand, read
[VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md).**

Key new capabilities (design phase):
- Declarative grammar expressions (data → variables → scales → geometry → coordinates)
- Tufte constraint system (data-ink ratio, lie factor, accessibility checks)
- barraCuda GPU compute offload for heavy statistics and 3D tessellation
- Inverse scale pipeline for interactive data exploration
- Streaming visualization for real-time data
- Domain-agnostic: same grammar renders molecules, game worlds, ecosystem topology

---

## For Other Primals

### Visualizing Your Data (New)

The simplest way to get petalTongue to visualize your primal's data:

1. Announce your data capabilities via Songbird discovery
2. Expose `{domain}.get` and `{domain}.schema` JSON-RPC methods
3. Send a `visualization.render` request with a grammar expression (or just raw data)

petalTongue handles modality selection, accessibility, Tufte compliance, and
barraCuda compute offload automatically.

See **[VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md)** for
the full grammar reference, domain examples, and sovereignty checklist.

### biomeOS Integration

petalTongue discovers biomeOS via:
1. `BIOMEOS_NEURAL_API_SOCKET` env var (explicit override)
2. `$XDG_RUNTIME_DIR/biomeos/neural-api.sock` (XDG standard)
3. `/tmp/biomeos-neural-api.sock` (legacy fallback)

API endpoints petalTongue consumes:
- `GET /api/v1/health` -- Health check
- `GET /api/v1/primals` -- List discovered primals
- `GET /api/v1/topology` -- Graph structure (nodes + edges)
- JSON-RPC 2.0 over Unix socket (9 methods)

See [BIOMEOS_API_SPECIFICATION.md](./BIOMEOS_API_SPECIFICATION.md) for details.

### healthSpring Integration

petalTongue renders healthSpring diagnostic data via `DataChannel`:
- `TimeSeries` -- Line charts (PK curves, RR tachograms)
- `Distribution` -- Histograms with mean/SD/patient markers
- `Bar` -- Categorical bar charts (microbiome abundances)
- `Gauge` -- Progress bars with normal/warning ranges

These map to grammar geometries: `TimeSeries` → `GeomLine` + `TemporalScale`,
`Distribution` → `GeomBar` + `StatBin`, `Bar` → `GeomBar` + `CategoricalScale`,
`Gauge` → `GeomArc` (polar) or `GeomRect` with annotation.

### ToadStool Integration

petalTongue discovers ToadStool display backend via capability-based discovery.
tarpc binary RPC for high-performance frame transport.
See [BIOMEOS_INTEGRATION_HANDOFF.md](./BIOMEOS_INTEGRATION_HANDOFF.md).

### barraCuda Integration

petalTongue offloads heavy visualization computation to barraCuda via capability
discovery (`math.stat.*`, `math.tessellate.*`, `math.project.*`, `math.physics.*`).
All payloads use `bytes::Bytes` for zero-copy tarpc transfer. barraCuda does not
need to know about petalTongue's grammar -- it receives computation requests and
returns results.

---

## IPC Protocol

petalTongue follows `UNIVERSAL_IPC_STANDARD_V3.md`:
- **Primary**: JSON-RPC 2.0 over Unix sockets
- **Secondary**: tarpc (binary, zero-copy `bytes::Bytes`)
- **Fallback**: HTTP REST (browser/external only)

Socket path: `$XDG_RUNTIME_DIR/petaltongue/petaltongue.sock`
Legacy: `/tmp/petaltongue.sock`

### Visualization JSON-RPC Methods

| Method | Direction | Purpose |
|--------|-----------|---------|
| `visualization.render` | Inbound | Render a grammar expression |
| `visualization.render.stream` | Inbound | Streaming visualization |
| `visualization.export` | Inbound | Export to SVG/PNG/JSON |
| `visualization.validate` | Inbound | Tufte-check a grammar expression |
| `visualization.capabilities` | Inbound | Query supported features |
| `visualization.interact` | Outbound | User interaction events |

---

## Documents

| Document | Purpose |
|----------|---------|
| [VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md) | **How to get petalTongue to visualize your data** |
| [BIOMEOS_INTEGRATION_HANDOFF.md](./BIOMEOS_INTEGRATION_HANDOFF.md) | biomeOS integration guide |
| [BIOMEOS_API_SPECIFICATION.md](./BIOMEOS_API_SPECIFICATION.md) | API contract and endpoints |
| [QUICK_START_FOR_BIOMEOS.md](./QUICK_START_FOR_BIOMEOS.md) | 5-minute quick start |
| [NEURAL_API_INTEGRATION_RESPONSE.md](./NEURAL_API_INTEGRATION_RESPONSE.md) | Neural API response format |
| [PETALTONGUE_SHOWCASE_LESSONS_LEARNED.md](./PETALTONGUE_SHOWCASE_LESSONS_LEARNED.md) | Production insights |

---

## Standards Compliance

| Standard | Status |
|----------|--------|
| `UNIBIN_ARCHITECTURE_STANDARD.md` | Compliant (1 binary, 5 modes) |
| `ECOBIN_ARCHITECTURE_STANDARD.md` | Partial (85% Pure Rust, no genomeBin yet) |
| `UNIVERSAL_IPC_STANDARD_V3.md` | Compliant (JSON-RPC + tarpc + HTTP fallback) |
| `SEMANTIC_METHOD_NAMING_STANDARD.md` | Compliant (`visualization.*` namespace) |
| `PRIMAL_IPC_PROTOCOL.md` | Compliant |
| License | AGPL-3.0-only on all crates |
