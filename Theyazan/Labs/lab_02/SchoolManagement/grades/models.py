from django.db import models

# Create your models here.
from django.db import models
from students.models import Student
from teachers.models import Teacher

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=2)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.course_name}: {self.grade}"
