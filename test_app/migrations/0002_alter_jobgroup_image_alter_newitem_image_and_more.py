# Generated by Django 5.0.1 on 2024-02-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobgroup',
            name='image',
            field=models.ImageField(upload_to='job-icon/'),
        ),
        migrations.AlterField(
            model_name='newitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='newItems/'),
        ),
        migrations.AlterUniqueTogether(
            name='newitem',
            unique_together={('name', 'season', 'proto')},
        ),
    ]