#!/bin/bash

# Raspberry Pi IP addresses
raspberry_ips=(
192.168.0.102
192.168.0.104
192.168.0.105
192.168.0.107
192.168.0.108
192.168.0.109
192.168.0.110
192.168.0.111
192.168.0.112
)

# SSH username and password
username="pi"
password="raspberry"

# Git repository to clone
repo="https://github.com/carlab-seestems/carlab-shoot-rx0.git"

# Function to install Git and clone the specified repository on a Raspberry Pi
install_git_and_clone_repo() {
  ip="$1"
  sshpass -p "${password}" ssh -oStrictHostKeyChecking=no "${username}@${ip}" 'bash -s' <<EOF
    sudo apt-get update
    sudo apt-get install -y git
    git clone ${repo}
EOF
}

# Iterate over Raspberry Pi IPs, install Git, and clone the repository on each
for ip in "${raspberry_ips[@]}"; do
  echo "Installing Git and cloning repository on Raspberry Pi at IP ${ip}..."
  install_git_and_clone_repo "${ip}"
  echo "Git installation and repository clone completed on ${ip}"
done

echo "Git installation and repository clone finished on all Raspberry Pis"

