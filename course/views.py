
from rest_framework.views import APIView
from rest_framework.response import Response
from course.serializers import CourseSerializer
from course.models import Course
from rest_framework import status
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class CourseView(APIView):
    def get(self,request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# class PlanView(generics.ListCreateAPIView):
#     queryset = Plan.objects.all()
#     serializer_class = PlanSerializer
#     # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access this view
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['title']

# class PlanRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Plan.objects.all()
#     serializer_class = PlanSerializer