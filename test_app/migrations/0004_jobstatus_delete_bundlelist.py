# Generated by Django 5.0.1 on 2024-03-07 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_remove_jobgroup_is_finished_bundlelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.yourlist')),
            ],
        ),
        migrations.DeleteModel(
            name='BundleList',
        ),
    ]
