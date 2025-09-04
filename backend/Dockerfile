# استخدم صورة Python الرسمية الخفيفة
FROM python:3.10-slim

# منع التفاعلية وتسريع التشغيل
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# إنشاء مجلد المشروع
WORKDIR /app

# نسخ الملفات الخاصة بالـ backend
COPY backend/requirements.txt .
COPY backend/ .

# تحديث pip وتثبيت المتطلبات
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# تشغيل FastAPI باستخدام Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
