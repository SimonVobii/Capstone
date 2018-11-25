import csv
import service.models as service_models

def run(*args):
	if 'load' in args:
		with open("raw_data/ticker.csv", newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader)
			for row in reader:
				newTicker = service_models.stockID(tickerID=row[0])
				newTicker.save()
	if 'delete' in args:
		service_models.stockID.objects.all().delete()