# Generated by Django 3.1.13 on 2022-11-30 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20221127_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='number',
            new_name='id',
        ),
    ]
