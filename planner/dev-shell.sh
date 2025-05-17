#!/bin/bash

# Check if container is running
CONTAINER_ID=$(docker-compose ps -q app)
STATUS=$(docker inspect --format='{{.State.Status}}' $CONTAINER_ID 2>/dev/null)

if [ "$STATUS" != "running" ]; then
  echo "Starting development container..."
  docker-compose up -d
fi

# Connect to the container with interactive shell
echo "Connecting to development container..."
docker-compose exec app bash -c "cd /home && bash"