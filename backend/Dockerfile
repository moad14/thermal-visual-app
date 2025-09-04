# استخدم صورة Python الرسمية الخفيفة
FROM python:3.10-slim

# ضبط المتغيرات البيئية لتجنب أي تفاعلية أثناء التثبيت
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# إنشاء مجلد التطبيق
WORKDIR /app

# نسخ ملفات requirements.txt أولًا لتسريع cache
COPY requirements.txt .

# تثبيت pip وتثبيت المتطلبات
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# الأمر الافتراضي لتشغيل التطبيق
# استبدل `app.py` باسم ملفك الرئيسي
CMD ["python", "app.py"]
