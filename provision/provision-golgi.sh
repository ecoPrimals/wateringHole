#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# provision-golgi.sh — Rebuild golgi VPS from a fresh Debian 12 droplet
#
# This script provisions the "thin edge" relay layer of the Sovereign Relay
# Architecture. golgi serves as the public ingress surface, running only:
#
#   - Forgejo    (sovereign git forge, SSH on :2222, HTTP on :3000)
#                Bare repos are SHALLOW (depth=1) — full history lives on
#                sporeGate at /opt/forgejo-mirror/. Pushes work normally;
#                periodic re-shallowing keeps disk thin.
#   - bearDog    (TLS gateway: ACME cert for primals.eco on :443/:80)
#   - Caddy      (TLS for remaining subdomains on :8443, depot file_server)
#   - membrane   (temporal.cascade — Forgejo→sporeGate sync + freshness)
#   - songBird   (mesh federation hub + TURN relay)
#   - bearDog    (crypto identity + BTSP security provider + ACME TLS gateway)
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
#   4. rsync SHALLOW Forgejo repos from sporeGate mirror:
#        bash provision-golgi-shallow-repos.sh   (or run inline — see bottom of file)
#      OR restore full history then shallow later:
#        rsync -avz /opt/forgejo-mirror/ root@$GOLGI_IP:/opt/forgejo/data/repositories/
#   5. rsync pepti depot:
#        rsync -avz /opt/ecoPrimals/depot/ root@$GOLGI_IP:/opt/ecoPrimals/depot/
#   6. Start services: systemctl start forgejo caddy-tls beardog-membrane beardog-sporeprint songbird-membrane songbird-relay cascade-sense.timer

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
# bearDog owns :443/:80 for primals.eco + www.primals.eco (ACME gateway).
# Caddy handles remaining domains on :8443/:8880 with existing LE certs.
# Caddy also serves sporePrint static content on :8091 (bearDog upstream).
{
    email ops@primals.eco
    http_port 8880
    https_port 8443
    storage file_system /caddy
}

# sporePrint static site — bearDog upstream (HTTP only, localhost)
:8091 {
    handle /lab/spores/* {
        root * /opt/ecoPrimals/sporePrint/spores
        file_server browse
        try_files {path} {path}/ {path}/index.html
    }
    handle {
        root * /opt/ecoPrimals/sporePrint/public
        file_server
        try_files {path} {path}/ /index.html
    }
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

git.primals.eco {
    reverse_proxy localhost:3000
}

lab.primals.eco {
    reverse_proxy 10.13.37.2:7780
}
EOCADDY

echo "=== 5. INSTALL RUSTDESK SERVER ==="
RUSTDESK_VERSION="1.1.14"
curl -sL "https://github.com/rustdesk/rustdesk-server/releases/download/${RUSTDESK_VERSION}/rustdesk-server-linux-amd64.zip" \
    -o /tmp/rustdesk-server.zip
unzip -o /tmp/rustdesk-server.zip -d /tmp/rustdesk-extract
cp /tmp/rustdesk-extract/amd64/hbbs /opt/membrane/hbbs
cp /tmp/rustdesk-extract/amd64/hbbr /opt/membrane/hbbr
chmod +x /opt/membrane/hbbs /opt/membrane/hbbr
rm -rf /tmp/rustdesk-server.zip /tmp/rustdesk-extract

mkdir -p /opt/membrane/rustdesk
echo "RustDesk identity will be restored from pepti depot (see NEXT STEPS)"

echo "=== 6. PULL BINARIES FROM SPOREGATE DEPOT ==="
echo "Binaries are deployed from pepti depot on sporeGate."
echo "After WireGuard is up, run:"
echo "  rsync -avz sporegate:/opt/ecoPrimals/depot/x86_64-unknown-linux-musl/{membrane,songbird,beardog} /opt/membrane/"
echo "  rsync -avz sporegate:/opt/ecoPrimals/depot/ /opt/ecoPrimals/depot/"
echo "  cp /opt/membrane/membrane /usr/local/bin/membrane"

echo "=== 7. WIREGUARD ==="
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

echo "=== 8. SYSTEMD SERVICES ==="

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
Description=Channel 3 TLS Surface (Caddy — subdomains on :8443)
After=network-online.target beardog-sporeprint.service
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/membrane/caddy run --config /etc/membrane/Caddyfile
Environment=HOME=/root
Restart=always
RestartSec=5
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

cat > /etc/systemd/system/beardog-sporeprint.service << 'EOSVC'
[Unit]
Description=bearDog ACME gateway (golgiBody — primals.eco sovereign TLS)
After=network-online.target petaltongue-sporeprint.service
Wants=network-online.target
Requires=petaltongue-sporeprint.service

[Service]
Type=simple
ExecStart=/opt/membrane/beardog server --bind-mode tcp --port 9999 --socket /run/membrane/beardog-gw.sock
Environment=BEARDOG_GATEHOUSE_MODE=true
Environment=BEARDOG_ACME_DOMAINS=primals.eco,www.primals.eco
Environment=BEARDOG_ACME_EMAIL=ops@primals.eco
Environment=BEARDOG_GATEWAY_UPSTREAM=127.0.0.1:8091
Environment=BEARDOG_DATA_DIR=/var/lib/beardog
Environment=GATE_NAME=golgiBody
AmbientCapabilities=CAP_NET_BIND_SERVICE
Restart=always
RestartSec=5

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

cat > /etc/systemd/system/hbbs-membrane.service << 'EOSVC'
[Unit]
Description=RustDesk Rendezvous Server (cellMembrane — remote.primals.eco)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=simple
ExecStart=/bin/sh -c '/opt/membrane/hbbs -r $(hostname -I | awk "{print \\$1}")'
WorkingDirectory=/opt/membrane/rustdesk
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/membrane/rustdesk
MemoryMax=64M
CPUQuota=25%

[Install]
WantedBy=multi-user.target
EOSVC

cat > /etc/systemd/system/hbbr-membrane.service << 'EOSVC'
[Unit]
Description=RustDesk Relay Server (cellMembrane — remote.primals.eco)
After=network-online.target hbbs-membrane.service
Wants=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=simple
ExecStart=/opt/membrane/hbbr
WorkingDirectory=/opt/membrane/rustdesk
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/membrane/rustdesk
MemoryMax=64M
CPUQuota=25%

[Install]
WantedBy=multi-user.target
EOSVC

systemctl daemon-reload

echo "=== 9. FIREWALL ==="
# UFW or iptables — allow essential ports only
if command -v ufw &>/dev/null; then
    ufw allow 22/tcp     # SSH
    ufw allow 2222/tcp   # Forgejo SSH
    ufw allow 80/tcp     # HTTP (bearDog ACME + HTTPS redirect)
    ufw allow 443/tcp    # HTTPS (bearDog TLS gateway — primals.eco)
    ufw allow 8443/tcp   # HTTPS (Caddy — membrane/git/lab subdomains)
    ufw allow 51820/udp  # WireGuard
    ufw allow 7700/tcp   # SongBird federation
    ufw allow 3478/udp   # TURN relay
    ufw allow 21115/tcp  # RustDesk NAT test
    ufw allow 21116/tcp  # RustDesk ID registration
    ufw allow 21116/udp  # RustDesk NAT probe
    ufw allow 21117/tcp  # RustDesk relay
    ufw --force enable
fi

echo "=== 10. FORGEJO RE-SHALLOW MAINTENANCE ==="

cat > /usr/local/bin/forgejo-reshallow << 'EOSHALLOW'
#!/usr/bin/env bash
set -euo pipefail
REPO_BASE="/opt/forgejo/data/repositories"
systemctl stop forgejo.service
SAVED=0
for repo_path in $(find "$REPO_BASE" -maxdepth 2 -name "*.git" -type d | sort); do
  before=$(du -sm "$repo_path" | awk '{print $1}')
  tmpdir=$(mktemp -d)
  if git clone --bare --depth=1 "file://${repo_path}" "${tmpdir}/shallow.git" 2>/dev/null; then
    [ -d "${repo_path}/hooks" ] && cp -a "${repo_path}/hooks" "${tmpdir}/shallow.git/hooks"
    rm -rf "$repo_path"
    mv "${tmpdir}/shallow.git" "$repo_path"
    chown -R git:git "$repo_path"
    after=$(du -sm "$repo_path" | awk '{print $1}')
    delta=$((before - after))
    SAVED=$((SAVED + delta))
  fi
  rm -rf "$tmpdir"
done
systemctl start forgejo.service
echo "forgejo-reshallow: saved ~${SAVED}M"
EOSHALLOW
chmod +x /usr/local/bin/forgejo-reshallow

cat > /etc/systemd/system/forgejo-reshallow.service << 'EOSVC'
[Unit]
Description=Re-shallow Forgejo bare repos (Thin Relay maintenance)
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/forgejo-reshallow
TimeoutStartSec=600
StandardOutput=journal
StandardError=journal
EOSVC

cat > /etc/systemd/system/forgejo-reshallow.timer << 'EOSVC'
[Unit]
Description=Monthly re-shallow of Forgejo bare repos

[Timer]
OnCalendar=monthly
RandomizedDelaySec=3600

[Install]
WantedBy=timers.target
EOSVC

echo "=== 11. ENABLE SERVICES ==="
systemctl enable forgejo caddy-tls beardog-membrane beardog-sporeprint songbird-membrane songbird-relay cascade-sense.timer hbbs-membrane hbbr-membrane fail2ban forgejo-reshallow.timer

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
echo "  6. Restore RustDesk identity from depot:"
echo "       cp /opt/ecoPrimals/depot/rustdesk/id_ed25519* /opt/membrane/rustdesk/"
echo "  7. Add remote.primals.eco DNS record:"
echo "       knotc zone-begin primals.eco"
echo "       knotc zone-set primals.eco remote.primals.eco. 300 A <NEW_VPS_IP>"
echo "       knotc zone-commit primals.eco"
echo "  8. Start services: systemctl start forgejo caddy-tls beardog-membrane beardog-sporeprint songbird-membrane songbird-relay cascade-sense.timer hbbs-membrane hbbr-membrane"
echo "  9. Verify: curl https://primals.eco && curl https://membrane.primals.eco:8443/health"
echo ""
echo "Estimated disk usage after restore: ~3.5GB of 10GB (35%)"
echo "If golgi dies, re-run this script + rsync from sporeGate."
echo ""
echo "MAINTENANCE:"
echo "  - forgejo-reshallow.timer runs monthly to keep repos at depth=1"
echo "  - Full history lives on sporeGate at /opt/forgejo-mirror/"
echo "  - Manual re-shallow: forgejo-reshallow"
