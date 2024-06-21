from django.urls import path, include
from Wizard.views import *

urlpatterns = [
    path('treatment-wizard/diagnosis/<int:wizard_id>', DiagnosisNewPageView.as_view(), name='diagnosisNewPage'),
    path('treatment-wizard/treatments/<int:wizard_id>/<int:plan_id>', TreatmentPage.as_view(), name='TreatmentPage'),
    path('treatment-wizard/document/<int:wizard_id>/<int:plan_id>', DocumentPageView.as_view(), name='DocumentPage'),
    path('treatment-wizard/pdf-report/<int:wizard_id>/<int:plan_id>', pdf_report_create, name='pdfreport'),
    path('treatment-wizard/overview/<int:wizard_id>/<int:plan_id>', OverviewPage.as_view(), name='overview'),
]


