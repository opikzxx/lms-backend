from rest_framework import serializers
from .models import *
from course.models import Course, Program

class ProgramModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Program
        fields= ["name"]

class CourseModelSerializer(serializers.ModelSerializer):
    program = ProgramModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "description", "image_url", "program"]

class CourseBatchModelSerializer(serializers.ModelSerializer):
    course = CourseModelSerializer()
    batch_id = serializers.IntegerField(source='id')
    batch_number = serializers.IntegerField(source='no')

    class Meta:
        model = CourseBatch
        fields = ["batch_id", "batch_number", "start_date", "end_date", "course"]

class CourseAssignmentModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer()

    class Meta:
        model = CourseAssignment
        fields = ["id", "title", "deadline", "file", "accesibility", "course_batch"]
        
class CardCourseQuizModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer()

    class Meta:
        model = CourseQuiz
        fields = ["id", "title", "course_batch"]

class SimpleUserAssignmentModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = AssignmentAttachment
        fields = ["id", "status", "score", "submitted_date", "feedback", "file"]

    def get_status(self, obj):
        return obj.get_status_display()

class UserAssignmentModelSerializer(serializers.ModelSerializer):
    assignment = CourseAssignmentModelSerializer()
    user_attachment_file = serializers.CharField(source="file")

    class Meta:
        model = AssignmentAttachment
        fields = ["id", "status", "assignment", "score", "submitted_date", "feedback", "user_attachment_file"]

class UserRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ["rating", "rating_detail"]

class CourseSessionModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer()

    class Meta:
        model = CourseSession
        fields = ["title", "time", "meeting_link", "record_link", "lesson_link", "course_batch"]

class CourseQuizModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseQuiz
        fields = ["id","title", "duration", "minimum_score", "accessibility", "status", "deadline"]

class QuizUserModelSerializer(serializers.ModelSerializer):
    # quiz = CourseQuizModelSerializer()
    class Meta:
        model = QuizUser
        fields = ["id", "score", "correct_answer", "question_order", "target_time", "completion_time", "is_remedial", "attempt"]

class LastAccessModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer()

    class Meta:
        model = LastAccess
        fields = ["course_batch"]

class QuizQuestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizQuestion
        fields = ["id", "question", "ordering"]

class QuizOptionModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizOption
        fields = ["id", "value"]

class QuizUserAnswerModelSerializer(serializers.ModelSerializer):
    answer = QuizOptionModelSerializer()

    class Meta:
        model = QuizUserAnswer
        fields = ["id", "answer"]

# --------------------- DTO ---------------------
class QuizDTO(serializers.Serializer):
    quiz_id = serializers.IntegerField()

class QuizAnswerDTO(serializers.Serializer):
    quiz_session_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()

class SubmitQuizDTO(serializers.Serializer):
    quiz_session_id = serializers.IntegerField()

class LastAccessDTO(serializers.Serializer):
    batch_id = serializers.IntegerField()

class EnrollDTO(serializers.Serializer):
    batch_id = serializers.IntegerField()