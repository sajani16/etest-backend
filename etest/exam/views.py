import json
from django.shortcuts import render
import secrets
from django.shortcuts import render
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from exam.models import ExamResult
from exam.serializers import ExamResultSerializer



load_dotenv()
# from .serializers import  question_serializer

# Create your views here.
# @api_view(['POST'])
# def generate_questions(request):
#     serializer = question_serializer(data=request.data)
#     if serializer.is_valid():
#         topic = serializer.validated_data['topic']
#         description= serializer.validated_data['description']
#         serializer.save()
#         return Response({serializer.data})

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # your Gemini AI lib

class GenerateQuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access this view
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            topic = data.get("topic")
            description = data.get("description")
            no_of_questions = data.get("no_of_questions")
            difficulty_level = data.get("difficulty_level")  # Default to medium if not provided

            if not all([topic, description, no_of_questions, difficulty_level is not None]):
                return Response(
                    {"message": "Missing required parameters", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                no_of_questions = int(no_of_questions)
            except ValueError:
                return Response(
                    {"message": "Number of questions must be an integer", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not 1 <= no_of_questions <= 101:
                return Response(
                    {"message": "Number of questions should be between 1 and 100", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                return Response(
                    {"message": "GEMINI_API_KEY not set", "success": False},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")

            prompt = f"""
Generate {no_of_questions}  {difficulty_level} multiple choice questions (MCQs) based on the topic "{topic}".
Use this description for more context: "{description}".

The format MUST be a pure JSON array of objects, where each object has:
- "question": The question text
- "options": A string with 4 options separated by comma character. Do not use any kind of numbering only use comma between texts"
- "answer": The correct option letter exactly one of the 4 options return index of the correct answer in number 1, 2, 3 or 4.

⚠️ Do not include any explanations, code blocks, or markdown.
⚠️ Strictly output only valid JSON — no introductory or trailing text.
"""

            response = model.generate_content(prompt)

            try:
                generated_questions = json.loads(response.text)
            except json.JSONDecodeError:
                return Response(
                    {"message": "Gemini response was not valid JSON.", "raw_output": response.text, "success": False},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response({"questions": generated_questions, "success": True}, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON in request body", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Unexpected error: {str(e)}", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )





class ExamResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Exam result saved successfully"}, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)  

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        results = ExamResult.objects.filter(user=request.user)
        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        