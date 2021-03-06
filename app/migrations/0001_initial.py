# Generated by Django 3.1.7 on 2021-02-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('type', models.CharField(max_length=200)),
                ('continent_code', models.CharField(max_length=200)),
                ('continent_name', models.CharField(max_length=200)),
                ('country_code', models.CharField(max_length=200)),
                ('country_name', models.CharField(max_length=200)),
                ('region_code', models.CharField(max_length=200)),
                ('region_name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('zip', models.PositiveIntegerField()),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('location', models.JSONField()),
            ],
        ),
    ]
