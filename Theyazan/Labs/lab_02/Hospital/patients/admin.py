from django.contrib import admin
from . models  import  Patients
# Register your models here.

admin.site.site_header='H.P.S'
admin.site.site_title='H.PS'
admin.site.register(Patients)