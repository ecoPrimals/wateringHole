# Forgejo VPS Hooks — waterFall Mediator

Server-side hooks for the golgiBody Forgejo instance. These make the VPS
the sovereign mediator in waterFall: gates push to Forgejo, Forgejo
auto-mirrors to GitHub, and impulse cascades fire automatically.

## Files

| Script | Purpose |
|--------|---------|
| `impulse-relay-hook.sh` | Post-receive handler — detects new impulses and relays via songbird |
| `setup-push-mirrors.sh` | One-time setup — creates Forgejo→GitHub push mirrors for all repos |

## Push Mirror Setup (One-Time)

1. Verify golgiBody has SSH connectivity to `github.com`
2. Run `setup-push-mirrors.sh --dry-run` to preview
3. Run `setup-push-mirrors.sh` to create mirrors
4. Verify with `membrane mirror.push-list ecoPrimals/<repo>` per repo

## Impulse Relay Setup

1. Deploy `impulse-relay-hook.sh` to golgiBody
2. Set up a lightweight webhook listener (port 3001) that calls the script
3. In Forgejo → wateringHole repo settings → Webhooks:
   - URL: `http://localhost:3001/hooks/impulse-relay`
   - Content type: `application/json`
   - Trigger: Push events
   - Branch filter: `main`

## Architecture

```
Gate ──push──→ Forgejo ──push-mirror──→ GitHub (external ledger)
                  │
                  └──webhook──→ impulse-relay-hook.sh
                                    │
                                    ├─ potential.sense (detect)
                                    └─ songbird relay (propagate)
```
