# RustDesk Sovereign Relay — One-Command Config

**Relay**: golgi VPS (157.230.3.183)
**Ports**: 21115 (NAT test), 21116 (rendezvous), 21117 (relay)

---

## The Config String

```
=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye
```

---

## Onboarding Any New Device

```bash
# Linux:
pkexec rustdesk --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"

# Windows (admin cmd):
rustdesk.exe --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"

# macOS:
sudo ./RustDesk --config "=0nI9E1NWJHc2UnbBlGSU9kbRRnRwUFS1ElcIp3MHZWarE1KWRGRVdVQP5Eb0VnI6ISeltmIsIiI6ISawFmIsIyM4EjLz4CMzIjL3UTMiojI5FGblJnIsIyM4EjLz4CMzIjL3UTMiojI0N3boJye"
```

After applying, the device registers on the sovereign relay and can see all other gates.

---

## What This Encodes

- ID Server: 157.230.3.183
- Relay Server: 157.230.3.183
- Key: utlNOAWUDdV+Q+ifG3zHrQ5HU0FtQnOTHiAnu6prV7Q=

---

## Security Note

The config string contains a public verification key (not a secret). Sharing it allows
devices to register on the relay, but connecting still requires the per-device password.
Safe to put on USB kits, blurbs, and onboarding docs.

---

## Deployed To

| Gate | Status |
|------|--------|
| eastGate | Configured |
| sporeGate | Configured |
| northGate | Configured |
| fieldGate | TODO (offline) |
| golgi | IS the relay |
