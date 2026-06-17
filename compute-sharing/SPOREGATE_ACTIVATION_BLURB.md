# Gate Deployment Template — Sovereign Mesh Node

**Template version**: 2.0.0 | **Wave**: 115
**Based on**: sporeGate live deployment (2026-06-16)

This template deploys a sovereign gate at any site, on any transport.
Fill in the parameters for your specific deployment scenario.

---

## Parameters (fill before deploying)

```toml
[gate]
name = "__GATE_NAME__"           # e.g. "sporeGate", "marshGate", "oakGate"
site = "__SITE__"                # e.g. "house1", "house2", "neighbor_alice"
role = "__ROLE__"                # "site_router" | "compute_node" | "relay"

[hardware]
vendor = "__VENDOR__"            # e.g. "GMKtec", "Beelink", "custom tower"
model = "__MODEL__"              # e.g. "NucBox M6"
cpu = "__CPU__"                  # e.g. "AMD Ryzen 5 6600H"
ram_gb = 0                       # e.g. 28
nic_count = 0                    # 1 = compute node, 2 = router
nic_wan_name = "__WAN_IF__"      # e.g. "enp1s0" (only if role=site_router)
nic_lan_name = "__LAN_IF__"      # e.g. "eno1" (only if role=site_router)

[network]
transport = "__TRANSPORT__"      # "wired_lan" | "p2p_radio" | "wireguard" | "cellular"
upstream_router = "__UPSTREAM__" # e.g. "sporeGate" (who gives this node internet?)
subnet = "__SUBNET__"            # e.g. "192.168.4.0/24" or "DHCP"
static_ip = "__IP__"             # e.g. "192.168.5.1" or "dhcp"
gateway = "__GATEWAY__"          # e.g. "192.168.4.1"

[mesh]
overlay_ip = "__WG_IP__"         # e.g. "10.13.37.5"
hub_endpoint = "157.230.3.183:51820"  # golgiBody
family_seed = "/etc/membrane/family/family.key"
```

---

## Deployment Scenarios

### Scenario A: Site Router (like sporeGate)

A new sovereignty boundary with two NICs — one WAN, one LAN.
Serves DHCP/DNS to its local site. NATs traffic to upstream.

**When to use**: Deploying at a new site with its own switch and local devices.

### Scenario B: Compute Node (single NIC)

A NUC or tower that plugs into an existing site's switch.
Gets DHCP from site router. Runs primals. No routing duties.

**When to use**: Adding compute capacity to an existing site.

### Scenario C: Remote Node (WireGuard only)

A NUC at a friend's house or institute. Internet via their ISP.
Joins the mesh via WireGuard overlay. No physical LAN connection to sovereign fabric.

**When to use**: Geo-distributed compute. The node has its own internet but joins your mesh.

---

## Step 0: Pre-Flight Checks

Run these BEFORE changing any network config:

```bash
# Detect actual interface names (kernel names vary by hardware)
ip -j link show | jq -r '.[] | select(.link_type=="ether") | .ifname'

# Record them — DO NOT assume enp1s0/eno1/enp2s0
WAN_IF="$(FILL_IN)"
LAN_IF="$(FILL_IN)"

# Check for IP conflicts on target address
arping -c 3 -I "$LAN_IF" "$TARGET_IP" 2>/dev/null

# Check for existing DHCP servers on LAN (only if site_router)
sudo timeout 10 tcpdump -i "$LAN_IF" -c 3 "port 67 or port 68" 2>/dev/null

# Check port 53 (DNS) availability
ss -tlnp | grep :53
# If systemd-resolved is listening: sudo systemctl disable --now systemd-resolved

# Verify internet connectivity (via whatever upstream is available)
ping -c 3 8.8.8.8
```

---

## Step 1: OS Install

Pop!_OS 22.04 or Ubuntu Server 24.04. Key requirements:
- systemd-networkd for wired networking
- WiFi via NetworkManager (OOB fallback only)
- nftables (not iptables)

```bash
sudo apt update && sudo apt install -y \
  nftables dnsmasq curl jq wireguard-tools \
  networkd-dispatcher
```

---

## Step 2: Network Configuration

### For Site Router (2 NICs):

Create `/etc/systemd/network/10-wan.network`:
```ini
[Match]
Name=__WAN_IF__

[Network]
DHCP=yes

[DHCPv4]
UseDNS=no
UseRoutes=yes
RouteMetric=100
```

Create `/etc/systemd/network/20-lan.network`:
```ini
[Match]
Name=__LAN_IF__

[Network]
Address=__STATIC_IP__/__PREFIX__
DHCPServer=yes
IPForward=yes

[DHCPServer]
PoolOffset=100
PoolSize=150
DNS=__STATIC_IP__
Router=__STATIC_IP__
DefaultLeaseTimeSec=86400
MaxLeaseTimeSec=172800
EmitDNS=yes
EmitRouter=yes
RapidCommit=yes
```

### For Compute Node (1 NIC, DHCP client):

Create `/etc/systemd/network/10-lan.network`:
```ini
[Match]
Name=__LAN_IF__

[Network]
DHCP=yes

[DHCPv4]
UseDNS=yes
UseRoutes=yes
RouteMetric=100
```

### For Remote Node (WireGuard only):

Keep existing network config (their ISP handles internet).
Only add WireGuard interface (Step 5).

---

## Step 3: IP Forwarding (Site Router only)

Create `/etc/sysctl.d/99-router.conf`:
```ini
net.ipv4.ip_forward = 1
net.ipv4.conf.all.forwarding = 1
net.ipv6.conf.all.forwarding = 0

net.ipv4.conf.default.rp_filter = 0
net.ipv4.conf.all.rp_filter = 0
```

Apply: `sudo sysctl -p /etc/sysctl.d/99-router.conf`

---

## Step 4: Firewall & NAT (Site Router only)

Create `/etc/nftables.conf`:
```nft
#!/usr/sbin/nft -f
flush ruleset

table ip filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif "lo" accept
        ct state established,related accept
        iifname "__LAN_IF__" accept
        icmp type echo-request accept
        tcp dport 22 accept
        udp dport 51820 accept
        log prefix "nft-drop: " drop
    }
    chain forward {
        type filter hook forward priority 0; policy drop;
        ct state established,related accept
        iifname "__LAN_IF__" oifname "__WAN_IF__" accept
        iifname "wg0" accept
        drop
    }
    chain output {
        type filter hook output priority 0; policy accept;
    }
}

table ip nat {
    chain postrouting {
        type nat hook postrouting priority 100; policy accept;
        oifname "__WAN_IF__" masquerade
    }
}

table ip6 filter {
    chain forward {
        type filter hook forward priority 0; policy drop;
        drop
    }
}
```

Enable: `sudo systemctl enable --now nftables`

---

## Step 5: WireGuard Mesh Overlay

All gate types join the WireGuard overlay for primal-to-primal communication.

Create `/etc/wireguard/wg0.conf`:
```ini
[Interface]
Address = __WG_IP__/24
PrivateKey = __GENERATED_PRIVATE_KEY__
ListenPort = 51820

[Peer]
# golgiBody (mesh hub)
PublicKey = __GOLGI_PUBLIC_KEY__
Endpoint = 157.230.3.183:51820
AllowedIPs = 10.13.37.0/24
PersistentKeepalive = 25
```

Generate keys and enable:
```bash
wg genkey | tee /etc/wireguard/private.key | wg pubkey > /etc/wireguard/public.key
chmod 600 /etc/wireguard/private.key
sudo systemctl enable --now wg-quick@wg0
```

---

## Step 6: DNS (Site Router only)

Create `/etc/dnsmasq.conf`:
```ini
interface=__LAN_IF__
bind-dynamic
listen-address=127.0.0.1

no-dhcp-interface=__LAN_IF__

server=1.1.1.1
server=8.8.8.8
server=9.9.9.9

cache-size=1000

local=/primals.local/
domain=primals.local

address=/__GATE_NAME__.primals.local/__STATIC_IP__

no-resolv
```

---

## Step 7: NetworkManager Exclusion

Prevent NM from interfering with systemd-networkd interfaces.

Create `/etc/NetworkManager/conf.d/99-unmanage-wired.conf`:
```ini
[keyfile]
unmanaged-devices=interface-name:__WAN_IF__;interface-name:__LAN_IF__
```

Restart: `sudo systemctl restart NetworkManager`

---

## Step 8: WiFi as OOB Management (Site Router)

Keep WiFi connected to an available network for emergency access:
```bash
nmcli device wifi connect "__SSID__" password "__PSK__"
nmcli connection modify "__SSID__" connection.autoconnect yes
nmcli connection modify "__SSID__" ipv4.route-metric 600
```

---

## Step 9: Membrane Bootstrap

```bash
# Fetch membrane binary
curl -fsSL https://membrane.primals.eco/depot/x86_64-unknown-linux-musl/membrane \
  -o ~/bin/membrane && chmod +x ~/bin/membrane

# Fetch primal depot (13 binaries)
~/bin/membrane plasmid.fetch --source wan

# Bootstrap gate identity
~/bin/membrane gate.bootstrap __GATE_NAME__
```

---

## Step 10: Primal Services (systemd)

Create `/etc/systemd/system/membrane-nucleus.target` and individual service units.
Each primal gets a unit file:

```ini
[Unit]
Description=ecoPrimal: __PRIMAL_NAME__
After=network.target

[Service]
Type=simple
ExecStartPre=/bin/mkdir -p /run/membrane
ExecStart=__PRIMAL_BINARY__ server --socket /run/membrane/__PRIMAL_NAME__.sock
Environment=FAMILY_ID=__FAMILY_ID__
Environment=FAMILY_SEED=__FAMILY_SEED_PATH__
Environment=MEMBRANE_GATE_NAME=__GATE_NAME__
Environment=MEMBRANE_MESH_HUB_ID=golgiBody
Environment=MEMBRANE_MESH_PEERS=157.230.3.183:7700
Restart=on-failure
RestartSec=3

[Install]
WantedBy=membrane-nucleus.target
```

Enable all:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now membrane-nucleus.target
```

---

## Step 11: RustDesk Remote Access

```bash
# Install
sudo dpkg -i rustdesk-*.deb  # or: sudo apt install ./rustdesk-*.deb

# Configure sovereign relay (one command)
sudo rustdesk --config "__RUSTDESK_CONFIG_STRING__"

# Enable at boot
sudo systemctl enable rustdesk
```

---

## Step 12: Verify

```bash
# Network
ip addr show                    # Correct IPs assigned
ip route                        # Default route via WAN (metric 100)
ping 8.8.8.8                    # Internet works
ping 10.13.37.1                 # WireGuard to golgiBody works

# Services
systemctl is-active membrane-nucleus.target   # active
systemctl is-active nftables                  # active
systemctl is-active dnsmasq                   # active (site_router only)
systemctl is-active wg-quick@wg0             # active

# Primals
~/bin/membrane gate.status      # All 13 primals alive

# Mesh
~/bin/membrane mesh.peers       # golgiBody reachable

# Remote access
systemctl is-active rustdesk    # active
```

---

## Cellular Failover (Optional)

For WAN redundancy without new hardware, add a phone hotspot as backup:

```bash
# USB tether: just plug phone and enable tethering
sudo cp configs/30-cellular-failover.network /etc/systemd/network/
sudo systemctl restart systemd-networkd

# Verify: ip route should show usb0 with metric 500
# Test: sudo ip link set __WAN_IF__ down && ping 8.8.8.8
```

See `configs/deploy-cellular-failover.sh` for full setup.

---

## Rollback

If anything breaks:
1. **Compute node**: Unplug ethernet. Node is isolated, LAN unaffected.
2. **Site router**: Unplug router. Reconnect upstream directly to switch.
   All devices fall back to upstream's DHCP.
3. **Remote node**: Stop WireGuard. Node leaves mesh. Its local internet unaffected.

---

## Transport-Specific Notes

### Wired LAN (Cat6/SFP+)
- Plug into CRS310 or site switch
- Gets DHCP automatically from site router
- Sub-1ms latency, full 2.5G/10G bandwidth
- Affinity: 0.9 (same_segment)

### P2P Radio (MikroTik/Ubiquiti)
- Configure radio pair as transparent L2 bridge
- Far-end NUC sees same LAN as local devices
- 2-3ms latency, 400-1200 Mbps depending on radio
- Affinity: 0.6-0.8 (neighborhood)

### WireGuard Overlay
- Node uses its own ISP for internet
- Joins mesh via encrypted tunnel to golgiBody
- 30-200ms latency depending on ISP path
- Affinity: 0.3-0.4 (remote)

### Cellular (Mint Mobile hotspot)
- Backup WAN only (metric 500)
- 30-100ms latency, 50-200 Mbps
- Activates automatically when primary WAN fails
- Affinity: 0.4 (cellular_failover)

---

## Historical: sporeGate Deployment Notes

The original sporeGate deployment (2026-06-16) encountered several issues
documented in `SPOREGATE_AAR_WAVE115.md`. Key lessons incorporated into
this template:

1. **Interface naming**: Always detect with `ip link show` first (Step 0)
2. **Port 53 conflict**: Disable systemd-resolved before dnsmasq (Step 0)
3. **IPv6 forwarding**: Default OFF — prevents iPhone stalling (Step 3)
4. **rp_filter**: Must be 0 for multi-subnet bridge routing (Step 3)
5. **NetworkManager conflicts**: Exclude wired interfaces explicitly (Step 7)
6. **Secondary IP for migration**: If replacing existing router, add old IP temporarily
7. **Cross-subnet proxy ARP**: Only needed when bridge carries multiple subnets

For the full story, see `SPOREGATE_AAR_WAVE115.md`.
