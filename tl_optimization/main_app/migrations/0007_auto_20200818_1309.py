# Generated by Django 3.0.7 on 2020-08-18 11:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20200727_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='road',
            name='trafficlight_id',
        ),
        migrations.RemoveField(
            model_name='trafficlight',
            name='intersection_id',
        ),
        migrations.AddField(
            model_name='road',
            name='position',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='trafficlight',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='trafficlight',
            name='road_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Road'),
        ),
        migrations.AddField(
            model_name='trafficlight',
            name='traffic_count',
            field=models.FloatField(default=0),
        ),
    ]
