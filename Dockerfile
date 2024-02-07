FROM mambaorg/micromamba:latest
WORKDIR /app
COPY --chown=$MAMBA_USER:$MAMBA_USER . .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes