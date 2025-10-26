# Avalanche Fuji Validator Automation (Technical Assessment)

This repository contains the automation scripts and documentation to deploy, operate, and monitor an Avalanche Fuji Testnet Validator, as required for the practical assessment.

The entire setup and deployment process is automated using **Ansible** and **Docker**.

## Core Objectives

* **Deploy:** Automate the deployment of an `avalanchego` node (Dockerized) on a target EC2 instance.
* **Automate:** Use Ansible to provide a repeatable, idempotent deployment process.
* **Monitor:** Identify and document key operational metrics.

## Tech Stack

* **Automation:** Ansible
* **Containerization:** Docker & Docker Compose
* **Base OS (Assumed):** Ubuntu 20.04/22.04 (or any Debian-based Linux with `apt`)

## Repository Structure

```bash
.
├── README.md               # This file
├── MONITORING.md           # Monitoring documentation (Deliverable)
├── docs                    # Documentation
└── ansible                 # Ansible playbook
```

## How to Use

#### 1. Prerequisites (On local machine)

* [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html)
* Clone this repository:
    ```bash
    git clone https://github.com/tobyqin/avalanche-validator-automation.git
    cd avalanche-validator-automation/ansible
    ```

#### 2. Configure Inventory (Local & Secret)

Edit the `inventory.ini` file. Replace `ansible_host` with the your IP address, and ensure `ansible_user` is correct (e.g., `ubuntu`, `ec2-user`).

#### 3. Run the Playbook

This command will connect to the EC2 instance, install Docker, and deploy the validator node.

```bash
ansible-playbook deploy.yml
```

The deploy playbook will install Docker and Docker Compose, and then deploy the validator node and verify that the node is running, but it will not verify the is synced.

To verify that the node is synced and get extra information, use the following command:

```bash
ansible-playbook monitor.yml
```



The playbook will handle all steps for deploying the validator node.

## Post-Deployment: Manual Steps

Ansible automates the *deployment*, but *registering* as a validator involves manual steps related to funds and timing.

### Step 1: Wait for Node to Sync

  * The node will take several hours to fully bootstrap (sync) with the Fuji testnet.
  * You can check the status using the monitoring queries. The node is synced when `info.isBootstrapped` returns `true`.
  * **See `MONITORING.md` for the exact command.**

### Step 2: Get Faucet Funds

  * **C-Chain Address:** You need a wallet (e.g., MetaMask) configured for the Fuji C-Chain.
  * **Faucet:** Go to [https://faucet.avax.network/](https://faucet.avax.network/) to acquire test AVAX. (Note: This may require a mainnet balance for anti-spam).
  * **Cross-Chain Transfer:** Use the [Avalanche Core Wallet](https://core.app/) to transfer your test AVAX from the **C-Chain** to the **P-Chain**. Validator staking happens on the P-Chain.

### Step 3: Register as Validator

Once your node is **fully synced** (Step 1) and you have **funds on the P-Chain** (Step 2):

1.  **Get Your NodeID:** SSH into your EC2 instance and run:

    ```bash
    curl -X POST --data '{
        "jsonrpc":"2.0",
        "id"     :1,
        "method" :"info.getNodeID"
    }' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
    ```

    Copy the `nodeID` from the response (it will look like `NodeID-...`).

2.  **Stake & Register:**

      * Go to the [Avalanche Core Wallet](https://core.app/), switch to testnet.
      * Navigate to the "Stake" section.
      * Select "Add Validator".
      * Follow the UI, entering your **NodeID** and staking the required amount for **14 days**.

## Deliverables Checklist

  * [x] **Running healthy validator:** The Ansible playbook deploys the node.
  * [x] **Testnet explorer dashboard URL:** (To be added manually after Step 3)
      * `https://subnets-test.avax.network/validators/[Your-NodeID]`
  * [ ] **GitHub repo (scripts, docs):** This repository.
  * [ ] **E-mail reply with experience:** (To be written post-completion).

## Contact

For any questions or feedback, please contact `tobyqin` at GitHub.
