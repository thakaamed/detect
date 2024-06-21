from django.contrib import admin
from Wizard.models import *
from django.apps import apps
app = apps.get_app_config('Wizard')

for model_name, model in app.models.items():
    admin.site.register(model)
