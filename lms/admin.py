from django.contrib import admin
from course.models import CourseBatch
from .models import CourseQuiz, CourseAssignment, CourseSession, QuizQuestion, QuizOption
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class QuizOptionInline(NestedStackedInline):
    model = QuizOption
    extra = 4
    max_num = 4
    exclude = ['id']

class QuizQuestionInline(NestedStackedInline):
    model = QuizQuestion
    extra = 1
    exclude = ['id']
    inlines = [
        QuizOptionInline
    ]

class CourseBatchQuizInline(NestedStackedInline):
    model = CourseQuiz
    extra = 1
    exclude = ['id']
    inlines = [
        QuizQuestionInline
    ]

class CourseBatchAssignmentInline(admin.StackedInline):
    model = CourseAssignment
    extra = 1
    exclude = ['id']

class CourseBatchSessionInline(admin.StackedInline):
    model = CourseSession
    extra = 1
    exclude = ['id']

class CourseBatchAdmin(NestedModelAdmin):
    inlines = [
        CourseBatchQuizInline,
        CourseBatchAssignmentInline,
        CourseBatchSessionInline
    ]
    exclude = ['id','created_at','updated_at', 'course']

admin.site.register(CourseBatch, CourseBatchAdmin)