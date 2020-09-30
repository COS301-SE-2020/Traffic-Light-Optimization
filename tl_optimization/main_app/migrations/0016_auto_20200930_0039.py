# Generated by Django 3.1.1 on 2020-09-29 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_auto_20200920_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='intersection',
            name='view_settings',
            field=models.FileField(blank=True, null=True, upload_to='config/intersection/settings/'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_0',
            field=models.IntegerField(default=230),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_1',
            field=models.IntegerField(default=187),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_10',
            field=models.IntegerField(default=177),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_11',
            field=models.IntegerField(default=319),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_12',
            field=models.IntegerField(default=357),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_13',
            field=models.IntegerField(default=299),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_14',
            field=models.IntegerField(default=326),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_15',
            field=models.IntegerField(default=340),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_16',
            field=models.IntegerField(default=217),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_17',
            field=models.IntegerField(default=316),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_18',
            field=models.IntegerField(default=351),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_19',
            field=models.IntegerField(default=296),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_2',
            field=models.IntegerField(default=307),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_20',
            field=models.IntegerField(default=363),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_21',
            field=models.IntegerField(default=174),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_22',
            field=models.IntegerField(default=341),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_23',
            field=models.IntegerField(default=237),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_3',
            field=models.IntegerField(default=158),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_4',
            field=models.IntegerField(default=276),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_5',
            field=models.IntegerField(default=238),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_6',
            field=models.IntegerField(default=300),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_7',
            field=models.IntegerField(default=167),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_8',
            field=models.IntegerField(default=304),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='hour_9',
            field=models.IntegerField(default=215),
        ),
    ]