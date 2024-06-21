from Wizard.api.views import *
from django.urls import path

urlpatterns = [
    # path("delete-patient-api", delete_patient_api, name="deletepatientApi"),
    path('register-tag', RegisterTag.as_view(), name = "register-tag"),
    path('delete-tag', DeleteTag.as_view(), name = "delete-tag"),
    path('add-manual-illness', AddManualIllnessToTooth.as_view(), name = "add-manual-illness"),
    path('delete-manual-illness', DeleteManualIllnessFromTooth.as_view(), name = "delete-manual-illness"),
    path('wizard-delete-treatment-from-tooth', DeleteTreatmentFromTooth.as_view(), name = "wizard-delete-treatment-from-tooth"),
    path('add-treatment-to-teeth', AddTreatmentToTeeth.as_view(), name = "add-treatment-to-teeth"),
    path('add-illness', AddIllnessToTeeth.as_view(), name = "add-illness-to-teeth"),
    path('delete-all-illnesses-from-tooth', DeleteAllIllnessesFromTooth.as_view(), name = "delete-all-illness-from-tooth"),
    path('create-new-treatment-plan', CreateNewTreatmentPlan.as_view(), name = "create-new-treatment-plan"),
    path('delete-treatment-plan', DeleteTreatmentPlan.as_view(), name = "delete-treatment-plan"),
    path('update-treatment-price', UpdateTreatmentPrice.as_view(), name = "update-treatment-price"),
    path('add-note-to-treatment', AddNoteToTreatment.as_view(), name = "add-note-to-treatment"),
    path('add-general-note', AddGeneralNote.as_view(), name = "add-general-note"),
    path('delete-specific-treatment', DeleteSpecificTreatment.as_view(), name = "delete-specific-treatment"),
    path('reset-treatment', ResetTreatment.as_view(), name = "reset-treatment"),
    path('change-pricing-type', ChangePricingType.as_view(), name = "change-pricing-type"),
    path('apply-discount', ApplyDiscount.as_view(), name = "apply-discount"),
    path('save-templates-for-treatment-plan', SaveDocumentsForTreatmentPlan.as_view(), name = "save-templates-for-treatment-plan"),
    path('modify-default-templates', SaveEditedDocumentsForCompany.as_view(), name = "modify-default-templates"),
    path('get-pdf-content', GetPdfContent.as_view(), name = "get-pdf-content"),
    path('download-pdf', DownloadPDF.as_view(), name = "download-pdf"),
    path('edit-tag', EditTag.as_view(), name = "edit-tag"),
    path('replace-diagnosis', ReplaceDiagnosis.as_view(), name = "replace-diagnosis"),
    path('save-extra-treatment', SaveExtraTreatment.as_view(), name = "save-extra-treatment"),
    path('save_cover_image', save_cover_image, name='save_cover_image'),
    path('save_end_cover_image', save_end_cover_image, name='save_end_cover_image'),


]