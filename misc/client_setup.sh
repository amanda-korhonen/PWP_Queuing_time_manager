#!/bin/bash

# =============================================================================
# Frontend (client) setup script
# Run this from the misc directory
# Usage: bash setup_client.sh [nginx-config-path] [server-name]
# Example: bash setup_client.sh /etc/nginx/sites-available/queueapp queueapp.ddns.net
# =============================================================================

set -e

NGINX_CONF=${1:-/etc/nginx/sites-available/queuinghub}
SERVER_NAME=${2:-localhost}

echo "==> Moving client to /var/www..."
cd ..

if [ -d "/var/www/client" ]; then
    echo "    /var/www/client already exists, removing old version..."
    sudo rm -rf /var/www/client
fi

sudo mv client /var/www/client

echo "==> Setting Nginx permissions on /var/www/client..."
sudo chown -R www-data:www-data /var/www/client

echo "==> Writing Nginx config to $NGINX_CONF..."
sudo tee "$NGINX_CONF" > /dev/null <<EOF
server {
    listen 80 default_server;
    return 444;
}

upstream app_server {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80 deferred;
    client_max_body_size 4G;
    server_name $SERVER_NAME;
    keepalive_timeout 5;

    location / {
        root /var/www/client;
        index home.html;
        try_files \$uri \$uri/ =404;
    }

    location /api/ {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }

    # Location for all Flasgger needs
    location ~* ^/(apidocs|flasgger_static|apispec_1.json) {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }
}
EOF

echo "==> Testing Nginx config..."
sudo nginx -t

echo "==> Reloading Nginx..."
sudo systemctl reload nginx

echo ""
echo "==> Done! Frontend is live at http://$SERVER_NAME/"
echo "    To enable HTTPS, run: sudo certbot --nginx -d your.servername.com"
