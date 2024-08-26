import os
from utils import *

ARGOCD_VERSION="v2.12.2"

if (
    DT_RW_API_TOKEN is None or
    DT_ENV_NAME is None or
    DT_ENV is None or
    DT_OAUTH_CLIENT_ID is None or
    DT_OAUTH_CLIENT_SECRET is None or
    DT_OAUTH_ACCOUNT_URN is None
):
    exit("Missing mandatory environment variables. Cannot proceed. Exiting.")

# Build DT environment URLs
DT_TENANT_APPS, DT_TENANT_LIVE = build_dt_urls(dt_env_name=DT_ENV_NAME, dt_env=DT_ENV)

# Get correct SSO URL
DT_SSO_TOKEN_URL = get_sso_token_url(dt_env=DT_ENV)

# Create other DT tokens
DT_ALL_INGEST_TOKEN = create_dt_api_token(token_name="[devrel demo] DT_ALL_INGEST_TOKEN", scopes=[
    "bizevents.ingest",
    "events.ingest",
    "logs.ingest",
    "metrics.ingest",
    "openTelemetryTrace.ingest",
    "DataExport", 
    "entities.read", 
    "settings.read", 
    "settings.write", 
    "activeGateTokenManagement.create"
], dt_rw_api_token=DT_RW_API_TOKEN, dt_tenant_live=DT_TENANT_LIVE)
DT_OP_TOKEN = create_dt_api_token(token_name="[devrel demo] DT_OP_TOKEN", scopes=[
    "InstallerDownload",
    "DataExport", 
    "entities.read", 
    "settings.read",
    "settings.write", 
    "activeGateTokenManagement.create"
    ], dt_rw_api_token=DT_RW_API_TOKEN, dt_tenant_live=DT_TENANT_LIVE)
DT_MONACO_TOKEN = create_dt_api_token(token_name="[devrel demo] DT_MONACO_TOKEN", scopes=[
    "settings.read",
    "settings.write",
    "slo.read",
    "slo.write",
    "DataExport",
    "ExternalSyntheticIntegration",
    "ReadConfig",
    "WriteConfig"
], dt_rw_api_token=DT_RW_API_TOKEN, dt_tenant_live=DT_TENANT_LIVE)

## Keptn
# Should Keptn be installed or not?
INSTALL_KEPTN = os.environ.get("INSTALL_KEPTN", "true")

if INSTALL_KEPTN.lower() == "false" or INSTALL_KEPTN.lower() == "no":
    # Rename files to prevent installation by argoCD
    try:
        os.rename(src="gitops/applications/platform/keptn.yml", dst="gitops/applications/platform/keptn.yml.BAK")
        os.rename(src="gitops/manifests/platform/keptn/keptn-metrics.yml", dst="gitops/manifests/platform/keptn/keptn-metrics.yml.BAK")
        os.rename(src="gitops/manifests/platform/keptn/otelcol-keptnconfig.yml", dst="gitops/manifests/platform/keptn/otelcol-keptnconfig.yml.BAK")
        git_commit(target_file="-A", commit_msg="do not install Keptn", push=True)
    except:
        print("Exception caught renaming (to remove) Keptn files. No big deal. You're probably re-running this script. Continuing.")

if TOOL_MODE.lower() == "oss":
    # Rename DT files to prevent installation by argoCD
    try:
        rename_file(src="gitops/applications/platform/dynatrace.yml", dst="gitops/applications/platform/dynatrace.yml.BAK")
        rename_file(src="gitops/manifests/platform/dynatrace/dynatrace.yml", dst="gitops/manifests/platform/dynatrace/dynatrace.yml.BAK")
        rename_file(src="gitops/manifests/platform/dynatrace/workflow.yml", dst="gitops/manifests/platform/dynatrace/workflow.yml.BAK")
        rename_file(src="gitops/manifests/platform/namespaces/dt.yaml", dst="gitops/manifests/platform/namespaces/dt.yaml.BAK")
        git_commit(target_file="-A", commit_msg="do not install Dynatrace OneAgent", push=True)
    except:
        print("Exception caught renaming (to remove) DT files. No big deal. You're probably re-running this script. Continuing.")

# Set DT GEOLOCATION based on env type used
# TODO: Find a better way here. If this was widely used, all load would be on one GEOLOCATION.
DT_GEOLOCATION = get_geolocation(dt_env=DT_ENV)

# Delete cluster first, in case this is a re-run
run_command(["kind", "delete", "cluster"])

# Find and replace placeholders
# Commit up to repo
# Find and replace DT_TENANT_LIVE_PLACEHOLDER with real text
# eg. "https://abc12345.live.dynatrace.com"
# Push = False for the first set
# because we push on the final git commit
do_file_replace(pattern="./**/*.y*ml", find_string="DT_TENANT_LIVE_PLACEHOLDER", replace_string=DT_TENANT_LIVE, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="DT_TENANT_LIVE_PLACEHOLDER", replace_string=DT_TENANT_LIVE, recursive=True)
git_commit(target_file="-A", commit_msg="update DT_TENANT_LIVE_PLACEHOLDER", push=False)

# Find and replace DT_TENANT_APPS_PLACEHOLDER with real text eg. "https://abc12345.live.apps.dynatrace.com"
do_file_replace(pattern="./**/*.y*ml", find_string="DT_TENANT_APPS_PLACEHOLDER", replace_string=DT_TENANT_APPS, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="DT_TENANT_APPS_PLACEHOLDER", replace_string=DT_TENANT_APPS, recursive=True)
git_commit(target_file="-A", commit_msg="update DT_TENANT_APPS_PLACEHOLDER", push=False)

# Find and replace GITHUB_DOT_COM_REPO_PLACEHOLDER with real text eg. "https://github.com/yourOrg/yourRepo.git"
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_DOT_COM_REPO_PLACEHOLDER", replace_string=GITHUB_DOT_COM_REPO, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_DOT_COM_REPO_PLACEHOLDER", replace_string=GITHUB_DOT_COM_REPO, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_DOT_COM_REPO_PLACEHOLDER", push=False)

# Find and replace GEOLOCATION_PLACEHOLDER with real text. eg. "GEOLOCATION-0A41430434C388A9"
do_file_replace(pattern="./**/*.y*ml", find_string="GEOLOCATION_PLACEHOLDER", replace_string=DT_GEOLOCATION, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GEOLOCATION_PLACEHOLDER", replace_string=DT_GEOLOCATION, recursive=True)
git_commit(target_file="-A", commit_msg="update GEOLOCATION_PLACEHOLDER", push=False)

# Find and replace GITHUB_REPOSITORY_PLACEHOLDER with real text. eg "yourOrg/yourRepo"
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_REPOSITORY_PLACEHOLDER", replace_string=GITHUB_ORG_SLASH_REPOSITORY, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_REPOSITORY_PLACEHOLDER", replace_string=GITHUB_ORG_SLASH_REPOSITORY, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_REPOSITORY_PLACEHOLDER", push=False)

# Find and replace GITHUB_REPO_NAME_PLACEHOLDER with real text. eg. `yourRepo`
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_REPO_NAME_PLACEHOLDER", replace_string=GITHUB_REPO_NAME, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_REPO_NAME_PLACEHOLDER", replace_string=GITHUB_REPO_NAME, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_REPO_NAME_PLACEHOLDER", push=False)

github_org = get_github_org(github_repo=GITHUB_ORG_SLASH_REPOSITORY)
# Find and replace GITHUB_ORG_NAME_PLACEHOLDER with real text. eg. `yourOrg`
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_ORG_NAME_PLACEHOLDER", replace_string=github_org, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_ORG_NAME_PLACEHOLDER", replace_string=github_org, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_ORG_NAME_PLACEHOLDER", push=False)

# Find and replace CODESPACE_NAME_PLACEHOLDER with real text. eg. `fantastic-onion-123ab233`
do_file_replace(pattern="./**/*.y*ml", find_string="CODESPACE_NAME_PLACEHOLDER", replace_string=CODESPACE_NAME, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="CODESPACE_NAME_PLACEHOLDER", replace_string=CODESPACE_NAME, recursive=True)
git_commit(target_file="-A", commit_msg="update CODESPACE_NAME_PLACEHOLDER", push=False)

# Find and replace ARGOCD_PORT_NUMBER_PLACEHOLDER with real text. eg. `30100`
do_file_replace(pattern="./**/*.y*ml", find_string="ARGOCD_PORT_NUMBER_PLACEHOLDER", replace_string=f"{ARGOCD_PORT_NUMBER}", recursive=True)
do_file_replace(pattern="./**/*.json", find_string="ARGOCD_PORT_NUMBER_PLACEHOLDER", replace_string=f"{ARGOCD_PORT_NUMBER}", recursive=True)
git_commit(target_file="-A", commit_msg="update ARGOCD_PORT_NUMBER_PLACEHOLDER", push=False)

# Find and replace DEMO_APP_PORT_NUMBER_PLACEHOLDER with real text. eg. `80`
do_file_replace(pattern="./**/*.y*ml", find_string="DEMO_APP_PORT_NUMBER_PLACEHOLDER", replace_string=f"{DEMO_APP_PORT_NUMBER}", recursive=True)
do_file_replace(pattern="./**/*.json", find_string="DEMO_APP_PORT_NUMBER_PLACEHOLDER", replace_string=f"{DEMO_APP_PORT_NUMBER}", recursive=True)
git_commit(target_file="-A", commit_msg="update DEMO_APP_PORT_NUMBER_PLACEHOLDER", push=False)

# Find and replace BACKSTAGE_PORT_NUMBER_PLACEHOLDER with real text. eg. `30105`
do_file_replace(pattern="./**/*.y*ml", find_string="BACKSTAGE_PORT_NUMBER_PLACEHOLDER", replace_string=f"{BACKSTAGE_PORT_NUMBER}", recursive=True)
do_file_replace(pattern="./**/*.json", find_string="BACKSTAGE_PORT_NUMBER_PLACEHOLDER", replace_string=f"{BACKSTAGE_PORT_NUMBER}", recursive=True)
git_commit(target_file="-A", commit_msg="update BACKSTAGE_PORT_NUMBER_PLACEHOLDER", push=False)

# Find and replace GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER with real text. eg. `.app.github.dev`
do_file_replace(pattern="./**/*.y*ml", find_string="GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", replace_string=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN, recursive=True)
do_file_replace(pattern="./**/*.json", find_string="GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", replace_string=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN, recursive=True)
git_commit(target_file="-A", commit_msg="update GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN_PLACEHOLDER", push=True)


###### Upload DT Assets
# Notebooks
type = "notebook"
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/notebooks/analyze-argocd-notification-events.json", name="[devrel demo] ArgoCD: Analyze Notification Events", type=type, dt_tenant_apps=DT_TENANT_APPS)
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/notebooks/argocd-log-analytics.json", name="[devrel demo] ArgoCD: Log Analytics", type=type, dt_tenant_apps=DT_TENANT_APPS)
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/notebooks/platform-engineering-walkthrough.json", name="[devrel demo] Platform Engineering Demo Walkthrough", type=type, dt_tenant_apps=DT_TENANT_APPS)
# Dashboards
type = "dashboard"
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/dashboards/argocd-lifecycle-dashboard.json", name="[devrel demo] ArgoCD: Lifecycle Dashboard", type=type, dt_tenant_apps=DT_TENANT_APPS)
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/dashboards/argocd-platform-observability.json", name="[devrel demo] ArgoCD: Platform Observability", type=type, dt_tenant_apps=DT_TENANT_APPS)
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/dashboards/backstage-error-analysis.json", name="[devrel demo] Backstage: Error Analysis", type=type, dt_tenant_apps=DT_TENANT_APPS)
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/dashboards/platform-observability-cockpit.json", name="[devrel demo] Platform Observability Cockpit", type=type, dt_tenant_apps=DT_TENANT_APPS)
upload_dt_document_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/dashboards/team-ownership-dashboard.json", name="[devrel demo] Team Ownership Dashboard", type=type, dt_tenant_apps=DT_TENANT_APPS)
# Workflows
upload_dt_workflow_asset(sso_token_url=DT_SSO_TOKEN_URL, path="dynatraceassets/workflows/lifecycle-events-workflow.json", name="[devrel demo] Lifecycle Events Workflow", dt_tenant_apps=DT_TENANT_APPS)

## Lets get started with Kind
# Create cluster
output = run_command(["kind", "create", "cluster", "--config", ".devcontainer/kind-cluster.yml", "--wait", STANDARD_TIMEOUT])

# Create namespaces
namespaces = ["argocd", "opentelemetry", "backstage", "monaco"]
if TOOL_MODE.lower() == "dt":
    namespaces.append("dynatrace")

for namespace in namespaces:
    output = run_command(["kubectl", "create", "namespace", namespace])

# Create Github API token
# Which the argo appset will use when polling GitHub's API
# If un-authenticated API access is used, we hit 403 rate throttling.
# See also: gitops/manifests/platform/argoconfig/appset.yml
output = run_command(["kubectl", "-n", "argocd", "create", "secret", "generic" ,"github-token", f"--from-literal=token={GITHUB_TOKEN}"])

# Create bizevent secrets
if TOOL_MODE.lower() == "dt":
    output = run_command(["kubectl", "-n", "dynatrace", "create", "secret", "generic", "dt-bizevent-oauth-details", f"--from-literal=dtTenant={DT_TENANT_LIVE}", f"--from-literal=oAuthClientID={DT_OAUTH_CLIENT_ID}", f"--from-literal=oAuthClientSecret={DT_OAUTH_CLIENT_SECRET}", f"--from-literal=accountURN={DT_OAUTH_ACCOUNT_URN}"])
output = run_command(["kubectl", "-n", "opentelemetry", "create", "secret", "generic", "dt-bizevent-oauth-details", f"--from-literal=dtTenant={DT_TENANT_LIVE}", f"--from-literal=oAuthClientID={DT_OAUTH_CLIENT_ID}", f"--from-literal=oAuthClientSecret={DT_OAUTH_CLIENT_SECRET}", f"--from-literal=accountURN={DT_OAUTH_ACCOUNT_URN}"])

# Install argocd
print(f"Installing argo cd version: {ARGOCD_VERSION}")
output = run_command(["kubectl", "apply", "-n", "argocd", "-f", f"https://raw.githubusercontent.com/argoproj/argo-cd/{ARGOCD_VERSION}/manifests/install.yaml"])

output = run_command(["kubectl", "wait", "--for=condition=Available=True", "deployments", "-n", "argocd", "--all", f"--timeout={STANDARD_TIMEOUT}"])

# Configure argocd
output = run_command(["kubectl", "apply", "-n", "argocd", "-f", "gitops/manifests/platform/argoconfig/argocd-cm.yml"])
output = run_command(["kubectl", "apply", "-n", "argocd", "-f", "gitops/manifests/platform/argoconfig/argocd-no-tls.yml"])
output = run_command(["kubectl", "apply", "-n", "argocd", "-f", "gitops/manifests/platform/argoconfig/argocd-nodeport.yml"])

# Restart argo server
output = run_command(["kubectl", "-n", "argocd", "scale", "deployment/argocd-server", "--replicas", "0"])
output = run_command(["kubectl", "-n", "argocd", "scale", "deployment/argocd-server", "--replicas", "1"])

# Wait until argo server exists (or timeout is hit)
output = run_command(["kubectl", "-n", "argocd", "wait", "--for=jsonpath={.status.readyReplicas}=1", "deployment", "--selector=app.kubernetes.io/name=argocd-server", "--timeout", "2m"])

# Apply platform
output = run_command(["kubectl", "apply", "-f", "gitops/platform.yml"])

# Wait until argo secret exists (or timeout is hit)
wait_for_artifact_to_exist(namespace="argocd", artifact_type="secret", artifact_name="argocd-initial-admin-secret")

# Set the default context to the argocd namespace so 'argocd' CLI works
output = run_command(["kubectl", "config", "set-context", "--current", "--namespace=argocd"])
# Now authenticate
output = run_command(["argocd", "login", "argo", "--core"])

# Wait until argo account 'alice' exists (or timeout is hit)
count = 1
get_argo_accounts_output = ""
while count < WAIT_FOR_ACCOUNTS_TIMEOUT and "alice" not in get_argo_accounts_output:
    print(f"Waiting for argo account alice to exist. Wait count: {count}")
    count += 1
    get_argo_accounts_output = run_command(["argocd", "account", "list"]).stdout
    time.sleep(1)

if get_argo_accounts_output == "":
    exit(f"ArgoCD Account alice does not exist. Cannot proceed.")

ARGOCD_TOKEN = run_command(["argocd", "account", "generate-token", "--account", "alice"]).stdout

if ARGOCD_TOKEN is None or ARGOCD_TOKEN == "":
    exit(f"ARGOCD_TOKEN is empty: {ARGOCD_TOKEN}. Cannot proceed!")

output = run_command(["kubectl", "config", "set-context", "--current", "--namespace=default"])

# create dt-details secret in opentelemetry namespace
output = run_command(["kubectl", "-n", "opentelemetry", "create", "secret", "generic", "dt-details", f"--from-literal=DT_URL={DT_TENANT_LIVE}", f"--from-literal=DT_OTEL_ALL_INGEST_TOKEN={DT_ALL_INGEST_TOKEN}"])

# create backstage-details secret in backstage namespace
output = run_command(["kubectl", "-n", "backstage", "create", "secret", "generic", "backstage-secrets",
                      f"--from-literal=BASE_DOMAIN={CODESPACE_NAME}",
                      f"--from-literal=BACKSTAGE_PORT_NUMBER={BACKSTAGE_PORT_NUMBER}",
                      f"--from-literal=ARGOCD_PORT_NUMBER={ARGOCD_PORT_NUMBER}",
                      f"--from-literal=ARGOCD_TOKEN={ARGOCD_TOKEN}",
                      f"--from-literal=GITHUB_TOKEN={GITHUB_TOKEN}",
                      f"--from-literal=GITHUB_ORG={github_org}",
                      f"--from-literal=GITHUB_REPO={GITHUB_REPO_NAME}",
                      f"--from-literal=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN={GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}",
                      f"--from-literal=DT_TENANT_NAME={DT_ENV_NAME}",
                      f"--from-literal=DT_TENANT_LIVE={DT_TENANT_LIVE}",
                      f"--from-literal=DT_TENANT_APPS={DT_TENANT_APPS}",
                      f"--from-literal=DT_SSO_TOKEN_URL={DT_SSO_TOKEN_URL}",
                      f"--from-literal=DT_OAUTH_CLIENT_ID={DT_OAUTH_CLIENT_ID}",
                      f"--from-literal=DT_OAUTH_CLIENT_SECRET={DT_OAUTH_CLIENT_SECRET}",
                      f"--from-literal=DT_OAUTH_ACCOUNT_URN={DT_OAUTH_ACCOUNT_URN}",
                      f"--from-literal=DT_ALL_INGEST_TOKEN={DT_ALL_INGEST_TOKEN}"
                    ])

# Create secret for OneAgent in dynatrace namespace
if TOOL_MODE.lower() == "dt":
    output = run_command([
        "kubectl", "-n", "dynatrace", "create", "secret", "generic", "platform-engineering-demo",
        f"--from-literal=apiToken={DT_OP_TOKEN}",
        f"--from-literal=dataIngestToken={DT_ALL_INGEST_TOKEN}"
        ])

# Create monaco-secret in monaco namespace
output = run_command(["kubectl", "-n", "monaco", "create", "secret", "generic", "monaco-secret", f"--from-literal=monacoToken={DT_MONACO_TOKEN}"])
# Create monaco-secret in dynatrace namespace
if TOOL_MODE.lower() == "dt":
    output = run_command(["kubectl", "-n", "dynatrace", "create", "secret", "generic", "monaco-secret", f"--from-literal=monacoToken={DT_MONACO_TOKEN}"])

# Wait for backstage deployment to be created
wait_for_artifact_to_exist(namespace="backstage", artifact_type="deployment", artifact_name="backstage")

# backstage deployment is ready
# restart backstage to pick up secret and start successfully
output = run_command(["kubectl", "-n", "backstage", "rollout", "restart", "deployment/backstage"])
output = run_command(["kubectl", "-n", "backstage", "rollout", "status", "deployment/backstage", f"--timeout={STANDARD_TIMEOUT}"])

# Send startup ping
send_startup_ping()
