## Objective

Deploy: Avalanche testnet validator (Dockerized or native) on AWS EC2.

Lesson Learned: See in [Error Fixed](./error_fixed.md).

## Automate by Ansible+Docker

1. Install Ansible
2. Implement node deployment playbook at `ansible` directory
3. Run `ansible-playbook main.yml` in `ansible` directory

### Why Ansible

- https://docs.ansible.com/

Pros:
1. Automation & Repeatability, we can automate the entire process (installing dependencies, configuring the node, and starting the node and more) with a playbook (one command).
2. Idempotency, we can run the playbook multiple times and ensure the state is consistent.
3. Infrastructure as Code, the entire setup is defined as human-readable code, we can check it into GitHub, run it on a CI/CD pipeline, and version control.
4. Agentless, we don't need to install any agent on target machine when using Ansible.
5. Orchestration, we can define multiple playbook and tasks to orchestrate the deployment process.

Key considerations:
1. Correct state handling, the owner should know when to `notify` or `trigger` a task, don't trust AI too much.
2. Managing Secrets, need to find a centralized way to store secrets securely, it should not be part of source code.
3. Testing(Dry Runs): Never run new playbook on production without testing, always using `--check` to do dry run.

### Why Docker

- https://build.avax.network/docs/nodes/run-a-node/using-docker

Pros:
1. Easy & Fast Upgrades, this is crucial for urgent network updates and security patches.
2. Consistent Environment, the node is running in a predictable and official environment, regardless of your infrastructure.
3. Clean Automation, just managing a `docker-compose.yml` file is enough.
4. Portable & Isolation, the config, the volume are easy to back up or migrate.

Key considerations:
1. Data persistence, we must mount the database directory to persist docker volume.
2. Log management, docker's default logging driver will write logs to the host disk, the avalanchego node is very chatty and will fill up the disk then crash. We must configure a log rotation in docker compose file.
3. Networking performance, the default bridge network adds a small layer of NAT, for high performance production nodes, we could use `host` mode to gain raw network performance.
4. Docker Daemon as a SPOF, if docker service is crashed or need to be restarted, the node will be unavailable.


## Playbook Logs

```bash
$ ansible-playbook  main.yml

PLAY [Deploy Avalanche Fuji Validator] **********************************************************************************************

TASK [Gathering Facts] **************************************************************************************************************
ok: [fuji-node]

TASK [Update apt cache and install prerequisites] ***********************************************************************************
ok: [fuji-node]

TASK [Install Docker GPG key] *******************************************************************************************************
ok: [fuji-node]

TASK [Add Docker repository] ********************************************************************************************************
ok: [fuji-node]

TASK [Install Docker] ***************************************************************************************************************
ok: [fuji-node]

TASK [Install Python Docker library (for Ansible modules)] **************************************************************************
ok: [fuji-node]

TASK [Ensure Docker service is started] *********************************************************************************************
ok: [fuji-node]

TASK [avalanche-validator : Create avalanche data directory] ************************************************************************
ok: [fuji-node]

TASK [avalanche-validator : Create avalanche config directory] **********************************************************************
ok: [fuji-node]

TASK [avalanche-validator : Template avalanchego config file] ***********************************************************************
ok: [fuji-node]

TASK [avalanche-validator : Template docker-compose file] ***************************************************************************
ok: [fuji-node]

TASK [avalanche-validator : Deploy and start avalanchego container] *****************************************************************
changed: [fuji-node]

PLAY RECAP **************************************************************************************************************************
fuji-node                  : ok=12   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## Verify Deployment

### Manual Steps

1. SSH into EC2 instance
2. Run `docker ps` to verify validator is running
3. Run `docker logs [validator-container-name]` to verify validator is syncing

```bash
ubuntu@ip-172-31-33-253:~$ docker logs avalanchego-fuji
[10-25|17:15:11.897] INFO node/node.go:150 initializing node {"version": "avalanchego/1.13.5", "commit": "37747dd9bfdd97a4917c69327a36ad22115ef5f8", "nodeID": "NodeID-...", "stakingKeyType": "ECDSA", "nodePOP": {"publicKey":"...","proofOfPossession":"...."}, ...}}
[10-25|17:15:11.898] INFO node/node.go:913 initializing NAT
[10-25|17:15:11.898] INFO node/node.go:931 initializing API server
[10-25|17:15:11.899] INFO server/server.go:133 API created {"allowedOrigins": ["*"]}
[10-25|17:15:11.899] INFO node/node.go:1281 initializing metrics API
...
[10-25|17:15:12.031] INFO server/server.go:245 adding route {"url": "/ext/health", "endpoint": ""}
[10-25|17:15:12.031] INFO server/server.go:245 adding route {"url": "/ext/health", "endpoint": "/readiness"}
[10-25|17:15:12.031] INFO server/server.go:245 adding route {"url": "/ext/health", "endpoint": "/health"}
[10-25|17:15:12.031] INFO server/server.go:245 adding route {"url": "/ext/health", "endpoint": "/liveness"}
[10-25|17:15:12.031] INFO node/node.go:1023 adding the default VM aliases
[10-25|17:15:12.032] INFO node/node.go:1166 initializing VMs
[10-25|17:15:12.032] INFO node/node.go:1297 skipping admin API initialization because it has been disabled
[10-25|17:15:12.032] INFO node/node.go:1354 initializing info API
[10-25|17:15:12.032] INFO server/server.go:245 adding route {"url": "/ext/info", "endpoint": ""}
[10-25|17:15:12.032] INFO node/node.go:1523 initializing chain aliases
[10-25|17:15:12.033] INFO node/node.go:1550 initializing API aliases
[10-25|17:15:12.033] INFO node/node.go:1327 skipping profiler initialization because it has been disabled
[10-25|17:15:12.033] INFO node/node.go:889 initializing chains
...
[10-25|17:15:12.037] INFO chains/manager.go:1492 starting chain creator
[10-25|17:15:12.037] INFO node/node.go:647 writing process context {"path": "/root/.avalanchego/process.json"}
[10-25|17:15:12.044] INFO node/node.go:674 API server listening {"uri": "http://[::]:9650"}
...
[10-25|17:15:17.705] INFO <P Chain> bootstrap/bootstrapper.go:397 starting to fetch blocks {"numKnownBlocks": 99, "numAcceptedBlocks": 1, "numMissingBlocks": 100}
[10-25|17:15:42.036] INFO health/worker.go:261 check started passing {"name": "health", "name": "network", "tags": ["application"]}
[10-25|17:16:04.102] INFO <P Chain> bootstrap/bootstrapper.go:644 fetching blocks {"numFetchedBlocks": 240051, "numTotalBlocks": 242483, "eta": "0s", "pctComplete": 99}
[10-25|17:16:08.615] INFO <P Chain> bootstrap/storage.go:138 compacting database before executing blocks...
[10-25|17:16:11.064] INFO <P Chain> bootstrap/storage.go:195 executing blocks {"numToExecute": 242483}
[10-25|17:16:56.796] INFO <P Chain> bootstrap/storage.go:252 executing blocks {"numExecuted": 44166, "numToExecute": 242483, "eta": "3m59s", "pctComplete": 18.21}
```

From the logs above, we can get the following information:
- Node version
- Node ID
- BLS public key
- BLS proof of possession (signature)
- Syncing status

### Wait for syncing completed

This is the most important query to run after deployment.

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.isBootstrapped",
    "params": {
        "chain":"P"
    }
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
````

**Response (Synced):**

```json
{
    "jsonrpc": "2.0",
    "result": {
        "isBootstrapped": true
    },
    "id": 1
}
```

### Automated testing

We can simplify the checks above by running a playbook on local machine.

```bash
cd ansible
ansible-playbook monitor.yml
```

Example output:
```bash

PLAY [Monitor Avalanche Node Status] **********************************************************

TASK [Gathering Facts] ************************************************************************
ok: [fuji-node]

TASK [Copy node deployment verification script] ***********************************************
changed: [fuji-node]

TASK [Run node deployment verification script (pre-check)] ************************************
ok: [fuji-node]

TASK [Display deployment verification results] ************************************************
ok: [fuji-node] => {
    "msg": [
        "Verifying basic Avalanche node deployment...",
        "Target node: 127.0.0.1:9650",
        "--------------------------------------------------",
        "✓ Node version: avalanchego/1.13.5",
        "✓ Node healthy: True",
        "✓ Node ID: NodeID-...",
        "✓ Node POP Public Key: ...",
        "✓ Node POP Proof: ...",
        "--------------------------------------------------",
        "✓ Basic node deployment verification PASSED"
    ]
}

TASK [Copy node sync status verification script] **********************************************
ok: [fuji-node]

TASK [Run node sync status verification script] ***********************************************
ok: [fuji-node]

TASK [Display sync status verification results] ***********************************************
ok: [fuji-node] => {
    "msg": [
        "Verifying Avalanche node sync status...",
        "Target node: 127.0.0.1:9650",
        "--------------------------------------------------",
        "✓ P chain synced: True",
        "✓ C chain synced: True",
        "✓ X chain synced: True",
        "✓ Number of peers: 1878",
        "--------------------------------------------------",
        "✓ Node sync status verification PASSED"
    ]
}

PLAY RECAP ************************************************************************************
fuji-node                  : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```