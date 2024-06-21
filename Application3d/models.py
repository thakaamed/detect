from django.db import models
from Application.models import ImageReport, Patient
import uuid
from datetime import datetime
from User.models import Profile


# Create your models here.


class DicomAnalysisType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    tr_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4()).replace("-", "")
        super(DicomAnalysisType, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} {self.name} {self.active}"

class DicomReport(models.Model):
    slug = models.TextField(blank=True, null=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE)
    result = models.TextField(blank=True, null=True)
    report_type = models.ForeignKey(DicomAnalysisType, models.SET_NULL, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.now()
        if not self.slug:
            self.slug = str(uuid.uuid4()).replace("-", "")
        super(DicomReport, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} {self.image_report.id} " \
               f"report_type: {self.report_type} "
    
    
class DicomUploadProgress(models.Model):
    progress_name = models.CharField(max_length=100, blank=True, null=True)
    progress = models.CharField(max_length=100, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"progress_name: {self.id} {self.progress_name} " \
               f"progress: {self.progress} " \
               f"is_completed: {self.is_completed} "

