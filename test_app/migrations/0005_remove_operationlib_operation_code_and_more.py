# Generated by Django 5.0.1 on 2024-02-06 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0004_remove_operationlistitem_expanding_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationlib',
            name='operation_code',
        ),
        migrations.AddField(
            model_name='operationlistitem',
            name='expanding_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='test_app.operationcode'),
        ),
    ]
