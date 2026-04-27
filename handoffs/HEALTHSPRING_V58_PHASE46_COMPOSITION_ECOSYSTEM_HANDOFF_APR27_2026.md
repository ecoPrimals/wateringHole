# healthSpring V58 — Phase 46 Composition Ecosystem Handoff

**Date**: April 27, 2026
**From**: healthSpring V58
**For**: primalSpring (upstream absorb), all primal teams, all spring teams

---

## Summary

healthSpring is the first spring to deploy against primalSpring's Phase 46
composition template. Full NUCLEUS (8 primals) validated on x86_64 Linux
using locally-built binaries via `composition_nucleus.sh`. Results:
**18/24 checks pass, 4 fail, 2 skip.** Five new gaps documented.

---

## What Worked

| Component | Evidence |
|-----------|----------|
| `composition_nucleus.sh` | Started 7/8 primals in dependency order. Socket naming, capability aliases, and PID management all correct. |
| `nucleus_composition_lib.sh` | All functions exercised: discover_capabilities, send_rpc, push_scene, subscribe_interactions, make_text_node, composition_startup/teardown. |
| Capability alias symlinks | `{cap}-{family}.sock → {primal}-{family}.sock` pattern enables discovery-based wiring. |
| barraCuda math IPC | 4/4 methods (mean, std_dev, variance, correlation) — all within float epsilon of expected. |
| bearDog crypto.sign | Ed25519 signature returned via JSON-RPC over UDS. |
| toadStool compute | Full capabilities response: 16 cores, 64GB RAM, distributed coordinator. |
| petalTongue (server mode) | Scene push, interaction subscribe, scene dismiss all work without GUI. |
| `find_binary` fallback | CamelCase directory → lowercase binary detection works for all locally-built primals. |

## What Failed

| Component | Issue | Impact |
|-----------|-------|--------|
| **Provenance trio** (rhizoCrypt, loamSpine, sweetGrass) | Accept UDS connections, return empty JSON-RPC responses | DAG, ledger, braid all offline for compositions |
| **Songbird** | `Failed to discover crypto provider` — can't find beardog | No dynamic discovery (symlink fallback works) |
| **petalTongue proprioception** | No frame_rate in server mode | Monitoring degraded in headless |
| **socat** | Not installed; lib requires it | Created `nc -U` shim |

---

## Upstream Asks

### For primalSpring
1. **Provenance trio startup**: Investigate why rhizoCrypt, loamSpine, and
   sweetGrass accept UDS but don't respond to JSON-RPC. This extends PG-45
   to the full trio. Possible causes: missing BTSP negotiation, nestgate
   dependency, different server subcommand, or startup delay.
2. **socat fallback**: Add `nc -U` detection to `nucleus_composition_lib.sh`
   or document socat as a required dependency.
3. **nestgate in defaults**: Add nestgate to `composition_nucleus.sh`'s
   default `PRIMAL_LIST`.

### For Songbird
4. **Crypto provider discovery docs**: Document the expected mechanism for
   finding beardog when started with `--beardog-socket`. Current env vars
   (`SONGBIRD_SECURITY_PROVIDER`, `BTSP_PROVIDER_SOCKET`) and CLI args
   don't seem sufficient.

### For petalTongue
5. **Server mode proprioception**: Return synthetic data (frame_rate=0,
   active_scenes=N, user_interactivity=none) when running headless.

### For All Primal Teams
6. **health.liveness**: The composition probes liveness on all primals.
   Most respond with *some* JSON-RPC (even if not standard health
   format). beardog, petalTongue, toadstool, and barracuda all responded.
   Consider standardizing a minimal health response.

---

## Patterns for Other Springs

### Headless Composition
If you're deploying in a headless/CI environment:
- Set `PETALTONGUE_LIVE=false` in `composition_nucleus.sh`
- Create a non-interactive validation script (see healthSpring's
  `healthspring_composition_headless.sh`)
- petalTongue scene push/dismiss works in server mode

### socat Shim
If socat is unavailable, create `tools/socat`:
```bash
#!/usr/bin/env bash
for arg in "$@"; do
    if [[ "$arg" =~ ^UNIX-CONNECT:(.+)$ ]]; then
        exec nc -q 1 -U "${BASH_REMATCH[1]}"
    fi
done
exit 1
```
Put it on PATH before running compositions.

### Build-from-Source
With `plasmidBin/primals/` empty, build primals locally and
`composition_nucleus.sh` finds them via `$ECO_ROOT/primals/*/target/release/`.
Build petalTongue and toadStool — they're not always pre-built.

---

## healthSpring Composition Architecture

```
composition_nucleus.sh start
  └── beardog → songbird (FAILED) → toadstool → barracuda
      → rhizocrypt → loamspine → sweetgrass → petaltongue
      → capability alias symlinks

healthspring_composition_headless.sh
  └── source nucleus_composition_lib.sh
      ├── discover_capabilities (7/8)
      ├── composition_startup (splash scene)
      ├── Tier 1: capability discovery validation
      ├── Tier 2: liveness probes (4/4)
      ├── Tier 2: barraCuda math IPC (4/4)
      ├── Tier 2: petalTongue scene push (1/1)
      ├── Tier 2: bearDog crypto.sign (1/1)
      ├── Tier 2: toadStool compute (1/1)
      ├── Tier 2: provenance trio (0/3 — empty responses)
      ├── Tier 2: proprioception (0/1 — no frame_rate)
      └── composition_teardown
```

---

**License**: AGPL-3.0-or-later
