# Generated by Django 5.0.1 on 2024-03-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlistitem',
            name='expanding_name',
            field=models.CharField(blank=True, default='N/A', max_length=500, null=True),
        ),
    ]