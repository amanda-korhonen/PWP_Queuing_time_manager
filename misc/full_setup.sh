echo "== Starting full deployment =="

# Ensure scripts are executable
chmod +x queue_setup.sh
chmod +x supervisor_setup.sh
chmod +x nginx_setup.sh

echo "== Running base setup (app, venv, repo) =="
./queue_setup.sh

echo "== Running supervisor setup =="
./supervisor_setup.sh

echo "== Running nginx setup =="
./nginx_setup.sh

echo "== Deployment complete =="
echo ""
echo "Test with:"
echo "  curl http://localhost:8000/api/"
