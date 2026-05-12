# rhizoCrypt — Unix Domain Socket Transport Gap

**Date**: March 31, 2026
**Priority**: P1 — CRITICAL
**Status**: **RESOLVED** — v0.14.0-dev session 23 (March 31, 2026)
**Reporter**: ludoSpring V37.1 live validation
**Cross-reference**: primalSpring `docs/PRIMAL_GAPS.md` RC-01

---

## Problem

rhizoCrypt only binds TCP (`0.0.0.0:9401`). It does not create a Unix domain socket.
Every other ecoBin primal (BearDog, NestGate, sweetGrass, barraCuda, Songbird) follows
`$XDG_RUNTIME_DIR/biomeos/{primal}.sock`. `start_primal.sh` passes `--socket` but
rhizoCrypt ignores it.

## Impact

- **4 experiments blocked**: exp094, exp095, exp096, exp098 cannot reach rhizoCrypt
- **+9 checks** will pass when fixed
- **All provenance trio compositions blocked** via UDS — the session_provenance graph
  cannot deploy rhizoCrypt alongside loamSpine and sweetGrass

## Required Fix

Add `--unix [PATH]` CLI flag with default `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`.

Follow barraCuda's pattern:
```
rhizocrypt server --unix                    # default XDG path
rhizocrypt server --unix /custom/path.sock  # override
rhizocrypt server --tcp 0.0.0.0:9401        # keep TCP as option
```

## Validation

After fix, run ludoSpring exp094-098:
```bash
ECOPRIMALS_PLASMID_BIN=../plasmidBin cargo run --bin exp094
ECOPRIMALS_PLASMID_BIN=../plasmidBin cargo run --bin exp095  # also needs loamSpine fix
```

Or test manually:
```bash
echo '{"jsonrpc":"2.0","method":"health.liveness","id":1}' | socat - UNIX-CONNECT:/run/user/1000/biomeos/rhizocrypt.sock
```
