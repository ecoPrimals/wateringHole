# coralReef — Phase D: Mixed Command Streams (Compute → Display Bridge)

**From**: primalSpring v0.9.17 (Phase 45c — Graphics Node)
**Date**: April 26, 2026
**For**: coralReef team

---

## Context

toadStool's `NEXT_STEPS.md` lists **Phase D: Mixed command streams** as
planned work blocked on coralReef/FECS. With petalTongue moving toward a
full graphics system and toadStool display backend reaching Phase 2, the
compute-to-display bridge is the longest-pole dependency for GPU-accelerated
rendering in NUCLEUS compositions.

Today, coralReef handles shader compilation and GPU compute dispatch through
`coral-gpu`/`coral-driver`. The compute results are read back to CPU, then
any display happens through a separate path (petalTongue/egui or toadStool
DRM framebuffer). There is no shared GPU memory between compute and display.

---

## What Phase D Needs

### Mixed command streams: draw + compute + framebuffer

The goal is a unified dispatch pipeline where a single GPU submission can
include both compute work (physics, simulation, procedural generation) and
display work (render the results to a framebuffer) without CPU readback in
between.

### Concrete scenarios this enables

**barraCuda physics → display** (zero-copy):
```
barraCuda computes particle positions (GPU buffer A)
  → coralReef mixed-command dispatch: compute → render pass
  → GPU renders particles directly from buffer A to framebuffer
  → toadStool presents framebuffer to DRM/display
  (no GPU→CPU→GPU roundtrip)
```

**Procedural terrain + live visualization**:
```
Perlin noise computed on GPU (barraCuda/coralReef)
  → mixed-command: compute pass → vertex generation → rasterization
  → framebuffer output to toadStool display
```

**Shader-driven UI elements**:
```
coralReef compiles custom WGSL fragment shader
  → toadStool dispatches as part of display pipeline
  → petalTongue SceneGraph references shader output as texture
```

### Proposed additions to coral-gpu

| Component | Current | Needed |
|-----------|---------|--------|
| `GpuCommandBuffer` | Compute-only (dispatch workgroups, buffer copy) | Mixed: compute dispatch + render pass (vertex/fragment) + framebuffer attachment |
| `GpuRenderPass` | Does not exist | Vertex buffer binding, fragment shader, framebuffer output target |
| `GpuSharedBuffer` | Compute buffers (storage, uniform) | Extend with vertex/index buffer usage flags + framebuffer-compatible format |
| `GpuFramebuffer` | Does not exist | wgpu `TextureView` as render target, exportable via DMA-BUF/memfd to toadStool |

### Proposed IPC additions

New methods on the `shader` capability (coralReef's IPC surface):

```
shader.compile.render    — compile a vertex + fragment shader pair
shader.framebuffer.create — allocate a GPU framebuffer exportable to display
shader.framebuffer.export — return DMA-BUF fd or memfd handle for toadStool
```

New dispatch mode in toadStool's `compute.dispatch.submit`:

```json
{
  "method": "compute.dispatch.submit",
  "params": {
    "binary": "<compiled compute shader bytes>",
    "dispatch_mode": "mixed",
    "render_pass": {
      "vertex_shader": "<compiled vertex shader bytes>",
      "fragment_shader": "<compiled fragment shader bytes>",
      "framebuffer_id": "fb-shared-001",
      "vertex_buffer": "buffer-particles",
      "draw_count": 10000
    },
    "buffers": [
      { "binding": 0, "id": "buffer-particles", "usage": "storage_vertex" }
    ]
  }
}
```

### Implementation path

**Step 1**: Add render pass support to `coral-gpu`
- wgpu `RenderPipeline` creation alongside existing `ComputePipeline`
- `GpuCommandBuffer` accepts both compute and render pass entries
- Buffer usage flags extended for vertex/index/render-target

**Step 2**: Framebuffer export
- Create framebuffer as wgpu `Texture` with `RENDER_ATTACHMENT` usage
- Export via DMA-BUF (Linux DRM) or map to shared memory (memfd)
- toadStool display backend imports the framebuffer for compositing

**Step 3**: Mixed-mode dispatch in toadStool
- `compute.dispatch.submit` accepts `dispatch_mode: "mixed"` with
  attached render pass configuration
- toadStool forwards to coralReef for execution
- Result includes framebuffer handle for display pipeline

**Step 4**: Wire to petalTongue
- petalTongue `Texture` primitive (see petalTongue handoff) references
  the exported framebuffer via `texture_id`
- Scene graph renders GPU-computed content at native speed

---

## Relationship to existing coralReef architecture

| Component | Role | Phase D Impact |
|-----------|------|----------------|
| `coral-reef` (compiler) | WGSL/SPIR-V → native | Add render shader compilation (vertex + fragment) |
| `coral-driver` | DRM ioctl dispatch | Extend for render-node dispatch (not just compute-node) |
| `coral-gpu` | In-process compute API | Add render pass, framebuffer, mixed command buffer |
| `coral-ember` | VFIO device management | Add display-capable device policy (currently isolates from display) |
| `coral-glowplug` | GPU lifecycle daemon | Add framebuffer allocation/export in `device.*` methods |

### DRM isolation consideration

`coral-ember`'s `drm_isolation` currently generates udev rules to keep
compute GPUs OFF the desktop compositor. For mixed command streams, the
policy needs a third option: **compute-primary with render export** — the
GPU handles compute dispatch AND can produce framebuffers, but does NOT
become a display seat. The framebuffer is exported to toadStool display
backend (which manages the actual DRM seat) for compositing.

---

## Priority and dependencies

Phase D is the **longest-pole** evolution in the graphics node plan.
It depends on:

1. toadStool Display Phase 2 (consumer of exported framebuffers)
2. petalTongue Texture Primitive (scene graph consumer of GPU output)
3. coralReef render pass support (this handoff)

The CPU-based path (compute → readback → upload to egui) works TODAY for
moderate frame rates. Phase D eliminates the readback bottleneck for
60+ FPS GPU-accelerated rendering.

### Interim workaround (no Phase D needed)

For immediate use, the composition can use the CPU path:

```
barraCuda compute → JSON-RPC result (CPU)
  → petalTongue visualization.render.stream (CPU)
  → egui paint (CPU/GPU via wgpu)
```

This works for dashboards, metrics, and moderate-complexity visualizations.
Phase D is needed for real-time game rendering, particle systems, and
GPU-heavy procedural content.

---

**References**:
- toadStool NEXT_STEPS.md: Phase D description
- coral-gpu: `coralReef/crates/coral-gpu/src/lib.rs`
- coral-driver: `coralReef/crates/coral-driver/`
- coral-ember DRM isolation: `coralReef/crates/coral-ember/src/drm_isolation.rs`
- toadStool dispatch spec: `toadStool/specs/DISPATCH_WIRE_CONTRACT.md`
- petalTongue texture handoff: `wateringHole/handoffs/PETALTONGUE_TEXTURE_PRIMITIVE_OVERLAY_HANDOFF_APR26_2026.md`
- toadStool display handoff: `wateringHole/handoffs/TOADSTOOL_DISPLAY_PHASE2_GRAPHICS_NODE_HANDOFF_APR26_2026.md`

License: AGPL-3.0-or-later
