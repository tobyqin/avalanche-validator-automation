Avalanche Node Troubleshooting Cheatsheet
=========================================

This cheatsheet provides commands and tips for diagnosing common issues with an `avalanchego` node, whether running via Docker or `systemd`.

1\. Basic Node Status
---------------------

**Is the process running?**

-   **Docker:** `sudo docker ps | grep avalanchego` (Check if container is listed and `STATUS` is `Up`)

-   **Systemd:** `sudo systemctl status avalanchego.service` (Check for `Active: active (running)`)

**Is the node internally healthy?** (Basic process health, DB, disk, etc.)

-   **API Check:**

    ```
    curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"health.health" }'\
    -H 'content-type:application/json;' http://127.0.0.1:9650/ext/health
    ```

    -   Look for `"healthy": true`. If `false`, check the `"error"` message within `"checks"` (e.g., `subnets not bootstrapped`).

**Is the node fully synchronized (Bootstrapped)?**

-   **Check Primary Network (P, C, X chains):**

    ```
    # Check P-Chain (Repeat for "C" and "X")
    curl -X POST --data '{
        "jsonrpc":"2.0", "id":1, "method":"info.isBootstrapped",
        "params": {"chain":"P"}
    }' -H 'content-type:application/json;' http://127.0.0.1:9650/ext/info
    ```

    -   Look for `"result":{"isBootstrapped":true}` for all three chains.

-   **Check Sync Progress (via Logs):**

    -   **Docker:** `sudo docker logs -f avalanchego-fuji | grep -E 'fetching blocks|executing blocks|sync progress'`

    -   **Systemd:** `sudo journalctl -f -u avalanchego.service | grep -E 'fetching blocks|executing blocks|sync progress'`

    -   Look for `pctComplete` or `percentage` fields.

2\. Configuration Check
-----------------------

**Where are the config files?**

-   **Docker (in container):** `/etc/avalanchego/config.json` (as per our setup)

-   **Systemd (typical):** `/etc/avalanchego/config.json` or `~/.avalanchego/configs/node.json`

**Key `config.json` settings:**

-   **Network ID:** `"network-id": "fuji"` (or `"mainnet"`)

-   **Database Dir:** `"db-dir": "/data"` (Docker volume) or `/var/lib/avalanchego` (Systemd typical)

-   **HTTP Host/Port:** `"http-host": "0.0.0.0"`, `"http-port": 9650` (Defaults if omitted)

-   **Staking Port:** `"staking-port": 9651` (Default)

-   **Public IP:**

    -   **Auto-discovery (Recommended for dynamic IPs):** `"public-ip-resolution-service": "opendns"` (Ensure `"public-ip"` is *not* set)

    -   **Static (For fixed IPs):** `"public-ip": "YOUR_STATIC_PUBLIC_IP"` (Ensure `public-ip-resolution-service` is *not* set)

-   **Log Config (Example):**

    ```
    "loggingConfig": {
      "directory": "/path/to/logs", // ~/.avalanchego/logs or container path
      "logLevel": "INFO",
      "maxAge": 14 // Days to keep logs
    }

    ```

3\. Network Connectivity
------------------------

**Is the P2P port (`9651`) open externally?**

1.  **Stop Node Temporarily:**

    -   **Docker:** `sudo docker stop avalanchego-fuji`

    -   **Systemd:** `sudo systemctl stop avalanchego.service`

2.  **Listen Locally:**

    -   `sudo nc -l -p 9651 -k -v` (or `sudo ncat -v -l -p 9651 -k`)

3.  **Test Externally:** Use `https://www.yougetsignal.com/tools/open-ports/` with your EC2 Public IP and port `9651`.

    -   **Expected:** "Port ... is open". If "closed", check **AWS Security Group** inbound rules.

4.  **Cleanup:** Stop `nc`/`ncat` (Ctrl+C), restart node (`docker start` or `systemctl start`).

**Is the local firewall blocking?**

-   `sudo ufw status` (Should be `Status: inactive` unless intentionally configured).

**Is the node advertising the correct public IP?**

```
# Get node's perceived IP
curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"info.ip" }'\
-H 'content-type:application/json;' http://127.0.0.1:9650/ext/info

# Get actual public IP
curl -s http://checkip.amazonaws.com
```

-   Compare the IPs. If mismatched, restart the node (`docker restart` or `systemctl restart`).

**Is the node receiving inbound connections?**

```
# Check health details
curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"health.health" }'\
-H 'content-type:application/json;' http://127.0.0.1:9650/ext/health
```

-   Look inside `"result" > "checks" > "network" > "message" > "primary network validator health" > "ingressConnectionCount"`.

-   **Should be > 0** for a healthy validator. If 0, investigate firewall, IP, or P2P state.

**How many peers is the node connected to?**

```
curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"info.peers" }'\
-H 'content-type:application/json;' http://127.0.0.1:9650/ext/info
```

-   Look at `"numPeers"`. Should ideally be several dozen or more. Low count indicates outbound connection issues.

**Force node to re-discover peers?**

1.  Stop node.

2.  **Backup** then remove the peerlist file (e.g., `/path/to/data/fuji/peerlist/peers.json`).

3.  Start node.

**Check `iptables` (If using Docker):**

-   `sudo iptables -L -n -v` (Look for explicit blocks, check `DOCKER`, `FORWARD` chains).

-   `sudo iptables -t nat -L -n -v` (Check `PREROUTING`, `DOCKER` chains for port mapping rules).

-   **Possible Fix:** Restart Docker service `sudo systemctl restart docker` (disruptive!).

4\. System Environment
----------------------

**Is the system clock synchronized?**

```
timedatectl status
```

-   Look for `System clock synchronized: yes` and `NTP service: active`.

-   If using `chrony`: `chronyc tracking` (Check `Reference ID` and `Stratum`).

-   **Fix (if using `systemd-timesyncd` and it's stopped/masked):**

    ```
    sudo systemctl unmask systemd-timesyncd.service
    sudo systemctl start systemd-timesyncd.service
    sudo systemctl enable systemd-timesyncd.service

    ```

**Are system resources exhausted?**

-   **CPU/Memory:** `htop` (Check `%CPU`, `MEM%` for `avalanchego` process and overall system load).

-   **Disk I/O:** `iostat -dx 5` (Check `%util` for the disk where node data resides).

5\. Docker Specifics
--------------------

**View Logs:**

-   **Live:** `sudo docker logs -f avalanchego-fuji`

-   **Last N lines:** `sudo docker logs --tail 200 avalanchego-fuji`

-   **Since time:** `sudo docker logs --since 1h avalanchego-fuji`

**Restart Container:**

-   `sudo docker restart avalanchego-fuji`

**Check Container Status:**

-   `sudo docker ps -a | grep avalanchego`

**Permissions Issue (e.g., Prometheus data volume):**

-   Identify the UID the container runs as (e.g., `nobody` is `65534`, `grafana` is `472`).

-   Ensure the host directory mounted as a volume has the correct owner: `sudo chown -R 65534:65534 /path/to/prometheus/data`

6\. Systemd Specifics
---------------------

**View Logs:**

-   **Live:** `sudo journalctl -f -u avalanchego.service`

-   **All Logs:** `sudo journalctl -u avalanchego.service`

-   **Last N lines:** `sudo journalctl -n 200 -u avalanchego.service`

-   **Since time:** `sudo journalctl --since "1 hour ago" -u avalanchego.service`

**Restart Service:**

-   `sudo systemctl restart avalanchego.service`

**Check Service Status:**

-   `sudo systemctl status avalanchego.service`

**Enable/Disable Service on Boot:**

-   `sudo systemctl enable avalanchego.service`

-   `sudo systemctl disable avalanchego.service`

7\. Validator / Staking Status
------------------------------

**Get NodeID:**

```
curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"info.getNodeID" }'\
-H 'content-type:application/json;' http://127.0.0.1:9650/ext/info
```

**Get BLS Keys (Proof of Possession):**

```
# Docker
sudo docker logs avalanchego-fuji 2>&1 | grep "nodePOP"
# Systemd (search recent logs)
sudo journalctl -u avalanchego.service -n 500 | grep "nodePOP"
```

-   Copy `publicKey` and `proofOfPossession`.

**Check Uptime (Requires Active, Non-Benched Stake):**

```
curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"info.uptime" }'\
-H 'content-type:application/json;' http://127.0.0.1:9650/ext/info
```

-   Error `"node is not a validator"` means the node doesn't have an *active* stake linked *right now* (could be expired or benched).

**Check Explorer:**

-   Go to `https://subnets.avax.network/p-chain`

-   Search for your `NodeID`.

-   Check `Status` (Active/Pending/Inactive), `Online` (Yes/No), `Accessible` (Yes/No), `Benched` (Yes/No), `End Time`.

8\. Log Analysis Keywords
-------------------------

When searching logs (`docker logs` or `journalctl`), look for keywords indicating problems:

-   `ERRO`, `WARN`, `FATAL`

-   `fail`, `error`, `unable`, `couldn't`

-   `timeout`, `disconnect`, `connection refused`

-   `handshake` (TLS or P2P handshake issues)

-   `consensus` (Problems participating in consensus)

-   `peer`, `p2p`, `gossip` (Network communication issues)

-   `database` (DB corruption or access problems)

-   `config` (Issues loading configuration)

-   `resource`, `limit` (Hitting system limits)