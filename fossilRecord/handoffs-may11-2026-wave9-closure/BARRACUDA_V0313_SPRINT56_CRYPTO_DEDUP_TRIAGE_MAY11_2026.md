# barraCuda v0.3.13 — Sprint 56 Stadial Gate Audit Triage

**Date**: 2026-05-11
**Version**: 0.3.13 (Sprint 56)
**Responding to**: primalSpring full stadial gate blurb (May 11, 2026)

---

## Item: Crypto dedup — `chacha20poly1305`/`hkdf`/`hmac` in barracuda-core (LOW)

**Audit claim**: "barracuda-core directly depends on chacha20poly1305, hkdf, hmac
for BTSP framing. Ecosystem pattern is to delegate crypto to bearDog IPC. This
creates duplicate crypto paths and version skew."

**Triage**: Acknowledged as **valid long-term debt, not actionable today**. Delegation
to bearDog IPC would introduce per-frame latency that is architecturally incompatible
with BTSP's wire framing requirements. This is a design constraint, not an oversight.

### Why IPC delegation doesn't work for BTSP framing

barraCuda's crypto usage is exclusively in the **BTSP transport layer** — the hot
path that processes every encrypted frame on every connection:

| File | Crate | Usage |
|------|-------|-------|
| `btsp_frame.rs` | `chacha20poly1305`, `hmac`, `sha2` | Per-frame AEAD encrypt/decrypt + HMAC tag verification |
| `btsp.rs` | `hkdf`, `sha2` | One-shot HKDF key derivation during `btsp.negotiate` |

**Per-frame AEAD** (`BtspFrameReader::read_frame`, `BtspFrameWriter::write_frame`):
Every JSON-RPC message over an encrypted BTSP connection passes through
ChaCha20-Poly1305 encrypt or decrypt. A round-trip IPC call to bearDog per frame
would add ~200-500μs of latency to every single RPC message, defeating the purpose
of the framing layer. This is the same reason every TLS library embeds its own
crypto rather than delegating to an external process.

**One-shot HKDF** (`handle_btsp_negotiate`): Key derivation happens once per
connection during Phase 3 negotiate. This *could* be delegated to bearDog IPC
without performance impact, but it's a single call site using 4 lines of code —
the savings from eliminating `hkdf` don't justify the added IPC complexity and
bearDog availability dependency during connection setup.

### Version alignment

All 4 crypto crates use RustCrypto ecosystem versions that are consistent across
the barraCuda workspace and aligned with the ecosystem standard:

| Crate | Version | Ecosystem standard |
|-------|---------|-------------------|
| `chacha20poly1305` | 0.10 | RustCrypto AEAD |
| `hkdf` | 0.12 | RustCrypto KDF |
| `hmac` | 0.12 | RustCrypto MAC |
| `sha2` | 0.10 | RustCrypto digest |

These are the same versions used by bearDog, rhizoCrypt, and other BTSP-implementing
primals. Version skew is between primals using different RustCrypto generations, not
between barraCuda's embedded crypto and bearDog's.

### Path forward

The correct dedup path is **not** IPC delegation, but rather:

1. **Shared `btsp-crypto` crate** (ecosystem-level): Extract the BTSP framing crypto
   into a shared crate that all BTSP-implementing primals depend on. This eliminates
   version skew at the source while keeping the hot-path crypto in-process.

2. **bearDog IPC for key management only**: bearDog's `crypto.*` surface is appropriate
   for key provisioning, signing, and token operations — not for per-frame symmetric
   crypto. The `FAMILY_SEED` and session key provisioning already goes through bearDog.

**Recommendation**: Mark as LOW/DEFERRED — no action until ecosystem-level `btsp-crypto`
crate extraction is planned. Per-frame IPC crypto delegation is architecturally unsound.

---

## Summary

| Audit Item | Severity | Status | Action |
|------------|----------|--------|--------|
| Crypto dedup (chacha20poly1305/hkdf/hmac) | LOW | ACKNOWLEDGED | Deferred — per-frame IPC delegation adds latency; correct path is shared `btsp-crypto` crate |

**Note**: This is barraCuda's only open item from the full stadial gate audit.
All other barraCuda items (BC-01 through BC-08, GAP-11, JH-0, BTSP Phase 3,
`unwrap()` false positive, optional dep pattern) are RESOLVED. 71 methods,
`#![forbid(unsafe_code)]`, `clippy::unwrap_used` enforced, all quality gates green.
