# cellMembrane — Self-Hosted GitHub Actions Runners

**From**: primalSpring (coordinator)
**To**: cellMembrane team
**Date**: May 26, 2026
**Wave**: 50
**Priority**: High — directly unblocks covalent HPC evolution

---

## Context

plasmidBin's CI pipeline runs on GitHub Actions free-tier hosted runners
(2,000 minutes/month). We hit a GitHub Actions incident today that silently
dropped all workflow triggers — no builds, no validation, no harvest. The
pipeline was dead until GitHub resolved it. This is unacceptable for a
sovereign ecosystem.

Additionally, the daily full-sweep cron was consuming ~$77/month in gross
Actions usage (120 runner-min/day rebuilding all primals). We've optimized
this to a lightweight tag-checker (~$25/month estimate), but the dependency
on GitHub runners remains.

## Requirement: 2+ Self-Hosted Runners on LAN

### Why 2 gates minimum

If the hosting company goes down, or one gate loses power/network, the other
must continue running CI independently. A single self-hosted runner creates
a single point of failure that's worse than GitHub's cloud runners.

### Architecture

```
GitHub Cloud                     Inner Membrane LAN
┌─────────────────┐              ┌──────────────────────────┐
│ Actions coord.  │──dispatch──▶ │ eastGate runner          │
│                 │──dispatch──▶ │ southGate runner         │
│ GitHub Releases │◀──upload───  │                          │
└─────────────────┘              │ cellMembrane Forgejo     │
                                 │   (repo mirrors + CI)    │
                                 └──────────────────────────┘
                                    ▲              ▲
                                    │  LAN sync    │
                                    └──────────────┘
```

### Setup checklist (per gate)

1. **Install GitHub Actions runner agent**
   ```bash
   # Get registration token
   gh api orgs/ecoPrimals/actions/runners/registration-token --jq '.token'

   # Download and configure runner
   mkdir ~/actions-runner && cd ~/actions-runner
   curl -o actions-runner.tar.gz -L \
     https://github.com/actions/runner/releases/latest/download/actions-runner-linux-x64-2.321.0.tar.gz
   tar xzf actions-runner.tar.gz
   ./config.sh --url https://github.com/ecoPrimals \
     --token <TOKEN> \
     --name "$(hostname)-runner" \
     --labels "self-hosted,linux,x86_64" \
     --work _work
   ```

2. **Install Rust toolchain + musl cross-compilation**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
   rustup target add x86_64-unknown-linux-musl
   rustup target add aarch64-unknown-linux-musl
   rustup target add armv7-unknown-linux-musleabihf

   # Cross-linkers
   sudo apt install -y musl-tools gcc-aarch64-linux-gnu gcc-arm-linux-gnueabihf lld

   # Cargo cross-linker config
   mkdir -p ~/.cargo
   cat >> ~/.cargo/config.toml <<'TOML'
   [target.aarch64-unknown-linux-musl]
   linker = "aarch64-linux-gnu-gcc"

   [target.armv7-unknown-linux-musleabihf]
   linker = "arm-linux-gnueabihf-gcc"
   TOML
   ```

3. **Install gh CLI** (needed for release uploads)
   ```bash
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
     | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
     | sudo tee /etc/apt/sources.list.d/github-cli.list
   sudo apt update && sudo apt install -y gh
   ```

4. **Register as systemd service**
   ```bash
   cd ~/actions-runner
   sudo ./svc.sh install
   sudo ./svc.sh start
   sudo systemctl enable actions.runner.ecoPrimals.$(hostname)-runner.service
   ```

5. **Verify runner is online**
   ```bash
   gh api orgs/ecoPrimals/actions/runners --jq '.runners[] | "\(.name) \(.status)"'
   ```

### Workflow migration (primalSpring will handle)

Once both runners report `online`, primalSpring will update `auto-harvest.yml`:

```yaml
# Before
runs-on: ubuntu-latest

# After
runs-on: [self-hosted, linux, x86_64]
```

Self-hosted runner minutes are free — they don't count against the 2,000
included minutes or any spending cap.

## Lockout Prevention

The `plasmidbin` CLI is a standalone Rust binary. If GitHub is fully down:

```bash
# On any gate with the plasmidBin repo:
cargo run -p plasmidbin -- validate .
cargo run -p plasmidbin -- harvest --arch x86_64 --source /path/to/binaries
```

No GitHub dependency. Forgejo on cellMembrane holds repo mirrors and can run
validation/harvest independently.

## Evolution Path

| Phase | GitHub | Forgejo | Who leads |
|-------|--------|---------|-----------|
| Now | hosted runners | mirror only | GitHub |
| Next | self-hosted on LAN | mirror + Woodpecker CI | GitHub (Forgejo fallback) |
| Covalent | public mirror | primary CI + releases | Forgejo |

The target state: Forgejo leads, GitHub mirrors. CI runs entirely on the
mesh. Zero external CI dependency. Full sovereignty.

## Dependencies

- 2 gates on LAN with stable network between them
- SSH access to both gates for runner installation
- `PLASMIDBIN_HARVEST_PAT` secret (already exists in GitHub, needs to be
  set as env var on self-hosted runners or configured in runner .env)
- Forgejo already mirroring repos (confirm with cellMembrane)

## Acceptance Criteria

- [ ] 2 runners show `online` in `gh api orgs/ecoPrimals/actions/runners`
- [ ] Manual workflow dispatch runs on self-hosted runner
- [ ] `plasmidbin validate .` passes on both gates
- [ ] If one runner goes offline, the other picks up jobs
