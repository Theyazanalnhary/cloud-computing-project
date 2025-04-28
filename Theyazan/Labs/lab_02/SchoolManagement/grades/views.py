from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Grade
from students.models import Student
from teachers.models import Teacher

def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'grades/grade_list.html', {'grades': grades})

def grade_edit(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        grade.student = get_object_or_404(Student, id=request.POST.get('student'))
        grade.teacher = get_object_or_404(Teacher, id=request.POST.get('teacher'))
        grade.course_name = request.POST.get('course_name')
        grade.grade = request.POST.get('grade')
        grade.save()
        return redirect('grade_list')
    return render(request, 'grades/grade_edit.html', {'grade': grade, 'students': students, 'teachers': teachers})

def grade_delete(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        grade.delete()
        return redirect('grade_list')
    return render(request, 'grades/grade_delete.html', {'grade': grade})
