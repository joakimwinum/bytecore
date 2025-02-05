FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

USER vscode

RUN curl -fsSL https://pyenv.run | bash

ENV PYENV_ROOT="/home/vscode/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN pyenv install 3.11 \
    && pyenv global 3.11
