#!/bin/sh
set -eu

PROJECT_FILE="${COVFEE_PROJECT_FILE:-getting_started.py}"
PUBLIC_HOST="${COVFEE_HOST:-localhost}"
PUBLIC_PORT="${COVFEE_PUBLIC_PORT:-5000}"
BIND_HOST="${COVFEE_BIND_HOST:-0.0.0.0}"
BIND_PORT="${COVFEE_BIND_PORT:-5000}"
FORCE_REBUILD="${COVFEE_FORCE_REBUILD:-false}"
DATABASE_PATH=".covfee/database.covfee.db"

if [ ! -f "${PROJECT_FILE}" ]; then
    echo "Project file not found: ${PROJECT_FILE}" >&2
    exit 1
fi

if [ "${FORCE_REBUILD}" = "true" ] || [ "${FORCE_REBUILD}" = "1" ]; then
    covfee make "${PROJECT_FILE}" --force --no-launch --deploy --host "${PUBLIC_HOST}" --port "${PUBLIC_PORT}"
elif [ ! -f "${DATABASE_PATH}" ]; then
    covfee make "${PROJECT_FILE}" --no-launch --deploy --host "${PUBLIC_HOST}" --port "${PUBLIC_PORT}"
fi

exec covfee start --deploy --host "${BIND_HOST}" --port "${BIND_PORT}"
