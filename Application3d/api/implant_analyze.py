import requests
from Server.settings import dcmServerUrl, company_api_key
from Application.models import *
from Application3d.models import *
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import threading
import traceback
from Application.functions import error_handler_function
import time
import urllib.request

def start_implant_analyze(ai_report_slug, tooth_spacing, dicom_report_obj):
    def get_analyzed_slices(dicom_report_slug, slices):
        def download_file(path=None):
            save_path = os.path.join("media", "Implantology", ai_report_slug, dicom_report_slug) # media/STL/predict2nifti_path/Param-dicom_folder_slug
            if not os.path.exists(save_path): os.makedirs(save_path)
            save_file = path.split("/")[-1] # Mandible.drc
            download_url = f"{dcmServerUrl}/{path}"
            new_save_path = os.path.join(save_path, save_file)
            print("Kayıt Yolu:" , new_save_path)
            try:
                urllib.request.urlretrieve(download_url, new_save_path)
            except:
                print("URLLIB ILE DOSYA ALINAMADI")
                traceback.print_exc()

        for slice_png, data in slices.items():
            download_path = data["path"]
            download_file(download_path)
            
    url = f"{dcmServerUrl}/api/v1.9/analyze/3D/"
    data = {
        'slug': ai_report_slug, 
        'company.api_key': company_api_key,
        "analysis_data": tooth_spacing,
        "analysis_id": 4}
        
    implant_response = requests.post(url, data=data)
    implant_response_json = implant_response.json()
    print("implant_response_json", implant_response_json)
    results_json = {}
    # ANALİZ DURUMUNU KONTROL EDEN YER
    if implant_response_json['status']:
        time_now = datetime.now()
        time_control = time_now + timedelta(minutes=5)
        response_url = implant_response_json['results']
        ai_get_response = requests.request('GET', response_url)
        ai_get_response_json = ai_get_response.json()
        while not datetime.now() > time_control:
            ai_get_response = requests.request('GET', response_url)
            ai_get_response_json = ai_get_response.json()
            if ai_get_response_json['is_done'] and not ai_get_response_json['error_status']:
                results_json = ai_get_response_json['results']
                print("results_json", results_json, type(results_json))
                break
            print("Analiz henüz tamamlanmadı...")
            time.sleep(5)
            print("Analiz bekleniyor...")
        print("ANALİZ TAMAMLANDI! JSON KAYDEDİLİYOR..." )
        slug = ai_get_response_json["id"]
        dicom_report_obj.slug = slug
        dicom_report_obj.result = json.dumps(results_json)
        dicom_report_obj.save()
        print(" DOSYALAR İNDİRİLİYOR...İNDİRME BAŞLIYOR...")
        get_analyzed_slices(slug, results_json["Reports"]["implant_report"])
        print("İNDİRME TAMAMLANDI")
        print(f"IMAGE REPORT ID: {dicom_report_obj.id}", dicom_report_obj)
        dicom_report_obj.is_done = True
        dicom_report_obj.save()
        print("KAYIT TAMAMLANDI")

@csrf_exempt
def implant_analysis(request):
    try:
        if request.method == 'POST':
            image_report_id = request.POST.get("image_report_id")
            tooth_spacing = request.POST.get("tooth_spacing")
            image_report_obj = ImageReport.objects.get(id=int(image_report_id))
            ai_report_slug = image_report_obj.slug
            report_type_obj = DicomAnalysisType.objects.get(id=4)
            dicom_report_obj = DicomReport.objects.create(image_report=image_report_obj, report_type=report_type_obj)
            t = threading.Thread(target=start_implant_analyze, args=(ai_report_slug, tooth_spacing, dicom_report_obj))
            t.start()
            created_date = dicom_report_obj.created_date + timedelta(hours=3)
            return JsonResponse({"status": True, 
                                "message": "Analyze Started",
                                "url": f"{report_type_obj.url}{dicom_report_obj.id}",
                                "report_type_name": report_type_obj.name,
                                "created_date": created_date.strftime("%d/%m/%Y"),
                                "id": dicom_report_obj.id
                                })
        else:
            return JsonResponse({"status": False})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@csrf_exempt
def save_implant(request):
    try:
        report_slug = request.POST.get("report_slug")
        result_json = request.POST.get("result_json")
        print("result", result_json)
        dicom_report_obj = DicomReport.objects.filter(slug=report_slug).first()
        if dicom_report_obj:
            dicom_report_obj.result = result_json
            dicom_report_obj.save()
        else:
            image_report = ImageReport.objects.get(id=12690)
            report_type = DicomAnalysisType.objects.get(id=4)
            dicom_report_obj = DicomReport.objects.create(
                slug=report_slug,
                image_report=image_report,
                result=result_json,
                report_type=report_type,
                is_done=True
            )
        return HttpResponse("OK")
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)