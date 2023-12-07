from django.shortcuts import render
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from lms.wrapper import validate_enrollment
from .models import *
from authentication.models import User
from .serializers import *

from datetime import datetime
from django.db.models import Avg

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from library.helper.interface import response

# Buat ringkasan di dashboard, meliputi course yang diikuti, daftar tugas, notif, dll
class DashboardOverviewApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)

        course_batch_ids = [enrollment.course_batch.id for enrollment in enrollments]
        course_batchs = CourseBatch.objects.filter(id__in=course_batch_ids).order_by('end_date')[:4]
        courses = CourseBatchModelSerializer(course_batchs, many=True)

        course_assignments = CourseAssignment.objects.filter(course_batch__in=course_batch_ids).order_by('deadline')
        course_assignment_ids = [course_assignment.id for course_assignment in course_assignments]
        
        user_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='BS').order_by('assignment__deadline')[:2]
        assignment = UserAssignmentModelSerializer(user_assignments, many=True)

        course_quizs = CourseQuiz.objects.filter(course_batch__in=course_batch_ids).order_by('deadline')
        course_quiz_not_finished = course_quizs.exclude(quizuser__user=user)[:2]
        quiz = CourseQuizModelSerializer(course_quiz_not_finished, many=True)

        last_access = LastAccess.objects.filter(user=user)

        data = {
            'enrollment_list' : courses.data,
            'assignment_list' : assignment.data,
            'quiz_list' : quiz.data,
            'last_access' : last_access.course_batch.id if last_access else None
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Nampilin course yang diikutin
class DashboardEnrolledCourseApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)

        course_batch_ids = [enrollment.course_batch.id for enrollment in enrollments]
        course_batchs = CourseBatch.objects.filter(id__in=course_batch_ids)

        program = request.GET.get('program')

        if program:
            course_batchs = course_batchs.filter(course__program__slug=program)

        courses = CourseBatchModelSerializer(course_batchs, many=True)

        data = {
            'enrollment_list' : courses.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Nampilin notifikasi si user
class DashboardNotificationListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)
        course_batch_ids = [enrollment.course_batch.id for enrollment in enrollments]
        
        # ambil data dari assignment_attachment, course_quiz, course_session
        course_assignments = CourseAssignment.objects.filter(course_batch__in=course_batch_ids).order_by('deadline')
        course_assignment_ids = [course_assignment.id for course_assignment in course_assignments]
        
        user_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='RV').order_by('assignment__deadline')
        assignment = UserAssignmentModelSerializer(user_assignments, many=True)

        course_quiz = CourseQuiz.objects.filter(Q(course_batch__in=course_batch_ids), Q(deadline__gt=datetime.now()))
        quiz = CourseQuizModelSerializer(course_quiz, many=True)

        course_session = CourseSession.objects.filter(Q(course_batch__in=course_batch_ids), Q(time__gt=datetime.now()))
        session = CourseSessionModelSerializer(course_session, many=True)

        data = {
            'assignment_list': assignment.data,
            'quiz_list': quiz.data,
            'session_list': session.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Nampilin semua tugas si user
class DashboardAssignmentListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)

        course_batch_ids = [enrollment.course_batch.id for enrollment in enrollments]

        course_assignments = CourseAssignment.objects.filter(course_batch__in=course_batch_ids).order_by('deadline')
        course_assignment_ids = [course_assignment.id for course_assignment in course_assignments]
        
        user_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='BS').order_by('assignment__deadline')
        assignment = UserAssignmentModelSerializer(user_assignments, many=True)

        data = {
            'assignment_list': assignment.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Nampilin quiz yang belum dikerjain
class DashboardQuizListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)

        course_batch_ids = [enrollment.course_batch.id for enrollment in enrollments]

        course_quizs = CourseQuiz.objects.filter(course_batch__in=course_batch_ids).order_by('deadline')
        course_quiz_not_finished = course_quizs.exclude(quizuser__user=user)
        quiz = CourseQuizModelSerializer(course_quiz_not_finished, many=True)

        data = {
            'quiz_list': quiz.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Nampilin semua transaksi si user
class DashboardTransactionListApiVew(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        pass

# Edit profil si user
class DashboardEditProfileApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        
        User = get_user_model()
        data = User.objects.filter(email=user.email)
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        user = request.user
        body = request.body
        
        User = get_user_model()
        data = User.objects.filter(email=user.email).update(**body)
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# ------------------Detail Enrolled Course------------------

# Nampilin ringkasan pengerjaan user di course itu
class UserAccomplishmenOverviewApiView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(validate_enrollment())
    def get(self, request, batch_id, enrollment, **kwargs):
        user = request.user
        course_batch = CourseBatch.objects.get(id=batch_id)
        AssignmentAttachment.objects.filter()

        course_assignments = CourseAssignment.objects.filter(course_batch=course_batch)
        course_assignment_ids = [course_assignment.id for course_assignment in course_assignments]
        
        count_finished_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='SL').count()
        average_grade_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='SL').aggregate(Avg('score'))['score__avg']

        data = {
            'count_finished_assignments': count_finished_assignments,
            'average_grade_assignments': average_grade_assignments
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Bikin get & post rating si user
class UserCourseRatingApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(validate_enrollment())
    def get(self, request, batch_id, enrollment, **kwargs):
        rating = UserRatingSerializer(enrollment)

        data = {
            'user_rating' : rating.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)
        
class UserOnlineSessionListApiView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(validate_enrollment())
    def get(self, request, batch_id, **kwargs):
        course_sessions = CourseSession.objects.filter(course_batch__id=batch_id).order_by('ordering')

        course_sessions_serializer = CourseSessionModelSerializer(course_sessions, many=True)

        data = {
            'online_session' : course_sessions_serializer.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

class UserAssignmentListApiView(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(validate_enrollment())
    def get(self, request, batch_id, **kwargs):
        course_assignments = CourseAssignment.objects.filter(course_batch__id=batch_id).order_by('ordering')
        course_assignment_ids = [assignment.id for assignment in course_assignments]
        assignment_attachment = AssignmentAttachment.objects.filter(assignment__id__in=course_assignment_ids)

        user_assignments_serializer = UserAssignmentModelSerializer(assignment_attachment, many=True)

        data = {
            'user_assignments' : user_assignments_serializer.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

class UserQuizListApiView(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(validate_enrollment())
    def get(self, request, batch_id, **kwargs):
        course_quizzes = CourseQuiz.objects.filter(course_batch__id=batch_id).order_by('ordering')
        course_quiz_ids = [course_quiz.id for course_quiz in course_quizzes]
        user_quizzes = QuizUser.objects.filter(quiz__id__in=course_quiz_ids)

        user_quizzes_serializer = QuizUserModelSerializer(user_quizzes, many=True)
        
        data = {
            'user_quizzes' : user_quizzes_serializer.data
        }
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# ------------------Api yang dibutuhin di tugas ------------------

# Liat, submit, ama replace tugas
class UserAssignmentAttachmentApiView(APIView):
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