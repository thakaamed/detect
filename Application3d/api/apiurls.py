from Application3d.api.views import *
from Application3d.api.analyze import *
from Application3d.api.third_molar_analyze import third_molar, save_third_molar
from Application3d.api.implant_analyze import implant_analysis, save_implant
from django.urls import path

urlpatterns = [
    path('start_3d_analyze', start_3d_analyze, name="start3danalyze"),
    path('end_3d_analyze', end_3d_analyze, name="end3danalyze"),
    path('create_image_report', create_image_report, name="create_image_report"),
    path('implant_analysis', implant_analysis, name="implant_analysis"),
    path('third_molar', third_molar, name="third_molar"),
    path('save_implant', save_implant, name="implant"),
    path('save_third_molar', save_third_molar, name="save_third_molar"),

    path('get_dicom_reports/<image_report_id>/', get_dicom_reports, name="getDicomReports"),
    path('get_analysis_types/', get_analysis_types, name="getAnalysisTypes"),
    path('dicom-image-upload', dicom_upload_api, name='dicom_image_upload'),
    path('get_list_of_dicoms', get_list_of_dicoms, name='getListOfDicoms'),
    path('convert_nifti_and_start_analyze', convert_nifti_and_start_analyze, name='convertNiftiStartAnalyze'), # ANALİZ BU FONKSİYONDAN BAŞLATILIYOR
    path('get_3d_labels/', get_3d_labels),
    path('get_3d_labels', get_3d_labels),
    path('get_dicom_image', get_dicom_image),
    path('get_analyzed_files', get_analyzed_files),
]