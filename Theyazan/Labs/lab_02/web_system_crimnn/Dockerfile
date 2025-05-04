# استخدام صورة Python خفيفة
FROM python:3.11-slim

# تعيين دليل العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# التأكد من أن ملف wsgi.py موجود
RUN test -f web_system_crimnn/web_system_crimnn/wsgi.py || (echo "❌ ملف wsgi.py غير موجود!" && exit 1)

# فتح المنفذ 8000
EXPOSE 8000

# تشغيل Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_system_crimnn.wsgi:application"]
