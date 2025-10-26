#!/usr/bin/env python3
"""
Script to verify Avalanche node sync status.
Checks number of peers and sync status for P, C, X chains.
This may take time after deployment as the node needs to catch up.
Uses Python 3 standard library only. No external dependencies required.
"""

import json
import urllib.request

# Configure the target node IP here
TARGET_IP = "127.0.0.1"
PORT = 9650

def make_request(method, params=None, endpoint="ext/info"):
    """
    Make a JSON-RPC request to the Avalanche node API.
    """
    url = f"http://{TARGET_IP}:{PORT}/{endpoint}"
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"Error connecting to {url}: {e}")
        return None

def check_sync_status(chain):
    """
    Check if the node is bootstrapped for the given chain.
    """
    result = make_request("info.isBootstrapped", {"chain": chain})
    if result is None:
        raise Exception(f"Failed to connect to info endpoint for {chain} chain")
    if 'error' in result:
        raise Exception(f"isBootstrapped API error for {chain} chain: {result['error']}")
    if 'result' not in result:
        raise Exception(f"Unexpected isBootstrapped response for {chain} chain: {result}")
    if not result['result']['isBootstrapped']:
        raise Exception(f"{chain} chain is not bootstrapped: {result['result']}")
    return result['result']['isBootstrapped']

def check_peers():
    """
    Get the number of connected peers.
    """
    result = make_request("info.peers")
    if result is None:
        raise Exception("Failed to connect to info endpoint")
    if 'error' in result:
        raise Exception(f"Peers API error: {result['error']}")
    if 'result' not in result:
        raise Exception(f"Unexpected peers response: {result}")
    peers = int(result['result']['numPeers'])
    if peers == 0:
        raise Exception(f"No peers connected: {result['result']}")
    return peers

def main():
    print("Verifying Avalanche node sync status...")
    print(f"Target node: {TARGET_IP}:{PORT}")
    print("-" * 50)

    try:
        # Check sync status for P, C, X chains
        chains = ['P', 'C', 'X']
        for chain in chains:
            synced = check_sync_status(chain)
            print(f"✓ {chain} chain synced: {synced}")

        # Check peer connectivity
        peers = check_peers()
        print(f"✓ Number of peers: {peers}")

        print("-" * 50)
        print("✓ Node sync status verification PASSED")
        exit(0)

    except Exception as e:
        print(f"✗ Node sync status verification FAILED: {e}")
        exit(1)

if __name__ == "__main__":
    main()