from django.contrib import admin
from django.urls import path, include
from .views_api import ListTeacherApiView, ListCourseApiView, ListContentApiView, ListDetailTeacherApiView, ListDetailCourseApiView, ListDetailContentApiView, ListCoursePriceApiView, ListCourseFaqApiView, ListCourseCurriculumApiView, ListCourseStudyMethodApiView, ListCourseBatchApiView, ListCourseScheduleApiView, ListTestimonyApiView

urlpatterns = [
    path('', ListCourseApiView.as_view(), name='ListCourseApiView'),
    path('teachers', ListTeacherApiView.as_view(), name='ListTeacherApiView'),
    path('teacher-list/<int:id>', ListDetailTeacherApiView.as_view(), name='ListDetailTeacherApiView'),
    path('course-list/<int:id>', ListDetailCourseApiView.as_view(), name='ListDetailCourseApiView'),
    path('content-list', ListContentApiView.as_view(), name='ListContentApiView'),
    path('content-list/<int:id>', ListDetailContentApiView.as_view(), name='ListDetailContentApiView'),
    path('prices/<str:id>', ListCoursePriceApiView.as_view(), name='ListCoursePriceApiView'),
    path('faq/<str:id>', ListCourseFaqApiView.as_view(), name='ListCourseFaqApiView'),
    path('curriculum/<str:id>', ListCourseCurriculumApiView.as_view(), name='ListCourseCurriculumApiView'),
    path('study-method/<str:id>', ListCourseStudyMethodApiView.as_view(), name='ListCourseStudyMethodApiView'),
    path('batch/<str:id>', ListCourseBatchApiView.as_view(), name='ListCourseBatchApiView'),
    path('schedule/<str:id>', ListCourseScheduleApiView.as_view(), name='ListCourseScheduleApiView'),
    path('testimony', ListTestimonyApiView.as_view(), name='ListTestimonyApiView'),
]