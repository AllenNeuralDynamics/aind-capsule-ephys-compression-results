# hash:sha256:624ec40008a00d4c6f1e798a57f31bac9d53751e4a717cfdc9a8b8df6ae16837
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN conda install -y \
        jupyterlab==3.0.9 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    nbconvert==7.2.9 \
    numpy==1.24.2 \
    pandas==1.5.3 \
    scikit-learn==1.2.1 \
    scikit-posthocs==0.7.0 \
    scipy==1.10.1 \
    seaborn==0.12.2

COPY postInstall /
RUN /postInstall
