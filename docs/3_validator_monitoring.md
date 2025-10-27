# Validator Monitoring Documentation

This document outlines the key metrics an operator should be concerned with and how to query them directly from the node's local API.

All commands assume you are running them *on the EC2 instance* itself, querying the local API endpoint.

---

### 1. Key Metric: Node Health & Liveness

**Concern:** Is the node process running, responding to requests, and healthy?

**How to Query (Health API - `health.getLiveness`):**
This is a quick check to see if the node is "alive".

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"health.health"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/health
```

**Response (Healthy):**

```json
{
    "jsonrpc": "2.0",
    "result": {
        "checks": {},
        "healthy": true
    },
    "id": 1
}
```

-----

### 2. Key Metric: Node Sync Status (Is it bootstrapped?)

**Concern:** Is my node fully synced with the network? A node cannot validate until it is fully synced.

**How to Query (Info API - `info.isBootstrapped`):**
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

**Response (Not Synced):**

```json
{
    "jsonrpc": "2.0",
    "result": {
        "isBootstrapped": false
    },
    "id": 1
}
```

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

Loop to verify `P`, `C`, `X` chain sync status to ensure they are all synced.

-----

### 3. Key Metric: Peer Connectivity

**Concern:** Is my node properly connected to other peers in the network? Low peer count can indicate a network configuration issue.

**How to Query (Info API - `info.peers`):**

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.peers"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

**Response (Example):**
The `numPeers` field shows the count.

```json
{
    "jsonrpc": "2.0",
    "result": {
        "numPeers": "23",
        "peers": [
            {
                "ip": "...",
                "publicIP": "...",
                "id": "NodeID-...",
                ...
            }
        ]
    },
    "id": 1
}
```

-----

### 4. Key Metric: Node Uptime

**Concern:** How long has my node been up?

**How to Query (Info API - `info.uptime`):**
```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.uptime"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "rewardingStakePercentage": "100.0000",
    "weightedAveragePercentage": "99.0000"
  }
}
```

### 5. Key Metric: Node ID

**Concern:** What is my unique Node ID? This is required to register the node as a validator.

**How to Query (Info API - `info.getNodeID`):**

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.getNodeID"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "result": {
        "nodeID": "NodeID-..."
    },
    "id": 1
}
```

-----

### 6. Key Metric: Node Version

**Concern:** What version of `avalanchego` am I running? This is crucial for planning upgrades.

**How to Query (Info API - `info.getNodeVersion`):**

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.getNodeVersion"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "result": {
        "version": "avalanche/1.13.5"
    },
    "id": 1
}
```