# Generated by Django 3.1.13 on 2022-11-30 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_auto_20221130_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.club'),
        ),
        migrations.AlterField(
            model_name='attend',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.activity'),
        ),
        migrations.AlterField(
            model_name='attend',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.member'),
        ),
        migrations.AlterField(
            model_name='club',
            name='principal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.member'),
        ),
        migrations.AlterField(
            model_name='join',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.club'),
        ),
        migrations.AlterField(
            model_name='join',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.member'),
        ),
    ]
