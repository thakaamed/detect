from PIL import Image as PILImage
from io import BytesIO
import threading
from datetime import datetime, timedelta
import time
from Application.functions import *
from Application.models import *
import json
from django.utils.translation import gettext as _
from django.conf import settings
from Server.settings import ccclinic_path, image_path_without_slash_after_media, company_api_key, AIServerUrl
import traceback
# from User.token_operations import spend_token as thakaa_spend_token
# from User.token_operationsv2 import spend_token as cranio_spend_token
from User.token_operationsv2 import spend_token as thakaa_spend_token
import urllib.request
from django.contrib.auth.decorators import login_required
from Application.functions import error_handler_function


def start_analyze_thread(image_report, image_path, image_path_exists, user):
    url = f"{AIServerUrl}/api/v1.9/analyze/radiography/"
    print("ai server url",AIServerUrl)
    if image_path_exists:
        path = ccclinic_path + image_path
        files = {'image': open(path, 'rb')}
    else:
        image_url = f"{AIServerUrl}/media" + image_path
        response = requests.get(image_url)
        files = {}
        if response.status_code == 200:
            image = PILImage.open(BytesIO(response.content))
            new_image_path = image_path_without_slash_after_media + image_path
            image.save(new_image_path)
            files = {'image': open(new_image_path, 'rb')}
        else:
            print("Resim indirilemedi.")
    data = {'company.api_key': company_api_key, 'request_user': user.username}

    if image_report.image.type:
        image_type = image_report.image.type.ai_type_id
        data["rt_id"] = image_type
        
    ai_post_response = requests.post(url, files=files, data=data)
    ai_post_response_json = ai_post_response.json()
    results_json = {}
    # ANALİZ DURUMUNU KONTROL EDEN YER
    if ai_post_response_json['status']:
        time_now = datetime.now()
        time_control = time_now + timedelta(minutes=3)
        response_url = ai_post_response_json['results']
        ai_get_response = requests.request('GET', response_url)
        ai_get_response_json = ai_get_response.json()
        while not datetime.now() > time_control:
            ai_get_response = requests.request('GET', response_url)
            ai_get_response_json = ai_get_response.json()
            if ai_get_response_json['is_done'] and not ai_get_response_json['error_status']:
                results_json = ai_get_response_json['results']
                break
            print("Analiz henüz tamamlanmadı...")
            time.sleep(3)
            print("Analiz bekleniyor...")
        print("ANALİZ TAMAMLANDI!")
        slug = ai_get_response_json["id"]
        image_report.slug = slug
        image_report.save()
        if 'tooth_results' in results_json.keys():
            treatmens_list = []
            treatment_for_tooth_auto = results_json["treatment_results"]
            
            for key, value in results_json['tooth_results'].items():
                if value and not value['is_missing']:
                    tooth_cropped_image = value["cropped_image"] if 'cropped_image' in value else ''
                    tooth_coordinates = value["coordinates"] if 'coordinates' in value else {}
                    tooth_illnesses = value["illnesses"] if 'illnesses' in value else []
                    image_name = tooth_cropped_image.split("/")[-1]
                    single_tooth_save_path = os.path.join("media", "single_tooth", image_name)
                    urllib.request.urlretrieve(tooth_cropped_image, single_tooth_save_path)
                    report_tooth = ReportTooth.objects.create(image_report=image_report, number_prediction=key,
                                                              path=single_tooth_save_path, coordinates=tooth_coordinates)


                    treatment_methods = treatment_for_tooth_auto[key]["treatment_methods"]
                    for method in treatment_methods:
                        method = TreatmentMethod.objects.filter(slug=method["slug"]).first()
                        if not method:
                            continue
                        treatment_recommendation, created = TreatmentRecommendationForTooth.objects.get_or_create(tooth=report_tooth, image_report=image_report)
                        treatment_recommendation.recommendation.add(method)
                        treatment_recommendation.save()

                    report_tooth_predicts = []
                    icon_type = None
                    icon_type_list = []
                    for i in tooth_illnesses:
                        icon = ToothTypeIcon.objects.filter(tooth_number=key, name__exact=i["name"])
                        if icon:
                            for j in icon:
                                icon_type_list.append(j.name)
                    if "Implant Supported Crown" in icon_type_list and "Dental Implant" in icon_type_list:
                        icon_type = ToothTypeIcon.objects.get(tooth_number=key, name__exact="Implant Supported Crown")
                    elif not icon_type_list:
                        icon_type = ToothTypeIcon.objects.get(tooth_number=key, name__exact="Tooth")
                    else:
                        icon_type = ToothTypeIcon.objects.get(tooth_number=key, name__exact=icon_type_list[0])
                    for illness in tooth_illnesses:
                        if "Dental Pulp" in illness['name']:
                            continue
                        report_tooth_predicts.append(
                            ReportToothPredict(report_tooth=report_tooth, prediction=illness, is_illness=True))
                    report_tooth.icon_type = icon_type
                    report_tooth.save()
                    # use bulk_create to create all ReportToothPredict objects at once
                    ReportToothPredict.objects.bulk_create(report_tooth_predicts)
                else: # EKSİK DİŞ İÇİN İMPLANT TEDAVİ ÖNERİSİ EKLENİR!
                    if key in treatment_for_tooth_auto.keys():
                        treatment_methods = treatment_for_tooth_auto[key]["treatment_methods"]
                        for method in treatment_methods:
                            method = TreatmentMethod.objects.get(slug=method["slug"])
                            suggested_implant_obj, created = SuggestImplantToMissingTooth.objects.get_or_create(tooth_number=key, image_report=image_report)
                            suggested_implant_obj.recommendation.add(method)
                            suggested_implant_obj.save()
                    
            results_json["palate_results"] = [{**item, "approve_status": 0} for item in results_json["palate_results"]]
            results_json["illness_pool"] = [{**item, "approve_status": 0} for item in results_json["illness_pool"]]

            image_report_dict = {"palate_results": results_json["palate_results"],
                                "illness_pool": results_json["illness_pool"]}
            if image_report.name == "Bitewing":
                image_report_dict["measurement_results"] = results_json["measurement_results"]
            image_report.result_json = json.dumps(image_report_dict)
            image_report.ai_response_image_type = results_json["image_type"]
            print("KAYIT TAMAMLANDI")
            print(f"IMAGE REPORT ID: {image_report.id}", image_report)
            image_report.is_done = True
            image_report.is_error = False
            image_report.save()        
            # wizard için gerekli objelerin oluşması #
            try:
                create_objects_for_wizard(image_report, results_json["tooth_results"],results_json["treatment_results"])
            except Exception as e:
                traceback_str = traceback.format_exc()
                logger.error(f"Error occurred while creating wizard object: {traceback_str}")
            # wizard için gerekli objelerin oluşması #
        if "image_type" in results_json.keys() and "Cephalometric" in results_json["image_type"]:
            results_json["calibration_status"] = "False"
            print("KAYIT TAMAMLANDI")
            print("LATERAL CEPHALOMETRİC")
            image_report.result_json = json.dumps(results_json)
            image_report.ai_response_image_type = results_json["image_type"]
            image_report.is_done = True
            image_report.save()

def start_manuel_analyze(user, image_obj, image_path):
    profile = Profile.objects.get(user=user)
    agent_status = True if not image_obj.type else False
    token_response = {}
    if not agent_status:
        token_response = thakaa_spend_token(profile.id, image_obj.type.name)
    image_path_exists = True
    
    if not agent_status and "status" in token_response.keys() and token_response["status"] == False:
        return {"status": False, "token": token_response}
    image_report = ImageReport.objects.create(
        image=image_obj, 
        name=image_obj.type.name if image_obj.type else "Unknown", 
        user=profile)
    t = threading.Thread(target=start_analyze_thread, args=(image_report, image_path, image_path_exists, user))
    t.start()

    return {"status": True, "image_report_id": image_report.id, "token": token_response}

@login_required
def start_analyze(request):
    user = request.user
    image_path = request.GET.get("image_path")
    image_path_exists = True if "media/dental/radio" in image_path else False
    image_id = request.GET.get("image_id")
    image_obj = Image.objects.get(id=image_id)
    profile = Profile.objects.get(user=request.user)
    token_response = thakaa_spend_token(profile.id, image_obj.type.name)
    if token_response["status"] == False:
        return {"status": False, "token": token_response}
    image_report = ImageReport.objects.create(
        image=image_obj,
        name=image_obj.type.name,
        user=profile
    )
    t = threading.Thread(target=start_analyze_thread, args=(image_report, image_path, image_path_exists, user))
    t.start()

    return JsonResponse({"status": True, "image_report_id":image_report.id, "token": token_response})


def lateral_analyze_thread(image_report, image_path, manuel_values, user):
    url = f"http://93.89.73.105:8001/api/v1.8/analyze/radiography/"
    path = ccclinic_path + image_path
    files = {'image': open(path, 'rb')}

    data = {'company.api_key': "27RJUIL3BL3X1RESUL7ATHOZYLJ09JWB", 'request_source': 'CCClinic', 'request_user': user.username, "manuel_measures": json.dumps(manuel_values)}
    ai_post_response = requests.post(url, files=files, data=data)
    ai_post_response_json = ai_post_response.json()
    print('ai_response', ai_post_response_json)
    results_json = {}
    # ANALİZ DURUMUNU KONTROL EDEN YER
    if ai_post_response_json['status']:
        time_now = datetime.now()
        time_control = time_now + timedelta(minutes=2)
        response_url = ai_post_response_json['results']
        if "105" in response_url: # AI DEN SONUÇLAR ÇEKİLMEŞE ÇALIŞILDIĞINDA CANLIDAKİ CLİNİC AYNI ORTAMDA OLDUĞUNDAN SSL SİZ ORTAMA ÇEKİLMESİ GEREKİYOR TESTTE DİREKT KENDİ PORTUNDAN ALINABİLİR
            response_url = response_url.replace(f"{AIServerUrl}/", "http://93.89.73.105:8001/")
        ai_get_response = requests.request('GET', response_url)
        ai_get_response_json = ai_get_response.json()
        while not datetime.now() > time_control:
            ai_get_response = requests.request('GET', response_url)
            ai_get_response_json = ai_get_response.json()
            if ai_get_response_json['is_done'] and not ai_get_response_json['error_status']:
                results_json = ai_get_response_json['results']
                break
            print("Analiz henüz tamamlanmadı...")
            time.sleep(5)
            print("Analiz bekleniyor...")
        

        print("ANALİZ TAMAMLANDI!")
        slug = ai_get_response_json["id"]
        image_report.slug = slug
        if "image_type" in results_json.keys() and "Cephalometric" in results_json["image_type"]:
            print("KAYIT TAMAMLANDI")
            print("LATERAL CEPHALOMETRİC")
            image_report.result_json = json.dumps(results_json)
            image_report.is_done = True
            image_report.save()


def start_lateral_analyze(measure, first_coord, second_coord, image_report_obj, user):
    try:
        image_obj = image_report_obj.image
        image_path = image_obj.path.url
        profile = Profile.objects.get(user=user)
        new_image_report_obj = ImageReport.objects.create(image=image_obj, name=image_obj.type.name, user=profile)
        manuel_measures = {"measure": measure, "first_coord": first_coord, "second_coord": second_coord}
        print("analysis Starting")
        t = threading.Thread(target=lateral_analyze_thread, args=(new_image_report_obj, image_path, manuel_measures, user))
        print("thread started")
        t.start()
        return True
    except:
        traceback.print_exc()
        return False
    
@login_required
def start_failed_analysis(request):
    try:
        if request.method == "POST":
            image_report_id = request.POST.get("image_report_id")
            image_report_obj = ImageReport.objects.select_related("image").get(id=image_report_id)
            image_report_obj.is_done = False
            image_report_obj.is_error = False
            image_report_obj.created_date = datetime.now()
            image_report_obj.save()
            image_obj = image_report_obj.image
            t = threading.Thread(target=start_analyze_thread, args=(image_report_obj, image_obj.path.url , True, request.user))
            t.start()
            return JsonResponse({"status": True})
    except:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)
        return JsonResponse({"status": False})
