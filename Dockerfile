# استخدم صورة Python الرسمية الخفيفة
FROM python:3.10-slim

# منع تفاعلية التثبيت وتسريع التشغيل
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# إنشاء مجلد المشروع
WORKDIR /app

# نسخ requirements أولًا لتسريع cache
COPY requirements.txt .

# تحديث pip وتثبيت المتطلبات
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تشغيل FastAPI باستخدام Uvicorn
# استبدل "main.py" باسم الملف الذي يحتوي على الكود الذي أرسلته
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
