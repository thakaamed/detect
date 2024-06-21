from django.urls import path, include
from django.contrib import admin
from agent.views import *

urlpatterns = [
    path('analyze', analyze.as_view(), name='analyze'),
    path('check_user', check_user, name='check_user'),
]

