import os
import sys
import time

import requests


base_url = os.environ.get("APP_BASE_URL", "http://app:5000").rstrip("/")

for attempt in range(1, 61):
    try:
        response = requests.get(f"{base_url}/", timeout=2)
        print(f"attempt={attempt}: GET / -> {response.status_code}")
        if response.status_code == 200:
            sys.exit(0)
    except requests.RequestException as exc:
        print(f"attempt={attempt}: app is not ready: {exc}")

    time.sleep(1)

print(f"app did not become ready at {base_url}", file=sys.stderr)
sys.exit(1)
