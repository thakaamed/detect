from django.contrib import admin
from User.models import *


# Register your models here.
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(UserTheme)
admin.site.register(UsagePackage)
admin.site.register(UserFeedBack)
admin.site.register(UsagePackageWithProfile)
admin.site.register(CreateUserToken)
admin.site.register(UserForgotPasswordKey)

admin.site.register(Package)
admin.site.register(ExtraPackage)
admin.site.register(BuyedPackage)
admin.site.register(BuyedExtraPackage)
admin.site.register(PackageRemainingUsage)
admin.site.register(ExtraPackageRemainingUsage)
admin.site.register(PurchaseRecords)
admin.site.register(UserTokenActivity)
admin.site.register(ThakaaPackage)
admin.site.register(ThakaaTokenBar)
admin.site.register(ThakaaBuyedPackage)
admin.site.register(ThakaaBuyedToken)
admin.site.register(ThakaaRemainingToken)
admin.site.register(ThakaaTokenActivity)
admin.site.register(Currency)


