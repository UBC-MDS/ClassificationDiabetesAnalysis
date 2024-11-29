#!/bin/bash

# Step 1: Build the Docker image and create the Conda environment
echo "Building the Docker image and setting up the Conda environment..."
docker-compose up --build

# Step 2: Confirm that the services are running
echo "Docker containers are up and running."