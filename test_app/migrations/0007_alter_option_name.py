# Generated by Django 5.0.1 on 2024-03-11 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0006_alter_elementlib_name_alter_timestudy_elements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]