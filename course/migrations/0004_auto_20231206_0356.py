# Generated by Django 3.2 on 2023-12-06 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20231201_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseprice',
            name='benefits',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseprice',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
