from embeded.models import EmbededImageReport, PublicAPICompany
def EmbededlerinKullaniminiHesapla(api_key,start_date=None,end_date=None):
    # slug listesini bir değişkene atayın, daha sonra bu listeyi fonksiyonu çağırarak içine verin
	Periapical = 0
	Panaromic = 0
	Bitewing = 0
	Lateral = 0

	PeriapicalToken = 0
	PanaromicToken = 0
	BitewingToken = 0
	LateralToken = 0
	company = PublicAPICompany.objects.get(api_key=api_key)
	if start_date and end_date:
		irs = EmbededImageReport.objects.filter(company=company, created_date__range=[start_date, end_date])
	else:
		irs = EmbededImageReport.objects.filter(company=company)
	for ir in irs:
		if not ir.company:
			ir.company = company 
			ir.save()
		if ir.image.type.name == "Periapical":
			Periapical += 1
		if ir.image.type.name == "Panaromic":
			Panaromic += 1
		if ir.image.type.name == "Bitewing":
			Bitewing += 1
		if ir.image.type.name == "Lateral Cephalometric":
			Lateral += 1
			
	PeriapicalToken = Periapical*1
	PanaromicToken = Panaromic*4
	BitewingToken = Bitewing*1
	LateralToken = Lateral*8

	print("PeriapicalToken: ", PeriapicalToken)
	print("PanaromicToken: ", PanaromicToken)
	print("BitewingToken: ", BitewingToken)
	print("LateralToken: ", LateralToken)
	remaining_dict = {
		"periapical":PeriapicalToken,
		"panaromic":PanaromicToken,
		"bitewing":BitewingToken,
		"lateral":LateralToken,
	}
	return remaining_dict