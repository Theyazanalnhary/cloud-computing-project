from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class SecureFileStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        )
    
    def get_valid_name(self, name):
        """تنظيف اسم الملف وإضافة timestamp"""
        from datetime import datetime
        name = super().get_valid_name(name)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(name)
        return f"{name}_{timestamp}{ext}"
    
    def _save(self, name, content):
        """تشفير الملف قبل حفظه"""
        # يمكن إضافة تشفير هنا
        return super()._save(name, content) 