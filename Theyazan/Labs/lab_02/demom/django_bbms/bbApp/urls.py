from django.contrib import admin
from django.urls import path
from bbApp import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('userlogin', views.login_user, name="login-user"),
    path('profile', views.profile, name="profile-page"),
    path('update_profile', views.update_profile, name="update-profile"),
    path('update_password', views.update_password, name="update-password"),
    path('', views.home,name="home-page"),
    path('blood_group_mgt', views.blood_group_mgt,name="blood_group-page"),
    path('manage_blood_group', views.manage_blood_group,name="manage-blood_group"),
    path('manage_blood_group/<int:pk>', views.manage_blood_group,name="manage-blood_group-pk"),
    path('save_blood_group', views.save_blood_group,name="save-blood_group"),
    path('delete_blood_group', views.delete_blood_group,name="delete-blood_group"),
    path('donation_mgt', views.donation_mgt,name="donation-page"),
    path('manage_donation', views.manage_donation,name="manage-donation"),
    path('manage_donation/<int:pk>', views.manage_donation,name="manage-donation-pk"),
    path('view_donation/<int:pk>', views.view_donation,name="view-donation-pk"),
    path('save_donation', views.save_donation,name="save-donation"),
    path('delete_donation', views.delete_donation,name="delete-donation"),
    path('brequest', views.brequest_mgt,name="request-page"),
    path('manage_brequest', views.manage_brequest,name="manage-request"),
    path('manage_brequest/<int:pk>', views.manage_brequest,name="manage-request-pk"),
    path('view_brequest/<int:pk>', views.view_brequest,name="view-request-pk"),
    path('save_brequest', views.save_brequest,name="save-request"),
    path('delete_brequest', views.delete_brequest,name="delete-request"),
    path('get_bg_availability', views.get_bg_availability,name="get-bg-available"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)