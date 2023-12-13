from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid, datetime

# Create your models here.
class Program(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=64, null=False)
    slug = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'program'
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

class Teacher(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=128, blank=True, null=False)
    occupation = models.CharField(max_length=50, null=False)
    experience = models.IntegerField(null=False)
    linkedinUrl = models.CharField(max_length=128, blank=True, null=True)
    profileImageUrl = models.ImageField(upload_to='cms-xpert/teacher_profile/', null=True)
    companyImageUrl = models.ImageField(upload_to='cms-xpert/teacher_profile_comapny/', null=True)
    isShownAtHomepage = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

class XpertOverview(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    peserta_tergabung = models.IntegerField(null=False)
    peserta_tersertifikasi = models.IntegerField(null=False)
    kelas_online = models.IntegerField(null=False)
    kegiatan_inhouse = models.IntegerField(null=False)

class Course(models.Model):
    class Status(models.TextChoices):
        COMING_SOON = 'CS', _('Coming Soon')
        AVAILABLE = 'AV', _('Available')
        ON_GOING = 'OG', _('On Going')
        FINISHED = 'FI', _('Finished')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=128, null=False)
    description = models.TextField(null=False)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.COMING_SOON,
        null=False
    )
    participant_amount = models.IntegerField(default=0)
    certified_participant_amount = models.IntegerField(default=0)
    image_url = models.ImageField(upload_to='eureka-xpert/images/', null=True)
    teacher = models.ManyToManyField(Teacher)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class CourseDetail(models.Model):

    id = models.OneToOneField(Course, on_delete=models.CASCADE, null=False, primary_key=True)
    course_overview = models.TextField(null=False)
    reason = models.JSONField(null=False)
    result = models.JSONField(null=False)
    skill = models.TextField(null=False)

    def __str__(self):
        return self.course_overview
    
    class Meta:
        db_table = 'course_detail'
        verbose_name = 'Course Detail'
        verbose_name_plural = 'Course Details'

class CoursePrice(models.Model):
    class Type(models.TextChoices):
        BELAJAR = 'BL', _('Belajar')
        SERTIFIKASI = 'SR', _('Sertifikasi')

    id = models.AutoField(primary_key=True,null=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    description = models.TextField(null=False)
    original_price = models.IntegerField(null=False)
    discounted_price = models.IntegerField(null=False)
    discount_percentage = models.IntegerField(null=False)
    benefits = models.JSONField(null=False)
    type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.BELAJAR,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'course_price'
        verbose_name = 'Course Price'
        verbose_name_plural = 'Course Prices'

class CourseCurriculum(models.Model):

    id = models.AutoField(primary_key=True, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=50, null=False)
    detail = models.TextField(null=False)
    # file = models.FileField(upload_to='cms-xpert/course_curriculum/', null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'course_curriculum'
        verbose_name = 'Course Curriculum'
        verbose_name_plural = 'Course Curriculums'

class CourseSchedule(models.Model):

    id = models.AutoField(primary_key=True, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    starting_week = models.IntegerField(null=False)
    ending_week = models.IntegerField(null=False)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'course_schedule'
        verbose_name = 'Course Schedule'
        verbose_name_plural = 'Course Schedules'

class CourseBatch(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AV', _('Available')
        SOLD_OUT = 'SO', _('Sold Out')

    id = models.AutoField(primary_key=True, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    open_date = models.DateField(null=True)
    close_date = models.DateField(null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.AVAILABLE,
        null=False
    )
    no = models.IntegerField()
    isShownAtHomepage = models.BooleanField(default=False)
    isSoldOut = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'course_batch'
        verbose_name = 'Course Batch'
        verbose_name_plural = 'Course Batches'

class CourseFaq(models.Model):

    id = models.AutoField(primary_key=True, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    question = models.CharField(max_length=128, null=False)
    answer = models.TextField(null=False)
    order = models.IntegerField()

    def __str__(self):
        return self.question
    
    class Meta:
        db_table = 'course_faq'
        verbose_name = 'Course Faq'
        verbose_name_plural = 'Course Faqs'

class Testimony(models.Model):
    
    id = models.AutoField(primary_key=True, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50, null=False)
    occupation = models.CharField(max_length=50, null=True)
    desciption = models.TextField(null=False)
    image_url = models.ImageField(upload_to='cms-xpert/testimony/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'testimony'
        verbose_name = 'Testimony'
        verbose_name_plural = 'Testimonies'