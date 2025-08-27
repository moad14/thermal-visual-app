# صورة بايثون خفيفة
FROM python:3.10-slim

# تثبيت مكتبات النظام الضرورية
RUN apt-get update && \
    apt-get install -y libgl1 exiftool curl && \
    rm -rf /var/lib/apt/lists/*

# مجلد العمل
WORKDIR /app

# نسخ متطلبات المشروع وتثبيتها
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY backend ./backend
COPY frontend ./frontend

# إنشاء مجلد لتخزين وزن الموديل
RUN mkdir -p backend/runs/train/my_yolov8_model/weights

# تنزيل الموديل تلقائيًا إذا تم تمرير رابط URL
ARG MODEL_URL
RUN if [ -n "${MODEL_URL}" ]; then \
      echo "🔽 تنزيل الموديل من ${MODEL_URL}" && \
      curl -L -o backend/runs/train/my_yolov8_model/weights/best.pt "${MODEL_URL}"; \
    fi

# تعيين منفذ التطبيق
ENV PORT=8000
EXPOSE 8000

# أمر تشغيل FastAPI
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]
