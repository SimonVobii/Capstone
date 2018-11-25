from django.db import models
from django.contrib.auth.models	import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import *

class PortfolioID(models.Model):
	portfolioID = models.AutoField(primary_key=True)
	userID = models.ForeignKey(User, on_delete=models.CASCADE)

class stockID(models.Model):
	tickerID = models.AutoField(primary_key=True)
	companyName = models.TextField()

class PortfolioWeights(models.Model):
	weightID = models.AutoField(primary_key=True)
	portfolioID = models.ForeignKey(PortfolioID, on_delete=models.CASCADE)
	tickerID = models.ForeignKey(stockID, on_delete=models.CASCADE)

class stockHistory(models.Model):
	eventID = models.AutoField(primary_key=True)
	tickerID = models.ForeignKey(stockID, on_delete=models.CASCADE)

class portfolioHistory(models.Model):
	rebalanceID = models.AutoField(primary_key=True)
	portfolioID = models.ForeignKey(PortfolioID, on_delete=models.CASCADE)
	tickerID = models.ForeignKey(stockID, on_delete=models.CASCADE)
