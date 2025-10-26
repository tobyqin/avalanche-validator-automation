### No package matching 'docker-ce' is available

When `dry-run` ansible with `ansible-playbook --check main.yml` it said `No package matching 'docker-ce' is available`

Actually it is not true, because dry run will not import the repo and key so the repo state is incorrect.

### Unsupported parameters for (community.docker.docker_compose_v2) module: restarted

This is because the unexpected parameter `restarted` was set in docker compose template, remove it will fix the problem.

### Avalanche configuration file updated but not applied

We have to add a ansible handler to handle config changes and docker compose changes.

```bash
...
TASK [avalanche-validator : Template avalanchego config file] ***********************************************************************
changed: [fuji-node]

TASK [avalanche-validator : Template docker-compose file] ***************************************************************************
changed: [fuji-node]

TASK [avalanche-validator : Deploy and start avalanchego container] *****************************************************************
changed: [fuji-node]

RUNNING HANDLER [avalanche-validator : Restart avalanchego] *************************************************************************
changed: [fuji-node]
...
```

### problem initializing networking: couldn't create IP resolver: unknown resolver: ifconfig.me

Using `ifconfig.me` as resolver will cause the problem, switch to `opendns` will fix the problem.

```json
  "public-ip-resolution-service": "opendns"
```
