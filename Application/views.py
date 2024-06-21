import os.path
import traceback
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from Application.functions import *
from Application.models import *
from User.models import *
from datetime import datetime, timedelta, date
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
import uuid
from Server.settings import ccclinic_path, ccclinic_path_with_slash, lateral_cephalometric_dict, clinic_project_id, patient_form_link, add_patient_form_site_link
import time
from django.contrib import messages
from collections import defaultdict
from Application.cache_processes import active_model_labels_function
from User.token_operations import remaining_token
from User.token_operationsv2 import remaining_token as cranio_remaining_token
import logging
from django.shortcuts import redirect
from django.db.models import Q
logger = logging.getLogger('main')

def get_specs():
    spec = SpecificParameter.objects.get(id=clinic_project_id)
    specs = {
        "login_page_logo": spec.loginpage_logo_design.url.replace("static/", "") if spec.loginpage_logo_design else None,
        "logo": spec.base_html_left_top_logo.url.replace("static/", ""), 
        "title": spec.page_title, 
        "banner": spec.loginpage_banner.url.replace("static/", "") if spec.loginpage_banner else None,
        "language_visibility": spec.language_visibility, 
        "brand": spec.base_html_left_bottom_title, 
        "theme_css": spec.base_html_css.url.replace("static/", "") if spec.base_html_css else None,
        "report_page_title_banner": spec.report_page_title_banner.url.replace("static/", ""),
        "favicon": spec.favicon.url.replace("static/", "") if spec.favicon else None,
        "clarification_text": spec.clarification_text.url.replace("static/", "") if spec.clarification_text else None,
        "privacy_policy": spec.privacy_policy.url.replace("static/", "") if spec.privacy_policy else None,
        "cookie_policy": spec.cookie_policy.url.replace("static/", "") if spec.cookie_policy else None,
        "terms_conditions_policy": spec.terms_conditions_policy.url.replace("static/", "") if spec.terms_conditions_policy else None,
        "login_page_content": spec.login_page_content if spec.login_page_content else None,
        "website_link": spec.website_link if spec.website_link else None,
        "website_name": spec.website_name if spec.website_name else None,
        }
    return specs

# Create your views here.
def login_page(request):
    print("request.user", str(request.user), type(str(request.user)))
    specs = get_specs()
    if not str(request.user) == "AnonymousUser":
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'login.html', context={"specs": specs})


@csrf_exempt
def login_page_validator(request):
    try:
        email = request.POST.get('emailInput')
        print("email",email)
        password = request.POST.get('passwordInput')
        key = request.POST.get('key')
        user = User.objects.filter(email=email).first()
        print("user",user)
        if not user:
            message = _("No user found for this email")
            return JsonResponse({'status': False, 'message':message})
        user = authenticate(username=user.username, password=password)
        if not user:
            message = _("Wrong username or password!")
            return JsonResponse({
                "status": False,
                #"message_tr": "Hatalı kullanıcı adı veya şifre",
                "message": message
                })
        username = user.username
        portalCheckbox = request.POST.get('terms')
        ip_address = request.META.get('REMOTE_ADDR')
        if not key:
            key = ip_address
        # pageLanguage = request.POST.get('pageLanguage')
        if user:
            if portalCheckbox == 'true':
                approved_portal_term_obj, created = ApprovedPortalTermsOfUse.objects.get_or_create(user=user)
                if created:
                    approved_portal_term_obj.date = datetime.now()
                else:
                    approved_portal_term_obj.date = datetime.now()
                login(request, user)
                user_lang = UserTheme.objects.get(user=user).language
                status = "LoginPage-Başarılı Giriş"
                save_user_informations(request, ip_address=key, status_or_url=status, username=user.username)
                message = _("Successfully logged in!")
                try:
                    set_user_login_logout(user,status="login")
                except Exception as e:
                    logger.info(f"Error occurred while trying to save login info to model: {e}")
                return JsonResponse({"status": True, "message": message, "language": user_lang})
            else:
                status = "LoginPage-Portal False"
                save_user_informations(request, ip_address=key, status_or_url=status, username=username)
                message = _("Accept the Terms of Use!")
                return JsonResponse({"status": False,
                                        #"message_tr": "Portal Kullanım Şartını Onaylayınız!",
                                        "message": message
                                        })
        else:
            status = "LoginPage-Hatalı Kullanıcı adı Şifre"
            save_user_informations(request, ip_address=key, status_or_url=status, username=username)
            message = _("Wrong username or password!")
            return JsonResponse({
                "status": False,
                #"message_tr": "Hatalı kullanıcı adı veya şifre",
                "message": message
                })
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def get_matched_questions(form_data):
    questions = get_questions_with_json()
    matched_questions = {}

    for key, value in form_data.items():
        if key != 'csrfmiddlewaretoken' and key != 'slug':
            question = questions.filter(slug=key).first()
            if question:
                if question.question in ['Patient Full Name', 'What is your gender?', 'E-Mail', 'Phone']:
                    matched_questions[question.question] = {
                        'question': question.question,
                        'value': value
                    }
                    if question.answers:
                        answers_dict = json.loads(question.answers)
                        for ans_key, ans_value in answers_dict.items():
                            if ans_key == value:
                                matched_questions[question.question]['answer_value'] = ans_value
                                break
    print("matcheds",matched_questions)
    return matched_questions


@login_required
def add_patient_page_from_form_prepare(request):
    try:
        user = request.user
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        user_theme_dict = user_theme_choices(user)
        specs = get_specs()
        if request.method == "POST":
            form_data = json.loads(request.body.decode('utf-8'))
            if form_data:
                profile = Profile.objects.get(user=user)

                datas = get_matched_questions(form_data)
                if "Patient Full Name" in datas.keys():
                    name = datas["Patient Full Name"]["value"]
                else:
                    name = ""
                if "E-Mail" in datas.keys():
                    email = datas["E-Mail"]["value"]
                else:
                    email = ""
                if "Phone" in datas.keys():
                    phone = datas["Phone"]["value"]
                else:
                    phone = ""
                if "What is your gender?" in datas.keys():
                    gender = datas["What is your gender?"]["answer_value"]
                else:
                    gender = ""

                profile = Profile.objects.get(user=user)
                last_patient = Patient.objects.filter(user=profile, archived=False).order_by('-id').first()
                if last_patient:
                    last_patient_id = last_patient.patient_id if last_patient.patient_id else 0
                else:
                    last_patient_id = 0
                new_patient_id = last_patient_id + 1
                context = {
                'patient_full_name': name,
                'gender': gender,
                'email': email,
                'phone': phone,
                'doc_name': profile.user.first_name + " " + profile.user.last_name,
                'new_patient_id': new_patient_id,
                'card_message': "Create Patient",
                'button_message': "Create",
                "user_theme_choices_json": json.dumps(user_theme_dict),
                "user_theme_choices": user_theme_dict,
                'redirect_url': f"{add_patient_form_site_link}/add-patient-form/" if lang == "tr" else f"{add_patient_form_site_link}/en/add-patient-form/"
            }
            return JsonResponse({"redirect_url": f"{add_patient_form_site_link}/add-patient-form/" if lang == "tr" else f"{add_patient_form_site_link}/en/add-patient-form/",
                                'patient_full_name': name,
                                'gender': gender,
                                'email': email,
                                'phone': phone,
                                'doc_name': profile.user.first_name + " " + profile.user.last_name,
                                'new_patient_id': new_patient_id,
            })
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def add_patient_form(request):
    try:
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        user = request.user
        time.sleep(0.4)
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        profile = Profile.objects.get(user=user)
        question_slugs = ['e3232c195e09412bab7e3344560e9e63','7d6e300e300443bf85006fe4e67659ad','48c104b2f3ea46caa58fa9b613eb7200','d8c41dfa5e5d4cc3b524570f45691fca']
        slug = request.GET.get("slug")
        form_answer_objects = FormAnswers.objects.filter(group_slug=slug, question_slug__in=question_slugs)

        if form_answer_objects.filter(question_slug='e3232c195e09412bab7e3344560e9e63').exists():
            patient_full_name = form_answer_objects.get(question_slug='e3232c195e09412bab7e3344560e9e63').answer
            # Değer varsa işlemleri yap
            print("patient_full_name:",patient_full_name)
        else:
            patient_full_name = ""
            print("İsim yanıtı bulunamadı.")

        if form_answer_objects.filter(question_slug='7d6e300e300443bf85006fe4e67659ad').exists():
            email = form_answer_objects.get(question_slug='7d6e300e300443bf85006fe4e67659ad').answer
            # Değer varsa işlemleri yap
            print("email:",email)
        else:
            # Değer yoksa işlemleri yap
            email = ""
            print("email yanıtı bulunamadı.")

        if form_answer_objects.filter(question_slug='48c104b2f3ea46caa58fa9b613eb7200').exists():
            phone = form_answer_objects.get(question_slug='48c104b2f3ea46caa58fa9b613eb7200').answer
            # Değer varsa işlemleri yap
            print("phone:",phone)
        else:
            # Değer yoksa işlemleri yap
            phone = ""
            print("phone yanıtı bulunamadı.")
        gender = ""
        if form_answer_objects.filter(question_slug='d8c41dfa5e5d4cc3b524570f45691fca').exists():
            gender = form_answer_objects.get(question_slug='d8c41dfa5e5d4cc3b524570f45691fca').answer
            questions = get_questions_with_json() #json yapısından dolayı önce form question objelerinin hepsini çekip ardından sadece cinsiyeti almak için bir filter yapıldı
            question = questions.get(slug='d8c41dfa5e5d4cc3b524570f45691fca')
            gender_answers = json.loads(question.answers)
            for key, value in gender_answers.items():
                if key == gender:
                    gender = value
                    break

        last_patient = Patient.objects.filter(user=profile, archived=False).order_by('-id').first()
        if last_patient:
            last_patient_id = last_patient.patient_id if last_patient.patient_id else 0
        else:
            last_patient_id = 0
        patient_id = last_patient_id + 1
        
        if phone != "":
            if phone.startswith('0'):
                phone = '9' + phone
            else:
                phone = '90' + phone
        else:
            phone = ""

        doc_name = profile.user.first_name + " " + profile.user.last_name
        radiography = None
        radiography_type = None
        radiography_id = request.GET.get("fradiographyid",None)
        radiography_type = request.GET.get("fradiography_type",None)
        if radiography_id and radiography_id != "":
            radiography = FormRadiographs.objects.get(id=radiography_id)
        if radiography_type and radiography_type != "undefined":
            radiography_type = ImageType.objects.get(id=radiography_type)

        context = {
            'patient_id': patient_id,
            'patient_full_name': patient_full_name,
            'gender': gender,
            'email': email,
            'phone': phone,
            'doc_name': doc_name,
            'card_message': "Add Patient",
            'button_message': "Add",
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "radiography_type":radiography_type,
            "radiography":radiography,
            "specs": specs,

        }
        return render(request,"add-patient.html", context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def add_patient_page(request,patient_slug=None):
    try:
        user = request.user
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        if patient_slug:
            patient = Patient.objects.get(slug=patient_slug)
            profile = Profile.objects.get(user=user)
            if patient.user != profile:
                messages.warning(request, "Hastanın doktoru değilsiniz.")
                return HttpResponseRedirect(reverse('patientsPage'))
            else:      
                context = {
                    'patient_slug': patient.slug,
                    'patient_id': patient.patient_id,
                    'patient_full_name': patient.full_name,
                    'gender': patient.gender,
                    'birthday': str(patient.date_of_birth),
                    'email': patient.email,
                    'phone': patient.phone,
                    'doc_name': profile.user.first_name + " " + profile.user.last_name,
                    'file_no': patient.file_no,
                    'card_message': "Update Patient",
                    'button_message': "Update",
                    "user_theme_choices_json": json.dumps(user_theme_dict),
                    "user_theme_choices": user_theme_dict,
                    "specs": specs,
                }
                return render(request,"add-patient.html", context)
        else:
            # last_patient = Patient.objects.aggregate(Max('patient_id'))['patient_id__max']
            profile = Profile.objects.get(user=user)
            last_patient = Patient.objects.filter(user=profile, archived=False).order_by('-id').first()
            if last_patient:
                last_patient_id = last_patient.patient_id if last_patient.patient_id else 0
            else:
                last_patient_id = 0
            new_patient_id = last_patient_id + 1
            profile = Profile.objects.get(user=user)
            context = {
                'doc_name': profile.user.first_name + " " + profile.user.last_name,
                'new_patient_id': new_patient_id,
                'card_message': "Add Patient",
                'button_message': "Add",
                "user_theme_choices_json": json.dumps(user_theme_dict),
                "user_theme_choices": user_theme_dict,
                "specs": specs
            }
            return render(request, "add-patient.html", context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def patients_page(request):
    try:
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        user = request.user
        specs = get_specs()
        profile = Profile.objects.get(user=user)
        company = profile.company
        patients = Patient.objects.select_related("user").filter(user__company=company, archived=False).order_by("-id")
        patients_list = []
        full_name = user.first_name + " " + user.last_name
        first_name = user.first_name
        for patient in patients:
            patient_dict = {}

            combined_query = ImageReport.objects.filter(
                Q(image__patient=patient, image__archived=False) |
                Q(dicom__patient=patient, name="CBCT")
            ).order_by('-id')

            # Sonuçları alın
            image_report_obj = combined_query.distinct()
            patient_images = Image.objects.select_related("type").filter(patient=patient, archived=False).order_by('-id')
            image_report_id = "None" if not image_report_obj else "None" if not image_report_obj.first().is_done or image_report_obj.first().is_error else image_report_obj.first().id
            patient_image_types_list = []
            for patient_image in patient_images:
                patient_image_types_list.append(patient_image.type.name if patient_image.type else "Unknown")

            patient_image_types_list = list(set(patient_image_types_list))
            patient_dict["image_types"] = patient_image_types_list
            patient_dict["image_report_id"] = image_report_id
            patient_dict["patient_id"] = patient.patient_id
            patient_dict["is_lateral"] = "True" if image_report_obj.first() and 'Lateral Cephalometric' in image_report_obj.first().name else "False"
            patient_dict["is_cbct"] = "True" if image_report_obj.first() and image_report_obj.first().cbct else "False"
            if image_report_obj and image_report_obj[0].image:
                last_image = image_report_obj[0].image
                if last_image.thumbnail_image_path:
                    patient_dict['cover_image'] = last_image.thumbnail_image_path.url
                elif last_image.type and last_image.type.name == "CBCT" and not last_image.path and not last_image.thumbnail_image_path:
                    patient_dict['cover_image'] = f"/media/dental/radio/{lang}3d.png"
                else:
                    patient_dict['cover_image'] = last_image.path.url
                patient_dict["image_id"] = last_image.id
            else:
                patient_dict['cover_image'] = "None"
            created_date_time_format = "%d/%m/%Y %H:%M"
            birth_time_format = "%d/%m/%Y"
            patient_informations_dict = {}
            patient_informations_dict["slug"] = patient.slug
            patient_informations_dict["first_name"] = patient.first_name
            patient_informations_dict["last_name"] = patient.last_name
            patient_informations_dict["date_of_birth"] = patient.date_of_birth.strftime(birth_time_format) if patient.date_of_birth else "-"
            patient_informations_dict["created_date"] = patient.created_date.strftime(created_date_time_format)
            patient_informations_dict["modified_date"] = patient.modified_date.strftime(created_date_time_format) if patient.modified_date else "-"
            patient_informations_dict["archived"] = str(patient.archived)
            patient_informations_dict["favorited"] = str(patient.favorited)
            patient_dict["patient"] = patient_informations_dict
            patients_list.append(patient_dict)
        image_type_dict = {}

        def upload_radiography_function():
            image_types = ImageType.objects.all().order_by("id")

            for image_type_obj in image_types:
                image_type_dict[image_type_obj.id] = image_type_obj.name
            # CBCT değerini en sona taşıma
            cbct_value = image_type_dict.pop(3)
            image_type_dict[3] = cbct_value
            return image_type_dict
        
        image_type_dict = upload_radiography_function()
        user_theme_dict = user_theme_choices(user)
        print("specs", specs)
        context = {
            "patients_list": patients_list if patients_list else None,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "image_type_dict": image_type_dict,
            "view_type": user_theme_dict["view_type"],
            "theme": user_theme_dict["color"],
            "lang": lang,
            "full_name":full_name,
            "first_name":first_name,
            "distributor": profile.is_distributor,
            "image_report_status": True if ImageReport.objects.filter(is_done=False, is_error=False, user=profile, image__archived=False) else False,
            "specs": specs,
        }
        return render(request, "patients.html", context=context)

    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def favourited_patients_page(request):
    try:
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        user = request.user
        specs = get_specs()
        profile = Profile.objects.get(user=user)
        company = profile.company
        patients = Patient.objects.filter(user__company=company, archived=False, favorited=True).order_by("-id")
        patients_list = []
        user_theme_obj = UserTheme.objects.get(user=user)
        page_size = 99999 if user_theme_obj.page_length == "Hepsi" else int(user_theme_obj.page_length)
        full_name = user.first_name + " " + user.last_name
        first_name = user.first_name
        for patient in patients:
            patient_dict = {}

            image_report_obj = ImageReport.objects.filter(image__patient=patient, image__archived=False).order_by('-id')

            patient_images = Image.objects.filter(patient=patient, archived=False).order_by('-id')
            image_report_id = "None" if not image_report_obj else "None" if not image_report_obj.first().is_done or image_report_obj.first().is_error else image_report_obj.first().id
            patient_image_types_list = []
            for patient_image in patient_images:
                patient_image_types_list.append(patient_image.type.name)

            patient_image_types_list = list(set(patient_image_types_list))
            patient_dict["image_types"] = patient_image_types_list
            patient_dict["image_report_id"] = image_report_id
            patient_dict["patient_id"] = patient.patient_id
            patient_dict["is_lateral"] = "True" if image_report_obj.first() and 'Lateral Cephalometric' in image_report_obj.first().name else "False"
            patient_dict["is_cbct"] = "True" if image_report_obj.first() and image_report_obj.first().cbct else "False"
            if image_report_obj:
                last_image = image_report_obj[0].image
                if last_image.thumbnail_image_path:
                    patient_dict['cover_image'] = last_image.thumbnail_image_path.url
                elif last_image.type.name == "CBCT" and not last_image.path and not last_image.thumbnail_image_path:
                    patient_dict['cover_image'] = f"/media/dental/radio/{lang}3d.png"
                else:
                    patient_dict['cover_image'] = last_image.path.url
                patient_dict["image_id"] = last_image.id
            else:
                patient_dict['cover_image'] = "None"
            created_date_time_format = "%d %B %Y %H:%M"
            birth_time_format = "%d %B %Y"
            patient_informations_dict = {}
            patient_informations_dict["slug"] = patient.slug
            patient_informations_dict["first_name"] = patient.first_name
            patient_informations_dict["last_name"] = patient.last_name
            patient_informations_dict["date_of_birth"] = patient.date_of_birth.strftime(birth_time_format) if patient.date_of_birth else "-"
            patient_informations_dict["created_date"] = patient.created_date.strftime(created_date_time_format)
            patient_informations_dict["modified_date"] = patient.modified_date.strftime(created_date_time_format) if patient.modified_date else "-"
            patient_informations_dict["archived"] = str(patient.archived)
            patient_informations_dict["favorited"] = str(patient.favorited)
            patient_dict["patient"] = patient_informations_dict
            patients_list.append(patient_dict)
        image_type_dict = {}

        def upload_radiography_function():
            image_types = ImageType.objects.all().order_by("id")

            for image_type_obj in image_types:
                image_type_dict[image_type_obj.id] = image_type_obj.name
            # CBCT değerini en sona taşıma
            cbct_value = image_type_dict.pop(3)
            image_type_dict[3] = cbct_value
            return image_type_dict
        
        image_type_dict = upload_radiography_function()
        user_theme_dict = user_theme_choices(user)
        print("specs", specs)
        context = {
            "patients_list": patients_list if patients_list else None,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "image_type_dict": image_type_dict,
            "view_type": user_theme_dict["view_type"],
            "theme": user_theme_dict["color"],
            "lang": lang,
            "full_name":full_name,
            "first_name":first_name,
            "image_report_status": True if ImageReport.objects.filter(is_done=False, is_error=False, user=profile, image__archived=False) else False,
            "specs": specs,
        }
        return render(request, "patients.html", context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def prepare_treatments(image_report_obj=None, illness_list=None):
    treatment_for_tooth_objects = TreatmentRecommendationForTooth.objects.filter(image_report=image_report_obj)
    treatment_recommendation_dict = {}
    merged_recommendations = {}  # Tedavi yöntemleri aynı olan diş numaralarını birleştirmek için kullanılacak sözlük
    
    if illness_list: # eğer istek olarak gelmişse ve hastalık listesi varsa
        treatment_method_objs = IllnessTreatmentMethod.objects.all()
        treatments = {treatment_method_obj.treatment_method.all(): [illness_label.name for illness_label in treatment_method_obj.label.all()] for treatment_method_obj in treatment_method_objs} #treatment method ve hastalık(illnesss_label) bazında bir sözlük oluşturdum
        copyed_treatments = dict(treatments) # aynı dict ten bir şey silmeye çalıştığımda sözlüğün boyutu değiştiği için hata veriyor o yüzden kopyaladım
        for treatment_methods, illnesses in copyed_treatments.items():
            is_subset = set(illnesses).issubset(set(illness_list)) #set ile liste oluşturdum daha sonra issubset ile alt kümesi mi diye kontrol ettim evetse True dönüyor
            if not is_subset: # alt kümesi olmayanları sözlükten sildirdim çünkü aşağıdaki döngüde eğer bu listenin içerisindeyse tedavileri oluşturacağım
                del treatments[treatment_methods]
        treatment_method_ids = [[method_obj.id for method_obj in method_objs_list] for method_objs_list, _ in treatments.items()] #treatments medhodların idlerini liste eşlemesi için alıyorum

    for treatment_for_tooth in treatment_for_tooth_objects:
        tooth_number = treatment_for_tooth.tooth.number_prediction
        recommendation_methods = treatment_for_tooth.recommendation.all()
        recommendation_method_ids = [method_obj.id for method_obj in recommendation_methods] # aynı şekilde treatment_medhod_ids ile aynı olduklarından bunları da alıp aynı mı diye kontrol ediyorum

        if illness_list:
            for treatment_method_id_list in treatment_method_ids:
                status = False
                if set(recommendation_method_ids) == set(treatment_method_id_list): # eşit mi kontrolü
                    status = True
                    break
            if not status: continue
        treatment_methods = set()  # Tedavi yöntemlerini bir küme olarak tutmak için set kullanıyoruz
        
        for method in recommendation_methods:
            en_treatment_method = method.en_treatment_method
            treatment_methods.add((en_treatment_method))  # Küme içerisine tedavi yöntemlerini ekliyoruz
        
        treatment_methods_tuple = tuple(treatment_methods)  # Tedavi yöntemlerini tuple olarak saklıyoruz
        
        if treatment_methods_tuple in merged_recommendations:
            merged_recommendations[treatment_methods_tuple].append(str(tooth_number))  # Aynı tedavi yöntemine sahip diş numarasını birleştiriyoruz
        else:
            merged_recommendations[treatment_methods_tuple] = [str(tooth_number)]
    
    # Birleştirilmiş tedavi yöntemlerini recommendation_dict'e aktarıyoruz
    for treatment_methods_tuple, tooth_numbers in merged_recommendations.items():
        en_treatment_method = treatment_methods_tuple[0]  # İlk tedavi yöntemini alıyoruz
        treatment_recommendation_dict[", ".join(tooth_numbers)] = {
            'en_treatment_method': en_treatment_method,
        }
    return treatment_recommendation_dict


def suggest_implant_section(image_report_obj):
    suggested_implant_objects = SuggestImplantToMissingTooth.objects.filter(image_report=image_report_obj)
    implant_recommendation_dict = {}
    merged_recommendations = {}  # Tedavi yöntemleri aynı olan diş numaralarını birleştirmek için kullanılacak sözlük
    
    for treatment_for_tooth in suggested_implant_objects:
        tooth_number = treatment_for_tooth.tooth_number
        recommendation_methods = treatment_for_tooth.recommendation.all()
        treatment_methods = set()  # Tedavi yöntemlerini bir küme olarak tutmak için set kullanıyoruz
        
        for method in recommendation_methods:
            en_treatment_method = method.en_treatment_method
            treatment_methods.add((en_treatment_method))  # Küme içerisine tedavi yöntemlerini ekliyoruz
        
        treatment_methods_tuple = tuple(treatment_methods)  # Tedavi yöntemlerini tuple olarak saklıyoruz
        
        if treatment_methods_tuple in merged_recommendations:
            merged_recommendations[treatment_methods_tuple].append(str(tooth_number))  # Aynı tedavi yöntemine sahip diş numarasını birleştiriyoruz
        else:
            merged_recommendations[treatment_methods_tuple] = [str(tooth_number)]
    
    # Birleştirilmiş tedavi yöntemlerini recommendation_dict'e aktarıyoruz
    for treatment_methods_tuple, tooth_numbers in merged_recommendations.items():
        en_treatment_method = treatment_methods_tuple[0]  # İlk tedavi yöntemini alıyoruz
        implant_recommendation_dict[", ".join(tooth_numbers)] = {
            'en_treatment_method': en_treatment_method,
        }
    return implant_recommendation_dict

# def treatment_planning_from_AI_function(image_report_obj): # SAĞ ÜSTTEN TEDAVİ PLANLAMASINA BASINDA TEXTAREA'NIN İÇİNİ DOLDURAN KISIM
#     treatment_recommendations = prepare_treatments(image_report_obj = image_report_obj)
#     implant_recommendation_dict = suggest_implant_section(image_report_obj)
#     all_recommendations = dict(list(treatment_recommendations.items()) + list(implant_recommendation_dict.items()))
#     return all_recommendations


@login_required
def treatment_planning_from_AI_request(request): # SAĞ ÜSTTEN TEDAVİ PLANLAMASINA BASINDA TEXTAREA'NIN İÇİNİ DOLDURAN KISIM
    
    selectedItems = []
    if request.method == "GET":
        print("request", request.GET)
        selectedItems = request.GET.getlist('selected_items[]', None)
        print("selectedItems", selectedItems)
        image_report_id = request.GET.get("image_report_id")
        image_report_obj = ImageReport.objects.get(id=image_report_id)
        treatment_recommendations = prepare_treatments(image_report_obj=image_report_obj, illness_list = selectedItems)
        implant_recommendation_dict = suggest_implant_section(image_report_obj)
        all_recommendations = dict(list(treatment_recommendations.items()) + list(implant_recommendation_dict.items()))
        return JsonResponse({"treatment_planning_from_AI": all_recommendations})


@login_required
def diagnosis_page(request, image_report_id):
    try:
        if "/tr/" in request.build_absolute_uri():
            lang = "tr"
        elif "/uz/" in request.build_absolute_uri():
            lang = "uz"
        elif "/nl/" in request.build_absolute_uri():
            lang = "nl"
        elif "/ru/" in request.build_absolute_uri():
            lang = "ru"
        else:
            lang = "en"

        start_time = time.time()
        user = request.user
        specs = get_specs()
        profile = Profile.objects.get(user=user)
        image_report_obj = ImageReport.objects.get(id=image_report_id, image__archived=False)
        report_tooth_obj = ReportTooth.objects.filter(image_report=image_report_obj).order_by('number_prediction')
        #hasta ad,yaş ve radyografi tarihi alma
        page_name = request.path
        has_page_name_diagnosis = 'diagnosis' in page_name
        patient_obj = image_report_obj.image.patient
        if patient_obj.user.company != profile.company and not user.is_superuser:
            messages.warning(request, "Hastanın doktoru değilsiniz.")
            return HttpResponseRedirect(reverse('patientsPage'))
        birthday = patient_obj.date_of_birth
        today_for_age = date.today()
        if birthday:
            patient_age = today_for_age.year - birthday.year
        else:
            patient_age = None
        patient_full_name = patient_obj.first_name + " " + patient_obj.last_name
        patient_email = patient_obj.email
        radiography_create_date = image_report_obj.created_date + timedelta(hours=3)
        radiography_create_date = radiography_create_date.strftime("%d.%m.%Y %H:%M")

        ### doktor not kısmı ###
        doctor_note = image_report_obj.note
        ####
        image_type = image_report_obj.image.type.name
        cache_active_models = active_model_labels_function()
        patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
        active_model_labels_dict = cache_active_models[image_report_obj.image.type.name][patient_type]
        illness_dict = {}
        radiography_section_dict = {}
        tooth_cards_dict = {}
        diagnosis_section_dict = {}
        other_radiographys_section_dict = {}
        image_type_dict = {}

        # diagnosis list left side
        def diagnosis_section_function():
            diagnosis_dict = {}
            if not image_report_obj.result_json:
                return diagnosis_section_dict
            result_json = json.loads(image_report_obj.result_json)

            # mevcut bulguları sözlük haline getirip birleştirme için hazıralma fonksiyonu
            def prepare_current_illness_for_concat_function():
                palate_results = result_json["palate_results"]
                illness_pool = result_json["illness_pool"]
                measurement_results = result_json["measurement_results"] if "measurement_results" in result_json.keys() else {}
                palate_results_list = [item for item in palate_results]
                illness_pool_list = [item for item in illness_pool]

                # illness pooldakileri ekleme
                def illness_pool_function():
                    for illness_pool in illness_pool_list:
                        prediction_name = illness_pool['name']
                        active_label = active_model_labels_dict.get(prediction_name, None)
                        if not active_label: continue
                        active_label_type = active_label["label_type"]
                        active_label_type_tr = active_label["label_type_tr"]
                        active_label_type_nl = active_label["label_type_nl"]
                        active_label_type_ru = active_label["label_type_ru"]
                        active_label_type_uz = active_label["label_type_uz"]
                        if active_label_type not in diagnosis_dict:
                            diagnosis_dict[active_label_type] = {"illness": {}, "label_type_tr": active_label_type_tr,"label_type_nl": active_label_type_nl,"label_type_uz": active_label_type_uz,"label_type_ru": active_label_type_ru}
                        if active_label["sub_label_status"] == True:
                            main_label = active_label["main_label"]
                            if main_label["model_label_name"] not in diagnosis_dict[active_label_type]["illness"].keys():
                                diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]] = {"label_dict": {}, "count": 0, "main_label_data": active_model_labels_dict[main_label["model_label_name"]]}
                            if main_label["model_label_name"] not in diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"].keys():
                                diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name] = active_label
                                if "count" in diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]:
                                    diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]["count"] += 1
                                else:
                                    diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]["count"] = 1

                        else:
                            if prediction_name not in diagnosis_dict[active_label_type]["illness"].keys():
                                diagnosis_dict[active_label_type]["illness"][prediction_name] = {"label_dict": {}, "count": 0, "main_label_data": active_label}

                            diagnosis_dict[active_label_type]["illness"][prediction_name]["count"] += 1
                # palate resultsları ekleme
                def palate_result_function():
                    for palate_result in palate_results_list:
                        prediction_name = palate_result['name']
                        active_label = active_model_labels_dict.get(prediction_name, None)
                        if not active_label: continue
                        active_label_type = active_label["label_type"]
                        active_label_type_tr = active_label["label_type_tr"]
                        active_label_type_uz = active_label["label_type_uz"]
                        active_label_type_ru = active_label["label_type_ru"]
                        active_label_type_nl = active_label["label_type_nl"]
                        if active_label_type not in diagnosis_dict:
                            diagnosis_dict[active_label_type] = {"illness": {}, "label_type_tr": active_label_type_tr,"label_type_uz": active_label_type_uz, "label_type_ru": active_label_type_ru,"label_type_nl": active_label_type_nl}
                        
                        if active_label["sub_label_status"] == True:
                            main_label = active_label["main_label"]
                            if main_label["model_label_name"] not in diagnosis_dict[active_label_type]["illness"].keys():
                                diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]] = {"label_dict": {}, "count": 0, "main_label_data": active_model_labels_dict[main_label["model_label_name"]]}
                                
                            if main_label["model_label_name"] not in diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"].keys():
                                diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name] = active_label
                                if "count" in diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]:
                                    diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]["count"] += 1
                                else:
                                    diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]["count"] = 1
                        else:
                            if prediction_name not in diagnosis_dict[active_label_type]["illness"].keys():
                                diagnosis_dict[active_label_type]["illness"][prediction_name] = {"label_dict": {}, "count": 0, "main_label_data": active_label}

                            diagnosis_dict[active_label_type]["illness"][prediction_name]["count"] += 1
                # Measure resultsları ekleme
                def measure_result_dict():
                    for measure in measurement_results:
                        prediction_name = measure['name']
                        active_label = active_model_labels_dict.get(prediction_name, None)
                        if not active_label: continue
                        active_label_type = active_label["label_type"]
                        active_label_type_tr = active_label["label_type_tr"]
                        active_label_type_uz = active_label["label_type_uz"]
                        active_label_type_ru = active_label["label_type_ru"]
                        active_label_type_nl = active_label["label_type_nl"]
                        if active_label_type not in diagnosis_dict:
                            diagnosis_dict[active_label_type] = {"illness": {}, "label_type_tr": active_label_type_tr,"label_type_uz": active_label_type_uz, "label_type_ru": active_label_type_ru,"label_type_nl": active_label_type_nl}
                        
                        if active_label["sub_label_status"] == True:
                            main_label = active_label["main_label"]
                            if main_label["model_label_name"] not in diagnosis_dict[active_label_type]["illness"].keys():
                                diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]] = {"label_dict": {}, "count": 0, "main_label_data": active_model_labels_dict[main_label["model_label_name"]]}

                            if main_label["model_label_name"] not in diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"].keys():
                                diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name] = active_label
                                if "count" in diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]:
                                    diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]["count"] += 1
                                else:
                                    diagnosis_dict[active_label_type]["illness"][main_label["model_label_name"]]["label_dict"][prediction_name]["count"] = 1

                        else:
                            if prediction_name not in diagnosis_dict[active_label_type]["illness"].keys():
                                diagnosis_dict[active_label_type]["illness"][prediction_name] = {"label_dict": {}, "count": 0, "main_label_data": active_label}

                            diagnosis_dict[active_label_type]["illness"][prediction_name]["count"] += 1

                # # hastalık count unu ekleme
                # def add_diagnosis_counts():
                #     diagnosis_dict_old = diagnosis_dict.copy()
                #     for label_type, illness_dict in diagnosis_dict_old.items():
                #         for label, value in illness_dict["illness"].items():
                #             count = len(value["label_list"])
                #             diagnosis_dict[label_type]["illness"][label]["count"] = count

                illness_pool_function()
                palate_result_function()
                measure_result_dict()
                # add_diagnosis_counts()
                return diagnosis_dict

            def add_label_data():
                for label, data in active_model_labels_dict.items():
                    if "sub_label_status" in data.keys():
                        data["sub_label_status"] = "true" if data["sub_label_status"] else "false"
                    for label_type, label_type_values in diagnosis_dict.items():
                        if label in label_type_values["illness"].keys():
                            label_type_values["illness"][label]["label_data"] = data
                return diagnosis_dict
            diagnosis_dict = prepare_current_illness_for_concat_function()
            diagnosis_dict = add_label_data()
            diagnosis_section_dict["labels"] = diagnosis_dict
            diagnosis_section_dict["filter"] = "abc"
            return diagnosis_section_dict

        # Radiography için sözlük hazırlanan fonksiyon
        def radiography_section_function():
            image_path = image_report_obj.image.path.url
            radiography_section_dict["image_path"] = image_path
            return radiography_section_dict

        # tooth chart
        def tooth_chart_function():
            tooth = {}
            tooth_icons = ToothTypeIcon.objects.all()
            dict_of_tooths = {"child_section_upper": [55, 54, 53, 52, 51, 61, 62, 63, 64, 65],
                "child_section_lower": [85, 84, 83, 82, 81, 71, 72, 73, 74, 75],
                "adult_section": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]}

            def get_tooth_icons(tooth_numbers):
                return tooth_icons.filter(tooth_number__in=tooth_numbers)

            def get_report_tooth(tooth_number):
                return (report_tooth_obj.filter(number_edited=tooth_number).first() or report_tooth_obj.filter(
                    number_prediction=tooth_number).first())

            def process_tooth_section(tooth_section, section_key):
                tooth_icons_section = get_tooth_icons(dict_of_tooths[section_key])
                section_dict = {}

                for tooth_number in dict_of_tooths[section_key]:
                    tooth_icon_with_number = tooth_icons_section.filter(tooth_number=tooth_number)
                    report_tooth = get_report_tooth(tooth_number)

                    if not report_tooth or not report_tooth.icon_type:
                        section_dict[tooth_number] = {"current_icon": None,
                            "other_icons": [{"name": i.name, "path": i.icon_path} for i in tooth_icon_with_number]}
                        continue

                    icon_type = report_tooth.icon_type
                    section_dict[tooth_number] = {"current_icon": {"name": icon_type.name, "path": icon_type.icon_path},
                        "other_icons": [{"name": i.name, "path": i.icon_path} for i in tooth_icon_with_number]}

                tooth[tooth_section] = section_dict

            process_tooth_section("section_upper", "child_section_upper")
            process_tooth_section("section_lower", "child_section_lower")
            process_tooth_section("section_adult", "adult_section")
            return tooth

        # tooth cards
        def tooth_cards_function():
            kid_tooth_list = [51, 52, 53, 54, 55, 61, 62, 63, 64, 65, 71, 72, 73, 74, 75, 81, 82, 83, 84, 85]
            is_kid_status = report_tooth_obj.filter(number_prediction__in=kid_tooth_list).exists()
            for disease, details in active_model_labels_dict.items():
                disease_name = disease
                disease_id = details["id"]
                illness_dict[disease_id] = {"en_disease_name": disease_name}
            else:
                print("Geçerli bir image type değeri bulunamadı.")
            for report_tooth in report_tooth_obj:
                report_tooth_predict_obj = report_tooth.reporttoothpredict_set.filter(is_active=True)
                illness_list = []

                for report_tooth_predict in report_tooth_predict_obj:
                    prediction = report_tooth_predict.correction or report_tooth_predict.prediction
                    prediction = json.loads(prediction.replace("'", '"'))
                    illness_names = active_model_labels_dict.get(prediction["name"], None)
                    if not illness_names: continue
                    illness_list.append(prediction)

                tooth_cards_dict[report_tooth.number_prediction] = {"illness": illness_list,
                    "path": report_tooth.path.url if report_tooth.path else None, "note": report_tooth.note,
                    "approved": report_tooth.new_approve_status, "id": report_tooth.id,
                    "number_edited": {"status": bool(report_tooth.number_edited), "number": report_tooth.number_edited},
                    "treatment_methods": []}

                treatment_recommendations = TreatmentRecommendationForTooth.objects.filter(tooth=report_tooth)
                for recommendation in treatment_recommendations:
                    treatment_methods = recommendation.recommendation.all()
                    for method in treatment_methods:
                        tooth_cards_dict[report_tooth.number_prediction]["treatment_methods"].append(
                            {"en_name": method.en_treatment_method, "slug": method.slug})
            
            
            return tooth_cards_dict, is_kid_status

        # Treatments
        def treatment_recommendation_manual():
            all_treatment_methods = TreatmentMethod.objects.all()
            treatment_method_list = []
            for method in all_treatment_methods:
                treatment_method_list.append({
                    'en_treatment_method': method.en_treatment_method,
                    'id': method.id,
                    'slug':method.slug
                })
            treatment_for_tooth_manual = {
                    'treatment_methods': treatment_method_list,
                }
            return treatment_for_tooth_manual
            ### treatment planning test  ### ESKİ DİŞTEKİ HASTALIĞA GÖRE TREATMENT GÖSTEREN KOD

        def treatment_recommendation_auto():
            all_illness_treatment_methods = IllnessTreatmentMethod.objects.all()
            treatment_methods_dict = {}

            for illness_treatment_method in all_illness_treatment_methods:
                label_names = [label.name for label in illness_treatment_method.label.all()]
                treatment_methods = [method.en_treatment_method for method in illness_treatment_method.treatment_method.all()]
                radiography_type = illness_treatment_method.radiography_type
                id = illness_treatment_method.id
                treatment_methods_dict[illness_treatment_method.id] = {
                    'label_names': label_names,
                    'treatment_methods': treatment_methods,
                    'radiography_type':radiography_type,
                    'id':id,
                }

            treatment_for_tooth_auto = {}
            for key, value in tooth_cards_dict.items():
                illness_list = value['illness']
                treatment_methods_list = []
                illness_names = [illness['name'] for illness in illness_list]
                for illness_name in illness_names:

                    for treatment in treatment_methods_dict.values():
                        label_names = treatment['label_names']
                        all_included = all(item in illness_names for item in label_names)
                        if all_included:
                            if illness_name in label_names:
                                treatment_methods = treatment['treatment_methods']
                                for method in treatment_methods:
                                    treatment_method_obj = IllnessTreatmentMethod.objects.filter(treatment_method__en_treatment_method=method).first()
                                    if treatment_method_obj:
                                        #listeye atarken tedavileri uniqueleştirme
                                        if method not in [treatment['treatment_method'] for treatment in treatment_methods_list]:
                                            treatment_methods_list.append({
                                                'treatment_method': method,
                                                'id': treatment_method_obj.id,
                                                'radiography_type': treatment_method_obj.radiography_type,
                                                'slug':treatment_method_obj.treatment_method.first().slug,
                                            })
                treatment_for_tooth_auto[key] = {
                    'illnesses': illness_names,
                    'treatment_methods': treatment_methods_list,
                }
            return treatment_for_tooth_auto

            ###

        # middle radiography area
        def other_radiographys_function():
            radiographys = Image.objects.filter(patient=patient_obj).order_by("-id")
            radiography_dict = {}
            for radiography in radiographys:
                image_report_last_obj = ImageReport.objects.filter(image=radiography, image__archived=False).last()
                if not image_report_last_obj:
                    continue
                status1 = "2"
                status2 = "2"
                if image_report_last_obj and image_report_last_obj.is_done and not image_report_last_obj.is_error:
                    status1 = "completed"
                    status2 = "success"
                elif image_report_last_obj and image_report_last_obj.is_error:
                    status1 = "not-completed"
                    status2 = "error"
                else:
                    status1 = "not-completed"
                    status2 = "error"
                if radiography.thumbnail_image_path:
                    radiography_image = radiography.thumbnail_image_path.url
                elif radiography.type and radiography.type.name == "CBCT" and not radiography.path and not radiography.thumbnail_image_path:
                    radiography_image = f"/media/dental/radio/{lang}3d.png"
                else:
                    radiography_image = radiography.path.url

                last_obj_id = None
                dynamic_href = None
                if image_report_last_obj:
                    last_obj_id = image_report_last_obj.id
                    if image_report_last_obj.name == "Lateral Cephalometric":
                        dynamic_href = f"/{lang}/cephalometric/{image_report_last_obj.id}"
                    elif image_report_last_obj.name == "CBCT":
                        dynamic_href = f"/{lang}/CBCT/{image_report_last_obj.id}"
                    else:
                        dynamic_href = f"/{lang}/diagnosis/{image_report_last_obj.id}"
                radiography_dict[last_obj_id] = {
                    "path": radiography_image,
                    "status1": status1,
                    "status2": status2,
                    "image_id": radiography.id,
                    "date": image_report_last_obj.updated_date.strftime("%d/%m/%Y") if image_report_last_obj else None,
                    "href": dynamic_href
                }

            other_radiographys_section_dict["radiography"] = radiography_dict
            return other_radiographys_section_dict

        # Treatments planning
        def treatment_planning_function():
            treatments = TreatmentPlanning.objects.filter(image_report=image_report_obj).order_by("-id")
            treatment_list = []

            for treatment in treatments:
                treatment_dict = {
                    'id': treatment.id,
                    'updated_planning': treatment.updated_planning if treatment.updated_planning else None,
                    'ai_planning': treatment.ai_planning,
                    'created_date': (treatment.created_date + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M"),
                    'modified_date': (treatment.modified_date + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M"),
                    # Diğer alanları da burada ekleyebilirsiniz
                }
                treatment_list.append(treatment_dict)

            grouped_treatments = {}
            today = date.today()


            for counter,treatment in enumerate(treatment_list):
                modified_date = datetime.strptime(treatment['modified_date'], "%d.%m.%Y %H:%M").date()
                if modified_date == today:
                    treatment["counter"] = counter + 1
                    if 'Today' in grouped_treatments:
                        grouped_treatments['Today'].append(treatment)
                    else:
                        grouped_treatments['Today'] = [treatment]
                else:
                    treatment["counter"] = counter + 1
                    if modified_date in grouped_treatments:
                        grouped_treatments[modified_date].append(treatment)
                    else:
                        grouped_treatments[modified_date] = [treatment]

            return grouped_treatments

        def upload_radiography_function():
            image_types = ImageType.objects.all().order_by("id")

            for image_type_obj in image_types:
                image_type_dict[image_type_obj.id] = image_type_obj.name
            cbct_value = image_type_dict.pop(3)
            image_type_dict[3] = cbct_value

            return image_type_dict

        def doctor_choices_for_report_function():
            profile = Profile.objects.get(user=user)
            doctor_choices = DoctorChoicesForReport.objects.filter(profile=profile).first()
            if doctor_choices:
                doctor_choices_dict = {
                    'format':doctor_choices.format,
                    'filter_report_based':doctor_choices.filter_report_based,
                    'patient_infos': doctor_choices.choices.filter(name='patient_infos').exists(),
                    'undrawed_radiography': doctor_choices.choices.filter(name='radiography_infos').exists(),
                    'drawed_radiography': doctor_choices.choices.filter(name='drawed_radiography_infos').exists(),
                    'selected_drawed_radiography':doctor_choices.choices.filter(name='draw_with_selected_labels').exists(),
                    'all_drawed_radiography':doctor_choices.choices.filter(name='draw_with_all_labels').exists(),
                    'draw_numbering':doctor_choices.choices.filter(name='draw_numbering').exists(),
                    'doctor_note': doctor_choices.choices.filter(name='doctor_note_infos').exists(),
                    'doctor_signature': doctor_choices.choices.filter(name='signature').exists(),
                    'treatment_plannings': doctor_choices.choices.filter(name='treatment_plans').exists(),
                }
            else:
                doctor_choices_dict = None
            return doctor_choices_dict
            
        def filter_illnesses_by_proba_tool(image_report_obj):
            selected_items = ["weak", "medium", "strong", "dentist"]
            filter_by_proba_dict = {"weak": {"lower": 0, "upper": 33, "length": 0},
                                    "medium": {"lower": 33, "upper": 66, "length": 0},
                                    "strong": {"lower": 66, "upper": 99, "length": 0}, 
                                    "dentist": {"lower": 99, "upper": 102, "length": 0} }
            result_json = json.loads(image_report_obj.result_json)
            new_palate_results = []
            new_illness_pool = []
            palate_results = result_json["palate_results"]
            illness_pool = result_json["illness_pool"]

            for i in palate_results:
                for j in selected_items:
                    if filter_by_proba_dict[j]["lower"] < int(i["probability"]) <= filter_by_proba_dict[j]["upper"]:
                        filter_by_proba_dict[j]["length"] += 1
            palate_results = new_palate_results

            for i in illness_pool:
                for j in selected_items:
                    if filter_by_proba_dict[j]["lower"] < int(i["probability"]) <= filter_by_proba_dict[j]["upper"]:
                        filter_by_proba_dict[j]["length"] += 1
            illness_pool = new_illness_pool

            return filter_by_proba_dict
        
        # treatment_planning_from_AI = treatment_planning_from_AI_function(image_report_obj) # TEDAVİ PLANLAMASININ İÇERİSİNDEKİ VERİYİ SAĞLAYAN FONKSİYON
        diagnosis_section = diagnosis_section_function() # SOL TARAFTAKİ RENKLER VE SAYILARIYLA BERABER HASTALIKLARI GETİREN FONKSİYON
        radiography_section = radiography_section_function() # ANA RADYOGRAFİYİ HAZIRLAYAN FONKSİYON
        tooth_cards_section, is_kid_status = tooth_cards_function() # SAĞ MENÜDEKİ DİŞLERİ 
        other_radiographys_section = other_radiographys_function() # ALT KISIMDAKİ SLİDER İÇİN HASTAYA AİT DİĞER RADYOGRAFİLERİ HAZIRLAYAN FONKSİYON
        tooth_chart_section = tooth_chart_function() # SAĞ MENÜDEKİ DİŞ İCONLARINI NUMARALARINI HAZIRLAYAN FONKSİYON
        user_theme_dict = user_theme_choices(user) # KULLANICININ TEMASINI GETİREN FONKSİYON
        grouped_treatments = treatment_planning_function() # KULLANICININ KAYDETTİĞİ TEDAVE PLANLAMALARINI, DAHA ÖNCESİNDEN OLUŞTURULMUŞ PLANLARLA BERABER LİSTELEYEN FONKSİYON
        image_type_dict = upload_radiography_function() # KULLANICININ RADYOGRAFİ YÜKLERKEN DROPZONENİN ÜST KISMINDA RADYOGRAFİ TÜRÜNÜ SEÇMESİ İÇİN HAZIRLANAN LİSTE
        treatment_recommendation_manual=treatment_recommendation_manual()
        treatment_recommendation_auto=treatment_recommendation_auto()
        doctor_choices_dict=doctor_choices_for_report_function() # RAPOR OLUŞTURDA DOKTORUN DAHA ÖNCEDEN YAPTIĞI TERCİHLERİ GETİREN FONKSİYON
        filter_by_proba_dict = filter_illnesses_by_proba_tool(image_report_obj) # ZAYIF ORTA YÜKSEK VE HEKİM OLARAK BELİRLENEN FİLTRELERE GÖRE ETİKETLERİ GETİREN FONKSİYON
        context = {
            "diagnosis_section": diagnosis_section,
            "radiography_section": radiography_section,
            "tooth_chart_section": tooth_chart_section,
            "tooth_cards_section": tooth_cards_section,
            "other_radiographys_section": other_radiographys_section,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "is_kid_status": is_kid_status,
            "image_report_id": image_report_id,
            "illness_dict": illness_dict,
            "image_type": image_type,
            "grouped_treatments": grouped_treatments,
            "image_type_dict": image_type_dict,
            "patient_age": patient_age,
            "patient_full_name": patient_full_name,
            "patient_email": patient_email,
            "has_page_name_diagnosis": has_page_name_diagnosis,
            "image_type": image_report_obj.image.type.name,
            "radiography_create_date": radiography_create_date,
            "treatment_recommendation_manual": treatment_recommendation_manual,
            "treatment_recommendation_auto": treatment_recommendation_auto,
            "doctor_note": doctor_note,
            "doctor_choices_dict": doctor_choices_dict,
            # "treatment_planning_from_AI": treatment_planning_from_AI,
            "filter_by_proba_dict": filter_by_proba_dict,
            "specs": specs,
        }
        end_time = time.time()  # Bitiş zamanını kaydet
        elapsed_time = end_time - start_time  # Geçen süreyi hesapla
        print("Elapsed", elapsed_time)
        print(f"Fonksiyon çalışma süresi: {elapsed_time:.4f} saniye")
        return render(request, "diagnosis.html", context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def log_out(request):
    user = request.user
    logout(request)
    set_user_login_logout(user,status="logout")
    return HttpResponseRedirect(reverse('loginPage'))


# şifremi unuttum ekranı ve kod gönderen yer
def forgot_password_page(request):
    try:
        specs = get_specs()
        if request.method == "POST":
            mail = request.POST.get("mailInput")
            user = User.objects.filter(email=mail).first()
            user_theme = UserTheme.objects.filter(user=user).first()
            if user_theme.language == "en":
                lang = "en"
            else:
                lang = "tr"
            if user:
                key = str(uuid.uuid4()).replace("-","")[0:6]
                full_name= user.first_name + " " + user.last_name
                ufpk_obj = UserForgotPasswordKey.objects.create(user=user)
                ufpk_obj.key = key
                ufpk_obj.save()
                if lang == "en":
                    send_email_for_password(mail,f"CranioCatch Password Reset",f"Hello Dear {full_name}\nA password reset request was made through the CranioCatch Clinic. If you did not send the request, please notify it by sending it to info@craniocatch.com.\nYou can reset your password with verification code {key} \nWe wish you healthy days…")
                    message = _("Mail Sent")
                    return JsonResponse({'status':True,'ufpk_id': ufpk_obj.id,'message':message})
                else:
                    send_email_for_password(mail,f"CranioCatch Şifre Sıfırlama",f"Merhaba Sayın {full_name}\nCranioCatch Clinic üzerinden bir şifre yenileme talebi yapıldı. Eğer talebi siz göndermediyseniz, lütfen info@craniocatch.com adresine ileterek bildiriniz.\n{key} doğrulama kodu ile işlem yapabilirsiniz.\nSağlıklı günler dileriz…")
                    message = _("Mail Sent")
                    return JsonResponse({'status':True,'ufpk_id': ufpk_obj.id,'message':message})
            else:
                message = _("No user found for this mail")
                return JsonResponse({"status":False, "message":message})
        return render(request, 'forgot-password-get-key.html', context={"specs": specs})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def change_password(request,ufpk_id):
    try:
        specs = get_specs()
        context = {'ufpk_id':ufpk_id, "specs": specs,}
        if request.method == 'POST':
            ufpk_obj = UserForgotPasswordKey.objects.get(id=ufpk_id)
            user = ufpk_obj.user
            key = request.POST.get("key")
            password1 = request.POST.get('new_password')
            password2 = request.POST.get('new_password2')
            if password1 != password2:
                message = _("The passwords you entered do not match")
                return JsonResponse({'status':False, 'code':"passwords do not match", 'message':message})
            if ufpk_obj.key == key:
                user.set_password(password1)
                user.save()
                message = _("Your password has been reset!")
                ufpk_obj.delete()
                return JsonResponse({'status':True, 'message':message})
            if ufpk_obj.key != key:
                message = _("Your reset code is wrong.")
                return JsonResponse({'status':False, 'code':'code is wrong', 'message':message})
        return render(request, 'reset-password-with-key.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def profile_page(request):
    try:
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        user_informations = {}
        user = request.user
        specs = get_specs()
        profile = Profile.objects.get(user=user)
        user_theme_dict = user_theme_choices(user)
        token_informations = cranio_remaining_token(profile_obj=profile, detailed_status=True)

        user_informations["profile_photo"] = profile.profile_photo.url if profile.profile_photo else "/static/img/profile_photo.jpg"
        user_informations["signature"] = profile.signature.url if profile.signature else None
        user_informations["full_name"] = user.first_name + " " + user.last_name
        user_informations["email"] = user.email
        user_informations["phone"] = profile.phone
        print("token_informations", token_informations)
        context = {
            "user_informations": user_informations,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "token_informations": token_informations,
            "specs": specs,
            "is_owner_of_company": profile.is_owner_of_company,
            "distributor": profile.is_distributor,
        }
        return render(request,'profile.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def update_profile_page(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        user_theme_dict = user_theme_choices(user)
        specs = get_specs()
        if profile.profile_photo:
            profile_photo = profile.profile_photo.url
        else:
            profile_photo = "/static/img/profile_photo.jpg"
        if profile.signature:
            signature = profile.signature.url
        else:
            signature = None
        if profile.company.logo:
            clinic_logo = profile.company.logo
        else:
            clinic_logo = None
        context = {
            'username':user.username,
            'full_name': user.first_name + " " + user.last_name,
            'name': user.first_name,
            'surname':user.last_name,
            'profile_photo': profile_photo,
            'signature':signature,
            'clinic_logo':clinic_logo,
            'email':user.email,
            'phone':profile.phone,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            'clinic_name':profile.company.name,
            "specs": specs,

        }
        return render(request,'update-profile.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def old_report_page(request, slug):
    redirected_url = reverse("report_page", args=[slug])
    return redirect(redirected_url)

def report_page(request, slug):
    try:
        if "/tr/" in request.build_absolute_uri():
            lang = "tr"
        elif "/uz/" in request.build_absolute_uri():
            lang = "uz"
        elif "/ru/" in request.build_absolute_uri():
            lang = "ru"
        elif "/nl/" in request.build_absolute_uri():
            lang = "nl"
        else:
            lang = "en"
        specs = get_specs()
        patient_infos = {}
        image_report_infos = {}
        doctor_notes_infos = {}
        signature_infos = {}
        Sections = {}
        treatment_plan_infos = []
        patient_info_option = None
        radiography_info_option = None
        drawed_radiography_info_option = None
        doctor_note_info_option = None
        treatment_plan_info_option = None
        signature_option = None
        arabic_status = False
        report_obj = CreateReportForPatient.objects.get(slug=slug)
        clinic_logo = report_obj.image_report.user.company.logo.url if report_obj.image_report.user.company.logo else None

        def patient_infos_function():
            patient = report_obj.patient
            patient_infos["first_name"] = patient.first_name
            patient_infos["last_name"] = patient.last_name
            patient_infos['email'] = patient.email if patient.email else None
            patient_infos['phone'] = patient.phone if patient.phone else None
            patient_infos['gender'] = patient.gender
            patient_infos['file_no'] = patient.file_no
            patient_infos['id'] = patient.id
            date_of_birth = patient.date_of_birth
            if date_of_birth:
                patient_infos['date_of_birth'] = date_of_birth.strftime("%d-%m-%Y")
            else:
                patient_infos['date_of_birth'] = None

        if report_obj.options.filter(name="patient_infos").exists():
            patient_infos_function()
            patient_info_option = True

        def image_report_object_infos_function():
            image_report_infos["image_reports_image"] = report_obj.image_report.image.path.url if report_obj.image_report.image.path else None

        if report_obj.options.filter(name="radiography_infos"):
            image_report_object_infos_function()
            radiography_info_option = True

        def drawed_radiography_object_infos_function():
            output_path = report_obj.drawed_image_path
            image_report_infos["drawed_image_reports_image"] = output_path.replace(ccclinic_path_with_slash, "") if os.path.exists(output_path) else None

        def drawed_implant_crown_radiography_object_infos_function():
            output_path_for_implant_or_crown = report_obj.drawed_implant_crown_image_path
            print("output_path_for_implant_or_crown",output_path_for_implant_or_crown)
            if output_path_for_implant_or_crown:
                image_report_infos["drawed_implant_crown_image_reports_image"] = output_path_for_implant_or_crown.replace(ccclinic_path_with_slash, "") if os.path.exists(output_path_for_implant_or_crown) else None

        image_report_obj = ImageReport.objects.get(cbct=False, id=report_obj.image_report.id, image__archived=False)
        labels_colors_on_radiography = None
        if "Lateral Cephalometric" not in image_report_obj.name:
            def prepare_labels_colors_on_radiography():
                illness_appended_list = []
                result_json = json.loads(image_report_obj.result_json)
                cache_active_models = active_model_labels_function()
                patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
                labels = cache_active_models[report_obj.image_report.name][patient_type]
                for illness_and_palate, illness_list in result_json.items():
                    for illness in illness_list:
                        label_illness = labels.get(illness["name"])
                        if label_illness:
                            label_illness["name"] = illness["name"]
                            illness_appended_list.append(label_illness)
                unique_data = []
                for d in illness_appended_list:
                    if "main_label" not in d.keys(): continue
                    del d["main_label"]
                unique_data = list(set(tuple(sorted(d.items())) for d in illness_appended_list))
                unique_data = [dict(t) for t in unique_data]
                return unique_data
            labels_colors_on_radiography = prepare_labels_colors_on_radiography()

        if report_obj.options.filter(name="drawed_radiography_infos"):
            drawed_radiography_object_infos_function()
            drawed_implant_crown_radiography_object_infos_function()
            drawed_radiography_info_option = True

        def doctor_note_infos_function():
            doctor_notes_infos["doctor_note"] = report_obj.image_report.note if report_obj.image_report.note else None
            doctor_notes_infos["doctor_full_name"] = report_obj.image_report.user.user.first_name + " " + report_obj.image_report.user.user.last_name
            doctor_notes_infos["image_report_created_date"] = report_obj.image_report.created_date.strftime("%d.%m.%Y")

        if report_obj.options.filter(name="doctor_note_infos"):
            doctor_note_infos_function()
            doctor_note_info_option = True

        def treatment_plan_infos_function():
            treatment_plans = TreatmentPlanning.objects.filter(image_report=report_obj.image_report).order_by("-id").first()
            if treatment_plans:
                if treatment_plans.updated_planning:
                    treatment_plan = treatment_plans.updated_planning
                    treatment_plan_infos.append(treatment_plan)
                elif treatment_plans.ai_planning:
                    treatment_plan = treatment_plans.ai_planning
                    treatment_plan_infos.append(treatment_plan)

        if report_obj.options.filter(name="treatment_plans"):
            treatment_plan_infos_function()
            treatment_plan_info_option = True

        def signature_infos_function():
            user = report_obj.image_report.user.user
            profile = Profile.objects.get(user=user)
            signature_infos["signature"] = profile.signature.url if profile.signature else None

        if report_obj.options.filter(name="signature"):
            signature_option = True
            signature_infos_function()
        def is_arabic():
            doctor_user = report_obj.patient.user.user
            theme_obj = UserTheme.objects.get(user=doctor_user)
            print("theme_obj", theme_obj)
            arabic_status = theme_obj.arabic
            return arabic_status
        if clinic_project_id == 1:
            arabic_status = is_arabic()
        labels_with_descriptions = None
        dental_dict = None

        if "Lateral Cephalometric" not in image_report_obj.name:
            def dentition_function():

                kid_numbers = [55, 54, 53, 52, 51, 61, 62, 63, 64, 65, 85, 84, 83, 82, 81, 71, 72, 73, 74, 75]
                
                tooth_numbers_dict = {
                    "Adult Panoramic": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 
                                        48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38],
                    "Kid Panoramic": [
                        18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 
                        48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38, 
                        55, 54, 53, 52, 51, 61, 62, 63, 64, 65, 
                        85, 84, 83, 82, 81, 71, 72, 73, 74, 75],
                    "Panoramic Adult": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 
                                        48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38],
                    "Panoramic Kid": [
                        18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 
                        48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38, 
                        55, 54, 53, 52, 51, 61, 62, 63, 64, 65, 
                        85, 84, 83, 82, 81, 71, 72, 73, 74, 75],
                    "Bitewing Left": [21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38],
                    "Bitewing Right": [18, 17, 16, 15, 14, 13, 12, 11,48, 47, 46, 45, 44, 43, 42, 41],
                    "Periapical Under": [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38],
                    "Periapical Up": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28],
                    "Periapical Under-Right": [48, 47, 46, 45, 44, 43, 42, 41],
                    "Periapical Up-Right": [18, 17, 16, 15, 14, 13, 12, 11],
                    "Periapical Under-Left": [31, 32, 33, 34, 35, 36, 37, 38],
                    "Periapical Up-Left": [21, 22, 23, 24, 25, 26, 27, 28],
                    }

                ReportToothKidNumbers = ReportTooth.objects.filter(image_report=report_obj.image_report,
                                                                number_prediction__in=kid_numbers)
                is_kid_status = True if ReportToothKidNumbers else False
                result_as_json = json.loads(image_report_obj.result_json)
                if not image_report_obj.ai_response_image_type:
                    tooth_numbers = tooth_numbers_dict["Adult Panoramic"].copy() 
                else:
                    if "up" in image_report_obj.ai_response_image_type.lower():
                        tooth_numbers = tooth_numbers_dict["Periapical Up"].copy()
                    elif "under" in image_report_obj.ai_response_image_type.lower():
                        tooth_numbers = tooth_numbers_dict["Periapical Under"].copy()
                    elif "right" in image_report_obj.ai_response_image_type.lower():
                        tooth_numbers = tooth_numbers_dict["Bitewing Right"].copy()
                    elif "left" in image_report_obj.ai_response_image_type.lower():
                        tooth_numbers = tooth_numbers_dict["Bitewing Left"].copy()
                    elif "kid" in image_report_obj.ai_response_image_type.lower():
                        tooth_numbers = tooth_numbers_dict["Kid Panoramic"].copy()
                    else:
                        tooth_numbers = tooth_numbers_dict["Adult Panoramic"].copy()

   
                if is_kid_status:
                    tooth_numbers.extend(kid_numbers)
                report_tooth_objs = ReportTooth.objects.filter(image_report=report_obj.image_report)

                if image_report_obj.ai_response_image_type and "Periapical" in image_report_obj.ai_response_image_type:

                    ReportToothNumbers = ReportTooth.objects.filter(image_report=report_obj.image_report,
                                                                number_prediction__in=tooth_numbers)
                    
                    if "Under" in image_report_obj.ai_response_image_type:
                        mean = 0
                        for i in ReportToothNumbers:
                            mean += 1 if str(i.number_prediction)[0] == "4" else -1
                        tooth_numbers = tooth_numbers_dict["Periapical Under-Right"] if mean > 0 else tooth_numbers_dict["Periapical Under-Left"]

                    if "Up" in image_report_obj.ai_response_image_type:
                        mean = 0
                        for i in ReportToothNumbers:
                            mean += 1 if str(i.number_prediction)[0] == "1" else -1
                        tooth_numbers = tooth_numbers_dict["Periapical Up-Right"] if mean > 0 else tooth_numbers_dict["Periapical Up-Left"]

                missing_tooths = []

                # olmayan dişlerin listesi 
                patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
                cache_active_models = active_model_labels_function()
                labels = cache_active_models[report_obj.image_report.name][patient_type]
                palate_results = result_as_json["palate_results"]
                descriptions = ReportPageIllnessDescriptions.objects.filter(radiography_type=image_report_obj.name)
                for result in palate_results:
                    del result['coordinates']
                for tooth_number in tooth_numbers: # olması gereken dişlerde dön
                    report_tooth_obj = report_tooth_objs.filter(number_prediction=tooth_number) # olması gereken diş veritabanında var mı
                    if report_tooth_obj:
                        report_tooth = report_tooth_obj.first()  # İlgili nesne bulundu, işlemleri gerçekleştirin
                    else:
                        missing_tooths.append(tooth_number)
                        continue # varsa objeyi al yoksa kayıp diş listesine ekle
                    report_tooth_predict_objs = report_tooth.reporttoothpredict_set.all()

                    for report_tooth_predict in report_tooth_predict_objs:
                        prediction = report_tooth_predict.prediction
                        prediction = json.loads(prediction.replace("'", '"'))
                        if prediction["name"] in labels:
                            label = labels[prediction["name"]]
                            if label["label_type"] in Sections.keys():
                                if prediction["name"] in Sections[label["label_type"]]["illnesses"].keys():
                                    Sections[label["label_type"]]["illnesses"][prediction["name"]]["values"].append(tooth_number)
                                else:
                                    Sections[label["label_type"]]["illnesses"][prediction["name"]] = {"values": [tooth_number]}
                            else:
                                Sections[label["label_type"]] = {"illnesses": {prediction["name"]: {
                                                                    "values": [tooth_number]}}}

                for palate_result in palate_results:
                    label = labels[palate_result["name"]]
                    if label["label_type"] in Sections.keys():
                        if palate_result["name"] in Sections[label["label_type"]]["illnesses"].keys():
                            pass
                        else:

                            Sections[label["label_type"]]["illnesses"][palate_result["name"]] = {"values": []}
                    else:
                        if not 'Anatomy' in Sections.keys():
                            continue
                        Sections[label["label_type"]]["illnesses"] = {palate_result["name"]: {"values": []}}
                Sections["Dentition"] = {"illnesses": {"Missing Teeth": {"values": missing_tooths}}}

                return descriptions

            descriptions = dentition_function()
            labels_with_descriptions = {}

            def add_text_to_illnesses():
                for label_type, labels in Sections.items():
                    labels = labels["illnesses"]
                    if "Anatomy" in label_type:
                        continue
                    for label, tr_name_and_values in labels.items():

                        label_list = tr_name_and_values["values"]
                        value_dict = {}
                        description = descriptions.filter(name=label)
                        if description:
                            description = description.first()
                            text_before = description.before_tooth_numbers_text_en
                            text_after = description.after_tooth_numbers_text_en
                            value_dict["text_before"] = text_before
                            value_dict["text_after"] = text_after
                            value_dict["label_list"] = label_list
                            value_dict["label_en_name"] = label
                        else:
                            value_dict["text_before"] = ""
                            value_dict["text_after"] = ""
                            value_dict["label_list"] = label_list
                        if label_type in labels_with_descriptions.keys():
                            if label in labels_with_descriptions[label_type]["illnesses"].keys():
                                labels_with_descriptions[label_type]["illnesses"][label] = value_dict
                            else:
                                labels_with_descriptions[label_type]["illnesses"][label] = value_dict
                        else:
                            labels_with_descriptions[label_type] = {"illnesses": {label: value_dict}}
            add_text_to_illnesses()

            
            dental_dict = {'missing_tooth': labels_with_descriptions.pop('Dentition')}
            dental_dict['unerupted_tooth'] = {"Unerupted Tooth": labels_with_descriptions["Dental Problems"].pop('Unerupted Tooth')} if "Dental Problems" in labels_with_descriptions.keys() and "Unerupted Tooth" in labels_with_descriptions["Dental Problems"].keys() else None
            new_dict = {}
            if dental_dict:
                for key, value in dental_dict.items():
                    if not value:
                        continue
                    name = list(value["illnesses"].keys())[0]
                    inner_value = value["illnesses"][name]
                    new_dict[key] = {'name': name, 'value': inner_value}

                dental_dict = new_dict
            view_analysis_returned_dict = None
            view_analysis_status_dict = None
            
            if not dental_dict["missing_tooth"]["value"]["label_list"]: # Dişler olmadığında yazı vardı ancak hepsi olduğunda yazı yoktu bu durum düzeltildi.
                all_teeths = ReportPageIllnessDescriptions.objects.get(name="Teeths")
                text_before = all_teeths.before_tooth_numbers_text_en
                text_after = all_teeths.after_tooth_numbers_text_en
                dental_dict["missing_tooth"]["name"] = all_teeths.name
                dental_dict["missing_tooth"]["value"]["text_before"] = text_before
                dental_dict["missing_tooth"]["value"]["text_after"] = text_after
                dental_dict["missing_tooth"]["value"]["label_en_name"] = "Teeth"
        if "Lateral Cephalometric" in image_report_obj.name:
            def view_analysis_function():
                result_json = json.loads(image_report_obj.result_json)
                Bjork = True
                Skeletal = True
                withanalysis = True
                downsanalysis = True
                view_analysis_dict = {
                    "bjork": {"name": "", "value": ""},
                    "skeletal": {"name": "", "value": ""},
                    "withanalysis": {"name": "", "value": ""},
                    "downsanalysis": {"name": "", "value": ""}
                }
                result_json = result_json["results"]["analysis_types"]
                if not report_obj.options.filter(name="Bjork-Jarabak Analysis"):
                    Bjork = False
                    result_json.pop("Bjork-Jarabak Analysis")
                else:
                    view_analysis_dict["bjork"]["name"] = "Bjork-Jarabak Analysis"
                    view_analysis_dict["bjork"]["value"] = result_json["Bjork-Jarabak Analysis"]

                if not report_obj.options.filter(name="Skeletal Factors - Anterior/Posterior"):
                    result_json.pop("Skeletal Factors - Anterior/Posterior")
                    Skeletal = False
                else:
                    view_analysis_dict["skeletal"]["name"] = "Skeletal Factors - Anterior/Posterior"

                    view_analysis_dict["skeletal"]["value"] = result_json["Skeletal Factors - Anterior/Posterior"]

                if not report_obj.options.filter(name="Wits Analysis"):
                    result_json.pop("Wits Analysis")
                    withanalysis = False
                else:
                    view_analysis_dict["withanalysis"]["name"] = "Wits Analysis"
                    view_analysis_dict["withanalysis"]["value"] = result_json["Wits Analysis"]

                if not report_obj.options.filter(name="Downs Analysis"):
                    result_json.pop("Downs Analysis") if "Downs Analysis" in result_json.keys() else print("AA")
                    downsanalysis = False
                else:
                    view_analysis_dict["downsanalysis"]["name"] = "Downs Analysis"
                    view_analysis_dict["downsanalysis"]["value"] = result_json["Downs Analysis"]

                view_analysis_status_dict = {"bjork": Bjork, "skeletal": Skeletal, "withanalysis": withanalysis, "downsanalysis": downsanalysis}

                return view_analysis_dict, view_analysis_status_dict
            view_analysis_returned_dict, view_analysis_status_dict = view_analysis_function()
        
        info_options_dict = {
            "doctor_note_info_option": doctor_note_info_option,
            "patient_info_option": patient_info_option,
            "radiography_info_option": radiography_info_option,
            "drawed_radiography_info_option": drawed_radiography_info_option,
            "treatment_plan_info_option": treatment_plan_info_option,
            "signature_option": signature_option,
            "view_analysis": view_analysis_status_dict}
        context = {
            # "qr_code_url": report_obj.qr_code.url,
            "patient_infos": patient_infos,
            "image_report_infos": image_report_infos,
            "doctor_notes_infos": doctor_notes_infos,
            "signature_infos": signature_infos,
            "clinic_logo": clinic_logo,
            "labels_colors_on_radiography": labels_colors_on_radiography,
            "info_options_dict": info_options_dict,
            "treatment_plans": treatment_plan_infos,
            "Sections": labels_with_descriptions,
            "dental_dict": dental_dict,
            "view_analysis_returned_dict": view_analysis_returned_dict,
            "specs": specs,
            "arabic_status": arabic_status,
        }
        return render(request, 'report.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


class AddPanel:
    
    @login_required
    def addDoctorOwnCompany(request):
        if request.method == "GET":
            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_distributor = profile.is_distributor
                is_owner_of_company = True if profile.is_owner_of_company else False
                is_admin = True if user.is_superuser else False
                company = profile.company
                user_theme_dict = user_theme_choices(user)

                context = {
                    "user_theme_choices_json": json.dumps(user_theme_dict),
                    "user_theme_choices": user_theme_dict,
                    "theme": user_theme_dict["color"],
                    "specs": specs,
                    "company": company,
                    "active_page_name": "addDoctorOwnCompany",
                    "user_type": {
                        "is_admin": is_admin, 
                        "is_owner_of_company": is_owner_of_company,
                        "is_distributor": is_distributor},

                }
                return render(request, 'adduser/add-doctor-to-company.html', context=context)

            except Exception as e:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def addDoctorDifferentCompany(request):
        if request.method == "GET" and request.user.is_superuser:
            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_owner_of_company = True if profile.is_owner_of_company else False
                is_admin = True if user.is_superuser else False
                company = profile.company
                user_theme_dict = user_theme_choices(user)
                company_dict = {}
                if request.user.is_superuser:
                    try:                
                        companys = Company.objects.all().order_by("-id").only("id", "name")
                        for company in companys:
                            company_dict[company.id] = {
                                "name": company.name,
                                } 
                    except:
                        traceback.print_exc()

                context = {
                    "user_theme_choices_json": json.dumps(user_theme_dict),
                    "user_theme_choices": user_theme_dict,
                    "theme": user_theme_dict["color"],
                    "specs": specs,
                    "company": company,
                    "active_page_name": "addDoctorDifferentCompany",
                    "user_type": {"is_admin": is_admin, "is_owner_of_company": is_owner_of_company},
                    "company_dict": company_dict
                }
                return render(request, 'adduser/add-doctor-to-different-company.html', context=context)

            except Exception as e:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def addDistributor(request):
        if request.method == "GET" and request.user.is_superuser:
            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_owner_of_company = True if profile.is_owner_of_company else False
                is_admin = True if user.is_superuser else False
                company = profile.company
                user_theme_dict = user_theme_choices(user)
                tokens = ThakaaTokenBar.objects.all().order_by("token")

                context = {
                    "user_theme_choices_json": json.dumps(user_theme_dict),
                    "user_theme_choices": user_theme_dict,
                    "theme": user_theme_dict["color"],
                    "specs": specs,
                    "company": company,
                    "tokens": tokens,
                    "active_page_name": "AddDistributor",
                    "user_type": {"is_admin": is_admin, "is_owner_of_company": is_owner_of_company},
                }
                return render(request, 'adduser/add-distributor.html', context=context)
            
            except:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def addCompanyDoctor(request):
        if request.method == "GET" and request.user.is_superuser:
            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_owner_of_company = True if profile.is_owner_of_company else False
                is_admin = True if user.is_superuser else False
                company = profile.company
                user_theme_dict = user_theme_choices(user)
                tokens = ThakaaTokenBar.objects.all().order_by("token")
                context = {
                    "user_theme_choices_json": json.dumps(user_theme_dict),
                    "user_theme_choices": user_theme_dict,
                    "theme": user_theme_dict["color"],
                    "specs": specs,
                    "company": company,
                    "active_page_name": "addCompanyDoctor",
                    "user_type": {"is_admin": is_admin, "is_owner_of_company": is_owner_of_company},
                    "tokens": tokens
                }
                return render(request, 'adduser/add-company-and-doctor.html', context=context)

            except:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)
    
    @login_required
    def addDemoUser(request):
        if request.method == "GET" and request.user.is_superuser:
            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_owner_of_company = True if profile.is_owner_of_company else False
                is_admin = True if user.is_superuser else False
                company = profile.company
                user_theme_dict = user_theme_choices(user)
                company_dict = {}
                context = {
                    "user_theme_choices_json": json.dumps(user_theme_dict),
                    "user_theme_choices": user_theme_dict,
                    "theme": user_theme_dict["color"],
                    "specs": specs,
                    "company": company,
                    "active_page_name": "addDemoUser",
                    "user_type": {"is_admin": is_admin, "is_owner_of_company": is_owner_of_company},
                    "company_dict": company_dict
                }
                return render(request, 'adduser/add-demo-user.html', context=context)

            except:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def DistributorAddsUser(request):
        if request.method == "GET":

            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_distributor = profile.is_distributor
                if is_distributor:
                    is_owner_of_company = True if profile.is_owner_of_company else False
                    is_admin = True if user.is_superuser else False
                    company = profile.company
                    user_theme_dict = user_theme_choices(user)
                    tokens = ThakaaTokenBar.objects.all().order_by("token")

                    context = {
                        "user_theme_choices_json": json.dumps(user_theme_dict),
                        "user_theme_choices": user_theme_dict,
                        "theme": user_theme_dict["color"],
                        "specs": specs,
                        "company": company,
                        "tokens": tokens,
                        "active_page_name": "DistributorAddsUser",
                        "user_type": {
                            "is_admin": is_admin, 
                            "is_owner_of_company": is_owner_of_company, 
                            "is_distributor": is_distributor},
                    }
                    return render(request, 'adduser/distributor-adds-user.html', context=context)
            
            except:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)

    @login_required
    def DistributorAddsUserToCompany(request):
        if request.method == "GET":
            try:
                user = request.user
                specs = get_specs()
                profile = Profile.objects.get(user=user)
                is_distributor = profile.is_distributor
                print("AAAAAAAAAAAAA")
                if is_distributor:
                    is_owner_of_company = True if profile.is_owner_of_company else False
                    is_admin = True if user.is_superuser else False
                    company = profile.company
                    user_theme_dict = user_theme_choices(user)
                    tokens = ThakaaTokenBar.objects.all().order_by("token")
                    distributor_profiles = Profile.objects.select_related("company").filter(added_by_distributor=profile)
                    company_dict = {}
                    try:                
                        for distributor_profile in distributor_profiles:
                            profile_company = distributor_profile.company
                            company_dict[profile_company.id] = {
                                "name": profile_company.name,
                                } 
                    except:
                        traceback.print_exc()
                    context = {
                        "user_theme_choices_json": json.dumps(user_theme_dict),
                        "user_theme_choices": user_theme_dict,
                        "theme": user_theme_dict["color"],
                        "specs": specs,
                        "company": company,
                        "tokens": tokens,
                        "company_dict": company_dict,
                        "active_page_name": "DistributorAddsUserToCompany",
                        "user_type": {
                            "is_admin": is_admin, 
                            "is_owner_of_company": is_owner_of_company, 
                            "is_distributor": is_distributor},
                    }
                    return render(request, 'adduser/distributor-adds-user-to-company.html', context=context)
            
            except:
                user = request.user
                traceback.print_exc()
                error = traceback.format_exc()
                error_handler_function(user,error)


@login_required
def add_demo_user_page(request):
    try:
        user = request.user
        specs = get_specs()
        profile = Profile.objects.get(user=user)
        is_owner_of_company = False
        is_admin = False
        if profile.is_owner_of_company:
            is_owner_of_company = True
        if user.is_superuser:
            is_admin = True
        packages = ThakaaTokenBar.objects.all() 

        company = profile.company
        time.sleep(0.5) #dil değiştirme isteği tamamlanmadan dicti çektiği için değişen dili değil eski dili getiriyor
        user_theme_dict = user_theme_choices(user)
        context = {
            "packages": packages,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
            "company": company,
            "user_type": {"is_admin": is_admin, "is_owner_of_company": is_owner_of_company, "distributor": profile.is_distributor}
        }
        if is_admin or is_owner_of_company:
            return render(request,'adduser/add-panel.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def send_form_to_patient_page(request, patient_slug=None):
    try:
        patient = Patient.objects.get(slug=patient_slug)
        specs = get_specs()
        logo = patient.user.company.logo.url if patient.user.company.logo else None 
        lang = None
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        
        patient_dict = {
            "full_name": patient.first_name + " " + patient.last_name,
            "slug": patient.slug,
            "logo":logo,
            "doctor_id":patient.user.user.id,
        }
        image_type_dict = {}
        
        def upload_radiography_function():
            image_types = ImageType.objects.all().order_by("id")

            for image_type_obj in image_types:
                image_type_dict[image_type_obj.id] = image_type_obj.name
            cbct_value = image_type_dict.pop(3)
            image_type_dict[3] = cbct_value

            return image_type_dict
            
        image_type_dict = upload_radiography_function()
        context = {
            "image_type_dict": image_type_dict,
            "patient_dict": json.dumps(patient_dict),
            "lang":lang,
            "specs": specs,
        }
        
        return render(request, 'deneme.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def buy(request, course_hash):
    specs = get_specs()
    return render(request, 'odeme.html', context = {
        "package": UsagePackage.objects.get(key=course_hash),
        "course_hash": course_hash,
        "specs":specs,
    })


def success_buy(request):
    specs = get_specs()
    return render(request, "succes-buy.html", context={"specs": specs})


@login_required
def list_users(request):
    try:
        login_user = request.user
        user_theme_dict = user_theme_choices(login_user)
        specs = get_specs()
        responsible_profile = Profile.objects.get(user=login_user)
        if login_user.is_superuser or responsible_profile.is_distributor:
            profiles = Profile.objects.select_related("user").all() if not responsible_profile.is_distributor else Profile.objects.select_related("user").filter(added_by_distributor=responsible_profile)
            users_list = []
            for profile in profiles:
                image_reports = None
                patient_len_for_limit = None
                images_len = None
                try:
                    token_informations = remaining_token(profile_obj=profile, detailed_status=False)
                except:
                    token_informations = None
                    user = request.user
                    traceback.print_exc()
                    error = traceback.format_exc()
                    error_handler_function(user,error)
                print("profile", profile)
                print("token_informations", token_informations)
                user_dict = {
                    "id": profile.user.id,
                    "username": profile.user.username,
                    "name": profile.user.first_name + " " + profile.user.last_name,
                    "created_date": str(profile.user.date_joined.date()), "profile_id": profile.id,
                    "is_active": profile.user.is_active,
                    "user_type": "Distributor" if profile.is_distributor else profile.user_type,
                    "last_login": str(profile.user.last_login.date()) if profile.user.last_login else "-",
                    "usage": token_informations['package']['total_usage'] if "package" in token_informations.keys() and "total_usage" in token_informations["package"].keys() else "-",
                    "usage_limit": token_informations['package']['limit'] if "package" in token_informations.keys() and "limit" in token_informations["package"].keys() else "-",
                    "last_token_activity": token_informations['package']['last_token_activity'] if "package" in token_informations.keys() and "last_token_activity" in token_informations["package"].keys() else "-",
                    "active": profile.user.is_active,
                    "package_start_end_date": f"{token_informations['package']['start_date'] if 'package' in token_informations.keys() and 'start_date' in token_informations['package'].keys() else '-'} - {token_informations['package']['end_date'] if 'package' in token_informations.keys() and 'end_date' in token_informations['package'].keys() else '-'}",
                    }
                users_list.append(user_dict)
        
        context = {
            'users_list': users_list, 
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
            }
        return render(request, 'list-users.html', context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def view_user(request,id):
    try:
        user = request.user
        user_obj = User.objects.get(id=id)
        profile_obj = Profile.objects.get(user=user_obj)
        current_token = ThakaaBuyedToken.objects.filter(company=profile_obj.company).last()
        priorited_profile = Profile.objects.get(user=user)
        
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        thakaa_token = ThakaaTokenBar.objects.all()
        time.sleep(0.5) #dil değiştirme isteği tamamlanmadan dicti çektiği için değişen dili değil eski dili getiriyor
        context = {
            'user_obj':user_obj,
            'profile_obj':profile_obj,
            'packages':thakaa_token,
            'current_token': current_token,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
        }
        if user.is_superuser or priorited_profile.is_distributor:
            return render(request,'view-users.html', context)
        
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def company_form_page(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        specs = get_specs()
        time.sleep(0.4)
        user_theme_dict = user_theme_choices(user)
        questions = get_questions_with_json()
        is_form_exists = FormWithCompany.objects.filter(company=profile.company)
        form_obj = FormWithCompany.objects.filter(company=profile.company).first()
        if form_obj:
            slug = form_obj.form_slug
        else:
            slug = None
        full_name = user.first_name + " " + user.last_name
        first_name = user.first_name
        user_theme_dict["color"] = "white"
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "questions":questions,
            "is_form_exists":is_form_exists,
            'full_name':full_name,
            'first_name':first_name,
            "slug":slug,
            "specs": specs,
            "patient_form_link": patient_form_link, 
        }
        if user.is_superuser:
            return render(request, "company-form.html",context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def clinic_form_page_to_patients(request,slug):
    try:
        print("slug", slug)
        specs = get_specs()
        clinic_questions = FormWithCompany.objects.filter(form_slug=slug, is_active=True).order_by("id")
        print("clinic questions", clinic_questions)
        for_logo = FormWithCompany.objects.filter(form_slug=slug).first()
        company = for_logo.company
        logo = company.logo
        questions = []
        for clinic_question in clinic_questions:
            form_question = clinic_question.question
            if form_question.answers:
                form_question.answers = json.loads(form_question.answers)
            if form_question.answers_tr:
                form_question.answers_tr = json.loads(form_question.answers_tr)
            form_question.required = clinic_question.required
            questions.append(form_question)
        
        context = {
            'questions': questions,
            'slug':slug,
            'logo_for_form':logo,
            "specs": specs
        }
        return render(request, 'clinic-form-page-to-patients.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def list_forms(request):
    try:
        print("here")
        user = request.user
        profile = Profile.objects.get(user=user)
        specs = get_specs()
        form_with_company_objects = FormWithCompany.objects.filter(company=profile.company)
        print("form with company objects", form_with_company_objects)
        form_answers = FormAnswers.objects.filter(form__in=form_with_company_objects).order_by("-id")
        print("form answers", form_answers)
        for form_answer in form_answers:
            if form_answer.question_slug == "e3232c195e09412bab7e3344560e9e63":
                print("isim: ", form_answer.answer)
        form_questions = get_questions_with_json()
        form_data = defaultdict(list)
        user_theme_dict = user_theme_choices(user)
        count = 0
        for answer in form_answers:
            group_slug = answer.group_slug
            question_slug = answer.question_slug
            form_question = None
            for question in form_questions:
                if question.slug == question_slug:
                    form_question = question
                    form_question_slug = question.slug
                    if question.answers:
                        form_question_answer = question.answers
                        if isinstance(form_question_answer, dict):
                            answer_value = form_question_answer.get(answer.answer)
                    else:
                        answer_value = answer.answer
                    break
                    
            if form_question is None:
                continue

            question = form_question.question
            date = answer.date
            date = date.strftime("%d-%m-%Y")
            answer_dict = {
                'question': question,
                'answer': answer_value if answer_value else "",
                'slug': form_question_slug,
                'date':date
                
            }
            form_data[group_slug].append(answer_dict)

        print("count", count)
        
        new_dict = {}
        for group_slug, answers in form_data.items():
            if group_slug not in new_dict:
                new_dict[group_slug] = []  # Yeni bir boş liste oluştur

            for answer in answers:
                new_dict[group_slug].append(answer)
        context = {
            'form_data': form_data,
            'new_dict':new_dict,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
        }
        print("context", context)

        return render(request, 'list-forms.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def patient_form_detail(request, slug):
    try:
        image_type_dict = {}
        specs = get_specs()
        patient_answers = FormAnswers.objects.filter(group_slug=slug)
        radiography_obj = FormRadiographs.objects.filter(form_answer_group_slug=slug).first()
        if radiography_obj:
            radiography = {"id": radiography_obj.id, "path": radiography_obj.path.url}
        else:
            radiography = None
        print("radiography_obj: ", radiography_obj, radiography_obj.path.url)
        user = request.user
        profile = Profile.objects.get(user=user)
        clinic_questions = FormWithCompany.objects.filter(company=profile.company, is_active=True).order_by("id")
        
        clinic_form = FormWithCompany.objects.filter(company=profile.company).first()
        
        questions = {}
        for clinic_question in clinic_questions:
            form_question = clinic_question.question

            if form_question.answers:
                form_question.answers = json.loads(form_question.answers)
            if form_question.answers_tr:
                form_question.answers_tr = json.loads(form_question.answers_tr)

            form_question.required = clinic_question.required

            # Hasta yanıtlarını al
            form_answers = patient_answers.filter(question_slug=clinic_question.question.slug)
            print("form answers: ", form_answers)
            answers_dict = {}
            if form_answers:
                answer = form_answers[0]
                if form_question.id == 37:
                    answers = []
                    specify = ""
                    for answer in form_answers:
                        answers.append(answer.answer)
                        if answer.specify:
                            specify = answer.specify
                    answers_dict = {
                        'question_id': form_question.id,
                        'question': form_question.question,
                        'question_tr': form_question.question_tr,
                        'question_answers': form_question.answers if form_question.answers else {},
                        'question_answers_tr': form_question.answers_tr if form_question.answers_tr else {},
                        'answers': json.dumps(answers),
                        'specifies': specify,
                        'slug': form_question.slug,
                        'date': answer.date if answer.date else ""  # Burada birden fazla cevap olduğu için tarih bilgisini nasıl yönetmek istediğinize göre düzenleme yapabilirsiniz
                    }
                else:
                    answer = form_answers[0]
                    answers_dict = {
                        'question_id': form_question.id,
                        'question': form_question.question,
                        'question_tr': form_question.question_tr,
                        'question_answers': form_question.answers if form_question.answers else {},
                        'question_answers_tr': form_question.answers_tr if form_question.answers_tr else {},
                        'answer': answer.answer,
                        'specifies': answer.specify if answer.specify else None,
                        'slug': form_question.slug,
                        'date': answer.date if answer.date else ""
                    }
            if "b1e47ae3e5d948c389e8d53f4e3cd745" in form_question.slug:
                continue
            if answers_dict:
                questions[form_question.slug] = answers_dict


                # # Sorunun cevapları JSON formatında ise
                # if form_question.answers:
                #     answers_dict['question_answers'] = json.dumps(form_question.answers)
                # if form_question.answers_tr:
                #     answers_dict['question_answers_tr'] = json.dumps(form_question.answers_tr)
        print("questionsss",questions)

        def upload_radiography_function():
            image_types = ImageType.objects.all().order_by("id")

            for image_type_obj in image_types:
                image_type_dict[image_type_obj.id] = image_type_obj.name

            cbct_value = image_type_dict.pop(3)
            image_type_dict[3] = cbct_value
            return image_type_dict

        user_theme_dict = user_theme_choices(user)
        image_type_dict = upload_radiography_function()
        context = {
            'questions': questions,
            'slug': slug,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "radiography":radiography,
            "image_type_dict":image_type_dict,
            "specs": specs
        }

        
        return render(request, 'patient-form-detail.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def cephalometric_page(request,image_report_id):
    try:
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        user = request.user
        specs = get_specs()
        image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id, image__archived=False)
        #hasta ad,yaş ve radyografi tarihi alma
        page_name = request.path
        has_page_name_cephalometric = 'cephalometric' in page_name
        patient_obj = image_report_obj.image.patient
        birthday = patient_obj.date_of_birth
        today_for_age = date.today()
        profile = Profile.objects.get(user=user)
        patient_age = today_for_age.year - birthday.year if birthday else None
        patient_gender = patient_obj.gender if patient_obj.gender else None
        patient_full_name = patient_obj.first_name + " " + patient_obj.last_name
        patient_email = patient_obj.email
        radiography_create_date = image_report_obj.created_date + timedelta(hours=3)
        radiography_create_date = radiography_create_date.strftime("%d.%m.%Y %H:%M")
        if patient_obj.user != profile:
            messages.warning(request, "Hastanın doktoru değilsiniz.")
            return HttpResponseRedirect(reverse('patientsPage'))
        ###
        ### doktor not kısmı ###
        doctor_note = image_report_obj.note
        ####
        image_type = image_report_obj.image.type.name
        illness_dict = {}
        radiography_section_dict = {}
        other_radiographys_section_dict = {}
        image_type_dict = {}
        ceph_analysis_types_dict = {}
        view_angle_dict = {}
        view_spline_points_dict = {}
        calibration_status = 'False'

        def view_analysis_function():
            if image_report_obj.result_json:
                result_json = json.loads(image_report_obj.result_json)
                view_analysis_dict = result_json["results"]["analysis_types"] if "results" in result_json.keys() and "analysis_types" in result_json["results"].keys() else None
                calibration_status = result_json["calibration_status"] if "calibration_status" in result_json.keys() else 'False'
                view_angle_dict = result_json["results"]["angle_planes"] if "results" in result_json.keys() and "angle_planes" in result_json["results"].keys() else None
                view_spline_points_dict = result_json["results"]["spline_points"] if "results" in result_json.keys() and "spline_points" in result_json["results"].keys() else None
                print("viewww", view_spline_points_dict)

            return view_analysis_dict, calibration_status, view_angle_dict, view_spline_points_dict
        
        # Radiography için sözlük hazırlanan fonksiyon
        def radiography_section_function():

            image_path = image_report_obj.image.path.url

            radiography_section_dict["image_path"] = image_path
            return radiography_section_dict

        # middle radiography area
        def other_radiographys_function():
            radiographys = Image.objects.filter(patient=patient_obj).order_by("-id")
            radiography_dict = {} 
            for radiography in radiographys:
                try:
                    image_report_last_obj = ImageReport.objects.filter(image=radiography, image__archived=False).last()
                    status1 = "2"
                    status2 = "2"
                    if image_report_last_obj and image_report_last_obj.is_done and not image_report_last_obj.is_error:
                        status1 = "completed"
                        status2 = "success"
                    elif image_report_last_obj and image_report_last_obj.is_error:
                        status1 = "not-completed"
                        status2 = "error"
                    else:
                        status1 = "not-completed"
                        status2 = "error"
                    # if radiography:
                    #     radiography_image = radiography.thumbnail_image_path.url if radiography.thumbnail_image_path else radiography.path.url if radiography.path else None
                    # else:
                    #     radiography_image = None

                    if radiography.thumbnail_image_path:
                            radiography_image = radiography.thumbnail_image_path.url
                    elif radiography.type.name == "CBCT" and not radiography.path and not radiography.thumbnail_image_path:
                        radiography_image = f"/media/dental/radio/{lang}3d.png"
                    else:
                        radiography_image = radiography.path.url

                    last_obj_id = None
                    dynamic_href = None
                    if image_report_last_obj:
                        last_obj_id = image_report_last_obj.id
                        if image_report_last_obj.name == "Lateral Cephalometric":
                            dynamic_href = f"/{lang}/cephalometric/{image_report_last_obj.id}"
                        elif image_report_last_obj.name == "CBCT":
                            dynamic_href = f"/{lang}/CBCT/{image_report_last_obj.id}"
                        else:
                            dynamic_href = f"/{lang}/diagnosis/{image_report_last_obj.id}"
                    radiography_dict[last_obj_id] = {
                        "path": radiography_image,
                        "status1": status1,
                        "status2": status2,
                        "image_id": radiography.id,
                        "date": image_report_last_obj.updated_date.strftime("%d/%m/%Y") if image_report_last_obj else None,
                        "href": dynamic_href
                    }
                except:
                    continue
            
            other_radiographys_section_dict["radiography"] = radiography_dict
            return other_radiographys_section_dict

        def upload_radiography_function():
            image_types = ImageType.objects.all().order_by("id")

            for image_type_obj in image_types:
                image_type_dict[image_type_obj.id] = image_type_obj.name

            cbct_value = image_type_dict.pop(3)
            image_type_dict[3] = cbct_value
            return image_type_dict

        def doctor_choices_for_report_function():
            profile = Profile.objects.get(user=user)
            doctor_choices = DoctorChoicesForReport.objects.filter(profile=profile).first()
            if doctor_choices:
                doctor_choices_dict = {
                    'format':doctor_choices.format,
                    'filter_report_based':doctor_choices.filter_report_based,
                    'patient_infos': doctor_choices.choices.filter(name='patient_infos').exists(),
                    'undrawed_radiography': doctor_choices.choices.filter(name='radiography_infos').exists(),
                    'drawed_radiography': doctor_choices.choices.filter(name='drawed_radiography_infos').exists(),
                    'selected_drawed_radiography':doctor_choices.choices.filter(name='draw_with_selected_labels').exists(),
                    'all_drawed_radiography':doctor_choices.choices.filter(name='draw_with_all_labels').exists(),
                    'draw_numbering': doctor_choices.choices.filter(name='draw_numbering').exists(),
                    'doctor_note': doctor_choices.choices.filter(name='doctor_note_infos').exists(),
                    'view_analysis': doctor_choices.choices.filter(name='lateral_view_analysis_infos').exists(),
                    'bjork': doctor_choices.choices.filter(name='Bjork-Jarabak Analysis').exists(),
                    'skeletal': doctor_choices.choices.filter(name='Skeletal Factors - Anterior/Posterior').exists(),
                    'withanalysis': doctor_choices.choices.filter(name='Wits Analysis').exists(),
                    'downsanalysis': doctor_choices.choices.filter(name='Downs Analysis').exists(),
                    'doctor_signature': doctor_choices.choices.filter(name='signature').exists(),
                    'treatment_plannings': doctor_choices.choices.filter(name='treatment_plans').exists(),
                }
            else:
                doctor_choices_dict = None
            return doctor_choices_dict

        # Rapor oluştur ve mail gönderdeki analizlerin dinamik olarak getirilmesi için hazırlanan fonksiyon --> js de işlem yaptırıldığı için idlerinin 3 ten başlaması gerekiyor
        def report_page_spesification_of_dynamic_analysis_types():
            for index, analysis_type_name in enumerate(view_analysis_dict):
                ceph_analysis_types_dict[index+3] = analysis_type_name

            return ceph_analysis_types_dict


        # run the functions
        view_analysis_dict, calibration_status, view_angle_dict, view_spline_points_dict = view_analysis_function()
        radiography_section = radiography_section_function()
        other_radiographys_section = other_radiographys_function()
        user_theme_dict = user_theme_choices(user)
        image_type_dict = upload_radiography_function()
        doctor_choices_dict=doctor_choices_for_report_function()
        ceph_analysis_types_dict = report_page_spesification_of_dynamic_analysis_types()
        
        context = {
            "radiography_section": radiography_section,
            "other_radiographys_section": other_radiographys_section,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "image_report_id": image_report_id,
            "illness_dict": illness_dict,
            "image_type": image_type,
            "image_type_dict": image_type_dict,
            "patient_age":patient_age,
            "patient_gender": patient_gender,
            "patient_full_name":patient_full_name,
            "patient_email":patient_email,
            "has_page_name_cephalometric":has_page_name_cephalometric,
            "radiography_create_date":radiography_create_date,
            "doctor_note":doctor_note,
            "doctor_choices_dict":doctor_choices_dict,
            "lateral_cephalometric_dict": json.dumps(lateral_cephalometric_dict),
            "view_analysis_dict": view_analysis_dict,
            "view_analysis_dict_str": json.dumps(view_analysis_dict),
            "view_angle_dict_str": json.dumps(view_angle_dict),
            "view_spline_points_dict": json.dumps(view_spline_points_dict),
            "ceph_analysis_types_dict": ceph_analysis_types_dict,
            "specs": specs,
            "calibration_status": calibration_status,
        }
        return render(request,'cephalometric-page.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def list_activities(request,id):
    try:
        user = request.user
        user_obj = User.objects.get(id=id)
        profile_obj = Profile.objects.get(user=user_obj)
        token_activities = ThakaaTokenActivity.objects.filter(profile=profile_obj)
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        time.sleep(0.5) #dil değiştirme isteği tamamlanmadan dicti çektiği için değişen dili değil eski dili getiriyor
        token_activities_list = []
        for i in token_activities:
            token_activities_list.append({
                "used_token": i.used_token,
                "image_type": i.image_type,
                "date": (i.date + timedelta(hours=3)).strftime('%Y.%m.%d %H:%M')
            })
        context = {
            'token_activities': token_activities_list,
            'user_obj':user_obj,
            'profile_obj':profile_obj,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
        }
        if user.is_superuser:
            return render(request,'list_activities.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def demo_accounts_list_page(request):
    try:
        user = request.user
        if user.is_superuser:
            specs = get_specs()
            user_theme_dict = user_theme_choices(user)
            demo_accs = ThakaaRemainingToken.objects.filter(thakaa_buyed_token__tokenbar__slug = "demo_token", is_expired=False).order_by("-id")
            demo_account_infos = []
            demo_acc_count = 0
            if "/en/" in request.build_absolute_uri():
                lang = "en"
            else:
                lang = "tr"
            for acc in demo_accs:
                creation_date = acc.thakaa_buyed_token.start_date + timedelta(hours=3)
                creation_date = creation_date.strftime("%d/%m/%Y %H:%M")
                renewal_date = acc.renewal_date + timedelta(hours=3)
                renewal_date = renewal_date.strftime("%d/%m/%Y %H:%M")     

                acc_dict = {
                "company":acc.thakaa_buyed_token.company.name if acc.thakaa_buyed_token.company.name else "-",
                "company_mail":acc.thakaa_buyed_token.company.email if acc.thakaa_buyed_token.company.email else "-",
                "company_phone":acc.thakaa_buyed_token.company.phone if acc.thakaa_buyed_token.company.phone else "-",
                "given_token":acc.thakaa_buyed_token.tokenbar.token if acc.thakaa_buyed_token.tokenbar.token else "-",
                "creation_date":creation_date,
                "date_renewed":renewal_date,
                "monthly_usage":acc.usage if acc.usage else "-" ,
                "total_usage":acc.total_usage if acc.total_usage else "-",
                }
                demo_account_infos.append(acc_dict)
                demo_acc_count += 1
            context = {
                "user_theme_choices_json": json.dumps(user_theme_dict),
                "user_theme_choices": user_theme_dict,
                "theme": user_theme_dict["color"],
                "specs": specs,
                "demo_account_infos":demo_account_infos,
                "demo_acc_count":demo_acc_count,
            }
            return render(request, 'dashboard/demo-accounts.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def analysis_list_page(request):
    try:
        user = request.user
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        profile_obj = Profile.objects.get(user=user)
        if profile_obj.is_distributor:
            all_analysis = ImageReport.objects.filter(
            Q(user__added_by_distributor=profile_obj) | Q(user=profile_obj)
        ).order_by("-id")
        else:
            all_analysis = ImageReport.objects.filter().order_by("-id")
        analysis_infos = []
        analysis_count = 0
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        for analysis in all_analysis:
            if lang == "tr":
                created_date = analysis.created_date + timedelta(hours=3)
                created_date = created_date.strftime("%d/%m/%Y %H:%M")
                updated_date = analysis.updated_date + timedelta(hours=3)
                updated_date = updated_date.strftime("%d/%m/%Y %H:%M")
            else:
                updated_date = analysis.updated_date.strftime("%d/%m/%Y %H:%M")            
                created_date = analysis.created_date.strftime("%d/%m/%Y %H:%M")            
            analysis_dict = {
            "company": analysis.user.company.name,
            "user": analysis.user.user.first_name + " " + analysis.user.user.last_name,
            "phone": analysis.user.phone,
            "radiography_type": analysis.name,
            "ai_image_type": analysis.ai_response_image_type if analysis.ai_response_image_type else "-",
            "created_date": created_date,
            "updated_date": updated_date,
            "status": "Success" if analysis.is_done else "Error"
            }
            analysis_infos.append(analysis_dict)
            analysis_count += 1
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
            "analysis_infos":analysis_infos,
            "analysis_count":analysis_count,
        }
        if user.is_superuser or profile_obj.is_distributor:
            return render(request, 'dashboard/analysis-list.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def purchase_list_page(request):
    try:
        if not request.user.is_superuser:
            return HttpResponse(status=404)
        purchase_objects = TokenPayment.objects.all()
        info_list = []
        user = request.user
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"
        for obj in purchase_objects:
            date = obj.transaction_date.strftime("%d/%m/%Y %H:%M")            
            status = "Test"
            message = "-"
            if obj.request_payment_details and not obj.redirect_payment_details:
                status = _("Card Error")
            if obj.redirect_payment_details:
                info_dict = obj.redirect_payment_details
                info_dict = info_dict.replace("'",'"')
                info_dict = json.loads(info_dict)
                status = info_dict["isSuccessful"]
                if status == "True":
                    status = _("Successful Payment")
                else:
                    status = _("Fail Payment")
                message = info_dict["resultMessage"]
            info_dict = {
                "slug":obj.slug,
                "full_name":obj.full_name,
                "email":obj.email,
                "phone":obj.phone,
                "company_name":obj.company_name,
                "total_price":obj.total_price,
                "price_per_token":obj.price_per_token,
                "token":obj.token,
                "currency":obj.currency,
                "is_valid":obj.is_valid,
                "OtherTrxCode":obj.OtherTrxCode,
                "code_for_hash":obj.code_for_hash,
                "request_payment_details":obj.request_payment_details,
                "redirect_payment_details":obj.redirect_payment_details,
                "transaction_date":date,
                "payment_date":obj.payment_date,
                "trxCode":obj.trxCode,
                "resultMessage":obj.resultMessage,
                "status":status,
                "message":message,
                "method":obj.payment_method,
            }
            info_list.append(info_dict)
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
            "info_list":info_list,
        }
        return render(request,'dashboard/purchase-list.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def user_activities_list_page(request):
    try:
        profile_obj = Profile.objects.get(user=request.user)
        user_activities = SpecificUserLoginDiary.objects.all().order_by("id")
        if profile_obj.is_distributor:
            users = [activity.user.email for activity in user_activities]
            profiles = Profile.objects.select_related("user").filter(user__email__in=users, added_by_distributor=profile_obj)
            related_users = [profile.user for profile in profiles]
        info_list = []
        user = request.user
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        lang = "en" if "/en/" in request.build_absolute_uri() else "tr"
        for obj in user_activities:
            if profile_obj.is_distributor and obj.user not in related_users: continue
            if lang == "tr":
                login_date = obj.login_date + timedelta(hours=3)
                login_date = login_date.strftime("%d/%m/%Y %H:%M")
                if not obj.logout_date:
                    logout_date = _("Active")
                else:
                    logout_date = obj.logout_date + timedelta(hours=3)
                    logout_date = logout_date.strftime("%d/%m/%Y %H:%M")       
            else:
                if not obj.logout_date:
                    logout_date = _("Active")

                else:
                    logout_date = obj.logout_date.strftime("%d/%m/%Y %H:%M")
                login_date = obj.login_date.strftime("%d/%m/%Y %H:%M")
            user = obj.user
            profile = Profile.objects.get(user=user)
            info_dict = {
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email":user.email,
                "company":profile.company.name,
                "login_date":login_date,
                "logout_date":logout_date,
            }
            info_list.append(info_dict)
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "specs": specs,
            "info_list":info_list,
        }
        return render(request,'dashboard/user-login-logout-activities.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

# views.py (örnek bir view dosyası)

# from rest_framework.views import APIView
# from Application.permissions import IPWhitelistPermission

# class MyAPIView(APIView):
#     permission_classes = [IPWhitelistPermission]

#     def get(self, request):
#         # API view işlemleri...
#         pass

def signup_page(request):
    specs = get_specs()
    print("request.user", request.user, type(request.user))
    if clinic_project_id != 2:
        return HttpResponseRedirect(reverse('patientsPage'))
    if not str(request.user) == "AnonymousUser":
        return HttpResponseRedirect(reverse('patientsPage'))
    packages = ThakaaTokenBar.objects.filter(slug="demo_token")
    time.sleep(0.5) #dil değiştirme isteği tamamlanmadan dicti çektiği için değişen dili değil eski dili getiriyor
    context = {
        'packages':packages,
        "specs": specs,
    }
    print(context)
    return render(request,'sign-up.html',context)

@login_required
def homepage(request):
    try:
        user=request.user
        specs = get_specs()
        user_theme_dict = user_theme_choices(user)
        if request.method == "POST":
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            period = request.POST.get("period")
            print(f"start_date: {start_date} -- end_date: {end_date} -- period:{period}")
            panaromic, bitewing, periapical, cbct, lateral = for_user_radiography_type_counts_with_date(user,start_date,end_date,period)
            patient_count = for_user_total_patient_count_with_date(user,start_date,end_date,period)
            user_count = for_user_total_user_count_with_date(user,start_date,end_date,period)
            radiography_count = for_user_total_uploaded_radiography_with_date(user,start_date,end_date,period)
            anaylse_count = for_user_total_analyse_count_with_date(user,start_date,end_date,period)
            radiography_type_count_dict = {
                "Panaromic":panaromic,
                "Bitewing":bitewing,
                "Periapical":periapical,
                "CBCT":cbct,
                "Lateral Cephalometric":lateral,
            }
            context = {
                "specs":specs,
                "user_theme_choices_json": json.dumps(user_theme_dict),
                "user_theme_choices": user_theme_dict,
                "radiography_type_count_dict":json.dumps(radiography_type_count_dict),
                "patient_count":patient_count,
                "user_count":user_count,
                "radiography_count":radiography_count,
                "analysis_count":anaylse_count,
            }
            return JsonResponse({'status':200, 'data':context})
        else:
            panaromic, bitewing, periapical, cbct, lateral = for_user_radiography_type_counts(user)
            patient_count = for_user_total_patient_count(user)
            radiography_count = for_user_total_uploaded_radiography(user)
            anaylses_by_months = for_user_analyses_by_months(user)
            analyse_count = for_user_total_anaylse_count(user)
            radiography_type_count_dict = {
                "Panaromic":panaromic,
                "Bitewing":bitewing,
                "Periapical":periapical,
                "CBCT":cbct,
                "Lateral Cephalometric":lateral,
            }
            print("radiography_type_count_dict",radiography_type_count_dict)
            context = {
                "specs":specs,
                "user_theme_choices_json": json.dumps(user_theme_dict),
                "user_theme_choices": user_theme_dict,
                "radiography_type_count_dict":json.dumps(radiography_type_count_dict),
                "patient_count":patient_count,
                "radiography_count":radiography_count,
                "anaylses_by_months":json.dumps(anaylses_by_months),
                "analysis_count":analyse_count,
            }
            return render(request,'homepage_dashboard_for_users.html',context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

def get_language(request):
    uri = request.build_absolute_uri()
    languages = {"tr": "tr/", "uz": "uz/", "ru": "ru/", "nl": "nl/"}

    for lang_code, lang_path in languages.items():
        if lang_path in uri:
            return lang_code

    return "en"
def treatment_pricing_for_company_page(request):
    try:
        lang = get_language(request)
        user = request.user
        profile = Profile.objects.get(user=user)
        company = profile.company
        treatments = TreatmentNamesForWizard.objects.all()
        treatment_dict = {}

        for treatment in treatments:
            company_pricing = CompanyTreatmentPricing.objects.filter(company=company, treatment_method=treatment).first()
            if company_pricing:
                treatment_name = getattr(company_pricing.treatment_method, f"{lang}_name")
                treatment_slug = company_pricing.treatment_method.slug
                price = company_pricing.price
            else:
                treatment_name = getattr(treatment, f"{lang}_name", treatment.en_name)
                treatment_slug = treatment.slug
                price = ""

            treatment_dict[treatment_name] = {"slug": treatment_slug, "price": price}

        context = {
            "specs": get_specs(),
            "user_theme_choices_json": json.dumps(user_theme_choices(user)),
            "user_theme_choices": user_theme_choices(user),
            "treatment_dict": treatment_dict,
        }
        print("treatment_dict",treatment_dict)
        return render(request, 'treatment-pricings-for-company.html', context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user, error)
