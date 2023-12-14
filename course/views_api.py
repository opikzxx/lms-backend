from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from library.helper.interface import response
from library.helper.wrapper import validate_serializer

class AllCourseApiView(APIView):
    def get(self, request, **kwargs):
        program_slug = request.GET.get('program')
        availability = request.GET.get('availability')
        limit = request.GET.get('limit')

        if program_slug:
            programs = Program.objects.filter(slug=program_slug)
        else: 
            programs = Program.objects.all()

        program_data = []

        for program in programs:
            courses = Course.objects.filter(program=program)
            if availability:
                courses = courses.filter(status=availability)
            if limit:
                courses = courses[:int(limit)]

            course_serializer = CourseCardModelSerializer(courses, many=True)
            
            program_serializer = ProgramModelSerializer(program)
            data = program_serializer.data
            data['courses'] = course_serializer.data
            program_data.append(data)
        
        return Response(response(200, "success", program_data), status=status.HTTP_200_OK)

class CourseOverviewApiView(APIView):
    def get(self, request, id):
        try:
            data = Course.objects.get(id=id)
            serializer = CourseOverviewModelSerializer(data)
            return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)
        
class AllTeacherApiView(APIView):
    def get(self, request, **kwargs):
        limit = request.GET.get('limit')

        teachers = Teacher.objects.all()
        if limit:
            teachers = teachers[:int(limit)]
            
        serializer = TeacherModelSerializer(teachers, many=True)
        return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)

class CoursePriceApiView(APIView):
    def get(self, request, id):
        try:
            course = Course.objects.filter(id=id).first()
            price = CoursePrice.objects.filter(course_id=course)
            if len(price)>0:
                serializer = CoursePriceModelSerializer(price, many=True)
                return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response(204, "No Data", []), status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)
    
class CourseFaqApiView(APIView):
    def get(self, request, id):
        try:
            course = Course.objects.filter(id=id).first()
            faq = CourseFaq.objects.filter(course_id=course)
            if len(faq)>0:
                serializer = CourseFaqModelSerializer(faq, many=True)
                return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response(204, "No Data", []), status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)

class CourseBatchApiView(APIView):
    def get(self, request, id):
        try:
            course = Course.objects.filter(id=id).first()
            batch = CourseBatch.objects.filter(course_id=course)
            if len(batch)>0:
                serializer = CourseBatchModelSerializer(batch, many=True)
                return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response(204, "No Data", []), status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)

class CourseCurriculumApiView(APIView):
    def get(self, request, id):
        try:
            course = Course.objects.filter(id=id).first()
            curriculum = CourseCurriculum.objects.filter(course_id=course)
            if len(curriculum)>0:
                serializer = CourseCurriculumModelSerializer(curriculum, many=True)
                return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response(204, "No Data", []), status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)

class CourseScheduleApiView(APIView):
    def get(self, request, id):
        try:
            course = Course.objects.filter(id=id).first()
            schedule = CourseSchedule.objects.filter(course_id=course)
            if len(schedule)>0:
                serializer = CourseScheduleModelSerializer(schedule, many=True)
                return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response(204, "No Data", []), status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)

class TeacherDetailApiView(APIView):
    def get(self, request, id):
        try:
            data = Teacher.objects.get(id=id)
            serializer = TeacherModelSerializer(data)
            return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(response(404, "ID Not Found", None, type(e).__name__), status=status.HTTP_404_NOT_FOUND)


class ListTestimonyApiView(APIView):
    def get(self, request, **kwargs):
        testimony = Testimony.objects.all()
        serializer = TestimonyModelSerializer(testimony, many=True)
        return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)
    
class CourseTestimonyApiView(APIView):
    def get(self, request, id, **kwargs):
        testimony = Testimony.objects.filter(course__id=id)
        serializer = TestimonyModelSerializer(testimony, many=True)
        return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)