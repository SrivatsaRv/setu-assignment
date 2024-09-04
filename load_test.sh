#!/bin/sh

# Install sysbench and mysql client if not installed already
apk add --no-cache sysbench mysql-client

# Generate CPU and Memory load on NGINX (which proxies to SQL1 first)
sysbench --test=cpu --cpu-max-prime=20000 run &
sysbench --test=memory --memory-total-size=6G run &

# SQL Transaction load - initially targeting NGINX (which proxies to SQL1 initially)
while true; do
  for i in $(seq 1 20); do  # Increase number of simultaneous connections
    name="User$(shuf -i 1-1000 -n 1)"
    email="user$(shuf -i 1-1000 -n 1)@example.com"
    # Target NGINX on port 8080 (mapped to NGINX 80) and MySQL port 3306
    mysql -h nginx -P 8080 -u user -ppassword -e "INSERT INTO users (name, email) VALUES ('$name', '$email');" testdb &
  done
  sleep 1
done
