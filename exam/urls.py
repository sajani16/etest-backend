from django.urls import  path

from exam.views import ExamResultView, GenerateQuestionsAPIView


urlpatterns = [
    path('generate-questions',GenerateQuestionsAPIView.as_view(), name='generate-questions'),
    path('results', ExamResultView.as_view(), name='exam-results'),

]