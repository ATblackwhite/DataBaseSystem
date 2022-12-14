# Generated by Django 3.1.13 on 2022-11-11 22:30

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('memberNumber', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('age', models.IntegerField(blank=True)),
                ('sex', models.CharField(max_length=5)),
                ('passwd', models.CharField(default=None, max_length=20)),
                ('session', models.UUIDField(default=uuid.uuid4, null=True)),
                ('level', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('clubNumber', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('principal', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.member')),
            ],
        ),
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendDate', models.DateTimeField(default=datetime.date.today)),
                ('confirm', models.BooleanField(default=False, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.member')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.club')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('number', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('activityLocation', models.CharField(max_length=20)),
                ('dateTime', models.DateTimeField(default=None)),
                ('memberNumber', models.IntegerField(default=0)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.club')),
                ('principal', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.member')),
            ],
        ),
    ]
