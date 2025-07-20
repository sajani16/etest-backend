from django.urls import  path
from plan.views import PlanRetrieveUpdateView, PlanView

urlpatterns = [
    path('', PlanView.as_view(), name='plan-list-create'),
    path('<int:pk>', PlanRetrieveUpdateView.as_view(), name='plan-retrieve-update'),
]