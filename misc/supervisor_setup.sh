#!/bin/bash
set -e

APP_USER="hubuser"
BASE_DIR="/opt/queuinghub"
VENV_DIR="$BASE_DIR/venv"
SCRIPT_DIR="$VENV_DIR/scripts"
START_SCRIPT="$SCRIPT_DIR/start_gunicorn"
LOG_DIR="$BASE_DIR/logs"
SUPERVISOR_CONF="/etc/supervisor/conf.d/queuinghub.conf"

echo "== Creating script directory =="
sudo -u $APP_USER mkdir -p $SCRIPT_DIR

echo "== Creating start_gunicorn script =="
sudo -u $APP_USER tee $START_SCRIPT > /dev/null << 'EOF'
#!/bin/sh

cd /opt/queuinghub/queuinghub
. /opt/queuinghub/venv/bin/activate
. /opt/queuinghub/venv/bin/postactivate

exec gunicorn -w $GUNICORN_WORKERS "queuinghub:create_app()"
EOF

echo "== Making script executable =="
sudo chmod u+x $START_SCRIPT

echo "== Creating log directory =="
sudo -u $APP_USER mkdir -p $LOG_DIR

echo "== Installing supervisor =="
sudo apt update
sudo apt install -y supervisor

echo "== Creating supervisor config =="
sudo tee $SUPERVISOR_CONF > /dev/null << 'EOF'
[program:queuinghub]
command=/opt/queuinghub/venv/scripts/start_gunicorn
autostart=true
autorestart=true
user=hubuser

stdout_logfile=/opt/queuinghub/logs/gunicorn.log
redirect_stderr=true
EOF

echo "== Reloading supervisor =="
sudo systemctl restart supervisor

echo "== Updating supervisor programs =="
sudo systemctl reload supervisor
#sudo supervisorctl update

echo "== Done =="
