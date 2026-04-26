# UniBin Architecture - Ecosystem Standard

**Status**: 🌟 **ECOSYSTEM STANDARD** 🌟  
**Adopted**: January 16, 2026  
**Authority**: WateringHole Consensus (All Primal Teams)  
**Compliance**: Mandatory for all new primals, recommended for existing  
**Reference Implementation**: NestGate v0.11.0+

---

## 📜 **Standard Declaration**

**UniBin Architecture** is hereby adopted as the official ecosystem standard for all ecoPrimals binaries. This standard eliminates binary naming fragility, improves deployment robustness, and establishes a consistent, professional user experience across the entire ecosystem.

**All primal teams** are expected to adopt this standard for new developments and evolve existing binaries to comply.

---

## 🎯 **Core Principle**

### **One Binary Per Primal, Multiple Modes**

Each primal SHALL provide a **single executable binary** that accepts **subcommands** to determine its operational mode.

**Pattern**:
```bash
<primal> <mode> [options]
```

**NOT This** (deprecated pattern):
```bash
<primal>-server    # ❌ Multiple binaries per primal
<primal>-client    # ❌ Variant naming
<primal>-daemon    # ❌ Deployment fragility
```

---

## ✅ **Standard Requirements**

### **1. Binary Naming** (MANDATORY)

**Rule**: Binary MUST be named after the primal, without suffixes.

**Examples**:
- ✅ `beardog` (not `beardog-server`)
- ✅ `songbird` (not `songbird-orchestrator`)
- ✅ `toadstool` (not `toadstool-server`)
- ✅ `nestgate` ✨ (reference implementation)
- ✅ `squirrel` (correct!)

**Rationale**: 
- Eliminates naming confusion
- Makes deployment graphs robust
- Professional UX (like `kubectl`, `docker`, `cargo`)

---

### **2. Subcommand Structure** (MANDATORY)

**Rule**: Binary MUST support subcommands for different operational modes.

**Minimum Required Modes**:
- `server` or `service`: Long-running service mode
- `--help`: Show all available modes and options
- `--version`: Show version information

**Common Optional Modes**:
- `client`: Client interaction mode
- `daemon`: Background daemon mode (alias for `server` is acceptable)
- `cli`: Interactive CLI mode
- `doctor`: Health check/diagnostics
- Custom modes as needed

**Example**:
```bash
nestgate --help           # Show all commands
nestgate service start    # Start service mode
nestgate doctor          # Health diagnostics
```

### **2a. Server `--port` Convention** (MANDATORY, v1.1)

**Rule**: The `server` subcommand MUST accept `--port <PORT>` to bind a TCP
JSON-RPC listener using newline-delimited framing (see `PRIMAL_IPC_PROTOCOL.md`
Wire Framing section).

```bash
# This MUST work for every primal
<primal> server --port 9000
```

`--port` is the universal entry point for orchestration. Springs, deploy graphs,
and launchers compose primals by calling `{binary} server --port {port}`. If a
primal uses a different flag name (e.g., `--jsonrpc-port`, `--http-address`,
`--listen`, `--rpc-bind`), it MUST also accept `--port` as an alias.

**Additional transport flags** are acceptable:
```bash
beardog server --port 9000 --uds-path /run/user/1000/biomeos/beardog.sock
sweetgrass server --port 9100 --http-address 127.0.0.1:9101
```

**`daemon` as an alias:** Primals that use `daemon` as their long-running
subcommand SHOULD also accept `server` as an alias for consistency.

### **2b. Standalone Startup** (MANDATORY, v1.1)

**Rule**: Primals MUST start successfully in standalone mode — without other
primals running and without identity environment variables.

When `FAMILY_ID` or `NODE_ID` are not set, the primal MUST default to
`standalone` (or `default`) rather than exit with an error. When Songbird or
Neural API are unreachable, the primal MUST log a warning and continue with
degraded discovery.

The environment variable precedence for identity:
1. `{PRIMAL}_FAMILY_ID` / `{PRIMAL}_NODE_ID` (primal-scoped, highest)
2. `FAMILY_ID` / `NODE_ID` (unscoped fallback)
3. Default `standalone` / hostname (lowest)

This enables local development, spring-driven composition, and incremental
deploy graph bringup.

---

### **3. Help Documentation** (MANDATORY)

**Rule**: Binary MUST provide comprehensive `--help` output.

**Required Help Information**:
- List of all available subcommands
- Brief description of each mode
- Common usage examples
- Version information

**Example Output**:
```bash
$ beardog --help

beardog v0.9.0 - Security & Cryptography Primal

USAGE:
    beardog <SUBCOMMAND>

SUBCOMMANDS:
    server      Start BearDog in server mode
    client      Interact with BearDog server
    daemon      Run as background daemon
    doctor      Run health diagnostics
    help        Print this message

EXAMPLES:
    beardog server --port 9000
    beardog client --endpoint unix:///tmp/beardog.sock
    beardog doctor --comprehensive

For more information on a specific command:
    beardog <subcommand> --help
```

---

### **4. Version Information** (MANDATORY)

**Rule**: Binary MUST support `--version` flag.

**Format**:
```bash
$ beardog --version
beardog 0.9.0
```

**Extended Format** (optional):
```bash
$ beardog --version --verbose
beardog 0.9.0
Build: 2026-01-16T12:00:00Z
Commit: a1b2c3d
Platform: x86_64-unknown-linux-gnu
Rust: 1.75.0
```

---

### **5. Error Messages** (MANDATORY)

**Rule**: Unknown subcommands MUST provide helpful error messages.

**Example**:
```bash
$ beardog foo
error: The subcommand 'foo' wasn't recognized

Usage: beardog <SUBCOMMAND>

For more information try '--help'
```

---

## 🏗️ **Implementation Guide**

### **Using Clap (Recommended)**

**Cargo.toml**:
```toml
[dependencies]
clap = { version = "4.4", features = ["derive"] }
```

**src/main.rs**:
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "beardog")]
#[command(about = "Security & Cryptography Primal", long_about = None)]
#[command(version)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Start BearDog in server mode
    Server {
        /// TCP port for newline-delimited JSON-RPC (REQUIRED by UniBin v1.1)
        #[arg(long, default_value = "9000")]
        port: u16,
        
        #[arg(long)]
        daemon: bool,
    },
    
    /// Interact with BearDog server
    Client {
        #[arg(long, default_value = "unix:///tmp/beardog.sock")]
        endpoint: String,
    },
    
    /// Run health diagnostics
    Doctor {
        #[arg(long)]
        comprehensive: bool,
    },
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Server { port, daemon } => {
            run_server(port, daemon).await?;
        }
        Commands::Client { endpoint } => {
            run_client(&endpoint).await?;
        }
        Commands::Doctor { comprehensive } => {
            run_doctor(comprehensive).await?;
        }
    }
    
    Ok(())
}
```

---

### **Cargo Configuration**

**Single Binary Definition**:
```toml
[[bin]]
name = "beardog"  # UniBin name (no suffix!)
path = "src/main.rs"
```

**NOT This** (old pattern):
```toml
[[bin]]
name = "beardog-server"  # ❌ Deprecated!
path = "src/bin/server.rs"

[[bin]]
name = "beardog-client"  # ❌ Deprecated!
path = "src/bin/client.rs"
```

---

## 📋 **Deployment Integration**

### **Graph Configuration**

**UniBin-Aware Graph** (biomeOS pattern):
```toml
[[nodes]]
id = "launch_beardog"
node_type = "primal.launch"

[nodes.config]
primal_name = "beardog"           # Logical name
binary_path = "plasmidBin/primals/beardog"  # UniBin path
mode = "server"                   # What to run
args = ["server", "--daemon"]     # How to run
family_id = "nat0"
socket_path = "/tmp/beardog-nat0.sock"
```

**Benefits**:
- Graph specifies WHAT to do (mode)
- Not WHICH binary variant to use
- Robust to binary renames
- Self-documenting

---

## 🌟 **Reference Implementation: NestGate**

**Status**: ✅ **FULLY UniBin COMPLIANT**

**Example Usage**:
```bash
# Show help
$ nestgate --help
🏠 NestGate - Sovereign Storage System
...

# Start service
$ nestgate service start --port 8080

# Health check
$ nestgate doctor --comprehensive

# Configure storage
$ nestgate storage configure --backend filesystem
```

**Why NestGate is the Reference**:
- ✅ Single binary (`nestgate`)
- ✅ Multiple subcommands (`service`, `doctor`, `storage`)
- ✅ Comprehensive `--help`
- ✅ Clear error messages
- ✅ Self-documenting CLI
- ✅ Professional UX

**All primals should follow NestGate's pattern!**

---

## 📊 **Ecosystem Compliance Status**

### **Compliant** ✅

| Primal | Status | Notes |
|--------|--------|-------|
| **BearDog** | ✅ UniBin name + clap 4 CLI | `beardog server --listen`. Missing: `--port` alias, standalone startup. |
| **Songbird** | ✅ UniBin name + subcommands | `songbird server --port`. Missing: `--dark-forest` CLI flag. |
| **Squirrel** | ✅ UniBin name + subcommands | `squirrel server`. Uses `--port + --bind` (should converge to `--listen`). |
| **ToadStool** | ✅ UniBin name + subcommands | `toadstool server --port`. `--port` flag not wired to implementation. |

### **Blocked** ❌

| Primal | Binary | Issue | Priority |
|--------|--------|-------|----------|
| **NestGate** | `nestgate` | musl-static binary **segfaults** (exit 139) on `--help`. glibc build works with full clap 4 CLI. ecoBin non-compliant until musl is fixed. `--port` non-functional. `daemon` subcommand (not `server`). | P0 |

### **Partial** ⏳

| Primal | Binary | Status | Notes |
|--------|--------|--------|-------|
| **NestGate** | `nestgate` (glibc only) | Structurally UniBin, functionally blocked | Subcommand is `daemon` not `server`. `--port` not wired. Reference implementation claim invalid until musl fixed. |

---

## 🚀 **Migration Path**

### **For Existing Primals**

**Phase 1: Assessment** (1 week)
- Review current binary structure
- Identify modes/variants
- Plan UniBin structure
- Estimate effort

**Phase 2: Implementation** (1-2 weeks)
- Restructure to single binary
- Implement subcommand structure (clap)
- Update help documentation
- Add comprehensive tests

**Phase 3: Testing** (1 week)
- Test all modes
- Verify backward compatibility (if needed)
- Update deployment scripts
- Update documentation

**Phase 4: Deployment** (1 week)
- Rebuild and harvest UniBin
- Update deployment graphs
- Deploy to testing
- Roll out to production

**Total Timeline**: 4-6 weeks per primal

---

### **For New Primals**

**Requirement**: MUST implement UniBin from day one.

**Checklist**:
- [ ] Single binary named after primal
- [ ] Subcommand structure using clap
- [ ] `--help` output comprehensive
- [ ] `--version` implemented
- [ ] At least `server` mode
- [ ] Error messages helpful
- [ ] Documentation includes CLI examples
- [ ] Deployment graphs use UniBin pattern

---

## 💡 **Best Practices**

### **1. Subcommand Naming**

**Prefer standard names**:
- ✅ `server` (not `run`, `start`, `serve`)
- ✅ `client` (not `connect`, `cli`)
- ✅ `daemon` (not `background`, `service`)
- ✅ `doctor` (for health checks)

**Be consistent with ecosystem**!

---

### **2. Configuration Hierarchy**

**Standard Priority Order**:
1. Command-line arguments (highest)
2. Environment variables
3. Configuration file
4. Defaults (lowest)

**Example**:
```bash
# CLI arg overrides env var
BEARDOG_PORT=8000 beardog server --port 9000  # Uses 9000
```

---

### **3. Logging and Diagnostics**

**All modes should**:
- Use structured logging (tracing)
- Include version in startup logs
- Log mode at startup
- Support `RUST_LOG` for verbosity

**Example**:
```
2026-01-16T12:00:00Z  INFO beardog v0.9.0
2026-01-16T12:00:00Z  INFO Mode: server (daemon: false)
2026-01-16T12:00:00Z  INFO Socket: /tmp/beardog-nat0.sock
```

---

### **4. Exit Codes**

**Standard Exit Codes**:
- `0`: Success
- `1`: General error
- `2`: Configuration error
- `3`: Network error
- `130`: Interrupted (Ctrl+C)

---

### **5. Signal Handling**

**All server modes MUST**:
- Handle `SIGTERM` gracefully
- Handle `SIGINT` (Ctrl+C) gracefully
- Log shutdown reason
- Clean up resources (sockets, etc.)

**Example**:
```rust
async fn run_server() -> Result<()> {
    let shutdown = signal::ctrl_c();
    
    tokio::select! {
        _ = shutdown => {
            info!("Received shutdown signal, cleaning up...");
            // Cleanup
        }
    }
    
    Ok(())
}
```

---

## 🎓 **Examples**

### **Minimal UniBin**

**Cargo.toml**:
```toml
[package]
name = "myprimal"
version = "0.1.0"

[[bin]]
name = "myprimal"
path = "src/main.rs"

[dependencies]
clap = { version = "4.4", features = ["derive"] }
```

**src/main.rs**:
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(version)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Start server mode
    Server,
}

fn main() {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Server => println!("Running server..."),
    }
}
```

**Usage**:
```bash
$ myprimal --version
myprimal 0.1.0

$ myprimal --help
Usage: myprimal <SUBCOMMAND>

Subcommands:
  server  Start server mode
  help    Print this message

$ myprimal server
Running server...
```

---

### **Full UniBin Example**

See biomeOS `UNIBIN_DEBT_ELIMINATION_JAN_16_2026.md` for comprehensive implementation guide.

---

## 🏆 **Benefits**

### **For Operators**

- ✅ Consistent CLI across all primals
- ✅ Self-documenting (`--help`)
- ✅ Professional UX (like kubectl, docker)
- ✅ Easy to learn and remember

### **For Developers**

- ✅ Single binary to maintain
- ✅ Simpler build process
- ✅ Easier testing (one binary, multiple modes)
- ✅ Standard patterns (clap)

### **For Deployment**

- ✅ Robust graphs (mode-based, not name-based)
- ✅ No binary naming confusion
- ✅ Easier maintenance
- ✅ Better error messages

### **For Ecosystem**

- ✅ Consistent architecture
- ✅ Professional image
- ✅ Easier onboarding
- ✅ Reduced technical debt

---

## 📚 **Resources**

### **Documentation**

- **biomeOS Implementation**: `/ecoPrimals/phase2/biomeOS/UNIBIN_DEBT_ELIMINATION_JAN_16_2026.md`
- **UniBin Graph**: `/ecoPrimals/phase2/biomeOS/graphs/02_nucleus_enclave_unibin.toml`
- **Clap Documentation**: https://docs.rs/clap/

### **Reference Code**

- **NestGate**: `/ecoPrimals/phase1/nestgate/` (reference implementation)
- **biomeOS**: `/ecoPrimals/phase2/biomeOS/` (UniBin-aware orchestration)

---

## 🎯 **Compliance & Review**

### **Compliance Checklist**

Before declaring a primal UniBin-compliant:

- [ ] Single binary named after primal (no suffixes)
- [ ] Subcommand structure implemented (clap recommended)
- [ ] `--help` shows all modes with descriptions
- [ ] `--version` implemented
- [ ] At least `server` or `service` mode exists
- [ ] `server --port <PORT>` binds newline-delimited TCP JSON-RPC (v1.1)
- [ ] Starts in standalone mode without `FAMILY_ID` / `NODE_ID` (v1.1)
- [ ] musl-static binary works identically to glibc build (v1.2)
- [ ] No writes to CWD — audit/PID paths configurable via flags or env (v1.2)
- [ ] `--abstract` flag supported for Android/SELinux substrates (v1.2, if Unix sockets used)
- [ ] Error messages helpful and actionable
- [ ] Logging includes mode and version
- [ ] Signal handling (graceful shutdown)
- [ ] Documentation updated with CLI examples
- [ ] Deployment graphs updated to use UniBin pattern
- [ ] Tests cover all modes
- [ ] Old binary variants removed (if applicable)

### **Review Process**

**Self-Assessment**: Use checklist above  
**Peer Review**: Request review from another primal team  
**WateringHole Consensus**: Present at inter-primal meeting  
**Final Approval**: Document compliance in this file

---

## 🔄 **Version History**

### **v1.1.0** (March 25, 2026)

**Server Port Convention & Standalone Startup**

**Author**: wateringHole (driven by esotericWebb live composition)

**Changes**:
- `server --port <PORT>` is now MANDATORY for orchestrator compatibility
- Standalone startup is MANDATORY (no hard-fail on missing identity env vars)
- Environment variable precedence defined for `FAMILY_ID` / `NODE_ID`
- `daemon` recognized as acceptable alias for `server`
- Compliance checklist updated

**Rationale**:
- Springs and launchers compose primals via `{binary} server --port {port}` — inconsistent flags break composition
- Primals that hard-fail without `FAMILY_ID` break local development and incremental bringup
- Discovered during esotericWebb's first live multi-primal composition

### **v1.2.0** (March 27, 2026)

**Cross-Substrate Deployment & CLI Convergence**

**Author**: wateringHole (driven by plasmidBin cross-hardware deployment testing)

**Changes**:
- `--listen addr:port` is RECOMMENDED as the canonical TCP bind flag (BearDog pattern). `--port` remains MANDATORY per v1.1; `--listen` provides the full `addr:port` form for deployment scripts.
- **Substrate-aware output paths**: Primals MUST NOT assume CWD is writable. Audit logs, PID files, and runtime data SHOULD be configurable via `--audit-dir`, `--pid-dir`, or environment variables (`{PRIMAL}_AUDIT_DIR`, `{PRIMAL}_PID_DIR`). Default: `$XDG_RUNTIME_DIR/biomeos/` on Linux, `$TMPDIR` on Android.
- **Abstract socket support**: Primals that create Unix sockets SHOULD accept `--abstract` to use Linux abstract namespace sockets (prefix `\0` on `AF_UNIX`). Required for Android/SELinux substrates.
- **musl-static compliance**: ecoBin requires musl-static cross-compilation. The UniBin binary MUST function identically under both glibc and musl libc. Segfaults, panics, or behavioral differences under musl constitute a compliance failure.
- NestGate reference implementation status revoked until musl segfault is resolved.
- Compliance table updated with live deployment results.

**Rationale**:
- Live deployment to Pixel/GrapheneOS (aarch64, Android) revealed primals writing to CWD (crash), using non-abstract sockets (SELinux block), and CLI inconsistency as the #1 deployment friction
- NestGate musl segfault (exit 139) discovered during plasmidBin binary validation
- Deploy scripts (`deploy_gate.sh`, `deploy_pixel.sh`, `bootstrap_gate.sh`) maintain 60+ line per-primal case blocks due to CLI divergence

### **v1.1.0** (March 25, 2026)

**Server Port Convention & Standalone Startup**

**Author**: wateringHole (driven by esotericWebb live composition)

**Changes**:
- `server --port <PORT>` is now MANDATORY for orchestrator compatibility
- Standalone startup is MANDATORY (no hard-fail on missing identity env vars)
- Environment variable precedence defined for `FAMILY_ID` / `NODE_ID`
- `daemon` recognized as acceptable alias for `server`
- Compliance checklist updated

**Rationale**:
- Springs and launchers compose primals via `{binary} server --port {port}` — inconsistent flags break composition
- Primals that hard-fail without `FAMILY_ID` break local development and incremental bringup
- Discovered during esotericWebb's first live multi-primal composition

### **v1.0.0** (January 16, 2026)

**Initial Standard Adoption**

**Author**: biomeOS Team  
**Consensus**: WateringHole (All Primal Teams)

**Changes**:
- Established UniBin as ecosystem standard
- Defined mandatory requirements
- Documented implementation guide
- Identified reference implementation (NestGate)
- Created migration path for existing primals

**Rationale**: 
- Eliminate recurrent binary naming issues
- Improve deployment robustness
- Establish professional, consistent UX
- Reduce technical debt across ecosystem

---

## 📞 **Support & Questions**

### **Where to Ask**

- **WateringHole**: Inter-primal discussions
- **biomeOS**: Technical implementation questions
- **NestGate Team**: Reference implementation questions

### **Common Questions**

**Q: Do I have to migrate existing binaries?**  
A: Mandatory for new primals, strongly recommended for existing. Migration path provided.

**Q: Can I use something other than clap?**  
A: Yes, but clap is recommended for consistency. Must still meet all requirements.

**Q: What if my primal only needs one mode?**  
A: Still use UniBin pattern! Single mode is fine, but structure should support future modes.

**Q: How do I handle backward compatibility?**  
A: Symlinks or wrapper scripts can provide transition period. Document clearly.

**Q: Can I have primal-specific subcommands?**  
A: Yes! Standard only requires minimum modes. Add domain-specific commands as needed.

---

## 🎊 **Conclusion**

**UniBin Architecture** is now the **official ecosystem standard** for all ecoPrimals binaries.

**This standard**:
- ✅ Eliminates technical debt
- ✅ Improves user experience
- ✅ Establishes professional patterns
- ✅ Reduces maintenance burden
- ✅ Makes deployment robust

**Compliance is expected** from all primal teams for new developments.

**Together, we build a consistent, professional, maintainable ecosystem!**

---

**Standard**: UniBin Architecture v1.2.0  
**Adopted**: January 16, 2026  
**Updated**: March 27, 2026  
**Authority**: WateringHole Consensus  
**Status**: 🌟 **ACTIVE ECOSYSTEM STANDARD** 🌟

---

🦀🧬✨ **UniBin Architecture - One Binary, Infinite Possibilities!** ✨🧬🦀

**Consistent | Robust | Professional | Maintainable**

