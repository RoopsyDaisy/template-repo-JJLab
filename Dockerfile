FROM docker.io/nvidia/cuda:13.0.1-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------------------------------------------------------
# Base system packages + GDAL/PROJ for geospatial support
# -----------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        python3.12 python3.12-dev python3-pip \
        build-essential git curl ca-certificates \
        rsync openssh-client sudo \
        # GDAL and geospatial libraries
        gdal-bin libgdal-dev \
        libproj-dev proj-bin \
        libgeos-dev \
        # Node.js for MCP servers (npx)
        nodejs npm \
        && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Install uv package manager
# -----------------------------------------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

# -----------------------------------------------------------------------------
# Create unprivileged user (UID/GID rewritten by devcontainers)
# -----------------------------------------------------------------------------
ARG USERNAME=vscode
RUN useradd -m "$USERNAME" && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# -----------------------------------------------------------------------------
# Workspace setup
# -----------------------------------------------------------------------------
WORKDIR /workspace
USER ${USERNAME}

CMD ["/bin/bash"]
