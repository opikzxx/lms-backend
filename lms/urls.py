from django.urls import path, include
from .views import *

urlpatterns = [
    path('overview', DashboardOverviewApiView.as_view(), name='dashboard-overview'),
    path('dashboard-class', DashboardEnrolledCourseApiView.as_view(), name='dashboard-class'),
    path('dashboard-notification', DashboardNotificationListApiView.as_view(), name='dashboard-notification'),
    path('dashboard-assignment', DashboardAssignmentListApiView.as_view(), name='dashboard-assignment'),
    path('dashboard-quiz', DashboardQuizListApiView.as_view(), name='dashboard-quiz'),
    path('profile', DashboardEditProfileApiView.as_view(), name='profile'),
    path('user-rating/<int:batch_id>', UserCourseRatingApiView.as_view(), name='user-rating'),
    path('online-session/<int:batch_id>', UserOnlineSessionListApiView.as_view(), name='online-session'),
    path('assignments/<int:batch_id>', UserAssignmentListApiView.as_view(), name='assignments'),
    path('quizzes/<int:batch_id>', UserQuizListApiView.as_view(), name='quizes'),
    path('accomplishment/<int:batch_id>', UserAccomplishmenOverviewApiView.as_view(), name='accomplishment'),
    path('start-quiz', UserQuizStartApiView.as_view(), name='start-quiz'),
    path('quiz/<int:quiz_session_id>/<int:no>', UserQuizPerNumberApiView.as_view(), name='quiz-per-number'),
    path('answer-quiz', SubmitQuizPerNumberApiView.as_view(), name='answer-quiz'),
    path('finish-quiz', FinishQuizApiView.as_view(), name='submit-quiz'),
]