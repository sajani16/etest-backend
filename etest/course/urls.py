from django.urls import  path
from course.views import CourseView

urlpatterns = [
    path('', CourseView.as_view(), name='course-list-create'),
    # path('<int:pk>', PlanRetrieveUpdateView.as_view(), name='plan-retrieve-update'),
]