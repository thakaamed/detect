from django.contrib import admin
from Application3d.models import *
from Application.models import DicomFile
# Register your models here.

admin.site.register(DicomAnalysisType)
admin.site.register(DicomReport)
admin.site.register(DicomUploadProgress)
admin.site.register(DicomFile)
