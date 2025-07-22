from rest_framework import serializers
from exam.models import ExamResult

# class question_serializer(serializers.ModelSerializer):
#     topic = serializers.CharField()
#     descriptions = serializers.CharField() 

#     class Meta:
#         model = Question
#         fields = ["topic","description"]


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['id', 'user', 'score', 'total_questions', 'topic', 'exam_date', 'details']
        read_only_fields = ['user', 'exam_date']