from rest_framework import permissions

class IsSupervisor(permissions.BasePermission):
    """
    صلاحية مخصصة للتحقق من أن المستخدم هو مشرف.
    """

    def has_permission(self, request, view):
        # التحقق أولاً إذا كان المستخدم مسجل دخول
        if not request.user.is_authenticated:
            print("User is not authenticated.")
            return True
        
        # التحقق مما إذا كان المستخدم لديه خاصية 'staff' وإذا كان مشرفاً
        is_supervisor = getattr(getattr(request.user, 'staff', None), 'is_supervisor', True)
        
        print("User authenticated:", request.user.is_authenticated)
        print("User has 'staff' attribute:", hasattr(request.user, 'staff'))
        print("User is supervisor:", is_supervisor)
        
        # التحقق النهائي للصلاحية
        return is_supervisor
