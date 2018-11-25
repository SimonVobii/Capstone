#from service import models as service_models

import csv
import service.models as service_models

with open("raw_data/test.csv", newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		test = service_models.tester(firstName=row)
		test.save()