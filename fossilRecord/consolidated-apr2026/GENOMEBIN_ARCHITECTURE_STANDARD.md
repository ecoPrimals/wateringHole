# genomeBin Architecture - Ecosystem Standard

**Status**: 🌟 **ECOSYSTEM STANDARD** 🌟  
**Adopted**: January 19, 2026  
**Authority**: WateringHole Consensus (All Primal Teams)  
**Compliance**: Optional for mature ecoBins  
**Reference Implementation**: sourDough (meta-circular genomeBin #1)

---

> **Implementation Note (March 2026):** The live binary distribution surface is
> [ecoPrimals/plasmidBin](https://github.com/ecoPrimals/plasmidBin). That repo
> implements the practical subset of this standard — per-primal `metadata.toml`,
> `manifest.lock`, `fetch.sh` (consumer pull), `harvest.sh` (maintainer publish),
> `start_primal.sh` (unified startup), and `ports.env` (canonical TCP ports).
> The `wateringHole/genomeBin/manifest.toml` retains the full capability registry,
> tier definitions, and architecture mappings as the reference specification.
> `plasmidBin/` is the operational surface; this document is the architectural
> standard it implements.

---

## 📜 **Standard Declaration**

**genomeBin Architecture** is hereby adopted as the official ecosystem standard for **autonomous cross-system deployment**. This standard builds upon ecoBin by adding deployment machinery, enabling **one-command installation** on ANY system with **zero manual configuration**.

**All ecoBin-certified primals** are eligible to evolve toward this standard for maximum deployment simplicity and user experience.

---

## 🎯 **Core Principle**

### **genomeBin = Complete Organism = Cross-System Autonomous Deployment**

**genomeBin** is an **ecoBin** wrapped with deployment machinery that creates a **complete autonomous organism**.

**The Biological Principle**:
Just like DNA needs cellular machinery to function as a living organism, an ecoBin needs deployment machinery to function as an autonomous system:

- 🧬 **DNA**: ecoBin core (functionality + portability)
- 🔬 **Cell Membrane**: Deployment wrapper (system detection + installation)
- 🔋 **Mitochondria**: Service management (systemd, launchd, rc.d)
- 🧪 **Ribosomes**: Configuration system (adaptive setup)
- 🩺 **Lysosomes**: Health monitoring (self-diagnostics)
- 🔄 **Endoplasmic Reticulum**: Update system (safe evolution)

**Formula**:
```
genomeBin = ecoBin (UniBin + Pure Rust + Cross-Compilation)
          + Deployment Wrapper (auto-detect + auto-install)
          + System Integration (services + health + updates)
          
Result: ONE command → Works on ANY system → ZERO configuration!
```

**The Goal**: `curl -sSf https://install.primal.dev/genome | sh` → DONE! 🎉

---

## 🆚 **The Three Evolutionary Stages**

### **Stage 1: UniBin** (Well-Structured DNA)

**Definition**: Single binary with multiple operational modes

**Metaphor**: Single strand of DNA (genetic code)

**Requirements**:
- ✅ One binary per primal
- ✅ Multiple operational modes
- ✅ Professional CLI
- ⚠️ May be arch-specific
- ⚠️ May have C dependencies
- ⚠️ User must install manually

**Example**:
```bash
beardog crypto      # One binary, many modes
beardog hsm
beardog entropy
```

**Status**: Foundation (all primals should be UniBin)

---

### **Stage 2: ecoBin** (The Double Helix)

**Definition**: UniBin + Pure Rust = cross-architecture portability

**Metaphor**: DNA double helix (stable + universal)

**Requirements**:
- ✅ All UniBin requirements (prerequisite)
- ✅ 100% Pure Rust (zero C dependencies)
- ✅ Cross-compiles to ALL architectures
- ✅ Static linking (self-contained)
- ✅ Binary validation (no C symbols)
- ⚠️ User must detect arch and install
- ⚠️ User must configure manually

**Example**:
```bash
beardog-x86_64-musl    # ecoBin for Intel/AMD
beardog-aarch64-musl   # ecoBin for ARM64
beardog-riscv64-musl   # ecoBin for RISC-V
```

**Status**: Excellence (4 primals achieved ecoBin status)

---

### **Stage 3: genomeBin** (The Living Cell)

**Definition**: ecoBin + Deployment Wrapper = autonomous organism

**Metaphor**: Complete living cell (DNA + all cellular machinery)

**Requirements**:
- ✅ All ecoBin requirements (prerequisite)
- ✅ Deployment wrapper (smart installer)
- ✅ System detection (OS, arch, init system)
- ✅ Auto-installation (binary, config, service)
- ✅ Service integration (systemd, launchd, rc.d)
- ✅ Health monitoring (self-diagnostics)
- ✅ Update system (safe evolution)
- ✅ Rollback capability (safety)
- ✅ Clean uninstall (leave no trace)
- ✅ **ZERO manual configuration**

**Example**:
```bash
# ONE command, ANY system!
curl -sSf https://install.beardog.dev/genome | sh

# Or download and run:
./beardog.genome

# Auto-detects everything, installs, configures, starts
# User gets: "BearDog v0.9.0 installed successfully! ✅"
```

**Status**: Innovation (ready for first implementations)

---

## 📊 **genomeBin Requirements**

### **Tier 1: ecoBin Foundation** (Prerequisite)

**Must be TRUE ecoBin first**:

- [ ] UniBin architecture (multiple modes) ✅
- [ ] 100% Pure Rust (production + dev) ✅
- [ ] Cross-compilation validated (x86_64 + ARM64 minimum) ✅
- [ ] Static linking (musl) ✅
- [ ] Binary analysis clean (no C symbols) ✅
- [ ] Multiple architectures built and tested ✅

**Validation**:
```bash
# Must pass all ecoBin checks first!
cargo tree | grep ring          # → empty
cargo build --target x86_64-unknown-linux-musl    # → success
cargo build --target aarch64-unknown-linux-musl   # → success
ldd binary                       # → "statically linked"
```

**If not ecoBin**: Complete ecoBin evolution FIRST, then return here.

---

### **Tier 2: Deployment Wrapper** (Core)

**Smart installer that adapts to environment**

#### 2.1: System Detection

**Must auto-detect**:
- [ ] Operating system (Linux, macOS, BSD, Windows WSL)
- [ ] Architecture (x86_64, aarch64, armv7, riscv64)
- [ ] Init system (systemd, launchd, rc.d, openrc)
- [ ] Privilege level (root, sudo, user-only)
- [ ] Environment type (development, production, embedded)

**Implementation**:
```bash
detect_os() {
    # Linux, Darwin (macOS), FreeBSD, OpenBSD, etc.
    uname -s
}

detect_arch() {
    # x86_64, aarch64, armv7l, riscv64, etc.
    uname -m
}

detect_init() {
    # systemd, launchd, rc.d, openrc, etc.
    # Check: /run/systemd/system, /Library/LaunchDaemons, etc.
}
```

#### 2.2: ecoBin Selection

**Must select correct ecoBin from embedded payload**:
- [ ] Match OS + architecture combination
- [ ] Extract correct binary from archive
- [ ] Verify checksum (integrity)
- [ ] Verify signature (security, optional but recommended)

**Embedded ecoBins** (minimum set):
```
Payload contains:
├── primal-x86_64-linux-musl      (Linux Intel/AMD)
├── primal-aarch64-linux-musl     (Linux ARM64)
├── primal-x86_64-macos           (macOS Intel)
└── primal-aarch64-macos          (macOS Apple Silicon)

Optional additional targets:
├── primal-armv7-linux-musl       (ARM32)
├── primal-riscv64-linux-musl     (RISC-V)
└── primal-x86_64-windows.exe     (Windows)
```

#### 2.3: Installation Logic

**Must install to appropriate location**:
- [ ] Root install: `/usr/local/bin/` (preferred)
- [ ] User install: `~/.local/bin/` (fallback)
- [ ] Permissions: `755` (executable)
- [ ] Ownership: appropriate user/group

**Must handle conflicts**:
- [ ] Check if already installed
- [ ] Prompt for upgrade/reinstall
- [ ] Backup existing version

---

### **Tier 3: System Integration** (Essential)

#### 3.1: Service Management

**Must integrate with native init system**:

**Linux (systemd)**:
- [ ] Create service unit: `/etc/systemd/system/primal.service`
- [ ] Enable auto-start: `systemctl enable primal`
- [ ] Start service: `systemctl start primal`
- [ ] Validate: `systemctl status primal`

**macOS (launchd)**:
- [ ] Create plist: `~/Library/LaunchAgents/dev.primal.plist`
- [ ] Load service: `launchctl load`
- [ ] Enable auto-start: `<RunAtLoad>true</RunAtLoad>`
- [ ] Validate: `launchctl list | grep primal`

**BSD (rc.d)**:
- [ ] Create rc script: `/etc/rc.d/primal`
- [ ] Enable in rc.conf: `primal_enable="YES"`
- [ ] Start service: `service primal start`
- [ ] Validate: `service primal status`

**Service Template** (systemd example):
```ini
[Unit]
Description={PRIMAL_NAME} Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/{primal} serve
Restart=on-failure
RestartSec=5s
User={primal}
Group={primal}

[Install]
WantedBy=multi-user.target
```

#### 3.2: Configuration Management

**Must create smart default configuration**:
- [ ] Detect environment (dev, prod, embedded)
- [ ] Generate appropriate config
- [ ] Allow user overrides
- [ ] Document configuration options

**Configuration Locations**:
- System (root): `/etc/primal/config.toml`
- User: `~/.config/primal/config.toml`
- Runtime: `~/.cache/primal/`
- Data: `/var/lib/primal/` or `~/.local/share/primal/`

**Smart Defaults**:
```toml
# Auto-generated based on environment detection

[core]
log_level = "info"  # "debug" for dev, "warn" for embedded

[data]
directory = "/var/lib/{primal}"  # Or ~/.local/share for user install

[network]
socket = "/var/run/{primal}/provider.sock"  # Unix socket path
```

---

### **Tier 4: Health & Monitoring** (Quality)

#### 4.1: Built-in Health Checks

**Must implement doctor mode** (part of UniBin):
- [ ] `primal doctor` command exists
- [ ] Checks all critical systems
- [ ] Reports status in human-readable format
- [ ] Supports JSON output for automation
- [ ] Exit code reflects health (0 = healthy, 1 = issues)

**Health Check Coverage**:
```bash
primal doctor

Output:
🏥 {PRIMAL} Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Core Systems
   ✅ Binary: v0.9.0
   ✅ Config: loaded from /etc/primal/config.toml
   ✅ Data directory: 12.3 MB

✅ Dependencies
   ✅ Unix socket: /var/run/primal/provider.sock
   ✅ Permissions: correct

✅ Performance
   ✅ Memory: 23.4 MB
   ✅ CPU: 0.3%
   ✅ Uptime: 3d 14h 22m

✅ Integration
   ✅ Other primals: 3 connected

Overall: HEALTHY ✅
```

#### 4.2: Automated Monitoring

**genomeBin wrapper provides**:
- [ ] Health check scheduling
- [ ] Alert on failures
- [ ] Log aggregation
- [ ] Metrics collection (optional)

**Monitoring Commands**:
```bash
# Automated health checks
primal.genome health              # One-time check
primal.genome monitor --interval 5m  # Continuous
primal.genome alert --webhook URL    # Alert integration
```

---

### **Tier 5: Lifecycle Management** (Advanced)

#### 5.1: Safe Updates

**Must support safe updates**:
- [ ] Check for new versions
- [ ] Download new genomeBin
- [ ] Verify signature/checksum
- [ ] Backup current version
- [ ] Stop service
- [ ] Replace binary
- [ ] Restart service
- [ ] Health check
- [ ] Auto-rollback on failure

**Update Process**:
```bash
# Check for updates
primal.genome update --check

Output:
Current: v0.9.0
Latest:  v0.10.0
Release: https://primal.dev/releases/v0.10.0

# Perform update
primal.genome update

Process:
  1. ✅ Backup current version
  2. ✅ Download v0.10.0
  3. ✅ Verify signature
  4. ✅ Stop service
  5. ✅ Replace binary
  6. ✅ Restart service
  7. ✅ Health check
  8. ✅ Update successful!
```

#### 5.2: Rollback Support

**Must support rollback**:
- [ ] Backup last N versions (default: 3)
- [ ] Manual rollback command
- [ ] Auto-rollback on health failure
- [ ] Preserve user data/config

**Rollback Process**:
```bash
# If update fails or causes issues
primal.genome rollback

Process:
  1. ✅ Stop service
  2. ✅ Restore previous binary
  3. ✅ Restart service
  4. ✅ Health check
  5. ✅ Rollback complete!
```

#### 5.3: Clean Uninstall

**Must uninstall completely**:
- [ ] Stop service
- [ ] Remove service files
- [ ] Remove binary
- [ ] Optionally remove data
- [ ] Optionally remove config
- [ ] Leave no trace

**Uninstall Process**:
```bash
primal.genome uninstall

Options:
  --keep-data     # Keep user data
  --keep-config   # Keep configuration
  --purge         # Remove everything
  --dry-run       # Show what would be removed

Process:
  1. ✅ Stop primal service
  2. ✅ Remove systemd/launchd files
  3. ✅ Remove /usr/local/bin/primal
  4. ❓ Remove data? (ask user or use flag)
  5. ❓ Remove config? (ask user or use flag)
  6. ✅ Cleanup complete!
```

---

## 🏗️ **genomeBin Structure**

### **File Format**

**Single self-extracting archive**:
```
primal.genome (executable shell script + embedded data)
├── Deployment wrapper (bash/sh script)
│   ├── System detection
│   ├── Installation logic
│   ├── Service integration
│   └── Health validation
├── Embedded payload (compressed tar.gz)
│   ├── ecoBins/
│   │   ├── primal-x86_64-linux-musl
│   │   ├── primal-aarch64-linux-musl
│   │   ├── primal-x86_64-macos
│   │   └── primal-aarch64-macos
│   ├── configs/
│   │   ├── config.toml.template
│   │   └── environment-configs/
│   ├── services/
│   │   ├── systemd.service.template
│   │   ├── launchd.plist.template
│   │   └── rc.d.template
│   └── scripts/
│       ├── health-check.sh
│       └── update.sh
└── Signature (GPG, optional)
```

### **Size Expectations**

**Typical genomeBin sizes**:
```
ecoBin core (per arch):        2-5 MB (stripped, musl)
× 4 architectures:            8-20 MB
+ Wrapper scripts:            50-100 KB
+ Templates/configs:          10-50 KB
+ Compression savings:        -30% to -50%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total genomeBin:              6-15 MB (typical)
```

**Trade-off**: Larger single file, but ONE download for ALL systems!

---

## 📦 **Creating a genomeBin**

### **Standard Scaffolding Available**

🎉 **80-90% of genomeBin creation is now STANDARDIZED!**

**Location**: `ecoPrimals/phase2/sourDough/genomebin/`

**What's provided**:
- ✅ Wrapper scripts (system detection, installation, lifecycle)
- ✅ Service templates (systemd, launchd, rc.d)
- ✅ Build scripts (create, test, sign)
- ✅ Configuration templates
- ✅ biomeOS/neuralAPI integration

**See**: `sourDough/genomebin/README.md` for complete guide

**Quick Start**:
```bash
# From your ecoBin-certified primal:
../../sourDough/genomebin/scripts/create-genomebin.sh \
    --primal yourprimal \
    --version 1.0.0 \
    --ecobins plasmidBin/primals/yourprimal/v1.0.0/ \
    --output yourprimal.genome

# That's it! genomeBin created in ~5 minutes!
```

### **Prerequisites**

**Must have**:
1. ✅ Primal is TRUE ecoBin (validated)
2. ✅ ecoBins built for all target architectures
3. ✅ Binary validation complete (all targets)
4. ✅ UniBin doctor mode implemented
5. ✅ Implements `sourdough-core` traits (PrimalHealth, PrimalLifecycle)

### **Build Process**

**Step 1: Collect ecoBins**
```bash
# Build all target architectures
cargo build --release --target x86_64-unknown-linux-musl
cargo build --release --target aarch64-unknown-linux-musl
cargo build --release --target x86_64-apple-darwin
cargo build --release --target aarch64-apple-darwin

# Collect binaries
mkdir -p genome/ecobins/
cp target/*/release/primal genome/ecobins/
```

**Step 2: Prepare templates**
```bash
# Create template directory
mkdir -p genome/{configs,services,scripts}

# Add configuration templates
cp config.toml.template genome/configs/

# Add service templates
cp systemd.service.template genome/services/
cp launchd.plist.template genome/services/
cp rc.d.template genome/services/

# Add scripts
cp health-check.sh genome/scripts/
cp update.sh genome/scripts/
```

**Step 3: Create payload**
```bash
# Create compressed archive
cd genome/
tar -czf ../payload.tar.gz *
cd ..
```

**Step 4: Create wrapper**
```bash
# Create self-extracting archive
cat wrapper-script.sh payload.tar.gz > primal.genome
chmod +x primal.genome
```

**Step 5: Sign (optional but recommended)**
```bash
# Sign with GPG
gpg --detach-sign --armor primal.genome

# Creates: primal.genome.asc
```

**Step 6: Checksum**
```bash
# Create checksum
sha256sum primal.genome > primal.genome.sha256
```

**Result**:
```
primal.genome           (10-15 MB, self-installing)
primal.genome.asc       (GPG signature)
primal.genome.sha256    (checksum)
```

---

## 🌐 **Distribution**

### **Hosting**

**Recommended structure**:
```
https://install.primal.dev/
├── genome                 (latest version, symlink)
├── latest                 (version info)
├── v0.9.0/
│   ├── primal.genome
│   ├── primal.genome.asc
│   └── primal.genome.sha256
└── v0.10.0/
    ├── primal.genome
    ├── primal.genome.asc
    └── primal.genome.sha256
```

### **Installation Methods**

**Method 1: One-liner** (recommended)
```bash
curl -sSf https://install.primal.dev/genome | sh
```

**Method 2: Download + Run**
```bash
curl -L -O https://install.primal.dev/genome
chmod +x genome
./genome
```

**Method 3: Specific version**
```bash
curl -sSf https://install.primal.dev/v0.9.0/primal.genome | sh
```

---

## ✅ **genomeBin Certification**

### **Compliance Checklist**

**Tier 1: ecoBin Foundation** (Prerequisite)
- [ ] Is TRUE ecoBin (all ecoBin requirements met)
- [ ] Multiple architectures validated (x86_64 + ARM64 minimum)
- [ ] Binary analysis clean (no C symbols)
- [ ] Static linking confirmed (ldd check)

**Tier 2: Deployment Wrapper**
- [ ] Auto-detects OS and architecture
- [ ] Selects correct ecoBin from payload
- [ ] Installs to appropriate location
- [ ] Handles permissions correctly

**Tier 3: System Integration**
- [ ] Creates native service (systemd/launchd/rc.d)
- [ ] Generates smart configuration
- [ ] Validates installation with health check

**Tier 4: Health & Monitoring**
- [ ] `primal doctor` command implemented
- [ ] Health check covers all critical systems
- [ ] Supports automation (JSON output)

**Tier 5: Lifecycle Management**
- [ ] Update system implemented
- [ ] Rollback capability tested
- [ ] Clean uninstall verified

**Tier 6: User Experience**
- [ ] ONE command installation works
- [ ] ZERO manual configuration needed
- [ ] Clear success/error messages
- [ ] Documentation complete

### **Certification Levels**

**Bronze genomeBin**: Tiers 1-3 (Core functionality)
**Silver genomeBin**: Tiers 1-4 (+ Health monitoring)
**Gold genomeBin**: Tiers 1-5 (+ Lifecycle management)
**Platinum genomeBin**: All tiers + exceptional UX

---

## 🎯 **Current Ecosystem Status**

### **genomeBin-Ready Primals** (ecoBin Certified)

**Ready to begin genomeBin evolution**:

1. **🐻 BearDog** - A++ ecoBin
   - Status: ✅ TRUE ecoBin certified
   - Architectures: x86_64, ARM64 (musl)
   - Grade: A++ (reference implementation)
   - **Recommended: FIRST genomeBin!**

2. **🏰 NestGate** - GOLD ecoBin
   - Status: ✅ TRUE ecoBin certified
   - Architectures: 5 Linux + 2 macOS targets
   - Grade: GOLD (exceptional coverage)

3. **🍄 ToadStool** - A++ ecoBin
   - Status: ✅ TRUE ecoBin certified
   - Architectures: 5 targets validated
   - Grade: A++ (compute reference)

4. **🧠 biomeOS** - A++ ecoBin
   - Status: ✅ TRUE ecoBin certified
   - Architectures: x86_64, ARM64 (musl)
   - Grade: A++ (orchestrator)

**Total Ready**: 4 primals can begin genomeBin evolution NOW!

### **Not Yet Ready** (Complete ecoBin first)

5. **🐿️ Squirrel** - 70% to ecoBin
   - Status: 🏗️ Active evolution
   - Blockers: Build errors, dependency cleanup
   - Timeline: ~7-10 hours to ecoBin

6. **👅 petalTongue** - Strategic approach
   - Status: 🎯 Hybrid strategy (2/3 ecoBin)
   - Plan: Headless + CLI to ecoBin
   - Timeline: ~6-8 hours

7. **🐦 Songbird** - N/A
   - Status: Intentional HTTP/TLS role
   - Reason: Not ecoBin candidate by design

---

## 🎊 **Success Metrics**

### **genomeBin Promises**

**User Experience**:
- ✅ ONE command installs on ANY system
- ✅ ZERO manual configuration required
- ✅ Works on x86_64, ARM64, RISC-V, macOS, etc.
- ✅ Native service integration (systemd/launchd/rc.d)
- ✅ Health monitoring built-in
- ✅ Safe updates with rollback
- ✅ Clean uninstall

**Developer Experience**:
- ✅ Standard format (same for all primals)
- ✅ Reusable tooling (create-genomebin.sh)
- ✅ Automated testing (multiple environments)
- ✅ Clear documentation (this standard!)

**Ecosystem Impact**:
- ✅ Revolutionary deployment simplicity
- ✅ Consumer-grade installation experience
- ✅ Competitive with Docker/Snap/Homebrew
- ✅ But SIMPLER and more UNIVERSAL!

---

## 📚 **Reference Implementation**

### **Recommended First genomeBin: BearDog**

**Why BearDog?**
1. Most mature ecoBin (A++ grade)
2. Well-tested across architectures
3. Clean UniBin with doctor mode
4. Already has service templates
5. Strong team support

**Timeline**: ~2-3 days to create first genomeBin

**Impact**: Sets standard for all others!

---

## 🌍 **The Vision**

### **Complete Organism Deployment**

**Today** (ecoBin):
```bash
# User must detect architecture
uname -m  # aarch64

# Download correct binary
wget https://cdn.primal.dev/releases/primal-aarch64-musl

# Install manually
sudo install -m 755 primal-aarch64-musl /usr/local/bin/primal

# Create service file manually
sudo nano /etc/systemd/system/primal.service

# Configure manually
sudo nano /etc/primal/config.toml

# Enable and start
sudo systemctl enable primal
sudo systemctl start primal
```

**Tomorrow** (genomeBin):
```bash
# ONE command, ZERO configuration!
curl -sSf https://install.primal.dev/genome | sh

# Auto-detects: Linux + ARM64
# Auto-installs: correct ecoBin
# Auto-configures: smart defaults
# Auto-starts: systemd service
# Reports: "Primal v0.9.0 installed successfully! ✅"
```

**Comparison**: 7 manual steps → 1 automated command! 🎉

---

## 🎯 **Adoption Path**

### **For Primal Teams**

**Step 1**: Achieve ecoBin status (prerequisite)
**Step 2**: Review this standard
**Step 3**: Implement deployment wrapper
**Step 4**: Test on multiple systems
**Step 5**: Submit for certification
**Step 6**: Publish to distribution

### **For Users**

**Before genomeBin**: Manual installation, architecture detection, configuration
**After genomeBin**: ONE command, works everywhere, ZERO configuration

**The Promise**: "Easier than Docker, simpler than Snap, more universal than Homebrew!"

---

**Date**: January 19, 2026  
**Status**: 🌟 ECOSYSTEM STANDARD  
**Version**: 1.0.0  
**Next**: First genomeBin implementation (BearDog recommended)

🧬🌍🦀 **The complete organism - deploy anywhere with one command!** ✨

---

## 📖 **Appendix: Related Standards**

- **UniBin Architecture**: wateringHole/UNIBIN_ARCHITECTURE_STANDARD.md
- **ecoBin Architecture**: wateringHole/ECOBIN_ARCHITECTURE_STANDARD.md
- **BTSP Protocol**: wateringHole/btsp/
- **BirdSong Protocol**: wateringHole/birdsong/

