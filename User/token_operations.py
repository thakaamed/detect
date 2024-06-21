import traceback
from User.models import *
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

amount_of_spending = {
    "Panaromic": 4,
    "Bitewing": 1,
    "CBCT": 16,
    "Periapical": 1,
    "Lateral Cephalometric": 8,
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
        1: (4, 3),
        2: (99, 2), # message break
        3: (6, 5),
        4: (20, 19),
        5: (8, 9),
        6: (3, None),
        7: (6, 5),
        8: (11, 10),
        9: (100, 9), # işlem break
        10: (99, 10), # message break
        11: (13, 12),
        12: (15, 14),
        13: (99, 13), # message break
        14: (18, 17),
        15: (16, None),
        16: (15, 14),
        17: (111, 17), # işlem break
        18: (99, 18), # message break
        19: (99, 19), # message break
        20: (22, 21),
        21: (24, 23),
        22: (99, 22), # message break
        23: (27, 26),
        24: (25, None),
        25: (24, 23),
        26: (111, 26), # işlem break
        27: (99, 27), # message break
        99: (99, "Break")
    }
    # values[99] = "Break" if u wanna break the while loop

    def does_the_user_have_a_package_function(profile): # 0: (1, 2),
        true_index, false_index = next_function_tree[function_index]
        buyed_package = BuyedPackage.objects.filter(company=profile.company).order_by("-id").first()
        values[true_index] = buyed_package
        values[false_index] = get_the_functions[false_index][1]
        values_for_return = true_index if buyed_package else false_index
        return values_for_return

    def is_package_expired_function(buyed_package): # 1: (4, 3),
        true_index, false_index = next_function_tree[function_index]
        is_expired_status = buyed_package.end_date < timezone.now()
        values[true_index] = buyed_package.company
        values[false_index] = buyed_package
        values_for_return = true_index if is_expired_status else false_index
        return values_for_return

    def is_renewal_date_of_the_package_expired_function(buyed_package): # 3: (6, 5),
        true_index, false_index = next_function_tree[function_index]
        package_remaining_usage = PackageRemainingUsage.objects.filter(buyed_package=buyed_package).order_by("-id").first()
        if not package_remaining_usage:
            ## Mail Fonksiyonu Eklenecek
            values_for_return = 112
            values[112] = get_the_functions[112][1]
            return values_for_return
        current_time = timezone.now()
        pack_expire_status = current_time > package_remaining_usage.next_renewal_date
        values[true_index] = package_remaining_usage
        values[false_index] = package_remaining_usage
        values_for_return = true_index if pack_expire_status else false_index
        return values_for_return

    def create_package_new_monthly_usage_function(package_remaining_usage): # 6: (3, None), 
        true_index, false_index = next_function_tree[function_index]
        package_remaining_usage.is_expired = True
        buyed_package = package_remaining_usage.buyed_package
        total_usage = package_remaining_usage.total_usage
        remain_usage_limit = package_remaining_usage.usage_limit
        next_renewal_date = package_remaining_usage.next_renewal_date
        new_package_remaining_usage = PackageRemainingUsage.objects.create(
                                                buyed_package = buyed_package,
                                                usage = 0,
                                                total_usage = total_usage,
                                                usage_limit = buyed_package.package.token + remain_usage_limit,
                                                renewal_date = next_renewal_date
                                            )
        values[true_index] = new_package_remaining_usage.buyed_package
        package_remaining_usage.save()
        return true_index

    def is_package_limit_exceeded_function(package_remaining_usage): # 5 : (8, 9),
        true_index, false_index = next_function_tree[function_index]
        buyed_package = package_remaining_usage.buyed_package
        is_limit_exceeded = package_remaining_usage.usage + spend_cost > package_remaining_usage.usage_limit # 10 - 16 = -6 TRUE*** kalan limit // limit aşıldı kalan kullanım - işlem bedeli > 0 = limit aşılmadı (FALSE)//
        values[true_index] = buyed_package.company
        values[false_index] = package_remaining_usage
        values_for_return = true_index if is_limit_exceeded else false_index
        return values_for_return

    def spend_package_token_and_create_log_function(package_remaining_usage): # 9: (99, 111), # işlem break
        true_index, false_index = next_function_tree[function_index]
        package_remaining_usage.usage += spend_cost
        package_remaining_usage.total_usage += spend_cost
        package_remaining_usage.save()
        values[true_index] = get_the_functions[true_index][1]
        values_for_return = true_index
        UserTokenActivity.objects.create(
            profile = profile,
            buyed_package_or_extra_slug = package_remaining_usage.buyed_package.slug,
            used_token = spend_cost,
            image_type = spend_type,
        )
        return values_for_return

    def is_extra_package_function(company): # 4: (20, 19), 8: (11, 10),
        true_index, false_index = next_function_tree[function_index]
        buyed_extra_package = BuyedExtraPackage.objects.filter(company=company).order_by("-id").first()
        values[true_index] = buyed_extra_package
        values[false_index] = get_the_functions[false_index][1]
        values_for_return = true_index if buyed_extra_package else false_index
        return values_for_return

    def is_extra_package_expired_function(buyed_extra_package): # 11: (13, 12), 20: (22, 21),
        true_index, false_index = next_function_tree[function_index]
        is_expired_status = buyed_extra_package.end_date < timezone.now()
        values[true_index] = get_the_functions[true_index][1]
        values[false_index] = buyed_extra_package
        values_for_return = true_index if is_expired_status else false_index
        return values_for_return

    def is_renewal_date_of_the_extra_package_expired_function(buyed_extra_package): # 12: (15, 14), 21: (24, 23),
        true_index, false_index = next_function_tree[function_index]
        extra_package_remaining_usage = ExtraPackageRemainingUsage.objects.filter(buyed_extra_package=buyed_extra_package).order_by("-id").first()
        if not extra_package_remaining_usage:
            ## Mail Fonksiyonu Eklenecek
            values_for_return = 112
            values[112] = get_the_functions[112][1]
            return values_for_return
        
        current_time = timezone.now()
        pack_expire_status = current_time > extra_package_remaining_usage.next_renewal_date
        values[true_index] = extra_package_remaining_usage
        values[false_index] = extra_package_remaining_usage
        values_for_return = true_index if pack_expire_status else false_index
        return values_for_return

    def create_extra_package_new_monthly_usage_function(extra_package_remaining_usage): # tamamlanacak
        true_index, false_index = next_function_tree[function_index]
        extra_package_remaining_usage.is_expired = True
        buyed_extra_package = extra_package_remaining_usage.buyed_extra_package
        total_usage = extra_package_remaining_usage.total_usage
        next_renewal_date = extra_package_remaining_usage.next_renewal_date
        new_extra_package_remaining_usage = ExtraPackageRemainingUsage.objects.create(
                                                buyed_extra_package = buyed_extra_package,
                                                usage = 0,
                                                total_usage = total_usage,
                                                renewal_date = next_renewal_date
                                            )
        values[true_index] = extra_package_remaining_usage.buyed_extra_package
        values_for_return = true_index
        extra_package_remaining_usage.save()
        return values_for_return

    def is_extra_package_limit_exceeded_function(extra_package_remaining_usage): # tamamlanacak
        true_index, false_index = next_function_tree[function_index]
        buyed_extra_package = extra_package_remaining_usage.buyed_extra_package
        is_limit_exceeded = extra_package_remaining_usage.total_usage + spend_cost > buyed_extra_package.extra_package.token
        values[true_index] = get_the_functions[true_index][1]
        values[false_index] = extra_package_remaining_usage
        values_for_return = true_index if is_limit_exceeded else false_index
        return values_for_return
        
    def spend_extra_package_token_and_create_log_function(extra_package_remaining_usage): # 26: (99, 26), # işlem break
        true_index, false_index = next_function_tree[function_index]
        extra_package_remaining_usage.usage += spend_cost
        extra_package_remaining_usage.total_usage += spend_cost
        extra_package_remaining_usage.save()
        values[true_index] = get_the_functions[true_index][1]
        values_for_return = true_index
        UserTokenActivity.objects.create(
            profile = profile,
            buyed_package_or_extra_slug = extra_package_remaining_usage.buyed_extra_package.slug,
            used_token = spend_cost,
            image_type = spend_type,
        )
        return values_for_return

    def finish_and_break(message):
        values[99] = "Break"
        values_for_return = function_index
        return values_for_return
    
    get_the_functions = {
        0: (does_the_user_have_a_package_function,), # Çıkan 1-2 0-A
        1: (is_package_expired_function,), # Çıkan 3-4 A-B
        2: (finish_and_break,{"status": False, "message": "You do not have an package. Would You Like to Buy Packages?"}), # Çıkan --dict-- A-
        3: (is_renewal_date_of_the_package_expired_function,), # Çıkan 5-6 B-D
        4: (is_extra_package_function,), # Çıkan 19-20 B-F
        5: (is_package_limit_exceeded_function,), # Çıkan 8-9 D-E
        6: (create_package_new_monthly_usage_function,), # Çıkan 7 D-C
        7: (is_renewal_date_of_the_package_expired_function,), # Çıkan 5-6 B-D
        8: (is_extra_package_function,), # Çıkan 10-11 E-G
        9: (spend_package_token_and_create_log_function,), # Çıkan E-
        10: (finish_and_break, {"status": False, "message": "You have reached the monthly usage limit of the package and you do not have an additional package. Would You Like to Buy Additional Packages?"}), # Çıkan --dict--  G-
        11: (is_extra_package_expired_function,), # Çıkan 12-13 G-H
        12: (is_renewal_date_of_the_extra_package_expired_function,), # Çıkan 14-15 G-
        13: (finish_and_break, {"status": False, "message": "You have reached the monthly usage limit of the package and additional package have expired. Would you like to buy a new additional package?"}), # Çıkan --dict--  G-
        14: (is_extra_package_limit_exceeded_function,), # Çıkan 17-18 İ-J
        15: (create_extra_package_new_monthly_usage_function,), # Çıkan 16 İ-İ
        16: (is_renewal_date_of_the_extra_package_expired_function,), # Çıkan 28-29 İ-K
        17: (spend_extra_package_token_and_create_log_function,), # Çıkan J-
        18: (finish_and_break, {"status": False, "message": "Your primary package limit have been reached and you don't have enough additional package limit. Would you like to buy a new additional package?"}), # Çıkan --dict-- J
        19: (finish_and_break, {"status": False, "message": "The package has expired and you do not have an additional package. Would You Like to Buy Additional Packages?"}), # Çıkan --dict--  F-
        20: (is_extra_package_expired_function,), # Çıkan 21-22 F-L 
        21: (is_renewal_date_of_the_extra_package_expired_function,), # Çıkan L-M 23-24
        22: (finish_and_break ,{"status": False, "message": "Your primary package and additional package have expired. Would you like to buy a new additional package?"}), # Çıkan --dict--  L-
        23: (is_extra_package_limit_exceeded_function,), # Çıkan 26-27 M-P
        24: (create_extra_package_new_monthly_usage_function,), # Çıkan 25 M-M
        25: (is_renewal_date_of_the_extra_package_expired_function,), # Çıkan 30-31 M-M
        26: (spend_extra_package_token_and_create_log_function,), # Çıkan P
        27: (finish_and_break, {"status": False, "message": "Your primary package and additional package limits have been reached. Would you like to buy a new additional package?"}), # Çıkan --dict-- P


        99: (finish_and_break,), 
        100: (finish_and_break, {"status": True, "message": "Spended token from your package!"}),
        111: (finish_and_break, {"status": True, "message": "Spended token from your extra package!"}),
        112: (finish_and_break, {"status": False, "message": "An error occurred during the token transaction. Please Contact With info@craniocatch.com."}),
    }

    function_index = 0
    while values[99] != "Break":
        function_parameter = values[function_index]
        index = get_the_functions[function_index][0](function_parameter)
        function_index = index

    return values[function_index]


def remaining_token(profile_obj=False, detailed_status=False):
    remaining_package_obj = PackageRemainingUsage.objects.filter(buyed_package__company=profile_obj.company).order_by("-id").first()
    if not remaining_package_obj:
        context = {
            "status": True, "package": {"name": None}
        }
        return context
    current_time = timezone.now()
    pack_expire_status = current_time > remaining_package_obj.next_renewal_date
    package_dict = {}
    extra_package_dict = {}
    doctor_usages_dict = {}
    if pack_expire_status:
        val = spend_token(profile_obj.id, "refresh")
        remaining_package_obj = PackageRemainingUsage.objects.filter(buyed_package__company=profile_obj.company).order_by("-id").first()

    package_dict["name"] = remaining_package_obj.buyed_package.package.name
    package_dict["usage"] = remaining_package_obj.usage
    package_dict["total_usage"] = remaining_package_obj.total_usage
    package_dict["limit"] = remaining_package_obj.usage_limit
    package_dict["usage_rate"] = f"{remaining_package_obj.usage}/{remaining_package_obj.usage_limit}"
    package_dict["usage_percent"] = int(remaining_package_obj.usage / remaining_package_obj.usage_limit * 100)
    package_dict["renewal_date"] = remaining_package_obj.next_renewal_date.strftime('%d.%m.%Y')
    package_dict["start_date"] = remaining_package_obj.buyed_package.start_date.strftime('%d.%m.%Y')
    package_dict["end_date"] = remaining_package_obj.buyed_package.end_date.strftime('%d.%m.%Y')

    extra_remaining_package_obj = ExtraPackageRemainingUsage.objects.filter(buyed_extra_package__company=profile_obj.company).order_by("-id").first()
    if extra_remaining_package_obj:
        extra_package_dict["name"] = extra_remaining_package_obj.buyed_extra_package.extra_package.name
        extra_package_dict["usage"] = extra_remaining_package_obj.total_usage
        extra_package_dict["limit"] = extra_remaining_package_obj.buyed_extra_package.extra_package.token
        extra_package_dict["usage_rate"] = f"{extra_remaining_package_obj.usage}/{extra_remaining_package_obj.buyed_extra_package.extra_package.token}"
        extra_package_dict["usage_percent"] = int(extra_remaining_package_obj.usage / extra_remaining_package_obj.buyed_extra_package.extra_package.token * 100)
        extra_package_dict["start_date"] = extra_remaining_package_obj.buyed_extra_package.start_date.strftime('%d.%m.%Y')
        extra_package_dict["end_date"] = extra_remaining_package_obj.buyed_extra_package.end_date.strftime('%d.%m.%Y')

    def get_doctor_usages(profiles):

        for index, doctor_profile in enumerate(profiles):
            print("doctor_profile", doctor_profile)
            doctor_package_dict = {}
            doctor_extra_package_dict = {}
            doctor_token_spends = UserTokenActivity.objects.filter(buyed_package_or_extra_slug=remaining_package_obj.buyed_package.slug, profile=doctor_profile).order_by("-id")
            monthly_spend_count = 0
            total_spend_count = 0
            extra_spend_count = 0
            for spend in doctor_token_spends:
                monthly_spend_count += spend.used_token if remaining_package_obj.renewal_date <= spend.date <= remaining_package_obj.next_renewal_date else 0
                total_spend_count += spend.used_token

            doctor_package_dict["monthly_usage_rate"] = f"{monthly_spend_count}/{remaining_package_obj.usage_limit}"
            doctor_package_dict["monthly_usage_percent"] = int(monthly_spend_count / remaining_package_obj.usage_limit * 100)
            doctor_package_dict["total_usage_rate"] = f"{total_spend_count}/{remaining_package_obj.buyed_package.package.token}"
            doctor_package_dict["total_usage_percent"] = int(total_spend_count / remaining_package_obj.usage_limit * 100)
            
            if extra_remaining_package_obj:
                doctor_extra_token_spends = UserTokenActivity.objects.filter(buyed_package_or_extra_slug=extra_remaining_package_obj.buyed_extra_package.slug, profile=doctor_profile).order_by("-id")
                for spend in doctor_extra_token_spends:
                    extra_spend_count += spend.used_token
                doctor_extra_package_dict["total_usage_rate"] = f"{extra_spend_count}/{extra_remaining_package_obj.buyed_extra_package.extra_package.token}"
                doctor_extra_package_dict["total_usage_percent"] = int(extra_spend_count / extra_remaining_package_obj.buyed_extra_package.extra_package.token * 100)
            add_usages = {"profile": doctor_profile, "package": doctor_package_dict, "extra_package": doctor_extra_package_dict}
            if doctor_profile == profile_obj:
                doctor_usages_dict[0] = add_usages
            else:
                doctor_usages_dict[index + 1] = add_usages
    context = {
        "status": True, "package": package_dict, "extra_package": extra_package_dict
    }
    if detailed_status:
        get_doctor_usages(remaining_package_obj.buyed_package.profiles.all())
        context["doctor_usages"] = doctor_usages_dict
    return context