import traceback
from Application.models import *
from Application3d.models import DicomReport
from User.models import *
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.db.models import Q
import json
from django.contrib.auth import update_session_auth_hash
from Application.functions import send_email,send_email_to_management, draw_function, cephalometric_analyses, error_handler_function,draw_implant_and_crown
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import uuid
import os
from Application.api.analyze import start_manuel_analyze
import requests
from Server.settings import ccreport_url, ccreport_url_tr, ccclinic_path_with_slash, ccclinic_path, image_path_without_slash_after_media, clinic_project_id
from django.shortcuts import render
from User.mail import send_feedback_email
from rest_framework.views import APIView
from .serializer import PatientSerializer
from rest_framework.response import Response
import cv2
from PIL import Image as pil_Image, ImageChops
from Application.cache_processes import active_model_labels_function, fetch_data_from_AI_labels
from User.token_operationsv2 import remaining_token as cranio_remaining_token
import secrets
import string
import logging
import traceback
import qrcode
from io import BytesIO
from django.core.files import File
import re
from django.db import transaction

logger = logging.getLogger('main')

@login_required
def add_patient_api(request):
    try:
        user = request.user
        patient_slug = request.POST.get('patientSlug', None)
        birthday = request.POST.get('dateofbirth')
        if patient_slug:
            patient = Patient.objects.get(slug=patient_slug)
        else:
            patient = Patient()
        if request.method == 'POST':
            full_name = request.POST.get('patientfullname')
            full_name_l = full_name.split(" ")
            last_name = full_name_l[-1]
            full_name_l.pop(-1)
            first_name = " ".join(full_name_l)
            patient.first_name = first_name
            patient.last_name = last_name
            patient.full_name = full_name
            profile = Profile.objects.get(user=user)
            patient.user = profile
            if birthday:
                patient.date_of_birth = birthday
            else:
                patient.date_of_birth = None
            user = request.user
            profile = Profile.objects.get(user=user)
            patient.gender = request.POST.get('gender')
            patient.file_no = request.POST.get('fileno')
            patient.email = request.POST.get('email')
            patient.phone = request.POST.get('patientphone')
            radiography_obj = request.POST.get('radiography_obj', None)
            radiography_type = request.POST.get('radiography_type', None)
            if radiography_obj:
                radiography = FormRadiographs.objects.get(id=int(radiography_obj))
            if radiography_type:
                radiography_type_obj = ImageType.objects.get(id=int(radiography_type))
            patient.save()
            if radiography_type and radiography_obj:
                image_object = Image.objects.create(path=radiography.path, patient=patient, type=radiography_type_obj, user=profile)
                manuel_analyze_return_dict = start_manuel_analyze(profile.user, image_object.id, image_object.path.url)
            return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
@login_required
def delete_patient_api(request):
    try:
        patientSlug = request.POST.get('patientSlug')
        patient = Patient.objects.get(slug=patientSlug)
        patient.archived = True
        patient.save()
        return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
@login_required
def change_favorite_status(request):
    try:
        patient_slug = request.POST.get("patient_slug")
        patient_obj = Patient.objects.get(slug=patient_slug)
        patient_obj.favorited = not patient_obj.favorited
        # not mantıksal operatörü, boolean ifadenin değerini tersine çevirir. Yani, True ise False yapar ve False ise True yapar.
        patient_obj.save()
        span_value = 1 if patient_obj.favorited else 0
        return JsonResponse(
            {'status': True, 'span_value': span_value, 'message': f"Patient favorite status: {patient_obj.favorited}."})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
@login_required
def update_page_length(request):
    try:
        user = request.user
        if request.method == "POST":
            page_length = request.POST.get("page_length")
            if page_length == "-1":
                page_length = "Hepsi"
            user_theme_obj = UserTheme.objects.get(user=user)
            user_theme_obj.page_length = page_length
            user_theme_obj.save()
            return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
@login_required
def change_card_view(request):
    try:
        user = request.user
        card_view = request.POST.get("card_view")
        user_theme_obj = UserTheme.objects.get(user=user)
        user_theme_obj.card_view_type = str(card_view)
        user_theme_obj.save()
        return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@csrf_exempt
@login_required
def change_theme_view(request):
    try:
        user = request.user
        theme = request.POST.get("theme")
        user_theme_obj = UserTheme.objects.get(user=user)
        user_theme_obj.color = theme
        user_theme_obj.save()
        return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def change_tooth_approved_status(request):
    try:
        tooth_number = int(request.POST.get("data_id"))
        approve_status = request.POST.get("data_approve_status")
        image_report_id = int(request.POST.get("image_report_id"))
        ReportTooth_obj = ReportTooth.objects.get(
            Q(image_report__id=image_report_id) & (Q(number_edited=tooth_number) | Q(number_prediction=tooth_number)))
        ReportTooth_obj.new_approve_status = approve_status
        ReportTooth_obj.save()
        return JsonResponse({"status": True, "new_approve_status": approve_status})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def set_timeout_image_reports(report, time):
    new_date = report.created_date
    new_date = new_date + timedelta(minutes=time)
    formatted_date = new_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    new_date = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S.%f")

    # print(new_date)  # 2023-06-19 15:00:10.679587
    # print(datetime.now())  # 2023-06-19 15:00:10.679587
    # print(type(new_date))  # <class 'datetime.datetime'>
    # print(type(datetime.now()))  # <class 'datetime.datetime'>

    # Raporun oluşturma tarihini kontrol et
    if new_date < datetime.now():
        report.is_error = True
        report.save()
        print(f"Raporun oluşturma tarihi {time} dakikayı aşmıştır.")
        return report
    return report


def get_user_info(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        if profile.profile_photo:
            profile_photo = profile.profile_photo.url
        else:
            profile_photo = "/static/img/profile_photo.jpg"

        data = []
        data.append({'full_name': user.first_name + " " + user.last_name, 'profile_photo': profile_photo})
        return JsonResponse({"data": data})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def get_notifications(request):
    try:
        lang = request.GET.get("lang")
        print("lang", lang)
        one_week_ago = datetime.now() - timedelta(weeks=2)
        image_reports = ImageReport.objects.filter(user__user=request.user, image__patient__archived=False, image__archived=False, created_date__gte=one_week_ago).order_by(
            '-created_date')[:10]
        nifti_reports = ImageReport.objects.filter(user__user=request.user, name="CBCT",created_date__gte=one_week_ago)
        dicom_reports = DicomReport.objects.filter(image_report__user__user=request.user, created_date__gte=one_week_ago)
        data = []
        # 0 başarıyla tamamlandı
        # 1 hatalı tamamlandı
        # 2 devam ediyor...
        status = "2"
        for nifti in nifti_reports:
            if not nifti.dicom: continue
            if nifti.is_done and not nifti.is_error:
                status = "fa-bolt completed-ok"
            elif nifti.is_error:
                status = "fa-bolt completed-no"
            elif not nifti.is_done and not nifti.is_error:
                nifti = set_timeout_image_reports(nifti, 15)
                status = "fa-spinner process"

            nifti_created_date = nifti.created_date + timedelta(hours=3)
            formatted_date = nifti_created_date.strftime('%d-%m-%Y %H:%M')
            url = f"/{lang}/cephalometric/{nifti.id}" if "Cephalometric" in nifti.name else f"/{lang}/diagnosis3d/{nifti.id}" if "CBCT" in nifti.name else f"/{lang}/diagnosis/{nifti.id}"
            data.append({'status': status, 'user': nifti.user.user.first_name + " " + nifti.user.user.last_name,
                'created_date': formatted_date, 'name': nifti.name, 'id': nifti.id,
                'patient': nifti.dicom.patient.first_name + " " + nifti.dicom.patient.last_name,
                'url': url, 'd': '2'})

        for report in image_reports:
            if report.is_done and not report.is_error:
                status = "fa-bolt completed-ok"
            elif report.is_error:
                status = "fa-bolt completed-no"
            elif not report.is_done and not report.is_error:
                report = set_timeout_image_reports(report, 15)
                status = "fa-spinner process"

            report_created_date = report.created_date + timedelta(hours=3)
            formatted_date = report_created_date.strftime('%d-%m-%Y %H:%M')

            url = f"/{lang}/cephalometric/{report.id}" if "Cephalometric" in report.name else f"/{lang}/diagnosis3d/{report.id}" if "CBCT" in report.name else f"/{lang}/diagnosis/{report.id}"
            data.append({'status': status, 'user': report.user.user.first_name + " " + report.user.user.last_name,
                'created_date': formatted_date, 'name': report.name, 'id': report.id,
                'patient': report.image.patient.first_name + " " + report.image.patient.last_name,
                'url': url, 'd': '2'})

        status = "2"
        for report in dicom_reports:
            if report.is_done and not report.is_error:
                status = "fa-bolt completed-ok"
            elif report.is_error:
                status = "fa-bolt completed-no"
            elif not report.is_done and not report.is_error:
                report = set_timeout_image_reports(report, 15)
                status = "fa-spinner process"
            else:
                pass

            report_created_date = report.created_date + timedelta(hours=3)
            formatted_date = report_created_date.strftime('%d-%m-%Y %H:%M')
            url = f"/{lang}{report.report_type.url}{report.id}"
            data.append({'status': status, 'user': report.image_report.user.user.first_name + " " + report.image_report.user.user.last_name,
                'created_date': formatted_date, 'name': report.report_type.name, 'id': report.id,
                'patient': report.image_report.dicom.patient.first_name + " " + report.image_report.dicom.patient.last_name,
                'url': url, 'd': '3'})

        sorted_data = sorted(data, key=lambda x: datetime.strptime(x['created_date'], '%d-%m-%Y %H:%M'), reverse=True)
        return JsonResponse({"data": sorted_data})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def process_status_for_notification(request):
    try:
        process_ir_id_list = request.GET.get("process_ir_id_list")
        process_ir_id_list = json.loads(process_ir_id_list)
        process_dr_id_list = request.GET.get("process_dr_id_list")
        process_dr_id_list = json.loads(process_dr_id_list)
        lang = request.GET.get("lang")
        print("lang", lang)
        image_reports = ImageReport.objects.filter(id__in=process_ir_id_list, image__archived=False)
        nifti_reports = ImageReport.objects.filter(id__in=process_ir_id_list, name="CBCT")
        dicom_reports = DicomReport.objects.filter(id__in=process_dr_id_list)
        status = "2"
        data = []

        for nifti in nifti_reports:
            if not nifti.dicom: continue
            if nifti.is_done and not nifti.is_error:
                status = "fa-bolt completed-ok"
            elif nifti.is_error:
                status = "fa-bolt completed-no"
            elif not nifti.is_done and not nifti.is_error:
                nifti = set_timeout_image_reports(nifti, 15)
                status = "fa-spinner process"
            print("lang", lang)
            nifti_created_date = nifti.created_date + timedelta(hours=3)
            formatted_date = nifti_created_date.strftime('%d-%m-%Y %H:%M')

            url = f"/{lang}/cephalometric/{nifti.id}" if "Cephalometric" in nifti.name else f"/{lang}/diagnosis3d/{nifti.id}" if "CBCT" in nifti.name else f"/{lang}/diagnosis/{nifti.id}"
            data.append({'status': status, 'user': nifti.user.user.first_name + " " + nifti.user.user.last_name,
                'created_date': formatted_date, 'name': nifti.name, 'id': nifti.id,
                'patient': nifti.dicom.patient.first_name + " " + nifti.dicom.patient.last_name,
                'url': url, 'd': '2'})
        
        for report in image_reports:
            if report.is_done and not report.is_error:
                status = "fa-bolt completed-ok"
            elif report.is_error:
                status = "fa-bolt completed-no"
            elif not report.is_done and not report.is_error:
                report = set_timeout_image_reports(report, 15)
                status = "fa-spinner process"
            print("lang", lang)
            report_created_date = report.created_date + timedelta(hours=3)
            formatted_date = report_created_date.strftime('%d-%m-%Y %H:%M')

            url = f"/{lang}/cephalometric/{report.id}" if "Cephalometric" in report.name else f"/{lang}/diagnosis3d/{report.id}" if "CBCT" in report.name else f"/{lang}/diagnosis/{report.id}"
            data.append({'status': status, 'user': report.user.user.first_name + " " + report.user.user.last_name,
                'created_date': formatted_date, 'name': report.name, 'id': report.id,
                'patient': report.image.patient.first_name + " " + report.image.patient.last_name,
                'url': url, 'd': '2'})
        
        status = "2"
        for report in dicom_reports:
            if report.is_done and not report.is_error:
                status = "fa-bolt completed-ok"
            elif report.is_error:
                status = "fa-bolt completed-no"
            elif not report.is_done and not report.is_error:
                report = set_timeout_image_reports(report, 15)
                status = "fa-spinner process"

            report_created_date = report.created_date + timedelta(hours=3)
            formatted_date = report_created_date.strftime('%d-%m-%Y %H:%M')

            url = f"/{lang}{report.report_type.url}{report.id}"
            data.append({'status': status, 'user': report.image_report.user.user.first_name + " " + report.image_report.user.user.last_name,
                'created_date': formatted_date, 'name': report.report_type.name, 'id': report.id,
                'patient': report.image_report.image.patient.first_name + " " + report.image_report.image.patient.last_name,
                'url': url, 'd': '3'})

        sorted_data = sorted(data, key=lambda x: datetime.strptime(x['created_date'], '%d-%m-%Y %H:%M'), reverse=True)

        return JsonResponse({"data": sorted_data})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def remove_phone_mask(phone):
    return ''.join(filter(str.isdigit, phone))


@login_required
def update_profile(request):
    try:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        json_data = json.loads(request.body)

        if 'name' and 'surname' in json_data:
            name = json_data['name']
            surname = json_data['surname']
            user.first_name = name
            user.last_name = surname
        if 'phone' in json_data:
            phone = json_data['phone']
            clean_phone = remove_phone_mask(phone)
            profile.phone = clean_phone
        if 'email' in json_data:
            email = json_data['email']
            user.email = email
        if 'clinicname' in json_data:
            clinic_name = json_data['clinicname']
            profile.clinic_name = clinic_name
            print(clinic_name)
        user.save()
        profile.save()
        return JsonResponse({'success': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def update_password(request):
    try:
        user = request.user
        json_data = json.loads(request.body)

        # Şu anki şifre doğrulaması
        old_password = json_data.get('oldpasswordinput')
        if not user.check_password(old_password):
            return JsonResponse({'success': False, 'code': "Invalid password"})

        # Yeni şifre kontrolü
        new_password = json_data.get('newpasswordinput1')
        confirm_password = json_data.get('newpasswordinput2')
        if new_password != confirm_password:
            return JsonResponse({'success': False, 'code': "passwords not match"})

        # Şifre güncelleme
        user.set_password(new_password)
        user.save()

        # Oturum kimliği güncelleme
        update_session_auth_hash(request, user)
        message = _("Your password updated")

        return JsonResponse({'success': True, 'message': message})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def change_language(request):
    try:
        language = request.GET.get('language', 'en')
        print("language",language)
        user = request.user
        theme = UserTheme.objects.get(user=user)
        theme.language = language
        theme.save()
        return JsonResponse({"status": True, "language": theme.language})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def save_profile_photo(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            profile_photo = request.FILES['image']
            profile = Profile.objects.get(user=request.user)
            profile.profile_photo = profile_photo
            profile.save()
            return JsonResponse({'success': True, 'image': profile.profile_photo.url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def save_signature(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            signature = request.FILES['image']
            print("signature", signature)
            profile = Profile.objects.get(user=request.user)
            profile.signature = signature
            profile.save()
            return JsonResponse({'success': True, 'image': profile.signature.url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def save_clinic_logo(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            clinic_logo = request.FILES['image']

            print("clinic_logo", clinic_logo)
            profile = Profile.objects.get(user=request.user)
            company = profile.company
            company.logo = clinic_logo
            company.save()
            return JsonResponse({'success': True, 'image': profile.company.logo.url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def save_tooth_note(request):
    try:
        tooth_number = request.POST.get("tooth_number")
        image_report_id = request.POST.get("image_report_id")
        tooth_note = request.POST.get("tooth_note")
        report_tooth_obj = ReportTooth.objects.get(
            Q(image_report__id=image_report_id) & (Q(number_edited=tooth_number) | Q(number_prediction=tooth_number)))
        report_tooth_obj.note = tooth_note
        report_tooth_obj.save()
        return JsonResponse({"status": True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def api_update_report_tooth(request):
    try:
        image_report_id = int(request.POST.get("image_report_id"))
        image_report = ImageReport.objects.filter(cbct=False, id=image_report_id, image__archived=False).first()
        icon_type = request.POST.get('icon_type')
        number_prediction = int(request.POST.get("number_prediction"))
        report_tooth_obj = ReportTooth.objects.filter(image_report__id=image_report_id,
                                                    number_edited=number_prediction).first() or ReportTooth.objects.filter(
            image_report__id=image_report_id, number_prediction=number_prediction).first()
        if not report_tooth_obj:
            report_tooth_obj = ReportTooth.objects.create(image_report=image_report, number_edited=number_prediction,
                                                        number_prediction=number_prediction)
        icon = ToothTypeIcon.objects.filter(tooth_number=number_prediction, name=icon_type).first()
        if icon:
            report_tooth_obj.icon_type = icon
        else:
            report_tooth_obj.icon_type = None
        report_tooth_obj.save()
        return JsonResponse({'success': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def illness_draw(request):
    try:
        lang = request.GET.get("lang")
        selected_items = request.GET.getlist('selected_items[]')  # Ajax isteğinden seçilen öğeleri çek
        # print("selected", selected_items)
        filter_by_proba_dict = {"weak": {"lower": 0, "upper": 33}, "medium": {"lower": 33, "upper": 66},
            "strong": {"lower": 66, "upper": 99}, "dentist": {"lower": 99, "upper": 102}}

        image_report_id = request.GET.get('image_report_id')
        illness_list = request.GET.get('illness_list')
        first_draw = request.GET.get('first_draw')
        restorations_list = []
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        image_type = image_report_obj.image.type.name

        draw_all = True if first_draw == "True" else False
        illness_list = illness_list.split(",") if illness_list else []
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
        active_model_labels_dict = active_model_labels_function()[image_type][patient_type]
        def normal_draw(image_report_obj, illness_list, draw_all, first_draw, image_report_id, filter_by_proba_dict, selected_items):
            # Dişleri ve üzerindeki hastalıkları radyografi üzerinde balon şeklinde göstermek için dict hazırlama
            report_tooth_obj = ReportTooth.objects.filter(image_report=image_report_obj).order_by('number_prediction')
            tooth_illness_coords = []
            measurement_list = []
            for report_tooth in report_tooth_obj:
                report_tooth_predict_obj = report_tooth.reporttoothpredict_set.all()

                illness_list_report_tooth = []
                for report_tooth_predict in report_tooth_predict_obj:
                    prediction = report_tooth_predict.correction if report_tooth_predict.correction else report_tooth_predict.prediction
                    prediction = json.loads(prediction.replace("'", '"'))
                    if prediction["name"] == "Root-Canal Filling":
                        continue
                    prediction["approve_status"] = report_tooth_predict.new_approve
                    illness_list_report_tooth.append(prediction)
                if not report_tooth.coordinates:
                    continue 
                tooth_coordinates = json.loads(report_tooth.coordinates.replace("'", '"'))
                xmin = tooth_coordinates["xmin"]
                ymin = tooth_coordinates["ymin"]
                xmax = tooth_coordinates["xmax"]
                ymax = tooth_coordinates["ymax"]
                tooth_coordinate_array_original = [[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]

                tooth_cards_dict = {"tooth_number": report_tooth.number_prediction,
                                    "illness": illness_list_report_tooth,
                                    "coordinates": tooth_coordinate_array_original,
                                    # "coordinates_original": tooth_coordinate_array_original,
                                    "probability": tooth_coordinates["proba"]}
                tooth_illness_coords.append(tooth_cards_dict)

            if not image_report_obj.result_json:
                return JsonResponse({"status": "continues", "image_id": image_report_id})
            ai_get_response_json = json.loads(image_report_obj.result_json)
            palate_results = ai_get_response_json["palate_results"]
            illness_pool = ai_get_response_json["illness_pool"]
            measurement_results = ai_get_response_json[
                "measurement_results"] if "measurement_results" in ai_get_response_json.keys() else {}

            if selected_items:
                new_palate_results = []
                new_illness_pool = []
                for i in palate_results:
                    for j in selected_items:
                        if filter_by_proba_dict[j]["lower"] < int(i["probability"]) <= filter_by_proba_dict[j]["upper"]:
                            new_palate_results.append(i)
                palate_results = new_palate_results

                for i in illness_pool:
                    for j in selected_items:
                        if filter_by_proba_dict[j]["lower"] < int(i["probability"]) <= filter_by_proba_dict[j]["upper"]:
                            new_illness_pool.append(i)
                illness_pool = new_illness_pool

            image_type = image_report_obj.image.type.name
            image_type_id = image_report_obj.image.type.id

            if illness_list or not draw_all:
                palate_results_list = [item for item in palate_results if item.get("name") in illness_list]
                illness_pool_list = [item for item in illness_pool if item.get("name") in illness_list]
                measurement_results_list = [item for item in measurement_results if item.get("name") in illness_list]
            else:
                palate_results_list = [item for item in palate_results]
                illness_pool_list = [item for item in illness_pool]
                measurement_results_list = [item for item in measurement_results]
            illness_coords_colors = []

            for illness in illness_pool_list:
                illness_name = illness['name']
                illness_slug = illness['slug']
                illness_get = active_model_labels_dict.get(illness_name)
                if illness_name == "Root-Canal Filling": 
                    continue
                if not illness_get: continue
                illness_coords_colors.append(
                    {"name": illness_name, "color": illness_get["color"], "proba": illness['probability'],
                     "coords": illness["coordinates"], "slug": illness_slug, "approve_status": "disabled",
                     "data-pointer": "false"})

            for illness in palate_results_list:
                illness_name = illness['name']
                illness_slug = illness['slug']
                illness_get = active_model_labels_dict.get(illness_name, None)
                if not illness_get: continue
                if illness_name == "Pontic" or illness_name == "Dental Implant":
                    illness_coords_colors.append(
                    {"name": illness_name, "color": illness_get["color"], "proba": illness['probability'],
                     "coords": illness["coordinates"], "slug": illness_slug, "approve_status": "disabled",
                     "data-pointer": "false"})
                else:
                    illness_coords_colors.append(
                        {"name": illness_name, "color": illness_get["color"], "proba": illness['probability'],
                         "coords": illness["coordinates"], "slug": illness_slug,
                         "approve_status": illness['approve_status'], "data-pointer": "true"})

            # BİTEWİNG MEASURE FOR ALVEOLAR BONE LOSS
            if image_report_obj.name == "Bitewing" and "measurement_results" in ai_get_response_json.keys():
                measurement_results = measurement_results_list
                for measurement in measurement_results:
                    illness = measurement["name"]
                    values = measurement["points"]
                    aml = active_model_labels_dict.get(illness, None)
                    if not aml: continue
                    for tooth_number, points in values.items():
                        for point, p_m in points.items():
                            coordinates = p_m["points"]
                            measurement_dict = {
                                "coordinates": coordinates,
                                "label": illness,
                                "label_tr_name": aml["tr_name"],
                                "marking_type": "point",
                                "label_id": aml["id"],
                                "color": aml["color"],
                                "measure": p_m["measure"],
                                "position": point,
                                "tooth_number": tooth_number
                            }
                            measurement_list.append(measurement_dict)
            
            return illness_coords_colors, tooth_illness_coords, image_type_id, measurement_list,

        def lateral_draw(image_report_obj):
            dict_for_lateral_draw = {}
            image_type = image_report_obj.image.type.name
            active_model_labels_dict = active_model_labels_function()[image_type][patient_type]
            result_json = image_report_obj.result_json
            result_json = json.loads(result_json)
            dict_for_lateral_draw["calibration_points"] = result_json["calibration_points"]
            dict_for_lateral_draw["results"] = {"cephalometric_landmarks": []}
            for point in result_json["results"]["cephalometric_landmarks"]:
                print("point", point)
                label = active_model_labels_dict.get(point["label"], None)
                if not label: continue
                print("label", label)
                dict_for_lateral_draw["results"]["cephalometric_landmarks"].append(
                    {"coordinates": point["coordinates"], "label": point["label"],
                        "marking_type": point["marking_type"], "label_tr_name": label["tr_name"],
                        "label_id": label["id"], })

            result_json["results"].pop("cephalometric_landmarks")
            for key, value in result_json["results"].items():
                dict_for_lateral_draw["results"][key] = value

            return dict_for_lateral_draw
        

        def restorations(image_report_obj):
            restorations = DrawedImplantOrCrown.objects.filter(image_report=image_report_obj)
            for restoration in restorations:
                restorations_list.append({
                    "slug": restoration.slug,
                    "item_type": restoration.item_type,
                    "icon_id": restoration.icon_id,
                    "coordinate": restoration.coordinate,
                    "dimension": restoration.dimension,
                    "rotate": restoration.rotate,
                    "original_shape": restoration.original_shape
                })
            return restorations_list
        if "Cephalometric" in image_report_obj.name:
            dict_for_lateral_draw = lateral_draw(image_report_obj)
            image_type_id = image_report_obj.image.type.id
            return JsonResponse({"status": True, "results": dict_for_lateral_draw, "image_type_id": image_type_id})
        else:
            illness_coords_colors, tooth_illness_coords, image_type_id, measurement_list = normal_draw(
                image_report_obj, illness_list, draw_all, first_draw, image_report_id, filter_by_proba_dict,
                selected_items)
            restorations_list = restorations(image_report_obj)
            return JsonResponse({"status": True, "illness_coords_colors": illness_coords_colors,
                                 "tooth_illness_coords": tooth_illness_coords, "image_type_id": image_type_id,
                                 "measurement_results": measurement_list, "restorations": restorations_list})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)



@login_required
def is_analyze_finished(request):
    image_report_id = request.GET.get("image_report_id")

    try:
        image_report = ImageReport.objects.get(cbct=False, id=image_report_id)
        is_done = image_report.is_done
        is_error = image_report.is_error
        if is_done:
            return JsonResponse({'status': True, 'success': True})
        elif is_error:
            return JsonResponse({'status': True, 'success': False})
        return JsonResponse({'status': is_done})

    except ImageReport.DoesNotExist:
        return JsonResponse({'status': False})
    

@login_required
def add_diagnosis(request):
    try:
        selected_illnesses = request.POST.getlist('selectedIllnesses[]')
        image_report_id = request.POST.get("image_report_id")
        image_type = request.POST.get('image_type')
        image_report_obj = ImageReport.objects.get(id=image_report_id)
        patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
        illnesses = active_model_labels_function()[image_type][patient_type]
        tooth_number = request.POST.get("tooth_number")
        report_tooth_obj = ReportTooth.objects.get(image_report__id=image_report_id, number_prediction=tooth_number)
        selected_illnesses_keys = []

        for illness_id in selected_illnesses:
            for key, value in illnesses.items():
                if value.get('id') == int(illness_id):
                    disease_infos = {"en_name": key, "tr_name": value["tr_name"]}
                    selected_illnesses_keys.append(disease_infos)
                    break
        ##
        existing_illnesses = ReportToothPredict.objects.filter(Q(report_tooth=report_tooth_obj))

        for existing_illness in existing_illnesses:
            prediction_dict = json.loads(existing_illness.prediction.replace("'", "\"")) if isinstance(
                existing_illness.prediction, str) else existing_illness.prediction
            if any(selected_illness['en_name'] == prediction_dict.get('name') for selected_illness in
                selected_illnesses_keys):
                # Hastalık mevcut, hata mesajı verilebilir
                error_message = _("The disease you are trying to add already exists")
                return JsonResponse({'error': error_message})

        ##
        for selected_illness in selected_illnesses_keys:
            uid = uuid.uuid4()
            slug = uid.hex
            illness_dict = {'name': selected_illness["en_name"], 'xmin': 0, 'ymin': 0, 'xmax': 0, 'ymax': 0,
                            'probability': 101, 'slug': slug}
            ReportToothPredict.objects.create(prediction=illness_dict, report_tooth=report_tooth_obj,)
        report_tooth_predict_obj = ReportToothPredict.objects.filter(report_tooth=report_tooth_obj).last()
        prediction = json.loads(report_tooth_predict_obj.prediction.replace("'", '"'))

        data = {'selected_illnesses': selected_illnesses_keys, 'tooth_number': tooth_number, "report_tooth_obj_id":report_tooth_obj.id,"slug":prediction["slug"]}
        return JsonResponse(data)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def add_treatment(request):
    try:
        selected_treatments = request.POST.getlist('selectedTreatments[]')
        tooth_number = request.POST.get("tooth_number")
        image_report_id = request.POST.get("image_report_id")
        report_tooth_obj = ReportTooth.objects.get(image_report__id=image_report_id, number_prediction=tooth_number)
        image_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        slug=None
        recommendations = []
        for slug in selected_treatments:
            existing_recommendation = TreatmentRecommendationForTooth.objects.filter(recommendation__slug=slug,
                                                                                    tooth=report_tooth_obj).exists()
            if existing_recommendation:
                return JsonResponse({"success": False, "error": "already exists"})
            else:
                treatment_recommendation = TreatmentMethod.objects.get(slug=slug)
                slug = treatment_recommendation.slug
                recommendation_obj = TreatmentRecommendationForTooth.objects.create(tooth=report_tooth_obj,
                    image_report=image_obj)
                recommendation_obj.recommendation.set([treatment_recommendation])
                recommendation_data = {"en_name": treatment_recommendation.en_treatment_method,"tr_name":treatment_recommendation.tr_treatment_method, "slug": treatment_recommendation.slug}
                recommendations.append(recommendation_data)
        return JsonResponse({"success": True, "tooth_number":tooth_number,"tooth_id":report_tooth_obj.id,"recommendations": recommendations})

    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
@csrf_exempt
def add_treatment_planning(request):
    try:
        content = request.POST.get('content')
        image_report_id = request.POST.get('image_report_id')
        image_report = ImageReport.objects.get(id=image_report_id)
        treatment_id = request.POST.get('treatment_id')
        total_treatments = TreatmentPlanning.objects.filter(image_report=image_report)
        counter_for_treatment = total_treatments.count() + 1
        if treatment_id != "null" and treatment_id != None and treatment_id != "None":
            # Var olan objeyi güncelle
            treatment_planning = TreatmentPlanning.objects.get(id=treatment_id)
            treatment_planning.updated_planning = content
            treatment_planning.modified_date = datetime.now()
            treatment_planning.save()
            modified_date = treatment_planning.modified_date.strftime("%d.%m.%Y %H:%M")
            return JsonResponse({"status": "updated-treatment", "treatment_id": treatment_planning.id,
                                "counter": int(counter_for_treatment), "modified_date": modified_date})

        else:
            # Yeni bir obje oluştur
            treatment_planning = TreatmentPlanning.objects.create(image_report=image_report, updated_planning=content)
            modified_date = treatment_planning.modified_date.strftime("%d.%m.%Y %H:%M")
            return JsonResponse(
                {"status": "new-treatment", "treatment_id": treatment_planning.id, "counter": int(counter_for_treatment),
                "modified_date": modified_date})
        return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def get_content_of_treatment_planning(request):
    try:
        id = request.GET.get("id")

        treatment = TreatmentPlanning.objects.get(id=id)
        if treatment.ai_planning:
            return JsonResponse({'success': True, 'content': treatment.ai_planning})
        else:
            return JsonResponse({'success': True, 'content': treatment.updated_planning})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def trim(im):
    bg = pil_Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def convert_tiff_to_png(tiff_path, png_path):
    try:
        tiff_image = pil_Image.open(tiff_path)
        tiff_image.save(png_path, format='PNG')
        return True
    except Exception as e:
        print("Hata:", str(e))
        return False


@csrf_exempt
@login_required
def upload_radyografi(request):
    try:
        if request.method == 'POST' and request.FILES.get('file'):
            try:
                if request.user.is_anonymous:
                    print("anonymous user çünkü yeni yapılan form kurgusundan geldi istek")
                    user_id = request.POST.get("doctor_id")
                    user = User.objects.get(id=user_id)
                else:
                    user = request.user
                    
                file = request.FILES['file']
                if file.content_type == 'image/tiff':
                    # TIFF dosyasını geçici bir yere kaydet
                    tiff_slug = str(uuid.uuid4())
                    tiff_path = f'{ccclinic_path_with_slash}media/temporary_tiff/{tiff_slug}.tiff'
                    with open(tiff_path, 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)
                    
                    # PNG dosyasını geçici olarak kaydet
                    png_path = f'{ccclinic_path_with_slash}media/dental/radio/{tiff_slug}.png'
                    if convert_tiff_to_png(tiff_path, png_path):
                        # Dönüşüm başarılıysa TemporaryUploadedFile oluştur
                        radiography_type = request.POST.get('radiography_type')
                        image_report_id = request.POST.get('image_report_id')
                        patient_slug = request.POST.get('patient_slug')
                        if not radiography_type:
                            return JsonResponse({'success': False, 'message': 'Radyografi Türünü Seçiniz!'})
                        image_type_obj = ImageType.objects.get(id=int(radiography_type))
                        if patient_slug:
                            patient_obj = Patient.objects.get(slug=patient_slug)
                        else:
                            image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
                            patient_obj = image_report_obj.image.patient

                        profile = Profile.objects.get(user=user)
                        image_object = Image.objects.create(path=png_path.replace(ccclinic_path_with_slash, ""), patient=patient_obj, type=image_type_obj, user=profile)

                        os.remove(tiff_path)
                        # TemporaryUploadedFile'ı uploaded_file ile değiştir
                        
                        # Daha sonra buradan devam edebilirsiniz...
                else:
                    original_file_name, file_extension = os.path.splitext(file.name)
                    new_file_name = str(uuid.uuid4()) + file_extension
                    file.name = new_file_name
                    radiography_type = request.POST.get('radiography_type')
                    image_report_id = request.POST.get('image_report_id')
                    patient_slug = request.POST.get('patient_slug')
                    if not radiography_type:
                        return JsonResponse({'success': False, 'message': 'Radyografi Türünü Seçiniz!'})
                    image_type_obj = ImageType.objects.get(id=int(radiography_type))
                    if patient_slug:
                        patient_obj = Patient.objects.get(slug=patient_slug)
                    else:
                        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
                        patient_obj = image_report_obj.image.patient

                    profile = Profile.objects.get(user=user)
                    image_object = Image.objects.create(path=file, patient=patient_obj, type=image_type_obj, user=profile)

                img_path = image_object.path.path
                name, extension = os.path.splitext(img_path)
                new_img_path = name + ".jpg"

                thumbnail_image_path = new_img_path.replace('.', '_thumbnail.')
                thumbnail_image_path = thumbnail_image_path.replace(ccclinic_path + "/", "")
                cv2.imwrite(thumbnail_image_path, cv2.resize(cv2.imread(image_object.path.path), (250, 109)))
                image_object.thumbnail_image_path = thumbnail_image_path.replace("/mnt/nfs_ai_v2/", "")
                image_object.save()
                manuel_analyze_return_dict = start_manuel_analyze(user, image_object, image_object.path.url)
                # Burada radyografi dosyasını işleyebilirsiniz
                # Dosyayı kaydedebilir, işleyebilir veya başka işlemler yapabilirsiniz
                return JsonResponse(
                    {'success': True, 'message': 'Radiography Uploaded.', 'analyze_status': manuel_analyze_return_dict})
            except Exception as e:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)
        return JsonResponse({'success': False, 'message': 'Radyografi yüklenirken bir hata oluştu.'})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
@login_required
def convert_tiff_to_png_js(request):
    file = request.FILES['file']
    if file.content_type == 'image/tiff':
        # TIFF dosyasını geçici bir yere kaydet
        tiff_slug = str(uuid.uuid4())
        tiff_path = f'{ccclinic_path_with_slash}media/temporary_tiff/{tiff_slug}.tiff'
        with open(tiff_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        
        # PNG dosyasını geçici olarak kaydet
        png_path = f'{ccclinic_path_with_slash}media/dental/radio/{tiff_slug}.png'
        if convert_tiff_to_png(tiff_path, png_path):
            return JsonResponse({"path": png_path.replace("/home/akilliceviribilisim/Clinic", "")})


@login_required
def delete_treatment_plan(request):
    try:
        id = request.POST.get("treatmentId")
        treatment_obj = TreatmentPlanning.objects.get(id=id)

        treatment_obj.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def change_approve_status(request):
    if request.method == 'GET':
        try:
            tooth_number = int(request.GET.get('tooth_number')) if request.GET.get('tooth_number') else None
            approve_status = request.GET.get('approve_status')
            illness_slug = request.GET.get('illness_slug')
            image_report_id = request.GET.get('image_report_id')
            image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
            changed_status = False
            delete_status = False
            result_json = json.loads(image_report_obj.result_json)

            if tooth_number:
                report_tooth_obj = ReportTooth.objects.get(number_prediction=tooth_number, image_report=image_report_obj)
                report_tooth_predict_obj = report_tooth_obj.reporttoothpredict_set.all()

                for report_tooth_predict in report_tooth_predict_obj:
                    prediction = report_tooth_predict.correction if report_tooth_predict.correction else report_tooth_predict.prediction
                    prediction = json.loads(prediction.replace("'", '"'))
                    if prediction["slug"] == illness_slug:
                        if int(approve_status) == 3: #delete
                            report_tooth_predict.delete()
                            delete_status = True
                            for i, item in enumerate(result_json["palate_results"]):
                                if item["slug"] == illness_slug:
                                    if int(approve_status) == 3: #delete
                                        result_json["palate_results"].pop(i)
                                        delete_status = True
                                        break  # Döngüyü sonlandırabilirsiniz, çünkü elemanı bulduğunuzda işlemi zaten yapmışsınız.
                                    else:
                                        item["approve_status"] = int(approve_status)
                                        changed_status = True
                                        result_json["palate_results"][i] = item
                                    break
                            for i, item in enumerate(result_json["illness_pool"]):
                                if item["slug"] == illness_slug:
                                    if int(approve_status) == 3: #delete
                                        result_json["illness_pool"].pop(i)
                                        delete_status = True
                                    else:
                                        item["approve_status"] = int(approve_status)
                                        changed_status = True
                                        result_json["illness_pool"][i] = item
                                    break
                        else:
                            report_tooth_predict.new_approve = str(approve_status)
                            report_tooth_predict.save()
                        break
                if not changed_status and not delete_status:
                    return JsonResponse({"message": "Hata!"})
                else:
                    image_report_obj.result_json = json.dumps(result_json)
                    image_report_obj.save()
                return JsonResponse({"status": True})
            else:
                for i, item in enumerate(result_json["palate_results"]):
                    if item["slug"] == illness_slug:
                        if int(approve_status) == 3: #delete
                            result_json["palate_results"].pop(i)
                            delete_status = True
                            break  # Döngüyü sonlandırabilirsiniz, çünkü elemanı bulduğunuzda işlemi zaten yapmışsınız.
                        else:
                            item["approve_status"] = int(approve_status)
                            changed_status = True
                            result_json["palate_results"][i] = item
                        break
                for i, item in enumerate(result_json["illness_pool"]):
                    if item["slug"] == illness_slug:
                        if int(approve_status) == 3: #delete
                            result_json["illness_pool"].pop(i)
                            delete_status = True
                        else:
                            item["approve_status"] = int(approve_status)
                            changed_status = True
                            result_json["illness_pool"][i] = item
                        break
                if not changed_status and not delete_status:
                    return JsonResponse({"message": "Hata!"})
                else:
                    image_report_obj.result_json = json.dumps(result_json)
                    image_report_obj.save()
                return JsonResponse({"status": True})
        except Exception as e:
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)

# dişteki hastalığı silme apisi
@login_required
def delete_illness_from_tooth(request):
    try:
        slug = request.POST.get("illnessSlug")
        tooth_number = request.POST.get("toothNumber")
        image_report_id = request.POST.get("imageReportID")
        tooth_id = request.POST.get("toothId")
        report_tooth_objects = ReportToothPredict.objects.filter(report_tooth__id=tooth_id,
                                                                report_tooth__image_report__id=image_report_id)
        filtered_object = report_tooth_objects.get(Q(correction__contains=slug) | Q(prediction__contains=slug))
        filtered_object.is_active = False
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        delete_status = False
        result_json = json.loads(image_report_obj.result_json)
        for i, item in enumerate(result_json["palate_results"]):
            if item["slug"] == slug:
                del result_json["palate_results"][i]
                delete_status = True
                break
        for i, item in enumerate(result_json["illness_pool"]):
            if item["slug"] == slug:
                del result_json["illness_pool"][i]
                delete_status = True
                break

        if not delete_status:
            return JsonResponse({"status": delete_status, "message": "Could not delete!"})
        else:
            image_report_obj.result_json = json.dumps(result_json)
            image_report_obj.save()
        filtered_object.save()
        return JsonResponse({'success': True})
    except Exception as e:
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)


# dişteki tedaviyi silme apisi
@login_required
def delete_treatment_from_tooth(request):
    try:
        slug = request.POST.get("treatmentSlug")
        tooth_number = request.POST.get("toothNumber")
        image_report_id = request.POST.get("imageReportID")
        tooth_id = request.POST.get("toothId")
        report_tooth_object = ReportTooth.objects.get(number_prediction=tooth_number, id=tooth_id,
                                                    image_report__id=image_report_id)
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        recommendation_obj = TreatmentRecommendationForTooth.objects.get(tooth=report_tooth_object,
                                                                        image_report=image_report_obj,
                                                                        recommendation__slug=slug)
        recommendation_obj.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def createReportForPatient(request):
    try:
        format_type = request.POST.get("formatType")
        patient_info_option = request.POST.get("hasta")

        radiography_info_option = request.POST.get("radiography")
        drawed_radiography_info_option = request.POST.get("drawed_radiography")
        draw_selected = request.POST.get("draw_selected")
        draw_all = request.POST.get("draw_all")
        draw_numbering = request.POST.get("draw_numbering")
        view_analysis = request.POST.get("view_analysis")
        bjork = request.POST.get("bjork", False)
        skeletal = request.POST.get("skeletal", False)
        withanalysis = request.POST.get("withanalysis", False)
        downsanalysis = request.POST.get("downsanalysis", False)
        selectedItems = request.POST.getlist('selected_items[]')
        doctor_notes_info_option = request.POST.get("hekim")
        qr_code = request.POST.get("qr_code")
        treatment_plannings_info_option = request.POST.get("tedavi_planlari")
        doctor_signature_info_option = request.POST.get("hekim_imzasi")
        filter_based_type = request.POST.get("filterBasedType")
        image_report_id = request.POST.get("imageReportID")
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        patient_obj = image_report_obj.image.patient
        slug = str(uuid.uuid4()).replace("-", "")
        create_report_obj = CreateReportForPatient.objects.create(format=format_type, filter_report_based=filter_based_type,
            slug=slug, image_report=image_report_obj, patient=patient_obj)
        if patient_info_option == "true":
            patient_options = CreateReportForPatientOptions.objects.filter(name="patient_infos")
            create_report_obj.options.add(*patient_options)

        # radiography_info_option varsa seçenekleri ekle
        if radiography_info_option == "true":
            radiography_options = CreateReportForPatientOptions.objects.filter(name="radiography_infos")
            create_report_obj.options.add(*radiography_options)
        
        if drawed_radiography_info_option == "true":
            drawed_radiography_options = CreateReportForPatientOptions.objects.filter(name="drawed_radiography_infos")
            create_report_obj.options.add(*drawed_radiography_options)
            if draw_all == "true" and draw_selected == "false":
                drawed_radiography_options = CreateReportForPatientOptions.objects.filter(name="draw_with_all_labels")
                create_report_obj.options.add(*drawed_radiography_options)
                path = image_report_obj.image.path
                output_path = draw_function(path=path, image_report_id=image_report_obj.id, )
                draw_implant_or_crown_objs = DrawedImplantOrCrown.objects.filter(image_report=image_report_obj)
                if draw_implant_or_crown_objs:
                    implant_crown_output_path =draw_implant_and_crown(implant_crown_draw=draw_implant_or_crown_objs,path=path, image_report_id=image_report_obj.id)
                    create_report_obj.drawed_implant_crown_image_path = implant_crown_output_path
                create_report_obj.drawed_image_path = output_path
                create_report_obj.save()
            elif draw_all == "false" and draw_selected == "true":
                drawed_radiography_options = CreateReportForPatientOptions.objects.filter(name="draw_with_selected_labels")
                create_report_obj.options.add(*drawed_radiography_options)
                path = image_report_obj.image.path
                draw_implant_or_crown_objs = DrawedImplantOrCrown.objects.filter(image_report=image_report_obj)
                if draw_implant_or_crown_objs:
                    implant_crown_output_path =draw_implant_and_crown(draw_implant_or_crown_objs)
                    create_report_obj.drawed_implant_crown_image_path = implant_crown_output_path
                output_path = draw_function(path=path, image_report_id=image_report_obj.id, selected_labels=selectedItems, implant_crown_draw=draw_implant_or_crown_objs)
                create_report_obj.drawed_image_path = output_path
                create_report_obj.save()

            if draw_numbering == "true":
                draw_numbering = CreateReportForPatientOptions.objects.filter(name="draw_numbering")
                create_report_obj.options.add(*draw_numbering)
                path = image_report_obj.image.path
                output_path = draw_function(path=path, image_report_id=image_report_obj.id, selected_labels=selectedItems, teethNumbering=True,)
                create_report_obj.drawed_image_path = output_path
                create_report_obj.save()

        if view_analysis == "true":
            lateral_withanalysis_analysis = CreateReportForPatientOptions.objects.filter(
                name="lateral_withanalysis_analysis")
            create_report_obj.options.add(*lateral_withanalysis_analysis)
            if bjork == "true":
                lateral_bjork_analysis = CreateReportForPatientOptions.objects.filter(name="Bjork-Jarabak Analysis")
                create_report_obj.options.add(*lateral_bjork_analysis)
            if skeletal == "true":
                lateral_skeletal_analysis = CreateReportForPatientOptions.objects.filter(
                    name="Skeletal Factors - Anterior/Posterior")
                create_report_obj.options.add(*lateral_skeletal_analysis)
            if withanalysis == "true":
                lateral_view_analysis_infos = CreateReportForPatientOptions.objects.filter(name="Wits Analysis")
                create_report_obj.options.add(*lateral_view_analysis_infos)
            if downsanalysis == "true":
                lateral_view_analysis_infos = CreateReportForPatientOptions.objects.filter(name="Downs Analysis")
                create_report_obj.options.add(*lateral_view_analysis_infos)

        # doctor_notes_info_option varsa seçenekleri ekle
        if doctor_notes_info_option == "true":
            doctor_notes_options = CreateReportForPatientOptions.objects.filter(name="doctor_note_infos")
            create_report_obj.options.add(*doctor_notes_options)

        if treatment_plannings_info_option == "true":
            treatment_planning_options = CreateReportForPatientOptions.objects.filter(name="treatment_plans")
            create_report_obj.options.add(*treatment_planning_options)

        if doctor_signature_info_option == "true":
            signature_options = CreateReportForPatientOptions.objects.filter(name="signature")
            create_report_obj.options.add(*signature_options)

        def generate_qr_code(create_report_obj):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            redirected_url = ccreport_url + create_report_obj.slug+"/"
            qr.add_data(redirected_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            filename = f'qr_code-{create_report_obj.slug}.png'
            filebuffer = File(buffer, filename)
            create_report_obj.qr_code.save(filename, filebuffer)
            buffer.close()
        if qr_code == "true":
            generate_qr_code(create_report_obj)

        return JsonResponse({"success": True, "slug": slug})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def save_doctor_note(request):
    try:
        doctor_note = request.POST.get("doctor_note")
        image_report_id = request.POST.get("image_report_id")
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        image_report_obj.note = doctor_note
        image_report_obj.save()
        return JsonResponse({'success': True, 'note': doctor_note})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def sendReportMail(request):
    try:
        name = request.POST.get("nameForSendMail")
        email = request.POST.get("emailForSendMail")
        slug = request.POST.get("slug")
        lang = request.POST.get("lang")
        image_report_id = request.POST.get("image_report_id")
        send_qr = request.POST.get("qr_code")
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        sender_doctor = image_report_obj.user
        receiver = image_report_obj.image.patient
        # report_mail_obj = ReportMails.objects.create(sender=sender_doctor, receiver=receiver, report_slug=slug,
        #     sending_date=datetime.now())
        spec = SpecificParameter.objects.get(id=clinic_project_id)
        created_report = CreateReportForPatient.objects.get(slug=slug)
        qr_path = created_report.qr_code.path if created_report.qr_code else None
        subject = f"{spec.page_title} Report"
        body = f"Hello {name}, you can follow the link to see report: {ccreport_url}{slug}"

        send_email(email, subject, body, qr_path if send_qr == "true" else None)

        return JsonResponse({"success": True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def get_current_lang(request):
    try:
        user = request.user
        lang = request.GET.get("language")
        theme = UserTheme.objects.get(user=user)
        theme.language = lang
        theme.save()
        language = theme.language
        return JsonResponse({"status": True, "language": language})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def save_doctor_choices(request):
    try:
        data = json.loads(request.body)
        image_report_id = data["image_report_id"]
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        profile = image_report_obj.user
        format = data["formatType"]
        patient_infos = data["hasta"]
        undrawed_radiography = data["radiography"]
        drawed_radiography = data["drawed_radiography"]
        doctor_note = data["hekim_notu"]
        doctor_signature = data["hekim_imzasi"]
        treatment_plannings = data["tedavi_planlari"]
        draw_selected = data["draw_selected"]
        draw_all = data["draw_all"]
        draw_numbering = data["draw_numbering"]

        view_analysis = data["view_analysis"] if "view_analysis" in data.keys() else None
        bjork = data["bjork"] if "bjork" in data.keys() else None
        skeletal = data["skeletal"] if "skeletal" in data.keys() else None
        withanalysis = data["withanalysis"] if "withanalysis" in data.keys() else None
        downs_analysis = data["downsanalysis"] if "downsanalysis" in data.keys() else None


        filter_type = data["filterBasedType"]
        doctor_choices, created = DoctorChoicesForReport.objects.get_or_create(profile=profile)
        doctor_choices.choices.clear()  # update olabilmesi için önceki seçimleri kaldırıyorum
        if patient_infos:
            patient_option = CreateReportForPatientOptions.objects.get(name="patient_infos")
            doctor_choices.choices.add(patient_option)

        if undrawed_radiography:
            undrawed_radiography_option = CreateReportForPatientOptions.objects.get(name="radiography_infos")
            doctor_choices.choices.add(undrawed_radiography_option)

        if drawed_radiography:
            drawed_radiography_option = CreateReportForPatientOptions.objects.get(name="drawed_radiography_infos")
            doctor_choices.choices.add(drawed_radiography_option)

        if draw_selected:
            draw_selected_option = CreateReportForPatientOptions.objects.get(name="draw_with_selected_labels")
            doctor_choices.choices.add(draw_selected_option)

        if draw_all:
            draw_all_option = CreateReportForPatientOptions.objects.get(name="draw_with_all_labels")
            doctor_choices.choices.add(draw_all_option)

        if draw_numbering:
            print("draw numberin")
            draw_numbering = CreateReportForPatientOptions.objects.get(name="draw_numbering")
            doctor_choices.choices.add(draw_numbering)
            print("eklendi")

        if view_analysis:
            draw_all_option = CreateReportForPatientOptions.objects.get(name="lateral_view_analysis_infos")
            doctor_choices.choices.add(draw_all_option)

        if bjork:
            draw_all_option = CreateReportForPatientOptions.objects.get(name="Bjork-Jarabak Analysis")
            doctor_choices.choices.add(draw_all_option)

        if skeletal:
            draw_all_option = CreateReportForPatientOptions.objects.get(name="Skeletal Factors - Anterior/Posterior")
            doctor_choices.choices.add(draw_all_option)

        if withanalysis:
            draw_all_option = CreateReportForPatientOptions.objects.get(name="Wits Analysis")
            doctor_choices.choices.add(draw_all_option)

        if downs_analysis:
            draw_all_option = CreateReportForPatientOptions.objects.get(name="Downs Analysis")
            doctor_choices.choices.add(draw_all_option)

        if doctor_note:
            doctor_note_option = CreateReportForPatientOptions.objects.get(name="doctor_note_infos")
            doctor_choices.choices.add(doctor_note_option)

        if doctor_signature:
            doctor_signature_option = CreateReportForPatientOptions.objects.get(name="signature")
            doctor_choices.choices.add(doctor_signature_option)

        if treatment_plannings:
            treatment_plannings_option = CreateReportForPatientOptions.objects.get(name="treatment_plans")
            doctor_choices.choices.add(treatment_plannings_option)

        if filter_type:
            doctor_choices.filter_report_based = filter_type

        if format:
            doctor_choices.format = format

        doctor_choices.save()
        return JsonResponse({'success': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


class CustomPasswordValidator:
    """
    Custom validation class.
    """

    def __init__(self, min_length=8):
        """
        Initialization method.
        """
        self.min_length = min_length
        self.errors = []  # Burada self.errors özelliğini başlatıyoruz.
        self.error_text = ""

    def validate(self, password):
        """
        Validates the password.
        """
        if password is None:
            password = ""  # nosec

        if not re.findall("[A-Z]", password):
            self.errors.append("The password must contain at least 1 uppercase letter.")

        if not re.findall("[0-9]", password):
            self.errors.append("The password must contain at least 1 digit.")

        if not re.findall('[!@#$%^&*(),.-_?":{}|<>]', password):
            self.errors.append("The password must contain at least 1 special character.")

        if len(password) < self.min_length:
            self.errors.append(f"The password must be at least {self.min_length} characters long.")
        
    def get_errors_list(self):
        return self.errors
    
    def get_error_text(self):
        if self.errors:
            for index, error in enumerate(self.errors):
                self.error_text += f"{error}" if index == 0 else f"\n{error}"
            return self.error_text
        else:
            return False



class AddPanelApi:

    @staticmethod
    def create_user(email, first_name, last_name, password):
        user = User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email, is_active=True)
        user.set_password(password)
        user.save()
        return user
    
    @staticmethod
    def create_user_theme(user):
        user_theme = UserTheme.objects.create(user=user)
        user_theme.language = "tr" if int(clinic_project_id) == 1 else "en"
        user_theme.save()
        return user_theme

    @staticmethod
    def create_buyed_package(slug="demo_token", profile_obj=None, company_obj=None):
        thakaa_package = ThakaaPackage.objects.first()
        buyed_package_obj = ThakaaBuyedPackage.objects.create(company=company_obj, thakaa_package=thakaa_package)
        buyed_package_obj.profiles.add(profile_obj)
        buyed_package_obj.save()
        thakaa_token_bar = ThakaaTokenBar.objects.get(slug=slug)
        thakaa_buyed_token = ThakaaBuyedToken.objects.create(company=company_obj, tokenbar=thakaa_token_bar)
        
        ThakaaRemainingToken.objects.create(thakaa_buyed_token=thakaa_buyed_token)
        return buyed_package_obj, thakaa_buyed_token, thakaa_token_bar

    @staticmethod
    def add_profile_to_company_package(thakaa_buyed_package, profile_obj):
        thakaa_buyed_package.profiles.add(profile_obj)
        thakaa_buyed_package.save()
        return thakaa_buyed_package
    
    @login_required
    def addDoctorOwnCompany(request): # Şirket sahibi kendine doktor ekler
        if request.method == "POST":
            try:
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                print("phone", phone)
                email = request.POST.get("email")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")
                        profile = Profile.objects.get(user=request.user)    
                        thakaa_buyed_package = ThakaaBuyedPackage.objects.filter(company=profile.company).last()
                        if len(thakaa_buyed_package.profiles.all()) >= thakaa_buyed_package.thakaa_package.audience:
                            return JsonResponse({"success": "reached_add_limit", "message": "You can't add more user!"})
                        
                        company_obj = profile.company
                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username)
                        if profile.is_distributor:
                            profile_obj.added_by_distributor = profile
                            profile_obj.save()
                        AddPanelApi.create_user_theme(user)
                        AddPanelApi.add_profile_to_company_package(thakaa_buyed_package, profile_obj)
                        return JsonResponse({"success": "success", "message": ""})
            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def addDoctorDifferentCompany(request): # Başka bir şirkete doktor ekleme
        if request.method == "POST":
            try:
                company = request.POST.get("company")
                print("company", company)
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                print("phone", phone)
                email = request.POST.get("email")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")  
                        company_obj = Company.objects.get(id=int(company))
                        thakaa_buyed_package = ThakaaBuyedPackage.objects.filter(company=company_obj).last()
                        if len(thakaa_buyed_package.profiles.all()) >= thakaa_buyed_package.thakaa_package.audience:
                            return JsonResponse({"success": "reached_add_limit", "message": "You can't add more user!"})

                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username)
                        user_theme = AddPanelApi.create_user_theme(user)
                        
                        thakaa_buyed_package.profiles.add(profile_obj)
                        thakaa_buyed_package.save()
                        
                        return JsonResponse({"success": "success", "message": ""})
            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def addDistributor(request):
        if request.method == "POST":
            try:
                company_name = request.POST.get("company_name")
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                email = request.POST.get("email")
                token = request.POST.get("token")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")                        

                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        company_name = company_name.strip()
                        company_obj = Company.objects.create(name=company_name, email=email, phone=phone)                        
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username, is_distributor=True, is_owner_of_company=True)
                        AddPanelApi.create_buyed_package(token, profile_obj=profile_obj, company_obj=company_obj)
                        AddPanelApi.create_user_theme(user)
                        return JsonResponse({"success": "success", "message": ""})

            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def addCompanyDoctor(request):
        if request.method == "POST":
            try:
                company_name = request.POST.get("company_name")
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                email = request.POST.get("email")
                token = request.POST.get("token")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")                        

                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        company_name = company_name.strip()
                        company_obj = Company.objects.create(name=company_name, email=email, phone=phone)                        
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username, is_owner_of_company=True)
                        AddPanelApi.create_buyed_package(token, profile_obj=profile_obj, company_obj=company_obj)
                        AddPanelApi.create_user_theme(user)
                        return JsonResponse({"success": "success", "message": ""})

            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)
    
    def addDemoUser(request):
        if request.method == "POST":
            try:
                company_name = request.POST.get("company_name")
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                email = request.POST.get("email")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")                        

                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        company_name = company_name.strip()
                        company_obj = Company.objects.create(name=company_name, email=email, phone=phone)
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username, is_owner_of_company=True)
                        AddPanelApi.create_buyed_package(slug="demo_token", profile_obj=profile_obj, company_obj=company_obj)
                        AddPanelApi.create_user_theme(user)
                        return JsonResponse({"success": "success", "message": ""})

            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)
    
    @login_required
    def DistributorAddsUser(request):
        if request.method == "POST":
            try:
                company_name = request.POST.get("company_name")
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                email = request.POST.get("email")
                token = request.POST.get("token")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                distributor_profile = Profile.objects.get(user=request.user)
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")                        

                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        company_name = company_name.strip()
                        company_obj = Company.objects.create(name=company_name, email=email, phone=phone)                        
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username, is_owner_of_company=True)
                        profile_obj.added_by_distributor = distributor_profile
                        profile_obj.save()
                        AddPanelApi.create_buyed_package(token, profile_obj=profile_obj, company_obj=company_obj)
                        AddPanelApi.create_user_theme(user)

                        return JsonResponse({"success": "success", "message": ""})

            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def DistributorAddsUserToCompany(request):
        if request.method == "POST":
            try:
                company = request.POST.get("company")
                first_name = request.POST.get("firstname")
                last_name = request.POST.get("lastname")
                phone = request.POST.get("phone")
                email = request.POST.get("email")
                password = request.POST.get("password")
                validator = CustomPasswordValidator()
                validator.validate(password)
                error_text = validator.get_error_text()
                distributor_profile = Profile.objects.get(user=request.user)
                if error_text:
                    return JsonResponse({"success": "password_error", "message": error_text})
                else:
                    with transaction.atomic():
                        # Password validation and user creation
                        print("Password is valid!")  
                        company_obj = Company.objects.get(id=int(company))
                        thakaa_buyed_package = ThakaaBuyedPackage.objects.filter(company=company_obj).last()
                        if len(thakaa_buyed_package.profiles.all()) >= thakaa_buyed_package.thakaa_package.audience:
                            return JsonResponse({"success": "reached_add_limit", "message": "You can't add more user!"})

                        if User.objects.filter(email=email).exists():
                            return JsonResponse({"success": "user_exists", "message": "A user with this email already exists."})
                        
                        user = AddPanelApi.create_user(email, first_name, last_name, password)
                        profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone, creator_username=request.user.username)
                        profile_obj.added_by_distributor = distributor_profile
                        profile_obj.save()
                        AddPanelApi.create_user_theme(user)

                        thakaa_buyed_package.profiles.add(profile_obj)
                        thakaa_buyed_package.save()

                        return JsonResponse({"success": "success", "message": ""})
            
            except:
                if 'user' in locals() and user is not None:
                    user.delete()
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)



def save_demo_user_api(request):
    try:
        if request.method == "POST":
            company_name = request.POST.get("name", None)
            def check_empty_string(param):
                if param == "":
                    param = None
                return param
            comp = check_empty_string(company_name.replace(" ", ""))
            company_name = comp
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            phone = request.POST.get("phone")
            token = request.POST.get("package", None)
            email = request.POST.get("email")
            password = request.POST.get("password")
            user_id = request.POST.get("user_id", None)
            payment_method = request.POST.get("payment_method", None)
            currency = request.POST.get("currency", None)
            is_admin = False
            is_owner_of_company = False
            if request.user.is_superuser:
                is_admin = True
            
            if str(request.user) == "AnonymousUser": # thakaa signup
                if not company_name or not company_name.strip():
                    return JsonResponse({"success": "reached_add_limit", "message": "Please Fill Company Name Field!"})
            
                company_name = company_name.strip()
                user = User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email)
                user.set_password(password)
                user.save()
                company_obj = None
                try:
                    company_objs = Company.objects.filter(name=company_name)
                    if company_objs.exists():
                        user.delete()
                        return JsonResponse({"success": "reached_add_limit", "message": "Company Name Already Exists!"})
                    else:
                        company_obj = Company.objects.create(name=company_name, email=email, phone=phone)

                    company_obj.email=email
                    company_obj.phone=phone
                    company_obj.save()
                except:
                    user.delete()
                    if company_obj: 
                        company_obj.delete()
                profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone,
                                                creator_username="AnonymousUser", is_owner_of_company=True)
                if token:
                    thakaa_package = ThakaaPackage.objects.first()
                    buyed_package_obj = ThakaaBuyedPackage.objects.create(company=company_obj, thakaa_package=thakaa_package)
                    buyed_package_obj.profiles.add(profile_obj)
                    buyed_package_obj.save()

                    thakaa_token = ThakaaTokenBar.objects.get(slug=token)
                    thakaa_buyed_token = ThakaaBuyedToken.objects.create(company=company_obj, tokenbar=thakaa_token)
                    
                    ThakaaRemainingToken.objects.create(thakaa_buyed_token=thakaa_buyed_token)
                    ## manual satın alımlar için token payment objesi oluşturma ###
                    token_amount = thakaa_token.token
                    total_price_of_token = thakaa_token.total_price.split(",")[0]
                    price_per_token = round(int(thakaa_token.token_per_price),2)
                    token_payment_obj=TokenPayment.objects.create(
                        full_name = first_name + " " + last_name,
                        email=email,
                        phone=phone,
                        total_price = total_price_of_token,
                        token=token_amount,
                        price_per_token=price_per_token,
                        currency="TL", #ahmetle konuştuktan sonra burası ayarlanacak
                        redirect_payment_detail = '{"isSuccessful": "True","resultMessage": "Manual"}',
                        transaction_date = timezone.now(),
                        payment_date = timezone.now(),
                        payment_method = payment_method
                    )
                    logger.info(f"TokenPayment oluşturuldu: {token_payment_obj}")
                    ## manual satın alma kaydı bitiş ##
                user_theme = UserTheme.objects.create(user=user)
                user.is_active = True
                user_theme.language = "en"
                user.save()
                user_theme.save()
                return JsonResponse({"success": True, "message": "Veriler başarıyla işlendi."})

            profile = Profile.objects.get(user=request.user)
            is_owner_of_company = profile.is_owner_of_company
            
            if is_owner_of_company and not company_name and not user_id: # şirket sahibi kendine hasta ekler
                print("is_owner")
                thakaa_buyed_package = ThakaaBuyedPackage.objects.filter(company=profile.company).last()
                if len(thakaa_buyed_package.profiles.all()) >= thakaa_buyed_package.thakaa_package.audience:
                    return JsonResponse({"success": "reached_add_limit", "message": "Daha fazla kullanıcı ekleyemezsiniz!"})
                company_obj = profile.company
                user = User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email)
                user.set_password(password)
                user.save()
                profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone,
                                                creator_username=request.user.username)
                user_theme = UserTheme.objects.create(user=user)
                user.is_active = True
                user_theme.language ="en"
                user.save()
                user_theme.save()
                thakaa_buyed_package.profiles.add(profile_obj)
                thakaa_buyed_package.save()
                

            elif is_admin and company_name and not user_id: #admin yeni kullanıcı oluşturur
                company_name = company_name.strip()
                company_objs = Company.objects.filter(name=company_name)
                if company_objs.exists():
                    return JsonResponse({"success": "reached_add_limit", "message": "Company Name Already Exists!"})
                else:
                    company_obj = Company.objects.create(name=company_name, email=email, phone=phone)

                user = User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email)
                user.set_password(password)
                user.save()
                profile_obj = Profile.objects.create(user=user, company=company_obj, phone=phone,
                                                creator_username=request.user.username, is_owner_of_company=True)                                   
                thakaa_package = ThakaaPackage.objects.first()
                buyed_package_obj = ThakaaBuyedPackage.objects.create(company=company_obj, thakaa_package=thakaa_package)
                buyed_package_obj.profiles.add(profile_obj)
                buyed_package_obj.save()

                if token:
                    thakaa_token_bar = ThakaaTokenBar.objects.get(slug=token)
                    thakaa_buyed_token = ThakaaBuyedToken.objects.create(company=company_obj, tokenbar=thakaa_token_bar)
                    
                    ThakaaRemainingToken.objects.create(thakaa_buyed_token=thakaa_buyed_token)
                    ## manual satın alımlar için token payment objesi oluşturma ###
                    currency_obj = Currency.objects.get(name=currency)
                    print("currency_obj",currency_obj, "currency_obj name",currency_obj.name, "equal", currency_obj.equal)
                    token_amount = thakaa_token_bar.token
                    total_price_of_token = float(thakaa_token_bar.total_price) * float(currency_obj.equal)
                    print("total_price_of_token",total_price_of_token)
                    price_per_token = float(thakaa_token_bar.token_per_price) * float(currency_obj.equal)
                    print("price_per_token",price_per_token)
                    total_price_of_token = round(total_price_of_token,2)
                    price_per_token = round(price_per_token,2)
                    logger.info(f"Total price: {total_price_of_token}, price per token: {price_per_token}")
                    token_payment_obj=TokenPayment.objects.create(
                        full_name = first_name + " " + last_name,
                        email=email,
                        phone=phone,
                        total_price = total_price_of_token,
                        token=token_amount,
                        price_per_token=price_per_token,
                        currency=currency_obj.name, 
                        redirect_payment_details = '{"isSuccessful": "True","resultMessage": "Manual"}',
                        transaction_date = timezone.now(),
                        payment_date = timezone.now(),
                        payment_method = payment_method,
                        company_name = company_name,
                    )
                    ## manual satın alma kaydı bitiş ##

                user_theme = UserTheme.objects.create(user=user)
                user.is_active = True
                user_theme.language = "en"
                user.save()
                user_theme.save()

            elif user_id and is_admin: # admin güncelleme yapar
                print("user_id, is_admin")
                user = User.objects.get(id=user_id)
                profile_obj = Profile.objects.get(user=user)

                if token:
                    thakaa_token = ThakaaTokenBar.objects.get(slug=token)
                    if thakaa_token.slug != ThakaaBuyedToken.objects.filter(company=profile_obj.company).last().tokenbar.slug:
                        thakaa_buyed_token = ThakaaBuyedToken.objects.create(company=profile_obj.company, tokenbar=thakaa_token)
                        ThakaaRemainingToken.objects.create(thakaa_buyed_token=thakaa_buyed_token)

                user.first_name = first_name    
                user.last_name = last_name
                user.email = email
                user.username = email
                user.save()
                profile_obj.phone = phone
                profile_obj.save()

            # Verileri işleme veya kaydetme işlemlerini burada gerçekleştirin

            return JsonResponse({"success": True, "message": "Veriler başarıyla işlendi."})

        return JsonResponse({"success": False, "message": "Geçersiz istek."})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def buy_product(request):
    try:
        print("request", request.method)
        # course_hash = request.GET.get('course_hash', None)
        # print("course", course_hash)
        # course_obj = UsagePackage.objects.get(key=course_hash)
        full_name = request.GET.get('full_name', None)
        email = request.GET.get('email', None)
        phone = request.GET.get('phone', None)
        phone = phone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        card_holder_name = request.GET.get('card_holder_name', None)
        card_number = request.GET.get('card_number', None)
        cvc_number = request.GET.get('cvc_number', None)
        exp_month = request.GET.get('exp_month', None)
        exp_year = request.GET.get('exp_year', None)
        # active_language = request.GET.get('active_language', None)
        # amount = course_obj.price if active_language == 'tr' else course_obj.global_price
        amount = 1.0
        print("amount", amount)
        currency = "TL"
        # currency = "TL" if active_language == 'tr' else "USD"
        # print("1:", course_obj)
        print("2:", full_name)
        print("3:", email)
        print("4:", phone)
        print("6:", amount)
        print("7:", card_holder_name)
        print("8:", card_number)
        print("9:", cvc_number)
        print("10:", exp_month)
        print("11:", exp_year)
        print("12:", currency)
        if len(exp_year) == 2:
            exp_year = "20" + str(exp_year)
            print(exp_year)
        moka_url = "https://service.moka.com/PaymentDealer/DoDirectPaymentThreeD"
        OtherTrxCode = str(uuid.uuid4()) + '-CRN'

        RedirectUrl = f"https://clinic.craniocatch.com/api/Buy/buy_product_result/?trxCodeCranio={OtherTrxCode}"

        request_json = {
            "PaymentDealerAuthentication": {
                "DealerCode": "29706", 
                "Username": "5b6b2459-1c54-47fc-b747-f132f0b4e4f8",
                "Password": "f9f5f0bd-4596-421c-808b-4d297c8617fa",
                "CheckKey": "c9d4600eee2f460618a6f27b0e67c9ebfa31ca7d6b17a462bd2e4ce18f8795b2"
            },
            "PaymentDealerRequest": {
                "CardHolderFullName": card_holder_name, 
                "CardNumber": card_number,
                "ExpMonth": exp_month, 
                "ExpYear": exp_year, 
                "CvcNumber": cvc_number, 
                "Amount": amount,
                "Currency": currency, 
                "InstallmentNumber": 0,
                "ClientIP": "195.155.96.234", 
                "OtherTrxCode": OtherTrxCode, 
                "IsPreAuth": 0,
                "IsPoolPayment": 0, 
                "Software": "CranioCatch", 
                "RedirectUrl": RedirectUrl, 
                "RedirectType": 0,
                "Description": "test açıklama",
                "BuyerInformation": {
                    "BuyerFullName": full_name, 
                    "BuyerEmail": email, 
                    "BuyerGsmNumber": phone
                }
            }
        }
        r = requests.post(moka_url, json=request_json)
        print("r", r)
        print("r.json()", r.json())
        print("r.json()", r.json()["ResultCode"])
        if r.json()["ResultCode"] == "Success":
            user_obj = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user_obj)
            # exist_course = UsagePackageWithProfile.objects.filter(profile=profile,usage_pack=course_obj,is_valid=True).order_by('-id').first()
            # if exist_course:
            #     print('kurs daha önceden satın alındı')
            #     return JsonResponse({'success': False})

            # UsagePackageWithProfile.objects.create(profile=profile, usage_pack=course_obj, selling_price=amount,
            #                                        trxCodeCranio=OtherTrxCode, is_valid=False)
            return JsonResponse({'success': True, 'response': r.json()})
        else:
            return JsonResponse({'success': False, 'response': r.json()})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@csrf_exempt
def buy_product_result(request):
    user_package_with_profile = None
    try:
        trxCodeCranio = request.GET.get("trxCodeCranio")
        if request.method == "POST":
            print("requestpost", request.POST)
            isSuccessful = request.POST.get('isSuccessful', None)
            trxCode = request.POST.get('trxCode', None)
            resultMessage = request.POST.get('resultMessage', None)

            print("1isSuccessful", isSuccessful)
            print("1trxCode", trxCode)
            print("1trxCodeCranio", trxCodeCranio)
            print("1resultMessage", resultMessage)

            # user_package_with_profile = UsagePackageWithProfile.objects.get(trxCodeCranio=trxCodeCranio)
            if isSuccessful == "true" or isSuccessful == "True" or isSuccessful == True:

                user_package_with_profile.is_valid = True
                user_package_with_profile.trxCode = trxCode
                user_package_with_profile.resultMessage = resultMessage
                user_package_with_profile.save()

                send_feedback_email("YENİ BİR SATIN ALIM",
                                    f"{user_package_with_profile.profile.user.username} kullanıcı adına sahip kişi {user_package_with_profile.usage_pack.pack_name} paketini satın aldı",
                                    user_package_with_profile.profile.user)

                return render(request, "succes-buy.html",
                              context={"status": True, "message": "Your purchase has been successful."})

            else:
                user_package_with_profile.resultMessage = resultMessage
                user_package_with_profile.save()
                send_feedback_email("SATIN ALMA BAŞARISIZ",
                                    f"{user_package_with_profile.profile.user.username} is succesfull FALSE",
                                    user_package_with_profile.profile.user)
                return render(request, "succes-buy.html", context={"status": True, "message": resultMessage})
        else:
            send_feedback_email("SATIN ALMA BAŞARISIZ", f"POST İSTEĞİ ATILMADI",
                                "BU URL YE FARKLI Bİ İSTEK ATILMAYA ÇALIŞILIYOR...")
            return render(request, "succes-buy.html", context={"status": True, "message": "Invalid request type."})

    except:
        print(traceback.print_exc())
        var = traceback.format_exc()
        send_feedback_email("SATIN ALMA İŞLEMİNDE HATA", "FALSE", str(var))

    return render(request, "succes-buy.html", context={"status": True, "message": "Rendered without Context"})


# if isSuccessful == "true" or isSuccessful == "True" or isSuccessful == True:
#     print("Başarılı")
#     cb_obj = CourseBuyed.objects.get(trxCode=trxCode)
#     app_api_url = f"http://93.89.73.104:8080/user/api/createUserWithPack/?username={cb_obj.user.username}"
#     app_api_url += f"&first_name={cb_obj.user.profile.full_name}"
#     app_api_url += f"&phone={cb_obj.user.username}"
#     app_api_url += f"&email={cb_obj.user.email}"
#     app_api_url += f"&password={cb_obj.user.profile.password}"
#     app_api_url += f"&pack_key={cb_obj.course.hash}"
#     app_api_url += f"&company_name={cb_obj.company_name}"
#     app_api_url += f"&trxCode={trxCode}"
#     app_api_url += f"&trxCodeCranio={trxCode}-CRN"
#     app_api_url += f"&production_type=app"
#     app_api_url += f"&token=09DC2632A0694D2AA2B0D05E9D0E2EDC1E4F2B6D85634641A30E85AA7DB0A4E0E2C485DF631444DA8AC5A950E31DDF90"
#     print(app_api_url)
#     try:
#         request_result = requests.get(app_api_url)
#         print("request_result.json()", request_result.json())
#         if request_result.json()['status'] == False:
#             print("hata api")
#             moka_url = "https://service.moka.com/PaymentDealer/DoVoid"
#             request_json = {"PaymentDealerAuthentication": {"DealerCode": "29706",
#                 "Username": "5b6b2459-1c54-47fc-b747-f132f0b4e4f8",
#                 "Password": "f9f5f0bd-4596-421c-808b-4d297c8617fa",
#                 "CheckKey": "c9d4600eee2f460618a6f27b0e67c9ebfa31ca7d6b17a462bd2e4ce18f8795b2"},
#                 "PaymentDealerRequest": {"VirtualPosOrderId": trxCode, "ClientIP": "195.155.96.234",
#                     "VoidRefundReason": 2}}
#             moka_request = requests.post(moka_url, json=request_json)
#             if moka_request.json()["ResultCode"] == "Success":
#                 print("İptal edildi işlem")
#                 isSuccessful = 'False'
#                 transaction_canceled = True
#         else:
#             exist_course = CourseBuyed.objects.filter(user=cb_obj.user, success=True).order_by('-id').first()
#             if exist_course:
#                 send_sms(str(cb_obj.user.username),
#                          f"CranioCatch {cb_obj.course.name} - {cb_obj.course.type_name}  ürününü başarı ile satın aldınız. Panel Giriş Linki: https://app.craniocatch.com/",
#                          'CRANIOCATCH')
#                 cb_obj.success = True
#                 cb_obj.save()
#                 send_email('BUY COURSE',
#                            f'Yeni bir satın alım isim:{str(cb_obj.user.username)}, kurs:{cb_obj.course.name} - {cb_obj.course.type_name}')
#             else:
#                 send_sms(str(cb_obj.user.username),
#                          f"CranioCatch {cb_obj.course.name} - {cb_obj.course.type_name}  ürününü başarı ile satın aldınız. Kullanıcı adınız:{cb_obj.user.username} Şifreniz:{cb_obj.user.profile.password} Panel Giriş Linki: https://app.craniocatch.com/  Lütfen şifrenizi kimse ile paylaşmayınız!",
#                          'CRANIOCATCH')
#                 cb_obj.success = True
#                 cb_obj.save()
#                 send_email('BUY COURSE',
#                            f'Yeni bir satın alım isim:{str(cb_obj.user.username)}, kurs:{cb_obj.course.name} - {cb_obj.course.type_name}')


# tüm hastalıkları veren kod,
@login_required
def all_diseases(request):
    try:
        diagnosis_dict = {}
        # image_report_id = request.POST.get("image_report_id")
        image_report_id = request.GET.get("image_report_id")
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
        patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
        active_labels = active_model_labels_function()[image_report_obj.name][patient_type]

        disease_list = []
        # aktif labelleri cacheden alıp bu labellerin içinde 2 kere key value dönerek gerekli bilgileri dicte, sonra da dicti listeye attım
        # for key, value in active_labels.items():
        for key, value in active_labels.items():
            disease_info = {"id": value["id"], "name": key, "tr_name": value["tr_name"], "color": value["color"]}
            disease_list.append(disease_info)
        return JsonResponse({"disease_list": disease_list})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
def formCreateUpdateForCompany(request):
    try:
        form_data = json.loads(request.POST.get('formData'))
        user = request.user
        profile = Profile.objects.get(user=user)
        slug = str(uuid.uuid4()).replace("-", "")
        for data in form_data:
            question_id = data['questionId']
            is_required = False
            is_active = False

            for item in form_data:
                if item['questionId'] == question_id:
                    if item['name'] == 'required' and item['value'] == 'on':
                        is_required = True
                    elif item['name'] == 'show' and item['value'] == 'on':
                        is_active = True
            questions = get_questions_with_json()
            try:
                question = questions.get(id=question_id)
                if not FormWithCompany.objects.filter(company=profile.company, question=question).exists():
                    form_with_company = FormWithCompany.objects.create(company=profile.company, question=question,
                        required=is_required, is_active=is_active, form_slug=slug)
                else:
                    form_with_company = FormWithCompany.objects.get(company=profile.company, question=question)
                    form_with_company.required = is_required
                    form_with_company.is_active = is_active
                    form_with_company.save()
            except FormQuestion.DoesNotExist:
                print("Question does not exist")

        return JsonResponse({'success': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@csrf_exempt
def save_patient_form(request):
    try:
        if request.method == 'POST':
            slug = str(uuid.uuid4()).replace("-", "")
            forms = request.POST
            print("forms: ", forms)
            file = request.FILES.get('file')
            form_obj = FormWithCompany.objects.filter(form_slug=forms['slug']).first()
            print("form obj", form_obj, form_obj.id)
            for question_slug, answers in forms.items():
                print("answers: ", answers)
                question_slug = question_slug.replace("[]", "")
                # if question_slug == "chronicDiseasesSpecify":
                #     FormAnswers.objects.create(
                #         form=form_obj,
                #         question_slug="fe91012bb2a140059985b10f774d5de4",
                #         group_slug=slug,
                #         answer=answers,  # Specify alanının answer değeri
                #         date=datetime.now()
                #     )
                # else:
                if question_slug == 'slug' or question_slug == "csrfmiddlewaretoken":
                    continue  # 'slug' anahtarını atla
                if answers:
                    if question_slug == "fe91012bb2a140059985b10f774d5de4":
                        FormAnswers.objects.create(form=form_obj, question_slug=question_slug, group_slug=slug,
                        answer=answers, date=datetime.now(), specify=forms["chronicDiseasesSpecify"])
                    elif question_slug == "ad5693a69e714905a68272d8994cc9a0":
                        FormAnswers.objects.create(form=form_obj, question_slug=question_slug, group_slug=slug,
                        answer=answers, date=datetime.now(), specify=forms["dentalIssueSpecify"])
                    elif question_slug == "c7c5de51a8424bc0bb16e344c62ae1a0":
                        FormAnswers.objects.create(form=form_obj, question_slug=question_slug, group_slug=slug,
                        answer=answers, date=datetime.now(), specify=forms["dietaryPreferenceSpecify"])
                    elif question_slug == "02893d1a43844e5aa043b586285deae0":
                        FormAnswers.objects.create(form=form_obj, question_slug=question_slug, group_slug=slug,
                        answer=answers, date=datetime.now(), specify=forms["allergicSpecify"])
                    else:
                        if question_slug == "dentalIssueSpecify" or  question_slug == "dietaryPreferenceSpecify" or question_slug == "allergicSpecify":
                            continue
                        FormAnswers.objects.create(form=form_obj, question_slug=question_slug, group_slug=slug,
                            answer=answers, date=datetime.now())
                
            if file:
                original_file_name, file_extension = os.path.splitext(file.name)
                new_file_name = str(uuid.uuid4()) + file_extension
                file.name = new_file_name
                image_object = FormRadiographs.objects.create(path=file, form_answer_group_slug=slug)
                image_object.save()

            return JsonResponse({'message': 'Success'})  # İsteği başarılı bir şekilde tamamlandı olarak yanıtla
        else:
            return JsonResponse({'message': 'Invalid request'}, status=400)  # Geçersiz bir istek olduğunu yanıtla
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def save_drawed_diagnosis(request):
    print("request")
    try:
        if request.method == 'POST':
            try:
                label_id = request.POST.get("label_id")
                coordinates = request.POST.get("coordinates")
                image_report_id = request.POST.get("image_report_id")
                original_shape = request.POST.get("original_shape")
                coordinates = json.loads(coordinates)
                original_shape = json.loads(original_shape)
                image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
                rate_x, rate_y = original_shape[0], original_shape[1]
                new_coordinates = []
                print("coordinates", coordinates, type(coordinates))
                for xy in coordinates:
                    print("xy", xy)
                    x = xy[0] / rate_x
                    y = xy[1] / rate_y
                    new_coordinates.append([x, y])
                coordinates = new_coordinates
                patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
                active_labels = active_model_labels_function()[image_report_obj.name][patient_type]
                current_label = None
                status = False
                slug = None

                def add_to_result_json(value):
                    slug = str(uuid.uuid4())
                    data = {
                        "name": value["name"],
                        "coordinates": coordinates,
                        "probability": 101,
                        "slug": slug,
                        "approve_status": 0,
                    }
                    if current_label["area"] == "Palate":
                        result_json = json.loads(image_report_obj.result_json)

                        result_json["palate_results"].append(data)
                        veri = json.dumps(result_json)
                        image_report_obj.result_json = veri
                        image_report_obj.save()
                        return True, slug

                    if current_label["area"] == "Tooth":
                        result_json = json.loads(image_report_obj.result_json)

                        result_json["illness_pool"].append(data)
                        veri = json.dumps(result_json)
                        image_report_obj.result_json = veri
                        image_report_obj.save()
                        return True, slug

                for label, value in active_labels.items():
                    if value["id"] == int(label_id):
                        value["name"] = label
                        current_label = value
                        print("current", current_label)
                        status, slug = add_to_result_json(value)
                        break
                return JsonResponse({"status": True if status else False, "slug": slug})
            except:
                traceback.print_exc()
                return JsonResponse({"status": False})
            #     print("error------------------------------------------------------------------------------------------")
            #     return JsonResponse({"status": False})
        return HttpResponse(status=404)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

class PatientsForDatatable(APIView):
    def get(self,request):
        user = request.user
        profile = Profile.objects.get(user=user)
        page = int(request.GET.get('page', 1))  # Sayfa numarasını al, eğer verilmezse varsayılan olarak 1
        print("page",page)
        page_size = request.GET.get('page_size', 10)  # Listeleme sayısını al, eğer verilmezse varsayılan olarak 10
        print("page size",page_size)
        if page_size == "Hepsi":
            patients = Patient.objects.filter(user=profile).order_by("-id")
            serializer = PatientSerializer(patients, many=True)
            print("serializer",serializer.data)
            user_theme = UserTheme.objects.get(user=user)
            user_theme.page_length = page_size
            user_theme.save()
        else:
            start_index = (page - 1) * int(page_size)
            end_index = start_index + int(page_size)
            print("start index",start_index)
            print("end index",end_index)
            
            patients = Patient.objects.filter(user=profile).order_by("-id")[start_index:end_index]
            serializer = PatientSerializer(patients, many=True)
            print("serializer",serializer.data)
            user_theme = UserTheme.objects.get(user=user)
            user_theme.page_length = page_size
            user_theme.save()
        return Response(serializer.data)


@login_required
def download_drawed_radiography_button(request):
    try:
        image_report_id = request.GET.get('image_report_id')
        image_report_obj = ImageReport.objects.get(id=image_report_id)
        path = image_report_obj.image.path
        output_path = draw_function(path, image_report_obj.id)
        print(f"OUTPUT PATH: {output_path}")
        output_path = output_path.replace(ccclinic_path, "")
        return JsonResponse({"status": "True", "output_path": output_path})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def delete_drawed_illness(request):
    try:
        if request.method == 'POST':
            illness_slug = request.POST.get('illness_slug')
            image_report_id = request.POST.get('image_report_id')
            image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
            delete_status = False
            result_json = json.loads(image_report_obj.result_json)

            for i, item in enumerate(result_json["palate_results"]):
                if item["slug"] == illness_slug:
                    del result_json["palate_results"][i]
                    delete_status = True
                    break
            for i, item in enumerate(result_json["illness_pool"]):
                if item["slug"] == illness_slug:
                    del result_json["illness_pool"][i]
                    delete_status = True
                    break

            if not delete_status:
                return JsonResponse({"status": delete_status, "message": "Could not delete!"})
            else:
                image_report_obj.result_json = json.dumps(result_json)
                image_report_obj.save()
            return JsonResponse({"status": delete_status})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def delete_user(request):
    try:
        user_id = request.POST.get("userId")
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        company = profile.company
        profiles = Profile.objects.filter(company=company)
        is_owner_status = False
        if len(profiles) <= 1: # Eğer o company'nin 1 tane kullanıcısı varsa
            user.delete()
            company.delete()
        else: # Company nin 1 den fazla kullanıcısı varsa
            for prof in profiles: # Diğer profillerde dön ve o company nin owneri yoksa yeni owner belirle
                if prof != profile and prof.is_owner_of_company:
                    is_owner_status = True
            if not is_owner_status:
                new_owner_profile = profiles[0]
                new_owner_profile.is_owner_of_company = True
                new_owner_profile.save()
            # Belirleme işlemi tamamlandı artık kullanıcıyı sil
            user.delete()
        return JsonResponse({'status': True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def get_manuel_calibration(request):
    try:
        measure = int(request.POST.get("measure"))
        first_coord = json.loads(request.POST.get("first_coord"))
        second_coord = json.loads(request.POST.get("second_coord"))
        image_report_id = request.POST.get("image_report_id")
        image_report_obj = ImageReport.objects.get(id=int(image_report_id))
        print("measure", measure, type(measure))
        print("first_coord", first_coord, type(first_coord))
        print("second_coord", second_coord, type(second_coord))
        print("image_report_id", image_report_id, type(image_report_id))
        cephalometric_landmarks = json.loads(image_report_obj.result_json)["results"]["cephalometric_landmarks"]
        result = cephalometric_analyses(cephalometric_landmarks, measure, first_coord, second_coord)
        if result:
            result["calibration_status"] = "True"
            image_report_obj.result_json = json.dumps(result)
            image_report_obj.save()
            print("RESULT: ", result)
        # analyze_start_status = start_lateral_analyze(measure, first_coord, second_coord, image_report_obj, request.user)

        return JsonResponse({"status": True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def archive_image(request):
    try:
        print("request", request)
        if request.method == "POST":
            print("inpost")
            print("requests", request.POST) 
            image_report_id = request.POST.get("image_report_id")
            image_report_obj = ImageReport.objects.get(id=int(image_report_id), user__user=request.user)
            image_obj = image_report_obj.image
            image_obj.archived = True
            image_obj.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def draw_treatment_plan(request):
    try:
        print("request", request)
        if request.method == "POST":
            coordinates = request.POST.get("coordinates")
            size = request.POST.get("size")
            transform = request.POST.get("transform")
            if coordinates and size and transform:
                slug = str(uuid.uuid4())
                draw_treatment_plan.objects.create(
                    slug=slug, 
                    coordinates=coordinates
                    )
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def save_implant_or_crown(request):
    try:
        status = False
        response_dict = {}
        if request.method == "POST":
            slug = request.POST.get("slug")
            item_type = request.POST.get("item_type") # crown, implant
            icon_id = request.POST.get("icon_id")
            coordinate = request.POST.get("coordinate")
            dimension = request.POST.get("dimension")
            image_report_id = request.POST.get("image_report_id")
            original_shape = request.POST.get("original_shape")
            rotate = request.POST.get("rotate")
            image_report_obj = ImageReport.objects.get(id=image_report_id)
            message = "İşlem Yapılmadı"
            if slug:
                drawed_implant_or_crown = DrawedImplantOrCrown.objects.get(slug=slug, image_report=image_report_obj)
                drawed_implant_or_crown.coordinate = coordinate
                drawed_implant_or_crown.dimension = dimension
                drawed_implant_or_crown.rotate = rotate
                drawed_implant_or_crown.original_shape = original_shape
                drawed_implant_or_crown.save()
                message = "Updated"
                status = True
            if not slug:
                drawed_implant_or_crown = DrawedImplantOrCrown.objects.create(
                    image_report = image_report_obj,
                    coordinate = coordinate,
                    dimension = dimension,
                    rotate = rotate,
                    original_shape = original_shape,
                    item_type = item_type,
                    icon_id = icon_id,
                )
                response_dict["slug"] = drawed_implant_or_crown.slug
                message = "Created"
                status = True
        else:
            message = "Yanlış istek türü: GET"
        return JsonResponse({"status": status, "response_dict": response_dict, "message": message})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def delete_implant_or_crown(request):
    try:
        status = False
        if request.method == "POST":
            slug = request.POST.get("slug")
            image_report_id = request.POST.get("image_report_id")
            image_report_obj = ImageReport.objects.get(id=image_report_id)
            if slug:
                drawed_implant_or_crown = DrawedImplantOrCrown.objects.get(slug=slug, image_report=image_report_obj)
                drawed_implant_or_crown.delete()
                message = "Deleted"
                status = True
            else:
                status = False
                message = "NO SLUG SENDED"
        else:
            message = "wrong request type"
        return JsonResponse({"status": status, "message": message})
        
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def get_token_informations(request):
    try:
        profile_obj = Profile.objects.get(user=request.user)
        remaining_dict = cranio_remaining_token(profile_obj=profile_obj, detailed_status=False)
        return JsonResponse({"status": True, "remaining_dict": remaining_dict})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)
        return JsonResponse({"status": False})

@csrf_exempt
def create_user_from_website(request):
    try:
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        company_name = request.POST.get("company_name")
        total_price = request.POST.get("total_price")
        price_per_token = request.POST.get("price_per_token")
        token = request.POST.get("token")
        currency = request.POST.get("currency")
        phone = request.POST.get("phone")
        user, user_created = User.objects.get_or_create(username=email)
        profile_status = False
        if user_created:
            user.first_name = full_name
            user.email = email
            user.save()
            company_obj, company_created = Company.objects.get_or_create(name=company_name)
            if company_created:
                company_obj.email = email 
                company_obj.phone = phone
        else:
            profile_status = True
            profile_obj = Profile.objects.get(user=user)
            company_obj = profile_obj.company
        if user_created:
            # Sadece harf ve sayı içeren karakter kümesi
            characters = string.ascii_letters + string.digits

            # 8 karakterli rasgele şifre oluştur
            password = ''.join(secrets.choice(characters) for _ in range(8))
            user.set_password(password)
            user.save()
        if profile_status == False:
            profile_obj, profile_created = Profile.objects.get_or_create(user=user, company=company_obj)
            if profile_created:
                profile_obj.creator_username = "Website-Buy"
                profile_obj.is_owner_of_company = True
                profile_obj.phone = phone
                profile_obj.save()
                                            
        cranio_package = ThakaaPackage.objects.first()
        buyed_package_obj, buyed_package_created = ThakaaBuyedPackage.objects.get_or_create(company=company_obj, cranio_package=cranio_package)
        buyed_package_obj.profiles.add(profile_obj)
        buyed_package_obj.save()

        if token:
            cranio_token_bar = ThakaaTokenBar.objects.get(token=token)
            cranio_buyed_token = ThakaaBuyedToken.objects.create(company=company_obj, tokenbar=cranio_token_bar)
            
            ThakaaRemainingToken.objects.create(cranio_buyed_token=cranio_buyed_token)

        user_theme, user_theme_created = UserTheme.objects.get_or_create(user=user)
        user.is_active = True
        user_theme.language = "en"
        user.save()
        user_theme.save()
        if user_created:
            send_payment_email(email,f"CranioCatch Password",f"Hello Dear {full_name}\nYour password has been automatically generated by Craniocatch. You can change your password later by going to the Profile-Update Profile page. \nPassword: {password}\nWe wish you healthy days…")
        return JsonResponse({"status": True})
    except:
        var = traceback.format_exc()
        send_feedback_email("CLİNİC create_user_from_website", str(var))
        traceback.print_exc()
        return JsonResponse({"status": False})


@csrf_exempt
def check_user_and_token(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            company = request.POST.get("company_name")
            total_price = request.POST.get("total_price")
            pricing_per_token = request.POST.get("pricing_per_token")
            pricing_token_count = request.POST.get("pricing_token_count")

            print(email, company, total_price, pricing_per_token, pricing_token_count)

            company_obj = Company.objects.filter(name=company).first()
            user_exists = User.objects.filter(username=email).first()

            user_obj = user_exists if user_exists else User.objects.filter(email=email).first()
            
            token_message = ""
            return_dict = {"status": True, "message": token_message}
            
            token_bar = ThakaaTokenBar.objects.filter(token=pricing_token_count).first()
            print("token_bar", token_bar)
            return_status = False
            # TOKEN BİLGİLERİ KONTROL EDİLİR, ÖNCE ATILAN TOKEN ADEDİNE BAKILIR DAHA SONRA TOPLAM ÜCRET 
            # VE TOKEN BAŞI ÜCRET VERİTABANINDAKİ BİLGİLERİYLE UYUŞUYOR MU DİYE HEM DOLAR HEM TL CİNCİNSEN 
            # KONTROLÜ GERÇEKLEŞTİRİLİR. DOLARDA DİREKT EŞLEŞME YAPILIR TL DE İSE GİRİLİEN DOLAR KURUNA GÖRE 
            # HESAPLANDIKTAN SONRA USD YE ÇEVRİLİP KONTROLÜ YAPILIR
            if not token_bar: 
                return_dict["status"] = False
                return_dict["message"] = ["Geçersiz Token", "Invalid Token"]
                return_status = True
            else:
                # TL TL TL TL TL TL TL TL TL TL 

                rounded_total_price = round(token_bar.total_price, 2)
                rounded_token_per_price = round(token_bar.token_per_price, 2)
                print("rounded_total_price", rounded_total_price, rounded_token_per_price)
                print("float(rounded_token_per_price/30)", round(float(float(total_price)/30), 2), float(rounded_token_per_price))
                if float(rounded_total_price) != round(float(float(total_price)/30), 2) and float(rounded_token_per_price) != round(float(pricing_per_token),2):
                    return_dict["status"] = False
                    return_dict["message"] = ["Token verisinde hata!", "Error in Token Data"]
                    return_status = True

                # TL TL TL TL TL TL TL TL TL TL 
                # USD USD USD USD USD USD USD USD 

                rounded_total_price = round(token_bar.total_price, 2)
                rounded_token_per_price = round(token_bar.token_per_price, 2)
                if return_status == True and float(rounded_total_price) != float(total_price) and float(rounded_token_per_price) != float(pricing_per_token):
                    return_dict["status"] = False
                    return_dict["message"] = ["Token verisinde hata!", "Error in Token Data"]
                    return_status = True

                # USD USD USD USD USD USD USD USD
            if user_obj and not return_status:
                if company_obj:
                    upgrade_message = [f"Şu anda var olan bir {email} hesabı için token satın alıyorsunuz. Eğer bu hesap size ait değilse lütfen farklı bir email adresi ile devam edin!" ,f"You are purchasing tokens for an existing {email} account. If this account does not belong to you, please continue with a different email address!"]
                    return_dict["status"] = "Info"
                    return_dict["message"] = upgrade_message
                else:
                    upgrade_message = [f"Girilen mail adresine bağlı bir hesap var ancak verilen şirket ismine ait bir kayıt bulunamadı. Şirket ismini kontrol ediniz." ,f"The account associated with the entered email address exists, however, no record was found for the provided company name. Please verify the company name."]
                    return_dict["status"] = False
                    return_dict["message"] = upgrade_message
            elif not user_obj and not return_status:
                if company_obj:
                    company_message = ["Girmiş olduğunuz mail adresiniz girilen şirket adına tanımlı değil!", "The email address you have entered is not associated with the provided company name!"]
                    return_dict["status"] = False
                    return_dict["message"] = company_message
            return JsonResponse(return_dict)
    except:
        traceback.print_exc()
        var = traceback.format_exc()
        send_feedback_email("CLİNİC check_user_and_token", "FALSE", str(var))
        return JsonResponse({"status": "Error!"})


def update_lateral_points(request):
    try:
        label_name = request.POST.get("label_name")
        str_coordinates = request.POST.get("coordinates")
        print("str_coordinates", str_coordinates, type(str_coordinates))
        coordinates = json.loads(str_coordinates)
        image_report_id = request.POST.get("image_report_id")
        print("label", label_name)
        print("coordinates", coordinates)
        print("image_report_id", image_report_id)
        image_report_obj = ImageReport.objects.get(id=image_report_id)
        result_json = json.loads(image_report_obj.result_json)
        cephalometric_landmarks = result_json["results"]["cephalometric_landmarks"]

        for item in cephalometric_landmarks:
            print("item", item)
            if item["label"] == label_name:
                print("itemitemitemitemitemitemitemitemitem", item)

                item["coordinates"] = [coordinates, coordinates]
                break
        
        print("\n\ncephalometric_landmarks", cephalometric_landmarks)
        measure = result_json["calibration_points"]["calibration_measure"]
        first_coord = result_json["calibration_points"]["calibration_points_xy"][0]
        second_coord = result_json["calibration_points"]["calibration_points_xy"][1]
        image_report_obj = ImageReport.objects.get(id=int(image_report_id))
        print("measure", measure, type(measure))
        print("first_coord", first_coord, type(first_coord))
        print("second_coord", second_coord, type(second_coord))
        print("image_report_id", image_report_id, type(image_report_id))
        result = cephalometric_analyses(cephalometric_landmarks, measure, first_coord, second_coord)
        print("result", result)
        if result:
            image_report_obj.result_json = json.dumps(result)
            image_report_obj.save()
            print("RESULT: ", result)

        return JsonResponse({"status": True})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def update_tokens(request):
    print("request", request)
    try:
        user = request.user
        profile_obj = Profile.objects.get(user=user)
        update_dict = {
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "company": profile_obj.company.name,
            "phone": profile_obj.phone,
        }
        url = "http://93.89.73.104:8081/api/update_token/"
        response = requests.post(url, data=update_dict)
        print("response", response)
        data = response.json()
        print("data", data)
        if data["status"] == True:
            slug = data["slug"]
            destination_url = f"https://www.craniocatch.com/update_pricing/{slug}/"
            return JsonResponse({"status": True, "url": destination_url})

        else:
            return JsonResponse({"status": False, "message": "Şu anda token satin alma işlemi yapilamiyor!"})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)
        return JsonResponse({"status": False, "message": "Şu anda token satin alma işlemi yapilamiyor!"})
    
def active_arabic(request):
    try:
        checked = request.POST.get("checked", False)
        checked = checked == "true" 
        user_theme_obj = UserTheme.objects.get(user=request.user)
        user_theme_obj.arabic = checked
        user_theme_obj.save()
        return JsonResponse({"status": True, "value": 1 if checked else 0})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)
    
def logout_save(request):
    user = request.user
    print("user çıkış yapıyor",user)

@csrf_exempt
def AICacheUpdateSignal(request):
    fetch_data_from_AI_labels() #sinyal gelince cacheyi güncelleme
    print("*** CACHE UPDATED ***")
    return HttpResponse(status=200)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        hl7_message = request.POST.get('hl7message', None)  # Gelen istek içinde 'url' parametresini al
        if hl7_message:
            print("hl7_message", hl7_message)
        else:
            return JsonResponse({'error': 'URL parameter is missing'}, status=400)  # URL parametresi eksik
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)  # Geçersiz istek metodu
    
@csrf_exempt
def feedback(request):
    try:
        user=request.user
        ui_design_star = request.POST.get("ui_design_star")
        print("ui desgin start",ui_design_star)
        ui_design_comment = request.POST.get("ui_design_comment")
        bug_star = request.POST.get("bug_star")
        bug_comment = request.POST.get("bug_comment")
        features_star = request.POST.get("features_star")
        features_comment = request.POST.get("features_comment")
        performance_star = request.POST.get("performance_star")
        performance_comment = request.POST.get("performance_comment")
        expected_outcome_star = request.POST.get("expected_outcome_star")
        expected_outcome_comment = request.POST.get("expected_outcome_comment")
        Feedback.objects.create(
            user=user,
            ui_design_star=ui_design_star,
            ui_design_comment=ui_design_comment,
            bug_star=bug_star,
            bug_comment=bug_comment,
            features_star=features_star,
            features_comment=features_comment,
            performance_star=performance_star,
            performance_comment=performance_comment,
            expected_outcome_star=expected_outcome_star,
            expected_outcome_comment=expected_outcome_comment,
        )
        print(f"user:{user.email}\nui_design_star:{ui_design_star}\n -- ui_design_comment:{ui_design_comment}\n -- bug_star:{bug_star}\n -- bug_comment:{bug_comment}\n -- features_star:{features_star}\n -- features_comment:{features_comment}\n -- performance_star:{performance_star}\n -- performance_comment:{performance_comment}\n -- expected_outcome_star:{expected_outcome_star}\n -- expected_outcome_comment:{expected_outcome_comment}")
        subject = "CranioCatch Clinic - Feedback"
        message = f"Feedback Detayı:\nKullanıcı: {user.email}\nUI Design Verilen Yıldız: {ui_design_star}\nUI Design Yorumu: {ui_design_comment}\nBug Yıldız: {bug_star}\nBug Yorumu: {bug_comment}\nFeature Yıldız:{features_star}\nFeature Yorum: {features_comment}\nPerformance Yıldız: {performance_star}\nPerformance Yorumu: {performance_comment}\Expected Outcome Yıldız: {expected_outcome_star}\nExpected Outcome Yorum:{expected_outcome_comment}"
        # send_email_to_management(subject, message)
        print("***** MAIL GONDERILIYOR *****" , " --- Başlık", subject , "--- KONU", message )
        return JsonResponse({'success':True})
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error occurred while getting feedback infos: {traceback_str} -- user: {user.email}")


def patient_past_analysis(request):
    def get_analysis_result_page_url(obj):
        if "Cephalometric" in obj.name:
            return f"/{lang}/cephalometric/{obj.id}" 
        elif "CBCT" in obj.name:
            return f"/{lang}/diagnosis3d/{obj.id}"
        else: 
            return f"/{lang}/diagnosis/{obj.id}"
    try:    
        if request.method == "GET":
            patient_slug = request.GET.get("patient_slug")
            patient_obj = Patient.objects.get(slug=patient_slug)

            lang = request.GET.get("lang")

            # Tek bir sorgu yaparak verileri alın
            reports = ImageReport.objects.select_related('user__user', 'dicom__patient').filter(
                Q(user__user=request.user) & Q(Q(image__patient=patient_obj) | Q(dicom__patient=patient_obj)),
                Q(name="CBCT") | Q(image__patient__archived=False, image__archived=False)
            ).order_by('-created_date')
            print("reports", reports)
            data = []

            for report in reports:
                if report.is_done and not report.is_error:
                    status = "fa-bolt completed-ok"
                elif report.is_error:
                    status = "fa-bolt completed-no"
                else:
                    report = set_timeout_image_reports(report, 15)
                    status = "fa-spinner process"

                nifti_created_date = report.created_date + timedelta(hours=3)
                formatted_date = nifti_created_date.strftime('%d-%m-%Y %H:%M')
                url = get_analysis_result_page_url(report)
                if report.image:
                    patient = report.image.patient.first_name + " " + report.image.patient.last_name,
                data.append({
                    'status': status,
                    'user': report.user.user.first_name + " " + report.user.user.last_name,
                    'created_date': formatted_date,
                    'name': report.name,
                    'id': report.id,
                    'patient': patient,
                    'url': url,
                    'image_url': report.image.thumbnail_image_path.url if report.image else None,
                })

        # sorted_data = sorted(data, key=lambda x: datetime.strptime(x['created_date'], '%d-%m-%Y %H:%M'), reverse=True)
        print("data", data)
        return JsonResponse({"data": data})

    except:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)
        return JsonResponse({"error": "Error at during process"})
