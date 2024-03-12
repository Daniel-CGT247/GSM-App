# Generated by Django 5.0.1 on 2024-03-11 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0004_jobstatus_delete_bundlelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobstatus',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_status', to='test_app.yourlist'),
        ),
    ]
