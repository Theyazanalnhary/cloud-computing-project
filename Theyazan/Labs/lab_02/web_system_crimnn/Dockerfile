FROM python:3.11-slim

WORKDIR /app

# نسخ المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي كود المشروع
COPY . .

# تشغيل الخادمة باستخدام wsgi الصحيح
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_system_crimnn.wsgi:application"]
