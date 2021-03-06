# Generated by Django 3.0.7 on 2020-07-16 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20200614_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='intersection',
            old_name='name',
            new_name='intersection_name',
        ),
        migrations.RenameField(
            model_name='road',
            old_name='name',
            new_name='road_name',
        ),
        migrations.RemoveField(
            model_name='road',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='road',
            name='traffic',
        ),
        migrations.AddField(
            model_name='road',
            name='road_distance',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='TrafficLight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timing_red', models.IntegerField(default=0)),
                ('timing_yellow', models.IntegerField(default=0)),
                ('timing_green', models.IntegerField(default=0)),
                ('intersection_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Intersection')),
            ],
        ),
        migrations.AddField(
            model_name='intersection',
            name='network_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Network'),
        ),
        migrations.AddField(
            model_name='road',
            name='trafficlight_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.TrafficLight'),
        ),
    ]
