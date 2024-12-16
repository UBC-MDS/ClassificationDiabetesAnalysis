#!/bin/bash

# Step 1: clean up all containers and networks associated with `docker-compose.yml` project
docker-compose down --rmi all --volumes

# Step 2: Build the Docker image and create the Conda environment
echo "Building the Docker image and setting up the Conda environment..."
docker-compose up --build

# Step 3: Confirm that the services are running
echo "Docker containers are up and running."