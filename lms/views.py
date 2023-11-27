from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from library.helper.interface import response

# Buat ringkasan di dashboard, meliputi course yang diikuti, daftar tugas, notif, dll
class DashboardOverviewApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)

        course_batch_ids = [enrollment.course_batch for enrollment in enrollments]
        course_batchs = CourseBatch.objects.filter(id__in=course_batch_ids)

        # get assignments for the user
        course_assignments = CourseAssignment.objects.filter(course_batch__in=course_batch_ids)
        course_assignment_ids = [course_assignment.id for course_assignment in course_assignments]
        user_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids)

        course_quizs = CourseQuiz.objects.filter(course_batch__in=course_batch_ids)
        course_quiz_ids = [course_quiz.id for course_quiz in course_quizs]
        user_quizs = QuizUser.objects.filter(user=user, quiz__in=course_quiz_ids)

        last_access = LastAccess.objects.filter(user=user, course_batch__in=course_batch_ids).order_by('-last_access').first()

        data = {
            course_batchs : course_batchs,
            user_assignments : user_assignments,
            user_quizs : user_quizs,
            last_access : last_access
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Nampilin course yang diikutin
class DashboardEnrolledCourseApiView(APIView):
    def get(self, request, **kwargs):
        pass

# Nampilin notifikasi si user
class DashboardNotificationListApiView(APIView):
    def get(self, request, **kwargs):
        pass

# Nampilin semua tugas si user
class DashboardAssignmentListApiView(APIView):
    def get(self, request, **kwargs):
        pass

# Nampilin quiz yang belum dikerjain
class DashboardQuizListApiView(APIView):
    def get(self, request, **kwargs):
        pass

# Nampilin semua transaksi si user
class DashboardTransactionListApiVew(APIView):
    def get(self, request, **kwargs):
        pass

# Edit profil si user
class DashboardEditProfileApiView(APIView):
    def get(self, request, **kwargs):
        pass

# ------------------Detail Enrolled Course------------------

# Nampilin ringkasan pengerjaan user di course itu
class UserAccomplishmenOverviewApiView(APIView):
    def get(self, request, **kwargs):
        pass

# Bikin get & post rating si user
class UserCourseRatingApiView(APIView):
    def get(self, request, **kwargs):
        pass
        
class UserOnlineSessionListApiView(APIView):
    def get(self, request, **kwargs):
        pass

class UserAssignmentListApiView(APIView):
    def get(self, request, **kwargs):
        pass

class UserQuizListApiView(APIView):
    def get(self, request, **kwargs):
        pass

# ------------------Api yang dibutuhin di tugas ------------------

# Liat, submit, ama replace tugas
class UserAssignmentApiView(APIView):
    def get(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        pass

    def delete(self, request, **kwargs):
        pass

# ------------------Api yang dibutuhin di quiz ------------------

# Mulai quiz
class UserQuizStartApiView(APIView):
    def post(self, request, **kwargs):
        pass

# Liat, submit pertanyaan quiz per nomor
class UserQuizPerNumberApiView(APIView):
    def get(self, request, question_id, no, **kwargs):
        pass

    def post(self, request, **kwargs):
        pass

# Liat review quiz, bener & salahnya 
class UserQuizReviewApiView(APIView):
    def get(self, request, **kwargs):
        pass