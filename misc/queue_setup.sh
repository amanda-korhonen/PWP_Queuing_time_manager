#!/bin/bash
set -e  # exit on error

# Variables
APP_DIR="/opt/queuinghub"
VENV_DIR="$APP_DIR/venv"
REPO_DIR="$APP_DIR/queuinghub"
REPO_URL="https://github.com/amanda-korhonen/PWP_Queuing_time_manager.git"
APP_USER="hubuser"
CURRENT_USER="$(whoami)"

#delete any remnants
sudo rm -r $APP_DIR
echo "== Creating system user =="
sudo useradd --system --create-home --shell /bin/bash $APP_USER || true

echo "== Adding current user to group =="
sudo usermod -aG $APP_USER $CURRENT_USER

echo "== Creating application directory =="
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR
sudo chmod -R o-rwx $APP_DIR

echo "== Installing dependencies =="
sudo apt update
sudo apt install  git
sudo apt-get install curl
python3 -m pip install "gunicorn<25"

echo "== Creating virtual environment =="
sudo -u $APP_USER python3 -m venv $VENV_DIR

echo "== Cloning repository =="
sudo -u $APP_USER git clone $REPO_URL $REPO_DIR

echo "== Creating postactivate script =="
sudo -u $APP_USER bash -c "echo 'export GUNICORN_WORKERS=3' > $VENV_DIR/bin/postactivate"

echo "== Installing application =="
sudo -u $APP_USER bash -c "
    source $VENV_DIR/bin/activate
    source $VENV_DIR/bin/postactivate
    cd $REPO_DIR
    pip install -r requirements.txt
    python3 -m pip install 'gunicorn<25'
"

echo "== Initializing database and generating test data =="
sudo -u $APP_USER bash -c "
    source $VENV_DIR/bin/activate
    source $VENV_DIR/bin/postactivate
    cd $REPO_DIR
    flask --app=queuinghub init-db
    python3 -m queuinghub.db_populate
    #flask --app=queuinghub testgen
"

echo "== Starting Gunicorn =="
sudo -u $APP_USER bash -c "
    source $VENV_DIR/bin/activate
    source $VENV_DIR/bin/postactivate
    cd $REPO_DIR
    gunicorn -w \$GUNICORN_WORKERS 'queuinghub:create_app()'
"
