# sweetGrass v0.7.6 — redb Migration Handoff (March 14, 2026)

**Date**: March 14, 2026
**Type**: Storage Evolution — sled → redb
**Primal**: sweetGrass (Attribution Layer)
**Breaking**: No (additive — new backend, sled still available via feature flag)

---

## Summary

sweetGrass now supports `redb` as a Pure Rust embedded storage backend alongside the existing memory, PostgreSQL, and sled backends. The sled backend is feature-gated behind `--features sled` and no longer compiled by default.

### What Changed

| Component | Change |
|-----------|--------|
| **New crate**: `sweet-grass-store-redb` | Full `BraidStore` implementation against redb 2.4 |
| **Factory**: `BraidStoreFactory` | Supports `STORAGE_BACKEND=redb` from env and config |
| **Service Cargo.toml** | `sweet-grass-store-sled` + `sled` now behind `features = ["sled"]` |
| **Error types** | `RedbError` with full redb error chain conversion |
| **Tests** | 42 new tests covering all BraidStore trait methods, concurrency, corruption |

### redb vs sled

| Property | redb 2.4 | sled 0.34 |
|----------|----------|-----------|
| Pure Rust | Yes | Yes |
| C dependencies | None | None (libc only) |
| Maintained | Active development | Unmaintained since 2022 |
| ACID | Full write transactions | Yes |
| MVCC | Yes (concurrent readers) | Limited |
| Table types | Typed `TableDefinition` | `Tree` of bytes |
| File format | Single `.redb` file | Directory of files |

### Environment Variables

```bash
# Use redb (recommended)
STORAGE_BACKEND=redb
STORAGE_PATH=./data/sweetgrass.redb

# Use sled (requires --features sled at build time)
STORAGE_BACKEND=sled
STORAGE_PATH=./data/sweetgrass
```

### StorageConfig API

```rust
let config = StorageConfig {
    backend: "redb".to_string(),
    redb_path: Some("/path/to/sweetgrass.redb".to_string()),
    ..StorageConfig::default()
};
let store = BraidStoreFactory::from_config(&config).await?;
```

---

## Table Structure (redb)

| Table | Key | Value |
|-------|-----|-------|
| `braids` | `braid_id` bytes | JSON-serialized Braid |
| `by_hash` | content hash bytes | braid_id bytes |
| `by_agent` | `agent_did:braid_id` bytes | braid_id bytes |
| `by_time` | `{:020}:braid_id` bytes | braid_id bytes |
| `by_tag` | `tag:braid_id` bytes | braid_id bytes |
| `activities` | `activity_id` bytes | JSON-serialized Activity |

All tables use `TableDefinition<&[u8], &[u8]>` — same pattern as rhizoCrypt.

---

## Migration Path for Consumers

### biomeOS

No action needed — biomeOS communicates with sweetGrass via JSON-RPC/tarpc, not direct storage access. The storage backend is an internal implementation detail.

### Deployments

Existing sled data is **not** automatically migrated. To migrate:
1. Export braids via `braid.query` JSON-RPC method
2. Switch `STORAGE_BACKEND=redb`
3. Re-import braids via `braid.create`

Or run both backends in parallel during transition.

### Build with sled support

```bash
cargo build -p sweet-grass-service --features sled
```

---

## Ecosystem Pattern

This follows rhizoCrypt's proven redb migration pattern:
- **rhizoCrypt**: redb default since v0.12
- **LoamSpine**: redb default, sled optional via `sled-storage` feature
- **sweetGrass**: redb supported, sled feature-gated

**Next candidates**: Songbird (orchestrator, tor-protocol), BearDog (workspace crates).

---

*Handoff complete. See `ECOSYSTEM_PURE_RUST_EVOLUTION_HANDOFF_MAR14_2026.md` for full ecosystem status.*
