from rest_framework import serializers
from .models import *

class CoursePriceModelSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    
    class Meta:
        model= CoursePrice
        fields= ["type","original_price","discounted_price","discount_percentage", "description","benefits"]

    def get_type(self, obj):
        return obj.get_type_display()

class CourseCurriculumModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCurriculum
        fields= ["title","detail"]

class CourseScheduleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = ["starting_week", "ending_week", "title", "description"]

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
        
class CourseDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields= ["course_overview","reason","result","skill"]

class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Teacher
        fields= ["id","name","occupation", "experience", "profileImageUrl", "companyImageUrl", "linkedinUrl"]
     
class CourseOverviewModelSerializer(serializers.ModelSerializer):
    course_detail = CourseDetailModelSerializer(source='coursedetail')
    course_price = CoursePriceModelSerializer(source='courseprice_set', many=True)
    course_curriculum = CourseCurriculumModelSerializer(source='coursecurriculum_set', many=True)
    course_schedule = CourseScheduleModelSerializer(source='courseschedule_set', many=True)
    course_batch = CourseBatchModelSerializer(source='coursebatch_set', many=True)
    course_faq = CourseFaqModelSerializer(source='coursefaq_set', many=True)
    teacher = TeacherModelSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model= Course
        fields= [
            "id","name","description","image_url","status",
            "course_detail",
            "course_price", 
            "course_curriculum",
            "course_schedule",
            "course_batch",
            "course_faq",
            "participant_amount", "certified_participant_amount", "teacher"
        ]

    def get_status(self, obj):
        return obj.get_status_display()
    
class CourseCardModelSerializer(serializers.ModelSerializer):
    course_price = CoursePriceModelSerializer(source='courseprice_set', many=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
            model= Course
            fields= ["id","name","description","image_url", "course_price","status"]
            
    def get_status(self, obj):
        return obj.get_status_display()

class ProgramModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Program
        fields= ["id","name"]


class TestimonyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimony
        fields = ["name", "occupation", "desciption", "image_url"]

class IDSerializer(serializers.Serializer):
    id = serializers.UUIDField()