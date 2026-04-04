# ⚡ Quick Start: BiomeOS → PetalTongue Integration
**For**: BiomeOS Team  
**Time**: 5 minutes to running UI  
**Date**: January 13, 2026

---

## 🎯 GOAL

Get PetalTongue visualization UI running with your BiomeOS instance.

---

## 📋 PREREQUISITES

- [x] BiomeOS running (any version with HTTP API)
- [x] Rust toolchain installed
- [x] 5 minutes of time

---

## 🚀 STEP 1: Get PetalTongue

```bash
# Clone if you don't have it
cd /path/to/ecoPrimals/phase2/petalTongue

# Or navigate if you do
cd petalTongue
```

---

## 🔨 STEP 2: Build (30 seconds)

```bash
# Full UI
cargo build --release --bin petal-tongue

# Or headless (terminal UI)
cargo build --release --bin petal-tongue-headless
```

**Note**: Builds in ~15 seconds on modern hardware. Zero dependencies needed!

---

## 🔌 STEP 3: Configure BiomeOS Endpoint

### Option A: Your BiomeOS is on localhost:3000

```bash
export BIOMEOS_URL=http://localhost:3000
```

### Option B: Your BiomeOS is on different port

```bash
export BIOMEOS_URL=http://localhost:8080  # Or your port
```

### Option C: Unix Socket (Recommended for production)

```bash
export BIOMEOS_URL=unix:///run/user/$(id -u)/biomeos.sock
```

### Option D: No BiomeOS yet? (Tutorial Mode)

```bash
# No env var needed! PetalTongue will use built-in mock data
export PETALTONGUE_MOCK_MODE=true
```

---

## ▶️ STEP 4: Run PetalTongue

```bash
# Full GUI
./target/release/petal-tongue

# Or terminal UI (works over SSH)
./target/release/petal-tongue-headless --mode terminal

# Or export to SVG
./target/release/petal-tongue-headless --mode svg --output topology.svg
```

---

## ✅ STEP 5: Verify It Works

You should see:

**GUI Mode**:
```
[INFO] Discovering BiomeOS...
[INFO] Found BiomeOS at http://localhost:3000
[INFO] Connected to BiomeOS v1.0.0
[INFO] Fetched 5 primals, 12 edges
[INFO] Topology rendered successfully
```

**Terminal Mode**:
```
┌─────────────────────────────────────┐
│     PetalTongue Topology View      │
├─────────────────────────────────────┤
│                                     │
│   ┌─────────┐                       │
│   │BearDog  │──────┐                │
│   └─────────┘      │                │
│                    ▼                │
│              ┌──────────┐           │
│              │Songbird  │           │
│              └──────────┘           │
└─────────────────────────────────────┘
```

---

## 🐛 TROUBLESHOOTING

### Issue: "Connection refused"

**Cause**: BiomeOS not running or wrong URL

**Fix**:
```bash
# Check if BiomeOS is running
curl http://localhost:3000/api/v1/health

# If it fails, check your BiomeOS is actually running
# Then verify the port in BIOMEOS_URL
```

### Issue: PetalTongue shows mock data despite BIOMEOS_URL

**Cause**: PETALTONGUE_MOCK_MODE is set

**Fix**:
```bash
unset PETALTONGUE_MOCK_MODE
BIOMEOS_URL=http://localhost:3000 ./target/release/petal-tongue
```

### Issue: "No primals found"

**This is normal!** Your BiomeOS might not have primals registered yet.

**Fix**: Register some primals in BiomeOS, or:
```bash
# Use tutorial mode to see what it should look like
PETALTONGUE_MOCK_MODE=true ./target/release/petal-tongue
```

### Issue: "Endpoint not found" errors

**Cause**: BiomeOS doesn't have the API endpoints yet

**Fix**: Implement the minimal endpoints (see below)

---

## 📡 MINIMAL BIOMEOS API (For Testing)

If your BiomeOS doesn't have the full API yet, implement these 2 endpoints:

### 1. Health Check (10 lines)

```python
# In your BiomeOS
@app.route('/api/v1/health')
def health():
    return {"status": "healthy", "version": "1.0.0"}
```

### 2. Primals List (20 lines)

```python
@app.route('/api/v1/primals')
def primals():
    return {
        "primals": [
            {
                "id": "beardog-1",
                "name": "BearDog",
                "primal_type": "security",
                "endpoint": "http://localhost:8080",
                "capabilities": ["crypto"],
                "health": "healthy",
                "last_seen": 1705152000
            }
        ]
    }
```

### 3. Topology (Optional, can return empty)

```python
@app.route('/api/v1/topology')
def topology():
    return {
        "nodes": [],
        "edges": [],
        "mode": "live"
    }
```

**That's it!** PetalTongue will render your primal.

---

## 🎨 FULL EXAMPLE: Flask Mock Server

Copy-paste this to test:

```python
# save as mock_biomeos.py
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/api/v1/health')
def health():
    return jsonify({"status": "healthy", "version": "1.0.0", "uptime": int(time.time())})

@app.route('/api/v1/primals')
def primals():
    return jsonify({
        "primals": [
            {
                "id": "beardog-1",
                "name": "BearDog",
                "primal_type": "security",
                "endpoint": "http://localhost:8080",
                "capabilities": ["crypto", "keys"],
                "health": "healthy",
                "last_seen": int(time.time())
            },
            {
                "id": "songbird-1",
                "name": "Songbird",
                "primal_type": "discovery",
                "endpoint": "http://localhost:8081",
                "capabilities": ["discovery", "mdns"],
                "health": "healthy",
                "last_seen": int(time.time())
            }
        ]
    })

@app.route('/api/v1/topology')
def topology():
    return jsonify({
        "nodes": [
            {"id": "beardog-1", "name": "BearDog", "type": "security", "status": "healthy"},
            {"id": "songbird-1", "name": "Songbird", "type": "discovery", "status": "healthy"}
        ],
        "edges": [
            {
                "source": "beardog-1",
                "target": "songbird-1",
                "edge_type": "encryption",
                "weight": 1.0
            }
        ],
        "mode": "mock"
    })

if __name__ == '__main__':
    print("Mock BiomeOS running on http://localhost:3000")
    print("Test with: curl http://localhost:3000/api/v1/health")
    app.run(port=3000, debug=True)
```

Run it:
```bash
# Terminal 1
python mock_biomeos.py

# Terminal 2
BIOMEOS_URL=http://localhost:3000 ./target/release/petal-tongue
```

You should see BearDog ↔ Songbird in the visualization!

---

## 📚 NEXT STEPS

Once you have the basic integration working:

1. **Implement full API** - See `BIOMEOS_API_SPECIFICATION.md`
2. **Add more primals** - Register your real primals
3. **Add topology edges** - Define relationships
4. **Test with real data** - Use your actual BiomeOS instance
5. **Enable auto-refresh** - PetalTongue polls every 5s by default
6. **Customize** - Use env vars to tune performance

---

## 📖 FULL DOCUMENTATION

**Integration Guide**: `BIOMEOS_INTEGRATION_HANDOFF.md` (comprehensive)  
**API Spec**: `BIOMEOS_API_SPECIFICATION.md` (detailed endpoints)  
**Env Vars**: `../../petalTongue/ENV_VARS.md` (all configuration options)

---

## 🎊 DONE!

You now have a working PetalTongue UI connected to BiomeOS!

**Time taken**: ~5 minutes  
**Lines of code**: ~30 (in mock server)  
**Result**: Beautiful topology visualization ✨

---

## 💡 PRO TIPS

### Tip 1: Use Headless Mode Over SSH

```bash
ssh your-server "cd petalTongue && ./target/release/petal-tongue-headless --mode terminal"
```

### Tip 2: Auto-Export to SVG for Dashboards

```bash
# Cron job to update topology.svg every minute
* * * * * cd /path/to/petalTongue && ./target/release/petal-tongue-headless --mode svg --output /var/www/html/topology.svg
```

### Tip 3: Debug Mode for Development

```bash
RUST_LOG=debug BIOMEOS_URL=http://localhost:3000 ./target/release/petal-tongue
```

You'll see detailed logs of every API call.

### Tip 4: Fast Refresh for Development

```bash
# Update every 1 second instead of 5
PETALTONGUE_REFRESH_INTERVAL=1.0 ./target/release/petal-tongue
```

### Tip 5: Lower CPU Usage for Production

```bash
# Update every 30 seconds, 30 FPS
PETALTONGUE_REFRESH_INTERVAL=30.0 PETALTONGUE_MAX_FPS=30 ./target/release/petal-tongue
```

---

## ❓ QUESTIONS?

**Slack**: #petaltongue-dev  
**Docs**: `wateringHole/petaltongue/`  
**Code**: `phase2/petalTongue/`

**We're here to help!** 🌸

---

**Created**: January 13, 2026  
**For**: BiomeOS Integration Team  
**Status**: ✅ **READY TO USE**

🚀 **Get started now!**

