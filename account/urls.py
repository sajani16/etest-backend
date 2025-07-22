from django.urls import include, path
from account.views import SignupView, UserProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    # path('signup', signup),
    # path('login',login),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup', SignupView.as_view(), name='signup'),
    path('profile', UserProfileView.as_view(), name ='profile')
]