from django.db import models
from Application.models import ImageReport,TreatmentMethod
from User.models import Company
import os
from ckeditor.fields import RichTextField
import uuid

# Create your models here.

def get_file_path(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/svg_teeth_images', new_file_name)
    
def get_file_path_for_pdf_cover(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/pdf_covers', new_file_name)

class TreatmentWizard(models.Model):
    image_report = models.ForeignKey(ImageReport, models.CASCADE,blank=True, null=True)
    general_tags = models.TextField(blank=True, null=True)
    diagnosis_data = models.TextField(null=True,blank=True)
    raw_treatment_data = models.TextField(null=True, blank=True)

class DefaultCoverImages(models.Model):
    pdf_cover = models.ImageField(blank=True, null=True, upload_to=get_file_path_for_pdf_cover)
    pdf_finish_cover = models.ImageField(blank=True, null=True, upload_to=get_file_path_for_pdf_cover)


class DocumentTemplates(models.Model):
    template_group_name = models.CharField(max_length = 99, null=True, blank=True)
    template_group_queue = models.IntegerField(blank=True, null=True)
    template_name = models.CharField(max_length = 99, null=True, blank=True)
    template_content = RichTextField(null=True, blank=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    containing_radiography = models.BooleanField(default=False)
    containing_cover_image = models.BooleanField(default=False)
    containing_end_cover_image = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4()).replace("-", "")
        super(DocumentTemplates, self).save(*args, **kwargs)

class TreatmentPlan(models.Model):
    treatment_wizard = models.ForeignKey(TreatmentWizard, models.CASCADE, null=True,blank=True)
    plan_treatment_data = models.TextField(blank=True, null=True)
    plan_queue = models.IntegerField(default=1, blank=True, null=True)
    plan_pricing = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    general_note = models.TextField(blank=True, null=True)
    discount = models.IntegerField(default=0, blank=True, null=True)
    pdf_file = models.CharField(max_length = 999, blank=True, null=True)
    pdf_created_date = models.DateTimeField(blank=True, null=True)
    drawed_radiography_path = models.CharField(max_length=500, blank=True, null=True)
    
class ClinicSavedTemplatesForTreatment(models.Model):
    templates = models.ManyToManyField(DocumentTemplates, blank=True)
    treatment_plan = models.ForeignKey(TreatmentPlan, models.CASCADE, null=True,blank=True)

class ClinicModifiedTemplates(models.Model):
    template = models.ForeignKey(DocumentTemplates, models.CASCADE, blank=True)
    company = models.ForeignKey(Company, models.CASCADE, null=True,blank=True)
    modified_content = RichTextField(null=True, blank=True)


class TeethImages(models.Model):
    teeth_number = models.IntegerField(null=True,blank=True)
    path = models.FileField(blank=True, null=True, upload_to=get_file_path)
    svg_paths_dict = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"ID: {self.id} TOOTH NUMBER: {self.teeth_number}"
    
class LabelNameGroup(models.Model):
    group_name = models.CharField(max_length=999,null=True,blank=True)
    def __str__(self):
        return f"ID: {self.id} GROUP NAME: {self.group_name}"
    
class LabelNamesForWizard(models.Model):
    group = models.ForeignKey(LabelNameGroup,models.CASCADE,null=True, blank=True)
    en_name = models.CharField(max_length=999,null=True,blank=True)
    tr_name = models.CharField(max_length=999,null=True,blank=True)
    pt_name = models.CharField(max_length=999,null=True,blank=True)
    ar_name = models.CharField(max_length=999,null=True,blank=True)
    fr_name = models.CharField(max_length=999,null=True,blank=True)
    slug = models.CharField(max_length=999,null=True,blank=True)
    sub_label_status = models.BooleanField(default=False)
    sub_of_this = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            # Eğer slug yoksa, yeni bir uuid oluştur
            self.slug = str(uuid.uuid4())[:16]
        super().save(*args, **kwargs)
    def __str__(self):
        return f"ID: {self.id} LABEL: {self.en_name}"
    
class TreatmentNameGroup(models.Model):
    group_name = models.CharField(max_length=999,null=True,blank=True)
    def __str__(self):
        return f"ID: {self.id} GROUP NAME: {self.group_name}"
    
class TreatmentNamesForWizard(models.Model):
    group = models.ForeignKey(TreatmentNameGroup,models.CASCADE,null=True, blank=True)
    en_name = models.CharField(max_length=999,null=True,blank=True)
    tr_name = models.CharField(max_length=999,null=True,blank=True)
    pt_name = models.CharField(max_length=999,null=True,blank=True)
    ar_name = models.CharField(max_length=999,null=True,blank=True)
    fr_name = models.CharField(max_length=999,null=True,blank=True)
    uz_name = models.CharField(max_length=999,null=True,blank=True)
    ru_name = models.CharField(max_length=999,null=True,blank=True)
    nl_name = models.CharField(max_length=999,null=True,blank=True)
    slug = models.CharField(max_length=999,null=True,blank=True)
    ai_slug = models.CharField(max_length=999,null=True,blank=True)
    sub_label_status = models.BooleanField(default=False)
    sub_of_this = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            # Eğer slug yoksa, yeni bir uuid oluştur
            self.slug = str(uuid.uuid4())[:16]
        super().save(*args, **kwargs)
    def __str__(self):
        return f"ID: {self.id} LABEL: {self.en_name} -- GROUP: {self.group.group_name}"


class CompanyTreatmentPricing(models.Model):
    company = models.ForeignKey(Company, models.CASCADE,null=True,blank=True)
    treatment_method = models.ForeignKey(TreatmentNamesForWizard, models.CASCADE,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    currency = models.CharField(max_length = 99, blank=True, null=True)

class ExtraTreatmentPlans(models.Model):
    treatment_wizard = models.ForeignKey(TreatmentWizard, models.CASCADE)
    treatment_plan = models.ForeignKey(TreatmentPlan, models.CASCADE, null=True, blank=True)
    selected_treatments = models.CharField(null=True, blank=True, max_length=999)
# class TeethDiseaseAndTreatmentSvg(models.Model):
#     teeth_number = models.IntegerField(null=True,blank=True)
#     svg_paths_dict = models.TextField(null=True,blank=True)
#     def __str__(self):
#         return f"TOOTH NUMBER: {self.teeth_number}"
