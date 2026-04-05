#!/bin/bash
set -e

NGINX_CONF="/etc/nginx/sites-available/queuinghub"
ENABLED_LINK="/etc/nginx/sites-enabled/queuinghub"

echo "== Installing nginx =="
sudo apt update
sudo apt install -y nginx

echo "== Creating nginx config =="

sudo tee $NGINX_CONF > /dev/null << 'EOF'
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

    server_name localhost;

    keepalive_timeout 5;

    root /opt/queuinghub/queuinghub/static/;

    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;

        proxy_redirect off;
        proxy_pass http://app_server;
    }
}
EOF

echo "== Enabling site =="
sudo ln -sf $NGINX_CONF $ENABLED_LINK

echo "== Removing default site =="
sudo rm -f /etc/nginx/sites-enabled/default

echo "== Testing nginx config =="
sudo nginx -t

echo "== Reloading nginx =="
sudo systemctl reload nginx

echo "== Done =="
