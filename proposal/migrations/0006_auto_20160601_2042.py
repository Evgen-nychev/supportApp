# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-01 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0005_auto_20160521_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfugurationOneC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name_plural': 'Конфигурации 1С',
                'verbose_name': 'Конфигурацию 1С',
            },
        ),
        migrations.AlterField(
            model_name='spec',
            name='support_rec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.SupportRecuest'),
        ),
        migrations.AddField(
            model_name='otdel',
            name='configuration_1c',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposal.ConfugurationOneC'),
        ),
        migrations.AddField(
            model_name='supportrecuest',
            name='configuration_1c',
            field=models.ManyToManyField(blank=True, to='proposal.ConfugurationOneC'),
        ),
        migrations.AddField(
            model_name='tema',
            name='configuration_1c',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposal.ConfugurationOneC'),
        ),
    ]
