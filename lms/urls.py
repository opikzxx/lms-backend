from django.urls import path, include
from .views import *

urlpatterns = [
    path('overview', DashboardOverviewApiView.as_view(), name='dashboard-overview'),
    path('class', DashboardEnrolledCourseApiView.as_view(), name='dashboard-class'),
    path('notification', DashboardNotificationListApiView.as_view(), name='dashboard-notification'),
    path('assignment', DashboardAssignmentListApiView.as_view(), name='dashboard-assignment'),
    path('quiz', DashboardQuizListApiView.as_view(), name='dashboard-quiz'),
    path('profile', DashboardEditProfileApiView.as_view(), name='profile'),
    path('user-rating/<int:batch_id>', UserCourseRatingApiView.as_view(), name='user-rating'),
    path('online-session/<int:batch_id>', UserOnlineSessionListApiView.as_view(), name='online-session'),
    path('assignments/<int:batch_id>', UserAssignmentListApiView.as_view(), name='assignments'),
    path('quizzes/<int:batch_id>', UserQuizListApiView.as_view(), name='quizes'),
    path('tes/<int:batch_id>', UserAccomplishmenOverviewApiView.as_view(), name='tes')
]