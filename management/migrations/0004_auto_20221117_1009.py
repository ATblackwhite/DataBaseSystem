# Generated by Django 3.1.13 on 2022-11-17 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20221112_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendDate', models.DateTimeField()),
                ('confirm', models.BooleanField(default=False, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.club')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='management.member')),
            ],
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='activityLocation',
            new_name='Location',
        ),
        migrations.DeleteModel(
            name='Attend',
        ),
    ]