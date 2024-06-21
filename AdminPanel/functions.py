from Application.models import *
from User.models import *
from django.db.models import F
import time
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta,date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import TruncMonth
from collections import defaultdict

def get_all_users():
    profiles = Profile.objects.annotate(
        company_name=F('company__name'),
        creator=F('creator_username')
    ).values(
        'user__id',
        'user__email', 
        'user__first_name',
        'user__last_name',
        'company_name',
        'phone',
        'clinic_name',
        'created_date',
        'creator',
        'is_owner_of_company',
    )

    return list(profiles)

def radiography_type_counts():
    start_time = time.time()
    radiography_types = Image.objects.values('type__name').annotate(count=Count('type'))
    lateral = radiography_types.get(type__name="Lateral Cephalometric")['count']
    panaromic = radiography_types.get(type__name="Panaromic")['count']
    bitewing = radiography_types.get(type__name="Bitewing")['count']
    cbct = radiography_types.get(type__name="CBCT")['count']
    periapical = radiography_types.get(type__name="Periapical")['count']
    end_time = time.time()
    elapsed_time = end_time - start_time
    return panaromic, bitewing, periapical, cbct, lateral

def total_patient_count():
    patient_count = Patient.objects.aggregate(total=Count('id'))['total']
    return patient_count

def total_user_count():
    user_count = User.objects.aggregate(total=Count('id'))['total']
    return user_count

def total_uploaded_radiography():   
    radiography_count = Image.objects.aggregate(total=Count('id'))['total']
    return radiography_count

def total_anaylse_count():
    analyse_count = ImageReport.objects.aggregate(total=Count('id'))['total']
    return analyse_count

def radiography_type_counts_with_date(start_date=None,end_date=None,period=None):
    if period:
        start_time = time.time()
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        radiography_types = Image.objects.filter(created_date__range=(start_point,today)).values('type__name').annotate(count=Count('type'))
        try:
            lateral = radiography_types.get(type__name="Lateral Cephalometric")['count']
        except ObjectDoesNotExist:
            lateral = 0
        try:
            panaromic = radiography_types.get(type__name="Panaromic")['count']
        except ObjectDoesNotExist:
            panaromic = 0
        try:
            bitewing = radiography_types.get(type__name="Bitewing")['count']
        except ObjectDoesNotExist:
            bitewing = 0
        try:
            cbct = radiography_types.get(type__name="CBCT")['count']
        except ObjectDoesNotExist:
            cbct = 0
        try:
            periapical = radiography_types.get(type__name="Periapical")['count']
        except ObjectDoesNotExist:
            periapical = 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        return panaromic, bitewing, periapical, cbct, lateral
    else:
        start_time = time.time()
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        radiography_types = Image.objects.filter(created_date__range=(start_date,end_date)).values('type__name').annotate(count=Count('type'))
        try:
            lateral = radiography_types.get(type__name="Lateral Cephalometric")['count']
        except ObjectDoesNotExist:
            lateral = 0
        try:
            panaromic = radiography_types.get(type__name="Panaromic")['count']
        except ObjectDoesNotExist:
            panaromic = 0
        try:
            bitewing = radiography_types.get(type__name="Bitewing")['count']
        except ObjectDoesNotExist:
            bitewing = 0
        try:
            cbct = radiography_types.get(type__name="CBCT")['count']
        except ObjectDoesNotExist:
            cbct = 0
        try:
            periapical = radiography_types.get(type__name="Periapical")['count']
        except ObjectDoesNotExist:
            periapical = 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        return panaromic, bitewing, periapical, cbct, lateral


def total_patient_count_with_date(start_date=None,end_date=None,period=None):
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        patient_count = Patient.objects.filter(created_date__range=(start_point, today)).count()
        return patient_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        patient_count = Patient.objects.filter(created_date__range=(start_date, end_date)).count()
        return patient_count

def total_analyse_count_with_date(start_date=None,end_date=None,period=None):
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        analyse_count = ImageReport.objects.filter(created_date__range=(start_point, today)).count()
        return analyse_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        analyse_count = ImageReport.objects.filter(created_date__range=(start_date, end_date)).count()
        return analyse_count

def total_user_count_with_date(start_date=None,end_date=None,period=None):
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        user_count = User.objects.filter(date_joined__range=(start_point,today)).count(),
        return user_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        user_count = User.objects.filter(date_joined__range=(start_date,end_date)).count(),
        return user_count


def total_uploaded_radiography_with_date(start_date=None,end_date=None,period=None):   
    if period:
        today = timezone.now()
        start_point = today - timedelta(days=int(period))
        radiography_count = Image.objects.filter(created_date__range=(start_point,today)).count(),
        return radiography_count
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        radiography_count = Image.objects.filter(created_date__range=(start_date,end_date)).count(),
        return radiography_count

def analyses_by_months():
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    analyses = (
        ImageReport.objects
        .filter(created_date__range=(start_date, end_date))
        .annotate(month=TruncMonth('created_date'))
        .values('month')
        .annotate(report_count=Count('id'))
        .order_by('month')
    )
    result_dict = {}
    for analysis in analyses:
        month = analysis['month'].strftime('%B')
        report_count = analysis['report_count']
        result_dict[month] = report_count
    return result_dict