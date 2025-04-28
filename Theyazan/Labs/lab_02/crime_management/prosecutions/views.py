from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Prosecution
from .forms import ProsecutionForm

def prosecution_list(request):
    query = request.GET.get('q', '')
    prosecutions = Prosecution.objects.filter(case_number__icontains=query) if query else Prosecution.objects.all()
    
    # التحقق من البيانات المُسترجعة
    print(prosecutions)  # طباعة البيانات للتأكد
    for prosecution in prosecutions:
        print(prosecution.prosecution_id, prosecution.case_number)  # التحقق من كل كائن

    return render(request, 'prosecution_list.html', {'prosecutions': prosecutions, 'query': query})

    
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProsecutionForm
from crimes.models import Crime
from investigations.models import Investigation

from django.shortcuts import render, redirect, get_object_or_404
from .models import Crime, Prosecution
from .forms import ProsecutionForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Crime, Prosecution
from .forms import ProsecutionForm
import json

def add_prosecution(request, crime_id):
    crime = get_object_or_404(Crime, id=crime_id)
    
    if request.method == "POST":
        form = ProsecutionForm(request.POST, crime_id=crime_id)
        
        if form.is_valid():
            try:
                prosecution = form.save(commit=False)
                prosecution.crime = crime
                prosecution.save()
                
                messages.success(request, _("تم إضافة إجراء النيابة بنجاح"))
                return redirect('crime_detail', pk=crime_id)
                
            except Exception as e:
                messages.error(request, _("حدث خطأ أثناء حفظ البيانات: {}").format(str(e)))
        else:
            # تحويل أخطاء النموذج إلى رسائل
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = ProsecutionForm(crime_id=crime_id)
    
    # تحضير الرسائل للعرض في SweetAlert2
    messages_json = []
    for message in messages.get_messages(request):
        messages_json.append({
            'text': str(message),
            'tags': message.tags
        })
    
    context = {
        'form': form,
        'crime': crime,
        'messages_json': json.dumps(messages_json),
        'page_title': _("إضافة إجراء نيابة"),
    }
    
    return render(request, 'add_prosecution.html', context)

from django.contrib import messages

def edit_prosecution(request, prosecution_id):
    prosecution = get_object_or_404(Prosecution, pk=prosecution_id)

    if request.method == 'POST':
        form = ProsecutionForm(request.POST, instance=prosecution)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الإجراء بنجاح.')
            return redirect('prosecution_list')
        else:
            messages.error(request, 'حدث خطأ أثناء تعديل الإجراء. يرجى التحقق من البيانات.')
    else:
        form = ProsecutionForm(instance=prosecution)

    return render(request, 'edit_prosecution.html', {'form': form, 'prosecution': prosecution})


def delete_prosecution(request, prosecution_id):
    prosecution = get_object_or_404(Prosecution, pk=prosecution_id)
    if request.method == 'POST':
        prosecution.delete()
        return redirect('prosecution_list')
    return render(request, 'delete_prosecution.html', {'prosecution': prosecution})