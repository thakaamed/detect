import cv2
import json
import numpy as np
import os
import pandas as pd
import requests
import traceback
from Server.settings import BASE_DIR
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from django.forms.models import model_to_dict
# from src.classification.classification import predict
from threading import Thread
from User.models import *
from Application.models import *
import pydicom
import imageio
from django.conf import settings
import uuid
from Application.api.analyze import start_manuel_analyze
# class RecordSerializerPage(ModelSerializer):
#     company = Company(api_key='company_api_key')

#     class Meta:
#         model = Patient
#         fields = ['first_name', 'last_name', 'gender', 'date_of_birth' 'user__api_key']

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['path']

class RecordSerializerPage(serializers.ModelSerializer):
    company__api_key = serializers.CharField(source='user.profile.company.api_key')
    user__api_key = serializers.CharField(source='user.api_key')

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'file_no', 'date_of_birth', 'gender', 'user__api_key', 'company__api_key']

    def create(self, validated_data):
        print("validated before", validated_data)
        user = validated_data.pop('user')
        print("user", user["api_key"])
        print("validated_data", validated_data)
        user = Profile.objects.get(api_key=user["api_key"])

        patient = Patient.objects.create(user=user, **validated_data)
        print("created", patient)
        return patient
    
class RadiographyAnalyzeApi(APIView):
    print("apiveiew")
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = RecordSerializerPage
    def post(self, request, api_version):
        print("request", request)
        print("api_version", api_version, type(api_version))
        try:
            if float(api_version) >= 1.5:
                print("request2", request.data)
                company_api_key = request.data.get("company__api_key")
                user_api_key = request.data.get("user__api_key")
                print("company", company_api_key)
                print("user", user_api_key)

                if not company_api_key or not user_api_key:
                    return Response({'status': False, 'message': 'API key required'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                company = Company.objects.filter(api_key=company_api_key).first()
                profile = Profile.objects.filter(api_key=user_api_key).first()
                print("obj company", company)
                print("obj prof", profile)
                if company is None or profile is None:
                    return Response({'status': False, 'message': 'Unknown api key'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            patient_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'file_no': request.data.get('file_no'),
                'date_of_birth': request.data.get('date_of_birth'),
                'gender': request.data.get('gender'),
                'user__api_key': request.data.get('user__api_key'),
                'company__api_key': request.data.get('company__api_key'),
            }
            print("patient_data", patient_data)
            patient_serializer = RecordSerializerPage(data=patient_data)
            if patient_serializer.is_valid():
                print("patient_isvalid")
                patient = patient_serializer.save()
                file = request.data.get('image.path')
                slug = str(uuid.uuid4()).replace("-", "")
                if file:
                    if file.name.lower().endswith(".dcm"):
                        print("dcm_file", file)
                        dicom = pydicom.dcmread(file)
                        print("dicom", dicom)
                        image_data = dicom.pixel_array.astype(np.int16)
                        
                        image_path = f'{settings.image_path_without_slash_after_media}/dental/radio/{slug}.png'
                        image_data = imageio.imwrite(image_path, image_data)
                        print("aa", image_data)
                        image_data = {'path': f'media/dental/radio/{slug}.png'}
                        print("image_data", image_data)
                        try:
                            image_obj = Image.objects.create(path=image_data['path'], patient=patient, user=profile, type=ImageType.objects.get(id=1))

                        except:
                            traceback.print_exc()
                            patient.delete()
                            return Response('ImageCreationFailed', status=status.HTTP_400_BAD_REQUEST)
                        
                        start_manuel_analyze(profile.user, image_obj.id, f'/media/dental/radio/{slug}.png')

                    else:
                        extension = file.name.split(".")[-1]
                        file.filename = f"{slug}.{extension}"
                        image_data = {'path': file}
                        print("image_data", image_data)
                        try:
                            image_obj = Image.objects.create(path=image_data['path'], patient=patient, user=profile, type=ImageType.objects.get(id=1))

                        except:
                            traceback.print_exc()
                            patient.delete()
                            return Response('ImageCreationFailed', status=status.HTTP_400_BAD_REQUEST)
                        
                        start_manuel_analyze(profile.user, image_obj.id, image_obj.path.url)

                return Response({'status': True, 'message': 'Patient and Image created successfully'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response({'status': False, "message": "Unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)