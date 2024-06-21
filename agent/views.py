import os.path
import traceback
from django.shortcuts import render
from Application.models import *
from User.models import *
from datetime import datetime, timedelta, date
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
import uuid
from Server.settings import ccclinic_path_with_slash, ccclinic_path
import time
from django.views import View
from django.middleware import csrf
from django.utils.decorators import method_decorator
import os
import cv2
from Application.api.analyze import start_manuel_analyze
from PIL import Image as pil_Image
from io import BytesIO
import imageio
import pydicom
import numpy as np
import logging

ERROR_LOG_FILE_PATH = "/home/ubuntu/Clinic/agent/agent_error.log"

# Hata log konfigürasyonu
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)  # Sadece ERROR seviyesi ve üzerindeki hataları kaydedecek
error_handler = logging.FileHandler(ERROR_LOG_FILE_PATH)
error_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

class analyze(View):

    csrf_protected_method = method_decorator(csrf_protect)
    def post(self, request):
        # CSRF token'ını almak gerekli değil, csrf_protect zaten bu işlemi yapar
        self.company_key = request.POST.get("company__api_key")
        self.first_name = request.POST.get("first_name")
        self.last_name = request.POST.get("last_name")
        self.date_of_birth = request.POST.get("date_of_birth")
        self.card_id = request.POST.get("card_id")
        self.gender = request.POST.get("gender")
        self.user_key = request.POST.get("user__api_key")
        self.user_check = request.POST.get("user_check")
        self.radiography = request.FILES["image"]
        self.analyze_radiography = None
        self.user_profile = None
        self.patient_obj = None
        self.image_obj = None
        self.status = True
        self.message = "" 
        self.analyze_status = ""
        print("verifying_keys", flush=True)
        self.verify_keys()

        return JsonResponse({"status": self.status, "message": self.message, "analyze_status": self.analyze_status})

    def verify_keys(self):
        # Bu kısımda Profile'ı almak için gerekli kodu ekleyin ve gerekirse hataları ele alın
        try:
            user_profile = Profile.objects.get(api_key=self.user_key, company__api_key=self.company_key)
            self.user_profile = user_profile
            self.convert_radiography()
        except Exception as e:
            error_message = f"Exception at 'Profile.DoesNotExist' occurred in create_patient: {str(e)}"
            error_logger.error(error_message)
            self.status = False
            self.message = "Wrong API Key"
            return JsonResponse({"status": self.status, "message": self.message})

    def convert_radiography(self):
        def convert_to_png(base_path, png_path):
            try:
                convert_image = pil_Image.open(base_path)
                convert_image.save(png_path, format='PNG')
                return True
            except Exception as e:
                error_message = f"Exception at 'Creating PNG from file' occurred in convert_to_png {self.radiography.name}: {str(e)}"
                error_logger.error(error_message)
                return False
        file_extension = self.radiography.name.split('.')[-1].lower()
       
        # İşlem yapmak istediğiniz dosya uzantısına göre karar verin
        if file_extension == 'png' or file_extension == 'jpg' or file_extension == 'jpeg':
            # PDF dosyası işleme
            # Örnek: PDF dosyasını okuma, içeriği analiz etme, vb.
            self.analyze_radiography = self.radiography 
        elif file_extension == 'dcm':
            def save_dcm_as_png(dcm_path, png_path):
                try:
                    dcm_data = pydicom.dcmread(dcm_path)
                    dcm_slice = dcm_data.pixel_array
                    min_value = np.min(dcm_slice)
                    max_value = np.max(dcm_slice)
                    dcm_slice = (dcm_slice - min_value) / (max_value - min_value) * 255
                    dcm_slice = dcm_slice.astype(np.uint8)
                    imageio.imsave(png_path, dcm_slice)
                    return True
                except Exception as e:
                    error_message = f"Exception at 'Saving DCM as PNG' occurred in save_dcm_as_png {self.radiography.name}: {str(e)}"
                    error_logger.error(error_message)
                    return False

            dcm_slug = str(uuid.uuid4())
            dcm_path = f'{ccclinic_path_with_slash}media/temporary_dcm/{dcm_slug}.dcm'
            with open(dcm_path, 'wb') as f:
                for chunk in self.radiography.chunks():
                    f.write(chunk)

            # PNG dosyasını geçici olarak kaydet
            png_path = f'{ccclinic_path_with_slash}media/dental/radio/{dcm_slug}.png'
            if save_dcm_as_png(dcm_path, png_path):
                # Dönüşüm başarılıysa TemporaryUploadedFile oluştur
                self.analyze_radiography = png_path.replace(ccclinic_path_with_slash, "")
                print("analyze", self.analyze_radiography, flush=True)
                os.remove(dcm_path)
            else:
                self.status = False
                self.message = '.dcm dosyasi dönüştürülemedi.'

        elif file_extension == 'tiff' or file_extension == 'tif':
            try:
                # TIFF dosyasını geçici bir yere kaydet
                tiff_slug = str(uuid.uuid4())
                tiff_path = f'{ccclinic_path_with_slash}media/temporary_tiff/{tiff_slug}.{file_extension}'
                with open(tiff_path, 'wb') as f:
                    for chunk in self.radiography.chunks():
                        f.write(chunk)
                
                # PNG dosyasını geçici olarak kaydet
                png_path = f'{ccclinic_path_with_slash}media/dental/radio/{tiff_slug}.png'
                if convert_to_png(tiff_path, png_path):
                    # Dönüşüm başarılıysa TemporaryUploadedFile oluştur
                    self.analyze_radiography = png_path.replace(ccclinic_path_with_slash, "")
                    print("analyze", self.analyze_radiography, flush=True)
                    os.remove(tiff_path)
                else:
                    self.status = False
                    self.message = f'.{file_extension} dosyasi dönüştürülemedi.'
            except Exception as e:
                error_message = f"Exception at 'Saving tif or tiff file' occurred in convert_radiography: {str(e)}"
                error_logger.error(error_message)
        
        elif file_extension == 'bmp':
            try:
                # TIFF dosyasını geçici bir yere kaydet
                bmp_slug = str(uuid.uuid4())
                bmp_path = f'{ccclinic_path_with_slash}media/temporary_bmp/{bmp_slug}.bmp'
                with open(bmp_path, 'wb') as f:
                    for chunk in self.radiography.chunks():
                        f.write(chunk)
                
                # PNG dosyasını geçici olarak kaydet
                png_path = f'{ccclinic_path_with_slash}media/dental/radio/{bmp_slug}.png'
                if convert_to_png(bmp_path, png_path):
                    # Dönüşüm başarılıysa TemporaryUploadedFile oluştur
                    self.analyze_radiography = png_path.replace(ccclinic_path_with_slash, "")
                    print("analyze", self.analyze_radiography, flush=True)
                    os.remove(bmp_path)
                else:
                    self.status = False
                    self.message = '.bmp dosyasi dönüştürülemedi.'
            except Exception as e:
                error_message = f"Exception at 'Saving bmp file' occurred in convert_radiography {self.radiography.name}: {str(e)}"
                error_logger.error(error_message)
        else:
            # Desteklenmeyen dosya uzantısı
            self.status = False
            self.message = 'Desteklenmeyen dosya uzantısı'
            error_message = f"Exception at 'else' occurred in convert_radiography {self.radiography.name}: {self.message}"
            error_logger.error(error_message)
            return JsonResponse({"status": self.status, "message": self.message})
        self.create_patient(file_extension)

    def create_patient(self, file_extension):
        try:
            gender = None if self.gender == "Unknown" else "Male" if self.gender == "f" else "Female"
            if self.card_id != "Unknown" and self.card_id is not None:
                patient_obj, created = Patient.objects.get_or_create(
                    user = self.user_profile,
                    file_no = self.card_id
                )
                if created:
                    try:
                        patient_obj.user = self.user_profile
                        patient_obj.first_name = self.first_name
                        patient_obj.last_name = self.last_name
                        patient_obj.full_name = f"{self.first_name} {self.last_name}"
                        patient_obj.date_of_birth = datetime.strptime(self.date_of_birth, '%Y-%m-%d') if self.date_of_birth != "Unknown" else None
                        patient_obj.gender = gender
                        patient_obj.save()
                    except Exception as e:
                        error_message = f"Exception at 'created' occurred in create_patinet: {str(e)}"
                        error_logger.error(error_message)
                        patient_obj.delete()
            else:
                patient_obj = Patient.objects.create(
                    user = self.user_profile,
                    first_name = self.first_name,
                    last_name = self.last_name,
                    full_name = f"{self.first_name} {self.last_name}",
                    date_of_birth = datetime.strptime(self.date_of_birth, '%Y-%m-%d') if self.date_of_birth != "Unknown" else None,
                    gender = gender,
                    file_no = "Unknown"
                )
            self.patient_obj = patient_obj
        except Exception as e:
            error_message = f"Exception at 'Creating Patinet' occurred in create_patient: {str(e)}"
            error_logger.error(error_message)
        self.create_image(file_extension)

    def create_image(self, file_ext):
        try:
            if file_ext == "tiff" or file_ext == "tif" or file_ext == "dcm" or file_ext == "bmp":
                self.image_object = Image.objects.create(path=self.analyze_radiography, patient=self.patient_obj, user=self.user_profile)
            else:
                original_file_name, file_extension = os.path.splitext(self.analyze_radiography.name)
                new_file_name = str(uuid.uuid4()) + file_extension
                self.analyze_radiography.name = new_file_name
                self.image_object = Image.objects.create(path=self.analyze_radiography, patient=self.patient_obj, user=self.user_profile)
            try:
                img_path = self.image_object.path.path
                name, extension = os.path.splitext(img_path)
                new_img_path = name + ".jpg"

                thumbnail_image_path = new_img_path.replace('.', '_thumbnail.')
                thumbnail_image_path = thumbnail_image_path.replace(ccclinic_path + "/", "")
                cv2.imwrite(thumbnail_image_path, cv2.resize(cv2.imread(self.image_object.path.path), (250, 109)))
                self.image_object.save()
                manuel_analyze_return_dict = start_manuel_analyze(self.user_profile.user, self.image_object.id, self.image_object.path.url)
                self.analyze_status = manuel_analyze_return_dict
            except Exception as e:
                error_message = f"Exception at 'Saving image obj or start_manuel_analyze' occurred in create_image: {str(e)}"
                error_logger.error(error_message)
                self.patient_obj.delete()
                self.image_object.delete()
        except Exception as e:
            error_message = f"Exception at 'Creating Image' occurred in create_image: {str(e)}"
            error_logger.error(error_message)
            traceback.print_exc()
            self.status = False
            self.message = "Error at Creating Image"
            self.patient_obj.delete()
            return JsonResponse({"status": self.status, "message": self.message})

    def get(self, request):
        csrf_token = csrf.get_token(request)
        return JsonResponse({'X-CSRFToken': csrf_token})


@csrf_exempt
def check_user(request):
    print(request)
    user_key = request.POST.get('user_key')
    company_key = request.POST.get('company_key')
    try:
        user_profile = Profile.objects.get(api_key=user_key, company__api_key=company_key)
        return JsonResponse({"status": True})
    except Profile.DoesNotExist as e:
        error_message = f"Exception at 'Checking User and Company Key' user key: {user_key} company key: {company_key} occurred in check_user: {str(e)}"
        error_logger.error(error_message)
        return JsonResponse({"status": False, "message": "Wrong API Key"})