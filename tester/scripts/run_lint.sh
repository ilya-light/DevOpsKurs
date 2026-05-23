#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="/workspace/tests/pylint_plugins:${PYTHONPATH:-}"
cd /workspace

pylint \
    --load-plugins=forbidden_name_checker \
    --disable=all \
    --enable=forbidden-user-variable \
    --score=n \
    /workspace/app
