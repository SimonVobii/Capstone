from adaptor.model import CsvModel

class StockHistoryModel(CsvModel):
	dateID = IntegerField()
	tickerID = CharField()