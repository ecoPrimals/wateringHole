#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# provision-golgi.sh — Rebuild golgi VPS from a fresh Debian 12 droplet
#
# This script provisions the "thin edge" relay layer of the Sovereign Relay
# Architecture. golgi serves as the public ingress surface, running only:
#
#   - Forgejo    (sovereign git forge, SSH on :2222, HTTP on :3000)
#   - Caddy      (TLS termination, depot file_server, reverse proxy)
#   - membrane   (temporal.cascade — Forgejo→sporeGate sync + freshness)
#   - songBird   (mesh federation hub + TURN relay)
#   - bearDog    (crypto identity + BTSP security provider)
#   - WireGuard  (backhaul tunnel to sporeGate LAN)
#   - fail2ban   (SSH brute-force protection)
#
# Prerequisites:
#   - Fresh Debian 12 (bookworm) VPS with ≥10GB disk, ≥2GB RAM
#   - sporeGate NUC online with full Forgejo mirror at /opt/forgejo-mirror/
#   - WireGuard keys generated for new droplet
#   - SSH access from sporeGate to new VPS
#
# Usage:
#   export GOLGI_IP=<new-vps-public-ip>
#   export SPOREGATE_WG_PUBKEY=<sporeGate-wg-pubkey>
#   export GOLGI_WG_PRIVKEY=<new-wg-private-key>
#   bash provision-golgi.sh
#
# Recovery from sporeGate:
#   1. Create new droplet
#   2. Set env vars above
#   3. Run this script via SSH
#   4. rsync Forgejo data:
#        rsync -avz /opt/forgejo-mirror/ root@$GOLGI_IP:/opt/forgejo/data/repositories/
#   5. rsync pepti depot:
#        rsync -avz /opt/ecoPrimals/depot/ root@$GOLGI_IP:/opt/ecoPrimals/depot/
#   6. Start services: systemctl start forgejo caddy-tls beardog-membrane songbird-membrane songbird-relay cascade-sense.timer

set -euo pipefail

GOLGI_IP="${GOLGI_IP:?Set GOLGI_IP to the VPS public IP}"

echo "=== 1. SYSTEM BASE ==="
apt-get update && apt-get upgrade -y
apt-get install -y \
    wireguard \
    fail2ban \
    git \
    curl \
    rsync \
    jq \
    sqlite3 \
    socat

echo "=== 2. CREATE USERS + DIRECTORIES ==="
adduser --system --shell /bin/bash --home /opt/forgejo --group git 2>/dev/null || true
mkdir -p /opt/forgejo/{custom/conf,data/repositories}
mkdir -p /opt/membrane
mkdir -p /opt/ecoPrimals/{depot/{x86_64-unknown-linux-musl,aarch64-unknown-linux-musl},infra/wateringHole/heads}
mkdir -p /etc/membrane
mkdir -p /run/membrane
mkdir -p /etc/songbird

echo "golgiBody" > /etc/membrane/gate-name

echo "=== 3. INSTALL FORGEJO ==="
FORGEJO_VERSION="10.0.1"
curl -sL "https://codeberg.org/forgejo/forgejo/releases/download/v${FORGEJO_VERSION}/forgejo-${FORGEJO_VERSION}-linux-amd64" \
    -o /usr/local/bin/forgejo
chmod +x /usr/local/bin/forgejo

cat > /opt/forgejo/custom/conf/app.ini << 'EOINI'
APP_NAME = ecoPrimals Forge
RUN_USER = git
RUN_MODE = prod
WORK_PATH = /opt/forgejo

[database]
DB_TYPE = sqlite3
PATH = /opt/forgejo/data/forgejo.db

[repository]
ROOT = /opt/forgejo/data/repositories

[server]
DOMAIN = git.primals.eco
SSH_DOMAIN = git.primals.eco
HTTP_ADDR = 127.0.0.1
HTTP_PORT = 3000
ROOT_URL = https://git.primals.eco/
DISABLE_SSH = false
START_SSH_SERVER = true
SSH_PORT = 2222
SSH_LISTEN_HOST = 0.0.0.0
SSH_LISTEN_PORT = 2222
LFS_START_SERVER = true

[service]
DISABLE_REGISTRATION = true
REQUIRE_SIGNIN_VIEW = false
EOINI

chown -R git:git /opt/forgejo

echo "=== 4. INSTALL CADDY ==="
curl -sL "https://caddyserver.com/api/download?os=linux&arch=amd64" -o /opt/membrane/caddy
chmod +x /opt/membrane/caddy

cat > /etc/membrane/Caddyfile << 'EOCADDY'
{
    email ops@primals.eco
}

membrane.primals.eco {
    handle /depot/* {
        uri strip_prefix /depot
        root * /opt/ecoPrimals/depot
        file_server browse
    }
    handle /health {
        respond "membrane-relay TLS active" 200
    }
    handle /status {
        respond "Channel 3 — sovereign TLS operational" 200
    }
    handle {
        root * /var/cache/membrane/nestgate
        file_server
        try_files {path} {path}/ /index.html
    }
}

primals.eco {
    handle {
        root * /opt/ecoPrimals/sporePrint/public
        file_server
        try_files {path} {path}/ /index.html
    }
}

www.primals.eco {
    redir https://primals.eco{uri} permanent
}

git.primals.eco {
    reverse_proxy localhost:3000
}

lab.primals.eco {
    reverse_proxy 10.13.37.2:7780
}
EOCADDY

echo "=== 5. PULL BINARIES FROM SPOREGATE DEPOT ==="
echo "Binaries are deployed from pepti depot on sporeGate."
echo "After WireGuard is up, run:"
echo "  rsync -avz sporegate:/opt/ecoPrimals/depot/x86_64-unknown-linux-musl/{membrane,songbird,beardog} /opt/membrane/"
echo "  rsync -avz sporegate:/opt/ecoPrimals/depot/ /opt/ecoPrimals/depot/"
echo "  cp /opt/membrane/membrane /usr/local/bin/membrane"

echo "=== 6. WIREGUARD ==="
cat > /etc/wireguard/wg0.conf << EOWG
[Interface]
Address = 10.13.37.1/24
ListenPort = 51820
PrivateKey = ${GOLGI_WG_PRIVKEY:-REPLACE_ME}

[Peer]
# sporeGate
PublicKey = ${SPOREGATE_WG_PUBKEY:-REPLACE_ME}
AllowedIPs = 10.13.37.2/32, 192.168.4.0/22
Endpoint = REPLACE_WITH_SPOREGATE_ENDPOINT
PersistentKeepalive = 25
EOWG

systemctl enable wg-quick@wg0

echo "=== 7. SYSTEMD SERVICES ==="

cat > /etc/systemd/system/forgejo.service << 'EOSVC'
[Unit]
Description=Forgejo — Sovereign Git Forge (golgiBody periplasmic surface)
After=network.target

[Service]
User=git
Group=git
Type=simple
WorkingDirectory=/opt/forgejo
ExecStart=/usr/local/bin/forgejo web --config /opt/forgejo/custom/conf/app.ini
Restart=always
RestartSec=5
Environment=USER=git HOME=/opt/forgejo FORGEJO_WORK_DIR=/opt/forgejo

[Install]
WantedBy=multi-user.target
EOSVC

cat > /etc/systemd/system/caddy-tls.service << 'EOSVC'
[Unit]
Description=Channel 3 TLS Surface (Membrane — ACME + Reverse Proxy)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/membrane/caddy run --config /etc/membrane/Caddyfile
Restart=always
RestartSec=5
AmbientCapabilities=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
PrivateTmp=true
MemoryMax=128M
CPUQuota=25%

[Install]
WantedBy=multi-user.target
EOSVC

cat > /etc/systemd/system/beardog-membrane.service << 'EOSVC'
[Unit]
Description=BearDog Crypto (Membrane Tower — BTSP + Secrets)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/membrane/beardog server --socket /run/membrane/beardog.sock
Environment=BEARDOG_SOCKET_MODE=0660
Environment=BEARDOG_LOG_LEVEL=info
Environment=BEARDOG_ROLE=membrane
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
MemoryMax=64M
CPUQuota=25%

[Install]
WantedBy=multi-user.target
EOSVC

cat > /etc/systemd/system/songbird-membrane.service << 'EOSVC'
[Unit]
Description=Songbird Discovery + Federation (Membrane Tower — Mesh Hub)
After=network-online.target beardog-membrane.service
Wants=network-online.target
Requires=beardog-membrane.service

[Service]
Type=simple
ExecStartPre=-/bin/rm -f /run/membrane/songbird.sock
ExecStart=/opt/membrane/songbird server \
    --socket /run/membrane/songbird.sock \
    --security-socket /run/membrane/beardog.sock \
    --federation-port 7700 \
    --bind 0.0.0.0 \
    --dark-forest \
    --pid-dir /run/membrane
Environment=SONGBIRD_NODE_ID=golgiBody
Environment=SONGBIRD_DARK_FOREST=true
Environment=SONGBIRD_SECURITY_PROVIDER=beardog
Environment=BEARDOG_SOCKET=/run/membrane/beardog.sock
Environment=SONGBIRD_FEDERATION_PORT=7700
Environment=SONGBIRD_FEDERATION_ENABLED=true
Restart=always
RestartSec=5
MemoryMax=128M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
EOSVC

cat > /etc/systemd/system/songbird-relay.service << 'EOSVC'
[Unit]
Description=Songbird TURN Relay (Membrane Channel 2)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/membrane/songbird relay --bind 0.0.0.0 --port 3478
Restart=always
RestartSec=5
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
PrivateTmp=true
MemoryMax=128M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
EOSVC

cat > /etc/systemd/system/cascade-sense.service << 'EOSVC'
[Unit]
Description=Quorum Phase 1 — Cascade Sense (temporal.cascade with freshness)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/membrane temporal.cascade --source forgejo
Environment=GATE_NAME=golgiBody
Environment=FORGEJO_REPO_ROOT=/opt/forgejo/data/repositories
User=root
WorkingDirectory=/opt/ecoPrimals
TimeoutStartSec=300
StandardOutput=journal
StandardError=journal
EOSVC

cat > /etc/systemd/system/cascade-sense.timer << 'EOSVC'
[Unit]
Description=Quorum Phase 1 — Cascade Sense Timer

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min
RandomizedDelaySec=60

[Install]
WantedBy=timers.target
EOSVC

systemctl daemon-reload

echo "=== 8. FIREWALL ==="
# UFW or iptables — allow essential ports only
if command -v ufw &>/dev/null; then
    ufw allow 22/tcp     # SSH
    ufw allow 2222/tcp   # Forgejo SSH
    ufw allow 80/tcp     # HTTP (ACME challenge)
    ufw allow 443/tcp    # HTTPS (Caddy)
    ufw allow 51820/udp  # WireGuard
    ufw allow 7700/tcp   # SongBird federation
    ufw allow 3478/udp   # TURN relay
    ufw --force enable
fi

echo "=== 9. ENABLE SERVICES ==="
systemctl enable forgejo caddy-tls beardog-membrane songbird-membrane songbird-relay cascade-sense.timer fail2ban

echo ""
echo "========================================="
echo " golgi VPS provisioned (Sovereign Relay)"
echo "========================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Configure WireGuard keys in /etc/wireguard/wg0.conf"
echo "  2. Start WireGuard: systemctl start wg-quick@wg0"
echo "  3. rsync Forgejo repos from sporeGate mirror:"
echo "       rsync -avz sporegate:/opt/forgejo-mirror/ /opt/forgejo/data/repositories/"
echo "       chown -R git:git /opt/forgejo/data/repositories/"
echo "  4. rsync pepti depot from sporeGate:"
echo "       rsync -avz sporegate:/opt/ecoPrimals/depot/ /opt/ecoPrimals/depot/"
echo "  5. Copy relay binaries:"
echo "       rsync sporegate:/opt/ecoPrimals/depot/x86_64-unknown-linux-musl/{membrane,songbird,beardog} /opt/membrane/"
echo "       cp /opt/membrane/membrane /usr/local/bin/membrane"
echo "  6. Start services: systemctl start forgejo caddy-tls beardog-membrane songbird-membrane songbird-relay cascade-sense.timer"
echo "  7. Verify: curl https://membrane.primals.eco/health"
echo ""
echo "Estimated disk usage after restore: ~5GB of 10GB (50%)"
echo "If golgi dies, re-run this script + rsync from sporeGate."
