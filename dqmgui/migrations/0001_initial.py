# Generated by Django 2.1.7 on 2019-04-12 12:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certifier', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Histogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('histogram_type', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('entries', models.FloatField()),
                ('x_mean', models.FloatField()),
                ('x_rms', models.FloatField()),
                ('x_label', models.CharField(max_length=100)),
                ('x_min', models.FloatField()),
                ('x_max', models.FloatField()),
                ('bins_integral', models.FloatField()),
                ('content', models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('run_reconstruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certifier.RunReconstruction')),
            ],
        ),
    ]