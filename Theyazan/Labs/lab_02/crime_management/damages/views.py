from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Damage
from .forms import DamageForm
from django.shortcuts import render, get_object_or_404, redirect
from crimes.models import Crime


from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render
from .forms import DamageForm
from .models import Crime
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DamageForm
from .models import Crime




from django.core.exceptions import ValidationError

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from .models import Damage, Crime
from .forms import DamageForm

def add_damage(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    
    if request.method == 'POST':
        form = DamageForm(request.POST, request.FILES, crime_id=crime_id)
        
        if form.is_valid():
            try:
                damage = form.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'تم إضافة الضرر بنجاح',
                        'redirect_url': reverse('add_investigation', kwargs={'crime_id': crime.id})
                    })
                messages.success(request, 'تم إضافة الضرر بنجاح')
                return redirect('add_investigation', crime_id=crime.id)
                    
            except (ValidationError, IntegrityError) as e:
                error_msg = str(e)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg,
                        'is_duplicate': 'مسجلة مسبقاً' in error_msg
                    }, status=400)
                messages.error(request, error_msg)
        
        # معالجة أخطاء الفورم
        errors = '\n'.join([error for errors in form.errors.values() for error in errors])
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': errors,
                'is_duplicate': False
            }, status=400)
        
        for error in form.errors.values():
            messages.error(request, error[0])

    form = DamageForm(crime_id=crime_id)
    context = {
        'form': form,
        'crime': crime,
        'messages_json': [{'text': str(msg), 'tags': msg.tags} for msg in messages.get_messages(request)]
    }
    return render(request, 'add_damage.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Damage
from .forms import DamageForm

def edit_damage(request, damage_id):
    damage = get_object_or_404(Damage, pk=damage_id)

    if request.method == 'POST':
        form = DamageForm(request.POST, instance=damage)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الضرر بنجاح.')
            return redirect('damage_list')
        else:
            messages.error(request, 'حدث خطأ أثناء تعديل الضرر. يرجى التحقق من البيانات.')
    else:
        form = DamageForm(instance=damage)

    return render(request, 'edit_damage.html', {'form': form, 'damage': damage})


def delete_damage(request, damage_id):
    damage = get_object_or_404(Damage, pk=damage_id)
    if request.method == 'POST':
        damage.delete()
        messages.success(request, 'تم حذف الضرر بنجاح.')
        return redirect('damage_list')
    return render(request, 'delete_damage.html', {'damage': damage})


def damage_list(request):
    query = request.GET.get('q', '')
    damages = Damage.objects.filter(damage_id__icontains=query) if query else Damage.objects.all()
    


    return render(request, 'damage_list.html', {'damages': damages, 'query': query})