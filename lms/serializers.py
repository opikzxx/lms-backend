from rest_framework import serializers
from .models import *
from course.models import Course, Program

class ProgramModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Program
        fields= ["name"]

class CourseModelSerializer(serializers.ModelSerializer):
    program = ProgramModelSerializer(source='program_set')

    class Meta:
        model = Course
        fields = ["id", "name", "description", "image_url", "program"]

class CourseBatchModelSerializer(serializers.ModelSerializer):
    course = CourseModelSerializer(source='course_set')

    class Meta:
        model = CourseBatch
        fields = ["id", "no", "course"]

class CourseAssignmentModelSerializer(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer(source='course_batch_set')

    class Meta:
        model = CourseAssignment
        fields = ["id", "title", "deadline", "course_batch"]

class CourseAssignmentForList(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer(source='course_batch_set')

    class Meta:
        model = CourseAssignment
        fields = ["id", "title", "deadline", "course_batch"]

class CourseQuizForList(serializers.ModelSerializer):
    course_batch = CourseBatchModelSerializer(source='course_batch_set')

    class Meta:
        model = CourseQuiz
        fields = ["id", "title", "course_batch"]

class UserAssignmentModelSerializer(serializers.ModelSerializer):
    assignment = CourseAssignmentForList(source='assignment_set')

    class Meta:
        model = AssignmentAttachment
        fields = ["id", "status", "assignment"]


