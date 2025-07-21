# import secrets
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
    def post(self , request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        serializer =    UserProfileSerializer(request.user)
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




