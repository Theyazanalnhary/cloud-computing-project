
from django.shortcuts import render, get_object_or_404
from crimes.models import Crime
from victims.models import Victim
from suspects.models import Suspect
from damages.models import Damage
from investigations.models import Investigation
from prosecutions.models import Prosecution

def crime_full_report(request, crime_id):
    # الحصول على الجريمة الأساسية
    crime = get_object_or_404(Crime, pk=crime_id)
    
    # الحصول على جميع البيانات المرتبطة
    victims = Victim.objects.filter(crime=crime)
    suspects = Suspect.objects.filter(crime=crime)
    damages = Damage.objects.filter(crime=crime)
    investigations = Investigation.objects.filter(crime=crime)
    prosecutions = Prosecution.objects.filter(crime=crime)
    
    context = {
        'crime': crime,
        'victims': victims,
        'suspects': suspects,
        'damages': damages,
        'investigations': investigations,
        'prosecutions': prosecutions,
    }
    
    return render(request, 'full_report.html', context)
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Crime
from .forms import CrimeForm  # استمارة الإدخال
# عرض قائمة الجرائم مع البحث
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# التحقق من الدور
@login_required
def crime_list(request):
    query = request.GET.get('q', '')
    if query:
        crimes = Crime.objects.filter(report_number__icontains=query)  # البحث برقم البلاغ
    else:
        crimes = Crime.objects.all()
    return render(request, 'crime_list.html', {'crimes': crimes, 'query': query})

# عرض تفاصيل جريمة واحدة
def crime_detail(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    return render(request, 'crime_detail.html', {'crime': crime})

from django.shortcuts import render, redirect
from .models import Crime
from .forms import CrimeForm

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CrimeForm

def crime_create(request):
    if request.method == "POST":
        form = CrimeForm(request.POST)
        if form.is_valid():
            # حفظ الجريمة والحصول على الكائن المحفوظ
            crime = form.save()

            # إضافة رسالة تأكيد باستخدام messages framework
            messages.success(request, 'تم حفظ البلاغ بنجاح!')

            # إعادة التوجيه إلى صفحة إضافة المجني عليه مع تمرير ID الجريمة
            return redirect('add_victim_for_crime', crime_id=crime.id)
        else:
            # إضافة رسالة خطأ إذا كانت البيانات غير صالحة
            messages.error(request, 'حدث خطأ أثناء حفظ البلاغ. يرجى تصحيح الأخطاء.')
    else:
        form = CrimeForm()

    # تمرير الرسائل إلى القالب
    return render(request, 'crime_form.html', {'form': form})

# تعديل جريمة
def crime_update(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    if request.method == "POST":
        form = CrimeForm(request.POST, instance=crime)
        if form.is_valid():
            form.save()
            return redirect('crime_list')
    else:
        form = CrimeForm(instance=crime)
    return render(request, 'crime_form.html', {'form': form})

# حذف جريمة
def crime_delete(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    if request.method == "POST":
        crime.delete()
        return redirect('crime_list')
    return render(request, 'crime_confirm_delete.html', {'crime': crime})
