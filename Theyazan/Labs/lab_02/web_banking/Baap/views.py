from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from Baap import forms, models

context={
    'page':'',
    'page_title':'',
    'system_name':'',
    'has_navigation':True,
    'has_sidebar':True,
}
# Create your views here.
@login_required
def home(request):
    context['page'] = 'home'
    context['page_title'] = ' '
    context['blood_groups'] = models.Blood_Group.objects.filter(status =1).all()
    return render(request,'home.html',context)

#تسجيل دخول
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#تسجيل الخروج
def logoutuser(request):
    logout(request)
    return redirect('/')


@login_required
def update_profile(request):
    context['page_title'] = 'تعديل الملف الشخصي'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الملف الشخصي بنجاح")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    context['page_title'] = "تعديل كلمة المرور"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"تم تعديل كلمة المرور بنجاح")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

#فصائل الدم
@login_required
def blood_group_mgt(request):
    context['page'] = 'blood_group_mgt'
    context['page_title'] = 'ادارة فصائل الدم'
    blood_groups = models.Blood_Group.objects.all()
    context['blood_groups'] = blood_groups
    return render(request,'blood_group_mgt.html',context)


@login_required
def manage_blood_group(request, pk = None):
    if not pk is None:
        blood_group = models.Blood_Group.objects.get(id = pk)
        context['blood_group'] = blood_group
    else:
        context['blood_group'] = {}
    return render(request, 'manage_blood_group.html', context)

@login_required
def save_blood_group(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveBloodGroup(post)
        else:
            blood_group = models.Blood_Group.objects.get(id = post['id'])
            form = forms.SaveBloodGroup(post, instance=blood_group)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            messages.success(request, "تم اضافة فصيلة الدم بنجاح")
        else:
            resp['msg'] = 'Blood Group Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str("<br/>"+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_blood_group(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Blood_Group.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "تم حذف فصيلة الدم بنجاح")
        except:
            resp['msg'] = 'Blood Group Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")



#المتبرع
@login_required
def donation_mgt(request):
    context['page'] = 'donation_mgt'
    context['page_title'] = ' '
    donations = models.Donation.objects.all()
    context['donations'] = donations
    return render(request,'donation_mgt.html',context)


@login_required
def manage_donation(request, pk = None):
    blood_groups = models.Blood_Group.objects.filter(status = 1).all()
    context['blood_groups'] = blood_groups
    if not pk is None:
        donation = models.Donation.objects.get(id = pk)
        context['donation'] = donation
    else:
        context['donation'] = {}
    return render(request, 'manage_donation.html', context)

@login_required
def view_donation(request, pk = None):
    blood_groups = models.Blood_Group.objects.filter(status = 1).all()
    context['blood_groups'] = blood_groups
    if not pk is None:
        donation = models.Donation.objects.get(id = pk)
        context['donation'] = donation
    else:
        context['donation'] = {}
    return render(request, 'view_donation.html', context)

@login_required
def save_donation(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveDonation(post)
        else:
            donation = models.Donation.objects.get(id = post['id'])
            form = forms.SaveDonation(post, instance=donation)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            messages.success(request, "Donation Detail has been saved successfully.")
        else:
            resp['msg'] = 'Donation Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(f"<br/> [{field.name}] "+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_donation(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Donation.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "تم الحذف بنجاح")
        except:
            resp['msg'] = 'Donation Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")



#طلب دم
@login_required
def brequest_mgt(request):
    context['page'] = 'request_mgt'
    context['page_title'] = ' '
    brequests = models.Request.objects.all()
    context['brequests'] = brequests
    return render(request,'request_mgt.html',context)


@login_required
def manage_brequest(request, pk = None):
    blood_groups = models.Blood_Group.objects.filter(status = 1).all()
    context['blood_groups'] = blood_groups
    if not pk is None:
        brequest = models.Request.objects.get(id = pk)
        context['brequest'] = brequest
    else:
        context['brequest'] = {}
    return render(request, 'manage_request.html', context)

@login_required
def view_brequest(request, pk = None):
    blood_groups = models.Blood_Group.objects.filter(status = 1).all()
    context['blood_groups'] = blood_groups
    if not pk is None:
        brequest = models.Request.objects.get(id = pk)
        context['brequest'] = brequest
    else:
        context['brequest'] = {}
    return render(request, 'view_request.html', context)

@login_required
def save_brequest(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveRequest(post)
        else:
            brequest = models.Request.objects.get(id = post['id'])
            form = forms.SaveRequest(post, instance=brequest)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            messages.success(request, "Request Detail has been saved successfully.")
        else:
            resp['msg'] = 'Request Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(f"<br/> [{field.name}] "+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_brequest(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Request.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "تم الحذف بنجاح")
        except:
            resp['msg'] = 'Request Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def get_bg_availability(request):
    resp = { 'status':'failed', 'msg' : '', 'volume':0 }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            req = models.Blood_Group.objects.get(id = post['id'])
            resp['status'] = 'success'
            if req.get_total_volume() is None:
                available = 0
            else:
                available = req.get_total_volume()
            resp['volume'] = available
        except Exception as err:
            print(err)
            resp['msg'] = 'Unable to fetch the available volume of the Blood Group.'

    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def profile(request):
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)
