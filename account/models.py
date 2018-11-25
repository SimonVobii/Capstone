from django.db import models
from django.contrib.auth.models	import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class SurveyID(models.Model):
	surveyID = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	age = models.IntegerField()

	gender_CHOICES = (('M','Male'),('F','Female'),('N','Prefer not to specify'))
	gender = models.CharField(max_length=1, choices=gender_CHOICES, default='N')

	status_CHOICES = (('S','Student'),('W','Working'),('R','Retired'))
	status = models.CharField(max_length=1, choices=status_CHOICES, default='W')

	investment_CHOICES = (('H','I prefer higher reward and I am willing to tolerate higher risk'),('L','I prefer relatively stable although the potential reward will be lower as well'))
	investment = models.CharField(max_length=1, choices=investment_CHOICES, default='H')

	combination_CHOICES = (('S','Pure Stocks'),('B','Pure Bonds'),('M', 'Stocks and Bonds'))
	combination = models.CharField(max_length=1, choices=combination_CHOICES, default='M')


"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""