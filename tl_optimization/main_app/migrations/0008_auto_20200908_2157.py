# Generated by Django 3.0.7 on 2020-09-08 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20200818_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='intersection',
            name='intersection_type',
            field=models.CharField(choices=[('Cross', 'Cross'), ('T-Up', 'T-Up'), ('T-Down', 'T-Down'), ('T-Left', 'T-Left'), ('T-Right', 'T-Right')], default='Cross', max_length=7),
        ),
        migrations.AddField(
            model_name='road',
            name='num_lanes',
            field=models.IntegerField(default=0),
        ),
    ]
