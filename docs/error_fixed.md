## Deployment

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

### Problem initializing networking: couldn't create IP resolver: unknown resolver: ifconfig.me

Using `ifconfig.me` as resolver will cause the problem, switch to `opendns` will fix the problem.

```json
  "public-ip-resolution-service": "opendns"
```

## Registration

### Failed to acquire AVAX faucet for testnet

It requires a small mainnet balance for spam protection.

There is 2 discount code can be used to bypass the spam protection:
1. `avalanche-academy`
2. `avalanche-academy25`

### Cannot transfer AVAX from C chain to P chain

Need to pay attention to:
1. Switch to testnet in core wallet
2. Use the Stake menu on left side, but not use the bridge button on main wallet
3. Need to leave enough balance for gas

### Need BLS public key and signature for registration

https://build.avax.network/docs/api-reference/info-api#infogetnodeid

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.getNodeID"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

### Validator node is unhealthy

```bash
ubuntu@ip:~$ curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"health.health"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/health

{"jsonrpc":"2.0","result":{"checks":{"C":{"message":...,"percentConnected":0.9999900664830199}},...,"bls":{"message":"node has the correct BLS key",..."diskspace":{"message":{"availableDiskBytes":465038942208},...,"network":{"message":{"connectedPeers":69,"primary network validator health":{"ingressConnectionCount":0,"primaryNetworkValidator":true},...,"error":"network layer is unhealthy reason: primary network validator has no inbound connections",...,"router":{"message":{"longestRunningRequest":"195.686998ms","outstandingRequests":35},...,"healthy":false},"id":1}
```

The node is highly synced, BLS key, diskspace and network are all healthy, but the node is not healthy because it has no inbound connections.

Most likely the node is not connected to any other nodes due to firewall configuration.

Now verify it by:
1. Stop the docker container `sudo docker stop avalanchego-fuji`
2. Now the port 9651 is released
3. Start a port listener `sudo nc -l -p 9651 -k -v`
4. Check port status by https://www.yougetsignal.com/tools/open-ports/
5. We can see the port 22 is open, but the port 9651 is closed

The conclusion is that the port is not accessible from outside, 99% chance is the firewall is blocking the port.

Sent a request to get it opened by email, fixed.

After that, stop the `nc` command and `sudo docker start avalanchego-fuji` to get the node back online.






