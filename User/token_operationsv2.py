import traceback
from User.models import Profile, Company, ThakaaPackage, ThakaaTokenBar, ThakaaBuyedPackage, ThakaaBuyedToken, ThakaaRemainingToken, ThakaaTokenActivity
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.core.cache import cache
from datetime import datetime, timedelta
import uuid
import os
from Application.cache_processes import active_model_labels_function
from django.views.decorators.csrf import csrf_exempt
from User.mail import send_feedback_email
# from Server.settings import server_type
from django.utils import timezone

amount_of_spending = {
    "Panoramic": 4,
    "Bitewing": 1,
    "CBCT": 16,
    "Periapical": 1,
    "Lateral Cephalometric": 12,
    "refresh": 0
}

def spend_token(profile_id, spend_type):
    # profile_id = request.POST.get("profile_id")
    # spend_type = request.POST.get("spend_type")
    profile = Profile.objects.get(id=profile_id)
    spend_cost = amount_of_spending[spend_type]
    print(f"profile {profile}")
    print(f"spend_cost {spend_cost}")
    values = {
        0: profile,
        99: None,
        111: None,
    }

    next_function_tree = {
        #index: (true_index, false_index)
        0: (1, 2),
        1: (3, 4),
        2: (99, 2), # message break
        3: (5, 6),
        4: (99, 4),
        5: (99, 5),
        6: (7, 8),
        7: (9, None), # repeat
        8: (11, 10),
        9: (7, 8),
        10: (111, 10), # do the job
        11: (99, 11),# message break
        99: (99, "Break"),
    }
    # values[99] = "Break" if u wanna break the while loop

    # MODELS: ThakaaPackage, ThakaaTokenBar, ThakaaBuyedPackage, ThakaaBuyedToken, ThakaaRemainingToken
    def is_have_package_function(profile): # 0: (1, 2),
        true_index, false_index = next_function_tree[function_index]
        thakaa_default_package = ThakaaBuyedPackage.objects.filter(company=profile.company).order_by("-id").first()
        values[true_index] = profile.company
        values[false_index] = get_the_functions[false_index][1]
        values_for_return = true_index if thakaa_default_package else false_index
        return values_for_return

    def is_have_token_package_function(company): # 4: (20, 19), 8: (11, 10),
        true_index, false_index = next_function_tree[function_index]
        thakaa_buyed_token = ThakaaBuyedToken.objects.filter(company=company).order_by("-id").first()
        values[true_index] = thakaa_buyed_token
        values[false_index] = get_the_functions[false_index][1]
        values_for_return = true_index if thakaa_buyed_token else false_index
        return values_for_return

    def is_token_package_expired_function(thakaa_buyed_token): # 1: (4, 3),
        true_index, false_index = next_function_tree[function_index]
        is_expired_status = thakaa_buyed_token.end_date < timezone.now()
        values[true_index] = get_the_functions[true_index][1]
        values[false_index] = thakaa_buyed_token
        values_for_return = true_index if is_expired_status else false_index
        return values_for_return

    def monthly_renewal_date_of_token_expired_function(thakaa_buyed_token): # 3: (6, 5),
        true_index, false_index = next_function_tree[function_index]
        thakaa_remaining_token = ThakaaRemainingToken.objects.filter(thakaa_buyed_token=thakaa_buyed_token).order_by("-id").first()
        if not thakaa_remaining_token:
            ## Mail Fonksiyonu Eklenecek
            values_for_return = 112
            values[112] = get_the_functions[112][1]
            return values_for_return
        current_time = timezone.now()
        thakaa_expire_status = current_time > thakaa_remaining_token.next_renewal_date
        values[true_index] = thakaa_remaining_token
        values[false_index] = thakaa_remaining_token
        values_for_return = true_index if thakaa_expire_status else false_index
        return values_for_return

    def create_token_new_monthly_usage_function(thakaa_remaining_token): # 6: (3, None), 
        true_index, false_index = next_function_tree[function_index]
        thakaa_remaining_token.is_expired = True
        thakaa_buyed_token = thakaa_remaining_token.thakaa_buyed_token
        total_usage = thakaa_remaining_token.total_usage
        next_renewal_date = thakaa_remaining_token.next_renewal_date
        new_thakaa_remaining_token = ThakaaRemainingToken.objects.create(
                                                thakaa_buyed_token = thakaa_buyed_token,
                                                usage = 0,
                                                total_usage = total_usage,
                                                renewal_date = next_renewal_date
                                            )
        values[true_index] = new_thakaa_remaining_token.thakaa_buyed_token
        thakaa_remaining_token.save()
        return true_index

    def is_token_limit_exceeded_function(thakaa_remaining_token): # 5 : (8, 9),
        true_index, false_index = next_function_tree[function_index]
        thakaa_buyed_token = thakaa_remaining_token.thakaa_buyed_token
        is_limit_exceeded = thakaa_remaining_token.total_usage + spend_cost > thakaa_remaining_token.thakaa_buyed_token.tokenbar.token # 10 - 16 = -6 TRUE*** kalan limit // limit aşıldı kalan kullanım - işlem bedeli > 0 = limit aşılmadı (FALSE)//
        values[true_index] = get_the_functions[true_index][1]
        values[false_index] = thakaa_remaining_token
        values_for_return = true_index if is_limit_exceeded else false_index
        return values_for_return

    def spend_token_and_create_log_function(thakaa_remaining_token): # 9: (99, 111), # işlem break
        true_index, false_index = next_function_tree[function_index]
        thakaa_remaining_token.usage += spend_cost
        thakaa_remaining_token.total_usage += spend_cost
        thakaa_remaining_token.save()
        values[true_index] = get_the_functions[true_index][1]
        values_for_return = true_index
        ThakaaTokenActivity.objects.create(
            profile = profile,
            thakaa_remaining_token = thakaa_remaining_token,
            used_token = spend_cost,
            image_type = spend_type,
        )
        return values_for_return

    def finish_and_break(message):
        values[99] = "Break"
        values_for_return = function_index
        return values_for_return

    get_the_functions = {
        0: (is_have_package_function,), # Çıkan 1-2 0-A
        1: (is_have_token_package_function,), # Çıkan 3-4 A-B
        2: (finish_and_break,{"status": False, "message": "Your account is not activated!"}), # Çıkan --dict-- A-
        3: (is_token_package_expired_function,), # Çıkan 5-6 B-D
        4: (finish_and_break,{"status": False, "message": "You don't have any token! Would you like to buy?"}), # Çıkan --dict-- A-
        5: (finish_and_break,{"status": False, "message": "The tokens you have purchased for 2 years have expired."}), # Çıkan --dict-- A-
        6: (monthly_renewal_date_of_token_expired_function,), # Çıkan 7 D-C
        7: (create_token_new_monthly_usage_function,), # Çıkan 5-6 B-D
        8: (is_token_limit_exceeded_function,), # Çıkan 10-11 E-G
        9: (monthly_renewal_date_of_token_expired_function,), # Çıkan E-
        10: (spend_token_and_create_log_function,), # Çıkan --dict--  G-
        11: (finish_and_break, {"status": False, "message": "You don't have enough token limit. Would you like to buy tokens?"}), # Çıkan 12-13 G-H


        99: (finish_and_break,), 
        111: (finish_and_break, {"status": True, "message": "Token Spended!"}),
        112: (finish_and_break, {"status": False, "message": "An error occurred during the token transaction. Please Contact With info@thakaacatch.com."}),
    }
    function_index = 0
    while values[99] != "Break":
        function_parameter = values[function_index]
        index = get_the_functions[function_index][0](function_parameter)
        function_index = index

    return values[function_index]


def remaining_token(profile_obj=False, detailed_status=False):
    thakaa_remaining_token_obj = ThakaaRemainingToken.objects.filter(thakaa_buyed_token__company=profile_obj.company).order_by("-id").first()
    if not thakaa_remaining_token_obj:
        context = {
            "status": True, "package": {"name": None}
        }

        return context
    current_time = timezone.now()
    pack_expire_status = current_time > thakaa_remaining_token_obj.next_renewal_date
    package_dict = {}
    doctor_usages_dict = {}
    if pack_expire_status:
        val = spend_token(profile_obj.id, "refresh")
        thakaa_remaining_token_obj = ThakaaRemainingToken.objects.filter(thakaa_buyed_token__company=profile_obj.company).order_by("-id").first()
    token_activities = ThakaaTokenActivity.objects.filter(profile=profile_obj).last()
    package_dict["total_usage"] = int(thakaa_remaining_token_obj.total_usage)
    package_dict["limit"] = int(thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token)
    package_dict["usage_rate"] = f"{thakaa_remaining_token_obj.total_usage}/{thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token}"
    package_dict["usage_percent"] = int(thakaa_remaining_token_obj.total_usage / thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token * 100)
    package_dict["renewal_date"] = thakaa_remaining_token_obj.next_renewal_date.strftime('%d.%m.%Y')
    package_dict["start_date"] = thakaa_remaining_token_obj.thakaa_buyed_token.start_date.strftime('%d.%m.%Y')
    package_dict["end_date"] = thakaa_remaining_token_obj.thakaa_buyed_token.end_date.strftime('%d.%m.%Y')
    package_dict["last_token_activity"] = (token_activities.date + timedelta(hours=3)).strftime('%Y.%m.%d %H:%M') if token_activities else ""   

    def get_doctor_usages(profiles):

        for index, doctor_profile in enumerate(profiles):
            doctor_package_dict = {}
            doctor_token_spends = ThakaaTokenActivity.objects.filter(thakaa_remaining_token=thakaa_remaining_token_obj, profile=doctor_profile).order_by("-id")
            monthly_spend_count = 0
            total_spend_count = 0
            extra_spend_count = 0
            for spend in doctor_token_spends:
                monthly_spend_count += spend.used_token if thakaa_remaining_token_obj.renewal_date <= spend.date <= thakaa_remaining_token_obj.next_renewal_date else 0
                total_spend_count += spend.used_token

            doctor_package_dict["monthly_usage_rate"] = f"{monthly_spend_count}/{thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token}"
            doctor_package_dict["monthly_usage_percent"] = int(monthly_spend_count / thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token * 100)
            doctor_package_dict["total_usage_rate"] = f"{total_spend_count}/{thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token}"
            doctor_package_dict["total_usage_percent"] = int(total_spend_count / thakaa_remaining_token_obj.thakaa_buyed_token.tokenbar.token * 100)

            add_usages = {"profile": doctor_profile, "package": doctor_package_dict}
            if doctor_profile == profile_obj:
                doctor_usages_dict[0] = add_usages
            else:
                doctor_usages_dict[index + 1] = add_usages
    context = {
        "status": True, "package": package_dict}
    if detailed_status:
        thakaa_buyed_package = ThakaaBuyedPackage.objects.get(company=profile_obj.company)
        get_doctor_usages(thakaa_buyed_package.profiles.all())
        context["doctor_usages"] = doctor_usages_dict
    return context