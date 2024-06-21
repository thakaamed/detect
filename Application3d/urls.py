from django.urls import path, include
from django.contrib import admin
from Application3d.views import *

urlpatterns = [
    path('stl-viewer/<dicom_report_id>', dicom_stl_viewer, name='dicom_stl_viewer'),
    path('dicom_upload', dicom_upload_page, name='dicom_upload_page'),
    # path('dicom-image-upload', dicom_upload_api, name='dicom_image_upload'),
    path('convert-nii-and-pano', convert_niftii_and_panoramic, name='convert_niftii_and_panoramic'),
    path('CBCT/<image_report_id>', cbct_page, name='cbct_page'),
    
    path('implantology/<image_report_id>', implantology_page, name="ImplantologyPage"),
    path('implantology/analyze/<dicom_report_id>', implantology_analyze, name="ImplantologyAnalyzePage"),
    path('diagnosis3d/<image_report_id>', diagnosis3d, name="diagnosis3d")

]


