# tasks.py

from __future__ import absolute_import, unicode_literals
from datetime import datetime
from celery import shared_task
from django.core.cache import cache


@shared_task
def start_auto_analyze():
    print("AAAAAAAAAAAAAAAA")
    shared_time = cache.get("shared_time")
    # Her çalışmadan önce 2 saniye ekleyin
    next_run_time = shared_time + timedelta(seconds=2)
    # Bir sonraki çalışma anını ayarlamak için `apply_async` yöntemini kullanın
    start_auto_analyze.apply_async(countdown=next_run_time.total_seconds())


start_auto_analyze.delay()