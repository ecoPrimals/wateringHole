#!/bin/sh
# biomeOS Universal Genome Deployment Script
# Deploys anywhere: Linux (x86_64, aarch64), macOS, Android (Termux)
# Version: 1.0.0

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION="1.0.0"

# Colors (if terminal supports)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

log_info()  { printf "${GREEN}[INFO]${NC} %s\n" "$1"; }
log_warn()  { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
log_error() { printf "${RED}[ERROR]${NC} %s\n" "$1"; }
log_step()  { printf "${BLUE}[STEP]${NC} %s\n" "$1"; }

# Detect platform
detect_platform() {
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    
    # Normalize architecture
    case "$ARCH" in
        x86_64|amd64)     ARCH="x86_64" ;;
        aarch64|arm64)    ARCH="aarch64" ;;
        armv7l|armhf)     ARCH="arm32" ;;
        riscv64)          ARCH="riscv64" ;;
    esac
    
    # Normalize OS
    case "$OS" in
        linux)            OS="linux" ;;
        darwin)           OS="darwin" ;;
        freebsd|openbsd)  OS="bsd" ;;
        mingw*|msys*)     OS="windows" ;;
    esac
    
    # Check for Android (Linux + Termux)
    if [ "$OS" = "linux" ] && [ -n "$TERMUX_VERSION" ]; then
        OS="android"
    fi
    
    PLATFORM="${ARCH}-${OS}"
}

# Find installation directory
find_install_dir() {
    # Prefer XDG paths
    if [ -n "$XDG_DATA_HOME" ]; then
        INSTALL_DIR="$XDG_DATA_HOME/biomeOS"
    elif [ -d "$HOME/.local/share" ]; then
        INSTALL_DIR="$HOME/.local/share/biomeOS"
    elif [ -n "$PREFIX" ]; then
        # Termux
        INSTALL_DIR="$PREFIX/share/biomeOS"
    else
        INSTALL_DIR="$HOME/.biomeOS"
    fi
    
    BIN_DIR="$HOME/.local/bin"
    [ ! -d "$BIN_DIR" ] && BIN_DIR="$INSTALL_DIR/bin"
}

# Find binary for platform
find_binary() {
    PRIMAL="$1"
    
    # Try exact platform match
    BIN="${SCRIPT_DIR}/primals/${PRIMAL}/latest/${PRIMAL}-${PLATFORM}"
    [ -f "$BIN" ] && echo "$BIN" && return 0
    
    # Try without version suffix
    BIN="${SCRIPT_DIR}/primals/${PRIMAL}/latest/${PRIMAL}-${ARCH}-linux"
    [ -f "$BIN" ] && echo "$BIN" && return 0
    
    # Try generic linux
    BIN="${SCRIPT_DIR}/primals/${PRIMAL}/latest/${PRIMAL}-${ARCH}-linux-musl"
    [ -f "$BIN" ] && echo "$BIN" && return 0
    
    BIN="${SCRIPT_DIR}/primals/${PRIMAL}/latest/${PRIMAL}-${ARCH}-linux-gnu"
    [ -f "$BIN" ] && echo "$BIN" && return 0
    
    return 1
}

# Verify binary is executable (PIE check)
verify_binary() {
    BIN="$1"
    
    # Check it's an ELF file
    if ! file "$BIN" 2>/dev/null | grep -q "ELF"; then
        log_error "Not an ELF binary: $BIN"
        return 1
    fi
    
    # Try to execute --version
    if ! "$BIN" --version >/dev/null 2>&1; then
        log_warn "Binary failed execution test (may need different platform)"
        return 1
    fi
    
    return 0
}

# Deploy a single primal
deploy_primal() {
    PRIMAL="$1"
    
    BIN=$(find_binary "$PRIMAL") || {
        log_warn "No binary found for $PRIMAL on $PLATFORM"
        return 1
    }
    
    log_info "Found: $(basename "$BIN")"
    
    if verify_binary "$BIN"; then
        mkdir -p "$BIN_DIR"
        cp "$BIN" "$BIN_DIR/$PRIMAL"
        chmod +x "$BIN_DIR/$PRIMAL"
        log_info "Installed: $BIN_DIR/$PRIMAL"
        return 0
    else
        log_warn "Skipping $PRIMAL (binary verification failed)"
        return 1
    fi
}

# Deploy genetics
deploy_genetics() {
    GENETICS_SRC="${SCRIPT_DIR}/genetics"
    
    if [ -f "${GENETICS_SRC}/.family.seed" ]; then
        mkdir -p "$INSTALL_DIR"
        
        # Copy family seed (PASSED - identical for all family members)
        cp "${GENETICS_SRC}/.family.seed" "$INSTALL_DIR/.family.seed"
        chmod 600 "$INSTALL_DIR/.family.seed"
        log_info "Family seed installed"
        
        # Derive unique lineage for this deployment
        if [ -f "${GENETICS_SRC}/.lineage.template" ]; then
            # Mix template with local entropy
            ENTROPY=$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | od -An -tx1 | tr -d ' \n')
            TEMPLATE=$(cat "${GENETICS_SRC}/.lineage.template" | od -An -tx1 | tr -d ' \n')
            echo -n "${TEMPLATE}${ENTROPY}" | sha256sum | cut -c1-64 | xxd -r -p > "$INSTALL_DIR/.lineage.seed"
            chmod 600 "$INSTALL_DIR/.lineage.seed"
            log_info "Lineage seed derived (unique to this deployment)"
        fi
    else
        log_warn "No genetics found in genome"
    fi
}

# Main deployment
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║          🧬 biomeOS Universal Genome Deployer             ║"
    echo "║                    Version $VERSION                         ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    
    log_step "Detecting platform..."
    detect_platform
    log_info "Platform: $PLATFORM"
    
    log_step "Finding installation directories..."
    find_install_dir
    log_info "Data: $INSTALL_DIR"
    log_info "Binaries: $BIN_DIR"
    
    echo ""
    log_step "Deploying primals..."
    
    DEPLOYED=0
    FAILED=0
    
    for PRIMAL in beardog songbird nestgate toadstool squirrel biomeos; do
        printf "  %-12s " "$PRIMAL:"
        if deploy_primal "$PRIMAL" 2>/dev/null; then
            DEPLOYED=$((DEPLOYED + 1))
        else
            FAILED=$((FAILED + 1))
            printf "${RED}SKIPPED${NC}\n"
        fi
    done
    
    echo ""
    log_step "Deploying genetics..."
    deploy_genetics
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    log_info "Deployment complete!"
    log_info "  Primals deployed: $DEPLOYED"
    [ $FAILED -gt 0 ] && log_warn "  Primals skipped: $FAILED"
    echo ""
    echo "To start NUCLEUS:"
    echo "  export PATH=\"\$PATH:$BIN_DIR\""
    echo "  biomeos nucleus --node-id $(hostname) --mode full"
    echo ""
}

# Handle arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    --platform)
        detect_platform
        echo "$PLATFORM"
        ;;
    --version)
        echo "biomeOS Genome Deployer v$VERSION"
        ;;
    --help|-h)
        echo "Usage: $0 [deploy|--platform|--version|--help]"
        echo ""
        echo "Commands:"
        echo "  deploy     Deploy biomeOS to this system (default)"
        echo "  --platform Show detected platform"
        echo "  --version  Show version"
        echo "  --help     Show this help"
        ;;
    *)
        log_error "Unknown command: $1"
        exit 1
        ;;
esac

