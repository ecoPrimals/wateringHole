#!/usr/bin/env bash
# beacon_tunnel.sh — BirdSong Beacon tunnel lifecycle management
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Manages the biomeOS beacon and Cloudflare Tunnel services.
# Designed to work on any machine in the LAN cloud.
set -euo pipefail

TUNNEL_NAME="nestgate-api"
BIOMEOS_SERVICE="biomeos-beacon.service"
CLOUDFLARED_SERVICE="cloudflared-beacon.service"
BEACON_ENDPOINT="https://api.nestgate.io/"

red()    { printf '\033[0;31m%s\033[0m\n' "$*"; }
green()  { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }

check_cloudflared() {
    if ! command -v cloudflared &>/dev/null; then
        red "cloudflared not found."
        echo "Install: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cloudflared.deb && sudo dpkg -i /tmp/cloudflared.deb"
        return 1
    fi
    green "cloudflared $(cloudflared version 2>&1 | head -1)"
}

check_credentials() {
    local creds_dir="${HOME}/.cloudflared"
    if [ ! -d "$creds_dir" ]; then
        red "No credentials directory at $creds_dir"
        return 1
    fi
    local json_count
    json_count=$(find "$creds_dir" -name "*.json" -type f | wc -l)
    if [ "$json_count" -eq 0 ]; then
        red "No tunnel credentials found in $creds_dir"
        return 1
    fi
    green "Tunnel credentials present ($json_count file(s) in $creds_dir)"
}

check_config() {
    local config="${HOME}/.cloudflared/config.yml"
    if [ ! -f "$config" ]; then
        red "No config at $config"
        return 1
    fi
    if grep -q "$TUNNEL_NAME" "$config"; then
        green "Config references tunnel '$TUNNEL_NAME'"
    else
        yellow "Config exists but does not reference '$TUNNEL_NAME'"
    fi
}

check_biomeos_socket() {
    local runtime_dir="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/biomeos"
    local sock_count
    sock_count=$(find "$runtime_dir" -name "biomeos-api-*.sock" -type s 2>/dev/null | wc -l)
    if [ "$sock_count" -gt 0 ]; then
        green "biomeOS socket(s) active in $runtime_dir ($sock_count found)"
        find "$runtime_dir" -name "biomeos-api-*.sock" -type s 2>/dev/null
    else
        yellow "No biomeOS API socket found in $runtime_dir"
        return 1
    fi
}

check_public_endpoint() {
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BEACON_ENDPOINT" 2>/dev/null || echo "000")
    case "$status" in
        403)
            green "Beacon endpoint returns 403 (Dark Forest active)"
            ;;
        000)
            red "Beacon endpoint unreachable (timeout or DNS failure)"
            return 1
            ;;
        *)
            yellow "Beacon endpoint returns $status (unexpected)"
            ;;
    esac
}

cmd_status() {
    echo "=== BirdSong Beacon Status ==="
    echo ""
    echo "-- Prerequisites --"
    check_cloudflared || true
    check_credentials || true
    check_config || true
    echo ""
    echo "-- Services --"
    systemctl --user is-active "$BIOMEOS_SERVICE" 2>/dev/null && green "biomeOS beacon: active" || red "biomeOS beacon: inactive"
    systemctl --user is-active "$CLOUDFLARED_SERVICE" 2>/dev/null && green "cloudflared tunnel: active" || red "cloudflared tunnel: inactive"
    echo ""
    echo "-- Runtime --"
    check_biomeos_socket || true
    echo ""
    echo "-- Public Endpoint --"
    check_public_endpoint || true
}

cmd_start() {
    echo "Starting BirdSong Beacon stack..."
    systemctl --user start "$BIOMEOS_SERVICE"
    sleep 2
    if ! systemctl --user is-active --quiet "$BIOMEOS_SERVICE"; then
        red "biomeOS failed to start"
        systemctl --user status "$BIOMEOS_SERVICE" --no-pager
        exit 1
    fi
    green "biomeOS beacon started"

    systemctl --user start "$CLOUDFLARED_SERVICE"
    sleep 3
    if ! systemctl --user is-active --quiet "$CLOUDFLARED_SERVICE"; then
        red "cloudflared failed to start"
        systemctl --user status "$CLOUDFLARED_SERVICE" --no-pager
        exit 1
    fi
    green "cloudflared tunnel started"
    echo ""
    check_public_endpoint || true
}

cmd_stop() {
    echo "Stopping BirdSong Beacon stack..."
    systemctl --user stop "$CLOUDFLARED_SERVICE" 2>/dev/null && green "cloudflared stopped" || yellow "cloudflared was not running"
    systemctl --user stop "$BIOMEOS_SERVICE" 2>/dev/null && green "biomeOS stopped" || yellow "biomeOS was not running"
}

cmd_restart() {
    cmd_stop
    echo ""
    cmd_start
}

cmd_install() {
    echo "Installing systemd user services..."
    local service_dir="${HOME}/.config/systemd/user"
    mkdir -p "$service_dir"

    if [ ! -f "$service_dir/$BIOMEOS_SERVICE" ]; then
        red "Missing $service_dir/$BIOMEOS_SERVICE"
        echo "Copy from wateringHole templates or create manually."
        exit 1
    fi
    if [ ! -f "$service_dir/$CLOUDFLARED_SERVICE" ]; then
        red "Missing $service_dir/$CLOUDFLARED_SERVICE"
        echo "Copy from wateringHole templates or create manually."
        exit 1
    fi

    systemctl --user daemon-reload
    systemctl --user enable "$BIOMEOS_SERVICE"
    systemctl --user enable "$CLOUDFLARED_SERVICE"
    loginctl enable-linger "$(whoami)" 2>/dev/null || yellow "Could not enable lingering (may need root)"
    green "Services installed and enabled"
}

cmd_logs() {
    local lines="${1:-50}"
    echo "=== biomeOS beacon (last $lines lines) ==="
    journalctl --user -u "$BIOMEOS_SERVICE" --no-pager -n "$lines" 2>/dev/null || systemctl --user status "$BIOMEOS_SERVICE" --no-pager
    echo ""
    echo "=== cloudflared tunnel (last $lines lines) ==="
    journalctl --user -u "$CLOUDFLARED_SERVICE" --no-pager -n "$lines" 2>/dev/null || systemctl --user status "$CLOUDFLARED_SERVICE" --no-pager
}

usage() {
    cat <<EOF
Usage: $(basename "$0") <command>

Commands:
  status   Check all components (prerequisites, services, endpoint)
  start    Start biomeOS beacon then cloudflared tunnel
  stop     Stop cloudflared then biomeOS
  restart  Stop then start
  install  Enable systemd services and lingering
  logs     Show recent logs (optional: logs <lines>)

EOF
}

case "${1:-}" in
    status)  cmd_status ;;
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    restart) cmd_restart ;;
    install) cmd_install ;;
    logs)    cmd_logs "${2:-50}" ;;
    *)       usage; exit 1 ;;
esac
