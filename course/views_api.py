from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .interface import response

class ListCourseApiView(APIView):
    def get(self, request, **kwargs):
        program_id = request.GET.get('program_id')
        availability = request.GET.get('availability')
        limit = request.GET.get('limit')

        if program_id:
            programs = Program.objects.filter(id=program_id)
        else: 
            programs = Program.objects.all()

        program_data = []

        for program in programs:
            courses = Course.objects.filter(program=program)
            if availability:
                courses = courses.filter(status=availability)
            if limit:
                courses = courses[:int(limit)]

            course_serializer = CourseOverviewModelSerializer(courses, many=True)
            
            program_serializer = ProgramModelSerializer(program)
            data = program_serializer.data
            data['courses'] = course_serializer.data
            program_data.append(data)
        
        return Response(response(200, "success", program_data), status=status.HTTP_200_OK)

class ListTeacherApiView(APIView):
    def get(self, request, **kwargs):
        limit = request.GET.get('limit')

        teachers = Teacher.objects.all()
        if limit:
            teachers = teachers[:int(limit)]
            
        serializer = TeacherApiSerializer(teachers, many=True)
        return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)

class ListContentApiView(APIView):
    def get(self, request, **kwargs):
        data = CourseContent.objects.all().order_by('name')
        serializer = ContentApiSerializer(data, many=True)
        if len(serializer.data) == 0 :
            data = {
                'status': True,
                'response': []
            }
        else:
            data = {
                'status': True,
                'response': serializer.data
            }
        return Response(data, status=status.HTTP_200_OK)

class ListCoursePriceApiView(APIView):
    def get(self, request, id):
        data = Course.objects.filter(id=id).first()
        test = CoursePrice.objects.filter(course_id=data)
        serializer = CoursePriceModelSerializer(test, many=True)
        return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)
    
class ListCourseFaqApiView(APIView):
    def get(self, request, id):
        data = Course.objects.filter(id=id).first()
        test = CourseFaq.objects.filter(course_id=data)
        if len(test)>0:
            serializer = CourseFaqModelSerializer(test, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "doesn't exist", "data":None}, status=status.HTTP_204_NO_CONTENT)

class ListCourseStudyMethodApiView(APIView):
    def get(self, request, id):
        data = Course.objects.filter(id=id).first()
        test = CourseStudyMethod.objects.filter(course=data)
        if len(test)>0:
            serializer = CourseStudyMethodModelSerializer(test, many=True)
            return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "doesn't exist", "data":None}, status=status.HTTP_204_NO_CONTENT)

class ListCourseBatchApiView(APIView):
    def get(self, request, id):
        data = Course.objects.filter(id=id).first()
        test = CourseBatch.objects.filter(course=data)
        if len(test)>0:
            serializer = CourseBatchModelSerializer(test, many=True)
            return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "doesn't exist", "data":None}, status=status.HTTP_204_NO_CONTENT)

class ListCourseCurriculumApiView(APIView):
    def get(self, request, id):
        data = Course.objects.filter(id=id).first()
        test = CourseCurriculum.objects.filter(course_id=data)
        if len(test)>0:
            serializer = CourseCurriculumModelSerializer(test, many=True)
            return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "doesn't exist", "data":None}, status=status.HTTP_204_NO_CONTENT)
    
class ListCourseScheduleApiView(APIView):
    def get(self, request, id):
        data = Course.objects.filter(id=id).first()
        test = CourseSchedule.objects.filter(course_id=data)
        if len(test)>0:
            serializer = CourseScheduleModelSerializer(test, many=True)
            return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "doesn't exist", "data":None}, status=status.HTTP_204_NO_CONTENT)

class ListDetailTeacherApiView(APIView):
    def get(self, request, id):
        try:
            data = Teacher.objects.get(id=id)
            if id:
                serializer = TeacherApiSerializer(data)
                return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            raise Http404

class ListDetailCourseApiView(APIView):
    def get(self, request, id):
        try:
            data = Course.objects.get(id=id)
            if id:
                serializer = CourseOverviewModelSerializer(data, many=True)
                return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            raise Http404

class ListDetailContentApiView(APIView):
    def get(self, request, id):
        try:
            data = CourseContent.objects.get(id=id)
            if id:
                serializer = ContentApiSerializer(data)
                return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except CourseContent.DoesNotExist:
            raise Http404

class ListTestimonyApiView(APIView):
    def get(self, request, **kwargs):
        limit = request.GET.get('limit')
        testimony = Testimony.objects.all()[:limit]
        serializer = TestimonyModelSerializer(testimony, many=True)
        return Response(response(200, "success", serializer.data), status=status.HTTP_200_OK)