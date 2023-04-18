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

# Function to pull the specified Docker image on a Raspberry Pi
pull_docker_image() {
  ip="$1"
  sshpass -p "${password}" ssh -oStrictHostKeyChecking=no "${username}@${ip}" 'bash -s' <<-'EOF'
    docker pull jhastoy/carlab-shoot-rx0
EOF
}

# Iterate over Raspberry Pi IPs and pull the Docker image on each
for ip in "${raspberry_ips[@]}"; do
  echo "Pulling Docker image on Raspberry Pi at IP ${ip}..."
  pull_docker_image "${ip}"
  echo "Docker image pull completed on ${ip}"
done

echo "Docker image pull finished on all Raspberry Pis"

