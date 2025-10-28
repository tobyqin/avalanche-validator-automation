#  Avalanche Node Deployment Documentation

## Documentation Structure

This documentation is organized into the following sections for a structured reading experience:

### Task Overview
- [`task.md`](task.md) - Objective, requirements, automation, monitoring, constraints, and deliverables for the Avalanche testnet validator deployment.

### Steps
1. [`1_deploy_node.md`](1_deploy_node.md) - Detailed steps for deploying an Avalanche node using Ansible with Docker or systemd.
2. [`2_register_validator.md`](2_register_validator.md) - Process for obtaining AVAX, verifying sync status, and registering the node as a validator.
3. [`3_validator_monitoring.md`](3_validator_monitoring.md) - Key metrics for monitoring node health, sync status, peer connectivity, uptime, and version.
4. [`4_structured_monitoring.md`](4_structured_monitoring.md) - Comprehensive monitoring strategy including reactive vs proactive approaches, KPIs, and implementation with Prometheus/Grafana.

### Errors Fixed
- [`error_fixed.md`](error_fixed.md) - Common issues encountered during deployment and registration, with solutions and troubleshooting tips.

### Cheatsheet
- [`cheatsheet.md`](cheatsheet.md) - Quick reference for diagnosing node issues, checking status, configuration, network connectivity, and validator staking.

### Overview

This document outlines the deployment process for an Avalanche node, including automated setup, configuration management, and monitoring.

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

Last but not least, **Official Avalanche Documentation** is the best resource to learn about Avalanche, don't trust AI can solve all your problems.