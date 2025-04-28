from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'Teachers/teacher_list.html', {'teachers': teachers})

def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.first_name = request.POST['first_name']
        teacher.last_name = request.POST['last_name']
        teacher.email = request.POST['email']
        teacher.save()
        return redirect('teacher_list')
    return render(request, 'Teachers/teacher_edit.html', {'teacher': teacher})

def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'teachers/teacher_delete.html', {'teacher': teacher})
