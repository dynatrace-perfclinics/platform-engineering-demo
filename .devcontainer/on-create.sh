#!/bin/bash

echo "[on-create] start" >> ~/status

# copy grafana.db to /grafana
#sudo cp deploy/grafanadata/grafana.db /grafana
#sudo chown -R 472:0 /grafana

# create local registry
#docker network create k3d
#k3d registry create registry.localhost --port 5500
#docker network connect k3d k3d-registry.localhost

# update the base docker images
#docker pull mcr.microsoft.com/dotnet/sdk:5.0-alpine
#docker pull mcr.microsoft.com/dotnet/aspnet:5.0-alpine
#docker pull mcr.microsoft.com/dotnet/sdk:5.0

echo "[on-create] complete" >> ~/status