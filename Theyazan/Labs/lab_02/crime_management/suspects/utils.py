from django.db.models import Q
from .models import Suspect

def search_suspects(query):
    """
    البحث عن المتهمين بناءً على الاسم الكامل أو رقم البلاغ.
    """
    if not query:
        return Suspect.objects.none()  # إرجاع قائمة فارغة إذا كان الاستعلام فارغًا
    
    suspects = Suspect.objects.filter(
        Q(full_name__icontains=query) |  # البحث بالاسم الكامل
        Q(crime__report_number__icontains=query)  # البحث برقم البلاغ
    )
    return suspects