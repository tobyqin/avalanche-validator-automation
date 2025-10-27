# Structured Monitoring Documentation

## 1. Why We Monitor: A Two-Layer Strategy

Monitoring a validator is not just about observing it; it's about actively protecting the stake and rewards. A professional SRE/DevOps strategy divides monitoring into two distinct categories: Reactive and Proactive.

### The Role of the Testnet Explorer (Reactive Monitoring)

The [Fuji Testnet Explorer](https://subnets-test.avax.network/p-chain) is the public-facing, on-chain "source of truth." It is a **Reactive** tool.

  * **What It Does:** It tells you the **result** of your node's performance, as seen by the rest of the network. It shows lagging indicators like:
      * `Status` (Active, Pending)
      * `Uptime` (Your final reward-bearing score)
      * `Time to Unlock` (Your stake duration)
  * **Its Limitation:** The Explorer is like a customer calling to say your website is down. By the time `uptime` drops, the damage is done, and you have already missed consensus requests and lost potential rewards. **It tells you *what* happened, not *why* it's happening.**

### The Necessity of Active Monitoring (Proactive Monitoring)

Active Monitoring is your internal, private, real-time "heart-rate monitor." It is a **Proactive** tool.

  * **What It Does:** It tells you the **cause** of a potential problem by monitoring the internal state of your server and the node application. It shows leading indicators like:
      * "Is the CPU about to max out?"
      * "Is the disk almost full?"
      * "Is the node disconnected from its peers?"
  * **Its Purpose:** To alert you to a problem *before* it affects your on-chain uptime. **It allows you to fix a problem *before* you lose money.**

**Conclusion:** A professional validator operator **must** use Active Monitoring to protect the on-chain results that the Explorer displays.

-----

## 2. What We Monitor: Key Performance Indicators (KPIs)

We organize our KPIs into three tiers, from the host system to the on-chain business logic.

### Tier 1: Host System Metrics (The Foundation)

If the server fails, the node fails. These metrics warn of hardware or OS-level failures.

  * **Disk Usage:**
      * **Why:** The blockchain database grows constantly. A full disk will crash the node and can corrupt the database. This is the most common cause of catastrophic node failure.
  * **CPU Usage:**
      * **Why:** `avalanchego` is CPU-intensive. Sustained high CPU (100%) will cause the node to miss consensus responses, directly lowering your uptime.
  * **Memory Usage:**
      * **Why:** If the node runs out of memory, the Linux Out-of-Memory (OOM) Killer will terminate the process, causing immediate downtime.
  * **Network Accessibility (Port `9651`):**
      * **Why:** As we discovered, if the **P2P Port `9651`** is blocked by a firewall (like an AWS Security Group), no other nodes can connect *to* you. This will cause the `network` health check to fail and will eventually destroy your uptime.

### Tier 2: Node Application Metrics (The Heartbeat)

These metrics are queried directly from the node's JSON-RPC API on port `9650`. They tell you if the `avalanchego` process itself is healthy.

  * **API Health:**
      * **Why:** This is the primary "is it alive?" check. If the `health.health` method returns `unhealthy`, the node is internally aware of a problem (like the firewall issue).
  * **Sync Status (Bootstrapped):**
      * **Why:** A node cannot validate if it is not fully synced with the P, X, and C chains. If this ever flips to `false`, the node has a serious network or peer problem.
  * **Peer Count:**
      * **Why:** A healthy node should be connected to dozens of peers. If this number drops to a low single-digit, it signals a network partition or configuration issue.

### Tier 3: Business & Chain Metrics (The Result)

These metrics confirm your node is performing its job and earning rewards.

  * **Validator Uptime:**
      * **Why:** This is your "score." The network requires \>80% uptime to earn rewards. This metric should be monitored to ensure it never trends downward.
  * **Validator Status:**
      * **Why:** You need to know if your node is `Pending` (waiting to start), `Active` (validating and earning), or `Benched` (temporarily kicked out for poor performance).

-----

## 3. How We Monitor: Implementation

This is how to query the Tier 2 Application Metrics from your EC2 instance's command line.

### 1. Check API Health (The "Heartbeat")

This check should return `{"healthy":true}`. If not, the `checks` object will contain the *reason* it is unhealthy (e.g., the "no inbound connections" error).

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"health.health"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/health
```

### 2. Check P-Chain Sync Status

This is the most important sync check for a validator. It **must** return `{"isBootstrapped":true}`.

```bash
curl -X POST --data '{
    "jsonrpc":"2.0", "id":1, "method" :"info.isBootstrapped",
    "params": {"chain":"P"}
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

### 3. Check Peer Count

This should return a healthy number of peers (e.g., \> 20).

```bash
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.peers"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

### 4. Check Validator Status (Tier 3)

The simplest and safest way to check your on-chain status (Uptime, Active) is to use the **Testnet Explorer** by searching for your `NodeID`:
`https://subnets-test.avax.network/p-chain`

### Recommended Professional Architecture

For a true production environment, you would not rely on manual `curl` commands. The standard SRE/DevOps solution is to:

1.  **Prometheus:** A time-series database. `avalanchego` natively exposes a Prometheus-compatible endpoint at `http://127.0.0.1:9650/ext/metrics` which includes all Tier 1 and Tier 2 metrics.
2.  **Grafana:** A visualization tool to build dashboards from the Prometheus data.
3.  **Alertmanager:** A tool to send proactive alerts (e.g., `"Disk usage > 85%"`) to Slack, PagerDuty, or email *before* the node fails.

See more about this implementation in `monitoring` folder.