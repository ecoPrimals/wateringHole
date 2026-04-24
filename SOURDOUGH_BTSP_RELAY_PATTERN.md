# sourDough BTSP Relay Pattern

**Version:** 1.0.0
**Date:** April 24, 2026
**Status:** Extracted from converged primals — the pattern that works
**Authority:** wateringHole (ecoPrimals Core Standards)
**Related:** `BTSP_PROTOCOL_STANDARD.md`, `handoffs/BTSP_WIRE_CONVERGENCE_APR24_2026.md`

---

## What This Is

This document extracts the BTSP relay pattern that **naturally emerged**
across 9 converged primals. It is not a dictated specification — it is
the pattern that survived contact with reality. Future primals (starting
with sourDough) absorb this as starter culture.

The pattern has three parts:

1. **Accept-side auto-detect** — route incoming connections to BTSP or
   plain JSON-RPC based on the first line of data
2. **BearDog relay** — delegate handshake cryptography to BearDog via
   two JSON-RPC calls
3. **Error handling** — never silently drop a connection

---

## Part 1: Accept-Side Auto-Detect

When a client connects to your UDS socket, you don't know if it wants
BTSP or plain JSON-RPC. Detect by peeking.

### Algorithm

```
1. Peek first byte (do NOT consume)
2. If byte == 0x7B ('{'):
   a. Read the full first line (up to '\n')
   b. If line contains "protocol" AND "btsp":
      → BTSP JSON-line handshake path
   c. Else:
      → Plain JSON-RPC (replay the first line as a request)
3. Else:
   → BTSP length-prefixed binary handshake path
```

### Reference (Songbird — connection.rs)

```rust
let first_byte = reader.fill_buf().await?[0];

if first_byte == b'{' {
    let mut first_line = String::new();
    reader.read_line(&mut first_line).await?;

    if is_btsp_client_hello(&first_line) {
        // → BTSP JSON-line handshake
        perform_server_handshake_ndjson(&first_line, &mut reader, &mut writer, &security_client).await
    } else {
        // → Plain JSON-RPC (process first_line as request, then continue)
        handle_ndjson_first_line_then_session(first_line, reader, writer).await
    }
}
```

### Gate: When to activate

Auto-detect activates when `FAMILY_ID` is set to a non-empty,
non-`"default"` value and `BIOMEOS_INSECURE` is NOT set. In development
mode (no `FAMILY_ID`), skip the peek and go directly to plain JSON-RPC.

```rust
fn btsp_required() -> bool {
    let insecure = env::var("BIOMEOS_INSECURE")
        .map(|v| v == "1" || v.eq_ignore_ascii_case("true"))
        .unwrap_or(false);
    if insecure { return false; }

    let fid = env::var("FAMILY_ID")
        .or_else(|_| env::var("BIOMEOS_FAMILY_ID"))
        .unwrap_or_default();

    !fid.is_empty() && fid != "default"
}
```

---

## Part 2: BearDog Relay

Your primal does NOT implement cryptography. BearDog does. Your job is
to relay the handshake between the connecting client and BearDog.

### Flow

```
Client                     Your Primal                  BearDog
  │                            │                           │
  │─── ClientHello ──────────→│                           │
  │                            │── btsp.session.create ──→│
  │                            │←── {session_token,       │
  │                            │     challenge,            │
  │                            │     server_ephemeral_pub} │
  │←── ServerHello ───────────│                           │
  │                            │                           │
  │─── ChallengeResponse ───→│                           │
  │                            │── btsp.session.verify ──→│
  │                            │←── {verified, session_id, │
  │                            │     cipher}               │
  │←── HandshakeComplete ────│                           │
  │                            │                           │
  │   (authenticated session)  │                           │
```

### Step-by-step

**1. Parse ClientHello** (already read from the first line)

```rust
let hello: ClientHello = serde_json::from_str(&first_line)?;
// hello.protocol == "btsp", hello.version == 1
// hello.client_ephemeral_pub == base64-encoded bytes
```

**2. Call BearDog `btsp.session.create`**

```rust
let family_seed = env::var("FAMILY_SEED")
    .or_else(|_| env::var("BEARDOG_FAMILY_SEED"))
    .or_else(|_| env::var("BIOMEOS_FAMILY_SEED"))?;

let create_req = json!({
    "jsonrpc": "2.0",
    "method": "btsp.session.create",
    "params": {
        "family_seed": family_seed.trim()  // raw string, NOT base64-encoded
    },
    "id": 1
});
```

Connect to BearDog socket, write request + `\n`, read JSON response.

**3. Build and send ServerHello**

```rust
let create_result = parse_response(beardog_response)?;

let server_hello = json!({
    "version": 1,
    "server_ephemeral_pub": create_result["server_ephemeral_pub"],
    "challenge": create_result["challenge"],
    // Optional but helpful:
    "session_id": create_result.get("session_token")
                    .or(create_result.get("session_id"))
});
write_json_line(&mut client_writer, &server_hello).await?;
```

**4. Read ChallengeResponse from client**

```rust
let mut response_line = String::new();
client_reader.read_line(&mut response_line).await?;
let challenge_resp: serde_json::Value = serde_json::from_str(&response_line)?;
```

**5. Call BearDog `btsp.session.verify`**

```rust
let verify_req = json!({
    "jsonrpc": "2.0",
    "method": "btsp.session.verify",
    "params": {
        "session_token": session_token,
        "response": challenge_resp["response"],
        "client_ephemeral_pub": hello.client_ephemeral_pub,
        "preferred_cipher": challenge_resp.get("preferred_cipher").unwrap_or(&json!("null"))
    },
    "id": 2
});
```

Write to BearDog socket (same connection), read JSON response.

**6. Build and send HandshakeComplete**

```rust
let verify_result = parse_response(beardog_response)?;
let verified = verify_result["verified"].as_bool().unwrap_or(false);

if !verified {
    write_error_frame(&mut client_writer, "verification failed").await?;
    return Err(...);
}

let complete = json!({
    "status": "ok",
    "session_id": verify_result.get("session_id").unwrap_or(&session_token_val),
    "cipher": verify_result.get("cipher").unwrap_or(&json!("null"))
});
write_json_line(&mut client_writer, &complete).await?;
```

---

## Part 3: Critical Implementation Details

### JSON-aware socket reads (DO NOT use read_to_end)

BearDog keeps sockets open. `read_to_end()` hangs forever. Read in
chunks and break when you have complete JSON:

```rust
async fn read_json_response<R: AsyncReadExt + Unpin>(
    stream: &mut R,
    timeout_per_chunk: Duration,
) -> Result<Vec<u8>> {
    let mut buffer = Vec::new();
    let mut temp = [0u8; 4096];
    loop {
        match timeout(timeout_per_chunk, stream.read(&mut temp)).await {
            Ok(Ok(0)) => break,
            Ok(Ok(n)) => {
                buffer.extend_from_slice(&temp[..n]);
                if serde_json::from_slice::<serde_json::Value>(&buffer).is_ok() {
                    break;
                }
            }
            Ok(Err(e)) => return Err(e.into()),
            Err(_) => {
                if !buffer.is_empty() && serde_json::from_slice::<serde_json::Value>(&buffer).is_ok() {
                    break;
                }
                return Err(anyhow!("timeout"));
            }
        }
    }
    Ok(buffer)
}
```

### Never call stream.shutdown() during relay

`stream.shutdown()` sends TCP FIN / closes write half. BearDog
interprets this as connection close and drops the response. Use
`flush()` instead:

```rust
// WRONG — kills the connection:
stream.shutdown().await?;

// RIGHT — ensures bytes are sent:
stream.flush().await?;
```

### family_seed as raw string

`FAMILY_SEED` from the environment is a hex string (e.g.,
`e06c1785c14c45983e...`). Pass it to BearDog as-is. Do NOT:
- Hex-decode it to bytes
- Base64-encode it
- Add or strip encoding

Just `trim()` whitespace and send the string.

### Error frames must match client framing

If the client sent JSON-line (starts with `{`), your error response
must be JSON-line:

```json
{"error":"handshake_failed","reason":"BearDog relay: session create failed"}
```

Never return nothing. Never close silently. The client (primalSpring
guidestone) reports silent drops as "BTSP: server closed connection
(no ServerHello)" — this is the hardest class of bug to diagnose.

---

## Self-Test

After implementing, verify with socat:

```bash
# 1. Launch NUCLEUS
export FAMILY_ID="test01"
export FAMILY_SEED="$(head -c 32 /dev/urandom | xxd -p | tr -d '\n')"
# ...start primals...

# 2. Test auto-detect (should return ServerHello)
echo '{"protocol":"btsp","version":1,"client_ephemeral_pub":"dGVzdA=="}' \
  | socat -t3 - UNIX-CONNECT:/run/user/$(id -u)/biomeos/yourprimal-test01.sock

# 3. Test plain JSON-RPC (should still work)
echo '{"jsonrpc":"2.0","method":"health.check","id":1}' \
  | socat -t3 - UNIX-CONNECT:/run/user/$(id -u)/biomeos/yourprimal-test01.sock

# 4. Full validation
primalspring_guidestone  # should show "BTSP authenticated" for your capability
```

---

## Convergence Status

| Primal | Auto-Detect | BearDog Relay | Error Frames | Full Handshake |
|---|---|---|---|---|
| coralReef | yes | yes | yes | **converged** |
| Squirrel | yes | yes | yes | **converged** |
| rhizoCrypt | yes | yes | yes | **converged** |
| sweetGrass | yes | yes | yes | **converged** |
| loamSpine | yes | yes | yes | **converged** |
| petalTongue | yes | yes | yes | **converged** |
| Songbird | yes | partial | no | converging (Wave 165) |
| ToadStool | yes | partial | yes | converging (Session 177) |
| barraCuda | yes | partial | yes | converging (Sprint 44g) |
| NestGate | yes | yes | yes | converging (Session 45c) |

"Partial" relay means ServerHello succeeds but the verify round-trip
to BearDog doesn't complete. The pattern above documents the full
path — compare against the reference implementations to find the
remaining mismatch.

---

## For sourDough

This pattern will be absorbed into sourDough as the default BTSP relay
implementation. New primals scaffolded from sourDough will have:

1. Auto-detect wired into the UDS accept loop
2. BearDog relay as a library function (not copy-pasted)
3. Error frames that match client framing
4. JSON-aware chunked reads
5. `btsp_required()` gate matching the ecosystem standard

The goal: future primals get BTSP relay correct on first compile.
