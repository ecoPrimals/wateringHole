# sporeGate Activation — LAN Periplasm Router

**Hardware**: GMKtec NucBox M6 (Ryzen 7 6800H, 32GB RAM, 2x 2.5G RJ45)
**Role**: Sovereign LAN perimeter — NAT, firewall, DHCP, DNS, VPN, NUCLEUS primals
**OS**: Pop!_OS 22.04 (Ubuntu-based, systemd-networkd for wired networking)
**Date**: 2026-06-16 (deployed and hardened)

---

## Physical Wiring

```
ATT Gateway LAN port ──RJ45──► sporeGate enp1s0 (WAN interface)
sporeGate eno1 (LAN interface) ──RJ45──► CRS310 RJ45 port (pure L2 bridge)
CRS310 ──10G/2.5G──► eastGate, fieldGate, towers, APs
```

After wiring: CRS310 is a pure L2 bridge. sporeGate handles all L3.

---

## Interface Naming (important)

Linux kernel names vary by hardware. On the NucBox M6:
- **enp1s0** — WAN (PCI slot 1, facing ATT gateway)
- **eno1** — LAN (onboard NIC, facing CRS310 bridge)

If `enp2s0` doesn't exist, check `ip link show` — you likely have `eno1`.
The USB deployment kit references `enp2s0` but actual kernel names win.

---

## Deployed Configuration

### 1. systemd-networkd

`/etc/systemd/network/10-wan.network`:
```ini
[Match]
Name=enp1s0

[Network]
DHCP=yes

[DHCPv4]
UseDNS=no
UseRoutes=yes
RouteMetric=100
```

`/etc/systemd/network/20-lan.network`:
```ini
[Match]
Name=eno1

[Network]
Address=192.168.4.1/22
Address=192.168.4.3/22
DHCPServer=yes
IPForward=yes

[DHCPServer]
PoolOffset=100
PoolSize=150
DNS=192.168.4.1
Router=192.168.4.1
DefaultLeaseTimeSec=3600
MaxLeaseTimeSec=7200
```

Note: `192.168.4.3/22` is a secondary address for backward compatibility
with clients that cached the old CRS310 DHCP lease pointing to .3.

### 2. Kernel Parameters

`/etc/sysctl.d/99-router.conf`:
```
net.ipv4.ip_forward = 1
net.ipv4.conf.all.forwarding = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.conf.default.rp_filter = 0
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.eno1.proxy_arp = 1
```

rp_filter disabled: required for cross-subnet proxy routing (192.168.1.x
devices on the CRS310 bridge that still have ATT-range IPs from Eero mesh).

### 3. Firewall & NAT (nftables)

`/etc/nftables.conf`:
```nft
flush ruleset

table ip filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif "lo" accept
        ct state established,related accept
        iifname "eno1" accept
        icmp type echo-request accept
        tcp dport 22 accept
        udp dport 51820 accept
        log prefix "nft-drop: " drop
    }
    chain forward {
        type filter hook forward priority 0; policy drop;
        ct state established,related accept
        iifname "eno1" oifname "enp1s0" accept
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
        oifname "enp1s0" masquerade
    }
}

table ip mangle {
    chain prerouting {
        type filter hook prerouting priority -150; policy accept;
        iifname "enp1s0" ip daddr 192.168.1.0/24 ip daddr != 192.168.1.233 meta mark set 0x1
    }
}
```

The mangle table marks de-NATed return packets destined for 192.168.1.x
clients so policy routing can direct them back through eno1 (the bridge).

### 4. DNS (dnsmasq)

`/etc/dnsmasq.conf`:
```
interface=eno1
bind-interfaces
listen-address=192.168.4.1
listen-address=192.168.4.3
listen-address=127.0.0.1
no-dhcp-interface=eno1
server=1.1.1.1
server=8.8.8.8
cache-size=1000
```

### 5. Cross-Subnet Routing (networkd-dispatcher)

`/etc/networkd-dispatcher/routable.d/50-sporegate-routes.sh`:
```bash
#!/bin/bash
if [ "$IFACE" != "eno1" ]; then exit 0; fi

ip neigh add proxy 192.168.1.254 dev eno1 2>/dev/null
ip route add 192.168.1.254/32 dev enp1s0 src 192.168.1.233 2>/dev/null
ip route replace 192.168.1.0/24 dev eno1 metric 50 2>/dev/null
ip rule add fwmark 1 lookup 100 priority 100 2>/dev/null
ip route add 192.168.1.0/24 dev eno1 table 100 2>/dev/null

nft add table ip mangle 2>/dev/null
nft flush chain ip mangle prerouting 2>/dev/null || \
  nft add chain ip mangle prerouting { type filter hook prerouting priority -150 \; }
nft add rule ip mangle prerouting iifname "enp1s0" ip daddr 192.168.1.0/24 \
  ip daddr != 192.168.1.233 meta mark set 0x1
```

This handles Eero mesh clients that have 192.168.1.x addresses (from ATT
DHCP) but are physically connected via the CRS310 bridge on eno1.

### 6. NetworkManager Exclusion

`/etc/NetworkManager/conf.d/99-unmanage-wired.conf`:
```ini
[keyfile]
unmanaged-devices=interface-name:enp1s0;interface-name:eno1;interface-name:enp2s0
```

NetworkManager still manages WiFi (for fallback). Wired = systemd-networkd only.

### 7. Remote Access (RustDesk)

- **ID**: `1871544996`
- **Relay**: golgiBody (`157.230.3.183:21116`)
- **Service**: `rustdesk.service` (enabled at boot, headless mode)
- **Key**: Obtain from operator / golgiBody hbbs public key

---

## Service Boot Order

| Service | Enabled | Role |
|---------|---------|------|
| systemd-networkd | yes | WAN DHCP, LAN static + DHCP server |
| nftables | yes | Firewall + NAT + mangle |
| dnsmasq | yes | DNS caching (port 53) |
| ssh | yes | Remote management |
| rustdesk | yes | GUI remote access relay |
| NetworkManager | yes | WiFi only (wired interfaces excluded) |
| networkd-dispatcher | yes | Post-routable route injection |

---

## CRS310 Configuration (Pure L2 Bridge)

After factory reset:
- All 8 RJ45 + 2 SFP+ ports in a single bridge
- Management IP: `192.168.4.2/24` (static)
- No DHCP server, no NAT, no firewall, no routing
- Bridge STP/RSTP: enabled (loop protection)
- REST API password set (sticker pwd for admin)

---

## Lessons Learned

1. **Interface naming**: Always verify with `ip link show`. Deployment kits
   should use udev rules or systemd `.link` files for stable naming.

2. **rp_filter**: Must be 0 when routing for multiple subnets on one physical
   segment. The kernel drops "impossible" source IPs by default.

3. **Cross-subnet proxy ARP**: When Eero mesh clients on 192.168.1.x share
   the same physical bridge as 192.168.4.x devices, sporeGate must:
   - Answer ARPs for 192.168.1.254 (the ATT gateway) on eno1
   - Use policy routing (fwmark + ip rule) to return de-NATed traffic

4. **Dnsmasq vs systemd-resolved**: Disable systemd-resolved first or dnsmasq
   can't bind port 53. (`sudo systemctl disable --now systemd-resolved`)

5. **Secondary IP for lease migration**: Old DHCP clients may cache the
   previous gateway IP. Adding it as a secondary address prevents DNS outage.

---

## Cloning This Gate

To deploy another sporeGate on similar hardware:

```bash
# 1. Install Pop!_OS or Ubuntu Server
# 2. Clone this repo
git clone https://github.com/ecoPrimals/wateringHole.git

# 3. Copy configs (adjust interface names)
sudo cp configs/systemd-network/* /etc/systemd/network/
sudo cp configs/nftables.conf /etc/nftables.conf
sudo cp configs/dnsmasq.conf /etc/dnsmasq.conf
sudo cp configs/sysctl-router.conf /etc/sysctl.d/99-router.conf
sudo cp configs/networkd-dispatcher/* /etc/networkd-dispatcher/routable.d/

# 4. Enable services
sudo systemctl enable --now systemd-networkd nftables dnsmasq
sudo systemctl disable systemd-resolved

# 5. Install RustDesk
sudo dpkg -i rustdesk-*.deb
# Configure relay in ~/.config/rustdesk/RustDesk2.toml

# 6. Reboot and verify
sudo reboot
```

---

## Next Steps (Wave 115+)

- [ ] ATT IP Passthrough (removes double-NAT)
- [ ] WireGuard tunnel to golgiBody
- [ ] NUCLEUS primals: bearDog, skunkBat, songBird, loamSpine
- [ ] Omada AP integration (replace Eero, unify on 192.168.4.0/22)
- [ ] plasmidBin local depot (LAN binary distribution)
- [ ] Monitoring dashboard (skunkBat → Grafana or native)
