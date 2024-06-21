from django.core.cache import cache
from Server.settings import AIServerUrl, dcmServerUrl
import json
import time
import threading
import requests

def fetch_data_from_AI_labels():
    print("**** UPDATING CACHE *****")

    #TEST URL
    print("AIServerUrl", AIServerUrl)
    url = f"{AIServerUrl}/label/list/activeModelLabels/"
    url_3d = f"{dcmServerUrl}/label/list/activeModelLabels/"

    #REALTİME URL
    # url = "http://93.89.73.105:8001/label/list/activeModelLabels/"
    # Verileri URL'den indirin ve Python sözlüğüne dönüştürün
    # Burada requests ve json kütüphanelerini kullanıyoruz.
    response = requests.get(url)
    print("response",response)
    active_model_labels = json.loads(response.content)
    # Verileri önbelleğe alın ve son kullanma süresi 2 saat olsun
    cache.set("active_model_labels_dict", active_model_labels, timeout=3600000)
    print("Setted 'active_model_labels_dict' is READY!" )
    try:
        response_3d = requests.get(url_3d)
        active_model_labels_3d = json.loads(response_3d.content)["Cone Beam Computed Tomography"]["Adult"]
        # Verileri önbelleğe alın ve son kullanma süresi 2 saat olsun
        cache.set("3d_labels_dict", active_model_labels_3d, timeout=3600000)
    except:
        print("3D CACHE ALINAMADI")
    print("active_model_labels_3d")
    print("Setted 'active_model_labels_dict' is READY!" )

def fetch_all_data_from_AI_labels():
    print("**** UPDATING CACHE *****")

    #TEST URL
    # url = f"{AIServerUrl}/label/list/allModelLabels/"

    #REALTİME URL
    # url = "http://93.89.73.105:8001/label/list/activeModelLabels/"
    # Verileri URL'den indirin ve Python sözlüğüne dönüştürün
    # Burada requests ve json kütüphanelerini kullanıyoruz.
    # response = requests.get(url)
    # active_model_labels = json.loads(response.content)
    # Verileri önbelleğe alın ve son kullanma süresi 2 saat olsun
    # cache.set("all_model_labels_dict", active_model_labels, timeout=3600)
    print("Setted 'all_model_labels_dict' is READY!" )

def active_model_labels_function():
    # while True:
    # Verileri önbellekten alıyoruz
    active_model_labels = cache.get("active_model_labels_dict")
    print("Getting 'active_model_labels_dict' from cache!")

    # Eğer önbellekte veri yoksa, verileri indirip ve önbelleğe alıayoruz
    if active_model_labels is None:
        fetch_data_from_AI_labels()
        active_model_labels = cache.get("active_model_labels_dict")

    return active_model_labels

def all_model_labels_function():
    # while True:
    # Verileri önbellekten alıyoruz
    active_model_labels = cache.get("all_model_labels_dict")
    print("active_model_labels", active_model_labels)

    # Eğer önbellekte veri yoksa, verileri indirip ve önbelleğe alıayoruz
    if active_model_labels is None:
        fetch_all_data_from_AI_labels()
        active_model_labels = cache.get("all_model_labels_dict")
    print("Getting 'all_model_labels_dict' from cache!")
    return active_model_labels

def cache_updater_function():
    # Thread'i başlat
    cache_updater = threading.Thread(target=active_model_labels_function)
    cache_updater.start()

def cache_all_updater_function():
    # Thread'i başlat
    cache_all_updater = threading.Thread(target=all_model_labels_function)
    cache_all_updater.start()