import requests
from Server.settings import dcmServerUrl
from Application.models import *
from Application3d.models import *
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import threading
import traceback
from Application.functions import error_handler_function

def start_implant_analyze(folder_slug, tooth_spacing):
    url = f"{dcmServerUrl}/dicom/analyze/start_implantology"
    data = {'folder_slug': folder_slug, "tooth_spacing": tooth_spacing}
    print("data", data)
    implant_response = requests.post(url, data=data)

@csrf_exempt
def third_molar(request):
    try:
        if request.method == 'POST':
            image_report_id = request.POST.get("image_report_id")
            tooth_spacing = request.POST.get("tooth_spacing")
            image_report_obj = ImageReport.objects.get(id=int(image_report_id))
            ai_report_slug = image_report_obj.slug
            report_type_obj = DicomAnalysisType.objects.get(id=4)
            dicom_report_obj = DicomReport.objects.create(image_report=image_report_obj, report_type=report_type_obj)
            t = threading.Thread(target=start_implant_analyze, args=(ai_report_slug, tooth_spacing))
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
def save_third_molar(request):
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