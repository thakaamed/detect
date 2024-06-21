import os.path
import traceback
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from User.models import *
from datetime import datetime, timedelta, date
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.translation import gettext as _
import uuid
from Server.settings import ccreport_url, ccclinic_path_with_slash, ccclinic_path, \
    image_path_without_slash_after_media, lateral_cephalometric_dict, clinic_project_id
import time
from django.contrib import messages
from collections import defaultdict
from django.forms.models import model_to_dict
from Application.views import get_specs

# Create your views here.
def first_page(request):
    specs = get_specs()
    if clinic_project_id != 2:
        return HttpResponseRedirect(reverse('patientsPage'))
    return render(request,'first_page.html', context = {"specs": specs})


def signup_page(request):
    specs = get_specs()
    print("request.user", request.user, type(request.user))
    if clinic_project_id != 2:
        return HttpResponseRedirect(reverse('patientsPage'))
    if not str(request.user) == "AnonymousUser":
        return HttpResponseRedirect(reverse('patientsPage'))
    packages = Package.objects.all()
    time.sleep(0.5) #dil değiştirme isteği tamamlanmadan dicti çektiği için değişen dili değil eski dili getiriyor
    context = {
        'packages':packages,
        "specs": specs,
    }
    print(context)
    return render(request,'sign-up.html',context)