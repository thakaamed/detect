from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
import uuid
USER_CHOICES = (('CranioCatch Group', 'CranioCatch Group'), ('Customer', 'Customer'))
TokenActivityChoices = (('Panaromic', 'Panaromic'), ('Bitewing', 'Bitewing'), ('CBCT', 'CBCT'), ('Periapical', 'Periapical'), ('Lateral Cephalometric', 'Lateral Cephalometric'))

def get_file_path(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/profile_photos', new_file_name)

def get_file_path_for_signature(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/signature_images', new_file_name)

def get_file_path_for_clinic_logo(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/clinic_logo', new_file_name)

def get_file_path_for_pdf_cover(instance, filename):
    _file_name, file_extension = os.path.splitext(filename)
    _file_name_ = _file_name.replace(".", "_")
    new_file_name = _file_name_ + file_extension
    return os.path.join('media/pdf_covers', new_file_name)


class Company(models.Model):
    name = models.CharField(max_length=160)
    logo = models.ImageField(upload_to=os.path.join("media", "clinic_logo"), blank=True, null=True)
    pdf_cover = models.ImageField(blank=True, null=True, upload_to=get_file_path_for_pdf_cover)
    pdf_finish_cover = models.ImageField(blank=True, null=True, upload_to=get_file_path_for_pdf_cover)
    email = models.EmailField(max_length=160, blank=True, null=True)
    website = models.CharField(max_length=160, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    api_key = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name_plural = "001. Company"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.updated_date = timezone.now()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} NAME:{self.name}"

class UsagePackage(models.Model):
    pack_name = models.CharField(max_length=20)
    pack_name_en = models.CharField(max_length=20, blank=True, null=True)
    patient_limit = models.IntegerField()
    image_limit = models.IntegerField()
    analysis_limit = models.IntegerField()
    key = models.CharField(max_length=160, blank=True, null=True)
    price = models.FloatField(blank=True, null=True, default=0)
    global_price = models.FloatField(null=True, blank=True, default=0)
    is_yearly = models.BooleanField(default=False)

    def __str__(self):
        return f"PACK ID: {self.id} PACK NAME:{self.pack_name} PACK NAME ENG:{self.pack_name_en} PATIENT LIMIT:{self.patient_limit} IMAGE LIMIT: {self.image_limit} ANALYSIS LIMIT: {self.analysis_limit}"

# class Profile(models.Model):
#     user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
#     company = models.ForeignKey(Company, models.CASCADE, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     signature = models.ImageField(blank=True, null=True, upload_to=get_file_path_for_signature)
#     profile_photo = models.ImageField(blank=True, null=True, upload_to=get_file_path)
#     user_type = models.CharField(choices=USER_CHOICES, default="Customer", max_length=100, blank=False, null=True)
#     profession = models.CharField(max_length=120, blank=True, null=True)
#     archived = models.BooleanField(default=False)
#     created_date = models.DateTimeField(blank=True, null=True)
#     creator_username = models.CharField(max_length=120, blank=True, null=True)
#     is_staff = models.BooleanField(default=False, null=True, blank=True)
#     is_owner_of_company = models.BooleanField(default=False)
#     api_key = models.CharField(max_length=32, blank=True, null=True)

class Profile(models.Model):
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    clinic_name = models.CharField(max_length=100, blank=True, null=True)
    signature = models.ImageField(blank=True, null=True, upload_to=get_file_path_for_signature)
    profile_photo = models.ImageField(blank=True, null=True, upload_to=get_file_path)
    user_type = models.CharField(choices=USER_CHOICES, default="Customer", max_length=100, blank=False, null=True)
    profession = models.CharField(max_length=120, blank=True, null=True)
    archived = models.BooleanField(default=False)
    created_date = models.DateTimeField(blank=True, null=True)
    creator_username = models.CharField(max_length=120, blank=True, null=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    is_owner_of_company = models.BooleanField(default=False)
    is_distributor = models.BooleanField(default=False)
    added_by_distributor = models.ForeignKey("self", models.CASCADE, blank=True, null=True)
    api_key = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name_plural = "000. Profile"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - COMPANY NAME:{self.company.name if self.company else '-'} DOCTOR: {self.user_type} DOCTOR: {self.user.first_name} {self.user.last_name} "

class UsagePackageWithProfile(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    usage_pack = models.ForeignKey(UsagePackage, models.CASCADE,null=True,blank=True)
    trxCode = models.CharField(max_length=255, blank=True, null=True)
    trxCodeCranio = models.CharField(max_length=255, blank=True, null=True)
    result_message = models.CharField(max_length=255, blank=True, null=True)
    is_valid = models.BooleanField(default=True, null=True, blank=True)
    selling_price = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            # self.selling_price = self.usage_pack.price
        super(UsagePackageWithProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"Profileid: {self.id} PACK NAME:{self.profile} usage_pack:{self.usage_pack}"

class UserTheme(models.Model):
    LANGs = (('en', 'EN'), ('fr', 'FR'))
    VIEWTYPEs = (('0', 'LIST'), ('1', 'CARD'))
    COLORs = (('dark', 'DARK'), ('light', 'LIGHT'))
    LENGTHs = (('5', '5'), ('10', '10'), ('25', '25'), ('50', '50'), ('Hepsi', 'Hepsi'))
    user = models.ForeignKey(User, models.CASCADE)
    language = models.CharField(verbose_name='Dil', default="en", max_length=2, choices=LANGs)
    color = models.CharField(verbose_name='Renk',  default="dark", max_length=5, choices=COLORs)
    page_length = models.CharField(verbose_name='Hasta Listeleme Adedi', default='10', max_length=5, choices=LENGTHs)
    card_view_type = models.CharField(verbose_name='Hasta Görüntüleme Türü', default='0', max_length=5, choices=VIEWTYPEs)
    arabic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.pk} - {self.user.username}"

class UserFeedBack(models.Model):
    user = models.ForeignKey(Profile, models.CASCADE, verbose_name='Kullanıcı', blank=True, null=True)
    subject = models.TextField(verbose_name='Konu')
    message = models.TextField(verbose_name='Mesaj')

    def __str__(self):
        return f"{self.user.user.username} - {self.subject}"

class CreateUserToken(models.Model):
    token = models.CharField(max_length=255)

class UserForgotPasswordKey(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    key = models.CharField(max_length=6, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}--{self.date.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        self.date = datetime.now()
        super(UserForgotPasswordKey, self).save(*args, **kwargs)

class FormQuestion(models.Model):
    question = models.CharField(max_length=255)
    answers = models.TextField()

class Package(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    audience = models.IntegerField()
    monthly_price = models.CharField(max_length=32, blank=True, null=True)
    token = models.IntegerField()
    price_per_token = models.CharField(max_length=32, blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)
    is_yearly = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "01. Package"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(Package, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.audience} - {self.token} - {self.monthly_price} - {self.price_per_token}"
    
class ExtraPackage(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    token = models.IntegerField()
    price = models.CharField(max_length=32, blank=True, null=True)
    price_per_token = models.CharField(max_length=32, blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name_plural = "04. ExtraPackage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(ExtraPackage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.token} - {self.price} - {self.price_per_token}"
    
class BuyedPackage(models.Model): # Kullanıcının satın aldığı paketi kapsayan, hangi şirketin aldığını ve bu pakete bağlı doktorları tutan model (Ayrıca satın alan kişiye profilden is_owner_of_the_company özelliği verilir. Bu da şirket için doktor ekleyip silmeyi sağlar)
    slug = models.CharField(max_length=32, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    profiles = models.ManyToManyField(Profile, blank=True)

    class Meta:
        verbose_name_plural = "02. BuyedPackage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
            # self.start_date = timezone.now()
            # # end_date'i oluşturma tarihinden 1 yıl sonrasına ayarla
            # self.end_date = self.start_date + relativedelta(years=1)
        if not self.start_date:
            self.start_date = timezone.now()
        # next_renewal_date'yi renewal_date tarihinden 1 ay sonrasına ayarla
        if self.package.is_yearly == True:
            self.end_date = self.start_date + relativedelta(years=1)
        else:
            self.end_date = self.start_date + relativedelta(months=1)
        super(BuyedPackage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} PACK NAME:{self.package.name} usage_pack:{self.company.name} profiles: {len(self.profiles.all())}"

class BuyedExtraPackage(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    extra_package = models.ForeignKey(ExtraPackage, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "05. BuyedExtraPackage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")

            # self.start_date = timezone.now()
            # # end_date'i oluşturma tarihinden 2 yıl sonrasına ayarla
            # self.end_date = self.start_date + relativedelta(years=2)
        if not self.start_date:
            self.start_date = timezone.now()
        # next_renewal_date'yi renewal_date tarihinden 1 ay sonrasına ayarla
        self.end_date = self.start_date + relativedelta(years=2)
        super(BuyedExtraPackage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} PACK NAME:{self.company.name} usage_pack:{self.extra_package.name}"

class PackageRemainingUsage(models.Model): # Kullanıcı paket kullanımını aylık olarak takip edebilmek için kullanılacak model
    slug = models.CharField(max_length=32, blank=True, null=True)
    buyed_package = models.ForeignKey(BuyedPackage, on_delete=models.CASCADE)
    usage = models.IntegerField(default=0)
    total_usage = models.IntegerField(default=0)
    usage_limit = models.IntegerField(default=0)
    renewal_date = models.DateTimeField(blank=True, null=True)
    next_renewal_date = models.DateTimeField(blank=True, null=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "03. PackageRemainingUsage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        if not self.renewal_date:
            self.renewal_date = timezone.now()
        # next_renewal_date'yi renewal_date tarihinden 1 ay sonrasına ayarla
        self.next_renewal_date = self.renewal_date + relativedelta(months=1)
        
        super(PackageRemainingUsage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} PACK NAME:{self.buyed_package.package.name} usage:{self.usage} Renewal Date: {self.renewal_date} - Next Renewal Date: {self.next_renewal_date} {'EXPIRED' if self.is_expired == True else ''}"
    
class ExtraPackageRemainingUsage(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    buyed_extra_package = models.ForeignKey(BuyedExtraPackage, on_delete=models.CASCADE)
    usage = models.IntegerField(default=0)
    total_usage = models.IntegerField(default=0)
    renewal_date = models.DateTimeField(blank=True, null=True)
    next_renewal_date = models.DateTimeField(blank=True, null=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "06. ExtraPackageRemainingUsage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        if not self.renewal_date:
            self.renewal_date = timezone.now()
        # next_renewal_date'yi renewal_date tarihinden 1 ay sonrasına ayarla
        self.next_renewal_date = self.renewal_date + relativedelta(months=1)
        super(ExtraPackageRemainingUsage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} PACK NAME:{self.buyed_extra_package.extra_package.name} usage:{self.usage} Renewal Date: {self.renewal_date} - Next Renewal Date: {self.next_renewal_date} {'EXPIRED' if self.is_expired == True else ''}"

class PurchaseRecords(models.Model):
    pack_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(blank=True, null=True)
    price = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.purchase_date:
            self.purchase_date = timezone.now()
        super(PurchaseRecords, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.company_name} - {self.username} - {self.purchase_date} - {self.price}"
    
class PurchaseRecord(models.Model):
    payment_slug = models.CharField(max_length=50, blank=False, null=False)
    pack_name = models.CharField(max_length=50, blank=False, null=False)
    company_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=100, blank=False, null=False)
    price = models.CharField(max_length=50, blank=False, null=False)
    transaction_status = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(blank=True, null=True)
    transaction_details = models.TextField(blank=True, null=True)

    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Purchase Records"

    def __str__(self):
        return f"{self.id} - {self.company_name} - {self.username} - {self.transaction_date} - {self.price}"
    
class UserTokenActivity(models.Model):
    profile = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True)
    buyed_package_or_extra_slug = models.CharField(max_length=32, blank=True, null=True)
    used_token = models.IntegerField()
    image_type = models.CharField(choices=TokenActivityChoices, max_length=100, blank=False, null=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "11. UserTokenActivity"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        super(UserTokenActivity, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.id} Profile:{self.profile.user.username} usage:{self.used_token}"


class PackagePricing(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)
    monthly_price = models.CharField(max_length=32, blank=True, null=True)
    yearly_price = models.CharField(max_length=32, blank=True, null=True)
    price_per_token = models.CharField(max_length=32, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "12. PackagePricing"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(PackagePricing, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.currency} - {self.monthly_price} - {self.yearly_price} - {self.price_per_token} - {self.package.name}"

class ExtraPackagePricing(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)
    monthly_price = models.CharField(max_length=32, blank=True, null=True)
    yearly_price = models.CharField(max_length=32, blank=True, null=True)
    price_per_token = models.CharField(max_length=32, blank=True, null=True)
    extra_package = models.ForeignKey(ExtraPackage, on_delete=models.CASCADE)    
    class Meta:
        verbose_name_plural = "13. ExtraPackagePricing"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(ExtraPackagePricing, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.currency} - {self.monthly_price} - {self.yearly_price} - {self.price_per_token} - {self.extra_package.name}"


class ThakaaPackage(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    audience = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "51. ThakaaPackage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(ThakaaPackage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.audience}"

class ThakaaTokenBar(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    token = models.IntegerField()
    token_per_price = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        verbose_name_plural = "52. ThakaaTokenBar"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(ThakaaTokenBar, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.token} - {self.token_per_price} - {self.total_price}"

class ThakaaBuyedPackage(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    thakaa_package = models.ForeignKey(ThakaaPackage, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    profiles = models.ManyToManyField(Profile, blank=True)
    
    class Meta:
        verbose_name_plural = "53. ThakaaBuyedPackage"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(ThakaaBuyedPackage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - company: {self.company.name if self.company else None}"

class ThakaaBuyedToken(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    tokenbar = models.ForeignKey(ThakaaTokenBar, on_delete=models.CASCADE, blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "54. ThakaaBuyedToken"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")

        if not self.start_date:
            self.start_date = timezone.now()
            # next_renewal_date'yi renewal_date tarihinden 1 ay sonrasına ayarla
        self.end_date = self.start_date + relativedelta(years=2)
        super(ThakaaBuyedToken, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.tokenbar.token} - {self.start_date} - {self.end_date}"

class ThakaaRemainingToken(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    thakaa_buyed_token = models.ForeignKey(ThakaaBuyedToken, on_delete=models.CASCADE)
    usage = models.IntegerField(default=0)
    total_usage = models.IntegerField(default=0)
    renewal_date = models.DateTimeField(blank=True, null=True)
    next_renewal_date = models.DateTimeField(blank=True, null=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "55. ThakaaRemainingToken"

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        if not self.renewal_date:
            self.renewal_date = timezone.now()
        # next_renewal_date'yi renewal_date tarihinden 1 ay sonrasına ayarla
        self.next_renewal_date = self.renewal_date + relativedelta(months=1)
        super(ThakaaRemainingToken, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - Usage: {self.usage} - total/limit{self.total_usage} / {self.thakaa_buyed_token.tokenbar.token} - {'EXPIRED' if self.is_expired == True else ''}"

class ThakaaTokenActivity(models.Model):
    profile = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True)
    thakaa_remaining_token = models.ForeignKey(ThakaaRemainingToken, models.SET_NULL, blank=True, null=True)
    used_token = models.IntegerField()
    image_type = models.CharField(choices=TokenActivityChoices, max_length=100, blank=False, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "56. ThakaaTokenActivity"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        super(ThakaaTokenActivity, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.id} Profile:{self.profile.user.username} usage:{self.used_token}"

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
    
class TokenPayment(models.Model):
    slug = models.CharField(max_length=32, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=160, blank=True, null=True)
    phone = models.CharField(max_length=160, blank=True, null=True) 
    company_name = models.CharField(max_length=160, blank=True, null=True)
    total_price = models.CharField(max_length=100, blank=True, null=True)
    price_per_token = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    is_valid = models.BooleanField(default=False)
    OtherTrxCode = models.CharField(max_length=100, blank=True, null=True)
    code_for_hash = models.CharField(max_length=100, blank=True, null=True)
    request_payment_details = models.TextField(blank=True, null=True)
    redirect_payment_details = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    trxCode = models.CharField(max_length=100, blank=True, null=True)
    resultMessage = models.TextField(blank=True, null=True)
    payment_method = models.TextField(blank=True, null=True)
    # TARİH KAYITLARI TİMEZONE.NOW() İLE YAPILIYOR
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = str(uuid.uuid4()).replace("-", "")
        super(TokenPayment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - company: {self.company_name}"