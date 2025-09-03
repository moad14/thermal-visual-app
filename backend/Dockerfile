FROM python:3.10-slim

# تثبيت مكتبات النظام الضرورية
RUN apt-get update && \
    apt-get install -y libgl1 exiftool curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# نسخ متطلبات المشروع فقط
COPY backend/requirements.txt .

# تحديث pip وتثبيت الحزم مع timeout و retries
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --timeout=100 --retries=5 -i https://pypi.org/simple

# نسخ باقي ملفات المشروع
COPY backend ./backend
COPY frontend ./frontend

# إنشاء مجلد لتخزين وزن الموديل
RUN mkdir -p backend/runs/train/my_yolov8_model/weights

# تنزيل الموديل إذا تم تمرير رابط URL
ARG MODEL_URL
RUN if [ -n "${MODEL_URL}" ]; then \
      echo "🔽 تنزيل الموديل من ${MODEL_URL}" && \
      curl -L --retry 5 --retry-delay 10 -o backend/runs/train/my_yolov8_model/weights/best.pt "${MODEL_URL}"; \
    fi

# إعدادات التطبيق
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]
