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

# Function to run docker-compose up -d in the ~/carlab-shoot-rx0 directory on a Raspberry Pi
run_docker_compose() {
  ip="$1"
  sshpass -p "${password}" ssh -oStrictHostKeyChecking=no "${username}@${ip}" 'bash -s' <<-'EOF'
    cd ~/carlab-shoot-rx0
    docker compose up -d
EOF
}

# Iterate over Raspberry Pi IPs and run docker-compose up -d in the ~/carlab-shoot-rx0 directory on each
for ip in "${raspberry_ips[@]}"; do
  echo "Running docker-compose up -d in ~/carlab-shoot-rx0 on Raspberry Pi at IP ${ip}..."
  run_docker_compose "${ip}"
  echo "docker-compose up -d completed on ${ip}"
done

echo "docker-compose up -d finished on all Raspberry Pis"

