from django.contrib import admin
from django.urls import path, include
from .views_api import *

urlpatterns = [
    path('', AllCourseApiView.as_view(), name='all-course'),
    path('teacher', AllTeacherApiView.as_view(), name='all-teacher'),
    path('teacher/<str:id>', TeacherDetailApiView.as_view(), name='teacher-detail'),
    path('prices/<str:id>', CoursePriceApiView.as_view(), name='course-price'),
    path('faq/<str:id>', CourseFaqApiView.as_view(), name='course-faq'),
    path('curriculum/<str:id>', CourseCurriculumApiView.as_view(), name='course-curriculum'),
    path('batch/<str:id>', CourseBatchApiView.as_view(), name='course-batch'),
    path('schedule/<str:id>', CourseScheduleApiView.as_view(), name='course-schedule'),
    path('testimony', ListTestimonyApiView.as_view(), name='all-testimony'),
    path('<str:id>', CourseOverviewApiView.as_view(), name='course-overview'),
]