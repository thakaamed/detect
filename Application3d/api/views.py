import traceback
from Application3d.models import *
from Application.models import DicomFile, Image, ImageType
from User.models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
import json
from Application.functions import error_handler_function
from django.core.cache import cache
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import uuid
import os
import requests
from Server.settings import cc_url, dcmServerUrl, company_api_key, ccclinic_path
from pydicom import dcmread
import cv2
from copy import deepcopy
import numpy as np
import threading
import dicom2nifti
import dicom2nifti.settings as dicom_settings
import time
import urllib.request
from django.core.files.base import ContentFile
from django.db import transaction


dicom_settings.disable_validate_slice_increment()

def get_random_slug():
    new_slug = str(uuid.uuid4()).replace("-", "")
    return new_slug

# def start_3d_analyze_thread(dicom_report_obj=None, ai_report_slug=None):
#     url = f"{dcmServerUrl}/dicom/analyze/start_dicom_analyze"
#     payload = {"slug": ai_report_slug, "dicom_report_slug": dicom_report_obj.slug, "url": f"{cc_url}/api/end_3d_analyze"}
#     requests.request("POST", url, data=payload)

# @csrf_exempt
# def start_3d_analyze(request):
#     try:
#         if request.method == 'POST':
#             image_report_id = request.POST.get("image_report_id")
#             dicom_analysis_type_slug = request.POST.get("selectedDicomTypeSlug")
#             print("image_report", image_report_id)
#             print("dicom_slug", dicom_analysis_type_slug)
#             image_report_obj = ImageReport.objects.get(id=int(image_report_id))
#             report_type_obj = DicomAnalysisType.objects.get(slug=dicom_analysis_type_slug)
#             print("image_report_obj", image_report_obj)
#             print("report_type_obj", report_type_obj)
#             dicom_report_obj = DicomReport.objects.create(image_report=image_report_obj, report_type=report_type_obj)
#             ai_report_slug = image_report_obj.slug
#             t = threading.Thread(target=start_3d_analyze_thread, args=(dicom_report_obj, ai_report_slug))
#             t.start()
#             created_date = dicom_report_obj.created_date + timedelta(hours=3)
#             return JsonResponse({"status": "True", 
#                                 "message": "Analyze Started",
#                                 "url": f"{report_type_obj.url}{dicom_report_obj.id}",
#                                 "report_type_name": report_type_obj.name,
#                                 "created_date": created_date.strftime("%d/%m/%Y"),
#                                 "id": dicom_report_obj.id
#                                 })
#         else:
#             return JsonResponse({"status": "False"})
#     except Exception as e:
#         user = request.user
#         traceback.print_exc()
#         error = traceback.format_exc()
#         error_handler_function(user,error)

# @csrf_exempt
# def end_3d_analyze(request):
#     try:
#         returned_output_json = request.POST.get("returned_output_json")
#         dicom_report_slug = request.POST.get("dicom_report_slug")
#         dicom_report_obj = DicomReport.objects.get(slug=dicom_report_slug)
#         dicom_report_obj.result = returned_output_json
#         dicom_report_obj.is_done = True
#         dicom_report_obj.save()
#         print("dicom_report_slug",dicom_report_slug)
#         print("returned_output_json",returned_output_json)
#         return JsonResponse({"Status": True})
#     except Exception as e:
#         user = request.user
#         traceback.print_exc()
#         error = traceback.format_exc()
#         error_handler_function(user,error)


def create_imageReport_for_dcm_without_image(user, is_done=False, is_error=False):
    image_report_obj = ImageReport.objects.create(
        slug = str(uuid.uuid4()).replace("-", ""),
        user = Profile.objects.get(user=user),
        name = "CBCT",
        cbct = True,
        is_done = is_done,
        is_error = is_error,
        )
    return image_report_obj


def create_image_report(request):
    try:
        user = request.user
        image_report_obj = create_imageReport_for_dcm_without_image(user)
        return JsonResponse({
            "status": "True", 
            "id": image_report_obj.id, 
            "slug": image_report_obj.slug, 
            "created_date": image_report_obj.created_date.strftime("%d/%m/%Y")
        })
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def start_implant_analyze(folder_slug, tooth_spacing):
    url = f"{dcmServerUrl}/dicom/analyze/start_implantology"
    data = {'folder_slug': folder_slug, "tooth_spacing": tooth_spacing}
    print("data", data)
    implant_response = requests.post(url, data=data)
    

        
# @login_required
@csrf_exempt
def get_dicom_reports(request, image_report_id):
    try:
        lang = "en"
        # #--GET PAGE LANG--
        # if "/en/" in request.build_absolute_uri():
        #     lang = "en"
        # else:
        #     lang = "tr"
        # #GET PAGE LANG
        dicom_report_objs = DicomReport.objects.select_related("report_type", "image_report").defer("result").filter(
            image_report__id=image_report_id,
            image_report__cbct=True, image_report__user__user=request.user,
            ).order_by("-id")
        
        # Gruplama için boş sözlükler oluştur
        daily_reports = []
        daily_reports_dict = {}
        other_reports = []
        other_reports_dict = {}
        now = datetime.now().date()
        for dicom_report in dicom_report_objs:
            if dicom_report.is_done and not dicom_report.is_error:
                status = "success"
                url = f"/{lang}{dicom_report.report_type.url}{dicom_report.id}"
            elif dicom_report.is_error:
                status = "error"
                url = "#;"
            elif not dicom_report.is_done and not dicom_report.is_error:
                status = "process"
                url = "#;"
            
            created_date = dicom_report.created_date + timedelta(hours=3)
            
            # Oluşturulan tarihe göre gruplama yap
            
            if created_date.date() == now:  # Günlük
                daily_reports.append({
                    "dicom_reoprt_id": dicom_report.id,
                    "dicom_report_slug": dicom_report.slug,
                    "report_type_name": dicom_report.report_type.name,
                    "report_type_tr_name": dicom_report.report_type.tr_name,
                    "report_type_slug": dicom_report.report_type.slug,
                    "report_type_id": dicom_report.report_type.id,
                    "date": created_date.strftime("%H:%M %d/%m/%Y"),
                    "status": status,
                    "url": url,
                })
            else:  # Diğer
                other_reports.append({
                    "id": dicom_report.id,
                    "dicom_report_slug": dicom_report.slug,
                    "report_type_name": dicom_report.report_type.name,
                    "report_type_tr_name": dicom_report.report_type.tr_name,
                    "report_type_slug": dicom_report.report_type.slug,
                    "report_type_id": dicom_report.report_type.id,
                    "date": created_date.strftime("%H:%M %d/%m/%Y"),
                    "status": status,
                    "url": url,
                })
        
        # Tüm raporları birleştir
        daily_reports_dict = {
            "date": "Todays Reports",
            "reports": daily_reports
        }
        other_reports_dict = {
            "date": "Past Reports",
            "reports": other_reports
        }
        list_dicom_reports_section_list = [
            daily_reports_dict,
            other_reports_dict
        ]

        return JsonResponse({"all_reports": list_dicom_reports_section_list})

    except:
        # user = request.user
        traceback.print_exc()
        # error = traceback.format_exc()
        # error_handler_function(user,error)
        daily_reports_dict = {
            "date": "Todays Reports",
            "reports": []
        }
        other_reports_dict = {
            "date": "Past Reports",
            "reports": []
        }
        list_dicom_reports_section_list = [
            daily_reports_dict,
            other_reports_dict
        ]
        return JsonResponse({"all_reports": list_dicom_reports_section_list})

@csrf_exempt
def get_analysis_types(request):
    analysis_types_section_list = []
    analysis_type_objs = DicomAnalysisType.objects.all().order_by("id")

    for analysis_type_obj in analysis_type_objs:
        analysis_types_section_list.append({
            "id": analysis_type_obj.id,
            "slug": analysis_type_obj.slug,
            "name": analysis_type_obj.name,
            "tr_name": analysis_type_obj.tr_name,
            "active": analysis_type_obj.active
        })

    return JsonResponse({"analysis_types": analysis_types_section_list})


def anonymize(dcm):
    def remove_private_tags(dataset, data_element):
        if data_element.tag.is_private:
            del dataset[data_element.tag]

    def remove_date_tags(dataset, data_element):
        if data_element.VR == 'DA':
            del dataset[data_element.tag]
        if data_element.VR == 'DT':
            del dataset[data_element.tag]
        if data_element.VR == 'TM':
            del dataset[data_element.tag]

    dcm.ReferringPhysicianName = 'ANONYM'
    dcm.PatientID = 'ANONYM'
    dcm.PatientName = 'ANONYM'
    dcm.PatientBirthDate = None
    dcm.PatientSex = 'ANONYM'

    dcm.walk(remove_private_tags)
    dcm.walk(remove_date_tags)
    return dcm


def all_dicoms_uploaded(dicom_group_obj, dcm_path, progress_obj=None):
    dicom_obj_folder_path = dicom_group_obj.folder_path
    new_dcm_name = dcm_path.split('/')[-1]
    # DCMNİN ANONİMİZE EDİLMESİ
    dcm = dcmread(dcm_path)
    dcm = anonymize(dcm)
    # Veri 3 boyutlu degil direkt kendisini kaydet !!
    def editPromax(frame=None, dcm=None): #Promax makineleri için dicomu düzenleme fonksiyonu
        if frame: # Parçalama işlemi sırasında dicomun bir parçası gönderilmişse
            frame.add_new([0x0020, 0x0032], 'DS', dcm[0x52009230][i][0x00209113][0][0x00200032].value)
            frame.add_new([0x0020, 0x0037], 'DS', dcm[0x52009230][i][0x00209116][0][0x00200037].value)
            frame.add_new([0x0028, 0x0030], 'DS', dcm[0x52009229][0][0x00289110][0][0x00280030].value)
            frame.file_meta.MediaStorageSOPClassUID = None
            if 0x52009229 in frame:
                del frame[0x52009229]
            if 0x52009230 in frame:
                del frame[0x52009230]
            return frame
        else: # Parçalama işleminden bağımsız tekli dicom gönderilmişse
            dcm.add_new([0x0020, 0x0032], 'DS', dcm[0x52009230][i][0x00209113][0][0x00200032].value)
            dcm.add_new([0x0020, 0x0037], 'DS', dcm[0x52009230][i][0x00209116][0][0x00200037].value)
            dcm.add_new([0x0028, 0x0030], 'DS', dcm[0x52009229][0][0x00289110][0][0x00280030].value)
            dcm.file_meta.MediaStorageSOPClassUID = None
            if 0x52009229 in dcm:
                del dcm[0x52009229]
            if 0x52009230 in dcm:
                del dcm[0x52009230]
            return dcm
    
    if len(dcm.pixel_array.shape) != 3: # Parçalı halde olan dicom
        if dcm[0x00081090].value == 'ProMax':
            try:
                dcm = editPromax(dcm=dcm)
            except:
                print("promax editlenemedi")
        dcm.save_as(dcm_path)
        # 1 == 3 boyutlu olmayan parçalı dicom
        # 3 == tek parça yani 3 boyutlu parçalanacak olan dicom
        return True, "1"

    # Veri 3 boyutlu kendisini kaydetme, parcalara ayir parcalari kaydet !!
    else: # Tek parça halinde olan dicom -- Burada parçalama işlemi yapılacak
        shape = dcm.pixel_array.shape
        frame = deepcopy(dcm)
        for i in range(shape[0]):
            slice = np.array(dcm.pixel_array[i, ...])
            if cv2.countNonZero(slice) != 0:
                frame.PixelData = slice.tobytes()
                frame.Rows, frame.Columns = slice.shape
                frame.SOPInstanceUID = f'{dcm.SOPInstanceUID}.{i}'
                frame.NumberOfFrames = '1'
                frame.InstanceNumber = f'{i}'
                
                if dcm[0x00081090].value == 'ProMax':
                    frame = editPromax(frame=frame, dcm=dcm)

                full_file_path = os.path.join(os.path.join("media"), dicom_obj_folder_path, f"{frame.SOPInstanceUID}.dcm")
                print("\n ", i, "Framelerine Parçalanıyor", full_file_path)
                f = open(full_file_path, "w") 
                frame.save_as(full_file_path)
                f.close()
        new_dcm_file_name_with_path = os.path.join(os.path.join("media"), f"{dicom_obj_folder_path}/")
        os.rename(dcm_path, new_dcm_file_name_with_path + new_dcm_name)
        delete_path = os.path.join(os.path.join("media"), f"{dicom_obj_folder_path}/", new_dcm_name)
        os.remove(delete_path)
        # 1 == 3 boyutlu olmayan parçalı dicom
        # 3 == tek parça yani 3 boyutlu parçalanacak olan dicom
        return True, "3"


def corvert2niftii(dicom_group_obj):

    dicom_path = os.path.join("media", dicom_group_obj.folder_path)
    niftii_save_path = os.path.join("media", dicom_group_obj.nifti_path)
    nib_save_path = f"{niftii_save_path}/{dicom_group_obj.slug}.nii.gz"

    dicom2nifti.dicom_series_to_nifti(dicom_path, nib_save_path, reorient_nifti=True)
    print("dicom_path", dicom_path)
    print("nib_save_path", nib_save_path)


@csrf_exempt
def get_analyzed_files(request):
    image_report_id = request.POST.get("image_report_id")
    print("image_report_id", image_report_id)
    image_report = ImageReport.objects.get(id=image_report_id)
    dicom_group_obj = image_report.dicom
    analysis_id = 0

    def get_analyzed_nifties(results_json):
        path_dict = results_json
        for name, path in path_dict.items():
            download_url = f"{dcmServerUrl}/{path}"
            response = requests.get(download_url)
    
            # Yanıt başarılı mı kontrol et
            if response.status_code == 200:
                # Dosyayı hedef dosya yoluna yaz
                save_path = os.path.join("media", dicom_group_obj.result_nifti_path)
                if not os.path.exists(save_path): os.makedirs(save_path)
                result_nifti_save_path = os.path.join(save_path, f"{name}.nii.gz")
                print("result_nifti_save_path", result_nifti_save_path)

                with open(result_nifti_save_path, 'wb') as f:
                    f.write(response.content)

    def get_analyzed_niftiDracos(results_json):
        nifti2draco_path = results_json["nifti2draco_path"]
        predict2nifti_path = results_json["predict2nifti_path"]
        draco_zip_path = results_json["draco_zip_path"][0]
        
        def download_file(folder_name=None, path=None):
            save_path = os.path.join("media", "STL", folder_name, dicom_group_obj.slug) # media/STL/predict2nifti_path/Param-dicom_folder_slug
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
                

        for label_name, path in nifti2draco_path.items():
            try:
                download_file("nifti2draco_path", path)
            except:
                print(f"Draco dosyası alınamadı: {label_name}")
                traceback.print_exc()

        for label_name, path in predict2nifti_path.items():
            try:
                download_file("predict2nifti_path", path)
            except:
                print(f"Nifti dosyası alınamadı: {label_name}")
                traceback.print_exc()

        try:
            download_file("draco_zip_path", draco_zip_path)
        except:
            print(f"Draco Zip alınamadı: {label_name}", e)


    results_json = {}
    print("image_report.slug", image_report.slug)
    ai_get_response = requests.request('GET', f"https://dcm.craniocatch.com/api/v1.9/analyze/radiography/?id=5a20bfed-45cc-4c8d-b8aa-69ff73866ee1e2da6a78-d6d8-4182-9070-43f66a5e302d")
    ai_get_response_json = ai_get_response.json()
    if ai_get_response_json['is_done'] and not ai_get_response_json['error_status']:
        results_json = ai_get_response_json['results']
        print("results_json", results_json, type(results_json))
    print("ANALİZ TAMAMLANDI!")
    get_analyzed_nifties(results_json["paths"])
    get_analyzed_niftiDracos(results_json["STL"])
    slug = "5a20bfed-45cc-4c8d-b8aa-69ff73866ee1e2da6a78-d6d8-4182-9070-43f66a5e302d"
    image_report.slug = slug
    image_report.result_json = json.dumps(results_json)
    image_report.ai_response_image_type = "CBCT"
    print("KAYIT TAMAMLANDI")
    print(f"IMAGE REPORT ID: {image_report.id}", image_report)
    image_report.is_done = True
    image_report.save()


def start_3d_analyze(request):
    pass

def end_3d_analyze(request):
    pass

def start_analyze_thread(image_report, dicom_group_obj, analysis_id=0):
    def get_analyzed_nifties(path_dict):
        for name, path in path_dict.items():
            save_file = path.split("/")[-1] # Mandible.drc
            download_url = f"{dcmServerUrl}/{path}"
            save_path = os.path.join("media", dicom_group_obj.result_nifti_path)
            if not os.path.exists(save_path): os.makedirs(save_path)
            new_save_path = os.path.join(save_path, save_file)
            print("Kayıt Yolu:" , new_save_path)
            try:
                urllib.request.urlretrieve(download_url, new_save_path)
            except:
                print("URLLIB ILE DOSYA ALINAMADI")
                traceback.print_exc()

    def get_analyzed_niftiDracos(results_json):
        nifti2draco_path = results_json["nifti2draco_path"]
        predict2nifti_path = results_json["predict2nifti_path"]
        draco_zip_path = results_json["draco_zip_path"][0]
        
        def download_file(folder_name=None, path=None):
            save_path = os.path.join("media", "STL", folder_name, dicom_group_obj.slug) # media/STL/predict2nifti_path/Param-dicom_folder_slug
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
                
        for label_name, path in nifti2draco_path.items():
            try:
                download_file("nifti2draco_path", path)
            except Exception as e:
                print(f"Draco dosyası alınamadı: {label_name}", e)

        for label_name, path in predict2nifti_path.items():
            try:
                download_file("predict2nifti_path", path)
            except:
                print(f"Nifti dosyası alınamadı: {label_name}", e)

        try:
            download_file("draco_zip_path", draco_zip_path)
        except:
            print(f"Draco Zip alınamadı: {label_name}", e)


    def get_panoramic_image(image_report, panoramic_image_path):
        try:
            response = requests.get(f"{dcmServerUrl}/{panoramic_image_path}")
            if response.status_code == 200:
                with transaction.atomic():
                    # ImageField'ın dosya adını oluşturmak için isteği dosya adından alın
                    file_name = panoramic_image_path.split('/')[-1]
                    
                    # Image modeli üzerinden yeni bir resim oluştur
                    new_image = Image.objects.create(
                        patient=image_report.dicom.patient,
                        user=image_report.user,
                        type=ImageType.objects.get(id=3),
                        patient_type_id=0,
                    )
                    
                    # Oluşturulan resme panoramic resmi ekle
                    new_image.path.save(file_name, ContentFile(response.content), save=True)
                    img_path = new_image.path.path
                    name, extension = os.path.splitext(img_path)
                    new_img_path = name + ".jpg"

                    thumbnail_image_path = new_img_path.replace('.', '_thumbnail.')
                    thumbnail_image_path = thumbnail_image_path.replace(ccclinic_path + "/", "")
                    cv2.imwrite(thumbnail_image_path, cv2.resize(cv2.imread(new_image.path.path), (250, 109)))
                    new_image.thumbnail_image_path = thumbnail_image_path.replace("/mnt/nfs_ai_v2/", "")
                    new_image.save()
                    image_report.image = new_image
                    image_report.save()
                    # Oluşturulan resmin thumbnail'ını oluştur
                    # Burada thumbnail oluşturma işlemini nasıl yapacağınıza dair bir kod örneği yok,
                    # bu kısmı kendi projenizin ihtiyacına göre uyarlayabilirsiniz.
                    # Eğer bir thumbnail oluşturma yönteminiz varsa, burada kullanabilirsiniz.
                    # new_image.thumbnail_image_path.save(thumbnail_file_name, ...)

        except Exception as e:
            print(f"Panoramic görüntüsü alınamadı: {panoramic_image_path}", e)


    url = f"{dcmServerUrl}/api/v1.9/analyze/radiography/"
    nifti_analyze_base_path = os.path.join("media", dicom_group_obj.nifti_path)
    nifti_full_path = os.path.join(nifti_analyze_base_path, f"{dicom_group_obj.slug}.nii.gz")
    files = {'image': open(nifti_full_path, 'rb')}
    data = {'company.api_key': company_api_key, 'analysis_id': analysis_id}
        
    ai_post_response = requests.post(url, files=files, data=data)
    print("ai_post_response", ai_post_response)
    ai_post_response_json = ai_post_response.json()
    print("ai_post_response_json", ai_post_response_json)
    results_json = {}
    # ANALİZ DURUMUNU KONTROL EDEN YER
    if ai_post_response_json['status']:
        time_now = datetime.now()
        time_control = time_now + timedelta(minutes=15)
        response_url = ai_post_response_json['results']
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
            time.sleep(10)
            print("Analiz bekleniyor...")
        print("ANALİZ TAMAMLANDI! DOSYALAR İNDİRİLİYOR..." )
        slug = ai_get_response_json["id"]
        image_report.slug = slug
        image_report.result_json = json.dumps(results_json)
        image_report.ai_response_image_type = "CBCT"
        image_report.save()
        print("İNDİRME BAŞLIYOR...")
        get_analyzed_nifties(results_json["paths"])
        get_analyzed_niftiDracos(results_json["STL"])
        get_panoramic_image(image_report, results_json["panoramic_image_path"])
        print("İNDİRME TAMAMLANDI")
        print("KAYIT TAMAMLANDI")
        print(f"IMAGE REPORT ID: {image_report.id}", image_report)
        image_report.is_done = True
        image_report.save()


def start_nifti_analyze(dicom_group_obj, profile):
    image_report = ImageReport.objects.create(
        dicom=dicom_group_obj, 
        name="CBCT", 
        user=profile,
        cbct=True,
        )
    t = threading.Thread(target=start_analyze_thread, args=(image_report, dicom_group_obj))
    t.start()

    return {"status": True, "image_report_id": image_report.id}


@login_required
def dicom_upload_api(request):
    try:
        current_upload_progress = 0
        if request.method == 'POST':
            if 'file' not in request.FILES:
                return HttpResponse(status=500)
            slug = request.POST.get("slug")
            patient_slug = request.POST.get("patient_slug")
            ## DicomFile
            # DicomFile modeli için gerekli olan patinets i parçalı veya chunklu yüklemede 
            # tekrar tekrar istekle veritabanının yormamak için ilk istekte cacheye alıp 
            # sonraki isteklerde cacheden kullanmak için yazılmıştır.
            print("patient_slug", patient_slug)
            def set_patinet_to_cache(patient_slug):
                patient_obj = Patient.objects.get(slug=patient_slug)
                patient_dict = {patient_slug: patient_obj}
                cache.set("patient_dict", patient_dict)
                return patient_obj
            
            patient_dict = cache.get("patient_dict", None)
            print("patient_dict", patient_dict)
            if not patient_dict:
                patient_obj = set_patinet_to_cache(patient_slug)
            else:
                patient_obj = patient_dict.get(patient_slug, None)
                if not patient_obj:
                    patient_obj = set_patinet_to_cache(patient_slug)
            dicom_group_obj, created = DicomFile.objects.get_or_create(slug=slug, patient=patient_obj)
            file = request.FILES['file']
            if not file:
                return JsonResponse({'success': False, 'message': 'File Yok'})
            current_chunk = int(request.POST['dzchunkindex']) + 1
            total_chunks = int(request.POST['dztotalchunkcount'])
            folder_and_slug = dicom_group_obj.folder_path
            nifti_and_slug = dicom_group_obj.nifti_path
            save_folder = os.path.join("media", folder_and_slug)
            nifti_and_slug = os.path.join("media", nifti_and_slug)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            if not os.path.exists(nifti_and_slug):
                os.makedirs(nifti_and_slug)
            if current_chunk == total_chunks and total_chunks < 3: # Parçalı dicom için dosyanın kaydedilme yeri
                dcm = dcmread(file, force=True)
                if cv2.countNonZero(dcm.pixel_array) != 0: # Dicomun yüklenen parçası siyah değil ise...
                    sop_instance_uid = str(dcm.SOPInstanceUID)
                    file_extension = '.dcm'
                    # Dosya adını SOP Instance UID'ye göre güncelleme
                    new_dcm_name = sop_instance_uid + file_extension
                    save_path = os.path.join(os.path.join("media"), dicom_group_obj.folder_path, new_dcm_name)                    
                    dcm.save_as(save_path)
                else:
                    return JsonResponse({'success': True, 'size': "1", 'message': 'File has been uploaded successfully'})
            else: # tekli dicom için gelen chunkların üzerine yazıldığı yer
                save_path = os.path.join(os.path.join("media"), dicom_group_obj.folder_path, "chunk_" + file.name)
                try:
                    with open(save_path, 'ab') as f:
                        f.seek(int(request.POST['dzchunkbyteoffset']))
                        f.write(file.read())  # f.write(file.stream.read())
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
            
            all_uploaded = current_chunk == total_chunks
            if all_uploaded: # parçalıların tüm parçaları ve teklinin tamamı yüklendiğinde burası çalışır.
                if not os.path.isfile(save_path):
                    return JsonResponse({'success': False, 'message': 'Size mismatch'})
                else:
                    result, size = all_dicoms_uploaded(dicom_group_obj=dicom_group_obj, dcm_path=save_path)
                    return JsonResponse({'success': True, 'size': size, 'message': 'File has been uploaded successfully'})
            # 1 == 3 boyutlu olmayan parçalı dicom
            # 3 == tek parça yani 3 boyutlu parçalanacak olan dicom
            return JsonResponse({'success': True, 'size': "3", 'progress': current_upload_progress})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def convert_nifti_and_start_analyze(request):
    try:
        slug = request.POST.get("slug")
        patient_slug = request.POST.get("patient_slug")
        def set_patinet_to_cache(patient_slug):
            patient_obj = Patient.objects.get(slug=patient_slug)
            patient_dict = {patient_slug: patient_obj}
            cache.set("patient_dict", patient_dict)
            return patient_obj

        patient_dict = cache.get("patient_dict", None)            
        if not patient_dict:
            patient_obj = set_patinet_to_cache(patient_slug)
        else:
            patient_obj = patient_dict.get(patient_slug, None)
            if not patient_obj:
                patient_obj = set_patinet_to_cache(patient_slug)
        dicom_group_obj = DicomFile.objects.get(slug=slug, patient=patient_obj)
        profile_obj = Profile.objects.get(user=request.user)
        corvert2niftii(dicom_group_obj)
        start_nifti_analyze(dicom_group_obj, profile_obj)
        return JsonResponse({"status": True})
    except:
        return JsonResponse({"status": False})


def get_list_of_dicoms(request):
    image_report_id = request.GET.get("image_report_id")
    try:
        image_report_obj = ImageReport.objects.select_related("dicom").get(id=image_report_id)
    except ImageReport.DoesNotExist:
        return JsonResponse({"status": False, "message": "No such record was found."})
    response_json = {}
    dicom_file_obj = image_report_obj.dicom
    
    def get_dicom_path():
        dicoms_obj_folder_path = dicom_file_obj.folder_path
        dicoms_path = os.path.join("media", dicoms_obj_folder_path)
        dicoms_url = f"/media/{dicoms_obj_folder_path}/"
        all_dicoms = []
        if os.path.exists(dicoms_path):
            all_dicoms = os.listdir(dicoms_path)
        
        response_json["all_dicoms"] = all_dicoms
        response_json["dicoms_url"] = dicoms_url

    def get_result_nifti_path():
        
        paths = result_json["paths"]   
        nifti_obj_result_nifti_path = dicom_file_obj.result_nifti_path
        result_nifti_path = os.path.join("media", nifti_obj_result_nifti_path)
        result_nifti_dict = {}
        result_nifti_url = f"/media/{nifti_obj_result_nifti_path}/"

        for key, path in paths.items():
            save_file = path.split("/")[-1] # Mandible.drc
            result_nifti_dict[key] = f"{result_nifti_path}/{save_file}"

            response_json["all_result_nifties"] = result_nifti_dict
        response_json["result_nifti_url"] = result_nifti_url

    def get_nifti_path():

        nifti_obj_nifti_path = dicom_file_obj.nifti_path
        nifti_path = os.path.join("media", nifti_obj_nifti_path)
        nifti_url = f"/media/{nifti_obj_nifti_path}/"
        all_nifties = []
        if os.path.exists(nifti_path):
            all_nifties = os.listdir(nifti_path)

        response_json["all_nifties"] = all_nifties
        response_json["nifti_url"] = nifti_url
    result_json = json.loads(image_report_obj.result_json)

    def get_predict2nifti_path():

        predict2nifti_json = result_json["STL"]["predict2nifti_path"]
        predict2nifti_path = os.path.join("media", "STL", "predict2nifti_path", dicom_file_obj.slug)
        nifti_dict = {}
        predict2nifti_url = f"/{predict2nifti_path}/"

        for key, path in predict2nifti_json.items():

            print("path", path) # media/STL/nifti2draco/9d4b442f-6add-4595-939f-3f53e390b1c0/
            save_file = path.split("/")[-1] # 9d4b442f-6add-4595-939f-3f53e390b1c0_anatomy_Mandible.drc
            drc_path = "media/STL/predict2nifti_path/"
            nifti_dict[key] = f"{drc_path}{dicom_file_obj.slug}/{save_file}"

            response_json["predict2nifti_path"] = nifti_dict
        response_json["predict2nifti_url"] = predict2nifti_url

    def get_nifti2draco_path():
        nifti2draco_json = result_json["STL"]["nifti2draco_path"]
        nifti2draco_path = os.path.join("media", "STL", "nifti2draco_path", dicom_file_obj.slug)
        draco_dict = {}
        nifti2draco_url = f"/{nifti2draco_path}/"
        for key, path in nifti2draco_json.items():

            print("path", path) # media/STL/nifti2draco/9d4b442f-6add-4595-939f-3f53e390b1c0/
            save_file = path.split("/")[-1] # 9d4b442f-6add-4595-939f-3f53e390b1c0_anatomy_Mandible.drc
            drc_path = "media/STL/nifti2draco_path/"
            draco_dict[key] = f"{drc_path}{dicom_file_obj.slug}/{save_file}"

            response_json["nifti2draco_path"] = draco_dict
        response_json["nifti2draco_url"] = nifti2draco_url

    def get_draco_zip_path():
        draco_zip_path = os.path.join("media", "STL", "draco_zip_path", dicom_file_obj.slug)
        draco_zip_url = f"/{draco_zip_path}/"

        if os.path.exists(draco_zip_path):
            all_draco_zip_path = os.listdir(draco_zip_path)

            response_json["draco_zip_path"] = all_draco_zip_path
        response_json["draco_zip_url"] = draco_zip_url

    get_dicom_path()
    get_nifti_path()
    get_result_nifti_path()
    get_predict2nifti_path()
    get_draco_zip_path()
    get_nifti2draco_path()
    
    return JsonResponse(response_json)


def get_3d_labels(request):
    image_report_id = request.GET.get("image_report_id")
    labels_3d = cache.get("3d_labels_dict")
    image_report_obj = ImageReport.objects.get(id=image_report_id)
    STL = json.loads(image_report_obj.result_json)["STL"]
    return_labels = []
    nifti = STL["predict2nifti_path"]
    for label_name in nifti.keys():
        label_3d_dict = labels_3d.get(label_name)
        if not label_3d_dict: continue
        return_labels.append(label_3d_dict)
    return JsonResponse({"labels": return_labels})

@csrf_exempt
def get_dicom_image(request):
    image_report_id = request.GET.get("image_report_id")
    print("image_report_id", image_report_id)
    image_report_obj = ImageReport.objects.get(id=image_report_id)
    try:
        image_url = f"{cc_url}{image_report_obj.image.path.url}"
    except:
        image_url = "No Image Data"
    return JsonResponse({"image_path": image_url})
