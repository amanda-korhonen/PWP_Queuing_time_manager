echo "== Starting full deployment =="

# Ensure scripts are executable
chmod +x setup_queuinghub.sh
chmod +x setup_supervisor.sh
chmod +x setup_nginx.sh

echo "== Running base setup (app, venv, repo) =="
./queue_setup.sh

echo "== Running supervisor setup =="
./supervisor_setup.sh

echo "== Running nginx setup =="
./nginx_setup.sh

echo "== Deployment complete =="
echo ""
echo "Test with:"
echo "  curl http://localhost"
