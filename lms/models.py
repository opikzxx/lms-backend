from django.db import models
from django.contrib.auth.models import User
from course.models import CourseBatch
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Enrollment(models.Model):
    class EnrollmentType(models.TextChoices):
        BELAJAR = "BL", _('Belajar')
        SERTIFIKASI = "SR", _('Sertifikasi')
    
    id = models.AutoField(primary_key=True)
    course_batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrollment_type = models.CharField(
        max_length=2,
        choices=EnrollmentType.choices,
        default=EnrollmentType.BELAJAR,
    )
    rating = models.IntegerField()
    ratingDetail = models.TextField()
    finalScore = models.DecimalField(max_digits=3, decimal_places=2)
    certificateUrl = models.CharField(max_length=255)

class CourseAssignment(models.Model):
    class Accessibility(models.TextChoices):
        OPEN = 'OP', _('Open')
        CLOSED = 'CL', _('Closed')

    id = models.AutoField(primary_key=True)
    course_batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.CharField(max_length=128)
    accesibility = models.CharField(
        max_length=2, 
        choices=Accessibility.choices,
        default=Accessibility.OPEN
    )
    ordering = models.IntegerField()
    deadline = models.DateTimeField()

class AssignmentAttachment(models.Model):
    class Status(models.TextChoices):
        BELUM_SUBMIT = 'BS', _('Belum Submit')
        REVIEW = 'RV', _('Review')
        SELESAI = 'SL', _('Selesai')

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255, 
        choices=Status.choices,
        default=Status.BELUM_SUBMIT
    )
    feedback = models.TextField()
    submitted_date = models.DateTimeField()
    score = models.DecimalField(max_digits=3, decimal_places=2)
    file = models.CharField(max_length=64)

class CourseQuiz(models.Model):
    class Accessibility(models.TextChoices):
        OPEN = 'OP', _('Open')
        CLOSED = 'CL', _('Closed')

    class Status(models.TextChoices):
        DRAFT = 'DR', _('Draft')
        FINAL = 'FN', _('Final')

    id = models.AutoField(primary_key=True)
    course_batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    minimum_score = models.DecimalField(max_digits=3, decimal_places=2)
    Accessibility = models.CharField(
        max_length=2, 
        choices=Accessibility.choices,
        default=Accessibility.OPEN
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    ordering = models.IntegerField()
    deadline = models.DateTimeField()

class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    ordering = models.IntegerField()

class QuizOption(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    value = models.TextField()
    is_correct = models.BooleanField()

class QuizUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(CourseQuiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=3, decimal_places=2)
    correct_answer = models.IntegerField()
    question_order = models.TextField()
    target_time = models.DateTimeField()
    completion_time = models.DateTimeField()
    is_remedial = models.BooleanField()
    attempt = models.IntegerField()

class QuizUserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(QuizOption, on_delete=models.CASCADE)

class CourseSession(models.Model):
    id = models.AutoField(primary_key=True)
    course_batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time = models.DateTimeField()
    meeting_link = models.TextField()
    record_link = models.TextField()
    lesson_link = models.TextField()
    ordering = models.IntegerField()

class LastAccess(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE)
    last_access = models.DateTimeField()