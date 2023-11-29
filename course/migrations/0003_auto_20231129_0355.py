# Generated by Django 3.2 on 2023-11-29 03:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20231123_0751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursestudymethod',
            name='course',
        ),
        migrations.AddField(
            model_name='coursebatch',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursefaq',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursebatch',
            name='close_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='coursebatch',
            name='open_date',
            field=models.DateField(null=True),
        ),
        migrations.DeleteModel(
            name='CourseContent',
        ),
        migrations.DeleteModel(
            name='CourseStudyMethod',
        ),
    ]
