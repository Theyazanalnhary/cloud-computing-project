# استخدام صورة Python خفيفة
FROM python:3.11-slim

# إنشاء مستخدم جديد لتحسين الأمان
RUN adduser --disabled-password --gecos '' appuser
USER appuser
WORKDIR /home/appuser/app

# نسخ ملف المتطلبات وتثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY --chown=appuser:appuser . .

# التأكد من أن ملف wsgi.py موجود (اختياري)
# RUN test -f web_system_crimnn/web_system_crimnn/wsgi.py || (echo "❌ ملف wsgi.py غير موجود!" && exit 1)

# جمع الملفات الثابتة
RUN python manage.py collectstatic --noinput

# فتح المنفذ 10000
EXPOSE 10000

# تشغيل Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "web_system_crimnn.wsgi:application"]
