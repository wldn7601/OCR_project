# =============================
# 1️⃣ 베이스 이미지 선택
# =============================
FROM python:3.12-slim

# =============================
# 2️⃣ 기본 환경 설정
# =============================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# =============================
# 3️⃣ 시스템 패키지 설치
# =============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    tesseract-ocr \
    tesseract-ocr-kor \
    && rm -rf /var/lib/apt/lists/*

# =============================
# 4️⃣ 종속성 설치
# =============================
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# =============================
# 5️⃣ 애플리케이션 복사
# =============================
COPY . .

# =============================
# 6️⃣ 환경 변수 파일 복사 (있다면)
# =============================

# 보안상의 이유로 .dockerignore에 .env를 추가 -> COPY 실패
# 컨테이너를 만들 때 docker run --env-file .env 로 주입해야 함
# COPY .env .env

# =============================
# 7️⃣ Gunicorn으로 Flask 실행
# =============================
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
