# Generated by Django 3.1.13 on 2022-11-17 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20221117_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='maxNumber',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.activity')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.member')),
            ],
        ),
    ]