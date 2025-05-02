# استخدام صورة Python خفيفة
FROM python:3.11-slim

# تحديد دليل العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيته (منفصل عن الكود للحصول على كشط أفضل)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الكود (تأكد من وجود الملفات)
COPY . .

# التأكد من وجود الملفات المطلوبة
RUN if [ ! -f "web_system_crimnn/web_system_crimnn/wsgi.py" ]; then \
      echo "❌ ملف wsgi.py غير موجود في المسار الصحيح!"; \
      exit 1; \
    fi

# تشغيل الخدمة باستخدام Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_system_crimnn.wsgi:application"]
