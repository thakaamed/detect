from datetime import datetime, timedelta
import pytz
from Application.models import *
from Wizard.models import LabelNamesForWizard
from Wizard.models import *
from User.models import *
from django.http import JsonResponse
import requests
# SAVE USER WİTH JS API METHOD
import smtplib
from email.message import EmailMessage
from dateutil.relativedelta import relativedelta
import os
import cv2
import json
from django.conf import settings
import numpy as np
from Server.settings import ccclinic_path_with_slash
from Application.cache_processes import active_model_labels_function
from src.point_detection.cephalometric.cephalometric_analysesv4 import CephalometricAnalysis
from datetime import datetime, timedelta,date
import time
from django.db.models import Count
from django.db.models.functions import TruncMonth
import logging
import traceback
from PIL import Image as pil_Image
import uuid
from ast import literal_eval
logger = logging.getLogger('main')
analyse = CephalometricAnalysis()

def create_objects_for_wizard(image_report,diagnosis_json, treatment_json):
    print("diagnosis_json",diagnosis_json)
    tooth_dict = {}
    treatment_dict = {}
    # image_type = image_report.image.type.name
    # cached_labels = active_model_labels_function[image_type]
    try:
        for key,value in diagnosis_json.items():
            tooth_dict[key] = {
                "is_missing": value["is_missing"],
                "illnesses": [{"name": illness["name"], "probability": illness["probability"], "slug": illness["slug"]} for illness in value.get("illnesses", [])]
            }
            if value["is_missing"]:
                missing_obj = LabelNamesForWizard.objects.get(en_name="Missing")
                tooth_dict[key] = {
                    "illnesses":[{"name":missing_obj.en_name,"tr_name":missing_obj.tr_name,"ar_name":missing_obj.ar_name,"fr_name":missing_obj.fr_name,"pt_name":missing_obj.pt_name, "slug":str(uuid.uuid4()).replace("-","")}],
                    "is_missing": value["is_missing"],
                }
            if str(key).startswith(('1', '2','5','6')):
                tooth_dict[key]["jaw_area"] = "upper_jaw"
            elif str(key).startswith(('3', '4','7','8')):
                tooth_dict[key]["jaw_area"] = "lower_jaw"
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error occurred while configuring diagnosis json: {traceback_str}")
    
    try:
        for key,value in treatment_json.items():
            if value["treatment_methods"]:
                treatment_dict[key] = {
                    "illnesses":value["illnesses"],
                    "treatment_methods": value["treatment_methods"]
                }
    except Exception as e:
        traceback_str = traceback.format_exc()
        logger.error(f"Error occurred while configuring treatment json: {traceback_str}")

    #treatment wizard objesi oluşturma #
    treatment_wizard=TreatmentWizard.objects.create(image_report=image_report, diagnosis_data=json.dumps(tooth_dict),raw_treatment_data = json.dumps(treatment_dict))
    TreatmentPlan.objects.create(
        treatment_wizard = treatment_wizard,
        plan_treatment_data = json.dumps(treatment_dict)
    )
def for_user_radiography_type_counts(user):
    profile = Profile.objects.get(user=user)
    start_time = time.time()
    radiography_types = Image.objects.filter(user=profile).values('type__name').annotate(count=Count('type'))
    try:
        lateral = radiography_types.get(type__name="Lateral Cephalometric")['count']
    except:
        lateral = 0
    try:
        panaromic = radiography_types.get(type__name="Panaromic")['count']
    except:
        panaromic = 0
    try:
        bitewing = radiography_types.get(type__name="Bitewing")['count']
    except:
        bitewing = 0
    try:
        cbct = radiography_types.get(type__name="CBCT")['count']
    except:
        cbct = 0
    try:
        periapical = radiography_types.get(type__name="Periapical")['count']
    except:
        periapical = 0
    end_time = time.time()
    elapsed_time = end_time - start_time
    return panaromic, bitewing, periapical, cbct, lateral

def for_user_total_patient_count(user):
    profile = Profile.objects.get(user=user)
    patient_count = Patient.objects.filter(user=profile).count()
    return patient_count

def for_user_total_uploaded_radiography(user):
    profile = Profile.objects.get(user=user)
    radiography_count = Image.objects.filter(user=profile).count()
    return radiography_count

def for_user_total_anaylse_count(user):
    profile = Profile.objects.get(user=user)
    analyse_count = ImageReport.objects.filter(user=profile).count()
    return analyse_count

def for_user_radiography_type_counts_with_date(start_date=None,end_date=None,period=None):
    if period:
        start_time = time.time()
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        radiography_types = Image.objects.filter(created_date__range=(start_point,today)).values('type__name').annotate(count=Count('type'))
        try:
            lateral = radiography_types.get(type__name="Lateral Cephalometric")['count']
        except ObjectDoesNotExist:
            lateral = 0
        try:
            panaromic = radiography_types.get(type__name="Panaromic")['count']
        except ObjectDoesNotExist:
            panaromic = 0
        try:
            bitewing = radiography_types.get(type__name="Bitewing")['count']
        except ObjectDoesNotExist:
            bitewing = 0
        try:
            cbct = radiography_types.get(type__name="CBCT")['count']
        except ObjectDoesNotExist:
            cbct = 0
        try:
            periapical = radiography_types.get(type__name="Periapical")['count']
        except ObjectDoesNotExist:
            periapical = 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        return panaromic, bitewing, periapical, cbct, lateral
    else:
        start_time = time.time()
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        radiography_types = Image.objects.filter(created_date__range=(start_date,end_date)).values('type__name').annotate(count=Count('type'))
        try:
            lateral = radiography_types.get(type__name="Lateral Cephalometric")['count']
        except ObjectDoesNotExist:
            lateral = 0
        try:
            panaromic = radiography_types.get(type__name="Panaromic")['count']
        except ObjectDoesNotExist:
            panaromic = 0
        try:
            bitewing = radiography_types.get(type__name="Bitewing")['count']
        except ObjectDoesNotExist:
            bitewing = 0
        try:
            cbct = radiography_types.get(type__name="CBCT")['count']
        except ObjectDoesNotExist:
            cbct = 0
        try:
            periapical = radiography_types.get(type__name="Periapical")['count']
        except ObjectDoesNotExist:
            periapical = 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        return panaromic, bitewing, periapical, cbct, lateral


def for_user_total_patient_count_with_date(start_date=None,end_date=None,period=None):
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        patient_count = Patient.objects.filter(created_date__range=(start_point, today)).count()
        return patient_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        patient_count = Patient.objects.filter(created_date__range=(start_date, end_date)).count()
        return patient_count

def for_user_total_analyse_count_with_date(start_date=None,end_date=None,period=None):
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        analyse_count = ImageReport.objects.filter(created_date__range=(start_point, today)).count()
        return analyse_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        analyse_count = ImageReport.objects.filter(created_date__range=(start_date, end_date)).count()
        return analyse_count

def for_user_total_user_count_with_date(start_date=None,end_date=None,period=None):
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        user_count = User.objects.filter(date_joined__range=(start_point,today)).count(),
        return user_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        user_count = User.objects.filter(date_joined__range=(start_date,end_date)).count(),
        return user_count


def for_user_total_uploaded_radiography_with_date(start_date=None,end_date=None,period=None):   
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        radiography_count = Image.objects.filter(created_date__range=(start_point,today)).count(),
        return radiography_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        radiography_count = Image.objects.filter(created_date__range=(start_date,end_date)).count(),
        return radiography_count

def for_user_analyses_by_months(user):
    profile = Profile.objects.get(user=user)
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    analyses = (
        ImageReport.objects
        .filter(user=profile,created_date__range=(start_date, end_date))
        .annotate(month=TruncMonth('created_date'))
        .values('month')
        .annotate(report_count=Count('id'))
        .order_by('month')
    )
    result_dict = {}
    for analysis in analyses:
        month = analysis['month'].strftime('%B')
        report_count = analysis['report_count']
        result_dict[month] = report_count
    return result_dict

def set_user_login_logout(user,status):
    print("status",status)
    if status == "login":
        have_last_logout = SpecificUserLoginDiary.objects.filter(user=user).last()
        if have_last_logout and not have_last_logout.logout_date:
            print("saving logout", have_last_logout, have_last_logout.id)
            have_last_logout.logout_date = timezone.now()
            have_last_logout.save()
            # SpecificUserLoginDiary.objects.create(
            #     user=user,
            #     login_date = timezone.now(),
            # )
        else:
            print("saving login")
            SpecificUserLoginDiary.objects.create(
                user=user,
                login_date = timezone.now(),
            )
    else:
        last_login_obj = SpecificUserLoginDiary.objects.filter(user=user).last()
        print("last login obj", last_login_obj, last_login_obj.id)
        if last_login_obj:
            last_login_obj.logout_date = timezone.now()
            last_login_obj.save()
    return True

def send_email_to_management(subject, message):
    mail_list = ["batuhanaltog88@gmail.com"] #,"ozercelik05@gmail.com"
    # mail_list =["ynsemrerkss@gmail.com"]
    try:
        mail_server = "mail.craniocatch.com"
        mail_username = 'teknik@craniocatch.com'
        mail_password = ".=4-CzHB6yvtM20="
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = mail_username
        msg["To"] = ", ".join(mail_list)
        server = smtplib.SMTP(mail_server, 587) #587 #465
        server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        print("Information mail sent.")
    except Exception as exc:
        print(f"Informatin mail could not be sent. Message: {exc}")

def error_handler_function(user,error,ignore=None):
    if user:
        error_log = ErrorLog.objects.create(
            # exception_type = exception_type,
            # request = request,
            traceback_info=error,
            # view_function=view_function,
            user=user,
        )
        subject = "CranioCatch Clinic - Bir Hata Oluştu"
        message = f"Hata Detayı:\nHata alan kullanıcı: {user.email}\nHata bilgisi: {error}"
        print("***** MAIL GONDERILIYOR *****" , " --- Başlık", subject , "--- KONU", message )
        if not ignore:
            send_email_to_management(subject, message)
        return True
    else:
        error_log = ErrorLog.objects.create(
            traceback_info=error,
        )
        subject = "CranioCatch Clinic - Bir Hata Oluştu"
        message = f"Hata Detayı:\nEmbeded fonksiyonun hata meydana geldi\nHata bilgisi: {error}"
        print("***** MAIL GONDERILIYOR *****" , " --- Başlık", subject , "--- KONU", message )
        if not ignore:
            send_email_to_management(subject, message)
        return True


def send_email_for_password(to,subject, body):
    try:
        mail_server = "mail.craniocatch.com"
        mail_username = 'teknik@craniocatch.com'
        mail_password = ".=4-CzHB6yvtM20="
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = mail_username
        message['To'] = to
        server = smtplib.SMTP(mail_server, 587)
        server.login(mail_username, mail_password)
        server.send_message(message)
        server.quit()
        print("Information mail sent.")
    except Exception as exc:
        print(f"Informatin mail could not be sent. Message: {exc}")


def send_email(to,subject, body, qr_for_report=None):
    try:
        mail_server = "mail.craniocatch.com"
        mail_username = 'report@craniocatch.com'
        mail_password = "9U:O4mE-t3@M5lq:"
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = mail_username
        message['To'] = to

        if qr_for_report:
            message.add_alternative(f"""\
                <html>
                    <body>
                        <p>{body}</p>
                        <img src="cid:qr_code">
                    </body>
                </html>
                """, subtype='html')

            # QR kodu resmini e-posta içeriğine ekleyin
            with open(qr_for_report, 'rb') as f:
                qr_code_data = f.read()
                qr_code_cid = 'qr_code'
                message.get_payload()[1].add_related(
                    qr_code_data, 'image', 'png', cid=qr_code_cid
                )

        server = smtplib.SMTP(mail_server, 587)
        server.login(mail_username, mail_password)
        server.send_message(message)
        server.quit()
        print("Information mail sent.")
    except Exception as exc:
        print(f"Informatin mail could not be sent. Message: {exc}")


def get_user_informations(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    platform = None
    browser = None
    if user_agent:
        if 'Windows' in user_agent:
            platform = 'Windows'
        elif 'Mac' in user_agent:
            platform = 'Mac'
        elif 'Linux' in user_agent:
            platform = 'Linux'
        else:
            platform = 'Undefined'

        if 'Firefox' in user_agent:
            browser = 'Firefox'
        elif 'Chrome' in user_agent:
            browser = 'Chrome'
        elif 'Safari' in user_agent:
            browser = 'Safari'
        elif 'OPR' in user_agent:
            browser = 'Opera'
        else:
            browser = 'Undefined'
    my_datetime = datetime.now()
    timezone = pytz.timezone('Europe/Istanbul')
    my_datetime_with_timezone = timezone.localize(my_datetime)
    data = {
        "ip_address": ip_address,
        "platform": platform,
        "browser": browser,
        "date": my_datetime_with_timezone,
    }
    return data


def save_user_informations(request, ip_address=None, status_or_url=None, username=None):
    informations = get_user_informations(request)
    UserInformations.objects.create(username=username,
                                    ip_address=ip_address,
                                    platform=informations["platform"],
                                    browser=informations["browser"],
                                    process_date=informations["date"],
                                    log_page=status_or_url)
    return JsonResponse({"status": True})


def user_theme_choices(user):
    user_theme = UserTheme.objects.get(user=user)
    print("lang 2",user_theme.language)
    user_theme_dict = {
        "language": user_theme.language,
        "color": user_theme.color,
        "page_length": user_theme.page_length,
        "view_type": user_theme.card_view_type,
        "arabic": user_theme.arabic
    }
    return user_theme_dict


def send_sms(gsm, message, msgheader):
    response = requests.post('https://api.netgsm.com.tr/sms/send/get',
                             params={'usercode': '2226060723', 'password': '8281$61', 'gsmno': gsm, 'message': message,
                                     'msgheader': msgheader})
    print(response.status_code, response, response.text, gsm, message, msgheader)


def get_package_usages(profile):
    usage_package_with_profile = UsagePackageWithProfile.objects.filter(profile=profile,
                                                                        is_valid=True).order_by("-id").first()
    package_created_date = usage_package_with_profile.created_date

    today = timezone.now()
    month_list = []
    limits = {}
    current_month = package_created_date
    usage_pack = usage_package_with_profile.usage_pack
    month_list.append(current_month)
    for i in range(1, 13):
        current_month += relativedelta(months=1)
        month_list.append(current_month)
    print("month_list", month_list)
    for a in range(1, 13):
        if month_list[a - 1] < today < month_list[a]:
            patient_len_for_limit = len(Patient.objects.filter(user=profile, created_date__gte=month_list[a - 1]))
            images_len_for_limit = len(Image.objects.filter(user=profile, created_date__gte=month_list[a - 1]))
            image_reports_for_limit = len(ImageReport.objects.filter(user=profile, created_date__gte=month_list[a - 1]))
            limits["patient"] = {"patient_count": patient_len_for_limit, "percentage": int(patient_len_for_limit / usage_package_with_profile.usage_pack.patient_limit *100), "patient_limit": usage_package_with_profile.usage_pack.patient_limit if usage_pack.patient_limit < 99999 else 'Limitsiz'}
            limits["image"] = {"image_count": images_len_for_limit, "percentage": int(images_len_for_limit / usage_package_with_profile.usage_pack.image_limit *100), "image_limit": usage_package_with_profile.usage_pack.image_limit if usage_pack.image_limit < 99999 else 'Limitsiz'}
            limits["analyse"] = {"analyse_count": image_reports_for_limit, "percentage": int(image_reports_for_limit / usage_package_with_profile.usage_pack.analysis_limit *100), "analyse_limit": usage_package_with_profile.usage_pack.analysis_limit if usage_pack.analysis_limit < 99999 else 'Limitsiz'}
    print("limits", limits)
    return limits


def subscription(user, usage_pack, usage_pack_buyed_date):
    limit_dict_year = {"is_expired": False}
    package_starts_date = usage_pack_buyed_date
    today = timezone.now()
    month_list = []
    current_month = package_starts_date
    month_list.append(current_month)
    image_report_list = []

    for i in range(1, 13):
        current_month += relativedelta(months=1)
        month_list.append(current_month)

    for a in range(1, 13):
        if month_list[a - 1] < today < month_list[a]:
            patient_len_for_limit = Patient.objects.filter(user__user=user, created_date__gte=month_list[a - 1]).count()
            images_len = Image.objects.filter(user__user=user, created_date__gte=month_list[a - 1]).count()
            image_reports = ImageReport.objects.filter(user__user=user, created_date__gte=month_list[a - 1])
            image_report_list.extend(image_reports)
            print("user analyse count",len(image_report_list))
            print("user analyse limit",usage_pack.analysis_limit)

            limit_dict_year["analyse_limit"] = True if len(image_report_list) >= usage_pack.analysis_limit else False

            limit_dict_year["patient_limit"] = True if patient_len_for_limit >= usage_pack.patient_limit else False

            limit_dict_year["image_limit"] = True if images_len >= usage_pack.image_limit else False
            

            return limit_dict_year


def over_limit_check(user):

    usage_pack_with_profile = UsagePackageWithProfile.objects.filter(profile__user=user, is_valid=True).order_by(
        "-id").first()

    usage_pack_is_yearly = usage_pack_with_profile.usage_pack.is_yearly
    usage_pack_buyed_date = usage_pack_with_profile.created_date
    usage_pack_ends_date_year = usage_pack_buyed_date + relativedelta(years=1)
    usage_pack_ends_date_month = usage_pack_buyed_date + relativedelta(months=1)
    usage_pack = usage_pack_with_profile.usage_pack

    today = timezone.now()

    def monthly_control():
        limit_dict = {}
        if today <= usage_pack_ends_date_month:  # yıllık paketin tarihi geçmemişse
            limit_dict = subscription(user, usage_pack, usage_pack_buyed_date)
        else:  # yıllık paketin tarihi geçmişse
            limit_dict["is_expired"] = True
            print("Yıllık paket süresi doldu")
        # limit_dict = {}
        # if today <= usage_pack_ends_date_month:
        #     image_reports = ImageReport.objects.filter(user__user=user, created_date__gte=usage_pack_buyed_date)
        #     patient_len_for_limit = Patient.objects.filter(user__user=user,
        #                                                    created_date__gte=usage_pack_buyed_date).count()
        #     images_len = Image.objects.filter(user__user=user, created_date__gte=usage_pack_buyed_date).count()
        #     limit_dict["analysis_limit"] = True if len(image_reports) >= usage_pack.analysis_limit else False
        #
        #     limit_dict["patient_limit"] = True if patient_len_for_limit >= usage_pack.patient_limit else False
        #
        #     limit_dict["image_report_limit"] = True if images_len >= usage_pack.image_limit else False
        #
        #     limit_dict["is_expired"] = False
        #
        # else:
        #     limit_dict["is_expired"] = True

        return limit_dict

    def yearly_control():
        limit_dict = {}
        if today <= usage_pack_ends_date_year:  # yıllık paketin tarihi geçmemişse
            limit_dict = subscription(user, usage_pack, usage_pack_buyed_date)
        else:  # yıllık paketin tarihi geçmişse
            limit_dict["is_expired"] = True
            print("Yıllık paket süresi doldu")
        return limit_dict

    if usage_pack_is_yearly: # paket yıllıksa
        limit_dict = yearly_control()
    else:
        limit_dict = monthly_control()

    return limit_dict


def draw_function(path=None, image_report_id=None, selected_labels=None, embeded=False, teethNumbering=False, implant_crown_draw=False, draw_values=None):
    filepath = path.name
    name, extension = os.path.splitext(filepath)
    output_path = ccclinic_path_with_slash + name + "_drawed" + extension

    # Görüntüyü yükleyin
    image = cv2.imread(ccclinic_path_with_slash + filepath)

    image_report_obj = ImageReport.objects.get(id=image_report_id)
    loaded_result_json = json.loads(image_report_obj.result_json)
    palate_results = loaded_result_json["palate_results"]
    illness_pool = loaded_result_json["illness_pool"]
    measurement_results = loaded_result_json["measurement_results"] if "measurement_results" in loaded_result_json.keys() else None
    cache_active_models = active_model_labels_function()
    patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
    active_model_labels_dict = cache_active_models[image_report_obj.name][patient_type]

    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#')  # '#' karakterini kaldırın (varsa)
        color = tuple(int(hex_code[rgb:rgb + 2], 16) for rgb in (0, 2, 4))
        color = color[::-1]
        return color
    # Çizimleri görüntü üzerine işleyin
    for result in palate_results:
        if selected_labels and result["name"] not in selected_labels:
            continue
        label = active_model_labels_dict.get(result["name"], None)
        if not label: continue
        coordinates = np.array(result['coordinates'])
        rgb = hex_to_rgb(label["color"])
        if image_report_obj.image.type.id in [2, 4]:
            height, width, channels = image.shape
            # Koordinatları orijinal boyuttan 512x512 boyutuna dönüştürün
            # coordinates = coordinates * (width / 512, height / 512)

        overlay = image.copy()
        cv2.fillPoly(image, [coordinates.astype(int)], color=rgb)
        alpha = 0.7  # Yarı saydamlık (0.0 - 1.0 arasında değer)
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
        cv2.polylines(image, [coordinates.astype(int)], isClosed=True, color=rgb, thickness=2)

    for result in illness_pool:
        if selected_labels and result["name"] not in selected_labels:
            continue
        if result["name"] == "Root-Canal Filling":
            continue
        label = active_model_labels_dict[result["name"]] 
        coordinates = np.array(result['coordinates'])
        rgb = hex_to_rgb(label["color"])
        if image_report_obj.image.type.id == 2:
            height, width, channels = image.shape
            # Koordinatları orijinal boyuttan 512x512 boyutuna dönüştürün
            # coordinates = coordinates * (width / 512, height / 512)

        if image_report_obj.image.type.id == 4:
            height, width, channels = image.shape
            # Koordinatları orijinal boyuttan 512x512 boyutuna dönüştürün
            # coordinates = coordinates * (width / 512, height / 512)
        try:
            overlay = image.copy()
            cv2.fillPoly(image, [coordinates.astype(int)], color=rgb)
            alpha = 0.7  # Yarı saydamlık (0.0 - 1.0 arasında değer)
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
            cv2.polylines(image, [coordinates.astype(int)], isClosed=True, color=rgb, thickness=2)
        except:
            print("HATA: ", result, "604drawfunction74892 Hata Kodunu aratin")

    def draw_measurements(measurement_results):
        for measurement_dict in measurement_results:
            model = measurement_dict["name"]
            result = measurement_dict["points"]

            for tooth, sides in result.items():
                for side in sides.keys():
                    coords = sides[side]['points']
                    if image_report_obj.image.type.id == 2:
                        height, width, channels = image.shape
                        first_point = coords[0]
                        second_point = coords[1]
                        first_point[0] = int(first_point[0] * width / 512)
                        first_point[1] = int(first_point[1] * height / 512)
                        second_point[0] = int(second_point[0] * width / 512)
                        second_point[1] = int(second_point[1] * height / 512)
                        coords = [first_point, second_point]
                        # Koordinatları orijinal boyuttan 512x512 boyutuna dönüştürün
                    cv2.circle(image, (coords[0][0], coords[0][1]), 3, (0, 255, 0), -1, cv2.LINE_AA)
                    cv2.circle(image, (coords[1][0], coords[1][1]), 3, (0, 255, 0), -1, cv2.LINE_AA)
                    cv2.line(image, (coords[0][0], coords[0][1]), (coords[1][0], coords[1][1]), (255, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(sides[side]['measure'])[:4] + 'mm', (coords[0][0], coords[0][1]), cv2.FONT_HERSHEY_SIMPLEX,
                                      0.4, (0, 0, 255), 1, cv2.LINE_AA)
        
    def draw_teeth_numbering():
        report_tooths = ReportTooth.objects.filter(image_report=image_report_obj)
        def for_top_of_tooths(number):
            cv2.circle(image, (xcoord, ycoord), 10, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(image, (xcoord, ycoord), 20, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.line(image, (xcoord, ycoord-20), (xcoord, ycoord-230), (255, 255, 255), 1, cv2.LINE_AA) 
            cv2.rectangle(image, (xcoord-30, ycoord-290), (xcoord+30, ycoord-230), (255, 255, 255), 1, cv2.LINE_AA)

            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # Using cv2.putText() method
            cv2.putText(image, str(number), (xcoord-22,ycoord-249), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        
        def for_bottom_of_tooths(number):
            cv2.circle(image, (xcoord, ycoord), 10, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(image, (xcoord, ycoord), 20, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.line(image, (xcoord, ycoord+20), (xcoord, ycoord+230), (255, 255, 255), 1, cv2.LINE_AA) 
            cv2.rectangle(image, (xcoord-30, ycoord+290), (xcoord+30, ycoord+230), (255, 255, 255), 1, cv2.LINE_AA)

            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # Using cv2.putText() method
            cv2.putText(image, str(number), (xcoord-20,ycoord+270), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        for report_tooth in report_tooths:
            tooth_coordinates = json.loads(report_tooth.coordinates.replace("'", '"'))
            tooth_number = report_tooth.number_prediction
            xmin = tooth_coordinates["xmin"]
            ymin = tooth_coordinates["ymin"]
            xmax = tooth_coordinates["xmax"]
            ymax = tooth_coordinates["ymax"]
            xcoord = int((xmin+xmax) / 2)
            ycoord = int((ymin+ymax) / 2)
            if image_report_obj.image.type.id in [2, 4]:
                height, width, channels = image.shape
                # Koordinatları orijinal boyuttan 512x512 boyutuna dönüştürün
                xcoord = int(xcoord * (width / 512))
                ycoord = int(ycoord * (height / 512))
                
            if str(tooth_number)[0] in ["1", "2"]:
                for_top_of_tooths(tooth_number)

            if str(tooth_number)[0] in ["3", "4"]:
                for_bottom_of_tooths(tooth_number)

    if measurement_results:
        draw_measurements(measurement_results)

    if teethNumbering:
        draw_teeth_numbering()

    # Sonucu kaydedin
    cv2.imwrite(output_path, image)
    return output_path


def draw_implant_and_crown(implant_crown_draw,path,image_report_id,embeded=False):
    print("drawqqq", )
    filepath = path.name
    name, extension = os.path.splitext(filepath)
    output_path = ccclinic_path_with_slash + name + "_crown_implant_drawed" + extension

    image_report_obj = ImageReport.objects.get(id=image_report_id)
    # Görüntüyü yükleyin
    image = cv2.imread(ccclinic_path_with_slash + filepath)
    for draw_obj in implant_crown_draw:
        if draw_obj.item_type == "implant":
            png_resmi_path = os.path.join(settings.BASE_DIR, "static", "img", "teeth", "tooth_implant_dental_36_1.png")
            png_resmi = cv2.imread(png_resmi_path, cv2.IMREAD_UNCHANGED)
            print("implant")
        elif draw_obj.item_type == "crown":
            png_resmi_path = os.path.join(settings.BASE_DIR, "static", "img", "crown-teeth", f"crown-{draw_obj.icon_id}.png")
            print("png path",png_resmi_path)
            png_resmi = cv2.imread(png_resmi_path, cv2.IMREAD_UNCHANGED)
            print("crown")
        # Koordinatları belirleyin (örneğin, 500, 500)
        if image_report_obj.image.type.id in [2, 4]:
            height, width, channels = image.shape
            coordinates = literal_eval(draw_obj.coordinate)
            coordinates = np.array(coordinates)
            coordinates = coordinates * (width / 512, height / 512)
        else:
            coordinates = json.loads(draw_obj.coordinate)
        x_koordinati = int(coordinates[0])
        y_koordinati = int(coordinates[1])

        print("xcord", x_koordinati)
        print("ycord", y_koordinati)
        # PNG resmini okuyun

        # dim = (int(json.loads(draw_obj.dimension)/json.loads(draw_obj.original_shape)), int(json.loads(draw_obj.dimension)/json.loads(draw_obj.original_shape)))
        dim = (int(json.loads(draw_obj.dimension)), int(json.loads(draw_obj.dimension)))
        print("dim", dim)
        # resize image
        png_resmi = cv2.resize(png_resmi, dim, interpolation = cv2.INTER_AREA)
        temporary_slug = f"{str(uuid.uuid4()).replace('-', '')}.png"
        png_temporary_path = os.path.join(settings.BASE_DIR, "media", "temporary_png", temporary_slug)
        cv2.imwrite(png_temporary_path, png_resmi)
        im1 = pil_Image.open(png_temporary_path)
        # rotating a image 90 deg counter clockwise
        derece = -draw_obj.rotate # sağa döndürmek için -, sola döndürmek için +
        png_resmi = im1.rotate(derece, pil_Image.BILINEAR, expand = 1)
        png_resmi.save(png_temporary_path)
        png_resmi = cv2.imread(png_temporary_path, cv2.IMREAD_UNCHANGED)
        # Döndürme açısını belirleyin (örneğin, 40 derece)

        # PNG resminin boyutlarını alın
        yükseklik, genişlik = png_resmi.shape[:2]
        merkez = (genişlik // 2, yükseklik // 2)

        y_koordinati = y_koordinati - merkez[1]
        x_koordinati = x_koordinati - merkez[0]
        print("yyy", y_koordinati)
        print("xxx", x_koordinati)
        # Döndürülen PNG görüntüsünü radyografi üzerine yerleştirin
        for y in range(yükseklik):
            for x in range(genişlik):
                alpha = png_resmi[y, x, 3] / 255.0
                image[y_koordinati + y, x_koordinati + x, 0] = (1.0 - alpha) * image[y_koordinati + y, x_koordinati + x, 0] + alpha * png_resmi[y, x, 0]
                image[y_koordinati + y, x_koordinati + x, 1] = (1.0 - alpha) * image[y_koordinati + y, x_koordinati + x, 1] + alpha * png_resmi[y, x, 1]
                image[y_koordinati + y, x_koordinati + x, 2] = (1.0 - alpha) * image[y_koordinati + y, x_koordinati + x, 2] + alpha * png_resmi[y, x, 2]
    cv2.imwrite(output_path, image)
    print("output path",output_path)
    return output_path

def cephalometric_analyses(cephalometric_landmarks, measure, first_coord, second_coord):
    analyse.calibration_points = [first_coord, second_coord]
    analyse.calibration_measure = measure
    analyse.set_calculate_calibration_measure()
    analyse.analysis_points = {content["label"]: content["coordinates"][0] for content in cephalometric_landmarks}
    analyse.angle_results()
    analyse.measurement_results()
    analyse.ratio_results()
    result = analyse.get_result_as_json()
    return result
