from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class ReportAccessMixin(UserPassesTestMixin):
    def test_func(self):
        report = self.get_object()
        user = self.request.user
        
        # المدير يمكنه الوصول لكل شيء
        if user.user_type == 'admin':
            return True
            
        # المحقق يمكنه الوصول للتقارير المسندة إليه
        if user.user_type == 'investigator' and report.assigned_to == user:
            return True
            
        # ضابط الشرطة يمكنه الوصول للتقارير في منطقته
        if user.user_type == 'police' and report.location in user.department:
            return True
            
        return False

    def handle_no_permission(self):
        raise PermissionDenied("ليس لديك صلاحية للوصول لهذا التقرير") 