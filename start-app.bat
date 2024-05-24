@echo off
docker-compose up -d --build
docker image prune -f > nul 2>&1