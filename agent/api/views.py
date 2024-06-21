import traceback
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from django.core.cache import cache
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import uuid
import os
import requests
from Server.settings import ccreport_url, ccreport_url_tr, ccclinic_path_with_slash, ccclinic_path, image_path_without_slash_after_media, clinic_project_id
from django.shortcuts import render
from User.mail import send_feedback_email
import cv2
from Application.cache_processes import active_model_labels_function
from User.models import Profile

def get_or_create_agent_keys(request):
    try:

        user_id = request.GET.get("userId")
        print("user_id", user_id)
        profile_obj = Profile.objects.get(user__id=user_id)
        company_obj = profile_obj.company
        if not profile_obj.api_key:
            user_api_key = str(uuid.uuid4()).replace("-", "")
            profile_obj.api_key = user_api_key
            profile_obj.save()
        else:
            user_api_key = profile_obj.api_key
        if not company_obj.api_key:
            company_api_key = str(uuid.uuid4()).replace("-", "")
            company_obj.api_key = company_api_key
            company_obj.save()
        else:
            company_api_key = company_obj.api_key
        keys = {
            "user_api_key": user_api_key,
            "company_api_key": company_api_key
        }
        return JsonResponse({"status": True, "keys": keys})
    except:
        return JsonResponse({"status": False})
