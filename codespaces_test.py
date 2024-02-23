import requests
import time
from utils import *

# This file should be executed by pytest
# like: pytest --export-traces

#COLLECTOR_WAIT_TIMEOUT_SECONDS = 300
#opentelemetry_collector_endpoint = "http://localhost:4318"

#dt_tenant_live = os.environ.get("DT_TENANT_LIVE")
#dt_api_token = os.environ.get("DT_ALL_INGEST_TOKEN")

#################################################
# TEST SUITE BEGINS
#
# pytest executes `test_` methods in order
#################################################
def test_wait_for_collector():
    
    _, dt_tenant_live = build_dt_urls(dt_env=DT_ENV, dt_env_name=DT_ENV_NAME)
    dt_all_ingest_token = create_dt_api_token(token_name="[devrel demo/codespaces_test.py] DT_ALL_INGEST_TOKEN pytest", dt_rw_api_token=DT_RW_API_TOKEN, dt_tenant_live=dt_tenant_live, scopes=[
        "bizevents.ingest",
        "events.ingest",
        "logs.ingest",
        "metrics.ingest",
        "openTelemetryTrace.ingest"
    ])
    count = 1

    COLLECTOR_AVAILABLE = False
    while count < COLLECTOR_WAIT_TIMEOUT_SECONDS:
        collector_response = requests.get(f"{OPENTELEMETRY_COLLECTOR_ENDPOINT}/v1/logs")
        
        # A 405 code means "GET worked but a GET isn't valid for this endpoint"
        # This is precisely what we're expecting as the real OP should be a POST
        if collector_response.status_code == 405:
            COLLECTOR_AVAILABLE = True
            send_log_to_dt_or_otel_collector(success=True, msg_string=f"OpenTelemetry collector available after {count} seconds. Proceed with test harness.", dt_api_token=dt_all_ingest_token, dt_tenant_live=dt_tenant_live)
            break
        else:
            count += 1
            time.sleep(1) # sleep for 1s

    # OTEL collector is not yet available
    # Send warning directly to cluster
    if not COLLECTOR_AVAILABLE:
        send_log_to_dt_or_otel_collector(success=False, endpoint=dt_tenant_live, msg_string="OpenTelemetry collector not available. Send via direct-to-cluster ingest endpoint.", destroy_codespace=True, dt_api_token=dt_all_ingest_token, dt_tenant_live=dt_tenant_live)
        raise Exception("On cluster collector is not available. Terminating codespace. Check DT for logs.")

def test_ensure_namespaces_exists():
    output = run_command(["kubectl", "get", "namespaces"])
    assert "argocd" in output.stdout
    assert "argo-rollouts" in output.stdout
    assert "backstage" in output.stdout
    assert "cronjobs" in output.stdout
    assert "dynatrace" in output.stdout
    assert "keptn" in output.stdout
    assert "kubeaudit" in output.stdout
    assert "monaco" in output.stdout
    assert "opentelemetry" in output.stdout

def test_ensure_opentelemetry_dtdetails_secret_exists():
    output = run_command(["kubectl", "-n", "opentelemetry", "get", "secrets"])
    assert "dt-details" in output.stdout
    output = run_command(["kubectl", "-n", "monaco", "get", "secrets"])
    assert "monaco-secret" in output.stdout
    output = run_command(["kubectl", "-n", "dynatrace", "get", "secrets"])
    assert "monaco-secret" in output.stdout