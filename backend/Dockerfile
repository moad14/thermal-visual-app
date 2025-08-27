# صورة بايثون خفيفة
FROM python:3.10-slim

# تثبيت exiftool و libgl (ضروري لـ OpenCV)
RUN apt-get update && apt-get install -y exiftool libgl1 curl && rm -rf /var/lib/apt/lists/*

# مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت الحزم
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع (backend + frontend)
COPY . .

# تنزيل الموديل إذا لم يكن موجود
ARG MODEL_URL
RUN if [ -n "${MODEL_URL}" ]; then \
    mkdir -p runs/train/my_yolov8_model/weights && \
    curl -L -o runs/train/my_yolov8_model/weights/best.pt "${MODEL_URL}"; \
    fi

# تعيين منفذ التطبيق
ENV PORT=8000
EXPOSE 8000

# أمر التشغيل
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]
