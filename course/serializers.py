from rest_framework import serializers
from .models import *

class CoursePriceModelSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    
    class Meta:
        model= CoursePrice
        fields= ["type","original_price","discounted_price","discount_percentage"]

    def get_type(self, obj):
        return obj.get_type_display()

class CourseOverviewModelSerializer(serializers.ModelSerializer):
    courseprice = CoursePriceModelSerializer(source='courseprice_set', many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model= Course
        fields= ["id","name","description","image_url","status","courseprice", "participant_amount", "certified_participant_amount"]

    def get_status(self, obj):
        return obj.get_status_display()

class ProgramModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Program
        fields= ["id","name"]

class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Teacher
        fields= ["id","name","occupation", "experience", "profileImageUrl", "companyImageUrl", "linkedinUrl"]

class ContentApiSerializer(serializers.ModelSerializer):
    class Meta:
        model= CourseContent
        fields= ["id","course","content_type","description"]

class CourseCurriculumModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCurriculum
        fields= ["title","detail","file"]

class CourseStudyMethodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStudyMethod
        fields = ["title","detail","image_url"]

class CourseBatchModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseBatch
        fields = ["open_date","close_date","start_date","status"]

    def get_status(self, obj):
        return obj.get_status_display()

class CourseFaqModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFaq
        fields= ["question","answer"]

class CourseScheduleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = ["starting_week", "ending_week", "title", "description"]

class TestimonyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimony
        fields = ["name", "occupation", "desciption", "image_url"]

class IDSerializer(serializers.Serializer):
    id = serializers.UUIDField()