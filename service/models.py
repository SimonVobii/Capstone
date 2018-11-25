from django.db import models
from django.contrib.auth.models	import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import *
from django.utils import timezone

class PortfolioID(models.Model):
#connects users to their saved portfolios. Also contains information on the portfolio's goals and time horizon
	portfolioID = models.AutoField(primary_key=True)
	portfolioName = models.CharField(max_length = 15, default='filler')
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	goalValue = models.FloatField(default = 0.05)
	timeHorizon = models.DateField(default=timezone.now)

class stockID(models.Model):
#contains information on particular stocks that is not appropriate to be stored elsewhere
	tickerID = models.CharField(max_length = 5, primary_key=True)
	companyName = models.TextField(default='filler')
	ipoDate = models.DateField(default=timezone.now)

class PortfolioWeights(models.Model):
#contains the current asset weights that define each portfolio
	weightID = models.AutoField(primary_key=True)
	portfolioID = models.ForeignKey(PortfolioID, on_delete=models.CASCADE)
	tickerID = models.ForeignKey(stockID, on_delete=models.CASCADE)
	volume = models.FloatField(default = 0)

	class Meta:
	#while django doesn't support true multi primary key, this gives us the desired functionality
		unique_together = (('tickerID','portfolioID'))

class stockHistory(models.Model):
#largest data table, contains daily price for each asset. Note that this uses
#a double primary key for easier indexing
	eventID = models.AutoField(primary_key=True)
	tickerID = models.ForeignKey(stockID, on_delete=models.CASCADE)
	dateID = models.DateField(default=timezone.now)
	assetPrice = models.FloatField(default = 0)
	assetReturn = models.FloatField(default = 0)

	class Meta:
	#while django doesn't support true multi primary key, this gives us the desired functionality
		unique_together = (('tickerID','dateID'))

class portfolioHistory(models.Model):
#contains a complete history of portfolio rebalancing (when the total volume of an asset changed,
#but now when the value of an asset holding varied in respect to total portfolio value)
	rebalanceID = models.AutoField(primary_key=True)
	portfolioID = models.ForeignKey(PortfolioID, on_delete=models.CASCADE)
	tickerID = models.ForeignKey(stockID, on_delete=models.CASCADE)
	dateID = models.DateField(auto_now=True)

class tester(models.Model):
	firstName = models.CharField(max_length = 15)
	dateTest = models.DateField(default = timezone.now)
