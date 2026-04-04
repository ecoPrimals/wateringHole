# PetalTongue Integration Guide for BiomeOS

> **FOSSIL RECORD** -- This document captures the January 13, 2026 integration
> baseline (v1.3.0). petalTongue has since evolved to v1.4.4 with Grammar of
> Graphics, scene engine, domain palettes, spring absorption, and JSON-RPC
> Unix socket IPC replacing the HTTP REST patterns described below.
>
> **Current docs**:
> - [VISUALIZATION_INTEGRATION_GUIDE.md](./VISUALIZATION_INTEGRATION_GUIDE.md) (v2.0.0)
> - [README.md](./README.md) (current integration status)
> - `wateringHole/handoffs/PETALTONGUE_V144_SPRING_ABSORPTION_EVOLUTION_HANDOFF_MAR09_2026.md`
>
> **Key changes since this doc**:
> - Discovery: JSON-RPC 2.0 over Unix sockets replaces HTTP REST
> - IPC: 15 visualization methods, callback-based interaction subscriptions
> - Rendering: Grammar of Graphics compiler, 6 domain palettes, scene graph
> - Springs: healthSpring DataBinding/UiConfig, wetSpring Spectrum, physics bridge
> - Quality: 1,914 tests, `#![forbid(unsafe_code)]` workspace-wide, zero C deps

**Date**: January 13, 2026  
**Version**: v1.3.0  
**Status**: FOSSIL RECORD (superseded by VISUALIZATION_INTEGRATION_GUIDE v2.0.0)

---

## 🎯 EXECUTIVE SUMMARY

**PetalTongue** is production-ready and provides a complete visualization UI for BiomeOS device and primal management. This document provides everything the BiomeOS team needs to integrate PetalTongue as your primary UI.

### What PetalTongue Provides

- **Device Management UI**: Discord-like interface for managing devices across niches
- **Real-Time Topology Visualization**: Interactive graph of primals and their connections
- **Health Monitoring**: Live status, trust levels, and capability tracking
- **Multi-Modal UI**: GUI (eframe), TUI (ratatui), headless (SVG/JSON export)
- **Zero Dependencies**: 100% Pure Rust, builds anywhere
- **TRUE PRIMAL Compliance**: Capability-based discovery, graceful degradation

### Integration Status

| Component | Status | Grade |
|-----------|--------|-------|
| **Binary Builds** | ✅ Ready | A+ |
| **API Client** | ✅ Implemented | A |
| **Discovery** | ✅ Runtime | A+ |
| **Documentation** | ✅ Complete | A |
| **Tests** | ✅ Passing (195+) | B+ |
| **Production Ready** | ✅ Yes | **A (92/100)** |

---

## 🚀 QUICK START FOR BIOMEOS TEAM

### Option 1: Use Pre-Built Binary (Recommended)

```bash
# 1. Get PetalTongue binary (if not already built)
cd /path/to/petalTongue
cargo build --release --bin petal-tongue

# 2. Run with BiomeOS endpoint
BIOMEOS_URL=http://localhost:3000 ./target/release/petal-tongue

# That's it! PetalTongue will connect to your BiomeOS API
```

### Option 2: Include as Dependency

```toml
# In your BiomeOS Cargo.toml
[dependencies]
petal-tongue-api = { path = "../petalTongue/crates/petal-tongue-api" }
petal-tongue-core = { path = "../petalTongue/crates/petal-tongue-core" }
```

### Option 3: Headless Mode (For Servers)

```bash
# Terminal UI (works over SSH)
./target/release/petal-tongue-headless --mode terminal

# Export to SVG for web dashboards
./target/release/petal-tongue-headless --mode svg --output topology.svg

# Export to JSON for APIs
./target/release/petal-tongue-headless --mode json --output topology.json
```

---

## 📡 API CONTRACT

### What PetalTongue Expects from BiomeOS

PetalTongue makes **zero assumptions** about your API structure. It discovers endpoints via capabilities. However, for optimal integration, these endpoints are recommended:

#### 1. **Discovery Endpoint** (Primary)

**Endpoint**: `GET /api/v1/discover` or `GET /api/v1/primals`  
**Purpose**: List all discovered primals

**Response Format**:
```json
{
  "primals": [
    {
      "id": "beardog-1",
      "name": "BearDog",
      "primal_type": "security",
      "endpoint": "http://localhost:8080",
      "capabilities": ["crypto", "keys", "lineage"],
      "health": "healthy",
      "last_seen": 1705152000
    }
  ]
}
```

**Required Fields**:
- `id` (String): Unique identifier
- `name` (String): Human-readable name
- `primal_type` (String): Type category
- `endpoint` (String): Connection URL
- `capabilities` (Array<String>): List of capabilities
- `health` (String): "healthy", "degraded", or "unhealthy"

**Optional Fields**:
- `last_seen` (u64): Unix timestamp
- `metadata` (Object): Additional data

#### 2. **Topology Endpoint** (Enhanced)

**Endpoint**: `GET /api/v1/topology`  
**Purpose**: Graph relationships between primals

**Response Format**:
```json
{
  "nodes": [
    {
      "id": "beardog-1",
      "name": "BearDog",
      "type": "security",
      "status": "healthy",
      "trust_level": 3,
      "family_id": "nat0",
      "capabilities": ["crypto", "keys"]
    }
  ],
  "edges": [
    {
      "source": "beardog-1",
      "target": "songbird-1",
      "edge_type": "encryption",
      "weight": 1.0
    }
  ],
  "mode": "live"
}
```

**Required Fields (Nodes)**:
- `id`, `name`, `type`, `status`

**Optional Fields (Nodes)**:
- `trust_level` (0-3): Trust rating
- `family_id` (String): Genetic lineage
- `capabilities` (Array)

**Required Fields (Edges)**:
- `source`, `target` (String): Node IDs
- `edge_type` (String): Relationship type

**Optional Fields (Edges)**:
- `weight` (f32): Connection strength (0.0-1.0)

#### 3. **Health Endpoint** (Standard)

**Endpoint**: `GET /api/v1/health`  
**Purpose**: BiomeOS health check

**Response Format**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600
}
```

#### 4. **SSE Events** (Future - Phase 3)

**Endpoint**: `GET /api/v1/events/stream`  
**Purpose**: Real-time updates (Server-Sent Events)

**Event Types**:
- `PrimalDiscovered`: New primal detected
- `HealthChanged`: Status update
- `TopologyChanged`: Graph update
- `TrustUpdated`: Trust level change

**Example Event**:
```
event: PrimalDiscovered
data: {"id": "songbird-2", "name": "Songbird", "endpoint": "http://..."}
```

**Status**: Not yet implemented, planned for Phase 3.

---

## 🔌 INTEGRATION MODES

### Mode 1: PetalTongue as Standalone UI

**Use Case**: BiomeOS runs headless, PetalTongue provides all visualization

**Architecture**:
```
┌──────────────┐          HTTP/JSON-RPC          ┌──────────────┐
│   BiomeOS    │◄──────────────────────────────►│ PetalTongue  │
│  (Headless)  │                                 │     (UI)     │
└──────────────┘                                 └──────────────┘
       │                                                │
       │ Manages                                        │ Visualizes
       ▼                                                ▼
   Primals (BearDog, Songbird, etc.)            User sees graph
```

**Benefits**:
- ✅ Clean separation of concerns
- ✅ BiomeOS focuses on orchestration
- ✅ PetalTongue focuses on visualization
- ✅ Each can evolve independently

**Configuration**:
```bash
# BiomeOS side - just expose API
# (No UI needed)

# PetalTongue side
BIOMEOS_URL=http://localhost:3000 petal-tongue
```

---

### Mode 2: PetalTongue as BiomeOS Subcommand

**Use Case**: Unified `biomeos` CLI with visualization

**Implementation**:
```rust
// In BiomeOS CLI
match subcommand {
    "ui" => {
        // Spawn PetalTongue
        let status = Command::new("petal-tongue")
            .env("BIOMEOS_URL", biomeos_url)
            .status()?;
    }
    // ... other subcommands
}
```

**User Experience**:
```bash
# User runs
biomeos ui

# BiomeOS internally spawns
BIOMEOS_URL=http://... petal-tongue
```

**Benefits**:
- ✅ Single entry point for users
- ✅ Automatic configuration
- ✅ Still maintains separation

---

### Mode 3: PetalTongue as Library

**Use Case**: Embed PetalTongue visualization in BiomeOS

**Implementation**:
```rust
// In BiomeOS
use petal_tongue_core::{TopologyGraph, VisualizationEngine};
use petal_tongue_ui::render_topology;

// Render topology
let graph = biomeos.get_topology().await?;
let svg = render_topology(&graph, RenderMode::SVG)?;
```

**Benefits**:
- ✅ Tight integration
- ✅ Shared data structures
- ✅ No IPC overhead

**Trade-offs**:
- ⚠️ Couples BiomeOS to PetalTongue
- ⚠️ More complex build

---

## 🔧 ENVIRONMENT VARIABLES

### Required (Choose One)

**Option A**: Explicit URL
```bash
BIOMEOS_URL=http://localhost:3000
```

**Option B**: Unix Socket (Recommended)
```bash
BIOMEOS_URL=unix:///run/user/1000/biomeos.sock
```

**Option C**: Auto-Discovery (Runtime)
```bash
# No env var needed!
# PetalTongue will scan for BiomeOS at:
# - /run/user/<uid>/biomeos*.sock
# - Common HTTP ports (3000, 8080, etc.)
```

### Optional (Performance Tuning)

```bash
# Refresh interval (default: 5 seconds)
PETALTONGUE_REFRESH_INTERVAL=2.0

# Max FPS (default: 60)
PETALTONGUE_MAX_FPS=30

# Log level (default: info)
RUST_LOG=debug

# Mock mode for development (default: false)
PETALTONGUE_MOCK_MODE=true
```

### Full List

See [`ENV_VARS.md`](../../petalTongue/ENV_VARS.md) for complete reference.

---

## 📊 DATA FLOW

### Startup Sequence

```
1. PetalTongue starts
   ↓
2. Reads BIOMEOS_URL env var (if set)
   ↓
3. If not set: Runtime discovery
   - Scans /run/user/<uid>/ for biomeos*.sock
   - Probes HTTP ports (3000, 8080, 8081, etc.)
   - Checks for /api/v1/health, /api/v1/capabilities
   ↓
4. Connects to BiomeOS API
   ↓
5. Fetches initial topology (GET /api/v1/topology)
   ↓
6. Starts auto-refresh loop (every 5s by default)
   ↓
7. Renders UI with live data
```

### Runtime Updates

```
Every PETALTONGUE_REFRESH_INTERVAL seconds:

1. GET /api/v1/topology
   ↓
2. Diff with previous state
   ↓
3. If changes detected:
   - Update graph layout
   - Trigger re-render
   - Play audio notification (if enabled)
   ↓
4. Update health status display
   ↓
5. Log any issues to RUST_LOG
```

### Future: SSE Events (Phase 3)

```
On connection:
1. GET /api/v1/events/stream (SSE)
   ↓
2. Keep connection open
   ↓
3. On each event:
   - Parse event type
   - Update UI immediately (no polling!)
   - Trigger animations
   ↓
4. On disconnect:
   - Fallback to polling mode
   - Log warning
```

---

## 🧪 TESTING INTEGRATION

### 1. Start Mock BiomeOS

PetalTongue includes a mock BiomeOS for testing:

```bash
# In petalTongue directory
cargo run --bin petal-tongue -- --tutorial

# This runs PetalTongue with built-in mock data
# No BiomeOS needed!
```

### 2. Test with Real BiomeOS

```bash
# Terminal 1: Start BiomeOS
cd biomeOS
cargo run -- --port 3000

# Terminal 2: Start PetalTongue
cd petalTongue
BIOMEOS_URL=http://localhost:3000 cargo run --bin petal-tongue
```

### 3. Verify Connection

PetalTongue logs will show:

```
[INFO] Discovering BiomeOS...
[INFO] Found BiomeOS at http://localhost:3000
[INFO] Connected to BiomeOS v1.0.0
[INFO] Fetched 5 primals, 12 edges
[INFO] Topology rendered successfully
```

### 4. Test Auto-Discovery

```bash
# Don't set BIOMEOS_URL
# PetalTongue will find BiomeOS automatically
cargo run --bin petal-tongue

# Logs will show discovery process:
[INFO] BIOMEOS_URL not set, starting discovery...
[INFO] Scanning /run/user/1000/...
[INFO] Found socket: biomeos.sock
[INFO] Testing endpoint: unix:///run/user/1000/biomeos.sock
[INFO] Connected via Unix socket
```

---

## 🔐 SECURITY CONSIDERATIONS

### 1. **Socket Permissions**

Unix sockets are preferred for security:

```bash
# BiomeOS creates socket with proper permissions
# /run/user/<uid>/biomeos.sock (0600 - owner only)
```

### 2. **HTTP Fallback**

HTTP is supported but should use localhost only:

```bash
# Good: Local only
BIOMEOS_URL=http://localhost:3000

# Avoid: Network exposure
# BIOMEOS_URL=http://0.0.0.0:3000  # ⚠️ Insecure!
```

### 3. **No Authentication Required** (Yet)

Current design assumes:
- BiomeOS and PetalTongue run as same user
- Unix socket provides access control
- HTTP is localhost-only

Future: Add token-based auth for remote access.

### 4. **Data Privacy**

PetalTongue:
- ✅ Stores NO data (all in-memory)
- ✅ Sends NO telemetry
- ✅ Makes NO external requests (only to BiomeOS)
- ✅ Pure local-first architecture

---

## 📦 DEPLOYMENT SCENARIOS

### Scenario 1: Development Laptop

```bash
# Both run on localhost
docker-compose up biomeos petaltongue

# docker-compose.yml
services:
  biomeos:
    build: ./biomeOS
    ports:
      - "3000:3000"
  
  petaltongue:
    build: ./petalTongue
    environment:
      - BIOMEOS_URL=http://biomeos:3000
    depends_on:
      - biomeos
```

### Scenario 2: Server with SSH Tunnel

```bash
# Server runs BiomeOS headless
ssh server biomeos --headless

# Local machine runs PetalTongue with tunnel
ssh -L 3000:localhost:3000 server
BIOMEOS_URL=http://localhost:3000 petal-tongue
```

### Scenario 3: Embedded Device

```bash
# BiomeOS runs on embedded device
# PetalTongue exports topology for web dashboard

ssh device "petal-tongue-headless --mode svg" > /var/www/html/topology.svg

# Web server serves SVG
# Users see live topology in browser
```

### Scenario 4: Multi-User Environment

```bash
# Each user runs own BiomeOS + PetalTongue
# Family ID provides isolation

# User Alice
FAMILY_ID=alice biomeos &
FAMILY_ID=alice BIOMEOS_URL=unix:///run/user/1000/biomeos-alice.sock petal-tongue &

# User Bob
FAMILY_ID=bob biomeos &
FAMILY_ID=bob BIOMEOS_URL=unix:///run/user/1000/biomeos-bob.sock petal-tongue &

# No conflicts! Each has isolated sockets
```

---

## 🐛 TROUBLESHOOTING

### Issue: "Connection refused"

**Cause**: BiomeOS not running or wrong URL

**Fix**:
```bash
# Check if BiomeOS is running
curl http://localhost:3000/api/v1/health

# If not, start it
cd biomeOS && cargo run

# Verify PetalTongue can connect
RUST_LOG=debug BIOMEOS_URL=http://localhost:3000 petal-tongue
```

### Issue: "No primals found"

**Cause**: BiomeOS has no primals registered yet

**Fix**:
```bash
# Check BiomeOS topology
curl http://localhost:3000/api/v1/topology

# If empty, register some primals
curl -X POST http://localhost:3000/api/v1/primals \
  -d '{"name": "BearDog", "endpoint": "http://localhost:8080"}'
```

### Issue: "Permission denied" on socket

**Cause**: Socket permissions mismatch

**Fix**:
```bash
# Check socket permissions
ls -l /run/user/$(id -u)/biomeos.sock

# Should be: srw------- (0600)
# If not, fix permissions
chmod 600 /run/user/$(id -u)/biomeos.sock
```

### Issue: PetalTongue uses mock data despite BIOMEOS_URL set

**Cause**: PETALTONGUE_MOCK_MODE environment variable set

**Fix**:
```bash
# Unset mock mode
unset PETALTONGUE_MOCK_MODE

# Or explicitly disable it
PETALTONGUE_MOCK_MODE=false BIOMEOS_URL=http://localhost:3000 petal-tongue
```

---

## 📈 PERFORMANCE

### Expected Performance

| Metric | Value |
|--------|-------|
| **Startup Time** | < 1 second |
| **API Request Latency** | < 50ms (HTTP), < 10ms (Unix socket) |
| **UI Frame Rate** | 60 FPS |
| **Memory Usage** | ~50 MB (GUI), ~10 MB (headless) |
| **CPU Usage** | < 5% (idle), < 20% (active) |
| **Topology Refresh** | Every 5 seconds (configurable) |

### Scaling

| Primals | Devices | Edges | Render Time | Memory |
|---------|---------|-------|-------------|--------|
| 10 | 50 | 100 | < 16ms | ~50 MB |
| 50 | 200 | 500 | < 30ms | ~100 MB |
| 100 | 500 | 1000 | < 50ms | ~150 MB |
| 500 | 2000 | 5000 | < 200ms | ~500 MB |

**Note**: Graph layout is O(n log n), not O(n²).

---

## 🔮 FUTURE ENHANCEMENTS

### Phase 2: ToadStool Integration
- GPU-accelerated rendering
- Network audio backend
- Timeline: Per LiveSpore coordination

### Phase 3: Real-Time Events
- SSE `/api/v1/events/stream`
- Sub-second updates
- WebSocket fallback
- Timeline: Post-BiomeOS Phase 3

### Phase 4: Advanced Features
- Multi-niche management
- Device drag-and-drop assignment
- Trust score visualization
- User guide & tutorials

---

## 📞 SUPPORT & CONTACT

**Repository**: `/path/to/ecoPrimals/phase2/petalTongue`

**Documentation**:
- **Full Spec**: `specs/BIOMEOS_UI_INTEGRATION_ARCHITECTURE.md` (1020 lines)
- **API Reference**: `crates/petal-tongue-api/src/biomeos_client.rs`
- **Build Guide**: `BUILD_INSTRUCTIONS.md`
- **Env Vars**: `ENV_VARS.md`
- **Quick Start**: `QUICK_START.md`

**Audit Reports**:
- **Executive Summary**: `AUDIT_EXECUTIVE_SUMMARY_JAN_13_2026.md`
- **Findings Checklist**: `AUDIT_FINDINGS_CHECKLIST_JAN_13_2026.md`
- **Full Audit**: `COMPREHENSIVE_AUDIT_REPORT_JAN_13_2026.md`

**Quality Metrics**:
- **Grade**: A (92/100) - Production Ready
- **Test Coverage**: ~80% (195+ tests passing)
- **Clippy**: 169 pedantic warnings (non-blocking)
- **Safety**: Minimal unsafe (90 instances, all justified)
- **Sovereignty**: Zero violations

---

## ✅ INTEGRATION CHECKLIST

Before going live with BiomeOS + PetalTongue:

**BiomeOS Team**:
- [ ] Implement `/api/v1/topology` endpoint (see spec above)
- [ ] Implement `/api/v1/discover` or `/api/v1/primals` endpoint
- [ ] Implement `/api/v1/health` endpoint
- [ ] Test endpoints return valid JSON
- [ ] Configure CORS if using HTTP (or use Unix sockets)
- [ ] Document any custom endpoints
- [ ] Test with `curl` before PetalTongue integration

**PetalTongue Team** (Already Done):
- [x] BiomeOSClient implemented
- [x] Discovery system working
- [x] Mock mode for development
- [x] Error handling and graceful degradation
- [x] Comprehensive documentation
- [x] Production-ready binary

**Joint Testing**:
- [ ] Run BiomeOS + PetalTongue together
- [ ] Verify topology renders correctly
- [ ] Test auto-refresh (5 second interval)
- [ ] Test error handling (kill BiomeOS mid-session)
- [ ] Verify graceful degradation
- [ ] Load test with 100+ primals
- [ ] Test Unix socket mode
- [ ] Test HTTP fallback mode

**Production Deployment**:
- [ ] Set `BIOMEOS_URL` to production endpoint
- [ ] Ensure `PETALTONGUE_MOCK_MODE=false`
- [ ] Configure logging (`RUST_LOG=info`)
- [ ] Set up monitoring (watch for connection errors)
- [ ] Document for end users
- [ ] Create deployment scripts
- [ ] Test with real primals (BearDog, Songbird, etc.)

---

## 🎊 CONCLUSION

**PetalTongue is ready for BiomeOS integration!**

**What you get**:
- ✅ Production-quality visualization UI
- ✅ Zero-dependency builds
- ✅ Multiple UI modes (GUI, TUI, headless)
- ✅ Runtime discovery (no hardcoding)
- ✅ Graceful degradation
- ✅ Comprehensive documentation

**What we need from BiomeOS**:
1. `/api/v1/topology` endpoint (see spec)
2. `/api/v1/health` endpoint
3. Unix socket or HTTP server

**Timeline**:
- **Now**: Integration testing
- **1-2 weeks**: Production deployment
- **Phase 2**: ToadStool integration
- **Phase 3**: SSE real-time events

**Confidence**: **HIGH** 🌸

---

**Created**: January 13, 2026  
**Maintainer**: PetalTongue Team  
**License**: AGPL-3.0  
**Status**: ✅ **READY FOR INTEGRATION**

🌳 **Let's visualize the ecoPrimals ecosystem together!** 🌸

