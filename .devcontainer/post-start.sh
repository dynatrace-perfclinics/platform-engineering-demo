#!/bin/bash

echo "[post-start] start" >> ~/status

# Install and configure cluster
#python3 cluster_installer.py

# Start the cluster
#kind create cluster --config .devcontainer/kind-cluster.yml --wait 300s

#echo "[post-start] cluster available" >> ~/status



# install argocd
# kubectl create namespace argocd
# echo "[post-start] argocd namespace created" >> ~/status
# kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
# kubectl wait --for=condition=Available=True deploy -n argocd --all --timeout=300s

# echo "[post-start] argocd deployed" >> ~/status


# kubectl apply -n argocd -f gitops/manifests/platform/argoconfig/argocd-no-tls.yml
# kubectl apply -n argocd -f gitops/manifests/platform/argoconfig/argocd-nodeport.yml
# kubectl -n argocd rollout restart deploy/argocd-server
# kubectl -n argocd rollout status deploy/argocd-server --timeout=300s

# # Set the default context to the argocd namespace so 'argocd' CLI works
# kubectl config set-context --current --namespace=argocd
# # Now authenticate
# argocd login argo --core

# # Set the default context to the argocd namespace so 'argocd' CLI works
# ARGOCD_TOKEN=$(argocd account generate-token --account alice)

# # Reset kubectl context
# kubectl config set-context --current --namespace=default

# echo "[post-start] argocd configured and restarted" >> ~/status

# kubectl create namespace opentelemetry
# kubectl -n opentelemetry create secret generic dt-details \
#   --from-literal=DT_URL=$DT_TENANT_LIVE \
#   --from-literal=DT_OTEL_ALL_INGEST_TOKEN=$DT_ALL_INGEST_TOKEN


# kubectl create namespace backstage
# kubectl -n backstage create secret generic backstage-secrets \
#   --from-literal=BASE_DOMAIN=$CODESPACE_NAME \
#   --from-literal=BACKSTAGE_PORT_NUMBER=7007 \
#   --from-literal=ARGOCD_PORT_NUMBER=30100 \
#   --from-literal=ARGOCD_TOKEN=$ARGOCD_TOKEN \
#   --from-literal=GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN=$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN \
#   --from-literal=GITHUB_TOKEN=$GITHUB_TOKEN \
#   --from-literal=GITHUB_USER=$GITHUB_USER \
#   --from-literal=DT_TENANT_NAME=$DT_TENANT_NAME \
#   --from-literal=DT_TENANT_LIVE=$DT_TENANT_LIVE \
#   --from-literal=DT_TENANT_APPS=$DT_TENANT_APPS \
#   --from-literal=DT_SSO_TOKEN_URL=$DT_SSO_TOKEN_URL \
#   --from-literal=DT_OAUTH_CLIENT_ID=$DT_OAUTH_CLIENT_ID \
#   --from-literal=DT_OAUTH_CLIENT_SECRET=$DT_OAUTH_CLIENT_SECRET \
#   --from-literal=DT_OAUTH_ACCOUNT_URN=$DT_OAUTH_ACCOUNT_URN \
#   --from-literal=DT_ALL_INGEST_TOKEN=$DT_ALL_INGEST_TOKEN

# kubectl create namespace dynatrace
# kubectl -n dynatrace create secret generic hot-day-platform-engineering --from-literal=apiToken=$DT_OP_TOKEN --from-literal=dataIngestToken=$DT_ALL_INGEST_TOKEN

# kubectl create namespace monaco
# kubectl -n monaco create secret generic monaco-secret --from-literal=monacoToken=$DT_MONACO_TOKEN
# kubectl -n dynatrace create secret generic monaco-secret --from-literal=monacoToken=$DT_MONACO_TOKEN

# Install platform
#kubectl apply -f gitops/platform.yml



##########################
# 2. Run test harness
export OTEL_SERVICE_NAME=codespace-platform
export PYTEST_RUN_NAME=startup-automated-test
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
pytest --export-traces codespaces_test.py
echo "[post-start] pytest finished" >> ~/status

echo "[post-start] complete" >> ~/status
