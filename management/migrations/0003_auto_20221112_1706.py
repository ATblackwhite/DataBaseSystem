# Generated by Django 3.1.13 on 2022-11-12 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20221112_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attend',
            old_name='number',
            new_name='club',
        ),
    ]
