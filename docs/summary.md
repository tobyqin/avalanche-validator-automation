Okay, here is a more concise version:

### What Was Done & Why

* **Automated Deployment:** Used Ansible & Docker for repeatable, consistent IaC deployment (Node, Prometheus, Grafana).
* **Config Management:** Templated configs (`.j2`), used Ansible handlers for reliable restarts on change.
* **Funding:** Used alternative faucet (Core Wallet + code) due to mainnet requirement; bridged C->P chain for staking.
* **Registration:** Staked via Core Wallet UI using NodeID & BLS PoP (from logs).
* **Testing:** Tested with `curl` & Python scripts, integrated into Ansible playbook, ready for CICD pipeline.
* **Monitoring:** Deployed Prometheus/Grafana via Ansible then official approach, scraped node metrics (`:9650`), imported official dashboards.
* **Log Rotation:** Configured in Docker Compose (size) & `config.json` (time) to prevent disk full.

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
* **Monitoring:** Practical understanding Business + Machine metrics (`node_exporter`) for Avalanche.
* **Avalanche Arch:** Practical understanding of P/C/X chains, ports (`9650`/`9651`), PoP. Reading official docs for key concepts.
* **Touching Avalanche:** Hand-on experience with Avalanche applications, core app, explorer, wallet, etc.