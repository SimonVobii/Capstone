# Generated by Django 2.1.2 on 2018-11-25 21:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20181118_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfoliohistory',
            name='dateID',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='portfolioid',
            name='goalValue',
            field=models.FloatField(default=0.05),
        ),
        migrations.AddField(
            model_name='portfolioid',
            name='timeHorizon',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='portfolioweights',
            name='volume',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='assetPrice',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='assetReturn',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='dateID',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='stockid',
            name='ipoDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name='portfolioweights',
            unique_together={('tickerID', 'portfolioID')},
        ),
        migrations.AlterUniqueTogether(
            name='stockhistory',
            unique_together={('tickerID', 'dateID')},
        ),
    ]
