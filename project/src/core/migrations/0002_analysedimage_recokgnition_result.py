# Generated by Django 2.0.6 on 2018-07-29 20:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysedimage',
            name='recokgnition_result',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
