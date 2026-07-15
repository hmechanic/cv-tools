# Pin the multi-platform manifest so builds use the reviewed TeX Live image.
FROM texlive/texlive:latest@sha256:d39efa547acfa518072600315280f92357ca8e0b9e295e09b6ccd5f5d82a1373

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV VENV_PATH=/venv

# Install Python and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a Python virtual environment
RUN python3 -m venv $VENV_PATH

# Install Python dependencies
COPY requirements.lock /app/
RUN $VENV_PATH/bin/pip install --require-hashes -r /app/requirements.lock

# Setup entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
WORKDIR /workdir
ENTRYPOINT ["/entrypoint.sh"]
