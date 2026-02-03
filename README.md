# 💧 The Watering Hole - ecoPrimal Knowledge Hub

**Purpose**: Central repository for cross-primal documentation, standards, and shared knowledge  
**Audience**: All primals in the ecosystem  
**Last Updated**: February 3, 2026

---

## 🎯 What is the Watering Hole?

The Watering Hole is where **all primals come to learn, share, and align**. Just like animals gather at a watering hole in nature, our primals gather here to:

- **Learn** about other primals' capabilities and APIs
- **Share** technical specifications and protocols
- **Align** on shared goals and standards
- **Reference** authoritative documentation

**Key Principle**: Any primal can read and contribute to the Watering Hole.

---

## 🏆 Current Ecosystem Status (Feb 3, 2026)

### NUCLEUS Architecture OPERATIONAL ✅

| Metric | Value |
|--------|-------|
| **TLS 1.3 Validation** | 93% (81/87 sites) |
| **Pure Rust** | 100% (all 6 primals) |
| **Platform Coverage** | Universal (x86_64, aarch64, Android) |
| **Deployment Standard** | v1.0 (deterministic) |

### ecoBin Status

| Primal | ecoBin | IPC | Notes |
|--------|--------|-----|-------|
| **BearDog** | ✅ v2.0 | Isomorphic | Reference implementation |
| **Songbird** | ✅ v2.0 | Isomorphic | Pure Rust TLS 1.3 |
| **Toadstool** | ✅ v2.0 | Isomorphic | Compute orchestration |
| **Squirrel** | ✅ v2.0 | Universal | AI via Tower Atomic |
| **NestGate** | ⚠️ Partial | Isomorphic | Needs socket-only default |
| **biomeOS** | ✅ v2.0 | Neural API | Graph-based deployment |

**5/6 primals fully compliant** - See [`biomeOS/docs/handoffs/PRIMAL_EVOLUTION_STATUS_FEB03_2026.md`](../phase2/biomeOS/docs/handoffs/PRIMAL_EVOLUTION_STATUS_FEB03_2026.md)

---

## 📚 Knowledge Areas

### 🏗️ Architecture Standards

#### **UniBin Architecture** (Structure Standard)

**Location**: `UNIBIN_ARCHITECTURE_STANDARD.md`

**What**: Single binary per primal with multiple operational modes

**Status**: ✅ Ecosystem Standard (Adopted Jan 16, 2026)

---

#### **ecoBin Architecture** (Pure Rust + Portability Standard)

**Location**: `ECOBIN_ARCHITECTURE_STANDARD.md`

**What**: UniBin + 100% Pure Rust = Universal cross-compilation

**Key Concepts**:
- ✅ Zero APPLICATION C dependencies
- ✅ Pure Rust crypto (RustCrypto suite)
- ✅ Cross-compile to ANY target
- ✅ Tower Atomic for HTTP/TLS

**Status**: ✅ Ecosystem Standard (5/5 core primals compliant)

---

#### **Primal IPC Protocol** (Communication Standard)

**Location**: `PRIMAL_IPC_PROTOCOL.md`

**What**: JSON-RPC 2.0 over Unix sockets for inter-primal communication

**Key Concepts**:
- ✅ Capability-based discovery
- ✅ Zero cross-embedding
- ✅ Platform universal (tokio)

**Status**: ✅ Ecosystem Standard

---

#### **Primal Deployment Standard** (Deployment Standard) - NEW

**Location**: [`biomeOS/specs/PRIMAL_DEPLOYMENT_STANDARD.md`](../phase2/biomeOS/specs/PRIMAL_DEPLOYMENT_STANDARD.md)

**What**: Deterministic primal behavior across all architectures

**Key Concepts**:
- ✅ 5-tier socket path resolution
- ✅ Same behavior on x86_64 and aarch64
- ✅ Unix sockets first, TCP fallback
- ✅ No HTTP by default (socket-only)

**Socket Resolution Order**:
```
1. $PRIMAL_SOCKET           (explicit override)
2. $XDG_RUNTIME_DIR/biomeos/
3. /run/user/$UID/biomeos/
4. /data/local/tmp/biomeos/  (Android)
5. /tmp/biomeos/             (fallback)
```

**Status**: ✅ Ecosystem Standard (v1.0 - Feb 3, 2026)

---

#### **Semantic Method Naming** (API Evolution Standard)

**Location**: `SEMANTIC_METHOD_NAMING_STANDARD.md`

**What**: Method names describe WHAT (semantic intent), not HOW (implementation)

**Key Concepts**:
- ✅ Domain namespaces (`crypto.*`, `tls.*`, `http.*`)
- ✅ Neural API translation layer
- ✅ Isomorphic evolution

**Status**: ✅ Ecosystem Standard (v2.0.0)

---

### 🐻 BTSP (BearDog Technical Stack)

**Location**: `btsp/BEARDOG_TECHNICAL_STACK.md`

**What**: BearDog is the genetic lineage keeper and cryptographic foundation

**Current Status**: ✅ Production Ready
- SHA-384 support complete
- TLS 1.3 cipher suites (0x1301, 0x1302, 0x1303)
- Pure Rust (RustCrypto suite)

---

### 🎵 BirdSong Protocol

**Location**: `birdsong/BIRDSONG_PROTOCOL.md`

**What**: Encrypted UDP discovery protocol for auto-trust within genetic lineages

**Status**: ✅ Production Ready (v2.0)

---

### 🐦 Songbird TLS Integration

**Location**: `SONGBIRD_TLS_TOWER_ATOMIC_INTEGRATION_GUIDE.md`

**What**: Guide for Tower Atomic Pure Rust TLS 1.3

**Current Status**: ✅ 93% TLS Validation
- Pure Rust TLS 1.3
- Chunked encoding support
- Adaptive HTTP with User-Agent
- 87 sites validated

---

### 🌸 PetalTongue (UI Primal)

**Location**: `petaltongue/`

**What**: Multi-modal visualization primal

**Key Docs**:
- `PETALTONGUE_SHOWCASE_LESSONS_LEARNED.md` - TRUE PRIMAL patterns
- `BIOMEOS_INTEGRATION_HANDOFF.md` - Integration guide

---

## 🎓 Quick Reference

### I want to...

| Task | Document |
|------|----------|
| **Understand binary architecture** | `UNIBIN_ARCHITECTURE_STANDARD.md` |
| **Achieve ecoBin compliance** | `ECOBIN_ARCHITECTURE_STANDARD.md` |
| **Implement IPC** | `PRIMAL_IPC_PROTOCOL.md` |
| **Deploy across platforms** | `biomeOS/specs/PRIMAL_DEPLOYMENT_STANDARD.md` |
| **Name methods correctly** | `SEMANTIC_METHOD_NAMING_STANDARD.md` |
| **Integrate TLS** | `SONGBIRD_TLS_TOWER_ATOMIC_INTEGRATION_GUIDE.md` |
| **Use BearDog crypto** | `btsp/BEARDOG_TECHNICAL_STACK.md` |
| **Understand evolution path** | `biomeOS/specs/EVOLUTION_PATH.md` |

---

## 📊 Documentation Status

| Knowledge Area | Status | Last Updated | Coverage |
|----------------|--------|--------------|----------|
| UniBin Architecture | ✅ Complete | Jan 16, 2026 | 100% |
| ecoBin Architecture | ✅ Complete | Jan 30, 2026 | 100% |
| Primal IPC Protocol | ✅ Complete | Jan 19, 2026 | 100% |
| **Deployment Standard** | ✅ Complete | Feb 3, 2026 | 100% |
| **Evolution Path** | ✅ Complete | Feb 3, 2026 | 100% |
| Semantic Naming | ✅ Complete | Jan 25, 2026 | 100% |
| BTSP (BearDog) | ✅ Complete | Jan 26, 2026 | 100% |
| BirdSong Protocol | ✅ Complete | Feb 2, 2026 | 100% |
| Songbird TLS | ✅ Complete | Jan 26, 2026 | 100% |
| PetalTongue | ✅ Complete | Jan 3, 2026 | 100% |

---

## 🌟 Core Concepts

### Genetic Lineage

**Definition**: A group of primals that share a common `family_seed`, enabling cryptographic auto-trust.

### Auto-Trust

**Definition**: Automatic trust establishment between primals of the same genetic lineage, without manual configuration.

### Tower Atomic

**Definition**: BearDog (crypto) + Songbird (HTTP/TLS) = Pure Rust HTTPS

```
External HTTPS → Songbird (TLS 1.3) → BearDog (crypto) → Pure Rust
```

### capability.call

**Definition**: Neural API semantic routing that enables primals to communicate without knowing each other's APIs.

```
Squirrel → capability.call("crypto", "sha256") → Neural API → BearDog
```

---

## 🔐 Security Principles

### 1. Secure by Default
- Family seeds never logged
- Encryption required for discovery
- Auto-zeroization of sensitive data

### 2. Pure Rust Only
- Zero C dependencies in application code
- RustCrypto suite for all crypto
- Memory safety guaranteed

### 3. Zero Trust (Outside Family)
- No trust without family membership
- Encrypted payloads unreadable to outsiders
- Continuous validation

### 4. Auto-Trust (Within Family)
- Shared genetic lineage enables trust
- Decryption proves family membership
- No manual configuration needed

---

## 🚀 Current Ecosystem Status

### Production Ready ✅

- **Tower Atomic** - 93% TLS validation (81/87 sites)
- **BearDog** - All cipher suites (0x1301, 0x1302, 0x1303)
- **Songbird** - Pure Rust TLS 1.3 + HTTP
- **biomeOS** - Graph-based deployment + capability.call
- **Neural API** - Semantic translation layer

### In Progress ⏳

- Songbird TLS 1.2 fallback (npm, Jenkins)
- Terraria testing system
- Apoptosis graceful shutdown

---

## 📖 Quick Navigation

### By Standard
- **UniBin** → `UNIBIN_ARCHITECTURE_STANDARD.md`
- **ecoBin** → `ECOBIN_ARCHITECTURE_STANDARD.md`
- **IPC Protocol** → `PRIMAL_IPC_PROTOCOL.md`
- **Semantic Naming** → `SEMANTIC_METHOD_NAMING_STANDARD.md`
- **genomeBin** → `GENOMEBIN_ARCHITECTURE_STANDARD.md`

### By Primal
- **BearDog** → `btsp/BEARDOG_TECHNICAL_STACK.md`
- **Songbird** → `SONGBIRD_TLS_TOWER_ATOMIC_INTEGRATION_GUIDE.md`
- **PetalTongue** → `petaltongue/`
- **biomeOS** → `../biomeOS/START_HERE.md`

---

## 💡 Contributing to the Watering Hole

### Adding Documentation

1. Create a new knowledge area (e.g., `songbird/`)
2. Write comprehensive docs following existing patterns
3. Update this README with links and status
4. Test all examples before committing

### Documentation Standards

- **Comprehensive**: Cover all aspects
- **Practical**: Include runnable examples
- **Current**: Keep up-to-date with implementations
- **Clear**: Write for cross-primal audience
- **Honest**: Document gaps and technical debt

---

## 📁 Archive

Historical documents are preserved in `archive/`:
- `archive/songbird_jan_2026/` - Old Songbird status files

---

**Status**: 🎊 **PRODUCTION READY** - Tower Atomic 93% TLS Validated  
**Coverage**: All standards complete (100%)  
**Pure Rust**: 5/5 core primals ecoBin compliant

💧 **Welcome to the Watering Hole - Where Primals Gather to Learn and Grow** 🌸

---

*The Watering Hole is maintained by all primals. Contributions welcome!*
