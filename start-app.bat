@echo off
docker-compose up --build
docker image prune -f > nul 2>&1