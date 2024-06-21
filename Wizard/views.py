from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Application.models import ReportTooth, ImageReport, TreatmentMethod, ReportToothPredict, TreatmentRecommendationForTooth
from Application.cache_processes import active_model_labels_function,all_model_labels_function
from .models import *
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Application.views import get_specs
from Application.functions import user_theme_choices,error_handler_function,draw_function
from User.models import Company, Profile
import logging
import traceback
from django.core.exceptions import ObjectDoesNotExist
from itertools import islice
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.urls import reverse
from Server.settings import ccclinic_path_with_slash
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from reportlab.lib.pagesizes import letter

logger = logging.getLogger('main')

def fix_one_time(image_report_id):
    tooth_dict = {}
    treatment_dict = {}
    adult_teeth_list = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
    report = ImageReport.objects.get(id=image_report_id)
    for tooth in adult_teeth_list:
        report_tooth = ReportTooth.objects.filter(image_report=report,number_prediction=int(tooth)).first()
        predict_list = []
        for_treatment = []
        if report_tooth:
            if str(tooth).startswith(('1', '2','5','6')):
                jaw_area = "upper_jaw"
            elif str(tooth).startswith(('3', '4','7','8')):
                jaw_area = "lower_jaw"
            report_tooth_predict = ReportToothPredict.objects.filter(report_tooth=report_tooth)
            for predict in report_tooth_predict:
                prediction = json.loads(predict.prediction.replace("'", '"'))
                predict_list = []
                name = prediction["name"]
                probability = prediction["probability"]
                slug = prediction["slug"]
                for_treatment.append(name)
                illness_dict = {
                    "name":name,
                    "probability":probability,
                    "slug":slug
                }
                predict_list.append(illness_dict)
            tooth_dict[tooth] = {
                "is_missing":False,
                "jaw_area":jaw_area,
                "illnesses":predict_list,
            }
            treatment_recommendation = TreatmentRecommendationForTooth.objects.filter(tooth=report_tooth, image_report=report)
            print("treatment_recommendation",treatment_recommendation)  # Örneğin, recommendation objesini yazdır
            treatment_methods = []
            for recommendation_obj in treatment_recommendation:
                recommendations = recommendation_obj.recommendation.all()  # Tüm recommendation objelerini al
                for recommendation in recommendations:
                    # recommendation objesini kullan
                    print("recommendation",recommendation)  # Örneğin, recommendation objesini yazdır
            treatment_dict[tooth] = {
            "illnesses":for_treatment,
            }
        else:
            if str(tooth).startswith(('1', '2','5','6')):
                jaw_area = "upper_jaw"
            elif str(tooth).startswith(('3', '4','7','8')):
                jaw_area = "lower_jaw"
            tooth_dict[tooth] = {
                "is_missing":True,
                "jaw_area":jaw_area,
                "illnesses":predict_list
            }
    print("tooth_dict",tooth_dict)
    wizard_obj = TreatmentWizard.objects.create(
        image_report = report,
        diagnosis_data = json.dumps(tooth_dict),
        raw_treatment_data = {}
    )
    treatment_obj = TreatmentPlan.objects.create(
        treatment_wizard = wizard_obj,
        plan_treatment_data = {}
    )
    return wizard_obj





class DiagnosisNewPageView(LoginRequiredMixin,TemplateView):
    template_name = 'wizard/diagnosis_new.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            user = self.request.user
            self.id = kwargs.get('wizard_id')
            try:
                self.wizard_obj = TreatmentWizard.objects.get(image_report__id=self.id)
            except TreatmentWizard.DoesNotExist:
                self.wizard_obj = fix_one_time(self.id) #eski analizlerde de açılabilmesi için 1 kereliğine gerekli verileri dbde dolduran fonk
            self.data = json.loads(self.wizard_obj.diagnosis_data)
            kid_status = False
            if not kid_status:
                self.data = {key: value for key, value in self.data.items() if not str(key).startswith(('5', '6', '7', '8'))}
                # self.data = {key: value for key, value in self.data.items() if not any(illness.get('name') == 'Dental Pulp' for illness in value.get('illnesses', []))}
            print("self data",self.data)
            # function calls #
            self.data = self.get_teeth_svg_paths()
            self.labels = {}
            tags = self.get_tags()
            self.get_labels()
            self.get_diseases_svg_paths()
            self.get_in_order()
            # call ends #
            #pull first treatment plan obj#
            first_treatment_plan=TreatmentPlan.objects.filter(treatment_wizard=self.wizard_obj).first()
            first_treatment_plan_id = None
            if first_treatment_plan:
                first_treatment_plan_id = first_treatment_plan.id
            #pull first treatment plan obj#
            self.get_radiography() 
            context['data'] = self.sorted_dict
            context['data_for_svg'] = json.dumps(self.data)
            context['wizard_id'] = self.id
            context['plan_id'] = first_treatment_plan_id
            context['first_treatment_plan_id'] = first_treatment_plan_id
            context["tags"] = list(tags)
            # context["labels"] = self.labels
            context["radiography_image"] = self.radiography_image
            specs = get_specs()
            user_theme_dict = user_theme_choices(user)
            context["specs"]=specs
            context["user_theme_choices_json"]=json.dumps(user_theme_dict)
            context["user_theme_choices"]=json.dumps(user_theme_dict)
            context['is_diagnosis_wizard_page'] = True
            context['labels'] = self.labels_dict
            context['active_page'] = "diagnosis"
            context['specs'] = specs
            return context
        except Exception as e:
            traceback_str = traceback.format_exc()
            print("TRACEBACK",traceback_str)
            logger.error(f"Error occurred while rendering wizard diagnosis part: {traceback_str}")
            user = self.request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)


    def get_teeth_svg_paths(self):
        try:
            # Sözlükteki diş numaralarını al
            tooth_numbers = [key for key in self.data.keys()]

            # Diş numaralarına karşılık gelen SVG yollarını bul ve sözlüğe ekle
            for tooth_number in tooth_numbers:
                try:
                    # Diş numarasına karşılık gelen SVG yolu bulunuyor mu kontrol et
                    tooth_image = TeethImages.objects.get(teeth_number=tooth_number)
                    svg_path = tooth_image.path
                    self.data[tooth_number]['svg_path'] = svg_path.url
                except TeethImages.DoesNotExist:
                    # SVG yolu bulunamazsa hata mesajı ya da başka bir işlem yapabilirsiniz
                    traceback_str = traceback.format_exc()
                    print(f"TeethImages entry not found for tooth number: {tooth_number}")

            return self.data
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while trying to get svg path for wizard diagnonis page: {traceback_str}")

    def get_tags(self):
        if self.wizard_obj.general_tags:
            return json.loads(self.wizard_obj.general_tags)
        else:
            return []
    
    def get_labels(self):
        labels = LabelNamesForWizard.objects.all()
        self.labels_dict = {} 
        for label in labels:
            # if not label.sub_label_status or label.en_name=="Missing Tooth":
            group_name = label.group.group_name
            if group_name not in self.labels_dict:
                self.labels_dict[group_name] = {}
            label_info = {
                'slug': label.slug,
                'tr_name': label.tr_name,
                'fr_name': label.fr_name,
                'pt_name': label.pt_name,
                'ar_name': label.ar_name,
                'id':label.id,
                'sub_level_status':True if label.sub_label_status else False,
                'sub_of_this':label.sub_of_this.slug if label.sub_of_this else None,
            }
            self.labels_dict[group_name][label.en_name] = label_info
    def get_diseases_svg_paths(self):
        for key,value in self.data.items():
            if value["illnesses"]:
                for illness in value["illnesses"]:
                    if "name" in illness:
                        illness_name = illness["name"]
                    else:
                        illness_name = illness["en_name"]
                    for_svg = TeethImages.objects.filter(teeth_number=int(key)).first()
                    print("illness name",illness_name)
                    if for_svg:
                        svg_path_dict = json.loads(for_svg.svg_paths_dict)
                        if "root-canal filling" in illness_name.lower():
                            svg_path = svg_path_dict.get("Root Treated")
                        elif "caries" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Caries B")
                        elif "bone loss" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Bone Loss 2")
                        elif "furcation defect" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Furcation Lesion")
                        elif "filling" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Filling B")
                        elif "inlay" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Inlay")
                        elif "onlay" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Onlay")
                        elif "overlay" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Overlay")
                        elif "post" in illness_name.lower() or "post-fiber" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Post")
                        elif "parapulpal pin" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Parapulpal Pin")
                        elif "veneer" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Veneer")
                        elif "periapical lesion" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Pericapical Lesion")
                        elif "residual root" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Radix")
                        elif "impacted tooth" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Impacted")
                        elif "dental fracture" in illness_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Fractured")
                        else:
                            svg_path = svg_path_dict.get(illness_name)
                            print("svg path 22", svg_path)

                        print("svg path", svg_path)
                        illness["svg_path"] = svg_path if svg_path is not None else None    
                        
    def get_radiography(self):
        radiography_obj = ImageReport.objects.get(id=self.id)
        self.radiography_image = radiography_obj.image.path

    def get_in_order(self):
        adult_teeth_list = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
        self.sorted_dict = {}
        for tooth_number in adult_teeth_list:
            tooth_number_str = str(tooth_number)
            if tooth_number_str in self.data:
                self.sorted_dict[tooth_number_str] = self.data[tooth_number_str]
                #substatus adder#
                illnesses = self.sorted_dict[tooth_number_str]["illnesses"]
                for illness in illnesses:
                    if not illness['name'] == "Dental Pulp":
                        db_labels = LabelNamesForWizard.objects.filter(sub_of_this__en_name=illness['name'])
                        if db_labels:
                            illness["subs"] = {}
                            for db_label in db_labels:
                                illness["subs"][db_label.en_name] = {
                                    "en_name": db_label.en_name,
                                    "tr_name": db_label.tr_name,
                                    "pt_name": db_label.pt_name,
                                    "fr_name": db_label.fr_name,
                                    "ar_name": db_label.ar_name,
                                    "slug": db_label.slug,
                                }
                #substatus adder end#
        
class TreatmentPage(LoginRequiredMixin,TemplateView):
    template_name = 'wizard/treatments.html'
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            self.user = self.request.user
            self.id = kwargs.get('wizard_id')
            self.plan_id = kwargs.get('plan_id')
            self.plan_obj = TreatmentPlan.objects.get(id=self.plan_id)
            self.wizard_obj = TreatmentWizard.objects.get(image_report__id=self.id)
            specs = get_specs() 
            user_theme_dict = user_theme_choices(self.user)
            kid_status = False
            self.data = json.loads(self.wizard_obj.diagnosis_data)
            if not kid_status:
                self.data = {key: value for key, value in self.data.items() if not str(key).startswith(('5', '6', '7', '8'))}
            self.get_teeth_svg_paths()
            treatments,redirect_status = self.get_treatments()
            context['redirect_status'] = redirect_status
            self.treatment_methods_for_right_side()
            first_treatment_plan_id=TreatmentPlan.objects.filter(treatment_wizard=self.wizard_obj).first().id
            treatment_tabs = self.get_treatment_tabs()
            treatments = self.get_diseases_svg_paths(treatments)
            print("treatments",treatments)
            self.get_notes()
            self.get_treatment_types()
            self.get_discount()
            self.get_in_order()
            context['data'] = self.sorted_dict
            context['data_for_svg'] = json.dumps(self.data)
            context["specs"]=specs
            context["user_theme_choices_json"]=json.dumps(user_theme_dict)
            context["user_theme_choices"]=json.dumps(user_theme_dict)
            context["treatments"] = treatments
            context["treatments_for_js"] = json.dumps(treatments)
            context["treatment_svgs"] = json.dumps(treatments)
            context["treatments_from_db"] = self.treatments_dict
            context['wizard_id'] = self.id
            context['plan_id'] = self.plan_id
            context['is_treatment_wizard_page'] = True
            context['first_treatment_plan_id'] = first_treatment_plan_id
            context['treatment_tabs'] = treatment_tabs
            context['notes'] = self.notes
            context['general_note'] = self.general_note
            context['pricing_types'] = json.dumps(self.treatment_types)
            context['discount'] = self.discount
            context['active_page'] = "treatment"
            context['specs'] = specs
            # context['radiography'] = self.radiography_image
            return context
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while trying to get context data for wizard treatment page: {traceback_str}")
            user = self.request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)

    def get_teeth_svg_paths(self):
        try:
            # Sözlükteki diş numaralarını al
            tooth_numbers = [key for key in self.data.keys()]

            # Diş numaralarına karşılık gelen SVG yollarını bul ve sözlüğe ekle
            for tooth_number in tooth_numbers:
                try:
                    # Diş numarasına karşılık gelen SVG yolu bulunuyor mu kontrol et
                    tooth_image = TeethImages.objects.get(teeth_number=tooth_number)
                    svg_path = tooth_image.path
                    self.data[tooth_number]['svg_path'] = svg_path.url
                except TeethImages.DoesNotExist:
                    # SVG yolu bulunamazsa hata mesajı ya da başka bir işlem yapabilirsiniz
                    print(f"TeethImages entry not found for tooth number: {tooth_number}")
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while trying to get svg path for wizard diagnonis page: {traceback_str}")

    def get_diseases_svg_paths(self,treatments):
        for key,value in treatments.items():
            treatment_name = value["treatment_method"]
            teeths = value["teeth"]
            for tooth in teeths:
                for_svg = TeethImages.objects.filter(teeth_number=int(tooth["tooth_id"])).first()
                if for_svg:
                    svg_path_dict = json.loads(for_svg.svg_paths_dict)
                    if treatment_name == "Filling" or treatment_name == "Refilling": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                        svg_path = svg_path_dict.get("Filling B")
                    elif treatment_name == "Root Canal Treatment" or treatment_name == "Root Canal Retreatment": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                        svg_path = svg_path_dict.get("Root Treated")
                    else:
                        try:
                            svg_path = svg_path_dict.get(treatment_name)
                        except:
                            svg_path = None
                            print("svg path bulunamadı")

                    tooth["svg_path"] = svg_path if svg_path is not None else None   
        return treatments
    
    def get_treatments(self):
        redirect_status = False
        try:
            treatment_data = json.loads(self.plan_obj.plan_treatment_data)
        except ObjectDoesNotExist:
            new_treatment_obj = TreatmentPlan.objects.create(
                treatment_wizard = self.wizard_obj,
                plan_treatment_data = self.wizard_obj.raw_treatment_data,
                plan_queue = 1
            )
            treatment_data = json.loads(new_treatment_obj.plan_treatment_data)
            self.plan_id = new_treatment_obj.id
            redirect_status = True
            return treatment_data,redirect_status
        except (json.decoder.JSONDecodeError, TypeError):
            treatment_data = {}
            return treatment_data,redirect_status
        print("treatment data", treatment_data)
        result = {}
        for key, value in treatment_data.items():
            result[key] = {}
            treatment_list = []
            ## implantation surgery tedavi önerisi AI'dan bozuk geldiği için yama yapılan yer
            for treatment_method in value["treatment_methods"]:
                if treatment_method["slug"] == "6b3a9a9ea64c4c7eb3ed0c75ed39565a":
                    pass
                elif treatment_method["slug"] == "fee7e2fbc6d645e3ac0d3b4d00785e60":
                    print("IFFFFFFFFFFFF")
                    pass
                elif treatment_method["slug"] == "aec2d476662f44d2b05e5290a7ce1527":
                    print("IFFFFFFFFFFFF 414")
                    pass
                elif treatment_method["slug"] == "00an0tbse2zquofz6dwu5bc16vprmntd":
                    print("IFFFFFFFFFFFF 417")
                    pass
                    # print("treatment_method",treatment_method)
                    # treatment_method["treatment_method"]["id"]=treatment_method["id"]
                    # treatment_method["treatment_method"]["slug"]=treatment_method["slug"]
                    # treatment_method["treatment_method"]["treatment_method"]= "Implantation, surgery"
                    # treatment_dict = treatment_method["treatment_method"]
                    # treatment_list.append(treatment_dict)
                    # result[key]["treatment_methods"] = treatment_list
                else:
                    result[key] = {"treatment_methods": value["treatment_methods"]}
            ## implantation surgery tedavi önerisi AI'dan bozuk geldiği için yama yapılan yer
        print("results",result)
            
        # result = {key: {"treatment_methods": value["treatment_methods"]} for key, value in treatment_data.items()}
        # result = {key: {"treatment_methods": treatment_method["treatment_method"]["en_treatment_method"] if "6b3a9a9ea64c4c7eb3ed0c75ed39565a" ==  treatment_method["treatment_method"]["slug"] else treatment_method["treatment_method"] for treatment_method in value["treatment_methods"]} for key, value in treatment_data.items()}
        
        grouped_data = {}
        profile = Profile.objects.get(user=self.user)
        company = profile.company
        for key, value in result.items():
            price = 1000
            if "treatment_methods" in value:
                for method in value["treatment_methods"]:
                    method_key = method["slug"]
                    treatment_for_clinic = CompanyTreatmentPricing.objects.filter(company=company,treatment_method__slug = method_key).first()
                    if not treatment_for_clinic:
                        treatment_for_clinic = CompanyTreatmentPricing.objects.filter(company=company,treatment_method__ai_slug = method_key).first()
                    if treatment_for_clinic:
                        price = treatment_for_clinic.price
                    if method_key not in grouped_data:
                        grouped_data[method_key] = {"treatment_method": method["treatment_method"], "teeth": [], "unit_price":price,"total_price": 0}
                    # Her diş eklenmesiyle birlikte toplam fiyatı güncelle
                    grouped_data[method_key]["total_price"] += price
                    grouped_data[method_key]["amount"] = len(grouped_data[method_key]["teeth"]) + 1
                    grouped_data[method_key]["teeth"].append({"tooth_id": key})
        return grouped_data,redirect_status
    
    def treatment_methods_for_right_side(self):
        all_treatments = TreatmentNamesForWizard.objects.all()
        self.treatments_dict = {} 
        for treatment in all_treatments:
            group_name = treatment.group.group_name
            if group_name not in self.treatments_dict:
                self.treatments_dict[group_name] = {}
            treatment_info = {
                'slug': treatment.slug,
                'tr_name': treatment.tr_name,
                'fr_name': treatment.fr_name,
                'pt_name': treatment.pt_name,
                'ar_name': treatment.ar_name,
                'id':treatment.id,
            }
            self.treatments_dict[group_name][treatment.en_name] = treatment_info


    def get_treatment_tabs(self):
        plans = TreatmentPlan.objects.filter(treatment_wizard=self.wizard_obj).order_by("id")
        treatment_tab_dict = {}
        for plan in plans:
            treatment_tab_dict[plan.id] = {"plan_queue":plan.plan_queue}
        return treatment_tab_dict
    
    def get_notes(self):
        treatment_obj = self.plan_obj
        self.notes = {}
        if treatment_obj.notes:
            self.notes = json.loads(treatment_obj.notes)
        self.general_note = treatment_obj.general_note

    def get_treatment_types(self):
        self.treatment_types = {}
        if self.plan_obj.plan_pricing:
            self.treatment_types = json.loads(self.plan_obj.plan_pricing)
    
    def get_discount(self):
        self.discount = self.plan_obj.discount

    def get_in_order(self):
        adult_teeth_list = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
        self.sorted_dict = {}
        for tooth_number in adult_teeth_list:
            tooth_number_str = str(tooth_number)
            if tooth_number_str in self.data:
                self.sorted_dict[tooth_number_str] = self.data[tooth_number_str]
     
class DocumentPageView(LoginRequiredMixin,TemplateView):
    template_name = 'wizard/documents.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            self.user = self.request.user
            self.profile = Profile.objects.get(user=self.user)
            self.company = self.profile.company
            id = kwargs.get('wizard_id')
            self.plan_id = kwargs.get('plan_id')
            self.wizard_obj = TreatmentWizard.objects.get(image_report__id=id)
            first_treatment_plan_id=TreatmentPlan.objects.filter(treatment_wizard=self.wizard_obj).first().id
            self.contents = {}
            self.slug_list = []
            specs = get_specs()
            user_theme_dict = user_theme_choices(self.user)
            self.get_contents()
            print("self content",self.contents)
            self.get_saved_templates()
            context['wizard_id'] = id
            context['html_content'] = self.contents
            context['first_treatment_plan_id'] = first_treatment_plan_id
            context['plan_id'] = self.plan_id
            context["specs"]=specs
            context["slug_list"]=self.slug_list
            context["user_theme_choices_json"]=json.dumps(user_theme_dict)
            context["user_theme_choices"]=json.dumps(user_theme_dict)
            context['active_page'] = "document"
            context['specs'] = specs
            return context
        except Exception as e:
            traceback_str = traceback.format_exc()
            print("TRACEBACK",traceback_str)
            logger.error(f"Error occurred while rendering wizard diagnosis part: {traceback_str}")
            user = self.request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
        
    def get_contents(self):
        html_content = DocumentTemplates.objects.all().order_by("template_group_queue")
        for obj in html_content:
            is_saved_exists = ClinicModifiedTemplates.objects.filter(company=self.company,template=obj).first()
            slug = obj.slug
            content = obj.template_content
            image_path = "None"
            cover_option = "False"
            end_cover_option = "False"
            if is_saved_exists:
                content = is_saved_exists.modified_content
            if obj.containing_radiography:
                image_path = self.wizard_obj.image_report.image.path.url
            if obj.containing_cover_image:
                default = DefaultCoverImages.objects.filter().first()
                image_path = self.company.pdf_cover.url if self.company.pdf_cover else default.pdf_cover.url
                cover_option = "True"
            if obj.containing_end_cover_image:
                default = DefaultCoverImages.objects.filter().first()
                image_path = self.company.pdf_finish_cover.url if self.company.pdf_finish_cover else default.pdf_finish_cover.url
                end_cover_option = "True"
            template_name = obj.template_name
            group_name = obj.template_group_name
            content_dict = {
                "content": content,
                "template_name": template_name,
                "slug": slug,
                "image_path":image_path,
                "cover_option":cover_option,
                "end_cover_option":end_cover_option,
            }
            if group_name not in self.contents:
                self.contents[group_name] = []  # Eğer group_name yoksa, yeni bir liste oluştur
            self.contents[group_name].append(content_dict)  # Sonra sözlüğü bu listeye ekleyin
        treatments = TreatmentPlan.objects.filter(treatment_wizard = self.wizard_obj).order_by("id")
        # key_of_dict = _("Your Other Treatments Plans")
        treatment_plan_msg = _("Treatment Plan")
        # self.contents[key_of_dict] = [] 

        if treatments:
            counter = 1
            extras = ExtraTreatmentPlans.objects.filter(treatment_wizard = self.wizard_obj, treatment_plan__id = self.plan_id).first()
            self.extra_treatments = []
            if extras:
                self.extra_treatments = json.loads(extras.selected_treatments)
                print("extra treatments",self.extra_treatments,type(self.extra_treatments))
            for treatment in treatments:
                print("treatment id", treatment.id)
                print("treatment",treatment)
                selected = "false"
                if treatment.id == self.plan_id or str(treatment.id) in self.extra_treatments:
                    selected = "true"
                other_plan_dict = {
                    "template_name":treatment_plan_msg + " " + str(counter),
                    "plan_id":treatment.id,
                    "type":"plan",
                    "selected":selected,
                }
                # self.contents[key_of_dict].append(other_plan_dict) BURASI AÇILACAK
                counter += 1

    def get_saved_templates(self):
        saved_templates = ClinicSavedTemplatesForTreatment.objects.filter(treatment_plan__id = self.plan_id)
        for template_obj in saved_templates:
            templates = template_obj.templates.all()
            for template in templates:
                self.slug_list.append(template.slug)


class PdfReportCreate(LoginRequiredMixin,TemplateView):
    template_name = 'pdf_report.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        self.user = self.request.user
        self.profile = Profile.objects.get(user=self.user)
        self.company = self.profile.company
        self.contents = []
        self.plan_id = kwargs.get('plan_id')
        self.wizard_obj = TreatmentWizard.objects.get(image_report__id=kwargs.get('wizard_id'))
        templates_obj = ClinicSavedTemplatesForTreatment.objects.get(treatment_plan__id = self.plan_id)
        containing_radiography = False
        for template in templates_obj.templates.all():
            if template.containing_radiography:
                template_content = self.wizard_obj.image_report.image.path
                containing_radiography = True
            else:
                template_content = template.template_content
                containing_radiography = False
            template_dict = {
                "content":template_content,
                "containing_radiography":containing_radiography,
            }
            self.contents.append(template_dict)
        context["html_contents"] = self.contents 
        return context

def prep_diagnosis_sorted_dict(diagnosis_data,adult_teeth_list):
    diagnosis_sorted_dict = {}
    for tooth_number in adult_teeth_list:
        tooth_number_str = str(tooth_number)
        if tooth_number_str in diagnosis_data:
            diagnosis_sorted_dict[tooth_number_str] = diagnosis_data[tooth_number_str]
    for key,value in diagnosis_sorted_dict.items():
        tooth_svg = TeethImages.objects.get(teeth_number=int(key))
        value["tooth_svg"] = tooth_svg.path.url
        svg_path_dict = json.loads(tooth_svg.svg_paths_dict)
        value["illnesses"] = [illness for illness in value["illnesses"] if illness["name"] != "Dental Pulp"]
        for illness_name in value["illnesses"]:
            if illness_name["name"] == "Filling" or illness_name["name"] == "Overhanging Filling": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                svg_path = svg_path_dict.get("Filling B")
            elif illness_name["name"] == "Caries": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                svg_path = svg_path_dict.get("Caries B")
            elif illness_name["name"] == "Horizontal Bone Loss": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                svg_path = svg_path_dict.get("Bone Loss 1")
            elif illness_name["name"] == "Furcation Defect": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                svg_path = svg_path_dict.get("Furcation Lesion")
            else:
                svg_path = svg_path_dict.get(illness_name["name"])
            illness_name["illness_svg_path"] = svg_path
    return diagnosis_sorted_dict
        
def prep_treatment_sorted_dict(treatment_data,adult_teeth_list):
    treatment_sorted_dict = {}
    for tooth_number in adult_teeth_list:
        tooth_number_str = str(tooth_number)
        if tooth_number_str in treatment_data:
            treatment_sorted_dict[tooth_number_str] = treatment_data[tooth_number_str]
    # for key,value in treatment_sorted_dict.items():
    #     tooth_svg = TeethImages.objects.get(teeth_number=int(key))
    #     value["tooth_svg"] = tooth_svg.path
    #     svg_path_dict = json.loads(tooth_svg.svg_paths_dict)
    #     for treatment_name in value["treatment_methods"]:
    #         if treatment_name["treatment_method"] == "Filling" or treatment_name["treatment_method"] == "Overhanging Filling": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
    #             svg_path = svg_path_dict.get("Filling B")
    #         elif treatment_name["treatment_method"] == "Caries": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
    #             svg_path = svg_path_dict.get("Caries B")
    #         elif treatment_name["treatment_method"] == "Horizontal Bone Loss": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
    #             svg_path = svg_path_dict.get("Bone Loss 1")
    #         elif treatment_name["treatment_method"] == "Furcation Defect": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
    #             svg_path = svg_path_dict.get("Furcation Lesion")
    #         else:
    #             try:
    #                 svg_path = svg_path_dict.get(treatment_name["treatment_method"])
    #             except:
    #                 svg_path = None
    #         treatment_name["illness_svg_path"] = svg_path
    return treatment_sorted_dict

def prep_treatment_grouped_data(treatment_sorted_dict,user,treatment_plan_obj):
    # IMPLANTIN BOZUK GELMESİNDEN SONRA KAPATILAN DAHA SONRA ACILACAK OLAN KOD result = {key: {"treatment_methods": value["treatment_methods"]} for key, value in treatment_sorted_dict.items()}
    result = {}
    for key, value in treatment_sorted_dict.items():
        result[key] = {}
        treatment_list = []
        ## implantation surgery tedavi önerisi AI'dan bozuk geldiği için yama yapılan yer
        for treatment_method in value["treatment_methods"]:
            if treatment_method["slug"] == "6b3a9a9ea64c4c7eb3ed0c75ed39565a":
                print("treatment_method",treatment_method)
                treatment_method["treatment_method"]["id"]=treatment_method["id"]
                treatment_method["treatment_method"]["slug"]=treatment_method["slug"]
                treatment_method["treatment_method"]["treatment_method"]= "Implantation, surgery"
                treatment_dict = treatment_method["treatment_method"]
                treatment_list.append(treatment_dict)
                result[key]["treatment_methods"] = treatment_list
            else:
                result[key] = {"treatment_methods": value["treatment_methods"]}
    grouped_data = {}
    profile = Profile.objects.get(user=user)
    company = profile.company
    total_price = 0
    for key, value in result.items():
        price = 1000
        if "treatment_methods" in value:
            for method in value["treatment_methods"]:
                method_key = method["slug"]
                treatment_for_clinic = CompanyTreatmentPricing.objects.filter(company=company,treatment_method__slug = method_key).first()
                if treatment_for_clinic:
                    price = treatment_for_clinic.price
                if method_key not in grouped_data:
                    grouped_data[method_key] = {"treatment_method": method["treatment_method"], "teeth": [], "unit_price":price,"total_price": 0}
                # Her diş eklenmesiyle birlikte toplam fiyatı güncelle
                treatment_method_for_type = None
                if treatment_plan_obj.plan_pricing:
                    pricing_types = json.loads(treatment_plan_obj.plan_pricing)
                    treatment_method_for_type = pricing_types.get(method_key)
                if treatment_method_for_type:
                    if treatment_method_for_type["type"] == "free" or treatment_method_for_type["type"] == "inpackage":
                        grouped_data[method_key]["total_price"] = 0
                        grouped_data[method_key]["unit_price"] = "Free" if treatment_method_for_type["type"] == "free" else "In Package"
                        grouped_data[method_key]["amount"] = len(grouped_data[method_key]["teeth"]) + 1
                        grouped_data[method_key]["teeth"].append({"tooth_id": key})
                    elif treatment_method_for_type["type"] == "package":
                        grouped_data[method_key]["total_price"] = price
                        grouped_data[method_key]["amount"] = 1
                        grouped_data[method_key]["teeth"].append({"tooth_id": key})
                else:
                    grouped_data[method_key]["total_price"] += price
                    grouped_data[method_key]["amount"] = len(grouped_data[method_key]["teeth"]) + 1
                    grouped_data[method_key]["teeth"].append({"tooth_id": key})
                total_price += price
    treatment_sorted_dict["total_price"] = total_price
    return grouped_data

def pdf_report_create(request,wizard_id,plan_id):
    try:
        template_path = 'pdf_report.html'
        user = request.user
        profile = Profile.objects.get(user=user)
        company = profile.company
        contents = []
        treatment_plan_obj = TreatmentPlan.objects.get(id=plan_id)
        wizard_obj = TreatmentWizard.objects.get(image_report__id=wizard_id)
        templates_obj = ClinicSavedTemplatesForTreatment.objects.filter(treatment_plan__id = plan_id).first()
        old_pdf_file_path = treatment_plan_obj.pdf_file
        if not templates_obj:
            cover_image = DocumentTemplates.objects.get(template_name="Cover Image")
            patient_radiography = DocumentTemplates.objects.get(template_name="Patient Radiography")
            clinic_saved_template = ClinicSavedTemplatesForTreatment.objects.create(treatment_plan=treatment_plan_obj)
            clinic_saved_template.templates.add(cover_image)
            clinic_saved_template.templates.add(patient_radiography)
            templates_obj = ClinicSavedTemplatesForTreatment.objects.filter(treatment_plan__id = plan_id).first()
        ###
        # Patient Radiography
        # Cover Image
        ###
        containing_radiography = False
        for template in templates_obj.templates.all().order_by("template_group_queue"):
            is_modified = ClinicModifiedTemplates.objects.filter(template=template).first()
            if template.containing_radiography:
                template_content = wizard_obj.image_report.image
                print("template content", template_content, type(template_content))
                containing_radiography = True
            else:
                if is_modified:
                    template_content = is_modified.modified_content
                else:
                    template_content = template.template_content
                containing_radiography = False
            template_dict = {
                "content":template_content,
                "containing_radiography":containing_radiography,
            }
            contents.append(template_dict)
        ###
        diagnosis_data = json.loads(wizard_obj.diagnosis_data)
        treatment_data = json.loads(TreatmentPlan.objects.get(id=plan_id).plan_treatment_data)
        adult_teeth_list = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
        
        diagnosis_sorted_dict = prep_diagnosis_sorted_dict(diagnosis_data,adult_teeth_list)
        treatment_sorted_dict = prep_treatment_sorted_dict(treatment_data,adult_teeth_list)
        treatment_grouped_data = prep_treatment_grouped_data(treatment_sorted_dict,user,treatment_plan_obj)
        grouped_treatments = json.dumps(treatment_grouped_data)
        total_price = 0
        for key,value in treatment_grouped_data.items():
            print("value",value)
            price = value["total_price"]
            total_price += price
        extra_treatment_plans = ExtraTreatmentPlans.objects.filter(treatment_wizard = wizard_obj, treatment_plan = treatment_plan_obj).exclude(treatment_plan__id=plan_id).first()
        extra_treatments = []
        if extra_treatment_plans:
            selected_treatments = json.loads(extra_treatment_plans.selected_treatments)
            for extra_treatment in selected_treatments:
                extra_treatment_obj = TreatmentPlan.objects.get(id=extra_treatment)
                extra_treatment_data = json.loads(extra_treatment_obj.plan_treatment_data)
                extra_treatment_sorted_dict = prep_treatment_sorted_dict(extra_treatment_data,adult_teeth_list)
                extra_treatment_grouped_data = prep_treatment_grouped_data(extra_treatment_sorted_dict,user,extra_treatment_obj)
                extra_treatment_sorted_dict["grouped_treatments"] = extra_treatment_grouped_data
                extra_treatments.append(extra_treatment_sorted_dict)
        treatment_sorted_dict["grouped_treatments"] = treatment_grouped_data
        default_cover_image = DefaultCoverImages.objects.filter().first()
        cover_image = company.pdf_cover if company.pdf_cover else default_cover_image.pdf_cover
        pdf_finish_cover = company.pdf_finish_cover if company.pdf_finish_cover else "" 
        patient_name = wizard_obj.image_report.image.patient.full_name if wizard_obj.image_report.image.patient.full_name else wizard_obj.image_report.image.patient.first_name + " " + wizard_obj.image_report.image.patient.last_name
        doctor_name = wizard_obj.image_report.user.user.first_name + " " + wizard_obj.image_report.user.user.first_name
        created_date_time_format = "%d/%m/%Y %H:%M"
        if treatment_plan_obj.pdf_created_date:
            pdf_create_date = treatment_plan_obj.pdf_created_date.strftime(created_date_time_format)
        else: 
            pdf_create_date = datetime.now().strftime(created_date_time_format)
        path = wizard_obj.image_report.image.path
        image_report_obj = wizard_obj.image_report
        output_path = draw_function(path=path, image_report_id=wizard_obj.image_report.id, )
        output_path = output_path.replace(ccclinic_path_with_slash, "") if os.path.exists(output_path) else None
        treatment_plan_obj.drawed_radiography_path = output_path
        labels_colors_on_radiography = None
        if "Lateral Cephalometric" not in image_report_obj.name:
            def prepare_labels_colors_on_radiography():
                illness_appended_list = []
                result_json = json.loads(image_report_obj.result_json)
                cache_active_models = active_model_labels_function()
                patient_type = "Kid" if "kid" in image_report_obj.ai_response_image_type.lower() else "Adult"
                labels = cache_active_models[image_report_obj.name][patient_type]
                for illness_and_palate, illness_list in result_json.items():
                    for illness in illness_list:
                        label_illness = labels.get(illness["name"])
                        if label_illness:
                            label_illness["name"] = illness["name"]
                            illness_appended_list.append(label_illness)
                unique_data = []
                for d in illness_appended_list:
                    if "main_label" not in d.keys(): continue
                    del d["main_label"]
                unique_data = list(set(tuple(sorted(d.items())) for d in illness_appended_list))
                unique_data = [dict(t) for t in unique_data]
                return unique_data
            labels_colors_on_radiography = prepare_labels_colors_on_radiography()
        context = {'total_price':total_price,'labels_colors_on_radiography':labels_colors_on_radiography,'output_path':output_path,'pdf_finish_cover':pdf_finish_cover,'pdf_create_date':pdf_create_date,'doctor_name':doctor_name,'patient_name':patient_name,'html_contents':contents, 'diagnosis_datas_for_svg':json.dumps(diagnosis_sorted_dict),'diagnosis_datas':diagnosis_sorted_dict, 'treatment_datas':treatment_sorted_dict, 'extra_treatments':extra_treatments,'cover_image':cover_image,"grouped_treatments":json.loads(grouped_treatments)} 
        response = HttpResponse(content_type="application/pdf")
        filename = str(uuid.uuid4()) + ".pdf"
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        template = get_template(template_path)
        html = template.render(context)
        # print("html",html)
        pdf_file_path = os.path.join("/home/ubuntu/Clinic/media/pdf_reports",filename)  # Örneğin 'media/pdf_reports' klasörüne kaydediyoruz
        with open(pdf_file_path, 'wb') as pdf_file:
            pisa.CreatePDF(html, dest=pdf_file,pagesize=letter)
        pdf_url = os.path.join(settings.MEDIA_URL, 'pdf_reports', filename)  # MEDIA_URL'inizi buraya ekleyin
        treatment_plan_obj.pdf_file = "/media"+pdf_url
        treatment_plan_obj.pdf_created_date = datetime.now()
        # Dosyanın varlığını kontrol et
        if old_pdf_file_path:
            if os.path.exists("/home/ubuntu/Clinic"+old_pdf_file_path):
                # Dosyayı sil
                os.remove("/home/ubuntu/Clinic"+old_pdf_file_path)
                print(f"{old_pdf_file_path} dosyası başarıyla silindi.")
            else:
                print(f"{old_pdf_file_path} dosyası zaten mevcut değil.")
        treatment_plan_obj.save()
        return render(request,'pdf_report.html',context)
        # return HttpResponse("/media"+pdf_url)
    except Exception as e:
        traceback_str = traceback.format_exc()
        print("TRACEBACK",traceback_str)
        logger.error(f"Error occurred while creating pdf: {traceback_str}")
        user = request.user
        error = traceback.format_exc()
        error_handler_function(user,error)

class OverviewPage(LoginRequiredMixin,TemplateView):
    template_name = 'wizard/overview.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            self.user = self.request.user
            self.profile = Profile.objects.get(user=self.user)
            self.company = self.profile.company
            id = kwargs.get('wizard_id')
            self.plan_id = kwargs.get('plan_id')
            self.treatment_plan_obj = TreatmentPlan.objects.get(id=self.plan_id)
            self.wizard_obj = TreatmentWizard.objects.get(image_report__id=id)
            first_treatment_plan_id=TreatmentPlan.objects.filter(treatment_wizard=self.wizard_obj).first().id
            specs = get_specs()
            self.template_contents = []
            self.fill_content_list()
            self.get_cover_image()
            self.prep_treatments()
            self.calculate_total_price()
            user_theme_dict = user_theme_choices(self.user)
            self.get_end_cover_image()
            context['wizard_id'] = id
            context['first_treatment_plan_id'] = first_treatment_plan_id
            context['plan_id'] = self.plan_id
            context["specs"]=specs
            context["user_theme_choices_json"]=json.dumps(user_theme_dict)
            context["user_theme_choices"]=json.dumps(user_theme_dict)
            context["template_contents"]=json.dumps(self.template_contents)
            context['active_page'] = "overview"
            context['cover_image'] = self.cover_image
            context['specs'] = specs
            context['diagnosis_datas'] = self.diagnosis_sorted_dict
            context['treatment_datas'] = self.treatment_sorted_dict,
            context['grouped_treatments'] = json.loads(self.grouped_treatments)
            context['total_price'] = self.total_price
            context['end_cover_image'] = self.end_cover_image
            
            return context
        except Exception as e:
            traceback_str = traceback.format_exc()
            print("TRACEBACK",traceback_str)
            logger.error(f"Error occurred while rendering wizard overview part: {traceback_str}")
            user = self.request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
    def prep_treatments(self):
        adult_teeth_list = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43,
                                42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
        self.diagnosis_data = json.loads(self.wizard_obj.diagnosis_data)
        self.treatment_data = json.loads(TreatmentPlan.objects.get(id=self.plan_id).plan_treatment_data)
        self.diagnosis_sorted_dict = prep_diagnosis_sorted_dict(self.diagnosis_data,adult_teeth_list)
        self.treatment_sorted_dict = prep_treatment_sorted_dict(self.treatment_data,adult_teeth_list)
        self.treatment_grouped_data = prep_treatment_grouped_data(self.treatment_sorted_dict,self.user,self.treatment_plan_obj)
        self.grouped_treatments = json.dumps(self.treatment_grouped_data)

    def calculate_total_price(self):
        self.total_price = 0
        for key,value in self.treatment_grouped_data.items():
            print("value",value)
            price = value["total_price"]
            self.total_price += price
    def get_cover_image(self):
        self.cover_image = self.company.pdf_cover
        if not self.cover_image:
            self.cover_image = DefaultCoverImages.objects.filter().first().pdf_cover.url
        else:
            self.cover_image = self.company.pdf_cover.url
    def fill_content_list(self):
        containing_radiography = False
        templates_obj = ClinicSavedTemplatesForTreatment.objects.get(treatment_plan__id = self.plan_id)
        for template in templates_obj.templates.all():
            is_modified = ClinicModifiedTemplates.objects.filter(template=template).first()
            if template.containing_radiography:
                template_content = self.wizard_obj.image_report.image.path.url
                containing_radiography = True
            else:
                if is_modified:
                    template_content = is_modified.modified_content
                else:
                    template_content = template.template_content
                containing_radiography = False
            template_dict = {
                "content":template_content,
                "containing_radiography":containing_radiography,
            }
            self.template_contents.append(template_dict)
    def get_end_cover_image(self):
        self.end_cover_image = self.company.pdf_finish_cover
        if not self.end_cover_image:
            self.end_cover_image = DefaultCoverImages.objects.filter().first().pdf_finish_cover.url
        else:
            self.end_cover_image = self.company.pdf_finish_cover.url
