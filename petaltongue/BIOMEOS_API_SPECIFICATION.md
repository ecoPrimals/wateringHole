# 🔌 BiomeOS API Specification for PetalTongue
**Date**: January 13, 2026  
**Version**: 1.0  
**Purpose**: API contract between BiomeOS and PetalTongue

---

## 📋 QUICK REFERENCE

| Endpoint | Method | Purpose | Priority |
|----------|--------|---------|----------|
| `/api/v1/health` | GET | Health check | Required |
| `/api/v1/primals` | GET | List primals | Required |
| `/api/v1/topology` | GET | Graph data | Required |
| `/api/v1/events/stream` | GET (SSE) | Real-time updates | Phase 3 |

---

## 1️⃣ HEALTH ENDPOINT

### `GET /api/v1/health`

**Purpose**: Check if BiomeOS is running and responsive

**Request**: None (GET)

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600
}
```

**Fields**:
- `status` (String, **required**): "healthy", "degraded", or "unhealthy"
- `version` (String, optional): BiomeOS version
- `uptime` (u64, optional): Seconds since start

**Status Codes**:
- `200 OK`: Service healthy
- `503 Service Unavailable`: Service degraded/unhealthy
- `500 Internal Server Error`: Service error

**Example**:
```bash
curl http://localhost:3000/api/v1/health
```

---

## 2️⃣ PRIMAL DISCOVERY ENDPOINT

### `GET /api/v1/primals`

**Purpose**: List all discovered primals in the ecosystem

**Request**: None (GET)

**Response**:
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
    },
    {
      "id": "songbird-1",
      "name": "Songbird",
      "primal_type": "discovery",
      "endpoint": "http://localhost:8081",
      "capabilities": ["discovery", "mdns"],
      "health": "healthy",
      "last_seen": 1705152000
    }
  ]
}
```

**Root Fields**:
- `primals` (Array, **required**): List of primal objects

**Primal Object Fields**:
- `id` (String, **required**): Unique identifier (e.g., "beardog-1")
- `name` (String, **required**): Human-readable name (e.g., "BearDog")
- `primal_type` (String, **required**): Type category (e.g., "security", "discovery")
- `endpoint` (String, **required**): Connection URL (http:// or unix://)
- `capabilities` (Array<String>, **required**): List of capabilities
- `health` (String, **required**): "healthy", "degraded", or "unhealthy"
- `last_seen` (u64, optional): Unix timestamp of last contact

**Additional Fields** (Optional):
```json
{
  "endpoints": {
    "http": "http://localhost:8080",
    "unix": "unix:///run/user/1000/beardog.sock",
    "tarpc": "tarpc://localhost:9001"
  },
  "metadata": {
    "version": "1.0.0",
    "platform": "linux-x86_64"
  },
  "trust_level": 3,
  "family_id": "nat0"
}
```

**Status Codes**:
- `200 OK`: Success
- `500 Internal Server Error`: Discovery failed

**Example**:
```bash
curl http://localhost:3000/api/v1/primals
```

---

## 3️⃣ TOPOLOGY ENDPOINT

### `GET /api/v1/topology`

**Purpose**: Graph structure showing primal relationships

**Request**: None (GET)

**Response**:
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
    },
    {
      "id": "songbird-1",
      "name": "Songbird",
      "type": "discovery",
      "status": "healthy",
      "trust_level": 3,
      "family_id": "nat0",
      "capabilities": ["discovery", "mdns"]
    }
  ],
  "edges": [
    {
      "source": "beardog-1",
      "target": "songbird-1",
      "edge_type": "encryption",
      "weight": 1.0,
      "bidirectional": true
    }
  ],
  "mode": "live"
}
```

**Root Fields**:
- `nodes` (Array, **required**): Graph nodes (enriched primal data)
- `edges` (Array, **required**): Graph edges (connections)
- `mode` (String, optional): "live", "mock", "cached"

**Node Object Fields**:
- `id` (String, **required**): Unique node ID (matches primal ID)
- `name` (String, **required**): Display name
- `type` (String, **required**): Node type
- `status` (String, **required**): "healthy", "degraded", "unhealthy"
- `trust_level` (u8, optional): Trust rating 0-3 (0=untrusted, 3=fully trusted)
- `family_id` (String, optional): Genetic lineage/family identifier
- `capabilities` (Array<String>, optional): Capability list

**Edge Object Fields**:
- `source` (String, **required**): Source node ID
- `target` (String, **required**): Target node ID
- `edge_type` (String, **required**): Relationship type (e.g., "encryption", "discovery", "data")
- `weight` (f32, optional): Connection strength 0.0-1.0 (default: 1.0)
- `bidirectional` (bool, optional): Is connection bidirectional? (default: false)

**Edge Types** (Examples):
- `"encryption"`: Uses for crypto operations
- `"discovery"`: Discovered via
- `"data"`: Data exchange
- `"health"`: Health monitoring
- `"control"`: Management/orchestration

**Status Codes**:
- `200 OK`: Success
- `500 Internal Server Error`: Topology generation failed

**Example**:
```bash
curl http://localhost:3000/api/v1/topology | jq .
```

---

## 4️⃣ EVENTS STREAM ENDPOINT (Phase 3)

### `GET /api/v1/events/stream`

**Purpose**: Real-time event stream (Server-Sent Events)

**Protocol**: SSE (text/event-stream)

**Request**: 
```http
GET /api/v1/events/stream HTTP/1.1
Accept: text/event-stream
```

**Response** (streaming):
```
event: PrimalDiscovered
data: {"id": "songbird-2", "name": "Songbird Node 2", "endpoint": "http://..."}

event: HealthChanged
data: {"primal_id": "beardog-1", "old_status": "healthy", "new_status": "degraded"}

event: TopologyChanged
data: {"added_edges": 2, "removed_edges": 0, "timestamp": 1705152000}

event: TrustUpdated
data: {"primal_id": "songbird-1", "old_trust": 2, "new_trust": 3}
```

**Event Types**:
1. **PrimalDiscovered**: New primal detected
   ```json
   {
     "id": "string",
     "name": "string",
     "endpoint": "string"
   }
   ```

2. **PrimalLost**: Primal became unreachable
   ```json
   {
     "id": "string",
     "name": "string",
     "last_seen": 1705152000
   }
   ```

3. **HealthChanged**: Primal health status changed
   ```json
   {
     "primal_id": "string",
     "old_status": "healthy",
     "new_status": "degraded"
   }
   ```

4. **TopologyChanged**: Graph structure changed
   ```json
   {
     "added_edges": 2,
     "removed_edges": 1,
     "timestamp": 1705152000
   }
   ```

5. **TrustUpdated**: Trust level changed
   ```json
   {
     "primal_id": "string",
     "old_trust": 2,
     "new_trust": 3
   }
   ```

6. **FamilyJoined**: New genetic family detected
   ```json
   {
     "family_id": "string",
     "member_count": 5
   }
   ```

**Status Codes**:
- `200 OK`: Stream established
- `503 Service Unavailable`: Events not available

**Connection Management**:
- Client should reconnect on disconnect
- Server may send keep-alive comments (`: ping`)
- Idle timeout: 60 seconds

**Example**:
```bash
curl -N http://localhost:3000/api/v1/events/stream
```

**Note**: This endpoint is **Phase 3**. PetalTongue will use polling (GET /api/v1/topology every 5s) until SSE is implemented.

---

## 🔒 AUTHENTICATION & SECURITY

### Current (Phase 1-2)

**No authentication required** - assumes local trust:
- BiomeOS and PetalTongue run as same user
- Unix sockets provide access control
- HTTP should be localhost-only

**Recommended**:
```bash
# Unix socket (preferred)
unix:///run/user/<uid>/biomeos.sock (0600 permissions)

# HTTP localhost only
http://localhost:3000 (NOT 0.0.0.0!)
```

### Future (Phase 3)

**Token-based authentication** for remote access:

**Header**:
```http
Authorization: Bearer <token>
```

**Token Generation**:
```bash
# BiomeOS generates token
biomeos token create --name petaltongue --expires 30d

# Token passed to PetalTongue
BIOMEOS_TOKEN=<token> petal-tongue
```

---

## 🧪 TESTING GUIDE

### 1. Mock Server (Quick Test)

Create a simple mock server:

```python
# mock_biomeos.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/health')
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/api/v1/primals')
def primals():
    return jsonify({
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
    })

@app.route('/api/v1/topology')
def topology():
    return jsonify({
        "nodes": [{"id": "beardog-1", "name": "BearDog", "type": "security", "status": "healthy"}],
        "edges": [],
        "mode": "mock"
    })

if __name__ == '__main__':
    app.run(port=3000)
```

Run:
```bash
python mock_biomeos.py

# In another terminal
BIOMEOS_URL=http://localhost:3000 petal-tongue
```

### 2. Validate JSON Schema

```bash
# Test health endpoint
curl http://localhost:3000/api/v1/health | jq .

# Test primals endpoint
curl http://localhost:3000/api/v1/primals | jq '.primals | length'

# Test topology endpoint
curl http://localhost:3000/api/v1/topology | jq '{nodes: .nodes | length, edges: .edges | length}'
```

### 3. Load Testing

```bash
# Apache Bench
ab -n 1000 -c 10 http://localhost:3000/api/v1/topology

# Expected: < 50ms per request
```

---

## 📊 ERROR HANDLING

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Use response |
| 404 | Endpoint not found | Check URL |
| 500 | Server error | Retry with backoff |
| 503 | Service unavailable | Fallback to mock mode |

### Error Response Format

**Standard**:
```json
{
  "error": "Description of error",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  }
}
```

**Example**:
```json
{
  "error": "Discovery service unreachable",
  "code": "DISCOVERY_FAILED",
  "details": {
    "service": "songbird",
    "last_attempt": 1705152000
  }
}
```

### PetalTongue Error Handling

PetalTongue handles errors gracefully:

1. **Connection Error**: Retry with exponential backoff (100ms, 200ms, 400ms)
2. **Parse Error**: Log warning, continue with last known state
3. **Timeout**: Fall back to cached data
4. **All Fail**: Switch to mock mode (with user notification)

---

## 🚀 IMPLEMENTATION CHECKLIST

**BiomeOS Team**:
- [ ] Implement `/api/v1/health` endpoint
- [ ] Implement `/api/v1/primals` endpoint
- [ ] Implement `/api/v1/topology` endpoint
- [ ] Test with `curl` commands
- [ ] Validate JSON responses with `jq`
- [ ] Handle CORS if using HTTP (or use Unix sockets)
- [ ] Add error handling
- [ ] Document any deviations from spec
- [ ] Load test endpoints
- [ ] (Phase 3) Implement `/api/v1/events/stream` SSE

**Testing Together**:
- [ ] Start BiomeOS
- [ ] Start PetalTongue with `BIOMEOS_URL`
- [ ] Verify connection in logs
- [ ] Confirm topology renders
- [ ] Test error cases (kill BiomeOS mid-session)
- [ ] Verify auto-refresh works (5s interval)
- [ ] Test with 10+ primals
- [ ] Test with 100+ primals (performance)

---

## 📞 QUESTIONS & CLARIFICATIONS

**Q**: What if our topology is huge (1000+ nodes)?

**A**: PetalTongue can handle it, but consider:
- Pagination: Return top 100 most important nodes
- Filtering: Add query params `?type=security&status=healthy`
- Caching: Use HTTP caching headers

**Q**: Can we use different field names?

**A**: Yes, but document the mapping. PetalTongue can adapt if needed.

**Q**: Do we need to implement all endpoints at once?

**A**: No! Minimum viable integration:
1. `/api/v1/health` - Returns 200 OK
2. `/api/v1/primals` - Returns at least 1 primal
3. `/api/v1/topology` - Returns empty edges is fine

Start simple, iterate!

**Q**: What about authentication?

**A**: Phase 1-2: None (local trust). Phase 3: Token-based.

**Q**: SSE vs WebSocket?

**A**: We chose SSE for simplicity. One-way communication is sufficient. If you prefer WebSocket, we can adapt.

---

## 🔗 REFERENCES

**PetalTongue Docs**:
- Integration Guide: `wateringHole/petaltongue/BIOMEOS_INTEGRATION_HANDOFF.md`
- Client Implementation: `petalTongue/crates/petal-tongue-api/src/biomeos_client.rs`
- Environment Variables: `petalTongue/ENV_VARS.md`

**BiomeOS Docs**:
- (Add your API documentation here)

**Standards**:
- [JSON API Specification](https://jsonapi.org/)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [HTTP Status Codes](https://httpstatuses.com/)

---

**Created**: January 13, 2026  
**Version**: 1.0  
**Status**: ✅ **READY FOR IMPLEMENTATION**

🌳 **Let's build the BiomeOS ↔ PetalTongue integration!** 🌸

