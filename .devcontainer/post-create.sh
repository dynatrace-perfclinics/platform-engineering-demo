#!/bin/bash

echo "[post-create] start" >> ~/status

# this runs in background after UI is available

# (optional) upgrade packages
#sudo apt-get update
#sudo apt-get upgrade -y
#sudo apt-get autoremove -y
#sudo apt-get clean -y

# add your commands here

##########################
# 1. Install Python, gh CLI and test harness dependencies
sudo apt install gh -y
sudo apt install -y python3
sudo apt install -y python3-pip
pip install --break-system-packages -r requirements.txt

wget -O argocd https://github.com/argoproj/argo-cd/releases/download/v2.12.2/argocd-linux-amd64
chmod +x argocd
sudo mv argocd /usr/bin


#echo alias k=kubectl >> /home/vscode/.zshrc

# Install and configure cluster
python3 cluster_installer.py

echo "[post-create] complete" >> ~/status