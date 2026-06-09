# Wave 106 Blurbs — Cross-Topology Validation & Autonomous Gates

**Date**: 2026-06-09
**From**: eastGate overwatch

**What changed**: Comprehensive AAR completed. Every deployment issue, every pipeline failure, every neuralAPI gap documented. Old FRAGO archived (12/16 items resolved). New FRAGO focused on cross-topology validation — proving the deployment model works on every gate, every arch, every network topology. Gate enrollment playbook published.

**The shift**: We are no longer building the deployment pipeline. We are now validating it across topologies. Each gate that comes online is a validation opportunity. We evolve the tooling as we go.

---

## To: cellMembrane

### Gate Bootstrap Command (P2)

The AAR identified that deploying a gate requires 5+ manual steps. As strandGate, ironGate, southGate, and future gates come online, this multiplies. We need `membrane gate.bootstrap <gate-name>` that does everything in one command: detect arch → fetch depot → verify checksums → configure mesh → start NUCLEUS → health sweep.

A gate enrollment playbook (manual version) is in the FRAGO. Each gate you help deploy makes the next one easier.

### Bug Fixes

1. **plasmid.fetch --source vps** — destination path doubles up (`primals/arch/primals/arch/`). All 13 downloads fail. Direct curl works. Need path normalization fix.
2. **cascade auto-fetch** — when checksums.toml changes in cascade, nothing triggers binary update. Post-cascade hook that calls `plasmid.fetch` would close the loop from peptidoglycan-build to gate-running.

### Resolved (thank you — massive wave)

Everything from Wave 104 FRAGO: WAN depot, cascade conflict auto-resolve, harvest atomic rename, aarch64 sweep, multi-target checksums, VPS depot sync. All shipped, all working.

---

## To: songBird

### Mesh Persistence (P1 — blocks autonomous operation)

The AAR's #1 interaction gap: mesh state is ephemeral. Every songbird restart requires manual `mesh.init`. When a gate reboots, it has zero peers. This blocks autonomous recovery.

**Action**:
1. Persist peers to `~/.local/share/songbird/peers.toml`
2. On startup, auto-connect to persisted peers
3. `mesh.init` should append to persistent store

### Federation Port Not Binding

eastGate songbird runs with `SONGBIRD_FEDERATION_PORT=7700` and `--port 7700` but port 7700 never appears in `ss -tlnp`. ironGate was blocked for days because eastGate:7700 refused connections. Meanwhile, golgiBody VPS songbird binds 7700 correctly.

**Action**: Investigate why the federation listener doesn't start in UDS-server mode. Either:
- Fix the server initialization to start TCP listener alongside UDS
- Add `federation.enable` JSON-RPC method that opens TCP at runtime
- Document the correct startup sequence that reliably binds both UDS + TCP

---

## To: biomeOS

### NUCLEUS Supervision (P1 — blocks autonomous operation)

NUCLEUS primals died silently 3+ times during Wave 105. No watchdog, no restart, no detection. Manual operator intervention each time.

**Action**: Implement one of:
- `lifecycle.watchdog` method — polls `health.liveness` every 30s, restarts failures from depot
- systemd user unit generation — `composition.deploy` creates per-primal `.service` files
- `--supervised` mode in nucleus-deploy that registers with systemd

This is the single biggest gap between "deployment works" and "deployment is autonomous."

---

## To: primalSpring (parallel team)

### grapheneGate 13/13 (P2)

You own grapheneGate. 6/13 running. 7 need `BIOMEOS_SOCKET_DIR` env var support:
- skunkbat, toadstool, barracuda, coralreef, nestgate, biomeos, petaltongue
- Android can't write to `/run/user/` or `/tmp/biomeos/`
- Override to `/data/local/tmp/biomeos/`
- `deploy_pixel.sh` should set this env var before launch

---

## To: all gates (when you come online)

### Gate Enrollment Playbook

Full manual procedure is in the FRAGO (`wave106-cross-topology-validation.toml`). Short version:

```bash
# Fetch from VPS (the sole authority)
for p in beardog songbird biomeos nestgate coralreef sweetgrass squirrel \
         loamspine rhizocrypt skunkbat petaltongue barracuda toadstool; do
  curl -o primals/x86_64-unknown-linux-musl/$p \
    https://membrane.primals.eco/depot/x86_64-unknown-linux-musl/$p
  chmod +x primals/x86_64-unknown-linux-musl/$p
done

# Start songbird, mesh to VPS
SONGBIRD_FEDERATION_PORT=7700 songbird server --socket /run/user/$(id -u)/biomeos/songbird.sock &
echo '{"jsonrpc":"2.0","method":"mesh.init","params":{"node_id":"<YOUR_GATE>","peers":["157.230.3.183:7700"]},"id":1}' | \
  socat - UNIX-CONNECT:/run/user/$(id -u)/biomeos/songbird.sock

# Start NUCLEUS, verify
for p in beardog biomeos nestgate ...; do primals/x86_64-unknown-linux-musl/$p server &; done
```

DO NOT `cargo build --release` for deployment. VPS is the sole depot authority.

---

## What Each Gate Validates

| Gate | Topology | What It Proves |
|------|----------|----------------|
| strandGate | LAN x86_64 re-enrollment | gate.bootstrap works, mesh rejoin after extended offline |
| ironGate | 3rd mesh node via VPS relay | Collective without direct peer (VPS-mediated mesh) |
| flockGate | WAN e2e 5/5 | Remote covalent over WAN → stadial criterion 4 |
| grapheneGate | aarch64 13/13 | Cross-arch + Android adaptation |
| southGate | Cross-subnet mesh | TURN relay or router-routed federation |

---

## Reshaped Priority Map

```
P1 (blocks autonomous operation):
  biomeOS → NUCLEUS supervision (watchdog or systemd units)
  songBird → mesh peer persistence (auto-reconnect on restart)

P2 (blocks stadial, validate as gates come online):
  eastGate → fix federation port 7700 binding
  cellMembrane → gate.bootstrap command + plasmid.fetch path fix
  ironGate → 3rd mesh node (mesh.init to VPS relay)
  flockGate → WAN e2e 5/5 (VPS relay now LIVE)
  primalSpring → grapheneGate 13/13 (UDS adaptation)

LOW (future targets):
  sourDough → validate depot segfault
  bearDog → StrongBox NDK compilation (android target)
  future → Windows ecoBin, wasm32-wasi
```

---

## Reference

- `AAR_WAVE105_COMPREHENSIVE_CROSS_DEPLOYMENT_JUN09_2026.md` — full AAR (17 issues documented)
- `wave106-cross-topology-validation.toml` — FRAGO (gate enrollment playbook + remaining work)
- `GLACIAL_SHIFT_READINESS.md` — updated to Wave 105c (post-primordial enforced)
- `ECOBIN_ARCHITECTURE_STANDARD.md` — plasmidBin submission rewritten for VPS-only
