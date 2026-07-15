# Keep Python aligned with local development and CI, and pin both stages by
# multi-platform digest so rebuilds do not silently change their runtimes.
FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c AS python-deps

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir --require-hashes -r /app/requirements.lock

# Pin the multi-platform manifest so builds use the reviewed TeX Live image.
FROM texlive/texlive:latest@sha256:d39efa547acfa518072600315280f92357ca8e0b9e295e09b6ccd5f5d82a1373

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# The TeX Live image tracks Debian testing. Copying the pinned Python runtime
# avoids an unversioned apt upgrade and the compiler toolchain it recommends.
COPY --from=python-deps /usr/local/ /usr/local/
COPY --from=python-deps /venv/ /venv/

COPY --chmod=0755 entrypoint.sh /entrypoint.sh
WORKDIR /workdir
USER texlive
ENTRYPOINT ["/entrypoint.sh"]
