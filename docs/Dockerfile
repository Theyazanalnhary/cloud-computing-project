# استخدام صورة Python خفيفة
FROM python:3.11-slim

# تحديد دليل العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيته
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الكود
COPY . .

# التأكد من وجود ملف wsgi.py
RUN if [ ! -f "Theyazan/Labs/lab_02/web_system_crimnn/wsgi.py" ]; then \
      echo "❌ ملف wsgi.py غير موجود في المسار الصحيح!"; \
      exit 1; \
    fi

# تشغيل الخدمة باستخدام Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_system_crimnn.wsgi:application"]
