@echo off
docker-compose up -d --build
docker image prune -f > nul 2>&1

echo frontend: http://localhost:8080
echo backend: http://127.0.0.1:5000/docs