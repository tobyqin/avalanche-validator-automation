#!/usr/bin/env python3
"""
Script to verify basic Avalanche node deployment.
Checks node version, node ID, and node health.
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

def check_health():
    """
    Check if the node is healthy.
    """
    result = make_request("health.health", endpoint="ext/health")
    if result is None:
        raise Exception("Failed to connect to health endpoint")
    if 'error' in result:
        raise Exception(f"Health API error: {result['error']}")
    if 'result' not in result:
        raise Exception(f"Unexpected health response: {result}")
    if not result['result']['healthy']:
        raise Exception(f"Node is not healthy: {result['result']}")
    return result['result']['healthy']

def get_node_id():
    """
    Get the node's unique ID.
    """
    result = make_request("info.getNodeID")
    if result is None:
        raise Exception("Failed to connect to info endpoint")
    if 'error' in result:
        raise Exception(f"GetNodeID API error: {result['error']}")
    if 'result' not in result:
        raise Exception(f"Unexpected getNodeID response: {result}")
    return result['result']['nodeID']

def get_version():
    """
    Get the node's version.
    """
    result = make_request("info.getNodeVersion")
    if result is None:
        raise Exception("Failed to connect to info endpoint")
    if 'error' in result:
        raise Exception(f"GetNodeVersion API error: {result['error']}")
    if 'result' not in result:
        raise Exception(f"Unexpected getNodeVersion response: {result}")
    return result['result']['version']

def main():
    print("Verifying basic Avalanche node deployment...")
    print(f"Target node: {TARGET_IP}:{PORT}")
    print("-" * 50)

    try:
        # Check node health
        healthy = check_health()
        print(f"✓ Node healthy: {healthy}")

        # Get node ID
        node_id = get_node_id()
        print(f"✓ Node ID: {node_id}")

        # Get version
        version = get_version()
        print(f"✓ Node version: {version}")

        print("-" * 50)
        print("✓ Basic node deployment verification PASSED")
        exit(0)

    except Exception as e:
        print(f"✗ Basic node deployment verification FAILED: {e}")
        exit(1)

if __name__ == "__main__":
    main()