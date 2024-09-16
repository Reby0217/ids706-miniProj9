# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/codespaces-linux/.devcontainer/base.Dockerfile

# Use a base image compatible with ARM and AMD64
FROM mcr.microsoft.com/devcontainers/python:3.9-bullseye

# Install necessary dependencies
RUN apt-get update && apt-get -y install --no-install-recommends \
   python3-venv \
   gcc

# Set environment variables
ARG USER="codespace"
ARG VENV_PATH="/home/${USER}/venv"

# Set the working directory (adjusted for better context handling)
WORKDIR /workspace

# Copy necessary files
COPY requirements.txt /tmp/
COPY Makefile /tmp/

# Create and activate the virtual environment, then install Python dependencies 
RUN /usr/bin/python3 -m venv ${VENV_PATH} \
   && ${VENV_PATH}/bin/pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt \
   && rm -rf /tmp/requirements.txt

# Clean up apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the default shell to bash for the user
USER root
SHELL ["/bin/bash", "-c"]