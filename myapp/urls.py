"""Intrusion_Detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login/', views.login_get),
    path('login_posts/',views.login_post),
    path('viewuser/', views.viewuser),
    path('admin_add_expert/', views.admin_add_expert),
    path('admin_add_expert_post/',views.admin_add_expert_post),
    path('admin_view_expert/', views.admin_view_expert),
    path('admin_App_Review/', views.admin_App_Review),
    path('admin_App_Review_post/', views.admin_App_Review_post),
    path('admin_changepassword/', views.admin_changepassword),
    path('admin_changepassword_post/',views.admin_changepassword_post),
    path('delete_expert/<eid>', views.delete_expert),
    path('admin_Edit_expert/<eid>', views.admin_Edit_expert),
    path('admin_Edit_expert_post/',views.admin_Edit_expert_post),
    path('admin_send_reply/<id>', views.admin_send_reply),
    path('admin_send_reply_post/',views.admin_send_reply_post),
    path('admin_view_complaint/', views.admin_view_complaint),
    path('admin_adminhome/', views.admin_adminhome),


    ############# EXPERT ###############
    path('expert_add_video/', views.expert_add_video),
    path('expert_add_video_post/', views.expert_add_video_post),
    path('expert_changepassword/', views.expert_changepassword),
    path('expert_changepassword_post/', views.expert_changepassword_post),
    path('expert_View_Profile/', views.expert_View_Profile),
    path('expert_view_video/', views.expert_view_video),
    path('expert_edit_video/<id>', views.expert_edit_video),
    path('expert_edit_video_post/', views.expert_edit_video_post),
    path('expert_App_Review/', views.expert_App_Review),
    path('delete_Video/<eid>', views.delete_Video),
    path('user_view_video/', views.user_view_video),
    path('view_log/', views.view_log),
    path('viewNotification/', views.viewNotification),
    path('viewuserexpert/', views.viewuserexpert),
    path('forgotpassword_get/', views.forgot_password, name='forgot_password'),


    path('chat1/<id>', views.chat1),
    path('chat_view/', views.chat_view),
    path('chat_send/<msg>', views.chat_send),

    path('expert_home/', views.experthome),
    path('log_out/', views.log_out),


    ################## USER ##################
    path('user_login_post/', views.user_login_post),
    path('user_signup/', views.user_signup),
    path('user_profile/', views.user_profile),
    path('view_profile/', views.view_profile),
    path('edit_profile/', views.edit_profile),
    path('change_password/', views.change_password),
    path('view_expert/', views.view_expert),
    path('view_uploaded_content/', views.view_uploaded_content),
    path('chat_with_expert/', views.chat_with_expert),
    path('send_app_complaint/', views.send_app_complaint),
    path('view_reply/', views.view_reply),
    path('send_app_review/', views.send_app_review),
    # path('forget_password/', views.forget_password),
    path('android_forget_password_post/', views.android_forget_password_post),
    path('admin_view_logs/<id>', views.admin_view_logs),
    path('User_sendchat/', views.User_sendchat),
    path('user_viewchat/', views.user_viewchat),
    path('change_user_password/', views.change_user_password),



]
