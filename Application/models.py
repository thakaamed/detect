from datetime import datetime

from User.models import Company, Profile
from django.contrib.auth.models import User
from django.db import models
import uuid
import os
from ckeditor.fields import RichTextField
import shutil
import json
GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
DRAW_TREATMENT_PLAN = (('Crown', 'Crown'), ('Implant', 'Implant'))
TYPE_CHOICES = (('Panaromic', 'Panaromic'), ('Bitewing', 'Bitewing'), ('Periapical', 'Periapical'), ('CBCT', 'CBCT'))
APPROVE_CHOICES = (("0", "blank"), ("1", "approved"), ("2", "rejected"),)
REPORT_FORMAT_CHOICES = (("SGK", "SGK"), ("PATIENT", "PATIENT"), ("DENTIST", "DENTIST"),)
REPORT_FILTER_BASED = (("PATIENT", "PATIENT"), ("TOOTH", "TOOTH"),)
ITEM_TYPE_CHOICES = (("implant", "Implant"), ("crown", "Crown"))


def get_file_path(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    _file_name_ = _file_name_ + str(uuid.uuid4()).replace("-", "")[0:10]
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/dental/radio', new_file_name)

class Patient(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    user = models.ForeignKey(Profile, models.CASCADE)
    first_name = models.CharField(max_length=240, blank=False, null=True)
    last_name = models.CharField(max_length=240, blank=False, null=True)
    full_name = models.CharField(max_length=480, blank=True, null=True)
    email = models.EmailField(max_length=160, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(max_length=240, blank=True, null=True)
    patient_id = models.IntegerField(blank=False, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100, blank=False, null=True)
    file_no = models.CharField(max_length=240, blank=True, null=True)
    created_date = models.DateTimeField(editable=True, null=True, blank=True)
    modified_date = models.DateTimeField(editable=False, null=True, blank=True)
    archived = models.BooleanField(default=False)
    favorited = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "001. Patient"

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.created_date = datetime.now()
            self.slug = str(uuid.uuid4()).replace("-", "")
            last_patient = Patient.objects.filter(user=self.user, archived=False).order_by('-id').first()
            if last_patient:
                last_patient_id = last_patient.patient_id if last_patient.patient_id else 0
                self.patient_id = last_patient_id + 1
            else:
                self.patient_id = 1
        self.modified_date = datetime.now()
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} DOCTOR: {self.user.user.first_name} {self.user.user.last_name} " \
               f"PATIENT: {self.first_name} {self.last_name}"


class ImageType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    queue = models.IntegerField(null=True, blank=True, default=0)
    ai_type_id = models.IntegerField(null=True, blank=True, default=1)
    
    class Meta:
        verbose_name_plural = "003. ImageType"
    def __str__(self):
        return f"ID: {self.id} PATIENT: {self.name}"



class Image(models.Model):
    path = models.ImageField(blank=True, null=True, upload_to=get_file_path)
    patient = models.ForeignKey(Patient, models.CASCADE)
    user = models.ForeignKey(Profile, models.CASCADE)
    type = models.ForeignKey(ImageType, models.CASCADE, blank=True, null=True)
    patient_type_id = models.IntegerField(default=0)
    thumbnail_image_path = models.ImageField(upload_to=get_file_path, verbose_name="Thumbnail Image Path",
                                             max_length=160, blank=True, null=True)
    name = models.CharField(max_length=240, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    archived = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "002. Image"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.now()
            self.name = datetime.now()
        self.updated_date = datetime.now()
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} PATIENT: {self.patient.first_name} {self.patient.last_name} " \
               f"IMAGEPATH: {self.path}" \
               f"IMAGETHUMBNAILPATH: {self.thumbnail_image_path}"


class DicomFile(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    folder_path = models.CharField(max_length=45, blank=True, null=True)
    nifti_path = models.CharField(max_length=45, blank=True, null=True)
    result_nifti_path = models.CharField(max_length=51, blank=True, null=True)
    patient = models.ForeignKey(Patient, models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.now()
        if not self.slug:
            self.slug = str(uuid.uuid4()).replace("-", "")
        if not self.folder_path:
            self.folder_path = f"dicomGroups/{self.slug}"
        if not self.nifti_path:
            self.nifti_path = f"niftiGroups/{self.slug}"
        if not self.result_nifti_path:
            self.result_nifti_path = f"resultNiftiGroups/{self.slug}"
        if not self.patient:
            raise("Patinet Field can't be empty!")
        super(DicomFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        dicoms_folder_path = os.path.join("media", self.folder_path)
        if os.path.exists(dicoms_folder_path):
            shutil.rmtree(self.folder_path, ignore_errors=True)

        # Sonra süper sınıfın delete metodu çağrılır
        super(DicomFile, self).delete(*args, **kwargs)


class ImageReport(models.Model):
    slug = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, models.CASCADE, blank=True, null=True)
    dicom = models.ForeignKey(DicomFile, models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Profile, models.CASCADE)
    name = models.CharField(max_length=240, blank=False, null=False)
    note = models.CharField(max_length=1000, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    result_json = models.TextField(blank=True, null=True)
    cbct = models.BooleanField(default=False)
    ai_response_image_type = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        verbose_name_plural = "004. ImageReport"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.now()
        self.updated_date = datetime.now()
        super(ImageReport, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}" \
               f"NAME: {self.name} {self.created_date} "
    

class ToothTypeIcon(models.Model):
    tooth_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    icon_path = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return f"tooth_number: {self.tooth_number} " \
               f"NAME: {self.name}"


class ReportTooth(models.Model):
    approve_user = models.ForeignKey(Profile, models.CASCADE, blank=True, null=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE)
    number_prediction = models.IntegerField(blank=False, null=False)
    number_correction = models.IntegerField(blank=True, null=True)
    number_edited = models.IntegerField(blank=True, null=True)
    path = models.ImageField(blank=False, null=False, upload_to="single_tooth")
    note = models.CharField(max_length=1000, blank=True, null=True)
    icon_type = models.ForeignKey(ToothTypeIcon, models.SET_NULL, blank=True, null=True)
    coordinates = models.CharField(max_length=1000, blank=True, null=True)
    approved = models.BooleanField(default=False)
    new_approve_status = models.CharField(choices=APPROVE_CHOICES, default="0", max_length=100)
    approved_date = models.DateTimeField(blank=True, null=True)
    wronged = models.BooleanField(default=False)
    wronged_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PATIENT: {self.image_report.image.patient.first_name} {self.image_report.image.patient.last_name} " \
               f"IMAGEPATH: {self.image_report.image.path} " \
               f"NAME: {self.image_report.name} " \
               f"NUMBER: {self.number_prediction} " \
               f"APPROVED STATUS: {self.approved}"

    def save(self, *args, **kwargs):
        if self.approved:
            self.approved_date = datetime.now()
        super(ReportTooth, self).save(*args, **kwargs)


class ReportToothPredict(models.Model):
    report_tooth = models.ForeignKey(ReportTooth, models.CASCADE)

    prediction = models.CharField(max_length=240, blank=True, null=True)
    correction = models.CharField(max_length=240, blank=True, null=True)
    treatment_recommendation = models.CharField(max_length=240, blank=True, null=True)

    approved = models.BooleanField(default=False)
    new_approve = models.CharField(choices=APPROVE_CHOICES, default="0", max_length=100)
    approved_date = models.DateTimeField(blank=True, null=True)
    approve_user = models.ForeignKey(Profile, models.CASCADE, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_illness = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.approved:
            self.approved_date = datetime.now()
        super(ReportToothPredict, self).save(*args, **kwargs)

    def __str__(self):
        return f"PATIENT: {self.report_tooth.image_report.image.patient.first_name} {self.report_tooth.image_report.image.patient.last_name} " \
               f"IMAGEPATH: {self.report_tooth.image_report.image.path} " \
               f"NAME: {self.report_tooth.image_report.name} " \
               f"NUMBER: {self.report_tooth.number_prediction} "


class LabelForAddDiagnosis(models.Model):
    name = models.CharField(max_length=160)
    tr_name = models.CharField(max_length=160, default="")
    color = models.CharField(max_length=160, blank=True, null=True)

    def __str__(self):
        return f"ID:{self.pk} | NAME: {self.name})"

    def save(self, *args, **kwargs):
        super(LabelForAddDiagnosis, self).save(*args, **kwargs)


class ApprovedPortalTermsOfUse(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)


class AnalysisDetailLog(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"user:{self.user} " \
               f"image_report: {self.image_report.image.path} {self.image_report.image.patient.first_name} {self.image_report.image.patient.last_name}" \
               f"date: {self.date} "

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
        super(AnalysisDetailLog, self).save(*args, **kwargs)


class UserInformations(models.Model):
    username = models.CharField(max_length=150, blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=50, blank=True, null=True)
    process_date = models.DateTimeField(blank=True, null=True)
    log_page = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"ID-USERNAME: {self.id} {self.username} " \
               f"ip_address: {self.ip_address} " \
               f"log_page: {self.log_page} "


class TreatmentPlanning(models.Model):
    image_report = models.ForeignKey(ImageReport, models.CASCADE)
    created_date = models.DateTimeField(null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    updated_planning = RichTextField(blank=True)
    ai_planning = RichTextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.now()
        self.modified_date = datetime.now()
        super(TreatmentPlanning, self).save(*args, **kwargs)

    def __str__(self):
        return f"Image Report:{self.image_report}"


class IllnessLabel(models.Model):
    label_type = models.CharField(max_length=100,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    tr_name = models.CharField(max_length=100,null=True, blank=True)
    color = models.CharField(max_length=100,null=True, blank=True)
    model = models.CharField(max_length=100,null=True, blank=True)
    model_label_name = models.CharField(max_length=100,null=True, blank=True)
    illness_slug = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"Label: {self.name}"


class TreatmentMethod(models.Model):
    tr_treatment_method = models.CharField(max_length=100,null=True, blank=True)
    en_treatment_method = models.CharField(max_length=100,null=True, blank=True)
    fr_treatment_method = models.CharField(max_length=100,null=True, blank=True)
    slug = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"Treatment: {self.tr_treatment_method}"
    

class IllnessTreatmentMethod(models.Model):
    label = models.ManyToManyField(IllnessLabel, blank=True)
    treatment_method = models.ManyToManyField(TreatmentMethod, blank=True)
    radiography_type = models.TextField(max_length=100,null=True, blank=True)
    slug = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"Label: {list(self.label.all())} - Treatment Method: {list(self.treatment_method.all())}, - "


class TreatmentRecommendationForTooth(models.Model):
    # recommendations = models.ForeignKey(IllnessTreatmentMethod, models.CASCADE, null=True, blank=True)
    recommendation = models.ManyToManyField(TreatmentMethod, blank=True)
    tooth = models.ForeignKey(ReportTooth, models.CASCADE, null=True, blank=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Recommendation: {list(self.recommendation.all())}"
    
class SuggestImplantToMissingTooth(models.Model):
    tooth_number = models.CharField(max_length=3, blank=True, null=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE, null=True, blank=True)
    recommendation = models.ManyToManyField(TreatmentMethod, blank=True)

    def __str__(self):
        return f"Suggested Tooth Number: {self.tooth_number}"



class CreateReportForPatientOptions(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"Option: {self.name}"


class CreateReportForPatient(models.Model):
    format = models.CharField(choices=REPORT_FORMAT_CHOICES, max_length=100)
    options = models.ManyToManyField(CreateReportForPatientOptions,max_length=100, blank=True)
    filter_report_based = models.CharField(choices=REPORT_FILTER_BASED, max_length=100)
    qr_code = models.ImageField(upload_to=os.path.join("media", "qrcodes"), null=True, blank=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, models.CASCADE, null=True, blank=True)
    drawed_image_path = models.CharField(max_length=500, blank=True, null=True)
    drawed_implant_crown_image_path = models.CharField(max_length=500, blank=True, null=True)


class ReportPageIllnessDescriptions(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    before_tooth_numbers_text_tr = models.CharField(max_length=200,null=True, blank=True)
    before_tooth_numbers_text_en = models.CharField(max_length=200,null=True, blank=True)
    before_tooth_numbers_text_fr = models.CharField(max_length=200,null=True, blank=True)
    after_tooth_numbers_text_tr = models.CharField(max_length=200,null=True, blank=True)
    after_tooth_numbers_text_en = models.CharField(max_length=200,null=True, blank=True)
    after_tooth_numbers_text_fr = models.CharField(max_length=200,null=True, blank=True)
    radiography_type = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f"type: {self.radiography_type}, name: {self.name}"


class ReportMails(models.Model):
    sender = models.ForeignKey(Profile, models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(Patient, models.CASCADE, null=True, blank=True)
    sending_date = models.DateTimeField(null=True, blank=True)
    report_slug = models.CharField(null=True, blank= True, max_length=50)

    def __str__(self):
        return f"Sender:{self.sender.user.username} " \
               f"Receiver:{self.receiver.first_name} {self.receiver.last_name}"


class DoctorChoicesForReport(models.Model):
    format = models.CharField(choices=REPORT_FORMAT_CHOICES, max_length=100, null=True, blank=True)
    filter_report_based = models.CharField(choices=REPORT_FILTER_BASED, max_length=100,null=True, blank=True)
    profile = models.ForeignKey(Profile, models.CASCADE, null=True, blank=True)
    choices = models.ManyToManyField(CreateReportForPatientOptions, max_length=100, blank=True)


class FormQuestion(models.Model):
    question = models.CharField(max_length=255,null=True, blank=True)
    question_tr = models.CharField(max_length=255,null=True, blank=True)
    answers = models.CharField(max_length=1000,null=True, blank=True)
    answers_tr = models.CharField(max_length=1000,null=True, blank=True)
    slug = models.CharField(max_length=32,null=True, blank=True)
    queue = models.IntegerField(null=True, blank=True)
    manual_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"en_name:{self.question} " \
               f"tr_name:{self.question_tr}" \
               f"ID: {self.id} " \
               f" Slug: {self.slug}"
    

def get_questions_with_json():
    questions = FormQuestion.objects.all()
    for question in questions:
        if question.answers:
            question.answers = json.loads(question.answers)
        if question.answers_tr:
            question.answers_tr = json.loads(question.answers_tr)
    return questions
# answers = {
#     "option1": "Omnivore",
#     "option2": "Vegetarian",
#     "option3": "Vegan",
#     "option4": "Pescatarian",
#     "option5": "Gluten-free",
#     "option6": "Other (please specify)",
# }
# answers_tr = {
#     "option1": "Hepçil",
#     "option2": "Vejetaryen",
#     "option3": "Vegan",
#     "option4": "Pesketaryen",
#     "option5": "Glutensiz",
#     "option6": "Diğer (lütfen belirtin)",
# }
# question = FormQuestion.objects.create(question="What is your dietary preference?", question_tr="Diyet tercihiniz nedir?", answers=json.dumps(answers), answers_tr=json.dumps(answers_tr,ensure_ascii=False))


class FormWithCompany(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    question = models.ForeignKey(FormQuestion, models.CASCADE)
    required = models.BooleanField()
    is_active = models.BooleanField()
    form_slug = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f"en_name:{self.question.question} " \
               f"tr_name:{self.question.question_tr} " \
               f"show:{self.is_active}"


class FormAnswers(models.Model):
    form = models.ForeignKey(FormWithCompany,models.CASCADE,null=True,blank=True)
    question_slug = models.CharField(max_length=32)
    group_slug = models.CharField(max_length = 100)
    date = models.DateTimeField(null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    specify = models.CharField(max_length=255,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.created_date = datetime.now()
        super(FormAnswers, self).save(*args, **kwargs)

    def __str__(self):
        return f"answer:{self.answer}"


class FormRadiographs(models.Model):
    form_answer_group_slug = models.CharField(max_length = 100)
    path = models.ImageField(blank=False, null=False, upload_to=get_file_path)


class DrawedTreatment(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE, null=True, blank=True)
    coordinates = models.CharField(max_length=200,null=True, blank=True)
    transform = models.CharField(max_length=200,null=True, blank=True)
    size = models.CharField(max_length=200,null=True, blank=True)
    type = models.CharField(choices=DRAW_TREATMENT_PLAN, max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.now()
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} IMAGEREPORT: {self.image_report} TYPE: {self.type}"


class SpecificParameter(models.Model):
    loginpage_logo_design = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "img"))
    loginpage_banner = models.ImageField(blank=True, null=True, upload_to=os.path.join("static", "img"))
    base_html_css = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "css"))
    base_html_left_top_logo = models.ImageField(blank=True, null=True, upload_to=os.path.join("static", "img"))
    base_html_left_bottom_title = models.CharField(max_length=50, null=True, blank=True)
    language_visibility = models.BooleanField(default=False)
    page_title = models.CharField(max_length=50, null=True, blank=True)
    report_page_title_banner = models.ImageField(blank=True, null=True, upload_to=os.path.join("static", "img"))
    favicon = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "img"))
    clarification_text = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "pdf"))
    cookie_policy = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "pdf"))
    privacy_policy = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "pdf"))
    terms_conditions_policy = models.FileField(blank=True, null=True, upload_to=os.path.join("static", "pdf"))
    login_page_content = models.TextField(blank=True, null=True)
    website_link = models.CharField(max_length=50, null=True, blank=True)
    website_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} PAGE TITLE: {self.page_title}"


class DrawedImplantOrCrown(models.Model):
    slug = models.CharField(max_length=32, null=True, blank=True)
    image_report = models.ForeignKey(ImageReport, models.CASCADE, null=True, blank=True)
    item_type = models.CharField(choices=ITEM_TYPE_CHOICES, max_length=10, blank=False, null=True)
    icon_id = models.IntegerField(blank=False, null=True)
    coordinate = models.CharField(max_length=50, blank=False, null=True)
    dimension = models.CharField(max_length=50, blank=False, null=True)
    rotate = models.IntegerField(blank=False, null=True)
    original_shape = models.CharField(max_length=50, blank=False, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.created_date = datetime.now()
            self.slug = str(uuid.uuid4()).replace("-", "")
        super(DrawedImplantOrCrown, self).save(*args, **kwargs)


    def __str__(self):
        return f"ID: {self.id} PAGE TITLE: {self.item_type}"

class ActiveUsers(models.Model):
    active_users = models.ManyToManyField(User)
    active_user_count = models.IntegerField(default=0, null=True, blank=True)

class SpecificUserLoginDiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateTimeField(blank=True, null=True)
    logout_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"User: {self.user.username} Login: {self.login_date} Logout: {self.logout_date}"
    
class ErrorLog(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    # exception_type = models.TextField(blank=True, null=True)
    # request = models.TextField(blank=True, null=True)
    traceback_info=models.TextField(blank=True, null=True)
    # view_function=models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_solved = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        self.created_at = datetime.now()
        super(ErrorLog, self).save(*args, **kwargs)
    
class LoginErrorLog(models.Model):
    email = models.CharField(max_length=150, blank=True, null=True)
    traceback_info=models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.created_at = datetime.now()
        super(LoginErrorLog, self).save(*args, **kwargs)

class Currency(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    equal = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - name: {self.name}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    ui_design_star = models.IntegerField(null=True, blank=True)
    ui_design_comment = models.CharField(null=True, blank=True, max_length=999)
    bug_star = models.IntegerField(null=True, blank=True)
    bug_comment = models.CharField(null=True, blank=True, max_length=999)
    features_star = models.IntegerField(null=True, blank=True)
    features_comment = models.CharField(null=True, blank=True, max_length=999)
    performance_star = models.IntegerField(null=True, blank=True)
    performance_comment = models.CharField(null=True, blank=True, max_length=999)
    expected_outcome_star = models.IntegerField(null=True, blank=True)
    expected_outcome_comment = models.CharField(null=True, blank=True, max_length=999)
    created_at = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        self.created_at = datetime.now()
        super(Feedback, self).save(*args, **kwargs)