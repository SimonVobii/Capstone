import csv
import service.models as service_models

def run(*args):
	if 'load' in args:
		with open("raw_data/stockret_5.csv", newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader)
			counter = 0
			for row in reader:
				x = service_models.stockHistory(dateID = row[0], tickerID=service_models.stockID.objects.get(tickerID=str(row[1])), assetPrice=row[2], assetReturn=row[3])
				x.save()
				counter += 1
				if (counter%10000 == 0):
					print(counter)
	if 'delete' in args:
		#service_models.stockHistory.objects.all().delete()
		print ("this is currently disabled to prevent accidental database deletion")