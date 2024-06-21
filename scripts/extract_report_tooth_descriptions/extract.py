from openpyxl import Workbook
from Application.models import ReportPageIllnessDescriptions

#from scripts.extract_report_tooth_descriptions import save_to_excel
def save_to_excel():
    # Yeni bir Excel dosyası oluştur
    wb = Workbook()
    ws = wb.active

    # Başlık satırını ekle
    ws.append(["ID", "Before Tooth Numbers (EN)", "After Tooth Numbers (EN)"])

    # Veritabanından verileri al ve Excel'e yaz
    for obj in ReportPageIllnessDescriptions.objects.all():
        before_text_en = obj.before_tooth_numbers_text_en
        after_text_en = obj.after_tooth_numbers_text_en

        # Verileri Excel dosyasına ekle
        ws.append([obj.id, before_text_en, after_text_en])

    # Excel dosyasını kaydet
    wb.save("report_illness_descriptions.xlsx")

