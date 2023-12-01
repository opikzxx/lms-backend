# Generated by Django 3.2 on 2023-12-01 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0003_auto_20231201_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseQuiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('duration', models.IntegerField(default=10)),
                ('minimum_score', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('Accessibility', models.CharField(choices=[('OP', 'Open'), ('CL', 'Closed')], default='OP', max_length=2)),
                ('status', models.CharField(choices=[('DR', 'Draft'), ('FN', 'Final')], default='DR', max_length=2)),
                ('ordering', models.IntegerField(null=True)),
                ('deadline', models.DateTimeField()),
                ('course_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursebatch')),
            ],
        ),
        migrations.CreateModel(
            name='QuizOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('ordering', models.IntegerField()),
                ('course_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.coursequiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('correct_answer', models.IntegerField(null=True)),
                ('question_order', models.TextField()),
                ('target_time', models.DateTimeField()),
                ('completion_time', models.DateTimeField(null=True)),
                ('is_remedial', models.BooleanField(default=False)),
                ('attempt', models.IntegerField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.coursequiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizUserAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lms.quizoption')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.quizquestion')),
                ('quiz_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.quizuser')),
            ],
        ),
        migrations.AddField(
            model_name='quizoption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.quizquestion'),
        ),
        migrations.CreateModel(
            name='LastAccess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('last_access', models.DateTimeField(null=True)),
                ('course_batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursebatch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('enrollment_type', models.CharField(choices=[('BL', 'Belajar'), ('SR', 'Sertifikasi')], default='BL', max_length=2)),
                ('rating', models.IntegerField(null=True)),
                ('ratingDetail', models.TextField(null=True)),
                ('finalScore', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('certificateUrl', models.CharField(max_length=255, null=True)),
                ('course_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursebatch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('meeting_link', models.TextField(null=True)),
                ('record_link', models.TextField(null=True)),
                ('lesson_link', models.TextField(null=True)),
                ('ordering', models.IntegerField()),
                ('course_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursebatch')),
            ],
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('file', models.CharField(max_length=128, null=True)),
                ('accesibility', models.CharField(choices=[('OP', 'Open'), ('CL', 'Closed')], default='OP', max_length=2)),
                ('ordering', models.IntegerField()),
                ('deadline', models.DateTimeField()),
                ('course_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursebatch')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('BS', 'Belum Submit'), ('RV', 'Review'), ('SL', 'Selesai')], default='BS', max_length=255)),
                ('feedback', models.TextField(null=True)),
                ('submitted_date', models.DateTimeField(null=True)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('file', models.CharField(max_length=64, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.courseassignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
