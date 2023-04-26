# hash:sha256:bd9ee9f91264dd0329f7a4fdc371d77707c2a9f4c3d5ff00ce1c5e8f7b321405
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libvips \
    && rm -rf /var/lib/apt/lists/*

RUN conda install -y \
        jupyterlab==3.0.9 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    nbconvert==7.2.9 \
    numpy==1.24.3 \
    pandas==2.0.1 \
    pyvips==2.2.1 \
    scikit-learn==1.2.2 \
    scikit-posthocs==0.7.0 \
    scipy==1.10.1 \
    seaborn==0.12.2 \
    wavpack-numcodecs==0.1.3

COPY postInstall /
RUN /postInstall
