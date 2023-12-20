from django.urls import path, include
from .views import *

urlpatterns = [
    path('enroll', EnrollApiView.as_view(), name='enroll'), # enroll user ke course
    path('overview', DashboardOverviewApiView.as_view(), name='dashboard-overview'), # Ringkasan user
    path('course-info/<int:batch_id>', DashboardCourseInfoApiView.as_view(), name='course-info'), # Ringkasan course
    path('dashboard-class', DashboardEnrolledCourseApiView.as_view(), name='dashboard-class'), # List course yang diikutin user
    path('dashboard-notification', DashboardNotificationListApiView.as_view(), name='dashboard-notification'), # List notifikasi user dari semua course
    path('dashboard-assignment', DashboardAssignmentListApiView.as_view(), name='dashboard-assignment'), # List assignment user dari semua course
    path('dashboard-quiz', DashboardQuizListApiView.as_view(), name='dashboard-quiz'), # List quiz user dari semua course
    path('last-access', LastAccessApiView.as_view(), name='last-access'), # last access user dari semua course
    path('profile', DashboardEditProfileApiView.as_view(), name='profile'), # liat & edit profile user
    path('user-rating/<int:batch_id>', UserCourseRatingApiView.as_view(), name='user-rating'), # liat & edit rating user di suatu course
    path('online-session/<int:batch_id>', UserOnlineSessionListApiView.as_view(), name='online-session'), # liat sesi kelas di suatu course
    path('assignments/<int:batch_id>', UserAssignmentListApiView.as_view(), name='assignments'), # liat assignment di suatu course
    path('quizzes/<int:batch_id>', UserQuizListApiView.as_view(), name='quizes'), # liat quiz di suatu course
    path('accomplishment/<int:batch_id>', UserAccomplishmenOverviewApiView.as_view(), name='accomplishment'), # liat ringkasan pencapaian & nilai user di suatu course
    path('start-quiz', UserQuizStartApiView.as_view(), name='start-quiz'), # start quiz setiap user mau mencet mulai quiz
    path('quiz/<int:quiz_session_id>/<int:no>', UserQuizPerNumberApiView.as_view(), name='quiz-per-number'), # liat soal quiz per nomor
    path('answer-quiz', SubmitQuizPerNumberApiView.as_view(), name='answer-quiz'), # submit jawaban quiz per nomor
    path('finish-quiz', FinishQuizApiView.as_view(), name='submit-quiz'), # submit quiz di akhir
]