#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/workspace/logs"
mkdir -p "${LOG_DIR}"

run_stage() {
    local stage_name="$1"
    shift
    local log_file="${LOG_DIR}/${stage_name}.log"

    echo "=== START ${stage_name} $(date -Iseconds) ===" | tee "${log_file}" /proc/1/fd/1

    set +e
    "$@" 2>&1 | tee -a "${log_file}" /proc/1/fd/1
    local status=${PIPESTATUS[0]}
    set -e

    echo "=== FINISH ${stage_name}: exit_code=${status} $(date -Iseconds) ===" | tee -a "${log_file}" /proc/1/fd/1
    return "${status}"
}

run_stage "00_wait_app" python3 "${SCRIPT_DIR}/wait_app.py"
run_stage "01_beautify_html" "${SCRIPT_DIR}/run_beautify.sh"
run_stage "02_pylint_custom" "${SCRIPT_DIR}/run_lint.sh"
run_stage "03_integration_status_codes" "${SCRIPT_DIR}/run_integration.sh"

echo "All testing stages passed" | tee -a "${LOG_DIR}/summary.log" /proc/1/fd/1
