from django.shortcuts import render
from .models import Login
# Create your views here.


def index(request):
    x={'name':'ahmes'
    ,'age':1234444574674}
    return render(request,'pages/index.html',x)

def about(request):
    username = request.POST.get('username')
    password= request.POST.get('password')
    data = Login(username=username,password=password)
    data.save()
   
    return render(request,'pages/about.html')