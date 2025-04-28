import os
import datetime
import zipfile
from django.conf import settings
from django.core.management import call_command
import boto3  # للنسخ الاحتياطي على Amazon S3

class DatabaseBackup:
    @staticmethod
    def create_backup():
        # إنشاء مجلد للنسخ الاحتياطي إذا لم يكن موجوداً
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # إنشاء اسم الملف بالتاريخ والوقت
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        # إنشاء نسخة احتياطية من قاعدة البيانات
        with open(backup_file, 'w') as f:
            call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], 
                        indent=2, output=backup_file)
        
        # ضغط الملف
        zip_file = f'{backup_file}.zip'
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(backup_file, os.path.basename(backup_file))
        
        # حذف الملف غير المضغوط
        os.remove(backup_file)
        
        # رفع النسخة الاحتياطية إلى S3 (اختياري)
        if hasattr(settings, 'AWS_STORAGE_BUCKET_NAME'):
            s3 = boto3.client('s3')
            s3.upload_file(
                zip_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                f'backups/{os.path.basename(zip_file)}'
            )
        
        return zip_file 