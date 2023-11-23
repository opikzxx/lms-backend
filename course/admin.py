from django.contrib import admin
from .models import Course, CourseContent, Teacher, Program, CourseDetail, CoursePrice, CourseStudyMethod, CourseCurriculum, CourseSchedule, CourseBatch,CourseFaq, Testimony

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at','profileImageUrl','companyImageUrl']

class CoursePriceInline(admin.TabularInline):
    model = CoursePrice
    exclude = ['id','created_at','updated_at']

class CourseCurriculumInline(admin.TabularInline):
    model = CourseCurriculum
    exclude = ['id']

class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    exclude = ['id']

class CourseStudyMethodInline(admin.TabularInline):
    model = CourseStudyMethod.course.through
    extra = 1

class CourseBatchInline(admin.TabularInline):
    model = CourseBatch
    exclude = ['id']

class CourseFaqInline(admin.TabularInline):
    model = CourseFaq
    exclude = ['id']

class CourseDetailInline(admin.TabularInline):
    model = CourseDetail

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseDetailInline,
        CourseScheduleInline, 
        CourseCurriculumInline, 
        CourseBatchInline,
        CourseFaqInline,
        CoursePriceInline,
        ]
    exclude = ['id','created_at','updated_at', 'image_url']

class CourseContentAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class ProgramAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CourseDetailAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CoursePriceAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CourseStudyMethodAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CourseCurriculumAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CourseScheduleAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CourseBatchAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class CourseFaqAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

class TestimonyAdmin(admin.ModelAdmin):
    exclude = ['id','created_at','updated_at']

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(CourseContent, CourseContentAdmin)
admin.site.register(Program, ProgramAdmin)
# admin.site.register(CourseDetail, CourseDetailAdmin)
# admin.site.register(CoursePrice, CoursePriceAdmin)
admin.site.register(CourseStudyMethod, CourseStudyMethodAdmin)
# admin.site.register(CourseCurriculum, CourseCurriculumAdmin)
# admin.site.register(CourseSchedule, CourseScheduleAdmin)
# admin.site.register(CourseBatch, CourseBatchAdmin)
# admin.site.register(CourseFaq, CourseFaqAdmin)
admin.site.register(Testimony, TestimonyAdmin)