# Generated by Django 2.2 on 2019-05-07 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_common', '0009_costusagereportstatus_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costusagereportstatus',
            name='history',
        ),
    ]