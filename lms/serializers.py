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
        fields = ["batch_id", "batch_number", "course"]

class CourseAssignmentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseAssignment
        fields = ["id", "title", "deadline", "file", "accesibility"]
        
class CourseQuizModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer()

    class Meta:
        model = CourseQuiz
        fields = ["id", "title", "course_batch"]

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

    class Meta:
        model = CourseSession
        fields = ["title", "time", "meeting_link", "record_link", "lesson_link"]

class CourseQuizModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseQuiz
        fields = ["id","title", "duration", "minimum_score", "accessibility", "status", "deadline"]

class QuizUserModelSerializer(serializers.ModelSerializer):
    quiz = CourseQuizModelSerializer()
    class Meta:
        model = QuizUser
        fields = ["id", "quiz","score", "correct_answer", "question_order", "target_time", "completion_time", "is_remedial", "attemp"]

class LastAccessModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer()

    class Meta:
        model = LastAccess
        fields = ["course_batch"]

class QuizDTO(serializers.Serializer):
    id = serializers.IntegerField()
