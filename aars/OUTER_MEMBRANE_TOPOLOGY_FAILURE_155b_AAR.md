# AAR: Outer Membrane Topology Failure — RustDesk NAT Rate-Limit Collapse

**Date**: 2026-07-28 | **Gate**: sporeGate (incident), golgiBody (root cause) | **Wave**: 155b
**Scope**: Full RustDesk outer membrane failure for house1 LAN gates, root cause analysis, architectural separation, recovery
**Duration**: ~2 hours diagnosis, 5 minutes to fix once root cause identified
**Severity**: P1 — complete loss of remote access to house1 gates (sporeGate, eastGate, northGate)

---

## EXECUTIVE SUMMARY

All house1 RustDesk gates went offline while flockGate (different WAN) remained connected. After extensive debugging across client versions, configs, and protocol layers, the root cause was a **silent iptables rate-limit DROP** on golgiBody that punished NAT-clustered gates. Multiple gates behind one WAN IP collectively exceeded per-source-IP UDP thresholds. The firewall silently discarded all their traffic — no logs, no errors, no indication of the block.

This AAR documents the failure, the diagnostic red herrings, and the architectural separation implemented to prevent recurrence.

---

## WHAT HAPPENED

### Symptom
- northGate could connect to flockGate (WAN: 24.128.136.74) but all house1 gates (sporeGate, eastGate, northGate — WAN: 162.226.225.148) showed as offline to each other
- RustDesk client logs showed `register_pk... due to key not confirmed` in an infinite loop
- Server-side hbbs logs showed zero `update_pk` entries for house1 gates

### Root Cause Chain

```
golgiBody iptables INPUT chain:
  Rule 4: UDP dpt:21116 → recent SET name:rustdesk_udp
  Rule 5: UDP dpt:21116 → recent UPDATE 10s hitcount:30 → DROP

house1 topology:
  sporeGate  ─┐
  eastGate   ─┼─ NAT ─→ WAN 162.226.225.148 ─→ golgiBody:21116
  northGate  ─┘

3 gates × ~10 UDP heartbeats/10s = 30 packets/10s per source IP
                                    ↑ exactly at the DROP threshold
```

The firewall saw all house1 traffic as a single flood source and silently dropped everything. flockGate, alone behind its own WAN IP, stayed well under the limit.

### Why It Was Hard to Find

1. **Silent DROP** — no iptables LOG target, no REJECT (which would produce ICMP unreachable), no server-side error. The packets simply vanished.
2. **Version red herring** — RustDesk 1.3.x on sporeGate had zero network connections (separate bug: dnsmasq was dead, causing init-time DNS hangs). This made it look like a client version incompatibility.
3. **Protocol red herring** — RustDesk 1.4.x clients connected TCP but failed to register. This looked like a 1.4.x-vs-1.1.x protocol mismatch (a real issue, but not the primary one).
4. **Key confirmation loop** — Client logs showed `key not confirmed` repeatedly, suggesting a key mismatch problem. In reality, the server simply never received the registration because the firewall ate it.

### Secondary Issue: Dead dnsmasq

sporeGate's `/etc/resolv.conf` pointed to `127.0.0.1` (dnsmasq) as primary DNS, but dnsmasq was disabled and not running. This caused RustDesk 1.3.x to hang during initialization (likely DNS lookup for API server check), producing zero outbound connections. This masked the real firewall issue by making it look like a client-side binary problem.

---

## DIAGNOSTIC TIMELINE

| Time | Action | Finding |
|------|--------|---------|
| T+0 | northGate reports LAN gates offline, flockGate works | Topology-specific failure |
| T+15m | Check client configs, key_confirmed state | Key confirmed = false, but server key present |
| T+30m | Try RustDesk 1.4.9, 1.4.8, 1.3.9, 1.3.8 on sporeGate | 1.3.x: zero connections. 1.4.x: TCP connects but no registration |
| T+45m | strace 1.4.x client | Sends UDP register_pk, tries TCP to port 21114 (API) |
| T+60m | strace 1.3.x client | Zero network syscalls — binary hangs in init |
| T+75m | Check dnsmasq | Dead. Port 53 unbound. Fix: `systemctl enable --now dnsmasq` |
| T+80m | Restart 1.3.8 with DNS fixed | Now connects! But still `key not confirmed` loop |
| T+90m | **tcpdump on golgiBody** | **SMOKING GUN**: server responds to flockGate (24.128.136.74), ignores ALL packets from 162.226.225.148 |
| T+95m | Check iptables | Rate limit: 30 UDP/10s per IP. House1 (3 gates, 1 NAT) exceeds it |
| T+100m | Raise limits, flush recent tables | **ALL 9 house1 peers register within 4 seconds** |

---

## WHAT WE FIXED

### 1. RUSTDESK_MEMBRANE Firewall Chain (golgiBody)

Created a dedicated iptables chain that isolates RustDesk traffic handling from all primals services:

```
INPUT chain:
  Rule 2: TCP 21114-21118 → jump RUSTDESK_MEMBRANE
  Rule 3: UDP 21116      → jump RUSTDESK_MEMBRANE
  (primals rules below — HTTPS, SSH, Forgejo — completely separate)

RUSTDESK_MEMBRANE chain:
  1. ACCEPT ESTABLISHED,RELATED
  2. UDP 21116 recent SET rd_membrane_udp
  3. UDP 21116 recent UPDATE 10s hitcount:120 → DROP
  4. TCP 21114-21118 NEW recent SET rd_membrane_tcp
  5. TCP 21114-21118 NEW recent UPDATE 10s hitcount:60 → DROP
  6. ACCEPT TCP 21114-21118
  7. ACCEPT UDP 21116
```

**NAT-aware limits**: 120 UDP/10s supports ~10 gates behind one NAT. 60 TCP new connections/10s is generous for legitimate use while still blocking scanners.

### 2. dnsmasq Re-enabled (sporeGate)

```bash
systemctl enable --now dnsmasq
```

Sovereign DNS chain restored: dnsmasq (port 53) → stubby (DoT) → upstream resolvers.

### 3. Duplicate Process Cleanup (golgiBody)

Killed stale manual-run hbbs/hbbr processes that were competing with systemd-managed services for port bindings.

### 4. Architectural Separation Documented

Cursor rule at `.cursor/rules/outer-membrane-rustdesk.mdc` codifies the separation:

| Concern | Outer Membrane (RustDesk) | Primals |
|---------|--------------------------|---------|
| Route | Public internet via default gateway | WireGuard wg0 (10.13.37.x) |
| Firewall | `RUSTDESK_MEMBRANE` chain | HTTPS rate-limit + ufw |
| Auth | Server key + per-gate password | Capability IPC / TLS |
| Failure domain | Independent | Independent |

---

## SKUNKBAT TARGETS — Future Detection

This failure class should be flaggable earlier. Key signals:

### 1. "Works from one WAN, fails from another" → NAT amplification

If a service works from one external IP but not another, and the failing IP has multiple clients behind NAT, check per-source-IP rate limits immediately. The rate limit may be counting aggregate traffic from all NATted clients as a single flood source.

### 2. "Silent DROP" → Always prefer REJECT or LOG before DROP

Silent DROPs are invisible to both client and server. For services we own (not public-facing scan targets), `LOG --log-prefix "RD_MEMBRANE_DROP: "` before DROP would make this visible in dmesg/journal. Consider adding LOG targets in the RUSTDESK_MEMBRANE chain for debugging.

### 3. "Client loops on register_pk" → Check server-side first

The client-side `key not confirmed` loop is a symptom, not a cause. The diagnostic shortcut: immediately check if the hbbs server logs `update_pk` for the client. If not, the packet isn't arriving — look at the network path, not the client config.

### 4. "Zero connections from a known-working binary" → Check local DNS

If a binary that should be making network calls shows zero sockets in `ss`, check if local DNS resolution is broken. Many applications do DNS lookups during init (API checks, update checks) and silently fail if DNS times out.

### 5. dnsmasq Health Check

Add to gate health monitoring: if `/etc/resolv.conf` points to localhost but nothing binds port 53, flag immediately.

---

## ARCHITECTURAL INSIGHT: Membrane Independence

The core learning: **the outer membrane (RustDesk) must be architecturally independent from the services it provides access to**. If the same firewall rules, DNS chain, or network path serves both RustDesk and primals, a failure in one domain cascades to the other — and you lose the ability to remotely fix the problem.

The separation is now:

```
User → RustDesk (public internet, RUSTDESK_MEMBRANE chain, server key + password)
     → Gate desktop
     → WireGuard (10.13.37.x, separate tunnel)
     → Primals (capability IPC, TLS, separate firewall rules)
```

If WireGuard dies, RustDesk still works. If RustDesk's firewall rules need tuning, primals are untouched. The outer membrane is the sovereign fallback — the human hand reaching through.

---

## CURRENT STATE

- All house1 gates (sporeGate, eastGate, northGate) online and registered
- flockGate remains online (was never affected)
- 10 total peers registered in hbbs DB
- `relay.primals.eco` resolves via Cloudflare wildcard to 157.230.3.183
- `https://relay.primals.eco` info page active (passphrase-gated bootstrap)
- `RUSTDESK_MEMBRANE` chain saved via netfilter-persistent
- dnsmasq enabled and persistent on sporeGate
- Cursor rule `.cursor/rules/outer-membrane-rustdesk.mdc` codifies the pattern

*Outer membrane recovered. Topology trap documented. Separation achieved. — sporeGate, wave 155b*
