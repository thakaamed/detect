from django.urls import path, include
from django.contrib import admin
from AdminPanel.views import *
urlpatterns = [
    # path('', dashboard_homepage, name='homepage'),
    # path('', dashboard_user_list, name='userlist'),
    # path('user-detail/<int:id>/', dashboard_user_detail_and_statistics, name='user_detail'),
    path('active-user-count',for_admin_active_users_and_count, name="for_admin_active_users_and_count"),
    path('',dashboard_homepage, name="dashboard_homepage"),
]