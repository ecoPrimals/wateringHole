# sporeGate Full Harvest — Wave 141b

**Date**: Jul 15, 2026 | **Wave**: 141b | **From**: eastGate overwatch
**To**: sporeGate builder team
**Priority**: P0 — all 14 primals have adopted cross-architecture support

---

## Directive

All 14 primals now have `#[cfg()]`-gated platform code and cross-architecture
adoption complete. Execute a full harvest across all depot architectures and
validate on real hardware where available.

## Phase 1: Windows Harvest (P0)

```bash
# On sporeGate, for each primal workspace:
membrane plasmid.harvest --target x86_64-pc-windows-gnu --local
```

**Expected result**: 14/14 Windows binaries (up from 1/14 songbird.exe).

Known expected failures:
- toadStool: `hw-safe` feature-gated behind `linux-hw` — may produce stub binary
- petalTongue: Android cdylib target, Windows binary may be headless-only

After harvest, push to VPS depot:
```bash
membrane plasmid.depot_sync --push
```

## Phase 2: Android Re-Harvest (P1)

Several primals had cross-arch changes that may improve Android results:
```bash
membrane plasmid.harvest --target aarch64-linux-android --local
```

**Current**: 12/14. Check if petalTongue or toadStool improved.

## Phase 3: Exotic Architecture Expansion (P2)

With all primals cross-arch adopted, try RISC-V and ARMv7 for all primals
(not just songBird):

```bash
# RISC-V (open silicon — strategic)
for primal in songBird bearDog nestGate ...; do
  cargo check --target riscv64gc-unknown-linux-gnu --manifest-path $primal/Cargo.toml
done

# ARMv7 (Raspberry Pi / IoT)
for primal in songBird bearDog nestGate ...; do
  cargo check --target armv7-unknown-linux-gnueabihf --manifest-path $primal/Cargo.toml
done
```

Add passing architectures to the depot.

## Phase 4: portable-atomic (P1)

Enable `tokio` `portable-atomic` feature in all workspace `Cargo.toml` files:

```toml
[dependencies]
tokio = { version = "1", features = ["full", "portable-atomic"] }
```

Then test PPC32:
```bash
cargo check --target powerpc-unknown-linux-gnu
```

## Phase 5: Cross-Platform E2E Validation

After binaries are built, deploy and test on real hardware:

| Target | Hardware | Test |
|--------|----------|------|
| x86_64-windows-gnu | northGate (Windows, RTX 5090) | songbird.exe mesh enrollment, IPC via NamedPipe |
| aarch64-android | grapheneGate (Pixel 8) | Termux deploy, StrongBox interaction |
| x86_64-linux-musl | golgi (VPS) | Full NUCLEUS, depot serving, sporePrint |
| aarch64-linux-musl | sporeGate (if ARM board available) | Cross-compile validation |

### UDS vs NamedPipe vs TCP Validation Matrix

| Subsystem | Linux (UDS) | Windows (NamedPipe) | Android (TCP fallback) |
|-----------|------------|--------------------|-----------------------|
| Primal-to-primal IPC | `UnixStream` | `NamedPipeClient` | `TcpStream` |
| biomeOS Neural API | tarpc unix | tarpc TCP | tarpc TCP |
| Service lifecycle | systemd | Windows SCM | Termux init |
| Socket discovery | `/run/membrane/*.sock` | `\\.\pipe\primal-*` | `127.0.0.1:PORT` |
| Credential store | fs-based (0600) | DPAPI (future) | Android Keystore |

**Key validation**: primal A on Linux talks to primal B on Windows via songBird
mesh. The transport layer dispatches correctly based on platform.

---

## Success Criteria

```
Windows harvest:   14/14 binaries built (or documented expected-fail)
Android harvest:   14/14 binaries built (or documented expected-fail)
Depot sync:        All binaries pushed to golgi VPS depot
BLAKE3+Ed25519:    All binaries signed
northGate test:    songbird.exe running, mesh enrolled
primalSpring:      full-cross-compile scenario GREEN
```

---

*Wave 141b: All 14 primals cross-arch adopted. Execute full harvest.
Test on real hardware. Validate transport dispatch across platforms.*
