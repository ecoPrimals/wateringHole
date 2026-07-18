# cellMembrane Wave 148a — esotericWebb Deploy Fix

**Date**: 2026-07-18 | **Wave**: 148a | **Scope**: esotericWebb port + unit + Caddy correction

---

## Summary

esotericWebb AAR resolved all 3 deploy blockers. This wave fixes the
cellMembrane-side artifacts to match the actual esotericWebb deploy command
and port assignment.

### Port Clarification

Port confusion clarified upstream:
- **8080** = nestGate / petalTongue (unchanged)
- **8090** = esotericWebb on flockGate (was incorrectly wired to 8080)

### Changes

1. **`esotericwebb-server.service`**: ExecStart fixed from `server --socket`
   to `serve --content content/ --listen 0.0.0.0:8090`. WorkingDirectory
   set to `/opt/ecoPrimals/gardens/esotericWebb`. Restart policy changed
   from `always` to `on-failure` per upstream spec.

2. **`DEFAULT_ESOTERICWEBB_PORT` constant** (8090): Added to
   `cellmembrane-types/src/service/constants.rs`.

3. **Caddy generation**: `/webb/*` sub-route upstream corrected from
   `petalTongue:8080` → `esotericWebb:8090`.

### Test Impact

1,100 tests — all passing. 0 clippy warnings. No new tests needed
(existing Caddy + gateway tests validate the routing).

---

## Remaining Upstream Gaps

| Gap | Owner | Priority |
|-----|-------|----------|
| songBird BTSP → `gate.enroll` integration | cellMembrane | P1 |
| squirrel: accept `null` params on health | squirrel | P1 |
| nestGate: `PROJECTS_PATH` CAS wiring | nestGate | P1 |
| petalTongue: `WS_PATH` agent bridge | petalTongue | P1 |
| bearDog: crypto JSON-RPC sigs | bearDog | P1 |
| sweetGrass: `braid.create/query` | sweetGrass | P1 |
