# import secrets
import random
from account.models import CustomUser
from rest_framework.views import APIView
from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
# from account.models import UserToken
from .serializers import  SignupSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny

# Create your views here.
# @api_view(['POST'])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         user =serializer.save()
#         token = secrets.token_hex(32)
#         UserToken.objects.create(user=user , token = token)
#         return Response({"message": "User created successfully", "token": token}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
         
#         user = authenticate(username=username,password=password)

#         if user:
#            token = secrets.token_hex(32)
#            UserToken.objects.update_or_create(user=user , defaults={"token":token}) 
#            return Response({
#             "message": "Login successful",
#             "token": token,
#             "success": True
#         }, status=status.HTTP_200_OK)
#         return Response({
#         "error": "Invalid credentials",
#         "success": False
#     }, status=status.HTTP_401_UNAUTHORIZED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self , request):
        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            otp = str(random.randint(100000, 999999))
            user.otp_code = otp
            user.save()

            subject = f"VedantaQ OTP Verification"
            text_content = f"Your OTP for VedantaQ signup is: {otp}"
            html_content = f"<p>Your <strong>OTP</strong> for VedantaQ signup is: <strong>{otp}</strong></p>"
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "OTP sent to email","user_id":user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserProfileSerializer(request.user , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST )
    
    def delete(self , request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class VerifyOTPView(APIView):
    def post (self,request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.otp_code == otp:
            user.is_Active = True
            user.otp_code = ''
            user.save()
            return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            
