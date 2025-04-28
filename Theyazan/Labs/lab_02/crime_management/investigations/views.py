from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Investigation,Crime
from .forms import InvestigationForm

def investigation_list(request):
    query = request.GET.get('q', '')
    investigations = Investigation.objects.filter(investigation_id__icontains=query) if query else Investigation.objects.all()
    
    # التحقق من البيانات المُسترجعة
    print(investigations)  # طباعة البيانات للتأكد
    for investigation in investigations:
        print(investigation.investigation_id)  # التحقق من كل كائن

    return render(request, 'investigation_list.html', {'investigations': investigations, 'query': query})


from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvestigationForm
from crimes.models import Crime

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvestigationForm
from crimes.models import Crime

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvestigationForm
from crimes.models import Crime
from suspects.models import Suspect

from django.shortcuts import render, get_object_or_404, redirect
from .models import Investigation, Crime, Suspect
from .forms import InvestigationForm
from django.urls import reverse
from django.urls import reverse

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Investigation, Crime, Suspect
from .forms import InvestigationForm

def add_investigation(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    
    # التعديل هنا لاستخدام العلاقة الجديدة ManyToMany
    suspects = Suspect.objects.filter(crimes=crime).select_related().values('suspect_id', 'full_name', 'release_date', 'is_fugitive')
    suspects_list = list(suspects)

    if request.method == "POST":
        form = InvestigationForm(request.POST, crime_id=crime_id)
        if form.is_valid():
            suspect = form.cleaned_data['suspect']
            
            # التحقق من وجود إجراء تحري سابق
            existing_investigation = Investigation.objects.filter(
                crime=crime, 
                suspect=suspect
            ).first()
            
            if existing_investigation:
                messages.error(
                    request,
                    f"إجراء التحري للمتهم ({suspect.full_name}) في هذه الجريمة موجود بالفعل."
                )
                return redirect('add_investigation', crime_id=crime_id)
            
            investigation = form.save(commit=False)
            investigation.crime = crime
            investigation.suspect = suspect
            
            # تحديث حالة التحقيق تلقائياً من حالة المتهم
            investigation.status = 'هارب' if suspect.is_fugitive else 'مقبوض'
            
            investigation.save()
            messages.success(request, "تم إضافة إجراء التحقيق بنجاح.")
            return redirect('add_prosecution', crime_id=crime_id)
    else:
        form = InvestigationForm(crime_id=crime_id)

    context = {
        'form': form,
        'crime': crime,
        'suspects_list': suspects_list,
    }
    return render(request, 'add_investigation.html', context)

def court_actions(request, pk):
    investigation = get_object_or_404(
        Investigation.objects.select_related('crime', 'suspect'), 
        pk=pk
    )
    
    # يمكنك إضافة المزيد من السياق إذا لزم الأمر
    context = {
        'investigation': investigation,
        'crime': investigation.crime,
        'suspect': investigation.suspect,
    }
    
    return render(request, 'add_prosecution.html', context)

def edit_investigation(request, investigation_id):
    investigation = get_object_or_404(Investigation, pk=investigation_id)
    if request.method == 'POST':
        form = InvestigationForm(request.POST, instance=investigation)
        if form.is_valid():
            form.save()
            return redirect('investigation_list')
    else:
        form = InvestigationForm(instance=investigation)
    return render(request, 'edit_investigation.html', {'form': form, 'investigation': investigation})

def delete_investigation(request, investigation_id):
    investigation = get_object_or_404(Investigation, pk=investigation_id)
    if request.method == 'POST':
        investigation.delete()
        messages.success(request, 'تم حذف التحقيق بنجاح.')
        return redirect('investigation_list')
    return render(request, 'delete_investigation.html', {'investigation': investigation})