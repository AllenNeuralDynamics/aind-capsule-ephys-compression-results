# hash:sha256:2339225513b50093e2fb85627adaede73c313cb19c37c22d8ea7121da8abe75b
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        fonts-freefont-ttf=20120503-10 \
        libvips \
        msttcorefonts \
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
