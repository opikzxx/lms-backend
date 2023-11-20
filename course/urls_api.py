from django.contrib import admin
from django.urls import path, include
from .views_api import *

urlpatterns = [
    path('', ListCourseApiView.as_view(), name='ListCourseApiView'),
    path('teachers', ListTeacherApiView.as_view(), name='ListTeacherApiView'),
    path('teacher/<str:id>', ListDetailTeacherApiView.as_view(), name='ListDetailTeacherApiView'),
    path('<str:id>', ListDetailCourseApiView.as_view(), name='ListDetailCourseApiView'),
    path('prices/<str:id>', ListCoursePriceApiView.as_view(), name='ListCoursePriceApiView'),
    path('faq/<str:id>', ListCourseFaqApiView.as_view(), name='ListCourseFaqApiView'),
    path('curriculum/<str:id>', ListCourseCurriculumApiView.as_view(), name='ListCourseCurriculumApiView'),
    path('study-method/<str:id>', ListCourseStudyMethodApiView.as_view(), name='ListCourseStudyMethodApiView'),
    path('batch/<str:id>', ListCourseBatchApiView.as_view(), name='ListCourseBatchApiView'),
    path('schedule/<str:id>', ListCourseScheduleApiView.as_view(), name='ListCourseScheduleApiView'),
    path('testimony', ListTestimonyApiView.as_view(), name='ListTestimonyApiView'),
]