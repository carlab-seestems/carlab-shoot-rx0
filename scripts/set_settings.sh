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

# settings

ISO_DEFINED="160"
TEMP_DEFINED="5000"


# Function to send a GET request with the settings to a Raspberry Pi
send_get_request() {
  ip="$1"

  curl -s "http://${ip}:8081/set_iso?iso=${ISO_DEFINED}"
  curl -s "http://${ip}:8081/set_color_temp?temp=${TEMP_DEFINED}"
}

# Iterate over Raspberry Pi IPs and send the GET request to each
for ip in "${raspberry_ips[@]}"; do
  echo "Sending GET request to Raspberry Pi at IP ${ip}..."
  send_get_request "${ip}"
  echo "GET request completed on ${ip}"
done

echo "GET requests finished on all Raspberry Pis"
