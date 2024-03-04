#!/bin/bash

# Add anonymous startup ping
curl -L -H "User-Agent: GitHub" https://dt-url.net/devrel-PE-startupping

##########################
# 2. Run test harness
export OTEL_SERVICE_NAME=codespace-platform
export PYTEST_RUN_NAME=startup-automated-test
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
pytest --export-traces codespaces_test.py
