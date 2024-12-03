# Lightweight Linux base image with Python pre-installed
FROM python:3.13-slim

# Set env variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    jq \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Grype
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh

# Install Trivy
RUN curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Install Syft
RUN curl -sfL https://raw.githubusercontent.com/anchore/syft/main/install.sh

# Install sigstore (cosign)
RUN curl -sSfL https://raw.githubusercontent.com/sigstore/cosign/main/install.sh | sh

# Copy python dependencies file
COPY requirements.txt /app/requirements.txt

# Add a working directory
WORKDIR /app

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Load Vuln Databases
RUN trivy --download-db-only
RUN grype db update

# Copy CLI and utilities
COPY cli.py /app/cli.py 
COPY utils.py /app/utils.py

# Health check to ensure tools are installed
HEALTHCHECK CMD syft --version && grype --version && trivy --version || exit 1

CMD ["python", "cli.py"]