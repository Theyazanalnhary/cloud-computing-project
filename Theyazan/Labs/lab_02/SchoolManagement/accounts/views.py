from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Account
from students.models import Student

def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

def account_edit(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    students = Student.objects.all()
    if request.method == 'POST':
        account.student = get_object_or_404(Student, id=request.POST.get('student'))
        account.amount_due = request.POST.get('amount_due')
        account.save()
        return redirect('account_list')
    return render(request, 'accounts/account_edit.html', {'account': account, 'students': students})

def account_delete(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == 'POST':
        account.delete()
        return redirect('account_list')
    return render(request, 'accounts/account_delete.html', {'account': account})
