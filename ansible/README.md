## deploy node playbook

```bash
ansible-playbook -i hosts.ini deploy-docker-node.yml
```

What it does:
1. Install Python3
2. Install Docker
3. Install Docker Compose
4. Deploy Avalanche Node using Docker Compose
5. Wait for node to be heathy and print node's info
6. Optimized logging for docker and avalanche, ensure logs will not fill up your disk

## Proactive monitoring playbook

```bash
ansible-playbook -i hosts.ini monitoring.yml
```

What it does:
1. Check node deployment status
2. Check node sync status as a validator
3. Print node's info and sync info if successful
4. Print detail error message if any check failed

### Deploy Prometheus and Grafana playbook

```bash
ansible-playbook -i hosts.ini deploy-monitoring-stack.yml
```
What it does:
1. Deploy Prometheus and Grafana using Docker Compose
2. Bake Avalanche node's exporter into Prometheus config
3. Expose Grafana on port 4000

### Remove Prometheus and Grafana playbook
```bash
ansible-playbook -i hosts.ini remove-monitoring-stack.yml
```
What it does:
1. Remove Prometheus and Grafana
2. Update the playbook to remove entire file and directory from server if needed