## deploy node playbook

```bash
ansible-playbook -i hosts.ini deploy.yml
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