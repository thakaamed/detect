from AdminPanel.api.views import *
from django.urls import path
urlpatterns = [
    path("update-user-infos", dashboard_update_user_infos, name="dashboard_update_user_infos"),
]