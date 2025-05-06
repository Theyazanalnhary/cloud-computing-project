# Theyazan/Labs/lab_02/web_system_crimnn/Dockerfile

FROM python:3.11-slim

# إنشاء مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ متطلبات بايثون وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ بقية ملفات المشروع
COPY . .

# فتح المنفذ المناسب
EXPOSE 8000

# تشغيل التطبيق باستخدام Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_system_crimnn.wsgi:application"]
