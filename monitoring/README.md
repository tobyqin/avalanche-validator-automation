## Installation

```bash
wget -nd -m https://raw.githubusercontent.com/tobyqin/avalanche-validator-automation/main/monitoring/installation.sh ;\
chmod 755 installation.sh;
./monitoring.sh --help
```

## Reference

The key functions please refer to https://build.avax.network/docs/nodes/maintain/monitoring

Purpose of this script is to update grafana dashboard port to 4000.

## Notes

We can install monitoring with docker compose and ansible playbook, but the docker version cannot use the official machine exporter and import the example dashboard, so this customized script version has a better experience.