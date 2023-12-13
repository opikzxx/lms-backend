from django.shortcuts import render
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from library.helper.wrapper import validate_serializer

from lms.wrapper import validate_enrollment
from .models import *
from authentication.models import User
from .serializers import *

from datetime import datetime, timedelta
from django.db.models import Avg

from django.utils import timezone

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from library.helper.interface import response

from decimal import Decimal

import random

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

        course_quiz = CourseQuiz.objects.filter(Q(course_batch__in=course_batch_ids), Q(deadline__gt=timezone.now()))
        quiz = CourseQuizModelSerializer(course_quiz, many=True)

        course_session = CourseSession.objects.filter(Q(course_batch__in=course_batch_ids), Q(time__gt=timezone.now()))
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

        course_assignments = CourseAssignment.objects.filter(course_batch=course_batch)
        course_assignment_ids = [course_assignment.id for course_assignment in course_assignments]
        
        count_finished_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='SL').count()
        average_grade_assignments = AssignmentAttachment.objects.filter(user=user, assignment__in=course_assignment_ids, status='SL').aggregate(Avg('score'))['score__avg']

        course_quizzes = CourseQuiz.objects.filter(course_batch=course_batch)
        course_quiz_ids = [course_quiz.id for course_quiz in course_quizzes]
        user_quizzes = QuizUser.objects.filter(user=user, quiz__id__in=course_quiz_ids)

        data = {
            'total_assignments': len(course_assignments),
            'finished_assignments': count_finished_assignments,
            'average_grade_assignments': average_grade_assignments,
            'total_quizzes': len(course_quizzes),
            'quiz_user': user_quizzes
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
    permission_classes = [IsAuthenticated]

    @method_decorator(validate_serializer(QuizDTO))
    def post(self, request, data, **kwargs):
        user = request.user
        course_quiz = CourseQuiz.objects.get(id=data['quiz_id'])

        enrollments = Enrollment.objects.filter(user=user, course_batch=course_quiz.course_batch)
        if len(enrollments) == 0:
            return Response(response(403, "User has no access to the course", None, "Not Enrolled to the course"), status=status.HTTP_403_FORBIDDEN)
        
        ongoing_quiz = QuizUser.objects.filter(user=user, quiz=course_quiz, target_time__gt=timezone.now(), completion_time__isnull=True).first()
        if ongoing_quiz:
            return Response(response(200, "User has ongoing quiz", {"quiz_session_id": ongoing_quiz.id}), status=status.HTTP_200_OK)

        current_attempt = QuizUser.objects.filter(user=user, quiz=course_quiz).count() + 1
        quiz_user = QuizUser.objects.create(user=user, 
                                            quiz=course_quiz, 
                                            target_time=timezone.now()+timedelta(minutes=course_quiz.duration), 
                                            question_order=";".join([str(num) for num in random.sample(range(1, 11), 10)]),
                                            attempt=current_attempt)
        return Response(response(200, "success", {"quiz_session_id": quiz_user.id}), status=status.HTTP_200_OK)

# Liat pertanyaan quiz per nomor
class UserQuizPerNumberApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_session_id, no, **kwargs):
        user = request.user

        try:
            quiz_user = QuizUser.objects.get(id=quiz_session_id, user=user)
        except QuizUser.DoesNotExist:
            return Response(response(404, "Quiz User not found", None, "Quiz User not found"), status=status.HTTP_404_NOT_FOUND)
        
        if quiz_user.target_time < timezone.now()+timedelta(seconds=15) or quiz_user.completion_time is not None:
            return Response(response(403, "Quiz has ended", None), status=status.HTTP_403_FORBIDDEN)
        
        course_quiz = quiz_user.quiz

        question_order = quiz_user.question_order.split(';')
        question_number = question_order[no-1]

        quiz_question = QuizQuestion.objects.get(course_quiz=course_quiz, ordering=question_number)
        quiz_options = QuizOption.objects.filter(question=quiz_question).order_by('id')
        try:
            user_answer = QuizUserAnswer.objects.get(quiz_user=quiz_user, question=quiz_question)
        except QuizUserAnswer.DoesNotExist:
            user_answer = None

        quiz_question_serializer = QuizQuestionModelSerializer(quiz_question)
        quiz_options_serializer = QuizOptionModelSerializer(quiz_options, many=True)
        if user_answer:
            user_answer_serializer = QuizUserAnswerModelSerializer(user_answer)

        data = {
            'quiz_question' : quiz_question_serializer.data,
            'quiz_options' : quiz_options_serializer.data,
            'user_answer' : user_answer_serializer.data if user_answer != None else None,
            'target_time' : quiz_user.target_time
        }
        
        return Response(response(200, "success", data), status=status.HTTP_200_OK)

# Submit pertanyaan quiz per nomor 
class SubmitQuizPerNumberApiView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(validate_serializer(QuizAnswerDTO))
    def post(self, request, data, **kwargs):
        user = request.user
        try:
            quiz_user = QuizUser.objects.get(id=data['quiz_session_id'], user=user)
        except QuizUser.DoesNotExist:
            return Response(response(404, "Quiz User not found", None, "Quiz User not found"), status=status.HTTP_404_NOT_FOUND)
        
        if quiz_user.target_time < timezone.now()+timedelta(seconds=15) or quiz_user.completion_time is not None:
            return Response(response(403, "Quiz has ended", None), status=status.HTTP_403_FORBIDDEN)

        question = QuizQuestion.objects.get(id=data['question_id'])
        answer = QuizOption.objects.get(id=data['answer_id'])
        
        user_answer, created = QuizUserAnswer.objects.get_or_create(quiz_user=quiz_user, question=question)
        user_answer.answer = answer
        user_answer.save()

        return Response(response(200, "success", None), status=status.HTTP_200_OK)


class FinishQuizApiView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(validate_serializer(SubmitQuizDTO))
    def post(self, request, data, **kwargs):
        user = request.user
        try:
            quiz_user = QuizUser.objects.get(id=data['quiz_session_id'], user=user)
        except QuizUser.DoesNotExist:
            return Response(response(404, "Quiz User not found", None, "Quiz User not found"), status=status.HTTP_404_NOT_FOUND)
        
        if quiz_user.completion_time is None:
            quiz_user.completion_time = timezone.now()
            quiz_user.save()

            answered_questions = QuizUserAnswer.objects.filter(quiz_user=quiz_user)
            correct_answer = 0
        
            for answered_question in answered_questions:
                chosen_option = answered_question.answer
                if chosen_option.is_correct:
                    correct_answer += 1

            quiz_user.correct_answer = correct_answer
            quiz_user.score = Decimal(str(correct_answer * 10) + ".00")

            quiz_user.save()

        return Response(response(200, "success", None), status=status.HTTP_200_OK)


# Liat review quiz, bener & salahnya 
class UserQuizReviewApiView(APIView):
    def get(self, request, **kwargs):
        pass