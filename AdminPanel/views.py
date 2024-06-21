from django.shortcuts import render
from Application.models import *
from User.models import *
from Application.functions import *
from .functions import *
from django.contrib.admin.views.decorators import staff_member_required
from Server.settings import clinic_project_id
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def get_specs():
    spec = SpecificParameter.objects.get(id=clinic_project_id)
    specs = {
        "login_page_logo": spec.loginpage_logo_design.url.replace("static/", "") if spec.loginpage_logo_design else None,
        "logo": spec.base_html_left_top_logo.url.replace("static/", ""), 
        "title": spec.page_title, 
        "banner": spec.loginpage_banner.url.replace("static/", "") if spec.loginpage_banner else None,
        "language_visibility": spec.language_visibility, 
        "brand": spec.base_html_left_bottom_title, 
        "theme_css": spec.base_html_css.url.replace("static/", "") if spec.base_html_css else None,
        "report_page_title_banner": spec.report_page_title_banner.url.replace("static/", ""),
        "favicon": spec.favicon.url.replace("static/", "") if spec.favicon else None,
        "clarification_text": spec.clarification_text.url.replace("static/", "") if spec.clarification_text else None,
        "privacy_policy": spec.privacy_policy.url.replace("static/", "") if spec.privacy_policy else None,
        "cookie_policy": spec.cookie_policy.url.replace("static/", "") if spec.cookie_policy else None,
        "terms_conditions_policy": spec.terms_conditions_policy.url.replace("static/", "") if spec.terms_conditions_policy else None,
        "login_page_content": spec.login_page_content if spec.login_page_content else None,
        "website_link": spec.website_link if spec.website_link else None,
        "website_name": spec.website_name if spec.website_name else None,
        }
    return specs

# @staff_member_required
def for_admin_active_users_and_count(request):
    if request.user.is_authenticated: 
        user = request.user
        profile = Profile.objects.get(user=user)
    else:
        return redirect('loginPage')
    if not profile.is_distributor and not request.user.is_superuser:
        # Eğer anonim bir kullanıcı ise, istediğiniz sayfaya yönlendirin
        return redirect('loginPage')
    active_users = ActiveUsers.objects.first()
    print("active_userS", active_users)
    infos_of_users = []
    specs = get_specs()
    user_theme_dict = user_theme_choices(user)
    if active_users:
        all_active_users = active_users.active_users.all()
        for active_user in all_active_users:
            username = active_user.username
            first_name = active_user.first_name 
            last_name = active_user.last_name 
            profile = Profile.objects.get(user=user)
            current_user_dict = {
                'username':username,
                'last_name':last_name,
                'first_name':first_name,
                'clinic':profile.company.name,
                'phone':profile.phone,
            }
            infos_of_users.append(current_user_dict)
        active_user_count = active_users.active_user_count
    else:
        active_user_count = 0
    print("infos of users",infos_of_users)
    context = {
        "infos_of_users":infos_of_users,
        "specs":specs,
        "active_user_count": active_user_count,
        "user_theme_choices_json": json.dumps(user_theme_dict),
        "user_theme_choices": user_theme_dict,
    }
    return render(request, "dashboard/active-users.html", context)

# def dashboard_user_list(request):
#     profiles = get_all_users()
#     context = {
#         "profiles":profiles,
#     }
#     return render(request, 'dashboard/user_list.html',context)

# def dashboard_user_detail_and_statistics(request,id):
#     user = User.objects.get(id=id)
#     user_profile = Profile.objects.get(user=user)
#     total_patient_count = Patient.objects.filter(user=user_profile).count()
#     total_image_count = Image.objects.filter(user=user_profile).count()
#     total_analyse_count = ImageReport.objects.filter(user=user_profile).count()
#     total_created_report_count = CreateReportForPatient.objects.filter(patient__user = user_profile).count()
#     context = {
#         'user':user,
#         'user_profile':user_profile,
#         'total_patient_count':total_patient_count,
#         'total_image_count':total_image_count,
#         'total_analyse_count':total_analyse_count,
#         'total_created_report_count':total_created_report_count,
#     }
#     return render(request, 'dashboard/user_detail.html',context)

@login_required
def dashboard_homepage(request):
    user=request.user
    specs = get_specs()
    user_theme_dict = user_theme_choices(user)
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        period = request.POST.get("period")
        print(f"start_date: {start_date} -- end_date: {end_date} -- period:{period}")
        panaromic, bitewing, periapical, cbct, lateral = radiography_type_counts_with_date(start_date,end_date,period)
        patient_count = total_patient_count_with_date(start_date,end_date,period)
        user_count = total_user_count_with_date(start_date,end_date,period)
        radiography_count = total_uploaded_radiography_with_date(start_date,end_date,period)
        anaylse_count = total_analyse_count_with_date(start_date,end_date,period)
        radiography_type_count_dict = {
            "Panaromic":panaromic,
            "Bitewing":bitewing,
            "Periapical":periapical,
            "CBCT":cbct,
            "Lateral Cephalometric":lateral,
        }
        context = {
            "specs":specs,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "radiography_type_count_dict":json.dumps(radiography_type_count_dict),
            "patient_count":patient_count,
            "user_count":user_count,
            "radiography_count":radiography_count,
            "analysis_count":anaylse_count,
        }
        return JsonResponse({'status':200, 'data':context})
    else:
        panaromic, bitewing, periapical, cbct, lateral = radiography_type_counts()
        patient_count = total_patient_count()
        user_count = total_user_count()
        radiography_count = total_uploaded_radiography()
        anaylses_by_months = analyses_by_months()
        analyse_count = total_anaylse_count()
        radiography_type_count_dict = {
            "Panaromic":panaromic,
            "Bitewing":bitewing,
            "Periapical":periapical,
            "CBCT":cbct,
            "Lateral Cephalometric":lateral,
        }
        print("radiography_type_count_dict",radiography_type_count_dict)
        context = {
            "specs":specs,
            "user_theme_choices_json": json.dumps(user_theme_dict),
            "user_theme_choices": user_theme_dict,
            "radiography_type_count_dict":json.dumps(radiography_type_count_dict),
            "patient_count":patient_count,
            "user_count":user_count,
            "radiography_count":radiography_count,
            "anaylses_by_months":json.dumps(anaylses_by_months),
            "analysis_count":analyse_count,
        }
        return render(request,'dashboard/dashboard.html',context)

def user_login_activities(request):
    pass
