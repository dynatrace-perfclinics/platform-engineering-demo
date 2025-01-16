#!/bin/bash

# Startup Ping
curl -X POST https://grzxx1q7wd.execute-api.us-east-1.amazonaws.com/default/codespace-tracker \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"com.dynatrace.devrel.handson.codespace.started\",
    \"tenant\": \"$DT_ENV_NAME\",
    \"repo\": \"$GITHUB_REPOSITORY\",
    \"demo\": \"obslab-platform-engineering-demo\",
    \"codespace.name\": \"$CODESPACE_NAME\"
  }"

##########################
# 2. Run test harness
export OTEL_SERVICE_NAME=codespace-platform
export PYTEST_RUN_NAME=startup-automated-test
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
pytest --export-traces codespaces_test.py
