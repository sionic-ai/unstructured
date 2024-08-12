FROM ubuntu:22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    gnupg \
    ca-certificates \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# GPG 키를 수동으로 추가
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776

# PPA 추가 및 Python 3.11 설치
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3.11-distutils \
    fonts-ubuntu \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python 3.11을 기본 Python으로 설정
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --set python3 /usr/bin/python3.11

# pip 설치
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

WORKDIR /

COPY ./requirements requirements/
COPY unstructured unstructured
# COPY test_unstructured test_unstructured
# COPY example-docs example-docs

RUN fc-cache -fv

# CPU 전용 최신 PyTorch 설치 및 requirements 설치
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    find requirements/ -type f -name "*.txt" -exec pip install --no-cache-dir -r '{}' ';' && \
    pip install --no-cache-dir unstructured.paddlepaddle

# 초기화 및 모델 다운로드
RUN python3 -c "from unstructured.nlp.tokenize import download_nltk_packages; download_nltk_packages()" && \
    python3 -c "from unstructured.partition.model_init import initialize; initialize()" && \
    python3 -c "from unstructured_inference.models.tables import UnstructuredTableTransformerModel; model = UnstructuredTableTransformerModel(); model.initialize('microsoft/table-transformer-structure-recognition')"

ENV PATH="${PATH}:/root/.local/bin"
ENV TESSDATA_PREFIX=/usr/local/share/tessdata

RUN if [ -d "/usr/local/share/tessdata" ]; then rm -rf /usr/local/share/tessdata; fi

CMD ["/bin/bash"]