Okay, here is a more concise version:

### What Was Done & Why

* **Automated Deployment:** Used Ansible & Docker for repeatable, consistent IaC deployment (Node, Prometheus, Grafana).
* **Config Management:** Templated configs (`.j2`), used Ansible handlers for reliable restarts on change.
* **Funding:** Used alternative faucet (Core Wallet + code) due to mainnet requirement; bridged C->P chain for staking.
* **Registration:** Staked via Core Wallet UI using NodeID & BLS PoP (from logs).
* **Log Rotation:** Configured in Docker Compose (size) & `config.json` (time) to prevent disk full.
* **Monitoring:** Deployed Prometheus/Grafana via Ansible then official approach, scraped node metrics (`:9650`), imported official dashboards.

### Issues Encountered / Discoveries

* **Faucet:** Official faucet blocked (mainnet balance); used Core Wallet + code instead.
* **Node Config:** Startup failures fixed by changing `public-ip-resolution-service` (`ifconfig.me` -> `opendns`).
* **BLS PoP:** Retrieved keys directly from startup logs.
* **Firewall:** Node unhealthy (`no inbound connections`); diagnosed with `nc` & port checker, confirmed need for Security Group rule for port `9651`.
* **Staking Duration:** **Key Discovery:** Fuji minimum stake is << 14 days, contradicting assessment info; re-staked correctly after short stake expired.
* **Prometheus Permissions:** Crash loop fixed by setting correct host directory owner UID (`65534`) via Ansible.
* **Host Metrics:** Dockerized Prometheus misses machine metrics; official dashboard requires `node_exporter` (`:9100`) for full visibility.

### What Was Learned

* **Automation is Key:** Ansible saved time, ensured repeatability.
* **Verify Assumptions:** Testnet params (staking duration) differ from mainnet/docs.
* **Troubleshooting:** Systematically addressed network, config, and permission issues for node operation.
* **Monitoring:** App + System metrics (`node_exporter`) needed for full picture.
* **Avalanche Arch:** Practical understanding of P/C chains, ports (`9650`/`9651`), PoP.