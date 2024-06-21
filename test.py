import json
import csv

def convert_nested_json_to_csv(json_filename, csv_filename):
    try:
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        # CSV dosyasına yazma
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # İlk satırı başlık olarak yazma
            csv_writer.writerow(['label_name', 'tr_name', 'color', 'id', 'label_type', 'label_type_tr', 'area'])

            # Her etiket için veriyi CSV dosyasına yazma
            for label_name, label_data in json_data.items():
                tr_name = label_data.get('tr_name', '')
                color = label_data.get('color', '')
                identifier = label_data.get('id', '')
                label_type = label_data.get('label_type', '')
                label_type_tr = label_data.get('label_type_tr', '')
                area = label_data.get('area', '')

                # Veriyi CSV dosyasına yazma
                csv_writer.writerow([label_name, tr_name, color, identifier, label_type, label_type_tr, area])

        print(f'CSV dosyası "{csv_filename}" başarıyla oluşturuldu.')
    except Exception as e:
        print(f'Hata oluştu: {e}')

# JSON dosyasını CSV'ye çevirme
convert_nested_json_to_csv('veri.json', 'active_labels_names.csv')