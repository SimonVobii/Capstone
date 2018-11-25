#from service import models as service_models

import csv
import service.models as service_models

def run(*args):
	if 'load' in args:
		with open("raw_data/test.csv", newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader)
			for row in reader:
				test = service_models.tester(date=row[0], ticker=row[1], assetPrice=row[2],assetReturn=row[3])
				test.save()
	if 'delete' in args:
		service_models.tester.objects.all().delete()