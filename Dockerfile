# 빌더 스테이지
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH" \
    TESSDATA_PREFIX=/usr/local/share/tessdata

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    gnupg \
    ca-certificates \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3.11 \
    python3.11-venv \
    python3.11-distutils \
    fonts-ubuntu \
    fontconfig \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --set python3 /usr/bin/python3.11 \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && fc-cache -fv

WORKDIR /app

COPY ./requirements ./requirements
COPY unstructured ./unstructured

RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && find requirements/ -type f -name "*.txt" -exec pip install --no-cache-dir -r '{}' ';' \
    && pip install --no-cache-dir unstructured.paddlepaddle \
    && pip cache purge

RUN python3 -c "from unstructured.nlp.tokenize import download_nltk_packages; download_nltk_packages()" \
    && python3 -c "from unstructured.partition.model_init import initialize; initialize()" \
    && python3 -c "from unstructured_inference.models.tables import UnstructuredTableTransformerModel; model = UnstructuredTableTransformerModel(); model.initialize('microsoft/table-transformer-structure-recognition')" \
    && if [ -d "/usr/local/share/tessdata" ]; then rm -rf /usr/local/share/tessdata; fi

# 실행 스테이지
FROM ubuntu:22.04-minimal AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH" \
    TESSDATA_PREFIX=/usr/local/share/tessdata

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    fonts-ubuntu \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -fv

WORKDIR /

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

CMD ["python3"]