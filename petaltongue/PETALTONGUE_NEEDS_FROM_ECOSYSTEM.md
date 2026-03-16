# petalTongue: Explicit Needs from the Ecosystem

**Version**: v1.6.5 (March 15, 2026)

petalTongue is the universal visualization primal. It renders data to humans
across every modality. This document states what petalTongue **needs** from
other primals to deliver complete rendering.

---

## 3D Rendering Pipeline

petalTongue does NOT render 3D directly. The pipeline is:

```
petalTongue (grammar/scene) → barraCuda (GPU compute) → coralReef (shader compile) → ToadStool (display)
```

### From ToadStool (display backend)

**Status**: Partially wired (window lifecycle works, frame submission not yet).

| Need | Method | Status |
|------|--------|--------|
| Create display window | `display.create_window` | Wired |
| Query display capabilities | `display.get_capabilities` | Wired |
| Submit rendered frame | `display.present` | NOT YET WIRED in ToadStool dispatch |
| Get framebuffer for zero-copy | `display.get_framebuffer` | Spec only |
| Frame transport routing | `transport.discover` / `transport.route` | Wired in ToadStool |

**Socket**: `$XDG_RUNTIME_DIR/toadstool/display.sock`

**What we need ToadStool to implement**: Wire `display.present` in the dispatch
handler so petalTongue can push pixel buffers for display. The TSXP frame
protocol exists but is not connected to `display.present`.

### From barraCuda (GPU compute)

**Status**: Physics bridge wired, but limited ops available.

| Need | Method | Status |
|------|--------|--------|
| Dispatch compute | `barracuda.compute.dispatch` | Wired (3 ops: zeros, ones, read) |
| N-body physics | `math.physics.nbody` | NOT in barraCuda dispatch table |
| Statistics | `math.stat.*` | NOT YET |
| Tessellation | `math.tessellate.*` | NOT YET |
| Projection | `math.project.*` | NOT YET |
| Precision routing | `barracuda.tolerances.get` | Available |

**Socket**: `$XDG_RUNTIME_DIR/barracuda/barracuda.sock`

**What we need barraCuda to implement**: Add `math.stat.histogram`,
`math.stat.kde`, `math.tessellate.delaunay`, `math.project.mercator` dispatch
ops. petalTongue currently computes these on CPU.

### From coralReef (shader compilation)

**Status**: Not directly called by petalTongue (goes through barraCuda).

| Need | Method | Status |
|------|--------|--------|
| Compile WGSL | `shader.compile.wgsl` | Available in coralReef |
| Check capabilities | `shader.compile.capabilities` | Available |

**Socket**: `$XDG_RUNTIME_DIR/ecoPrimals/coralreef.sock`

petalTongue does not call coralReef directly. If we ever need custom GPU
visualization shaders, we would submit WGSL through barraCuda.

---

## Sound Output

petalTongue synthesizes audio (5 waveforms, stereo panning, fade envelopes)
in `petal-tongue-scene/src/soundscape.rs`. However, **there is no ecosystem
audio output path**.

### Current Gap

| Component | Audio Status |
|-----------|-------------|
| ToadStool | No `audio.*` methods, `transport.*` is for display/capture/serial only |
| barraCuda | Has audio WGSL shaders (mel_scale, conv1d) but no audio I/O |
| coralReef | Shader compiler only, no audio |

### What We Need

**Option A (preferred)**: ToadStool adds `audio.play` and `audio.stream`
JSON-RPC methods, with ALSA/PulseAudio/PipeWire backend. petalTongue sends
PCM samples via `audio.play { samples: [...], sample_rate: 44100 }`.

**Option B**: A new `audioSpring` primal handles audio I/O. petalTongue
sends synthesized PCM via JSON-RPC.

**Option C (current fallback)**: petalTongue uses `cpal`/`rodio` directly
for local audio output, bypassing the ecosystem. This works for single-machine
deployment but breaks the primal separation model.

**Interim**: petalTongue exports WAV files and soundscape definitions as JSON.
ludoSpring and other consumers can render locally.

---

## Discovery & Registration

### From Songbird

| Need | Method | Status |
|------|--------|--------|
| Register at startup | `discovery.register` | Wired |
| Heartbeat | `discovery.heartbeat` | Wired |
| Discover by capability | `discovery.query` | Available |

**Socket**: Via `SONGBIRD_SOCKET` env or capability discovery.

### From NestGate (artifact storage)

| Need | Method | Status |
|------|--------|--------|
| Store dashboard SVG | `storage.put` | NOT YET called by petalTongue |
| Retrieve stored artifacts | `storage.get` | NOT YET |

**Socket**: Via capability discovery (`storage` capability).

petalTongue currently exports SVG/PNG to local filesystem. Evolving to
NestGate storage would enable ecosystem-wide artifact sharing.

---

## Provenance & Attribution

### From rhizoCrypt (ephemeral state)

| Need | Method | Status |
|------|--------|--------|
| Session-scoped viz state | `dag.create_session` | NOT YET |
| Commit viz to permanent | `dag.dehydration.trigger` | NOT YET |

### From sweetGrass (attribution)

| Need | Method | Status |
|------|--------|--------|
| Record viz attribution | `provenance.create_braid` | NOT YET |
| Track data lineage | `provenance.attribution_chain` | NOT YET |

---

## Summary: What Other Primals Should Know

1. **petalTongue renders anything**: Send us grammar expressions or DataBinding
   payloads (11 variants) and we compile to the best available modality.

2. **We need `display.present`**: ToadStool window lifecycle works, but we
   cannot push frames yet.

3. **We need audio output**: No ecosystem path exists for synthesized audio.
   ToadStool `audio.*` methods would be ideal.

4. **We need more GPU ops**: barraCuda has 3 ops; we need statistics,
   tessellation, and projection for offloading visualization computation.

5. **ludoSpring**: We support `GameScene` and `Soundscape` DataBindings.
   Send `channel_type: "game_scene"` or `channel_type: "soundscape"` via
   `visualization.render` and we handle it.

---

**Last Updated**: March 15, 2026
**Maintainer**: ecoPrimals / petalTongue
**License**: AGPL-3.0-only
