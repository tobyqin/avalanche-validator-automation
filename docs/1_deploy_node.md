## Objective

Deploy: Avalanche testnet validator (Dockerized or native) on AWS EC2.

Lesson Learned: See in [Error Fixed](./error_fixed.md).

## Automate by Ansible+Docker

1. Install Ansible
2. Implement node deployment playbook at `ansible` directory
3. Run `ansible-playbook main.yml` in `ansible` directory

### Why Ansible

### Why Docker

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

We can simplify the checks above by running a script.

```
curl -s https://raw.githubusercontent.com/ava-labs/avalanche-ops/main/scripts/check_node.sh | bash
```
