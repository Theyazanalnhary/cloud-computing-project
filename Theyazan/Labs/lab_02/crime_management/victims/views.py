from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Victim
from .forms import VictimForm

from django.shortcuts import render
from .models import Victim, Crime

def victim_list(request):
    # الحصول على كلمة البحث من طلب GET
    query = request.GET.get('q', '').strip()  # إزالة الفراغات الزائدة
    
    # استعلام البيانات بناءً على البحث
    if query:
        victims = Victim.objects.filter(full_name__icontains=query).order_by('full_name')
    else:
        victims = Victim.objects.all().order_by('full_name')  # ترتيب حسب الاسم
    
    # التحقق من البيانات المُسترجعة (للأغراض التصحيحية)
    print(f"Query: {query}")
    print("Victims retrieved:", victims)
    for victim in victims:
        print(f"ID: {victim.victim_id}, Full Name: {victim.full_name}, Crime ID: {victim.crime.id}")

    # استعلام جميع الجرائم مع عدد المجني عليهم
    crimes = Crime.objects.all().prefetch_related('victims').order_by('id')

    context = {
        'victims': victims,
        'crimes': crimes,
        'query': query,
    }

    return render(request, 'victim_list.html', context)

def victim_list_for_crime(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    victims = Victim.objects.filter(crime=crime)  # قائمة المجني عليهم لهذه الجريمة
    return render(request, 'victim_list_for_crime.html', {'crime': crime, 'victims': victims})

from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from .models import Victim
from .forms import VictimForm
from crimes.models import Crime
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.core.exceptions import ValidationError

def add_victim_for_crime(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    
    if request.method == "POST":
        form = VictimForm(request.POST, crime_id=crime_id)
        if form.is_valid():
            try:
                victim = form.save(commit=False)
                
                # التحقق من التكرار قبل الحفظ
                full_name = form.cleaned_data.get('full_name')
                age = form.cleaned_data.get('age')
                phone = form.cleaned_data.get('phone')
                
                # 1. التحقق من التكرار في نفس الجريمة
                if Victim.objects.filter(
                    crimes__id=crime_id,
                    full_name=full_name,
                    age=age,
                    phone=phone
                ).exists():
                    error_msg = "المجني عليه مسجل بالفعل في هذه الجريمة!"
                    return JsonResponse({
                        'success': False,
                        'message': error_msg,
                        'is_duplicate': True
                    }, status=400)
                
                # 2. التحقق من التكرار في جرائم أخرى
                existing_victim = Victim.objects.filter(
                    full_name=full_name,
                    age=age,
                    phone=phone
                ).first()
                
                if existing_victim:
                    # ربط المجني عليه الموجود بالجريمة الحالية
                    existing_victim.crimes.add(crime)
                    success_msg = (
                        f"تم ربط المجني عليه '{full_name}' بالجريمة الحالية حيث كان مسجلًا سابقًا "
                        f"برقم سجل: {existing_victim.victim_id}"
                    )
                    return JsonResponse({
                        'success': True,
                        'message': success_msg,
                        'is_linked': True,
                        'victim_id': existing_victim.victim_id,
                        'redirect_url': reverse('suspects:add_suspect', kwargs={'crime_id': crime.id})
                    })
                
                # إذا لم يكن هناك تكرار، احفظ المجني عليه الجديد
                victim.save()
                crime.victims.add(victim)
                
                success_msg = "تم إضافة المجني عليه بنجاح"
                return JsonResponse({
                    'success': True,
                    'message': success_msg,
                    'redirect_url': reverse('suspects:add_suspect', kwargs={'crime_id': crime.id})
                })
                    
            except Exception as e:
                error_msg = f"حدث خطأ غير متوقع: {str(e)}"
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                }, status=500)
        else:
            # معالجة أخطاء النموذج
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            
            return JsonResponse({
                'success': False,
                'message': 'يوجد أخطاء في البيانات المدخلة',
                'errors': errors
            }, status=400)

    # تحضير الرسائل للقالب
    messages_list = []
    for message in messages.get_messages(request):
        messages_list.append({
            'tags': message.tags,
            'text': str(message.message)
        })
    messages_json = json.dumps(messages_list, cls=DjangoJSONEncoder) if messages_list else '[]'

    return render(request, 'add_victim.html', {
        'form': VictimForm(crime_id=crime_id),
        'crime': crime,
        'messages_json': messages_json,

    })

# views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Victim
from .forms import VictimForm
from crimes.models import Crime
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.urls import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from .forms import VictimForm
from .models import Victim, Crime
import json

def add_victim_for_crime(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    
    if request.method == "POST":
        form = VictimForm(request.POST, crime_id=crime_id)
        if form.is_valid():
            try:
                victim = form.save(commit=False)
                victim.save()
                crime.victims.add(victim)
                messages.success(request, "تم إضافة المجني عليه بنجاح")
                return redirect('suspects:add_suspect', crime_id=crime.id)
            except ValidationError as e:
                for error in e.message_dict.get('non_field_errors', []):
                    messages.error(request, error)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = VictimForm(crime_id=crime_id)

    # تحضير الرسائل للقالب
    messages_list = []
    for message in messages.get_messages(request):
        messages_list.append({
            'tags': message.tags,
            'text': str(message.message)
        })

    return render(request, 'add_victim.html', {
        'form': form,
        'crime': crime,
        'messages_json': json.dumps(messages_list, cls=DjangoJSONEncoder)
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Victim
from .forms import VictimForm

def edit_victim(request, victim_id):
    victim = get_object_or_404(Victim, pk=victim_id)
    
    if request.method == 'POST':
        form = VictimForm(request.POST, instance=victim)
        if form.is_valid():
            updated_victim = form.save()
            messages.success(request, f'تم تحديث بيانات المجني عليه {updated_victim.full_name} بنجاح')
            return redirect('victim_list')
        else:
            messages.error(request, 'حدث خطأ أثناء تحديث البيانات. يرجى تصحيح الأخطاء أدناه.')
    else:
        form = VictimForm(instance=victim)
    
    context = {
        'form': form,
        'victim': victim,
    }
    
    return render(request, 'edit_victim.html', context)

def delete_victim(request, victim_id):
    victim = get_object_or_404(Victim, pk=victim_id)
    if request.method == 'POST':
        victim.delete()
        messages.success(request, 'تم حذف المجني عليه بنجاح.')
        return redirect('victim_list')
    return render(request, 'delete_victim.html', {'victim': victim})