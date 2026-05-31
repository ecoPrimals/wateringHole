# Forgejo VPS Hooks — K-Derm Diderm Relay Chain

Server-side hooks for the three-node K-Derm diderm envelope. The push flow
traverses each layer with proper bond-type degradation:

```
Gate ──covalent──→ golgiBody-inner (cis: receives)
                       │
                       │ metallic bond (post-receive webhook)
                       ▼
                   peptidoglycan (structural: sync + impulse cascade)
                       │
                       │ ionic bond (SSH relay)
                       ▼
                   golgiBody-ext (trans: ships to extracellular)
                       │
                       │ weak bond (git push)
                       ▼
                   GitHub (extracellular linear ledger)
```

## Scripts

| Script | Runs On | Bond | Purpose |
|--------|---------|------|---------|
| `pepti-sync-relay.sh` | peptidoglycan | Metallic→Ionic | Pull from Forgejo, run impulse cascade, relay to outer |
| `ext-github-push.sh` | golgiBody-ext | Ionic→Weak | Push to GitHub from the trans (shipping) face |
| `impulse-relay-hook.sh` | peptidoglycan | — | Standalone impulse detection + songbird relay |
| `setup-push-mirrors.sh` | golgiBody-inner | — | Legacy: Forgejo push mirror setup (pre-diderm) |

## K-Derm Diderm Flow

### Full relay chain (target architecture)

1. Gate pushes to Forgejo on golgiBody-inner (covalent SSH)
2. Forgejo post-receive webhook notifies peptidoglycan
3. `pepti-sync-relay.sh` on peptidoglycan:
   - Pulls from Forgejo (metallic: inner→structural)
   - Runs impulse cascade (detect + relay pending impulses)
   - SSHs to golgiBody-ext, triggers `ext-github-push.sh`
4. `ext-github-push.sh` on golgiBody-ext:
   - Pushes to GitHub (weak: outer→extracellular)
   - golgiBody-ext holds the only GitHub SSH write credentials

### SSH key placement (bonding model)

| Node | GitHub SSH | Forgejo SSH | Bond Types |
|------|-----------|-------------|------------|
| golgiBody-inner | None (revoked) | Yes (Forgejo owns it) | Covalent, Metallic |
| peptidoglycan | None (revoked) | Yes (pull from Forgejo) | Metallic |
| golgiBody-ext | **Yes (push to GitHub)** | Yes (pull from Forgejo) | Ionic, Weak |

Only the outer membrane (trans face) has extracellular write access.

## Setup

### peptidoglycan

```bash
# Ensure wateringHole is synced
cd /opt/ecoPrimals/infra/wateringHole
git pull --ff-only forgejo main

# Install scripts
chmod +x hooks/forgejo/pepti-sync-relay.sh
chmod +x hooks/forgejo/impulse-relay-hook.sh
```

### golgiBody-ext

```bash
# Clone wateringHole (if not present)
cd /opt/ecoPrimals/infra
git clone ssh://git@git.primals.eco:2222/ecoPrimals/wateringHole.git

# Ensure GitHub remote exists (origin should point to GitHub)
cd wateringHole
git remote get-url origin  # should be github.com

# Install push script
chmod +x hooks/forgejo/ext-github-push.sh
```

### golgiBody-inner (Forgejo webhook)

In Forgejo → wateringHole repo settings → Webhooks:
- URL: `http://157.230.209.218:3001/hooks/pepti-sync-relay`
- Content type: `application/json`
- Trigger: Push events
- Branch filter: `main`
