# barraCuda — HCI Formula Variant Gaps + Perlin Lattice

**Date**: March 31, 2026
**Priority**: P2 — HIGH
**Reporter**: ludoSpring V37.1 live validation
**Cross-reference**: primalSpring `docs/PRIMAL_GAPS.md` BC-01, BC-02, BC-03, BC-04

---

## Gap 1: Fitts Formula (BC-01)

`activation.fitts(distance=256, width=32, a=200, b=150)`:
- **barraCuda returns**: 800 (Welford: `a + b * log2(D/W)`)
- **Python baseline**: 708.85 (Shannon: `a + b * log2(2*D/W + 1)`)

Shannon is the most-cited formulation in HCI literature.

**Fix**: Add `variant` parameter (default: `"shannon"`):
```json
{"method": "activation.fitts", "params": {"distance": 256, "width": 32, "a": 200, "b": 150, "variant": "shannon"}}
```

## Gap 2: Hick Formula (BC-02)

`activation.hick(n_choices=8, a=200, b=150)`:
- **barraCuda returns**: 675.49 (`a + b * log2(n+1)` — includes "no-choice" option)
- **Python baseline**: 650 (`a + b * log2(n)` — standard)

**Fix**: Add `include_no_choice` parameter (default: `false`):
```json
{"method": "activation.hick", "params": {"n_choices": 8, "a": 200, "b": 150, "include_no_choice": false}}
```

## Gap 3: Perlin3D Lattice Invariant (BC-03)

`noise.perlin3d(0, 0, 0)` returns `-0.11` instead of `0`.

By definition, gradient noise MUST be zero at integer lattice points. This suggests
a bug in the 3D gradient interpolation at lattice boundaries.

**Fix**: Check gradient dot products at integer inputs — they should all be exactly 0.

## Gap 4: No plasmidBin Binary (BC-04)

barraCuda was started from source build (`target/release/barracuda`) during ludoSpring
testing. Needs a published ecoBin in `infra/plasmidBin/barracuda/`.

## Impact

- **exp089**: -4 checks (Fitts + Hick)
- **exp091**: -1 check (Perlin3D)
- **Total**: +5 checks when fixed

## Experiments Affected

ludoSpring V37.1: exp089 (psychomotor composition), exp091 (PCG/noise)
