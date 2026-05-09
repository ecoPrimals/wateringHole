<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# neuralSpring → Squirrel: Inference Provider Registration Guide

**Date**: May 7, 2026
**From**: Squirrel (primalSpring Phase 60 audit response)
**Priority**: P3 (not blocking NUCLEUS deployment)

## Context

primalSpring's `validate_squirrel_roundtrip` experiment exits with `skip` because no
live native inference provider is available. Squirrel's `inference.complete` pipeline
is fully functional (15 wire tests pass), but it bridges to external providers
(Ollama, OpenAI-compatible). For full E2E parity without external deps, neuralSpring
needs to register a native inference endpoint with Squirrel.

## What neuralSpring Needs to Implement

### 1. JSON-RPC Server on Unix Socket

neuralSpring must expose a JSON-RPC 2.0 server on a Unix domain socket that handles:

```json
{
  "jsonrpc": "2.0",
  "method": "inference.complete",
  "params": {
    "prompt": "string",
    "model": "optional-string",
    "temperature": 0.7,
    "max_tokens": 1024
  },
  "id": 1
}
```

**Response format** (Squirrel expects these fields in `result`):

```json
{
  "jsonrpc": "2.0",
  "result": {
    "text": "generated text response",
    "model": "model-name-used",
    "provider": "neuralSpring"
  },
  "id": 1
}
```

Optional fields in response: `usage` (`{ prompt_tokens, completion_tokens, total_tokens }`).

### 2. Register with Squirrel at Startup

After launching the inference socket, send:

```json
{
  "jsonrpc": "2.0",
  "method": "inference.register_provider",
  "params": {
    "provider_id": "neuralspring-native",
    "socket": "/run/user/<uid>/biomeos/neuralspring-inference.sock",
    "capabilities": ["text-generation", "embedding"]
  },
  "id": 1
}
```

To Squirrel's control socket at:
```
$XDG_RUNTIME_DIR/biomeos/squirrel-${FAMILY_ID}.sock
```

### 3. Handle `inference.embed` (optional, for embedding parity)

```json
{
  "jsonrpc": "2.0",
  "method": "inference.embed",
  "params": {
    "text": "string to embed",
    "model": "optional-string"
  },
  "id": 1
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "embedding": [0.1, 0.2, ...],
    "model": "model-name",
    "dimensions": 768
  },
  "id": 1
}
```

## Squirrel's Internal Flow

```
caller → inference.complete (JSON-RPC)
       → AiRouter::generate_text
       → ProviderSelector::select_best (filters by is_available + supports_text)
       → RemoteInferenceAdapter::generate_text
       → forward JSON-RPC "inference.complete" to registered socket
       → parse response → return to caller
```

## Wire Protocol Details

- Transport: **Unix domain socket**, newline-delimited JSON-RPC
- Each message is a single JSON line terminated by `\n`
- Squirrel sends exactly one request per connection (short-lived)
- No batching, no streaming (simple request/response)

## Registration Lifecycle

- `inference.register_provider` — registers or upserts (idempotent)
- `inference.unregister_provider { provider_id }` — removes
- `inference.models` — returns merged model list from all providers
- Provider health: Squirrel marks providers as unavailable if socket connection fails

## Reference Implementation

See Squirrel's test mock at:
`crates/main/tests/inference_register_provider_tests.rs` (function `spawn_mock_neural_spring`)

This spawns a tiny UDS server that implements `inference.complete` and `inference.embed`
and demonstrates the exact wire protocol neuralSpring needs to speak.
