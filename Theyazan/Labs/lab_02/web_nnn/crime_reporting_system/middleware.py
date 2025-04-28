from django.http import HttpResponseForbidden
from django.conf import settings
import re
import time
from django.db import connection

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # التحقق من محاولات XSS
        if self._contains_xss(request):
            return HttpResponseForbidden("محتوى غير آمن")
            
        # التحقق من محاولات SQL Injection
        if self._contains_sql_injection(request):
            return HttpResponseForbidden("محتوى غير آمن")
            
        response = self.get_response(request)
        
        # إضافة headers أمان
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
        
    def _contains_xss(self, request):
        dangerous_patterns = [
            r'<script.*?>',
            r'javascript:',
            r'onload=',
            r'onerror='
        ]
        return self._check_patterns(request, dangerous_patterns)
        
    def _contains_sql_injection(self, request):
        sql_patterns = [
            r'UNION.*?SELECT',
            r'DROP.*?TABLE',
            r'--.*?',
            r';.*?'
        ]
        return self._check_patterns(request, sql_patterns)
        
    def _check_patterns(self, request, patterns):
        for key, value in request.GET.items():
            for pattern in patterns:
                if re.search(pattern, value, re.I):
                    return True
        return False 

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        # عدد الاستعلامات قبل تنفيذ الطلب
        n_queries_before = len(connection.queries)
        
        response = self.get_response(request)
        
        # حساب الوقت المستغرق وعدد الاستعلامات
        duration = time.time() - start_time
        n_queries_after = len(connection.queries)
        n_queries = n_queries_after - n_queries_before
        
        # إضافة headers للأداء
        response['X-Page-Generation-Duration-ms'] = int(duration * 1000)
        response['X-Queries-Count'] = n_queries
        
        return response 