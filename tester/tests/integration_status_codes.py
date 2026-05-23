import os
import sys

import requests


BASE_URL = os.environ.get("APP_BASE_URL", "http://app:5000").rstrip("/")
TIMEOUT_SECONDS = 5

TEST_CASES = [
    ("GET", "/", None, 200, True),
    ("GET", "/upload", None, 200, True),
    ("GET", "/files", None, 200, True),
    ("GET", "/to_files", None, 302, False),
    ("GET", "/download/file_that_does_not_exist.txt", None, 404, False),
    ("POST", "/login", {"name": "admin", "password": "password"}, 302, False),
    ("POST", "/login", {"name": "admin", "password": "wrong"}, 401, False),
]


def run_case(method, path, data, expected_status, allow_redirects):
    url = f"{BASE_URL}{path}"
    response = requests.request(
        method=method,
        url=url,
        data=data,
        allow_redirects=allow_redirects,
        timeout=TIMEOUT_SECONDS,
    )

    print(
        f"{method} {path}: expected={expected_status}, actual={response.status_code}, "
        f"allow_redirects={allow_redirects}"
    )

    if response.status_code != expected_status:
        raise AssertionError(
            f"{method} {path}: expected HTTP {expected_status}, got HTTP {response.status_code}"
        )


def main():
    failed_cases = 0

    for case in TEST_CASES:
        try:
            run_case(*case)
        except Exception as exc:  # noqa: BLE001 - test runner prints all failed checks.
            failed_cases += 1
            print(f"FAILED: {exc}", file=sys.stderr)

    if failed_cases:
        print(f"Integration tests failed: {failed_cases}", file=sys.stderr)
        return 1

    print("Integration status-code tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
