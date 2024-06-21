import traceback
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.core.cache import cache
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import uuid
import os
from django.shortcuts import render
from User.mail import send_feedback_email
from rest_framework.views import APIView
from rest_framework.response import Response
from Application.cache_processes import active_model_labels_function,fetch_data_from_AI_labels
from Application.functions import error_handler_function
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from Wizard.models import *
from User.models import Profile
import json 
from django.http import HttpResponseRedirect, JsonResponse
import traceback
from reportlab.pdfgen import canvas
from io import BytesIO
import io
from bs4 import BeautifulSoup
logger = logging.getLogger('main')


class RegisterTag(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            tag_value = request.POST.get('tag_value')
            image_report_id = request.POST.get('image_report_id')
            wizard_obj = TreatmentWizard.objects.get(image_report__id=image_report_id)
            existing_general_tags = wizard_obj.general_tags
            key = str(uuid.uuid4()).replace("-","")[0:10]
            tag_dict = {
                "tag_value":tag_value,
                "slug":key
            }
            if not existing_general_tags:
                existing_general_tags = []
                tag_dict = {
                    "tag_value":tag_value,
                    "slug":key
                }
                existing_general_tags.append(tag_dict)
            else:
                existing_general_tags = json.loads(existing_general_tags)
                existing_general_tags.append(tag_dict)
            wizard_obj.general_tags = json.dumps(existing_general_tags)
            wizard_obj.save()
            return JsonResponse({'success':True, 'slug':key})
        except Exception as e:
            logger.error(f"Error occurred while trying to add tag: {e}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class DeleteTag(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            tag_id = request.POST.get('tag_id')
            image_report_id = request.POST.get('image_report_id')
            wizard_obj = TreatmentWizard.objects.get(image_report__id=image_report_id)
            existing_general_tags = json.loads(wizard_obj.general_tags)
            matching_dict = next((item for item in existing_general_tags if item.get("slug") == tag_id), None)
            if matching_dict:
                existing_general_tags.remove(matching_dict)
                wizard_obj.general_tags = json.dumps(existing_general_tags)
                wizard_obj.save()
            return JsonResponse({'success':True})
        except Exception as e:
            logger.error(f"Error occurred while deleting tag: {e}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class AddManualIllnessToTooth(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            tooth_number = request.POST.get("tooth_number")
            image_report_id = request.POST.get("image_report_id")
            illness_value = request.POST.get("value")
            wizard_obj = TreatmentWizard.objects.get(image_report__id=image_report_id)
            diagnosis_data = json.loads(wizard_obj.diagnosis_data)
            tooth_to_add_illness = diagnosis_data[tooth_number]["illnesses"]
            key = str(uuid.uuid4()).replace("-","")
            manual_illness_dict = {
                'name':illness_value,
                'probability':101,
                'slug':key
            }
            tooth_to_add_illness.append(manual_illness_dict)
            wizard_obj.diagnosis_data = json.dumps(diagnosis_data) #diagnosis data içerisinde değişiklik yapıldığı için diagnosis data tekrar kayıt ediliyor
            wizard_obj.save()
            return JsonResponse({'success':True, "slug":key})
        except Exception as e:
            logger.error(f"Error occurred while adding manual illness: {e}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class DeleteManualIllnessFromTooth(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            tooth_number = request.POST.get("tooth_number")
            image_report_id = request.POST.get("image_report_id")
            illness_slug = request.POST.get("illness_slug")
            wizard_obj = TreatmentWizard.objects.get(image_report__id=image_report_id)
            diagnosis_data = json.loads(wizard_obj.diagnosis_data)
            remove_illness_from_tooth = diagnosis_data[tooth_number]["illnesses"]
            tooth_svg_path = None
            # İlk eşleşen öğeyi sil
            for item in remove_illness_from_tooth:
                print("item",item)
                if item['slug'] == illness_slug:
                    if item['name'] == "Missing":
                        diagnosis_data[tooth_number]["is_missing"] = False
                        tooth_svg_path = TeethImages.objects.get(teeth_number = int(tooth_number)).path.url
                    remove_illness_from_tooth.remove(item)
                    break
            wizard_obj.diagnosis_data = json.dumps(diagnosis_data) #diagnosis data içerisinde değişiklik yapıldığı için diagnosis data tekrar kayıt ediliyor
            wizard_obj.save()
            return JsonResponse({'success':True, 'tooth_svg_path':tooth_svg_path})
        except Exception as e:
            logger.error(f"Error occurred while adding manual illness: {e}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class DeleteTreatmentFromTooth(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            company = profile.company
            treatment_slug = request.POST.get("treatment_slug")
            treatment_method_obj = CompanyTreatmentPricing.objects.filter(company=company, treatment_method__slug=treatment_slug).first()
            price = 1000
            currency = "tl"
            if treatment_method_obj:
                price = treatment_method_obj.price
                currency = treatment_method_obj.currency
            tooth_id = request.POST.get("tooth_id")
            plan_id = request.POST.get("plan_id")
            plan_obj = TreatmentPlan.objects.get(id=plan_id)
            treatment_data = json.loads(plan_obj.plan_treatment_data)
            target_tooth = treatment_data[tooth_id]["treatment_methods"]
            new_target_tooth = [item for item in target_tooth if item['slug'] != treatment_slug]
            target_tooth = new_target_tooth
            treatment_data[tooth_id]["treatment_methods"] = new_target_tooth
            plan_obj.plan_treatment_data = json.dumps(treatment_data) #diagnosis data içerisinde değişiklik yapıldığı için diagnosis data tekrar kayıt ediliyor
            plan_obj.save()
            return JsonResponse({'success':True, 'price':price, 'currency':currency})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            logger.error(f"Error occurred while deleting treatment from teeth: {traceback_str}")
            return JsonResponse({'success':False})

class AddTreatmentToTeeth(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            treatment_slug = request.POST.get("treatment_slug")
            print("treatment slug", treatment_slug)
            teeth = request.POST.getlist("activeToothNumbersList[]",None)
            if teeth:
                teeth = list(set(teeth))
            print("TEETH",teeth)
            plan_id = request.POST.get("plan_id")
            plan_obj = TreatmentPlan.objects.get(id=plan_id)
            print("data",plan_obj.plan_treatment_data,type(plan_obj.plan_treatment_data))
            if plan_obj.plan_treatment_data:
                treatment_data = json.loads(plan_obj.plan_treatment_data)
            else:
                treatment_data = {}
            treatment_obj = TreatmentNamesForWizard.objects.get(slug=treatment_slug)
            user = request.user
            profile = Profile.objects.get(user=user)
            company = profile.company
            price_for_treatment = CompanyTreatmentPricing.objects.filter(company=company, treatment_method=treatment_obj).first()
            is_treatment_price_exist = False
            default_price = 1000
            loop_price = 0
            svg_paths = {}
            unit_price = default_price
            currency = None
            if price_for_treatment:
                is_treatment_price_exist = True
                price = price_for_treatment.price
                unit_price = price_for_treatment.price
                currency = price_for_treatment.currency
            for tooth in teeth:
                if is_treatment_price_exist:
                    loop_price += price
                else:
                    loop_price += default_price
                added_treatment_dict = {
                    "treatment_method":treatment_obj.en_name,
                    "slug":treatment_obj.slug,
                }
                if tooth in treatment_data:
                    treatment_data[tooth]["treatment_methods"].append(added_treatment_dict)
                else:
                    treatment_data[tooth] = {}
                    treatment_data[tooth]["illnesses"] = []
                    treatment_data[tooth]["treatment_methods"] = []
                    treatment_data[tooth]["treatment_methods"].append(added_treatment_dict)
                #start getting svg path if exists#
                tooth_obj = TeethImages.objects.filter(teeth_number = int(tooth)).first()
                svg_path_dict = json.loads(tooth_obj.svg_paths_dict)
                if tooth_obj:
                    svg_path_dict = json.loads(tooth_obj.svg_paths_dict)
                    if treatment_obj.en_name == "Filling" or treatment_obj.en_name == "Refilling": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                        svg_path = svg_path_dict.get("Filling B")
                    elif treatment_obj.en_name == "Root Canal Treatment" or treatment_obj.en_name == "Root Canal Retreatment": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                        svg_path = svg_path_dict.get("Root Treated")
                    else:
                        svg_path = svg_path_dict.get(treatment_obj.en_name)
                    print("svg_path",svg_path)
                    svg_paths[tooth] = svg_path
                #end getting svg path if exists#
            print("svg paths",svg_paths)
            treatment_data = json.dumps(treatment_data)
            plan_obj.plan_treatment_data = treatment_data
            plan_obj.save()
            return JsonResponse({'success':True, 'treatment_slug':treatment_slug, 'teeth':teeth,'unit_price':unit_price, 'treatment_name':treatment_obj.en_name, 'price':loop_price, 'currency':currency, 'svg_paths':svg_paths})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while adding treatment to teeth: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class AddGeneralNote(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            plan_id = request.POST.get("plan_id")
            note = request.POST.get("note")
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            treatment_obj.general_note = note
            treatment_obj.save()
            print(f"plan id: {plan_id} -- note: {note}" )
            return JsonResponse({'success':True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while saving general note: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class AddIllnessToTeeth(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            image_report_id = request.POST.get("image_report_id")
            teeth_list = request.POST.getlist("teeth_list[]",None)
            label_slug = request.POST.get("label_slug")
            wizard_obj = TreatmentWizard.objects.get(image_report__id = image_report_id)
            diagnosis_data = json.loads(TreatmentWizard.objects.get(image_report__id = image_report_id).diagnosis_data)
            label_obj = LabelNamesForWizard.objects.get(slug=label_slug)
            subs = LabelNamesForWizard.objects.filter(sub_of_this=label_obj)
            returned_dict = {}
            print("teeth_list",teeth_list)
            for tooth in teeth_list:
                if label_obj.en_name == "Missing":
                    diagnosis_data[str(tooth)]["is_missing"] = True
                    tooths_illness_list = diagnosis_data[str(tooth)]["illnesses"] = []
                    key = str(uuid.uuid4()).replace("-","")
                    new_illness_dict = {
                        "name":label_obj.en_name,
                        "slug":key,
                        "probability":101,
                        "tr_name":label_obj.tr_name,
                        "ar_name":label_obj.ar_name,
                        "pt_name":label_obj.pt_name,
                        "fr_name":label_obj.fr_name,
                    }
                    returned_dict[tooth] = new_illness_dict
                    tooths_illness_list.append(new_illness_dict)
                    wizard_obj.diagnosis_data = json.dumps(diagnosis_data)
                    wizard_obj.save()
                    tooth_obj = TeethImages.objects.filter(teeth_number = int(tooth)).first()
                    svg_path = tooth_obj.path
                    returned_dict[tooth]["svg_path"] = svg_path.path
                else:
                    tooths_illness_list = diagnosis_data[str(tooth)]["illnesses"]
                    key = str(uuid.uuid4()).replace("-","")
                    new_illness_dict = {
                        "name":label_obj.en_name,
                        "slug":key,
                        "probability":101,
                        "tr_name":label_obj.tr_name,
                        "ar_name":label_obj.ar_name,
                        "pt_name":label_obj.pt_name,
                        "fr_name":label_obj.fr_name,
                    }
                    returned_dict[tooth] = new_illness_dict
                    tooths_illness_list.append(new_illness_dict)
                    wizard_obj.diagnosis_data = json.dumps(diagnosis_data)
                    wizard_obj.save()
                    #start of finding svg element for added disease#
                    tooth_obj = TeethImages.objects.filter(teeth_number = int(tooth)).first()
                    if tooth_obj:
                        svg_path_dict = json.loads(tooth_obj.svg_paths_dict)
                        if "filling" in label_obj.en_name.lower():
                            svg_path = svg_path_dict.get("Filling B")
                        elif "caries" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Caries B")
                        elif "bone loss" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Bone Loss 2")
                        elif "furcation defect" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Furcation Lesion")
                        elif "root-canal filling" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Root Treated")
                        elif "inlay" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Inlay")
                        elif "onlay" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Onlay")
                        elif "overlay" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Overlay")
                        elif "post" in label_obj.en_name.lower() or "post-fiber" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Post")
                        elif "parapulpal pin" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Parapulpal Pin")
                        elif "veneer" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Veneer")
                        elif "periapical lesion" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Preiapical Lesion")
                        elif "residual root" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Radix")
                        elif "impacted tooth" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Impacted")
                        elif "dental fracture" in label_obj.en_name.lower(): #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Fractured")
                        elif label_obj.en_name == "Missing": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = None
                        else:
                            svg_path = svg_path_dict.get(label_obj.en_name)
                        print("svg path",svg_path)
                        print("svg path",)
                    returned_dict[tooth]["svg_path"] = svg_path
                    #sublevel status check start#
                    returned_dict[tooth]["subs"] = {}
                    if subs:
                        for sub in subs:
                            returned_dict[tooth]["subs"][sub.en_name] = {
                              "en_name":sub.en_name,  
                              "tr_name":sub.tr_name,  
                              "pt_name":sub.pt_name,  
                              "fr_name":sub.fr_name,  
                              "ar_name":sub.ar_name,  
                              "slug":sub.slug,  
                            }
                    #sublevel status check end#
                    #end of finding svg element for added disease#
            return JsonResponse({'success':True,"data":returned_dict})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while adding illness to teeth: {traceback_str}")
            user = request.user
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class DeleteAllIllnessesFromTooth(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            image_report_id = request.POST.get("image_report_id")
            tooth_number = request.POST.get("tooth_number")
            print(f"tooth number : {tooth_number} -- image report id : {image_report_id}")
            wizard_obj = TreatmentWizard.objects.get(image_report__id = image_report_id)
            diagnosis_data = json.loads(TreatmentWizard.objects.get(image_report__id = image_report_id).diagnosis_data)
            target_tooth = diagnosis_data[tooth_number]["illnesses"]
            print("target tooth",target_tooth, type(target_tooth))
            target_tooth.clear()
            print("diagnosis data", diagnosis_data)
            wizard_obj.diagnosis_data = json.dumps(diagnosis_data)
            wizard_obj.save()
            return JsonResponse({'success':True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while deleting all illness from tooth: {traceback_str}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class CreateNewTreatmentPlan(LoginRequiredMixin,APIView):
    def get(self,request):
        try:
            user = request.user
            image_report_id = request.GET.get("image_report_id")
            wizard_obj = TreatmentWizard.objects.get(image_report__id = image_report_id)
            raw_treatment_data = json.loads(wizard_obj.raw_treatment_data)
            last_treatment_obj = TreatmentPlan.objects.filter(treatment_wizard = wizard_obj).last()
            treatment_count = TreatmentPlan.objects.filter(treatment_wizard = wizard_obj).count()
            print("treatment count",treatment_count)
            if last_treatment_obj:
                queue = last_treatment_obj.plan_queue + 1
            else:
                queue = 1
            new_treatment_plan = TreatmentPlan.objects.create(
                plan_queue = queue,
                treatment_wizard = wizard_obj,
                plan_treatment_data = json.dumps(raw_treatment_data)
            )
            return JsonResponse({'success':True, 'plan_id':new_treatment_plan.id, 'counter':treatment_count+1})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while deleting all illness from tooth: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class DeleteTreatmentPlan(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            image_report_id = request.POST.get("image_report_id")
            wizard_obj = TreatmentWizard.objects.get(image_report__id = image_report_id)
            plan_id = request.POST.get("treatment_plan_id")
            is_last = TreatmentPlan.objects.filter(treatment_wizard = wizard_obj).count()
            if is_last == 1:
                return JsonResponse({'success':True, 'is_last':True})
            treatment_obj_to_delete = TreatmentPlan.objects.get(id=plan_id, treatment_wizard=wizard_obj)
            treatment_obj_to_delete.delete()
            first_treatment_plan = TreatmentPlan.objects.filter(treatment_wizard = wizard_obj).first()
            first_treatment_plan_id = first_treatment_plan.id
            return JsonResponse({'success':True, 'first_treatment_plan_id':first_treatment_plan_id})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while deleting all illness from tooth: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class UpdateTreatmentPrice(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            profile = Profile.objects.get(user=user) 
            company = profile.company
            treatment_slug = request.POST.get("treatment_slug")
            price = request.POST.get("price")
            treatment_method = TreatmentNamesForWizard.objects.get(slug=treatment_slug)
            company_treatment_obj, created = CompanyTreatmentPricing.objects.get_or_create(treatment_method=treatment_method, company=company)
            print("company_treatment_obj", company_treatment_obj)

            # Eğer kayıt oluşturulduysa veya zaten var olan bir kayıt güncelleniyorsa, fiyatı güncelle.
            company_treatment_obj.price = price
            company_treatment_obj.save()

            print("treatment_slug", treatment_slug)
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while updating price of treatment: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class AddNoteToTreatment(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            treatment_slug = request.POST.get("treatment_slug")
            plan_id = request.POST.get("plan_id")
            note = request.POST.get("note")
            print(f"treatment slug: {treatment_slug} -- plan id: {plan_id} -- note:{note}")
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            note_area = {}
            if treatment_obj.notes:
                note_area = json.loads(treatment_obj.notes)
            note_area[treatment_slug] = note
            treatment_obj.notes = json.dumps(note_area)
            treatment_obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while updating price of treatment: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class DeleteSpecificTreatment(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            treatment_slug = request.POST.get("treatment_slug")
            plan_id = request.POST.get("plan_id")
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            treatment_json = json.loads(treatment_obj.plan_treatment_data)
            print(f"treatment slug: {treatment_slug}")
            print("treatment json 1", treatment_json)
            for tooth_number,value in treatment_json.items():
                treatment_methods = value["treatment_methods"]
                if treatment_methods:
                    for item in treatment_methods:
                        if item["slug"] == treatment_slug:
                            treatment_methods.remove(item)
            print("treatment json 2", treatment_json)
            treatment_obj.plan_treatment_data = json.dumps(treatment_json)
            treatment_obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while deleting specific treatment: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class ResetTreatment(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            plan_id = request.POST.get("plan_id")
            print("plan id", plan_id)
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            treatment_obj.plan_treatment_data = ""
            treatment_obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            logger.error(f"Error occurred while deleting specific treatment: {traceback_str} -- user: {user.email}")
            return JsonResponse({'success':False})

class ChangePricingType(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            plan_id = request.POST.get("plan_id")
            treatment_slug = request.POST.get("treatment_slug")
            pricing_type = request.POST.get("pricing_type")
            profile = Profile.objects.get(user=user)
            company = profile.company
            print(f"plan id : {plan_id} -- treatment slug: {treatment_slug} -- pricing_type: {pricing_type}")
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            plan_pricing = json.loads(treatment_obj.plan_pricing) if treatment_obj.plan_pricing else {}
            plan_pricing[treatment_slug]= {
                "type":pricing_type
            }
            treatment_obj.plan_pricing = json.dumps(plan_pricing)
            treatment_obj.save()
            # start - datas to returned for updating amount and price colons #
            treatment_price_obj = CompanyTreatmentPricing.objects.filter(treatment_method__slug = treatment_slug, company=company).first()
            if not treatment_price_obj:
                if pricing_type == "free":
                    price = "-"
                elif pricing_type == "inpackage":
                    price = "-"
                elif pricing_type == "package":
                    price = 1000
                else:
                    price = 1000
            else:
                if pricing_type == "free":
                    price = "-"
                elif pricing_type == "inpackage":
                    price = "-"
                elif pricing_type == "package":
                    price = treatment_price_obj.price
                else:
                    price = treatment_price_obj.price
            # end - datas to returned for updating amount and price colons #
            return JsonResponse({'success': True, 'price':price})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while changing pricing type: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class ApplyDiscount(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            plan_id = request.POST.get("plan_id")
            discount = request.POST.get("discount")
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            print(f"discount : {discount} -- plan id: {plan_id}")
            treatment_obj.discount = discount
            treatment_obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while changing pricing type: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})

class SaveDocumentsForTreatmentPlan(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            plan_id = request.POST.get("plan_id")
            slug = request.POST.get("slug")
            parameter = request.POST.get("parameter")
            print(f"plan_id : {plan_id} -- slug: {slug}")
            document_obj = DocumentTemplates.objects.get(slug=slug)
            treatment_plan = TreatmentPlan.objects.get(id=plan_id)
            if parameter == "save":
                clinic_saved_templates, created = ClinicSavedTemplatesForTreatment.objects.get_or_create(treatment_plan=treatment_plan)
                clinic_saved_templates.templates.add(document_obj)
            else:
                clinic_saved_template = ClinicSavedTemplatesForTreatment.objects.get(treatment_plan=treatment_plan)
                clinic_saved_template.templates.remove(document_obj)
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while changing pricing type: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class SaveEditedDocumentsForCompany(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            user = request.user
            slug = request.POST.get("slug")
            profile = Profile.objects.get(user=user)
            company = profile.company
            content = request.POST.get("content")
            template_obj = DocumentTemplates.objects.get(slug=slug)
            clinic_modified_templates, created = ClinicModifiedTemplates.objects.get_or_create(company=company,template=template_obj)
            clinic_modified_templates.modified_content = content
            clinic_modified_templates.save()
            print(f"slug : {slug} -- content: {content}")
            return JsonResponse({'success': True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Error occurred while changing pricing type: {traceback_str} -- user: {user.email}")
            user = request.user
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error)
            return JsonResponse({'success':False})
        
class GetPdfContent(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            self.content_list = request.POST.getlist("contentList[]",None)
            self.content_text = '\n\n'.join(self.content_list)
            print("content list",self.content_text)
            filename = "test_" + str(uuid.uuid4()).replace("-", "")[0:10] + ".pdf"
            pdf_path = os.path.join("/home/akilliceviribilisim/Clinic/Wizard/api", filename)  # Bu kısma PDF'nin kaydedileceği konumu belirtin
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            y_position = 750 
            soup = BeautifulSoup(self.content_text, 'html.parser')
            print("soup",soup)
           # Her bir HTML etiketini ele alarak içeriğini yazdırma
            for tag in soup.find_all(recursive=False):  # Sadece ilk seviyedeki etiketleri ele al
                content = tag.get_text(strip=True)  # Etiket içeriğini al, boşlukları kaldır
                p.drawString(100, y_position, content)
                y_position -= 20  # Her etiketin altında 20 birim dikey konum değişikliği yap
            p.showPage()
            p.save()
            with open(pdf_path, 'wb') as f:
                f.write(buffer.getvalue())

            return JsonResponse({'success': True, 'pdf_path': pdf_path})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            logger.error(f"Error occurred while writing pdf file: {traceback_str} -- user: {user.email}")
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error,ignore=True)
            return JsonResponse({'success':False})
    
class DownloadPDF(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            plan_id = request.POST.get("plan_id")
            print("plan id",plan_id)
            treatment_plan_obj = TreatmentPlan.objects.get(id=plan_id)
            if treatment_plan_obj.pdf_file:
                pdf_path = treatment_plan_obj.pdf_file
                file_name = pdf_path.split("/")[-1]
            else:
                pdf_path = None
                file_name = None
            print(f"treatment obj: {treatment_plan_obj} && pdf path: {pdf_path} && file name: {file_name}")
            return JsonResponse({'success': True, 'pdf_path':pdf_path, "file_name":file_name})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            logger.error(f"Error occurred while writing pdf file: {traceback_str} -- user: {user.email}")
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error,ignore=True)
            return JsonResponse({'success':False})

class EditTag(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            tag_slug = request.POST.get("tag_slug")
            wizard_id = request.POST.get("wizard_id")
            new_tag_value = request.POST.get("new_tag_value")
            print(f"tag_slug: {tag_slug} -- wizard_id: {wizard_id} -- new_tag_value: {new_tag_value}")
            wizard_obj = TreatmentWizard.objects.get(image_report__id=wizard_id)
            if wizard_obj.general_tags:
                print("tags", wizard_obj.general_tags)
                tags = json.loads(wizard_obj.general_tags)
                for tag in tags:
                    if tag["slug"] == tag_slug:
                        tag["tag_value"] = new_tag_value
                        wizard_obj.general_tags = json.dumps(tags)
                        wizard_obj.save()
                        break
            return JsonResponse({'success':True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            logger.error(f"Error occurred while editing tag: {traceback_str} -- user: {user.email}")
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error,ignore=True)
            return JsonResponse({'success':False})
        
class ReplaceDiagnosis(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            old_slug = request.POST.get("old_slug")
            new_slug = request.POST.get("new_slug")
            wizard_id = request.POST.get("wizard_id")
            print(f"old slug: {old_slug} -- new slug: {new_slug} -- wizard id: {wizard_id}")
            wizard_obj = TreatmentWizard.objects.get(image_report__id=wizard_id)
            data = json.loads(wizard_obj.diagnosis_data)
            new_illness = LabelNamesForWizard.objects.get(slug=new_slug)
            returned_data = None
            for key,value in data.items():
                for illness in value["illnesses"]:
                    if illness["slug"] == old_slug:
                        illness["name"] = new_illness.en_name
                        illness["en_name"] = new_illness.en_name
                        illness["tr_name"] = new_illness.tr_name
                        illness["pt_name"] = new_illness.pt_name
                        illness["ar_name"] = new_illness.ar_name
                        illness["slug"] = str(uuid.uuid4()).replace("-","")
                        illness["probability"] = 101
                        tooth = TeethImages.objects.get(teeth_number = int(key))
                        svg_path_dict = json.loads(tooth.svg_paths_dict)
                        if new_illness.en_name == "Filling" or new_illness.en_name == "Refilling": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Filling B")
                        elif new_illness.en_name == "Root Canal Treatment" or new_illness.en_name == "Root Canal Retreatment": #buralar sonra dinamik olacak şimdilik ibrahim hoca ayarlayana kadar böyle
                            svg_path = svg_path_dict.get("Root Treated")
                        else:
                            svg_path = svg_path_dict.get(new_illness.en_name)
                        illness["svg_path"] = svg_path
                        returned_data = illness
                        break
            wizard_obj.diagnosis_data = json.dumps(data)
            wizard_obj.save()
            return JsonResponse({'success':True, 'returned_data':returned_data})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            logger.error(f"Error occurred while replacing illness: {traceback_str} -- user: {user.email}")
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error,ignore=True)
            return JsonResponse({'success':False})
        
class SaveExtraTreatment(LoginRequiredMixin,APIView):
    def post(self,request):
        try:
            selected_plan_id= request.POST.get("selected_plan_id")
            wizard_id = request.POST.get("wizard_id")
            plan_id = request.POST.get("current_treatment_plan")
            wizard_obj = TreatmentWizard.objects.get(image_report__id = wizard_id)
            treatment_obj = TreatmentPlan.objects.get(id=plan_id)
            extra_treatment, created = ExtraTreatmentPlans.objects.get_or_create(treatment_wizard = wizard_obj, treatment_plan = treatment_obj)
            list_of_extras = extra_treatment.selected_treatments
            request_type = request.POST.get("request_type")
            print(f"wizard_id: {wizard_id} -- plan_id: {plan_id} -- selected_plan_id: {selected_plan_id} -- request_type: {request_type}")
            if list_of_extras and request_type == "add":
                list_of_extras = json.loads(list_of_extras)
                print("list of extras",list_of_extras,type(list_of_extras))
                if not selected_plan_id in list_of_extras: 
                    list_of_extras.append(selected_plan_id)
            elif list_of_extras and request_type == "remove":
                list_of_extras = json.loads(list_of_extras)
                list_of_extras.remove(selected_plan_id)
            else:
                list_of_extras = []
                list_of_extras.append(selected_plan_id)
            extra_treatment.selected_treatments = json.dumps(list_of_extras)
            extra_treatment.save()
            return JsonResponse({'success':True})
        except Exception as e:
            traceback_str = traceback.format_exc()
            user = request.user
            logger.error(f"Error occurred while saving extra treatment plan to pdf: {traceback_str} -- user: {user.email}")
            traceback.print_exc()
            error = traceback.format_exc()
            error_handler_function(user,error,ignore=True)
            return JsonResponse({'success':False})

@login_required
def save_cover_image(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            profile_photo = request.FILES['image']
            profile = Profile.objects.get(user=request.user)
            company = profile.company
            company.pdf_cover = profile_photo
            company.save()
            return JsonResponse({'success': True, 'image': profile.profile_photo.url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)

@login_required
def save_end_cover_image(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            image = request.FILES['image']
            profile = Profile.objects.get(user=request.user)
            company = profile.company
            company.pdf_finish_cover = image
            company.save()
            return JsonResponse({'success': True, 'image': company.pdf_finish_cover.url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        user = request.user
        traceback.print_exc()
        error = traceback.format_exc()
        error_handler_function(user,error)