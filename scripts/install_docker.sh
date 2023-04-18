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

# Function to install Docker on a Raspberry Pi
install_docker() {
  ip="$1"
  sshpass -p "${password}" ssh -oStrictHostKeyChecking=no "${username}@${ip}" 'bash -s' <<-'EOF'
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker pi
    rm get-docker.sh
EOF
}

# Iterate over Raspberry Pi IPs and install Docker on each
for ip in "${raspberry_ips[@]}"; do
  echo "Installing Docker on Raspberry Pi at IP ${ip}..."
  install_docker "${ip}"
  echo "Docker installation completed on ${ip}"
done

echo "Docker installation finished on all Raspberry Pis"

