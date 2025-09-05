#!/bin/bash
set -e

# 1) create the socket dir on the host under /mnt (COS root is read‑only)
mkdir -p /mnt/cloudsql
chmod 755 /mnt/cloudsql

# 2) launch the proxy from its COS install location
/usr/bin/cloud_sql_proxy \
  -dir=/mnt/cloudsql \
  -instances=planar-outlook-454509-e8:us-west1:unimarketplace-pg &

# give it a moment
sleep 2

