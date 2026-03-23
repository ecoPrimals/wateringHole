# Spring Provenance Trio Integration Pattern

> Reusable pattern for integrating any ecoSpring with the provenance trio
> (rhizoCrypt + loamSpine + sweetGrass) via biomeOS capability routing.

## Status

- **Version**: 1.1
- **Derived from**: ludoSpring V15 (`barracuda/src/ipc/provenance.rs`)
- **Wire types**: Each primal owns its own types — no shared `provenance-trio-types` crate (archived per sovereignty standard, Mar 2026)
- **Validated by**: biomeOS E2E (`provenance_trio_e2e.rs`), ludoSpring exp052-066

---

## Architecture

```text
┌─────────────────┐
│   Your Spring    │
│                  │
│  begin_session() ──→ capability.call("dag", "create_session", ...)
│  record_step()   ──→ capability.call("dag", "event.append", ...)
│  complete()      ──→ 1. capability.call("dag", "dehydration.trigger", ...)
│                  │   2. capability.call("commit", "session", ...)
│                  │   3. capability.call("provenance", "create_braid", ...)
└────────┬─────────┘
         │ Unix socket (Neural API)
         ▼
┌─────────────────┐    capability routing
│    biomeOS       │──→ dag.*        → rhizoCrypt
│   Neural API     │──→ commit.*     → loamSpine
│                  │──→ provenance.* → sweetGrass
└──────────────────┘
```

Springs never import trio crates directly in production code. All trio
interaction goes through biomeOS `capability.call` over a Unix socket,
which provides:

- **Zero compile-time coupling** to trio crates
- **Graceful degradation** when trio is unavailable
- **Semantic routing** via Neural API (capability → primal mapping)

---

## Wire Types

Each primal defines its own wire types. JSON is the contract. The shared
`provenance-trio-types` crate has been **archived** — primals must not take
compile-time dependencies on other primals' types.

| Wire type | Producer | Consumer | Contract |
|-----------|----------|----------|----------|
| `DehydrationSummary` | rhizoCrypt | loamSpine, sweetGrass | JSON-RPC payload (unknown fields silently ignored) |
| `PipelineRequest` | biomeOS graph | sweetGrass | JSON-RPC `pipeline.attribute` params |
| `PipelineResult` | sweetGrass | biomeOS graph | JSON-RPC `pipeline.attribute` result |

Springs define their own local structs with `serde::Deserialize` / `serde::Serialize`
and `#[serde(default)]` for forward compatibility. No `From` impls needed — JSON
is the canonical representation.

---

## Implementation Template

### 1. Result Type

```rust
/// Result of a provenance operation; includes availability status.
#[derive(Debug)]
pub struct ProvenanceResult {
    pub id: String,
    pub available: bool,
    pub data: serde_json::Value,
}
```

### 2. Socket Discovery (XDG-compliant)

```rust
fn neural_api_socket_path() -> Option<PathBuf> {
    let family_id = std::env::var("FAMILY_ID")
        .or_else(|_| std::env::var("BIOMEOS_FAMILY_ID"))
        .unwrap_or_else(|_| "default".to_string());

    let sock_name = format!("neural-api-{family_id}.sock");

    // Priority: explicit env → BIOMEOS_SOCKET_DIR → XDG_RUNTIME_DIR → /tmp
    for candidate in [
        std::env::var("NEURAL_API_SOCKET").ok().map(PathBuf::from),
        std::env::var("BIOMEOS_SOCKET_DIR").ok().map(|d| PathBuf::from(d).join(&sock_name)),
        std::env::var("XDG_RUNTIME_DIR").ok().map(|d| PathBuf::from(d).join("biomeos").join(&sock_name)),
        Some(PathBuf::from("/tmp").join(&sock_name)),
    ].into_iter().flatten() {
        if candidate.exists() { return Some(candidate); }
    }

    None
}
```

### 3. Capability Call Helper

```rust
fn capability_call(
    socket_path: &Path,
    capability: &str,
    operation: &str,
    args: &serde_json::Value,
) -> Result<serde_json::Value, String> {
    use std::os::unix::net::UnixStream;

    let request = serde_json::json!({
        "jsonrpc": "2.0",
        "method": "capability.call",
        "params": { "capability": capability, "operation": operation, "args": args },
        "id": 1
    });

    let mut stream = UnixStream::connect(socket_path).map_err(|e| format!("connect: {e}"))?;
    stream.set_read_timeout(Some(Duration::from_secs(10))).ok();
    stream.set_write_timeout(Some(Duration::from_secs(10))).ok();

    let payload = serde_json::to_string(&request).map_err(|e| format!("serialize: {e}"))?;
    stream.write_all(payload.as_bytes()).map_err(|e| format!("write: {e}"))?;
    stream.write_all(b"\n").map_err(|e| format!("write newline: {e}"))?;
    stream.flush().map_err(|e| format!("flush: {e}"))?;
    stream.shutdown(std::net::Shutdown::Write).map_err(|e| format!("shutdown: {e}"))?;

    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).map_err(|e| format!("read: {e}"))?;

    let parsed: serde_json::Value = serde_json::from_str(line.trim())
        .map_err(|e| format!("parse: {e}"))?;

    if let Some(err) = parsed.get("error") {
        return Err(format!("rpc error: {}",
            err.get("message").and_then(|m| m.as_str()).unwrap_or("unknown")));
    }

    parsed.get("result").cloned().ok_or_else(|| "no result in response".to_string())
}
```

### 4. Session Lifecycle (adapt domain names)

Replace `game_session` / `game_action` with your domain:

```rust
/// Begin a provenance-tracked experiment session.
pub fn begin_experiment_session(experiment_name: &str) -> Result<ProvenanceResult, String> {
    let Some(socket) = neural_api_socket_path() else {
        return Ok(ProvenanceResult {
            id: format!("local-{}", uuid::Uuid::now_v7()),
            available: false,
            data: serde_json::json!({ "provenance": "unavailable" }),
        });
    };

    let args = serde_json::json!({
        "metadata": { "type": "experiment", "name": experiment_name },
        "session_type": { "Experiment": { "spring_id": "YOUR_SPRING_NAME" } },
        "description": experiment_name,
    });

    match capability_call(&socket, "dag", "create_session", &args) {
        Ok(result) => {
            let session_id = result.get("session_id")
                .and_then(|v| v.as_str()).unwrap_or("unknown").to_string();
            Ok(ProvenanceResult {
                id: session_id.clone(),
                available: true,
                data: serde_json::json!({ "session_id": session_id }),
            })
        }
        Err(_) => Ok(ProvenanceResult {
            id: format!("local-{}", uuid::Uuid::now_v7()),
            available: false,
            data: serde_json::json!({ "provenance": "unavailable" }),
        }),
    }
}

/// Record an experiment step in the DAG.
pub fn record_experiment_step(
    session_id: &str,
    step: &serde_json::Value,
) -> Result<ProvenanceResult, String> {
    let Some(socket) = neural_api_socket_path() else {
        return Ok(ProvenanceResult {
            id: "unavailable".to_string(),
            available: false,
            data: serde_json::json!({ "provenance": "unavailable" }),
        });
    };

    let args = serde_json::json!({ "session_id": session_id, "event": step });

    match capability_call(&socket, "dag", "append_event", &args) {
        Ok(result) => {
            let vertex_id = result.get("vertex_id")
                .or_else(|| result.get("id"))
                .and_then(|v| v.as_str()).unwrap_or("unknown").to_string();
            Ok(ProvenanceResult {
                id: vertex_id.clone(),
                available: true,
                data: serde_json::json!({ "vertex_id": vertex_id }),
            })
        }
        Err(_) => Ok(ProvenanceResult {
            id: "unavailable".to_string(),
            available: false,
            data: serde_json::json!({ "provenance": "unavailable" }),
        }),
    }
}

/// Complete an experiment: dehydrate → commit → attribute.
pub fn complete_experiment(session_id: &str) -> Result<serde_json::Value, String> {
    let Some(socket) = neural_api_socket_path() else {
        return Ok(serde_json::json!({
            "provenance": "unavailable", "session_id": session_id,
        }));
    };

    // Step 1: Dehydrate (rhizoCrypt)
    let dehydration = match capability_call(
        &socket, "dag", "dehydrate", &serde_json::json!({ "session_id": session_id }),
    ) {
        Ok(r) => r,
        Err(_) => return Ok(serde_json::json!({
            "provenance": "unavailable", "session_id": session_id,
        })),
    };

    let merkle_root = dehydration.get("merkle_root")
        .and_then(|v| v.as_str()).unwrap_or("").to_string();

    // Step 2: Commit (loamSpine)
    let commit_result = match capability_call(
        &socket, "commit", "session",
        &serde_json::json!({ "summary": dehydration, "content_hash": merkle_root }),
    ) {
        Ok(r) => r,
        Err(_) => return Ok(serde_json::json!({
            "provenance": "partial", "session_id": session_id,
            "dehydrated": true, "committed": false,
        })),
    };

    let commit_id = commit_result.get("commit_id")
        .or_else(|| commit_result.get("entry_id"))
        .and_then(|v| v.as_str()).unwrap_or("").to_string();

    // Step 3: Attribute (sweetGrass) — best-effort
    let braid_result = capability_call(
        &socket, "provenance", "create_braid",
        &serde_json::json!({
            "commit_ref": commit_id,
            "agents": [{ "did": "did:key:YOUR_SPRING_DID", "role": "author", "contribution": 1.0 }],
        }),
    );

    let braid_id = braid_result.ok()
        .and_then(|r| r.get("braid_id").or(r.get("id")).and_then(|v| v.as_str()).map(str::to_string))
        .unwrap_or_default();

    Ok(serde_json::json!({
        "provenance": "complete",
        "session_id": session_id,
        "merkle_root": merkle_root,
        "commit_id": commit_id,
        "braid_id": braid_id,
    }))
}
```

---

## Graceful Degradation Contract

| Condition | Behavior | Status |
|-----------|----------|--------|
| Socket missing | Return `Ok` + `"unavailable"` | Experiment succeeds |
| Dehydrate fails | Return `Ok` + `"unavailable"` | Experiment succeeds |
| Commit fails | Return `Ok` + `"partial"` | Dehydration preserved |
| Braid fails | Return `Ok` + `"complete"` with empty `braid_id` | Commit preserved |

**Rule**: Domain logic must never fail because provenance is unavailable.
Springs return `Ok` with a status field indicating provenance availability.

---

## Handler Integration

```rust
fn handle_begin_experiment(req: &JsonRpcRequest) -> HandlerResult {
    let p: BeginExperimentParams = parse_params(req)?;
    let result = provenance::begin_experiment_session(&p.experiment_name)
        .map_err(|e| JsonRpcError::internal(req.id.clone(), &e))?;
    to_json(&req.id, serde_json::json!({
        "session_id": result.id,
        "provenance": if result.available { "available" } else { "unavailable" },
        "data": result.data,
    }))
}
```

---

## ProvenancePipeline Pattern (Optional)

For springs that want tighter biomeOS integration (e.g., continuous sessions,
auto-dehydration), define your own pipeline trait locally:

```rust
/// Define locally — no shared crate import.
#[derive(serde::Serialize)]
struct PipelineRequest {
    session_id: String,
    agent_did: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    niche: Option<String>,
    #[serde(default)]
    agent_summaries: Vec<serde_json::Value>,
}

/// Result from pipeline.attribute.
#[derive(serde::Deserialize)]
struct PipelineResult {
    #[serde(default)]
    braid_ref: Option<String>,
    #[serde(default)]
    commit_ref: String,
    #[serde(default)]
    dehydration_merkle_root: String,
}

struct MySpring { session_id: Option<String> }

impl MySpring {
    fn producer_name(&self) -> &str { "my-spring" }
    fn active_session(&self) -> Option<&str> { self.session_id.as_deref() }

    fn dehydrate_params(&self) -> Option<PipelineRequest> {
        self.session_id.as_ref().map(|sid| PipelineRequest {
            session_id: sid.clone(),
            agent_did: "did:key:my-spring".to_string(),
            niche: Some("my-niche".to_string()),
            agent_summaries: Vec::new(),
        })
    }

    fn on_pipeline_complete(&mut self, _result: &PipelineResult) {
        self.session_id = None;
    }
}
```

---

## Capability Routing Reference

| Capability | Operation | Primal | JSON-RPC Method |
|------------|-----------|--------|-----------------|
| `dag` | `create_session` | rhizoCrypt | `dag.session.create` |
| `dag` | `append_event` | rhizoCrypt | `dag.event.append` |
| `dag` | `dehydrate` | rhizoCrypt | `dag.dehydration.trigger` |
| `commit` | `session` | loamSpine | `commit.session` |
| `provenance` | `create_braid` | sweetGrass | `braid.create` |
| `provenance` | `record_dehydration` | sweetGrass | `contribution.record_dehydration` |

---

## Checklist for Spring Adoption

- [ ] Create `ipc/provenance.rs` module following this template
- [ ] Adapt domain names (`experiment`/`step` vs `game_session`/`action`)
- [ ] Wire `begin`/`record`/`complete` into your JSON-RPC handler dispatch
- [ ] Return provenance availability status in handler responses
- [ ] Ensure domain logic never fails when provenance is unavailable
- [ ] Define local wire types with `#[serde(default)]` for forward compatibility
- [ ] Test with `NEURAL_API_SOCKET` unset (degradation path)
- [ ] Test with biomeOS running (happy path)
