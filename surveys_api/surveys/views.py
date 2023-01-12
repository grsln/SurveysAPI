from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, Question, SimpleSurvey, SimpleSurveyResult, User
from .serializers import (AnswerSerializer, CustomUserEditSerializer, CustomUserSerializer, QuestionSerializer,
                          ResultSerializer,
                          SimpleSurveyResSerializer, SimpleSurveySerializer)


class ResultView(APIView):
    def get(self, request, pk):
        simple_survey_result = SimpleSurveyResult.objects.filter(pk=pk)
        serializer = ResultSerializer(simple_survey_result, many=True)
        return Response({"simplesurveyresult": serializer.data})


class AnswerView(APIView):
    def get(self, request, pk):
        answer = Answer.objects.filter(pk=pk)
        serializer = AnswerSerializer(answer, many=True)
        return Response({"answer": serializer.data})


class QuestionView(APIView):
    def get(self, request, pk):
        question = Question.objects.filter(pk=pk)
        serializer = QuestionSerializer(question, many=True)
        return Response({"question": serializer.data})


class QuestionAnswersView(APIView):
    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        question_answers = question.answers.all()
        serializer = AnswerSerializer(question_answers, many=True)
        return Response({"question_answers": serializer.data})


class SimpleSurveyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        survey = SimpleSurvey.objects.filter(pk=pk)
        serializer = SimpleSurveySerializer(survey, many=True)
        return Response({"SimpleSurvey": serializer.data})

    def put(self, request, pk):
        saved_survey = get_object_or_404(SimpleSurvey.objects.all(), pk=pk)
        if not saved_survey.status:
            request_survey = request.data.get("SimpleSurvey")
            answers_list = request_survey[0]["simplesurveyresult"]
            for answers_item in answers_list:
                survey_result_item = saved_survey.simple_survey_result_set.get(id=answers_item["id"])
                serializer = ResultSerializer(instance=survey_result_item, data=answers_item, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    survey_result_item.simple_survey_question_answered(answer_id=answers_item["answered_id"])
            saved_survey.status = True
            saved_survey.save()
            survey = SimpleSurvey.objects.get(pk=pk, status=True)
            serializer = SimpleSurveyResSerializer(survey, many=False)
            return Response({"success": "Опрос успешно сохранен", "SimpleSurvey": serializer.data})
        return Response({"error": "Опрос был ранее сохранен"})


class SimpleSurveyResView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        survey = SimpleSurvey.objects.filter(pk=pk, status=True)
        serializer = SimpleSurveyResSerializer(survey, many=True)
        return Response({"SimpleSurvey": serializer.data})


class SimpleSurveyCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        survey = SimpleSurvey.objects.create(simple_survey_date=timezone.now(), status=False)
        serializer = SimpleSurveySerializer(survey, many=False)
        return Response({"SimpleSurvey": serializer.data})


class CustomUserCreate(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format="json"):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                json['id'] = user.pk
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUser(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk, format="json"):
        serializer = CustomUserEditSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format="json"):
        user = self.get_object(pk)
        serializer = CustomUserEditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response({"Message": "Пользователь удален."}, status=status.HTTP_200_OK)
