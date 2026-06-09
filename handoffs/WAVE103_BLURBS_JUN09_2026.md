# Wave 103 Blurbs — Unlocking WAN/LAN/Cross-Arch Deployments

**Date**: 2026-06-09
**From**: eastGate overwatch

**Where we are**: Mesh LIVE (11.6h+ stable). Transport injection at 10/11 non-exempt primals. Depot fresh (14/14 x86_64-musl). Zero P1 blockers. Zero self-knowledge violations. NUCLEUS 13/13 alive.

**What we're driving**: Every remaining item below directly unlocks a deployment topology. Transport injection makes primals deploy identically across UDS/TCP/mesh. `ipc.resolve` connects the consumer side (10 primals ready) to the producer side (songBird). Cross-arch gets us to Pixel. WAN mesh gets us to flockGate. These aren't cleanup — they're the infrastructure for the next phase.

---

## 1. toadStool — Transport Adoption (Last Gap)

You're the only non-exempt primal without `TransportEndpoint`. 10/11 have shipped. This blocks isomorphic deployment of any composition that includes toadStool (which is most of them — GPU compute is in `tower`, `agent`, `node`, and `full`).

**What to implement** (~60 lines total):

```rust
// In toadstool-types or equivalent:
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "transport")]
pub enum TransportEndpoint {
    #[serde(rename = "uds")]   Uds { path: String },
    #[serde(rename = "tcp")]   Tcp { host: String, port: u16 },
    #[serde(rename = "mesh_relay")] MeshRelay { peer_id: String, capability: String },
}

// In main.rs — accept at startup:
if let Ok(json) = std::env::var("TRANSPORT_ENDPOINT") {
    match serde_json::from_str::<TransportEndpoint>(&json) {
        Ok(ep) => info!("transport = {ep}"),
        Err(e) => warn!("TRANSPORT_ENDPOINT parse error: {e}"),
    }
}
```

**Reference**: sweetGrass `sweet_grass_core::transport` or nestGate `nestgate-types::transport`. Do NOT import `sourdough-core` — implement locally.

**Why it matters**: Without this, toadStool needs manual `--port` configuration on every deployment. With it, the launcher injects the right transport for the topology.

---

## 2. songBird — `ipc.resolve` Must Return Structured Endpoints (Phase 2 M1)

10 primals accept `TRANSPORT_ENDPOINT`. Nobody produces it yet. `ipc.resolve` is the keystone that connects the two sides.

**Current**: `ipc.resolve` returns plain strings (`/run/biomeos/beardog.sock` or `192.168.1.173:9100`).

**Target**: Return structured JSON that Tower Atomic can inject directly:
```json
{"transport":"uds","path":"/run/user/1000/biomeos/beardog.sock"}
{"transport":"tcp","host":"192.168.1.173","port":9100}
{"transport":"mesh_relay","peer_id":"strandgate","capability":"security"}
```

**Why it matters**: This is what makes topology-aware deployment automatic. When a composition deploys on LAN, `ipc.resolve` returns TCP endpoints to remote primals. On the same machine, UDS. Through the mesh, relay. The primal never knows — it just calls `connect_transport()` on whatever it gets.

---

## 3. biomeOS — Rebuild v4.14 for LocalTrusted

`a459ec58` adds `LocalTrusted` access level. The running binary is pre-v4.14, so `nucleus-deploy --graph-deploy` is still auth-gated.

**Action**: Rebuild from latest, harvest to depot. eastGate revalidates `--graph-deploy` immediately after.

**Why it matters**: Automated graph deployment via `nucleus-deploy` is how we scale from "manually start 13 primals" to "deploy a composition with one command." LocalTrusted means UDS callers (the local operator) can deploy without BTSP token ceremony.

---

## 4. cellMembrane — aarch64 Cross-Compile Pipeline

Pixel deploy script is wired (all 13 handlers). Only sourdough is built for `aarch64-linux-android`. Ring/C-dep elimination is complete across the ecosystem — pure Rust enables clean cross-compile.

**Action**: Set up NDK cross-compile in peptidoglycan. Priority order:
1. beardog (security — needed first on any device)
2. songbird (mesh — needed for connectivity)
3. biomeos (orchestrator)
4. Remaining primals

**Why it matters**: Mobile NUCLEUS on Pixel 8 / GrapheneOS. Transport injection (10/11 done) means the same binary logic works — just different architecture.

---

## 5. cellMembrane — Build-Carrying Cascades

Depot rebuilds are currently manual. After every wave of primal evolution, someone rebuilds on a gate and pushes checksums. `sourDough validate depot --json` (cb526d8) now provides machine-readable staleness data.

**Action**: Wire cascade to detect stale depot binaries and trigger peptidoglycan rebuild automatically. `depot.rs` (194 lines) already tracks `stale=true` per primal.

**Why it matters**: Eliminates the depot freshness gap. When a primal pushes a fix, the depot catches up on next cascade instead of waiting for manual intervention.

---

## 6. All Gates — Mesh Enrollment

The mesh protocol is proven. Any gate with songBird `03f23d45`+ can enroll:

```bash
SECURITY_PROVIDER_SOCKET=/run/user/1000/biomeos/security.sock \
SONGBIRD_PRODUCTION_BIND_ADDRESS=0.0.0.0 \
songbird server --port 7700

echo '{"jsonrpc":"2.0","method":"mesh.init","params":{"node_id":"<gate>","peers":["192.168.1.173:7700","192.168.1.144:7700"]},"id":1}' \
  | socat - UNIX-CONNECT:/run/user/1000/biomeos/songbird.sock
```

**ironGate**: Start federation port to become 3rd LAN gate.
**flockGate**: WAN mesh validation — proves transport works across network boundaries.

---

## How This Unlocks Deployment Topologies

| Topology | Blocked On | When Ready |
|----------|-----------|------------|
| **LAN multi-gate** | ironGate federation port | Now (protocol proven) |
| **WAN covalent** | flockGate coordination | When flockGate enrolls |
| **Pixel mobile NUCLEUS** | aarch64 cross-compile (12 primals) | After NDK pipeline |
| **Automated graph deploy** | biomeOS v4.14 rebuild | After rebuild |
| **Topology-aware routing** | songBird ipc.resolve + toadStool transport | After both ship |
| **Zero-touch gate enrollment** | ipc.resolve + build-carrying cascades | After pipeline automation |
