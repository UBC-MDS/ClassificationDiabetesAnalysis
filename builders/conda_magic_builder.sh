#!/bin/bash

# Set environment name and required dependency versions
ENV_NAME="diabetes_predictor"
CONDA_VERSION="24.11.0"
CONDA_LOCK_VERSION="2.5.7"
MAMBA_VERSION="2.0.4"
JUPYTERLAB_VERSION="4.3.2"
NB_CONDA_KERNELS_VERSION="2.5.1"

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "$1 is not installed. Please install it before running this script."
        exit 1
    fi
}

# Function to check and install dependencies
ensure_dependency() {
    local package="$1"
    local version="$2"
    echo "Checking if $package (version $version or higher) is installed..."
    if ! conda list "$package" | grep -q "$package.*$version"; then
        echo "$package is not installed or is outdated. Installing..."
        conda install -c conda-forge "$package>=$version" --yes
    else
        echo "$package is up-to-date."
    fi
}

# Step 1: Check for Conda and initialize if necessary
check_command conda
if ! grep -q 'conda' <<< "$PATH"; then
    echo "Conda is not initialized. Initializing Conda..."
    conda init
    exec bash
fi

# Step 2: Remove the existing environment if it exists
if conda env list | grep -q "^${ENV_NAME}"; then
    echo "Environment '${ENV_NAME}' already exists. Removing it..."
    conda env remove --name "$ENV_NAME" --yes
fi

# # Step 3: Create the Conda environment from environment.yml
# echo "Creating the Conda environment from environment.yml..."
# conda env create --file environment.yml --name "$ENV_NAME"

# Step 3: Ensure all dependencies are installed
ensure_dependency "conda" "$CONDA_VERSION"
ensure_dependency "conda-lock" "$CONDA_LOCK_VERSION"
ensure_dependency "mamba" "$MAMBA_VERSION"
ensure_dependency "jupyterlab" "$JUPYTERLAB_VERSION"
ensure_dependency "nb_conda_kernels" "$NB_CONDA_KERNELS_VERSION"

# Step 4: Create a conda-lock.yml file
echo "Creating a conda-lock.yml from environment.yml across all platforms"
conda-lock lock --file environment.yml

# Step 5: Install environment using conda-lock
echo "Installing environment using conda-lock..."
conda-lock install --name "$ENV_NAME" conda-lock.yml

# Step 6: Activate the Conda environment
echo "Activating the environment..."
eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"

# # Step 7: Start JupyterLab
# echo "Starting JupyterLab..."
# jupyter lab