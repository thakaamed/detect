from django.shortcuts import render
from Application3d.models import *
from Application.models import *
from User.models import *
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
import traceback
from Application.functions import *
import time
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt
from Server.settings import ccreport_url, ccclinic_path_with_slash, ccclinic_path, \
    image_path_without_slash_after_media, dicom_server_url, dicom_base_path, dcmServerUrl
from Application.functions import user_theme_choices
import uuid
import urllib.request
from Application.views import get_specs
import threading

# Create your views here.

@login_required
def dicom_stl_viewer(request, dicom_report_id):
    try:
        specs = get_specs()
        dicom_report_obj = DicomReport.objects.get(id=dicom_report_id)
        page_name = request.path
        has_page_name_stl = 'stl' in page_name
        patient_obj = dicom_report_obj.image_report.image.patient
        patient_full_name = patient_obj.first_name + " " + patient_obj.last_name
        birthday = patient_obj.date_of_birth
        today_for_age = date.today()
        if birthday:
            patient_age = today_for_age.year - birthday.year
        else:
            patient_age = None
        radiography_create_date = dicom_report_obj.image_report.created_date + timedelta(hours=3)
        radiography_create_date = radiography_create_date.strftime("%d.%m.%Y %H:%M")
        image_type = dicom_report_obj.image_report.image.type.name
        user_theme_dict = user_theme_choices(request.user)
        profile_user = Profile.objects.filter(user=request.user).first()
        patient = Patient.objects.filter(user=profile_user).first()
        loaded_json = json.loads(dicom_report_obj.result)
        drc_path = loaded_json["requested_order_type_path"]
        drc_path = drc_path.replace(dicom_base_path, "")
        print(drc_path, type(drc_path))
        context = {
            'user_theme_choices_json': json.dumps(user_theme_dict),
            'user_theme_choices': user_theme_dict,
            "has_page_name_stl": has_page_name_stl,
            'status': True,
            "image_type": image_type,
            "radiography_create_date": radiography_create_date,
            "patient_age": patient_age,
            "patient_full_name": patient_full_name,
            'drc_path': drc_path,
            'patient': patient,
            'image_report_id': dicom_report_obj.image_report.id,
            "specs": specs
        }
        return render(request, 'dicom/stl-viewer/example/webgl_loader_draco.html', context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def dicom_upload_page(request):
    try:
        print("SAYFA RENDERLENDI")
        user_theme_dict = user_theme_choices(request.user)
        context = {'user_theme_choices_json': json.dumps(user_theme_dict), 'user_theme_choices': user_theme_dict,
        }
        return render(request, 'dropzone_upload.html', context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


def save_dicomImage_from_url(url, name, patient_slug, user, image_obj):
    image_save_name = image_path_without_slash_after_media + "/" + name
    urllib.request.urlretrieve(url, image_save_name)
    with open(image_save_name, 'rb') as f:
        file_obj = File(f)
        file_obj.name = name
        image_obj.path = file_obj
        image_obj.save()
        img_path = image_obj.path.path
        thumbnail_name, extension = os.path.splitext(img_path)
        new_img_path = thumbnail_name + ".jpg"
        thumbnail_image_path = new_img_path.replace('.', '_thumbnail.')
        thumbnail_image_path = thumbnail_image_path.replace(ccclinic_path + "/", "")
        cv2.imwrite(thumbnail_image_path, cv2.resize(cv2.imread(image_obj.path.path), (250, 109)))
        image_obj.thumbnail_image_path = thumbnail_image_path
        image_obj.save()
    os.remove(image_save_name)
    return image_obj


def create_imageReport_for_dcm(image_obj, result_dict, image_report_obj):
    print("result_dict", result_dict, type(result_dict))
    result_json = json.dumps(result_dict)
    image_report_obj.image = image_obj
    image_report_obj.is_done = True
    image_report_obj.result_json = result_json
    image_report_obj.save()
    return image_report_obj


def convert_niftii_and_panoramic_thread(folder_slug, image_report_obj, patient_slug, user, image_obj):
    url = f'{dicom_server_url}/dicom/convert-niftii-and-panoramic'
    data = {"slug": folder_slug}
    response = requests.post(url, data=data)
    response_dict = response.json()

    panoramic_image_path = response_dict['panoramic_img_path']
    niftii_path = response_dict['niftii_path']
    response_dict["folder_slug"] = folder_slug
    print("panoramic_image_path", panoramic_image_path)
    print("niftii_path", niftii_path)
    url = f'{dicom_server_url}{panoramic_image_path}'
    name = panoramic_image_path.split("/")[-1]
    image_obj = save_dicomImage_from_url(url, name, patient_slug, user, image_obj) if panoramic_image_path != "None" else image_obj
    image_report_obj = create_imageReport_for_dcm(image_obj, response_dict, image_report_obj)


@login_required
def convert_niftii_and_panoramic(request): #dicom yükleme işlemi sonrasında niftii oluşturulmadan önce imagereport oluşturulması ve oluşturma sürecinde raporun takibinin bildirimler kısmından yapılabilmesi
    try:
        if request.method == 'POST':
            user = request.user
            folder_slug = request.POST.get('slug')
            patient_slug = request.POST.get('patient_slug')
            image_report_id = request.POST.get('image_report_id')

            print(f"folder{folder_slug}", f"patient{patient_slug}")
            image_type = ImageType.objects.get(id=3)
            profile = Profile.objects.get(user=user)
            if patient_slug:
                patient_obj = Patient.objects.get(slug=patient_slug)
                image_obj = Image.objects.create(patient=patient_obj,
                                            type=image_type, user=profile)
            else:
                image_report_obj = ImageReport.objects.get(cbct=False, id=image_report_id)
                image_obj = Image.objects.create(patient=image_report_obj.image.patient,
                                            type=image_type, user=profile)

            
            image_report_obj = ImageReport.objects.create(
                image = image_obj,
                slug = str(uuid.uuid4()).replace("-", ""),
                user = Profile.objects.get(user=user),
                name = "CBCT",
                cbct = True,
            )
            t = threading.Thread(target=convert_niftii_and_panoramic_thread, args=(folder_slug, image_report_obj, patient_slug, user, image_obj))
            t.start()
            
            return JsonResponse({"status": True, "message": "Convert Started"})
        return JsonResponse({"status": False})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def cbct_page(request,image_report_id):
    try:
        specs = get_specs()
        user = request.user
        user_theme_dict = user_theme_choices(user)

        #--GET PAGE LANG--
        if "/en/" in request.build_absolute_uri():
            lang = "en"
        else:
            lang = "tr"

        #GET PAGE LANG

        #--QUERY'S--
        image_report_obj = ImageReport.objects.get(cbct=True, id=image_report_id)
        #QUERY'S
        
        #--DICT'S--
        #DICT'S
        
        # PRINTS
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "image_report_id": image_report_id,
            "specs": specs,
        }

        return render(request,"cbct-page.html", context)

    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

#IMPLANTOLOGY
@login_required
def implantology_page(request, image_report_id):
    try:
        specs = get_specs()
        user = request.user
        user_theme_dict = user_theme_choices(user)

        tooth_chart_dict = {}
        radiography_dict = {}

        image_report_obj = ImageReport.objects.get(id=image_report_id)
        image_obj = image_report_obj.image

        def tooth_chart_function():
            dict_of_tooths = {"adult_section": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]}
            tooth_spacing_for_frontend = [
                11, 12, 13, 14, 15, 16, 17, 18, 
                21, 22, 23, 24, 25, 26, 27, 28, 
                31, 32, 33, 34, 35, 36, 37, 38,
                41, 42, 43, 44, 45, 46, 47, 48]
            tooth_icons = ToothTypeIcon.objects.filter(name="Tooth", tooth_number__in=dict_of_tooths["adult_section"]).order_by("tooth_number")

            for index, tooth in enumerate(dict_of_tooths["adult_section"]):
                tooth_spacing_index = tooth_spacing_for_frontend[index]
                tooth_obj = tooth_icons.get(tooth_number=tooth)
                tooth_number = tooth_obj.tooth_number
                name = tooth_obj.name
                icon_path = tooth_obj.icon_path
                tooth_chart_dict[tooth_number] = {"name": name, "path": icon_path, "index": tooth_spacing_index}
            return tooth_chart_dict


        def radiography_function():
            radiography_dict["path"] = image_obj.path.url if image_obj else None
            return radiography_dict

        radiography_dict = radiography_function() # RADYOGRAFİYİ ALMA FONKSİYONU
        tooth_chart_dict = tooth_chart_function() # RADYOGRAFİNİN ALTINDAKİ MENÜDEKİ DİŞ İCONLARINI NUMARALARINI HAZIRLAYAN FONKSİYON

        print("radiography_dict", radiography_dict)
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "image_report_id": image_report_id,
            "tooth_chart_section": tooth_chart_dict,
            "radiography_section": radiography_dict,
            "specs": specs,
        }
        return render(request, "dicom/implantology_report/implantology.html", context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def implantology_analyze(request, dicom_report_id):
    try:
        dicom_report_obj = DicomReport.objects.get(id=dicom_report_id)
        specs = get_specs()
        user = request.user
        user_theme_dict = user_theme_choices(user)
        image_report_obj = dicom_report_obj.image_report
        image_report_id = image_report_obj.id
        tooth_chart_section = {}
        main_image = {}
        tooth_chart_section = {}
        replaced_slice_dict = {}
        def tooth_chart_function():
            dict_of_tooths = {"adult_section": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]}
            tooth_spacing_for_frontend = [
                11, 12, 13, 14, 15, 16, 17, 18, 
                21, 22, 23, 24, 25, 26, 27, 28, 
                31, 32, 33, 34, 35, 36, 37, 38,
                41, 42, 43, 44, 45, 46, 47, 48]
            tooth_icons = ToothTypeIcon.objects.filter(name="Tooth", tooth_number__in=dict_of_tooths["adult_section"]).order_by("tooth_number")
            section_dict = {}

            for index, tooth in enumerate(dict_of_tooths["adult_section"]):
                tooth_spacing_index = tooth_spacing_for_frontend[index]
                tooth_obj = tooth_icons.get(tooth_number=tooth)
                tooth_number = tooth_obj.tooth_number
                name = tooth_obj.name
                icon_path = tooth_obj.icon_path
                section_dict[tooth_number] = {"name": name, "path": icon_path, "index": tooth_spacing_index}
            return section_dict

        def main_image_function():
            main_image["path"] = image_report_obj.image.path.url

        def replace_slice_paths():
            dicom_result_dict = json.loads(dicom_report_obj.result)
            report = dicom_result_dict["Reports"]
            tooth_spacing = report["tooth_array"]
            implant_report = report["implant_report"]
            slice_dict = {"result_dict": {}}
            for png, value in implant_report.items():
                slice_dict["result_dict"][png.replace(".png", "")] = {
                    "path": f"{dcmServerUrl}/{value['path']}",
                    "distances": {
                        "vertical_points_distance": value["vertical_points_distance"],
                        "horizontal_points_distance": value["horizontal_points_distance"]},
                    "pixel_spacing": value["pixel_spacing"],
                    "points": {
                        "horizontal": {
                            "right_point": value["horizontal_right_point"], 
                            "left_point": value["horizontal_left_point"]
                            },
                        "vertical": {
                            "upper_point": value["vertical_upper_point"],
                            "under_point": value["vertical_under_point"]
                        }
                    }
                    }
            return slice_dict, tooth_spacing
        
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
        
        
        tooth_chart_section = tooth_chart_function() # RADYOGRAFİNİN ALTINDAKİ MENÜDEKİ DİŞ İCONLARINI NUMARALARINI HAZIRLAYAN FONKSİYON
        grouped_treatments = treatment_planning_function() # KULLANICININ KAYDETTİĞİ TEDAVE PLANLAMALARINI, DAHA ÖNCESİNDEN OLUŞTURULMUŞ PLANLARLA BERABER LİSTELEYEN FONKSİYON
        main_image_function() # 
        replaced_slice_dict, tooth_spacing = replace_slice_paths() # 
        print("grouped_treatments", grouped_treatments)
        context = {
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "theme": user_theme_dict["color"],
            "image_report_id": image_report_id,
            "tooth_chart_section": tooth_chart_section,
            "grouped_treatments": grouped_treatments,
            "specs": specs,
            "dicom_result": json.dumps(replaced_slice_dict),
            "dicom_result_dict": replaced_slice_dict,
            "main_image": main_image,
            "tooth_spacing": tooth_spacing,
        }
        return render(request, "dicom/implantology_report/implantology_analyze.html", context=context)
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)


@login_required
def diagnosis3d(request, image_report_id):
    print("image_report_id", image_report_id)
    return render(request, "dicom/stl3dviewer.html")


# @csrf_exempt
# @login_required
# def dicom_upload_api(request):
#     try:
#         current_upload_progress = 0
#         if request.method == 'POST':
#             if 'file' not in request.FILES:
#                 return HttpResponse(status=500)
#             file = request.FILES['file']
#             if not file:
#                 return JsonResponse({'success': False, 'message': 'File Yok'})
#             current_chunk = int(request.POST['dzchunkindex']) + 1
#             total_chunks = int(request.POST['dztotalchunkcount'])
#             dzchunkbyteoffset = int(request.POST['dzchunkbyteoffset'])
#             folder_slug = request.POST.get('slug')
#             dicom_upload_url = f'{dicom_server_url}/dicom/dicom-image-upload'
#             files = {'file': (file.name, file.read())}  # Dosyayı isim ve içerik olarak sözlüğe ekliyoruz
#             data = {'current_chunk': current_chunk, 'total_chunks': total_chunks, 
#                     'dzchunkbyteoffset': dzchunkbyteoffset, 'folder_slug': folder_slug}
#             response = requests.post(dicom_upload_url, files=files, data=data)
#             return JsonResponse({'success': True, 'size': "3", 'progress': current_upload_progress})
#     except Exception as e:
#         user = request.user
#         traceback.print_exc()
#         error = traceback.format_exc()
#         error_handler_function(user,error)