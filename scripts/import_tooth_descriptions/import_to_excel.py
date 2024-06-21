import pandas as pd
import traceback
from Application.models import ReportPageIllnessDescriptions
from tqdm import tqdm
# from scripts.import_tooth_descriptions.import_to_excel import import_excel_to_db
# import_excel_to_db()
def import_excel_to_db():
    # Excel dosyasını oku
    dosya_yolu = r'/home/akilliceviribilisim/Clinic/scripts/import_tooth_descriptions/report_illness_descriptions.xlsx'  # Okunacak Excel dosyasının yolunu belirtin
    veri = pd.read_excel(dosya_yolu)
    # Excel dosyasındaki verilere erişim
    # Örnek olarak ilk sayfa (varsayılan olarak ilk sayfa yüklenir)
    ilk_sayfa = veri.iloc[:, :]  # Tüm hücrelerin değerleri
    print("len", len(ilk_sayfa))
    # İstediğiniz satır ve sütundaki değerlere erişim
    belirli_hucre = veri.iloc[0, 1]  # Örneğin, ilk satırın ve ilk sütunun değeri
    print("belirli_hucre", belirli_hucre)
    counter = 0
    for i in tqdm(range(len(ilk_sayfa))):
        try:
            label_id = veri.iloc[i, 0]
            besinci_kolon = veri.iloc[i,5]
            altinci_kolon = veri.iloc[i,6]
            yedinci_kolon = veri.iloc[i,7]
            sekizinci_kolon = veri.iloc[i,8]
            description_obj = ReportPageIllnessDescriptions.objects.get(id=int(label_id))
            counter += 1
            description_obj.before_tooth_numbers_text_ru = besinci_kolon
            description_obj.after_tooth_numbers_text_ru = altinci_kolon
            description_obj.before_tooth_numbers_text_uz = yedinci_kolon
            description_obj.after_tooth_numbers_text_uz = sekizinci_kolon
            description_obj.save()
        except:
            print("i", i)
            traceback.print_exc()
    print("counter",counter)