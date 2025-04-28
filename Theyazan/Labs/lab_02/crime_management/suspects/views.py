from django.shortcuts import render, get_object_or_404, redirect
from .models import Suspect
from .forms import SuspectForm

def home(request):
    suspects = Suspect.objects.all()
    return render(request, 'suspecthome.html', {'suspects': suspects})

def homes(request):
    suspects = Suspect.objects.all()
    return render(request, 'suspecthome.html', {'suspects': suspects})


def suspect_list(request):
    # الحصول على كلمة البحث من طلب GET
    query = request.GET.get('q', '').strip()  # إزالة الفراغات الزائدة
    
    # استعلام البيانات بناءً على البحث
    if query:
        suspects = Suspect.objects.filter(full_name__icontains=query).order_by('full_name')
    else:
        suspects = Suspect.objects.all().order_by('full_name')  # ترتيب حسب الاسم
    
    # التحقق من البيانات المُسترجعة (للأغراض التصحيحية)
    print(f"Query: {query}")
    print("suspects retrieved:", suspects)
   
    # استعلام جميع الجرائم مع عدد المجني عليهم
    crimes = Crime.objects.all().prefetch_related('suspects').order_by('id')

    context = {
        'suspects': suspects,
        'crimes': crimes,
        'query': query,
    }

    return render(request, 'suspect_list.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Suspect, Crime
from .forms import SuspectForm
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import SuspectForm
from .models import Crime

def add_suspect(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    
    if request.method == "POST":
        form = SuspectForm(request.POST, request.FILES, crime_id=crime_id)
        if form.is_valid():
            try:
                suspect = form.save()  # يتم الحفظ والربط تلقائياً في form.save()
                
                # عرض رسالة نجاح مختلفة إذا كان المتهم موجوداً مسبقاً وتم ربطه فقط
                if 'non_field_errors' in form._errors:
                    for error in form._errors['non_field_errors']:
                        messages.warning(request, error)
                else:
                    messages.success(request, "تم إضافة المتهم بنجاح")
                
                return redirect('suspects:add_suspect', crime_id=crime.id)
            
            except ValidationError as e:
                # معالجة أخطاء التحقق من الصحة
                for field, error_list in e.message_dict.items():
                    for error in error_list:
                        if field == 'non_field_errors':
                            messages.warning(request, error)
                        else:
                            messages.error(request, f"{form.fields[field].label}: {error}")
            except Exception as e:
                messages.error(request, f"حدث خطأ غير متوقع: {str(e)}")
    else:
        form = SuspectForm(crime_id=crime_id)

    # تحضير الرسائل للقالب (إذا كنت تستخدم JavaScript لعرضها)
    messages_list = [
        {
            'tags': message.tags,
            'text': str(message.message),
            'extra_tags': message.extra_tags
        } for message in messages.get_messages(request)
    ]

    return render(request, 'add_suspect.html.html', {
        'form': form,
        'crime': crime,
        'messages_json': json.dumps(messages_list, ensure_ascii=False)
    })
from django.http import JsonResponse
from django.http import JsonResponse

from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import json

from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import SuspectForm
from .models import Crime
import json

def add_suspect(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    form = SuspectForm(crime_id=crime_id)

    if request.method == "POST":
        form = SuspectForm(request.POST, request.FILES, crime_id=crime_id)
        if form.is_valid():
            try:
                suspect = form.save(commit=False)
                suspect.save()
                crime.suspects.add(suspect)  # ربط المتهم بالجريمة
                messages.success(request, "تم إضافة المتهم بنجاح")
                return redirect('suspects:add_suspect', crime_id=crime.id)
            except ValidationError as e:
                for error in e.message_dict.get('non_field_errors', []):
                    messages.error(request, error)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    # تحضير الرسائل للقالب
    messages_list = []
    for message in messages.get_messages(request):
        messages_list.append({
            'tags': message.tags,
            'text': str(message.message)
        })

    return render(request, 'add_suspect.html', {
        'form': form,
        'crime': crime,
        'messages_json': json.dumps(messages_list, ensure_ascii=False)
    })

def suspect_list_for_crime(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    suspects = Suspect.objects.filter(crime=crime)  # قائمة المجني عليهم لهذه الجريمة
    return render(request, 'suspects_list_for_crime.html', {'crime': crime, 'suspects': suspects})

from django.http import JsonResponse
from django.contrib import messages

def edit_suspect(request, suspect_id):
    suspect = get_object_or_404(Suspect, suspect_id=suspect_id)
    if request.method == 'POST':
        form = SuspectForm(request.POST, instance=suspect)
        if form.is_valid():
            form.save()
            # إرجاع استجابة JSON بنجاح
            return JsonResponse({
                'success': True,
                'message': 'تم تحديث بيانات المتهم بنجاح.',
                'redirect_url': reverse('suspects:suspect_list')
            })
        else:
            # جمع الأخطاء وإرجاعها كاستجابة JSON
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'message': 'يوجد أخطاء في البيانات المدخلة.',
                'errors': errors
            }, status=400)
    else:
        form = SuspectForm(instance=suspect)
    return render(request, 'edit_suspect.html', {'form': form})

def delete_suspect(request, suspect_id):
    suspect = get_object_or_404(Suspect, suspect_id=suspect_id)
    if request.method == 'POST':
        suspect.delete()
        return redirect('suspects:suspect_list')
    return render(request, 'delete_suspect.html', {'suspect': suspect})

from django.shortcuts import render
from .models import Suspect, Crime
from .forms import SearchForm

from django.shortcuts import render
from django.db.models import Q
from .models import Suspect, Crime
from .forms import SearchForm

from django.shortcuts import render
from django.db.models import Q
from .models import Suspect, Crime
from .forms import SearchForm

def search_suspects(request):
    """
    دالة البحث عن المتهمين بناءً على اسم المتهم، رقم البلاغ، أو نوع الجريمة.
    """
    # استخراج معايير البحث من طلب GET
    form = SearchForm(request.GET or None)
    crimes_details = []

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        report_number = form.cleaned_data.get('report_number', '').strip()
        crime_type = form.cleaned_data.get('crime_type', '').strip()

        # إنشاء استعلام فارغ
        search_query = Q()

        # إضافة شروط البحث بناءً على المدخلات
        if query:
            search_query &= Q(full_name__icontains=query) | Q(nickname__icontains=query)

        if report_number:
            search_query &= Q(crimes__report_number__icontains=report_number)

        if crime_type:
            search_query &= Q(crimes__type__icontains=crime_type)

        # تنفيذ الاستعلام للحصول على النتائج
        suspects = Suspect.objects.filter(search_query).distinct()

        # إنشاء هيكل بيانات يحتوي على المتهمين والجرائم المرتبطة بهم
        for suspect in suspects:
            crimes = suspect.crimes.all()
            crimes_details.append({
                'suspect': suspect,
                'crimes': [
                    {
                        'report_number': crime.report_number,
                        'crime_type': crime.crime_type,
                        'crime_date': crime.crime_date,
                        'description': crime.description,
                    }
                    for crime in crimes
                ]
            })

    # تمرير النتائج إلى القالب
    return render(request, 'search_suspects.html', {
        'form': form,
        'crimes_details': crimes_details,
    })